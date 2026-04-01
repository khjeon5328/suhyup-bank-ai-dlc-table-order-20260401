"""Order and OrderItem models."""

import enum
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class OrderStatus(str, enum.Enum):
    """Order status enum."""

    PENDING = "pending"
    PREPARING = "preparing"
    COMPLETED = "completed"


class Order(TimestampMixin, Base):
    """Order entity - represents a customer order."""

    __tablename__ = "order"
    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="ck_order_total_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    store_code: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("store.store_code", ondelete="RESTRICT"),
        nullable=False,
        comment="매장 코드",
    )
    table_no: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="테이블 번호"
    )
    session_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("table_session.id", ondelete="RESTRICT"),
        nullable=False,
        comment="세션 ID",
    )
    total_amount: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="총 주문 금액 (원)"
    )
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        nullable=False,
        server_default="pending",
        comment="주문 상태",
    )
    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None, comment="아카이브 시각"
    )

    # Relationships
    session = relationship("TableSession", back_populates="orders")
    items = relationship(
        "OrderItem", back_populates="order", lazy="selectin", cascade="all, delete-orphan"
    )

    @property
    def is_archived(self) -> bool:
        """Check if the order is archived."""
        return self.archived_at is not None

    def __repr__(self) -> str:
        return (
            f"<Order(id={self.id}, store_code='{self.store_code}', "
            f"table_no={self.table_no}, status='{self.status.value}', "
            f"total={self.total_amount})>"
        )


class OrderItem(Base):
    """OrderItem entity - represents a single item in an order."""

    __tablename__ = "order_item"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_orderitem_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="ck_orderitem_price_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("order.id", ondelete="CASCADE"),
        nullable=False,
        comment="주문 ID",
    )
    menu_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("menu.id", ondelete="RESTRICT"),
        nullable=False,
        comment="메뉴 ID",
    )
    menu_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="주문 시점 메뉴명 (스냅샷)"
    )
    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="수량"
    )
    unit_price: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="주문 시점 단가 (스냅샷)"
    )
    subtotal: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="소계"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), comment="생성 시각"
    )

    # Relationships
    order = relationship("Order", back_populates="items")

    def __repr__(self) -> str:
        return (
            f"<OrderItem(id={self.id}, order_id={self.order_id}, "
            f"menu_name='{self.menu_name}', qty={self.quantity})>"
        )
