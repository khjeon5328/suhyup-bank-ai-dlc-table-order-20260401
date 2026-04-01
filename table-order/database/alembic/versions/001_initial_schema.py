"""Initial schema - all tables.

Revision ID: 001
Revises: None
Create Date: 2026-04-01
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Store
    op.create_table(
        "store",
        sa.Column("store_code", sa.String(20), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("address", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )

    # User
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("store_code", sa.String(20), sa.ForeignKey("store.store_code", ondelete="RESTRICT"), nullable=False),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum("owner", "manager", name="userrole"), nullable=False),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("store_code", "username", name="uq_user_store_username"),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )

    # RestaurantTable
    op.create_table(
        "restaurant_table",
        sa.Column("store_code", sa.String(20), sa.ForeignKey("store.store_code", ondelete="RESTRICT"), primary_key=True),
        sa.Column("table_no", sa.Integer, primary_key=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )

    # TableSession
    op.create_table(
        "table_session",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("store_code", sa.String(20), nullable=False),
        sa.Column("table_no", sa.Integer, nullable=False),
        sa.Column("started_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("ended_at", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(
            ["store_code", "table_no"],
            ["restaurant_table.store_code", "restaurant_table.table_no"],
            ondelete="RESTRICT",
        ),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )
    op.create_index("ix_session_active", "table_session", ["store_code", "table_no", "ended_at"])

    # Category
    op.create_table(
        "category",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("store_code", sa.String(20), sa.ForeignKey("store.store_code", ondelete="RESTRICT"), nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("sort_order", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("store_code", "name", name="uq_category_store_name"),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )

    # Menu
    op.create_table(
        "menu",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("store_code", sa.String(20), sa.ForeignKey("store.store_code", ondelete="RESTRICT"), nullable=False),
        sa.Column("category_id", sa.Integer, sa.ForeignKey("category.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("price", sa.Integer, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("image_url", sa.String(500), nullable=True),
        sa.Column("sort_order", sa.Integer, nullable=False, server_default="0"),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("price >= 0", name="ck_menu_price_positive"),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )
    op.create_index("ix_menu_store_category", "menu", ["store_code", "category_id", "sort_order"])

    # Order
    op.create_table(
        "order",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("store_code", sa.String(20), sa.ForeignKey("store.store_code", ondelete="RESTRICT"), nullable=False),
        sa.Column("table_no", sa.Integer, nullable=False),
        sa.Column("session_id", sa.Integer, sa.ForeignKey("table_session.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("total_amount", sa.Integer, nullable=False),
        sa.Column("status", sa.Enum("pending", "preparing", "completed", name="orderstatus"), nullable=False, server_default="pending"),
        sa.Column("archived_at", sa.DateTime, nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("total_amount >= 0", name="ck_order_total_positive"),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )
    op.create_index("ix_order_store_archived", "order", ["store_code", "archived_at", "created_at"])
    op.create_index("ix_order_store_table", "order", ["store_code", "table_no", "archived_at"])

    # OrderItem
    op.create_table(
        "order_item",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("order.id", ondelete="CASCADE"), nullable=False),
        sa.Column("menu_id", sa.Integer, sa.ForeignKey("menu.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("menu_name", sa.String(100), nullable=False),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("unit_price", sa.Integer, nullable=False),
        sa.Column("subtotal", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("quantity > 0", name="ck_orderitem_quantity_positive"),
        sa.CheckConstraint("unit_price >= 0", name="ck_orderitem_price_positive"),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )


def downgrade() -> None:
    op.drop_table("order_item")
    op.drop_table("order")
    op.drop_table("menu")
    op.drop_table("category")
    op.drop_table("table_session")
    op.drop_table("restaurant_table")
    op.drop_table("user")
    op.drop_table("store")
    op.execute("DROP TYPE IF EXISTS userrole")
    op.execute("DROP TYPE IF EXISTS orderstatus")
