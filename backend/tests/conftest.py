"""Pytest fixtures for backend tests."""

import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import get_db_session
from app.core.event_bus import EventBus
from app.core.dependencies import get_event_bus
from app.core.security import create_access_token, hash_password
from app.models.base import Base
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def test_event_bus() -> EventBus:
    return EventBus()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession, test_event_bus: EventBus) -> AsyncGenerator[AsyncClient, None]:
    async def override_db():
        yield db_session

    def override_event_bus():
        return test_event_bus

    app.dependency_overrides[get_db_session] = override_db
    app.dependency_overrides[get_event_bus] = override_event_bus

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as ac:
        yield ac

    app.dependency_overrides.clear()


def make_owner_token(user_id: int = 1, store_id: int = 1) -> str:
    return create_access_token(data={"user_id": user_id, "store_id": store_id, "role": "owner"})


def make_manager_token(user_id: int = 2, store_id: int = 1) -> str:
    return create_access_token(data={"user_id": user_id, "store_id": store_id, "role": "manager"})


def make_table_token(table_id: int = 1, store_id: int = 1, session_id: int = 1) -> str:
    return create_access_token(
        data={"table_id": table_id, "store_id": store_id, "session_id": session_id, "role": "table"}
    )
