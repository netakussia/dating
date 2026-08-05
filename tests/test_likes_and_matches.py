from types import SimpleNamespace

import pytest

from services.like_service import LikeService
from services.match_service import MatchService
from utils.contacts import telegram_contact


class FakeLikeRepository:
    def __init__(self, *, created=True, reciprocal=None):
        self.created = created
        self.reciprocal_like = reciprocal
        self.add_calls = []

    async def add(self, source, target, comment):
        self.add_calls.append((source, target, comment))
        return SimpleNamespace(is_mutual=False), self.created

    async def reciprocal(self, _source, _target):
        return self.reciprocal_like


class FakeMatchRepository:
    def __init__(self, *, created=True):
        self.created = created
        self.calls = []

    async def create_once(self, source, target):
        self.calls.append((source, target))
        return SimpleNamespace(), self.created

    async def by_user_id(self, _user_id, _limit):
        return []


@pytest.mark.asyncio
async def test_like_rejects_self_like_and_duplicate_like():
    service = LikeService(None)
    repository = FakeLikeRepository(created=False)
    service.repo = repository

    with pytest.raises(ValueError, match="самому себе"):
        await service.create(1, 1)
    result = await service.create(1, 2)

    assert not result.created
    assert repository.add_calls == [(1, 2, None)]


@pytest.mark.asyncio
async def test_like_comment_is_saved_and_match_is_created_once():
    likes = FakeLikeRepository(created=True, reciprocal=SimpleNamespace(is_mutual=False))
    matches = FakeMatchRepository(created=True)
    like_service = LikeService(None)
    like_service.repo = likes
    like_result = await like_service.create(1, 2, "Привет!")
    match_service = MatchService(None)
    match_service.likes = likes
    match_service.matches = matches

    result = await match_service.create_if_mutual(1, 2, like_result.like)

    assert likes.add_calls == [(1, 2, "Привет!")]
    assert result.created
    assert matches.calls == [(1, 2)]
    assert like_result.like.is_mutual and likes.reciprocal_like.is_mutual


@pytest.mark.asyncio
async def test_existing_match_does_not_create_duplicate_notification_event():
    likes = FakeLikeRepository(reciprocal=SimpleNamespace(is_mutual=False))
    matches = FakeMatchRepository(created=False)
    service = MatchService(None)
    service.likes = likes
    service.matches = matches

    result = await service.create_if_mutual(1, 2, SimpleNamespace(is_mutual=False))

    assert result.match is not None
    assert not result.created


def test_match_contact_falls_back_to_safe_telegram_link_without_username():
    assert telegram_contact(42, None, "Анна") == '<a href="tg://user?id=42">Анна</a>'
