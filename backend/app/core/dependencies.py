"""FastAPI dependency injection — synced with Unit 1 (store_code based)."""

from typing import Optional

import jwt
import structlog
from fastapi import Depends, Path
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.database import get_db_session
from app.core.event_bus import EventBus, event_bus
from app.core.exceptions import (
    ForbiddenException,
    InsufficientPermissionException,
    InvalidCredentialsException,
    TokenExpiredException,
)
from app.core.sse_manager import SSEManager, sse_manager
from app.schemas.auth import TokenPayload

logger = structlog.get_logger()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/admin", auto_error=False)


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)) -> TokenPayload:
    if not token:
        raise InvalidCredentialsException()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException()
    except (jwt.InvalidTokenError, Exception):
        raise InvalidCredentialsException()


async def require_owner(user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
    if user.role != "owner":
        raise InsufficientPermissionException()
    return user


async def require_admin(user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
    if user.role not in ("owner", "manager"):
        raise InsufficientPermissionException()
    return user


async def require_table(token: Optional[str] = Depends(oauth2_scheme)) -> TokenPayload:
    if not token:
        raise InvalidCredentialsException()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        tp = TokenPayload(**payload)
        if tp.role != "table":
            raise InsufficientPermissionException()
        return tp
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException()
    except (jwt.InvalidTokenError, Exception) as e:
        if isinstance(e, (InsufficientPermissionException, TokenExpiredException)):
            raise
        raise InvalidCredentialsException()


async def verify_store_access(
    store_code: str = Path(...),
    user: TokenPayload = Depends(get_current_user),
) -> str:
    if user.store_code != store_code:
        raise ForbiddenException("매장 접근 권한이 없습니다.")
    return store_code


def get_event_bus() -> EventBus:
    return event_bus


def get_sse_manager() -> SSEManager:
    return sse_manager
