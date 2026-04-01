"""Store repository — synced with Unit 1."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import Store


class StoreRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_code(self, store_code: str) -> Optional[Store]:
        result = await self.db.execute(
            select(Store).where(Store.store_code == store_code)
        )
        return result.scalar_one_or_none()
