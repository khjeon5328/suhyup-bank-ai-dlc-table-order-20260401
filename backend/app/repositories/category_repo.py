"""Category repository."""

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

    async def get_by_id(self, store_id: int, category_id: int) -> Optional[Category]:
        result = await self.db.execute(
            select(Category).where(
                Category.id == category_id, Category.store_id == store_id, Category.is_active == True
            )
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, store_id: int, name: str) -> Optional[Category]:
        result = await self.db.execute(
            select(Category).where(
                Category.store_id == store_id, Category.name == name, Category.is_active == True
            )
        )
        return result.scalar_one_or_none()

    async def get_by_store(self, store_id: int) -> List[Category]:
        result = await self.db.execute(
            select(Category)
            .where(Category.store_id == store_id, Category.is_active == True)
            .order_by(Category.sort_order)
        )
        return list(result.scalars().all())

    async def get_max_sort_order(self, store_id: int) -> int:
        result = await self.db.execute(
            select(func.coalesce(func.max(Category.sort_order), 0)).where(
                Category.store_id == store_id, Category.is_active == True
            )
        )
        return result.scalar_one()

    async def has_active_menus(self, category_id: int) -> bool:
        result = await self.db.execute(
            select(func.count()).where(Menu.category_id == category_id, Menu.is_active == True)
        )
        return result.scalar_one() > 0
