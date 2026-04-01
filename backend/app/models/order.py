"""Order and OrderItem models — synced with Unit 1."""

import enum
from datetime import datetime

from sqlalchemy import (
    CheckConstraint, DateTime, Enum, ForeignKey, Integer, String, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    COMPLETED = "completed"


class Order(TimestampMixin, Base):
    __tablename__ = "order"
    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="ck_order_total_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    store_code: Mapped[str] = mapped_column(
        String(20), ForeignKey("store.store_code", ondelete="RESTRICT"), nullable=False,
    )
    table_no: Mapped[int] = mapped_column(Integer, nullable=False)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("table_session.id", ondelete="RESTRICT"), nullable=False,
    )
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False, server_default="pending",
    )
    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None,
    )

    session = relationship("TableSession", back_populates="orders")
    items = relationship(
        "OrderItem", back_populates="order", lazy="selectin", cascade="all, delete-orphan",
    )

    @property
    def is_archived(self) -> bool:
        return self.archived_at is not None
