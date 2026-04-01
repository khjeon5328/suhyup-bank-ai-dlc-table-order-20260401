"""SSE events router — admin and table event streams."""

from fastapi import APIRouter, Depends, Request
from starlette.responses import StreamingResponse

from app.core.dependencies import get_sse_manager, require_admin, require_table, verify_store_access
from app.core.sse_manager import SSEManager
from app.schemas.auth import TokenPayload

router = APIRouter()


@router.get("/admin")
async def admin_sse_stream(
    request: Request,
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_admin),
    manager: SSEManager = Depends(get_sse_manager),
):
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
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_table),
    manager: SSEManager = Depends(get_sse_manager),
):
    async def event_generator():
        async for event_str in manager.stream_table(store_id, table_id):
            if await request.is_disconnected():
                break
            yield event_str

    return StreamingResponse(event_generator(), media_type="text/event-stream")
