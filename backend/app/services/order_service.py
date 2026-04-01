"""Order service — US-C06, US-C07, US-O02~O05, US-O08, US-M02, US-M04."""

from datetime import date, datetime, timezone
from typing import List, Optional

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.event_bus import EventBus, SSEEvent
from app.core.exceptions import (
    InvalidStatusTransitionException,
    MenuNotFoundException,
    OrderNotFoundException,
    SessionNotFoundException,
    ValidationException,
)
from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.menu_repo import MenuRepository
from app.repositories.order_history_repo import OrderHistoryRepository
from app.repositories.order_item_repo import OrderItemRepository
from app.repositories.order_repo import OrderRepository
from app.repositories.session_repo import SessionRepository
from app.schemas.order import OrderCreate, OrderHistoryResponse, OrderResponse

logger = structlog.get_logger()

VALID_TRANSITIONS = {
    "pending": "preparing",
    "preparing": "completed",
}


class OrderService:
    def __init__(self, db: AsyncSession, event_bus: EventBus):
        self.order_repo = OrderRepository(db)
        self.item_repo = OrderItemRepository(db)
        self.menu_repo = MenuRepository(db)
        self.session_repo = SessionRepository(db)
        self.history_repo = OrderHistoryRepository(db)
        self.event_bus = event_bus
        self.db = db

    async def create_order(
        self, store_id: int, table_id: int, session_id: int, data: OrderCreate
    ) -> Order:
        # Verify session
        session = await self.session_repo.get_active(table_id)
        if not session or session.id != session_id:
            raise SessionNotFoundException("활성 세션이 없습니다.")

        # Validate menus and build items
        items = []
        total = 0
        for item_data in data.items:
            menu = await self.menu_repo.get_by_id(store_id, item_data.menu_id)
            if not menu:
                raise MenuNotFoundException(details={"menu_id": item_data.menu_id})
            subtotal = menu.price * item_data.quantity
            items.append(OrderItem(
                menu_id=menu.id,
                menu_name=menu.name,
                quantity=item_data.quantity,
                unit_price=menu.price,
                subtotal=subtotal,
            ))
            total += subtotal

        # Generate order number
        today = date.today()
        order_no = await self.order_repo.get_next_order_no(store_id, today)

        # Create order
        order = Order(
            store_id=store_id,
            table_id=table_id,
            session_id=session_id,
            order_no=order_no,
            total_amount=total,
            status="pending",
        )
        order = await self.order_repo.create(order)

        for item in items:
            item.order_id = order.id
        await self.item_repo.bulk_create(items)
        await self.db.commit()
        await self.db.refresh(order)

        # SSE event
        await self.event_bus.publish(SSEEvent(
            type="order_created",
            data={
                "id": order.id, "order_no": order.order_no, "table_id": table_id,
                "items": [{"menu_name": i.menu_name, "quantity": i.quantity,
                           "unit_price": i.unit_price, "subtotal": i.subtotal} for i in items],
                "total_amount": total, "status": "pending",
            },
            store_id=store_id,
            table_id=table_id,
        ))

        logger.info("order_created", store_id=store_id, order_id=order.id, order_no=order_no)
        return order

    async def get_orders_by_session(self, session_id: int) -> List[Order]:
        return await self.order_repo.get_by_session(session_id)

    async def get_orders_by_store(self, store_id: int) -> List[Order]:
        return await self.order_repo.get_by_store_active(store_id)

    async def get_order(self, store_id: int, order_id: int) -> Order:
        order = await self.order_repo.get_by_id(store_id, order_id)
        if not order:
            raise OrderNotFoundException()
        return order

    async def update_status(self, store_id: int, order_id: int, new_status: str) -> Order:
        order = await self.order_repo.get_by_id(store_id, order_id)
        if not order:
            raise OrderNotFoundException()

        expected_next = VALID_TRANSITIONS.get(order.status)
        if expected_next != new_status:
            raise InvalidStatusTransitionException(
                details={"current": order.status, "requested": new_status}
            )

        old_status = order.status
        order.status = new_status
        order.updated_at = datetime.now(timezone.utc)
        await self.db.commit()

        await self.event_bus.publish(SSEEvent(
            type="order_status_changed",
            data={"order_id": order.id, "old_status": old_status, "new_status": new_status},
            store_id=store_id,
            table_id=order.table_id,
        ))

        logger.info("order_status_changed", order_id=order_id, old=old_status, new=new_status)
        return order

    async def delete_order(self, store_id: int, order_id: int) -> None:
        order = await self.order_repo.get_by_id(store_id, order_id)
        if not order:
            raise OrderNotFoundException()
        await self.order_repo.soft_delete(order)
        await self.db.commit()

        await self.event_bus.publish(SSEEvent(
            type="order_deleted",
            data={"order_id": order.id, "table_id": order.table_id},
            store_id=store_id,
            table_id=order.table_id,
        ))
        logger.info("order_deleted", order_id=order_id)

    async def get_order_history(
        self, store_id: int, table_id: int,
        date_from: Optional[date] = None, date_to: Optional[date] = None,
    ) -> list:
        return await self.history_repo.get_by_table(store_id, table_id, date_from, date_to)
