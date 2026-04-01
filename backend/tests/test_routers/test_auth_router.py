"""Tests for auth router."""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.store import Store
from app.models.table import Table
from app.models.table_session import TableSession
from app.models.user import User


@pytest.mark.asyncio
class TestAuthRouter:
    @pytest_asyncio.fixture
    async def seed_data(self, db_session: AsyncSession):
        store = Store(name="테스트매장", code="TEST01")
        db_session.add(store)
        await db_session.flush()

        user = User(store_id=store.id, username="admin", password_hash=hash_password("password123"), role="owner")
        db_session.add(user)

        table = Table(store_id=store.id, table_no=1, password_hash=hash_password("1234"))
        db_session.add(table)
        await db_session.flush()

        session = TableSession(store_id=store.id, table_id=table.id)
        db_session.add(session)
        await db_session.commit()
        return store

    async def test_admin_login(self, client: AsyncClient, seed_data):
        resp = await client.post("/api/v1/auth/login/admin", json={
            "store_code": "TEST01", "username": "admin", "password": "password123"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["user"]["role"] == "owner"

    async def test_admin_login_invalid(self, client: AsyncClient, seed_data):
        resp = await client.post("/api/v1/auth/login/admin", json={
            "store_code": "TEST01", "username": "admin", "password": "wrong"
        })
        assert resp.status_code == 401

    async def test_table_login(self, client: AsyncClient, seed_data):
        resp = await client.post("/api/v1/auth/login/table", json={
            "store_code": "TEST01", "table_no": 1, "password": "1234"
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()
