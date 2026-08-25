# DEVELOPMENT/ALPHA TOOL ONLY
# This script creates test profiles for development and fills recommendation queues.

"""
Usage:
  python -m tools.seed_test_profiles --count 50

Notes:
- Only allowed when ENV or ENVIRONMENT is set to 'development', 'dev' or 'test'.
- Will refuse to run when ENV/ENVIRONMENT == 'production'.
- Inserts Users and Profiles with synthetic data and triggers RecommendationService.rebuild_queue

"""

import argparse
import asyncio
import os
import random
import sys

# Do not execute on import
if __name__ != "__main__":
    __all__ = []


FIRST_NAMES = [
    "Alex", "Ivan", "Marius", "Andrei", "Diana", "Elena", "Maria", "Olga", "Sergiu", "Nikita",
    "Irina", "Vlad", "Anna", "Oleg", "Tatiana", "Cristina", "Yuri", "Ion", "Nicoleta", "Eugen",
]
CITIES = [
    "Bălți", "Chișinău", "Кишинёв", "Balti", "Chișinău Center", "Bălți Sector 1", "Centru", "Râșcani",
]
INTERESTS = [
    "music", "travel", "movies", "sports", "hiking", "reading", "cooking", "technology", "photography", "dancing",
]
BIOS = [
    "Love exploring new places and coffee.",
    "Working in tech, looking to meet interesting people.",
    "Dog lover, runner, and amateur chef.",
    "Into movies, board games, and good conversations.",
    "Student of life — curiosity first.",
]


def _ensure_env_dev() -> None:
    env = (os.environ.get("ENV") or os.environ.get("ENVIRONMENT") or "").lower()
    if env in ("production", "prod"):
        print("Refusing to run in production environment (ENV/ENVIRONMENT=production).", file=sys.stderr)
        sys.exit(2)
    if env not in ("development", "dev", "test"):
        print(f"Danger: ENV/ENVIRONMENT must be one of: development, dev, test. Got: {env!r}", file=sys.stderr)
        sys.exit(3)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed test profiles (development only)")
    parser.add_argument("--count", type=int, default=50, help="How many profiles to create")
    parser.add_argument(
        "--photo-file-id",
        type=str,
        default=None,
        help="Optional Telegram file_id to use for all photos (useful for real-file testing)",
    )
    parser.add_argument(
        "--target-gender",
        type=str,
        choices=["MALE", "FEMALE", "ALL"],
        default=None,
        help="Optional target gender for created profiles",
    )
    return parser.parse_args()


async def _seed(count: int, photo_file_id: str | None, target_gender: str | None = None) -> list[int]:
    # Lazy imports to avoid side-effects at module import

    from config import get_settings
    from database.connection import make_session_factory
    from models.profile import Profile
    from models.user import User

    settings = get_settings()
    factory = make_session_factory(settings)

    created_ids: list[int] = []

    async with factory() as session:
        async with session.begin():
            # choose a base telegram id high enough not to collide with real users
            base = 200000
            for i in range(count):
                user_id = base + i
                name = random.choice(FIRST_NAMES)
                age = random.randint(18, 30)
                city = random.choice(CITIES)
                interests = random.sample(INTERESTS, k=random.randint(1, 4))
                bio = random.choice(BIOS)
                username = f"testuser{user_id}"

                user = User(id=user_id, username=username)
                # Photo placeholders (these are not real Telegram file ids but valid strings used by system tests)
                if photo_file_id:
                    photo_ids = [photo_file_id]
                else:
                    # Use public placeholder image URLs by default (picsum seed ensures variety)
                    num_photos = random.randint(2, 3)
                    photo_ids = [f"https://picsum.photos/seed/{user_id}_{j}/600/800" for j in range(1, num_photos + 1)]
                # determine gender for profile
                if target_gender in ("MALE", "FEMALE", "ALL"):
                    gender_val = target_gender
                else:
                    gender_val = random.choice(["MALE", "FEMALE"])

                profile = Profile(
                    user_id=user_id,
                    gender=gender_val,
                    target_gender="ALL",
                    name=name,
                    age=age,
                    district=city,
                    institution=random.choice(["USM", "Technical University", "State University"]),
                    interests=interests,
                    bio=bio,
                    photo_file_ids=photo_ids,
                    main_photo_file_id=photo_ids[0] if photo_ids else None,
                    is_visible=True,
                    moderation_locked=False,
                )
                session.add(user)
                session.add(profile)
                created_ids.append(user_id)
        # commit happens on context exit
    print(
        f"Created {len(created_ids)} test users: "
        f"{created_ids[:5]}{'...' if len(created_ids) > 5 else ''}"
    )

    # Now trigger rebuild_queue for each created user so Redis queues are filled.
    # We create a short-lived session per user to run the rebuild, which relies on
    # services.recommendation.RecommendationService.
    from services.recommendation import RecommendationService

    for uid in created_ids:
        async with factory() as session:
            svc = RecommendationService(session)
            n = await svc.rebuild_queue(uid)
            print(f"Rebuilt queue for {uid}: {n} entries")

    # Close global default queue Redis client if present to avoid destructor warnings
    from services.recommendation_queue import get_default_queue

    try:
        q = get_default_queue()
        if hasattr(q, "_redis"):
            try:
                await q._redis.aclose()
            except Exception:
                pass
    except Exception:
        pass

    return created_ids


def main() -> None:
    _ensure_env_dev()
    args = _parse_args()
    asyncio.run(_seed(args.count, args.photo_file_id, args.target_gender))


if __name__ == "__main__":
    main()
