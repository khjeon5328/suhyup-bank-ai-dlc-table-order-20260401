"""Menu model."""

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin


class Menu(TimestampMixin, SoftDeleteMixin, Base):
    """Menu entity - represents a menu item in a store."""

    __tablename__ = "menu"
    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_menu_price_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    store_code: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("store.store_code", ondelete="RESTRICT"),
        nullable=False,
        comment="소속 매장",
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("category.id", ondelete="RESTRICT"),
        nullable=False,
        comment="카테고리",
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="메뉴명"
    )
    price: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="가격 (원)"
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="메뉴 설명"
    )
    image_url: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="메뉴 이미지 URL"
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, comment="노출 순서"
    )

    # Relationships
    store = relationship("Store", back_populates="menus")
    category = relationship("Category", back_populates="menus")

    def __repr__(self) -> str:
        return (
            f"<Menu(id={self.id}, store_code='{self.store_code}', "
            f"name='{self.name}', price={self.price})>"
        )
