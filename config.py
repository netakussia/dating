import json
from functools import lru_cache
from typing import Literal

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
    photo_safety_provider: Literal["ml", "heuristic", "disabled"] = "heuristic"
    nsfw_model_path: str = "/models/open_nsfw.onnx"
    face_model_path: str = "/models/face_detection_yunet_2023mar.onnx"
    face_detection_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    photo_safety_max_bytes: int = Field(default=10 * 1024 * 1024, ge=1)
    photo_safety_max_pixels: int = Field(default=20_000_000, ge=1)
    photo_safety_min_dimension: int = Field(default=64, ge=1)
    matching_weights_raw: str = Field(default="", alias="MATCHING_WEIGHTS_JSON")
    report_threshold: int = Field(default=3, ge=1, alias="REPORT_THRESHOLD")

    @property
    def admin_ids(self) -> set[int]:
        """Accepts both one ID (`123`) and a comma-separated list (`123,456`)."""
        values = [item.strip() for item in self.admin_ids_raw.split(",") if item.strip()]
        try:
            return {int(item) for item in values}
        except ValueError as error:
            raise ValueError("ADMIN_IDS должен содержать только числовые Telegram ID через запятую.") from error

    @property
    def matching_weights(self) -> dict[str, float]:
        defaults = {
            "gender": 35.0,
            "target_gender": 25.0,
            "age": 10.0,
            "district": 10.0,
            "institution": 10.0,
            "interests": 7.0,
            "bio": 3.0,
        }
        if not self.matching_weights_raw:
            return defaults
        try:
            configured = json.loads(self.matching_weights_raw)
        except json.JSONDecodeError as error:
            raise ValueError("MATCHING_WEIGHTS_JSON должен содержать JSON-объект с числовыми весами.") from error
        if not isinstance(configured, dict):
            raise ValueError("MATCHING_WEIGHTS_JSON должен содержать JSON-объект.")
        for name, value in configured.items():
            if name not in defaults or not isinstance(value, int | float) or value < 0:
                raise ValueError(f"Некорректный вес matching: {name!r}.")
            defaults[name] = float(value)
        return defaults


@lru_cache
def get_settings() -> Settings:
    return Settings()
