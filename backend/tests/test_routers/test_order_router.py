"""Tests for order router."""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.category import Category
from app.models.menu import Menu
from app.models.store import Store
from app.models.table import Table
from app.models.table_session import TableSession
from app.models.user import User
from tests.conftest import make_owner_token, make_table_token


@pytest.mark.asyncio
class TestOrderRouter:
    @pytest_asyncio.fixture
    async def seed_data(self, db_session: AsyncSession):
        store = Store(name="테스트매장", code="TEST01")
        db_session.add(store)
        await db_session.flush()

        user = User(store_id=store.id, username="admin", password_hash=hash_password("pw"), role="owner")
        db_session.add(user)

        table = Table(store_id=store.id, table_no=1, password_hash=hash_password("1234"))
        db_session.add(table)
        await db_session.flush()

        session = TableSession(store_id=store.id, table_id=table.id)
        db_session.add(session)
        await db_session.flush()

        cat = Category(store_id=store.id, name="메인")
        db_session.add(cat)
        await db_session.flush()

        menu = Menu(store_id=store.id, category_id=cat.id, name="김치찌개", price=9000)
        db_session.add(menu)
        await db_session.commit()
        return store, user, table, session, menu

    async def test_create_order(self, client: AsyncClient, seed_data):
        store, user, table, session, menu = seed_data
        token = make_table_token(table_id=table.id, store_id=store.id, session_id=session.id)
        resp = await client.post(
            f"/api/v1/stores/{store.id}/orders",
            json={"items": [{"menu_id": menu.id, "quantity": 2}]},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["total_amount"] == 18000
        assert data["status"] == "pending"

    async def test_get_orders_as_table(self, client: AsyncClient, seed_data):
        store, _, table, session, menu = seed_data
        token = make_table_token(table_id=table.id, store_id=store.id, session_id=session.id)
        # Create order first
        await client.post(
            f"/api/v1/stores/{store.id}/orders",
            json={"items": [{"menu_id": menu.id, "quantity": 1}]},
            headers={"Authorization": f"Bearer {token}"},
        )
        resp = await client.get(
            f"/api/v1/stores/{store.id}/orders",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    async def test_update_order_status(self, client: AsyncClient, seed_data):
        store, user, table, session, menu = seed_data
        table_token = make_table_token(table_id=table.id, store_id=store.id, session_id=session.id)
        owner_token = make_owner_token(user_id=user.id, store_id=store.id)

        # Create order
        create_resp = await client.post(
            f"/api/v1/stores/{store.id}/orders",
            json={"items": [{"menu_id": menu.id, "quantity": 1}]},
            headers={"Authorization": f"Bearer {table_token}"},
        )
        order_id = create_resp.json()["id"]

        # Update status
        resp = await client.patch(
            f"/api/v1/stores/{store.id}/orders/{order_id}/status",
            json={"status": "preparing"},
            headers={"Authorization": f"Bearer {owner_token}"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "preparing"

    async def test_create_order_unauthorized(self, client: AsyncClient, seed_data):
        store, user, _, _, menu = seed_data
        owner_token = make_owner_token(user_id=user.id, store_id=store.id)
        resp = await client.post(
            f"/api/v1/stores/{store.id}/orders",
            json={"items": [{"menu_id": menu.id, "quantity": 1}]},
            headers={"Authorization": f"Bearer {owner_token}"},
        )
        assert resp.status_code == 403
