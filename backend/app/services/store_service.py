"""Store service — synced with Unit 1."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import StoreNotFoundException
from app.models.store import Store
from app.repositories.store_repo import StoreRepository


class StoreService:
    def __init__(self, db: AsyncSession):
        self.store_repo = StoreRepository(db)

    async def get_store(self, store_code: str) -> Store:
        store = await self.store_repo.get_by_code(store_code)
        if not store:
            raise StoreNotFoundException()
        return store
