from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.enums import Environment


class Settings(BaseSettings):
    """Application configuration."""

    APP_NAME: str = "Shades of Grace LLC API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    APP_ENV: Environment

    DATABASE_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    LOG_LEVEL: str = "INFO"

    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
