"""Menu repository with soft delete filter."""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.menu import Menu
from .base import BaseRepository


class MenuRepository(BaseRepository[Menu]):
    """Repository for Menu entity with soft delete support."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Menu)

    async def get_active_by_id(self, menu_id: int) -> Menu | None:
        """Get active (non-deleted) menu by ID."""
        stmt = select(Menu).where(Menu.id == menu_id, Menu.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_store(
        self,
        store_code: str,
        category_id: int | None = None,
        include_deleted: bool = False,
    ) -> list[Menu]:
        """Get menus for a store, optionally filtered by category."""
        stmt = select(Menu).where(Menu.store_code == store_code)
        if not include_deleted:
            stmt = stmt.where(Menu.deleted_at.is_(None))
        if category_id is not None:
            stmt = stmt.where(Menu.category_id == category_id)
        stmt = stmt.order_by(Menu.sort_order, Menu.id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def soft_delete(self, menu: Menu) -> Menu:
        """Soft delete a menu by setting deleted_at."""
        menu.deleted_at = datetime.now(timezone.utc)
        await self.session.flush()
        await self.session.refresh(menu)
        return menu

    async def update_sort_orders(
        self, store_code: str, menu_orders: list[dict]
    ) -> bool:
        """Update sort orders for multiple menus."""
        for item in menu_orders:
            menu = await self.get_active_by_id(item["menu_id"])
            if menu and menu.store_code == store_code:
                menu.sort_order = item["sort_order"]
        await self.session.flush()
        return True
