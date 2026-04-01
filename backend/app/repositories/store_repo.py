"""Store repository."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import Store


class StoreRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, store_id: int) -> Optional[Store]:
        result = await self.db.execute(select(Store).where(Store.id == store_id, Store.is_active == True))
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Optional[Store]:
        result = await self.db.execute(select(Store).where(Store.code == code, Store.is_active == True))
        return result.scalar_one_or_none()
