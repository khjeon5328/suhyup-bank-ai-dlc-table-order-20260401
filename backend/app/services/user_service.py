"""User service — synced with Unit 1."""

from datetime import datetime
from typing import List

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    CannotChangeOwnRoleException,
    CannotDeleteSelfException,
    DuplicateUserException,
    LastOwnerException,
    UserNotFoundException,
)
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate

logger = structlog.get_logger()


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.db = db

    async def create_user(self, store_code: str, data: UserCreate) -> User:
        existing = await self.user_repo.get_by_username(store_code, data.username)
        if existing:
            raise DuplicateUserException()
        user = User(
            store_code=store_code, username=data.username,
            password_hash=hash_password(data.password), role=UserRole(data.role),
        )
        user = await self.user_repo.create(user)
        await self.db.commit()
        logger.info("user_created", store_code=store_code, user_id=user.id)
        return user

    async def get_users(self, store_code: str) -> List[User]:
        return await self.user_repo.get_by_store(store_code)

    async def update_user(
        self, store_code: str, user_id: int, current_user_id: int, data: UserUpdate,
    ) -> User:
        user = await self.user_repo.get_by_id(store_code, user_id)
        if not user:
            raise UserNotFoundException()
        if data.role and user_id == current_user_id:
            raise CannotChangeOwnRoleException()
        if data.username and data.username != user.username:
            dup = await self.user_repo.get_by_username(store_code, data.username)
            if dup:
                raise DuplicateUserException()
            user.username = data.username
        if data.password:
            user.password_hash = hash_password(data.password)
        if data.role:
            user.role = UserRole(data.role)
        await self.db.commit()
        return user

    async def delete_user(self, store_code: str, user_id: int, current_user_id: int) -> None:
        if user_id == current_user_id:
            raise CannotDeleteSelfException()
        user = await self.user_repo.get_by_id(store_code, user_id)
        if not user:
            raise UserNotFoundException()
        if user.role == UserRole.OWNER:
            owner_count = await self.user_repo.count_owners(store_code)
            if owner_count <= 1:
                raise LastOwnerException()
        user.deleted_at = datetime.utcnow()
        await self.db.commit()
        logger.info("user_deleted", store_code=store_code, user_id=user_id)
