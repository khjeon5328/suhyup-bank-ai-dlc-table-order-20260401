"""Order service — synced with Unit 1."""

from datetime import datetime
from typing import List, Optional

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.event_bus import EventBus, SSEEvent
from app.core.exceptions import (
    InvalidStatusTransitionException,
    MenuNotFoundException,
    OrderNotFoundException,
    SessionNotFoundException,
)
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.repositories.menu_repo import MenuRepository
from app.repositories.order_repo import OrderRepository
from app.repositories.session_repo import SessionRepository
from app.schemas.order import OrderCreate

logger = structlog.get_logger()

VALID_TRANSITIONS = {
    OrderStatus.PENDING: OrderStatus.PREPARING,
    OrderStatus.PREPARING: OrderStatus.COMPLETED,
}


class OrderService:
    def __init__(self, db: AsyncSession, event_bus: EventBus):
        self.order_repo = OrderRepository(db)
        self.menu_repo = MenuRepository(db)
        self.session_repo = SessionRepository(db)
        self.event_bus = event_bus
        self.db = db

    async def create_order(
        self, store_code: str, table_no: int, session_id: int, data: OrderCreate,
    ) -> Order:
        session = await self.session_repo.get_active(store_code, table_no)
        if not session or session.id != session_id:
            raise SessionNotFoundException("활성 세션이 없습니다.")

        items = []
        total = 0
        for item_data in data.items:
            menu = await self.menu_repo.get_by_id(store_code, item_data.menu_id)
            if not menu:
                raise MenuNotFoundException(details={"menu_id": item_data.menu_id})
            subtotal = menu.price * item_data.quantity
            items.append(OrderItem(
                menu_id=menu.id, menu_name=menu.name,
                quantity=item_data.quantity, unit_price=menu.price, subtotal=subtotal,
            ))
            total += subtotal

        order = Order(
            store_code=store_code, table_no=table_no, session_id=session_id, total_amount=total,
        )
        order = await self.order_repo.create(order)
        for item in items:
            item.order_id = order.id
        self.db.add_all(items)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(order)

        await self.event_bus.publish(SSEEvent(
            type="order_created",
            data={
                "id": order.id, "table_no": table_no,
                "items": [{"menu_name": i.menu_name, "quantity": i.quantity,
                           "unit_price": i.unit_price, "subtotal": i.subtotal} for i in items],
                "total_amount": total, "status": "pending",
            },
            store_code=store_code, table_no=table_no,
        ))
        logger.info("order_created", store_code=store_code, order_id=order.id)
        return order

    async def get_orders_by_session(self, session_id: int) -> List[Order]:
        return await self.order_repo.get_by_session(session_id)

    async def get_orders_by_store(self, store_code: str) -> List[Order]:
        return await self.order_repo.get_by_store_active(store_code)

    async def get_order(self, store_code: str, order_id: int) -> Order:
        order = await self.order_repo.get_by_id(store_code, order_id)
        if not order:
            raise OrderNotFoundException()
        return order

    async def update_status(self, store_code: str, order_id: int, new_status: str) -> Order:
        order = await self.order_repo.get_by_id(store_code, order_id)
        if not order:
            raise OrderNotFoundException()

        new_enum = OrderStatus(new_status)
        expected = VALID_TRANSITIONS.get(order.status)
        if expected != new_enum:
            raise InvalidStatusTransitionException(
                details={"current": order.status.value, "requested": new_status}
            )

        old_status = order.status.value
        order.status = new_enum
        await self.db.commit()

        await self.event_bus.publish(SSEEvent(
            type="order_status_changed",
            data={"order_id": order.id, "old_status": old_status, "new_status": new_status},
            store_code=store_code, table_no=order.table_no,
        ))
        logger.info("order_status_changed", order_id=order_id, old=old_status, new=new_status)
        return order

    async def delete_order(self, store_code: str, order_id: int) -> None:
        order = await self.order_repo.get_by_id(store_code, order_id)
        if not order:
            raise OrderNotFoundException()
        await self.order_repo.archive(order)
        await self.db.commit()

        await self.event_bus.publish(SSEEvent(
            type="order_deleted",
            data={"order_id": order.id, "table_no": order.table_no},
            store_code=store_code, table_no=order.table_no,
        ))
        logger.info("order_deleted", order_id=order_id)
