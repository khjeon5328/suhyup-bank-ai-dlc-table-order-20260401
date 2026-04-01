"""User repository with soft delete filter."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User entity with soft delete support."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_by_username(
        self, store_code: str, username: str, include_deleted: bool = False
    ) -> User | None:
        """Get user by store_code and username."""
        stmt = select(User).where(
            User.store_code == store_code,
            User.username == username,
        )
        if not include_deleted:
            stmt = stmt.where(User.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_users(self, store_code: str) -> list[User]:
        """Get all active (non-deleted) users for a store."""
        stmt = (
            select(User)
            .where(User.store_code == store_code, User.deleted_at.is_(None))
            .order_by(User.id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_active_by_id(self, user_id: int) -> User | None:
        """Get active user by ID."""
        stmt = select(User).where(User.id == user_id, User.deleted_at.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def soft_delete(self, user: User) -> User:
        """Soft delete a user by setting deleted_at."""
        from datetime import datetime, timezone

        user.deleted_at = datetime.now(timezone.utc)
        await self.session.flush()
        await self.session.refresh(user)
        return user
