"""Tests for TableService — store_code based."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.event_bus import EventBus
from app.core.exceptions import DuplicateTableException, PendingOrdersException
from app.core.security import hash_password
from app.models.category import Category
from app.models.menu import Menu
from app.models.store import Store
from app.schemas.order import OrderCreate, OrderItemCreate
from app.services.order_service import OrderService
from app.services.table_service import TableService


@pytest.mark.asyncio
class TestTableService:
    @pytest_asyncio.fixture
    async def seed_store(self, db_session: AsyncSession):
        store = Store(store_code="TEST01", name="테스트매장")
        db_session.add(store)
        await db_session.commit()
        return store

    async def test_setup_table(self, db_session, test_event_bus, seed_store):
        service = TableService(db_session, test_event_bus)
        result = await service.setup_table("TEST01", 1, "1234")
        assert result.table.table_no == 1
        assert result.session.ended_at is None

    async def test_setup_duplicate_table(self, db_session, test_event_bus, seed_store):
        service = TableService(db_session, test_event_bus)
        await service.setup_table("TEST01", 1, "1234")
        with pytest.raises(DuplicateTableException):
            await service.setup_table("TEST01", 1, "5678")

    async def test_end_session_no_orders(self, db_session, test_event_bus, seed_store):
        service = TableService(db_session, test_event_bus)
        setup = await service.setup_table("TEST01", 1, "1234")
        result = await service.end_session("TEST01", 1)
        assert result.archived_orders == 0
        assert result.new_session.ended_at is None

    async def test_end_session_with_pending_orders(self, db_session, test_event_bus, seed_store):
        table_svc = TableService(db_session, test_event_bus)
        setup = await table_svc.setup_table("TEST01", 1, "1234")

        cat = Category(store_code="TEST01", name="메인")
        db_session.add(cat)
        await db_session.flush()
        menu = Menu(store_code="TEST01", category_id=cat.id, name="김치찌개", price=9000)
        db_session.add(menu)
        await db_session.commit()

        order_svc = OrderService(db_session, test_event_bus)
        await order_svc.create_order("TEST01", 1, setup.session.id, OrderCreate(items=[OrderItemCreate(menu_id=menu.id, quantity=1)]))

        with pytest.raises(PendingOrdersException):
            await table_svc.end_session("TEST01", 1, force=False)

        result = await table_svc.end_session("TEST01", 1, force=True)
        assert result.archived_orders == 1
