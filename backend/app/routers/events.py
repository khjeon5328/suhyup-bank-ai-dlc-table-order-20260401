"""SSE events router — supports query param token for EventSource clients."""

from typing import Optional

import jwt
from fastapi import APIRouter, Depends, Query, Request
from starlette.responses import StreamingResponse

from app.config import settings
from app.core.dependencies import get_sse_manager
from app.core.exceptions import InsufficientPermissionException, InvalidCredentialsException, TokenExpiredException
from app.core.sse_manager import SSEManager
from app.schemas.auth import TokenPayload

router = APIRouter()


def _decode_token(token: Optional[str]) -> TokenPayload:
    """Decode JWT from query param (EventSource cannot send headers)."""
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
    store_code: str,
    token: Optional[str] = Query(None),
    manager: SSEManager = Depends(get_sse_manager),
):
    user = _decode_token(token)
    if user.role not in ("owner", "manager"):
        raise InsufficientPermissionException()
    if user.store_code != store_code:
        raise InsufficientPermissionException()

    async def event_generator():
        async for event_str in manager.stream_admin(store_code):
            if await request.is_disconnected():
                break
            yield event_str
    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/table/{table_no}")
async def table_sse_stream(
    table_no: int,
    request: Request,
    store_code: str,
    token: Optional[str] = Query(None),
    manager: SSEManager = Depends(get_sse_manager),
):
    user = _decode_token(token)
    if user.role != "table":
        raise InsufficientPermissionException()
    if user.store_code != store_code:
        raise InsufficientPermissionException()

    async def event_generator():
        async for event_str in manager.stream_table(store_code, table_no):
            if await request.is_disconnected():
                break
            yield event_str
    return StreamingResponse(event_generator(), media_type="text/event-stream")
