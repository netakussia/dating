from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_container_startup_applies_alembic_migrations_before_polling():
    dockerfile = (PROJECT_ROOT / "Dockerfile").read_text(encoding="utf-8")

    assert "alembic upgrade head && exec python main.py" in dockerfile


def test_internal_state_services_are_not_published_and_redis_persists_queue_data():
    compose = (PROJECT_ROOT / "docker-compose.yml").read_text(encoding="utf-8")

    assert "ports:" not in compose
    assert '"--requirepass", "${REDIS_PASSWORD:?REDIS_PASSWORD must be set in .env}"' in compose
    assert "pgdata:/var/lib/postgresql/data" in compose
    assert "redisdata:/data" in compose
