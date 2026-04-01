"""Table service — synced with Unit 1."""

from typing import List

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.event_bus import EventBus, SSEEvent
from app.core.exceptions import (
    DuplicateTableException,
    PendingOrdersException,
    SessionNotFoundException,
    TableNotFoundException,
)
from app.core.security import hash_password
from app.models.table import RestaurantTable
from app.models.table_session import TableSession
from app.repositories.order_repo import OrderRepository
from app.repositories.session_repo import SessionRepository
from app.repositories.table_repo import TableRepository
from app.schemas.table import SessionEndResponse, SessionResponse, TableResponse, TableSetupResponse

logger = structlog.get_logger()


class TableService:
    def __init__(self, db: AsyncSession, event_bus: EventBus):
        self.table_repo = TableRepository(db)
        self.session_repo = SessionRepository(db)
        self.order_repo = OrderRepository(db)
        self.event_bus = event_bus
        self.db = db

    async def setup_table(self, store_code: str, table_no: int, password: str) -> TableSetupResponse:
        existing = await self.table_repo.get_by_pk(store_code, table_no)
        if existing:
            raise DuplicateTableException()

        table = RestaurantTable(store_code=store_code, table_no=table_no, password_hash=hash_password(password))
        table = await self.table_repo.create(table)

        session = TableSession(store_code=store_code, table_no=table_no)
        session = await self.session_repo.create(session)
        await self.db.commit()

        logger.info("table_setup", store_code=store_code, table_no=table_no)
        return TableSetupResponse(
            table=TableResponse.model_validate(table),
            session=SessionResponse.model_validate(session),
        )

    async def get_tables(self, store_code: str) -> List[RestaurantTable]:
        return await self.table_repo.get_by_store(store_code)

    async def end_session(
        self, store_code: str, table_no: int, force: bool = False,
    ) -> SessionEndResponse:
        table = await self.table_repo.get_by_pk(store_code, table_no)
        if not table:
            raise TableNotFoundException()

        active_session = await self.session_repo.get_active(store_code, table_no)
        if not active_session:
            raise SessionNotFoundException()

        if not force:
            pending = await self.order_repo.get_pending_by_session(active_session.id)
            if pending:
                raise PendingOrdersException(
                    message=f"미완료 주문 {len(pending)}건이 존재합니다.",
                    details={"pending_count": len(pending)},
                )

        # Archive orders
        orders = await self.order_repo.get_by_session(active_session.id)
        for order in orders:
            await self.order_repo.archive(order)

        old_session = await self.session_repo.deactivate(active_session)
        new_session = TableSession(store_code=store_code, table_no=table_no)
        new_session = await self.session_repo.create(new_session)
        await self.db.commit()

        await self.event_bus.publish(SSEEvent(
            type="session_ended",
            data={"table_no": table_no, "session_id": old_session.id},
            store_code=store_code,
            table_no=table_no,
        ))

        logger.info("session_ended", store_code=store_code, table_no=table_no, archived=len(orders))
        return SessionEndResponse(
            old_session=SessionResponse.model_validate(old_session),
            new_session=SessionResponse.model_validate(new_session),
            archived_orders=len(orders),
        )
