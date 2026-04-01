"""Store model — synced with Unit 1."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Store(TimestampMixin, Base):
    __tablename__ = "store"

    store_code: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    users = relationship("User", back_populates="store", lazy="selectin")
    tables = relationship("RestaurantTable", back_populates="store", lazy="selectin")
    categories = relationship("Category", back_populates="store", lazy="selectin")
    menus = relationship("Menu", back_populates="store", lazy="selectin")
