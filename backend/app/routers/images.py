"""Image router — presigned URL generation."""

from fastapi import APIRouter, Depends

from app.core.dependencies import require_owner, verify_store_access
from app.schemas.auth import TokenPayload
from app.schemas.image import PresignedUrlRequest, PresignedUrlResponse
from app.services.image_service import ImageService

router = APIRouter()


@router.post("/presigned-url", response_model=PresignedUrlResponse)
async def generate_presigned_url(
    data: PresignedUrlRequest,
    store_id: int = Depends(verify_store_access),
    user: TokenPayload = Depends(require_owner),
):
    service = ImageService()
    return service.generate_presigned_url(store_id, data.filename, data.content_type)
