"""User repository — synced with Unit 1."""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, store_code: str, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(
                User.id == user_id, User.store_code == store_code, User.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, store_code: str, username: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(
                User.store_code == store_code, User.username == username, User.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()

    async def get_by_store(self, store_code: str) -> List[User]:
        result = await self.db.execute(
            select(User).where(User.store_code == store_code, User.deleted_at.is_(None))
        )
        return list(result.scalars().all())

    async def count_owners(self, store_code: str) -> int:
        result = await self.db.execute(
            select(func.count()).where(
                User.store_code == store_code, User.role == "owner", User.deleted_at.is_(None)
            )
        )
        return result.scalar_one()
