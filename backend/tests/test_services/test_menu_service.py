"""Tests for MenuService — store_code based."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CategoryHasMenusException, DuplicateCategoryException, MenuNotFoundException
from app.models.store import Store
from app.schemas.menu import CategoryCreate, MenuCreate, MenuUpdate
from app.services.menu_service import MenuService


@pytest.mark.asyncio
class TestMenuService:
    @pytest_asyncio.fixture
    async def seed_store(self, db_session: AsyncSession):
        store = Store(store_code="TEST01", name="테스트매장")
        db_session.add(store)
        await db_session.commit()
        return store

    async def test_create_category(self, db_session, seed_store):
        cat = await MenuService(db_session).create_category("TEST01", CategoryCreate(name="메인"))
        assert cat.name == "메인"

    async def test_duplicate_category(self, db_session, seed_store):
        svc = MenuService(db_session)
        await svc.create_category("TEST01", CategoryCreate(name="메인"))
        with pytest.raises(DuplicateCategoryException):
            await svc.create_category("TEST01", CategoryCreate(name="메인"))

    async def test_create_menu(self, db_session, seed_store):
        svc = MenuService(db_session)
        cat = await svc.create_category("TEST01", CategoryCreate(name="메인"))
        menu = await svc.create_menu("TEST01", MenuCreate(name="김치찌개", price=9000, category_id=cat.id))
        assert menu.name == "김치찌개"

    async def test_update_menu(self, db_session, seed_store):
        svc = MenuService(db_session)
        cat = await svc.create_category("TEST01", CategoryCreate(name="메인"))
        menu = await svc.create_menu("TEST01", MenuCreate(name="김치찌개", price=9000, category_id=cat.id))
        updated = await svc.update_menu("TEST01", menu.id, MenuUpdate(price=10000))
        assert updated.price == 10000

    async def test_delete_category_with_menus(self, db_session, seed_store):
        svc = MenuService(db_session)
        cat = await svc.create_category("TEST01", CategoryCreate(name="메인"))
        await svc.create_menu("TEST01", MenuCreate(name="김치찌개", price=9000, category_id=cat.id))
        with pytest.raises(CategoryHasMenusException):
            await svc.delete_category("TEST01", cat.id)
