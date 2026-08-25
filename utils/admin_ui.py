from __future__ import annotations

import uuid


def compact_display_id(value: str | int | uuid.UUID | None) -> str:
    if value is None:
        return "—"
    if isinstance(value, uuid.UUID):
        return str(value).replace("-", "")[:8]
    if isinstance(value, int):
        digits = str(abs(value))
        return digits[-6:] if len(digits) > 6 else digits or "0"
    text = str(value).replace("-", "")
    return text[:8] if len(text) > 8 else text or "—"


def admin_role_label(
    admin_id: int,
    *,
    username: str | None = None,
    owner_admin_id: int | None = None,
    owner_name: str = "Netakussia",
) -> str:
    if owner_admin_id is not None and admin_id == owner_admin_id:
        return f"👑 {owner_name} — владелец"
    handle = f"@{username.lstrip('@')}" if username else "модератор"
    return f"⚔️ {handle} — модератор"


def user_display_name(user_id: int, *, username: str | None = None) -> str:
    if username:
        return f"@{username.lstrip('@')}"
    return f"#{compact_display_id(user_id)}"
