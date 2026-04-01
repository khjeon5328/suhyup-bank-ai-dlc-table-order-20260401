"""Database configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database connection and pool settings loaded from environment variables."""

    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "tableorder"
    db_password: str = "tableorder"
    db_name: str = "tableorder"

    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_timeout: int = 30
    db_pool_recycle: int = 3600
    db_echo: bool = False

    db_ssl_mode: str | None = None
    db_ssl_ca: str | None = None

    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def database_url(self) -> str:
        """Build async database URL."""
        return (
            f"mysql+asyncmy://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def database_url_sync(self) -> str:
        """Build sync database URL for Alembic migrations."""
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def connect_args(self) -> dict:
        """Build connection arguments including TLS settings."""
        args: dict = {"charset": "utf8mb4"}
        if self.environment == "production" and self.db_ssl_ca:
            args["ssl"] = {"ca": self.db_ssl_ca}
        return args


settings = DatabaseSettings()
