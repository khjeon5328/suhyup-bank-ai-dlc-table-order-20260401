"""Menu service — synced with Unit 1."""

from datetime import datetime
from typing import List, Optional

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    CategoryHasMenusException,
    CategoryNotFoundException,
    DuplicateCategoryException,
    MenuNotFoundException,
)
from app.models.category import Category
from app.models.menu import Menu
from app.repositories.category_repo import CategoryRepository
from app.repositories.menu_repo import MenuRepository
from app.schemas.menu import CategoryCreate, CategoryUpdate, MenuCreate, MenuOrderUpdate, MenuUpdate

logger = structlog.get_logger()


class MenuService:
    def __init__(self, db: AsyncSession):
        self.menu_repo = MenuRepository(db)
        self.category_repo = CategoryRepository(db)
        self.db = db

    async def create_category(self, store_code: str, data: CategoryCreate) -> Category:
        existing = await self.category_repo.get_by_name(store_code, data.name)
        if existing:
            raise DuplicateCategoryException()
        max_order = await self.category_repo.get_max_sort_order(store_code)
        category = Category(store_code=store_code, name=data.name, sort_order=max_order + 1)
        category = await self.category_repo.create(category)
        await self.db.commit()
        return category

    async def get_categories(self, store_code: str) -> List[Category]:
        return await self.category_repo.get_by_store(store_code)

    async def update_category(self, store_code: str, category_id: int, data: CategoryUpdate) -> Category:
        category = await self.category_repo.get_by_id(store_code, category_id)
        if not category:
            raise CategoryNotFoundException()
        if data.name and data.name != category.name:
            dup = await self.category_repo.get_by_name(store_code, data.name)
            if dup:
                raise DuplicateCategoryException()
            category.name = data.name
        if data.sort_order is not None:
            category.sort_order = data.sort_order
        await self.db.commit()
        return category

    async def delete_category(self, store_code: str, category_id: int) -> None:
        category = await self.category_repo.get_by_id(store_code, category_id)
        if not category:
            raise CategoryNotFoundException()
        if await self.category_repo.has_active_menus(category_id):
            raise CategoryHasMenusException()
        await self.db.delete(category)
        await self.db.commit()

    async def create_menu(self, store_code: str, data: MenuCreate) -> Menu:
        category = await self.category_repo.get_by_id(store_code, data.category_id)
        if not category:
            raise CategoryNotFoundException()
        max_order = await self.menu_repo.get_max_sort_order(store_code, data.category_id)
        menu = Menu(
            store_code=store_code, category_id=data.category_id,
            name=data.name, price=data.price,
            description=data.description, image_url=data.image_url,
            sort_order=max_order + 1,
        )
        menu = await self.menu_repo.create(menu)
        await self.db.commit()
        logger.info("menu_created", store_code=store_code, menu_id=menu.id)
        return menu

    async def get_menus(self, store_code: str, category_id: Optional[int] = None) -> List[Menu]:
        return await self.menu_repo.get_by_store(store_code, category_id)

    async def get_menu(self, store_code: str, menu_id: int) -> Menu:
        menu = await self.menu_repo.get_by_id(store_code, menu_id)
        if not menu:
            raise MenuNotFoundException()
        return menu

    async def update_menu(self, store_code: str, menu_id: int, data: MenuUpdate) -> Menu:
        menu = await self.menu_repo.get_by_id(store_code, menu_id)
        if not menu:
            raise MenuNotFoundException()
        if data.category_id is not None:
            cat = await self.category_repo.get_by_id(store_code, data.category_id)
            if not cat:
                raise CategoryNotFoundException()
            menu.category_id = data.category_id
        for field in ("name", "price", "description", "image_url", "sort_order"):
            val = getattr(data, field, None)
            if val is not None:
                setattr(menu, field, val)
        await self.db.commit()
        return menu

    async def delete_menu(self, store_code: str, menu_id: int) -> None:
        menu = await self.menu_repo.get_by_id(store_code, menu_id)
        if not menu:
            raise MenuNotFoundException()
        menu.deleted_at = datetime.utcnow()
        await self.db.commit()

    async def update_menu_order(self, store_code: str, data: MenuOrderUpdate) -> None:
        for item in data.items:
            menu = await self.menu_repo.get_by_id(store_code, item.menu_id)
            if menu:
                menu.sort_order = item.sort_order
        await self.db.commit()
