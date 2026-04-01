"""Table repository — synced with Unit 1 (composite PK)."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.table import RestaurantTable


class TableRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, table: RestaurantTable) -> RestaurantTable:
        self.db.add(table)
        await self.db.flush()
        await self.db.refresh(table)
        return table

    async def get_by_pk(self, store_code: str, table_no: int) -> Optional[RestaurantTable]:
        result = await self.db.execute(
            select(RestaurantTable).where(
                RestaurantTable.store_code == store_code,
                RestaurantTable.table_no == table_no,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_store(self, store_code: str) -> List[RestaurantTable]:
        result = await self.db.execute(
            select(RestaurantTable)
            .where(RestaurantTable.store_code == store_code)
            .order_by(RestaurantTable.table_no)
        )
        return list(result.scalars().all())
