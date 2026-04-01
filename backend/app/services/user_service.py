"""User service — US-O11."""

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
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserUpdate

logger = structlog.get_logger()


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.db = db

    async def create_user(self, store_id: int, data: UserCreate) -> User:
        existing = await self.user_repo.get_by_username(store_id, data.username)
        if existing:
            raise DuplicateUserException()
        user = User(
            store_id=store_id,
            username=data.username,
            password_hash=hash_password(data.password),
            role=data.role,
        )
        user = await self.user_repo.create(user)
        await self.db.commit()
        logger.info("user_created", store_id=store_id, user_id=user.id)
        return user

    async def get_users(self, store_id: int) -> List[User]:
        return await self.user_repo.get_by_store(store_id)

    async def update_user(
        self, store_id: int, user_id: int, current_user_id: int, data: UserUpdate
    ) -> User:
        user = await self.user_repo.get_by_id(store_id, user_id)
        if not user:
            raise UserNotFoundException()

        # Cannot change own role
        if data.role and user_id == current_user_id:
            raise CannotChangeOwnRoleException()

        if data.username and data.username != user.username:
            dup = await self.user_repo.get_by_username(store_id, data.username)
            if dup:
                raise DuplicateUserException()
            user.username = data.username
        if data.password:
            user.password_hash = hash_password(data.password)
        if data.role:
            user.role = data.role
        await self.db.commit()
        return user

    async def delete_user(self, store_id: int, user_id: int, current_user_id: int) -> None:
        if user_id == current_user_id:
            raise CannotDeleteSelfException()

        user = await self.user_repo.get_by_id(store_id, user_id)
        if not user:
            raise UserNotFoundException()

        # Cannot delete last owner
        if user.role == "owner":
            owner_count = await self.user_repo.count_owners(store_id)
            if owner_count <= 1:
                raise LastOwnerException()

        user.is_active = False
        await self.db.commit()
        logger.info("user_deleted", store_id=store_id, user_id=user_id)
