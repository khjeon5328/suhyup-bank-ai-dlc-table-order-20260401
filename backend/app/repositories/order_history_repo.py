"""OrderHistory repository."""

from datetime import date
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order_history import OrderHistory


class OrderHistoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def bulk_create(self, histories: List[OrderHistory]) -> List[OrderHistory]:
        self.db.add_all(histories)
        await self.db.flush()
        return histories

    async def get_by_table(
        self,
        store_id: int,
        table_id: int,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> List[OrderHistory]:
        stmt = select(OrderHistory).where(
            OrderHistory.store_id == store_id,
            OrderHistory.table_id == table_id,
        )
        if date_from:
            stmt = stmt.where(OrderHistory.ordered_at >= date_from)
        if date_to:
            stmt = stmt.where(OrderHistory.ordered_at <= date_to)
        stmt = stmt.order_by(OrderHistory.ordered_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
