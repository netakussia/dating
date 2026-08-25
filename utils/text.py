from __future__ import annotations

from html import escape as _html_escape


def escape_html(value: object) -> str:
    """Escape text for safe Telegram HTML rendering."""
    if value is None:
        return ""
    return _html_escape(str(value), quote=True)


__all__ = ["escape_html"]
