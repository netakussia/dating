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
- Redis keys cleared: recommendation_queue:<user_id>, keys matching f"fsm*{user_id}*", rate:<user_id> and related patterns.
"""

import argparse
import asyncio
import os
import sys
from typing import Iterable

from sqlalchemy import delete, or_

# Avoid importing this module from runtime code: this file must not be executed by the bot.
if __name__ != "__main__":
    # When imported, expose nothing and avoid side-effects.
    __all__ = []


def _ensure_env_allows_run() -> None:
    env = os.environ.get("ENV") or os.environ.get("ENVIRONMENT") or ""
    env_l = env.lower()
    if env_l in ("production", "prod"):
        print("Refusing to run in production environment (ENV/ENVIRONMENT=production).", file=sys.stderr)
        sys.exit(2)
    if env_l not in ("development", "dev", "test"):
        print("Danger: ENV/ENVIRONMENT must be one of: development, dev, test. Got: %r" % env, file=sys.stderr)
        sys.exit(3)


async def _clear_redis_for_user(redis, user_id: int) -> None:
    # Explicit keys
    keys_to_del = [f"recommendation_queue:{user_id}", f"rate:{user_id}"]

    # Scan for keys related to FSM and other patterns that include the user id.
    pattern1 = f"*:{user_id}*"

    async for key in redis.scan_iter(match=pattern1):
        ks = key.decode() if isinstance(key, (bytes, bytearray)) else str(key)
        # keep keys that look like FSM, rate, recommendation_queue or contain :<user_id> pattern
        if ":%s" % user_id in ks or ks.startswith("fsm:") or ks.startswith("rate:") or ks.startswith("recommendation_queue:"):
            keys_to_del.append(ks)

    # Also remove keys matching fsm:*{user_id}*
    async for key in redis.scan_iter(match=f"fsm:*{user_id}*"):
        ks = key.decode() if isinstance(key, (bytes, bytearray)) else str(key)
        keys_to_del.append(ks)

    # Deduplicate
    keys_to_del = list(dict.fromkeys(keys_to_del))
    if not keys_to_del:
        return
    await redis.delete(*keys_to_del)
    print("Deleted Redis keys:", keys_to_del)


async def _clear_redis_all(redis) -> None:
    # Be conservative: only remove recommendation_queue:* and rate:* and fsm:* keys
    keys = []
    async for key in redis.scan_iter(match="recommendation_queue:*"):
        ks = key.decode() if isinstance(key, (bytes, bytearray)) else str(key)
        keys.append(ks)
    async for key in redis.scan_iter(match="rate:*"):
        ks = key.decode() if isinstance(key, (bytes, bytearray)) else str(key)
        keys.append(ks)
    async for key in redis.scan_iter(match="fsm:*"):
        ks = key.decode() if isinstance(key, (bytes, bytearray)) else str(key)
        keys.append(ks)
    if keys:
        await redis.delete(*keys)
    print("Deleted Redis keys (count):", len(keys))


async def _reset_user(session_factory, redis_url: str, user_id: int) -> None:
    # Import settings and models lazily to avoid runtime interference
    from config import get_settings
    from database.connection import make_session_factory
    # Import models here to avoid side effects at module import time
    from models.recommendation_view import RecommendationView
    from models.trust import PhotoModeration
    from models.report import Report
    from models.block import Block
    from models.match import Match
    from models.like import Like
    from models.dislike import Dislike
    from models.profile import Profile
    from models.user import User

    settings = get_settings()
    factory = make_session_factory(settings)

    # Delete in a single transaction in the requested order
    async with factory() as session:
        async with session.begin():
            # recommendation_views: viewer_id or candidate_id
            await session.execute(delete(RecommendationView).where(or_(RecommendationView.viewer_id == user_id, RecommendationView.candidate_id == user_id)))
            # photo_moderations
            await session.execute(delete(PhotoModeration).where(PhotoModeration.user_id == user_id))
            # reports
            await session.execute(delete(Report).where(or_(Report.reporter_id == user_id, Report.target_user_id == user_id)))
            # blocks
            await session.execute(delete(Block).where(or_(Block.blocker_id == user_id, Block.blocked_id == user_id)))
            # matches
            await session.execute(delete(Match).where(or_(Match.user1_id == user_id, Match.user2_id == user_id)))
            # likes
            await session.execute(delete(Like).where(or_(Like.from_user_id == user_id, Like.to_user_id == user_id)))
            # dislikes
            await session.execute(delete(Dislike).where(or_(Dislike.from_user_id == user_id, Dislike.to_user_id == user_id)))
            # profiles
            await session.execute(delete(Profile).where(Profile.user_id == user_id))
            # users
            await session.execute(delete(User).where(User.id == user_id))
        await session.commit()
    # Redis cleanup
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
    # Import models here
    from models.recommendation_view import RecommendationView
    from models.trust import PhotoModeration
    from models.report import Report
    from models.block import Block
    from models.match import Match
    from models.like import Like
    from models.dislike import Dislike
    from models.profile import Profile
    from models.user import User

    settings = get_settings()
    factory = make_session_factory(settings)

    async with factory() as session:
        async with session.begin():
            await session.execute(delete(RecommendationView))
            await session.execute(delete(PhotoModeration))
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


def main() -> None:
    _ensure_env_allows_run()
    args = _parse_args()

    redis_url = os.environ.get("REDIS_URL") or os.environ.get("REDIS") or None
    if not redis_url:
        # fallback to settings.url but avoid importing settings too early
        from config import get_settings

        redis_url = get_settings().redis_url

    if args.all and not args.yes:
        confirm = input("Type 'CONFIRM_RESET' to proceed: ")
        if confirm.strip() != "CONFIRM_RESET":
            print("Aborted by user")
            sys.exit(1)

    # Build session factory lazily inside async functions
    async def _run():
        if args.user:
            await _reset_user(None, redis_url, args.user)
        elif args.all:
            await _reset_all(None, redis_url)

    asyncio.run(_run())


if __name__ == "__main__":
    main()
