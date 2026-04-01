"""User model."""

import enum

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin


class UserRole(str, enum.Enum):
    """User role enum."""

    OWNER = "owner"
    MANAGER = "manager"


class User(TimestampMixin, SoftDeleteMixin, Base):
    """User entity - represents an admin account (owner or manager)."""

    __tablename__ = "user"
    __table_args__ = (
        UniqueConstraint(
            "store_code", "username", name="uq_user_store_username"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    store_code: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("store.store_code", ondelete="RESTRICT"),
        nullable=False,
        comment="소속 매장",
    )
    username: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="사용자명"
    )
    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="bcrypt 해싱된 비밀번호"
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), nullable=False, comment="역할 (owner/manager)"
    )

    # Relationships
    store = relationship("Store", back_populates="users")

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, store_code='{self.store_code}', "
            f"username='{self.username}', role='{self.role.value}')>"
        )
