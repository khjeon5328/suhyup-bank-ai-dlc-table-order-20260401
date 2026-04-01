"""Order repository."""

from datetime import date, datetime, timezone
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, order: Order) -> Order:
        self.db.add(order)
        await self.db.flush()
        await self.db.refresh(order)
        return order

    async def get_by_id(self, store_id: int, order_id: int) -> Optional[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id, Order.store_id == store_id, Order.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def get_by_session(self, session_id: int) -> List[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.session_id == session_id, Order.is_deleted == False)
            .order_by(Order.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_store_active(self, store_id: int) -> List[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.store_id == store_id, Order.is_deleted == False)
            .order_by(Order.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_next_order_no(self, store_id: int, today: date) -> str:
        result = await self.db.execute(
            select(func.count()).where(
                Order.store_id == store_id,
                func.date(Order.created_at) == today,
            )
        )
        count = result.scalar_one()
        return str(count + 1).zfill(3)

    async def get_pending_by_session(self, session_id: int) -> List[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(
                Order.session_id == session_id,
                Order.is_deleted == False,
                Order.status.in_(["pending", "preparing"]),
            )
        )
        return list(result.scalars().all())

    async def soft_delete(self, order: Order) -> Order:
        order.is_deleted = True
        order.deleted_at = datetime.now(timezone.utc)
        await self.db.flush()
        return order
