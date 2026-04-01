"""Test configuration and fixtures for database tests."""

import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.config import DatabaseSettings
from database.models import Base


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_settings() -> DatabaseSettings:
    """Test database settings."""
    return DatabaseSettings(
        db_host="localhost",
        db_port=3306,
        db_user="tableorder_test",
        db_password="tableorder_test",
        db_name="tableorder_test",
        db_echo=True,
        environment="test",
    )


@pytest_asyncio.fixture(scope="session")
async def test_engine(test_settings: DatabaseSettings):
    """Create test database engine."""
    engine = create_async_engine(
        test_settings.database_url,
        echo=test_settings.db_echo,
        connect_args={"charset": "utf8mb4"},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional test session that rolls back after each test."""
    session_factory = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        async with session.begin():
            yield session
            await session.rollback()
