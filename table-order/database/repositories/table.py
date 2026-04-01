"""RestaurantTable repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.table import RestaurantTable
from .base import BaseRepository


class TableRepository(BaseRepository[RestaurantTable]):
    """Repository for RestaurantTable entity."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RestaurantTable)

    async def get_by_table_no(
        self, store_code: str, table_no: int
    ) -> RestaurantTable | None:
        """Get table by store_code and table_no."""
        return await self.get_by_id((store_code, table_no))

    async def get_tables_by_store(self, store_code: str) -> list[RestaurantTable]:
        """Get all tables for a store."""
        stmt = (
            select(RestaurantTable)
            .where(RestaurantTable.store_code == store_code)
            .order_by(RestaurantTable.table_no)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
