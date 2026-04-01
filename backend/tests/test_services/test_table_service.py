"""Tests for TableService."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.event_bus import EventBus
from app.core.exceptions import DuplicateTableException, PendingOrdersException
from app.core.security import hash_password
from app.models.category import Category
from app.models.menu import Menu
from app.models.store import Store
from app.models.table import Table
from app.models.table_session import TableSession
from app.schemas.order import OrderCreate, OrderItemCreate
from app.services.order_service import OrderService
from app.services.table_service import TableService


@pytest.mark.asyncio
class TestTableService:
    @pytest_asyncio.fixture
    async def seed_store(self, db_session: AsyncSession):
        store = Store(name="테스트매장", code="TEST01")
        db_session.add(store)
        await db_session.commit()
        return store

    async def test_setup_table(self, db_session: AsyncSession, test_event_bus: EventBus, seed_store):
        service = TableService(db_session, test_event_bus)
        result = await service.setup_table(seed_store.id, 1, "1234")
        assert result.table.table_no == 1
        assert result.session.is_active is True

    async def test_setup_duplicate_table(self, db_session: AsyncSession, test_event_bus: EventBus, seed_store):
        service = TableService(db_session, test_event_bus)
        await service.setup_table(seed_store.id, 1, "1234")
        with pytest.raises(DuplicateTableException):
            await service.setup_table(seed_store.id, 1, "5678")

    async def test_end_session_no_orders(self, db_session: AsyncSession, test_event_bus: EventBus, seed_store):
        service = TableService(db_session, test_event_bus)
        setup = await service.setup_table(seed_store.id, 1, "1234")
        result = await service.end_session(seed_store.id, setup.table.id)
        assert result.archived_orders == 0
        assert result.new_session.is_active is True

    async def test_end_session_with_pending_orders(self, db_session: AsyncSession, test_event_bus: EventBus, seed_store):
        table_svc = TableService(db_session, test_event_bus)
        setup = await table_svc.setup_table(seed_store.id, 1, "1234")

        # Create a menu and order
        cat = Category(store_id=seed_store.id, name="메인")
        db_session.add(cat)
        await db_session.flush()
        menu = Menu(store_id=seed_store.id, category_id=cat.id, name="김치찌개", price=9000)
        db_session.add(menu)
        await db_session.commit()

        order_svc = OrderService(db_session, test_event_bus)
        await order_svc.create_order(
            seed_store.id, setup.table.id, setup.session.id,
            OrderCreate(items=[OrderItemCreate(menu_id=menu.id, quantity=1)])
        )

        # Should raise without force
        with pytest.raises(PendingOrdersException):
            await table_svc.end_session(seed_store.id, setup.table.id, force=False)

        # Should succeed with force
        result = await table_svc.end_session(seed_store.id, setup.table.id, force=True)
        assert result.archived_orders == 1
