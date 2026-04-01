"""Table service — US-O06, US-O07, US-M03."""

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
from app.models.order_history import OrderHistory
from app.models.table import Table
from app.models.table_session import TableSession
from app.repositories.order_history_repo import OrderHistoryRepository
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
        self.history_repo = OrderHistoryRepository(db)
        self.event_bus = event_bus
        self.db = db

    async def setup_table(self, store_id: int, table_no: int, password: str) -> TableSetupResponse:
        existing = await self.table_repo.get_by_store_and_no(store_id, table_no)
        if existing:
            raise DuplicateTableException()

        table = Table(store_id=store_id, table_no=table_no, password_hash=hash_password(password))
        table = await self.table_repo.create(table)

        session = TableSession(store_id=store_id, table_id=table.id)
        session = await self.session_repo.create(session)
        await self.db.commit()

        logger.info("table_setup", store_id=store_id, table_no=table_no)
        return TableSetupResponse(
            table=TableResponse.model_validate(table),
            session=SessionResponse.model_validate(session),
        )

    async def get_tables(self, store_id: int) -> List[Table]:
        return await self.table_repo.get_by_store(store_id)

    async def end_session(
        self, store_id: int, table_id: int, force: bool = False
    ) -> SessionEndResponse:
        table = await self.table_repo.get_by_id(store_id, table_id)
        if not table:
            raise TableNotFoundException()

        active_session = await self.session_repo.get_active(table_id)
        if not active_session:
            raise SessionNotFoundException()

        # Check pending orders
        if not force:
            pending = await self.order_repo.get_pending_by_session(active_session.id)
            if pending:
                raise PendingOrdersException(
                    message=f"미완료 주문 {len(pending)}건이 존재합니다.",
                    details={"pending_count": len(pending), "pending_order_ids": [o.id for o in pending]},
                )

        # Archive orders
        orders = await self.order_repo.get_by_session(active_session.id)
        histories = []
        for order in orders:
            history = OrderHistory(
                store_id=store_id,
                table_id=table_id,
                session_id=active_session.id,
                original_order_id=order.id,
                order_no=order.order_no,
                order_data={
                    "items": [
                        {"menu_name": item.menu_name, "quantity": item.quantity,
                         "unit_price": item.unit_price, "subtotal": item.subtotal}
                        for item in order.items
                    ]
                },
                total_amount=order.total_amount,
                status=order.status,
                ordered_at=order.created_at,
            )
            histories.append(history)
            await self.order_repo.soft_delete(order)

        if histories:
            await self.history_repo.bulk_create(histories)

        # End session, create new
        old_session = await self.session_repo.deactivate(active_session)
        new_session = TableSession(store_id=store_id, table_id=table_id)
        new_session = await self.session_repo.create(new_session)
        await self.db.commit()

        # SSE event
        await self.event_bus.publish(SSEEvent(
            type="session_ended",
            data={"table_id": table_id, "session_id": old_session.id},
            store_id=store_id,
            table_id=table_id,
        ))

        logger.info("session_ended", store_id=store_id, table_id=table_id, archived=len(histories))
        return SessionEndResponse(
            old_session=SessionResponse.model_validate(old_session),
            new_session=SessionResponse.model_validate(new_session),
            archived_orders=len(histories),
        )
