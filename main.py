import asyncio
import logging
import sys

from aiogram.exceptions import TelegramUnauthorizedError
from pydantic import ValidationError
from redis.asyncio import Redis
from bot.commands import set_commands
from bot.factory import create_dispatcher
from config import get_settings
from database.base import Base
from database.connection import make_session_factory
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
import models  # noqa: F401

logger = logging.getLogger(__name__)


async def run() -> None:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    logger.info("Starting dating bot")
    engine = create_async_engine(settings.database_url)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        # Lightweight forward migrations for installations created before moderation was added.
        await connection.execute(text("ALTER TYPE userstatus ADD VALUE IF NOT EXISTS 'SUSPENDED'"))
        await connection.execute(
            text("ALTER TABLE profiles ADD COLUMN IF NOT EXISTS moderation_locked BOOLEAN NOT NULL DEFAULT FALSE")
        )
        await connection.execute(text("ALTER TABLE profiles ADD COLUMN IF NOT EXISTS photo_file_ids JSON"))
        await connection.execute(text("ALTER TABLE profiles ADD COLUMN IF NOT EXISTS main_photo_file_id VARCHAR(255)"))
        await connection.execute(text("ALTER TABLE profiles ADD COLUMN IF NOT EXISTS locale VARCHAR(8) DEFAULT 'ru'"))
        await connection.execute(text("ALTER TABLE profiles ADD COLUMN IF NOT EXISTS extra_data JSON"))
        await connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS trust_score INTEGER NOT NULL DEFAULT 95"))
        await connection.execute(text("""
            DO $$ BEGIN
                CREATE TYPE verificationstatus AS ENUM ('UNVERIFIED', 'PENDING', 'VERIFIED', 'REJECTED');
            EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        """))
        await connection.execute(text("""
            DO $$ BEGIN
                CREATE TYPE moderationstatus AS ENUM ('CLEAR', 'UNDER_REVIEW');
            EXCEPTION WHEN duplicate_object THEN NULL; END $$;
        """))
        await connection.execute(text("ALTER TABLE profiles ADD COLUMN IF NOT EXISTS verification_status verificationstatus NOT NULL DEFAULT 'UNVERIFIED'"))
        await connection.execute(text("ALTER TABLE profiles ADD COLUMN IF NOT EXISTS moderation_status moderationstatus NOT NULL DEFAULT 'CLEAR'"))
        await connection.execute(text("ALTER TABLE admin_logs ADD COLUMN IF NOT EXISTS target_type VARCHAR(32)"))
        await connection.execute(text("ALTER TABLE admin_logs ADD COLUMN IF NOT EXISTS target_id VARCHAR(64)"))
        await connection.execute(text("ALTER TABLE admin_logs ADD COLUMN IF NOT EXISTS metadata_json JSON NOT NULL DEFAULT '{}'"))
    factory = make_session_factory(settings)
    redis = Redis.from_url(settings.redis_url)
    bot, dp = create_dispatcher(settings, factory, redis)
    try:
        await set_commands(bot)
        await dp.start_polling(bot)
    except Exception:
        logger.exception("Bot polling failed")
        raise
    finally:
        await redis.aclose()
        await engine.dispose()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(run())
    except TelegramUnauthorizedError as error:
        print(
            "\nОШИБКА TELEGRAM: BOT_TOKEN неверный или был отозван в BotFather.\n"
            "Создайте/получите актуальный токен у @BotFather, замените только значение "
            "BOT_TOKEN в .env и снова выполните: docker compose up --build\n",
            file=sys.stderr,
        )
        raise SystemExit(2) from error
    except ValidationError as error:
        print(
            "\nОШИБКА НАСТРОЙКИ: заполните файл .env рядом с docker-compose.yml.\n"
            "Обязательные строки: BOT_TOKEN=... и DAILY_SECRET_SALT=...\n"
            "Возьмите шаблон из .env.example. Текущая ошибка:\n"
            f"{error}\n",
            file=sys.stderr,
        )
        raise SystemExit(2) from error
