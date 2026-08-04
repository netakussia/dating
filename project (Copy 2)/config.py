from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str = Field(..., min_length=20)
    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/dating_db"
    redis_url: str = "redis://redis:6379/0"
    daily_secret_salt: str = Field(..., min_length=16)
    admin_ids: set[int] = set()
    log_level: str = "INFO"
    nsfw_threshold: float = 0.85

    @field_validator("admin_ids", mode="before")
    @classmethod
    def parse_admin_ids(cls, value: object) -> object:
        if isinstance(value, str):
            return {int(item.strip()) for item in value.split(",") if item.strip()}
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
