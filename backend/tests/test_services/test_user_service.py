"""Tests for UserService."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    CannotChangeOwnRoleException,
    CannotDeleteSelfException,
    DuplicateUserException,
    LastOwnerException,
)
from app.core.security import hash_password
from app.models.store import Store
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService


@pytest.mark.asyncio
class TestUserService:
    @pytest_asyncio.fixture
    async def seed_data(self, db_session: AsyncSession):
        store = Store(name="테스트매장", code="TEST01")
        db_session.add(store)
        await db_session.flush()
        owner = User(
            store_id=store.id, username="owner1",
            password_hash=hash_password("password"), role="owner",
        )
        db_session.add(owner)
        await db_session.commit()
        return store, owner

    async def test_create_user(self, db_session: AsyncSession, seed_data):
        store, _ = seed_data
        service = UserService(db_session)
        user = await service.create_user(store.id, UserCreate(username="manager1", password="password123", role="manager"))
        assert user.username == "manager1"
        assert user.role == "manager"

    async def test_duplicate_user(self, db_session: AsyncSession, seed_data):
        store, _ = seed_data
        service = UserService(db_session)
        with pytest.raises(DuplicateUserException):
            await service.create_user(store.id, UserCreate(username="owner1", password="password123", role="manager"))

    async def test_cannot_delete_self(self, db_session: AsyncSession, seed_data):
        store, owner = seed_data
        service = UserService(db_session)
        with pytest.raises(CannotDeleteSelfException):
            await service.delete_user(store.id, owner.id, owner.id)

    async def test_cannot_delete_last_owner(self, db_session: AsyncSession, seed_data):
        store, owner = seed_data
        service = UserService(db_session)
        manager = await service.create_user(store.id, UserCreate(username="mgr", password="password123", role="manager"))
        with pytest.raises(LastOwnerException):
            await service.delete_user(store.id, owner.id, manager.id)

    async def test_cannot_change_own_role(self, db_session: AsyncSession, seed_data):
        store, owner = seed_data
        service = UserService(db_session)
        with pytest.raises(CannotChangeOwnRoleException):
            await service.update_user(store.id, owner.id, owner.id, UserUpdate(role="manager"))
