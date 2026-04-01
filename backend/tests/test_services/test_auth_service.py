"""Tests for AuthService — store_code based."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidCredentialsException
from app.core.security import hash_password
from app.models.store import Store
from app.models.table import RestaurantTable
from app.models.table_session import TableSession
from app.models.user import User, UserRole
from app.services.auth_service import AuthService


@pytest.mark.asyncio
class TestAuthService:
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
        return store, user, table, session

    async def test_admin_login_success(self, db_session, seed_data):
        service = AuthService(db_session)
        result = await service.login_admin("TEST01", "admin", "password123")
        assert result.access_token
        assert result.user.username == "admin"

    async def test_admin_login_wrong_password(self, db_session, seed_data):
        service = AuthService(db_session)
        with pytest.raises(InvalidCredentialsException):
            await service.login_admin("TEST01", "admin", "wrong")

    async def test_table_login_success(self, db_session, seed_data):
        service = AuthService(db_session)
        result = await service.login_table("TEST01", 1, "1234")
        assert result.access_token
        assert result.table.table_no == 1

    async def test_table_login_wrong_password(self, db_session, seed_data):
        service = AuthService(db_session)
        with pytest.raises(InvalidCredentialsException):
            await service.login_table("TEST01", 1, "wrong")
