"""Store router."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.dependencies import verify_store_access
from app.schemas.store import StoreResponse
from app.services.store_service import StoreService

router = APIRouter()


@router.get("/{store_code}", response_model=StoreResponse)
async def get_store(
    store_code: str = Depends(verify_store_access),
    db: AsyncSession = Depends(get_db_session),
):
    service = StoreService(db)
    return await service.get_store(store_code)
