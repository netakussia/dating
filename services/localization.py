import json
from functools import lru_cache
from pathlib import Path
from typing import Any


class LocalizationService:
    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent / "data" / "locales"

    @lru_cache(maxsize=8)
    def _load(self, locale: str) -> dict[str, Any]:
        path = self.base_dir / f"{locale}.json"
        if not path.exists():
            path = self.base_dir / "ru.json"
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def get(self, key: str, locale: str = "ru", default: str | None = None) -> str:
        data = self._load(locale)
        value = data.get(key)
        if isinstance(value, str):
            return value
        return default or key

    def format(self, key: str, locale: str = "ru", **kwargs: Any) -> str:
        value = self.get(key, locale=locale)
        if not kwargs:
            return value
        try:
            return value.format(**kwargs)
        except (IndexError, KeyError, TypeError, ValueError):
            # A broken catalog entry must never take down a user update.
            return value
