"""Menu router — menus and categories CRUD."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.dependencies import get_current_user, require_owner, verify_store_access
from app.schemas.auth import TokenPayload
from app.schemas.menu import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    MenuCreate,
    MenuOrderUpdate,
    MenuResponse,
    MenuUpdate,
)
from app.services.menu_service import MenuService

router = APIRouter()


# --- Categories ---
@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories(
    store_id: int = Depends(verify_store_access),
    db: AsyncSession = Depends(get_db_session),
):
    service = MenuService(db)
    return await service.get_categories(store_id)


@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_owner),
    db: AsyncSession = Depends(get_db_session),
):
    service = MenuService(db)
    return await service.create_category(store_id, data)


@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_owner),
    db: AsyncSession = Depends(get_db_session),
):
    service = MenuService(db)
    return await service.update_category(store_id, category_id, data)


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_owner),
    db: AsyncSession = Depends(get_db_session),
):
    service = MenuService(db)
    await service.delete_category(store_id, category_id)


# --- Menus ---
@router.get("/", response_model=List[MenuResponse])
async def get_menus(
    category_id: Optional[int] = Query(None),
    store_id: int = Depends(verify_store_access),
    db: AsyncSession = Depends(get_db_session),
):
    service = MenuService(db)
    return await service.get_menus(store_id, category_id)


@router.post("/", response_model=MenuResponse, status_code=201)
async def create_menu(
    data: MenuCreate,
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_owner),
    db: AsyncSession = Depends(get_db_session),
):
    service = MenuService(db)
    return await service.create_menu(store_id, data)


@router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu(
    menu_id: int,
    store_id: int = Depends(verify_store_access),
    db: AsyncSession = Depends(get_db_session),
):
    service = MenuService(db)
    return await service.get_menu(store_id, menu_id)


@router.put("/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: int,
    data: MenuUpdate,
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_owner),
    db: AsyncSession = Depends(get_db_session),
):
    service = MenuService(db)
    return await service.update_menu(store_id, menu_id, data)


@router.delete("/{menu_id}", status_code=204)
async def delete_menu(
    menu_id: int,
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_owner),
    db: AsyncSession = Depends(get_db_session),
):
    service = MenuService(db)
    await service.delete_menu(store_id, menu_id)


@router.put("/order", status_code=204)
async def update_menu_order(
    data: MenuOrderUpdate,
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_owner),
    db: AsyncSession = Depends(get_db_session),
):
    service = MenuService(db)
    await service.update_menu_order(store_id, data)
