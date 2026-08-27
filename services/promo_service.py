from __future__ import annotations

from typing import Any

from services.localization import LocalizationService


def get_empty_discovery_promo(
    user_id: int, *, profile: Any | None = None, locale: str = "ru"
) -> dict[str, Any]:
    """Return a fallback promo card for users with no more nearby matches.

    The broader app may customize this later with personalized copy, but the UI code
    only requires a small dict with title/text/button values.
    """
    localizer = LocalizationService()
    return {
        "title": localizer.get("promo_empty_title", locale),
        "text": localizer.get("promo_empty_text", locale),
        "button_text": localizer.get("promo_refresh", locale),
        "button_action": "next:profile",
    }
