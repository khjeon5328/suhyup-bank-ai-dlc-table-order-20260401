"""Menu schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    """Menu base fields."""

    name: str = Field(..., min_length=1, max_length=100, description="메뉴명")
    price: int = Field(..., ge=0, description="가격 (원)")
    description: str | None = Field(None, description="메뉴 설명")
    category_id: int = Field(..., description="카테고리 ID")
    image_url: str | None = Field(None, max_length=500, description="이미지 URL")
    sort_order: int = Field(default=0, ge=0, description="노출 순서")


class MenuCreate(MenuBase):
    """Menu creation request."""

    pass


class MenuUpdate(BaseModel):
    """Menu update request (all fields optional)."""

    name: str | None = Field(None, min_length=1, max_length=100)
    price: int | None = Field(None, ge=0)
    description: str | None = None
    category_id: int | None = None
    image_url: str | None = Field(None, max_length=500)
    sort_order: int | None = Field(None, ge=0)


class MenuResponse(MenuBase):
    """Menu response."""

    id: int
    store_code: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MenuOrderItem(BaseModel):
    """Single menu sort order update."""

    menu_id: int
    sort_order: int = Field(..., ge=0)


class MenuOrderUpdate(BaseModel):
    """Batch menu sort order update request."""

    items: list[MenuOrderItem]
