"""Tests for table router."""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.store import Store
from app.models.user import User
from tests.conftest import make_manager_token, make_owner_token


@pytest.mark.asyncio
class TestTableRouter:
    @pytest_asyncio.fixture
    async def seed_data(self, db_session: AsyncSession):
        store = Store(name="테스트매장", code="TEST01")
        db_session.add(store)
        await db_session.flush()
        user = User(store_id=store.id, username="admin", password_hash=hash_password("pw"), role="owner")
        db_session.add(user)
        await db_session.commit()
        return store, user

    async def test_setup_table(self, client: AsyncClient, seed_data):
        store, user = seed_data
        token = make_owner_token(user_id=user.id, store_id=store.id)
        resp = await client.post(
            f"/api/v1/stores/{store.id}/tables",
            json={"table_no": 1, "password": "1234"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 201
        assert resp.json()["table"]["table_no"] == 1
        assert resp.json()["session"]["is_active"] is True

    async def test_manager_cannot_setup_table(self, client: AsyncClient, seed_data):
        store, _ = seed_data
        token = make_manager_token(store_id=store.id)
        resp = await client.post(
            f"/api/v1/stores/{store.id}/tables",
            json={"table_no": 1, "password": "1234"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 403
