"""User schemas — synced with Unit 1."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=8)
    role: str = Field(..., pattern="^(owner|manager)$")


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[str] = Field(None, pattern="^(owner|manager)$")


class UserResponse(BaseModel):
    id: int
    store_code: str
    username: str
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}
