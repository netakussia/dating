from html import escape


def telegram_contact(user_id: int, username: str | None, display_name: str) -> str:
    """Returns a public @username or a Telegram deep link when no username exists."""

    if username:
        return f"@{username}"
    return f'<a href="tg://user?id={user_id}">{escape(display_name)}</a>'
