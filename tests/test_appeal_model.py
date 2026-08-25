from models import Appeal, AppealStatus


def test_appeal_model_exports_and_statuses():
    assert AppealStatus.PENDING.value == "PENDING"
    assert Appeal.__tablename__ == "appeals"
