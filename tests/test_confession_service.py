from services.confession_service import ConfessionService


def test_sender_hash_length():
    svc = ConfessionService(None, salt="testsalt")
    h = svc.sender_hash(12345)
    assert isinstance(h, str)
    assert len(h) == 64


def test_create_invalid_text_raises():
    svc = ConfessionService(None, salt="testsalt")
    try:
        import asyncio
        asyncio.run(svc.create(1, "@user", "x"))
    except ValueError as e:
        assert "Text length" in str(e)
    else:
        raise AssertionError("Expected ValueError for short text")


def test_create_empty_recipient_raises():
    svc = ConfessionService(None, salt="testsalt")
    try:
        import asyncio
        asyncio.run(svc.create(1, "   ", "Hello world"))
    except ValueError as e:
        assert "Recipient must be provided" in str(e)
    else:
        raise AssertionError("Expected ValueError for empty recipient")
