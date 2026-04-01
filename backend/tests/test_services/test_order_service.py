"""Tests for OrderService."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.event_bus import EventBus
from app.core.exceptions import (
    InvalidStatusTransitionException,
    MenuNotFoundException,
    OrderNotFoundException,
)
from app.core.security import hash_password
from app.models.category import Category
from app.models.menu import Menu
from app.models.order import Order
from app.models.store import Store
from app.models.table import Table
from app.models.table_session import TableSession
from app.schemas.order import OrderCreate, OrderItemCreate
from app.services.order_service import OrderService


@pytest.mark.asyncio
class TestOrderService:
    @pytest_asyncio.fixture
    async def seed_data(self, db_session: AsyncSession):
        store = Store(name="테스트매장", code="TEST01")
        db_session.add(store)
        await db_session.flush()

        table = Table(store_id=store.id, table_no=1, password_hash=hash_password("1234"))
        db_session.add(table)
        await db_session.flush()

        session = TableSession(store_id=store.id, table_id=table.id)
        db_session.add(session)
        await db_session.flush()

        category = Category(store_id=store.id, name="메인")
        db_session.add(category)
        await db_session.flush()

        menu = Menu(store_id=store.id, category_id=category.id, name="김치찌개", price=9000)
        db_session.add(menu)
        await db_session.commit()
        return store, table, session, menu

    async def test_create_order(self, db_session: AsyncSession, test_event_bus: EventBus, seed_data):
        store, table, session, menu = seed_data
        service = OrderService(db_session, test_event_bus)
        data = OrderCreate(items=[OrderItemCreate(menu_id=menu.id, quantity=2)])
        order = await service.create_order(store.id, table.id, session.id, data)
        assert order.order_no == "001"
        assert order.total_amount == 18000
        assert order.status == "pending"
        assert len(order.items) == 1

    async def test_update_status_valid(self, db_session: AsyncSession, test_event_bus: EventBus, seed_data):
        store, table, session, menu = seed_data
        service = OrderService(db_session, test_event_bus)
        data = OrderCreate(items=[OrderItemCreate(menu_id=menu.id, quantity=1)])
        order = await service.create_order(store.id, table.id, session.id, data)

        updated = await service.update_status(store.id, order.id, "preparing")
        assert updated.status == "preparing"

    async def test_update_status_invalid_transition(self, db_session: AsyncSession, test_event_bus: EventBus, seed_data):
        store, table, session, menu = seed_data
        service = OrderService(db_session, test_event_bus)
        data = OrderCreate(items=[OrderItemCreate(menu_id=menu.id, quantity=1)])
        order = await service.create_order(store.id, table.id, session.id, data)

        with pytest.raises(InvalidStatusTransitionException):
            await service.update_status(store.id, order.id, "completed")

    async def test_delete_order(self, db_session: AsyncSession, test_event_bus: EventBus, seed_data):
        store, table, session, menu = seed_data
        service = OrderService(db_session, test_event_bus)
        data = OrderCreate(items=[OrderItemCreate(menu_id=menu.id, quantity=1)])
        order = await service.create_order(store.id, table.id, session.id, data)

        await service.delete_order(store.id, order.id)
        with pytest.raises(OrderNotFoundException):
            await service.get_order(store.id, order.id)

    async def test_create_order_invalid_menu(self, db_session: AsyncSession, test_event_bus: EventBus, seed_data):
        store, table, session, _ = seed_data
        service = OrderService(db_session, test_event_bus)
        data = OrderCreate(items=[OrderItemCreate(menu_id=9999, quantity=1)])
        with pytest.raises(MenuNotFoundException):
            await service.create_order(store.id, table.id, session.id, data)
