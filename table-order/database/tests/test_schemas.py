"""Tests for Pydantic schemas: validation rules."""

import pytest
from pydantic import ValidationError

from database.schemas.auth import AdminLoginRequest, TableLoginRequest
from database.schemas.menu import MenuCreate
from database.schemas.order import OrderCreate, OrderItemCreate
from database.schemas.store import StoreCreate
from database.schemas.table import TableCreate
from database.schemas.user import UserCreate
from database.models.user import UserRole


def test_store_create_valid():
    """Test valid store creation schema."""
    store = StoreCreate(store_code="PIZZA01", name="피자 매장")
    assert store.store_code == "PIZZA01"


def test_store_create_invalid_code():
    """Test store code validation (uppercase + digits only)."""
    with pytest.raises(ValidationError):
        StoreCreate(store_code="pizza01", name="피자 매장")


def test_user_create_valid():
    """Test valid user creation schema."""
    user = UserCreate(username="admin", role=UserRole.OWNER, password="password123")
    assert user.role == UserRole.OWNER


def test_user_create_short_password():
    """Test password minimum length validation."""
    with pytest.raises(ValidationError):
        UserCreate(username="admin", role=UserRole.OWNER, password="short")


def test_table_create_valid_pin():
    """Test valid table PIN (4-6 digits)."""
    table = TableCreate(table_no=1, password="1234")
    assert table.password == "1234"


def test_table_create_invalid_pin():
    """Test table PIN validation (digits only)."""
    with pytest.raises(ValidationError):
        TableCreate(table_no=1, password="abcd")


def test_menu_create_valid():
    """Test valid menu creation schema."""
    menu = MenuCreate(name="피자", price=15000, category_id=1)
    assert menu.price == 15000


def test_menu_create_negative_price():
    """Test menu price must be >= 0."""
    with pytest.raises(ValidationError):
        MenuCreate(name="피자", price=-1000, category_id=1)


def test_order_create_valid():
    """Test valid order creation schema."""
    order = OrderCreate(items=[OrderItemCreate(menu_id=1, quantity=2)])
    assert len(order.items) == 1


def test_order_create_empty_items():
    """Test order must have at least 1 item."""
    with pytest.raises(ValidationError):
        OrderCreate(items=[])


def test_order_item_zero_quantity():
    """Test order item quantity must be >= 1."""
    with pytest.raises(ValidationError):
        OrderItemCreate(menu_id=1, quantity=0)


def test_admin_login_request():
    """Test admin login request schema."""
    req = AdminLoginRequest(store_code="PIZZA01", username="admin", password="pass123")
    assert req.store_code == "PIZZA01"


def test_table_login_request():
    """Test table login request schema."""
    req = TableLoginRequest(store_code="PIZZA01", table_no=1, password="1234")
    assert req.table_no == 1
