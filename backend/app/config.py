"""Application configuration using Pydantic Settings."""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./table_order.db"

    # JWT
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ADMIN_EXPIRE_HOURS: int = 16

    # S3
    S3_BUCKET: str = "table-order-images"
    S3_REGION: str = "ap-northeast-2"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"]

    # Rate Limiting
    RATE_LIMIT_LOGIN: str = "20/15minutes"
    RATE_LIMIT_GENERAL: str = "60/minute"

    # Logging
    LOG_LEVEL: str = "INFO"

    # Environment
    ENVIRONMENT: str = "development"


settings = Settings()
