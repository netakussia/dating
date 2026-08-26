from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from models import UserRole, VerificationDecision
from services.verification_service import VerificationService


class VerificationSession:
    def __init__(self, request, *, update_result):
        self.request = request
        self.update_result = update_result
        self.statement = None

    async def get(self, model, _identity):
        if model.__name__ == "User":
            return SimpleNamespace(role=UserRole.MODERATOR, trust_score=95)
        return self.request

    async def execute(self, statement):
        self.statement = statement
        return SimpleNamespace(scalar_one_or_none=lambda: self.update_result)

    async def scalar(self, _statement):
        return None

    def add(self, _value):
        return None

    async def flush(self):
        return None


def request(assigned_to, status=VerificationDecision.PENDING):
    return SimpleNamespace(
        id="request-1",
        user_id=7,
        assigned_to=assigned_to,
        status=status,
        admin_id=None,
    )


@pytest.mark.asyncio
async def test_other_moderator_cannot_decide_claimed_verification():
    current = request(assigned_to=101)
    session = VerificationSession(current, update_result=None)
    service = VerificationService(session)
    service.repo.verification = AsyncMock(return_value=current)

    result, changed = await service.decide(
        "request-1", 202, VerificationDecision.APPROVED, actor_role=UserRole.MODERATOR
    )

    assert result is current
    assert changed is False
    assert "assigned_to" in str(session.statement)


@pytest.mark.asyncio
async def test_assigned_owner_can_decide_verification():
    current = request(assigned_to=101)
    session = VerificationSession(current, update_result=current)
    service = VerificationService(session)
    service.repo.log = AsyncMock()

    result, changed = await service.decide(
        "request-1", 101, VerificationDecision.REJECTED, actor_role=UserRole.MODERATOR
    )

    assert result is current
    assert changed is True


@pytest.mark.asyncio
async def test_privileged_moderator_can_override_verification_owner():
    current = request(assigned_to=101)
    session = VerificationSession(current, update_result=current)
    service = VerificationService(session)
    service.repo.log = AsyncMock()

    _, changed = await service.decide(
        "request-1", 303, VerificationDecision.RETAKE_REQUESTED, actor_role=UserRole.OWNER
    )

    assert changed is True


@pytest.mark.asyncio
async def test_unassigned_verification_remains_decidable():
    current = request(assigned_to=None)
    session = VerificationSession(current, update_result=current)
    service = VerificationService(session)
    service.repo.log = AsyncMock()

    _, changed = await service.decide(
        "request-1", 202, VerificationDecision.APPROVED, actor_role=UserRole.MODERATOR
    )

    assert changed is True


@pytest.mark.asyncio
async def test_already_decided_verification_is_idempotent():
    current = request(assigned_to=101, status=VerificationDecision.APPROVED)
    session = VerificationSession(current, update_result=None)
    service = VerificationService(session)
    service.repo.verification = AsyncMock(return_value=current)

    result, changed = await service.decide(
        "request-1", 101, VerificationDecision.REJECTED, actor_role=UserRole.MODERATOR
    )

    assert result is current
    assert changed is False