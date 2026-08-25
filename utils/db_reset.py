from __future__ import annotations

import asyncio
import os
import sys

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

RESET_TABLES = [
    "likes",
    "dislikes",
    "matches",
    "reports",
    "appeals",
    "verification_requests",
    "photo_moderations",
    "trust_score_events",
    "moderation_cases",
    "confessions",
    "confession_daily_limits",
    "admin_logs",
    "profiles",
    "users",
]


def get_reset_table_names() -> list[str]:
    return list(RESET_TABLES)


def _build_database_urls(explicit_url: str | None = None) -> list[str]:
    candidates: list[str] = []
    if explicit_url:
        candidates.append(explicit_url)

    env_url = os.getenv("DATABASE_URL") or os.getenv("DATABASE_URL_ASYNC")
    if env_url:
        candidates.append(env_url)

    if "localhost" in env_url if env_url else False:
        candidates.append(env_url.replace("localhost", "postgres", 1))

    candidates.extend(
        [
            "postgresql+asyncpg://postgres:postgres@localhost:5432/dating_db",
            "postgresql+asyncpg://postgres:postgres@postgres:5432/dating_db",
        ]
    )

    return list(dict.fromkeys(candidates))


async def reset_database(database_url: str | None = None, *, confirm: bool = False) -> list[str]:
    if not confirm:
        raise ValueError("Reset requires confirm=True")

    last_error: Exception | None = None
    for url in _build_database_urls(database_url):
        try:
            engine = create_async_engine(url)
            try:
                async with engine.begin() as connection:
                    for table in RESET_TABLES:
                        await connection.execute(text(f'DELETE FROM "{table}"'))
                    await connection.execute(text('ALTER SEQUENCE IF EXISTS users_id_seq RESTART WITH 1'))
                    await connection.execute(text('ALTER SEQUENCE IF EXISTS profiles_id_seq RESTART WITH 1'))
            finally:
                await engine.dispose()
            return RESET_TABLES
        except Exception as exc:  # pragma: no cover - exercised at runtime
            last_error = exc

    if last_error is not None:
        message = (
            "Failed to connect to PostgreSQL. "
            "Start the test database first, for example: "
            "docker compose up -d postgres redis"
        )
        raise RuntimeError(f"{message}\nOriginal error: {last_error}") from last_error
    raise RuntimeError("Failed to reset database: no connection information provided")


def main() -> None:
    database_url = os.getenv("DATABASE_URL") or os.getenv("DATABASE_URL_ASYNC")
    try:
        asyncio.run(reset_database(database_url, confirm=True))
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
