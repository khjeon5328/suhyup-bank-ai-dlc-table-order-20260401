"""Store repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.store import Store
from .base import BaseRepository


class StoreRepository(BaseRepository[Store]):
    """Repository for Store entity."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Store)

    async def get_by_code(self, store_code: str) -> Store | None:
        """Get store by store_code."""
        return await self.get_by_id(store_code)

    async def get_all_stores(self) -> list[Store]:
        """Get all stores."""
        stmt = select(Store).order_by(Store.store_code)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
