"""Auth router — POST /login/admin, POST /login/table."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas.auth import AdminLoginRequest, AdminLoginResponse, TableLoginRequest, TableLoginResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login/admin", response_model=AdminLoginResponse)
async def login_admin(
    data: AdminLoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db_session),
):
    service = AuthService(db)
    ip = request.client.host if request.client else "unknown"
    return await service.login_admin(data.store_code, data.username, data.password, ip)


@router.post("/login/table", response_model=TableLoginResponse)
async def login_table(
    data: TableLoginRequest,
    db: AsyncSession = Depends(get_db_session),
):
    service = AuthService(db)
    return await service.login_table(data.store_code, data.table_no, data.password)
