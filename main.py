import asyncio
import logging
import sys

from aiogram.exceptions import TelegramUnauthorizedError
from pydantic import ValidationError
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine

import models  # noqa: F401
from bot.commands import set_commands
from bot.factory import create_dispatcher
from config import get_settings
from database.connection import make_session_factory

logger = logging.getLogger(__name__)


async def run() -> None:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    logger.info("Starting dating bot")
    engine = create_async_engine(settings.database_url)
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
