"""Authentication service — synced with Unit 1."""

from datetime import timedelta

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import (
    InvalidCredentialsException,
    StoreNotFoundException,
)
from app.core.security import create_access_token, verify_password
from app.repositories.session_repo import SessionRepository
from app.repositories.store_repo import StoreRepository
from app.repositories.table_repo import TableRepository
from app.repositories.user_repo import UserRepository
from app.models.table_session import TableSession
from app.schemas.auth import (
    AdminLoginResponse,
    TableInfo,
    TableLoginResponse,
    UserInfo,
)

logger = structlog.get_logger()


class AuthService:
    def __init__(self, db: AsyncSession):
        self.store_repo = StoreRepository(db)
        self.user_repo = UserRepository(db)
        self.table_repo = TableRepository(db)
        self.session_repo = SessionRepository(db)
        self.db = db

    async def login_admin(
        self, store_code: str, username: str, password: str,
    ) -> AdminLoginResponse:
        store = await self.store_repo.get_by_code(store_code)
        if not store:
            raise InvalidCredentialsException()

        user = await self.user_repo.get_by_username(store_code, username)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsException()

        token = create_access_token(
            data={"user_id": user.id, "store_code": store_code, "role": user.role.value},
            expires_delta=timedelta(hours=settings.JWT_ADMIN_EXPIRE_HOURS),
        )

        logger.info("admin_login_success", store_code=store_code, username=username)
        return AdminLoginResponse(
            access_token=token,
            expires_in=settings.JWT_ADMIN_EXPIRE_HOURS * 3600,
            user=UserInfo(id=user.id, username=user.username, role=user.role.value, store_code=store_code),
        )

    async def login_table(
        self, store_code: str, table_no: int, password: str,
    ) -> TableLoginResponse:
        store = await self.store_repo.get_by_code(store_code)
        if not store:
            raise StoreNotFoundException()

        table = await self.table_repo.get_by_pk(store_code, table_no)
        if not table or not verify_password(password, table.password_hash):
            raise InvalidCredentialsException()

        session = await self.session_repo.get_active(store_code, table_no)
        if not session:
            session = await self.session_repo.create(
                TableSession(store_code=store_code, table_no=table_no)
            )
            await self.db.commit()

        token = create_access_token(
            data={
                "table_no": table_no,
                "store_code": store_code,
                "session_id": session.id,
                "role": "table",
            }
        )

        logger.info("table_login_success", store_code=store_code, table_no=table_no)
        return TableLoginResponse(
            access_token=token,
            table=TableInfo(store_code=store_code, table_no=table_no, session_id=session.id),
        )
