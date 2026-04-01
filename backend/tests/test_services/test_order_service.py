"""Tests for OrderService — store_code based."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.event_bus import EventBus
from app.core.exceptions import InvalidStatusTransitionException, MenuNotFoundException, OrderNotFoundException
from app.core.security import hash_password
from app.models.category import Category
from app.models.menu import Menu
from app.models.store import Store
from app.models.table import RestaurantTable
from app.models.table_session import TableSession
from app.schemas.order import OrderCreate, OrderItemCreate
from app.services.order_service import OrderService


@pytest.mark.asyncio
class TestOrderService:
    @pytest_asyncio.fixture
    async def seed_data(self, db_session: AsyncSession):
        store = Store(store_code="TEST01", name="테스트매장")
        db_session.add(store)
        await db_session.flush()
        table = RestaurantTable(store_code="TEST01", table_no=1, password_hash=hash_password("1234"))
        db_session.add(table)
        await db_session.flush()
        session = TableSession(store_code="TEST01", table_no=1)
        db_session.add(session)
        await db_session.flush()
        category = Category(store_code="TEST01", name="메인")
        db_session.add(category)
        await db_session.flush()
        menu = Menu(store_code="TEST01", category_id=category.id, name="김치찌개", price=9000)
        db_session.add(menu)
        await db_session.commit()
        return store, table, session, menu

    async def test_create_order(self, db_session, test_event_bus, seed_data):
        _, table, session, menu = seed_data
        service = OrderService(db_session, test_event_bus)
        order = await service.create_order("TEST01", 1, session.id, OrderCreate(items=[OrderItemCreate(menu_id=menu.id, quantity=2)]))
        assert order.total_amount == 18000
        assert order.status.value == "pending"

    async def test_update_status_valid(self, db_session, test_event_bus, seed_data):
        _, _, session, menu = seed_data
        service = OrderService(db_session, test_event_bus)
        order = await service.create_order("TEST01", 1, session.id, OrderCreate(items=[OrderItemCreate(menu_id=menu.id, quantity=1)]))
        updated = await service.update_status("TEST01", order.id, "preparing")
        assert updated.status.value == "preparing"

    async def test_update_status_invalid(self, db_session, test_event_bus, seed_data):
        _, _, session, menu = seed_data
        service = OrderService(db_session, test_event_bus)
        order = await service.create_order("TEST01", 1, session.id, OrderCreate(items=[OrderItemCreate(menu_id=menu.id, quantity=1)]))
        with pytest.raises(InvalidStatusTransitionException):
            await service.update_status("TEST01", order.id, "completed")

    async def test_delete_order(self, db_session, test_event_bus, seed_data):
        _, _, session, menu = seed_data
        service = OrderService(db_session, test_event_bus)
        order = await service.create_order("TEST01", 1, session.id, OrderCreate(items=[OrderItemCreate(menu_id=menu.id, quantity=1)]))
        await service.delete_order("TEST01", order.id)
        with pytest.raises(OrderNotFoundException):
            await service.get_order("TEST01", order.id)
