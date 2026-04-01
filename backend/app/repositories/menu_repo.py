"""Menu repository."""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.menu import Menu


class MenuRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, menu: Menu) -> Menu:
        self.db.add(menu)
        await self.db.flush()
        await self.db.refresh(menu)
        return menu

    async def get_by_id(self, store_id: int, menu_id: int) -> Optional[Menu]:
        result = await self.db.execute(
            select(Menu).where(Menu.id == menu_id, Menu.store_id == store_id, Menu.is_active == True)
        )
        return result.scalar_one_or_none()

    async def get_by_store(self, store_id: int, category_id: Optional[int] = None) -> List[Menu]:
        stmt = select(Menu).where(Menu.store_id == store_id, Menu.is_active == True)
        if category_id:
            stmt = stmt.where(Menu.category_id == category_id)
        stmt = stmt.order_by(Menu.sort_order, Menu.created_at)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_max_sort_order(self, store_id: int, category_id: int) -> int:
        result = await self.db.execute(
            select(func.coalesce(func.max(Menu.sort_order), 0)).where(
                Menu.store_id == store_id, Menu.category_id == category_id, Menu.is_active == True
            )
        )
        return result.scalar_one()
