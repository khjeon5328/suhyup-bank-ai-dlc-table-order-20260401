"""Image upload service — US-O09 (image)."""

import uuid

import boto3
import structlog

from app.config import settings
from app.schemas.image import PresignedUrlResponse

logger = structlog.get_logger()


class ImageService:
    def __init__(self):
        self.s3_client = boto3.client("s3", region_name=settings.S3_REGION)
        self.bucket = settings.S3_BUCKET

    def generate_presigned_url(
        self, store_id: int, filename: str, content_type: str
    ) -> PresignedUrlResponse:
        ext = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
        key = f"{store_id}/{uuid.uuid4()}.{ext}"

        upload_url = self.s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": self.bucket, "Key": key, "ContentType": content_type},
            ExpiresIn=300,
        )
        image_url = f"https://{self.bucket}.s3.{settings.S3_REGION}.amazonaws.com/{key}"

        logger.info("presigned_url_generated", store_id=store_id, key=key)
        return PresignedUrlResponse(upload_url=upload_url, image_url=image_url)
