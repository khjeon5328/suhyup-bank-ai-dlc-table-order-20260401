"""TableSession model."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, ForeignKeyConstraint, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class TableSession(Base):
    """TableSession entity - represents a customer session at a table."""

    __tablename__ = "table_session"
    __table_args__ = (
        ForeignKeyConstraint(
            ["store_code", "table_no"],
            ["restaurant_table.store_code", "restaurant_table.table_no"],
            ondelete="RESTRICT",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    store_code: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="매장 코드"
    )
    table_no: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="테이블 번호"
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), comment="세션 시작 시각"
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, default=None, comment="세션 종료 시각"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), comment="레코드 생성 시각"
    )

    # Relationships
    table = relationship("RestaurantTable", back_populates="sessions")
    orders = relationship("Order", back_populates="session", lazy="selectin")

    @property
    def is_active(self) -> bool:
        """Check if the session is currently active."""
        return self.ended_at is None

    def __repr__(self) -> str:
        status = "ACTIVE" if self.is_active else "COMPLETED"
        return (
            f"<TableSession(id={self.id}, store_code='{self.store_code}', "
            f"table_no={self.table_no}, status={status})>"
        )
