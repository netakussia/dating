import json
import re
import unicodedata
from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path


def _normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.strip().casefold())
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return re.sub(r"[^\w]+", " ", normalized, flags=re.UNICODE).strip()


@lru_cache(maxsize=1)
def _load_categories() -> dict[str, dict[str, object]]:
    data_path = Path(__file__).resolve().parent.parent / "data" / "interest_categories.json"
    with data_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    categories: dict[str, dict[str, object]] = {}
    for item in payload.get("categories", []):
        key = str(item["key"])
        aliases = {_normalize_text(str(alias)) for alias in item.get("aliases", [])}
        aliases.add(_normalize_text(key))
        label = str(item.get("label", key))
        categories[key] = {"label": label, "aliases": aliases}
    return categories


def normalize_interests(raw_text: str | Iterable[str] | None) -> list[str]:
    if raw_text is None:
        return []

    items: list[str] = []
    if isinstance(raw_text, str):
        items.extend(re.split(r"[,;|/]+", raw_text))
    else:
        for item in raw_text:
            if isinstance(item, str):
                items.extend(re.split(r"[,;|/]+", item))
            else:
                items.append(str(item))

    normalized: list[str] = []
    seen: set[str] = set()

    for item in items:
        candidate = str(item).strip()
        if not candidate:
            continue

        cleaned = _normalize_text(candidate)
        if not cleaned:
            continue

        matched = False
        for key, category in _load_categories().items():
            aliases = category.get("aliases", set())
            if cleaned in aliases or any(token in aliases for token in cleaned.split()):
                if key not in seen:
                    normalized.append(key)
                    seen.add(key)
                matched = True
                break

        if not matched:
            if candidate not in seen:
                normalized.append(candidate)
                seen.add(candidate)

    return normalized


def format_interests(interests: list[str] | str | None) -> str:
    if interests is None:
        return "—"
    if isinstance(interests, str):
        interests = normalize_interests(interests)
    formatted = [f"#{interest.title().replace('_', '')}" for interest in interests if str(interest).strip()]
    return " ".join(formatted) if formatted else "—"
