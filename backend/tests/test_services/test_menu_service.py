"""Tests for MenuService."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    CategoryHasMenusException,
    CategoryNotFoundException,
    DuplicateCategoryException,
    MenuNotFoundException,
)
from app.models.store import Store
from app.schemas.menu import CategoryCreate, MenuCreate, MenuUpdate
from app.services.menu_service import MenuService


@pytest.mark.asyncio
class TestMenuService:
    @pytest_asyncio.fixture
    async def seed_store(self, db_session: AsyncSession):
        store = Store(name="테스트매장", code="TEST01")
        db_session.add(store)
        await db_session.commit()
        return store

    async def test_create_category(self, db_session: AsyncSession, seed_store):
        service = MenuService(db_session)
        cat = await service.create_category(seed_store.id, CategoryCreate(name="메인"))
        assert cat.name == "메인"
        assert cat.sort_order == 1

    async def test_duplicate_category(self, db_session: AsyncSession, seed_store):
        service = MenuService(db_session)
        await service.create_category(seed_store.id, CategoryCreate(name="메인"))
        with pytest.raises(DuplicateCategoryException):
            await service.create_category(seed_store.id, CategoryCreate(name="메인"))

    async def test_create_menu(self, db_session: AsyncSession, seed_store):
        service = MenuService(db_session)
        cat = await service.create_category(seed_store.id, CategoryCreate(name="메인"))
        menu = await service.create_menu(
            seed_store.id, MenuCreate(name="김치찌개", price=9000, category_id=cat.id)
        )
        assert menu.name == "김치찌개"
        assert menu.price == 9000

    async def test_update_menu(self, db_session: AsyncSession, seed_store):
        service = MenuService(db_session)
        cat = await service.create_category(seed_store.id, CategoryCreate(name="메인"))
        menu = await service.create_menu(
            seed_store.id, MenuCreate(name="김치찌개", price=9000, category_id=cat.id)
        )
        updated = await service.update_menu(seed_store.id, menu.id, MenuUpdate(price=10000))
        assert updated.price == 10000

    async def test_delete_category_with_menus(self, db_session: AsyncSession, seed_store):
        service = MenuService(db_session)
        cat = await service.create_category(seed_store.id, CategoryCreate(name="메인"))
        await service.create_menu(
            seed_store.id, MenuCreate(name="김치찌개", price=9000, category_id=cat.id)
        )
        with pytest.raises(CategoryHasMenusException):
            await service.delete_category(seed_store.id, cat.id)
