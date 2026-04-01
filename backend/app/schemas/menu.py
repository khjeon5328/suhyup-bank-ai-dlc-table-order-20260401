"""Menu and Category schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# Category
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    sort_order: Optional[int] = Field(None, ge=0)


class CategoryResponse(BaseModel):
    id: int
    store_id: int
    name: str
    sort_order: int
    is_active: bool

    model_config = {"from_attributes": True}


# Menu
class MenuCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: int = Field(..., ge=0)
    category_id: int
    description: Optional[str] = Field(None, max_length=1000)
    image_url: Optional[str] = Field(None, max_length=500)


class MenuUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None
    description: Optional[str] = Field(None, max_length=1000)
    image_url: Optional[str] = Field(None, max_length=500)
    sort_order: Optional[int] = Field(None, ge=0)


class MenuResponse(BaseModel):
    id: int
    store_id: int
    category_id: int
    name: str
    price: int
    description: Optional[str] = None
    image_url: Optional[str] = None
    sort_order: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class MenuOrderItem(BaseModel):
    menu_id: int
    sort_order: int


class MenuOrderUpdate(BaseModel):
    items: List[MenuOrderItem]
