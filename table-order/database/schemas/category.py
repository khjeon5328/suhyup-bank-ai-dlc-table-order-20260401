"""Category schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    """Category base fields."""

    name: str = Field(..., min_length=1, max_length=50, description="카테고리명")
    sort_order: int = Field(default=0, ge=0, description="노출 순서")


class CategoryCreate(CategoryBase):
    """Category creation request."""

    pass


class CategoryUpdate(BaseModel):
    """Category update request (all fields optional)."""

    name: str | None = Field(None, min_length=1, max_length=50)
    sort_order: int | None = Field(None, ge=0)


class CategoryResponse(CategoryBase):
    """Category response."""

    id: int
    store_code: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
