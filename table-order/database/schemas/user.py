"""User schemas."""

from datetime import datetime

from pydantic import BaseModel, Field

from ..models.user import UserRole


class UserBase(BaseModel):
    """User base fields."""

    username: str = Field(..., min_length=1, max_length=50, description="사용자명")
    role: UserRole = Field(..., description="역할")


class UserCreate(UserBase):
    """User creation request."""

    password: str = Field(..., min_length=8, description="비밀번호")


class UserUpdate(BaseModel):
    """User update request (all fields optional)."""

    username: str | None = Field(None, min_length=1, max_length=50)
    role: UserRole | None = None
    password: str | None = Field(None, min_length=8)


class UserResponse(UserBase):
    """User response (excludes password_hash)."""

    id: int
    store_code: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
