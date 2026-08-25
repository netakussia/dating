import asyncio
import os

import pytest
from sqlalchemy import delete, func, select

from config import get_settings
from database.connection import make_session_factory
from models import Profile, TrustScoreEvent, User, VerificationDecision, VerificationRequest
from services.verification_service import VerificationService

INTEGRATION = os.environ.get("INTEGRATION")
USER_ID = 991_001


@pytest.mark.skipif(not INTEGRATION, reason="Integration tests require INTEGRATION=1")
@pytest.mark.asyncio
async def test_concurrent_verification_decisions_apply_trust_score_once():
    factory = make_session_factory(get_settings())
    async with factory() as session:
        await session.execute(delete(TrustScoreEvent).where(TrustScoreEvent.user_id == USER_ID))
        await session.execute(delete(VerificationRequest).where(VerificationRequest.user_id == USER_ID))
        await session.execute(delete(Profile).where(Profile.user_id == USER_ID))
        await session.execute(delete(User).where(User.id == USER_ID))
        user = User(id=USER_ID, username="alpha_resolution_test")
        session.add(user)
        await session.flush()
        session.add(
            Profile(
                user_id=USER_ID,
                gender="MALE",
                target_gender="FEMALE",
                name="Alpha Test",
                age=25,
                district="Center",
                institution="Test University",
                interests=["music"],
                bio="Concurrency test profile",
            )
        )
        request = VerificationRequest(user_id=USER_ID, video_file_id="test-video")
        session.add(request)
        await session.commit()
        request_id = request.id

    async def decide_once(admin_id: int) -> bool:
        async with factory() as session:
            _, changed = await VerificationService(session).decide(request_id, admin_id, VerificationDecision.APPROVED)
            await session.commit()
            return changed

    try:
        outcomes = await asyncio.gather(decide_once(991_101), decide_once(991_102))
        async with factory() as session:
            event_count = await session.scalar(
                select(func.count()).select_from(TrustScoreEvent).where(TrustScoreEvent.user_id == USER_ID)
            )

        assert outcomes.count(True) == 1
        assert event_count == 1
    finally:
        async with factory() as session:
            await session.execute(delete(TrustScoreEvent).where(TrustScoreEvent.user_id == USER_ID))
            await session.execute(delete(VerificationRequest).where(VerificationRequest.user_id == USER_ID))
            await session.execute(delete(Profile).where(Profile.user_id == USER_ID))
            await session.execute(delete(User).where(User.id == USER_ID))
            await session.commit()
