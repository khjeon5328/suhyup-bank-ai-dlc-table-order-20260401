"""Order repository — synced with Unit 1."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
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

    async def get_by_id(self, store_code: str, order_id: int) -> Optional[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id, Order.store_code == store_code, Order.archived_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_by_session(self, session_id: int) -> List[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.session_id == session_id, Order.archived_at.is_(None))
            .order_by(Order.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_store_active(self, store_code: str) -> List[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.store_code == store_code, Order.archived_at.is_(None))
            .order_by(Order.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_pending_by_session(self, session_id: int) -> List[Order]:
        result = await self.db.execute(
            select(Order)
            .options(selectinload(Order.items))
            .where(
                Order.session_id == session_id,
                Order.archived_at.is_(None),
                Order.status.in_(["pending", "preparing"]),
            )
        )
        return list(result.scalars().all())

    async def archive(self, order: Order) -> Order:
        order.archived_at = datetime.utcnow()
        await self.db.flush()
        return order
