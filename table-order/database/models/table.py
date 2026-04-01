"""RestaurantTable model."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class RestaurantTable(TimestampMixin, Base):
    """RestaurantTable entity - represents a physical table in a store."""

    __tablename__ = "restaurant_table"

    store_code: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("store.store_code", ondelete="RESTRICT"),
        primary_key=True,
        comment="소속 매장",
    )
    table_no: Mapped[int] = mapped_column(
        Integer, primary_key=True, comment="테이블 번호"
    )
    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="bcrypt 해싱된 PIN"
    )

    # Relationships
    store = relationship("Store", back_populates="tables")
    sessions = relationship("TableSession", back_populates="table", lazy="selectin")

    def __repr__(self) -> str:
        return (
            f"<RestaurantTable(store_code='{self.store_code}', "
            f"table_no={self.table_no})>"
        )
