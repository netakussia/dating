from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str = Field(..., min_length=20)
    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/dating_db"
    redis_url: str = "redis://redis:6379/0"
    daily_secret_salt: str = Field(..., min_length=16)
    admin_ids_raw: str = Field(default="", alias="ADMIN_IDS")
    log_level: str = "INFO"
    nsfw_threshold: float = 0.85

    @property
    def admin_ids(self) -> set[int]:
        """Accepts both one ID (`123`) and a comma-separated list (`123,456`)."""
        values = [item.strip() for item in self.admin_ids_raw.split(",") if item.strip()]
        try:
            return {int(item) for item in values}
        except ValueError as error:
            raise ValueError("ADMIN_IDS должен содержать только числовые Telegram ID через запятую.") from error


@lru_cache
def get_settings() -> Settings:
    return Settings()
