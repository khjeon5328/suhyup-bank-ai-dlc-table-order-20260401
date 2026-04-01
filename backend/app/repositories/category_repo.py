"""Category repository — synced with Unit 1."""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.models.menu import Menu


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, category: Category) -> Category:
        self.db.add(category)
        await self.db.flush()
        await self.db.refresh(category)
        return category

    async def get_by_id(self, store_code: str, category_id: int) -> Optional[Category]:
        result = await self.db.execute(
            select(Category).where(Category.id == category_id, Category.store_code == store_code)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, store_code: str, name: str) -> Optional[Category]:
        result = await self.db.execute(
            select(Category).where(Category.store_code == store_code, Category.name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_store(self, store_code: str) -> List[Category]:
        result = await self.db.execute(
            select(Category).where(Category.store_code == store_code).order_by(Category.sort_order)
        )
        return list(result.scalars().all())

    async def get_max_sort_order(self, store_code: str) -> int:
        result = await self.db.execute(
            select(func.coalesce(func.max(Category.sort_order), 0)).where(
                Category.store_code == store_code
            )
        )
        return result.scalar_one()

    async def has_active_menus(self, category_id: int) -> bool:
        result = await self.db.execute(
            select(func.count()).where(Menu.category_id == category_id, Menu.deleted_at.is_(None))
        )
        return result.scalar_one() > 0
