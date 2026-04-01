"""Order and OrderItem schemas."""

from datetime import datetime

from pydantic import BaseModel, Field

from ..models.order import OrderStatus


class OrderItemCreate(BaseModel):
    """Order item creation request."""

    menu_id: int = Field(..., description="메뉴 ID")
    quantity: int = Field(..., ge=1, description="수량")


class OrderCreate(BaseModel):
    """Order creation request."""

    items: list[OrderItemCreate] = Field(..., min_length=1, description="주문 항목")


class OrderItemResponse(BaseModel):
    """Order item response."""

    id: int
    menu_id: int
    menu_name: str
    quantity: int
    unit_price: int
    subtotal: int

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    """Order response."""

    id: int
    store_code: str
    table_no: int
    session_id: int
    total_amount: int
    status: OrderStatus
    items: list[OrderItemResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrderStatusUpdate(BaseModel):
    """Order status update request."""

    status: OrderStatus = Field(..., description="주문 상태")
