"""Tests for auth router — store_code based."""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.store import Store
from app.models.table import RestaurantTable
from app.models.table_session import TableSession
from app.models.user import User, UserRole


@pytest.mark.asyncio
class TestAuthRouter:
    @pytest_asyncio.fixture
    async def seed_data(self, db_session: AsyncSession):
        store = Store(store_code="TEST01", name="테스트매장")
        db_session.add(store)
        await db_session.flush()
        user = User(store_code="TEST01", username="admin", password_hash=hash_password("password123"), role=UserRole.OWNER)
        db_session.add(user)
        table = RestaurantTable(store_code="TEST01", table_no=1, password_hash=hash_password("1234"))
        db_session.add(table)
        await db_session.flush()
        session = TableSession(store_code="TEST01", table_no=1)
        db_session.add(session)
        await db_session.commit()

    async def test_admin_login(self, client: AsyncClient, seed_data):
        resp = await client.post("/api/v1/auth/login/admin", json={"store_code": "TEST01", "username": "admin", "password": "password123"})
        assert resp.status_code == 200
        assert resp.json()["user"]["role"] == "owner"

    async def test_admin_login_invalid(self, client: AsyncClient, seed_data):
        resp = await client.post("/api/v1/auth/login/admin", json={"store_code": "TEST01", "username": "admin", "password": "wrong"})
        assert resp.status_code == 401

    async def test_table_login(self, client: AsyncClient, seed_data):
        resp = await client.post("/api/v1/auth/login/table", json={"store_code": "TEST01", "table_no": 1, "password": "1234"})
        assert resp.status_code == 200
        assert "access_token" in resp.json()
