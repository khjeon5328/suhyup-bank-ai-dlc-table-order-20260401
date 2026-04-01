"""User router."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.dependencies import require_owner, verify_store_access
from app.schemas.auth import TokenPayload
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("", response_model=List[UserResponse])
async def get_users(store_code: str = Depends(verify_store_access), user: TokenPayload = Depends(require_owner), db: AsyncSession = Depends(get_db_session)):
    return await UserService(db).get_users(store_code)


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(data: UserCreate, store_code: str = Depends(verify_store_access), user: TokenPayload = Depends(require_owner), db: AsyncSession = Depends(get_db_session)):
    return await UserService(db).create_user(store_code, data)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, data: UserUpdate, store_code: str = Depends(verify_store_access), user: TokenPayload = Depends(require_owner), db: AsyncSession = Depends(get_db_session)):
    return await UserService(db).update_user(store_code, user_id, user.user_id, data)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, store_code: str = Depends(verify_store_access), user: TokenPayload = Depends(require_owner), db: AsyncSession = Depends(get_db_session)):
    await UserService(db).delete_user(store_code, user_id, user.user_id)
