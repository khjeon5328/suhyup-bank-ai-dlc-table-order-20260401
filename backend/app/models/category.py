"""Category model — synced with Unit 1."""

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Category(TimestampMixin, Base):
    __tablename__ = "category"
    __table_args__ = (
        UniqueConstraint("store_code", "name", name="uq_category_store_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    store_code: Mapped[str] = mapped_column(
        String(20), ForeignKey("store.store_code", ondelete="RESTRICT"), nullable=False,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    store = relationship("Store", back_populates="categories")
    menus = relationship("Menu", back_populates="category", lazy="selectin")
