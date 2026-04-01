"""Category model."""

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class Category(TimestampMixin, Base):
    """Category entity - represents a menu category in a store."""

    __tablename__ = "category"
    __table_args__ = (
        UniqueConstraint("store_code", "name", name="uq_category_store_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    store_code: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("store.store_code", ondelete="RESTRICT"),
        nullable=False,
        comment="소속 매장",
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="카테고리명"
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="노출 순서"
    )

    # Relationships
    store = relationship("Store", back_populates="categories")
    menus = relationship("Menu", back_populates="category", lazy="selectin")

    def __repr__(self) -> str:
        return (
            f"<Category(id={self.id}, store_code='{self.store_code}', "
            f"name='{self.name}')>"
        )
