import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Iterable


@lru_cache(maxsize=1)
def _load_categories() -> dict[str, dict[str, object]]:
    data_path = Path(__file__).resolve().parent.parent / "data" / "interest_categories.json"
    with data_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    categories: dict[str, dict[str, object]] = {}
    for item in payload.get("categories", []):
        key = str(item["key"])
        aliases = [str(alias).casefold() for alias in item.get("aliases", [])]
        label = str(item.get("label", key))
        categories[key] = {"label": label, "aliases": aliases}
    return categories


def normalize_interests(raw_text: str | Iterable[str] | None) -> list[str]:
    if raw_text is None:
        return []

    if isinstance(raw_text, str):
        items = re.split(r"[,;|/]+", raw_text)
    else:
        items = list(raw_text)

    normalized: list[str] = []
    seen: set[str] = set()

    for item in items:
        candidate = str(item).strip()
        if not candidate:
            continue

        cleaned = re.sub(r"[^a-zа-я0-9]+", " ", candidate.casefold()).strip()
        if not cleaned:
            continue

        matched = False
        for key, category in _load_categories().items():
            aliases = {str(alias).casefold() for alias in category.get("aliases", [])}
            if cleaned in aliases or any(token in aliases for token in cleaned.split()):
                if key not in seen:
                    normalized.append(key)
                    seen.add(key)
                matched = True
                break

        if not matched:
            display_value = candidate.strip()
            if display_value not in seen:
                normalized.append(display_value)
                seen.add(display_value)

    return normalized
