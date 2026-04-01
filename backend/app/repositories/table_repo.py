"""Table repository."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.table import Table


class TableRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, table: Table) -> Table:
        self.db.add(table)
        await self.db.flush()
        await self.db.refresh(table)
        return table

    async def get_by_id(self, store_id: int, table_id: int) -> Optional[Table]:
        result = await self.db.execute(
            select(Table).where(Table.id == table_id, Table.store_id == store_id, Table.is_active == True)
        )
        return result.scalar_one_or_none()

    async def get_by_store_and_no(self, store_id: int, table_no: int) -> Optional[Table]:
        result = await self.db.execute(
            select(Table).where(Table.store_id == store_id, Table.table_no == table_no, Table.is_active == True)
        )
        return result.scalar_one_or_none()

    async def get_by_store(self, store_id: int) -> List[Table]:
        result = await self.db.execute(
            select(Table).where(Table.store_id == store_id, Table.is_active == True).order_by(Table.table_no)
        )
        return list(result.scalars().all())
