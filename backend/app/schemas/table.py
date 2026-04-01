"""Table schemas — synced with Unit 1."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TableCreate(BaseModel):
    table_no: int = Field(..., ge=1)
    password: str = Field(..., min_length=4)


class TableResponse(BaseModel):
    store_code: str
    table_no: int
    created_at: datetime

    model_config = {"from_attributes": True}


class SessionResponse(BaseModel):
    id: int
    store_code: str
    table_no: int
    started_at: datetime
    ended_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

    @property
    def is_active(self) -> bool:
        return self.ended_at is None


class TableSetupResponse(BaseModel):
    table: TableResponse
    session: SessionResponse


class SessionEndRequest(BaseModel):
    force: bool = False


class SessionEndResponse(BaseModel):
    old_session: SessionResponse
    new_session: SessionResponse
    archived_orders: int
