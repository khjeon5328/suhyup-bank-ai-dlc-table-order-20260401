"""Table router."""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.dependencies import get_event_bus, require_admin, require_owner, verify_store_access
from app.core.event_bus import EventBus
from app.schemas.auth import TokenPayload
from app.schemas.table import SessionEndRequest, SessionEndResponse, TableCreate, TableResponse, TableSetupResponse
from app.services.table_service import TableService

router = APIRouter()


@router.get("", response_model=List[TableResponse])
async def get_tables(
    store_code: str = Depends(verify_store_access),
    user: TokenPayload = Depends(require_admin),
    db: AsyncSession = Depends(get_db_session),
):
    service = TableService(db, get_event_bus())
    tables = await service.get_tables(store_code)
    return [TableResponse.model_validate(t) for t in tables]


@router.post("", response_model=TableSetupResponse, status_code=201)
async def setup_table(
    data: TableCreate,
    store_code: str = Depends(verify_store_access),
    user: TokenPayload = Depends(require_owner),
    db: AsyncSession = Depends(get_db_session),
):
    service = TableService(db, get_event_bus())
    return await service.setup_table(store_code, data.table_no, data.password)


@router.post("/{table_no}/session/end", response_model=SessionEndResponse)
async def end_session(
    table_no: int,
    data: SessionEndRequest = SessionEndRequest(),
    store_code: str = Depends(verify_store_access),
    user: TokenPayload = Depends(require_admin),
    db: AsyncSession = Depends(get_db_session),
    bus: EventBus = Depends(get_event_bus),
):
    service = TableService(db, bus)
    return await service.end_session(store_code, table_no, data.force)
