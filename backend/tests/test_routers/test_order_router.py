"""Tests for order router — store_code based."""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.category import Category
from app.models.menu import Menu
from app.models.store import Store
from app.models.table import RestaurantTable
from app.models.table_session import TableSession
from app.models.user import User, UserRole
from tests.conftest import make_owner_token, make_table_token


@pytest.mark.asyncio
class TestOrderRouter:
    @pytest_asyncio.fixture
    async def seed_data(self, db_session: AsyncSession):
        store = Store(store_code="TEST01", name="테스트매장")
        db_session.add(store)
        await db_session.flush()
        user = User(store_code="TEST01", username="admin", password_hash=hash_password("pw"), role=UserRole.OWNER)
        db_session.add(user)
        table = RestaurantTable(store_code="TEST01", table_no=1, password_hash=hash_password("1234"))
        db_session.add(table)
        await db_session.flush()
        session = TableSession(store_code="TEST01", table_no=1)
        db_session.add(session)
        await db_session.flush()
        cat = Category(store_code="TEST01", name="메인")
        db_session.add(cat)
        await db_session.flush()
        menu = Menu(store_code="TEST01", category_id=cat.id, name="김치찌개", price=9000)
        db_session.add(menu)
        await db_session.commit()
        return store, user, table, session, menu

    async def test_create_order(self, client: AsyncClient, seed_data):
        store, user, table, session, menu = seed_data
        token = make_table_token(table_no=1, store_code="TEST01", session_id=session.id)
        resp = await client.post(f"/api/v1/stores/TEST01/orders", json={"items": [{"menu_id": menu.id, "quantity": 2}]}, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 201
        assert resp.json()["total_amount"] == 18000

    async def test_create_order_unauthorized(self, client: AsyncClient, seed_data):
        store, user, _, _, menu = seed_data
        token = make_owner_token(user_id=user.id, store_code="TEST01")
        resp = await client.post(f"/api/v1/stores/TEST01/orders", json={"items": [{"menu_id": menu.id, "quantity": 1}]}, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 403
