"""Tests for SQLAlchemy models: CRUD, constraints, relationships."""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Category, Menu, Order, OrderItem, RestaurantTable, Store, TableSession, User
from database.models.order import OrderStatus
from database.models.user import UserRole
from database.utils.security import hash_password


@pytest.mark.asyncio
async def test_create_store(db_session: AsyncSession):
    """Test store creation."""
    store = Store(store_code="TEST01", name="테스트 매장")
    db_session.add(store)
    await db_session.flush()

    result = await db_session.get(Store, "TEST01")
    assert result is not None
    assert result.name == "테스트 매장"


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    """Test user creation with hashed password."""
    store = Store(store_code="TEST02", name="테스트 매장2")
    db_session.add(store)
    await db_session.flush()

    user = User(
        store_code="TEST02",
        username="admin",
        password_hash=hash_password("password123"),
        role=UserRole.OWNER,
    )
    db_session.add(user)
    await db_session.flush()

    assert user.id is not None
    assert user.role == UserRole.OWNER
    assert user.is_deleted is False


@pytest.mark.asyncio
async def test_user_soft_delete(db_session: AsyncSession):
    """Test user soft delete sets deleted_at."""
    store = Store(store_code="TEST03", name="테스트 매장3")
    db_session.add(store)
    await db_session.flush()

    user = User(
        store_code="TEST03",
        username="todelete",
        password_hash=hash_password("password123"),
        role=UserRole.MANAGER,
    )
    db_session.add(user)
    await db_session.flush()

    from datetime import datetime, timezone
    user.deleted_at = datetime.now(timezone.utc)
    await db_session.flush()

    assert user.is_deleted is True


@pytest.mark.asyncio
async def test_create_table_and_session(db_session: AsyncSession):
    """Test table creation and session lifecycle."""
    store = Store(store_code="TEST04", name="테스트 매장4")
    db_session.add(store)
    await db_session.flush()

    table = RestaurantTable(
        store_code="TEST04", table_no=1, password_hash=hash_password("1234")
    )
    db_session.add(table)
    await db_session.flush()

    session = TableSession(store_code="TEST04", table_no=1)
    db_session.add(session)
    await db_session.flush()

    assert session.is_active is True
    assert session.ended_at is None


@pytest.mark.asyncio
async def test_create_category_and_menu(db_session: AsyncSession):
    """Test category and menu creation with relationship."""
    store = Store(store_code="TEST05", name="테스트 매장5")
    db_session.add(store)
    await db_session.flush()

    category = Category(store_code="TEST05", name="메인", sort_order=1)
    db_session.add(category)
    await db_session.flush()

    menu = Menu(
        store_code="TEST05",
        category_id=category.id,
        name="테스트 메뉴",
        price=10000,
        description="테스트 설명",
    )
    db_session.add(menu)
    await db_session.flush()

    assert menu.id is not None
    assert menu.price == 10000
    assert menu.is_deleted is False


@pytest.mark.asyncio
async def test_create_order_with_items(db_session: AsyncSession):
    """Test order creation with order items."""
    store = Store(store_code="TEST06", name="테스트 매장6")
    db_session.add(store)
    await db_session.flush()

    table = RestaurantTable(
        store_code="TEST06", table_no=1, password_hash=hash_password("1234")
    )
    db_session.add(table)
    await db_session.flush()

    session = TableSession(store_code="TEST06", table_no=1)
    db_session.add(session)
    await db_session.flush()

    category = Category(store_code="TEST06", name="메인", sort_order=1)
    db_session.add(category)
    await db_session.flush()

    menu = Menu(
        store_code="TEST06", category_id=category.id,
        name="테스트 메뉴", price=10000,
    )
    db_session.add(menu)
    await db_session.flush()

    order = Order(
        store_code="TEST06", table_no=1, session_id=session.id,
        total_amount=20000, status=OrderStatus.PENDING,
    )
    db_session.add(order)
    await db_session.flush()

    item = OrderItem(
        order_id=order.id, menu_id=menu.id,
        menu_name="테스트 메뉴", quantity=2, unit_price=10000, subtotal=20000,
    )
    db_session.add(item)
    await db_session.flush()

    assert order.id is not None
    assert order.is_archived is False
    assert item.subtotal == 20000


@pytest.mark.asyncio
async def test_order_status_enum(db_session: AsyncSession):
    """Test order status enum values."""
    assert OrderStatus.PENDING.value == "pending"
    assert OrderStatus.PREPARING.value == "preparing"
    assert OrderStatus.COMPLETED.value == "completed"
