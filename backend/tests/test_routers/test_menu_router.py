"""Tests for menu router."""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.store import Store
from app.models.user import User
from tests.conftest import make_manager_token, make_owner_token


@pytest.mark.asyncio
class TestMenuRouter:
    @pytest_asyncio.fixture
    async def seed_data(self, db_session: AsyncSession):
        store = Store(name="테스트매장", code="TEST01")
        db_session.add(store)
        await db_session.flush()
        user = User(store_id=store.id, username="admin", password_hash=hash_password("pw"), role="owner")
        db_session.add(user)
        await db_session.commit()
        return store, user

    async def test_create_category(self, client: AsyncClient, seed_data):
        store, user = seed_data
        token = make_owner_token(user_id=user.id, store_id=store.id)
        resp = await client.post(
            f"/api/v1/stores/{store.id}/menus/categories",
            json={"name": "메인"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 201
        assert resp.json()["name"] == "메인"

    async def test_create_menu(self, client: AsyncClient, seed_data):
        store, user = seed_data
        token = make_owner_token(user_id=user.id, store_id=store.id)
        # Create category first
        cat_resp = await client.post(
            f"/api/v1/stores/{store.id}/menus/categories",
            json={"name": "메인"},
            headers={"Authorization": f"Bearer {token}"},
        )
        cat_id = cat_resp.json()["id"]
        resp = await client.post(
            f"/api/v1/stores/{store.id}/menus",
            json={"name": "김치찌개", "price": 9000, "category_id": cat_id},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 201
        assert resp.json()["name"] == "김치찌개"

    async def test_manager_cannot_create_menu(self, client: AsyncClient, seed_data):
        store, _ = seed_data
        token = make_manager_token(store_id=store.id)
        resp = await client.post(
            f"/api/v1/stores/{store.id}/menus",
            json={"name": "된장찌개", "price": 8000, "category_id": 1},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 403
