import asyncio
import logging
from types import SimpleNamespace

from config import get_settings
from database.connection import make_session_factory
from handlers.profile import profile as profile_handler
from handlers.verification import verification_start as verification_start_handler
from middlewares.profile_required import ProfileRequiredMiddleware
from models import Gender, Profile
from repositories.profile import ProfileRepository
from repositories.user import UserRepository

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("simulate")


class DummyState:
    async def set_state(self, *args, **kwargs):
        logger.info("DummyState.set_state called with %s %s", args, kwargs)


class FakeMessage:
    def __init__(self, user_id: int, text: str = None):
        self.from_user = SimpleNamespace(id=user_id, username=f"user{user_id}", full_name=f"User {user_id}")
        self.text = text
        self.message = self

    async def answer(self, *args, **kwargs):
        logger.info("Message.answer called: %s %s", args, kwargs)

    async def edit_text(self, *args, **kwargs):
        logger.info("Message.edit_text called: %s %s", args, kwargs)


async def run():
    settings = get_settings()
    engine_factory = make_session_factory(settings)
    async with engine_factory() as session:
        # create/get user
        user = await UserRepository(session).get_or_create(1234567890, "tester123")
        logger.info("Got user id=%s", user.id)
        # ensure profile exists
        repo = ProfileRepository(session)
        profile = await repo.by_user_id(user.id)
        if not profile:
            profile = Profile(
                user_id=user.id,
                gender=Gender.MALE,
                target_gender=Gender.FEMALE,
                name="Tester",
                age=25,
                district="TestDistrict",
                institution="TestUni",
                interests=[],
                bio="Bio",
            )
            await repo.add(profile)
            logger.info("Created profile for user %s", user.id)
        else:
            logger.info("Profile already exists for user %s", user.id)

        # Prepare middleware and fake handler
        middleware = ProfileRequiredMiddleware()

        async def handler(event, data):
            logger.info("Handler executed for event text=%s", getattr(event, 'text', None))
            return "handled"

        # Case 1: message '🛡 Верификация' with current_user set
        msg = FakeMessage(user.id, text="🛡 Верификация")
        data = {"current_user": user, "session": session}
        res = await middleware(handler, msg, data)
        logger.info("Middleware result for verification message: %s", res)
        if res is not None:
            # call the verification handler to see what it does
            await verification_start_handler(msg, DummyState())

        # Case 2: message '👤 Моя анкета'
        msg2 = FakeMessage(user.id, text="👤 Моя анкета")
        res2 = await middleware(handler, msg2, data)
        logger.info("Middleware result for profile message: %s", res2)
        if res2 is not None:
            await profile_handler(msg2, session=session, state=SimpleNamespace())


if __name__ == '__main__':
    try:
        asyncio.run(run())
    except Exception as exc:
        import traceback

        logger.exception("Simulator failed: %s", exc)
        traceback.print_exc()
