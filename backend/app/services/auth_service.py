"""Authentication service — US-O01, US-M01, US-C01."""

from datetime import timedelta

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.exceptions import (
    AccountLockedException,
    InvalidCredentialsException,
    RateLimitException,
    StoreNotFoundException,
    TableNotFoundException,
)
from app.core.security import create_access_token, verify_password
from app.models.login_attempt import LoginAttempt
from app.repositories.login_attempt_repo import LoginAttemptRepository
from app.repositories.session_repo import SessionRepository
from app.repositories.store_repo import StoreRepository
from app.repositories.table_repo import TableRepository
from app.repositories.user_repo import UserRepository
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
        self.login_attempt_repo = LoginAttemptRepository(db)
        self.db = db

    async def login_admin(
        self, store_code: str, username: str, password: str, ip_address: str
    ) -> AdminLoginResponse:
        # Brute-force check: IP
        ip_failures = await self.login_attempt_repo.count_recent_by_ip(ip_address)
        if ip_failures >= 20:
            raise RateLimitException("IP 기반 로그인 시도 횟수를 초과했습니다.")

        # Find store
        store = await self.store_repo.get_by_code(store_code)
        if not store:
            await self._record_attempt(None, username, ip_address, False)
            raise InvalidCredentialsException()

        # Brute-force check: account
        account_failures = await self.login_attempt_repo.count_recent_by_account(
            store.id, username
        )
        if account_failures >= 5:
            raise AccountLockedException()

        # Find user
        user = await self.user_repo.get_by_username(store.id, username)
        if not user or not verify_password(password, user.password_hash):
            await self._record_attempt(store.id, username, ip_address, False)
            await self.db.commit()
            raise InvalidCredentialsException()

        # Success
        await self._record_attempt(store.id, username, ip_address, True)
        token = create_access_token(
            data={"user_id": user.id, "store_id": store.id, "role": user.role},
            expires_delta=timedelta(hours=settings.JWT_ADMIN_EXPIRE_HOURS),
        )
        await self.db.commit()

        logger.info("admin_login_success", store_id=store.id, username=username)
        return AdminLoginResponse(
            access_token=token,
            expires_in=settings.JWT_ADMIN_EXPIRE_HOURS * 3600,
            user=UserInfo(id=user.id, username=user.username, role=user.role, store_id=store.id),
        )

    async def login_table(
        self, store_code: str, table_no: int, password: str
    ) -> TableLoginResponse:
        store = await self.store_repo.get_by_code(store_code)
        if not store:
            raise StoreNotFoundException()

        table = await self.table_repo.get_by_store_and_no(store.id, table_no)
        if not table or not verify_password(password, table.password_hash):
            raise InvalidCredentialsException()

        session = await self.session_repo.get_active(table.id)
        if not session:
            raise InvalidCredentialsException("활성 세션이 없습니다.")

        token = create_access_token(
            data={
                "table_id": table.id,
                "store_id": store.id,
                "session_id": session.id,
                "role": "table",
            }
        )

        logger.info("table_login_success", store_id=store.id, table_no=table_no)
        return TableLoginResponse(
            access_token=token,
            table=TableInfo(
                id=table.id, table_no=table.table_no, store_id=store.id, session_id=session.id
            ),
        )

    async def _record_attempt(
        self, store_id: int | None, username: str, ip_address: str, success: bool
    ) -> None:
        attempt = LoginAttempt(
            store_id=store_id, username=username, ip_address=ip_address, success=success
        )
        await self.login_attempt_repo.create(attempt)
