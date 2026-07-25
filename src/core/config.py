from pathlib import Path

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.common.utils.enums import Environment
from src.core.logging import LogLevelStr

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Application configuration management."""

    APP_NAME: str = "Fast api starter file"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    APP_ENV: Environment

    DATABASE_URL: PostgresDsn | None = Field(
        default=None,
        examples=["postgresql+asyncpg://user:password@localhost:5432/dbname"],
    )

    JWT_SECRET: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, ge=1)

    LOG_LEVEL: LogLevelStr = "INFO"

    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
    ]

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()
