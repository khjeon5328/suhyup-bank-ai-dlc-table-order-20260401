"""TableSession model — synced with Unit 1."""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKeyConstraint, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TableSession(Base):
    __tablename__ = "table_session"
    __table_args__ = (
        ForeignKeyConstraint(
            ["store_code", "table_no"],
            ["restaurant_table.store_code", "restaurant_table.table_no"],
            ondelete="RESTRICT",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    store_code: Mapped[str] = mapped_column(String(20), nullable=False)
    table_no: Mapped[int] = mapped_column(Integer, nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(),
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(),
    )

    table = relationship("RestaurantTable", back_populates="sessions")
    orders = relationship("Order", back_populates="session", lazy="selectin")

    @property
    def is_active(self) -> bool:
        return self.ended_at is None
