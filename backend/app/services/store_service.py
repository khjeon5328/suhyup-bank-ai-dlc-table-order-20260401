"""Store service."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import StoreNotFoundException
from app.models.store import Store
from app.repositories.store_repo import StoreRepository


class StoreService:
    def __init__(self, db: AsyncSession):
        self.store_repo = StoreRepository(db)

    async def get_store(self, store_id: int) -> Store:
        store = await self.store_repo.get_by_id(store_id)
        if not store:
            raise StoreNotFoundException()
        return store
