"""RestaurantTable model — synced with Unit 1."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class RestaurantTable(TimestampMixin, Base):
    __tablename__ = "restaurant_table"

    store_code: Mapped[str] = mapped_column(
        String(20), ForeignKey("store.store_code", ondelete="RESTRICT"), primary_key=True,
    )
    table_no: Mapped[int] = mapped_column(Integer, primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    store = relationship("Store", back_populates="tables")
    sessions = relationship("TableSession", back_populates="table", lazy="selectin")
