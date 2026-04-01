"""OrderItem repository."""

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order_item import OrderItem


class OrderItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def bulk_create(self, items: List[OrderItem]) -> List[OrderItem]:
        self.db.add_all(items)
        await self.db.flush()
        for item in items:
            await self.db.refresh(item)
        return items

    async def get_by_order(self, order_id: int) -> List[OrderItem]:
        result = await self.db.execute(
            select(OrderItem).where(OrderItem.order_id == order_id)
        )
        return list(result.scalars().all())
