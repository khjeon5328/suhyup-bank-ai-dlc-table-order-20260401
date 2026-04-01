"""Tests for Repository layer: CRUD, soft delete, archive."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Category, Menu, Order, OrderItem, RestaurantTable, Store, TableSession
from database.models.order import OrderStatus
from database.models.user import UserRole, User
from database.repositories.category import CategoryRepository
from database.repositories.menu import MenuRepository
from database.repositories.order import OrderRepository
from database.repositories.session import SessionRepository
from database.repositories.store import StoreRepository
from database.repositories.user import UserRepository
from database.utils.security import hash_password


async def _create_test_store(session: AsyncSession, code: str = "REPO01") -> Store:
    """Helper to create a test store."""
    store = Store(store_code=code, name=f"Repo Test {code}")
    session.add(store)
    await session.flush()
    return store


@pytest.mark.asyncio
async def test_store_repository_get_by_code(db_session: AsyncSession):
    """Test StoreRepository.get_by_code."""
    await _create_test_store(db_session, "SREPO1")
    repo = StoreRepository(db_session)
    store = await repo.get_by_code("SREPO1")
    assert store is not None
    assert store.store_code == "SREPO1"


@pytest.mark.asyncio
async def test_user_repository_soft_delete(db_session: AsyncSession):
    """Test UserRepository soft delete and active filter."""
    await _create_test_store(db_session, "UREPO1")
    repo = UserRepository(db_session)

    user = User(
        store_code="UREPO1", username="testuser",
        password_hash=hash_password("password123"), role=UserRole.MANAGER,
    )
    await repo.create(user)

    active_users = await repo.get_active_users("UREPO1")
    assert len(active_users) == 1

    await repo.soft_delete(user)
    active_users = await repo.get_active_users("UREPO1")
    assert len(active_users) == 0


@pytest.mark.asyncio
async def test_session_repository_lifecycle(db_session: AsyncSession):
    """Test SessionRepository create and end session."""
    await _create_test_store(db_session, "SSREPO")
    table = RestaurantTable(
        store_code="SSREPO", table_no=1, password_hash=hash_password("1234")
    )
    db_session.add(table)
    await db_session.flush()

    repo = SessionRepository(db_session)
    new_session = await repo.create_session("SSREPO", 1)
    assert new_session.is_active is True

    active = await repo.get_active_session("SSREPO", 1)
    assert active is not None
    assert active.id == new_session.id

    ended = await repo.end_session(new_session.id)
    assert ended is not None
    assert ended.is_active is False

    active_after = await repo.get_active_session("SSREPO", 1)
    assert active_after is None


@pytest.mark.asyncio
async def test_menu_repository_soft_delete(db_session: AsyncSession):
    """Test MenuRepository soft delete and active filter."""
    await _create_test_store(db_session, "MREPO1")
    cat = Category(store_code="MREPO1", name="테스트", sort_order=1)
    db_session.add(cat)
    await db_session.flush()

    repo = MenuRepository(db_session)
    menu = Menu(
        store_code="MREPO1", category_id=cat.id,
        name="삭제 테스트 메뉴", price=5000,
    )
    await repo.create(menu)

    menus = await repo.get_by_store("MREPO1")
    assert len(menus) == 1

    await repo.soft_delete(menu)
    menus_after = await repo.get_by_store("MREPO1")
    assert len(menus_after) == 0

    menus_all = await repo.get_by_store("MREPO1", include_deleted=True)
    assert len(menus_all) == 1


@pytest.mark.asyncio
async def test_order_repository_archive(db_session: AsyncSession):
    """Test OrderRepository archive by session."""
    await _create_test_store(db_session, "OREPO1")
    table = RestaurantTable(
        store_code="OREPO1", table_no=1, password_hash=hash_password("1234")
    )
    db_session.add(table)
    await db_session.flush()

    ts = TableSession(store_code="OREPO1", table_no=1)
    db_session.add(ts)
    await db_session.flush()

    cat = Category(store_code="OREPO1", name="메인", sort_order=1)
    db_session.add(cat)
    await db_session.flush()

    menu = Menu(
        store_code="OREPO1", category_id=cat.id, name="테스트", price=10000
    )
    db_session.add(menu)
    await db_session.flush()

    order = Order(
        store_code="OREPO1", table_no=1, session_id=ts.id,
        total_amount=10000, status=OrderStatus.PENDING,
    )
    db_session.add(order)
    await db_session.flush()

    repo = OrderRepository(db_session)
    current = await repo.get_current_orders("OREPO1")
    assert len(current) == 1

    archived_count = await repo.archive_by_session(ts.id)
    assert archived_count == 1

    current_after = await repo.get_current_orders("OREPO1")
    assert len(current_after) == 0

    archived = await repo.get_archived_orders("OREPO1")
    assert len(archived) == 1
