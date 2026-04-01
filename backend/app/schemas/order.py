"""Order schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    menu_id: int
    quantity: int = Field(..., ge=1)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(..., min_length=1)


class OrderItemResponse(BaseModel):
    id: int
    menu_id: int
    menu_name: str
    quantity: int
    unit_price: int
    subtotal: int

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    store_id: int
    table_id: int
    session_id: int
    order_no: str
    total_amount: int
    status: str
    items: List[OrderItemResponse] = []
    created_at: datetime

    model_config = {"from_attributes": True}


class OrderStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|preparing|completed)$")


class OrderHistoryResponse(BaseModel):
    id: int
    store_id: int
    table_id: int
    original_order_id: int
    order_no: str
    order_data: dict
    total_amount: int
    status: str
    ordered_at: datetime
    archived_at: datetime

    model_config = {"from_attributes": True}
