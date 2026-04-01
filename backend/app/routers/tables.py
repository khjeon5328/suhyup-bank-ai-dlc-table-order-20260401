"""Table router — tables CRUD, session management, order history."""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.dependencies import get_event_bus, require_admin, require_owner, verify_store_access
from app.core.event_bus import EventBus
from app.schemas.auth import TokenPayload
from app.schemas.order import OrderHistoryResponse
from app.schemas.table import (
    SessionEndRequest,
    SessionEndResponse,
    TableCreate,
    TableResponse,
    TableSetupResponse,
)
from app.services.order_service import OrderService
from app.services.table_service import TableService

router = APIRouter()


@router.get("/", response_model=List[TableResponse])
async def get_tables(
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_admin),
    db: AsyncSession = Depends(get_db_session),
):
    service = TableService(db, get_event_bus())
    tables = await service.get_tables(store_id)
    return [TableResponse.model_validate(t) for t in tables]


@router.post("/", response_model=TableSetupResponse, status_code=201)
async def setup_table(
    data: TableCreate,
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_owner),
    db: AsyncSession = Depends(get_db_session),
):
    service = TableService(db, get_event_bus())
    return await service.setup_table(store_id, data.table_no, data.password)


@router.post("/{table_id}/session/end", response_model=SessionEndResponse)
async def end_session(
    table_id: int,
    data: SessionEndRequest = SessionEndRequest(),
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_admin),
    db: AsyncSession = Depends(get_db_session),
    bus: EventBus = Depends(get_event_bus),
):
    service = TableService(db, bus)
    return await service.end_session(store_id, table_id, data.force)


@router.get("/{table_id}/history", response_model=List[OrderHistoryResponse])
async def get_table_history(
    table_id: int,
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_admin),
    db: AsyncSession = Depends(get_db_session),
):
    service = OrderService(db, get_event_bus())
    return await service.get_order_history(store_id, table_id, date_from, date_to)
