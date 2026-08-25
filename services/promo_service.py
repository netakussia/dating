from __future__ import annotations

from typing import Any


def get_empty_discovery_promo(user_id: int, *, profile: Any | None = None) -> dict[str, Any]:
    """Return a fallback promo card for users with no more nearby matches.

    The broader app may customize this later with personalized copy, but the UI code
    only requires a small dict with title/text/button values.
    """
    return {
        "title": "Пока всё в порядке",
        "text": "Сейчас рядом больше не осталось подходящих анкет. Попробуйте позже или обновите поиск.",
        "button_text": "🔄 Обновить выдачу",
        "button_action": "next:profile",
    }
