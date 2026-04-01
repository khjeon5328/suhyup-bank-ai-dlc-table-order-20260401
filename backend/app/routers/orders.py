"""Order router."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.dependencies import get_current_user, get_event_bus, require_admin, require_owner, require_table, verify_store_access
from app.core.event_bus import EventBus
from app.schemas.auth import TokenPayload
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order_service import OrderService

router = APIRouter()


@router.get("", response_model=List[OrderResponse])
async def get_orders(
    store_code: str = Depends(verify_store_access),
    user: TokenPayload = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    service = OrderService(db, get_event_bus())
    if user.role == "table":
        return await service.get_orders_by_session(user.session_id)
    return await service.get_orders_by_store(store_code)


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(
    data: OrderCreate,
    store_code: str = Depends(verify_store_access),
    user: TokenPayload = Depends(require_table),
    db: AsyncSession = Depends(get_db_session),
    bus: EventBus = Depends(get_event_bus),
):
    service = OrderService(db, bus)
    return await service.create_order(store_code, user.table_no, user.session_id, data)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    store_code: str = Depends(verify_store_access),
    user: TokenPayload = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    service = OrderService(db, get_event_bus())
    return await service.get_order(store_code, order_id)


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    store_code: str = Depends(verify_store_access),
    user: TokenPayload = Depends(require_admin),
    db: AsyncSession = Depends(get_db_session),
    bus: EventBus = Depends(get_event_bus),
):
    service = OrderService(db, bus)
    return await service.update_status(store_code, order_id, data.status)


@router.delete("/{order_id}", status_code=204)
async def delete_order(
    order_id: int,
    store_code: str = Depends(verify_store_access),
    user: TokenPayload = Depends(require_owner),
    db: AsyncSession = Depends(get_db_session),
    bus: EventBus = Depends(get_event_bus),
):
    service = OrderService(db, bus)
    await service.delete_order(store_code, order_id)
