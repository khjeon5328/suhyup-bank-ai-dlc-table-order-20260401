"""User model — synced with Unit 1."""

import enum

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, SoftDeleteMixin, TimestampMixin


class UserRole(str, enum.Enum):
    OWNER = "owner"
    MANAGER = "manager"


class User(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "user"
    __table_args__ = (
        UniqueConstraint("store_code", "username", name="uq_user_store_username"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    store_code: Mapped[str] = mapped_column(
        String(20), ForeignKey("store.store_code", ondelete="RESTRICT"), nullable=False,
    )
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, values_callable=lambda x: [e.value for e in x]), nullable=False,
    )

    store = relationship("Store", back_populates="users")
