"""Store model."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Store(TimestampMixin, Base):
    """Store entity - represents a restaurant/shop."""

    __tablename__ = "store"

    store_code: Mapped[str] = mapped_column(
        String(20), primary_key=True, comment="매장 고유 코드"
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="매장명")
    address: Mapped[str | None] = mapped_column(
        String(255), nullable=True, comment="매장 주소"
    )
    phone: Mapped[str | None] = mapped_column(
        String(20), nullable=True, comment="매장 전화번호"
    )

    # Relationships
    users = relationship("User", back_populates="store", lazy="selectin")
    tables = relationship("RestaurantTable", back_populates="store", lazy="selectin")
    categories = relationship("Category", back_populates="store", lazy="selectin")
    menus = relationship("Menu", back_populates="store", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Store(store_code='{self.store_code}', name='{self.name}')>"
