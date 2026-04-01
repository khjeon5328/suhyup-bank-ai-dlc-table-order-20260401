"""Image upload schemas."""

from pydantic import BaseModel, Field


class PresignedUrlRequest(BaseModel):
    filename: str = Field(..., min_length=1)
    content_type: str = Field(..., pattern="^image/(jpeg|png|webp)$")


class PresignedUrlResponse(BaseModel):
    upload_url: str
    image_url: str
    expires_in: int = 300
