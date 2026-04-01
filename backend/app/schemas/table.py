"""Table schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TableCreate(BaseModel):
    table_no: int = Field(..., ge=1)
    password: str = Field(..., min_length=4)


class TableResponse(BaseModel):
    id: int
    store_id: int
    table_no: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class SessionResponse(BaseModel):
    id: int
    store_id: int
    table_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    is_active: bool

    model_config = {"from_attributes": True}


class TableSetupResponse(BaseModel):
    table: TableResponse
    session: SessionResponse


class SessionEndRequest(BaseModel):
    force: bool = False


class SessionEndResponse(BaseModel):
    old_session: SessionResponse
    new_session: SessionResponse
    archived_orders: int


class PendingOrdersWarning(BaseModel):
    warning: str
    pending_orders: List[dict]
