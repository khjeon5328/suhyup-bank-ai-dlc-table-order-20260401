"""Store schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class StoreBase(BaseModel):
    """Store base fields."""

    name: str = Field(..., min_length=1, max_length=100, description="매장명")
    address: str | None = Field(None, max_length=255, description="매장 주소")
    phone: str | None = Field(None, max_length=20, description="매장 전화번호")


class StoreCreate(StoreBase):
    """Store creation request."""

    store_code: str = Field(
        ..., min_length=1, max_length=20, pattern=r"^[A-Z0-9]+$",
        description="매장 고유 코드",
    )


class StoreResponse(StoreBase):
    """Store response."""

    store_code: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
