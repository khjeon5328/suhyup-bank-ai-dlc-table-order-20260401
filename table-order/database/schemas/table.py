"""RestaurantTable schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class TableCreate(BaseModel):
    """Table creation/setup request."""

    table_no: int = Field(..., ge=1, description="테이블 번호")
    password: str = Field(
        ..., min_length=4, max_length=6, pattern=r"^\d+$",
        description="4~6자리 숫자 PIN",
    )


class TableResponse(BaseModel):
    """Table response."""

    store_code: str
    table_no: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
