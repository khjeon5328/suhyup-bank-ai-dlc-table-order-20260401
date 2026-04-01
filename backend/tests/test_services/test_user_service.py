"""Tests for UserService — store_code based."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CannotChangeOwnRoleException, CannotDeleteSelfException, DuplicateUserException, LastOwnerException
from app.core.security import hash_password
from app.models.store import Store
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService


@pytest.mark.asyncio
class TestUserService:
    @pytest_asyncio.fixture
    async def seed_data(self, db_session: AsyncSession):
        store = Store(store_code="TEST01", name="테스트매장")
        db_session.add(store)
        await db_session.flush()
        owner = User(store_code="TEST01", username="owner1", password_hash=hash_password("password"), role=UserRole.OWNER)
        db_session.add(owner)
        await db_session.commit()
        return store, owner

    async def test_create_user(self, db_session, seed_data):
        user = await UserService(db_session).create_user("TEST01", UserCreate(username="manager1", password="password123", role="manager"))
        assert user.username == "manager1"

    async def test_duplicate_user(self, db_session, seed_data):
        with pytest.raises(DuplicateUserException):
            await UserService(db_session).create_user("TEST01", UserCreate(username="owner1", password="password123", role="manager"))

    async def test_cannot_delete_self(self, db_session, seed_data):
        _, owner = seed_data
        with pytest.raises(CannotDeleteSelfException):
            await UserService(db_session).delete_user("TEST01", owner.id, owner.id)

    async def test_cannot_delete_last_owner(self, db_session, seed_data):
        _, owner = seed_data
        mgr = await UserService(db_session).create_user("TEST01", UserCreate(username="mgr", password="password123", role="manager"))
        with pytest.raises(LastOwnerException):
            await UserService(db_session).delete_user("TEST01", owner.id, mgr.id)

    async def test_cannot_change_own_role(self, db_session, seed_data):
        _, owner = seed_data
        with pytest.raises(CannotChangeOwnRoleException):
            await UserService(db_session).update_user("TEST01", owner.id, owner.id, UserUpdate(role="manager"))
