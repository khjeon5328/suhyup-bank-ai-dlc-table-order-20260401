"""Tests for menu router — store_code based."""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.store import Store
from app.models.user import User, UserRole
from tests.conftest import make_manager_token, make_owner_token


@pytest.mark.asyncio
class TestMenuRouter:
    @pytest_asyncio.fixture
    async def seed_data(self, db_session: AsyncSession):
        store = Store(store_code="TEST01", name="테스트매장")
        db_session.add(store)
        await db_session.flush()
        user = User(store_code="TEST01", username="admin", password_hash=hash_password("pw"), role=UserRole.OWNER)
        db_session.add(user)
        await db_session.commit()
        return store, user

    async def test_create_category(self, client: AsyncClient, seed_data):
        _, user = seed_data
        token = make_owner_token(user_id=user.id, store_code="TEST01")
        resp = await client.post("/api/v1/stores/TEST01/menus/categories", json={"name": "메인"}, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 201
        assert resp.json()["name"] == "메인"

    async def test_create_menu(self, client: AsyncClient, seed_data):
        _, user = seed_data
        token = make_owner_token(user_id=user.id, store_code="TEST01")
        cat_resp = await client.post("/api/v1/stores/TEST01/menus/categories", json={"name": "메인"}, headers={"Authorization": f"Bearer {token}"})
        cat_id = cat_resp.json()["id"]
        resp = await client.post("/api/v1/stores/TEST01/menus", json={"name": "김치찌개", "price": 9000, "category_id": cat_id}, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 201

    async def test_manager_cannot_create_menu(self, client: AsyncClient, seed_data):
        token = make_manager_token(store_code="TEST01")
        resp = await client.post("/api/v1/stores/TEST01/menus", json={"name": "된장찌개", "price": 8000, "category_id": 1}, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 403
