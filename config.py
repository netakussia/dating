import json
import math
from functools import lru_cache
from typing import Literal

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DOCUMENT_URLS = {
    "terms": "https://netakussia.github.io/meanima-docs/terms-of-service",
    "privacy": "https://netakussia.github.io/meanima-docs/privacy-policy",
    "community": "https://netakussia.github.io/meanima-docs/community-guidelines",
    "safety": "https://netakussia.github.io/meanima-docs/dating-safety",
    "moderation": "https://netakussia.github.io/meanima-docs/moderation-and-appeals",
    "alpha": "https://netakussia.github.io/meanima-docs/alpha-notice",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    def __init__(self, **data):
        explicit = dict(data)
        super().__init__(**data)
        for name in (
            "meanima_internal_chat_id",
            "meanima_internal_bug_thread_id",
            "meanima_internal_moderation_thread_id",
            "meanima_internal_errors_thread_id",
            "meanima_internal_stats_thread_id",
        ):
            if name in explicit:
                object.__setattr__(self, name, explicit[name])
        if self.environment.lower() in {"production", "prod", "staging"} and self.photo_safety_provider != "ml":
            raise ValueError("PHOTO_SAFETY_PROVIDER must be 'ml' in production-like environments.")

    bot_token: str = Field(..., min_length=20)
    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/dating_db"
    redis_url: str = "redis://redis:6379/0"
    daily_secret_salt: str = Field(..., min_length=16)
    admin_ids_raw: str = Field(default="", alias="ADMIN_IDS")
    owner_admin_id_raw: str = Field(default="", alias="OWNER_ADMIN_ID")
    document_base_url: str = Field(default="https://example.com/me-anima/docs", alias="DOCUMENT_BASE_URL")
    log_level: str = "INFO"
    nsfw_threshold: float = 0.85
    photo_safety_provider: Literal["ml", "heuristic", "disabled"] = "ml"
    environment: str = Field(
        default="development",
        validation_alias=AliasChoices("ENVIRONMENT", "ENV"),
    )
    nsfw_model_path: str = "/models/open_nsfw.onnx"
    face_model_path: str = "/models/face_detection_yunet_2023mar.onnx"
    face_detection_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    photo_safety_max_bytes: int = Field(default=10 * 1024 * 1024, ge=1)
    photo_safety_max_pixels: int = Field(default=24_000_000, ge=1)
    photo_safety_min_dimension: int = Field(default=64, ge=1)
    face_detection_max_dimension: int = Field(default=960, ge=320, le=2048)
    matching_weights_raw: str = Field(default="", alias="MATCHING_WEIGHTS_JSON")
    report_threshold: int = Field(default=3, ge=1, alias="REPORT_THRESHOLD")
    confession_daily_limit: int = Field(default=20, ge=1, le=100, alias="CONFESSION_DAILY_LIMIT")
    confession_pending_ttl_hours: int = Field(default=168, ge=1, le=24 * 31, alias="CONFESSION_PENDING_TTL_HOURS")
    fsm_state_ttl_seconds: int = Field(default=3600, ge=60, le=7 * 24 * 3600, alias="FSM_STATE_TTL_SECONDS")
    meanima_internal_chat_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("MEANIMA_INTERNAL_CHAT_ID", "MEANIMA_INTERNAL_CHAT"),
    )
    meanima_internal_bug_thread_id: int | None = Field(
        default=None,
        alias="MEANIMA_INTERNAL_BUG_THREAD_ID",
    )
    meanima_internal_moderation_thread_id: int | None = Field(
        default=None,
        alias="MEANIMA_INTERNAL_MODERATION_THREAD_ID",
    )
    meanima_internal_errors_thread_id: int | None = Field(
        default=None,
        alias="MEANIMA_INTERNAL_ERRORS_THREAD_ID",
    )
    meanima_internal_stats_thread_id: int | None = Field(
        default=None,
        alias="MEANIMA_INTERNAL_STATS_THREAD_ID",
    )

    @property
    def admin_ids(self) -> set[int]:
        """Accepts both one ID (`123`) and a comma-separated list (`123,456`)."""
        values = [item.strip() for item in self.admin_ids_raw.split(",") if item.strip()]
        try:
            return {int(item) for item in values}
        except ValueError as error:
            raise ValueError("ADMIN_IDS должен содержать только числовые Telegram ID через запятую.") from error

    @property
    def owner_admin_id(self) -> int | None:
        """Return the explicitly configured owner, or retain the legacy first-admin fallback."""
        if not self.admin_ids:
            return None
        if not self.owner_admin_id_raw.strip():
            return min(self.admin_ids)
        try:
            owner_id = int(self.owner_admin_id_raw.strip())
        except ValueError as error:
            raise ValueError("OWNER_ADMIN_ID должен содержать числовой Telegram ID.") from error
        if owner_id not in self.admin_ids:
            raise ValueError("OWNER_ADMIN_ID должен быть указан также в ADMIN_IDS.")
        return owner_id

    @property
    def document_urls(self) -> dict[str, str]:
        base = self.document_base_url.rstrip("/")
        return {
            "terms": f"{base}/terms-of-service",
            "privacy": f"{base}/privacy-policy",
            "community": f"{base}/community-guidelines",
            "safety": f"{base}/dating-safety",
            "moderation": f"{base}/moderation-and-appeals",
            "alpha": f"{base}/alpha-notice",
        }

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
            if (
                name not in defaults
                or isinstance(value, bool)
                or not isinstance(value, int | float)
                or not math.isfinite(value)
                or value < 0
            ):
                raise ValueError(f"Некорректный вес matching: {name!r}.")
            defaults[name] = float(value)
        return defaults


@lru_cache
def get_settings() -> Settings:
    return Settings()
