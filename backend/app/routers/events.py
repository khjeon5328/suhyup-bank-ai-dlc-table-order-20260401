"""SSE events router — admin and table event streams."""

from typing import Optional

import jwt
from fastapi import APIRouter, Depends, Path, Query, Request
from starlette.responses import StreamingResponse

from app.config import settings
from app.core.dependencies import get_sse_manager
from app.core.exceptions import ForbiddenException, InsufficientPermissionException, InvalidCredentialsException, TokenExpiredException
from app.core.sse_manager import SSEManager
from app.schemas.auth import TokenPayload

router = APIRouter()


def _decode_token(token: Optional[str]) -> TokenPayload:
    """Decode JWT from query parameter (EventSource cannot send headers)."""
    if not token:
        raise InvalidCredentialsException()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException()
    except (jwt.InvalidTokenError, Exception):
        raise InvalidCredentialsException()


@router.get("/admin")
async def admin_sse_stream(
    request: Request,
    store_id: int = Path(...),
    token: Optional[str] = Query(None),
    manager: SSEManager = Depends(get_sse_manager),
):
    user = _decode_token(token)
    if user.role not in ("owner", "manager"):
        raise InsufficientPermissionException()
    if user.store_id != store_id:
        raise ForbiddenException("매장 접근 권한이 없습니다.")

    async def event_generator():
        async for event_str in manager.stream_admin(store_id):
            if await request.is_disconnected():
                break
            yield event_str

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/table/{table_id}")
async def table_sse_stream(
    table_id: int,
    request: Request,
    store_id: int = Path(...),
    token: Optional[str] = Query(None),
    manager: SSEManager = Depends(get_sse_manager),
):
    user = _decode_token(token)
    if user.role != "table":
        raise InsufficientPermissionException()
    if user.store_id != store_id:
        raise ForbiddenException("매장 접근 권한이 없습니다.")

    async def event_generator():
        async for event_str in manager.stream_table(store_id, table_id):
            if await request.is_disconnected():
                break
            yield event_str

    return StreamingResponse(event_generator(), media_type="text/event-stream")
