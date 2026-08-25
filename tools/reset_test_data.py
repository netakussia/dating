# DEVELOPMENT/ALPHA TOOL ONLY
# This script is dangerous and must only be used in development/testing environments.
# It performs destructive deletes in PostgreSQL and Redis. Do NOT run in production.

"""
Usage examples:
  python -m tools.reset_test_data --user 12345
  python -m tools.reset_test_data --all --yes

Behaviour:
- Allows execution only when ENV or ENVIRONMENT is set to 'development', 'dev' or 'test'.
- If ENV/ENVIRONMENT equals 'production' the script exits immediately.
- Deletions are performed inside a single async DB transaction for consistency.
- Redis keys cleared: recommendation_queue:<user_id>, keys matching f"fsm*{user_id}*",
  rate:<user_id> and related patterns.
"""

import argparse
import asyncio
import os
import socket
import sys
from urllib.parse import urlparse

from sqlalchemy import delete, or_

# Avoid importing this module from runtime code: this file must not be executed by the bot.
if __name__ != "__main__":
    __all__ = []


def _ensure_env_allows_run() -> None:
    env = os.environ.get("ENV") or os.environ.get("ENVIRONMENT") or ""
    env_l = env.lower()
    if env_l in ("production", "prod"):
        print(
            "Refusing to run in production environment (ENV/ENVIRONMENT=production).",
            file=sys.stderr,
        )
        sys.exit(2)
    if env_l not in ("development", "dev", "test"):
        print(
            f"Danger: ENV/ENVIRONMENT must be one of: development, dev, test. Got: {env!r}",
            file=sys.stderr,
        )
        sys.exit(3)


def _decode_key(value: object) -> str:
    if isinstance(value, bytes | bytearray):
        return value.decode()
    return str(value)


async def _clear_redis_for_user(redis, user_id: int) -> None:
    keys_to_del = [f"recommendation_queue:{user_id}", f"rate:{user_id}"]
    pattern1 = f"*:{user_id}*"

    async for key in redis.scan_iter(match=pattern1):
        ks = _decode_key(key)
        if (
            f":{user_id}" in ks
            or ks.startswith("fsm:")
            or ks.startswith("rate:")
            or ks.startswith("recommendation_queue:")
        ):
            keys_to_del.append(ks)

    async for key in redis.scan_iter(match=f"fsm:*{user_id}*"):
        ks = _decode_key(key)
        keys_to_del.append(ks)

    keys_to_del = list(dict.fromkeys(keys_to_del))
    if not keys_to_del:
        return
    await redis.delete(*keys_to_del)
    print("Deleted Redis keys:", keys_to_del)


async def _clear_redis_all(redis) -> None:
    keys: list[str] = []
    for pattern in ("recommendation_queue:*", "rate:*", "fsm:*"):
        async for key in redis.scan_iter(match=pattern):
            keys.append(_decode_key(key))
    if keys:
        await redis.delete(*keys)
    print("Deleted Redis keys (count):", len(keys))


async def _reset_user(session_factory, redis_url: str, user_id: int) -> None:
    from config import get_settings
    from database.connection import make_session_factory
    from models.admin_log import AdminLog
    from models.appeal import Appeal
    from models.block import Block
    from models.confession import Confession, ConfessionDailyLimit
    from models.dislike import Dislike
    from models.like import Like
    from models.match import Match
    from models.profile import Profile
    from models.recommendation_view import RecommendationView
    from models.report import Report
    from models.trust import ModerationCase, PhotoModeration, TrustScoreEvent, VerificationRequest
    from models.user import User

    settings = get_settings()
    factory = make_session_factory(settings)

    async with factory() as session:
        async with session.begin():
            await session.execute(
                delete(RecommendationView).where(
                    or_(
                        RecommendationView.viewer_id == user_id,
                        RecommendationView.candidate_id == user_id,
                    )
                )
            )
            await session.execute(
                delete(TrustScoreEvent).where(TrustScoreEvent.user_id == user_id)
            )
            await session.execute(
                delete(VerificationRequest).where(VerificationRequest.user_id == user_id)
            )
            await session.execute(
                delete(Appeal).where(Appeal.user_id == user_id)
            )
            await session.execute(
                delete(ModerationCase).where(ModerationCase.user_id == user_id)
            )
            await session.execute(delete(PhotoModeration).where(PhotoModeration.user_id == user_id))
            await session.execute(
                delete(Confession).where(
                    or_(
                        Confession.sender_id == user_id,
                        Confession.receiver_id == user_id,
                    )
                )
            )
            await session.execute(
                delete(ConfessionDailyLimit).where(ConfessionDailyLimit.user_id == user_id)
            )
            await session.execute(
                delete(AdminLog).where(
                    or_(
                        AdminLog.admin_id == user_id,
                        AdminLog.target_user_id == user_id,
                    )
                )
            )
            await session.execute(
                delete(Report).where(
                    or_(
                        Report.reporter_id == user_id,
                        Report.target_user_id == user_id,
                    )
                )
            )
            await session.execute(
                delete(Block).where(
                    or_(
                        Block.blocker_id == user_id,
                        Block.blocked_id == user_id,
                    )
                )
            )
            await session.execute(
                delete(Match).where(
                    or_(
                        Match.user1_id == user_id,
                        Match.user2_id == user_id,
                    )
                )
            )
            await session.execute(
                delete(Like).where(
                    or_(
                        Like.from_user_id == user_id,
                        Like.to_user_id == user_id,
                    )
                )
            )
            await session.execute(
                delete(Dislike).where(
                    or_(
                        Dislike.from_user_id == user_id,
                        Dislike.to_user_id == user_id,
                    )
                )
            )
            await session.execute(delete(Profile).where(Profile.user_id == user_id))
            await session.execute(delete(User).where(User.id == user_id))
        await session.commit()

    import redis.asyncio as aioredis

    r = aioredis.Redis.from_url(redis_url)
    try:
        await _clear_redis_for_user(r, user_id)
    finally:
        await r.aclose()

    print(f"Reset completed for user {user_id}")


async def _reset_all(session_factory, redis_url: str) -> None:
    from config import get_settings
    from database.connection import make_session_factory
    from models.admin_log import AdminLog
    from models.appeal import Appeal
    from models.block import Block
    from models.confession import Confession, ConfessionDailyLimit
    from models.dislike import Dislike
    from models.like import Like
    from models.match import Match
    from models.profile import Profile
    from models.recommendation_view import RecommendationView
    from models.report import Report
    from models.trust import ModerationCase, PhotoModeration, TrustScoreEvent, VerificationRequest
    from models.user import User

    settings = get_settings()
    factory = make_session_factory(settings)

    async with factory() as session:
        async with session.begin():
            await session.execute(delete(RecommendationView))
            await session.execute(delete(TrustScoreEvent))
            await session.execute(delete(VerificationRequest))
            await session.execute(delete(Appeal))
            await session.execute(delete(ModerationCase))
            await session.execute(delete(PhotoModeration))
            await session.execute(delete(Confession))
            await session.execute(delete(ConfessionDailyLimit))
            await session.execute(delete(AdminLog))
            await session.execute(delete(Report))
            await session.execute(delete(Block))
            await session.execute(delete(Match))
            await session.execute(delete(Like))
            await session.execute(delete(Dislike))
            await session.execute(delete(Profile))
            await session.execute(delete(User))
        await session.commit()

    import redis.asyncio as aioredis

    r = aioredis.Redis.from_url(redis_url)
    try:
        await _clear_redis_all(r)
    finally:
        await r.aclose()

    print("Full reset completed")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reset test data (development only)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--user", type=int, help="Telegram user ID to reset")
    group.add_argument("--all", action="store_true", help="Reset all test data (destructive)")
    parser.add_argument("--yes", action="store_true", help="Assume yes for confirmation prompts")
    return parser.parse_args()


def _db_host_resolvable(database_url: str | None) -> bool:
    if not database_url:
        return False
    # Attempt to parse common SQLAlchemy/DSN formats
    try:
        parsed = urlparse(database_url)
        host = parsed.hostname
        if not host:
            # Try fallback: database_url might be like 'postgres:5432/db' without scheme
            if ":" in database_url:
                host = database_url.split(":")[0]
        if not host:
            return False
        # Try to resolve DNS / hostname
        try:
            socket.getaddrinfo(host, None)
            return True
        except socket.gaierror:
            return False
    except Exception:
        return False


def main() -> None:
    _ensure_env_allows_run()
    args = _parse_args()

    redis_url = os.environ.get("REDIS_URL") or os.environ.get("REDIS") or None
    from config import get_settings

    settings = get_settings()

    if not redis_url:
        redis_url = settings.redis_url

    database_url = settings.database_url

    # If DB host is not resolvable from this environment, provide a clearer error
    if not _db_host_resolvable(database_url):
        print(
            "Cannot resolve database host from DATABASE_URL. This usually means you're running the tool on the host",
            "but the database is only available inside Docker (hostname like 'postgres').",
            file=sys.stderr,
        )
        print("Options:", file=sys.stderr)
        print(
            "  * Run the tool inside the bot container where service hostnames are resolvable:",
            file=sys.stderr,
        )
        print(
            "      docker compose -f project1/docker-compose.yml exec -e ENV=development "
            "bot python -m tools.reset_test_data --all --yes",
            file=sys.stderr,
        )
        print(
            "  * Or set DATABASE_URL to a reachable address from your host "
            "(e.g. localhost:5432 if you published the port)",
            file=sys.stderr,
        )
        sys.exit(4)

    if args.all and not args.yes:
        confirm = input("Type 'CONFIRM_RESET' to proceed: ")
        if confirm.strip() != "CONFIRM_RESET":
            print("Aborted by user")
            sys.exit(1)

    async def _run() -> None:
        if args.user:
            await _reset_user(None, redis_url, args.user)
        elif args.all:
            await _reset_all(None, redis_url)

    asyncio.run(_run())


if __name__ == "__main__":
    main()
