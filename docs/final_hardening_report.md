# Final Hardening Report

## Environment
- Repository: `/home/neta/dating/project1`
- Python: project virtualenv `.venv/bin/python`
- Verification performed locally on Linux with project dependencies installed in `.venv`

## Problems Reproduced
- Duplicate report handling used a full `session.rollback()` after a uniqueness conflict, which could discard unrelated work in an outer transaction.
- Report threshold detection used `>= threshold`; concurrent reporters that had passed eligibility before suspension could each trigger the threshold side effect.
- Stale photo callbacks could reach `list.index()` and raise; a fourth photo upload could be silently ignored while the user saw a success message.
- Docker startup did not apply Alembic migrations, and Redis persistence was not explicitly enabled.

## Fixes Applied
- `repositories/report.py`
  - Handles duplicate-report `IntegrityError` in a nested transaction (savepoint), preserving the outer transaction.
  - Treats only the exact threshold crossing as the suspension/moderation-case trigger.
- `services/recommendation_queue.py`
  - Added corruption resilience in `RedisRecommendationQueue.pop()`.
  - Malformed Redis queue entries are now skipped with a warning log instead of raising, allowing the queue to continue serving valid recommendations.
- `tests/test_likes_and_matches.py`
  - Enhanced fake repository stubs with a minimal `session` interface for eligibility checks.
- `tests/test_recommendation_queue.py`
  - Added regression coverage for corrupted Redis queue entries.
- `tests/test_reports.py`
  - Covers duplicate-report savepoint handling and confirms reports above the threshold do not repeat the suspension side effect.
- `services/profile_service.py`, `handlers/profile.py`, `tests/test_profile_registration.py`
  - Stale move/replace operations are safe no-ops.
  - A stale fourth upload is rejected clearly instead of silently discarded.
- `Dockerfile`, `docker-compose.yml`, `tests/test_deployment_config.py`
  - Container startup applies `alembic upgrade head` before polling.
  - PostgreSQL and Redis are internal-only; Redis uses AOF persistence on its named volume.

## Regression Tests
- `pytest -q -s` → `61 passed`
- `ruff check` on all modified Python files → `All checks passed`
- `python -m compileall -q .` → success
- `alembic heads` → one head: `20260808_unlock_photo_cases`
- Fresh PostgreSQL volume: `alembic upgrade head` applied all revisions successfully; `current` reported head and a repeated upgrade was idempotent.

## Stress Tests
- Recommendation performance tests: 50/200/500/1000/2000/5000 candidates completed; at 1000 candidates queue rebuild took ~6.1 ms and first-card lookup ~0.1 ms in the local in-memory benchmark.
- Real Redis: wrote a key, restarted Redis, and read the key back successfully with the AOF configuration.
- Real PostgreSQL: performed fresh and repeat Alembic upgrade checks in a temporary isolated Compose project.

## Security / Safety Verification
- Recommendation queue now fails forward when Redis queue payloads are damaged.
- Duplicate reporting is now idempotent at the repository boundary and no longer relies solely on read-before-write semantics.
- Eligibility enforcement remains in service layer for likes, matches, and reports.
- Photo safety was not modified and retains its fail-closed behavior.

## Remaining Risks
- True cross-transaction PostgreSQL concurrency verification for reports/likes/matches is still not done.
- Existing unrelated `ruff` violations exist elsewhere in the repo; this audit only corrected the modified hardening-related files.
- The actual Redis unavailable/reconnect path and multi-process recommendation consumers were not tested here.

## Not Verified
- End-to-end PostgreSQL concurrency with simultaneous reports, likes, and match creation.
- Live Redis connection-loss/reconnect behavior and queue consumers in separate bot processes.
- Actual photo safety provider runtime with missing ML models in production.

## Alpha Readiness
- Hardening-related code changes are regression tested and passing unit test coverage.
- `pytest` is green for the project test suite (61 passed).
- `compileall` is green.
- Changed files pass `ruff`.
- Fresh and repeat Alembic migrations were verified on local PostgreSQL; Redis persistence was verified across a local restart.
- The project is closer to alpha readiness, but production-level concurrency and reconnect tests should be completed next.

## Recommended Next Module
- Add staging integration tests for PostgreSQL and Redis concurrency paths.
- Improve operational observability for recommendation queue warnings and report submission errors.
