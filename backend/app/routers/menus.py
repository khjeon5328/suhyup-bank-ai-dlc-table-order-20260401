"""Menu router."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.dependencies import require_owner, verify_store_access
from app.schemas.auth import TokenPayload
from app.schemas.menu import CategoryCreate, CategoryResponse, CategoryUpdate, MenuCreate, MenuOrderUpdate, MenuResponse, MenuUpdate
from app.services.menu_service import MenuService

router = APIRouter()


@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories(store_code: str = Depends(verify_store_access), db: AsyncSession = Depends(get_db_session)):
    return await MenuService(db).get_categories(store_code)


@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(data: CategoryCreate, store_code: str = Depends(verify_store_access), user: TokenPayload = Depends(require_owner), db: AsyncSession = Depends(get_db_session)):
    return await MenuService(db).create_category(store_code, data)


@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, data: CategoryUpdate, store_code: str = Depends(verify_store_access), user: TokenPayload = Depends(require_owner), db: AsyncSession = Depends(get_db_session)):
    return await MenuService(db).update_category(store_code, category_id, data)


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(category_id: int, store_code: str = Depends(verify_store_access), user: TokenPayload = Depends(require_owner), db: AsyncSession = Depends(get_db_session)):
    await MenuService(db).delete_category(store_code, category_id)


@router.get("", response_model=List[MenuResponse])
async def get_menus(category_id: Optional[int] = Query(None), store_code: str = Depends(verify_store_access), db: AsyncSession = Depends(get_db_session)):
    return await MenuService(db).get_menus(store_code, category_id)


@router.post("", response_model=MenuResponse, status_code=201)
async def create_menu(data: MenuCreate, store_code: str = Depends(verify_store_access), user: TokenPayload = Depends(require_owner), db: AsyncSession = Depends(get_db_session)):
    return await MenuService(db).create_menu(store_code, data)


@router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu(menu_id: int, store_code: str = Depends(verify_store_access), db: AsyncSession = Depends(get_db_session)):
    return await MenuService(db).get_menu(store_code, menu_id)


@router.put("/{menu_id}", response_model=MenuResponse)
async def update_menu(menu_id: int, data: MenuUpdate, store_code: str = Depends(verify_store_access), user: TokenPayload = Depends(require_owner), db: AsyncSession = Depends(get_db_session)):
    return await MenuService(db).update_menu(store_code, menu_id, data)


@router.delete("/{menu_id}", status_code=204)
async def delete_menu(menu_id: int, store_code: str = Depends(verify_store_access), user: TokenPayload = Depends(require_owner), db: AsyncSession = Depends(get_db_session)):
    await MenuService(db).delete_menu(store_code, menu_id)


@router.put("/order", status_code=204)
async def update_menu_order(data: MenuOrderUpdate, store_code: str = Depends(verify_store_access), user: TokenPayload = Depends(require_owner), db: AsyncSession = Depends(get_db_session)):
    await MenuService(db).update_menu_order(store_code, data)
