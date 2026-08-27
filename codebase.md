This file is a merged representation of a subset of the codebase, containing files not matching ignore patterns, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching these patterns are excluded: .venv, venv, __pycache__, .git, .pytest_cache, .ruff_cache, *.pyc, *.sqlite3, *.db, codebase.md
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
````
.github/
  workflows/
    tests.yml
bot/
  __init__.py
  commands.py
  factory.py
data/
  locales/
    en.json
    ro.json
    ru.json
  interest_categories.json
  normalization_aliases.json
database/
  migrations/
    versions/
      20260805_matching_engine.py
      20260805_trust_system.py
      20260806_photo_safety_cache.py
      20260807_legacy_schema_alignment.py
      20260808_schema_baseline.py
      20260808_unlock_resolved_photo_cases.py
      20260815_rec_view_claim.py
      20260827_confession_key.py
      20260828_report_assigned.py
      20260828_user_accepts_confessions.py
      20260828_verif_assigned.py
      20260829_high_workflow_invariants.py
    env.py
  __init__.py
  base.py
  connection.py
docs/
  admin.md
  AI_AGENT_RULES.md
  alpha_operations.md
  api.md
  architecture_decisions.md
  architecture.md
  database.md
  dev_notes.md
  final_hardening_report.md
  manual_two_user_alpha_test.md
  matching.md
  next_agent_context.md
  project_structure.md
  registration.md
  trust.md
dtos/
  profile_dto.py
filters/
  __init__.py
  admin.py
  chat_type.py
handlers/
  __init__.py
  admin.py
  appeals.py
  callback_fallback.py
  common.py
  confessions.py
  dating.py
  likes.py
  profile.py
  registration.py
  verification.py
keyboards/
  __init__.py
  admin.py
  dating.py
  menu.py
  profile.py
middlewares/
  __init__.py
  db.py
  i18n.py
  profile_required.py
  rate_limit.py
  user.py
models/
  __init__.py
  .gitkeep
  admin_log.py
  appeal.py
  block.py
  confession.py
  dislike.py
  face_detection_yunet_2023mar.onnx
  like.py
  match.py
  open_nsfw.onnx
  profile.py
  recommendation_view.py
  report.py
  trust.py
  user.py
privacy/
  alpha-notice.md
  bot-short-texts.md
  community-guidelines.md
  dating-safety.md
  moderation-and-appeals.md
  privacy-policy.md
  terms-of-service.md
repositories/
  __init__.py
  appeal.py
  base.py
  confession.py
  discovery.py
  like.py
  match.py
  matching_stats.py
  profile.py
  recommendation.py
  report.py
  trust.py
  user.py
scripts/
  backup_postgres.sh
  install_backup_cron.sh
  run_integration.sh
services/
  __init__.py
  confession_service.py
  eligibility.py
  interest_normalizer.py
  like_service.py
  localization.py
  match_service.py
  matching_debug.py
  matching_stats.py
  moderation_service.py
  notification_service.py
  nsfw_service.py
  photo_analysis_progress.py
  photo_moderation_service.py
  photo_safety_providers.py
  photo_upload_lock.py
  profile_service.py
  promo_service.py
  recommendation_queue.py
  recommendation_strategy.py
  recommendation.py
  report_service.py
  trust_score_service.py
  trust_stats_service.py
  verification_service.py
states/
  __init__.py
  admin.py
  appeal.py
  bug_report.py
  confession.py
  dating.py
  profile_photo.py
  registration.py
  verification.py
tests/
  integration/
    test_moderation_resolution_concurrency.py
    test_redis_multiprocess_pop.py
  photo/
    IMG_20260717_164527.jpg
    IMG_20260718_185752.jpg
    IMG_20260719_181857.jpg
    IMG_20260809_131212.jpg (1)
    IMG_20260809_131744.jpg (1)
    MVIMG_20260822_182014.jpg
    Pokecut_1784476792359.jpg
  __init__.py
  test_admin_ui.py
  test_appeal_model.py
  test_callback_resilience.py
  test_confession_service.py
  test_db_reset.py
  test_deployment_config.py
  test_eligibility.py
  test_high_regressions.py
  test_i18n.py
  test_likes_and_matches.py
  test_photo_analysis_progress.py
  test_photo_safety_providers.py
  test_profile_inline_navigation.py
  test_profile_registration.py
  test_profile_required.py
  test_rate_limit.py
  test_recommendation_extra.py
  test_recommendation_performance.py
  test_recommendation_queue.py
  test_recommendation_repository.py
  test_recommendation.py
  test_registration_progress.py
  test_reports.py
  test_trust_services.py
  test_verification_handlers.py
  test_verification_ownership.py
tools/
  __init__.py
  reset_test_data.py
  seed_test_profiles.py
  simulate_events.py
utils/
  __init__.py
  admin_roles.py
  admin_ui.py
  contacts.py
  db_reset.py
  deep_links.py
  document_links.py
  legal.py
  logging.py
  profile_media.py
  text.py
validators/
  __init__.py
  profile_validator.py
__init__.py
.dockerignore
.env.example
.gitignore
alembic.ini
config.py
conftest.py
docker-compose.override.yml.example
docker-compose.yml
Dockerfile
main.py
pack.sh
PROJECT_RULES.md
pyproject.toml
README.md
requirements.txt
ROADMAP.md
TEST_CHECKLIST.md
````

# Files

## File: pack.sh
````bash
#!/usr/bin/env bash

# Имя итогового файла
OUTPUT="codebase.md"

echo "📦 Собираем кодовую базу в $OUTPUT..."

# Запуск repomix с исключением виртуальных окружений, кэша и гита
npx repomix \
  --output "$OUTPUT" \
  --ignore ".venv,venv,__pycache__,.git,.pytest_cache,.ruff_cache,*.pyc,*.sqlite3,*.db,codebase.md" \
  --style markdown

echo "✅ Готово! Файл $OUTPUT сформирован."
````

## File: .github/workflows/tests.yml
````yaml
name: Tests

on:
  push:
  workflow_dispatch:

jobs:
  pytest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest -q
````

## File: bot/__init__.py
````python

````

## File: bot/commands.py
````python
from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Открыть бота"),
            BotCommand(command="help", description="Помощь"),
            BotCommand(command="admin", description="Админ-панель"),
            BotCommand(command="debug_matching", description="Диагностика matching (admin)"),
        ]
    )
````

## File: data/locales/en.json
````json
{
  "welcome": "Welcome! Create a profile or find a match.",
  "profile_created": "✅ Profile saved.",
  "profile_preview": "Profile preview",
  "publish": "Publish",
  "edit": "Edit",
  "back": "Back",
  "cancel": "Cancel",
  "photo_required": "A photo is required.",
  "photo_limit": "You can upload up to 3 photos.",
  "profile_paused": "Profile paused.",
  "profile_deleted": "Profile deleted.",
  "profile_updated": "Profile updated.",
  "profile_visibility_changed": "Visibility changed",
  "profile_not_found": "Profile not found.",
  "registration_step_gender": "Your gender?",
  "registration_step_target_gender": "Who are you looking for?",
  "registration_step_name": "What is your name? (2–32 characters)",
  "registration_step_age": "Your age (16–99)?",
  "registration_step_district": "Your district?",
  "registration_step_institution": "Where do you study/work? (3–64 characters)",
  "registration_step_interests": "Interests separated by commas",
  "registration_step_bio": "Tell us about yourself (10–500 characters)",
  "registration_step_photo": "Send photos. You can upload up to 3.",
  "registration_step_preview": "This is how your profile will look.",
  "registration_step_confirm": "Confirm profile publication."
}
````

## File: data/interest_categories.json
````json
{
  "categories": [
    {"key": "music", "label": "🎧 Люблю музыку", "aliases": ["music", "музыка", "muzica", "muzică", "spotify", "рок", "рэп", "гитара", "rock", "rap", "song", "hip hop", "hip-hop", "hiphop"]},
    {"key": "sport", "label": "🏃 Спорт", "aliases": ["sport", "спорт", "fitness", "фитнес", "run", "gym", "football", "basketball", "tennis", "зал", "тренажёрка"]},
    {"key": "cinema", "label": "🎬 Кино", "aliases": ["cinema", "кино", "movie", "movies", "film", "films"]},
    {"key": "anime", "label": "🌸 Аниме", "aliases": ["anime", "аниме", "manga"]},
    {"key": "programming", "label": "💻 Программирование", "aliases": ["programming", "программирование", "code", "coding", "dev", "python", "java", "javascript", "it", "айти", "cybersecurity", "linux", "network"]},
    {"key": "games", "label": "🎮 Игры", "aliases": ["games", "игры", "game", "gamer", "gaming", "csgo", "minecraft"]},
    {"key": "books", "label": "📚 Книги", "aliases": ["books", "книги", "book", "reading", "literature"]},
    {"key": "cars", "label": "🚗 Автомобили", "aliases": ["cars", "машины", "авто", "car", "automotive"]},
    {"key": "travel", "label": "✈️ Путешествия", "aliases": ["travel", "traveling", "путешествия", "trip", "voyage"]},
    {"key": "drawing", "label": "🎨 Рисование", "aliases": ["drawing", "рисование", "art", "paint", "drawing"]},
    {"key": "photography", "label": "📷 Фотография", "aliases": ["photography", "фотография", "photo", "camera"]},
    {"key": "cooking", "label": "🍳 Кулинария", "aliases": ["cooking", "кулинария", "food", "cook", "chef"]},
    {"key": "animals", "label": "🐾 Животные", "aliases": ["animals", "животные", "pet", "pets", "dog", "cat"]},
    {"key": "dance", "label": "💃 Танцы", "aliases": ["dance", "танцы", "dancing", "music"]},
    {"key": "science", "label": "🔬 Наука", "aliases": ["science", "наука", "astro", "astrophysics", "physics", "biology"]}
  ]
}
````

## File: data/normalization_aliases.json
````json
{
  "districts": {
    "beltsy": [
      "бельцы",
      "бэлць",
      "balti",
      "bălți",
      "balți",
      "balti md",
      "mun. balti",
      "бэлци",
      "beltsy",
      "belți"
    ],
    "центр": [
      "center",
      "centru",
      "ctr",
      "centr",
      "цент",
      "centre"
    ],
    "пэмынтэны": [
      "pământeni",
      "pemanteni",
      "пэмынтэны"
    ]
  },
  "institutions": {
    "colegiul politehnic": [
      "cpb",
      "колледж политехник",
      "политех",
      "colegiul politehnic",
      "c.p.b."
    ],
    "usarb": [
      "aleccu russo",
      "alecu russo",
      "usarb",
      "universitatea alecu russo",
      "universitatea de stat alecu russo"
    ],
    "draxlmaier": [
      "dräxlmaier",
      "drăxlmaier",
      "drexlaier",
      "дрэксельмайер",
      "draxlmaier"
    ],
    "gebauer": [
      "gg",
      "gebauer"
    ],
    "sebn": [
      "sebn"
    ]
  }
}
````

## File: database/migrations/versions/20260805_matching_engine.py
````python
"""Add persistent recommendation view events for matching analytics.

Revision ID: 20260805_matching_engine
Revises:
Create Date: 2026-08-05
"""


revision = "20260805_matching_engine"
down_revision = "20260808_schema_baseline"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # The baseline migration already creates the current schema, so this historical
    # revision is kept as a compatibility no-op for fresh installs.
    pass


def downgrade() -> None:
    pass
````

## File: database/migrations/versions/20260805_trust_system.py
````python
"""Add extensible Trust System records and profile/user trust state.

Revision ID: 20260805_trust_system
Revises: 20260805_matching_engine
Create Date: 2026-08-05
"""

import sqlalchemy as sa

revision = "20260805_trust_system"
down_revision = "20260805_matching_engine"
branch_labels = None
depends_on = None

verificationstatus = sa.Enum("UNVERIFIED", "PENDING", "VERIFIED", "REJECTED", name="verificationstatus")
moderationstatus = sa.Enum("CLEAR", "UNDER_REVIEW", name="moderationstatus")
verificationdecision = sa.Enum("PENDING", "APPROVED", "REJECTED", "RETAKE_REQUESTED", name="verificationdecision")
moderationcasetype = sa.Enum("REPORT_THRESHOLD", "NSFW", "NO_FACE", name="moderationcasetype")
moderationcasestatus = sa.Enum("PENDING", "RESOLVED", name="moderationcasestatus")


def upgrade() -> None:
    # The baseline migration already creates the current schema, so this historical
    # revision is kept as a compatibility no-op for fresh installs.
    pass


def downgrade() -> None:
    pass
````

## File: database/migrations/versions/20260806_photo_safety_cache.py
````python
"""Add normalized image hash cache for photo safety assessments.

Revision ID: 20260806_photo_safety_cache
Revises: 20260805_trust_system
"""


revision = "20260806_photo_safety_cache"
down_revision = "20260805_trust_system"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # The baseline migration already creates the current schema, so this historical
    # revision is kept as a compatibility no-op for fresh installs.
    pass


def downgrade() -> None:
    pass
````

## File: database/migrations/versions/20260807_legacy_schema_alignment.py
````python
"""Align create_all legacy installations with current profile and trust metadata.

Revision ID: 20260807_legacy_schema_alignment
Revises: 20260806_photo_safety_cache
"""


revision = "20260807_legacy_schema_alignment"
down_revision = "20260806_photo_safety_cache"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # The baseline migration already creates the current schema, so this historical
    # revision is kept as a compatibility no-op for fresh installs.
    pass


def downgrade() -> None:
    pass
````

## File: database/migrations/versions/20260808_schema_baseline.py
````python
"""Create the full application schema from the current SQLAlchemy metadata.

Revision ID: 20260808_schema_baseline
Revises:
Create Date: 2026-08-08
"""

from alembic import op

import models  # noqa: F401
from database.base import Base

revision = "20260808_schema_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind(), checkfirst=True)


def downgrade() -> None:
    # Keep rollback safe and non-destructive: the baseline only establishes the current schema.
    pass
````

## File: database/migrations/versions/20260808_unlock_resolved_photo_cases.py
````python
"""Release stale locks left by already resolved photo moderation cases.

Revision ID: 20260808_unlock_photo_cases
Revises: 20260807_legacy_schema_alignment
"""


revision = "20260808_unlock_photo_cases"
down_revision = "20260807_legacy_schema_alignment"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # The baseline migration already creates the current schema, so this historical
    # revision is kept as a compatibility no-op for fresh installs.
    pass


def downgrade() -> None:
    pass
````

## File: database/migrations/versions/20260815_rec_view_claim.py
````python
"""Prevent duplicate recommendation delivery during concurrent queue rebuilds.

Revision ID: 20260815_rec_view_claim
Revises: 20260808_unlock_photo_cases
Create Date: 2026-08-15
"""

from alembic import op
from sqlalchemy import inspect, text

revision = "20260815_rec_view_claim"
down_revision = "20260808_unlock_photo_cases"
branch_labels = None
depends_on = None

CONSTRAINT_NAME = "uq_recommendation_views_viewer_candidate"


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    constraints = inspector.get_unique_constraints("recommendation_views")
    if any(set(item.get("column_names") or ()) == {"viewer_id", "candidate_id"} for item in constraints):
        return

    if bind.dialect.name == "postgresql":
        op.execute(
            text(
                """
                DELETE FROM recommendation_views older
                USING recommendation_views newer
                WHERE older.viewer_id = newer.viewer_id
                  AND older.candidate_id = newer.candidate_id
                  AND (older.created_at, older.id) > (newer.created_at, newer.id)
                """
            )
        )
    op.create_unique_constraint(CONSTRAINT_NAME, "recommendation_views", ["viewer_id", "candidate_id"])


def downgrade() -> None:
    bind = op.get_bind()
    constraints = inspect(bind).get_unique_constraints("recommendation_views")
    if any(item.get("name") == CONSTRAINT_NAME for item in constraints):
        op.drop_constraint(CONSTRAINT_NAME, "recommendation_views", type_="unique")
````

## File: database/migrations/versions/20260827_confession_key.py
````python
"""Add the confession submission key used for idempotent deep-link creation.

Revision ID: 20260827_confession_key
Revises: 20260815_rec_view_claim
Create Date: 2026-08-27
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision = "20260827_confession_key"
down_revision = "20260815_rec_view_claim"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_columns = {column["name"] for column in inspector.get_columns("confessions")}
    if "submission_key" not in existing_columns:
        with op.batch_alter_table("confessions") as batch:
            batch.add_column(sa.Column("submission_key", sa.String(length=64), nullable=True))

    existing_indexes = {index["name"] for index in inspector.get_indexes("confessions")}
    if "ix_confessions_submission_key" not in existing_indexes:
        op.create_index("ix_confessions_submission_key", "confessions", ["submission_key"], unique=True)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_indexes = {index["name"] for index in inspector.get_indexes("confessions")}
    if "ix_confessions_submission_key" in existing_indexes:
        op.drop_index("ix_confessions_submission_key", table_name="confessions")

    existing_columns = {column["name"] for column in inspector.get_columns("confessions")}
    if "submission_key" in existing_columns:
        with op.batch_alter_table("confessions") as batch:
            batch.drop_column("submission_key")
````

## File: database/migrations/versions/20260828_report_assigned.py
````python
"""Add assigned_to and assigned_at fields to Report model.

Revision ID: 20260828_report_assigned
Revises: 20260828_verif_assigned
Create Date: 2026-08-28
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision = "20260828_report_assigned"
down_revision = "20260828_verif_assigned"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_columns = {column["name"] for column in inspector.get_columns("reports")}
    
    if "assigned_to" not in existing_columns:
        with op.batch_alter_table("reports") as batch:
            batch.add_column(
                sa.Column("assigned_to", sa.BigInteger(), nullable=True)
            )
    
    if "assigned_at" not in existing_columns:
        with op.batch_alter_table("reports") as batch:
            batch.add_column(
                sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=True)
            )
    
    # Create index for assigned_to
    existing_indexes = {index["name"] for index in inspector.get_indexes("reports")}
    if "ix_reports_assigned_to" not in existing_indexes:
        op.create_index("ix_reports_assigned_to", "reports", ["assigned_to"])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_indexes = {index["name"] for index in inspector.get_indexes("reports")}
    
    if "ix_reports_assigned_to" in existing_indexes:
        op.drop_index("ix_reports_assigned_to", table_name="reports")
    
    existing_columns = {column["name"] for column in inspector.get_columns("reports")}
    if "assigned_to" in existing_columns or "assigned_at" in existing_columns:
        with op.batch_alter_table("reports") as batch:
            if "assigned_to" in existing_columns:
                batch.drop_column("assigned_to")
            if "assigned_at" in existing_columns:
                batch.drop_column("assigned_at")
````

## File: database/migrations/versions/20260828_user_accepts_confessions.py
````python
"""Add accepts_confessions field to User model.

Revision ID: 20260828_user_confessions
Revises: 20260827_confession_key
Create Date: 2026-08-28
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision = "20260828_user_confessions"
down_revision = "20260827_confession_key"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_columns = {column["name"] for column in inspector.get_columns("users")}
    
    if "accepts_confessions" not in existing_columns:
        with op.batch_alter_table("users") as batch:
            batch.add_column(
                sa.Column("accepts_confessions", sa.Boolean(), nullable=False, server_default="true")
            )
        
        # Create index for the new column
        existing_indexes = {index["name"] for index in inspector.get_indexes("users")}
        if "ix_users_accepts_confessions" not in existing_indexes:
            op.create_index("ix_users_accepts_confessions", "users", ["accepts_confessions"])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_indexes = {index["name"] for index in inspector.get_indexes("users")}
    
    if "ix_users_accepts_confessions" in existing_indexes:
        op.drop_index("ix_users_accepts_confessions", table_name="users")
    
    existing_columns = {column["name"] for column in inspector.get_columns("users")}
    if "accepts_confessions" in existing_columns:
        with op.batch_alter_table("users") as batch:
            batch.drop_column("accepts_confessions")
````

## File: database/migrations/versions/20260828_verif_assigned.py
````python
"""Add assigned_to and assigned_at fields to VerificationRequest model.

Revision ID: 20260828_verif_assigned
Revises: 20260828_user_confessions
Create Date: 2026-08-28
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision = "20260828_verif_assigned"
down_revision = "20260828_user_confessions"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_columns = {column["name"] for column in inspector.get_columns("verification_requests")}
    
    if "assigned_to" not in existing_columns:
        with op.batch_alter_table("verification_requests") as batch:
            batch.add_column(
                sa.Column("assigned_to", sa.BigInteger(), nullable=True)
            )
    
    if "assigned_at" not in existing_columns:
        with op.batch_alter_table("verification_requests") as batch:
            batch.add_column(
                sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=True)
            )
    
    # Create index for assigned_to
    existing_indexes = {index["name"] for index in inspector.get_indexes("verification_requests")}
    if "ix_verification_requests_assigned_to" not in existing_indexes:
        op.create_index("ix_verification_requests_assigned_to", "verification_requests", ["assigned_to"])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_indexes = {index["name"] for index in inspector.get_indexes("verification_requests")}
    
    if "ix_verification_requests_assigned_to" in existing_indexes:
        op.drop_index("ix_verification_requests_assigned_to", table_name="verification_requests")
    
    existing_columns = {column["name"] for column in inspector.get_columns("verification_requests")}
    if "assigned_to" in existing_columns or "assigned_at" in existing_columns:
        with op.batch_alter_table("verification_requests") as batch:
            if "assigned_to" in existing_columns:
                batch.drop_column("assigned_to")
            if "assigned_at" in existing_columns:
                batch.drop_column("assigned_at")
````

## File: database/migrations/env.py
````python
import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

# ensure project path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import models  # noqa: F401
from config import get_settings
from database.base import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = get_settings()


def run_migrations_offline() -> None:
    raise RuntimeError("Offline migrations not supported; run alembic with an async engine")


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = create_async_engine(settings.database_url, poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_async_migrations())
````

## File: database/__init__.py
````python
from database.base import Base
from database.connection import make_session_factory

__all__ = ("Base", "make_session_factory")
````

## File: database/base.py
````python
import uuid
from datetime import datetime

from sqlalchemy import DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class UUIDPKMixin:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
````

## File: database/connection.py
````python
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from config import Settings


def make_session_factory(
    settings: Settings, *, engine: AsyncEngine | None = None
) -> async_sessionmaker[AsyncSession]:
    engine = engine or create_async_engine(settings.database_url, pool_pre_ping=True)
    return async_sessionmaker(engine, expire_on_commit=False)


async def session_scope(factory: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
    async with factory() as session:
        yield session
````

## File: docs/AI_AGENT_RULES.md
````markdown
# Регламент для ИИ-агентов

Этот регламент обязателен для каждого ИИ-агента, который изменяет проект.

## Правило коммитов

После каждого важного, стабильного и успешно проверенного этапа работы агент обязан:

1. Запустить относящиеся к изменению тесты и убедиться, что они прошли.
2. Проверить состав изменений через `git status` и `git diff`.
3. Выполнить `git add` для необходимых файлов.
4. Создать осмысленный коммит в формате Conventional Commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:` и т. п.
5. Выполнить `git push` в настроенный удалённый репозиторий.

К важным этапам относятся успешное завершение крупной задачи, исправление бага, изменение архитектуры, миграция, успешный набор тестов и любая готовая к передаче пользователю функциональность.

Запрещено оставлять эксперименты, сломанные worktree и непроверенные изменения без ясного статуса. Если `git push` невозможен из-за отсутствующего remote, прав доступа или сети, агент обязан сообщить причину и сохранить успешный локальный коммит.
````

## File: docs/alpha_operations.md
````markdown
# Операции закрытой альфы

## Бэкапы PostgreSQL

Скрипт `scripts/backup_postgres.sh` создаёт проверяемый дамп PostgreSQL в `../backups/` относительно корня проекта и хранит последние 14 дней. Для ручного запуска:

```bash
./scripts/backup_postgres.sh
```

Чтобы установить ежедневный запуск в 03:30 по времени сервера, выполните один раз:

```bash
./scripts/install_backup_cron.sh
```

Для восстановления используйте `pg_restore` в пустую PostgreSQL БД. Перед сменой пароля создан baseline-дамп: `../backups/project1_pre_password_rotation_20260825.dump`.

## Секреты и сетевой доступ

- `.env` не коммитится. Задайте отдельные длинные пароли для PostgreSQL и Redis.
- В Compose не опубликованы порты: PostgreSQL и Redis доступны только контейнеру бота во внутренней сети Docker.
- Redis запускается с паролем; `REDIS_URL` должен содержать этот пароль.
````

## File: docs/api.md
````markdown
# API и внешние интеграции

## Telegram
Проект использует aiogram для работы с Telegram Bot API.

### Основные точки интеграции
- отправка сообщений;
- обработка callback-queries;
- работа с фото и сообщениями;
- настройка команд бота.

## Redis
Redis используется как хранилище FSM и как backend для rate limiting.

## PostgreSQL
База данных хранит все пользовательские и бизнес-данные.

## Внешние расширения
- NSFWService — extension point для интеграции с внешним сервисом модерации фото.
- В текущем варианте он является заглушкой и не выполняет реальную проверку.

## Точки расширения
- уведомления в Telegram;
- будущие интеграции с внешними сервисами модерации;
- возможные webhooks и API-сервисы поверх текущей архитектуры.
````

## File: docs/architecture_decisions.md
````markdown
# Architecture Decisions (ADR)

Дата: 2026-08-05

## ADR-001: Миграции и схема БД

Решение
- Оставить текущее поведение `main.py` (автоматическое создание таблиц + lightweight ALTER statements) как совместимый временный механизм для локальной разработки.
- Ввести явный план перевода проекта на Alembic baseline миграций до production: создать baseline-маршрут, удалить `create_all`/inline-ALTERs из основной ветки релиза и выполнять `alembic upgrade head` в процессе деплоя.

Почему
- Текущая реализация удобна для локальной разработки и CI, но усложняет развёртывание, откаты и историю изменений схемы.

Альтернативы
- Немедленное удаление `create_all` и inline-миграций (отклонено): сломает текущие инсталляции и тесты.

Следующие шаги
- Создать `alembic revision --autogenerate` с baseline-стартом и протестировать миграции в staging.

---

## ADR-002: Секреты в репозитории

Решение
- Признать факт наличия секретов в `.env` как критическую проблему и очистить репозиторий от реальных секретов (в будущем).
- Пока — пометить в отчёте и добавить `docs/` инструкции по безопасной работе с `.env` и `git`.

Почему
- BOT_TOKEN и другие секреты в репозитории представляют серьёзный риск безопасности.

Альтернативы
- Игнорировать (отклонено).

Следующие шаги
- Удалить/переместить `.env` из истории git (BFG/git-filter-branch) и добавить `.env.example`.

---

## ADR-003: Очередь рекомендаций (Queue)

Решение
- Сохранить `MemoryRecommendationQueue` как дефолт для разработки и одного процесса.
- Ввести интерфейс/контракт для Redis-backed очереди и задокументировать миграцию к Redis/atomic operations для production.

Почему
- Memory-queue не синхронизируется между процессами; для масштабирования нужен Redis.

Альтернативы
- Немедленная миграция на Redis (отклонено): дополнительная инфраструктура, не требуемая для текущей функциональности.

Следующие шаги
- Реализовать `RedisRecommendationQueue` и интеграционные тесты.

---

## ADR-004: Логирование и зависимость `structlog`

Решение
- Поддерживать стандартную библиотеку `logging` в кодовой базе и считать `structlog` опциональной зависимостью для future structured logging.
- Пока не применять глобенной миграции на `structlog`.

Почему
- В коде используется `logging`; переход на structlog требует единообразной конфигурации и тестирования.

Альтернативы
- Переход на `structlog` сейчас (отклонено).

Следующие шаги
- Если нужен структурированный лог, добавить конфигурацию и единую точку инициализации логгирования.

---

## ADR-005: Типизация и статический анализ

Решение
- Поддерживать текущие аннотации типов в коде и добавить `mypy` в CI как опциональный шаг.

Почему
- Проект использует современные аннотации, но не выполняет `mypy`-проверку.

Альтернативы
- Немедленное внедрение строгого `mypy --strict` (отклонено): потребует значительных правок.

Следующие шаги
- Добавить `mypy.ini` с разумными настройками и запускать `mypy` в CI; по мере исправления повышать строгость.

---

## ADR-006: Пакетная структура и публичные интерфейсы

Решение
- Сохранить существующую слойную структуру `handlers -> services -> repositories -> models`.
- Документировать назначение слоёв в `docs/project_structure.md` и избегать переноса бизнес-логики из `services` обратно в `handlers`.

Почему
- Текущая архитектура уже модульная и подходит для дальнейшего роста.

Альтернативы
- Сильно реорганизовать сейчас (отклонено): риск регрессий.

Следующие шаги
- Периодически ревью больших сервисов на предмет God Service и разделять обязанности.

---

## ADR-007: Trust System — журнал событий вместо неявной репутации

Решение
- Хранить быстрый внутренний `users.trust_score` и неизменяемые `TrustScoreEvent` с причиной и ссылкой на решение.
- Выделить верификации, автоматические кейсы и фото-проверки в отдельные таблицы и сервисы.
- Записывать решения модераторов в расширенный `AdminLog`; повторная обработка закрытого объекта не меняет состояние.

Почему
- Решения становятся объяснимыми, а будущие наказания, уровни доверия, рейтинг модераторов и anti-fraud/ML добавляются без изменения пользовательского контракта.

Альтернативы
- Одно числовое поле без журнала (отклонено): нет аудита и безопасной идемпотентности.

Следующие шаги
- Подключить реальную локальную модель к `PhotoSafetyProvider` после выбора пакета модели и политики хранения файлов.

---

Все решения и планы в этом документе должны быть расширяемыми и пересматриваемыми при росте продукта.
````

## File: docs/database.md
````markdown
# База данных

## Основные сущности
- User — пользователь Telegram, роль и статус.
- Profile — анкета пользователя: пол, цели, данные профиля, фото, видимость, жалобы, moderation state.
- Like — лайк между пользователями.
- Match — взаимная симпатия.
- Dislike — скрытая/пропущенная анкета.
- Block — двусторонняя блокировка выдачи.
- Report — жалоба на пользователя/анкету.
- Appeal — апелляция после модерации.
- Confession — анонимное признание.
- AdminLog — административные действия.
- RecommendationView — событие показа карточки с рассчитанным Score для аналитики matching.
- VerificationRequest — отправленный видеокружок и решение модератора.
- ModerationCase — независимая очередь автоматической модерации (порог жалоб, NSFW, отсутствие лица).
- PhotoModeration — результат конкретной проверки фотографии и провайдер.
- TrustScoreEvent — неизменяемый журнал изменения внутреннего рейтинга.

## Ключевые правила
- Profiles связаны с пользователями через unique constraint по user_id.
- Likes и dislikes имеют уникальные пары (from_user_id, to_user_id).
- Matches хранят пару пользователей без дублирования.
- Recommendation views хранят viewer, candidate и Score; уникальная пара `(viewer_id, candidate_id)` исключает повторную выдачу, а временные индексы покрывают аналитику.
- Reports и appeals связаны с пользователями и могут быть обработаны администратором.
- Reports имеют уникальную пару `(reporter_id, target_user_id)`, поэтому повторная жалоба идемпотентна.
- `users.trust_score` ограничивается сервисом диапазоном 0–100; причина и ссылка на решение хранятся в TrustScoreEvent.
- `profiles.verification_status` и `profiles.moderation_status` отделены от legacy-флагов видимости/блокировки и готовы к новым уровням доверия.
- При NSFW-оценке выше порога профиль немедленно скрывается и блокируется до ручного решения; отсутствие лица создаёт отдельный кейс замены фото.
- Confessions хранят sender_hash для защиты от спама.

## Текущая схема запуска
- PostgreSQL запускается в контейнере.
- Схема больше не создаётся автоматически при старте через `Base.metadata.create_all`; startup-логика не производит schema mutations.
- Для обновления схемы используется Alembic; baseline-миграция зафиксирована в `database/migrations/versions/20260808_schema_baseline.py`.
- В продакшене следует применять `alembic upgrade head` как единственный путь обновления схемы.

## Расширения профиля
Для модуля регистрации и профиля в таблицу profiles добавлены поля:
- moderation_locked BOOLEAN
- photo_file_ids JSON
- main_photo_file_id VARCHAR(255)
- locale VARCHAR(8)
- extra_data JSON

## Потенциальные риски
- Отсутствие полноценной миграционной истории для всех изменений может усложнить развёртывание.
- Некоторые модели содержат важную бизнес-логику напрямую в репозиториях, что надо контролировать.
- Нужен контроль целостности запросов и индексов по мере роста базы.
- Изменения профиля затрагивают как бизнес-логику, так и UI, поэтому любые изменения схемы должны сопровождаться обновлением сервиса, DTO и валидатора.

## Matching-ограничения и индексы

- `likes` и `dislikes` имеют уникальные пары `(from_user_id, to_user_id)` и индексы по обоим направлениям.
- `matches` нормализует пару через сортировку ID и защищён уникальным ограничением `(user1_id, user2_id)`.
- `blocks` имеет уникальную пару `(blocker_id, blocked_id)`; выдача исключает оба направления пары.
- `profiles.user_id`, `profiles.is_visible`, `users.status`, `likes.from_user_id`, `blocks.blocker_id` используются в фильтрах выдачи.
- `recommendation_views` индексирована по `(viewer_id, created_at)` и `(candidate_id, created_at)` для аналитики и будущего retention.
- Trust-очереди индексированы по пользователю и статусу; `moderation_cases` дополнительно индексирована по типу и источнику.

## Аудит схемы

- Ограничения Like/Match/Report защищают от дубликатов; для существующих инсталляций они становятся гарантией БД после применения Alembic-миграции.
- `report_count` является денормализованным счётчиком; для конкурентных жалоб используется атомарный SQL update path, а не read-modify-write.
- Таблицы событий (`recommendation_views`, `trust_score_events`, `photo_moderations`) требуют retention/партиционирования до роста нагрузки.

## Миграция matching

Добавлены миграции для `recommendation_views` и trust/photo moderation путей; baseline для текущей схемы зафиксирован в `20260808_schema_baseline.py`. Для развёртывания в боевом окружении требуется выполнить `alembic upgrade head` и проверять повторный запуск/рестарт без самостоятельного изменения схемы.
````

## File: docs/dev_notes.md
````markdown
# Dev notes

## Что уже хорошо реализовано
- Основная бизнес-логика вынесена в services/ и repositories/.
- Для ключевых сценариев есть FSM-состояния.
- Есть Docker Compose и базовая конфигурация.
- Для некоторых сценариев уже написаны тесты.

## Что требует внимания
- RecommendationService содержит ошибку в логике возврата результата: после вычисления score функция возвращает None и не возвращает список кандидатов.
- В handlers/dating.py есть сценарий с комментариями к лайку, где логика может быть улучшена и лучше разделена.
- Текущие тексты интерфейса встроены прямо в код, что затрудняет локализацию и поддержку.
- Для продакшена необходимо подключить настоящую модерацию фото.

## Места, которые лучше не менять без необходимости
- main.py и конфигурационный слой.
- модели и базовые репозитории, если нет прямой необходимости в изменении схемы.
- маршруты обработки регистрации и модерации, потому что они тесно связаны с FSM.
````

## File: docs/final_hardening_report.md
````markdown
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
````

## File: docs/manual_two_user_alpha_test.md
````markdown
# Manual two-user ALPHA E2E test checklist

Purpose: Step-by-step manual end-to-end checklist for verifying basic functionality and resilience of the dating bot with two test users (User A and User B). Follow each step and mark ACTUAL and PASS/FAIL.

Usage: run the checklist while two test Telegram accounts are available. For destructive cleanup between runs use the tools/reset_test_data.py utility (development only).

| STEP | ACTION | EXPECTED | ACTUAL | PASS/FAIL | NOTES |
|------|--------|----------|--------|----------|-------|
| 1 | User A: /start | Bot prompts to create a profile or continue registration | | | |
| 2 | User A: complete registration (name/age/district/institution/interests/bio) | Profile draft created; preview shown | | | |
| 3 | User A: Upload first photo (photo 1) | Photo uploaded and accepted by UI | | | |
| 4 | User A: Upload second photo (photo 2) | Photo uploaded and shown as second | | | |
| 5 | User A: Upload third photo (photo 3) | Photo uploaded and shown as third | | | |
| 6 | User A: Check photo order in profile preview | Photos appear in the expected order (1,2,3) | | | |
| 7 | User A: Publish profile | Profile visible (is_visible=True) and claim success message | | | |
| 8 | Repeat steps 1–7 for User B | User B has published profile | | | |
| 9 | User A: Open "Знакомства" / recommendations | User B appears in recommendation card for User A (unless filtered by eligibility) | | | |
| 10 | User B: Open recommendations | User A appears in recommendation card for User B | | | |
| 11 | Inspect match percentage shown on cards | A numeric compatibility/score is displayed and within 0..100 or documented range | | | |
| 12 | User A: Press LIKE for User B | Like recorded; User B receives in-chat notification of like | | | |
| 13 | User B: Verify like notification | Notification received (inline or direct) | | | |
| 14 | User B: Press LIKE for User A | Like recorded and mutual match created | | | |
| 15 | Check that Match event triggers contact exchange (username or contact message) | Both users see contact / username shown or instructions to contact | | | |
| 16 | Check "Симпатии" (sent likes) lists | Each user's sent likes includes the other | | | |
| 17 | Press old inline like/match buttons again (replay callbacks) | Actions are idempotent: no duplicate likes/matches or errors | | | |
| 18 | Verify no duplicate matches in database / UI | Only single Match record exists | | | |
| 19 | User A: Press DISLIKE on User B | Dislike recorded; User B not notified by default | | | |
| 20 | User A: Block User B | Block recorded; User B cannot see User A in recommendations anymore | | | |
| 21 | User A: Send REPORT against User B | Report recorded and report_count incremented; if threshold reached moderation_case may be created | | | |
| 22 | User A: Send another REPORT against User B (duplicate) | Duplicate report from same reporter is prevented (duplicate report policy) | | | |
| 23 | Verify blocked profile is hidden from recommendations for blocker and blocked | Blocked pair no longer returns in recommendations | | | |
| 24 | User A: Edit profile text/bio | Changes saved and visible in preview | | | |
| 25 | User A: Replace a photo in profile | New photo replaces old one, moderation flow triggered if necessary | | | |
| 26 | User A: Delete a photo | Photo removed from profile and UI updates | | | |
| 27 | Trigger stale photo callbacks (simulate or retry stale) | Old inline/photo moderation callback handlers do not crash; UI remains consistent | | | |
| 28 | Attempt to upload 4th photo (beyond allowed limit) | Upload refused with clear message; no silent acceptance | | | |
| 29 | Force ML to mark photo UNDER_REVIEW (simulate provider error or use test hook) | Profile moderation status becomes UNDER_REVIEW and is_visible=False; moderation_locked=True | | | |
| 30 | Run `python -m tools.reset_test_data --user <id_A>` | The profile and all related rows are removed for that user; Redis cleaned for that user | | | |
| 31 | After reset: try to view the deleted profile via recommendations | Profile not present; handlers return user-friendly message or not found handling | | | |
| 32 | Re-register User A from scratch | New profile can be created with same telegram id and functions as expected | | | |
| 33 | Rapid double-click test: quickly press like/dislike twice | Server handles idempotency and no duplicate DB records/errors | | | |
| 34 | Press stale callback for removed/archived profile | Handlers are resilient and do not raise uncaught exceptions | | | |
| 35 | Final sanity: Open recommendations for both users and perform a short happy-path session | No exceptions, correct counts, no duplicated cards or crashes | | | |


## Infrastructure resilience checks (additional manual steps)

| STEP | ACTION | EXPECTED | ACTUAL | PASS/FAIL | NOTES |
|------|--------|----------|--------|----------|-------|
| R1 | While a user session is active, restart Redis server | Bot remains responsive; in-flight operations either succeed or fail gracefully; recommendation queue recovers | | | |
| R2 | Restart bot process (docker compose restart bot) during active session | Bot reconnects; no stuck transactions; no duplicate matches created | | | |
| R3 | Restart PostgreSQL during active session | Long-running transactions handled; system returns to consistent state after DB comes back | | | |
| R4 | Replay old inline callback data (expired/replayed) | Handlers tolerate stale callback data and do not crash; user sees a helpful message | | | |
| R5 | Rapid double-click (like/skip) | No duplicate entries or unhandled exceptions | | | |
| R6 | Request a non-existent or deleted profile via direct link or callback | Handler responds with not-found message; no stack-trace visible to user | | | |


Notes:
- Keep two separate Telegram client sessions; prefer one mobile and one desktop client to simulate realistic timing.
- Use tools/reset_test_data.py for cleanups between runs (development-only). Do NOT run tool in production.
- If you need to publish Redis locally for GUI debugging, copy docker-compose.override.yml.example -> docker-compose.override.yml (this file is gitignored by default) and run docker compose up -d.


Seeding test data (mass profiles):

- To generate a batch of fake test profiles and warm up recommendation queues run inside the bot container (development only):

  export ENV=development
  docker compose exec -T bot /bin/sh -lc "python -m tools.seed_test_profiles --count 50"

- The tool will create users with IDs starting at 200000 and fill Redis recommendation queues by invoking RecommendationService.rebuild_queue for each created user.
````

## File: docs/matching.md
````markdown
# Recommendation Engine, Likes и Matches

## Поток пользователя

Кнопка «💘 Смотреть анкеты» вызывает `RecommendationService`. Сервис получает активную анкету пользователя, строит очередь совместимых кандидатов, показывает самый высокий Score и записывает событие просмотра. Под карточкой показывается только округлённый процент совместимости; внутренние компоненты Score пользователю не раскрываются.

После показа доступны лайк, лайк с сообщением, пропуск, блокировка и жалоба. Лайк удаляет кандидата из текущей очереди, пропуск переносит его в конец очереди, блокировка и жалоба удаляют его из выдачи. Блокировка учитывается в обоих направлениях: ни заблокированный пользователь, ни автор блока не увидят друг друга.

## Стратегии рекомендаций

Движок зависит от интерфейса `RecommendationStrategy` с асинхронным методом `score(viewer, candidate)`. Текущая реализация — `WeightedRecommendationStrategy`; она детерминированно рассчитывает Score 0–100 по компонентам:

- gender — 35;
- target_gender — 25;
- age — 10;
- district — 10;
- institution — 10;
- interests — 7;
- bio — 3.

Весами можно управлять без изменения кода через `MATCHING_WEIGHTS_JSON`. Неизвестные и отрицательные значения отклоняются; нулевые допустимы, пока сумма всех весов положительна. В будущем можно добавить `PopularityRecommendationStrategy`, `ActivityRecommendationStrategy`, `MLRecommendationStrategy` или `HybridRecommendationStrategy`, реализовав `RecommendationStrategy.score(viewer, candidate)` и передав стратегию в `RecommendationService(strategy=...)`.

Контракт подходит для постепенного ML/AI: SQL eligibility-фильтры остаются неизменными, а модель получает только допустимых кандидатов. Для высоконагруженной batch/remote модели потребуется дополнительный batch-контракт, чтобы не выполнять сетевой вызов на каждого кандидата.

Совместимость пола и цели поиска остаётся обязательным фильтром до ранжирования, а стратегия отвечает только за оценку совместимого кандидата. Это не смешивает правила безопасности выдачи с алгоритмом сортировки.

## Очередь и кэширование

`RecommendationQueue` — сменяемый протокол. Runtime по умолчанию использует Redis-реализацию; `MemoryRecommendationQueue` остаётся только для тестов и локальных сценариев одного процесса. Очередь не является источником истины: при исчерпании она строится заново из БД, поэтому учитывает новые анкеты, лайки, блокировки и изменения профиля. Перед возвратом элемента сервис повторно проверяет активность, видимость, лайки и блокировку, поэтому устаревшая очередь не покажет снятую анкету. Если Redis временно недоступен, один кандидат выбирается напрямую из PostgreSQL; запись просмотра атомарно закрепляет пару viewer/candidate, поэтому конкурентный rebuild не может показать одну карточку дважды.

Для нескольких экземпляров бота потребуется Redis-адаптер с атомарными `pop/move/remove`; SQL остаётся источником истины.

## Likes и Match Engine

- `LikeService` создаёт однонаправленный `Like`, валидирует комментарий, запрещает self-like и возвращает признак фактического создания.
- `MatchService` проверяет reciprocal Like, выставляет `is_mutual` у обеих записей и идемпотентно создаёт нормализованную пару `Match`.
- Уникальные ограничения и savepoint-операции защищают от повторов при конкурентных запросах.
- Уведомление о входящем лайке не раскрывает отправителя. Контакты раскрываются только после нового Match; при отсутствии username используется безопасная Telegram-ссылка.
- Вкладка «💕 Мои симпатии» читает только Match через `MatchService`.

## Жалобы и статистика

Жалоба одновременно создаёт Report, создаёт персональную блокировку выдачи и удаляет кандидата из текущей очереди. Повторная жалоба того же пользователя на ту же анкету не увеличивает счётчик. При достижении `REPORT_THRESHOLD` профиль скрывается, блокируется модерацией и администраторам отправляется уведомление.

События просмотров хранятся в `recommendation_views`. `MatchingStatsService` агрегирует views, likes, matches, reports, CTR и среднюю совместимость одним SQL-запросом. `/debug_matching` доступна администраторам и показывает размеры выборки, фильтры пола/цели, возраст, общие районы/интересы и причины исключений.

## Ограничения

- Очередь в памяти не синхронизируется между процессами и теряется при рестарте.
- Метрики пока считаются по всей истории без временных окон и retention-политики.
- Нет baseline Alembic-истории для старой схемы; migration matching рассчитана на уже существующие таблицы пользователей.
- Полная локализация и отдельный domain/event layer ещё не завершены.
- Текущий контракт ранжирования по одному кандидату не оптимален для внешних/batch ML-моделей.
````

## File: docs/next_agent_context.md
````markdown
# Next Agent Context

Документ отражает фактическое состояние после hardening-pass по P0/P1 аудитным находкам.

## Что реализовано

- Регистрация и редактирование профиля продолжают работать через FSM, DTO `ProfileDraft`, валидатор и сервисы профиля без добавления нового пользовательского функционала.
- Recommendation Engine по-прежнему строит совместимую выборку в SQL, ранжирует её стратегией и пишет показы; для текущей архитектуры очередь переведена на Redis-backed implementation при сохранении прежнего интерфейса `RecommendationQueue`.
- Eligibility checks вынесены в доменную/service-логику: лайк, жалоба, блокировка, матч и связанные действия теперь запрещаются для удалённых, скрытых, заблокированных, `UNDER_REVIEW`, неактивных или собственных профилей до попадания в репозиторий/handler.
- Trust/Photo moderation усилили fail-closed поведение: ошибки провайдера, битые изображения, слишком большие файлы и повторные/заменяемые фото не становятся публичными; для одного события moderation case создаётся не бесконечно, а единожды.
- Report counter теперь увеличивается атомарно через PostgreSQL-safe update path, что устраняет lost-update для конкурентных жалоб.
- Alembic взят как единственный источник истины схемы: runtime `create_all` и inline `ALTER/CREATE TYPE` из startup убраны, добавлена baseline-миграция для текущей схемы.

## Добавленные и расширенные таблицы

- `profiles`: профиль, `moderation_locked`, фото, locale/extra_data, `verification_status`, `moderation_status`, `report_count`.
- `likes`, `matches`, `dislikes`, `blocks`: направленные действия; Like/Match/Block защищены уникальными парами.
- `recommendation_views`: viewer/candidate/score, индексы `(viewer_id, created_at)` и `(candidate_id, created_at)`.
- `reports`, `appeals`, `admin_logs`: модерация и аудит; повторные жалобы остаются идемпотентными.
- `verification_requests`, `moderation_cases`, `photo_moderations`, `trust_score_events`: расширяемые данные Trust.

Миграции: `20260805_matching_engine.py`, `20260805_trust_system.py`, `20260806_photo_safety_cache.py`, `20260807_legacy_schema_alignment.py`, `20260808_schema_baseline.py`, `20260808_unlock_resolved_photo_cases.py`. На текущий момент Alembic baseline зафиксирован и приложение больше не пытается менять схему на старте.

## Сервисы и репозитории

- Matching: `RecommendationService`, `RecommendationStrategy`, `WeightedRecommendationStrategy`, `RecommendationQueue`, `RecommendationRepository`.
- Social: `LikeService`/`LikeRepository`, `MatchService`/`MatchRepository`, `ProfileService`, `DiscoveryRepository`.
- Trust: `VerificationService`, `ReportService`, `ModerationService`, `PhotoModerationService`, `TrustScoreService`, `TrustStatsService`, `TrustRepository`.
- Cross-cutting: `NotificationService`, `LocalizationService`, `MatchingStatsService`, rate-limit middleware.

## Интерфейсы, которые нельзя менять без миграции потребителей

- `RecommendationStrategy.score(viewer, candidate)`, `RecommendationService.next_recommendation`, `rebuild_queue`, `skip`, `remove_candidate`.
- `RecommendationQueue.replace/pop/move_to_end/remove/clear` (async methods now; queue operations are awaited by RecommendationService).
- `LikeService.create`, `MatchService.create_if_mutual`, `MatchService.matches_for`.
- `ProfileService.create_or_update` и `ProfileDraft.to_payload()`.
- `PhotoSafetyProvider.assess(photo_file_id)`.
- FSM/callback data: `like:*`, `comment:*`, `skip:*`, `block:*`, `report:*`, `verify:*`, `case:*`, `appeal:*`.

## Принятые решения

## Test utilities

- To reset test data (development only) use: python -m tools.reset_test_data. The tool is located at tools/reset_test_data.py and performs destructive delete operations in a single DB transaction and complementary Redis cleanup. It only runs when ENV or ENVIRONMENT is set to one of: development, dev, test. Do NOT run in production.

- To seed mass test profiles (development only) use: python -m tools.seed_test_profiles --count 50. This will create fake Users/Profiles (IDs start at 200000) and invoke RecommendationService.rebuild_queue for each created user.



- Eligibility (видимость, статус пользователя, лайки, двусторонние блоки, `UNDER_REVIEW`) теперь проверяется в сервисе/репозитории до сохранения действия; стратегия отвечает только за score, а ML/AI не должен обходить этот фильтр.
- Веса matching по-прежнему настраиваются через `MATCHING_WEIGHTS_JSON`; неизвестные/отрицательные значения отклоняются, нулевые допустимы при положительной сумме.
- Report counter использует атомарный SQL update path (`UPDATE ... SET report_count = report_count + 1 RETURNING ...`) и не полагается на read-modify-write.
- Photo safety остаётся fail-closed: при ошибке провайдера, загрузки или декодирования изображения фото не становится публичным, профиль скрывается и создаётся moderation case.
- Redis-backed recommendation queue является текущим multi-process адаптером; `MemoryRecommendationQueue` больше не используется как default path в runtime.

## Текущая валидация

- Unit/integration tests для eligibility, report counter, recommendation queue, photo moderation и performance-пути пройдены локально.
- Ruff и compile check для изменённых модулей пройдены.
- Попытка выполнить реальный Alembic upgrade в этой среде не удалась из-за недоступности целевого PostgreSQL endpoint; в боевом окружении следует выполнять `alembic upgrade head` после развёртывания/доступа к БД.

## Потенциальные проблемы

- Для полного end-to-end proof требуется запустить приложение и worker против живого PostgreSQL/Redis и проверить multi-process/ restart сценарии.
- Событийные таблицы по-прежнему требуют внимания к retention/партиционированию по мере роста нагрузки.
- Внешняя/batch ML-стратегия потребует отдельного batch API, если объём фото станет значительным.
- UI локализован частично, уведомления по-прежнему не имеют outbox/retry очереди.

## Критически важные места

- `repositories/recommendation.py` — safety/visibility SQL-фильтры.
- `services/recommendation.py` и `services/recommendation_strategy.py` — жизненный цикл очереди и расширяемое ранжирование.
- `services/like_service.py`, `services/match_service.py`, их репозитории — идемпотентность и приватность.
- `services/report_service.py`, `services/moderation_service.py`, `repositories/trust.py` — Trust policy и аудит.
- `main.py` и `database/migrations/` — порядок и безопасное обновление схемы.

## Следующий рекомендуемый модуль

Дальнейшее production hardening: live PostgreSQL/Redis integration smoke-test, restart/multi-process regression, наблюдаемость очередей и moderation, а затем при необходимости тонкая оптимизация только по фактическим bottlenecks.
````

## File: docs/project_structure.md
````markdown
# Project Structure

Этот документ описывает назначение каждой папки и слоя проекта, а также рекомендации, какой код куда помещать.

Общая идея: чёткое разделение ответственности по слоям, минимальная связность и возможность замены реализаций через интерфейсы/контракты.

- `main.py` — точка входа приложения. Инициализация конфигурации, подключения к БД/Redis и запуск aiogram dispatcher.

- `bot/` — инфраструктура бота: фабрика dispatcher, установка команд, контейнеры/интеграция с aiogram. Здесь не должно быть бизнес-логики.

- `handlers/` — Telegram обработчики и маршруты (aiogram routers). Должны быть "тонкими":
  - Вызовы `services` и `repositories` только через чёткие интерфейсы.
  - Минимальная валидация, переходы по FSM, подготовка аргументов для вызовов бизнес-логики.

- `states/` — определения FSM (`StatesGroup`). Каждый сценарий — отдельный модуль/класс.

- `services/` — бизнес-логика приложения. Здесь находятся сервисы, которые:
  - Координируют репозитории и внешний мир (уведомления, очереди).
  - Не должны напрямую управлять HTTP/Telegram API (за это отвечает `notification_service` или отдельный адаптер).
  - Быть единичной ответственностью (каждый сервис — одна область: `ProfileService`, `LikeService`, `MatchService`, `RecommendationService`).

- `repositories/` — слой доступа к данным и SQL. Правила:
  - Все SQL должны находиться здесь.
  - Репозитории предоставляют простые, переиспользуемые методы (by_user_id, add, create_once и т.п.).
  - Не помещайте бизнес-логику в репозитории.

- `models/` — SQLAlchemy ORM-модели и перечисления. Модели должны быть максимально «тонкими» (описание полей, ограничения, связи).

- `dtos/` — Data Transfer Objects (например `ProfileDraft`) для преобразования между handler и service; DTO помогают отделять внешнее представление от модели БД.

- `middlewares/` — aiogram middlewares (DB session, rate limiting, user sync). Middleware может класть `session`/`settings`/`redis` в `data`.

- `filters/` — aiogram фильтры (например `IsAdmin`). Простые, переиспользуемые предикаты.

- `keyboards/` — генерация inline/reply-клавиатур и callback data. Чисто-презентационный код.

- `utils/` — небольшие утилиты, не относящиеся к бизнес-логике (например `contacts` helper). Не храните здесь большие сервисы.

- `database/` — конфигурация SQLAlchemy, фабрики сессий, Alembic migration scripts. `migrations/` — код alembic. Рекомендация: использовать Alembic как источник правды для схемы в production.

- `docs/` — документация проекта: архитектура, ADR, инструкции по развёртыванию и разработке.

- `tests/` — тесты (unit/asyncio/интеграционные). Тесты должны покрывать границы сервисов и репозиториев.

Рекомендации по размещению кода
- Новые SQL-запросы и фильтры — в `repositories/`.
- Логика проверки согласованности/идемпотентности — в `services/`, не в `handlers/`.
- Адаптеры внешних сервисов (Telegram/NSFW API/Redis) — отдельные классы и подключаются через DI в `services`.

Перемещение и реорганизация
- Избегайте масштабных рефакторингов без тестов. Разделяйте большие модули постепенно:
  - Если файл > 400 строк и имеет более двух областей ответственности — разбить.
  - Не создавать циклических импортов: опирайтесь на интерфейсы и отложенные импорты внутри функций.

CI/Quality
- Статический анализ: `ruff` настроен в `pyproject.toml`.
- Добавить `mypy` в CI и постепенно повышать покрытие типов.

Безопасность
- Никогда не хранить реальные секреты в репозитории. Держать `.env.example` в репозитории и реальные секреты через CI/secret manager.

Этот документ — живая справка. Обновляйте его при серьёзных перестановках архитектуры.
````

## File: docs/trust.md
````markdown
# Trust System: локальная проверка фото

## Провайдеры

`PHOTO_SAFETY_PROVIDER` выбирает провайдер без изменения handlers:

- `ml` — production-вариант: OpenNSFW-совместимая ONNX-модель и YuNet ONNX для лица, только CPU и локальные файлы;
- `heuristic` — development-заглушка, не предназначена для production;
- `disabled` — явное отключение проверки только для изолированных локальных сценариев.

Для `ml` положите модели в `./models` (либо задайте `PHOTO_SAFETY_MODELS_DIR`) и выставьте пути контейнера в `.env`:

```env
PHOTO_SAFETY_PROVIDER=ml
NSFW_MODEL_PATH=/models/open_nsfw.onnx
FACE_MODEL_PATH=/models/face_detection_yunet_2023mar.onnx
```

YuNet распространяется OpenCV Zoo под MIT; используйте проверенный файл из официального репозитория OpenCV Zoo. NSFW-модель должна быть совместима с OpenNSFW: вход BGR NCHW `1×3×224×224`, выход `[sfw, nsfw]`. Перед размещением модели фиксируйте её источник, лицензию и SHA-256 в процедуре поставки. Во время работы бота модели и фото никуда не отправляются.

## Безопасность и кэш

Telegram-файл проверяется по фактическим байтам, а не по MIME/расширению. Разрешены JPEG, PNG и WebP; EXIF удаляется нормализацией. Ограничения на размер, пиксели и минимальную сторону задаются `PHOTO_SAFETY_*` в `.env`.

SHA-256 считается по нормализованному изображению. Ранее проверенный хэш повторно не отправляется в ML-модель; его решение копируется в запись нового пользователя/файла. Уникальная пара `user_id/content_hash` не допускает дублирования истории одной анкеты.

Любая ошибка скачивания, декодирования, модели или некорректный score переводит анкету в `UNDER_REVIEW`, скрывает её из рекомендаций и создаёт кейс ручной модерации. Исключения не возвращаются пользователю как traceback.

## Рекомендации по развитию

- Добавить фоновую очередь для CPU inference и метрики latency/error-rate.
- Проверять подпись и SHA-256 model manifest при старте контейнера.
- Ввести отдельный тип кейса `PHOTO_PROVIDER_ERROR` вместо технического использования NSFW-кейса.
- Добавить retention для исходных фото и журналов moderation, а также нагрузочные тесты очереди.
````

## File: dtos/profile_dto.py
````python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ProfileDraft:
    gender: str | None = None
    target_gender: str | None = None
    name: str | None = None
    age: int | None = None
    district: str | None = None
    institution: str | None = None
    interests: list[str] = field(default_factory=list)
    bio: str | None = None
    photo_file_ids: list[str] = field(default_factory=list)
    main_photo_file_id: str | None = None
    locale: str = "ru"
    is_visible: bool = True
    extra_data: dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        return {
            "gender": self.gender,
            "target_gender": self.target_gender,
            "name": self.name,
            "age": self.age,
            "district": self.district,
            "institution": self.institution,
            "interests": self.interests,
            "bio": self.bio,
            "photo_file_ids": self.photo_file_ids,
            "main_photo_file_id": self.main_photo_file_id,
            "locale": self.locale,
            "is_visible": self.is_visible,
            "extra_data": self.extra_data,
        }
````

## File: filters/__init__.py
````python

````

## File: filters/admin.py
````python
from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: set[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return bool(message.from_user and message.from_user.id in self.admin_ids)
````

## File: filters/chat_type.py
````python
from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsPrivate(BaseFilter):
    async def __call__(self, message: Message) -> bool: return message.chat.type == "private"
````

## File: handlers/appeals.py
````python
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from models import UserStatus
from repositories.appeal import AppealRepository
from repositories.trust import TrustRepository
from repositories.user import UserRepository
from services.notification_service import NotificationService
from states.appeal import AppealState
from utils.admin_ui import compact_display_id, user_display_name
from utils.document_links import documents_keyboard

router = Router()


@router.message(F.text == "🆘 Апелляция")
async def appeal_start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    user = await UserRepository(session).get(message.from_user.id)
    if user is None or user.status not in {UserStatus.SUSPENDED, UserStatus.BANNED}:
        await message.answer(
            "⚠️ Апелляция доступна только после ограничения или блокировки анкеты."
        )
        return
    existing = await AppealRepository(session).active_for_user(message.from_user.id)
    if existing is not None:
        await message.answer(
            "⚖️ У вас уже есть активная апелляция на рассмотрении. Модератор свяжется с вами после проверки."
        )
        return
    await state.set_state(AppealState.enter_text)
    await message.answer(
        "🆘 Апелляция\nОпишите ситуацию для модератора в свободной форме (20–1500 символов).\n\n"
        "Перед подачей можно быстро ознакомиться с правилами сообщества и процессом апелляции:",
        reply_markup=documents_keyboard("community", "moderation", "safety"),
    )


@router.message(AppealState.enter_text)
async def appeal_send(message: Message, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    text = (message.text or "").strip()
    if not 20 <= len(text) <= 1500:
        await message.answer("⚠️ Текст должен быть от 20 до 1500 символов.")
        return
    appeal = await AppealRepository(session).create(message.from_user.id, text)
    await state.clear()
    notifier = NotificationService(message.bot)
    for admin_id in settings.admin_ids:
        await notifier.safe_send(
            admin_id,
            (
                f"⚖️ Новая апелляция {compact_display_id(appeal.id)}\n"
                f"Пользователь: {user_display_name(appeal.user_id)}\n\n{text[:400]}"
            ),
            dedupe_key=f"appeal:{appeal.id}",
        )
        await TrustRepository(session).log(
            admin_id,
            "appeal_notice_sent",
            target_type="appeal",
            target_id=str(appeal.id),
            metadata={"user_id": appeal.user_id},
        )
    await message.answer(
        "✅ Апелляция передана администрации. Если потребуется, модератор "
        "свяжется с вами со своего личного Telegram-аккаунта. Бот не "
        "участвует в дальнейшем общении."
    )
````

## File: handlers/likes.py
````python
from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.discovery import DiscoveryRepository
from services.match_service import MatchService

router = Router()


@router.message(F.text.in_({"❤️ Симпатии", "💕 Мои симпатии"}))
async def likes_history(message: Message, session: AsyncSession) -> None:
    repo = DiscoveryRepository(session)
    matches = await MatchService(session).matches_for(message.from_user.id)

    match_lines: list[str] = []
    for match in matches[:20]:
        partner_id = match.user2_id if match.user1_id == message.from_user.id else match.user1_id
        profile, user = await repo.profile_and_user(partner_id)
        name = profile.name if profile else "Пользователь"
        contact = f"@{user.username}" if user and user.username else f"<a href=\"tg://user?id={partner_id}\">{name}</a>"
        match_lines.append(f"• {name} — {contact}")

    matches_text = "\n".join(match_lines) if match_lines else "Пока нет взаимных симпатий."
    await message.answer(
        f"<b>Взаимные симпатии и контакты</b>\n{matches_text}\n\n"
        "Входящие лайки остаются анонимными до взаимного лайка."
    )
````

## File: keyboards/__init__.py
````python

````

## File: middlewares/__init__.py
````python

````

## File: middlewares/db.py
````python
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, factory: async_sessionmaker[AsyncSession]) -> None:
        self.factory = factory

    async def __call__(self, handler: Callable[..., Awaitable[Any]], event: Any, data: dict[str, Any]) -> Any:
        async with self.factory() as session:
            data["session"] = session
            try:
                result = await handler(event, data)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise
````

## File: middlewares/i18n.py
````python
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from repositories.profile import ProfileRepository
from services.localization import LocalizationService

SUPPORTED_LOCALES = {"ru", "ro"}


def normalize_locale(value: str | None) -> str:
    code = (value or "ru").split("-", 1)[0].lower()
    return code if code in SUPPORTED_LOCALES else "ru"


class FSMI18nMiddleware(BaseMiddleware):
    def __init__(self, localizer: LocalizationService | None = None) -> None:
        self.localizer = localizer or LocalizationService()

    async def __call__(
        self,
        handler: Callable[..., Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        telegram_user = data.get("event_from_user")
        locale = normalize_locale(getattr(telegram_user, "language_code", None))
        session = data.get("session")
        if telegram_user is not None and session is not None:
            profile = await ProfileRepository(session).by_user_id(telegram_user.id)
            if profile is not None:
                locale = normalize_locale(profile.locale)
        data["locale"] = locale
        data["localizer"] = self.localizer
        return await handler(event, data)
````

## File: models/__init__.py
````python
from models.admin_log import AdminLog
from models.appeal import Appeal, AppealStatus
from models.block import Block
from models.confession import Confession, ConfessionDailyLimit, ConfessionStatus
from models.dislike import Dislike
from models.like import Like
from models.match import Match
from models.profile import Gender, ModerationStatus, Profile, VerificationStatus
from models.recommendation_view import RecommendationView
from models.report import Report, ReportReason, ReportStatus
from models.trust import (
    ModerationCase,
    ModerationCaseStatus,
    ModerationCaseType,
    PhotoModeration,
    TrustScoreEvent,
    VerificationDecision,
    VerificationRequest,
)
from models.user import User, UserRole, UserStatus

__all__ = (
    "AdminLog",
    "Appeal",
    "AppealStatus",
    "Block",
    "Confession",
    "ConfessionDailyLimit",
    "ConfessionStatus",
    "Dislike",
    "Gender",
    "Like",
    "Match",
    "ModerationCase",
    "ModerationCaseStatus",
    "ModerationCaseType",
    "ModerationStatus",
    "PhotoModeration",
    "Profile",
    "RecommendationView",
    "Report",
    "ReportReason",
    "ReportStatus",
    "TrustScoreEvent",
    "User",
    "UserRole",
    "UserStatus",
    "VerificationDecision",
    "VerificationRequest",
    "VerificationStatus",
)
````

## File: models/.gitkeep
````

````

## File: models/admin_log.py
````python
from sqlalchemy import JSON, BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class AdminLog(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "admin_logs"
    admin_id: Mapped[int] = mapped_column(BigInteger, index=True)
    action: Mapped[str] = mapped_column(String(64))
    target_type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    target_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    target_user_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
````

## File: models/block.py
````python
from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class Block(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "blocks"
    __table_args__ = (UniqueConstraint("blocker_id", "blocked_id"),)

    blocker_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    blocked_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
````

## File: models/confession.py
````python
import enum
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class ConfessionStatus(str, enum.Enum):
    DELIVERED = "DELIVERED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


class Confession(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "confessions"
    sender_hash: Mapped[str] = mapped_column(String(64), index=True)
    submission_key: Mapped[str | None] = mapped_column(String(64), nullable=True, unique=True, index=True)
    recipient_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    target_username: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    # Pending deep links are tied to a mutable Telegram username.  They must
    # expire before that username can be reassigned to another account.
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    text: Mapped[str] = mapped_column(Text)
    status: Mapped[ConfessionStatus] = mapped_column(Enum(ConfessionStatus), default=ConfessionStatus.PENDING)


class ConfessionDailyLimit(Base):
    """Atomic per-day sender counter keyed by the daily salted sender hash."""

    __tablename__ = "confession_daily_limits"
    sender_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    sent_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
````

## File: models/dislike.py
````python
from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class Dislike(UUIDPKMixin, TimestampMixin, Base):
    """A skip is retained for analytics; recommendation queues place it at the end."""

    __tablename__ = "dislikes"
    __table_args__ = (UniqueConstraint("from_user_id", "to_user_id"),)

    from_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    to_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
````

## File: models/like.py
````python
from sqlalchemy import BigInteger, Boolean, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class Like(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("from_user_id", "to_user_id"),)
    from_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    to_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_mutual: Mapped[bool] = mapped_column(Boolean, default=False)
````

## File: models/match.py
````python
from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class Match(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "matches"
    __table_args__ = (UniqueConstraint("user1_id", "user2_id"),)
    user1_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    user2_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
````

## File: models/profile.py
````python
import enum
from typing import TYPE_CHECKING

from sqlalchemy import JSON, BigInteger, Boolean, CheckConstraint, Enum, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base, TimestampMixin, UUIDPKMixin

if TYPE_CHECKING:
    from models.user import User


class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    ALL = "ALL"


class VerificationStatus(str, enum.Enum):
    UNVERIFIED = "UNVERIFIED"
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class ModerationStatus(str, enum.Enum):
    CLEAR = "CLEAR"
    UNDER_REVIEW = "UNDER_REVIEW"


class Profile(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "profiles"
    __table_args__ = (CheckConstraint("age >= 14 AND age <= 99", name="valid_age"),)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    target_gender: Mapped[Gender] = mapped_column(Enum(Gender))
    name: Mapped[str] = mapped_column(String(64))
    age: Mapped[int] = mapped_column(SmallInteger)
    district: Mapped[str] = mapped_column(String(64), index=True)
    institution: Mapped[str] = mapped_column(String(128), index=True)
    interests: Mapped[list[str]] = mapped_column(JSON, default=list)
    bio: Mapped[str] = mapped_column(Text)
    photo_file_id: Mapped[str] = mapped_column(String(255), default="")
    photo_file_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    main_photo_file_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    locale: Mapped[str] = mapped_column(String(8), default="ru")
    extra_data: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    moderation_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    report_count: Mapped[int] = mapped_column(Integer, default=0)
    verification_status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus), default=VerificationStatus.UNVERIFIED, index=True
    )
    moderation_status: Mapped[ModerationStatus] = mapped_column(
        Enum(ModerationStatus), default=ModerationStatus.CLEAR, index=True
    )
    user: Mapped["User"] = relationship(back_populates="profile")
````

## File: models/recommendation_view.py
````python
from sqlalchemy import BigInteger, Float, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class RecommendationView(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "recommendation_views"
    __table_args__ = (
        UniqueConstraint("viewer_id", "candidate_id", name="uq_recommendation_views_viewer_candidate"),
        Index("ix_recommendation_views_viewer_created", "viewer_id", "created_at"),
        Index("ix_recommendation_views_candidate_created", "candidate_id", "created_at"),
    )

    viewer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    candidate_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    score: Mapped[float] = mapped_column(Float)
````

## File: models/user.py
````python
import enum
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from models.profile import Profile


class UserRole(str, enum.Enum):
    USER = "USER"
    MODERATOR = "MODERATOR"
    HEAD_MODERATOR = "HEAD_MODERATOR"
    CHIEF_MODERATOR = "HEAD_MODERATOR"
    OWNER = "OWNER"
    ADMIN = "ADMIN"


class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    SUSPENDED = "SUSPENDED"
    BANNED = "BANNED"


class User(TimestampMixin, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.ACTIVE, index=True)
    # Internal-only value. It must never be rendered in the user interface.
    trust_score: Mapped[int] = mapped_column(Integer, default=95, index=True)
    accepts_confessions: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    profile: Mapped["Profile | None"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
````

## File: privacy/community-guidelines.md
````markdown
# Правила сообщества MeAnima

Простыми словами — как быть здесь классным человеком.

---

**Будь настоящим.** Фото — твои, анкета — про тебя. Не притворяйся кем-то другим.

**Уважай других.** Никаких оскорблений, травли, угроз. Отказ — это нормально, прими его спокойно.

**Никакого спама и разводов.** Не рекламируй, не проси денег, не веди людей на подозрительные сайты.

**Без откровенного контента.** Фото и описания должны быть без наготы и сексуального контента.

**Не обходи правила.** Если тебя ограничили — не создавай новый аккаунт в обход. Лучше подай апелляцию.

**Заботься о себе.** Не спеши делиться личными данными, будь внимателен при переходе в другие мессенджеры. Подробности — в разделе Dating Safety.

**Видишь нарушение — сообщи.** Кнопки `Report` и `Block` — твои инструменты. Мы разбираем каждую жалобу.

---

Если анкету заморозили — это не всегда финал. Можно подать апелляцию, и модератор рассмотрит ситуацию заново.

MeAnima сейчас в закрытой альфе — если что-то работает не так, пиши через `/help`, мы правда читаем.
````

## File: privacy/dating-safety.md
````markdown
# Безопасность знакомств — MeAnima

Несколько практических правил, которые стоит держать в голове.

---

## Прежде чем делиться личным

- Не спеши сообщать адрес, место учёбы/работы, финансовые данные или документы новому знакомому.
- Настороженно относись к собеседнику, который слишком быстро настаивает на личных данных.

## Переход в другие мессенджеры

- Если собеседник сразу и настойчиво зовёт перейти в другой мессенджер, не отвечая на обычные вопросы — это повод насторожиться.
- Не спеши — лучше сначала пообщаться внутри MeAnima, где работает модерация.

## Деньги

- **Никогда не переводи деньги** человеку, с которым познакомился в приложении, — вне зависимости от причины (помощь, "долг", "срочная ситуация").
- Просьбы о деньгах, подарочных картах, крипте от нового знакомого — почти всегда мошенничество.

## Если что-то не так

- Собеседник давит, угрожает, шантажирует — сразу используй `Block` и `Report`, и по возможности сохрани переписку.
- При реальной угрозе безопасности обращайся не только в поддержку MeAnima, но и в соответствующие службы (полиция и т.п.) — мы можем помочь с модерацией внутри сервиса, но не заменяем экстренные службы.

## Личные встречи

- Первую встречу лучше назначать в людном публичном месте.
- Стоит сообщить кому-то из близких, куда и с кем идёшь.

## Report и Block — как этим пользоваться

- `Report` — сообщить о нарушении: спам, оскорбления, фейковый профиль, мошенничество, неприемлемый контент.
- `Block` — сразу прекратить любое взаимодействие с конкретным пользователем.
- Обе кнопки доступны прямо из чата или анкеты. Жалобы рассматриваются модератором.
````

## File: privacy/moderation-and-appeals.md
````markdown
# Модерация и апелляции — MeAnima

Как работает проверка анкет, фото и жалоб, и что делать, если ты не согласен с решением.

---

## Почему анкета или фото могут попасть на проверку

- Фото проходят автоматическую проверку при загрузке.
- Профиль может быть отправлен на ручную проверку модератором, если на него поступают жалобы от других пользователей.
- При накоплении нескольких жалоб на профиль срабатывает автоматическая временная заморозка анкеты — это защитная мера, а не окончательное решение.

Мы намеренно не раскрываем точные внутренние пороги и механику защиты от злоупотреблений — это сделано, чтобы их было сложнее обойти.

## Что происходит после заморозки

- Анкета временно не показывается другим пользователям.
- Модератор рассматривает ситуацию: жалобы, содержание анкеты, историю поведения.
- По итогам модератор может: снять заморозку, оставить предупреждение, или заблокировать анкету на более длительный срок.

## Какие действия может предпринять администрация

- Временная заморозка анкеты.
- Предупреждение пользователю.
- Временная или постоянная блокировка аккаунта — в случае серьёзных или повторных нарушений.

## Как подать апелляцию

Если ты считаешь, что анкету заморозили или заблокировали по ошибке:

1. Напиши через `/help` в боте или на `meanima.support@gmail.com`.
2. Опиши ситуацию — что произошло, почему ты считаешь решение ошибочным.
3. Модератор рассмотрит апелляцию и сообщит решение.

## Что происходит после апелляции

- Апелляция рассматривается вручную — это не мгновенный автоматический процесс.
- Возможные исходы: анкета восстанавливается полностью, восстанавливается с предупреждением, или решение о блокировке остаётся в силе.
- Решение по апелляции является окончательным на данном этапе — отдельного механизма многоступенчатого обжалования в закрытой альфе пока нет.
````

## File: repositories/__init__.py
````python
from repositories.appeal import AppealRepository as AppealRepository
from repositories.confession import ConfessionRepository as ConfessionRepository
from repositories.discovery import DiscoveryRepository as DiscoveryRepository
from repositories.like import LikeRepository as LikeRepository
from repositories.match import MatchRepository as MatchRepository
from repositories.matching_stats import MatchingStatsRepository as MatchingStatsRepository
from repositories.profile import ProfileRepository as ProfileRepository
from repositories.recommendation import RecommendationRepository as RecommendationRepository
from repositories.report import ReportRepository as ReportRepository
from repositories.user import UserRepository as UserRepository

__all__ = (
    "AppealRepository",
    "ConfessionRepository",
    "DiscoveryRepository",
    "LikeRepository",
    "MatchRepository",
    "MatchingStatsRepository",
    "ProfileRepository",
    "RecommendationRepository",
    "ReportRepository",
    "UserRepository",
)
````

## File: repositories/base.py
````python
from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self.session, self.model = session, model

    async def get(self, key: object) -> T | None:
        return await self.session.get(self.model, key)

    async def add(self, instance: T) -> T:
        self.session.add(instance)
        await self.session.flush()
        return instance
````

## File: repositories/confession.py
````python
import uuid
from datetime import UTC, datetime

from sqlalchemy import or_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Confession, ConfessionDailyLimit, ConfessionStatus


class ConfessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, confession: Confession) -> Confession:
        nested = getattr(self.session, "begin_nested", None)
        try:
            if nested is None:
                self.session.add(confession)
                await self.session.flush()
            else:
                async with nested():
                    self.session.add(confession)
                    await self.session.flush()
        except IntegrityError:
            if confession.submission_key:
                existing = await self.by_submission_key(confession.submission_key)
                if existing is not None:
                    return existing
            raise
        return confession

    async def by_submission_key(self, submission_key: str) -> Confession | None:
        return await self.session.scalar(
            select(Confession).where(Confession.submission_key == submission_key)
        )

    async def reserve_daily_send(self, sender_hash: str, *, limit: int) -> bool:
        """Reserve one send without a read/modify/write race between workers."""
        statement = (
            insert(ConfessionDailyLimit)
            .values(sender_hash=sender_hash, sent_count=1)
            .on_conflict_do_update(
                index_elements=[ConfessionDailyLimit.sender_hash],
                set_={"sent_count": ConfessionDailyLimit.sent_count + 1},
                where=ConfessionDailyLimit.sent_count < limit,
            )
            .returning(ConfessionDailyLimit.sender_hash)
        )
        return (await self.session.scalar(statement)) is not None

    async def get_pending(self, confession_id: uuid.UUID) -> Confession | None:
        return await self.session.scalar(
            select(Confession).where(
                Confession.id == confession_id,
                Confession.status == ConfessionStatus.PENDING,
                or_(Confession.expires_at.is_(None), Confession.expires_at > datetime.now(UTC)),
            )
        )

    async def claim_pending(self, confession_id: uuid.UUID, recipient_id: int) -> Confession | None:
        """Claim exactly once so repeated /start updates cannot redeliver it."""
        result = await self.session.execute(
            update(Confession)
            .where(
                Confession.id == confession_id,
                Confession.status == ConfessionStatus.PENDING,
                or_(Confession.expires_at.is_(None), Confession.expires_at > datetime.now(UTC)),
            )
            .values(recipient_id=recipient_id, status=ConfessionStatus.DELIVERED)
            .returning(Confession)
        )
        return result.scalar_one_or_none()
````

## File: repositories/like.py
````python
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Like


class LikeRepository:
    def __init__(self, session: AsyncSession) -> None: self.session = session
    async def exists(self, source: int, target: int) -> bool:
        statement = select(Like.id).where(Like.from_user_id == source, Like.to_user_id == target)
        return bool(await self.session.scalar(statement))
    async def add(self, source: int, target: int, comment: str | None = None) -> tuple[Like, bool]:
        existing = await self.session.scalar(select(Like).where(Like.from_user_id == source, Like.to_user_id == target))
        if existing:
            return existing, False
        like = Like(from_user_id=source, to_user_id=target, comment=comment)
        try:
            async with self.session.begin_nested():
                self.session.add(like)
                await self.session.flush()
        except IntegrityError:
            existing = await self.session.scalar(
                select(Like).where(Like.from_user_id == source, Like.to_user_id == target)
            )
            if existing is not None:
                return existing, False
            raise
        return like, True
    async def reciprocal(self, source: int, target: int) -> Like | None:
        return await self.session.scalar(select(Like).where(Like.from_user_id == target, Like.to_user_id == source))
````

## File: repositories/match.py
````python
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Match


class MatchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_between(self, first_user_id: int, second_user_id: int) -> Match | None:
        first, second = sorted((first_user_id, second_user_id))
        return await self.session.scalar(
            select(Match).where(Match.user1_id == first, Match.user2_id == second)
        )

    async def create_once(self, first_user_id: int, second_user_id: int) -> tuple[Match, bool]:
        first, second = sorted((first_user_id, second_user_id))
        existing = await self.get_between(first, second)
        if existing is not None:
            return existing, False
        match = Match(user1_id=first, user2_id=second)
        try:
            async with self.session.begin_nested():
                self.session.add(match)
                await self.session.flush()
        except IntegrityError:
            existing = await self.get_between(first, second)
            if existing is not None:
                return existing, False
            raise
        return match, True

    async def by_user_id(self, user_id: int, limit: int = 50) -> list[Match]:
        statement = (
            select(Match)
            .where((Match.user1_id == user_id) | (Match.user2_id == user_id))
            .order_by(Match.created_at.desc())
            .limit(limit)
        )
        return list((await self.session.scalars(statement)).all())
````

## File: repositories/matching_stats.py
````python
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Like, Match, RecommendationView, Report, User, UserStatus


class MatchingStatsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def snapshot(self) -> dict[str, float | int]:
        result = await self.session.execute(
            select(
                func.count(User.id),
                func.count(User.id).filter(User.status == UserStatus.ACTIVE),
                select(func.count(Like.id)).scalar_subquery(),
                select(func.count(Match.id)).scalar_subquery(),
                select(func.count(Report.id)).scalar_subquery(),
                select(func.count(RecommendationView.id)).scalar_subquery(),
                select(func.avg(RecommendationView.score)).scalar_subquery(),
            )
        )
        users, active_users, likes, matches, reports, views, average_score = result.one()
        return {
            "users": int(users or 0),
            "active_users": int(active_users or 0),
            "likes": int(likes or 0),
            "matches": int(matches or 0),
            "reports": int(reports or 0),
            "views": int(views or 0),
            "ctr": round(100 * int(likes or 0) / int(views), 2) if views else 0.0,
            "average_compatibility": round(float(average_score or 0), 2),
        }
````

## File: repositories/profile.py
````python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Profile
from repositories.base import BaseRepository


class ProfileRepository(BaseRepository[Profile]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Profile)

    async def by_user_id(self, user_id: int) -> Profile | None:
        return await self.session.scalar(select(Profile).where(Profile.user_id == user_id))

    async def save(self, profile: Profile) -> Profile:
        self.session.add(profile)
        await self.session.flush()
        return profile
````

## File: repositories/recommendation.py
````python
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Block, Dislike, Like, ModerationStatus, Profile, RecommendationView, User, UserStatus


class RecommendationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def profile(self, user_id: int) -> Profile | None:
        return await self.session.scalar(select(Profile).where(Profile.user_id == user_id))

    async def eligible_profiles(self, user_id: int) -> list[Profile]:
        liked_ids = select(Like.to_user_id).where(Like.from_user_id == user_id)
        disliked_ids = select(Dislike.to_user_id).where(Dislike.from_user_id == user_id)
        blocked_by_me = select(Block.blocked_id).where(Block.blocker_id == user_id)
        blocked_me = select(Block.blocker_id).where(Block.blocked_id == user_id)
        viewed_ids = select(RecommendationView.candidate_id).where(RecommendationView.viewer_id == user_id)
        statement = (
            select(Profile)
            .join(User)
            .where(
                Profile.user_id != user_id,
                Profile.is_visible.is_(True),
                Profile.moderation_locked.is_(False),
                Profile.moderation_status == ModerationStatus.CLEAR,
                User.status == UserStatus.ACTIVE,
                Profile.user_id.not_in(liked_ids),
                Profile.user_id.not_in(disliked_ids),
                Profile.user_id.not_in(blocked_by_me),
                Profile.user_id.not_in(blocked_me),
                Profile.user_id.not_in(viewed_ids),
            )
        )
        return list((await self.session.scalars(statement)).all())

    async def eligible_profile(self, user_id: int, candidate_id: int) -> Profile | None:
        liked_ids = select(Like.to_user_id).where(Like.from_user_id == user_id)
        disliked_ids = select(Dislike.to_user_id).where(Dislike.from_user_id == user_id)
        blocked_by_me = select(Block.blocked_id).where(Block.blocker_id == user_id)
        blocked_me = select(Block.blocker_id).where(Block.blocked_id == user_id)
        viewed_ids = select(RecommendationView.candidate_id).where(RecommendationView.viewer_id == user_id)
        statement = (
            select(Profile)
            .join(User)
            .where(
                Profile.user_id == candidate_id,
                Profile.user_id != user_id,
                Profile.is_visible.is_(True),
                Profile.moderation_locked.is_(False),
                Profile.moderation_status == ModerationStatus.CLEAR,
                User.status == UserStatus.ACTIVE,
                Profile.user_id.not_in(liked_ids),
                Profile.user_id.not_in(disliked_ids),
                Profile.user_id.not_in(blocked_by_me),
                Profile.user_id.not_in(blocked_me),
                Profile.user_id.not_in(viewed_ids),
            )
        )
        return await self.session.scalar(statement)

    async def active_profiles(self, user_id: int) -> list[Profile]:
        disliked_ids = select(Dislike.to_user_id).where(Dislike.from_user_id == user_id)
        blocked_by_me = select(Block.blocked_id).where(Block.blocker_id == user_id)
        blocked_me = select(Block.blocker_id).where(Block.blocked_id == user_id)
        statement = (
            select(Profile)
            .join(User)
            .where(
                Profile.user_id != user_id,
                Profile.is_visible.is_(True),
                Profile.moderation_locked.is_(False),
                Profile.moderation_status == ModerationStatus.CLEAR,
                User.status == UserStatus.ACTIVE,
                Profile.user_id.not_in(disliked_ids),
                Profile.user_id.not_in(blocked_by_me),
                Profile.user_id.not_in(blocked_me),
            )
        )
        return list((await self.session.scalars(statement)).all())

    async def record_view_once(self, viewer_id: int, candidate_id: int, score: float) -> RecommendationView | None:
        """Atomically claim a candidate for a viewer before rendering its card."""
        event = RecommendationView(viewer_id=viewer_id, candidate_id=candidate_id, score=score)
        try:
            async with self.session.begin_nested():
                self.session.add(event)
                await self.session.flush()
        except IntegrityError:
            return None
        return event
````

## File: repositories/user.py
````python
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, UserStatus
from repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None: super().__init__(session, User)
    async def get_or_create(self, user_id: int, username: str | None) -> User:
        normalized_username = username.casefold() if username else None
        user = await self.get(user_id)
        if user is None:
            user = await self.add(User(id=user_id, username=normalized_username))
        elif user.username != normalized_username:
            user.username = normalized_username
            await self.session.flush()
        return user
    async def by_username(self, username: str) -> User | None:
        normalized = username.lstrip("@").casefold()
        return await self.session.scalar(select(User).where(func.lower(User.username) == normalized))
    async def active(self, user_id: int) -> bool:
        status = await self.session.scalar(select(User.status).where(User.id == user_id))
        return (status == UserStatus.ACTIVE) if status is not None else False

    async def all_ids(self) -> list[int]:
        return list((await self.session.scalars(select(User.id).where(User.status == UserStatus.ACTIVE))).all())
````

## File: scripts/backup_postgres.sh
````bash
#!/usr/bin/env bash
set -euo pipefail

# Creates a PostgreSQL custom-format dump and keeps the latest 14 daily copies.
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="${BACKUP_DIR:-$(dirname "$PROJECT_DIR")/backups}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-14}"
STAMP="$(date +%Y%m%d_%H%M%S)"
DESTINATION="$BACKUP_DIR/project1_${STAMP}.dump"
TEMPORARY_FILE="${DESTINATION}.tmp"

mkdir -p "$BACKUP_DIR"
trap 'rm -f "$TEMPORARY_FILE"' EXIT

cd "$PROJECT_DIR"
docker compose exec -T postgres sh -c 'exec pg_dump --format=custom --no-owner --no-privileges -U "$POSTGRES_USER" "$POSTGRES_DB"' > "$TEMPORARY_FILE"

# Validate the dump inside the database image before it is published as a backup.
docker compose exec -T postgres sh -c 'exec pg_restore --list' < "$TEMPORARY_FILE" > /dev/null
mv "$TEMPORARY_FILE" "$DESTINATION"
find "$BACKUP_DIR" -type f -name 'project1_*.dump' -mtime "+$RETENTION_DAYS" -delete

echo "PostgreSQL backup created: $DESTINATION"
````

## File: scripts/install_backup_cron.sh
````bash
#!/usr/bin/env bash
set -euo pipefail

# Installs one daily backup job at 03:30 local server time. Re-running is safe.
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_SCRIPT="$PROJECT_DIR/scripts/backup_postgres.sh"
LOG_FILE="$(dirname "$PROJECT_DIR")/backups/backup_postgres.log"
CRON_LINE="30 3 * * * $BACKUP_SCRIPT >> $LOG_FILE 2>&1"

mkdir -p "$(dirname "$LOG_FILE")"
(crontab -l 2>/dev/null | grep -F -v "$BACKUP_SCRIPT" || true; echo "$CRON_LINE") | crontab -
echo "Daily PostgreSQL backup scheduled for 03:30."
````

## File: scripts/run_integration.sh
````bash
#!/usr/bin/env bash
set -euo pipefail

# Run integration tests for recommendation engine.
# Usage: INTEGRATION=1 REDIS_URL=redis://localhost:6379 ./scripts/run_integration.sh

WORKDIR=$(dirname "$0")/..
cd "$WORKDIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is not installed or not in PATH; please run integration tests against an existing Redis instance by setting INTEGRATION=1 and REDIS_URL"
  exit 1
fi

echo "Bringing up docker-compose services (Postgres + Redis)"
# Assumes docker-compose.yml exists and defines postgres & redis services
docker compose up -d --remove-orphans

# Wait for redis to be ready
REDIS_URL=${REDIS_URL:-redis://localhost:6379}
export REDIS_URL
export INTEGRATION=1

echo "Waiting for Redis to accept connections..."
for i in {1..30}; do
  if docker compose exec -T redis redis-cli ping >/dev/null 2>&1; then
    echo "Redis is ready"
    break
  fi
  sleep 1
done

# Determine how to run tests: prefer running pytest on host connecting to published ports.
# If Redis on localhost is reachable, run pytest locally. Otherwise, run pytest inside the 'bot' container.
REDIS_PING_OK=0
if command -v redis-cli >/dev/null 2>&1; then
  if redis-cli -h 127.0.0.1 -p 6379 ping >/dev/null 2>&1; then
    REDIS_PING_OK=1
  fi
fi

echo "Running integration pytest suite... (REDIS_PING_OK=${REDIS_PING_OK})"
if [ "$REDIS_PING_OK" -eq 1 ]; then
  INTEGRATION=1 REDIS_URL=${REDIS_URL:-redis://localhost:6379} ./venv/bin/pytest -q tests/integration
  STATUS=$?
else
  # Try running inside the 'bot' service container where Docker Compose network is available
  if docker compose ps --services | grep -q '^bot$'; then
    echo "Running tests inside docker-compose 'bot' service"
  # Prefer using virtualenv if present inside container
  # When running inside the 'bot' container, force the compose network address for Redis (redis) so tests connect to the redis service.
  docker compose exec -T bot /bin/sh -lc "if [ -x .venv/bin/python ]; then export INTEGRATION=1 REDIS_URL=redis://redis:6379 && .venv/bin/python -m pytest -q tests/integration; else export INTEGRATION=1 REDIS_URL=redis://redis:6379 && pytest -q tests/integration; fi"
  STATUS=$?
  else
    echo "'bot' service not found in compose. Attempting to run tests in any running service."
    # pick the first running service and execute tests there
    SERVICE=$(docker compose ps --services | head -n1)
    if [ -n "$SERVICE" ]; then
      echo "Running tests inside container: $SERVICE"
      docker compose exec -T "$SERVICE" /bin/sh -lc "export INTEGRATION=1 REDIS_URL=${REDIS_URL:-redis:6379} && pytest -q tests/integration"
      STATUS=$?
    else
      echo "No running compose services found to run tests inside."
      STATUS=2
    fi
  fi
fi

echo "Tearing down docker-compose services"
docker compose down

exit $STATUS
````

## File: services/__init__.py
````python

````

## File: services/confession_service.py
````python
import hashlib
import re
import uuid
from datetime import UTC, date, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from models import Confession, ConfessionStatus, UserStatus
from repositories.confession import ConfessionRepository
from repositories.user import UserRepository


class ConfessionService:
    def __init__(
        self, session: AsyncSession, salt: str, *, daily_limit: int = 20, pending_ttl_hours: int = 168
    ) -> None:
        self.session, self.salt, self.daily_limit = session, salt, daily_limit
        self.pending_ttl_hours = pending_ttl_hours
    def sender_hash(self, user_id: int) -> str:
        return hashlib.sha256(f"{user_id}:{date.today().isoformat()}:{self.salt}".encode()).hexdigest()
    async def create(
        self, sender_id: int, recipient: str, text: str, *, submission_key: str | None = None
    ) -> Confession:
        """Create a confession record after validating inputs.

        Raises ValueError for invalid input (empty recipient or invalid text length).
        """
        if not (text and 5 <= len(text.strip()) <= 1000):
            raise ValueError("Text length must be between 5 and 1000 characters")
        if not (recipient and recipient.strip()):
            raise ValueError("Recipient must be provided as @username or Telegram ID")

        repo = ConfessionRepository(self.session)
        if submission_key:
            existing = await repo.by_submission_key(submission_key)
            if existing is not None:
                return existing

        normalized = recipient.strip().lstrip("@")
        if normalized.isdigit() and int(normalized) == sender_id:
            raise ValueError("Нельзя отправить признание самому себе.")
        if not normalized.isdigit() and not re.fullmatch(r"[A-Za-z0-9_]{3,32}", normalized):
            raise ValueError("Укажите корректный Telegram username.")
        user = None
        if normalized.isdigit():
            try:
                user = await UserRepository(self.session).get(int(normalized))
            except Exception:
                user = None
        else:
            user = await UserRepository(self.session).by_username(normalized)

        if user is not None and (
            getattr(user, "status", UserStatus.ACTIVE) != UserStatus.ACTIVE
            or not getattr(user, "accepts_confessions", True)
        ):
            # Do not disclose whether a recipient paused messages or was restricted.
            raise ValueError("Сейчас этому пользователю нельзя отправить признание.")

        sender_hash = self.sender_hash(sender_id)
        if not await repo.reserve_daily_send(sender_hash, limit=self.daily_limit):
            raise ValueError("На сегодня лимит анонимных признаний исчерпан. Попробуйте завтра.")

        confession = Confession(
            sender_hash=sender_hash,
            submission_key=submission_key,
            recipient_id=user.id if user else None,
            target_username=None if user else recipient.lstrip("@"),
            text=text.strip(),
            status=ConfessionStatus.DELIVERED if user else ConfessionStatus.PENDING,
            expires_at=None if user else datetime.now(UTC) + timedelta(hours=self.pending_ttl_hours),
        )
        return await repo.add(confession)
    async def claim(self, confession_id: uuid.UUID, recipient_id: int) -> Confession | None:
        confession = await ConfessionRepository(self.session).get_pending(confession_id)
        if confession is None:
            return None

        # A pending confession is delivered through a shareable deep link.
        # It can be claimed either by a matching username or by a matching Telegram ID
        # if the sender used an ID instead of a username.
        recipient = await UserRepository(self.session).get(recipient_id)
        if not recipient:
            return None

        expected_target = (confession.target_username or "").lstrip("@").casefold()
        if not expected_target:
            return None

        # Check if target matches either ID or username
        is_match = False
        if expected_target.isdigit():
            is_match = int(expected_target) == recipient_id
        else:
            actual_username = (recipient.username or "").casefold()
            is_match = actual_username == expected_target

        if not is_match:
            return None

        if (
            getattr(recipient, "status", UserStatus.ACTIVE) != UserStatus.ACTIVE
            or not getattr(recipient, "accepts_confessions", True)
        ):
            return None

        return await ConfessionRepository(self.session).claim_pending(confession_id, recipient_id)
````

## File: services/eligibility.py
````python
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Block, ModerationStatus, Profile, User, UserStatus


class EligibilityError(ValueError):
    pass


class EligibilityService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def ensure_source_allowed(self, source_id: int, *, action: str) -> Profile:
        """Check if the source user is allowed to perform an action (e.g., send confessions)."""
        source_profile = await self.session.scalar(select(Profile).where(Profile.user_id == source_id))
        source_user = await self.session.get(User, source_id)
        if source_profile is None or source_user is None:
            raise EligibilityError("Анкета недоступна.")

        if not source_profile.is_visible:
            raise EligibilityError(f"Нельзя {action}: анкета недоступна.")
        if source_profile.moderation_locked:
            raise EligibilityError(f"Нельзя {action}: анкета на проверке модератором.")
        if source_profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            raise EligibilityError(f"Нельзя {action}: анкета на проверке модератором.")
        if source_user.status != UserStatus.ACTIVE:
            raise EligibilityError(f"Нельзя {action}: ваша анкета ограничена или заблокирована.")

        return source_profile

    async def ensure_action_allowed(self, source_id: int, target_id: int, *, action: str) -> tuple[Profile, User]:
        if source_id == target_id:
            raise EligibilityError(f"Нельзя {action} самому себе.")

        target_profile = await self.session.scalar(select(Profile).where(Profile.user_id == target_id))
        target_user = await self.session.get(User, target_id)
        if target_profile is None or target_user is None:
            raise EligibilityError("Анкета недоступна.")

        if not target_profile.is_visible:
            raise EligibilityError("Анкета недоступна.")
        if target_profile.moderation_locked:
            raise EligibilityError("Анкета недоступна.")
        if target_profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            raise EligibilityError("Анкета недоступна.")
        if target_user.status != UserStatus.ACTIVE:
            raise EligibilityError("Анкета недоступна.")

        blocked = await self.session.scalar(
            select(Block.id).where(
                ((Block.blocker_id == source_id) & (Block.blocked_id == target_id))
                | ((Block.blocker_id == target_id) & (Block.blocked_id == source_id))
            )
        )
        if blocked is not None:
            raise EligibilityError("Анкета недоступна.")

        return target_profile, target_user
````

## File: services/interest_normalizer.py
````python
import json
import re
import unicodedata
from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path


def _normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.strip().casefold())
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return re.sub(r"[^\w]+", " ", normalized, flags=re.UNICODE).strip()


@lru_cache(maxsize=1)
def _load_categories() -> dict[str, dict[str, object]]:
    data_path = Path(__file__).resolve().parent.parent / "data" / "interest_categories.json"
    with data_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    categories: dict[str, dict[str, object]] = {}
    for item in payload.get("categories", []):
        key = str(item["key"])
        aliases = {_normalize_text(str(alias)) for alias in item.get("aliases", [])}
        aliases.add(_normalize_text(key))
        label = str(item.get("label", key))
        categories[key] = {"label": label, "aliases": aliases}
    return categories


def normalize_interests(raw_text: str | Iterable[str] | None) -> list[str]:
    if raw_text is None:
        return []

    items: list[str] = []
    if isinstance(raw_text, str):
        items.extend(re.split(r"[,;|/]+", raw_text))
    else:
        for item in raw_text:
            if isinstance(item, str):
                items.extend(re.split(r"[,;|/]+", item))
            else:
                items.append(str(item))

    normalized: list[str] = []
    seen: set[str] = set()

    for item in items:
        candidate = str(item).strip()
        if not candidate:
            continue

        cleaned = _normalize_text(candidate)
        if not cleaned:
            continue

        matched = False
        for key, category in _load_categories().items():
            aliases = category.get("aliases", set())
            if cleaned in aliases or any(token in aliases for token in cleaned.split()):
                if key not in seen:
                    normalized.append(key)
                    seen.add(key)
                matched = True
                break

        if not matched:
            if candidate not in seen:
                normalized.append(candidate)
                seen.add(candidate)

    return normalized


def format_interests(interests: list[str] | str | None) -> str:
    if interests is None:
        return "—"
    if isinstance(interests, str):
        interests = normalize_interests(interests)
    formatted = [f"#{interest.title().replace('_', '')}" for interest in interests if str(interest).strip()]
    return " ".join(formatted) if formatted else "—"
````

## File: services/like_service.py
````python
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from models import Like
from repositories.like import LikeRepository
from services.eligibility import EligibilityError, EligibilityService


@dataclass(frozen=True, slots=True)
class LikeResult:
    like: Like
    created: bool


class LikeService:
    """Owns one-way Like creation and duplicate/self-like protection."""

    def __init__(self, session: AsyncSession) -> None:
        self.repo = LikeRepository(session)

    async def create(self, source_id: int, target_id: int, comment: str | None = None) -> LikeResult:
        normalized_comment = comment.strip() if comment else None
        if normalized_comment is not None and not 1 <= len(normalized_comment) <= 200:
            raise ValueError("Комментарий к лайку должен содержать от 1 до 200 символов.")
        try:
            await EligibilityService(self.repo.session).ensure_action_allowed(
                source_id,
                target_id,
                action="поставить лайк",
            )
        except EligibilityError as error:
            raise ValueError(str(error)) from error
        like, created = await self.repo.add(source_id, target_id, normalized_comment)
        return LikeResult(like=like, created=created)
````

## File: services/match_service.py
````python
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from models import Like, Match
from repositories.like import LikeRepository
from repositories.match import MatchRepository
from services.eligibility import EligibilityError, EligibilityService


@dataclass(frozen=True, slots=True)
class MatchResult:
    match: Match | None
    created: bool


class MatchService:
    """Owns mutual-like detection and idempotent Match persistence."""

    def __init__(self, session: AsyncSession) -> None:
        self.likes = LikeRepository(session)
        self.matches = MatchRepository(session)

    async def create_if_mutual(self, source_id: int, target_id: int, like: Like) -> MatchResult:
        try:
            await EligibilityService(self.likes.session).ensure_action_allowed(
                source_id,
                target_id,
                action="создать мэтч",
            )
            await EligibilityService(self.likes.session).ensure_action_allowed(
                target_id,
                source_id,
                action="создать мэтч",
            )
        except EligibilityError:
            return MatchResult(match=None, created=False)

        reciprocal = await self.likes.reciprocal(source_id, target_id)
        if reciprocal is None:
            return MatchResult(match=None, created=False)
        like.is_mutual = True
        reciprocal.is_mutual = True
        match, created = await self.matches.create_once(source_id, target_id)
        return MatchResult(match=match, created=created)

    async def matches_for(self, user_id: int, limit: int = 50) -> list[Match]:
        return await self.matches.by_user_id(user_id, limit)
````

## File: services/matching_debug.py
````python
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from services.matching_stats import MatchingStats, MatchingStatsService
from services.recommendation import CandidateDiagnostic, RecommendationService
from services.recommendation_strategy import WeightedRecommendationStrategy


@dataclass(frozen=True, slots=True)
class MatchingDebugReport:
    stats: MatchingStats
    candidates: tuple[CandidateDiagnostic, ...]
    gender_compatible: int
    age_relevant: int
    same_district: int
    shared_interests: int


class MatchingDebugService:
    def __init__(self, session: AsyncSession, *, weights: dict[str, float]) -> None:
        self.recommendations = RecommendationService(session, weights=weights)
        self.stats = MatchingStatsService(session)

    async def report_for(self, user_id: int) -> MatchingDebugReport:
        candidates = tuple(await self.recommendations.diagnostics(user_id))
        included = [candidate for candidate in candidates if candidate.included]
        mine = await self.recommendations.repo.profile(user_id)
        profiles = {profile.user_id: profile for profile in await self.recommendations.repo.active_profiles(user_id)}
        components = [
            WeightedRecommendationStrategy.components(mine, profiles[item.candidate_id])
            for item in included
            if mine is not None and item.candidate_id in profiles
        ]
        return MatchingDebugReport(
            stats=await self.stats.snapshot(),
            candidates=candidates,
            gender_compatible=sum(
                "gender" not in item.reasons and "target_gender" not in item.reasons for item in candidates
            ),
            age_relevant=sum(item["age"] > 0 for item in components),
            same_district=sum(item["district"] > 0 for item in components),
            shared_interests=sum(item["interests"] > 0 for item in components),
        )
````

## File: services/matching_stats.py
````python
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from repositories.matching_stats import MatchingStatsRepository


@dataclass(frozen=True, slots=True)
class MatchingStats:
    users: int
    active_users: int
    views: int
    likes: int
    matches: int
    reports: int
    ctr: float
    average_compatibility: float


class MatchingStatsService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = MatchingStatsRepository(session)

    async def snapshot(self) -> MatchingStats:
        return MatchingStats(**await self.repo.snapshot())
````

## File: services/nsfw_service.py
````python
class NSFWService:
    """Safety extension point. Override `score` with an ONNX/service-backed classifier."""
    def __init__(self, threshold: float = 0.85) -> None: self.threshold = threshold
    async def score(self, photo_file_id: str) -> float: return 0.0
    async def is_allowed(self, photo_file_id: str) -> bool: return await self.score(photo_file_id) < self.threshold
````

## File: services/photo_analysis_progress.py
````python
from __future__ import annotations

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

PHOTO_ANALYSIS_TEXT = "⏳ Анализируем фото нейросетью. Это займёт несколько секунд…"


async def show_photo_analysis_progress(message: Message) -> Message | None:
    """Show a disposable status without allowing Telegram errors to stop moderation."""
    try:
        return await message.answer(PHOTO_ANALYSIS_TEXT)
    except TelegramBadRequest:
        return None


async def dismiss_photo_analysis_progress(progress: Message | None) -> None:
    if progress is None:
        return
    try:
        await progress.delete()
    except TelegramBadRequest:
        pass
````

## File: services/recommendation_queue.py
````python
from __future__ import annotations

import logging
import math
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any, Protocol

import redis.asyncio as aioredis


@dataclass(frozen=True, slots=True)
class QueueEntry:
    candidate_id: int
    score: float


class RecommendationQueue(Protocol):
    async def replace(self, user_id: int, entries: list[QueueEntry]) -> None: ...
    async def pop(self, user_id: int) -> QueueEntry | None: ...
    async def move_to_end(self, user_id: int, candidate_id: int, score: float) -> None: ...
    async def remove(self, user_id: int, candidate_id: int) -> None: ...
    async def clear(self, user_id: int) -> None: ...


class MemoryRecommendationQueue:
    """Process-local queue implementation; retained for tests and local fallback."""

    def __init__(self) -> None:
        self._queues: dict[int, deque[QueueEntry]] = defaultdict(deque)

    async def replace(self, user_id: int, entries: list[QueueEntry]) -> None:
        self._queues[user_id] = deque(entries)

    async def pop(self, user_id: int) -> QueueEntry | None:
        queue = self._queues[user_id]
        return queue.popleft() if queue else None

    async def move_to_end(self, user_id: int, candidate_id: int, score: float) -> None:
        await self.remove(user_id, candidate_id)
        self._queues[user_id].append(QueueEntry(candidate_id, score))

    async def remove(self, user_id: int, candidate_id: int) -> None:
        self._queues[user_id] = deque(entry for entry in self._queues[user_id] if entry.candidate_id != candidate_id)

    async def clear(self, user_id: int) -> None:
        self._queues.pop(user_id, None)


logger = logging.getLogger(__name__)


class RedisRecommendationQueue:
    def __init__(self, redis_client: aioredis.Redis | Any) -> None:
        self._redis = redis_client

    def _key(self, user_id: int) -> str:
        return f"recommendation_queue:{user_id}"

    @staticmethod
    def _encode(entry: QueueEntry) -> str:
        if not math.isfinite(entry.score):
            raise ValueError("Recommendation score must be finite")
        return f"{entry.candidate_id}:{entry.score}"

    @staticmethod
    def _decode(raw: bytes | str | None) -> QueueEntry | None:
        if raw is None:
            return None
        text = raw.decode("utf-8") if isinstance(raw, bytes | bytearray) else str(raw)
        candidate_id_str, score_str = text.split(":", 1)
        entry = QueueEntry(candidate_id=int(candidate_id_str), score=float(score_str))
        if not math.isfinite(entry.score):
            raise ValueError("Recommendation score must be finite")
        return entry

    async def replace(self, user_id: int, entries: list[QueueEntry]) -> None:
        key = self._key(user_id)
        encoded: list[str] = []
        candidate_ids: set[int] = set()
        for entry in entries:
            if entry.candidate_id in candidate_ids:
                continue
            encoded.append(self._encode(entry))
            candidate_ids.add(entry.candidate_id)
        # DEL and RPUSH must be atomic so a concurrent pop cannot observe an
        # artificial empty queue and start an unnecessary rebuild.
        await self._redis.eval(
            """
            local key = KEYS[1]
            redis.call('DEL', key)
            for i = 1, #ARGV do
                redis.call('RPUSH', key, ARGV[i])
            end
            return #ARGV
            """,
            1,
            key,
            *encoded,
        )

    async def pop(self, user_id: int) -> QueueEntry | None:
        key = self._key(user_id)
        while True:
            raw = await self._redis.lpop(key)
            if raw is None:
                return None
            try:
                return self._decode(raw)
            except (ValueError, UnicodeDecodeError) as error:
                logger.warning("Corrupted recommendation queue entry for user %s: %s", user_id, error)
                continue

    async def move_to_end(self, user_id: int, candidate_id: int, score: float) -> None:
        key = self._key(user_id)
        entry = self._encode(QueueEntry(candidate_id, score))
        await self._redis.eval(
            """
            local key = KEYS[1]
            local candidate_id = tonumber(ARGV[1])
            local entry = ARGV[2]
            local values = redis.call('LRANGE', key, 0, -1)
            local filtered = {}
            for i = 1, #values do
                local value = values[i]
                local id = tonumber(string.match(value, '^(.-):'))
                if id ~= candidate_id then
                    table.insert(filtered, value)
                end
            end
            redis.call('DEL', key)
            for i = 1, #filtered do
                redis.call('RPUSH', key, filtered[i])
            end
            redis.call('RPUSH', key, entry)
            return 1
            """,
            1,
            key,
            str(candidate_id),
            entry,
        )

    async def remove(self, user_id: int, candidate_id: int) -> None:
        key = self._key(user_id)
        await self._redis.eval(
            """
            local key = KEYS[1]
            local candidate_id = tonumber(ARGV[1])
            local values = redis.call('LRANGE', key, 0, -1)
            local filtered = {}
            for i = 1, #values do
                local value = values[i]
                local id = tonumber(string.match(value, '^(.-):'))
                if id ~= candidate_id then
                    table.insert(filtered, value)
                end
            end
            redis.call('DEL', key)
            for i = 1, #filtered do
                redis.call('RPUSH', key, filtered[i])
            end
            return 1
            """,
            1,
            key,
            str(candidate_id),
        )

    async def clear(self, user_id: int) -> None:
        await self._redis.delete(self._key(user_id))


_DEFAULT_QUEUE: RecommendationQueue | None = None


def get_default_queue() -> RecommendationQueue:
    global _DEFAULT_QUEUE
    if _DEFAULT_QUEUE is None:
        from config import get_settings

        _DEFAULT_QUEUE = RedisRecommendationQueue(aioredis.Redis.from_url(get_settings().redis_url))
    return _DEFAULT_QUEUE
````

## File: services/recommendation_strategy.py
````python
from __future__ import annotations

import json
import math
import re
import unicodedata
from collections.abc import Iterable, Mapping
from functools import lru_cache
from pathlib import Path
from typing import Protocol

from models import Gender, Profile

DEFAULT_MATCHING_WEIGHTS: dict[str, float] = {
    "gender": 35.0,
    "target_gender": 25.0,
    "age": 10.0,
    "district": 10.0,
    "institution": 10.0,
    "interests": 7.0,
    "bio": 3.0,
}


def _normalize_text(value: str | None) -> str:
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKD", value.strip().casefold())
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return re.sub(r"[^\w]+", " ", normalized, flags=re.UNICODE).strip()


@lru_cache(maxsize=1)
def _load_aliases() -> dict[str, str]:
    aliases_path = Path(__file__).resolve().parent.parent / "data" / "normalization_aliases.json"
    if not aliases_path.exists():
        return {}
    with aliases_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    mapping: dict[str, str] = {}
    for canonical, variants in payload.get("districts", {}).items():
        canonical_normalized = _normalize_text(canonical)
        mapping[canonical_normalized] = canonical_normalized
        for variant in variants:
            mapping[_normalize_text(str(variant))] = canonical_normalized
    for canonical, variants in payload.get("institutions", {}).items():
        canonical_normalized = _normalize_text(canonical)
        mapping[canonical_normalized] = canonical_normalized
        for variant in variants:
            mapping[_normalize_text(str(variant))] = canonical_normalized
    return mapping


def _normalize_match_text(value: str) -> str:
    normalized = _normalize_text(value)
    return _load_aliases().get(normalized, normalized)


class RecommendationStrategy(Protocol):
    """Asynchronous ranking contract for a compatible recommendation candidate."""

    async def score(self, viewer: Profile, candidate: Profile) -> float: ...


class WeightedRecommendationStrategy:
    """Deterministic strategy based on configurable compatibility weights."""

    def __init__(self, weights: Mapping[str, float] | None = None) -> None:
        self.weights = {**DEFAULT_MATCHING_WEIGHTS, **dict(weights or {})}
        unknown = self.weights.keys() - DEFAULT_MATCHING_WEIGHTS.keys()
        if unknown:
            raise ValueError(f"Неизвестные веса рекомендаций: {', '.join(sorted(unknown))}.")
        if any(
            isinstance(value, bool) or not isinstance(value, int | float) or not math.isfinite(value) or value < 0
            for value in self.weights.values()
        ):
            raise ValueError("Веса рекомендаций должны быть неотрицательными числами.")
        if sum(self.weights.values()) <= 0:
            raise ValueError("Сумма весов рекомендаций должна быть больше нуля.")

    async def score(self, viewer: Profile, candidate: Profile) -> float:
        return self.score_sync(viewer, candidate)

    def score_sync(self, viewer: Profile, candidate: Profile) -> float:
        components = self.components(viewer, candidate)
        total_weight = sum(self.weights.values())
        return round(100 * sum(self.weights[name] * components[name] for name in self.weights) / total_weight, 1)

    @classmethod
    def components(cls, viewer: Profile, candidate: Profile) -> dict[str, float]:
        return {
            "gender": 1.0 if viewer.target_gender == Gender.ALL or candidate.gender == viewer.target_gender else 0.0,
            "target_gender": (
                1.0 if candidate.target_gender == Gender.ALL or candidate.target_gender == viewer.gender else 0.0
            ),
            "age": max(0.0, 1.0 - abs(viewer.age - candidate.age) / 20),
            "district": cls._text_match(viewer.district, candidate.district),
            "institution": cls._text_match(viewer.institution, candidate.institution),
            "interests": cls._jaccard(viewer.interests or [], candidate.interests or []),
            "bio": cls._jaccard(cls._tokens(viewer.bio), cls._tokens(candidate.bio)),
        }

    @staticmethod
    def _text_match(first: str, second: str) -> float:
        return 1.0 if _normalize_match_text(first) == _normalize_match_text(second) else 0.0

    @staticmethod
    def _tokens(value: str) -> list[str]:
        return re.findall(r"[\w-]+", value.casefold())

    @staticmethod
    def _jaccard(first: Iterable[str], second: Iterable[str]) -> float:
        first_values = {str(item).casefold() for item in first if str(item).strip()}
        second_values = {str(item).casefold() for item in second if str(item).strip()}
        union = first_values | second_values
        return len(first_values & second_values) / len(union) if union else 0.0
````

## File: services/recommendation.py
````python
from __future__ import annotations

import logging
import math
from dataclasses import dataclass

from redis.exceptions import RedisError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Gender, Profile
from repositories.recommendation import RecommendationRepository
from services.recommendation_queue import QueueEntry, RecommendationQueue, get_default_queue
from services.recommendation_strategy import (
    DEFAULT_MATCHING_WEIGHTS,
    RecommendationStrategy,
    WeightedRecommendationStrategy,
)


@dataclass(frozen=True, slots=True)
class Recommendation:
    profile: Profile
    score: float


@dataclass(frozen=True, slots=True)
class CandidateDiagnostic:
    candidate_id: int
    included: bool
    reasons: tuple[str, ...]
    score: float | None


class RecommendationService:
    def __init__(
        self,
        session: AsyncSession,
        *,
        weights: dict[str, float] | None = None,
        queue: RecommendationQueue | None = None,
        strategy: RecommendationStrategy | None = None,
    ) -> None:
        self.repo = RecommendationRepository(session)
        self.strategy = strategy or WeightedRecommendationStrategy(weights)
        self.queue = queue or get_default_queue()

    async def next_recommendation(self, user_id: int) -> Recommendation | None:
        mine = await self.repo.profile(user_id)
        if mine is None:
            return None
        try:
            return await self._next_from_queue(user_id, mine)
        except RedisError as error:
            logging.getLogger(__name__).warning(
                "Recommendation queue unavailable for user %s; using database fallback: %s", user_id, error
            )
            return await self._next_from_database(user_id, mine)

    async def _next_from_queue(self, user_id: int, mine: Profile) -> Recommendation | None:
        entry = await self.queue.pop(user_id)
        if entry is None:
            await self.rebuild_queue(user_id, mine)
            entry = await self.queue.pop(user_id)
        while entry is not None:
            profile = await self.repo.eligible_profile(user_id, entry.candidate_id)
            if profile is None or not self.is_compatible(mine, profile):
                entry = await self.queue.pop(user_id)
                continue
            if await self.repo.record_view_once(user_id, profile.user_id, entry.score) is not None:
                return Recommendation(profile=profile, score=entry.score)
            entry = await self.queue.pop(user_id)
        return None

    async def _next_from_database(self, user_id: int, mine: Profile) -> Recommendation | None:
        """Serve one card when disposable Redis state is temporarily unavailable."""
        candidates = await self.repo.eligible_profiles(user_id)
        ranked: list[QueueEntry] = []
        for candidate in candidates:
            if not self.is_compatible(mine, candidate):
                continue
            try:
                score = float(await self.strategy.score(mine, candidate))
            except Exception as error:
                logging.getLogger(__name__).warning(
                    "Error scoring database-fallback candidate %s for user %s: %s", candidate.user_id, user_id, error
                )
                continue
            if math.isfinite(score):
                ranked.append(QueueEntry(candidate.user_id, score))
        for entry in sorted(ranked, key=lambda item: (-item.score, item.candidate_id)):
            profile = await self.repo.eligible_profile(user_id, entry.candidate_id)
            if profile is None:
                continue
            if await self.repo.record_view_once(user_id, profile.user_id, entry.score) is not None:
                return Recommendation(profile=profile, score=entry.score)
        return None

    async def next_profile(self, user_id: int) -> Profile | None:
        recommendation = await self.next_recommendation(user_id)
        return recommendation.profile if recommendation else None

    async def rebuild_queue(self, user_id: int, mine: Profile | None = None) -> int:
        import asyncio
        import logging

        logger = logging.getLogger(__name__)

        mine = mine or await self.repo.profile(user_id)
        if mine is None:
            await self.queue.clear(user_id)
            return 0
        candidates = await self.repo.eligible_profiles(user_id)
        # Filter compatible candidates first to avoid unnecessary scoring
        candidates_to_score = [candidate for candidate in candidates if self.is_compatible(mine, candidate)]
        entries: list[QueueEntry] = []
        if candidates_to_score:
            # Compute scores concurrently to improve rebuild latency for large pools.
            coros = [self.strategy.score(mine, candidate) for candidate in candidates_to_score]
            results = await asyncio.gather(*coros, return_exceptions=True)
            for candidate, result in zip(candidates_to_score, results):
                if isinstance(result, Exception):
                    logger.exception("Error scoring candidate %s for user %s: %s", candidate.user_id, user_id, result)
                    # Skip candidates that failed scoring
                    continue
                try:
                    score = float(result)
                except (TypeError, ValueError):
                    logger.warning("Invalid score returned for candidate %s: %r", candidate.user_id, result)
                    continue
                if not math.isfinite(score):
                    logger.warning("Non-finite score returned for candidate %s: %r", candidate.user_id, result)
                    continue
                entries.append(QueueEntry(candidate.user_id, score))
        entries.sort(key=lambda entry: (-entry.score, entry.candidate_id))
        await self.queue.replace(user_id, entries)
        return len(entries)

    async def skip(self, user_id: int, candidate_id: int) -> None:
        mine = await self.repo.profile(user_id)
        candidate = await self.repo.profile(candidate_id)
        if mine is not None and candidate is not None and self.is_compatible(mine, candidate):
            try:
                await self.queue.move_to_end(user_id, candidate_id, await self.strategy.score(mine, candidate))
            except RedisError as error:
                logging.getLogger(__name__).warning(
                    "Could not update recommendation queue for skipped candidate %s: %s", candidate_id, error
                )

    async def remove_candidate(self, user_id: int, candidate_id: int) -> None:
        try:
            await self.queue.remove(user_id, candidate_id)
        except RedisError as error:
            logging.getLogger(__name__).warning(
                "Could not remove candidate %s from recommendation queue: %s", candidate_id, error
            )

    @staticmethod
    def is_compatible(mine: Profile, candidate: Profile) -> bool:
        gender_ok = mine.target_gender == Gender.ALL or candidate.gender == mine.target_gender
        target_ok = candidate.target_gender == Gender.ALL or candidate.target_gender == mine.gender
        return gender_ok and target_ok

    @staticmethod
    def compute_score(mine: Profile, candidate: Profile) -> float:
        """Compatibility score using the default weights; retained as a stable public helper."""
        return WeightedRecommendationStrategy(DEFAULT_MATCHING_WEIGHTS).score_sync(mine, candidate)

    async def diagnostics(self, user_id: int) -> list[CandidateDiagnostic]:
        mine = await self.repo.profile(user_id)
        if mine is None:
            return []
        active = await self.repo.active_profiles(user_id)
        eligible_ids = {profile.user_id for profile in await self.repo.eligible_profiles(user_id)}
        diagnostics: list[CandidateDiagnostic] = []
        for candidate in active:
            reasons: list[str] = []
            if candidate.user_id not in eligible_ids:
                reasons.append("already_viewed_or_excluded")
            if mine.target_gender != Gender.ALL and candidate.gender != mine.target_gender:
                reasons.append("gender")
            if candidate.target_gender != Gender.ALL and candidate.target_gender != mine.gender:
                reasons.append("target_gender")
            included = not reasons
            diagnostics.append(
                CandidateDiagnostic(
                    candidate.user_id,
                    included,
                    tuple(reasons),
                    await self.strategy.score(mine, candidate) if included else None,
                )
            )
        return diagnostics
````

## File: services/trust_score_service.py
````python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import TrustScoreEvent, User
from repositories.trust import TrustRepository


class TrustScoreService:
    """Internal reputation ledger. Every applied change is recorded for future fraud models."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = TrustRepository(session)

    async def change(
        self,
        user_id: int,
        delta: int,
        reason: str,
        *,
        reference_type: str | None = None,
        reference_id: str | None = None,
    ) -> bool:
        user = await self.session.get(User, user_id)
        if user is None:
            return False
        # A reference makes moderation retries idempotent.
        if reference_id:
            duplicate = await self.session.scalar(
                select(TrustScoreEvent).where(
                    TrustScoreEvent.user_id == user_id,
                    TrustScoreEvent.reason == reason,
                    TrustScoreEvent.reference_type == reference_type,
                    TrustScoreEvent.reference_id == reference_id,
                )
            )
            if duplicate:
                return False
        user.trust_score = max(0, min(100, user.trust_score + delta))
        await self.repo.add_score_event(user_id, delta, reason, reference_type, reference_id)
        return True
````

## File: services/trust_stats_service.py
````python
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.trust import TrustRepository


class TrustStatsService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = TrustRepository(session)

    async def snapshot(self) -> dict[str, float | int]:
        return await self.repo.stats()
````

## File: states/__init__.py
````python

````

## File: states/admin.py
````python
from aiogram.fsm.state import State, StatesGroup


class AdminState(StatesGroup):
    moderation_queue = State()
    broadcast_message = State()
    appeal_reply = State()
````

## File: states/appeal.py
````python
from aiogram.fsm.state import State, StatesGroup


class AppealState(StatesGroup):
    enter_text = State()
````

## File: states/bug_report.py
````python
from aiogram.fsm.state import State, StatesGroup


class BugReportState(StatesGroup):
    waiting_description = State()
````

## File: states/confession.py
````python
from aiogram.fsm.state import State, StatesGroup


class ConfessionState(StatesGroup):
    recipient = State()
    text = State()
    confirm = State()
````

## File: states/dating.py
````python
from aiogram.fsm.state import State, StatesGroup


class DatingState(StatesGroup):
    browsing = State()
    like_comment = State()
    report_reason = State()
````

## File: states/registration.py
````python
from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):
    gender = State()
    target_gender = State()
    name = State()
    age = State()
    district = State()
    institution = State()
    interests = State()
    bio = State()
    photo = State()
    preview = State()
    confirmation = State()
````

## File: states/verification.py
````python
from aiogram.fsm.state import State, StatesGroup


class VerificationState(StatesGroup):
    waiting_video = State()
````

## File: tests/integration/test_moderation_resolution_concurrency.py
````python
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
````

## File: tests/integration/test_redis_multiprocess_pop.py
````python
import asyncio
import json
import os
import tempfile
from multiprocessing import Process
from pathlib import Path

import pytest
import redis.asyncio as aioredis

from services.recommendation_queue import QueueEntry, RedisRecommendationQueue

REDIS_URL = os.environ.get("REDIS_URL")
INTEGRATION = os.environ.get("INTEGRATION")


def _pop_once_process(redis_url: str, user_id: int, out_path: str):
    # Runs in a separate process: create an event loop and pop one entry
    import asyncio

    import redis.asyncio as aioredis

    from services.recommendation_queue import RedisRecommendationQueue

    async def _run():
        r = aioredis.Redis.from_url(redis_url)
        queue = RedisRecommendationQueue(r)
        try:
            entry = await queue.pop(user_id)
            result = (entry.candidate_id if entry else None)
        finally:
            await r.aclose()
        Path(out_path).write_text(json.dumps(result))

    asyncio.run(_run())


@pytest.mark.skipif(not INTEGRATION or not REDIS_URL, reason="Integration tests require INTEGRATION=1 and REDIS_URL")
def test_redis_pop_is_atomic_across_processes():
    redis_url = REDIS_URL
    user_id = 99999
    count = 10

    async def setup_list():
        r = aioredis.Redis.from_url(redis_url)
        key = f"recommendation_queue:{user_id}"
        await r.delete(key)
        # push 5 entries only
        entries = [f"{i}:{float(i)}" for i in range(2, 2 + (count // 2))]
        if entries:
            await r.rpush(key, *entries)
        await r.aclose()

    asyncio.run(setup_list())

    tmpdir = tempfile.TemporaryDirectory()
    procs = []
    out_files = []
    # spawn more processes than entries to ensure some get None
    for idx in range(count):
        out_path = Path(tmpdir.name) / f"result_{idx}.json"
        p = Process(target=_pop_once_process, args=(redis_url, user_id, str(out_path)))
        p.start()
        procs.append(p)
        out_files.append(out_path)

    for p in procs:
        p.join(timeout=30)
        if p.exitcode is None:
            p.terminate()

    # Collect results

    values = []
    for f in out_files:
        if f.exists():
            try:
                values.append(json.loads(f.read_text()))
            except Exception:
                values.append(None)
        else:
            values.append(None)

    # Unique non-None values should be equal to number of entries pushed
    non_none = [v for v in values if v is not None]
    assert len(set(non_none)) == (count // 2)
    tmpdir.cleanup()


@pytest.mark.skipif(not INTEGRATION or not REDIS_URL, reason="Integration tests require INTEGRATION=1 and REDIS_URL")
def test_redis_queue_skips_corrupted_entry(real_redis=True):
    # Push corrupted entry and a good one, ensure pop skips corrupted and returns valid
    redis_url = REDIS_URL
    user_id = 99998

    async def setup_list():
        r = aioredis.Redis.from_url(redis_url)
        key = f"recommendation_queue:{user_id}"
        await r.delete(key)
        await r.rpush(key, "bad-entry", "3:30")
        await r.aclose()

    asyncio.run(setup_list())

    async def run_pop():
        r = aioredis.Redis.from_url(redis_url)
        queue = RedisRecommendationQueue(r)
        first = await queue.pop(user_id)
        second = await queue.pop(user_id)
        await r.aclose()
        return first, second

    first, second = asyncio.run(run_pop())
    assert first == QueueEntry(3, 30.0)
    assert second is None
````

## File: tests/__init__.py
````python

````

## File: tests/test_appeal_model.py
````python
from models import Appeal, AppealStatus


def test_appeal_model_exports_and_statuses():
    assert AppealStatus.PENDING.value == "PENDING"
    assert Appeal.__tablename__ == "appeals"
````

## File: tests/test_confession_service.py
````python
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
````

## File: tests/test_i18n.py
````python
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

from keyboards.menu import main_menu
from keyboards.profile import profile_keyboard
from middlewares.i18n import normalize_locale
from services.localization import LocalizationService
from services.notification_service import NotificationService
from services.promo_service import get_empty_discovery_promo


def test_normalize_locale_supports_telegram_variants_and_falls_back_to_russian():
    assert normalize_locale("ro-RO") == "ro"
    assert normalize_locale("en") == "ru"
    assert normalize_locale(None) == "ru"


def test_ru_and_ro_have_the_same_localization_keys():
    locale_dir = Path(__file__).parents[1] / "data" / "locales"
    with (locale_dir / "ru.json").open(encoding="utf-8") as handle:
        russian = json.load(handle)
    with (locale_dir / "ro.json").open(encoding="utf-8") as handle:
        romanian = json.load(handle)
    assert russian.keys() == romanian.keys()


def test_romanian_ui_uses_translated_labels():
    localizer = LocalizationService()
    assert localizer.get("menu_profile", "ro") == "👤 Profilul meu"
    assert main_menu("ro").keyboard[1][0].text == "👤 Profilul meu"
    assert profile_keyboard(locale="ro").inline_keyboard[-1][0].text == "🌐 Язык / Limba"


def test_romanian_dating_and_empty_state_are_translated():
    from keyboards.dating import dating_keyboard

    assert dating_keyboard(7, "ro").inline_keyboard[0][0].text == "❤️ Îmi place"
    promo = get_empty_discovery_promo(7, locale="ro")
    assert promo["title"] == "Totul este în regulă"
    assert promo["button_text"] == "🔄 Reîmprospătează lista"


def test_help_verification_and_profile_status_keys_are_translated():
    localizer = LocalizationService()
    assert "Ajutor" in localizer.get("help_text", "ro")
    assert "verificat" in localizer.get("verification_verified", "ro").lower()
    assert localizer.get("profile_verified", "ro") == "🟢 Verificat"
    assert "Profilul este ascuns" in localizer.get("profile_moderation_hidden", "ro")


def test_format_returns_unformatted_template_when_placeholder_is_missing():
    localizer = LocalizationService()
    assert localizer.format("notification_like_comment", "ru") == "💌 Кому-то понравилась ваша анкета.\n\n{comment}"
    assert localizer.format("notification_like_comment", "ru", wrong_name="x").endswith("{comment}")


async def test_notification_uses_recipient_profile_locale():
    bot = SimpleNamespace(send_message=AsyncMock())
    session = SimpleNamespace(
        scalar=AsyncMock(return_value=SimpleNamespace(locale="ro")),
    )
    await NotificationService(bot).safe_send_localized(7, session, "notification_like")
    bot.send_message.assert_awaited_once_with(7, "💌 Cineva a apreciat profilul tău.", reply_markup=None)
````

## File: tests/test_likes_and_matches.py
````python
from types import SimpleNamespace

import pytest

from models import ModerationStatus, UserStatus
from services.like_service import LikeService
from services.match_service import MatchService
from utils.contacts import telegram_contact


class FakeLikeRepository:
    def __init__(self, *, created=True, reciprocal=None):
        self.created = created
        self.reciprocal_like = reciprocal
        self.add_calls = []
        self.session = SimpleNamespace(
            scalar=self._scalar,
            get=self._get,
        )
        self.target_profile = SimpleNamespace(
            is_visible=True,
            moderation_locked=False,
            moderation_status=ModerationStatus.CLEAR,
        )
        self.target_user = SimpleNamespace(status=UserStatus.ACTIVE)
    async def _scalar(self, query):
        query_text = str(query).lower()
        if "block" in query_text:
            return None
        return self.target_profile

    async def _get(self, _model, _key):
        return self.target_user

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
````

## File: tests/test_profile_inline_navigation.py
````python
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from handlers.profile import promo_my_profile


@pytest.mark.asyncio
async def test_inline_my_profile_uses_callback_user_id(monkeypatch):
    show_profile = AsyncMock()
    monkeypatch.setattr("handlers.profile.show_profile", show_profile)
    message = SimpleNamespace()
    callback = SimpleNamespace(
        message=message,
        from_user=SimpleNamespace(id=42),
        answer=AsyncMock(),
    )
    session = SimpleNamespace()
    state = SimpleNamespace()

    await promo_my_profile(callback, session, state)

    callback.answer.assert_awaited_once()
    show_profile.assert_awaited_once_with(message, 42, session, state)
````

## File: tests/test_recommendation_extra.py
````python
import asyncio
from types import SimpleNamespace

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

from models import Gender
from services.recommendation import RecommendationService
from services.recommendation_queue import MemoryRecommendationQueue, QueueEntry


def profile(user_id: int, *, age: int = 24, district: str = "Center", interests: list[str] | None = None):
    return SimpleNamespace(
        user_id=user_id,
        gender=Gender.MALE if user_id % 2 else Gender.FEMALE,
        target_gender=Gender.FEMALE if user_id % 2 else Gender.MALE,
        age=age,
        district=district,
        institution="University",
        interests=interests or ["music"],
        bio="Люблю музыку, прогулки и кофе",
    )


class ErrorStrategy:
    def __init__(self, fail_for: set[int] | None = None):
        self.fail_for = set(fail_for or ())

    async def score(self, _viewer, candidate):
        if candidate.user_id in self.fail_for:
            raise RuntimeError("scoring failed")
        return float(candidate.user_id)


class NonFiniteStrategy:
    async def score(self, _viewer, candidate):
        return float("nan") if candidate.user_id == 2 else float(candidate.user_id)


class UnavailableQueue:
    async def pop(self, _user_id):
        raise RedisConnectionError("redis unavailable")


class FakeRepository:
    def __init__(self, mine, candidates):
        self.profiles = {mine.user_id: mine, **{c.user_id: c for c in candidates}}
        self.candidates = candidates
        self.views = []

    async def profile(self, user_id):
        return self.profiles.get(user_id)

    async def eligible_profiles(self, _user_id):
        return self.candidates

    async def eligible_profile(self, _user_id, candidate_id):
        return self.profiles.get(candidate_id)

    async def active_profiles(self, _user_id):
        return self.candidates

    async def record_view_once(self, viewer_id, candidate_id, score):
        if any(viewer == viewer_id and candidate == candidate_id for viewer, candidate, _ in self.views):
            return None
        self.views.append((viewer_id, candidate_id, score))
        return object()


@pytest.mark.asyncio
async def test_rebuild_skips_candidates_with_scoring_exceptions():
    mine = profile(1)
    c1 = profile(2)
    c2 = profile(4)
    repo = FakeRepository(mine, [c1, c2])
    strategy = ErrorStrategy(fail_for={2})
    svc = RecommendationService(None, queue=MemoryRecommendationQueue(), strategy=strategy)
    svc.repo = repo

    count = await svc.rebuild_queue(mine.user_id)
    # one candidate failed scoring and should be skipped
    assert count == 1


@pytest.mark.asyncio
async def test_rebuild_skips_non_finite_scores():
    mine = profile(1)
    c1, c2 = profile(2), profile(4)
    svc = RecommendationService(None, queue=MemoryRecommendationQueue(), strategy=NonFiniteStrategy())
    svc.repo = FakeRepository(mine, [c1, c2])

    assert await svc.rebuild_queue(mine.user_id) == 1
    recommendation = await svc.next_recommendation(mine.user_id)
    assert recommendation is not None
    assert recommendation.profile.user_id == c2.user_id


@pytest.mark.asyncio
async def test_redis_failure_uses_database_as_the_source_of_truth():
    mine = profile(1)
    candidate = profile(2)
    svc = RecommendationService(None, queue=UnavailableQueue())
    svc.repo = FakeRepository(mine, [candidate])

    recommendation = await svc.next_recommendation(mine.user_id)

    assert recommendation is not None
    assert recommendation.profile.user_id == candidate.user_id
    assert svc.repo.views == [(mine.user_id, candidate.user_id, recommendation.score)]


@pytest.mark.asyncio
async def test_concurrent_next_recommendation_no_duplicate_delivery():
    mine = profile(1)
    candidates = [profile(2), profile(3), profile(4)]
    repo = FakeRepository(mine, candidates)
    queue = MemoryRecommendationQueue()
    svc = RecommendationService(None, queue=queue)
    svc.repo = repo

    # rebuild queue
    await svc.rebuild_queue(mine.user_id)

    # run two concurrent next_recommendation calls
    r1, r2 = await asyncio.gather(svc.next_recommendation(mine.user_id), svc.next_recommendation(mine.user_id))

    ids = {r1.profile.user_id if r1 else None, r2.profile.user_id if r2 else None}
    # both results should not be the same candidate
    assert len(ids) == 2


@pytest.mark.asyncio
async def test_duplicate_queue_entries_are_claimed_only_once():
    mine = profile(1)
    candidate = profile(2)
    repo = FakeRepository(mine, [candidate])
    queue = MemoryRecommendationQueue()
    svc = RecommendationService(None, queue=queue)
    svc.repo = repo
    await queue.replace(1, [QueueEntry(candidate.user_id, 100.0), QueueEntry(candidate.user_id, 100.0)])

    first, second = await asyncio.gather(svc.next_recommendation(1), svc.next_recommendation(1))

    assert [item for item in (first, second) if item is not None]
    assert sum(item is not None for item in (first, second)) == 1
    assert repo.views == [(mine.user_id, candidate.user_id, 100.0)]
````

## File: tests/test_recommendation_performance.py
````python
import time
import tracemalloc
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from models import Gender
from services.recommendation import RecommendationService
from services.recommendation_queue import MemoryRecommendationQueue


class FixedStrategy:
    async def score(self, _viewer, candidate):
        return float(candidate.user_id)


class PerformanceRepository:
    def __init__(self, mine, candidates):
        self.mine = mine
        self.candidates = candidates
        self.query_count = 0

    async def profile(self, user_id):
        if user_id == self.mine.user_id:
            return self.mine
        return None

    async def eligible_profiles(self, _user_id):
        self.query_count += 1
        return self.candidates

    async def eligible_profile(self, _user_id, candidate_id):
        self.query_count += 1
        return next((candidate for candidate in self.candidates if candidate.user_id == candidate_id), None)

    async def active_profiles(self, _user_id):
        return self.candidates

    async def record_view_once(self, viewer_id, candidate_id, score):
        return object()


def profile(user_id: int):
    return SimpleNamespace(
        user_id=user_id,
        gender=Gender.MALE if user_id % 2 else Gender.FEMALE,
        target_gender=Gender.FEMALE if user_id % 2 else Gender.MALE,
        age=24,
        district="Center",
        institution="University",
        interests=["music"],
        bio="Люблю музыку",
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("candidate_count", [50, 200, 500, 1000, 2000, 5000])
async def test_recommendation_service_handles_large_candidate_sets(candidate_count):
    mine = profile(1)
    candidates = [profile(candidate_id) for candidate_id in range(2, candidate_count + 2)]
    for candidate in candidates:
        candidate.gender = Gender.FEMALE
        candidate.target_gender = Gender.MALE
    service = RecommendationService(None, queue=MemoryRecommendationQueue(), strategy=FixedStrategy())
    service.repo = PerformanceRepository(mine, candidates)

    tracemalloc.start()
    start_cpu = time.process_time()
    start_wall = time.perf_counter()
    queue_size = await service.rebuild_queue(mine.user_id)
    build_cpu = time.process_time() - start_cpu
    build_wall = time.perf_counter() - start_wall
    first_start_cpu = time.process_time()
    first_start_wall = time.perf_counter()
    first = await service.next_recommendation(mine.user_id)
    first_cpu = time.process_time() - first_start_cpu
    first_wall = time.perf_counter() - first_start_wall
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    assert queue_size == candidate_count
    assert first is not None
    assert first.profile.user_id == candidate_count + 1
    assert service.repo.query_count <= candidate_count + 2

    print(
        f"count={candidate_count} queue_build_ms={build_wall * 1000:.2f} "
        f"first_profile_ms={first_wall * 1000:.2f} queries={service.repo.query_count} "
        f"cpu_ms={build_cpu * 1000:.2f}/{first_cpu * 1000:.2f} mem_kib={peak / 1024:.2f}"
    )
````

## File: tests/test_recommendation_queue.py
````python
import pytest

from services.recommendation_queue import QueueEntry, RedisRecommendationQueue


class FakeRedis:
    def __init__(self):
        self.store = {}

    async def delete(self, key):
        self.store.pop(key, None)

    async def rpush(self, key, *values):
        self.store.setdefault(key, []).extend(values)

    async def lpop(self, key):
        values = self.store.get(key)
        if not values:
            return None
        return values.pop(0)

    async def eval(self, script, numkeys, *args):
        key = args[0]
        if "for i = 1, #ARGV do" in script:
            self.store[key] = list(args[1:])
            return len(args) - 1
        candidate_id = int(args[1])
        values = list(self.store.get(key, []))
        if "entry" in script:
            filtered = [value for value in values if self._candidate_id(value) != candidate_id]
            self.store[key] = filtered + [args[2]]
        else:
            self.store[key] = [value for value in values if self._candidate_id(value) != candidate_id]
        return 1

    @staticmethod
    def _candidate_id(raw):
        return int(str(raw).split(":", 1)[0])


@pytest.mark.asyncio
async def test_redis_queue_replace_and_pop_are_ordered_and_persistent():
    redis = FakeRedis()
    queue = RedisRecommendationQueue(redis)

    await queue.replace(1, [QueueEntry(2, 10.0), QueueEntry(3, 20.0)])

    assert await queue.pop(1) == QueueEntry(2, 10.0)
    assert await queue.pop(1) == QueueEntry(3, 20.0)
    assert await queue.pop(1) is None


@pytest.mark.asyncio
async def test_redis_queue_replace_deduplicates_candidates():
    redis = FakeRedis()
    queue = RedisRecommendationQueue(redis)

    await queue.replace(1, [QueueEntry(2, 10.0), QueueEntry(2, 20.0), QueueEntry(3, 30.0)])

    assert await queue.pop(1) == QueueEntry(2, 10.0)
    assert await queue.pop(1) == QueueEntry(3, 30.0)
    assert await queue.pop(1) is None


@pytest.mark.asyncio
async def test_redis_queue_move_to_end_and_remove_keep_the_expected_entries():
    redis = FakeRedis()
    queue = RedisRecommendationQueue(redis)

    await queue.replace(1, [QueueEntry(2, 10.0), QueueEntry(3, 20.0), QueueEntry(4, 30.0)])
    await queue.move_to_end(1, 3, 25.0)
    await queue.remove(1, 2)

    assert await queue.pop(1) == QueueEntry(4, 30.0)
    assert await queue.pop(1) == QueueEntry(3, 25.0)
    assert await queue.pop(1) is None


@pytest.mark.asyncio
async def test_redis_queue_skips_corrupted_entries_and_returns_next_valid_entry():
    redis = FakeRedis()
    queue = RedisRecommendationQueue(redis)

    redis.store["recommendation_queue:1"] = ["bad-entry", "3:30"]

    assert await queue.pop(1) == QueueEntry(3, 30.0)
    assert await queue.pop(1) is None
````

## File: tests/test_recommendation_repository.py
````python
from sqlalchemy.dialects import postgresql

from repositories.recommendation import RecommendationRepository


def test_recommendations_exclude_blocks_in_both_directions():
    """A profile must disappear whether the viewer blocked it or was blocked by it."""
    repository = RecommendationRepository(None)
 
    # Compile-only regression test: it validates the SQL predicate without requiring PostgreSQL.
    import asyncio
 
    class Session:
        statement = None
 
        async def scalars(self, statement):
            self.statement = statement
 
            class Result:
                def all(self):
                   return []
 
            return Result()
 
    session = Session()
    repository.session = session
    asyncio.run(repository.eligible_profiles(10))
    sql = str(session.statement.compile(dialect=postgresql.dialect()))
 
    assert sql.count("blocks") >= 2
 

def test_recommendations_exclude_previously_viewed_profiles():
    repository = RecommendationRepository(None)
 
    import asyncio
 
    class Session:
        statement = None
 
        async def scalars(self, statement):
            self.statement = statement
 
            class Result:
                def all(self):
                   return []
 
            return Result()
 
    session = Session()
    repository.session = session
    asyncio.run(repository.eligible_profiles(10))
    sql = str(session.statement.compile(dialect=postgresql.dialect()))
 
    assert "recommendation_views" in sql
````

## File: tests/test_recommendation.py
````python
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from models import Gender
from services.recommendation import RecommendationService
from services.recommendation_queue import MemoryRecommendationQueue, QueueEntry
from services.recommendation_strategy import WeightedRecommendationStrategy


def profile(user_id: int, *, age: int = 24, district: str = "Center", interests: list[str] | None = None):
    return SimpleNamespace(
        user_id=user_id,
        gender=Gender.MALE if user_id % 2 else Gender.FEMALE,
        target_gender=Gender.FEMALE if user_id % 2 else Gender.MALE,
        age=age,
        district=district,
        institution="University",
        interests=interests or ["music"],
        bio="Люблю музыку, прогулки и кофе",
        created_at=datetime(2026, 1, user_id % 28 + 1, tzinfo=UTC),
    )


class FakeRecommendationRepository:
    def __init__(self, mine, candidates):
        self.profiles = {mine.user_id: mine, **{item.user_id: item for item in candidates}}
        self.candidates = candidates
        self.views = []
 
    async def profile(self, user_id):
        return self.profiles.get(user_id)
 
    async def eligible_profiles(self, _user_id):
        return self.candidates
 
    async def eligible_profile(self, _user_id, candidate_id):
        return self.profiles.get(candidate_id)
 
    async def active_profiles(self, _user_id):
        return self.candidates
 
    async def record_view_once(self, viewer_id, candidate_id, score):
        if any(viewer == viewer_id and candidate == candidate_id for viewer, candidate, _ in self.views):
            return None
        self.views.append((viewer_id, candidate_id, score))
        return object()
 
 
class ViewedRecommendationRepository(FakeRecommendationRepository):
    async def eligible_profiles(self, _user_id):
        viewed = {candidate_id for viewer_id, candidate_id, _ in self.views if viewer_id == _user_id}
        return [candidate for candidate in self.candidates if candidate.user_id not in viewed]
 
    async def eligible_profile(self, _user_id, candidate_id):
        if any(
            viewer_id == _user_id and seen_candidate_id == candidate_id
            for viewer_id, seen_candidate_id, _ in self.views
        ):
            return None
        return self.profiles.get(candidate_id)


class FixedRecommendationStrategy:
    async def score(self, _viewer, candidate):
        return float(candidate.user_id)


def service(mine, candidates):
    result = RecommendationService(None, queue=MemoryRecommendationQueue())
    result.repo = FakeRecommendationRepository(mine, candidates)
    return result


def test_dating_keyboard_has_no_next_profile_button():
    from keyboards.dating import dating_keyboard

    markup = dating_keyboard(42)
    callback_data = {button.callback_data for row in markup.inline_keyboard for button in row}

    assert "next:profile" not in callback_data


def test_compute_score_uses_configurable_default_weights():
    mine = profile(1, age=20)
    candidate = profile(2, age=21)

    assert RecommendationService.compute_score(mine, candidate) == 99.5


def test_normalize_text_matching_handles_aliases():
    from services.recommendation_strategy import WeightedRecommendationStrategy

    assert WeightedRecommendationStrategy._text_match("Bălți", "Бельцы") == 1.0
    assert WeightedRecommendationStrategy._text_match("CPB", "Colegiul Politehnic") == 1.0


def test_weighted_strategy_rejects_invalid_weight_configuration():
    with pytest.raises(ValueError, match="Неизвестные"):
        WeightedRecommendationStrategy({"unknown": 1})
    with pytest.raises(ValueError, match="Сумма"):
        WeightedRecommendationStrategy({name: 0 for name in WeightedRecommendationStrategy().weights})
    with pytest.raises(ValueError, match="неотрицательными"):
        WeightedRecommendationStrategy({"age": float("nan")})


@pytest.mark.asyncio
async def test_empty_database_or_one_user_has_no_recommendation():
    mine = profile(1)
    engine = service(mine, [])

    assert await engine.next_recommendation(mine.user_id) is None


@pytest.mark.asyncio
async def test_two_users_receive_ranked_recommendation_and_view_event():
    mine = profile(1)
    candidate = profile(2)
    engine = service(mine, [candidate])

    recommendation = await engine.next_recommendation(mine.user_id)

    assert recommendation is not None
    assert recommendation.profile is candidate
    assert recommendation.score == 100.0
    assert engine.repo.views == [(1, 2, 100.0)]


@pytest.mark.asyncio
async def test_engine_accepts_replacement_strategy_without_handler_changes():
    mine = profile(1)
    first, second = profile(2), profile(4)
    engine = RecommendationService(None, queue=MemoryRecommendationQueue(), strategy=FixedRecommendationStrategy())
    engine.repo = FakeRecommendationRepository(mine, [first, second])

    recommendation = await engine.next_recommendation(mine.user_id)

    assert recommendation is not None
    assert recommendation.profile is second
    assert recommendation.score == 4.0


@pytest.mark.asyncio
async def test_stale_queue_entry_is_skipped_without_recursion():
    mine, candidate = profile(1), profile(2)
    engine = service(mine, [candidate])
    await engine.queue.replace(1, [QueueEntry(999, 99), QueueEntry(candidate.user_id, 90)])

    recommendation = await engine.next_recommendation(1)

    assert recommendation is not None
    assert recommendation.profile is candidate


@pytest.mark.asyncio
@pytest.mark.parametrize("candidate_count", [10, 100])
async def test_ten_and_hundred_candidates_are_sorted_without_duplicates(candidate_count):
    mine = profile(1)
    candidates = [
        profile(number, age=20 + number % 20, district="Center" if number % 3 else "North")
        for number in range(2, candidate_count + 2)
    ]
    for candidate in candidates:
        candidate.gender = Gender.FEMALE
        candidate.target_gender = Gender.MALE
    engine = service(mine, candidates)

    assert await engine.rebuild_queue(mine.user_id) == candidate_count
    delivered = []
    for _ in candidates:
        recommendation = await engine.next_recommendation(mine.user_id)
        assert recommendation is not None
        delivered.append(recommendation.profile.user_id)

    assert len(delivered) == candidate_count
    assert len(set(delivered)) == candidate_count
    assert delivered[0] == 4


@pytest.mark.asyncio
async def test_skip_moves_profile_to_end_of_current_queue():
    mine = profile(1)
    first, second, third = profile(2), profile(4, age=35), profile(6, age=38)
    engine = service(mine, [first, second, third])
 
    await engine.rebuild_queue(1)
    await engine.skip(1, first.user_id)
    delivered = [
        (await engine.next_recommendation(1)).profile.user_id,
        (await engine.next_recommendation(1)).profile.user_id,
        (await engine.next_recommendation(1)).profile.user_id,
    ]
 
    assert delivered[-1] == first.user_id
 
 
@pytest.mark.asyncio
async def test_viewed_profiles_are_excluded_from_recommendations():
    mine = profile(1)
    candidate = profile(2)
    engine = RecommendationService(None, queue=MemoryRecommendationQueue())
    engine.repo = ViewedRecommendationRepository(mine, [candidate])
    engine.repo.views.append((1, candidate.user_id, 80.0))
 
    await engine.rebuild_queue(mine.user_id)
 
    assert await engine.next_recommendation(mine.user_id) is None
 
 
def test_incompatible_gender_is_not_eligible_for_queue():
    mine, candidate = profile(1), profile(3)
    candidate.gender = Gender.MALE
    engine = service(mine, [candidate])

    assert not engine.is_compatible(mine, candidate)


@pytest.mark.asyncio
async def test_paused_or_blocked_profiles_are_not_delivered_when_repository_excludes_them():
    mine = profile(1)
    engine = service(mine, [])

    assert await engine.rebuild_queue(mine.user_id) == 0
    assert await engine.next_recommendation(mine.user_id) is None
````

## File: tests/test_verification_handlers.py
````python
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from handlers.verification import verification_start
from services.profile_service import ProfileService
from states.verification import VerificationState


@pytest.mark.asyncio
async def test_verification_start_shows_status_if_already_verified(monkeypatch):
    # Prepare a fake profile marked as VERIFIED
    fake_profile = SimpleNamespace(verification_status=SimpleNamespace(value="VERIFIED"))

    async def fake_get_profile(self, user_id: int):
        return fake_profile

    monkeypatch.setattr(ProfileService, "get_profile", fake_get_profile)

    message = SimpleNamespace(from_user=SimpleNamespace(id=7), answer=AsyncMock())
    state = SimpleNamespace(set_state=AsyncMock())

    # Call handler
    await verification_start(message, state, session=None)

    # Should not set FSM state and should answer with verified status
    assert not state.set_state.called
    message.answer.assert_called_once()
    called_text = message.answer.call_args.args[0]
    assert "вы уже верифицированы" in called_text.lower() or "verified" in called_text.lower()


@pytest.mark.asyncio
async def test_verification_start_prompts_recording_when_not_verified(monkeypatch):
    # Prepare a fake profile not verified
    fake_profile = SimpleNamespace(verification_status=SimpleNamespace(value="UNVERIFIED"))

    async def fake_get_profile(self, user_id: int):
        return fake_profile

    monkeypatch.setattr(ProfileService, "get_profile", fake_get_profile)

    message = SimpleNamespace(from_user=SimpleNamespace(id=8), answer=AsyncMock())
    state = SimpleNamespace(set_state=AsyncMock())

    await verification_start(message, state, session=None)

    # Should set FSM state to waiting_video and prompt for recording
    state.set_state.assert_called_once_with(VerificationState.waiting_video)
    message.answer.assert_called_once()
    called_text = message.answer.call_args.args[0]
    assert "видеосообщение" in called_text.lower() or "video" in called_text.lower()
````

## File: tests/test_verification_ownership.py
````python
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
````

## File: tools/__init__.py
````python
# tools package marker
````

## File: tools/seed_test_profiles.py
````python
# DEVELOPMENT/ALPHA TOOL ONLY
# This script creates test profiles for development and fills recommendation queues.

"""
Usage:
  python -m tools.seed_test_profiles --count 50

Notes:
- Only allowed when ENV or ENVIRONMENT is set to 'development', 'dev' or 'test'.
- Will refuse to run when ENV/ENVIRONMENT == 'production'.
- Inserts Users and Profiles with synthetic data and triggers RecommendationService.rebuild_queue

"""

import argparse
import asyncio
import os
import random
import sys

# Do not execute on import
if __name__ != "__main__":
    __all__ = []


FIRST_NAMES = [
    "Alex", "Ivan", "Marius", "Andrei", "Diana", "Elena", "Maria", "Olga", "Sergiu", "Nikita",
    "Irina", "Vlad", "Anna", "Oleg", "Tatiana", "Cristina", "Yuri", "Ion", "Nicoleta", "Eugen",
]
CITIES = [
    "Bălți", "Chișinău", "Кишинёв", "Balti", "Chișinău Center", "Bălți Sector 1", "Centru", "Râșcani",
]
INTERESTS = [
    "music", "travel", "movies", "sports", "hiking", "reading", "cooking", "technology", "photography", "dancing",
]
BIOS = [
    "Love exploring new places and coffee.",
    "Working in tech, looking to meet interesting people.",
    "Dog lover, runner, and amateur chef.",
    "Into movies, board games, and good conversations.",
    "Student of life — curiosity first.",
]


def _ensure_env_dev() -> None:
    env = (os.environ.get("ENV") or os.environ.get("ENVIRONMENT") or "").lower()
    if env in ("production", "prod"):
        print("Refusing to run in production environment (ENV/ENVIRONMENT=production).", file=sys.stderr)
        sys.exit(2)
    if env not in ("development", "dev", "test"):
        print(f"Danger: ENV/ENVIRONMENT must be one of: development, dev, test. Got: {env!r}", file=sys.stderr)
        sys.exit(3)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed test profiles (development only)")
    parser.add_argument("--count", type=int, default=50, help="How many profiles to create")
    parser.add_argument(
        "--photo-file-id",
        type=str,
        default=None,
        help="Optional Telegram file_id to use for all photos (useful for real-file testing)",
    )
    parser.add_argument(
        "--target-gender",
        type=str,
        choices=["MALE", "FEMALE", "ALL"],
        default=None,
        help="Optional target gender for created profiles",
    )
    return parser.parse_args()


async def _seed(count: int, photo_file_id: str | None, target_gender: str | None = None) -> list[int]:
    # Lazy imports to avoid side-effects at module import

    from config import get_settings
    from database.connection import make_session_factory
    from models.profile import Profile
    from models.user import User

    settings = get_settings()
    factory = make_session_factory(settings)

    created_ids: list[int] = []

    async with factory() as session:
        async with session.begin():
            # choose a base telegram id high enough not to collide with real users
            base = 200000
            for i in range(count):
                user_id = base + i
                name = random.choice(FIRST_NAMES)
                age = random.randint(18, 30)
                city = random.choice(CITIES)
                interests = random.sample(INTERESTS, k=random.randint(1, 4))
                bio = random.choice(BIOS)
                username = f"testuser{user_id}"

                user = User(id=user_id, username=username)
                # Photo placeholders (these are not real Telegram file ids but valid strings used by system tests)
                if photo_file_id:
                    photo_ids = [photo_file_id]
                else:
                    # Use public placeholder image URLs by default (picsum seed ensures variety)
                    num_photos = random.randint(2, 3)
                    photo_ids = [f"https://picsum.photos/seed/{user_id}_{j}/600/800" for j in range(1, num_photos + 1)]
                # determine gender for profile
                if target_gender in ("MALE", "FEMALE", "ALL"):
                    gender_val = target_gender
                else:
                    gender_val = random.choice(["MALE", "FEMALE"])

                profile = Profile(
                    user_id=user_id,
                    gender=gender_val,
                    target_gender="ALL",
                    name=name,
                    age=age,
                    district=city,
                    institution=random.choice(["USM", "Technical University", "State University"]),
                    interests=interests,
                    bio=bio,
                    photo_file_ids=photo_ids,
                    main_photo_file_id=photo_ids[0] if photo_ids else None,
                    is_visible=True,
                    moderation_locked=False,
                )
                session.add(user)
                session.add(profile)
                created_ids.append(user_id)
        # commit happens on context exit
    print(
        f"Created {len(created_ids)} test users: "
        f"{created_ids[:5]}{'...' if len(created_ids) > 5 else ''}"
    )

    # Now trigger rebuild_queue for each created user so Redis queues are filled.
    # We create a short-lived session per user to run the rebuild, which relies on
    # services.recommendation.RecommendationService.
    from services.recommendation import RecommendationService

    for uid in created_ids:
        async with factory() as session:
            svc = RecommendationService(session)
            n = await svc.rebuild_queue(uid)
            print(f"Rebuilt queue for {uid}: {n} entries")

    # Close global default queue Redis client if present to avoid destructor warnings
    from services.recommendation_queue import get_default_queue

    try:
        q = get_default_queue()
        if hasattr(q, "_redis"):
            try:
                await q._redis.aclose()
            except Exception:
                pass
    except Exception:
        pass

    return created_ids


def main() -> None:
    _ensure_env_dev()
    args = _parse_args()
    asyncio.run(_seed(args.count, args.photo_file_id, args.target_gender))


if __name__ == "__main__":
    main()
````

## File: tools/simulate_events.py
````python
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
````

## File: utils/__init__.py
````python

````

## File: utils/admin_ui.py
````python
from __future__ import annotations

import uuid


def compact_display_id(value: str | int | uuid.UUID | None) -> str:
    if value is None:
        return "—"
    if isinstance(value, uuid.UUID):
        return str(value).replace("-", "")[:8]
    if isinstance(value, int):
        digits = str(abs(value))
        return digits[-6:] if len(digits) > 6 else digits or "0"
    text = str(value).replace("-", "")
    return text[:8] if len(text) > 8 else text or "—"


def admin_role_label(
    admin_id: int,
    *,
    username: str | None = None,
    owner_admin_id: int | None = None,
    owner_name: str = "Netakussia",
) -> str:
    if owner_admin_id is not None and admin_id == owner_admin_id:
        return f"👑 {owner_name} — владелец"
    handle = f"@{username.lstrip('@')}" if username else "модератор"
    return f"⚔️ {handle} — модератор"


def user_display_name(user_id: int, *, username: str | None = None) -> str:
    if username:
        return f"@{username.lstrip('@')}"
    return f"#{compact_display_id(user_id)}"
````

## File: utils/contacts.py
````python
from html import escape


def telegram_contact(user_id: int, username: str | None, display_name: str) -> str:
    """Returns a public @username or a Telegram deep link when no username exists."""

    if username:
        return f"@{username}"
    return f'<a href="tg://user?id={user_id}">{escape(display_name)}</a>'
````

## File: utils/db_reset.py
````python
from __future__ import annotations

import asyncio
import os
import sys

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

RESET_TABLES = [
    "likes",
    "dislikes",
    "matches",
    "reports",
    "appeals",
    "verification_requests",
    "photo_moderations",
    "trust_score_events",
    "moderation_cases",
    "confessions",
    "confession_daily_limits",
    "admin_logs",
    "profiles",
    "users",
]


def get_reset_table_names() -> list[str]:
    return list(RESET_TABLES)


def _build_database_urls(explicit_url: str | None = None) -> list[str]:
    candidates: list[str] = []
    if explicit_url:
        candidates.append(explicit_url)

    env_url = os.getenv("DATABASE_URL") or os.getenv("DATABASE_URL_ASYNC")
    if env_url:
        candidates.append(env_url)

    if "localhost" in env_url if env_url else False:
        candidates.append(env_url.replace("localhost", "postgres", 1))

    candidates.extend(
        [
            "postgresql+asyncpg://postgres:postgres@localhost:5432/dating_db",
            "postgresql+asyncpg://postgres:postgres@postgres:5432/dating_db",
        ]
    )

    return list(dict.fromkeys(candidates))


async def reset_database(database_url: str | None = None, *, confirm: bool = False) -> list[str]:
    if not confirm:
        raise ValueError("Reset requires confirm=True")

    last_error: Exception | None = None
    for url in _build_database_urls(database_url):
        try:
            engine = create_async_engine(url)
            try:
                async with engine.begin() as connection:
                    for table in RESET_TABLES:
                        await connection.execute(text(f'DELETE FROM "{table}"'))
                    await connection.execute(text('ALTER SEQUENCE IF EXISTS users_id_seq RESTART WITH 1'))
                    await connection.execute(text('ALTER SEQUENCE IF EXISTS profiles_id_seq RESTART WITH 1'))
            finally:
                await engine.dispose()
            return RESET_TABLES
        except Exception as exc:  # pragma: no cover - exercised at runtime
            last_error = exc

    if last_error is not None:
        message = (
            "Failed to connect to PostgreSQL. "
            "Start the test database first, for example: "
            "docker compose up -d postgres redis"
        )
        raise RuntimeError(f"{message}\nOriginal error: {last_error}") from last_error
    raise RuntimeError("Failed to reset database: no connection information provided")


def main() -> None:
    database_url = os.getenv("DATABASE_URL") or os.getenv("DATABASE_URL_ASYNC")
    try:
        asyncio.run(reset_database(database_url, confirm=True))
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
````

## File: utils/deep_links.py
````python

````

## File: utils/logging.py
````python

````

## File: utils/profile_media.py
````python
import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message

from models import Profile

logger = logging.getLogger(__name__)


def profile_photo_ids(profile: Profile | None) -> list[str]:
    """Return the list of photo IDs used by moderation and reporting flows."""
    if profile is None:
        return []
    photos = ordered_photo_ids(profile)
    return photos or ([profile.photo_file_id] if profile.photo_file_id else [])


def ordered_photo_ids(profile: Profile) -> list[str]:
    """Return gallery order with the chosen main image first."""
    photos = list(profile.photo_file_ids or [])
    main = profile.main_photo_file_id
    if main in photos:
        photos.remove(main)
        photos.insert(0, main)
    return photos or ([profile.photo_file_id] if profile.photo_file_id else [])


async def send_profile_gallery(
    message: Message, profile: Profile, caption: str, reply_markup: InlineKeyboardMarkup
) -> None:
    photos = ordered_photo_ids(profile)
    if not photos:
        await message.answer(caption, reply_markup=reply_markup)
        return
    # Single photo case: try sending photo, fallback to text or placeholder if Telegram rejects media
    if len(photos) <= 1:
        try:
            await message.answer_photo(photos[0], caption=caption, reply_markup=reply_markup)
            return
        except TelegramBadRequest as e:
            logger.warning(
                "Failed to send photo for profile %s: %s. Falling back to text message.",
                profile.user_id,
                e,
            )
            # Send text fallback and optionally a generic placeholder image link
            fallback_text = f"{caption}\n\n[image unavailable]"
            await message.answer(fallback_text, reply_markup=reply_markup)
            return
    # Multiple photos: try media group, fallback to single-photo sends or text
    media = [
        InputMediaPhoto(media=photo_id, caption=caption if index == 0 else None)
        for index, photo_id in enumerate(photos)
    ]
    try:
        await message.answer_media_group(media)
        await message.answer("Выберите действие:", reply_markup=reply_markup)
    except TelegramBadRequest as e:
        logger.warning(
            "Failed to send media group for profile %s: %s. Attempting individual sends/fallback.",
            profile.user_id,
            e,
        )
        # Try sending first photo alone, then text
        first = photos[0]
        try:
            await message.answer_photo(first, caption=caption, reply_markup=reply_markup)
        except TelegramBadRequest as e2:
            logger.warning(
                "Failed to send first photo fallback for profile %s: %s. Sending text-only fallback.",
                profile.user_id,
                e2,
            )
            await message.answer(f"{caption}\n\n[image unavailable]", reply_markup=reply_markup)
        else:
            # if first photo succeeded, prompt for action
            await message.answer("Выберите действие:", reply_markup=reply_markup)
````

## File: utils/text.py
````python
from __future__ import annotations

from html import escape as _html_escape


def escape_html(value: object) -> str:
    """Escape text for safe Telegram HTML rendering."""
    if value is None:
        return ""
    return _html_escape(str(value), quote=True)


__all__ = ["escape_html"]
````

## File: validators/__init__.py
````python
from validators.profile_validator import ProfileValidationError, validate_profile_payload

__all__ = ("ProfileValidationError", "validate_profile_payload")
````

## File: __init__.py
````python

````

## File: .dockerignore
````
.git
.env
__pycache__/
**/__pycache__/
*.pyc
*.zip
project/
logs/
````

## File: alembic.ini
````ini
[alembic]
script_location = database/migrations
prepend_sys_path = .
sqlalchemy.url = driver://user:pass@localhost/dbname

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
````

## File: conftest.py
````python
import sys
from pathlib import Path

# Ensure project root is on sys.path so local imports work when running pytest
ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
````

## File: docker-compose.override.yml.example
````
# Example override for local development to expose Redis/DB ports for GUI clients
# Copy this file to docker-compose.override.yml (do NOT commit) when needed.

version: '3.8'
services:
  redis:
    ports:
      - "6379:6379"
  postgres:
    ports:
      - "5432:5432"
  bot:
    volumes:
      - ./:/app:cached
    environment:
      - LOCAL_DEV=1
# Note: This override is for convenience only. Do not commit docker-compose.override.yml with secrets or published ports.
````

## File: Dockerfile
````dockerfile
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Schema changes are owned exclusively by Alembic and are applied before polling.
CMD ["sh", "-c", "alembic upgrade head && exec python main.py"]
````

## File: main.py
````python
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
    factory = make_session_factory(settings, engine=engine)
    redis = Redis.from_url(settings.redis_url)
    bot, dp = create_dispatcher(settings, factory, redis)
    try:
        if bot is None:
            # Offline mode (invalid or missing BOT_TOKEN). Keep process alive for debugging
            logger.warning(
                "Bot running in offline mode due to invalid or missing BOT_TOKEN. "
                "Dispatcher wired but not polling."
            )
            # Block indefinitely so container stays up and logs can be inspected
            await asyncio.Event().wait()
        # Normal startup with a valid bot
        await set_commands(bot)
        await dp.start_polling(bot)
    except Exception:
        logger.exception("Bot polling failed")
        raise
    finally:
        await redis.aclose()
        await engine.dispose()
        if bot is not None:
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
````

## File: PROJECT_RULES.md
````markdown
# PROJECT_RULES

## 1. Используемый стек
- Python 3.12
- aiogram 3.x для Telegram-бота
- SQLAlchemy 2.x + asyncpg для работы с PostgreSQL
- Alembic для миграций
- Redis для FSM storage и rate limiting
- Pydantic + pydantic-settings для конфигурации
- pytest для тестов
- Docker Compose для локального запуска

## 2. Архитектурные принципы
- Проект строится по слоям: handlers -> services -> repositories -> models.
- Бизнес-логика не должна находиться прямо в обработчиках.
- Все операции с БД выполняются через асинхронные сессии.
- Telegram-обработчики должны быть тонкими и ориентированными на сценарий пользователя.
- Состояния диалога (FSM) описываются в отдельных модулях states/.
- Конфигурация должна читаться из .env и централизоваться в config.py.

## 3. Правила кодирования
- Код должен быть читаемым, коротким и понятным.
- Следовать стилю Ruff/PEP8.
- Не использовать блокирующие вызовы в обработчиках.
- Не хранить секреты в коде.
- Новые функции должны иметь понятные имена и быть покрытыми тестами по возможности.
- Изменения должны быть локальными и не ломать существующие сценарии.

## 4. Соглашения по именованию
- Модули: snake_case.
- Классы: PascalCase.
- Функции/методы: snake_case.
- Константы: UPPER_SNAKE_CASE.
- FSM-состояния: PascalCase для классов StatesGroup, snake_case для полей состояний.
- SQLAlchemy модели: PascalCase, таблицы в snake_case.

## 5. Структура каталогов
- main.py — точка входа.
- bot/ — настройка бота и команд.
- handlers/ — Telegram-обработчики.
- services/ — бизнес-логика.
- repositories/ — доступ к данным.
- models/ — ORM-модели.
- states/ — FSM-состояния.
- keyboards/ — клавиатуры.
- filters/ — фильтры aiogram.
- middlewares/ — промежуточные слои.
- utils/ — вспомогательные функции.
- tests/ — тесты.
- database/ — базовая конфигурация и миграции.

## 6. Правила локализации
- Тексты интерфейса в основном должны быть на русском.
- Слова и фразы не следует размазывать по нескольким файлам без необходимости.
- Для новых сценариев лучше добавлять текст рядом с обработчиком, если это не нарушает структуру.
- В дальнейшем возможно выделение отдельного слоя локализации, но сейчас это не требуется.

## 7. Требования к безопасности
- BOT_TOKEN и другие секреты не должны попадать в репозиторий.
- Для признаний используется дневной salted SHA-256-хэш для ограничения спама.
- В продакшене требуется отдельная модерация и правила конфиденциальности.
- Фото должны проходить проверку через отдельный сервис, а не доверять только клиентской логике.

## 8. Требования к Docker
- Проект должен запускаться через Docker Compose.
- Контейнеры: bot, postgres, redis.
- База данных и Redis должны быть здоровыми до старта бота.
- Сборка должна быть воспроизводимой и не зависеть от локального окружения разработчика.

## 9. Требования к БД
- Основная БД — PostgreSQL.
- SQLAlchemy модели должны быть синхронизированы с миграциями.
- При изменении схемы необходимо добавлять Alembic-миграции.
- Важно учитывать индексы и ограничения на ключевые сущности: users, profiles, likes, matches, reports, appeals.

## 10. Правила работы FSM
- Каждое состояние диалога должно быть объявлено в модуле states/.
- Обработчики должны быть привязаны к конкретным состояниям через aiogram FSM.
- После завершения сценария состояние должно очищаться.
- Данные сценария следует хранить в FSMContext и не смешивать с глобальным состоянием.

## 11. Правила UI
- Взаимодействие строится через inline-кнопки и reply-клавиатуры.
- Основные действия должны быть понятны и быстры.
- Для администратора нужен отдельный модуль интерфейса и понятный набор действий.
- В сообщениях следует избегать перегруженного текста.

## 12. Правила разработки
- Работать в рамках существующей архитектуры, не вводя новый слой без необходимости.
- Перед изменением схемы БД и бизнес-правил изучать текущие сервисы и репозитории.
- Не изменять код без понимания влияния на меню, FSM и репозитории.
- Для новых функций сначала оценивать, где они лучше вписываются: handler, service или repository.

## 13. Требования к масштабируемости
- Сервис должен быть готов к расширению за счёт выделения логики в services/ и repositories/.
- Redis следует использовать для временного состояния и антиспама.
- При росте нагрузки стоит выделять отдельные очереди и сервисы для уведомлений и модерации.

## 14. Требования к документации
- При изменении архитектуры или ключевых сценариев обновлять документацию в docs/.
- Документация должна отражать фактическое состояние проекта, а не только желаемое.
- Для новых функций и критичных изменений лучше добавлять краткую заметку в dev_notes.md.
````

## File: pyproject.toml
````toml
[tool.ruff]
target-version = "py312"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
````

## File: requirements.txt
````
aiogram==3.4.1
sqlalchemy==2.0.29
asyncpg==0.29.0
alembic==1.13.1
pydantic==2.5.3
pydantic-settings==2.2.1
redis==5.0.3
structlog==24.1.0
python-dotenv==1.0.1
Pillow==10.4.0
numpy==1.26.4
onnxruntime==1.19.2
opencv-python-headless==4.10.0.84
ruff==0.9.10
pytest==7.4.0
pytest-asyncio==0.22.0
````

## File: ROADMAP.md
````markdown
# Roadmap

## Этап 1
- [x] Архитектура
- [x] Docker
- [x] База данных
- [x] Регистрация
- [x] Алгоритм рекомендаций
- [x] Лайки
- [x] Мэтчи
- [x] Жалобы
- [x] Trust System: верификация, жалобы, автоматическая модерация, апелляции, NSFW-очередь, рейтинг доверия
- [x] Админ-панель
- [x] Анонимные признания
- [x] Локализация (базовая)
- [x] Полировка UX
- [x] Стресс-тесты
- [x] Production hardening: baseline Alembic, Redis queue, реальный NSFW/face provider, retention и observability
- [ ] Production Release

## Принцип обновления

После завершения каждого модуля следующий агент должен отмечать прогресс здесь, а не только в чате.
````

## File: TEST_CHECKLIST.md
````markdown
# Чек-лист ручного тестирования

Для проверки нужны два обычных Telegram-аккаунта (A и B) и один аккаунт администратора (C), ID которого указан в `ADMIN_IDS` файла `.env`.

Перед тестом обновите контейнеры:

```bash
docker compose up --build
```

## 1. Регистрация и выдача

- [ ] На аккаунтах A и B нажмите `/start` и заполните анкеты.
- [ ] У A и B выставьте совместимые пол и «кого ищет».
- [ ] На A нажмите «💘 Знакомства»: должна показаться анкета B с фото, возрастом, районом, местом и интересами.
- [ ] Нажмите «👎»: анкета B не должна появиться снова.
- [ ] На другой тестовой анкете нажмите «🚫»: она также не должна появляться; взаимная блокировка не позволит ей увидеть A.

## 2. Приватность лайков и матч

- [ ] Создайте ещё две совместимые анкеты D и E.
- [ ] С D поставьте лайк E. E должен получить только сообщение «Кому-то понравилась ваша анкета», без имени, фото, username или ссылки.
- [ ] На E нажмите «❤️ Симпатии». Входящий лайк не должен раскрывать контакт D.
- [ ] Поставьте лайк D с E. Оба аккаунта должны получить «Взаимная симпатия» и кликабельный контакт или `@username`.
- [ ] На E нажмите «❤️ Симпатии»: D должен быть в списке взаимных симпатий с контактом.
- [ ] Проверьте кнопку «💌»: текст до 200 символов отправляется вместе с лайком; личность до матча не раскрывается.

## 3. Жалобы и приостановка

- [ ] С трёх разных тестовых аккаунтов отправьте жалобу на одну анкету через «⚠️» и выберите причины.
- [ ] После третьей жалобы анкета должна исчезнуть из выдачи и стать приостановленной.
- [ ] Откройте «👤 Моя анкета» на приостановленном аккаунте и нажмите «Показать»: бот обязан отказать и предложить апелляцию.

## 4. Работа администратора

- [ ] С C отправьте `/admin` → «📋 Жалобы». Проверьте, что видны причина, детали и данные анкеты.
- [ ] Нажмите «⏸ Приостановить и скрыть»: пользователь получает сообщение с предложением апелляции.
- [ ] Вернитесь в `/admin` → «⚖️ Апелляции» после её создания.
- [ ] Нажмите «💬 Ответить», отправьте текст. Пользователь должен получить ответ администрации.
- [ ] Нажмите «✅ Восстановить». Пользователь должен снова иметь возможность включить видимость анкеты.
- [ ] Отдельно проверьте «🚫 Забанить»: этот Telegram-аккаунт больше не сможет пользоваться ботом даже после `/start`.

## 5. Анонимные признания

- [ ] С A откройте «💌 Признание», укажите `@username` B или числовой Telegram ID зарегистрированного B.
- [ ] Введите текст, убедитесь, что есть экран подтверждения, и нажмите «Отправить».
- [ ] B получает текст без имени отправителя.
- [ ] Повторите, указав username человека, который ещё не запускал бота: A получает ссылку-приглашение для передачи этому человеку.

## 6. Финальная проверка

- [ ] Выполните `docker compose logs -f bot` и убедитесь, что нет `Traceback`, `Unauthorized` или ошибок базы данных.
- [ ] Перезапустите: `docker compose down`, затем `docker compose up -d`. Созданные анкеты должны сохраниться.

Если какой-либо пункт не проходит, сохраните вывод `docker compose logs bot --tail=200` и приложите его вместе с номером пункта из этого списка.
````

## File: data/locales/ro.json
````json
{
  "welcome": "Bun venit! Creează un profil sau găsește o potrivire.",
  "profile_created": "✅ Profilul a fost salvat.",
  "profile_preview": "Previzualizare profil",
  "publish": "Publică",
  "edit": "Editează",
  "back": "Înapoi",
  "cancel": "Anulare",
  "photo_required": "Este necesară o fotografie.",
  "photo_limit": "Poți încărca până la 3 fotografii.",
  "profile_paused": "Profilul este în pauză.",
  "profile_deleted": "Profilul a fost șters.",
  "profile_updated": "Profilul a fost actualizat.",
  "profile_visibility_changed": "Vizibilitatea a fost schimbată",
  "profile_not_found": "Profilul nu a fost găsit.",
  "registration_step_gender": "Sexul tău?",
  "registration_step_target_gender": "Ce cauți?",
  "registration_step_name": "Cum te cheamă? (2–32 de caractere)",
  "registration_step_age": "Vârsta ta (16–99)?",
  "registration_step_district": "Zona ta?",
  "registration_step_institution": "Unde studiezi/lucrezi? (3–64 de caractere)",
  "registration_step_interests": "Interese, separate prin virgulă",
  "registration_step_bio": "Spune-ne despre tine (10–500 de caractere)",
  "registration_step_photo": "Trimite fotografii. Poți încărca până la 3.",
  "registration_step_preview": "Așa va arăta profilul tău.",
  "registration_step_confirm": "Confirmă publicarea profilului.",
  "menu_dating": "💘 Cunoașteri",
  "menu_likes": "💕 Simpatiile mele",
  "menu_profile": "👤 Profilul meu",
  "menu_verification": "🛡 Verificare",
  "menu_confession": "💌 Mărturisire",
  "menu_appeal": "🆘 Contestație",
  "menu_help": "❓ Ajutor",
  "profile_hidden": "🚫 Profil ascuns",
  "profile_hide": "🙈 Ascunde",
  "profile_show": "👀 Arată",
  "profile_edit": "✏️ Editează",
  "profile_photos": "📷 Fotografii",
  "confessions_on": "💌 Mărturisiri: Pornite",
  "confessions_off": "💌 Mărturisiri: Oprite",
  "profile_pause": "⏸ Pauză",
  "profile_delete": "🗑 Șterge",
  "language_button": "🌐 Язык / Limba",
  "language_saved": "✅ Limba interfeței a fost schimbată.",
  "legal_notice": "👋 MeAnima este un serviciu de întâlniri în format Telegram bot.\n\nAceasta este o versiune alfa închisă: unele funcții sunt încă dezvoltate, iar unele procese abia pornesc.\n\nÎnainte de utilizare, citește regulile, politica de confidențialitate și condițiile serviciului.\n\nFolosim MeAnima pentru a ne cunoaște și a comunica într-un mediu sigur, în cadrul testării închise.",
  "promo_empty_title": "Totul este în regulă",
  "promo_empty_text": "Nu mai sunt profiluri potrivite în apropiere. Încearcă mai târziu sau reîmprospătează căutarea.",
  "promo_refresh": "🔄 Reîmprospătează lista",
  "notification_confession": "💌 Ai primit o mărturisire anonimă:\n\n{confession}",
  "validation_name_required": "Numele este obligatoriu.",
  "validation_name_length": "Numele trebuie să aibă între 2 și 32 de caractere.",
  "validation_name_characters": "Numele conține caractere nepermise.",
  "validation_name_blocked": "Numele conține cuvinte interzise.",
  "validation_age_required": "Vârsta este obligatorie.",
  "validation_age_number": "Vârsta trebuie să fie un număr.",
  "validation_age_range": "Vârsta trebuie să fie între 16 și 99 de ani.",
  "validation_district_required": "Zona este obligatorie.",
  "validation_district_length": "Numele zonei este prea lung.",
  "validation_institution_required": "Instituția de învățământ este obligatorie.",
  "validation_institution_length": "Numele instituției este prea lung.",
  "validation_gender_required": "Sexul este obligatoriu.",
  "validation_target_gender": "Preferința de căutare este invalidă.",
  "validation_bio_required": "Descrierea este obligatorie.",
  "validation_bio_length": "Descrierea trebuie să aibă între 10 și 500 de caractere.",
  "validation_photos_required": "Trebuie încărcată cel puțin o fotografie.",
  "validation_photos_limit": "Poți încărca cel mult trei fotografii.",
  "dating_like": "❤️ Îmi place",
  "dating_comment": "💌 Scrie",
  "dating_skip": "⏭️ Omite",
  "dating_report": "🚩 Raportează",
  "dating_block": "🚫 Blochează",
  "report_fake": "Profil fals",
  "report_insult": "Insulte",
  "report_inappropriate": "Conținut nepotrivit",
  "report_nsfw": "Conținut 18+",
  "report_spam": "Spam",
  "report_other": "Altele",
  "notification_like": "💌 Cineva a apreciat profilul tău.",
  "notification_like_comment": "💌 Cineva a apreciat profilul tău.\n\n{comment}",
  "notification_match": "🎉 <b>Ai o simpatie reciprocă cu {name}!</b>\n\nSe pare că vă plăceți! ✨ Fă primul pas și scrie chiar acum.\n\n💬 <b>Contact:</b> {contact}\n\nVă dorim o conversație plăcută și caldă! 💫",
  "help_text": "❓ <b>Ajutor</b>\nIntră la «👤 Profilul meu» pentru a crea sau edita profilul, apoi deschide «💘 Cunoașteri» pentru a căuta persoane.\n\nMărturisirile sunt trimise anonim.\n\n📚 <b>Documentele MeAnima</b>",
  "help_support_prompt": "Dacă ai nevoie de ajutor, scrie unuia dintre administratori:",
  "help_support_unconfigured": "Serviciul de suport nu este configurat.",
  "help_report_problem": "🐛 Raportează o problemă",
  "profile_verified": "🟢 Verificat",
  "profile_unverified": "⚪ Neverificat",
  "profile_moderation_hidden": "⏳ Profilul este ascuns până la decizia moderatorului sau înlocuirea fotografiei.",
  "verification_retry": "🔄 Repetă verificarea",
  "verification_home": "🏠 Meniul principal",
  "verification_retry_prompt": "🛡 Verificare repetată\nTrimite un scurt mesaj video pentru reverificarea de către moderatori.",
  "verification_profile_required": "📝 Pentru verificare trebuie mai întâi să creezi un profil.",
  "verification_create_profile": "✨ Creează profilul",
  "verification_verified": "✅ <b>Profilul tău este deja verificat</b>\n\nProfilul are statut confirmat (bifă verde). Nu este necesară o nouă verificare acum.",
  "verification_pending": "⏳ <b>Cererea ta este deja în examinare</b>\n\nModeratorii verifică mesajul video trimis. Te rugăm să aștepți decizia.",
  "verification_start": "🛡 Verificare\nTrimite un scurt mesaj video — moderatorii îl vor vedea doar pentru verificare.",
  "verification_submitted": "✅ Mesajul video a fost trimis pentru verificare. Statutul profilului este încă neverificat.",
  "verification_video_required": "⚠️ Trebuie să trimiți un mesaj video.",
  "verification_error_generic": "⚠️ Mesajul video nu a putut fi trimis. Verifică statutul profilului și încearcă din nou.",
  "returned_to_menu": "Ai revenit la meniul principal.",
  "registration_cancelled": "❌ Înregistrarea a fost anulată. Poți începe din nou oricând din «👤 Profilul meu»."
}
````

## File: data/locales/ru.json
````json
{
  "welcome": "Добро пожаловать! Создайте анкету или найдите симпатию.",
  "profile_created": "✅ Анкета сохранена.",
  "profile_preview": "Предпросмотр анкеты",
  "publish": "Опубликовать",
  "edit": "Изменить",
  "back": "Назад",
  "cancel": "Отмена",
  "photo_required": "Нужна фотография.",
  "photo_limit": "Можно загрузить до 3 фотографий.",
  "profile_paused": "Анкета на паузе.",
  "profile_deleted": "Анкета удалена.",
  "profile_updated": "Анкета обновлена.",
  "profile_visibility_changed": "Видимость изменена",
  "profile_not_found": "Анкета не найдена.",
  "registration_step_gender": "Ваш пол?",
  "registration_step_target_gender": "Кого ищете?",
  "registration_step_name": "Как вас зовут? (2–32 символа)",
  "registration_step_age": "Ваш возраст (16–99)?",
  "registration_step_district": "Ваш район?",
  "registration_step_institution": "Где учитесь/работаете? (3–64 символа)",
  "registration_step_interests": "Интересы через запятую",
  "registration_step_bio": "Расскажите о себе (10–500 символов)",
  "registration_step_photo": "Отправьте фото. Можно до 3 фотографий.",
  "registration_step_preview": "Вот как будет выглядеть ваша анкета.",
  "registration_step_confirm": "Подтвердите публикацию анкеты.",
  "menu_dating": "💘 Знакомства",
  "menu_likes": "💕 Мои симпатии",
  "menu_profile": "👤 Моя анкета",
  "menu_verification": "🛡 Верификация",
  "menu_confession": "💌 Признание",
  "menu_appeal": "🆘 Апелляция",
  "menu_help": "❓ Помощь",
  "profile_hidden": "🚫 Анкета скрыта",
  "profile_hide": "🙈 Скрыть",
  "profile_show": "👀 Показать",
  "profile_edit": "✏️ Редактировать",
  "profile_photos": "📷 Фотографии",
  "confessions_on": "💌 Признания: Вкл",
  "confessions_off": "💌 Признания: Выкл",
  "profile_pause": "⏸ Пауза",
  "profile_delete": "🗑 Удалить",
  "language_button": "🌐 Язык / Limba",
  "language_saved": "✅ Язык интерфейса изменён.",
  "legal_notice": "👋 MeAnima — это сервис знакомств в формате Telegram-бота.\n\nЭто закрытая альфа: часть функциональности ещё дорабатывается, а часть процессов только запускается.\n\nПеред использованием важно ознакомиться с правилами, политикой конфиденциальности и условиями сервиса.\n\nМы используем MeAnima, чтобы знакомиться и общаться в безопасной среде в рамках закрытого тестирования.",
  "promo_empty_title": "Пока всё в порядке",
  "promo_empty_text": "Сейчас рядом больше не осталось подходящих анкет. Попробуйте позже или обновите поиск.",
  "promo_refresh": "🔄 Обновить выдачу",
  "notification_confession": "💌 Вам анонимное признание:\n\n{confession}",
  "validation_name_required": "Имя обязательно.",
  "validation_name_length": "Имя должно быть от 2 до 32 символов.",
  "validation_name_characters": "Имя содержит недопустимые символы.",
  "validation_name_blocked": "Имя содержит запрещённые слова.",
  "validation_age_required": "Возраст обязателен.",
  "validation_age_number": "Возраст должен быть числом.",
  "validation_age_range": "Возраст должен быть от 16 до 99 лет.",
  "validation_district_required": "Район обязателен.",
  "validation_district_length": "Район слишком длинный.",
  "validation_institution_required": "Учебное заведение обязательно.",
  "validation_institution_length": "Название учреждения слишком длинное.",
  "validation_gender_required": "Пол обязателен.",
  "validation_target_gender": "Цель поиска указана неверно.",
  "validation_bio_required": "Описание обязательно.",
  "validation_bio_length": "Описание должно быть от 10 до 500 символов.",
  "validation_photos_required": "Нужно загрузить хотя бы одну фотографию.",
  "validation_photos_limit": "Можно загрузить не больше трёх фотографий.",
  "dating_like": "❤️ Нравится",
  "dating_comment": "💌 Написать",
  "dating_skip": "⏭️ Пропустить",
  "dating_report": "🚩 Пожаловаться",
  "dating_block": "🚫 Заблокировать",
  "report_fake": "Фейк",
  "report_insult": "Оскорбления",
  "report_inappropriate": "Неприемлемый контент",
  "report_nsfw": "18+ контент",
  "report_spam": "Спам",
  "report_other": "Другое",
  "notification_like": "💌 Кому-то понравилась ваша анкета.",
  "notification_like_comment": "💌 Кому-то понравилась ваша анкета.\n\n{comment}",
  "notification_match": "🎉 <b>У вас взаимная симпатия с {name}!</b>\n\nКажется, вы понравились друг другу! ✨ Не стесняйтесь сделать первый шаг и написать прямо сейчас.\n\n💬 <b>Контакт для связи:</b> {contact}\n\nЖелаем вам приятного и тёплого общения! 💫",
  "help_text": "❓ <b>Помощь</b>\nПереходите в «👤 Моя анкета» для создания или редактирования анкеты, а затем откройте «💘 Знакомства» для поиска.\n\nПризнания отправляются анонимно.\n\n📚 <b>Документы MeAnima</b>",
  "help_support_prompt": "Если нужна помощь, напишите одному из администраторов:",
  "help_support_unconfigured": "Служба поддержки не настроена.",
  "help_report_problem": "🐛 Сообщить о проблеме",
  "profile_verified": "🟢 Проверенный",
  "profile_unverified": "⚪ Непроверенный",
  "profile_moderation_hidden": "⏳ Анкета скрыта до решения модератора или замены фотографии.",
  "verification_retry": "🔄 Повторить проверку",
  "verification_home": "🏠 Главное меню",
  "verification_retry_prompt": "🛡 Повторная верификация\nОтправьте короткое видеосообщение-кружок для повторной проверки модераторами.",
  "verification_profile_required": "📝 Для прохождения верификации сначала необходимо создать анкету.",
  "verification_create_profile": "✨ Создать анкету",
  "verification_verified": "✅ <b>Вы уже верифицированы</b>\n\nВаша анкета имеет подтвержденный статус (зеленая галочка). Повторная проверка сейчас не требуется.",
  "verification_pending": "⏳ <b>Ваша заявка уже на рассмотрении</b>\n\nМодераторы проверяют отправленный видеокружок. Пожалуйста, ожидайте решения.",
  "verification_start": "🛡 Верификация\nОтправьте короткое видеосообщение-кружок — модераторы увидят его только для проверки.",
  "verification_submitted": "✅ Видеокружок отправлен на проверку. Статус анкеты пока: непроверенный.",
  "verification_video_required": "⚠️ Нужно отправить именно видеосообщение-кружок.",
  "verification_error_generic": "⚠️ Не удалось отправить видеокружок. Проверьте статус анкеты и попробуйте ещё раз.",
  "returned_to_menu": "Вы вернулись в главное меню.",
  "registration_cancelled": "❌ Регистрация отменена. Вы можете начать заново в любой момент через «👤 Моя анкета»."
}
````

## File: database/migrations/versions/20260829_high_workflow_invariants.py
````python
"""Add report evidence and active-workflow uniqueness invariants.

Revision ID: 20260829_workflow_invariants
Revises: 20260828_report_assigned
Create Date: 2026-08-29
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

revision = "20260829_workflow_invariants"
down_revision = "20260828_report_assigned"
branch_labels = None
depends_on = None


def _fail_if_active_duplicates(bind, table: str, group_sql: str, where_sql: str) -> None:
    count = bind.execute(
        sa.text(
            f"SELECT count(*) FROM (SELECT {group_sql} FROM {table} "
            f"WHERE {where_sql} GROUP BY {group_sql} HAVING count(*) > 1) duplicates"
        )
    ).scalar_one()
    if count:
        raise RuntimeError(
            f"{table} contains {count} active duplicate group(s); resolve them manually before applying this migration."
        )


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    report_columns = {column["name"] for column in inspector.get_columns("reports")}
    if "evidence_snapshot" not in report_columns:
        op.add_column("reports", sa.Column("evidence_snapshot", sa.JSON(), nullable=True))

    _fail_if_active_duplicates(bind, "appeals", "user_id", "status = 'PENDING'")
    _fail_if_active_duplicates(bind, "verification_requests", "user_id", "status = 'PENDING'")
    _fail_if_active_duplicates(
        bind,
        "moderation_cases",
        "user_id, case_type, COALESCE(source_id, '')",
        "status IN ('PENDING', 'IN_PROGRESS')",
    )

    indexes = {index["name"] for index in inspector.get_indexes("appeals")}
    if "uq_appeals_one_pending_per_user" not in indexes:
        op.create_index(
            "uq_appeals_one_pending_per_user",
            "appeals",
            ["user_id"],
            unique=True,
            postgresql_where=sa.text("status = 'PENDING'"),
        )

    indexes = {index["name"] for index in inspector.get_indexes("verification_requests")}
    if "uq_verification_requests_one_pending_per_user" not in indexes:
        op.create_index(
            "uq_verification_requests_one_pending_per_user",
            "verification_requests",
            ["user_id"],
            unique=True,
            postgresql_where=sa.text("status = 'PENDING'"),
        )

    indexes = {index["name"] for index in inspector.get_indexes("moderation_cases")}
    if "uq_moderation_cases_one_active_event" not in indexes:
        op.execute(
            "CREATE UNIQUE INDEX uq_moderation_cases_one_active_event "
            "ON moderation_cases (user_id, case_type, COALESCE(source_id, '')) "
            "WHERE status IN ('PENDING', 'IN_PROGRESS')"
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    for table, index in (
        ("moderation_cases", "uq_moderation_cases_one_active_event"),
        ("verification_requests", "uq_verification_requests_one_pending_per_user"),
        ("appeals", "uq_appeals_one_pending_per_user"),
    ):
        if index in {item["name"] for item in inspector.get_indexes(table)}:
            op.drop_index(index, table_name=table)
    if "evidence_snapshot" in {column["name"] for column in inspector.get_columns("reports")}:
        op.drop_column("reports", "evidence_snapshot")
````

## File: docs/admin.md
````markdown
# Администрирование

## Доступ
Админ-панель доступна пользователям, чьи Telegram ID указаны в ADMIN_IDS.

## Возможности
- Trust-панель: очереди верификаций, жалоб, NSFW/лица и апелляций;
- Trust-статистика, список заблокированных и история решений;
- бан пользователя;
- скрытие и приостановка профиля;
- отклонение жалобы;
- просмотр апелляций;
- ответ администрации пользователю;
- рассылка активным пользователям.

Одобрение апелляции выполняется через `ModerationService`: проверяются RBAC и отсутствие
другой открытой санкции, затем appeal переводится в `APPROVED`, пользователь становится
`ACTIVE`, а профиль восстанавливается. Повторный callback не меняет уже закрытую апелляцию.

Выход кнопками «Назад» или «В меню» очищает admin FSM, поэтому следующий обычный текст
не может случайно стать текстом рассылки. Уведомления ведут непосредственно к очереди
соответствующего кейса.

## Реализация
- admin.py содержит обработчики для команд и inline-кнопок;
- AdminState хранит состояния для ответа на апелляцию и рассылки;
- NotificationService используется для отправки сообщений.

## Важные замечания
- Действия модерации влияют и на status пользователя, и на видимость профиля.
- Для пользователя после приостановки доступна апелляция через отдельный сценарий.
- Каждое решение Trust пишет `AdminLog`; повторная обработка уже закрытого объекта безопасно отклоняется.
````

## File: docs/architecture.md
````markdown
# Архитектура проекта

## Общая схема
Проект представляет собой Telegram-бота на aiogram 3 с асинхронной архитектурой.

Основные слои:
- handlers/ — маршруты и сценарии Telegram-интерфейса;
- services/ — бизнес-логика: профиль, независимые рекомендации, лайки, мэтчи, признания, уведомления;
- repositories/ — доступ к данным и базовые запросы;
- models/ — ORM-модели SQLAlchemy;
- middlewares/ — общие действия для всех событий: DB session, user sync, rate limit.

Порядок outer middleware в dispatcher:
`DbSessionMiddleware -> UserSyncMiddleware -> ProfileRequiredMiddleware -> RateLimitMiddleware`.
Заблокированные пользователи блокируются UserSyncMiddleware, кроме входа и отправки текста
в состоянии апелляции. ProfileRequiredMiddleware проверяет profile-only действия, но
`profile:create` и апелляция без профиля проходят к своим handlers.

Recommendation layer разделён на три контракта: `RecommendationStrategy` оценивает кандидата, `RecommendationQueue` управляет временной очередью, `RecommendationRepository` выполняет SQL-фильтры и записывает просмотры. `RecommendationService` координирует их, но не знает деталей будущей ML/Redis реализации.

Trust System использует те же слои: handlers вызывают независимые `VerificationService`, `ReportService`, `ModerationService`, `PhotoModerationService`, `TrustScoreService` и `TrustStatsService`; SQL и журнал аудита находятся в `TrustRepository`. Рейтинг доступен исключительно внутренним алгоритмам. Анкеты `UNDER_REVIEW` исключаются на уровне SQL в `RecommendationRepository`; при ошибке provider проверки фото анкета скрывается до ручного решения.

## Запуск
Точка входа — main.py. При запуске:
1. загружается конфигурация из .env;
2. создаётся фабрика сессий SQLAlchemy;
3. инициализируется Redis для FSM, rate limit, dedupe и recommendation queue;
4. создаётся dispatcher aiogram и подключаются роутеры.

Схема базы обновляется отдельной командой `alembic upgrade head`, а не во время
старта bot process.

## Ключевые сценарии
- Регистрация профиля и заполнение анкеты.
- Просмотр рекомендаций и взаимодействие с анкетами: лайк, комментарий, пропуск, блокировка, жалоба.
- Управление взаимными симпатиями и контактами.
- Анонимные признания и апелляции.
- Модерация жалоб и апелляций администраторами.
- Верификация видеокружком, очередь NSFW/лица и журнал решений Trust.

FSM registration/photo/verification/confession/appeal/admin broadcast используют Redis
storage с общим TTL `FSM_STATE_TTL_SECONDS`. Неожиданный текст без активного состояния
попадает в fallback и получает главное меню; старое состояние не восстанавливается.

## Сильные стороны текущей архитектуры
- Чёткое разделение на слои.
- Асинхронная работа с БД.
- Использование Redis для FSM и ограничения частоты.
- Наличие отдельной логики для администратора и бизнес-функций.
- Модуль регистрации и профиля теперь имеет отдельный сервис и валидатор, что снижает связность обработчиков.
- Независимые `LikeService` и `MatchService` с идемпотентными repository-операциями.
- Стратегия рекомендаций заменяема без изменения handler/UI-контрактов.
- Eligibility выдачи остаётся в SQL, а ранжирование — в стратегии; это не позволяет ML/AI обойти блоки, статусы и модерацию.

## Текущие ограничения и архитектурные риски
- UI-тексты не полностью вынесены в отдельный слой локализации.
- Часть логики всё ещё находится в обработчиках, особенно в сценариях FSM.
- Recommendation queue хранится в Redis по ключу `recommendation_queue:<user_id>`. Очередь пересоздаётся при отсутствии записи, изменяется при skip/like/block и очищается при remove/clear. Для неё намеренно не установлен TTL: это disposable состояние, а rebuild является источником восстановления.
- Проверка фото выбирается конфигурацией через `PhotoSafetyProvider`: локальный ONNX/OpenCV ML-провайдер, development heuristic или явный disabled. В ML-режиме изображение нормализуется и хэшируется до inference, поэтому повторная проверка не запускает модель; ошибка любой стадии fail-closed отправляет анкету в ручную модерацию.
- Для горизонтального масштабирования используется Redis-адаптер для очередей рекомендаций.
- Обёртка savepoint защищает конкурентные Like/Match, но полноценное управление транзакциями и retry-политика ещё не выделены в отдельный слой.
- Текущий контракт ранжирования по одному кандидату не оптимален для внешних/batch ML-моделей.

## Рекомендации по поддержке
- Не добавлять новую бизнес-логику напрямую в handlers без предварительного анализа места в services/.
- При изменении контракта профиля обновлять ProfileService, DTO и validator вместе.
- При изменении схемы БД добавлять полноценные Alembic-миграции.
- Новые алгоритмы подключать через `RecommendationStrategy`, не добавляя условные ветки в `RecommendationService`.
- Не считать Memory queue источником истины: все eligibility-проверки должны оставаться в repository/DB.
- Moderation notifications используют case-specific callbacks `mycase:report:*`, `mycase:case:*`, `mycase:verify:*` и `mycase:appeal:*`; ownership и RBAC повторно проверяются в admin handlers.
- Перед релизом запускать `pytest -q`, `ruff check .`, а integration tests — с `INTEGRATION=1` и доступными PostgreSQL/Redis.
````

## File: docs/registration.md
````markdown
# Регистрация и профиль

## Сценарий
Пользователь запускает бот, проходит FSM-диалог регистрации и создаёт анкету.

## Состояния FSM
- RegistrationState.gender
- RegistrationState.target_gender
- RegistrationState.name
- RegistrationState.age
- RegistrationState.district
- RegistrationState.institution
- RegistrationState.interests
- RegistrationState.bio
- RegistrationState.photo
- RegistrationState.preview

## Что происходит
1. Пользователь получает вопрос о поле.
2. Выбирает кого ищет.
3. Заполняет базовые данные профиля.
4. Передаёт фото.
5. На этапе предпросмотра подтверждает публикацию.
6. Анкета сохраняется в базе как Profile.

## Текущие особенности
- Для сохранения используется ProfileService, а не прямой доступ из handler.
- Валидация перенесена в отдельный модуль validator.
- DTO ProfileDraft используется для передачи данных между handler и сервисом.
- После сохранения анкета становится доступной для рекомендаций и профиля.
- При редактировании анкеты сценарий запускается заново, но используется тот же FSM-скелет.

## Важные замечания
- Валидация ключевых полей выполняется до сохранения.
- На этапе публикации обработчик показывает пользователю ошибки валидации, а не просто падает.
- Фото принимается как Telegram-photo и после сохранения проверяется PhotoModerationService;
	NSFW, отсутствие лица или ошибка провайдера скрывают профиль и создают moderation case.
- Важно не менять callback data и структуру FSM без обновления связанных обработчиков.
````

## File: handlers/__init__.py
````python
from handlers import (
    admin,
    appeals,
    callback_fallback,
    common,
    confessions,
    dating,
    likes,
    profile,
    registration,
    verification,
)

routers = (
    common.router,
    registration.router,
    profile.router,
    verification.router,
    dating.router,
    likes.router,
    confessions.router,
    appeals.router,
    admin.router,
    callback_fallback.router,
)
````

## File: handlers/confessions.py
````python
from uuid import uuid4

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from keyboards.menu import MENU_CONFESSION_LABELS, MENU_LABELS, main_menu
from services.confession_service import ConfessionService
from services.eligibility import EligibilityError, EligibilityService
from services.localization import LocalizationService
from services.notification_service import NotificationService
from states.confession import ConfessionState
from utils.text import escape_html

router = Router()


@router.message(
    StateFilter(ConfessionState),
    F.text.in_(MENU_LABELS),
)
async def handle_menu_buttons_during_confession(
    message: Message, state: FSMContext, locale: str = "ru"
) -> None:
    await state.clear()
    await message.answer(LocalizationService().get("returned_to_menu", locale), reply_markup=main_menu(locale))

@router.message(F.text.in_(MENU_CONFESSION_LABELS))
async def begin(message: Message, state: FSMContext, session: AsyncSession) -> None:
    # This source-only guard covers the first step; send() repeats it for a
    # stale FSM state after a later freeze.
    try:
        await EligibilityService(session).ensure_source_allowed(message.from_user.id, action="отправлять признания")
    except EligibilityError as error:
        await message.answer(str(error))
        return
    await state.set_state(ConfessionState.recipient)
    await message.answer(
        "💌 Анонимное признание\nКому отправить? Введите @username получателя или его числовой Telegram ID.",
        reply_markup=InlineKeyboardBuilder().button(text="❌ Отмена", callback_data="confession:cancel").as_markup()
    )

@router.message(ConfessionState.recipient)
async def recipient(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    valid_username = value.startswith("@") and 3 <= len(value) <= 33
    valid_id = value.isdigit() and 4 <= len(value) <= 20
    if not (valid_username or valid_id):
        await message.answer("⚠️ Введите корректный @username или числовой Telegram ID.")
        return
    await state.update_data(recipient=value)
    await state.set_state(ConfessionState.text)
    await message.answer("✍️ Напишите текст признания (5–1000 символов).")

@router.message(ConfessionState.text)
async def confirmation(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not 5 <= len(text) <= 1000:
        await message.answer("⚠️ Текст должен быть от 5 до 1000 символов.")
        return
    await state.update_data(text=text)
    await state.update_data(submission_key=uuid4().hex)
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Отправить", callback_data="confession:send")
    kb.button(text="❌ Отмена", callback_data="confession:cancel")
    kb.adjust(2)
    await state.set_state(ConfessionState.confirm)
    await message.answer(
        "📩 Проверьте сообщение. Отправитель останется анонимным:\n\n" + escape_html(text),
        reply_markup=kb.as_markup(),
    )

@router.callback_query(F.data == "confession:cancel")
async def cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("❌ Отправка признания отменена.")
    await callback.answer()

@router.callback_query(ConfessionState.confirm, F.data == "confession:send")
async def send(callback: CallbackQuery, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    try:
        await EligibilityService(session).ensure_source_allowed(callback.from_user.id, action="отправлять признания")
    except EligibilityError as error:
        await state.clear()
        await callback.answer(str(error), show_alert=True)
        return
    data = await state.get_data()
    recipient, text = data["recipient"], data["text"]
    try:
        confession = await ConfessionService(
            session,
            settings.daily_secret_salt,
            daily_limit=settings.confession_daily_limit,
            pending_ttl_hours=settings.confession_pending_ttl_hours,
        ).create(callback.from_user.id, recipient, text, submission_key=data.get("submission_key"))
    except ValueError as error:
        await state.clear()
        await callback.message.edit_text(str(error))
        await callback.answer()
        return
    if confession.recipient_id:
        delivered = await NotificationService(callback.bot).safe_send_localized(
            confession.recipient_id, session, "notification_confession", confession=escape_html(text)
        )
        await callback.message.edit_text(
            "✅ Признание доставлено анонимно."
            if delivered
            else "✅ Признание сохранено, но Telegram временно не подтвердил доставку."
        )
    else:
        link = f"https://t.me/{(await callback.bot.get_me()).username}?start=confession_{confession.id}"
        await callback.message.edit_text(
            f"📎 Получатель ещё не запускал бота. Передайте ему ссылку:\n{link}"
        )
    await state.clear()
    await callback.answer()
````

## File: keyboards/admin.py
````python
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_keyboard(role_can_manage_admins: bool = False):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛡 Модерация", callback_data="admin:section:moderation")
    kb.button(text="👤 Пользователи", callback_data="admin:section:users")
    kb.button(text="📊 Статистика", callback_data="admin:section:stats")
    kb.button(text="👤 Просмотр анкет", callback_data="admin:browse")
    if role_can_manage_admins:
        kb.button(text="⚙️ Администрирование", callback_data="admin:section:administration")
    kb.adjust(1)
    return kb.as_markup()


def admin_moderation_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="📢 Жалобы", callback_data="admin:reports")
    kb.button(text="🖼️ Фото на проверку", callback_data="admin:nsfw")
    kb.button(text="🛡 Верификация", callback_data="admin:verifications")
    kb.button(text="⚖️ Апелляции", callback_data="admin:appeals")
    kb.button(text="📌 Мои кейсы", callback_data="admin:my_cases")
    kb.button(text="⬅️ Назад", callback_data="admin:menu")
    kb.adjust(1)
    return kb.as_markup()


def admin_users_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="🔎 Просмотр анкет", callback_data="admin:browse")
    kb.button(text="🚫 Заблокированные", callback_data="admin:blocked")
    kb.button(text="⬅️ Назад", callback_data="admin:menu")
    kb.adjust(1)
    return kb.as_markup()


def admin_stats_keyboard(can_view_history: bool = True):
    kb = InlineKeyboardBuilder()
    kb.button(text="📊 Общая статистика", callback_data="admin:trust_stats")
    if can_view_history:
        kb.button(text="📜 История решений", callback_data="admin:trust_history")
    kb.button(text="⬅️ Назад", callback_data="admin:menu")
    kb.adjust(1)
    return kb.as_markup()


def admin_administration_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="📣 Рассылка", callback_data="admin:broadcast")
    kb.button(text="⬅️ Назад", callback_data="admin:menu")
    kb.adjust(1)
    return kb.as_markup()


def admin_nav_keyboard(
    next_callback: str | None = None,
    back_callback: str = "admin:menu",
    refresh_callback: str | None = None,
    prev_callback: str | None = None,
):
    kb = InlineKeyboardBuilder()
    if refresh_callback:
        kb.button(text="🔄 Обновить", callback_data=refresh_callback)
    if prev_callback:
        kb.button(text="⬅️ Предыдущий", callback_data=prev_callback)
    if next_callback:
        kb.button(text="➡️ Следующий", callback_data=next_callback)
    kb.button(text="⬅️ Назад", callback_data=back_callback)
    kb.button(text="🏠 Главное меню", callback_data="admin:menu")
    kb.adjust(2 if refresh_callback or next_callback or prev_callback else 1)
    return kb.as_markup()


def browse_nav_keyboard(current_user_id: int | None = None):
    next_callback = "admin:browse:next" if current_user_id is None else f"admin:browse:next:{current_user_id}"
    return admin_nav_keyboard(
        next_callback=next_callback,
        back_callback="admin:section:users",
        refresh_callback="admin:browse",
    )


def verification_keyboard(request_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="🙋 Взять заявку", callback_data=f"verify:claim:{request_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def verification_decision_keyboard(request_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Подтвердить", callback_data=f"verify:approve:{request_id}")
    kb.button(text="🔁 Запросить повтор", callback_data=f"verify:retake:{request_id}")
    kb.button(text="❌ Отклонить", callback_data=f"verify:reject:{request_id}")
    kb.button(text="↩️ Освободить", callback_data=f"verify:release:{request_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def case_keyboard(case_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="🙋 Взять кейс", callback_data=f"case:claim:{case_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def case_decision_keyboard(case_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Одобрить фото", callback_data=f"case:restore:{case_id}")
    kb.button(text="✍️ Запросить замену", callback_data=f"case:retake:{case_id}")
    kb.button(text="❌ Отклонить кейс", callback_data=f"case:reject:{case_id}")
    kb.button(text="↩️ Освободить", callback_data=f"case:release:{case_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def moderation_keyboard(report_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="🙋 Взять жалобу", callback_data=f"moderate:claim:{report_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def moderation_decision_keyboard(report_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="🚫 Заблокировать пользователя", callback_data=f"moderate:prompt:ban:{report_id}")
    kb.button(text="⏸ Скрыть анкету", callback_data=f"moderate:prompt:hide:{report_id}")
    kb.button(text="✅ Отклонить жалобу", callback_data=f"moderate:prompt:dismiss:{report_id}")
    kb.button(text="↩️ Освободить", callback_data=f"moderate:release:{report_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def appeal_keyboard(appeal_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="🙋 Взять апелляцию", callback_data=f"appeal:claim:{appeal_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def appeal_decision_keyboard(appeal_id: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="💬 Написать пользователю", callback_data=f"appeal:reply:{appeal_id}")
    kb.button(text="✅ Одобрить апелляцию", callback_data=f"appeal:prompt:restore:{appeal_id}")
    kb.button(text="❌ Отклонить апелляцию", callback_data=f"appeal:prompt:reject:{appeal_id}")
    kb.button(text="↩️ Освободить", callback_data=f"appeal:release:{appeal_id}")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.adjust(1)
    return kb.as_markup()


def profile_moderation_keyboard(
    user_id: int,
    next_callback: str | None = None,
    can_unban: bool = False,
    is_banned: bool = False,
    is_frozen: bool = False,
):
    kb = InlineKeyboardBuilder()
    if next_callback:
        kb.button(text="➡️ Следующая", callback_data=next_callback)

    if is_banned:
        if can_unban:
            kb.button(text="✅ Разблокировать", callback_data=f"profilemod:prompt:unban:{user_id}")
    else:
        kb.button(text="🚫 Заблокировать", callback_data=f"profilemod:prompt:ban:{user_id}")

        if is_frozen:
            if can_unban:
                kb.button(text="▶️ Разморозить", callback_data=f"profilemod:prompt:unfreeze:{user_id}")
        else:
            kb.button(text="⏸ Заморозить", callback_data=f"profilemod:prompt:freeze:{user_id}")

    kb.button(text="⬅️ Назад", callback_data="admin:section:users")
    kb.button(text="🏠 В меню", callback_data="admin:menu")
    kb.adjust(2)
    return kb.as_markup()


def confirm_action_keyboard(confirm_data: str, back_data: str = "admin:menu"):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Подтвердить", callback_data=confirm_data)
    kb.button(text="❌ Отмена", callback_data=back_data)
    kb.adjust(2)
    return kb.as_markup()


def my_cases_keyboard(items: list[tuple[str, str]] | None = None):
    kb = InlineKeyboardBuilder()
    if items:
        for title, callback_data in items:
            kb.button(text=title, callback_data=callback_data)
    kb.button(text="🔄 Обновить", callback_data="admin:my_cases")
    kb.button(text="⬅️ Назад", callback_data="admin:section:moderation")
    kb.button(text="🏠 Главное меню", callback_data="admin:menu")
    kb.adjust(1)
    return kb.as_markup()
````

## File: keyboards/dating.py
````python
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.localization import LocalizationService


def dating_keyboard(user_id: int, locale: str = "ru"):
    localizer = LocalizationService()
    kb = InlineKeyboardBuilder()
    kb.button(text=localizer.get("dating_like", locale), callback_data=f"like:{user_id}")
    kb.button(text=localizer.get("dating_comment", locale), callback_data=f"comment:{user_id}")
    kb.button(text=localizer.get("dating_skip", locale), callback_data=f"skip:{user_id}")
    kb.button(text=localizer.get("dating_report", locale), callback_data=f"report:{user_id}")
    kb.button(text=localizer.get("dating_block", locale), callback_data=f"block:{user_id}")
    kb.adjust(2, 2, 1)
    return kb.as_markup()

def choice_keyboard(prefix: str, values: list[tuple[str, str]]):
    kb = InlineKeyboardBuilder()
    for text, value in values:
        kb.button(text=text, callback_data=f"{prefix}:{value}")
    kb.adjust(2)
    return kb.as_markup()

def report_reasons_keyboard(user_id: int, locale: str = "ru"):
    localizer = LocalizationService()
    kb = InlineKeyboardBuilder()
    for code, key in [
        ("FAKE", "report_fake"),
        ("INSULT", "report_insult"),
        ("INAPPROPRIATE_CONTENT", "report_inappropriate"),
        ("NSFW", "report_nsfw"),
        ("SPAM", "report_spam"),
        ("OTHER", "report_other"),
    ]:
        kb.button(text=localizer.get(key, locale), callback_data=f"report_reason:{user_id}:{code}")
    kb.adjust(1)
    return kb.as_markup()
````

## File: keyboards/menu.py
````python
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from services.localization import LocalizationService

_localizer = LocalizationService()
MENU_LABEL_KEYS = (
    "menu_dating", "menu_likes", "menu_profile", "menu_verification",
    "menu_confession", "menu_appeal", "menu_help",
)
MENU_LABELS = frozenset(_localizer.get(key, locale) for locale in ("ru", "ro") for key in MENU_LABEL_KEYS)
MENU_HELP_LABELS = frozenset(_localizer.get("menu_help", locale) for locale in ("ru", "ro"))
MENU_DATING_LABELS = frozenset(_localizer.get("menu_dating", locale) for locale in ("ru", "ro"))
MENU_PROFILE_LABELS = frozenset(_localizer.get("menu_profile", locale) for locale in ("ru", "ro"))
MENU_CONFESSION_LABELS = frozenset(_localizer.get("menu_confession", locale) for locale in ("ru", "ro"))
MENU_VERIFICATION_LABELS = frozenset(_localizer.get("menu_verification", locale) for locale in ("ru", "ro"))


def main_menu(locale: str = "ru") -> ReplyKeyboardMarkup:
    text = LocalizationService().get
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text("menu_dating", locale)), KeyboardButton(text=text("menu_likes", locale))],
            [KeyboardButton(text=text("menu_profile", locale)), KeyboardButton(text=text("menu_verification", locale))],
            [KeyboardButton(text=text("menu_confession", locale)), KeyboardButton(text=text("menu_appeal", locale))],
            [KeyboardButton(text=text("menu_help", locale))],
        ],
        resize_keyboard=True,
    )
````

## File: middlewares/rate_limit.py
````python
import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from redis.asyncio import Redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self._fallback_last_seen: dict[int, float] = {}

    async def __call__(
        self, handler: Callable[..., Awaitable[Any]], event: TelegramObject, data: dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)
        key = f"rate:{user.id}"
        try:
            allowed = await self.redis.set(key, "1", ex=1, nx=True)
        except RedisError as error:
            # Keep a small local emergency limit while Redis is unavailable.
            # This preserves basic availability without leaving every process open to bursts.
            now = time.monotonic()
            last_seen = self._fallback_last_seen.get(user.id)
            if last_seen is not None and now - last_seen < 1:
                return None
            self._fallback_last_seen[user.id] = now
            logger.warning("Rate limiter unavailable; using local fallback: %s", error)
            return await handler(event, data)
        if allowed:
            return await handler(event, data)
        return None
````

## File: middlewares/user.py
````python
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from models import UserStatus
from repositories.user import UserRepository
from states.appeal import AppealState


class UserSyncMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[..., Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        session = data.get("session")
        if user and session:
            db_user = await UserRepository(session).get_or_create(user.id, user.username)
            if db_user.status == UserStatus.BANNED:
                state = data.get("state")
                current_state = await state.get_state() if state is not None else None
                appeal_allowed = isinstance(event, Message) and (
                    (event.text or "") == "🆘 Апелляция" or current_state == AppealState.enter_text.state
                )
                if appeal_allowed:
                    data["current_user"] = db_user
                    return await handler(event, data)
                if isinstance(event, CallbackQuery):
                    await event.answer("🚫 Ваш аккаунт заблокирован. Доступ к боту ограничен.", show_alert=True)
                elif isinstance(event, Message):
                    await event.answer("🚫 Ваш аккаунт заблокирован. Доступ к боту ограничен.")
                return None
            data["current_user"] = db_user
        return await handler(event, data)
````

## File: models/appeal.py
````python
import enum
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class AppealStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Appeal(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "appeals"
    __table_args__ = (
        Index(
            "uq_appeals_one_pending_per_user",
            "user_id",
            unique=True,
            postgresql_where="status = 'PENDING'",
        ),
    )

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    text: Mapped[str] = mapped_column(Text)
    status: Mapped[AppealStatus] = mapped_column(Enum(AppealStatus), default=AppealStatus.PENDING, index=True)
    assigned_to: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    admin_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
````

## File: models/report.py
````python
import enum
from datetime import datetime

from sqlalchemy import JSON, BigInteger, DateTime, Enum, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class ReportReason(str, enum.Enum):
    FAKE = "FAKE"
    INSULT = "INSULT"
    INAPPROPRIATE_CONTENT = "INAPPROPRIATE_CONTENT"
    NSFW = "NSFW"
    SPAM = "SPAM"
    OTHER = "OTHER"


class ReportStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DISMISSED = "DISMISSED"


class Report(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "reports"
    __table_args__ = (UniqueConstraint("reporter_id", "target_user_id", name="uq_reports_reporter_target"),)
    reporter_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    target_user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    reason: Mapped[ReportReason] = mapped_column(Enum(ReportReason))
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus), default=ReportStatus.PENDING)
    # Immutable profile evidence captured when the report is filed.  Existing
    # reports from before this column deliberately remain nullable.
    evidence_snapshot: Mapped[dict[str, object] | None] = mapped_column(JSON, nullable=True)
    assigned_to: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    assigned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
````

## File: privacy/alpha-notice.md
````markdown
# Alpha Notice — MeAnima

*Документ подготовлен для этапа закрытой альфы MeAnima.*

---

## Вы участвуете в закрытой альфе

MeAnima сейчас находится на этапе **закрытого альфа-тестирования**. Это значит:

- **Возможны баги.** Функции могут работать нестабильно или неожиданно.
- **Функции могут меняться.** Что-то может быть добавлено, изменено или временно отключено без предупреждения.
- **Данные и анкеты могут быть затронуты техническими сбоями.** Мы стараемся этого избежать, но на этапе альфы возможны потери или ошибки в данных, связанные с техническими проблемами.
- **Вы — часть тестирования.** Ваше участие и обратная связь помогают нам находить и исправлять проблемы до более широкого запуска.

## Сообщить о проблеме

Если вы столкнулись с багом, ошибкой или чем-то, что работает не так:

- Напишите администратору через `/help` в боте
- Или на почту: `meanima.support@gmail.com`

Мы читаем всё, что присылают. На этапе альфы обратная связь особенно ценна.

## Что это не означает

Статус альфы не означает, что правила использования, безопасности и модерации применяются менее строго — они действуют в полном объёме. Альфа касается технической зрелости продукта, а не смягчения правил.
````

## File: privacy/bot-short-texts.md
````markdown
# Короткие тексты для бота MeAnima

*Каждый блок — отдельный модуль, кодирующий агент сам расставляет по нужным местам интерфейса.*

---

## 1. Подтверждение возраста (при регистрации)

> MeAnima доступна пользователям от `16` лет.
> Регистрируясь, вы подтверждаете, что достигли этого возраста и указываете достоверную информацию о себе.

## 2. Согласие с правилами (чекбокс/кнопка при регистрации)

> Продолжая, вы соглашаетесь с [Правилами сообщества] и [Пользовательским соглашением] MeAnima.

## 3. Короткая плашка про данные (рядом с согласием)

> Мы собираем данные вашей анкеты, чтобы показывать вас другим пользователям и обеспечивать работу лайков, матчей и модерации. Подробнее — в [Политике конфиденциальности].

## 4. Alpha-напоминание (можно показывать один раз при первом входе)

> MeAnima сейчас в закрытой альфе: возможны баги и изменения. Если что-то работает не так — напишите нам через `/help`.

## 5. Пункт в меню Help

> **Помощь и поддержка**
> Если у вас проблема, вопрос или жалоба — напишите администратору здесь: `/help`, либо на `meanima.support@gmail.com`.
> Документы: [Правила сообщества] · [Политика конфиденциальности] · [Пользовательское соглашение] · [Безопасность знакомств]

## 6. Короткая safety-плашка (например, при первом матче/чате)

> Пара базовых правил безопасности:
> — не делитесь личными данными (адрес, финансы, документы) раньше времени;
> — будьте осторожны, если собеседник настойчиво зовёт перейти в другой мессенджер;
> — никогда не переводите деньги людям, с которыми познакомились в приложении;
> — если что-то подозрительно — используйте `Report` или `Block`.

## 7. Сообщение после жалобы/заморозки анкеты (пользователю, чей профиль заморожен)

> Ваша анкета временно приостановлена и находится на проверке модератором. Это не окончательное решение. Вы можете подать апелляцию: `[ссылка/команда апелляции]`.

## 8. Кнопка/пункт "Пожаловаться"

> Если профиль или сообщение нарушает правила — нажмите **Report**. Мы рассмотрим жалобу и, если нужно, ограничим доступ пользователя.
````

## File: privacy/privacy-policy.md
````markdown
# Политика конфиденциальности — MeAnima

*Документ подготовлен для этапа закрытой альфы (до ~50 пользователей). Не является профессиональной юридической консультацией; при масштабировании сервиса рекомендуется проверка юристом — в частности, договороспособность пользователей 16–17 лет по Гражданскому кодексу Молдовы (раздел 9) и применимое право (раздел 12).*

---

## 1. Кто мы

MeAnima — сервис знакомств в формате Telegram-бота. Оператором сервиса на данном этапе является `Neta (независимый разработчик, оператор MeAnima)`.

MeAnima сейчас находится в статусе **закрытой альфы** (см. Alpha Notice) — это влияет на то, как мы обрабатываем данные: сервис небольшой, аудитория ограничена, а процессы могут меняться быстрее, чем в зрелом продукте.

Контакт по вопросам конфиденциальности: `meanima.support@gmail.com`.

## 2. Какие данные мы собираем

- **Данные анкеты**, которые вы сами указываете: возраст, пол, кого ищете, район/место (вводится вами вручную — точная геолокация не собирается), учёба/работа, интересы, описание.
- **Фотографии**, загруженные вами для анкеты.
- **Статус верификации** анкеты.
- **Технический идентификатор Telegram** (ID) и username, необходимые для работы аккаунта.
- **Данные взаимодействия**: лайки, скипы, матчи — в объёме, необходимом для работы рекомендаций.
- **Данные модерации**: жалобы (reports), блокировки (blocks), решения модераторов, апелляции.

Мы не собираем точную геолокацию, платёжные данные или данные из других приложений.

## 3. Зачем мы это собираем

- Чтобы показывать вашу анкету другим пользователям и работать функциям лайков/матчей.
- Чтобы проверять фото и профили на соответствие правилам (см. Правила сообщества и Пользовательское соглашение).
- Чтобы реагировать на жалобы, обеспечивать безопасность и рассматривать апелляции.
- Чтобы поддерживать техническую работу сервиса.

## 4. Правовое основание обработки

Обработка данных основывается на вашем согласии, которое вы даёте при регистрации, а также — в части модерации и безопасности — на законном интересе оператора в защите пользователей сообщества.

Обработка регулируется Законом Республики Молдова №195/2024 о защите персональных данных, действующим с 23 августа 2026 года.

См. раздел 9 — там отдельно про минимальный возраст и согласие несовершеннолетних.

## 5. Кто имеет доступ к данным

- Администраторы и модераторы MeAnima — в объёме, необходимом для работы и модерации.
- Автоматическая ML-проверка фотографий выполняется локально (модели YuNet и OpenNSFW или аналогичные); на данный момент фотографии **не передаются внешним сторонним сервисам**. Если это изменится, политика будет обновлена заранее.
- Третьим лицам вне сервиса данные не передаются, за исключением случаев, предусмотренных законом (например, официальный запрос уполномоченного органа).

## 6. Хранение и удаление

- При удалении анкеты данные профиля (описание, фото, интересы и т.д.) удаляются немедленно.
- Отдельные технические данные, необходимые для работы, безопасности, предотвращения злоупотреблений и выполнения обязательств, могут сохраняться ограниченный период — **до 21 дня** после удаления анкеты, после чего окончательно удаляются, если нет отдельного законного основания для дальнейшего хранения.
- Данные модерации (история жалоб, решений) могут храниться дольше в объёме, необходимом для защиты сообщества от повторных злоупотреблений — точный срок будет уточнён отдельно.

## 7. Ваши права

Вы имеете право:
- запросить доступ к своим данным;
- запросить исправление неточных данных;
- запросить удаление анкеты и аккаунта;
- возразить против обработки в определённых случаях;
- подать жалобу в Национальный центр по защите персональных данных Молдовы (NCPDP), если считаете, что ваши права нарушены.

Для реализации этих прав напишите на `meanima.support@gmail.com` или через `/help` в боте.

## 8. Безопасность данных

Мы принимаем разумные технические и организационные меры для защиты данных от несанкционированного доступа, потери или раскрытия. Как и любой сервис на этапе альфы, MeAnima может содержать технические недоработки — подробнее в Alpha Notice.

## 9. Несовершеннолетние пользователи

Минимальный возраст пользователя MeAnima — `16` лет (сейчас — 16).

Этот порог выбран не произвольно: согласно статье 8 Закона №195/2024 "Согласие детей в связи с услугами информационного общества", обработка персональных данных ребёнка на основании согласия является законной, если ребёнку не менее 16 лет. Если ребёнку меньше 16 лет, обработка законна только при наличии согласия родителя или иного законного представителя. MeAnima не принимает пользователей младше 16 лет и не запрашивает согласие родителей — вместо этого доступ к сервису ограничен порогом 16+.

⚠️ Это закрывает вопрос **правового основания обработки данных**, но не вопрос **договороспособности** по Гражданскому кодексу Молдовы (там иная логика: сделки лиц 14–17 лет по общему правилу требуют согласия законного представителя). Этот отдельный аспект — договорная природа Пользовательского соглашения для пользователей 16–17 лет — требует юридической проверки перед выходом за пределы закрытой альфы.

MeAnima полагается на самостоятельное указание возраста пользователем (self-report) и не имеет отдельного механизма технической верификации возраста.

## 10. Изменения политики

Мы можем обновлять эту политику по мере развития сервиса, особенно на этапе альфы. Существенные изменения будут сообщены пользователям через бота.

## 11. Контакты

По всем вопросам конфиденциальности: `meanima.support@gmail.com` или `/help` в боте.

## 12. Применимое право

Сервис ориентирован на пользователей в Молдове, к отношениям применяется законодательство Республики Молдова. Отдельная формализация юрисдикции для споров будет уточнена после регистрации юридической формы оператора.
````

## File: privacy/terms-of-service.md
````markdown
# Пользовательское соглашение — MeAnima

*Документ подготовлен для этапа закрытой альфы (до ~50 пользователей). Не является профессиональной юридической консультацией; при масштабировании сервиса рекомендуется проверка юристом — см. разделы 2 и 11.*

---

## 1. О сервисе

MeAnima — сервис знакомств в формате Telegram-бота, оператором которого является `Neta (независимый разработчик, оператор MeAnima)`. Сервис сейчас находится в статусе **закрытой альфы** — см. Alpha Notice, который является неотъемлемой частью этого соглашения.

Используя MeAnima, вы соглашаетесь с этим документом, Правилами сообщества и Политикой конфиденциальности.

## 2. Возраст и допуск к сервису

MeAnima предназначена для пользователей от `16` лет. Регистрируясь, вы подтверждаете, что достигли этого возраста и предоставляете достоверную информацию о себе.

Порог 16 лет соответствует статье 8 Закона №195/2024 о защите персональных данных, согласно которой обработка данных ребёнка на основании его собственного согласия законна с 16 лет.

⚠️ Отдельный открытый вопрос — договороспособность пользователей 16–17 лет по Гражданскому кодексу Молдовы: заключение сделок в этом возрасте по общему правилу требует согласия законного представителя. Это требует юридической проверки перед выходом за пределы закрытой альфы; на данном этапе MeAnima продолжает работу с этим допущением как с временным.

MeAnima не проводит отдельной верификации возраста — используется самостоятельное указание возраста пользователем. Ложное указание возраста является нарушением этого соглашения и основанием для блокировки.

## 3. Требования к профилю

- Информация в анкете должна быть достоверной и принадлежать вам лично.
- Фотографии должны быть вашими собственными и актуальными.
- Запрещено выдавать себя за другого человека (impersonation) или создавать фейковые/дублирующие анкеты.

## 4. Запрещённое поведение и контент

Запрещается:
- домогательства, травля, оскорбления, угрозы (harassment);
- спам, реклама, мошенничество (scams), в том числе просьбы о переводе денег;
- NSFW-контент (откровенно сексуальный контент, нагота) в фото и анкете;
- контент, пропагандирующий насилие, дискриминацию или незаконную деятельность;
- попытки обойти модерацию, автоматические проверки или ограничения аккаунта;
- сбор данных других пользователей вне функциональности сервиса.

Подробнее — в Правилах сообщества (человеческая версия этих правил).

## 5. Модерация и блокировки

- Профиль автоматически замораживается и отправляется на проверку модератору при накоплении определённого числа жалоб от других пользователей.
- Заморозка не означает автоматический окончательный бан — решение принимает модератор.
- MeAnima оставляет за собой право ограничить или прекратить доступ пользователя к сервису при нарушении этого соглашения, в том числе без предварительного уведомления в случаях серьёзных нарушений (угрозы, мошенничество, контент с несовершеннолетними и т.п.).

## 6. Апелляции

Если вы считаете решение модерации ошибочным, вы можете подать апелляцию через `/help` в боте или на `meanima.support@gmail.com`. Подробный процесс описан в документе Moderation & Appeals.

## 7. Ответственность пользователя

Вы несёте ответственность за:
- достоверность предоставленной информации;
- своё поведение при общении с другими пользователями внутри и вне сервиса;
- соблюдение применимого законодательства при использовании сервиса.

MeAnima не может гарантировать достоверность анкет других пользователей и не несёт ответственности за их поведение вне сервиса. Рекомендации по безопасному общению — в документе Dating Safety.

## 8. Статус альфы и ограничения сервиса

Сервис предоставляется "как есть" (as is), на этапе закрытого тестирования. Возможны технические сбои, изменения функциональности и временная недоступность. Подробнее — в Alpha Notice.

## 9. Прекращение использования

Вы можете прекратить использование сервиса и удалить аккаунт в любой момент. Порядок удаления данных описан в Политике конфиденциальности.

MeAnima может приостановить или прекратить ваш доступ при нарушении этого соглашения.

## 10. Изменения соглашения

Мы можем обновлять это соглашение по мере развития сервиса. О существенных изменениях пользователи будут уведомлены через бота.

## 11. Применимое право

К этому соглашению применяется законодательство Республики Молдова. Отдельная формализация порядка разрешения споров будет уточнена после регистрации юридической формы оператора.

## 12. Контакты

`meanima.support@gmail.com` или `/help` в боте.
````

## File: repositories/discovery.py
````python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Block, Dislike, Like, Match, Profile, User
from services.eligibility import EligibilityError, EligibilityService


class DiscoveryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def skip(self, source_id: int, target_id: int) -> None:
        existing = await self.session.scalar(
            select(Dislike).where(Dislike.from_user_id == source_id, Dislike.to_user_id == target_id)
        )
        if existing is None:
            self.session.add(Dislike(from_user_id=source_id, to_user_id=target_id))
            await self.session.flush()

    async def block(self, blocker_id: int, blocked_id: int) -> bool:
        try:
            await EligibilityService(self.session).ensure_action_allowed(blocker_id, blocked_id, action="заблокировать")
        except EligibilityError:
            return False

        existing = await self.session.scalar(
            select(Block).where(Block.blocker_id == blocker_id, Block.blocked_id == blocked_id)
        )
        if existing is None:
            self.session.add(Block(blocker_id=blocker_id, blocked_id=blocked_id))
            await self.session.flush()
            return True
        return False

    async def received_likes(self, user_id: int) -> list[Like]:
        return list((await self.session.scalars(
            select(Like).where(Like.to_user_id == user_id).order_by(Like.created_at.desc())
        )).all())

    async def matches(self, user_id: int) -> list[Match]:
        return list(
            (
                await self.session.scalars(
                    select(Match)
                    .where((Match.user1_id == user_id) | (Match.user2_id == user_id))
                    .order_by(Match.created_at.desc())
                )
            ).all()
        )

    async def profile_and_user(self, user_id: int) -> tuple[Profile | None, User | None]:
        return (
            await self.session.scalar(select(Profile).where(Profile.user_id == user_id)),
            await self.session.get(User, user_id),
        )
````

## File: services/localization.py
````python
import json
from functools import lru_cache
from pathlib import Path
from typing import Any


class LocalizationService:
    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent / "data" / "locales"

    @lru_cache(maxsize=8)
    def _load(self, locale: str) -> dict[str, Any]:
        path = self.base_dir / f"{locale}.json"
        if not path.exists():
            path = self.base_dir / "ru.json"
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def get(self, key: str, locale: str = "ru", default: str | None = None) -> str:
        data = self._load(locale)
        value = data.get(key)
        if isinstance(value, str):
            return value
        return default or key

    def format(self, key: str, locale: str = "ru", **kwargs: Any) -> str:
        value = self.get(key, locale=locale)
        if not kwargs:
            return value
        try:
            return value.format(**kwargs)
        except (IndexError, KeyError, TypeError, ValueError):
            # A broken catalog entry must never take down a user update.
            return value
````

## File: services/moderation_service.py
````python
import uuid
from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
    Appeal,
    AppealStatus,
    ModerationCase,
    ModerationCaseStatus,
    ModerationStatus,
    Profile,
    User,
    UserRole,
    UserStatus,
)
from repositories.trust import TrustRepository
from utils.admin_roles import (
    can_access_moderation,
    can_ban,
    can_override_case,
    can_release_cases,
    can_unban,
    normalize_admin_role,
)


class ModerationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = TrustRepository(session)

    async def _role_for(self, admin_id: int) -> UserRole:
        user = await self.session.get(User, admin_id)
        return normalize_admin_role(getattr(user, "role", UserRole.USER))

    async def _conflicting_case_for_user(
        self, user_id: int, admin_id: int, *, role: UserRole | None = None
    ) -> ModerationCase | None:
        role = role or await self._role_for(admin_id)
        if can_override_case(role):
            return None
        result = await self.session.execute(
            select(ModerationCase).where(
                ModerationCase.user_id == user_id,
                ModerationCase.status == ModerationCaseStatus.IN_PROGRESS,
            )
        )
        scalars = getattr(result, "scalars", None)
        if scalars is None:
            # Safety fallback for lightweight session stubs used in tests: if the session
            # cannot provide a real SQLAlchemy result, we conservatively deny the action
            # to non-overriding moderators rather than allowing a forbidden ban/freeze.
            return object()
        for case in scalars().all():
            if case.assigned_to not in {None, admin_id}:
                return case
        return None

    async def claim_case(
        self, case_id: uuid.UUID, moderator_id: int, *, actor_role: UserRole | None = None
    ) -> tuple[ModerationCase | None, bool, str | None]:
        case = await self.session.get(ModerationCase, case_id)
        if case is None:
            return None, False, "case_not_found"
        if case.status == ModerationCaseStatus.RESOLVED:
            return case, False, "already_resolved"
        role = actor_role or await self._role_for(moderator_id)
        if not can_access_moderation(role):
            return case, False, "forbidden"
        if case.status == ModerationCaseStatus.IN_PROGRESS and case.assigned_to != moderator_id:
            return case, False, "already_assigned"
        if case.status == ModerationCaseStatus.IN_PROGRESS and case.assigned_to == moderator_id:
            return case, False, "already_claimed"

        result = await self.session.execute(
            update(ModerationCase)
            .where(
                ModerationCase.id == case_id,
                ModerationCase.status == ModerationCaseStatus.PENDING,
                (ModerationCase.assigned_to.is_(None) | (ModerationCase.assigned_to == moderator_id)),
            )
            .values(
                status=ModerationCaseStatus.IN_PROGRESS,
                assigned_to=moderator_id,
                assigned_at=datetime.now(UTC),
            )
            .returning(ModerationCase)
        )
        updated = result.scalar_one_or_none()
        if updated is None:
            refreshed = await self.session.get(ModerationCase, case_id)
            if refreshed is None:
                return None, False, "case_not_found"
            if refreshed.status == ModerationCaseStatus.RESOLVED:
                return refreshed, False, "already_resolved"
            if refreshed.status == ModerationCaseStatus.IN_PROGRESS and refreshed.assigned_to != moderator_id:
                return refreshed, False, "already_assigned"
            return refreshed, False, "already_claimed"

        await self.repo.log(
            moderator_id,
            "CASE_CLAIMED",
            target_type="case",
            target_id=str(updated.id),
            target_user_id=updated.user_id,
            details="moderation case assigned",
            metadata={"case_type": updated.case_type.value, "assigned_to": moderator_id},
        )
        await self.session.flush()
        return updated, True, None

    async def release_case(
        self,
        case_id: uuid.UUID,
        actor_id: int,
        *,
        moderator_id: int | None = None,
    ) -> tuple[ModerationCase | None, bool, str | None]:
        role = await self._role_for(actor_id)
        if not can_release_cases(role):
            return await self.session.get(ModerationCase, case_id), False, "forbidden"
        case = await self.session.get(ModerationCase, case_id)
        if case is None:
            return None, False, "case_not_found"
        if case.status == ModerationCaseStatus.RESOLVED:
            return case, False, "already_resolved"
        if case.assigned_to is None:
            return case, False, "not_assigned"
        if case.assigned_to != actor_id and not can_override_case(role):
            return case, False, "forbidden"
        if moderator_id is not None and case.assigned_to != moderator_id and role == UserRole.MODERATOR:
            return case, False, "forbidden"

        result = await self.session.execute(
            update(ModerationCase)
            .where(
                ModerationCase.id == case_id,
                ModerationCase.status == ModerationCaseStatus.IN_PROGRESS,
                ModerationCase.assigned_to == case.assigned_to,
            )
            .values(status=ModerationCaseStatus.PENDING, assigned_to=None, assigned_at=None)
            .returning(ModerationCase)
        )
        updated = result.scalar_one_or_none()
        if updated is None:
            return case, False, "not_assigned"
        await self.repo.log(
            actor_id,
            "CASE_UNASSIGNED",
            target_type="case",
            target_id=str(updated.id),
            target_user_id=updated.user_id,
            details="moderation case released",
            metadata={"released_from": case.assigned_to, "case_type": updated.case_type.value},
        )
        await self.session.flush()
        return updated, True, None

    async def resolve_case(
        self,
        case_id: uuid.UUID,
        admin_id: int,
        *,
        restore: bool = False,
        retake: bool = False,
        actor_role: UserRole | None = None,
    ) -> tuple[ModerationCase | None, bool, str | None]:
        case = await self.session.get(ModerationCase, case_id)
        if case is None:
            return None, False, "case_not_found"
        if case.status == ModerationCaseStatus.RESOLVED:
            return case, False, "already_resolved"
        if case.status != ModerationCaseStatus.IN_PROGRESS:
            return case, False, "not_in_progress"

        role = actor_role or await self._role_for(admin_id)
        if not can_access_moderation(role):
            return case, False, "forbidden"

        if case.assigned_to not in {None, admin_id}:
            if not can_override_case(role):
                return case, False, "forbidden"

        if case.assigned_to is None:
            case, claimed, message = await self.claim_case(case_id, admin_id, actor_role=role)
            if not claimed:
                return case, False, message or "claim_required"

        result = await self.session.execute(
            update(ModerationCase)
            .where(
                ModerationCase.id == case_id,
                ModerationCase.status == ModerationCaseStatus.IN_PROGRESS,
                ModerationCase.assigned_to == case.assigned_to,
            )
            .values(status=ModerationCaseStatus.RESOLVED, admin_id=admin_id, assigned_to=admin_id)
            .returning(ModerationCase)
        )
        updated = result.scalar_one_or_none()
        if updated is None:
            refreshed = await self.session.get(ModerationCase, case_id)
            if refreshed and refreshed.status == ModerationCaseStatus.RESOLVED:
                return refreshed, False, "already_resolved"
            return refreshed, False, "already_assigned"
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == updated.user_id))
        if profile:
            profile.moderation_status = ModerationStatus.CLEAR
            if restore:
                profile.moderation_locked = False
                profile.is_visible = True
            elif retake:
                # A replacement request is not an approval.  Keep the account
                # frozen until a moderator explicitly restores it after review.
                profile.is_visible = False
        await self.repo.log(
            admin_id,
            "CASE_RESOLVED",
            target_type="case",
            target_id=str(updated.id),
            target_user_id=updated.user_id,
            details="moderation case resolved",
            metadata={"restore": restore, "retake": retake, "case_type": updated.case_type.value},
        )
        await self.session.flush()
        return updated, True, None

    async def suspend(
        self, user_id: int, admin_id: int, *, reason: str, actor_role: UserRole | None = None
    ) -> bool:
        role = actor_role or await self._role_for(admin_id)
        if not can_ban(role):
            return False
        if user_id == admin_id:
            return False
        if await self._conflicting_case_for_user(user_id, admin_id, role=role) is not None:
            return False
        user = await self.session.get(User, user_id)
        if user is None or getattr(user, "status", None) == UserStatus.BANNED:
            return False
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        user.status = UserStatus.SUSPENDED
        if profile:
            profile.is_visible = False
            profile.moderation_locked = True
            profile.moderation_status = ModerationStatus.UNDER_REVIEW
        await self.repo.log(
            admin_id,
            "FREEZE",
            target_type="user",
            target_id=str(user_id),
            target_user_id=user_id,
            details=reason,
            metadata={"kind": "freeze"},
        )
        await self.session.flush()
        return True

    async def ban(
        self, user_id: int, admin_id: int, *, reason: str, actor_role: UserRole | None = None
    ) -> bool:
        role = actor_role or await self._role_for(admin_id)
        if not can_ban(role):
            return False
        if user_id == admin_id:
            return False
        if await self._conflicting_case_for_user(user_id, admin_id, role=role) is not None:
            return False
        user = await self.session.get(User, user_id)
        if user is None:
            return False
        if getattr(user, "status", None) == UserStatus.BANNED:
            return False
        user.status = UserStatus.BANNED
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        if profile:
            profile.is_visible = False
            profile.moderation_locked = True
        await self.repo.log(
            admin_id,
            "BAN",
            target_type="user",
            target_id=str(user_id),
            target_user_id=user_id,
            details=reason,
            metadata={"kind": "ban"},
        )
        await self.session.flush()
        return True

    async def unban(self, user_id: int, admin_id: int, *, actor_role: UserRole | None = None) -> bool:
        role = actor_role or await self._role_for(admin_id)
        if not can_unban(role):
            return False
        user = await self.session.get(User, user_id)
        if user is None or getattr(user, "status", None) != UserStatus.BANNED:
            return False
        user.status = UserStatus.ACTIVE
        await self.repo.log(
            admin_id,
            "UNBAN",
            target_type="user",
            target_id=str(user_id),
            target_user_id=user_id,
            details="manual unban",
        )
        await self.session.flush()
        return True

    async def restore_appeal_sanction(
        self, appeal: Appeal, admin_id: int, *, actor_role: UserRole | None = None
    ) -> tuple[bool, str | None]:
        role = actor_role or await self._role_for(admin_id)
        if not can_unban(role):
            return False, "forbidden"
        if appeal.status != AppealStatus.PENDING:
            return False, "already_resolved"

        result = await self.session.execute(
            select(ModerationCase).where(
                ModerationCase.user_id == appeal.user_id,
                ModerationCase.status == ModerationCaseStatus.IN_PROGRESS,
            )
        )
        if result.scalars().first() is not None:
            return False, "other_open_sanction"

        user = await self.session.get(User, appeal.user_id)
        if user is None or user.status not in {UserStatus.BANNED, UserStatus.SUSPENDED}:
            return False, "not_restricted"
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == appeal.user_id))
        user.status = UserStatus.ACTIVE
        if profile:
            profile.moderation_locked = False
            profile.moderation_status = ModerationStatus.CLEAR
            profile.is_visible = True
        appeal.status = AppealStatus.APPROVED
        appeal.admin_id = admin_id
        appeal.reviewed_at = datetime.now(UTC)
        await self.repo.log(
            admin_id,
            "appeal_restored",
            target_type="appeal",
            target_id=str(appeal.id),
            target_user_id=appeal.user_id,
        )
        await self.session.flush()
        return True, None
````

## File: services/photo_safety_providers.py
````python
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


class PhotoSafetyConfigurationError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class SafeImage:
    """Decoded, EXIF-stripped image accepted by the moderation boundary."""

    rgb_bytes: bytes
    width: int
    height: int


@dataclass(frozen=True, slots=True)
class PhotoAssessment:
    nsfw_score: float
    face_detected: bool
    provider: str = "heuristic"


class PhotoSafetyProvider(Protocol):
    name: str

    async def assess(self, image: SafeImage | None) -> PhotoAssessment: ...


class HeuristicPhotoSafetyProvider:
    name = "heuristic"

    async def assess(self, image: SafeImage | None) -> PhotoAssessment:
        return PhotoAssessment(nsfw_score=0.0, face_detected=True, provider=self.name)


class DisabledPhotoSafetyProvider:
    name = "disabled"

    async def assess(self, image: SafeImage | None) -> PhotoAssessment:
        return PhotoAssessment(nsfw_score=0.0, face_detected=True, provider=self.name)


def face_detection_size(width: int, height: int, max_dimension: int) -> tuple[int, int]:
    """Fit a camera image into YuNet's working size without distorting it."""
    largest_dimension = max(width, height)
    if largest_dimension <= max_dimension:
        return width, height
    scale = max_dimension / largest_dimension
    return max(1, round(width * scale)), max(1, round(height * scale))


class OnnxPhotoSafetyProvider:
    """Local CPU inference: OpenNSFW-compatible ONNX + OpenCV YuNet, no cloud calls."""

    name = "ml_onnx"

    def __init__(
        self,
        *,
        nsfw_model_path: str,
        face_model_path: str,
        face_threshold: float,
        face_max_dimension: int,
    ) -> None:
        self.nsfw_model_path = Path(nsfw_model_path)
        self.face_model_path = Path(face_model_path)
        self.face_threshold = face_threshold
        self.face_max_dimension = face_max_dimension
        self._nsfw_session = None

    async def assess(self, image: SafeImage | None) -> PhotoAssessment:
        if image is None:
            raise PhotoSafetyConfigurationError("Telegram photo source is required for ML provider")
        return await asyncio.to_thread(self._assess_sync, image)

    def _assess_sync(self, image: SafeImage) -> PhotoAssessment:
        if not self.nsfw_model_path.is_file() or not self.face_model_path.is_file():
            raise PhotoSafetyConfigurationError("Local ONNX models are missing")
        try:
            import cv2
            import numpy as np
            import onnxruntime as ort
        except ImportError as error:  # pragma: no cover - covered by deployment image
            raise PhotoSafetyConfigurationError("ML dependencies are not installed") from error

        decoded = cv2.imdecode(np.frombuffer(image.rgb_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
        if decoded is None:
            raise ValueError("Normalized image cannot be decoded")
        face_width, face_height = face_detection_size(image.width, image.height, self.face_max_dimension)
        face_image = decoded
        if (face_width, face_height) != (image.width, image.height):
            face_image = cv2.resize(decoded, (face_width, face_height), interpolation=cv2.INTER_AREA)
        detector = cv2.FaceDetectorYN.create(
            str(self.face_model_path), "", (face_width, face_height), self.face_threshold, 0.3, 5000
        )
        _, faces = detector.detect(face_image)

        if self._nsfw_session is None:
            self._nsfw_session = ort.InferenceSession(str(self.nsfw_model_path), providers=["CPUExecutionProvider"])
        model_input = self._nsfw_session.get_inputs()[0]
        resized = cv2.resize(decoded, (224, 224), interpolation=cv2.INTER_AREA).astype(np.float32)
        if model_input.shape[-1] == 3:
            # Keras/OpenNSFW2 ONNX exports use NHWC RGB tensors.
            tensor = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)[None, ...]
        else:
            # Legacy Yahoo/OpenNSFW exports use BGR NCHW with Caffe channel means.
            resized -= np.array([104.0, 117.0, 123.0], dtype=np.float32)
            tensor = np.transpose(resized, (2, 0, 1))[None, ...]
        input_name = model_input.name
        output = np.asarray(self._nsfw_session.run(None, {input_name: tensor})[0]).reshape(-1)
        if output.size < 2:
            raise ValueError("OpenNSFW model returned an invalid output")
        score = float(output[-1])
        if not 0.0 <= score <= 1.0:
            raise ValueError("OpenNSFW model returned an invalid score")
        return PhotoAssessment(nsfw_score=score, face_detected=faces is not None and len(faces) > 0, provider=self.name)


_PROVIDER_CACHE: dict[tuple[str, str, str, float, int], PhotoSafetyProvider] = {}


def build_photo_safety_provider(settings) -> PhotoSafetyProvider:
    if settings.photo_safety_provider == "heuristic":
        return HeuristicPhotoSafetyProvider()
    if settings.photo_safety_provider == "disabled":
        return DisabledPhotoSafetyProvider()
    if settings.photo_safety_provider == "ml":
        return OnnxPhotoSafetyProvider(
            nsfw_model_path=settings.nsfw_model_path,
            face_model_path=settings.face_model_path,
            face_threshold=settings.face_detection_threshold,
            face_max_dimension=settings.face_detection_max_dimension,
        )
    raise PhotoSafetyConfigurationError(f"Unknown photo safety provider: {settings.photo_safety_provider}")


def get_photo_safety_provider(settings) -> PhotoSafetyProvider:
    """Reuse loaded model sessions for the bot process; selection still comes entirely from config."""
    key = (
        settings.photo_safety_provider,
        settings.nsfw_model_path,
        settings.face_model_path,
        settings.face_detection_threshold,
        settings.face_detection_max_dimension,
    )
    if key not in _PROVIDER_CACHE:
        _PROVIDER_CACHE[key] = build_photo_safety_provider(settings)
    return _PROVIDER_CACHE[key]
````

## File: services/photo_upload_lock.py
````python
from __future__ import annotations

import asyncio
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

_local_locks: dict[int, asyncio.Lock] = {}


class PhotoUploadBusyError(RuntimeError):
    pass


@asynccontextmanager
async def photo_upload_lock(bot, user_id: int) -> AsyncIterator[None]:
    """Serialize photo updates across workers when the shared Redis client is available."""
    redis = getattr(bot, "notification_redis", None)
    if redis is None:
        lock = _local_locks.setdefault(user_id, asyncio.Lock())
        async with lock:
            yield
        return

    key = f"photo_upload:lock:{user_id}"
    token = uuid.uuid4().hex
    acquired = False
    try:
        for _ in range(40):
            if await redis.set(key, token, nx=True, ex=10):
                acquired = True
                break
            await asyncio.sleep(0.05)
        if not acquired:
            raise PhotoUploadBusyError("Photo upload is busy; please retry")
        yield
    finally:
        if acquired:
            try:
                await redis.eval(
                    "if redis.call('GET', KEYS[1]) == ARGV[1] then return redis.call('DEL', KEYS[1]) else return 0 end",
                    1,
                    key,
                    token,
                )
            except Exception:
                pass
````

## File: services/promo_service.py
````python
from __future__ import annotations

from typing import Any

from services.localization import LocalizationService


def get_empty_discovery_promo(
    user_id: int, *, profile: Any | None = None, locale: str = "ru"
) -> dict[str, Any]:
    """Return a fallback promo card for users with no more nearby matches.

    The broader app may customize this later with personalized copy, but the UI code
    only requires a small dict with title/text/button values.
    """
    localizer = LocalizationService()
    return {
        "title": localizer.get("promo_empty_title", locale),
        "text": localizer.get("promo_empty_text", locale),
        "button_text": localizer.get("promo_refresh", locale),
        "button_action": "next:profile",
    }
````

## File: services/report_service.py
````python
from sqlalchemy.ext.asyncio import AsyncSession

from models import ModerationCaseType, ModerationStatus, ReportReason, ReportStatus
from repositories.discovery import DiscoveryRepository
from repositories.profile import ProfileRepository
from repositories.report import ReportRepository
from repositories.trust import TrustRepository
from services.eligibility import EligibilityError, EligibilityService
from services.trust_score_service import TrustScoreService


class ReportService:
    def __init__(self, session: AsyncSession, *, threshold: int) -> None:
        self.session = session
        self.threshold = threshold

    async def submit(self, reporter_id: int, target_id: int, reason: ReportReason):
        try:
            await EligibilityService(self.session).ensure_action_allowed(reporter_id, target_id, action="пожаловаться")
        except EligibilityError as error:
            raise ValueError(str(error)) from error

        target_profile = await ProfileRepository(self.session).by_user_id(target_id)
        evidence_snapshot = self._evidence_snapshot(target_profile)
        report, created, threshold_reached = await ReportRepository(self.session).add(
            reporter_id,
            target_id,
            reason,
            threshold=self.threshold,
            evidence_snapshot=evidence_snapshot,
        )
        await DiscoveryRepository(self.session).block(reporter_id, target_id)
        if created:
            await TrustScoreService(self.session).change(
                target_id, -10, "report_received", reference_type="report", reference_id=str(report.id)
            )
        if threshold_reached:
            profile = await ProfileRepository(self.session).by_user_id(target_id)
            if profile:
                profile.moderation_status = ModerationStatus.UNDER_REVIEW
            await TrustRepository(self.session).open_case(
                target_id,
                ModerationCaseType.REPORT_THRESHOLD,
                source_id=str(report.id),
                details=f"Reached {self.threshold} unique reports",
            )
        return report, created, threshold_reached

    @staticmethod
    def _evidence_snapshot(profile) -> dict[str, object]:
        """Capture report evidence before later profile edits or deletion."""
        if profile is None:
            return {}
        return {
            "name": profile.name,
            "age": profile.age,
            "district": profile.district,
            "institution": profile.institution,
            "bio": profile.bio,
            "interests": list(profile.interests or []),
            "photo_file_ids": list(profile.photo_file_ids or []),
            "main_photo_file_id": profile.main_photo_file_id,
        }

    async def dismiss(self, report_id, admin_id: int):
        repo = ReportRepository(self.session)
        report = await repo.resolve(report_id, ReportStatus.DISMISSED)
        if report:
            await TrustScoreService(self.session).change(
                report.reporter_id, -5, "false_report", reference_type="report", reference_id=str(report.id)
            )
            await TrustRepository(self.session).log(
                admin_id, "report_dismissed", target_type="report", target_id=str(report.id)
            )
        return report

    async def confirm_fake(self, report_id, admin_id: int):
        repo = ReportRepository(self.session)
        report = await repo.resolve(report_id, ReportStatus.APPROVED)
        if report:
            await TrustScoreService(self.session).change(
                report.target_user_id, -40, "confirmed_fake", reference_type="report", reference_id=str(report.id)
            )
            await TrustRepository(self.session).log(
                admin_id, "report_confirmed_fake", target_type="report", target_id=str(report.id)
            )
        return report
````

## File: states/profile_photo.py
````python
from aiogram.fsm.state import State, StatesGroup


class ProfilePhotoState(StatesGroup):
    waiting_photo = State()
    awaiting_manual_review = State()
````

## File: tests/test_callback_resilience.py
````python
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from handlers.admin import mycase_open
from handlers.callback_fallback import no_state_message, outdated_callback
from handlers.profile import delete_confirm
from repositories.report import ReportRepository
from services.profile_service import ProfileService


@pytest.mark.asyncio
async def test_outdated_callback_always_stops_telegram_loading_indicator():
    callback = SimpleNamespace(answer=AsyncMock())

    await outdated_callback(callback)

    callback.answer.assert_awaited_once_with(
        "Эта кнопка устарела. Откройте актуальный раздел меню.", show_alert=True
    )


@pytest.mark.asyncio
async def test_deleted_admin_case_is_acknowledged(monkeypatch):
    monkeypatch.setattr("handlers.admin._require_admin_capability", AsyncMock(return_value=True))

    async def no_report(self, report_id):
        return None

    monkeypatch.setattr(ReportRepository, "get", no_report)
    message = SimpleNamespace(delete=AsyncMock(), answer=AsyncMock())
    callback = SimpleNamespace(
        data="mycase:report:00000000-0000-0000-0000-000000000001",
        from_user=SimpleNamespace(id=1),
        message=message,
        answer=AsyncMock(),
    )

    await mycase_open(callback, session=SimpleNamespace(), settings=SimpleNamespace())

    callback.answer.assert_awaited_once_with("Жалоба уже удалена.", show_alert=True)


@pytest.mark.asyncio
async def test_deleted_profile_confirmation_does_not_report_success(monkeypatch):
    monkeypatch.setattr(ProfileService, "delete", AsyncMock(return_value=False))
    message = SimpleNamespace(edit_text=AsyncMock())
    callback = SimpleNamespace(from_user=SimpleNamespace(id=1), message=message, answer=AsyncMock())

    await delete_confirm(callback, session=SimpleNamespace())

    callback.answer.assert_awaited_once_with("Анкета уже была удалена.", show_alert=True)
    message.edit_text.assert_not_awaited()


@pytest.mark.asyncio
async def test_no_state_message_returns_to_main_menu():
    message = SimpleNamespace(answer=AsyncMock())

    await no_state_message(message)

    message.answer.assert_awaited_once()
    assert message.answer.await_args.kwargs["reply_markup"] is not None
````

## File: tests/test_db_reset.py
````python
from utils.db_reset import get_reset_table_names


def test_reset_tool_uses_current_confession_schema() -> None:
    from pathlib import Path

    source = Path("tools/reset_test_data.py").read_text()

    assert "Confession.sender_id" not in source
    assert "Confession.receiver_id" not in source
    assert "ConfessionDailyLimit.user_id" not in source


def test_reset_table_names_are_sorted_for_fk_safe_cleanup() -> None:
    tables = get_reset_table_names()

    assert tables[:3] == ["likes", "dislikes", "matches"]
    assert tables[-2:] == ["profiles", "users"]
    assert "admin_logs" in tables
````

## File: tests/test_deployment_config.py
````python
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
````

## File: tests/test_eligibility.py
````python
from types import SimpleNamespace

import pytest

from handlers.dating import _target_id
from models import ModerationStatus, ReportReason, UserStatus
from repositories.discovery import DiscoveryRepository
from services.like_service import LikeService
from services.report_service import ReportService


class FakeEligibilitySession:
    def __init__(self, *, profile=None, user=None, block=None):
        self._scalar_results = [profile, block]
        self.user = user
        self.added = []

    async def scalar(self, _statement):
        if not self._scalar_results:
            return None
        return self._scalar_results.pop(0)

    async def get(self, _model, _key):
        return self.user

    def add(self, item):
        self.added.append(item)

    async def flush(self):
        return None


@pytest.mark.asyncio
async def test_like_service_rejects_ineligible_targets():
    profile = SimpleNamespace(
        user_id=2,
        is_visible=False,
        moderation_locked=False,
        moderation_status=ModerationStatus.CLEAR,
    )
    user = SimpleNamespace(status=UserStatus.ACTIVE)
    session = FakeEligibilitySession(profile=profile, user=user)

    with pytest.raises(ValueError, match="Анкета недоступна"):
        await LikeService(session).create(1, 2)


@pytest.mark.asyncio
async def test_report_service_rejects_inactive_users():
    profile = SimpleNamespace(
        user_id=2,
        is_visible=True,
        moderation_locked=False,
        moderation_status=ModerationStatus.CLEAR,
    )
    user = SimpleNamespace(status=UserStatus.PAUSED)
    session = FakeEligibilitySession(profile=profile, user=user)

    with pytest.raises(ValueError, match="Анкета недоступна"):
        await ReportService(session, threshold=3).submit(1, 2, ReportReason.SPAM)


@pytest.mark.asyncio
async def test_block_repository_skips_ineligible_target_without_persisting_block():
    profile = SimpleNamespace(
        user_id=2,
        is_visible=True,
        moderation_locked=False,
        moderation_status=ModerationStatus.CLEAR,
    )
    user = SimpleNamespace(status=UserStatus.ACTIVE)
    session = FakeEligibilitySession(profile=profile, user=user, block=1)

    created = await DiscoveryRepository(session).block(1, 2)

    assert created is False
    assert session.added == []


@pytest.mark.asyncio
async def test_block_repository_reports_when_block_is_created():
    profile = SimpleNamespace(
        user_id=2,
        is_visible=True,
        moderation_locked=False,
        moderation_status=ModerationStatus.CLEAR,
    )
    user = SimpleNamespace(status=UserStatus.ACTIVE)
    session = FakeEligibilitySession(profile=profile, user=user, block=None)

    created = await DiscoveryRepository(session).block(1, 2)

    assert created is True
    assert len(session.added) == 1


def test_legacy_callback_data_still_parses_target_id():
    assert _target_id(SimpleNamespace(data="comment:42")) == 42
````

## File: tests/test_high_regressions.py
````python
import asyncio
import uuid
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest

from config import Settings
from handlers.admin import _render_report
from models import ReportReason, ReportStatus
from services.notification_service import NotificationService
from services.report_service import ReportService


class FakeRedis:
    def __init__(self):
        self.values = {}

    async def exists(self, key):
        return key in self.values

    async def set(self, key, value, *, nx=False, ex=None):
        if nx and key in self.values:
            return False
        self.values[key] = value
        return True

    async def delete(self, key):
        self.values.pop(key, None)


class FakeBot:
    def __init__(self, redis=None, *, fail=False):
        self.notification_redis = redis
        self.fail = fail
        self.sent = []

    async def send_message(self, chat_id, text, **kwargs):
        if self.fail:
            raise RuntimeError("telegram unavailable")
        self.sent.append((chat_id, text, kwargs))


class BrokenRedis:
    async def exists(self, _key):
        raise RuntimeError("redis unavailable")

    async def set(self, *_args, **_kwargs):
        raise RuntimeError("redis unavailable")


class CleanupBrokenRedis(FakeRedis):
    async def delete(self, _key):
        raise RuntimeError("redis unavailable")


class FakeMessage:
    def __init__(self):
        self.sent = []

    async def answer(self, text, **kwargs):
        self.sent.append((text, kwargs))

    async def answer_photo(self, _photo, *, caption, **kwargs):
        self.sent.append((caption, kwargs))


class FakeSession:
    async def get(self, _model, _user_id):
        return SimpleNamespace(username="target")


def test_confession_and_fsm_settings_have_safe_defaults():
    settings = Settings(bot_token="x" * 30, daily_secret_salt="y" * 20)

    assert settings.confession_daily_limit == 20
    assert settings.confession_pending_ttl_hours == 168
    assert settings.fsm_state_ttl_seconds == 3600


@pytest.mark.asyncio
async def test_report_snapshot_survives_profile_change_and_is_rendered():
    profile = SimpleNamespace(
        name="Before",
        age=22,
        district="Center",
        institution="University",
        bio="Original bio",
        interests=["music"],
        photo_file_ids=["photo-before"],
        main_photo_file_id="photo-before",
    )
    snapshot = ReportService._evidence_snapshot(profile)
    profile.name, profile.bio, profile.photo_file_ids = "After", "Changed", []

    report = SimpleNamespace(
        id=uuid.uuid4(),
        evidence_snapshot=snapshot,
        target_user_id=42,
        reason=ReportReason.FAKE,
        details=None,
        status=ReportStatus.PENDING,
        assigned_to=None,
        created_at=datetime.now(UTC),
    )
    message = FakeMessage()
    callback = SimpleNamespace(message=message, from_user=SimpleNamespace(id=7))

    await _render_report(callback, FakeSession(), report)

    assert snapshot["name"] == "Before"
    assert snapshot["photo_file_ids"] == ["photo-before"]
    assert "Before, 22" in message.sent[0][0]


@pytest.mark.asyncio
async def test_redis_notification_dedupe_survives_new_service_and_retries_failure():
    redis = FakeRedis()
    bot = FakeBot(redis)
    first = NotificationService(bot)
    restarted = NotificationService(bot)

    assert await first.safe_send(42, "event", dedupe_key="event:1") is True
    assert await restarted.safe_send(42, "event", dedupe_key="event:1") is False
    assert len(bot.sent) == 1

    failing = FakeBot(redis, fail=True)
    assert await NotificationService(failing).safe_send(43, "event", dedupe_key="event:2") is False
    retry = FakeBot(redis)
    assert await NotificationService(retry).safe_send(43, "event", dedupe_key="event:2") is True


@pytest.mark.asyncio
async def test_redis_notification_concurrent_duplicates_send_once():
    redis = FakeRedis()
    bot = FakeBot(redis)
    results = await asyncio.gather(
        NotificationService(bot).safe_send(42, "event", dedupe_key="concurrent"),
        NotificationService(bot).safe_send(42, "event", dedupe_key="concurrent"),
    )

    assert results.count(True) == 1
    assert len(bot.sent) == 1


@pytest.mark.asyncio
async def test_redis_dedupe_failure_does_not_abort_notification():
    bot = FakeBot(BrokenRedis())

    assert await NotificationService(bot).safe_send(42, "event", dedupe_key="outage") is True
    assert len(bot.sent) == 1


@pytest.mark.asyncio
async def test_successful_notification_survives_redis_cleanup_failure():
    bot = FakeBot(CleanupBrokenRedis())

    assert await NotificationService(bot).safe_send(42, "event", dedupe_key="cleanup") is True
    assert len(bot.sent) == 1
````

## File: tests/test_photo_analysis_progress.py
````python
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from keyboards.profile import failed_photo_keyboard
from services.photo_analysis_progress import (
    PHOTO_ANALYSIS_TEXT,
    dismiss_photo_analysis_progress,
    show_photo_analysis_progress,
)


@pytest.mark.asyncio
async def test_photo_analysis_progress_is_shown_and_removed():
    progress = SimpleNamespace(delete=AsyncMock())
    message = SimpleNamespace(answer=AsyncMock(return_value=progress))

    shown = await show_photo_analysis_progress(message)
    await dismiss_photo_analysis_progress(shown)

    message.answer.assert_awaited_once_with(PHOTO_ANALYSIS_TEXT)
    progress.delete.assert_awaited_once()


def test_failed_photo_keyboard_offers_replace_or_manual_review():
    callback_data = {
        button.callback_data
        for row in failed_photo_keyboard().inline_keyboard
        for button in row
    }

    assert callback_data == {"photo:retry_failed", "photo:review_failed"}
````

## File: tests/test_profile_registration.py
````python
import pytest

from services.interest_normalizer import normalize_interests
from services.profile_service import ProfileService
from utils.profile_media import ordered_photo_ids
from validators.profile_validator import ProfileValidationError, validate_profile_payload


def test_validate_profile_payload_rejects_bad_name_and_age():
    payload = {
        "name": "***",
        "age": 10,
        "district": "A" * 200,
        "institution": "B" * 200,
        "bio": "x",
    }

    try:
        validate_profile_payload(payload)
    except ProfileValidationError as exc:
        assert "name" in exc.errors
        assert "age" in exc.errors
        assert "district" in exc.errors
        assert "institution" in exc.errors
        assert "bio" in exc.errors
    else:
        raise AssertionError("Expected validation to fail")


def test_normalize_interests_maps_popular_categories():
    normalized = normalize_interests("Люблю музыку, рок, спорт, программирование, астрономия")

    assert "music" in normalized
    assert "sport" in normalized
    assert "programming" in normalized
    assert "астрономия" in normalized
    assert len(normalized) >= 4


def test_normalize_interests_splits_comma_separated_values_in_list():
    normalized = normalize_interests(["Music, sport, movie"])

    assert "music" in normalized
    assert "sport" in normalized
    assert "cinema" in normalized
    assert len(normalized) == 3


def test_format_interests_returns_hashtag_style_text():
    from services.interest_normalizer import format_interests

    assert format_interests(["music", "sport"]) == "#Music #Sport"


def test_validate_profile_payload_rejects_invalid_gender_values():
    payload = {
        "name": "Аня",
        "age": 24,
        "district": "Центр",
        "institution": "Университет",
        "bio": "Люблю прогулки и кофе.",
        "gender": "UNKNOWN",
        "target_gender": "WRONG",
    }

    try:
        validate_profile_payload(payload, photo_file_ids=["photo-id"])
    except ProfileValidationError as exc:
        assert "gender" in exc.errors
        assert "target_gender" in exc.errors
    else:
        raise AssertionError("Expected validation to fail")


def test_main_photo_is_rendered_first_in_gallery():
    profile = type(
        "Profile",
        (),
        {"photo_file_ids": ["one", "two", "three"], "main_photo_file_id": "two", "photo_file_id": "one"},
    )()

    assert ordered_photo_ids(profile) == ["two", "one", "three"]


class FakeProfileRepository:
    def __init__(self, profile):
        self.profile = profile
        self.save_calls = 0

    async def by_user_id(self, _user_id):
        return self.profile

    async def save(self, _profile):
        self.save_calls += 1


def managed_profile(photo_ids):
    return type(
        "Profile",
        (),
        {
            "photo_file_ids": list(photo_ids),
            "photo_file_id": photo_ids[0] if photo_ids else "",
            "main_photo_file_id": photo_ids[0] if photo_ids else None,
            "extra_data": {"photo_file_ids": list(photo_ids)},
            "moderation_locked": False,
            "moderation_status": None,
            "is_visible": True,
        },
    )()


@pytest.mark.asyncio
async def test_stale_photo_operations_are_safe_noops():
    profile = managed_profile(["one", "two"])
    service = ProfileService(None)
    service.repo = FakeProfileRepository(profile)

    assert await service.move_photo(1, "gone", 1) is profile
    assert await service.replace_photo(1, "gone", "new") is profile
    assert profile.photo_file_ids == ["one", "two"]
    assert service.repo.save_calls == 0


@pytest.mark.asyncio
async def test_add_photo_rejects_stale_fourth_upload():
    profile = managed_profile(["one", "two", "three"])
    service = ProfileService(None)
    service.repo = FakeProfileRepository(profile)

    with pytest.raises(ValueError, match="не более трёх"):
        await service.add_photo(1, "four")

    assert profile.photo_file_ids == ["one", "two", "three"]


@pytest.mark.asyncio
async def test_add_photo_accumulates_up_to_three_ids():
    profile = managed_profile([])
    service = ProfileService(None)
    service.repo = FakeProfileRepository(profile)

    await service.add_photo(1, "one")
    await service.add_photo(1, "two")
    await service.add_photo(1, "three")

    assert profile.photo_file_ids == ["one", "two", "three"]
    assert profile.extra_data["photo_file_ids"] == ["one", "two", "three"]
````

## File: tests/test_profile_required.py
````python
from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from aiogram.types import CallbackQuery, User

from middlewares.profile_required import ProfileRequiredMiddleware


@pytest.mark.asyncio
async def test_allows_when_current_user_has_profile(monkeypatch):
    middleware = ProfileRequiredMiddleware()
    handled = False

    async def handler(event, data):
        nonlocal handled
        handled = True
        return "handled"

    # force middleware to consider the event as one that requires profile
    monkeypatch.setattr(ProfileRequiredMiddleware, "_requires_profile", classmethod(lambda cls, event: True))

    async def fake_get_profile(self, user_id):
        return True

    monkeypatch.setattr("services.profile_service.ProfileService.get_profile", fake_get_profile)

    data = {"current_user": SimpleNamespace(id=42), "session": SimpleNamespace()}
    result = await middleware(handler, SimpleNamespace(), data)

    assert result == "handled"
    assert handled


@pytest.mark.asyncio
async def test_allows_when_event_from_user_has_profile(monkeypatch):
    middleware = ProfileRequiredMiddleware()
    handled = False

    async def handler(event, data):
        nonlocal handled
        handled = True
        return "handled"

    monkeypatch.setattr(ProfileRequiredMiddleware, "_requires_profile", classmethod(lambda cls, event: True))

    async def fake_get_profile(self, user_id):
        return True

    monkeypatch.setattr("services.profile_service.ProfileService.get_profile", fake_get_profile)

    data = {"event_from_user": SimpleNamespace(id=43), "session": SimpleNamespace()}
    result = await middleware(handler, SimpleNamespace(from_user=SimpleNamespace(id=43)), data)

    assert result == "handled"
    assert handled


@pytest.mark.asyncio
async def test_blocks_when_no_profile(monkeypatch):
    middleware = ProfileRequiredMiddleware()
    handled = False

    async def handler(event, data):
        nonlocal handled
        handled = True
        return "handled"

    monkeypatch.setattr(ProfileRequiredMiddleware, "_requires_profile", classmethod(lambda cls, event: True))

    async def fake_get_profile_none(self, user_id):
        return None

    monkeypatch.setattr("services.profile_service.ProfileService.get_profile", fake_get_profile_none)

    class FakeEvent:
        def __init__(self, from_user=None):
            self.from_user = from_user
            self.message = self

        async def answer(self, *args, **kwargs):
            return None

        async def message_answer(self, *args, **kwargs):
            return None

        async def answer_message(self, *args, **kwargs):
            return None

    data = {"current_user": SimpleNamespace(id=44), "session": SimpleNamespace()}
    result = await middleware(handler, FakeEvent(), data)

    assert result is None
    assert not handled


@pytest.mark.asyncio
async def test_requires_profile_for_verify_callback_and_inline_promo_text(monkeypatch):
    middleware = ProfileRequiredMiddleware()

    async def handler(event, data):
        return "handled"

    async def fake_get_profile(self, user_id):
        return True

    monkeypatch.setattr("services.profile_service.ProfileService.get_profile", fake_get_profile)

    event_with_inline_verify = SimpleNamespace(
        data="verify:start",
        from_user=SimpleNamespace(id=77),
        message=SimpleNamespace(answer=lambda *a, **k: None),
    )
    data = {"session": SimpleNamespace(), "current_user": SimpleNamespace(id=77)}
    assert await middleware(handler, event_with_inline_verify, data) == "handled"

    msg = SimpleNamespace(text="Верификация профиля", from_user=SimpleNamespace(id=78))
    data = {"session": SimpleNamespace(), "current_user": SimpleNamespace(id=78)}
    assert await middleware(handler, msg, data) == "handled"


def test_profile_create_is_not_profile_only_callback():
    callback = CallbackQuery(
        id="query",
        from_user=User(id=1, is_bot=False, first_name="Test"),
        chat_instance="chat",
        data="profile:create",
    )

    assert ProfileRequiredMiddleware._requires_profile(callback) is False


@pytest.mark.asyncio
async def test_banned_user_can_submit_appeal_state(monkeypatch):
    from aiogram.types import Chat, Message

    from middlewares.user import UserSyncMiddleware
    from states.appeal import AppealState

    user = User(id=7, is_bot=False, first_name="Blocked")
    db_user = SimpleNamespace(id=7, username=None, status="BANNED")
    session = SimpleNamespace()
    state = SimpleNamespace(get_state=AsyncMock(return_value=AppealState.enter_text.state))
    event = Message(
        message_id=1,
        date=datetime.now(UTC),
        chat=Chat(id=7, type="private"),
        from_user=user,
        text="valid appeal text",
    )
    handler = AsyncMock(return_value="handled")
    monkeypatch.setattr(
        "middlewares.user.UserRepository.get_or_create",
        AsyncMock(return_value=db_user),
    )

    result = await UserSyncMiddleware()(handler, event, {"event_from_user": user, "session": session, "state": state})

    assert result == "handled"
    handler.assert_awaited_once()
````

## File: tests/test_rate_limit.py
````python
from types import SimpleNamespace

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

from middlewares.rate_limit import RateLimitMiddleware


class UnavailableRedis:
    async def set(self, *_args, **_kwargs):
        raise RedisConnectionError("redis unavailable")


@pytest.mark.asyncio
async def test_rate_limit_allows_update_when_redis_is_unavailable():
    middleware = RateLimitMiddleware(UnavailableRedis())
    handled = False

    async def handler(_event, _data):
        nonlocal handled
        handled = True
        return "handled"

    result = await middleware(handler, object(), {"event_from_user": SimpleNamespace(id=42)})

    assert result == "handled"
    assert handled

    second_result = await middleware(handler, object(), {"event_from_user": SimpleNamespace(id=42)})

    assert second_result is None
    assert handled is True
````

## File: tests/test_registration_progress.py
````python
from handlers.registration import STEP_ORDER, _step_prompt
from keyboards.profile import photo_upload_keyboard


def test_registration_progress_bar_is_always_a_separate_single_line():
    prompt = _step_prompt("preview", "ru")
    lines = prompt.splitlines()

    assert lines[0] == f"📝 Шаг {len(STEP_ORDER)}/{len(STEP_ORDER)}"
    assert lines[1] == "🟩" * len(STEP_ORDER)


def test_photo_upload_keyboard_has_explicit_done_action():
    markup = photo_upload_keyboard("registration:photos_done")

    assert markup.inline_keyboard[0][0].callback_data == "registration:photos_done"
````

## File: tests/test_reports.py
````python
from types import SimpleNamespace

import pytest
from sqlalchemy.exc import IntegrityError

from models import ReportReason, UserStatus
from repositories.report import ReportRepository


class FakeResult:
    def __init__(self, row):
        self._row = row

    def one_or_none(self):
        return self._row


class FakeSavepoint:
    async def __aenter__(self):
        return self

    async def __aexit__(self, _exc_type, _exc, _traceback):
        return False


class FakeReportSession:
    def __init__(self, *, existing=None, report_count=2):
        self.existing = existing
        self.profile = SimpleNamespace(report_count=report_count, is_visible=True, moderation_locked=False)
        self.target_profile = self.profile
        self.user = SimpleNamespace(status=UserStatus.ACTIVE)
        self.added = []
        self.scalar_calls = 0
        self.executed_updates = []

    async def scalar(self, _statement):
        self.scalar_calls += 1
        if self.scalar_calls == 1:
            return self.existing
        return self.target_profile

    async def execute(self, statement):
        self.executed_updates.append(statement)
        if len(self.executed_updates) == 1:
            self.profile.report_count += 1
            return FakeResult(
                SimpleNamespace(
                    report_count=self.profile.report_count,
                    user_id=2,
                    is_visible=True,
                    moderation_locked=False,
                )
            )
        if len(self.executed_updates) == 2:
            self.profile.is_visible = False
            self.profile.moderation_locked = True
            return FakeResult(None)
        if len(self.executed_updates) == 3:
            self.user.status = UserStatus.SUSPENDED
            return FakeResult(None)
        return FakeResult(None)

    async def get(self, _model, _key):
        return self.user

    def add(self, item):
        self.added.append(item)

    def begin_nested(self):
        return FakeSavepoint()

    async def flush(self):
        return None


class FakeDuplicateReportSession(FakeReportSession):
    def __init__(self):
        super().__init__(existing=None, report_count=2)
        self.rollback_called = False
        self.existing = SimpleNamespace(reporter_id=1, target_user_id=2)

    async def scalar(self, _statement):
        self.scalar_calls += 1
        if self.scalar_calls == 1:
            return None
        return self.existing

    async def flush(self):
        raise IntegrityError("duplicate key value violates unique constraint", {}, None)


class FakePendingReportSession:
    def __init__(self):
        self.statement = None

    async def scalars(self, statement):
        self.statement = statement
        return SimpleNamespace(all=lambda: [])


@pytest.mark.asyncio
async def test_report_threshold_hides_profile_and_suspends_user():
    session = FakeReportSession(report_count=2)

    _, created, threshold_reached = await ReportRepository(session).add(1, 2, ReportReason.SPAM, threshold=3)

    assert created and threshold_reached
    assert session.added[0].target_user_id == 2
    assert len(session.executed_updates) == 3
    assert not session.target_profile.is_visible
    assert session.target_profile.moderation_locked
    assert session.user.status == UserStatus.SUSPENDED


@pytest.mark.asyncio
async def test_duplicate_report_does_not_increment_report_count_or_raise():
    session = FakeDuplicateReportSession()

    existing_report, created, threshold_reached = await ReportRepository(session).add(
        1,
        2,
        ReportReason.SPAM,
        threshold=3,
    )

    assert not created
    assert not threshold_reached
    assert existing_report is not None


@pytest.mark.asyncio
async def test_report_above_threshold_does_not_repeat_suspension_side_effects():
    session = FakeReportSession(report_count=3)

    _, created, threshold_reached = await ReportRepository(session).add(1, 2, ReportReason.SPAM, threshold=3)

    assert created
    assert not threshold_reached
    assert len(session.executed_updates) == 1


@pytest.mark.asyncio
async def test_pending_reports_filter_out_other_moderators_claims():
    session = FakePendingReportSession()

    await ReportRepository(session).pending(moderator_id=202)

    statement = str(session.statement)
    assert "assigned_to" in statement
    assert 202 in session.statement.compile().params.values()
````

## File: tools/reset_test_data.py
````python
# DEVELOPMENT/ALPHA TOOL ONLY
# This script is dangerous and must only be used in development/testing environments.
# It performs destructive deletes in PostgreSQL and Redis. Do NOT run in production.

"""
Usage examples:
  python -m tools.reset_test_data --user 12345
  python -m tools.reset_test_data --all --yes

Behaviour:
- Allows execution only when ENV or ENVIRONMENT is set to 'development', 'dev' or 'test'.
- If ENV/ENVIRONMENT equals 'production' the script exits immediately.
- Deletions are performed inside a single async DB transaction for consistency.
- Redis keys cleared: recommendation_queue:<user_id>, keys matching f"fsm*{user_id}*",
  rate:<user_id> and related patterns.
"""

import argparse
import asyncio
import os
import socket
import sys
from urllib.parse import urlparse

from sqlalchemy import delete, or_

# Avoid importing this module from runtime code: this file must not be executed by the bot.
if __name__ != "__main__":
    __all__ = []


def _ensure_env_allows_run() -> None:
    env = os.environ.get("ENV") or os.environ.get("ENVIRONMENT") or ""
    env_l = env.lower()
    if env_l in ("production", "prod"):
        print(
            "Refusing to run in production environment (ENV/ENVIRONMENT=production).",
            file=sys.stderr,
        )
        sys.exit(2)
    if env_l not in ("development", "dev", "test"):
        print(
            f"Danger: ENV/ENVIRONMENT must be one of: development, dev, test. Got: {env!r}",
            file=sys.stderr,
        )
        sys.exit(3)


def _decode_key(value: object) -> str:
    if isinstance(value, bytes | bytearray):
        return value.decode()
    return str(value)


async def _clear_redis_for_user(redis, user_id: int) -> None:
    keys_to_del = [f"recommendation_queue:{user_id}", f"rate:{user_id}"]
    pattern1 = f"*:{user_id}*"

    async for key in redis.scan_iter(match=pattern1):
        ks = _decode_key(key)
        if (
            f":{user_id}" in ks
            or ks.startswith("fsm:")
            or ks.startswith("rate:")
            or ks.startswith("recommendation_queue:")
        ):
            keys_to_del.append(ks)

    async for key in redis.scan_iter(match=f"fsm:*{user_id}*"):
        ks = _decode_key(key)
        keys_to_del.append(ks)

    keys_to_del = list(dict.fromkeys(keys_to_del))
    if not keys_to_del:
        return
    await redis.delete(*keys_to_del)
    print("Deleted Redis keys:", keys_to_del)


async def _clear_redis_all(redis) -> None:
    keys: list[str] = []
    for pattern in ("recommendation_queue:*", "rate:*", "fsm:*"):
        async for key in redis.scan_iter(match=pattern):
            keys.append(_decode_key(key))
    if keys:
        await redis.delete(*keys)
    print("Deleted Redis keys (count):", len(keys))


async def _reset_user(session_factory, redis_url: str, user_id: int) -> None:
    from config import get_settings
    from database.connection import make_session_factory
    from models.admin_log import AdminLog
    from models.appeal import Appeal
    from models.block import Block
    from models.confession import Confession
    from models.dislike import Dislike
    from models.like import Like
    from models.match import Match
    from models.profile import Profile
    from models.recommendation_view import RecommendationView
    from models.report import Report
    from models.trust import ModerationCase, PhotoModeration, TrustScoreEvent, VerificationRequest
    from models.user import User

    settings = get_settings()
    factory = make_session_factory(settings)

    async with factory() as session:
        async with session.begin():
            await session.execute(
                delete(RecommendationView).where(
                    or_(
                        RecommendationView.viewer_id == user_id,
                        RecommendationView.candidate_id == user_id,
                    )
                )
            )
            await session.execute(
                delete(TrustScoreEvent).where(TrustScoreEvent.user_id == user_id)
            )
            await session.execute(
                delete(VerificationRequest).where(VerificationRequest.user_id == user_id)
            )
            await session.execute(
                delete(Appeal).where(Appeal.user_id == user_id)
            )
            await session.execute(
                delete(ModerationCase).where(ModerationCase.user_id == user_id)
            )
            await session.execute(delete(PhotoModeration).where(PhotoModeration.user_id == user_id))
            await session.execute(
                delete(Confession).where(
                    Confession.recipient_id == user_id
                )
            )
            await session.execute(
                delete(AdminLog).where(
                    or_(
                        AdminLog.admin_id == user_id,
                        AdminLog.target_user_id == user_id,
                    )
                )
            )
            await session.execute(
                delete(Report).where(
                    or_(
                        Report.reporter_id == user_id,
                        Report.target_user_id == user_id,
                    )
                )
            )
            await session.execute(
                delete(Block).where(
                    or_(
                        Block.blocker_id == user_id,
                        Block.blocked_id == user_id,
                    )
                )
            )
            await session.execute(
                delete(Match).where(
                    or_(
                        Match.user1_id == user_id,
                        Match.user2_id == user_id,
                    )
                )
            )
            await session.execute(
                delete(Like).where(
                    or_(
                        Like.from_user_id == user_id,
                        Like.to_user_id == user_id,
                    )
                )
            )
            await session.execute(
                delete(Dislike).where(
                    or_(
                        Dislike.from_user_id == user_id,
                        Dislike.to_user_id == user_id,
                    )
                )
            )
            await session.execute(delete(Profile).where(Profile.user_id == user_id))
            await session.execute(delete(User).where(User.id == user_id))
        await session.commit()

    import redis.asyncio as aioredis

    r = aioredis.Redis.from_url(redis_url)
    try:
        await _clear_redis_for_user(r, user_id)
    finally:
        await r.aclose()

    print(f"Reset completed for user {user_id}")


async def _reset_all(session_factory, redis_url: str) -> None:
    from config import get_settings
    from database.connection import make_session_factory
    from models.admin_log import AdminLog
    from models.appeal import Appeal
    from models.block import Block
    from models.confession import Confession, ConfessionDailyLimit
    from models.dislike import Dislike
    from models.like import Like
    from models.match import Match
    from models.profile import Profile
    from models.recommendation_view import RecommendationView
    from models.report import Report
    from models.trust import ModerationCase, PhotoModeration, TrustScoreEvent, VerificationRequest
    from models.user import User

    settings = get_settings()
    factory = make_session_factory(settings)

    async with factory() as session:
        async with session.begin():
            await session.execute(delete(RecommendationView))
            await session.execute(delete(TrustScoreEvent))
            await session.execute(delete(VerificationRequest))
            await session.execute(delete(Appeal))
            await session.execute(delete(ModerationCase))
            await session.execute(delete(PhotoModeration))
            await session.execute(delete(Confession))
            await session.execute(delete(ConfessionDailyLimit))
            await session.execute(delete(AdminLog))
            await session.execute(delete(Report))
            await session.execute(delete(Block))
            await session.execute(delete(Match))
            await session.execute(delete(Like))
            await session.execute(delete(Dislike))
            await session.execute(delete(Profile))
            await session.execute(delete(User))
        await session.commit()

    import redis.asyncio as aioredis

    r = aioredis.Redis.from_url(redis_url)
    try:
        await _clear_redis_all(r)
    finally:
        await r.aclose()

    print("Full reset completed")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reset test data (development only)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--user", type=int, help="Telegram user ID to reset")
    group.add_argument("--all", action="store_true", help="Reset all test data (destructive)")
    parser.add_argument("--yes", action="store_true", help="Assume yes for confirmation prompts")
    return parser.parse_args()


def _db_host_resolvable(database_url: str | None) -> bool:
    if not database_url:
        return False
    # Attempt to parse common SQLAlchemy/DSN formats
    try:
        parsed = urlparse(database_url)
        host = parsed.hostname
        if not host:
            # Try fallback: database_url might be like 'postgres:5432/db' without scheme
            if ":" in database_url:
                host = database_url.split(":")[0]
        if not host:
            return False
        # Try to resolve DNS / hostname
        try:
            socket.getaddrinfo(host, None)
            return True
        except socket.gaierror:
            return False
    except Exception:
        return False


def main() -> None:
    _ensure_env_allows_run()
    args = _parse_args()

    redis_url = os.environ.get("REDIS_URL") or os.environ.get("REDIS") or None
    from config import get_settings

    settings = get_settings()

    if not redis_url:
        redis_url = settings.redis_url

    database_url = settings.database_url

    # If DB host is not resolvable from this environment, provide a clearer error
    if not _db_host_resolvable(database_url):
        print(
            "Cannot resolve database host from DATABASE_URL. This usually means you're running the tool on the host",
            "but the database is only available inside Docker (hostname like 'postgres').",
            file=sys.stderr,
        )
        print("Options:", file=sys.stderr)
        print(
            "  * Run the tool inside the bot container where service hostnames are resolvable:",
            file=sys.stderr,
        )
        print(
            "      docker compose -f project1/docker-compose.yml exec -e ENV=development "
            "bot python -m tools.reset_test_data --all --yes",
            file=sys.stderr,
        )
        print(
            "  * Or set DATABASE_URL to a reachable address from your host "
            "(e.g. localhost:5432 if you published the port)",
            file=sys.stderr,
        )
        sys.exit(4)

    if args.all and not args.yes:
        confirm = input("Type 'CONFIRM_RESET' to proceed: ")
        if confirm.strip() != "CONFIRM_RESET":
            print("Aborted by user")
            sys.exit(1)

    async def _run() -> None:
        if args.user:
            await _reset_user(None, redis_url, args.user)
        elif args.all:
            await _reset_all(None, redis_url)

    asyncio.run(_run())


if __name__ == "__main__":
    main()
````

## File: utils/admin_roles.py
````python
from models.user import UserRole


def normalize_admin_role(role: UserRole | str | None) -> UserRole:
    if role is None:
        return UserRole.USER
    if isinstance(role, str):
        try:
            return UserRole(role)
        except ValueError:
            return UserRole.USER
    return role


def resolve_admin_role(
    user_id: int,
    *,
    owner_admin_id: int | None = None,
    admin_ids: set[int] | None = None,
    user_role: UserRole | None = None,
) -> UserRole:
    if owner_admin_id is not None and user_id == owner_admin_id:
        return UserRole.OWNER
    stored_role = normalize_admin_role(user_role)
    if stored_role != UserRole.USER:
        return stored_role
    if admin_ids and user_id in admin_ids:
        return UserRole.MODERATOR
    return UserRole.USER


def can_manage_admins(role: UserRole) -> bool:
    return role == UserRole.OWNER


def can_review_moderator_decisions(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_access_moderation(role: UserRole) -> bool:
    return role in {
        UserRole.MODERATOR,
        UserRole.HEAD_MODERATOR,
        UserRole.CHIEF_MODERATOR,
        UserRole.OWNER,
        UserRole.ADMIN,
    }


def can_ban(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_override_case(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_release_cases(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_unban(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_unfreeze(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_view_all_profiles(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_view_audit_history(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}


def can_override_appeal_assignment(role: UserRole) -> bool:
    return role in {UserRole.OWNER, UserRole.CHIEF_MODERATOR, UserRole.HEAD_MODERATOR}
````

## File: utils/document_links.py
````python
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

DOCUMENT_LABELS = {
    "terms": "📄 Условия использования",
    "privacy": "🔐 Политика конфиденциальности",
    "community": "🛡 Правила сообщества",
    "safety": "🚨 Безопасность знакомств",
    "moderation": "⚖️ Модерация и апелляции",
    "alpha": "📌 Альфа-статус",
}

DOCUMENT_LABELS_RO = {
    "terms": "📄 Termeni de utilizare",
    "privacy": "🔐 Politica de confidențialitate",
    "community": "🛡 Regulile comunității",
    "safety": "🚨 Siguranța întâlnirilor",
    "moderation": "⚖️ Moderare și contestații",
    "alpha": "📌 Statut alfa",
}


def documents_keyboard(*keys: str, include_continue: bool = False, locale: str = "ru") -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    from config import get_settings

    settings = get_settings()
    current: list[InlineKeyboardButton] = []
    for key in keys:
        url = settings.document_urls[key]
        labels = DOCUMENT_LABELS_RO if locale == "ro" else DOCUMENT_LABELS
        current.append(InlineKeyboardButton(text=labels[key], url=url))
        if len(current) == 2:
            rows.append(current)
            current = []
    if current:
        rows.append(current)
    if include_continue:
        continue_text = "✅ Continuă" if locale == "ro" else "✅ Продолжить"
        rows.append([InlineKeyboardButton(text=continue_text, callback_data="legal:accept")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
````

## File: utils/legal.py
````python
from __future__ import annotations

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from services.localization import LocalizationService
from services.profile_service import ProfileService
from utils.document_links import documents_keyboard

CONSENT_KEY = "legal_consent"

LEGAL_NOTICE_TEXT = (
    "👋 MeAnima — это сервис знакомств в формате Telegram-бота.\n\n"
    "Это закрытая альфа: часть функциональности ещё дорабатывается, а часть процессов только запускается.\n\n"
    "Перед использованием важно ознакомиться с правилами, политикой конфиденциальности и условиями сервиса.\n\n"
    "Мы используем MeAnima, чтобы знакомиться и общаться в безопасной среде в рамках закрытого тестирования."
)


def legal_notice_text(locale: str = "ru") -> str:
    return LocalizationService().get("legal_notice", locale)


async def consent_already_given(state: FSMContext) -> bool:
    data = await state.get_data()
    return bool(data.get(CONSENT_KEY))


async def ensure_consent_for_new_user(
    state: FSMContext,
    session: AsyncSession,
    user_id: int,
    message: Message | CallbackQuery,
    locale: str = "ru",
) -> bool:
    if await consent_already_given(state):
        return True

    if await ProfileService(session).get_profile(user_id) is not None:
        await state.update_data(**{CONSENT_KEY: True})
        return True

    if isinstance(message, CallbackQuery):
        await message.answer()
        await message.message.answer(
            legal_notice_text(locale),
            reply_markup=documents_keyboard(
                "terms",
                "privacy",
                "community",
                "safety",
                "moderation",
                "alpha",
                include_continue=True,
                locale=locale,
            ),
        )
    else:
        await message.answer(
            legal_notice_text(locale),
            reply_markup=documents_keyboard(
                "terms",
                "privacy",
                "community",
                "safety",
                "moderation",
                "alpha",
                include_continue=True,
                locale=locale,
            ),
        )
    return False


async def accept_consent(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(**{CONSENT_KEY: True})
    await callback.answer()
````

## File: validators/profile_validator.py
````python
import re
from collections.abc import Mapping
from typing import Any

from services.localization import LocalizationService


class ProfileValidationError(Exception):
    def __init__(self, errors: dict[str, str]) -> None:
        self.errors = errors
        super().__init__("Profile validation failed")


_BLOCKED_WORDS = {
    "fuck",
    "shit",
    "bitch",
    "сука",
    "пизд",
    "хуй",
    "бляд",
    "ебан",
    "чмыр",
}


def validate_profile_payload(
    payload: Mapping[str, Any], *, photo_file_ids: list[str] | None = None, locale: str = "ru"
) -> None:
    localizer = LocalizationService()

    def error(key: str) -> str:
        return localizer.get(key, locale)

    errors: dict[str, str] = {}

    name = str(payload.get("name") or "").strip()
    if not name:
        errors["name"] = error("validation_name_required")
    elif not 2 <= len(name) <= 32:
        errors["name"] = error("validation_name_length")
    elif not re.match(r"^[A-Za-zА-Яа-яЁёІЇієїҐґ'’\- ]+$", name):
        errors["name"] = error("validation_name_characters")
    else:
        normalized = name.casefold()
        if any(word in normalized for word in _BLOCKED_WORDS):
            errors["name"] = error("validation_name_blocked")

    age_value = payload.get("age")
    if age_value is None:
        errors["age"] = error("validation_age_required")
    else:
        try:
            age = int(age_value)
        except (TypeError, ValueError):
            errors["age"] = error("validation_age_number")
        else:
            if not 16 <= age <= 99:
                errors["age"] = error("validation_age_range")

    district = str(payload.get("district") or "").strip()
    if not district:
        errors["district"] = error("validation_district_required")
    elif len(district) > 64:
        errors["district"] = error("validation_district_length")

    institution = str(payload.get("institution") or "").strip()
    if not institution:
        errors["institution"] = error("validation_institution_required")
    elif len(institution) > 128:
        errors["institution"] = error("validation_institution_length")

    gender = payload.get("gender")
    if gender not in {"MALE", "FEMALE"}:
        errors["gender"] = error("validation_gender_required")

    target_gender = payload.get("target_gender")
    if target_gender not in {"MALE", "FEMALE", "ALL"}:
        errors["target_gender"] = error("validation_target_gender")

    bio = str(payload.get("bio") or "").strip()
    if not bio:
        errors["bio"] = error("validation_bio_required")
    elif not 10 <= len(bio) <= 500:
        errors["bio"] = error("validation_bio_length")

    if photo_file_ids is not None:
        if not photo_file_ids:
            errors["photos"] = error("validation_photos_required")
        elif len(photo_file_ids) > 3:
            errors["photos"] = error("validation_photos_limit")

    if errors:
        raise ProfileValidationError(errors)
````

## File: .gitignore
````
.env
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
logs/
.venv/
venv/
.vscode/
.idea/
*.sqlite
*.sqlite3
*.db
*.db-journal
*.log
.coverage
htmlcov/
backups/
````

## File: docker-compose.yml
````yaml
services:
  bot:
    build: .
    restart: unless-stopped
    env_file: .env
    volumes:
      - ./:/app:cached
      - ${PHOTO_SAFETY_MODELS_DIR:-./models}:/models:ro
    depends_on:
      postgres: { condition: service_healthy }
      redis: { condition: service_healthy }
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB:?POSTGRES_DB must be set in .env}
      POSTGRES_USER: ${POSTGRES_USER:?POSTGRES_USER must be set in .env}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?POSTGRES_PASSWORD must be set in .env}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER}"]
      interval: 5s
      timeout: 5s
      retries: 5
  redis:
    image: redis:7-alpine
    command: ["redis-server", "--appendonly", "yes", "--appendfsync", "everysec", "--requirepass", "${REDIS_PASSWORD:?REDIS_PASSWORD must be set in .env}"]
    environment:
      REDIS_PASSWORD: ${REDIS_PASSWORD:?REDIS_PASSWORD must be set in .env}
    volumes:
      - redisdata:/data
    healthcheck:
      test: ["CMD-SHELL", "redis-cli -a \"$$REDIS_PASSWORD\" ping"]
      interval: 5s
      timeout: 5s
      retries: 5
volumes:
  pgdata:
  redisdata:
````

## File: bot/factory.py
````python
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.token import TokenValidationError
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from config import Settings
from handlers import routers
from middlewares.db import DbSessionMiddleware
from middlewares.i18n import FSMI18nMiddleware
from middlewares.profile_required import ProfileRequiredMiddleware
from middlewares.rate_limit import RateLimitMiddleware
from middlewares.user import UserSyncMiddleware

logger = logging.getLogger(__name__)


def create_dispatcher(
    settings: Settings, factory: async_sessionmaker[AsyncSession], redis: Redis
) -> tuple[Bot | None, Dispatcher]:
    """
    Create and return (bot, dispatcher). If BOT_TOKEN is invalid, return (None, dispatcher)
    and log a warning — caller should handle offline mode.
    """
    try:
        bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    except TokenValidationError:
        logger.warning("BOT_TOKEN appears invalid — running in offline mode (no Telegram connection).")
        bot = None
    # The same Redis connection backs FSM expiry and notification deduplication.
    dp = Dispatcher(
        storage=RedisStorage(
            redis=redis,
            state_ttl=settings.fsm_state_ttl_seconds,
            data_ttl=settings.fsm_state_ttl_seconds,
        )
    )
    if bot is not None:
        bot.notification_redis = redis
    dp.update.outer_middleware(DbSessionMiddleware(factory))
    dp.update.outer_middleware(UserSyncMiddleware())
    dp.update.outer_middleware(FSMI18nMiddleware())
    dp.update.outer_middleware(ProfileRequiredMiddleware())
    dp.update.outer_middleware(RateLimitMiddleware(redis))
    for router in routers:
        dp.include_router(router)
    dp["settings"] = settings
    return bot, dp
````

## File: handlers/callback_fallback.py
````python
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from keyboards.menu import main_menu

router = Router()


@router.callback_query()
async def outdated_callback(callback: CallbackQuery) -> None:
    """Acknowledge buttons retained in old Telegram messages after UI changes."""
    await callback.answer("Эта кнопка устарела. Откройте актуальный раздел меню.", show_alert=True)


@router.message(StateFilter(None), F.text, ~F.text.startswith("/"))
async def no_state_message(message: Message) -> None:
    await message.answer(
        "Я не нашёл активного действия для этого сообщения. Откройте нужный раздел меню.",
        reply_markup=main_menu(),
    )
````

## File: handlers/verification.py
````python
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from keyboards.menu import MENU_VERIFICATION_LABELS
from models import VerificationStatus
from repositories.trust import TrustRepository
from services.localization import LocalizationService
from services.notification_service import InternalNotificationService, NotificationService
from services.profile_service import ProfileService
from services.verification_service import VerificationService
from states.verification import VerificationState
from utils.admin_ui import compact_display_id, user_display_name

router = Router()
localizer = LocalizationService()


def verification_navigation_keyboard(show_retake: bool = False, locale: str = "ru") -> InlineKeyboardMarkup:
    buttons = []
    if show_retake:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=localizer.get("verification_retry", locale), callback_data="verification:start_upload"
                )
            ]
        )
    buttons.append([
        InlineKeyboardButton(text=localizer.get("menu_profile", locale), callback_data="promo:my_profile"),
        InlineKeyboardButton(text=localizer.get("verification_home", locale), callback_data="verification:home"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data == "verification:home")
async def verification_home(callback: CallbackQuery, locale: str = "ru") -> None:
    await callback.answer()
    from keyboards.menu import main_menu
    await callback.message.answer(localizer.get("verification_home", locale), reply_markup=main_menu(locale))


@router.callback_query(F.data == "verification:start_upload")
async def verification_start_upload(callback: CallbackQuery, state: FSMContext, locale: str = "ru") -> None:
    await state.set_state(VerificationState.waiting_video)
    await callback.answer()
    await callback.message.answer(
        localizer.get("verification_retry_prompt", locale)
    )


@router.message(F.text.in_(MENU_VERIFICATION_LABELS))
async def verification_start(message: Message, state: FSMContext, session: AsyncSession, locale: str = "ru") -> None:
    profile = await ProfileService(session).get_profile(message.from_user.id)
    if profile is None:
        await message.answer(
            localizer.get("verification_profile_required", locale),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=localizer.get("verification_create_profile", locale), callback_data="profile:create"
                        )
                    ]
                ]
            ),
        )
        return

    status_value = getattr(profile.verification_status, "value", profile.verification_status)
    if status_value == VerificationStatus.VERIFIED.value:
        await message.answer(
            localizer.get("verification_verified", locale),
            reply_markup=verification_navigation_keyboard(show_retake=False, locale=locale),
        )
        return

    if status_value == VerificationStatus.PENDING.value:
        await message.answer(
            localizer.get("verification_pending", locale),
            reply_markup=verification_navigation_keyboard(show_retake=False, locale=locale),
        )
        return

    await state.set_state(VerificationState.waiting_video)
    await message.answer(
        localizer.get("verification_start", locale)
    )


@router.message(VerificationState.waiting_video, F.video_note)
async def verification_video(
    message: Message, state: FSMContext, session: AsyncSession, settings: Settings, locale: str = "ru"
) -> None:
    try:
        request = await VerificationService(session).submit(message.from_user.id, message.video_note.file_id)
    except ValueError:
        # Friendly message for known validation errors (already verified / pending request)
        await state.clear()
        await message.answer(localizer.get("verification_error_generic", locale))
        return

    await state.clear()
    await InternalNotificationService(message.bot, settings).send_moderation_event(
        "Новая verification request",
        user_id=request.user_id,
        username=message.from_user.username,
        reason="verification request",
        case_id=str(request.id),
        target_callback=f"mycase:verify:{request.id}",
        details=f"Verification case: {compact_display_id(request.id)}",
    )
    notifier = NotificationService(message.bot)
    for admin_id in settings.admin_ids:
        await notifier.safe_send(
            admin_id,
            (
                f"🛡 Новая верификация {compact_display_id(request.id)}\n"
                f"Пользователь: {user_display_name(request.user_id)}"
            ),
            dedupe_key=f"verification:{request.id}",
        )
        await TrustRepository(session).log(
            admin_id,
            "verification_notice_sent",
            target_type="verification",
            target_id=str(request.id),
            metadata={"user_id": request.user_id},
        )
    await message.answer(
        localizer.get("verification_submitted", locale)
    )


@router.message(VerificationState.waiting_video)
async def verification_not_video(message: Message, locale: str = "ru") -> None:
    await message.answer(localizer.get("verification_video_required", locale))
````

## File: middlewares/profile_required.py
````python
from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, TelegramObject

from services.localization import LocalizationService
from services.profile_service import ProfileService
from states.appeal import AppealState

logger = logging.getLogger(__name__)


class ProfileRequiredMiddleware(BaseMiddleware):
    """Stops profile-only actions in one place and offers registration."""

    message_actions = {
        "💘 Знакомства", "💘 Смотреть анкеты", "Смотреть анкеты",
        "💕 Мои симпатии", "❤️ Симпатии",
        "🛡 Верификация", "Верификация профиля", "💌 Признание",
        "Посмотреть анкеты", "Показать анкеты", "Открыть анкеты",
        "👤 Моя анкета", "Моя анкета"
    }
    callback_prefixes = (
        "like:", "comment:", "skip:", "block:", "report:", "report_reason:",
        "profile:", "verify:", "photo:"
    )

    @classmethod
    def _requires_profile(cls, event: TelegramObject) -> bool:
        if isinstance(event, Message):
            return (event.text or "") in cls.message_actions
        if isinstance(event, CallbackQuery):
            data = event.data or ""
            return data != "profile:create" and data.startswith(cls.callback_prefixes)
        return False

    @staticmethod
    def _keyboard() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="✨ Создать анкету", callback_data="profile:create")]]
        )

    async def __call__(
        self, handler: Callable[..., Awaitable[Any]], event: TelegramObject, data: dict[str, Any]
    ) -> Any:
        requires_profile = self._requires_profile(event)
        if isinstance(event, Message):
            localizer = data.get("localizer") or LocalizationService()
            message_actions = set(self.message_actions)
            for locale in ("ru", "ro"):
                message_actions.update(
                    localizer.get(key, locale)
                    for key in ("menu_dating", "menu_likes", "menu_profile", "menu_verification", "menu_confession")
                )
            requires_profile = (event.text or "") in message_actions
        if not requires_profile:
            return await handler(event, data)
        # Prefer the synchronized DB user set by UserSyncMiddleware; fall back to event.from_user
        current_user = data.get("current_user")
        session = data.get("session")
        user_id = None
        if current_user is not None:
            # current_user is a DB model with an `id` attribute
            user_id = getattr(current_user, "id", None)
        else:
            # Prefer an explicit event_from_user in data (some middlewares set this), then event.from_user
            event_user = data.get("event_from_user") or getattr(event, "from_user", None)
            if event_user is not None:
                user_id = getattr(event_user, "id", None)
        # If we don't have session or user id, let the handler run (can't enforce)
        from_user = getattr(event, "from_user", None)
        from_user_id = getattr(from_user, "id", None) if from_user is not None else None
        logger.debug(
            "ProfileRequiredMiddleware invoked: event_type=%s, current_user_id=%s, from_user_id=%s, session_present=%s",
            type(event).__name__, getattr(current_user, "id", None), from_user_id, session is not None,
        )
        if user_id is None or session is None:
            logger.debug("ProfileRequiredMiddleware: insufficient context, passing through")
            return await handler(event, data)
        state = data.get("state")
        current_state = await state.get_state() if state is not None else None
        if isinstance(event, Message) and (
            (event.text or "") == "🆘 Апелляция" or current_state == AppealState.enter_text.state
        ):
            return await handler(event, data)
        # If the profile exists, continue; otherwise prompt to create one
        profile = await ProfileService(session).get_profile(user_id)
        logger.debug("ProfileRequiredMiddleware: profile lookup for user_id=%s -> %s", user_id, bool(profile))
        if profile:
            return await handler(event, data)
        text = "📝 Для начала нужно создать анкету.\n\nБез неё мы не сможем подобрать подходящих людей."
        if isinstance(event, CallbackQuery):
            await event.answer()
            await event.message.answer(text, reply_markup=self._keyboard())
        else:
            await event.answer(text, reply_markup=self._keyboard())
        return None
````

## File: models/trust.py
````python
import enum
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base, TimestampMixin, UUIDPKMixin


class VerificationDecision(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    RETAKE_REQUESTED = "RETAKE_REQUESTED"


class ModerationCaseType(str, enum.Enum):
    REPORT_THRESHOLD = "REPORT_THRESHOLD"
    NSFW = "NSFW"
    NO_FACE = "NO_FACE"
    PHOTO_RETAKE = "PHOTO_RETAKE"


class ModerationCaseStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class VerificationRequest(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "verification_requests"
    __table_args__ = (
        Index(
            "uq_verification_requests_one_pending_per_user",
            "user_id",
            unique=True,
            postgresql_where="status = 'PENDING'",
        ),
    )
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    video_file_id: Mapped[str] = mapped_column(String(255))
    status: Mapped[VerificationDecision] = mapped_column(
        Enum(VerificationDecision), default=VerificationDecision.PENDING, index=True
    )
    assigned_to: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    assigned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    admin_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)


class ModerationCase(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "moderation_cases"
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    case_type: Mapped[ModerationCaseType] = mapped_column(Enum(ModerationCaseType), index=True)
    status: Mapped[ModerationCaseStatus] = mapped_column(
        Enum(ModerationCaseStatus), default=ModerationCaseStatus.PENDING, index=True
    )
    assigned_to: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    assigned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    source_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    admin_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    __table_args__ = (
        Index(
            "uq_moderation_cases_one_active_event",
            "user_id",
            "case_type",
            func.coalesce(source_id, ""),
            unique=True,
            postgresql_where="status IN ('PENDING', 'IN_PROGRESS')",
        ),
    )


class PhotoModeration(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "photo_moderations"
    __table_args__ = (UniqueConstraint("user_id", "content_hash", name="uq_photo_moderations_user_hash"),)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    photo_file_id: Mapped[str] = mapped_column(String(255), index=True)
    content_hash: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    provider: Mapped[str] = mapped_column(String(64), default="heuristic")
    nsfw_score: Mapped[float] = mapped_column(Float, default=0.0)
    face_detected: Mapped[bool] = mapped_column(default=True)


class TrustScoreEvent(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "trust_score_events"
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    delta: Mapped[int] = mapped_column()
    reason: Mapped[str] = mapped_column(String(64), index=True)
    reference_type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    reference_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
````

## File: repositories/appeal.py
````python
import uuid

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Appeal, AppealStatus


class AppealRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: int, text: str) -> Appeal:
        appeal = Appeal(user_id=user_id, text=text)
        try:
            nested = getattr(self.session, "begin_nested", None)
            if nested is None:
                self.session.add(appeal)
                await self.session.flush()
            else:
                async with nested():
                    self.session.add(appeal)
                    await self.session.flush()
        except IntegrityError:
            existing = await self.active_for_user(user_id)
            if existing is not None:
                return existing
            raise
        return appeal

    async def get(self, appeal_id: uuid.UUID) -> Appeal | None:
        return await self.session.get(Appeal, appeal_id)

    async def active_for_user(self, user_id: int) -> Appeal | None:
        statement = (
            select(Appeal)
            .where(Appeal.user_id == user_id, Appeal.status == AppealStatus.PENDING)
            .order_by(Appeal.created_at.desc())
        )
        return await self.session.scalar(statement)

    async def pending(self, moderator_id: int | None = None) -> list[Appeal]:
        statement = select(Appeal).where(Appeal.status == AppealStatus.PENDING)
        if moderator_id is not None:
            statement = statement.where((Appeal.assigned_to == moderator_id) | (Appeal.assigned_to.is_(None)))
        statement = statement.order_by(Appeal.created_at)
        return list((await self.session.scalars(statement)).all())

    async def claim(self, appeal_id: uuid.UUID, moderator_id: int) -> Appeal | None:
        result = await self.session.execute(
            update(Appeal)
            .where(
                Appeal.id == appeal_id,
                Appeal.status == AppealStatus.PENDING,
                (Appeal.assigned_to.is_(None) | (Appeal.assigned_to == moderator_id)),
            )
            .values(assigned_to=moderator_id)
            .returning(Appeal)
        )
        appeal = result.scalar_one_or_none()
        if appeal is not None:
            return appeal
        current = await self.get(appeal_id)
        if current is None or current.status != AppealStatus.PENDING:
            return None
        if current.assigned_to not in {None, moderator_id}:
            return None
        current.assigned_to = moderator_id
        await self.session.flush()
        return current

    async def release(self, appeal_id: uuid.UUID, moderator_id: int, *, override: bool = False) -> Appeal | None:
        conditions = [
            Appeal.id == appeal_id,
            Appeal.status == AppealStatus.PENDING,
            Appeal.assigned_to.is_not(None),
        ]
        if not override:
            conditions.append(Appeal.assigned_to == moderator_id)
        result = await self.session.execute(
            update(Appeal)
            .where(*conditions)
            .values(assigned_to=None)
            .returning(Appeal)
        )
        return result.scalar_one_or_none()

    async def resolve(self, appeal_id: uuid.UUID, status: AppealStatus, admin_id: int) -> Appeal | None:
        result = await self.session.execute(
            update(Appeal)
            .where(Appeal.id == appeal_id, Appeal.status == AppealStatus.PENDING)
            .values(
                status=status,
                admin_id=admin_id,
                reviewed_at=__import__("datetime").datetime.now(
                    __import__("datetime").timezone.utc
                ),
            )
            .returning(Appeal)
        )
        return result.scalar_one_or_none()
````

## File: repositories/report.py
````python
from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Profile, Report, ReportReason, ReportStatus, User, UserStatus


class ReportRepository:
    def __init__(self, session: AsyncSession) -> None: self.session = session
    async def add(
        self,
        reporter_id: int,
        target_id: int,
        reason: ReportReason,
        *,
        threshold: int = 3,
        evidence_snapshot: dict[str, object] | None = None,
    ) -> tuple[Report, bool, bool]:
        existing = await self.session.scalar(
            select(Report).where(Report.reporter_id == reporter_id, Report.target_user_id == target_id)
        )
        if existing is not None:
            return existing, False, False

        try:
            async with self.session.begin_nested():
                report = Report(
                    reporter_id=reporter_id,
                    target_user_id=target_id,
                    reason=reason,
                    evidence_snapshot=evidence_snapshot,
                )
                self.session.add(report)
                await self.session.flush()

                updated_profile = await self.session.execute(
                    update(Profile)
                    .where(Profile.user_id == target_id)
                    .values(report_count=Profile.report_count + 1)
                    .returning(Profile.user_id, Profile.report_count, Profile.is_visible, Profile.moderation_locked)
                )
                row = updated_profile.one_or_none()
                threshold_reached = False
                if row is not None:
                    new_report_count = int(row.report_count)
                    # Only the transaction that crosses the threshold owns the
                    # suspension and moderation-case side effect.
                    threshold_reached = new_report_count == threshold
                    if threshold_reached:
                        await self.session.execute(
                            update(Profile)
                            .where(
                                Profile.user_id == target_id,
                                Profile.is_visible.is_(True),
                                Profile.moderation_locked.is_(False),
                            )
                            .values(is_visible=False, moderation_locked=True)
                        )
                        await self.session.execute(
                            update(User)
                            .where(User.id == target_id, User.status != UserStatus.SUSPENDED)
                            .values(status=UserStatus.SUSPENDED)
                        )
        except IntegrityError:
            existing = await self.session.scalar(
                select(Report).where(Report.reporter_id == reporter_id, Report.target_user_id == target_id)
            )
            return existing, False, False
        return report, True, threshold_reached
    async def pending(self, moderator_id: int | None = None) -> list[Report]:
        statement = select(Report).where(Report.status == ReportStatus.PENDING)
        if moderator_id is not None:
            statement = statement.where((Report.assigned_to == moderator_id) | (Report.assigned_to.is_(None)))
        statement = statement.order_by(Report.created_at)
        return list((await self.session.scalars(statement)).all())

    async def get(self, report_id):
        return await self.session.get(Report, report_id)

    async def claim(self, report_id, moderator_id: int) -> Report | None:
        """Claim a report for processing."""
        result = await self.session.execute(
            update(Report)
            .where(
                Report.id == report_id,
                Report.status == ReportStatus.PENDING,
                (Report.assigned_to.is_(None) | (Report.assigned_to == moderator_id)),
            )
            .values(assigned_to=moderator_id, assigned_at=datetime.now(UTC))
            .returning(Report)
        )
        report = result.scalar_one_or_none()
        if report is not None:
            return report
        current = await self.get(report_id)
        if current is None or current.status != ReportStatus.PENDING:
            return None
        if current.assigned_to not in {None, moderator_id}:
            return None
        current.assigned_to = moderator_id
        current.assigned_at = datetime.now(UTC)
        await self.session.flush()
        return current

    async def release(self, report_id, moderator_id: int, *, override: bool = False) -> Report | None:
        conditions = [
            Report.id == report_id,
            Report.status == ReportStatus.PENDING,
            Report.assigned_to.is_not(None),
        ]
        if not override:
            conditions.append(Report.assigned_to == moderator_id)
        result = await self.session.execute(
            update(Report)
            .where(*conditions)
            .values(assigned_to=None, assigned_at=None)
            .returning(Report)
        )
        return result.scalar_one_or_none()

    async def resolve(self, report_id, status: ReportStatus) -> Report | None:
        result = await self.session.execute(
            update(Report)
            .where(Report.id == report_id, Report.status == ReportStatus.PENDING)
            .values(status=status)
            .returning(Report)
        )
        return result.scalar_one_or_none()
````

## File: repositories/trust.py
````python
import uuid

from sqlalchemy import func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
    AdminLog,
    ModerationCase,
    ModerationCaseStatus,
    ModerationCaseType,
    PhotoModeration,
    Report,
    ReportStatus,
    TrustScoreEvent,
    User,
    VerificationDecision,
    VerificationRequest,
)


class TrustRepository:
    """Persistence primitives for trust services; policy stays in services/."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def active_verification_for_user(self, user_id: int) -> VerificationRequest | None:
        return await self.session.scalar(
            select(VerificationRequest)
            .where(
                VerificationRequest.user_id == user_id,
                VerificationRequest.status == VerificationDecision.PENDING,
            )
            .order_by(VerificationRequest.created_at.desc())
        )

    async def open_verification(self, user_id: int, video_file_id: str) -> tuple[VerificationRequest, bool]:
        """
        Open a verification request for a user. Returns (request, created) where created
        is True when a new request was created, or False when an existing pending request
        was found and returned.

        This method is defensive: callers may run it under concurrent transactions and
        the DB or elsewhere may also enforce uniqueness. If insertion fails due to a
        race, the method attempts to return the existing pending request.
        """
        active = await self.active_verification_for_user(user_id)
        if active is not None:
            return active, False
        request = VerificationRequest(user_id=user_id, video_file_id=video_file_id)
        try:
            nested = getattr(self.session, "begin_nested", None)
            if nested is None:
                self.session.add(request)
                await self.session.flush()
            else:
                async with nested():
                    self.session.add(request)
                    await self.session.flush()
        except IntegrityError:
            # The savepoint keeps the outer transaction usable after a race.
            existing = await self.active_verification_for_user(user_id)
            if existing:
                return existing, False
            raise
        return request, True

    async def verification(self, request_id: uuid.UUID) -> VerificationRequest | None:
        return await self.session.get(VerificationRequest, request_id)

    async def pending_verifications(self) -> list[VerificationRequest]:
        query = select(VerificationRequest).where(VerificationRequest.status == VerificationDecision.PENDING)
        return list((await self.session.scalars(query.order_by(VerificationRequest.created_at))).all())

    async def open_case(
        self, user_id: int, case_type: ModerationCaseType, *, source_id: str | None = None, details: str | None = None
    ) -> tuple[ModerationCase, bool]:
        query = select(ModerationCase).where(
            ModerationCase.user_id == user_id,
            ModerationCase.case_type == case_type,
            ModerationCase.status.in_((ModerationCaseStatus.PENDING, ModerationCaseStatus.IN_PROGRESS)),
        )
        if source_id is not None:
            query = query.where(ModerationCase.source_id == source_id)
        else:
            query = query.where(ModerationCase.source_id.is_(None))
        existing = await self.session.scalar(query)
        if existing:
            if details is not None and existing.details != details:
                existing.details = details
                await self.session.flush()
            return existing, False
        case = ModerationCase(user_id=user_id, case_type=case_type, source_id=source_id, details=details)
        try:
            nested = getattr(self.session, "begin_nested", None)
            if nested is None:
                self.session.add(case)
                await self.session.flush()
            else:
                async with nested():
                    self.session.add(case)
                    await self.session.flush()
        except IntegrityError:
            existing = await self.session.scalar(query)
            if existing:
                return existing, False
            raise
        return case, True

    async def case(self, case_id: uuid.UUID) -> ModerationCase | None:
        return await self.session.get(ModerationCase, case_id)

    async def pending_cases(self, case_type: ModerationCaseType | None = None) -> list[ModerationCase]:
        query = select(ModerationCase).where(ModerationCase.status == ModerationCaseStatus.PENDING)
        if case_type:
            query = query.where(ModerationCase.case_type == case_type)
        return list((await self.session.scalars(query.order_by(ModerationCase.created_at))).all())

    async def pending_cases_for_user(self, user_id: int) -> list[ModerationCase]:
        return list(
            (
                await self.session.scalars(
                    select(ModerationCase)
                    .where(
                        ModerationCase.user_id == user_id,
                        ModerationCase.status == ModerationCaseStatus.PENDING,
                    )
                    .order_by(ModerationCase.created_at)
                )
            ).all()
        )

    async def close_photo_cases(self, user_id: int, *, source_id: str | None = None) -> int:
        statement = (
            update(ModerationCase)
            .where(
                ModerationCase.user_id == user_id,
                ModerationCase.case_type.in_(
                    (ModerationCaseType.NSFW, ModerationCaseType.NO_FACE, ModerationCaseType.PHOTO_RETAKE)
                ),
                ModerationCase.status.in_((ModerationCaseStatus.PENDING, ModerationCaseStatus.IN_PROGRESS)),
            )
            .values(status=ModerationCaseStatus.RESOLVED)
        )
        if source_id is not None:
            statement = statement.where(ModerationCase.source_id == source_id)
        result = await self.session.execute(statement)
        return int(getattr(result, "rowcount", 0) or 0)

    async def photo_by_hash(self, content_hash: str) -> PhotoModeration | None:
        return await self.session.scalar(
            select(PhotoModeration)
            .where(PhotoModeration.content_hash == content_hash)
            .order_by(PhotoModeration.created_at)
        )

    async def photo_for_case(self, user_id: int, source_id: str | None) -> PhotoModeration | None:
        query = select(PhotoModeration).where(PhotoModeration.user_id == user_id)
        if source_id:
            query = query.where(
                (PhotoModeration.content_hash == source_id) | (PhotoModeration.photo_file_id == source_id)
            )
        return await self.session.scalar(query.order_by(PhotoModeration.created_at.desc()))

    async def record_photo(
        self,
        user_id: int,
        photo_file_id: str,
        provider: str,
        nsfw_score: float,
        face_detected: bool,
        content_hash: str | None = None,
    ) -> PhotoModeration:
        if content_hash:
            existing = await self.session.scalar(
                select(PhotoModeration).where(
                    PhotoModeration.user_id == user_id, PhotoModeration.content_hash == content_hash
                )
            )
            if existing:
                return existing
        item = PhotoModeration(
            user_id=user_id,
            photo_file_id=photo_file_id,
            content_hash=content_hash,
            provider=provider,
            nsfw_score=nsfw_score,
            face_detected=face_detected,
        )
        self.session.add(item)
        await self.session.flush()
        return item

    async def add_score_event(
        self, user_id: int, delta: int, reason: str, reference_type: str | None, reference_id: str | None
    ) -> TrustScoreEvent:
        event = TrustScoreEvent(
            user_id=user_id,
            delta=delta,
            reason=reason,
            reference_type=reference_type,
            reference_id=reference_id,
        )
        self.session.add(event)
        await self.session.flush()
        return event

    async def log(
        self,
        admin_id: int,
        action: str,
        *,
        target_type: str | None = None,
        target_id: str | None = None,
        target_user_id: int | None = None,
        details: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> AdminLog:
        item = AdminLog(
            admin_id=admin_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            target_user_id=target_user_id,
            details=details,
            metadata_json=metadata or {},
        )
        self.session.add(item)
        await self.session.flush()
        return item

    async def history(self, limit: int = 30) -> list[AdminLog]:
        return list(
            (await self.session.scalars(select(AdminLog).order_by(AdminLog.created_at.desc()).limit(limit))).all()
        )

    async def stats(self) -> dict[str, float | int]:
        verified = await self.session.scalar(
            select(func.count(VerificationRequest.id)).where(
                VerificationRequest.status == VerificationDecision.APPROVED
            )
        )
        reports = await self.session.scalar(select(func.count()).select_from(Report))
        false_reports = await self.session.scalar(
            select(func.count()).select_from(Report).where(Report.status == ReportStatus.DISMISSED)
        )
        confirmed_fakes = await self.session.scalar(
            select(func.count()).select_from(TrustScoreEvent).where(TrustScoreEvent.reason == "confirmed_fake")
        )
        average = await self.session.scalar(select(func.avg(User.trust_score)))
        return {
            "verified": int(verified or 0),
            "reports": int(reports or 0),
            "false_reports": int(false_reports or 0),
            "confirmed_fakes": int(confirmed_fakes or 0),
            "average_trust_score": round(float(average or 0), 2),
        }
````

## File: services/profile_service.py
````python
from __future__ import annotations

import logging

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from dtos.profile_dto import ProfileDraft
from models import Appeal, Gender, ModerationCase, ModerationStatus, Profile, User, UserStatus
from repositories.profile import ProfileRepository
from services.interest_normalizer import normalize_interests
from validators.profile_validator import ProfileValidationError, validate_profile_payload

logger = logging.getLogger(__name__)


class ProfileService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = ProfileRepository(session)

    async def get_profile(self, user_id: int) -> Profile | None:
        return await self.repo.by_user_id(user_id)

    async def _user_status_for(self, user_id: int) -> UserStatus | None:
        user = await self.session.get(User, user_id)
        return user.status if user else None

    def _is_visibility_restricted(self, profile: Profile | None, *, user_status: UserStatus | None = None) -> bool:
        if profile is None:
            return False
        if profile.moderation_locked:
            return True
        if profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            return True
        if user_status in {UserStatus.SUSPENDED, UserStatus.BANNED}:
            return True
        return False

    def _sync_photo_state(self, profile: Profile, photo_ids: list[str]) -> None:
        normalized = list(dict.fromkeys(photo_ids))[:3]
        profile.photo_file_ids = normalized
        profile.extra_data = {**(profile.extra_data or {}), "photo_file_ids": normalized}
        profile.photo_file_id = normalized[0] if normalized else ""
        profile.main_photo_file_id = normalized[0] if normalized else None

    async def create_or_update(self, user_id: int, draft: ProfileDraft) -> Profile:
        payload = draft.to_payload()
        photo_file_ids = list(payload.get("photo_file_ids") or [])
        try:
            validate_profile_payload(
                payload, photo_file_ids=photo_file_ids, locale=str(payload.get("locale") or "ru")
            )
        except ProfileValidationError as exc:
            logger.warning("Invalid profile payload for user %s: %s", user_id, exc.errors)
            raise

        profile = await self.repo.by_user_id(user_id)
        if profile is None:
            profile = Profile(user_id=user_id)
            self.session.add(profile)

        profile.gender = Gender(payload["gender"]) if payload.get("gender") else profile.gender
        profile.target_gender = (
            Gender(payload["target_gender"]) if payload.get("target_gender") else profile.target_gender
        )
        profile.name = str(payload.get("name") or "").strip()
        profile.age = int(payload.get("age"))
        profile.district = str(payload.get("district") or "").strip()
        profile.institution = str(payload.get("institution") or "").strip()
        profile.interests = normalize_interests(payload.get("interests") or [])
        profile.bio = str(payload.get("bio") or "").strip()
        profile.locale = str(payload.get("locale") or profile.locale or "ru").split("-", 1)[0].lower()

        user_status = await self._user_status_for(user_id)
        if self._is_visibility_restricted(profile, user_status=user_status):
            profile.is_visible = False
        else:
            profile.is_visible = bool(payload.get("is_visible", profile.is_visible))

        if photo_file_ids:
            self._sync_photo_state(profile, photo_file_ids)
        elif getattr(profile, "extra_data", None) is None:
            self._sync_photo_state(profile, [])

        await self.repo.save(profile)
        return profile

    async def pause(self, user_id: int) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        profile.is_visible = False
        await self.repo.save(profile)
        return profile

    async def resume(self, user_id: int) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        # Resuming a profile is a user action, never a moderation decision.  In
        # particular it must not be a back door out of a freeze/ban after an
        # edit or a photo replacement.
        user_status = await self._user_status_for(user_id)
        if self._is_visibility_restricted(profile, user_status=user_status):
            profile.is_visible = False
        else:
            profile.is_visible = True
        await self.repo.save(profile)
        return profile

    async def delete(self, user_id: int) -> bool:
        user = await self.session.get(User, user_id)
        if user is None:
            return False
        # Keep the user row as an anonymized tombstone: reports reference it with
        # CASCADE FKs, so deleting the row would destroy retained evidence.
        execute = getattr(self.session, "execute", None)
        if execute is not None:
            await execute(delete(Appeal).where(Appeal.user_id == user_id))
            await execute(delete(ModerationCase).where(ModerationCase.user_id == user_id))
        profile = await self.repo.by_user_id(user_id)
        if profile is not None:
            await self.session.delete(profile)
        user.username = None
        user.status = UserStatus.PAUSED
        await self.session.flush()
        return True

    async def add_photo(self, user_id: int, photo_file_id: str) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        photo_ids = list((profile.extra_data or {}).get("photo_file_ids", list(profile.photo_file_ids or [])))
        if photo_file_id not in photo_ids:
            if len(photo_ids) >= 3:
                raise ValueError("В анкете может быть не более трёх фотографий.")
            photo_ids.append(photo_file_id)
        self._sync_photo_state(profile, photo_ids)
        if profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            profile.is_visible = False
        await self.repo.save(profile)
        return profile

    async def remove_photo(self, user_id: int, photo_file_id: str) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        photo_ids = list((profile.extra_data or {}).get("photo_file_ids", list(profile.photo_file_ids or [])))
        if photo_file_id in photo_ids:
            photo_ids.remove(photo_file_id)
        self._sync_photo_state(profile, photo_ids)
        if profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            profile.is_visible = False
        await self.repo.save(profile)
        return profile

    async def move_photo(self, user_id: int, photo_file_id: str, direction: int) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        photo_ids = list(profile.photo_file_ids or [])
        if photo_file_id not in photo_ids:
            return profile
        index = photo_ids.index(photo_file_id)
        target = index + direction
        if not 0 <= target < len(photo_ids):
            return profile
        photo_ids[index], photo_ids[target] = photo_ids[target], photo_ids[index]
        self._sync_photo_state(profile, photo_ids)
        if profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            profile.is_visible = False
        await self.repo.save(profile)
        return profile

    async def replace_photo(self, user_id: int, old_file_id: str, new_file_id: str) -> Profile:
        profile = await self.get_profile(user_id)
        if profile is None:
            raise ValueError("Profile does not exist")
        photo_ids = list(profile.photo_file_ids or [])
        if new_file_id == old_file_id:
            return profile
        if old_file_id not in photo_ids:
            return profile
        if new_file_id in photo_ids:
            photo_ids.remove(new_file_id)
        index = photo_ids.index(old_file_id)
        photo_ids[index] = new_file_id
        self._sync_photo_state(profile, photo_ids)
        if profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW:
            profile.is_visible = False
        await self.repo.save(profile)
        return profile
````

## File: tests/test_photo_safety_providers.py
````python
import io
from types import SimpleNamespace

import pytest
from PIL import Image

from config import Settings
from services.photo_moderation_service import (
    PhotoAssessment,
    PhotoModerationService,
    PhotoValidationError,
    normalize_image,
)
from services.photo_safety_providers import (
    DisabledPhotoSafetyProvider,
    HeuristicPhotoSafetyProvider,
    OnnxPhotoSafetyProvider,
    build_photo_safety_provider,
    face_detection_size,
)


def safety_settings(**changes):
    values = {
        "photo_safety_provider": "heuristic",
        "nsfw_model_path": "/missing/nsfw.onnx",
        "face_model_path": "/missing/face.onnx",
        "face_detection_threshold": 0.75,
        "face_detection_max_dimension": 960,
        "photo_safety_min_dimension": 64,
        "photo_safety_max_pixels": 1_000_000,
    }
    values.update(changes)
    return SimpleNamespace(**values)


def test_photo_safety_default_is_fail_closed():
    settings = Settings(_env_file=None, bot_token="x" * 30, daily_secret_salt="y" * 20)

    assert settings.photo_safety_provider == "ml"


def test_production_rejects_non_ml_photo_safety_provider():
    with pytest.raises(ValueError, match="PHOTO_SAFETY_PROVIDER"):
        Settings(
            _env_file=None,
            bot_token="x" * 30,
            daily_secret_salt="y" * 20,
            environment="production",
            photo_safety_provider="heuristic",
        )


def image_bytes(size=(100, 100), image_format="JPEG"):
    buffer = io.BytesIO()
    Image.new("RGB", size, "white").save(buffer, format=image_format)
    return buffer.getvalue()


def test_provider_is_selected_only_by_configuration():
    assert isinstance(build_photo_safety_provider(safety_settings()), HeuristicPhotoSafetyProvider)
    assert isinstance(
        build_photo_safety_provider(safety_settings(photo_safety_provider="disabled")), DisabledPhotoSafetyProvider
    )
    assert isinstance(build_photo_safety_provider(safety_settings(photo_safety_provider="ml")), OnnxPhotoSafetyProvider)


def test_face_detection_size_downscales_phone_photos_without_distortion():
    assert face_detection_size(3888, 5184, 960) == (720, 960)
    assert face_detection_size(709, 945, 960) == (709, 945)


def test_normalization_strips_metadata_and_produces_stable_image():
    image = normalize_image(image_bytes(), safety_settings())

    assert image.width == 100
    assert image.height == 100
    assert image.rgb_bytes.startswith(b"\xff\xd8")


@pytest.mark.parametrize("payload", [b"", b"not-an-image", image_bytes((16, 16))])
def test_invalid_or_too_small_images_are_rejected(payload):
    with pytest.raises(PhotoValidationError):
        normalize_image(payload, safety_settings())


class FakeBot:
    def __init__(self, raw):
        self.raw = raw

    async def get_file(self, _file_id):
        return SimpleNamespace(file_size=len(self.raw), file_path="photo")

    async def download_file(self, _path, destination):
        destination.write(self.raw)


class CountingProvider:
    name = "counting"

    def __init__(self):
        self.calls = 0

    async def assess(self, _image):
        self.calls += 1
        return PhotoAssessment(0.1, True, self.name)


class FakePhotoRepository:
    def __init__(self):
        self.cached = None
        self.records = []

    async def photo_by_hash(self, _content_hash):
        return self.cached

    async def record_photo(self, _user_id, _file_id, provider, score, face, content_hash):
        item = SimpleNamespace(provider=provider, nsfw_score=score, face_detected=face, content_hash=content_hash)
        self.records.append(item)
        self.cached = item
        return item

    async def open_case(self, *_args, **_kwargs):
        return None, True


class FakeSession:
    async def scalar(self, _query):
        return SimpleNamespace(moderation_status=None, is_visible=True, moderation_locked=False)


@pytest.mark.asyncio
async def test_identical_normalized_photo_reuses_saved_assessment():
    provider = CountingProvider()
    service = PhotoModerationService(
        FakeSession(),
        nsfw_threshold=0.85,
        provider=provider,
        settings=safety_settings(photo_safety_max_bytes=1_000_000),
        bot=FakeBot(image_bytes()),
    )
    service.repo = FakePhotoRepository()

    await service.inspect(1, "first")
    cached = await service.inspect(2, "second")

    assert provider.calls == 1
    assert cached.provider == "counting:cached"
````

## File: tests/test_trust_services.py
````python
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from models import (
    AppealStatus,
    ModerationCaseStatus,
    ModerationCaseType,
    ModerationStatus,
    UserRole,
    UserStatus,
    VerificationStatus,
)
from repositories.trust import TrustRepository
from services.moderation_service import ModerationService
from services.photo_moderation_service import PhotoAssessment, PhotoModerationService
from services.profile_service import ProfileService
from services.verification_service import VerificationService


class FakeSession:
    def __init__(self, user=None, profile=None):
        self.user = user
        self.profile = profile
        self.added = []
        self.scalar_values = []

    async def get(self, _model, _id):
        return self.user

    async def scalar(self, _query):
        if self.scalar_values:
            return self.scalar_values.pop(0)
        return self.profile

    def add(self, value):
        self.added.append(value)

    async def flush(self):
        return None


class UnsafeProvider:
    async def assess(self, _photo_id):
        return PhotoAssessment(nsfw_score=0.99, face_detected=False, provider="test")


class SafeProvider:
    async def assess(self, _photo_id):
        return PhotoAssessment(nsfw_score=0.0, face_detected=True, provider="test")


class NoFaceProvider:
    async def assess(self, _photo_id):
        return PhotoAssessment(nsfw_score=0.0, face_detected=False, provider="test")


class FailingProvider:
    async def assess(self, _photo_id):
        raise RuntimeError("model unavailable")


@pytest.mark.asyncio
async def test_ban_and_unban_are_idempotent():
    user = SimpleNamespace(status=UserStatus.ACTIVE)
    profile = SimpleNamespace(is_visible=True, moderation_locked=False, moderation_status=ModerationStatus.CLEAR)
    session = FakeSession(user, profile)
    service = ModerationService(session)

    async def fake_get(model, _id):
        if model.__name__ == "User" and _id == 99:
            return SimpleNamespace(role=UserRole.OWNER)
        return user

    session.get = fake_get

    assert await service.ban(7, 99, reason="test")
    assert user.status == UserStatus.BANNED
    assert not profile.is_visible and profile.moderation_locked
    assert not await service.ban(7, 99, reason="test")
    assert await service.unban(7, 99)
    assert user.status == UserStatus.ACTIVE
    assert not await service.unban(7, 99)


@pytest.mark.asyncio
async def test_approve_appeal_restores_user_profile_and_marks_appeal():
    user = SimpleNamespace(status=UserStatus.SUSPENDED, role=UserRole.OWNER)
    profile = SimpleNamespace(
        is_visible=False,
        moderation_locked=True,
        moderation_status=ModerationStatus.UNDER_REVIEW,
    )
    appeal = SimpleNamespace(user_id=7, id="appeal-1", status=AppealStatus.PENDING, admin_id=None)

    class AppealSession:
        async def get(self, _model, _identity):
            return user

        async def scalar(self, _query):
            return profile

        async def execute(self, _query):
            return SimpleNamespace(scalars=lambda: SimpleNamespace(first=lambda: None))

        def add(self, _value):
            return None

        async def flush(self):
            return None

    service = ModerationService(AppealSession())
    service.repo.log = AsyncMock()

    restored, reason = await service.restore_appeal_sanction(appeal, 99, actor_role=UserRole.OWNER)

    assert (restored, reason) == (True, None)
    assert user.status == UserStatus.ACTIVE
    assert profile.is_visible is True
    assert profile.moderation_locked is False
    assert profile.moderation_status == ModerationStatus.CLEAR
    assert appeal.status == AppealStatus.APPROVED
    service.repo.log.assert_awaited_once()


@pytest.mark.asyncio
async def test_moderator_cannot_ban_self():
    user = SimpleNamespace(status=UserStatus.ACTIVE, role=UserRole.MODERATOR)

    class SelfBanSession:
        async def get(self, model, item_id):
            if model.__name__ == "User":
                return user if item_id == 7 else SimpleNamespace(role=UserRole.MODERATOR)
            return None

        async def scalar(self, _query):
            return None

        async def flush(self):
            return None

    service = ModerationService(SelfBanSession())

    assert await service.ban(7, 7, reason="self-ban") is False


@pytest.mark.asyncio
async def test_case_claim_wins_and_wrong_owner_cannot_resolve():
    case = SimpleNamespace(
        id="case-1",
        user_id=7,
        case_type=ModerationCaseType.NSFW,
        status=ModerationCaseStatus.PENDING,
        assigned_to=None,
        assigned_at=None,
        admin_id=None,
    )

    class ClaimSession:
        def __init__(self, case_ref):
            self.case_ref = case_ref

        async def get(self, model, item_id):
            if model.__name__ == "User":
                if item_id == 101:
                    return SimpleNamespace(role=UserRole.MODERATOR)
                if item_id == 202:
                    return SimpleNamespace(role=UserRole.MODERATOR)
                return None
            if model.__name__ == "ModerationCase":
                return self.case_ref
            return None

        async def scalar(self, _query):
            return None

        async def flush(self):
            return None

        def add(self, _value):
            return None

        async def execute(self, _query):
            self.case_ref.status = ModerationCaseStatus.IN_PROGRESS
            self.case_ref.assigned_to = 101
            self.case_ref.assigned_at = "now"
            return SimpleNamespace(scalar_one_or_none=lambda: self.case_ref)

    session = ClaimSession(case)
    service = ModerationService(session)

    claimed_case, claimed, _ = await service.claim_case(case.id, 101)
    assert claimed is True
    assert claimed_case.assigned_to == 101
    assert claimed_case.status == ModerationCaseStatus.IN_PROGRESS

    resolved_case, changed, resolution = await service.resolve_case(case.id, 202)
    assert changed is False
    assert resolution in {"already_assigned", "forbidden"}
    assert resolved_case.assigned_to == 101


@pytest.mark.asyncio
async def test_moderator_cannot_resolve_or_ban_other_claimed_case():
    case = SimpleNamespace(
        id="case-2",
        user_id=7,
        case_type=ModerationCaseType.NSFW,
        status=ModerationCaseStatus.IN_PROGRESS,
        assigned_to=101,
        assigned_at=None,
        admin_id=None,
    )

    class PermissionSession:
        async def get(self, model, item_id):
            if model.__name__ == "User":
                return SimpleNamespace(role=UserRole.MODERATOR)
            if model.__name__ == "ModerationCase":
                return case
            return None

        async def scalar(self, _query):
            return None

        async def flush(self):
            return None

        def add(self, _value):
            return None

        async def execute(self, _query):
            return SimpleNamespace(scalar_one_or_none=lambda: None)

    service = ModerationService(PermissionSession())

    resolved_case, changed, resolution = await service.resolve_case(case.id, 202)
    assert changed is False
    assert resolution == "forbidden"
    assert resolved_case.assigned_to == 101

    assert await service.ban(7, 202, reason="test") is False


@pytest.mark.asyncio
async def test_resolved_case_cannot_be_reprocessed_by_stale_callback():
    case = SimpleNamespace(
        id="case-3",
        user_id=7,
        case_type=ModerationCaseType.NSFW,
        status="RESOLVED",
        assigned_to=101,
        assigned_at=None,
        admin_id=101,
    )

    class ResolvedSession:
        async def get(self, model, _item_id):
            if model.__name__ == "User":
                return SimpleNamespace(role=UserRole.MODERATOR)
            if model.__name__ == "ModerationCase":
                return case
            return None

        async def scalar(self, _query):
            return None

        async def flush(self):
            return None

        def add(self, _value):
            return None

        async def execute(self, _query):
            return SimpleNamespace(scalar_one_or_none=lambda: None)

    service = ModerationService(ResolvedSession())
    resolved_case, changed, resolution = await service.resolve_case(case.id, 101)
    assert changed is False
    assert resolution in {"already_resolved", "not_in_progress"}
    assert resolved_case is case


@pytest.mark.asyncio
async def test_nsfw_and_no_face_open_manual_review_case():
    profile = SimpleNamespace(
        moderation_status=ModerationStatus.CLEAR,
        is_visible=True,
        moderation_locked=False,
    )
    session = FakeSession(profile=profile)
    session.scalar_values = [profile, None]
    assessment = await PhotoModerationService(session, nsfw_threshold=0.85, provider=UnsafeProvider()).inspect(
        7, "photo"
    )

    assert assessment.nsfw_score == 0.99
    assert not assessment.face_detected
    assert profile.moderation_status == ModerationStatus.UNDER_REVIEW
    assert not profile.is_visible and profile.moderation_locked
    assert any(getattr(item, "case_type", None) == ModerationCaseType.NSFW for item in session.added)


@pytest.mark.asyncio
async def test_no_face_review_can_be_deferred_without_hiding_profile():
    profile = SimpleNamespace(
        moderation_status=ModerationStatus.CLEAR,
        is_visible=True,
        moderation_locked=False,
    )
    session = FakeSession(profile=profile)
    session.scalar_values = [profile]

    assessment = await PhotoModerationService(
        session, nsfw_threshold=0.85, provider=NoFaceProvider()
    ).inspect(7, "photo", defer_no_face_review=True)

    assert not assessment.face_detected
    assert profile.moderation_status == ModerationStatus.CLEAR
    assert profile.is_visible and not profile.moderation_locked
    assert not any(getattr(item, "case_type", None) == ModerationCaseType.NO_FACE for item in session.added)


def test_new_profile_defaults_are_unverified():
    assert VerificationStatus.UNVERIFIED.value == "UNVERIFIED"


@pytest.mark.asyncio
async def test_photo_provider_failure_hides_profile_and_opens_review_case():
    from services.photo_moderation_service import PhotoModerationError

    profile = SimpleNamespace(
        moderation_status=ModerationStatus.CLEAR,
        is_visible=True,
        moderation_locked=False,
    )
    session = FakeSession(profile=profile)
    session.scalar_values = [profile, None]

    with pytest.raises(PhotoModerationError):
        await PhotoModerationService(session, nsfw_threshold=0.85, provider=FailingProvider()).inspect(7, "photo")

    assert profile.moderation_status == ModerationStatus.UNDER_REVIEW
    assert not profile.is_visible and profile.moderation_locked
    assert any(getattr(item, "case_type", None) == ModerationCaseType.NSFW for item in session.added)


@pytest.mark.asyncio
async def test_frozen_profile_remains_frozen_after_safe_photo_assessment():
    profile = SimpleNamespace(
        moderation_status=ModerationStatus.UNDER_REVIEW,
        is_visible=False,
        moderation_locked=True,
    )
    session = FakeSession(profile=profile)
    session.scalar_values = [profile, None]

    service = PhotoModerationService(session, nsfw_threshold=0.85, provider=SafeProvider())
    service.repo = SimpleNamespace(
        record_photo=AsyncMock(),
        open_case=AsyncMock(return_value=(None, True)),
        pending_cases_for_user=AsyncMock(return_value=[]),
    )

    await service.inspect(7, "photo")

    assert profile.moderation_status == ModerationStatus.UNDER_REVIEW
    assert profile.is_visible is False
    assert profile.moderation_locked is True


@pytest.mark.asyncio
async def test_frozen_profile_remains_frozen_after_photo_update_actions():
    profile = SimpleNamespace(
        user_id=7,
        photo_file_ids=["old-1", "old-2"],
        extra_data={"photo_file_ids": ["old-1", "old-2"]},
        moderation_status=ModerationStatus.UNDER_REVIEW,
        is_visible=False,
        moderation_locked=True,
    )
    session = FakeSession(profile=profile)
    session.scalar_values = [profile]

    service = ProfileService(session)
    updated_add = await service.add_photo(7, "new-3")
    updated_replace = await service.replace_photo(7, "old-1", "new-1")
    updated_remove = await service.remove_photo(7, "old-2")

    assert updated_add.moderation_locked is True
    assert updated_replace.moderation_locked is True
    assert updated_remove.moderation_locked is True
    assert updated_add.is_visible is False
    assert updated_replace.is_visible is False
    assert updated_remove.is_visible is False


@pytest.mark.asyncio
async def test_trust_repository_does_not_create_duplicate_pending_cases_for_same_event():
    class TrustSession:
        def __init__(self):
            self.added = []
            self._pending = None

        async def scalar(self, _statement):
            return self._pending

        def add(self, item):
            self.added.append(item)
            self._pending = item

        async def flush(self):
            return None

    session = TrustSession()
    repo = TrustRepository(session)

    await repo.open_case(7, ModerationCaseType.NSFW, source_id="hash-1")
    await repo.open_case(7, ModerationCaseType.NSFW, source_id="hash-1")

    assert len(session.added) == 1


@pytest.mark.asyncio
async def test_verification_submit_blocks_verified_and_pending_user():
    profile = SimpleNamespace(verification_status=VerificationStatus.VERIFIED)
    session = FakeSession(profile=profile)
    service = VerificationService(session)
    service.repo = SimpleNamespace(active_verification_for_user=AsyncMock(return_value=None))

    with pytest.raises(ValueError, match="уже верифицированы"):
        await service.submit(7, "video-file")

    profile.verification_status = VerificationStatus.PENDING
    service.repo.active_verification_for_user = AsyncMock(return_value=SimpleNamespace(user_id=7))
    with pytest.raises(ValueError, match="текущая заявка"):
        await service.submit(7, "video-file")


@pytest.mark.asyncio
async def test_verification_submit_accepts_rejected_user_and_sets_pending():
    profile = SimpleNamespace(verification_status=VerificationStatus.REJECTED)
    session = FakeSession(profile=profile)
    service = VerificationService(session)
    service.repo = SimpleNamespace(
        active_verification_for_user=AsyncMock(return_value=None),
        open_verification=AsyncMock(return_value=(SimpleNamespace(user_id=7, video_file_id="video-file"), True)),
    )

    request = await service.submit(7, "video-file")

    assert profile.verification_status == VerificationStatus.PENDING
    assert request.video_file_id == "video-file"
````

## File: README.md
````markdown
# Бот знакомств и анонимных признаний — альфа

Это готовый Telegram-бот для локальных знакомств. Пользователь создаёт анкету с фото, смотрит подходящие анкеты, ставит лайки, получает уведомление о взаимной симпатии и может отправить анонимное признание. У администратора есть очередь жалоб, скрытие/блокировка анкет и текстовая рассылка.

> Это альфа-версия: перед публикацией обязательно подготовьте правила сервиса, политику конфиденциальности и модерацию. Не используйте бота для несовершеннолетних там, где это запрещено законом.

## Что уже работает

- регистрация анкеты: пол, кого искать, имя, возраст, район, место учёбы/работы, интересы, описание и фото;
- показ анкет с сортировкой по району, месту, интересам и близости возраста;
- лайки и автоматическое создание взаимной симпатии;
- список взаимных симпатий с Telegram-контактами; входящие лайки до матча остаются анонимными;
- «👎» навсегда убирает анкету из вашей ленты, «🚫» создаёт двустороннюю блокировку выдачи;
- пауза/возобновление своей анкеты и её полное редактирование;
- анонимные признания зарегистрированному пользователю или через персональную ссылку-приглашение;
- жалобы с причинами, автоматическое скрытие анкеты после трёх жалоб;
- админ-панель: разбор жалоб с данными анкеты, приостановка, бан, апелляции с ответом пользователю и рассылка;
- PostgreSQL для данных и Redis для состояний диалогов, антиспам-ограничения,
  dedupe уведомлений и временной recommendation queue;
- запуск одной командой через Docker Compose.

## Что понадобится

1. Компьютер с Windows 10/11, macOS или Linux.
2. Учётная запись Telegram.
3. Установленный [Docker Desktop](https://www.docker.com/products/docker-desktop/). После установки **обязательно запустите Docker Desktop** и дождитесь статуса *Engine running*.
4. Текстовый редактор. Подойдёт VS Code или обычный Блокнот.

Вам не нужно отдельно устанавливать Python, PostgreSQL или Redis: Docker загрузит их сам.

## Шаг 1. Создайте бота в Telegram

1. Откройте Telegram и найдите `@BotFather`.
2. Отправьте команду `/newbot`.
3. Введите отображаемое имя, например `Знакомства моего города`.
4. Введите username, который обязательно заканчивается на `bot`, например `my_city_dates_bot`.
5. BotFather пришлёт токен вида `123456789:AA...`. Скопируйте его. Никому его не отправляйте и не публикуйте.

## Шаг 2. Подготовьте настройки

В папке проекта найдите файл `.env.example`, сделайте его копию с именем `.env` и откройте `.env` в редакторе.

Не создавайте пустой `.env`: в нём обязательно должны быть строки с настройками. Если у вас уже есть пустой файл `.env`, удалите его содержимое и вставьте пример ниже.

Заполните минимум эти строки:

```dotenv
BOT_TOKEN=сюда-вставьте-токен-от-BotFather
DAILY_SECRET_SALT=придумайте-длинную-случайную-строку-минимум-16-символов
ADMIN_IDS=123456789
OWNER_ADMIN_ID=123456789
```

Как узнать `ADMIN_IDS` и назначить владельца:

1. Напишите любое сообщение боту `@userinfobot` в Telegram.
2. Он покажет ваш числовой `Id`.
3. Вставьте это число вместо `123456789` в обе строки: `ADMIN_IDS` и `OWNER_ADMIN_ID`.
4. Если администраторов несколько, разделите ID запятой: `ADMIN_IDS=111111,222222`. В `OWNER_ADMIN_ID` оставьте ID владельца, например: `OWNER_ADMIN_ID=111111`.

После изменения `.env` перезапустите бот:

```bash
docker compose up -d --build
```

Остальные строки в `.env` можно оставить как есть. Файл `.env` уже исключён из Git и не должен попадать в публичный репозиторий.

## Шаг 3. Запустите

Откройте терминал в папке проекта и выполните:

```bash
docker compose up --build
```

Первый запуск может занять несколько минут: Docker скачает Python, PostgreSQL и Redis. Когда в терминале появятся сообщения о запуске polling, бот готов.

Теперь откройте своего бота в Telegram и нажмите **Start** или отправьте `/start`.

Чтобы остановить бота, вернитесь в терминал и нажмите `Ctrl+C`.

Чтобы в следующий раз запустить его снова, выполните:

```bash
docker compose up
```

Чтобы запустить в фоне (терминал можно закрыть):

```bash
docker compose up -d --build
```

Посмотреть сообщения бота в фоне:

```bash
docker compose logs -f bot
```

Полностью остановить контейнеры:

```bash
docker compose down
```

Команда `down` не удаляет анкеты. Чтобы удалить **все** данные тестового бота, используйте `docker compose down -v` — это необратимо.

## Как проверять работу

Для полноценной проверки нужны хотя бы два Telegram-аккаунта.

1. На каждом аккаунте запустите бота и создайте анкету через «👤 Моя анкета».
2. На первом аккаунте нажмите «💘 Знакомства» и поставьте сердечко второй анкете.
3. На втором аккаунте поставьте сердечко первой анкете. Оба увидят сообщение о взаимной симпатии.
4. Нажмите «💌 Признание», укажите `@username` второго аккаунта, напишите текст и подтвердите отправку.
5. С аккаунта, указанного в `ADMIN_IDS`, отправьте `/admin`, проверьте жалобу и тестовую рассылку.

Важно: Telegram позволяет искать получателя признания по `@username`. Пользователь без username может получить признание только по ссылке-приглашению после первого запуска бота. В матче бот отдаёт `@username`, а если его нет — кликабельную Telegram-ссылку на профиль.

## Команды и кнопки

| Для кого | Действие | Результат |
| --- | --- | --- |
| Все | `/start` | Открывает главное меню |
| Все | `/help` | Показывает краткую справку |
| Все | «👤 Моя анкета» | Создание, просмотр, скрытие или редактирование анкеты |
| Все | «💘 Знакомства» | Лента подходящих анкет |
| Все | «❤️ Симпатии» | Входящие лайки, взаимные симпатии и контакты |
| Все | «💌 Признание» | Анонимное сообщение по `@username` |
| Админ | `/admin` | Жалобы и рассылка |

## Структура и данные

- `main.py` — старт приложения;
- `handlers/` — действия, которые видят пользователи и администраторы;
- `models/` — таблицы базы данных;
- `repositories/` — чтение и запись базы;
- `services/` — подбор анкет, взаимные лайки, признания и уведомления;
- `docker-compose.yml` — запуск бота, PostgreSQL и Redis;
- `.env` — ваши секретные настройки (создаётся вами, не публикуется).

База данных обновляется миграциями Alembic. Перед первым запуском или обновлением выполните:

```bash
alembic upgrade head
alembic current
alembic heads
```

Исторические migration files не изменяются. Для обновления уже работающего проекта
сначала сделайте резервную копию базы.

FSM хранится в Redis с TTL из `FSM_STATE_TTL_SECONDS`. После истечения TTL старый диалог
не восстанавливается: неизвестное сообщение получает понятный ответ и главное меню.

Для локальной проверки:

```bash
pytest -q
ruff check .
PYTHONPYCACHEPREFIX=/tmp/pycache python3 -m compileall -q .
```

Integration tests находятся в `tests/integration/` и запускаются только при `INTEGRATION=1`
и доступных PostgreSQL/Redis.

## Безопасность и ограничения альфы

- Признания не хранят ID отправителя: хранится дневной salted SHA-256-хэш для ограничения спама. Это не отменяет доступ Telegram и администратора базы к инфраструктурным данным.
- Ограничитель частоты защищает от быстрых повторных нажатий; при большом публичном запуске стоит добавить полноценный token-bucket с отдельными лимитами для каждого действия.
- Класс `services/nsfw_service.py` — точка подключения к реальному провайдеру проверки фото. В текущем виде он не распознаёт 18+ изображения; подключите проверенный сервис модерации **до** публичного запуска.
- Перед реальными пользователями добавьте кнопку согласия с правилами, контакты поддержки, политику удаления данных и ручную модерацию.


- Признания не хранят ID отправителя: хранится дневной salted SHA-256-хэш для ограничения спама. Это не отменяет доступ Telegram и администратора базы к инфраструктурным данным.
- Ограничитель частоты защищает от быстрых повторных нажатий; при большом публичном запуске стоит добавить полноценный token-bucket с отдельными лимитами для каждого действия.
- Класс `services/nsfw_service.py` — точка подключения к реальному провайдеру проверки фото. В текущем виде он не распознаёт 18+ изображения; подключите проверенный сервис модерации **до** публичного запуска.
- Перед реальными пользователями добавьте кнопку согласия с правилами, контакты поддержки, политику удаления данных и ручную модерацию.

## Если что-то не запускается

- `env file .env not found` — вы не создали `.env` из `.env.example`.
- `Unauthorized` или `TelegramUnauthorizedError` — проверьте `BOT_TOKEN`; старый токен можно отозвать у BotFather командой `/revoke`.
- `Cannot connect to the Docker daemon` — запустите Docker Desktop и подождите его полной загрузки.
- Бот не отвечает, но контейнер запущен — смотрите `docker compose logs -f bot`.
- Не видны анкеты — создайте минимум две видимые анкеты с подходящими настройками пола и поиска.

## Обновление

После изменения кода выполните:

```bash
docker compose up -d --build
```

Ваш `.env` и данные PostgreSQL сохранятся.

Полный сценарий проверки после обновления находится в [TEST_CHECKLIST.md](TEST_CHECKLIST.md).
````

## File: handlers/dating.py
````python
from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.verification import verification_start
from keyboards.dating import dating_keyboard, report_reasons_keyboard
from keyboards.menu import MENU_DATING_LABELS
from models import ReportReason, User, UserStatus
from repositories.discovery import DiscoveryRepository
from repositories.profile import ProfileRepository
from repositories.trust import TrustRepository
from services.interest_normalizer import format_interests
from services.like_service import LikeService
from services.localization import LocalizationService
from services.match_service import MatchService
from services.notification_service import InternalNotificationService, NotificationService
from services.profile_service import ProfileService
from services.promo_service import get_empty_discovery_promo
from services.recommendation import RecommendationService
from services.report_service import ReportService
from states.dating import DatingState
from utils.admin_ui import user_display_name
from utils.contacts import telegram_contact
from utils.document_links import documents_keyboard
from utils.profile_media import profile_photo_ids, send_profile_gallery
from utils.text import escape_html

router = Router()
localizer = LocalizationService()


def _match_notification(name: str, contact: str, locale: str) -> str:
    return localizer.format("notification_match", locale, name=name, contact=contact)


def _target_id(callback: CallbackQuery) -> int | None:
    try:
        return int((callback.data or "").split(":")[1])
    except (IndexError, TypeError, ValueError):
        return None


async def _clear_callback_keyboard(callback: CallbackQuery) -> None:
    """Deactivate a consumed discovery card so its action cannot be repeated."""
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except TelegramBadRequest as exc:
        if "message is not modified" not in str(exc).lower():
            raise


async def show_next(message: Message, user_id: int, session: AsyncSession, settings, locale: str = "ru") -> None:
    profile = await ProfileService(session).get_profile(user_id)
    if profile is None:
        await message.answer(
            "📝 Для начала нужно создать анкету.\n\nБез неё мы не сможем подобрать подходящих людей.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="✨ Создать анкету", callback_data="profile:create")]]
            ),
        )
        return
    user = await session.get(User, user_id)
    if user is None or user.status != UserStatus.ACTIVE:
        await message.answer(
            "⏸️ Ваш аккаунт временно ограничен. Доступ к знакомствам будет восстановлен после решения модератора."
        )
        return
    if profile.moderation_locked or profile.moderation_status.value == "UNDER_REVIEW":
        await message.answer(
            "⏳ Ваша анкета сейчас на проверке или ожидает замены фотографии. Пока она не участвует в знакомствах.\n\n"
            "Откройте анкету, чтобы увидеть статус и заменить фото или подать апелляцию.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="📷 Управлять фото", callback_data="profile:photos")]]
            ),
        )
        return
    recommendation = await RecommendationService(session, weights=settings.matching_weights).next_recommendation(
        user_id
    )
    if not recommendation:
        promo = get_empty_discovery_promo(user_id, profile=profile, locale=locale)
        empty_kb_rows = [
            [
                InlineKeyboardButton(text="🔄 Обновить выдачу", callback_data="next:profile"),
                InlineKeyboardButton(text="👤 Моя анкета", callback_data="promo:my_profile"),
            ]
        ]
        if promo["button_action"] == "promo:share":
            bot_info = await message.bot.get_me()
            bot_username = bot_info.username
            share_text = "Присоединяйся к MeAnima для знакомств!"
            share_url = f"https://t.me/share/url?url=https://t.me/{bot_username}&text={share_text}"
            empty_kb_rows.append([InlineKeyboardButton(text=promo["button_text"], url=share_url)])
        elif promo["button_action"] not in {"next:profile", "promo:my_profile"}:
            action_btn = InlineKeyboardButton(text=promo["button_text"], callback_data=promo["button_action"])
            empty_kb_rows.append([action_btn])

        empty_kb = InlineKeyboardMarkup(inline_keyboard=empty_kb_rows)
        await message.answer(
            "✨ Похоже, ты посмотрел всех доступных людей поблизости.\n\n"
            f"<b>{escape_html(promo['title'])}</b>\n"
            f"{escape_html(promo['text'])}",
            reply_markup=empty_kb,
        )
        return
    p = recommendation.profile
    caption = (
        f"{escape_html(p.name)}, {p.age}\n📍 {escape_html(p.district)}\n"
        f"🏫 {escape_html(p.institution)}\n🎯 {escape_html(format_interests(p.interests))}\n\n{escape_html(p.bio)}"
    )
    if p.verification_status.value == "VERIFIED":
        caption += "\n\n🟢 Проверенный профиль"
    caption += f"\n\n❤️ Совместимость: {round(recommendation.score)}%"
    await send_profile_gallery(message, p, caption, dating_keyboard(p.user_id, locale))


@router.message(F.text.in_(MENU_DATING_LABELS))
async def browse(message: Message, session: AsyncSession, settings, locale: str = "ru") -> None:
    await show_next(message, message.from_user.id, session, settings, locale)


@router.callback_query(F.data.startswith("like:"))
async def like(callback: CallbackQuery, session: AsyncSession, settings) -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    try:
        result = await LikeService(session).create(callback.from_user.id, target)
    except ValueError as error:
        await callback.answer(str(error), show_alert=True)
        return
    if not result.created:
        await _clear_callback_keyboard(callback)
        await callback.answer("Лайк уже был отправлен.")
        return
    await _clear_callback_keyboard(callback)
    match = await MatchService(session).create_if_mutual(callback.from_user.id, target, result.like)
    await callback.answer("Это взаимно! 🎉" if match.created else "Лайк отправлен ❤️")
    rec_svc = RecommendationService(session, weights=settings.matching_weights)
    await rec_svc.remove_candidate(callback.from_user.id, target)
    notifier = NotificationService(callback.bot)
    if match.created:
        target_profile, target_user = await DiscoveryRepository(session).profile_and_user(target)
        source_contact = telegram_contact(
            callback.from_user.id, callback.from_user.username, callback.from_user.full_name
        )
        target_contact = telegram_contact(
            target,
            target_user.username if target_user else None,
            target_profile.name if target_profile else "Пользователь",
        )
        target_url = f"https://t.me/{target_user.username}" if target_user and target_user.username else f"tg://user?id={target}"
        match_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="💬 Написать", url=target_url),
                    InlineKeyboardButton(text="💘 Продолжить поиск", callback_data="next:profile"),
                ]
            ]
        )
        target_name = escape_html(target_profile.name if target_profile else 'пользователем')
        source_profile, _ = await DiscoveryRepository(session).profile_and_user(callback.from_user.id)
        fallback_source = callback.from_user.full_name or "Пользователь"
        source_name = escape_html(source_profile.name if source_profile else fallback_source)

        target_locale = target_profile.locale if target_profile else "ru"
        source_locale = source_profile.locale if source_profile else "ru"
        match_target_text = _match_notification(source_name, source_contact, target_locale)
        match_source_text = _match_notification(target_name, target_contact, source_locale)

        source_url = f"https://t.me/{callback.from_user.username}" if callback.from_user.username else f"tg://user?id={callback.from_user.id}"
        await notifier.safe_send(
            target,
            match_target_text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="💬 Написать", url=source_url),
                        InlineKeyboardButton(text="💘 Продолжить поиск", callback_data="next:profile"),
                    ]
                ]
            ),
        )
        await callback.message.answer(
            match_source_text,
            reply_markup=match_kb,
        )
    else:
        await notifier.safe_send_localized(target, session, "notification_like")
    await show_next(callback.message, callback.from_user.id, session, settings)


@router.callback_query(F.data.startswith("comment:"))
async def comment_start(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    from services.eligibility import EligibilityError, EligibilityService

    try:
        await EligibilityService(session).ensure_recommendation_action_allowed(
            callback.from_user.id, target, action="поставить лайк"
        )
    except EligibilityError as error:
        await callback.answer(str(error), show_alert=True)
        return
    await state.update_data(like_target=target)
    await state.set_state(DatingState.like_comment)
    await callback.message.answer("💌 Напишите короткое сообщение к лайку (до 200 символов).")
    await callback.answer()


@router.message(DatingState.like_comment)
async def comment_finish(message: Message, state: FSMContext, session: AsyncSession, settings) -> None:
    text = (message.text or "").strip()
    if not 1 <= len(text) <= 200:
        await message.answer("⚠️ Сообщение должно быть от 1 до 200 символов.")
        return
    target = (await state.get_data())["like_target"]
    try:
        result = await LikeService(session).create(message.from_user.id, target, text)
    except ValueError as error:
        await state.clear()
        await message.answer(str(error))
        return
    await state.clear()
    if not result.created:
        await message.answer("❤️ Лайк уже был отправлен ранее.")
        return
    match = await MatchService(session).create_if_mutual(message.from_user.id, target, result.like)
    rec_svc = RecommendationService(session, weights=settings.matching_weights)
    await rec_svc.remove_candidate(message.from_user.id, target)
    notifier = NotificationService(message.bot)
    await notifier.safe_send_localized(target, session, "notification_like_comment", comment=escape_html(text))
    if match.created:
        target_profile, target_user = await DiscoveryRepository(session).profile_and_user(target)
        source_profile, _ = await DiscoveryRepository(session).profile_and_user(message.from_user.id)
        source_contact = telegram_contact(message.from_user.id, message.from_user.username, message.from_user.full_name)
        target_contact = telegram_contact(
            target,
            target_user.username if target_user else None,
            target_profile.name if target_profile else "Пользователь",
        )
        target_url = f"https://t.me/{target_user.username}" if target_user and target_user.username else f"tg://user?id={target}"
        source_url = f"https://t.me/{message.from_user.username}" if message.from_user.username else f"tg://user?id={message.from_user.id}"

        target_name = escape_html(target_profile.name if target_profile else 'пользователем')
        fallback_source = message.from_user.full_name or "Пользователь"
        source_name = escape_html(source_profile.name if source_profile else fallback_source)

        match_target_text = (
            f"🎉 <b>У вас взаимная симпатия с {source_name}!</b>\n\n"
            f"Кажется, вы понравились друг другу! ✨ Не стесняйтесь сделать первый шаг и написать прямо сейчас.\n\n"
            f"💬 <b>Контакт для связи:</b> {source_contact}\n\n"
            f"Желаем вам приятного и тёплого общения! 💫"
        )
        match_source_text = (
            f"🎉 <b>У вас взаимная симпатия с {target_name}!</b>\n\n"
            f"Кажется, вы понравились друг другу! ✨ Не стесняйтесь сделать первый шаг и написать прямо сейчас.\n\n"
            f"💬 <b>Контакт для связи:</b> {target_contact}\n\n"
            f"Желаем вам приятного и тёплого общения! 💫"
        )

        match_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="💬 Написать", url=target_url),
                    InlineKeyboardButton(text="💘 Продолжить поиск", callback_data="next:profile"),
                ]
            ]
        )
        await notifier.safe_send(
            target,
            match_target_text,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="💬 Написать", url=source_url),
                        InlineKeyboardButton(text="💘 Продолжить поиск", callback_data="next:profile"),
                    ]
                ]
            ),
        )
        await message.answer(match_source_text, reply_markup=match_kb)
    else:
        await message.answer("❤️ Лайк с сообщением отправлен.")


@router.callback_query(F.data == "promo:verification")
async def promo_verification(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession, locale: str = "ru"
) -> None:
    await callback.answer()
    await verification_start(callback.message, state, session, locale)


@router.callback_query(F.data == "promo:confession")
async def promo_confession(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await callback.answer()
    from handlers.confessions import begin
    await begin(callback.message, state, session)


@router.callback_query(F.data == "next:profile")
async def next_profile(callback: CallbackQuery, session: AsyncSession, settings) -> None:
    await callback.answer("Ищу следующую анкету...")
    await show_next(callback.message, callback.from_user.id, session, settings)


@router.callback_query(F.data.startswith("skip:"))
async def skip(callback: CallbackQuery, session: AsyncSession, settings) -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    from services.eligibility import EligibilityError, EligibilityService

    try:
        await EligibilityService(session).ensure_recommendation_action_allowed(
            callback.from_user.id, target, action="пропустить анкету"
        )
    except EligibilityError as error:
        await callback.answer(str(error), show_alert=True)
        return
    await DiscoveryRepository(session).skip(callback.from_user.id, target)
    await RecommendationService(session, weights=settings.matching_weights).skip(callback.from_user.id, target)
    await _clear_callback_keyboard(callback)
    await callback.answer("Анкета больше не будет показана. Ищу следующую анкету...")
    await show_next(callback.message, callback.from_user.id, session, settings)


@router.callback_query(F.data.startswith("block:"))
async def block(callback: CallbackQuery, session: AsyncSession, settings) -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    if not await DiscoveryRepository(session).block(callback.from_user.id, target):
        await callback.answer("Анкета уже недоступна.", show_alert=True)
        return
    await _clear_callback_keyboard(callback)
    await callback.answer("Пользователь заблокирован. Ищу следующую анкету...")
    rec_svc = RecommendationService(session, weights=settings.matching_weights)
    await rec_svc.remove_candidate(callback.from_user.id, target)
    await show_next(callback.message, callback.from_user.id, session, settings)


@router.callback_query(F.data.startswith("report:"))
async def report(callback: CallbackQuery, session: AsyncSession, locale: str = "ru") -> None:
    target = _target_id(callback)
    if target is None:
        await callback.answer("Некорректная анкета.", show_alert=True)
        return
    await callback.message.answer(
        "⚠️ Жалоба отправляется модераторам.\n\nПроверьте правила сообщества и процесс модерации:",
        reply_markup=documents_keyboard("community", "safety", "moderation"),
    )
    await callback.message.answer("📌 Выберите причину жалобы:", reply_markup=report_reasons_keyboard(target, locale))
    await callback.answer()


@router.callback_query(F.data.startswith("report_reason:"))
async def report_reason(callback: CallbackQuery, session: AsyncSession, settings) -> None:
    try:
        _, raw_target, reason = (callback.data or "").split(":")
        target = int(raw_target)
        report_reason_value = ReportReason(reason)
    except (ValueError, TypeError):
        await callback.answer("Некорректная жалоба.", show_alert=True)
        return
    try:
        report, created, threshold_reached = await ReportService(session, threshold=settings.report_threshold).submit(
            callback.from_user.id, target, report_reason_value
        )
    except ValueError as error:
        await callback.answer(str(error), show_alert=True)
        return
    rec_svc = RecommendationService(session, weights=settings.matching_weights)
    await rec_svc.remove_candidate(callback.from_user.id, target)
    profile = await ProfileRepository(session).by_user_id(target)
    internal = InternalNotificationService(callback.bot, settings)
    await internal.send_moderation_event(
        "Новая жалоба",
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        reason=report_reason_value.value,
        case_id=str(report.id),
        target_callback=f"mycase:report:{report.id}",
        details=f"Target user: {user_display_name(target)} | created={created}",
        photo_file_ids=profile_photo_ids(profile),
    )
    if threshold_reached:
        for admin_id in settings.admin_ids:
            await NotificationService(callback.bot).safe_send(
                admin_id,
                f"⚠️ Анкета {user_display_name(target)} автоматически снята с публикации: достигнут порог жалоб.",
                dedupe_key=f"report-threshold:{target}",
            )
            await TrustRepository(session).log(
                admin_id,
                "report_threshold_notice_sent",
                target_type="report",
                target_id=str(target),
                metadata={"target_user_id": target},
            )
        await internal.send_moderation_event(
            "⚠️ Profile frozen",
            user_id=target,
            username=None,
            reason=f"3 reports ({settings.report_threshold})",
            case_id=str(report.id),
            target_callback=f"mycase:report:{report.id}",
            details="Автоматическая заморозка анкеты после достижения порога жалоб.",
            photo_file_ids=profile_photo_ids(profile),
        )
    await callback.message.edit_text("✅ Жалоба отправлена модераторам." if created else "Эта жалоба уже была учтена.")
    await callback.answer("Спасибо за помощь")
````

## File: keyboards/profile.py
````python
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.localization import LocalizationService


def profile_keyboard(
    visible: bool = True, *, hidden_by_moderation: bool = False, accepts_confessions: bool = True,
    locale: str = "ru",
):
    text = LocalizationService().get
    kb = InlineKeyboardBuilder()
    if hidden_by_moderation:
        kb.button(text=text("profile_hidden", locale), callback_data="profile:blocked")
    else:
        kb.button(text=text("profile_hide" if visible else "profile_show", locale), callback_data="profile:toggle")
    kb.button(text=text("profile_edit", locale), callback_data="profile:edit")
    kb.button(text=text("profile_photos", locale), callback_data="profile:photos")
    kb.button(
        text=text("confessions_on" if accepts_confessions else "confessions_off", locale),
        callback_data="profile:confessions_toggle",
    )
    kb.button(text=text("profile_pause", locale), callback_data="profile:pause")
    kb.button(text=text("profile_delete", locale), callback_data="profile:delete")
    kb.button(text=text("language_button", locale), callback_data="profile:language")
    kb.adjust(2)
    return kb.as_markup()


def photo_management_keyboard(photo_count: int):
    kb = InlineKeyboardBuilder()
    for index in range(photo_count):
        position = index + 1
        kb.button(text=f"⭐ Главная #{position}", callback_data=f"photo:main:{index}")
        kb.button(text="⬅️", callback_data=f"photo:move:{index}:-1")
        kb.button(text="➡️", callback_data=f"photo:move:{index}:1")
        kb.button(text="🔄 Заменить", callback_data=f"photo:replace:{index}")
        kb.button(text="🗑 Удалить", callback_data=f"photo:delete:{index}")
    if photo_count < 3:
        kb.button(text="➕ Добавить фото", callback_data="photo:add")
    kb.button(text="🏠 Главное меню", callback_data="photo:done")
    kb.adjust(1, 2, 2, 1)
    return kb.as_markup()


def photo_upload_keyboard(done_callback: str):
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Готово", callback_data=done_callback)
    return kb.as_markup()


def failed_photo_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 Заменить фото", callback_data="photo:retry_failed")
    kb.button(text="🛡 Отправить модераторам", callback_data="photo:review_failed")
    kb.adjust(1)
    return kb.as_markup()


def registration_preview_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Опубликовать", callback_data="profile:publish")
    kb.button(text="✏️ Изменить", callback_data="profile:edit")
    kb.button(text="📷 Изменить фото", callback_data="profile:rephoto")
    kb.button(text="⬅️ Назад", callback_data="profile:back")
    kb.button(text="❌ Отмена", callback_data="profile:cancel")
    kb.adjust(2, 2, 1)
    return kb.as_markup()
````

## File: services/notification_service.py
````python
import logging
import re
import time
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

from config import Settings, get_settings
from repositories.profile import ProfileRepository
from services.localization import LocalizationService

logger = logging.getLogger(__name__)


def _truncate_text(value: str | None, max_length: int = 4000) -> str:
    if value is None:
        return ""
    cleaned = value.strip()
    if len(cleaned) <= max_length:
        return cleaned
    return cleaned[: max_length - 3].rstrip() + "..."


def _redact_sensitive(value: str | None) -> str:
    if not value:
        return ""
    redacted = re.sub(
        r"(?i)(token|password|secret|api[_-]?key|authorization)\s*[:=]\s*[^\s,\n]+",
        r"\1=[REDACTED]",
        value,
    )
    redacted = re.sub(
        r"(?i)(BOT_TOKEN|MEANIMA_INTERNAL_CHAT_ID|MEANIMA_INTERNAL_\w+_THREAD_ID)\s*[:=]\s*[^\s,\n]+",
        r"\1=[REDACTED]",
        redacted,
    )
    return redacted


class NotificationService:
    _recent_alerts: dict[tuple[int, str], float] = {}

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def safe_send_localized(
        self,
        user_id: int,
        session,
        key: str,
        *,
        reply_markup: InlineKeyboardMarkup | None = None,
        dedupe_key: str | None = None,
        **kwargs,
    ) -> bool:
        profile = await ProfileRepository(session).by_user_id(user_id)
        locale = profile.locale if profile is not None else "ru"
        text = LocalizationService().format(key, locale, **kwargs)
        return await self.safe_send(
            user_id,
            text,
            reply_markup=reply_markup,
            dedupe_key=dedupe_key,
        )

    async def _acquire_delivery(self, key: str, window: int) -> tuple[bool, str | None]:
        """Shared Redis idempotency lock; falls back only for legacy tests."""
        redis = getattr(self.bot, "notification_redis", None)
        if redis is None:
            return True, None
        delivered, lock = f"notification:delivered:{key}", f"notification:lock:{key}"
        if await redis.exists(delivered):
            return False, None
        # A short lease makes a worker crash retryable; delivery is marked only
        # after Telegram accepted the message.
        if not await redis.set(lock, "1", nx=True, ex=60):
            return False, None
        return True, lock

    async def _finish_delivery(self, key: str, lock: str | None, *, success: bool, window: int) -> None:
        redis = getattr(self.bot, "notification_redis", None)
        if redis is None or lock is None:
            return
        if success:
            await redis.set(f"notification:delivered:{key}", "1", ex=window)
        await redis.delete(lock)

    async def safe_send(
        self,
        user_id: int,
        text: str,
        *,
        reply_markup: InlineKeyboardMarkup | None = None,
        dedupe_key: str | None = None,
        dedupe_window_seconds: int = 1800,
    ) -> bool:
        shared_key = f"{user_id}:{dedupe_key}" if dedupe_key else None
        lock = None
        if shared_key:
            try:
                acquired, lock = await self._acquire_delivery(shared_key, dedupe_window_seconds)
            except Exception:
                logger.warning("Notification dedupe unavailable; sending without Redis lock.", exc_info=True)
                shared_key = None
                lock = None
            else:
                if not acquired:
                    return False
        if dedupe_key and getattr(self.bot, "notification_redis", None) is None:
            cache_key = (user_id, dedupe_key)
            now = time.monotonic()
            last_sent = self._recent_alerts.get(cache_key)
            if last_sent is not None and now - last_sent < dedupe_window_seconds:
                return False
        try:
            await self.bot.send_message(user_id, text, reply_markup=reply_markup)
        except Exception:
            if shared_key:
                try:
                    await self._finish_delivery(shared_key, lock, success=False, window=dedupe_window_seconds)
                except Exception:
                    logger.warning("Notification dedupe cleanup failed after delivery error.", exc_info=True)
            logger.warning("Telegram notification delivery failed", extra={"user_id": user_id}, exc_info=True)
            return False
        if dedupe_key and getattr(self.bot, "notification_redis", None) is None:
            self._recent_alerts[(user_id, dedupe_key)] = time.monotonic()
        if shared_key:
            try:
                await self._finish_delivery(shared_key, lock, success=True, window=dedupe_window_seconds)
            except Exception:
                logger.warning("Notification dedupe cleanup failed after successful delivery.", exc_info=True)
        return True


class InternalNotificationService:
    _recent_alerts: dict[tuple[str, str], float] = {}
    _sending_error_notification = False
    # how many consecutive "chat not found" errors before we disable notifications
    _CHAT_NOT_FOUND_DISABLE_AFTER = 3

    def __init__(self, bot: Bot, settings: Settings | None = None) -> None:
        self.bot = bot
        self.settings = settings or get_settings()
        self._disabled_by_chat = False
        # Counter for consecutive chat-not-found errors. Reset on success.
        self._consecutive_chat_not_found = 0

    @property
    def enabled(self) -> bool:
        return bool(self.settings.meanima_internal_chat_id) and not self._disabled_by_chat

    def _thread_id_for(self, kind: str) -> int | None:
        threads: Mapping[str, int | None] = {
            "bugs": self.settings.meanima_internal_bug_thread_id,
            "moderation": self.settings.meanima_internal_moderation_thread_id,
            "errors": self.settings.meanima_internal_errors_thread_id,
            "stats": self.settings.meanima_internal_stats_thread_id,
        }
        return threads.get(kind)

    async def send_event(
        self,
        kind: str,
        text: str,
        *,
        thread_id: int | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        dedupe_key: str | None = None,
        dedupe_window_seconds: int = 1800,
    ) -> bool:
        if not self.enabled:
            return False
        if kind == "errors" and self._sending_error_notification:
            logger.warning("Skipping recursive internal error notification.")
            return False
        if dedupe_key:
            cache_key = (kind, dedupe_key)
            now = time.monotonic()
            last_sent = self._recent_alerts.get(cache_key)
            if last_sent is not None and now - last_sent < dedupe_window_seconds:
                return False

        target_thread = thread_id if thread_id is not None else self._thread_id_for(kind)
        chat_id = self.settings.meanima_internal_chat_id
        payload = {
            "chat_id": chat_id,
            "text": _truncate_text(_redact_sensitive(text), 4096),
        }
        if reply_markup is not None:
            payload["reply_markup"] = reply_markup

        attempt_payloads = [payload]
        if target_thread is not None:
            attempt_payloads = [{**payload, "message_thread_id": target_thread}, payload]

        # Diagnostic log: what we are attempting to send (redact only sensitive content already applied to text)
        try:
            logger.debug(
                "Attempting internal notification",
                extra={
                    "chat_id": int(chat_id) if chat_id is not None else None,
                    "message_thread_id": int(target_thread) if target_thread is not None else None,
                    "kind": kind,
                },
            )
        except Exception:
            # Avoid any accidental logging of unexpected objects — fall back to safe message
            logger.debug("Attempting internal notification for kind=%s", kind)

        last_error: Exception | None = None
        for attempt in attempt_payloads:
            try:
                if kind == "errors":
                    self.__class__._sending_error_notification = True
                await self.bot.send_message(**attempt)
                if dedupe_key:
                    # A failed Telegram request must remain retryable.  This
                    # mirrors user notifications' success-only dedupe rule.
                    self._recent_alerts[(kind, dedupe_key)] = time.monotonic()
                # Success — reset chat-not-found counter
                self._consecutive_chat_not_found = 0
                return True
            except TelegramBadRequest as exc:
                last_error = exc
                msg = str(exc).lower()
                # A broken, closed, or unavailable forum topic must not swallow
                # the notification: retry in the main group without a thread.
                if target_thread is not None and ("message thread" in msg or "topic" in msg):
                    logger.warning(
                        "Internal Telegram notification topic is invalid for %s; retrying without thread_id.",
                        kind,
                        exc_info=True,
                    )
                    # don't mark chat as unavailable; try fallback (next iteration)
                    continue

                # Chat not found or invalid chat id — increment counter and disable only after threshold
                if "chat not found" in msg or "chat_id is invalid" in msg or "not found" in msg:
                    # increment counter and log diagnostic without exposing secrets
                    self._consecutive_chat_not_found += 1
                    logger.warning(
                        "Internal Telegram chat reported 'chat not found' for kind=%s (chat_id=%s)."
                        " Consecutive missing count=%d/%d.",
                        kind,
                        str(chat_id),
                        self._consecutive_chat_not_found,
                        self._CHAT_NOT_FOUND_DISABLE_AFTER,
                        exc_info=False,
                    )
                    if self._consecutive_chat_not_found >= self._CHAT_NOT_FOUND_DISABLE_AFTER:
                        self._disabled_by_chat = True
                        logger.exception(
                            "Internal Telegram chat unavailable for %s; disabling after %d failed attempts",
                            kind,
                            self._consecutive_chat_not_found,
                        )
                        return False
                    # Do not disable yet — allow future attempts
                    return False

                # Other TelegramBadRequest — treat as permanent for now
                logger.exception("Internal Telegram notification delivery failed for %s", kind)
                return False
            except Exception as exc:
                last_error = exc
                logger.exception("Internal Telegram notification delivery failed for %s", kind)
                return False
            finally:
                if kind == "errors":
                    self.__class__._sending_error_notification = False

        if last_error is not None:
            logger.exception("Internal Telegram notification delivery failed for %s", kind)
        return False

    async def send_bug_report(
        self,
        user_id: int,
        *,
        username: str | None,
        description: str,
        context: str | None = None,
    ) -> bool:
        user_label = f"@{username}" if username else "без username"
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        lines = [
            "🐛 BUG REPORT",
            "",
            f"👤 User: {user_label}",
            f"🆔 ID: {user_id}",
            f"🕐 Time: {timestamp}",
            "",
            "📝 Description:",
            _truncate_text(description, 1800),
        ]
        if context:
            lines.extend(["", "Контекст:", _truncate_text(context, 600)])
        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="Открыть кейс", callback_data="admin:reports")]]
        )
        return await self.send_event("bugs", "\n".join(lines), reply_markup=markup, dedupe_key=f"bug:{user_id}")

    async def send_moderation_event(
        self,
        title: str,
        *,
        user_id: int | None = None,
        username: str | None = None,
        reason: str | None = None,
        case_id: str | None = None,
        details: str | None = None,
        photo_file_ids: Sequence[str] | None = None,
        event_key: str | None = None,
        target_callback: str | None = None,
    ) -> bool:
        user_label = f"@{username}" if username else "без username" if user_id is not None else "—"
        lines = ["🚩 MODERATION", "", title]
        if user_id is not None:
            lines.append(f"User: {user_label}")
            lines.append(f"ID: {user_id}")
        if reason:
            lines.append(f"Reason: {reason}")
        if case_id:
            lines.append(f"Case: {case_id}")
        if details:
            lines.append("")
            lines.append(_truncate_text(details, 600))
        markup = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="Открыть кейс", callback_data=target_callback or "admin:reports")
            ]]
        )
        text = "\n".join(lines)
        if photo_file_ids:
            photo_ids = [photo for photo in photo_file_ids if photo][:3]
            if photo_ids:
                media = [
                    InputMediaPhoto(media=photo_id, caption=text if index == 0 else None)
                    for index, photo_id in enumerate(photo_ids)
                ]
                try:
                    if hasattr(self.bot, "send_media_group"):
                        await self.bot.send_media_group(
                            chat_id=self.settings.meanima_internal_chat_id,
                            media=media,
                            message_thread_id=self._thread_id_for("moderation"),
                        )
                    else:
                        await self.bot.send_photo(
                            chat_id=self.settings.meanima_internal_chat_id,
                            photo=photo_ids[0],
                            caption=text,
                            message_thread_id=self._thread_id_for("moderation"),
                        )
                except Exception:
                    logger.warning("Failed to send moderation photos for internal moderation event.", exc_info=True)
                return await self.send_event(
                    "moderation",
                    text,
                    reply_markup=markup,
                    dedupe_key=f"moderation:{event_key or case_id or user_id or title}",
                )
        return await self.send_event(
            "moderation",
            text,
            reply_markup=markup,
            dedupe_key=f"moderation:{event_key or case_id or user_id or title}",
        )

    async def send_error_notification(
        self,
        *,
        module: str,
        exception_type: str,
        message: str,
        traceback_text: str | None,
    ) -> bool:
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        lines = [
            "⚠️ APPLICATION ERROR",
            "",
            f"🕐 {timestamp}",
            f"📍 {module}",
            "",
            "Exception:",
            exception_type,
            "",
            "Message:",
            _truncate_text(_redact_sensitive(message), 800),
            "",
            "Traceback:",
            _truncate_text(_redact_sensitive(traceback_text or ""), 1800),
        ]
        return await self.send_event("errors", "\n".join(lines), dedupe_key="error:system")

    async def send_daily_stats(self, stats: Mapping[str, int | float]) -> bool:
        lines = [
            "📊 DAILY STATS",
            "",
            f"👤 New users: {stats.get('new_users', 0)}",
            f"📝 New profiles: {stats.get('new_profiles', 0)}",
            f"❤️ Likes: {stats.get('likes', 0)}",
            f"💞 Matches: {stats.get('matches', 0)}",
            f"🚩 Reports: {stats.get('reports', 0)}",
            f"🛡 Moderation cases: {stats.get('moderation_cases', 0)}",
            f"✅ Verifications: {stats.get('verifications', 0)}",
        ]
        return await self.send_event("stats", "\n".join(lines), dedupe_key="stats:daily")
````

## File: services/photo_moderation_service.py
````python
from __future__ import annotations

import hashlib
import io
import logging
import warnings

from aiogram import Bot
from PIL import Image, ImageOps, UnidentifiedImageError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings, get_settings
from models import ModerationCaseType, ModerationStatus, Profile
from repositories.trust import TrustRepository
from services.notification_service import InternalNotificationService
from services.photo_safety_providers import (
    PhotoAssessment,
    PhotoSafetyProvider,
    SafeImage,
    get_photo_safety_provider,
)

logger = logging.getLogger(__name__)


class PhotoModerationError(RuntimeError):
    pass


class PhotoValidationError(PhotoModerationError):
    pass


class TelegramPhotoSource:
    """Fetches only Telegram files and rejects oversized inputs before decoding."""

    def __init__(self, bot: Bot, *, max_bytes: int) -> None:
        self.bot = bot
        self.max_bytes = max_bytes

    async def fetch(self, photo_file_id: str) -> bytes:
        file = await self.bot.get_file(photo_file_id)
        if file.file_size is not None and file.file_size > self.max_bytes:
            raise PhotoValidationError("Photo is too large")
        destination = io.BytesIO()
        await self.bot.download_file(file.file_path, destination=destination)
        payload = destination.getvalue()
        if not payload or len(payload) > self.max_bytes:
            raise PhotoValidationError("Photo is empty or too large")
        return payload


def normalize_image(raw: bytes, settings: Settings) -> SafeImage:
    """Decode bytes instead of trusting MIME/extension; strip EXIF before ML and hashing."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(raw)) as source:
                source.verify()
            with Image.open(io.BytesIO(raw)) as source:
                if source.format not in {"JPEG", "PNG", "WEBP"}:
                    raise PhotoValidationError("Unsupported image format")
                image = ImageOps.exif_transpose(source)
                width, height = image.size
                if min(width, height) < settings.photo_safety_min_dimension:
                    raise PhotoValidationError("Photo is too small")
                if width * height > settings.photo_safety_max_pixels:
                    raise PhotoValidationError("Photo has too many pixels")
                normalized = io.BytesIO()
                image.convert("RGB").save(normalized, format="JPEG", quality=95, optimize=True)
    except (Image.DecompressionBombError, UnidentifiedImageError, OSError, ValueError) as error:
        raise PhotoValidationError("Image is damaged or unsupported") from error
    return SafeImage(rgb_bytes=normalized.getvalue(), width=width, height=height)


class PhotoModerationService:
    def __init__(
        self,
        session: AsyncSession,
        *,
        nsfw_threshold: float,
        provider: PhotoSafetyProvider | None = None,
        settings: Settings | None = None,
        bot: Bot | None = None,
    ) -> None:
        self.session, self.threshold = session, nsfw_threshold
        self.settings = settings
        self.provider = provider or get_photo_safety_provider(settings or get_settings())
        self.bot = bot
        self.repo = TrustRepository(session)

    async def inspect(
        self, user_id: int, photo_file_id: str, *, defer_no_face_review: bool = False
    ) -> PhotoAssessment:
        content_hash: str | None = None
        image: SafeImage | None = None
        try:
            if self.bot is not None:
                settings = self.settings or get_settings()
                source = TelegramPhotoSource(self.bot, max_bytes=settings.photo_safety_max_bytes)
                raw = await source.fetch(photo_file_id)
                image = normalize_image(raw, settings)
                content_hash = hashlib.sha256(image.rgb_bytes).hexdigest()
                cached = await self.repo.photo_by_hash(content_hash)
                if cached is not None:
                    assessment = PhotoAssessment(cached.nsfw_score, cached.face_detected, f"{cached.provider}:cached")
                    await self._apply_assessment(
                        user_id, photo_file_id, content_hash, assessment, defer_no_face_review=defer_no_face_review
                    )
                    return assessment
            assessment = await self.provider.assess(image)
            if not 0.0 <= assessment.nsfw_score <= 1.0:
                raise ValueError("NSFW score must be between 0 and 1")
        except Exception as error:
            logger.warning("Photo safety check failed for user %s: %s", user_id, type(error).__name__)
            await self._send_to_manual_review(user_id, photo_file_id, content_hash, type(error).__name__)
            raise PhotoModerationError("Photo safety check failed") from error
        await self._apply_assessment(
            user_id, photo_file_id, content_hash, assessment, defer_no_face_review=defer_no_face_review
        )
        return assessment

    async def _apply_assessment(
        self,
        user_id: int,
        photo_file_id: str,
        content_hash: str | None,
        assessment: PhotoAssessment,
        *,
        defer_no_face_review: bool = False,
    ) -> None:
        await self.repo.record_photo(
            user_id, photo_file_id, assessment.provider, assessment.nsfw_score, assessment.face_detected, content_hash
        )
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        is_nsfw = assessment.nsfw_score >= self.threshold
        if not is_nsfw and not assessment.face_detected and defer_no_face_review:
            return
        if is_nsfw or not assessment.face_detected:
            if profile:
                profile.moderation_status = ModerationStatus.UNDER_REVIEW
                profile.is_visible = False
                profile.moderation_locked = True
            case_type = ModerationCaseType.NSFW if is_nsfw else ModerationCaseType.NO_FACE
            case, _ = await self.repo.open_case(
                user_id,
                case_type,
                source_id=content_hash or photo_file_id,
                details=(
                    f"provider={assessment.provider}; score={assessment.nsfw_score:.3f}; "
                    f"face={assessment.face_detected}"
                ),
            )
            if self.bot is not None:
                await InternalNotificationService(self.bot, self.settings).send_moderation_event(
                    "⚠️ ML moderation trigger",
                    user_id=user_id,
                    reason=case_type.value,
                    case_id=str(case.id),
                    target_callback=f"mycase:case:{case.id}",
                    details=(
                        f"provider={assessment.provider}; score={assessment.nsfw_score:.3f}; "
                        f"face_detected={assessment.face_detected}"
                    ),
                )
        else:
            close_photo_cases = getattr(self.repo, "close_photo_cases", None)
            if close_photo_cases is not None:
                await close_photo_cases(user_id)
            if profile and profile.moderation_locked:
                # Freeze/lock is a moderator-controlled state. A successful photo check
                # must never automatically lift a moderation restriction.
                return

    async def _send_to_manual_review(
        self, user_id: int, photo_file_id: str, content_hash: str | None, error_name: str
    ) -> None:
        await self.repo.record_photo(user_id, photo_file_id, "provider_error", 0.0, False, content_hash)
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id))
        if profile:
            profile.moderation_status = ModerationStatus.UNDER_REVIEW
            profile.is_visible = False
            profile.moderation_locked = True
        await self.repo.open_case(
            user_id,
            ModerationCaseType.NSFW,
            source_id=content_hash or photo_file_id,
            details=f"provider_error={error_name}",
        )
````

## File: services/verification_service.py
````python
import uuid
from datetime import UTC

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Profile, User, UserRole, VerificationDecision, VerificationRequest, VerificationStatus
from repositories.trust import TrustRepository
from services.trust_score_service import TrustScoreService
from utils.admin_roles import can_override_case, normalize_admin_role


class VerificationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = TrustRepository(session)

    async def submit(self, user_id: int, video_file_id: str):
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == user_id).with_for_update())
        if profile is None:
            raise ValueError("Сначала создайте анкету.")
        if profile.verification_status == VerificationStatus.VERIFIED:
            raise ValueError("Вы уже верифицированы и повторная отправка кружка недоступна.")
        if profile.verification_status == VerificationStatus.PENDING:
            raise ValueError("У вас уже есть текущая заявка на верификацию.")
        active = await self.repo.active_verification_for_user(user_id)
        if active is not None:
            raise ValueError("У вас уже есть активная заявка на верификацию.")
        profile.verification_status = VerificationStatus.PENDING
        request, _ = await self.repo.open_verification(user_id, video_file_id)
        return request

    async def claim(self, request_id: uuid.UUID, admin_id: int) -> VerificationRequest | None:
        """Claim a verification request for processing."""
        from datetime import datetime
        result = await self.session.execute(
            update(VerificationRequest)
            .where(
                VerificationRequest.id == request_id,
                VerificationRequest.status == VerificationDecision.PENDING,
                (VerificationRequest.assigned_to.is_(None) | (VerificationRequest.assigned_to == admin_id)),
            )
            .values(assigned_to=admin_id, assigned_at=datetime.now(UTC))
            .returning(VerificationRequest)
        )
        request = result.scalar_one_or_none()
        if request is not None:
            return request
        current = await self.repo.verification(request_id)
        if current is None or current.status != VerificationDecision.PENDING:
            return None
        if current.assigned_to not in {None, admin_id}:
            return None
        current.assigned_to = admin_id
        current.assigned_at = datetime.now(UTC)
        await self.session.flush()
        return current

    async def decide(
        self,
        request_id: uuid.UUID,
        admin_id: int,
        decision: VerificationDecision,
        comment: str | None = None,
        *,
        actor_role: UserRole | None = None,
    ):
        if decision not in {
            VerificationDecision.APPROVED,
            VerificationDecision.REJECTED,
            VerificationDecision.RETAKE_REQUESTED,
        }:
            raise ValueError(f"Unsupported verification decision: {decision}")
        conditions = [
            VerificationRequest.id == request_id,
            VerificationRequest.status == VerificationDecision.PENDING,
            VerificationRequest.assigned_to == admin_id,
        ]
        result = await self.session.execute(
            update(VerificationRequest)
            .where(*conditions)
            .values(status=decision, admin_id=admin_id, comment=comment)
            .returning(VerificationRequest)
        )
        request = result.scalar_one_or_none()
        if request is None:
            return await self.repo.verification(request_id), False
        profile = await self.session.scalar(select(Profile).where(Profile.user_id == request.user_id))
        if profile:
            profile.verification_status = {
                VerificationDecision.APPROVED: VerificationStatus.VERIFIED,
                VerificationDecision.REJECTED: VerificationStatus.REJECTED,
                VerificationDecision.RETAKE_REQUESTED: VerificationStatus.UNVERIFIED,
            }[decision]
        if decision == VerificationDecision.APPROVED:
            await TrustScoreService(self.session).change(
                request.user_id, 5, "verified", reference_type="verification", reference_id=str(request.id)
            )
        await self.repo.log(
            admin_id,
            f"verification_{decision.value.lower()}",
            target_type="verification",
            target_id=str(request.id),
            details=comment,
        )
        await self.session.flush()
        return request, True

    async def release(
        self, request_id: uuid.UUID, admin_id: int, *, actor_role: UserRole | None = None
    ) -> tuple[VerificationRequest | None, bool]:
        role = actor_role or normalize_admin_role(getattr(await self.session.get(User, admin_id), "role", None))
        conditions = [
            VerificationRequest.id == request_id,
            VerificationRequest.status == VerificationDecision.PENDING,
            VerificationRequest.assigned_to.is_not(None),
        ]
        if not can_override_case(role):
            conditions.append(VerificationRequest.assigned_to == admin_id)
        result = await self.session.execute(
            update(VerificationRequest)
            .where(*conditions)
            .values(assigned_to=None, assigned_at=None)
            .returning(VerificationRequest)
        )
        request = result.scalar_one_or_none()
        if request is not None:
            await self.session.flush()
            return request, True
        return await self.repo.verification(request_id), False
````

## File: tests/test_admin_ui.py
````python
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from aiogram.exceptions import TelegramBadRequest

from config import Settings
from keyboards.admin import admin_keyboard
from models import UserRole
from services.notification_service import InternalNotificationService, NotificationService
from utils.admin_roles import can_manage_admins, can_review_moderator_decisions, resolve_admin_role
from utils.admin_ui import admin_role_label, compact_display_id, user_display_name


class FakeBot:
    def __init__(self):
        self.sent = []

    async def send_message(self, chat_id, text, **kwargs):
        self.sent.append((chat_id, text, kwargs))


class FailingBot:
    async def send_message(self, *_args, **_kwargs):
        raise RuntimeError("telegram down")


def test_compact_display_id_shortens_queue_ids_for_moderation_ui():
    report_id = uuid.UUID("12345678-1234-4234-8234-123456789abc")

    assert compact_display_id(report_id) == "12345678"
    assert compact_display_id(123456789) == "456789"


def test_admin_role_label_uses_owner_and_moderator_tiers():
    assert admin_role_label(100, username="alice", owner_admin_id=100) == "👑 Netakussia — владелец"
    assert admin_role_label(200, username="alice") == "⚔️ @alice — модератор"
    assert admin_role_label(300, username=None) == "⚔️ модератор — модератор"


def test_user_display_name_hides_the_full_telegram_id():
    assert user_display_name(123456789, username="alice") == "@alice"
    assert user_display_name(123456789).startswith("#")
    assert len(user_display_name(123456789)) <= 8


def test_admin_permission_hierarchy_is_explicit_and_safe():
    assert resolve_admin_role(100, owner_admin_id=100, admin_ids={100, 200}) == UserRole.OWNER
    assert resolve_admin_role(200, owner_admin_id=100, admin_ids={100, 200}) == UserRole.MODERATOR
    assert resolve_admin_role(100, owner_admin_id=100, user_role=UserRole.USER) == UserRole.OWNER
    assert resolve_admin_role(200, admin_ids={100, 200}, user_role=UserRole.USER) == UserRole.MODERATOR
    assert can_manage_admins(UserRole.OWNER)
    assert not can_manage_admins(UserRole.MODERATOR)
    assert can_review_moderator_decisions(UserRole.CHIEF_MODERATOR)
    assert not can_review_moderator_decisions(UserRole.MODERATOR)


def test_explicit_owner_id_is_validated_and_overrides_admin_sorting():
    settings = Settings(
        _env_file=None,
        bot_token="x" * 30,
        daily_secret_salt="y" * 20,
        admin_ids_raw="100,200",
        owner_admin_id_raw="200",
    )

    assert settings.owner_admin_id == 200


def test_backend_role_hierarchy_blocks_forbidden_admin_actions():
    assert not can_review_moderator_decisions(UserRole.MODERATOR)
    assert not can_manage_admins(UserRole.MODERATOR)
    assert not can_manage_admins(UserRole.HEAD_MODERATOR)


def test_admin_menu_includes_profile_browse_action():
    markup = admin_keyboard()
    callback_ids = {
        button.callback_data
        for row in markup.inline_keyboard
        for button in row
        if getattr(button, "callback_data", None)
    }
    assert "admin:browse" in callback_ids


def test_admin_browse_next_nav_uses_current_profile_id():
    from keyboards.admin import admin_nav_keyboard, profile_moderation_keyboard

    markup = profile_moderation_keyboard(999, "admin:browse:next:999")
    callback_ids = {
        button.callback_data
        for row in markup.inline_keyboard
        for button in row
        if getattr(button, "callback_data", None)
    }
    assert "admin:browse:next:999" in callback_ids
    assert "profilemod:prompt:ban:999" in callback_ids

    nav = admin_nav_keyboard("admin:browse:next:999")
    assert "admin:browse:next:999" in {
        button.callback_data
        for row in nav.inline_keyboard
        for button in row
        if getattr(button, "callback_data", None)
    }


def test_photo_case_requires_an_explicit_atomic_claim_before_decision():
    from keyboards.admin import case_decision_keyboard, case_keyboard

    callbacks = {
        button.callback_data
        for row in case_keyboard("case-id").inline_keyboard
        for button in row
    }
    assert "case:claim:case-id" in callbacks
    decisions = {
        button.callback_data
        for row in case_decision_keyboard("case-id").inline_keyboard
        for button in row
    }
    assert "case:reject:case-id" in decisions


@pytest.mark.asyncio
async def test_notification_service_deduplicates_repeated_admin_alerts():
    bot = FakeBot()
    service = NotificationService(bot)

    first = await service.safe_send(777, "alert", dedupe_key="verification:abc")
    second = await service.safe_send(777, "alert", dedupe_key="verification:abc")

    assert first is True
    assert second is False
    assert len(bot.sent) == 1


@pytest.mark.asyncio
async def test_internal_notification_service_is_disabled_without_chat_id():
    settings = Settings(bot_token="x" * 30, daily_secret_salt="y" * 20, meanima_internal_chat_id=None)
    bot = FakeBot()
    service = InternalNotificationService(bot, settings)

    assert service.enabled is False
    assert await service.send_event("bugs", "hello") is False
    assert bot.sent == []


def test_internal_chat_accepts_short_environment_name(monkeypatch):
    monkeypatch.setenv("MEANIMA_INTERNAL_CHAT", "42")
    settings = Settings(_env_file=None, bot_token="x" * 30, daily_secret_salt="y" * 20)

    assert settings.meanima_internal_chat_id == 42


@pytest.mark.asyncio
async def test_internal_notification_service_sends_to_forum_thread():
    settings = Settings(
        bot_token="x" * 30,
        daily_secret_salt="y" * 20,
        meanima_internal_chat_id=42,
        meanima_internal_errors_thread_id=7,
    )
    bot = FakeBot()
    service = InternalNotificationService(bot, settings)

    sent = await service.send_event("errors", "oops", thread_id=7)

    assert sent is True
    assert bot.sent[0][0] == 42
    assert bot.sent[0][2]["message_thread_id"] == 7


@pytest.mark.asyncio
async def test_notification_service_failure_does_not_break_main_operation():
    service = NotificationService(FailingBot())

    assert await service.safe_send(123, "alert") is False
    assert await service.safe_send(456, "other") is False


@pytest.mark.asyncio
async def test_leaving_admin_administration_clears_broadcast_state(monkeypatch):
    from handlers.admin import section_administration

    monkeypatch.setattr("handlers.admin._require_admin_capability", AsyncMock(return_value=True))
    monkeypatch.setattr("handlers.admin._safe_edit_message_text", AsyncMock())
    callback = SimpleNamespace(answer=AsyncMock(), from_user=SimpleNamespace(id=1), message=SimpleNamespace())
    state = SimpleNamespace(clear=AsyncMock())
    settings = SimpleNamespace()

    await section_administration(callback, session=SimpleNamespace(), settings=settings, state=state)

    state.clear.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("callback_data", "expected"),
    [
        ("mycase:verify:request", "mycase:verify:request"),
        ("mycase:case:case", "mycase:case:case"),
        ("mycase:report:report", "mycase:report:report"),
        ("mycase:appeal:appeal", "mycase:appeal:appeal"),
    ],
)
async def test_moderation_notification_uses_case_specific_callback(callback_data, expected):
    from services.notification_service import InternalNotificationService

    settings = Settings(
        bot_token="x" * 30,
        daily_secret_salt="y" * 20,
        meanima_internal_chat_id=42,
    )
    bot = FakeBot()

    await InternalNotificationService(bot, settings).send_moderation_event(
        "moderation event", case_id=callback_data, target_callback=callback_data, event_key=callback_data
    )

    markup = bot.sent[0][2]["reply_markup"]
    assert markup.inline_keyboard[0][0].callback_data == expected


@pytest.mark.asyncio
async def test_admin_browse_fetches_one_profile_at_a_time():
    from handlers.admin import _next_browse_user

    class Session:
        def __init__(self):
            self.queries = []

        async def scalar(self, statement):
            self.queries.append(statement)
            return SimpleNamespace(id=20)

    session = Session()

    target = await _next_browse_user(session, current_user_id=10)

    assert target.id == 20
    assert len(session.queries) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("case_type", ["NSFW", "NO_FACE"])
async def test_photo_queue_accepts_supported_case_types(monkeypatch, case_type):
    from handlers.admin import _show_next_photo_case
    from models import ModerationCaseType
    from repositories.trust import TrustRepository

    item = SimpleNamespace(case_type=getattr(ModerationCaseType, case_type))
    monkeypatch.setattr(TrustRepository, "pending_cases", AsyncMock(return_value=[item]))
    render_photo_case = AsyncMock()
    monkeypatch.setattr("handlers.admin._render_photo_case", render_photo_case)
    callback = SimpleNamespace(message=SimpleNamespace(delete=AsyncMock()), from_user=SimpleNamespace(id=1))

    await _show_next_photo_case(callback, SimpleNamespace())

    callback.message.delete.assert_awaited_once()
    render_photo_case.assert_awaited_once_with(callback, SimpleNamespace(), item)


@pytest.mark.asyncio
async def test_internal_notification_disables_after_chat_not_found():
    settings = Settings(
        bot_token="x" * 30,
        daily_secret_salt="y" * 20,
        meanima_internal_chat_id=42,
    )

    class ChatMissingBot:
        def __init__(self):
            self.calls = 0

        async def send_message(self, **kwargs):
            self.calls += 1
            raise TelegramBadRequest(method="sendMessage", message="Bad Request: chat not found")

    bot = ChatMissingBot()
    service = InternalNotificationService(bot, settings)

    # first failure should not immediately disable notifications (transient)
    assert await service.send_event("moderation", "oops") is False
    assert service.enabled is True
    assert bot.calls == 1

    # after threshold failures, notifications become disabled
    threshold = service._CHAT_NOT_FOUND_DISABLE_AFTER
    for _ in range(threshold - 1):
        assert await service.send_event("moderation", "oops") is False

    assert service.enabled is False
    assert bot.calls == threshold


def test_admin_section_keyboards_structure_and_callbacks():
    from keyboards.admin import (
        admin_administration_keyboard,
        admin_moderation_keyboard,
        admin_nav_keyboard,
        admin_stats_keyboard,
        admin_users_keyboard,
        my_cases_keyboard,
    )

    mod_cb = {
        btn.callback_data
        for row in admin_moderation_keyboard().inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert {
        "admin:reports",
        "admin:nsfw",
        "admin:verifications",
        "admin:appeals",
        "admin:my_cases",
        "admin:menu",
    }.issubset(mod_cb)

    users_cb = {
        btn.callback_data
        for row in admin_users_keyboard().inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert {"admin:browse", "admin:blocked", "admin:menu"}.issubset(users_cb)

    stats_cb = {
        btn.callback_data
        for row in admin_stats_keyboard(can_view_history=True).inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert {"admin:trust_stats", "admin:trust_history", "admin:menu"}.issubset(stats_cb)

    admin_cb = {
        btn.callback_data
        for row in admin_administration_keyboard().inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert {"admin:broadcast", "admin:menu"}.issubset(admin_cb)

    my_cases_markup = my_cases_keyboard([("Кейс 1", "mycase:report:123")])
    my_cases_cb = {
        btn.callback_data
        for row in my_cases_markup.inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert {"mycase:report:123", "admin:my_cases", "admin:section:moderation", "admin:menu"}.issubset(my_cases_cb)

    nav = admin_nav_keyboard(
        next_callback="next:1",
        back_callback="back:1",
        refresh_callback="refresh:1",
        prev_callback="prev:1",
    )
    nav_cb = {
        btn.callback_data
        for row in nav.inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert {"next:1", "back:1", "refresh:1", "prev:1", "admin:menu"}.issubset(nav_cb)


def test_profile_moderation_keyboard_roles_and_states():
    from keyboards.admin import profile_moderation_keyboard

    # Active user, ordinary moderator cannot unban
    active_markup = profile_moderation_keyboard(123, is_banned=False, is_frozen=False, can_unban=False)
    active_cbs = {
        btn.callback_data
        for row in active_markup.inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert "profilemod:prompt:ban:123" in active_cbs
    assert "profilemod:prompt:freeze:123" in active_cbs

    # Suspended user, admin with can_unban
    frozen_markup = profile_moderation_keyboard(123, is_banned=False, is_frozen=True, can_unban=True)
    frozen_cbs = {
        btn.callback_data
        for row in frozen_markup.inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert "profilemod:prompt:unfreeze:123" in frozen_cbs
    assert "profilemod:prompt:ban:123" in frozen_cbs

    # Banned user, admin with can_unban
    banned_markup = profile_moderation_keyboard(123, is_banned=True, is_frozen=False, can_unban=True)
    banned_cbs = {
        btn.callback_data
        for row in banned_markup.inline_keyboard
        for btn in row
        if btn.callback_data
    }
    assert "profilemod:prompt:unban:123" in banned_cbs
````

## File: handlers/common.py
````python
import uuid

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.menu import MENU_HELP_LABELS, main_menu
from models import User
from services.confession_service import ConfessionService
from services.localization import LocalizationService
from services.notification_service import InternalNotificationService
from states.bug_report import BugReportState
from utils.admin_ui import admin_role_label
from utils.document_links import documents_keyboard
from utils.legal import accept_consent, consent_already_given, ensure_consent_for_new_user
from utils.text import escape_html

ALPHA_NOTICE_TEXT = (
    "🚀 <b>Внимание: Альфа-версия MeAnima</b>\n\n"
    "Бот находится в режиме активного тестирования. "
    "Если вы обнаружите баг или ошибку, нажмите «❓ Помощь» → «🐛 Сообщить о проблеме»."
)

router = Router()


async def _send_welcome(message: Message, locale: str = "ru") -> None:
    await send_and_pin_alpha_notice(message)
    await message.answer(
        LocalizationService().get("welcome", locale),
        reply_markup=main_menu(locale),
    )


async def send_and_pin_alpha_notice(message: Message) -> None:
    """Send alpha notice and attempt to pin it quietly in private chat."""
    try:
        notice_msg = await message.answer(ALPHA_NOTICE_TEXT)
        await notice_msg.pin(disable_notification=True)
    except TelegramBadRequest:
        pass


@router.callback_query(F.data == "legal:accept")
async def legal_accept(callback: CallbackQuery, state: FSMContext, session: AsyncSession, locale: str = "ru") -> None:
    await accept_consent(callback, state)
    await _send_welcome(callback.message, locale)


async def _text_start(message: Message, state: FSMContext, session: AsyncSession, settings, locale: str = "ru") -> None:
    await start(message, state, session, settings, locale)


@router.message(F.text.casefold() == "start")
async def text_start(message: Message, state: FSMContext, session: AsyncSession, settings, locale: str = "ru") -> None:
    await _text_start(message, state, session, settings, locale)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext, session: AsyncSession, settings, locale: str = "ru") -> None:
    args = message.text.split(maxsplit=1)
    if len(args) == 2 and args[1].startswith("confession_"):
        try:
            confession = await ConfessionService(session, settings.daily_secret_salt).claim(
                uuid.UUID(args[1].removeprefix("confession_")), message.from_user.id
            )
            if confession:
                await message.answer(f"💌 Вам анонимное признание:\n\n{escape_html(confession.text)}")
        except ValueError:
            pass

    if not await ensure_consent_for_new_user(state, session, message.from_user.id, message, locale):
        return

    consent = bool((await state.get_data()).get("legal_consent", False))
    await state.clear()
    if consent:
        await state.update_data(legal_consent=True)

    await _send_welcome(message, locale)


@router.message(F.text.in_({"Продолжить", "✅ Продолжить"}))
async def text_continue(message: Message, state: FSMContext, session: AsyncSession, locale: str = "ru") -> None:
    if not await consent_already_given(state):
        await message.answer(
            LocalizationService().get("legal_notice", locale),
            reply_markup=documents_keyboard(
                "terms",
                "privacy",
                "community",
                "safety",
                "moderation",
                "alpha",
                include_continue=True,
                locale=locale,
            ),
        )
        return
    await _send_welcome(message, locale)


@router.callback_query(F.data == "bug_report:start")
async def bug_report_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BugReportState.waiting_description)
    await callback.answer()
    await callback.message.answer(
        "🐛 Опишите проблему коротко и по сути. Можно также отправить скриншот вместе с описанием."
    )


@router.message(BugReportState.waiting_description)
async def bug_report_submit(message: Message, state: FSMContext, settings) -> None:
    text = (message.text or message.caption or "").strip()
    if not text:
        await message.answer("⚠️ Опишите проблему одним сообщением, чтобы мы смогли разобраться.")
        return
    context = "\n".join(
        [
            f"chat_type={message.chat.type}",
            f"chat_id={message.chat.id}",
            f"message_id={message.message_id}",
            f"location={message.location is not None}",
        ]
    )
    await InternalNotificationService(message.bot, settings).send_bug_report(
        message.from_user.id,
        username=message.from_user.username,
        description=text,
        context=context,
    )
    await state.clear()
    await message.answer("✅ Сообщение о проблеме отправлено. Спасибо — мы посмотрим и исправим.")


@router.message(Command("help"))
@router.message(lambda m: m.text in MENU_HELP_LABELS or m.text in {"⚙️ Настройки", "Настройки"})
async def help_(message: Message, settings, session: AsyncSession, locale: str = "ru") -> None:
    admin_ids = sorted(settings.admin_ids)
    support_lines = []
    for admin_id in admin_ids:
        user = await session.get(User, admin_id)
        username = user.username if user and user.username else None
        label = admin_role_label(admin_id, username=username, owner_admin_id=settings.owner_admin_id)
        support_lines.append(f'<a href="tg://user?id={admin_id}">{label}</a>')
    localizer = LocalizationService()
    support = "\n".join(support_lines) if support_lines else localizer.get("help_support_unconfigured", locale)
    markup = documents_keyboard(
        "terms",
        "privacy",
        "community",
        "safety",
        "moderation",
        "alpha",
        locale=locale,
    )
    markup.inline_keyboard.append(
        [InlineKeyboardButton(text=localizer.get("menu_profile", locale), callback_data="promo:my_profile")]
    )
    markup.inline_keyboard.append(
        [InlineKeyboardButton(text=localizer.get("help_report_problem", locale), callback_data="bug_report:start")]
    )
    await message.answer(localizer.get("help_text", locale), reply_markup=markup)
    await message.answer(
        f"{localizer.get('help_support_prompt', locale)}\n{support}",
    )
````

## File: .env.example
````
# Copy to .env and fill values for local development

BOT_TOKEN=replace-with-bot-token
POSTGRES_DB=dating_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=replace-with-a-long-random-postgres-password
DATABASE_URL=postgresql+asyncpg://postgres:replace-with-a-long-random-postgres-password@postgres:5432/dating_db
REDIS_PASSWORD=replace-with-a-long-random-redis-password
REDIS_URL=redis://:replace-with-a-long-random-redis-password@redis:6379/0
DAILY_SECRET_SALT=replace-with-a-long-random-secret
ADMIN_IDS=123456789
# The owner must also be included in ADMIN_IDS. This account has the highest admin permissions.
OWNER_ADMIN_ID=123456789
LOG_LEVEL=INFO
PHOTO_SAFETY_PROVIDER=heuristic
# For PHOTO_SAFETY_PROVIDER=ml, mount these downloaded local ONNX files into /models.
NSFW_MODEL_PATH=/models/open_nsfw.onnx
FACE_MODEL_PATH=/models/face_detection_yunet_2023mar.onnx
FACE_DETECTION_THRESHOLD=0.50
PHOTO_SAFETY_MAX_BYTES=10485760
PHOTO_SAFETY_MAX_PIXELS=24000000
PHOTO_SAFETY_MIN_DIMENSION=64
# YuNet receives a downscaled copy for reliable CPU face detection on phone photos.
FACE_DETECTION_MAX_DIMENSION=960
# Anonymous confessions: daily sender quota and deep-link lifetime in hours.
CONFESSION_DAILY_LIMIT=20
CONFESSION_PENDING_TTL_HOURS=168
# Redis FSM state/data expiry. Expired flows restart safely from the menu.
FSM_STATE_TTL_SECONDS=3600
````

## File: config.py
````python
import json
import math
from functools import lru_cache
from typing import Literal

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DOCUMENT_URLS = {
    "terms": "https://netakussia.github.io/meanima-docs/terms-of-service",
    "privacy": "https://netakussia.github.io/meanima-docs/privacy-policy",
    "community": "https://netakussia.github.io/meanima-docs/community-guidelines",
    "safety": "https://netakussia.github.io/meanima-docs/dating-safety",
    "moderation": "https://netakussia.github.io/meanima-docs/moderation-and-appeals",
    "alpha": "https://netakussia.github.io/meanima-docs/alpha-notice",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    def __init__(self, **data):
        explicit = dict(data)
        super().__init__(**data)
        for name in (
            "meanima_internal_chat_id",
            "meanima_internal_bug_thread_id",
            "meanima_internal_moderation_thread_id",
            "meanima_internal_errors_thread_id",
            "meanima_internal_stats_thread_id",
        ):
            if name in explicit:
                object.__setattr__(self, name, explicit[name])
        if self.environment.lower() in {"production", "prod", "staging"} and self.photo_safety_provider != "ml":
            raise ValueError("PHOTO_SAFETY_PROVIDER must be 'ml' in production-like environments.")

    bot_token: str = Field(..., min_length=20)
    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/dating_db"
    redis_url: str = "redis://redis:6379/0"
    daily_secret_salt: str = Field(..., min_length=16)
    admin_ids_raw: str = Field(default="", alias="ADMIN_IDS")
    owner_admin_id_raw: str = Field(default="", alias="OWNER_ADMIN_ID")
    document_base_url: str = Field(default="https://example.com/me-anima/docs", alias="DOCUMENT_BASE_URL")
    log_level: str = "INFO"
    nsfw_threshold: float = 0.85
    photo_safety_provider: Literal["ml", "heuristic", "disabled"] = "ml"
    environment: str = Field(
        default="development",
        validation_alias=AliasChoices("ENVIRONMENT", "ENV"),
    )
    nsfw_model_path: str = "/models/open_nsfw.onnx"
    face_model_path: str = "/models/face_detection_yunet_2023mar.onnx"
    face_detection_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    photo_safety_max_bytes: int = Field(default=10 * 1024 * 1024, ge=1)
    photo_safety_max_pixels: int = Field(default=24_000_000, ge=1)
    photo_safety_min_dimension: int = Field(default=64, ge=1)
    face_detection_max_dimension: int = Field(default=960, ge=320, le=2048)
    matching_weights_raw: str = Field(default="", alias="MATCHING_WEIGHTS_JSON")
    report_threshold: int = Field(default=3, ge=1, alias="REPORT_THRESHOLD")
    confession_daily_limit: int = Field(default=20, ge=1, le=100, alias="CONFESSION_DAILY_LIMIT")
    confession_pending_ttl_hours: int = Field(default=168, ge=1, le=24 * 31, alias="CONFESSION_PENDING_TTL_HOURS")
    fsm_state_ttl_seconds: int = Field(default=3600, ge=60, le=7 * 24 * 3600, alias="FSM_STATE_TTL_SECONDS")
    meanima_internal_chat_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("MEANIMA_INTERNAL_CHAT_ID", "MEANIMA_INTERNAL_CHAT"),
    )
    meanima_internal_bug_thread_id: int | None = Field(
        default=None,
        alias="MEANIMA_INTERNAL_BUG_THREAD_ID",
    )
    meanima_internal_moderation_thread_id: int | None = Field(
        default=None,
        alias="MEANIMA_INTERNAL_MODERATION_THREAD_ID",
    )
    meanima_internal_errors_thread_id: int | None = Field(
        default=None,
        alias="MEANIMA_INTERNAL_ERRORS_THREAD_ID",
    )
    meanima_internal_stats_thread_id: int | None = Field(
        default=None,
        alias="MEANIMA_INTERNAL_STATS_THREAD_ID",
    )

    @property
    def admin_ids(self) -> set[int]:
        """Accepts both one ID (`123`) and a comma-separated list (`123,456`)."""
        values = [item.strip() for item in self.admin_ids_raw.split(",") if item.strip()]
        try:
            return {int(item) for item in values}
        except ValueError as error:
            raise ValueError("ADMIN_IDS должен содержать только числовые Telegram ID через запятую.") from error

    @property
    def owner_admin_id(self) -> int | None:
        """Return the explicitly configured owner, or retain the legacy first-admin fallback."""
        if not self.admin_ids:
            return None
        if not self.owner_admin_id_raw.strip():
            return min(self.admin_ids)
        try:
            owner_id = int(self.owner_admin_id_raw.strip())
        except ValueError as error:
            raise ValueError("OWNER_ADMIN_ID должен содержать числовой Telegram ID.") from error
        if owner_id not in self.admin_ids:
            raise ValueError("OWNER_ADMIN_ID должен быть указан также в ADMIN_IDS.")
        return owner_id

    @property
    def document_urls(self) -> dict[str, str]:
        base = self.document_base_url.rstrip("/")
        return {
            "terms": f"{base}/terms-of-service",
            "privacy": f"{base}/privacy-policy",
            "community": f"{base}/community-guidelines",
            "safety": f"{base}/dating-safety",
            "moderation": f"{base}/moderation-and-appeals",
            "alpha": f"{base}/alpha-notice",
        }

    @property
    def matching_weights(self) -> dict[str, float]:
        defaults = {
            "gender": 35.0,
            "target_gender": 25.0,
            "age": 10.0,
            "district": 10.0,
            "institution": 10.0,
            "interests": 7.0,
            "bio": 3.0,
        }
        if not self.matching_weights_raw:
            return defaults
        try:
            configured = json.loads(self.matching_weights_raw)
        except json.JSONDecodeError as error:
            raise ValueError("MATCHING_WEIGHTS_JSON должен содержать JSON-объект с числовыми весами.") from error
        if not isinstance(configured, dict):
            raise ValueError("MATCHING_WEIGHTS_JSON должен содержать JSON-объект.")
        for name, value in configured.items():
            if (
                name not in defaults
                or isinstance(value, bool)
                or not isinstance(value, int | float)
                or not math.isfinite(value)
                or value < 0
            ):
                raise ValueError(f"Некорректный вес matching: {name!r}.")
            defaults[name] = float(value)
        return defaults


@lru_cache
def get_settings() -> Settings:
    return Settings()
````

## File: handlers/admin.py
````python
import uuid

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import Settings
from keyboards.admin import (
    admin_administration_keyboard,
    admin_keyboard,
    admin_moderation_keyboard,
    admin_nav_keyboard,
    admin_stats_keyboard,
    admin_users_keyboard,
    appeal_decision_keyboard,
    appeal_keyboard,
    case_decision_keyboard,
    case_keyboard,
    confirm_action_keyboard,
    moderation_decision_keyboard,
    moderation_keyboard,
    my_cases_keyboard,
    profile_moderation_keyboard,
    verification_decision_keyboard,
    verification_keyboard,
)
from models import (
    Appeal,
    AppealStatus,
    ModerationCase,
    ModerationCaseStatus,
    ModerationCaseType,
    ModerationStatus,
    Profile,
    Report,
    ReportStatus,
    User,
    UserRole,
    UserStatus,
    VerificationDecision,
    VerificationRequest,
)
from repositories.appeal import AppealRepository
from repositories.profile import ProfileRepository
from repositories.report import ReportRepository
from repositories.trust import TrustRepository
from repositories.user import UserRepository
from services.matching_debug import MatchingDebugService
from services.moderation_service import ModerationService
from services.notification_service import InternalNotificationService, NotificationService
from services.report_service import ReportService
from services.trust_stats_service import TrustStatsService
from services.verification_service import VerificationService
from states.admin import AdminState
from utils.admin_roles import (
    can_access_moderation,
    can_manage_admins,
    can_override_appeal_assignment,
    can_override_case,
    can_unban,
    can_unfreeze,
    can_view_all_profiles,
    can_view_audit_history,
    resolve_admin_role,
)
from utils.admin_ui import compact_display_id, user_display_name
from utils.profile_media import ordered_photo_ids, send_profile_gallery
from utils.text import escape_html

router = Router()


class _SanctionNotApplied(RuntimeError):
    """Roll back a report decision when its paired sanction cannot be applied."""


def allowed(user_id: int, settings: Settings) -> bool:
    return user_id in settings.admin_ids


def admin_role_for_user(user_id: int, settings: Settings, *, user_role: UserRole | None = None) -> UserRole:
    return resolve_admin_role(
        user_id,
        owner_admin_id=settings.owner_admin_id,
        admin_ids=settings.admin_ids,
        user_role=user_role,
    )


async def _safe_edit_message_text(message: Message, text: str, *, reply_markup=None) -> None:
    try:
        if getattr(message, "photo", None) or getattr(message, "caption", None) is not None:
            await message.edit_caption(caption=text, reply_markup=reply_markup, parse_mode="HTML")
            return
        await message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except TelegramBadRequest as exc:
        msg = str(exc).lower()
        if "message is not modified" in msg or "there is no text in the message to edit" in msg:
            try:
                await message.answer(text, reply_markup=reply_markup, parse_mode="HTML")
            except Exception:
                pass
            return
        if "message to edit not found" in msg or "chat not found" in msg:
            return
        raise


async def _safe_callback_answer(callback: CallbackQuery, text: str | None = None, *, show_alert: bool = False) -> None:
    try:
        await callback.answer(text, show_alert=show_alert)
    except TelegramBadRequest as exc:
        msg = str(exc).lower()
        if any(token in msg for token in ("query is too old", "response timeout expired", "query id is invalid")):
            return
        raise


async def _user_label(session: AsyncSession, user_id: int) -> str:
    user = await session.get(User, user_id)
    return user_display_name(user_id, username=user.username if user else None)


async def _admin_label(session: AsyncSession, admin_id: int | None) -> str:
    if admin_id is None:
        return "не назначен"
    user = await session.get(User, admin_id)
    return user_display_name(admin_id, username=user.username if user else None)


async def _assigned_label(session: AsyncSession, assigned_to: int | None) -> str:
    if assigned_to is None:
        return "не закреплено"
    user = await session.get(User, assigned_to)
    return user_display_name(assigned_to, username=user.username if user else None)


async def _case_label(raw_id: str | uuid.UUID) -> str:
    return f"#{compact_display_id(raw_id)}"


async def _role_for_admin(session: AsyncSession, user_id: int, settings: Settings) -> UserRole:
    """Resolve permissions server-side, rather than trusting Telegram UI state."""
    user = await session.get(User, user_id)
    return admin_role_for_user(user_id, settings, user_role=user.role if user else None)


async def _require_admin_capability(
    callback: CallbackQuery, session: AsyncSession, settings: Settings, capability
) -> bool:
    if not allowed(callback.from_user.id, settings) or not capability(
        await _role_for_admin(session, callback.from_user.id, settings)
    ):
        await callback.answer("Недостаточно прав", show_alert=True)
        return False
    return True


async def _render_report(callback: CallbackQuery, session: AsyncSession, report: Report) -> None:
    snapshot = report.evidence_snapshot or {}
    name = escape_html(snapshot.get("name") or "Не указано")
    age = snapshot.get("age") if snapshot.get("age") is not None else "—"
    district = escape_html(snapshot.get("district") or "Не указано")
    institution = escape_html(snapshot.get("institution") or "Не указано")
    bio = escape_html(snapshot.get("bio") or "Не указано")
    profile_info = f"{name}, {age}; {district}; {institution}\n{bio}"
    photo_ids = [item for item in snapshot.get("photo_file_ids", []) if isinstance(item, str) and item]
    photo_note = f"\nФото на момент жалобы: {len(photo_ids)}"
    target_user = await _user_label(session, report.target_user_id)
    created_str = f"\n📅 Создано: {report.created_at:%d.%m.%Y %H:%M}" if getattr(report, "created_at", None) else ""
    assigned_str = await _assigned_label(session, report.assigned_to)
    caption = (
        f"📢 <b>Жалоба #{compact_display_id(report.id)}</b>\n"
        f"👤 Пользователь: {target_user}\n"
        f"⚠️ Причина: {report.reason.value}\n"
        f"📝 Детали: {escape_html(report.details) if report.details else 'не указаны'}"
        f"{created_str}\n"
        f"📊 Статус: {report.status.value}\n"
        f"👤 Закреплено: {assigned_str}\n\n"
        f"📋 <b>Анкета на момент жалобы:</b>\n{profile_info}{photo_note}"
    )
    if report.assigned_to == callback.from_user.id:
        markup = moderation_decision_keyboard(str(report.id))
    elif report.assigned_to is None:
        markup = moderation_keyboard(str(report.id))
    else:
        markup = admin_nav_keyboard(refresh_callback="admin:reports", back_callback="admin:section:moderation")

    if len(photo_ids) > 1:
        media = [
            InputMediaPhoto(media=photo_id, caption=caption if index == 0 else None, parse_mode="HTML")
            for index, photo_id in enumerate(photo_ids)
        ]
        await callback.message.answer_media_group(media)
        await callback.message.answer("Действие модератора:", reply_markup=markup)
        return
    if photo_ids:
        await callback.message.answer_photo(photo_ids[0], caption=caption, parse_mode="HTML", reply_markup=markup)
        return
    await callback.message.answer(caption, parse_mode="HTML", reply_markup=markup)


async def _show_next_report(callback: CallbackQuery, session: AsyncSession) -> None:
    try:
        await callback.message.delete()
    except Exception:
        pass
    items = await ReportRepository(session).pending(callback.from_user.id)
    if not items:
        await callback.message.answer(
            "📭 Очередь жалоб пуста.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:reports", back_callback="admin:section:moderation"
            ),
        )
        return
    await _render_report(callback, session, items[0])


async def _render_photo_case(callback: CallbackQuery, session: AsyncSession, item: ModerationCase) -> None:
    profile = await ProfileRepository(session).by_user_id(item.user_id)
    created_str = f"\n📅 Создано: {item.created_at:%d.%m.%Y %H:%M}" if getattr(item, "created_at", None) else ""
    assigned_str = await _assigned_label(session, item.assigned_to)
    target_user = await _user_label(session, item.user_id)
    caption = (
        f"🖼️ <b>Фото-проверка #{compact_display_id(item.id)}</b>\n"
        f"👤 Пользователь: {target_user}\n"
        f"⚠️ Тип: {item.case_type.value}\n"
        f"📝 Детали: {escape_html(item.details) if item.details else 'не указаны'}"
        f"{created_str}\n"
        f"📊 Статус: {item.status.value}\n"
        f"👤 Закреплено: {assigned_str}"
    )
    if item.assigned_to == callback.from_user.id:
        markup = case_decision_keyboard(str(item.id))
    elif item.assigned_to is None:
        markup = case_keyboard(str(item.id))
    else:
        markup = admin_nav_keyboard(refresh_callback="admin:nsfw", back_callback="admin:section:moderation")
    photos = ordered_photo_ids(profile) if profile else []
    if photos:
        await send_profile_gallery(callback.message, profile, caption, markup)
        return
    photo = await TrustRepository(session).photo_for_case(item.user_id, item.source_id)
    if photo:
        await callback.message.answer_photo(
            photo.photo_file_id,
            caption=caption,
            parse_mode="HTML",
            reply_markup=markup,
        )
    else:
        await callback.message.answer(
            caption + "\n\n⚠️ Исходное фото недоступно; проверьте детали кейса.",
            parse_mode="HTML",
            reply_markup=markup,
        )


async def _show_next_photo_case(callback: CallbackQuery, session: AsyncSession) -> None:
    try:
        await callback.message.delete()
    except Exception:
        pass
    items = await TrustRepository(session).pending_cases()
    items = [
        item
        for item in items
        if item.case_type in {ModerationCaseType.NSFW, ModerationCaseType.NO_FACE, ModerationCaseType.PHOTO_RETAKE}
    ]
    if not items:
        await callback.message.answer(
            "📭 Очередь фото на проверку пуста.",
            reply_markup=admin_nav_keyboard(refresh_callback="admin:nsfw", back_callback="admin:section:moderation"),
        )
        return
    await _render_photo_case(callback, session, items[0])


async def _render_verification(callback: CallbackQuery, session: AsyncSession, item: VerificationRequest) -> None:
    created_str = f"\n📅 Создано: {item.created_at:%d.%m.%Y %H:%M}" if getattr(item, "created_at", None) else ""
    assigned_str = await _assigned_label(session, item.assigned_to)
    target_user = await _user_label(session, item.user_id)
    text = (
        f"🛡 <b>Верификация #{compact_display_id(item.id)}</b>\n"
        f"👤 Пользователь: {target_user}"
        f"{created_str}\n"
        f"📊 Статус: {item.status.value}\n"
        f"👤 Закреплено: {assigned_str}"
    )
    if item.assigned_to == callback.from_user.id:
        markup = verification_decision_keyboard(str(item.id))
    elif item.assigned_to is None:
        markup = verification_keyboard(str(item.id))
    else:
        markup = admin_nav_keyboard(
            refresh_callback="admin:verifications", back_callback="admin:section:moderation"
        )

    await callback.message.answer_video_note(item.video_file_id)
    await callback.message.answer(text, parse_mode="HTML", reply_markup=markup)


async def _show_next_verification(callback: CallbackQuery, session: AsyncSession) -> None:
    try:
        await callback.message.delete()
    except Exception:
        pass
    items = await TrustRepository(session).pending_verifications()
    if not items:
        await callback.message.answer(
            "📭 Очередь верификаций пуста.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:verifications", back_callback="admin:section:moderation"
            ),
        )
        return
    await _render_verification(callback, session, items[0])


async def _render_appeal(callback: CallbackQuery, session: AsyncSession, appeal: Appeal) -> None:
    created_str = f"\n📅 Создано: {appeal.created_at:%d.%m.%Y %H:%M}" if getattr(appeal, "created_at", None) else ""
    assigned_str = await _assigned_label(session, appeal.assigned_to)
    target_user = await _user_label(session, appeal.user_id)
    text = (
        f"⚖️ <b>Апелляция #{compact_display_id(appeal.id)}</b>\n"
        f"👤 Пользователь: {target_user}"
        f"{created_str}\n"
        f"📊 Статус: {appeal.status.value}\n"
        f"👤 Закреплено: {assigned_str}\n\n"
        f"💬 <b>Текст апелляции:</b>\n{escape_html(appeal.text)}"
    )
    if appeal.assigned_to == callback.from_user.id:
        markup = appeal_decision_keyboard(str(appeal.id))
    elif appeal.assigned_to is None:
        markup = appeal_keyboard(str(appeal.id))
    else:
        markup = admin_nav_keyboard(refresh_callback="admin:appeals", back_callback="admin:section:moderation")

    await callback.message.answer(text, parse_mode="HTML", reply_markup=markup)


async def _show_next_appeal(callback: CallbackQuery, session: AsyncSession, moderator_id: int) -> None:
    try:
        await callback.message.delete()
    except Exception:
        pass
    items = await AppealRepository(session).pending(moderator_id)
    if not items:
        await callback.message.answer(
            "📭 Очередь апелляций пуста.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:appeals", back_callback="admin:section:moderation"
            ),
        )
        return
    await _render_appeal(callback, session, items[0])


async def _render_admin_browse_profile(
    callback: CallbackQuery, session: AsyncSession, target_id: int, actor_role: UserRole
) -> None:
    target = await session.get(User, target_id)
    if target is None:
        await callback.answer("Анкета не найдена.", show_alert=True)
        return
    profile = await ProfileRepository(session).by_user_id(target.id)
    if profile is None:
        await callback.answer("У пользователя нет активной анкеты.", show_alert=True)
        return
    is_banned = target.status == UserStatus.BANNED
    is_frozen = target.status == UserStatus.SUSPENDED
    user_can_unban = can_unban(actor_role)

    caption = (
        f"🔎 <b>Просмотр анкеты</b>\n"
        f"👤 Пользователь: {user_display_name(target.id, username=target.username)}\n"
        f"📊 Статус аккаунта: {target.status.value}\n"
        f"🛡 Модерация анкеты: {profile.moderation_status.value}\n"
        f"🎖 Роль: {target.role.value}\n"
        f"⭐ Trust Score: {target.trust_score}\n\n"
        f"👤 <b>{escape_html(profile.name)}</b>, {profile.age}\n"
        f"📍 Район: {escape_html(profile.district)}\n"
        f"🏫 Учёба/работа: {escape_html(profile.institution)}\n"
        f"📝 О себе: {escape_html(profile.bio or 'Без описания')}"
    )
    markup = profile_moderation_keyboard(
        target.id,
        next_callback=f"admin:browse:next:{target.id}",
        can_unban=user_can_unban,
        is_banned=is_banned,
        is_frozen=is_frozen,
    )
    await send_profile_gallery(callback.message, profile, caption, markup)


async def _next_browse_user(session: AsyncSession, current_user_id: int | None = None) -> User | None:
    statement = select(User).join(Profile).order_by(User.id).limit(1)
    if current_user_id is not None:
        statement = select(User).join(Profile).where(User.id > current_user_id).order_by(User.id).limit(1)
    target = await session.scalar(statement)
    if target is None and current_user_id is not None:
        target = await session.scalar(select(User).join(Profile).order_by(User.id).limit(1))
    return target


@router.message(Command("admin"))
async def admin(message: Message, session: AsyncSession, settings: Settings) -> None:
    if not allowed(message.from_user.id, settings):
        return
    role = await _role_for_admin(session, message.from_user.id, settings)
    await message.answer(
        "🛡 <b>Панель модерации</b>\nВыберите раздел:",
        reply_markup=admin_keyboard(role_can_manage_admins=can_manage_admins(role)),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "admin:menu")
async def admin_menu(callback: CallbackQuery, session: AsyncSession, settings: Settings, state: FSMContext) -> None:
    if not allowed(callback.from_user.id, settings):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    await state.clear()
    role = await _role_for_admin(session, callback.from_user.id, settings)
    await _safe_edit_message_text(
        callback.message,
        "🛡 <b>Панель модерации</b>\nВыберите раздел:",
        reply_markup=admin_keyboard(role_can_manage_admins=can_manage_admins(role)),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:section:moderation")
async def section_moderation(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    await _safe_edit_message_text(
        callback.message,
        "🛡 <b>Раздел модерации</b>\nВыберите категорию для проверки:",
        reply_markup=admin_moderation_keyboard(),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:section:users")
async def section_users(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_view_all_profiles):
        return
    await _safe_edit_message_text(
        callback.message,
        "👤 <b>Управление пользователями</b>\nВыберите действие:",
        reply_markup=admin_users_keyboard(),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:section:stats")
async def section_stats(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    role = await _role_for_admin(session, callback.from_user.id, settings)
    await _safe_edit_message_text(
        callback.message,
        "📊 <b>Статистика и аналитика</b>\nВыберите раздел:",
        reply_markup=admin_stats_keyboard(can_view_history=can_view_audit_history(role)),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:section:administration")
async def section_administration(
    callback: CallbackQuery, session: AsyncSession, settings: Settings, state: FSMContext
) -> None:
    if not await _require_admin_capability(callback, session, settings, can_manage_admins):
        return
    await state.clear()
    await _safe_edit_message_text(
        callback.message,
        "⚙️ <b>Панель администратора</b>\nВыберите действие:",
        reply_markup=admin_administration_keyboard(),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:my_cases")
async def my_cases(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    moderator_id = callback.from_user.id

    my_reports = list(
        (
            await session.scalars(
                select(Report).where(Report.assigned_to == moderator_id, Report.status == ReportStatus.PENDING)
            )
        ).all()
    )
    my_cases_list = list(
        (
            await session.scalars(
                select(ModerationCase).where(
                    ModerationCase.assigned_to == moderator_id,
                    ModerationCase.status == ModerationCaseStatus.IN_PROGRESS,
                )
            )
        ).all()
    )
    my_verifications = list(
        (
            await session.scalars(
                select(VerificationRequest).where(
                    VerificationRequest.assigned_to == moderator_id,
                    VerificationRequest.status == VerificationDecision.PENDING,
                )
            )
        ).all()
    )
    my_appeals = list(
        (
            await session.scalars(
                select(Appeal).where(Appeal.assigned_to == moderator_id, Appeal.status == AppealStatus.PENDING)
            )
        ).all()
    )

    items: list[tuple[str, str]] = []
    for r in my_reports:
        items.append((f"📢 Жалоба #{compact_display_id(r.id)}", f"mycase:report:{r.id}"))
    for c in my_cases_list:
        items.append((f"🖼️ Кейс #{compact_display_id(c.id)}", f"mycase:case:{c.id}"))
    for v in my_verifications:
        items.append((f"🛡 Верификация #{compact_display_id(v.id)}", f"mycase:verify:{v.id}"))
    for a in my_appeals:
        items.append((f"⚖️ Апелляция #{compact_display_id(a.id)}", f"mycase:appeal:{a.id}"))

    total = len(items)
    if total == 0:
        text = "📌 <b>Мои кейсы</b>\n\nУ вас нет активных кейсов в работе."
    else:
        text = (
            f"📌 <b>Мои кейсы в работе ({total}):</b>\n"
            f"• 📢 Жалобы: {len(my_reports)}\n"
            f"• 🖼️ Фото-кейсы: {len(my_cases_list)}\n"
            f"• 🛡 Верификации: {len(my_verifications)}\n"
            f"• ⚖️ Апелляции: {len(my_appeals)}\n\n"
            f"Выберите кейс для перехода к решению:"
        )

    await _safe_edit_message_text(callback.message, text, reply_markup=my_cases_keyboard(items))
    await _safe_callback_answer(callback)


@router.callback_query(F.data.startswith("mycase:"))
async def mycase_open(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    parts = (callback.data or "").split(":")
    if len(parts) != 3:
        await callback.answer("Некорректный кейс", show_alert=True)
        return
    _, item_type, raw_id = parts
    try:
        item_id = uuid.UUID(raw_id)
    except ValueError:
        await callback.answer("Некорректный идентификатор", show_alert=True)
        return

    try:
        await callback.message.delete()
    except Exception:
        pass

    if item_type == "report":
        report = await ReportRepository(session).get(item_id)
        if not report:
            await callback.message.answer("Жалоба не найдена.", reply_markup=admin_nav_keyboard())
            await _safe_callback_answer(callback, "Жалоба уже удалена.", show_alert=True)
            return
        await _render_report(callback, session, report)
    elif item_type == "case":
        case = await TrustRepository(session).case(item_id)
        if not case:
            await callback.message.answer("Кейс не найден.", reply_markup=admin_nav_keyboard())
            await _safe_callback_answer(callback, "Кейс уже удалён.", show_alert=True)
            return
        await _render_photo_case(callback, session, case)
    elif item_type == "verify":
        req = await TrustRepository(session).verification(item_id)
        if not req:
            await callback.message.answer("Верификация не найдена.", reply_markup=admin_nav_keyboard())
            await _safe_callback_answer(callback, "Верификация уже удалена.", show_alert=True)
            return
        await _render_verification(callback, session, req)
    elif item_type == "appeal":
        appeal = await AppealRepository(session).get(item_id)
        if not appeal:
            await callback.message.answer("Апелляция не найдена.", reply_markup=admin_nav_keyboard())
            await _safe_callback_answer(callback, "Апелляция уже удалена.", show_alert=True)
            return
        await _render_appeal(callback, session, appeal)
    await _safe_callback_answer(callback)


@router.message(Command("debug_matching"))
async def debug_matching(message: Message, session: AsyncSession, settings: Settings) -> None:
    if not allowed(message.from_user.id, settings):
        return
    report = await MatchingDebugService(session, weights=settings.matching_weights).report_for(message.from_user.id)
    excluded = [item for item in report.candidates if not item.included]
    lines = [
        "<b>Matching debug</b>",
        f"Пользователей: {report.stats.users}; активных: {report.stats.active_users}",
        f"Просмотров: {report.stats.views}; лайков: {report.stats.likes}; матчей: {report.stats.matches}",
        f"CTR: {report.stats.ctr}%; средняя совместимость: {report.stats.average_compatibility}%",
        f"Кандидатов после базовых фильтров: {len(report.candidates)}",
        f"Прошли фильтр пола/цели: {report.gender_compatible}",
        (
            f"Релевантный возраст: {report.age_relevant}; совпали районы: {report.same_district}; "
            f"общие интересы: {report.shared_interests}"
        ),
        f"В очереди: {len(report.candidates) - len(excluded)}",
        "Исключения:",
    ]
    if excluded:
        lines.extend(f"• {item.candidate_id}: {', '.join(item.reasons)}" for item in excluded[:50])
    else:
        lines.append("• нет")
    await message.answer("\n".join(lines), parse_mode="HTML")


@router.callback_query(F.data == "admin:reports")
async def reports(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    await _show_next_report(callback, session)
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:browse")
async def admin_browse(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_view_all_profiles):
        return
    target = await _next_browse_user(session)
    if target is None:
        await callback.message.answer(
            "👥 Анкеты отсутствуют.",
            reply_markup=admin_nav_keyboard(refresh_callback="admin:browse", back_callback="admin:section:users"),
        )
        await _safe_callback_answer(callback)
        return
    role = await _role_for_admin(session, callback.from_user.id, settings)
    await _render_admin_browse_profile(callback, session, target.id, role)
    await _safe_callback_answer(callback)


@router.callback_query(F.data.startswith("admin:browse:next"))
async def admin_browse_next(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_view_all_profiles):
        return
    parts = (callback.data or "").split(":")
    current_user_id = None
    if len(parts) >= 4 and parts[1] == "browse" and parts[2] == "next":
        try:
            current_user_id = int(parts[3])
        except ValueError:
            current_user_id = None
    target = await _next_browse_user(session, current_user_id)
    if target is None:
        await callback.message.answer(
            "👥 Анкеты отсутствуют.",
            reply_markup=admin_nav_keyboard(refresh_callback="admin:browse", back_callback="admin:section:users"),
        )
        await _safe_callback_answer(callback)
        return
    role = await _role_for_admin(session, callback.from_user.id, settings)
    await _render_admin_browse_profile(callback, session, target.id, role)
    await _safe_callback_answer(callback, "Следующая анкета")


@router.callback_query(F.data.startswith("profilemod:"))
async def profile_moderation_action(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    parts = (callback.data or "").split(":")
    if len(parts) == 4 and parts[1] == "prompt":
        _, _, action, raw_user_id = parts
        action_names = {
            "ban": "заблокировать",
            "freeze": "заморозить",
            "unban": "разблокировать",
            "unfreeze": "разморозить",
        }
        action_name = action_names.get(action)
        if action_name is None:
            await callback.answer("Некорректное действие", show_alert=True)
            return
        await _safe_edit_message_text(
            callback.message,
            f"⚠️ <b>Подтверждение действия</b>\nВы действительно хотите {action_name} пользователя?",
            reply_markup=confirm_action_keyboard(
                f"profilemod:execute:{action}:{raw_user_id}", back_data="admin:browse"
            ),
        )
        await _safe_callback_answer(callback)
        return
    if len(parts) != 4 or parts[1] != "execute":
        await callback.answer("Некорректное действие", show_alert=True)
        return
    _, _, action, raw_user_id = parts
    try:
        user_id = int(raw_user_id)
    except ValueError:
        await callback.answer("Некорректный пользователь", show_alert=True)
        return
    actor_role = await _role_for_admin(session, callback.from_user.id, settings)
    service = ModerationService(session)
    if user_id == callback.from_user.id:
        await callback.answer("Нельзя применить санкцию к самому себе.", show_alert=True)
        return
    if action == "ban":
        changed = await service.ban(user_id, callback.from_user.id, reason="manual moderation", actor_role=actor_role)
        result = "Пользователь заблокирован."
    elif action == "freeze":
        changed = await service.suspend(
            user_id,
            callback.from_user.id,
            reason="manual moderation",
            actor_role=actor_role,
        )
        result = "Анкета заморожена."
    elif action == "unban":
        if not can_unban(actor_role):
            await callback.answer("Недостаточно прав для разблокировки.", show_alert=True)
            return
        changed = await service.unban(user_id, callback.from_user.id, actor_role=actor_role)
        result = "Пользователь разблокирован."
    elif action == "unfreeze":
        if not can_unfreeze(actor_role):
            await callback.answer("Недостаточно прав для разморозки.", show_alert=True)
            return
        target_user = await session.get(User, user_id)
        if target_user is None or target_user.status != UserStatus.SUSPENDED:
            await callback.answer("Пользователь не находится в заморозке.", show_alert=True)
            return
        target_user.status = UserStatus.ACTIVE
        target_profile = await ProfileRepository(session).by_user_id(user_id)
        if target_profile:
            target_profile.is_visible = True
            target_profile.moderation_locked = False
            target_profile.moderation_status = ModerationStatus.CLEAR
        await TrustRepository(session).log(
            callback.from_user.id,
            "UNFREEZE",
            target_type="user",
            target_id=str(user_id),
            target_user_id=user_id,
            details="manual unfreeze",
        )
        await session.flush()
        changed = True
        result = "Анкета разморожена."
    else:
        await callback.answer("Некорректное действие", show_alert=True)
        return
    if not changed:
        await callback.answer("Действие недоступно для этого пользователя.", show_alert=True)
        return
    await InternalNotificationService(callback.bot, settings).send_moderation_event(
        "Ручная санкция модератора",
        user_id=user_id,
        details=f"Action: {action}; moderator: {callback.from_user.id}",
        event_key=f"profile-{action}:{user_id}",
        target_callback="admin:browse",
    )
    await _safe_edit_message_text(
        callback.message,
        f"✅ {result}",
        reply_markup=admin_nav_keyboard(refresh_callback="admin:browse", back_callback="admin:section:users"),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:verifications")
async def verification_queue(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    await _show_next_verification(callback, session)
    await _safe_callback_answer(callback)


@router.callback_query(F.data.startswith("verify:"))
async def verification_decision(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    try:
        _, action, raw_id = callback.data.split(":")
        if action == "claim":
            request_id = uuid.UUID(raw_id)
            request = await VerificationService(session).claim(request_id, callback.from_user.id)
            if request is None:
                await callback.answer("Заявка уже взята или обработана.", show_alert=True)
                return
            await callback.message.edit_reply_markup(reply_markup=verification_decision_keyboard(str(request.id)))
            await callback.answer("Заявка закреплена за вами.")
            return
        decision = {
            "approve": VerificationDecision.APPROVED,
            "reject": VerificationDecision.REJECTED,
            "retake": VerificationDecision.RETAKE_REQUESTED,
        }.get(action)
        if decision is None and action != "release":
            raise KeyError(action)
        request_id = uuid.UUID(raw_id)
    except (KeyError, ValueError):
        await callback.answer("Некорректное решение", show_alert=True)
        return
    actor_role = await _role_for_admin(session, callback.from_user.id, settings)
    if action == "release":
        request, changed = await VerificationService(session).release(
            request_id, callback.from_user.id, actor_role=actor_role
        )
        if not changed:
            await callback.answer("Заявка уже освобождена или недоступна.", show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id,
            "VERIFICATION_RELEASED",
            target_type="verification",
            target_id=str(request.id),
            target_user_id=request.user_id,
        )
        await _safe_edit_message_text(
            callback.message,
            "✅ Верификация освобождена и возвращена в общую очередь.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:verifications", back_callback="admin:section:moderation"
            ),
        )
        await _safe_callback_answer(callback)
        return
    request, changed = await VerificationService(session).decide(
        request_id,
        callback.from_user.id,
        decision,
        actor_role=actor_role,
    )
    if not changed:
        handled_by = await _admin_label(session, request.admin_id if request else None)
        await callback.answer(f"Эта верификация уже обработана модератором {handled_by}.", show_alert=True)
        return
    messages = {
        VerificationDecision.APPROVED: "🟢 Верификация подтверждена.",
        VerificationDecision.REJECTED: "❌ Верификация отклонена.",
        VerificationDecision.RETAKE_REQUESTED: "🔁 Пожалуйста, запишите кружок ещё раз.",
    }
    await NotificationService(callback.bot).safe_send(request.user_id, messages[decision])
    await _safe_edit_message_text(
        callback.message,
        f"✅ Решение сохранено: {decision.value}",
        reply_markup=admin_nav_keyboard(
            refresh_callback="admin:verifications", back_callback="admin:section:moderation"
        ),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:nsfw")
async def nsfw_queue(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    await _show_next_photo_case(callback, session)
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:blocked")
async def blocked_users(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    users = list((await session.scalars(select(User).where(User.status == UserStatus.BANNED).limit(30))).all())
    if not users:
        await _safe_edit_message_text(
            callback.message,
            "🚫 <b>Заблокированные пользователи</b>\n\nЗаблокированных пользователей нет.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:blocked", back_callback="admin:section:users"
            ),
        )
    else:
        names = []
        for user in users:
            label = user_display_name(user.id, username=user.username)
            names.append(f"• {label} (ID: <code>{user.id}</code>)")
        text = (
            f"🚫 <b>Заблокированные пользователи ({len(users)}):</b>\n\n"
            + "\n".join(names)
            + "\n\n<i>Для управления статусом перейдите в «Просмотр анкет».</i>"
        )
        await _safe_edit_message_text(
            callback.message,
            text,
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:blocked", back_callback="admin:section:users"
            ),
        )
    await _safe_callback_answer(callback)


@router.callback_query(F.data.startswith("case:"))
async def moderation_case(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    try:
        _, action, raw_id = callback.data.split(":")
        case_id = uuid.UUID(raw_id)
    except ValueError:
        await callback.answer("Некорректный кейс", show_alert=True)
        return
    service = ModerationService(session)
    actor_role = await _role_for_admin(session, callback.from_user.id, settings)
    if action == "claim":
        case, changed, reason = await service.claim_case(case_id, callback.from_user.id, actor_role=actor_role)
        if not changed:
            if reason == "already_assigned":
                handled_by = await _admin_label(session, case.assigned_to if case else None)
                await callback.answer(f"Кейс уже взял {handled_by}.", show_alert=True)
            else:
                await callback.answer("Кейс уже нельзя взять в работу.", show_alert=True)
            return
        await InternalNotificationService(callback.bot, settings).send_moderation_event(
            "Кейс взят в работу",
            user_id=case.user_id,
            case_id=str(case.id),
            details=f"Moderator: {callback.from_user.id}",
            event_key=f"case-claimed:{case.id}",
            target_callback=f"mycase:case:{case.id}",
        )
        await callback.message.edit_reply_markup(reply_markup=case_decision_keyboard(str(case.id)))
        await callback.answer("Кейс закреплён за вами.")
        return
    if action == "release":
        case, changed, reason = await service.release_case(
            case_id, callback.from_user.id, moderator_id=callback.from_user.id
        )
        if not changed:
            await callback.answer(reason or "Кейс уже освобождён или недоступен.", show_alert=True)
            return
        await _safe_edit_message_text(
            callback.message,
            "✅ Кейс освобождён и возвращён в общую очередь.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:nsfw", back_callback="admin:section:moderation"
            ),
        )
        await _safe_callback_answer(callback)
        return
    if action not in {"restore", "retake", "reject"}:
        await callback.answer("Некорректное решение по кейсу.", show_alert=True)
        return
    case, changed, _ = await service.resolve_case(
        case_id,
        callback.from_user.id,
        restore=action in {"restore", "reject"},
        retake=action == "retake",
        actor_role=actor_role,
    )
    if not changed:
        handled_by = await _admin_label(session, case.admin_id if case else None)
        await callback.answer(f"Этот кейс уже обработан модератором {handled_by}.", show_alert=True)
        return
    if action in {"restore", "reject"}:
        user_message = "✅ Фото одобрено. Ваша анкета снова видна в знакомствах."
        result = (
            "✅ Кейс отклонён, анкета восстановлена."
            if action == "reject"
            else "✅ Фото одобрено, анкета восстановлена."
        )
    else:
        user_message = (
            "📝 Фото нужно заменить. Откройте «Моя анкета» → «Управлять фото» "
            "и загрузите новое фото. Анкета останется скрытой до отдельного "
            "решения модератора."
        )
        result = "📝 Пользователю отправлен запрос на замену фотографии; ограничение сохранено."
    await NotificationService(callback.bot).safe_send(case.user_id, user_message)
    await InternalNotificationService(callback.bot, settings).send_moderation_event(
        "Кейс решён",
        user_id=case.user_id,
        case_id=str(case.id),
        details=f"Decision: {action}; moderator: {callback.from_user.id}",
        event_key=f"case-resolved:{case.id}",
    )
    await _safe_edit_message_text(
        callback.message,
        result,
        reply_markup=admin_nav_keyboard(refresh_callback="admin:nsfw", back_callback="admin:section:moderation"),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:trust_history")
async def trust_history(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_view_audit_history):
        return
    items = await TrustRepository(session).history()
    lines = ["📜 <b>История решений модерации:</b>\n"] + [
        f"• {item.created_at:%d.%m %H:%M}: <code>{item.action}</code> → {item.target_id or '—'}" for item in items
    ]
    text = "\n".join(lines[:31]) if items else "История решений пуста."
    await _safe_edit_message_text(
        callback.message,
        text,
        reply_markup=admin_nav_keyboard(
            refresh_callback="admin:trust_history", back_callback="admin:section:stats"
        ),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:trust_stats")
async def trust_stats(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    stats = await TrustStatsService(session).snapshot()
    text = (
        "📊 <b>Общая статистика Trust</b>\n\n"
        f"• Проверенных пользователей: <b>{stats['verified']}</b>\n"
        f"• Всего жалоб: <b>{stats['reports']}</b>\n"
        f"• Ложных жалоб: <b>{stats['false_reports']}</b>\n"
        f"• Подтверждённых нарушений: <b>{stats['confirmed_fakes']}</b>\n"
        f"• Средний Trust Score: <b>{stats['average_trust_score']}</b>"
    )
    await _safe_edit_message_text(
        callback.message,
        text,
        reply_markup=admin_nav_keyboard(
            refresh_callback="admin:trust_stats", back_callback="admin:section:stats"
        ),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data.startswith("moderate:"))
async def moderate(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    parts = (callback.data or "").split(":")
    if not parts or parts[0] != "moderate":
        return
    if len(parts) == 4 and parts[1] == "prompt":
        _, _, action, raw_id = parts
        action_text = {
            "ban": "заблокировать пользователя",
            "hide": "скрыть анкету",
            "dismiss": "отклонить жалобу",
        }.get(action)
        if action_text is None:
            await callback.answer("Некорректное действие", show_alert=True)
            return
        try:
            report_id = uuid.UUID(raw_id)
        except ValueError:
            await callback.answer("Некорректная жалоба", show_alert=True)
            return
        repo = ReportRepository(session)
        report = await repo.get(report_id)
        if report is None or report.status != ReportStatus.PENDING:
            await callback.answer("Жалоба уже обработана", show_alert=True)
            return
        if report.assigned_to != callback.from_user.id:
            await callback.answer("Сначала возьмите жалобу в работу.", show_alert=True)
            return
        confirm_data = f"moderate:execute:{action}:{raw_id}"
        await _safe_edit_message_text(
            callback.message,
            f"⚠️ <b>Подтвердите действие:</b> {action_text}.\n\nПосле подтверждения это действие нельзя будет отменить.",
            reply_markup=confirm_action_keyboard(confirm_data, back_data="admin:reports"),
        )
        await _safe_callback_answer(callback)
        return
    if len(parts) == 3 and parts[1] == "claim":
        _, _, raw_id = parts
        try:
            report_id = uuid.UUID(raw_id)
        except ValueError:
            await callback.answer("Некорректная жалоба", show_alert=True)
            return
        report = await ReportRepository(session).claim(report_id, callback.from_user.id)
        if report is None:
            await callback.answer("Жалоба уже взята или обработана.", show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id,
            "REPORT_CLAIMED",
            target_type="report",
            target_id=str(report.id),
            target_user_id=report.target_user_id,
        )
        await callback.message.edit_reply_markup(reply_markup=moderation_decision_keyboard(str(report.id)))
        await callback.answer("Жалоба закреплена за вами.")
        return
    if len(parts) == 3 and parts[1] == "release":
        _, _, raw_id = parts
        try:
            report_id = uuid.UUID(raw_id)
        except ValueError:
            await callback.answer("Некорректная жалоба", show_alert=True)
            return
        role = await _role_for_admin(session, callback.from_user.id, settings)
        released = await ReportRepository(session).release(
            report_id, callback.from_user.id, override=can_override_case(role)
        )
        if released is None:
            await callback.answer("Жалоба уже освобождена или недоступна.", show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id,
            "REPORT_RELEASED",
            target_type="report",
            target_id=str(released.id),
            target_user_id=released.target_user_id,
        )
        await _safe_edit_message_text(
            callback.message,
            "✅ Жалоба освобождена и возвращена в общую очередь.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:reports", back_callback="admin:section:moderation"
            ),
        )
        await _safe_callback_answer(callback)
        return
    if len(parts) == 4 and parts[1] == "execute":
        _, _, action, raw_id = parts
    elif len(parts) == 3:
        _, action, raw_id = parts
    else:
        await callback.answer("Некорректная жалоба", show_alert=True)
        return
    try:
        report_id = uuid.UUID(raw_id)
    except ValueError:
        await callback.answer("Некорректная жалоба", show_alert=True)
        return
    repo = ReportRepository(session)
    report = await repo.get(report_id)
    if report is None or report.status != ReportStatus.PENDING:
        await callback.answer("Жалоба уже обработана", show_alert=True)
        return
    if report.assigned_to != callback.from_user.id:
        await callback.answer("Сначала возьмите жалобу в работу.", show_alert=True)
        return
    if action == "ban":
        try:
            async with session.begin_nested():
                resolved = await ReportService(session, threshold=settings.report_threshold).confirm_fake(
                    report_id, callback.from_user.id
                )
                if resolved is None:
                    raise _SanctionNotApplied
                banned = await ModerationService(session).ban(
                    report.target_user_id,
                    callback.from_user.id,
                    reason="report",
                    actor_role=await _role_for_admin(session, callback.from_user.id, settings),
                )
                if not banned:
                    raise _SanctionNotApplied
        except _SanctionNotApplied:
            await callback.answer("Не удалось применить блокировку", show_alert=True)
            return
        result = "Пользователь заблокирован."
    elif action == "hide":
        try:
            async with session.begin_nested():
                resolved = await repo.resolve(report_id, ReportStatus.APPROVED, admin_id=callback.from_user.id)
                if resolved is None:
                    raise _SanctionNotApplied
                suspended = await ModerationService(session).suspend(
                    report.target_user_id,
                    callback.from_user.id,
                    reason="report",
                    actor_role=await _role_for_admin(session, callback.from_user.id, settings),
                )
                if not suspended:
                    raise _SanctionNotApplied
        except _SanctionNotApplied:
            await callback.answer("Не удалось применить ограничение", show_alert=True)
            return
        await NotificationService(callback.bot).safe_send(
            report.target_user_id,
            "⏸ Ваша анкета временно приостановлена модерацией. Вы можете нажать «🆘 Апелляция» и описать ситуацию.",
        )
        result = "Анкета приостановлена и скрыта. Пользователю предложена апелляция."
    elif action == "dismiss":
        resolved = await ReportService(session, threshold=settings.report_threshold).dismiss(
            report_id, callback.from_user.id
        )
        if resolved is None:
            await callback.answer("Жалоба уже обработана", show_alert=True)
            return
        result = "Жалоба отклонена."
    else:
        await callback.answer("Некорректное действие", show_alert=True)
        return
    await InternalNotificationService(callback.bot, settings).send_moderation_event(
        "Решение по жалобе",
        user_id=report.target_user_id,
        case_id=str(report.id),
        details=f"Decision: {action}; moderator: {callback.from_user.id}",
        event_key=f"report-decision:{report.id}",
        target_callback=f"mycase:report:{report.id}",
    )
    await _safe_edit_message_text(
        callback.message,
        f"✅ {result}",
        reply_markup=admin_nav_keyboard(refresh_callback="admin:reports", back_callback="admin:section:moderation"),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:appeals")
async def appeals(callback: CallbackQuery, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    await _show_next_appeal(callback, session, callback.from_user.id)
    await _safe_callback_answer(callback)


@router.callback_query(F.data.startswith("appeal:"))
async def appeal_action(callback: CallbackQuery, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    if not await _require_admin_capability(callback, session, settings, can_access_moderation):
        return
    parts = (callback.data or "").split(":")
    if len(parts) == 3 and parts[1] == "claim":
        try:
            appeal_id = uuid.UUID(parts[2])
        except ValueError:
            await callback.answer("Некорректная апелляция", show_alert=True)
            return
        appeal = await AppealRepository(session).claim(appeal_id, callback.from_user.id)
        if appeal is None:
            await callback.answer("Апелляция уже взята или обработана.", show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id,
            "APPEAL_CLAIMED",
            target_type="appeal",
            target_id=str(appeal.id),
            target_user_id=appeal.user_id,
        )
        await callback.message.edit_reply_markup(reply_markup=appeal_decision_keyboard(str(appeal.id)))
        await callback.answer("Апелляция закреплена за вами.")
        return
    if len(parts) == 4 and parts[1] == "prompt":
        _, _, action, raw_id = parts
        action_name = "отклонение апелляции" if action == "reject" else "одобрение апелляции"
        try:
            appeal_id = uuid.UUID(raw_id)
        except ValueError:
            await callback.answer("Некорректная апелляция", show_alert=True)
            return
        repo = AppealRepository(session)
        appeal = await repo.get(appeal_id)
        if appeal is None or appeal.status != AppealStatus.PENDING:
            await callback.answer("Апелляция уже обработана", show_alert=True)
            return
        if appeal.assigned_to != callback.from_user.id:
            await callback.answer("Сначала возьмите апелляцию в работу.", show_alert=True)
            return
        await _safe_edit_message_text(
            callback.message,
            f"⚠️ <b>Подтвердите {action_name}.</b>\n\nПосле подтверждения решение нельзя будет отменить.",
            reply_markup=confirm_action_keyboard(f"appeal:execute:{action}:{raw_id}", back_data="admin:appeals"),
        )
        await _safe_callback_answer(callback)
        return
    if len(parts) == 4 and parts[1] == "execute":
        _, _, action, raw_id = parts
    else:
        try:
            _, action, raw_id = parts
        except (ValueError, TypeError):
            await callback.answer("Некорректная апелляция", show_alert=True)
            return
    try:
        appeal_id = uuid.UUID(raw_id)
    except (ValueError, TypeError):
        await callback.answer("Некорректная апелляция", show_alert=True)
        return
    repo = AppealRepository(session)
    appeal = await repo.get(appeal_id)
    if appeal is None or appeal.status != AppealStatus.PENDING:
        await callback.answer("Апелляция уже обработана", show_alert=True)
        return
    actor_role = await _role_for_admin(session, callback.from_user.id, settings)
    override = can_override_appeal_assignment(actor_role)
    if action == "release":
        released = await repo.release(appeal_id, callback.from_user.id, override=override)
        if released is None:
            await callback.answer("Апелляция уже освобождена или недоступна.", show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id,
            "APPEAL_RELEASED",
            target_type="appeal",
            target_id=str(released.id),
            target_user_id=released.user_id,
        )
        await _safe_edit_message_text(
            callback.message,
            "✅ Апелляция освобождена и возвращена в общую очередь.",
            reply_markup=admin_nav_keyboard(
                refresh_callback="admin:appeals", back_callback="admin:section:moderation"
            ),
        )
        await _safe_callback_answer(callback)
        return
    if appeal.assigned_to != callback.from_user.id and not override:
        await callback.answer("Сначала возьмите апелляцию в работу.", show_alert=True)
        return
    if action == "reply":
        user = await UserRepository(session).get(appeal.user_id)
        username = user.username if user else None
        contact = f"@{username}" if username else f"ID: {appeal.user_id}"
        template = (
            "Здравствуйте. Я модератор MeAnima. Пишу вам по поводу вашей "
            "апелляции на ограничение анкеты. Расскажите, пожалуйста, что "
            "произошло..."
        )
        await callback.message.answer(
            "💬 <b>Связь с пользователем:</b>\n"
            "Напишите пользователю со своего личного Telegram-аккаунта.\n\n"
            f"👤 Контакт: <b>{contact}</b>\n"
            f'📝 Шаблон сообщения: "<i>{template}</i>"\n\n'
            "<i>Бот не отправляет это сообщение и не является посредником переписки.</i>",
            parse_mode="HTML",
            reply_markup=admin_nav_keyboard(refresh_callback="admin:appeals", back_callback="admin:appeals"),
        )
        await _safe_callback_answer(callback)
        return
    if action in {"restore", "approve"}:
        restored, restore_reason = await ModerationService(session).restore_appeal_sanction(
            appeal, callback.from_user.id, actor_role=actor_role
        )
        if not restored:
            message = (
                "Недостаточно прав для снятия ограничения."
                if restore_reason == "forbidden"
                else "Нельзя снять это ограничение: есть другая открытая санкция."
                if restore_reason == "other_open_sanction"
                else "Ограничение уже не может быть снято."
            )
            await callback.answer(message, show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id, "appeal_restored", target_type="appeal", target_id=str(appeal_id)
        )
        await NotificationService(callback.bot).safe_send(
            appeal.user_id,
            "✅ Апелляция одобрена. Ограничение снято; при желании включите видимость анкеты.",
        )
        result = "Апелляция одобрена, аккаунт восстановлен."
    elif action in {"reject", "execute"}:
        resolved = await repo.resolve(appeal_id, AppealStatus.REJECTED, callback.from_user.id)
        if resolved is None:
            await callback.answer("Апелляция уже обработана", show_alert=True)
            return
        await TrustRepository(session).log(
            callback.from_user.id, "appeal_rejected", target_type="appeal", target_id=str(appeal_id)
        )
        await NotificationService(callback.bot).safe_send(
            appeal.user_id, "❌ Апелляция отклонена. Анкета остаётся приостановленной."
        )
        result = "Апелляция отклонена."
    else:
        await callback.answer("Некорректная апелляция", show_alert=True)
        return
    await InternalNotificationService(callback.bot, settings).send_moderation_event(
        "Решение по апелляции",
        user_id=appeal.user_id,
        case_id=str(appeal.id),
        details=f"Decision: {action}; moderator: {callback.from_user.id}",
        event_key=f"appeal-decision:{appeal.id}",
        target_callback=f"mycase:appeal:{appeal.id}",
    )
    await _safe_edit_message_text(
        callback.message,
        f"✅ {result}",
        reply_markup=admin_nav_keyboard(refresh_callback="admin:appeals", back_callback="admin:section:moderation"),
    )
    await _safe_callback_answer(callback)


@router.callback_query(F.data == "admin:broadcast")
async def broadcast_start(callback: CallbackQuery, state: FSMContext, settings: Settings) -> None:
    if not allowed(callback.from_user.id, settings):
        await callback.answer("Недостаточно прав", show_alert=True)
        return
    await state.set_state(AdminState.broadcast_message)
    await _safe_edit_message_text(
        callback.message,
        "📣 <b>Рассылка сообщений</b>\n\nОтправьте текст рассылки. Его получат все активные пользователи.",
        reply_markup=admin_nav_keyboard(back_callback="admin:section:administration"),
    )
    await _safe_callback_answer(callback)


@router.message(AdminState.broadcast_message)
async def broadcast_send(message: Message, state: FSMContext, session: AsyncSession, settings: Settings) -> None:
    if not allowed(message.from_user.id, settings):
        await state.clear()
        return
    text = (message.text or "").strip()
    if not 1 <= len(text) <= 4000:
        await message.answer("Текст должен содержать от 1 до 4000 символов.")
        return
    notifier = NotificationService(message.bot)
    delivered = 0
    for user_id in await UserRepository(session).all_ids():
        delivered += await notifier.safe_send(user_id, text)
    await state.clear()
    await message.answer(
        f"✅ <b>Рассылка завершена.</b>\nДоставлено пользователям: <b>{delivered}</b>.",
        reply_markup=admin_nav_keyboard(back_callback="admin:section:administration"),
        parse_mode="HTML",
    )
````

## File: handlers/registration.py
````python
from __future__ import annotations

from typing import Any

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from sqlalchemy.ext.asyncio import AsyncSession

from dtos.profile_dto import ProfileDraft
from keyboards.dating import choice_keyboard
from keyboards.menu import main_menu
from keyboards.profile import photo_upload_keyboard, registration_preview_keyboard
from services.interest_normalizer import format_interests
from services.localization import LocalizationService
from services.photo_analysis_progress import dismiss_photo_analysis_progress, show_photo_analysis_progress
from services.photo_moderation_service import PhotoModerationError, PhotoModerationService
from services.photo_upload_lock import PhotoUploadBusyError, photo_upload_lock
from services.profile_service import ProfileService
from states.registration import RegistrationState
from utils.document_links import documents_keyboard
from utils.legal import CONSENT_KEY
from utils.text import escape_html
from validators.profile_validator import ProfileValidationError

router = Router()
localizer = LocalizationService()

STEP_ORDER = [
    "gender",
    "target_gender",
    "name",
    "age",
    "district",
    "institution",
    "interests",
    "bio",
    "photo",
    "preview",
]
STATE_BY_STEP = {
    "gender": RegistrationState.gender,
    "target_gender": RegistrationState.target_gender,
    "name": RegistrationState.name,
    "age": RegistrationState.age,
    "district": RegistrationState.district,
    "institution": RegistrationState.institution,
    "interests": RegistrationState.interests,
    "bio": RegistrationState.bio,
    "photo": RegistrationState.photo,
    "preview": RegistrationState.preview,
}


def _language_code(message: Message | CallbackQuery | None) -> str:
    if message is None:
        return "ru"
    user = getattr(message, "from_user", None)
    code = getattr(user, "language_code", None)
    if not code:
        return "ru"
    return code.split("-")[0].lower() if "-" in code else code.lower()


async def _get_draft(state: FSMContext) -> dict[str, Any]:
    data = await state.get_data()
    draft = data.get("draft") or {}
    if "locale" not in draft:
        draft["locale"] = "ru"
    return draft


async def _set_draft(state: FSMContext, **updates: Any) -> None:
    draft = await _get_draft(state)
    draft.update(updates)
    await state.update_data(draft=draft)


async def _set_step(state: FSMContext, step: str) -> None:
    draft = await _get_draft(state)
    draft["step"] = step
    await state.update_data(draft=draft)
    await state.set_state(STATE_BY_STEP[step])


def _progress_bar(number: int, total: int) -> str:
    filled = "🟩" * number
    empty = "⬜" * (total - number)
    return f"{filled}{empty}"


def _step_prompt(step: str, locale: str) -> str:
    number = STEP_ORDER.index(step) + 1
    total = len(STEP_ORDER)
    bar = _progress_bar(number, total)
    return f"📝 Шаг {number}/{total}\n{bar}\n{localizer.get(f'registration_step_{step}', locale=locale)}"


async def _show_step(message: Message | CallbackQuery, state: FSMContext, step: str) -> None:
    target_msg = message.message if isinstance(message, CallbackQuery) else message
    if isinstance(message, CallbackQuery):
        try:
            await target_msg.edit_reply_markup(reply_markup=None)
        except TelegramBadRequest as exc:
            if "message is not modified" not in str(exc).lower():
                raise
    draft = await _get_draft(state)
    locale = draft.get("locale") or _language_code(target_msg)
    if step == "gender":
        await _set_step(state, "gender")
        await target_msg.answer(
            _step_prompt("gender", locale),
            reply_markup=choice_keyboard("reg_gender", [("Парень", "MALE"), ("Девушка", "FEMALE")]),
        )
    elif step == "target_gender":
        await _set_step(state, "target_gender")
        await target_msg.answer(
            _step_prompt("target_gender", locale),
            reply_markup=choice_keyboard(
                "reg_target", [("Парней", "MALE"), ("Девушек", "FEMALE"), ("Не важно", "ALL")]
            ),
        )
    elif step in {"name", "age", "district", "institution", "interests", "bio", "photo"}:
        await _set_step(state, step)
        await target_msg.answer(_step_prompt(step, locale))
    elif step == "preview":
        await _set_step(state, "preview")
        await _render_preview(message, state)


async def _render_preview(message: Message | CallbackQuery, state: FSMContext) -> None:
    target_msg = message.message if isinstance(message, CallbackQuery) else message
    draft = await _get_draft(state)
    locale = draft.get("locale") or _language_code(target_msg)
    photo_ids = list(draft.get("photo_file_ids") or [])
    caption = (
        f"<b>{escape_html(draft.get('name') or '—')}</b>, {draft.get('age') or '—'}\n"
        f"📍 <code>{escape_html(draft.get('district') or '—')}</code>\n"
        f"🏫 <i>{escape_html(draft.get('institution') or '—')}</i>\n"
        f"🎯 {escape_html(format_interests(draft.get('interests')))}\n\n"

        f"{escape_html(draft.get('bio') or '—')}"
    )
    header = _step_prompt("preview", locale)
    if photo_ids:
        if len(photo_ids) == 1:
            await target_msg.answer_photo(
                photo_ids[0], caption=f"{header}\n{caption}", reply_markup=registration_preview_keyboard()
            )
            return
        media = [
            InputMediaPhoto(media=photo_id, caption=f"{header}\n{caption}" if index == 0 else None)
            for index, photo_id in enumerate(photo_ids)
        ]
        await target_msg.answer_media_group(media)
        await target_msg.answer("📋 Предпросмотр анкеты", reply_markup=registration_preview_keyboard())
        return
    await target_msg.answer(header, reply_markup=registration_preview_keyboard())
    await target_msg.answer(caption)


async def start_registration(
    message: Message, state: FSMContext, *, edit: bool = False, initial_draft: dict[str, Any] | None = None
) -> None:
    consent = bool((await state.get_data()).get(CONSENT_KEY, False))
    if not consent and not edit:
        await message.answer(
            "⚠️ Для создания анкеты сначала ознакомьтесь с документами MeAnima.",
            reply_markup=documents_keyboard(
                "terms",
                "privacy",
                "community",
                "safety",
                "moderation",
                "alpha",
                include_continue=True,
            ),
        )
        return
    draft = initial_draft or await _get_draft(state)
    draft.setdefault("locale", _language_code(message))
    draft.setdefault("is_visible", True)
    draft.setdefault("photo_file_ids", [])
    draft.setdefault("extra_data", {})
    draft.setdefault("photo_replacement_started", False)
    draft["legal_consent"] = consent
    await state.clear()
    await state.update_data(draft=draft, legal_consent=consent)
    if edit:
        await state.update_data(edit_mode=True)
    else:
        await state.update_data(edit_mode=False)
    await _show_step(message, state, "gender")


@router.message(
    StateFilter(RegistrationState),
    F.text.in_(
        {
            "💘 Знакомства",
            "💕 Мои симпатии",
            "👤 Моя анкета",
            "🛡 Верификация",
            "💌 Признание",
            "🆘 Апелляция",
            "❓ Помощь",
        }
    ),
)
async def handle_menu_buttons_during_registration(
    message: Message, state: FSMContext, locale: str = "ru"
) -> None:
    await state.clear()
    await message.answer(LocalizationService().get("returned_to_menu", locale), reply_markup=main_menu(locale))


async def _go_to_previous_step(state: FSMContext) -> str:
    draft = await _get_draft(state)
    current = draft.get("step") or "gender"
    try:
        index = STEP_ORDER.index(current)
    except ValueError:
        return "gender"
    previous = STEP_ORDER[max(index - 1, 0)]
    return previous


async def _go_to_next_step(state: FSMContext) -> str:
    draft = await _get_draft(state)
    current = draft.get("step") or "gender"
    try:
        index = STEP_ORDER.index(current)
    except ValueError:
        return "preview"
    if index + 1 >= len(STEP_ORDER):
        return "preview"
    return STEP_ORDER[index + 1]


@router.callback_query(F.data == "profile:edit")
async def edit_profile(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await callback.answer()
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await start_registration(callback.message, state)
        return
    await start_registration(
        callback.message,
        state,
        edit=True,
        initial_draft={
            "gender": profile.gender.value,
            "target_gender": profile.target_gender.value,
            "name": profile.name,
            "age": profile.age,
            "district": profile.district,
            "institution": profile.institution,
            "interests": profile.interests,
            "bio": profile.bio,
            "photo_file_ids": list(profile.photo_file_ids or []),
            "main_photo_file_id": profile.main_photo_file_id,
            "locale": profile.locale,
            "is_visible": profile.is_visible,
            "extra_data": profile.extra_data or {},
        },
    )


@router.callback_query(RegistrationState.gender, F.data.startswith("reg_gender:"))
async def gender(callback: CallbackQuery, state: FSMContext) -> None:
    value = callback.data.split(":", 1)[1]
    await _set_draft(state, gender=value)
    await _show_step(callback, state, "target_gender")
    await callback.answer()


@router.callback_query(RegistrationState.target_gender, F.data.startswith("reg_target:"))
async def target(callback: CallbackQuery, state: FSMContext) -> None:
    value = callback.data.split(":", 1)[1]
    await _set_draft(state, target_gender=value)
    await _show_step(callback, state, "name")
    await callback.answer()


@router.message(RegistrationState.name)
async def name(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not 2 <= len(value) <= 32:
        await message.answer("⚠️ Имя должно содержать от 2 до 32 символов. Попробуйте ещё раз.")
        return
    await _set_draft(state, name=value)
    await _show_step(message, state, "age")


@router.message(RegistrationState.age)
async def age(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    try:
        value = int(text)
    except (TypeError, ValueError):
        await message.answer("⚠️ Укажите возраст числом от 16 до 99.")
        return
    if not 16 <= value <= 99:
        await message.answer("⚠️ Укажите возраст от 16 до 99 лет.")
        return
    await _set_draft(state, age=value)
    await _show_step(message, state, "district")


@router.message(RegistrationState.district)
async def district(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not value:
        await message.answer("⚠️ Укажите свой район.")
        return
    if len(value) > 64:
        await message.answer("⚠️ Район должен быть не длиннее 64 символов. Напишите ещё раз.")
        return
    await _set_draft(state, district=value)
    await _show_step(message, state, "institution")


@router.message(RegistrationState.institution)
async def institution(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not 3 <= len(value) <= 64:
        await message.answer("⚠️ Укажите место учебы или работы: 3–64 символа.")
        return
    await _set_draft(state, institution=value)
    await _show_step(message, state, "interests")


@router.message(RegistrationState.interests)
async def interests(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not value:
        await message.answer("⚠️ Напишите хотя бы одну интересную тему через запятую.")
        return
    await _set_draft(state, interests=value)
    await _show_step(message, state, "bio")


@router.message(RegistrationState.bio)
async def bio(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not 10 <= len(value) <= 500:
        await message.answer("⚠️ Напишите о себе 10–500 символов.")
        return
    await _set_draft(state, bio=value)
    await _show_step(message, state, "photo")


@router.message(RegistrationState.photo, F.photo)
async def photo(message: Message, state: FSMContext) -> None:
    try:
        async with photo_upload_lock(message.bot, message.from_user.id):
            draft = await _get_draft(state)
            photos = list(draft.get("photo_file_ids") or [])
            file_id = message.photo[-1].file_id
            replacing_photos = bool(
                draft.get("edit_mode")
                and draft.get("photo_file_ids")
                and not draft.get("photo_replacement_started")
            )
            if replacing_photos:
                photos = [file_id]
                await _set_draft(state, photo_replacement_started=True)
            elif file_id not in photos:
                photos.append(file_id)
            photos = photos[:3]
            await _set_draft(state, photo_file_ids=photos, main_photo_file_id=photos[0] if photos else None)
            if len(photos) < 3:
                await message.answer(
                    f"📸 Загружено {len(photos)}/3 фото. Можно добавить ещё или нажать «Готово».",
                    reply_markup=photo_upload_keyboard("registration:photos_done"),
                )
                return
            await _show_step(message, state, "preview")
    except PhotoUploadBusyError:
        await message.answer("⏳ Фото ещё обрабатываются. Попробуйте отправить фото ещё раз через секунду.")


@router.callback_query(RegistrationState.photo, F.data == "registration:photos_done")
async def photos_done(callback: CallbackQuery, state: FSMContext) -> None:
    draft = await _get_draft(state)
    if not draft.get("photo_file_ids"):
        await callback.answer("Загрузите хотя бы одну фотографию.", show_alert=True)
        return
    await _show_step(callback, state, "preview")
    await callback.answer()


@router.message(RegistrationState.photo)
async def non_photo(message: Message, state: FSMContext) -> None:
    await message.answer("⚠️ Отправьте фотографию, чтобы продолжить.")


@router.callback_query(RegistrationState.preview, F.data == "profile:rephoto")
async def preview_rephoto(callback: CallbackQuery, state: FSMContext) -> None:
    await _show_step(callback, state, "photo")
    await callback.answer()


@router.callback_query(RegistrationState.preview, F.data == "profile:publish")
async def publish(callback: CallbackQuery, state: FSMContext, session: AsyncSession, settings) -> None:
    draft = await _get_draft(state)
    locale = draft.get("locale") or "ru"
    payload = ProfileDraft(
        gender=draft.get("gender"),
        target_gender=draft.get("target_gender"),
        name=draft.get("name"),
        age=draft.get("age"),
        district=draft.get("district"),
        institution=draft.get("institution"),
        interests=draft.get("interests"),
        bio=draft.get("bio"),
        photo_file_ids=list(draft.get("photo_file_ids") or []),
        main_photo_file_id=draft.get("main_photo_file_id"),
        locale=draft.get("locale") or "ru",
        is_visible=bool(draft.get("is_visible", True)),
        extra_data=draft.get("extra_data") or {},
    )
    profile_service = ProfileService(session)
    try:
        await profile_service.create_or_update(callback.from_user.id, payload)
    except ProfileValidationError as exc:
        details = "\n".join(f"- {message}" for message in exc.errors.values())
        await callback.message.answer(f"Проверьте анкету:\n{details}")
        await callback.answer("Данные анкеты не прошли проверку", show_alert=True)
        return
    flagged_no_face = False
    flagged_nsfw = False
    photo_moderation = PhotoModerationService(
        session, nsfw_threshold=settings.nsfw_threshold, settings=settings, bot=callback.bot
    )
    progress = await show_photo_analysis_progress(callback.message)
    try:
        for photo_file_id in payload.photo_file_ids:
            assessment = await photo_moderation.inspect(callback.from_user.id, photo_file_id)
            flagged_no_face = flagged_no_face or not assessment.face_detected
            flagged_nsfw = flagged_nsfw or assessment.nsfw_score >= settings.nsfw_threshold
    except PhotoModerationError:
        await dismiss_photo_analysis_progress(progress)
        await state.clear()
        await callback.message.answer("⚠️ Не удалось проверить фото. Анкета скрыта и отправлена модераторам.")
        await callback.answer()
        return
    await dismiss_photo_analysis_progress(progress)
    await state.clear()
    if flagged_nsfw:
        await callback.message.answer(
            "⚠️ Фото отправлено на проверку модераторам. До решения анкета скрыта.\n"
            "Вы можете продолжить использование бота или заглянуть в «👤 Моя анкета».",
            reply_markup=main_menu(locale),
        )
    elif flagged_no_face:
        await callback.message.answer(
            "⚠️ На фото не найдено лицо. Замените фотографию в профиле; анкета отправлена на проверку.",
            reply_markup=main_menu(locale),
        )
    else:
        await callback.message.answer(
            "✅ Ваша анкета успешно опубликована!\n\n"
            "Теперь вы можете искать пару в разделе «💘 Знакомства» или настроить анкету в «👤 Моя анкета».",
            reply_markup=main_menu(locale),
        )
    await callback.answer()


@router.callback_query(RegistrationState.preview, F.data == "profile:edit")
async def preview_edit(callback: CallbackQuery, state: FSMContext) -> None:
    await _show_step(callback, state, "gender")
    await callback.answer()


@router.callback_query(RegistrationState.preview, F.data == "profile:back")
async def preview_back(callback: CallbackQuery, state: FSMContext) -> None:
    previous = await _go_to_previous_step(state)
    await _show_step(callback, state, previous)
    await callback.answer()


@router.callback_query(RegistrationState.preview, F.data == "profile:cancel")
async def preview_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    locale = (await _get_draft(state)).get("locale") or "ru"
    await state.clear()
    localizer = LocalizationService()
    msg = localizer.get("registration_cancelled", locale)
    await callback.message.answer(msg, reply_markup=main_menu(locale))
    await callback.answer()
````

## File: handlers/profile.py
````python
from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.registration import start_registration
from keyboards.menu import MENU_PROFILE_LABELS, main_menu
from keyboards.profile import failed_photo_keyboard, photo_management_keyboard, photo_upload_keyboard, profile_keyboard
from middlewares.i18n import normalize_locale
from models import ModerationStatus, User, UserStatus
from services.interest_normalizer import format_interests
from services.localization import LocalizationService
from services.photo_analysis_progress import dismiss_photo_analysis_progress, show_photo_analysis_progress
from services.photo_moderation_service import PhotoModerationError, PhotoModerationService
from services.photo_upload_lock import PhotoUploadBusyError, photo_upload_lock
from services.profile_service import ProfileService
from states.profile_photo import ProfilePhotoState
from utils.document_links import documents_keyboard
from utils.legal import CONSENT_KEY
from utils.profile_media import ordered_photo_ids, send_profile_gallery
from utils.text import escape_html

router = Router()
localizer = LocalizationService()


def _accepts_confessions(user: User | None) -> bool:
    return user.accepts_confessions if user else True


def _photo_management_text() -> str:
    return (
        "📸 Управление фотографиями.\n"
        "Главная фотография будет показываться первой. Меняйте порядок, заменяйте или удаляйте фото."
    )


def _confirm_keyboard(yes_text: str, yes_data: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=yes_text, callback_data=yes_data),
            InlineKeyboardButton(text="❌ Отмена", callback_data=f"{yes_data}_cancel"),
        ]
    ])
    return kb


async def _update_message_text(message: Message, text: str, reply_markup: InlineKeyboardMarkup | None = None) -> None:
    try:
        if message.photo:
            await message.edit_caption(caption=text, reply_markup=reply_markup)
        else:
            await message.edit_text(text, reply_markup=reply_markup)
    except TelegramBadRequest as exc:
        if "message is not modified" not in str(exc).lower():
            raise


async def _safe_edit_reply_markup(message: Message, reply_markup: InlineKeyboardMarkup) -> None:
    try:
        await message.edit_reply_markup(reply_markup=reply_markup)
    except TelegramBadRequest as exc:
        if "message is not modified" not in str(exc).lower():
            raise


def _profile_description(profile, locale: str = "ru") -> str:
    verification_key = "profile_verified" if profile.verification_status.value == "VERIFIED" else "profile_unverified"
    verification = LocalizationService().get(verification_key, locale)
    description = (
        f"{escape_html(profile.name)}, {profile.age}\n"
        f"📍 {escape_html(profile.district)}\n"
        f"🏫 {escape_html(profile.institution)}\n"
        f"🎯 {escape_html(format_interests(profile.interests))}\n\n"

        f"{escape_html(profile.bio)}\n\n"
        f"{verification}"
    )
    if profile.moderation_locked or profile.moderation_status.value == "UNDER_REVIEW":
        description += "\n" + LocalizationService().get("profile_moderation_hidden", locale)
    return description


async def _render_profile_message(
    message: Message, profile, *, accepts_confessions: bool = True, locale: str = "ru"
) -> None:
    hidden_by_moderation = (
        profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW
    )
    await _update_message_text(
        message,
        _profile_description(profile, locale),
        reply_markup=profile_keyboard(
            profile.is_visible and not hidden_by_moderation,
            hidden_by_moderation=hidden_by_moderation,
            accepts_confessions=accepts_confessions,
            locale=locale,
        ),
    )


async def show_profile(
    message: Message, user_id: int, session: AsyncSession, state: FSMContext, locale: str = "ru"
) -> None:
    """Show the same profile screen for reply and inline menu actions."""
    user = await session.get(User, user_id)
    if user is not None and user.status in {UserStatus.SUSPENDED, UserStatus.BANNED}:
        await message.answer(
            "⏸️ Ваша анкета временно ограничена или заблокирована. "
            "Нажмите «🆘 Апелляция», чтобы описать ситуацию и запросить пересмотр."
        )
        return
    service = ProfileService(session)
    p = await service.get_profile(user_id)
    if not p:
        if not (await state.get_data()).get(CONSENT_KEY, False):
            await message.answer(
                "⚠️ Для создания анкеты сначала ознакомьтесь с документами MeAnima.",
                reply_markup=documents_keyboard(
                    "terms",
                    "privacy",
                    "community",
                    "safety",
                    "moderation",
                    "alpha",
                    include_continue=True,
                ),
            )
            return
        await start_registration(message, state)
        return
    hidden_by_moderation = p.moderation_locked or p.moderation_status == ModerationStatus.UNDER_REVIEW
    await send_profile_gallery(
        message,
        p,
        _profile_description(p, locale),
        profile_keyboard(
            p.is_visible and not hidden_by_moderation,
            hidden_by_moderation=hidden_by_moderation,
            accepts_confessions=_accepts_confessions(user),
            locale=locale,
        ),
    )


@router.message(F.text.in_(MENU_PROFILE_LABELS))
async def profile(message: Message, session: AsyncSession, state: FSMContext, locale: str = "ru") -> None:
    await show_profile(message, message.from_user.id, session, state, locale)


@router.callback_query(F.data == "profile:language")
async def choose_language(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer(
        "🌐 Выберите язык / Alege limba:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="language:set:ru")],
            [InlineKeyboardButton(text="🇲🇩 Română", callback_data="language:set:ro")],
        ]),
    )


@router.callback_query(F.data.startswith("language:set:"))
async def set_language(callback: CallbackQuery, session: AsyncSession) -> None:
    locale = normalize_locale(callback.data.rsplit(":", 1)[-1])
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.answer(localizer.get("profile_not_found", locale), show_alert=True)
        return
    profile.locale = locale
    await session.flush()
    await callback.answer(localizer.get("language_saved", locale))
    await callback.message.answer(
        localizer.get("language_saved", locale),
        reply_markup=main_menu(locale),
    )


@router.callback_query(F.data == "promo:my_profile")
async def promo_my_profile(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext, locale: str = "ru"
) -> None:
    await callback.answer()
    if locale == "ru":
        await show_profile(callback.message, callback.from_user.id, session, state)
    else:
        await show_profile(callback.message, callback.from_user.id, session, state, locale)


@router.callback_query(F.data == "profile:blocked")
async def profile_blocked(callback: CallbackQuery) -> None:
    await callback.answer(
        "🚫 Анкета скрыта модерацией или находится на проверке. "
        "Перейдите в «🆘 Апелляция», если хотите запросить пересмотр.",
        show_alert=True,
    )


@router.callback_query(F.data == "profile:confessions_toggle")
async def toggle_confessions(callback: CallbackQuery, session: AsyncSession) -> None:
    user = await session.get(User, callback.from_user.id)
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if user is None or profile is None:
        await callback.answer("Сначала создайте анкету.", show_alert=True)
        return
    user.accepts_confessions = not user.accepts_confessions
    await session.flush()
    hidden_by_moderation = profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW
    await _safe_edit_reply_markup(
        callback.message,
        profile_keyboard(
            profile.is_visible and not hidden_by_moderation,
            hidden_by_moderation=hidden_by_moderation,
            accepts_confessions=user.accepts_confessions,
        ),
    )
    await callback.answer("Признания включены." if user.accepts_confessions else "Признания отключены.")


@router.callback_query(F.data == "profile:create")
async def create_profile(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    await callback.answer()
    if not (await state.get_data()).get(CONSENT_KEY, False):
        await callback.message.answer(
            "⚠️ Для создания анкеты сначала ознакомьтесь с документами MeAnima.",
            reply_markup=documents_keyboard(
                "terms",
                "privacy",
                "community",
                "safety",
                "moderation",
                "alpha",
                include_continue=True,
            ),
        )
        return
    await start_registration(callback.message, state)


@router.callback_query(F.data == "profile:photos")
async def manage_photos(callback: CallbackQuery, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.answer("Сначала создайте анкету.", show_alert=True)
        return
    photos = ordered_photo_ids(profile)
    await _update_message_text(
        callback.message,
        _photo_management_text(),
        reply_markup=photo_management_keyboard(len(photos)),
    )
    await callback.answer()


def _photo_at(profile, raw_index: str) -> str | None:
    try:
        return ordered_photo_ids(profile)[int(raw_index)]
    except (IndexError, ValueError):
        return None


@router.callback_query(F.data.startswith("photo:main:"))
async def set_main_photo(callback: CallbackQuery, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    photo_id = _photo_at(profile, (callback.data or "").rsplit(":", 1)[-1]) if profile else None
    if photo_id is None:
        await callback.answer("Фотография уже изменилась. Откройте управление снова.", show_alert=True)
        return
    await ProfileService(session).move_photo(
        callback.from_user.id, photo_id, -ordered_photo_ids(profile).index(photo_id)
    )
    updated = await ProfileService(session).get_profile(callback.from_user.id)
    await callback.answer("⭐ Главная фотография обновлена")
    await _safe_edit_reply_markup(callback.message, photo_management_keyboard(len(updated.photo_file_ids)))


@router.callback_query(F.data.startswith("photo:move:"))
async def move_photo(callback: CallbackQuery, session: AsyncSession) -> None:
    try:
        _, _, raw_index, raw_direction = (callback.data or "").split(":")
        direction = int(raw_direction)
    except ValueError:
        await callback.answer("Некорректная фотография.", show_alert=True)
        return
    if direction not in {-1, 1}:
        await callback.answer("Некорректное направление.", show_alert=True)
        return
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    photo_id = _photo_at(profile, raw_index) if profile else None
    if photo_id is None:
        await callback.answer("Фотография уже изменилась.", show_alert=True)
        return
    await ProfileService(session).move_photo(callback.from_user.id, photo_id, direction)
    updated = await ProfileService(session).get_profile(callback.from_user.id)
    await callback.answer("↔️ Порядок фотографий обновлён")
    await _safe_edit_reply_markup(callback.message, photo_management_keyboard(len(updated.photo_file_ids)))


@router.callback_query(F.data.startswith("photo:delete:"))
async def delete_photo(callback: CallbackQuery, session: AsyncSession) -> None:
    raw_index = (callback.data or "").rsplit(":" , 1)[-1]
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    photo_id = _photo_at(profile, raw_index) if profile else None
    if photo_id is None:
        await callback.answer("Фотография уже изменилась.", show_alert=True)
        return
    if len(ordered_photo_ids(profile)) == 1:
        await callback.answer("В анкете должна остаться хотя бы одна фотография.", show_alert=True)
        return
    await _update_message_text(
        callback.message,
        "🗑 Вы уверены, что хотите удалить эту фотографию?",
        reply_markup=_confirm_keyboard("Да, удалить", f"photo:delete_confirm:{raw_index}"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("photo:delete_confirm:"))
async def delete_photo_confirm(callback: CallbackQuery, session: AsyncSession) -> None:
    raw_index = (callback.data or "").split(":", 2)[-1]
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    photo_id = _photo_at(profile, raw_index) if profile else None
    if photo_id is None:
        await callback.answer("Фотография уже изменилась.", show_alert=True)
        return
    if len(ordered_photo_ids(profile)) == 1:
        await callback.answer("В анкете должна остаться хотя бы одна фотография.", show_alert=True)
        return
    await ProfileService(session).remove_photo(callback.from_user.id, photo_id)
    updated = await ProfileService(session).get_profile(callback.from_user.id)
    await callback.answer("Фотография удалена")
    await _update_message_text(
        callback.message,
        _photo_management_text(),
        reply_markup=photo_management_keyboard(len(updated.photo_file_ids)),
    )


@router.callback_query(F.data == "photo:add")
async def request_add_photo(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(photo_action="add", photo_index=None)
    await state.set_state(ProfilePhotoState.waiting_photo)
    await _update_message_text(callback.message, "📸 Отправьте новую фотографию.", reply_markup=None)
    await callback.answer()


@router.callback_query(F.data.startswith("photo:replace:"))
async def request_replace_photo(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        _, _, raw_index = (callback.data or "").split(":")
        int(raw_index)
    except ValueError:
        await callback.answer("Некорректная фотография.", show_alert=True)
        return
    await state.update_data(photo_action="replace", photo_index=raw_index)
    await state.set_state(ProfilePhotoState.waiting_photo)
    await _update_message_text(callback.message, "📸 Отправьте новую фотографию.", reply_markup=None)
    await callback.answer()


@router.message(ProfilePhotoState.waiting_photo, F.photo)
async def save_changed_photo(message: Message, state: FSMContext, session: AsyncSession, settings) -> None:
    try:
        async with photo_upload_lock(message.bot, message.from_user.id):
            data = await state.get_data()
            profile_service = ProfileService(session)
            profile = await profile_service.get_profile(message.from_user.id)
            if profile is None:
                await state.clear()
                return
            photo_id = message.photo[-1].file_id
            progress = await show_photo_analysis_progress(message)
            try:
                old_photo_id = None
                if data.get("photo_action") == "replace":
                    old_id = _photo_at(profile, str(data.get("photo_index")))
                    if old_id is None:
                        await dismiss_photo_analysis_progress(progress)
                        await message.answer("Список фото изменился. Откройте управление снова.")
                        await state.clear()
                        return
                    old_photo_id = old_id
                    await profile_service.replace_photo(message.from_user.id, old_id, photo_id)
                else:
                    await profile_service.add_photo(message.from_user.id, photo_id)
                assessment = await PhotoModerationService(
                    session, nsfw_threshold=settings.nsfw_threshold, settings=settings, bot=message.bot
                ).inspect(message.from_user.id, photo_id, defer_no_face_review=True)
            except ValueError as error:
                await dismiss_photo_analysis_progress(progress)
                await message.answer(str(error))
            except PhotoModerationError:
                await dismiss_photo_analysis_progress(progress)
                await message.answer("⚠️ Не удалось проверить фото. Анкета скрыта и отправлена модераторам.")
            else:
                await dismiss_photo_analysis_progress(progress)
                if assessment.nsfw_score >= settings.nsfw_threshold:
                    await state.clear()
                    await message.answer(
                        "⚠️ Фото не прошло автоматическую проверку и отправлено модераторам. "
                        "До решения анкета скрыта."
                    )
                    return
                if not assessment.face_detected:
                    if old_photo_id is None:
                        await profile_service.remove_photo(message.from_user.id, photo_id)
                    else:
                        await profile_service.replace_photo(message.from_user.id, photo_id, old_photo_id)
                    await state.update_data(
                        failed_photo_id=photo_id,
                        failed_photo_action=data.get("photo_action"),
                        failed_original_id=old_photo_id,
                    )
                    await state.set_state(ProfilePhotoState.awaiting_manual_review)
                    await message.answer(
                        "⚠️ На фото не удалось уверенно найти лицо. Анкета остаётся без изменений. "
                        "Замените фото или отправьте именно его на ручную проверку.",
                        reply_markup=failed_photo_keyboard(),
                    )
                    return
                updated_profile = await profile_service.get_profile(message.from_user.id)
                if data.get("photo_action") == "add" and updated_profile and len(updated_profile.photo_file_ids) < 3:
                    await message.answer(
                        f"✅ Фото сохранено. Загружено {len(updated_profile.photo_file_ids)}/3.",
                        reply_markup=photo_upload_keyboard("photo:done"),
                    )
                    return
                await message.answer(
                    "✅ Фотография сохранена.",
                    reply_markup=(
                        photo_management_keyboard(len(updated_profile.photo_file_ids)) if updated_profile else None
                    ),
                )
                await state.clear()
    except PhotoUploadBusyError:
        await message.answer("⏳ Фото ещё обрабатываются. Попробуйте отправить фото ещё раз через секунду.")


@router.callback_query(ProfilePhotoState.awaiting_manual_review, F.data == "photo:retry_failed")
async def retry_failed_photo(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ProfilePhotoState.waiting_photo)
    await callback.message.answer("📸 Отправьте другую фотографию.")
    await callback.answer()


@router.callback_query(ProfilePhotoState.awaiting_manual_review, F.data == "photo:review_failed")
async def review_failed_photo(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession, settings
) -> None:
    data = await state.get_data()
    photo_id = data.get("failed_photo_id")
    action = data.get("failed_photo_action")
    original_id = data.get("failed_original_id")
    profile_service = ProfileService(session)
    profile = await profile_service.get_profile(callback.from_user.id)
    if not photo_id or action not in {"add", "replace"} or profile is None:
        await state.clear()
        await callback.answer("Фото уже нельзя отправить на проверку. Загрузите его заново.", show_alert=True)
        return
    try:
        if action == "add":
            await profile_service.add_photo(callback.from_user.id, photo_id)
        elif not original_id:
            raise ValueError("Исходная фотография недоступна")
        else:
            await profile_service.replace_photo(callback.from_user.id, original_id, photo_id)
        assessment = await PhotoModerationService(
            session, nsfw_threshold=settings.nsfw_threshold, settings=settings, bot=callback.bot
        ).inspect(callback.from_user.id, photo_id)
    except PhotoModerationError:
        await state.clear()
        await callback.message.answer("⚠️ Фото отправлено модераторам. До решения анкета скрыта.")
        await callback.answer()
        return
    except ValueError:
        await state.clear()
        await callback.message.answer("⚠️ Не удалось отправить это фото. Загрузите его ещё раз.")
        await callback.answer()
        return
    await state.clear()
    if assessment.nsfw_score >= settings.nsfw_threshold or not assessment.face_detected:
        await callback.message.answer("⚠️ Фото отправлено модераторам. До решения анкета скрыта.")
    else:
        await callback.message.answer("✅ Повторная проверка прошла успешно. Фото сохранено.")
    await callback.answer()


@router.message(ProfilePhotoState.waiting_photo)
async def changed_photo_not_photo(message: Message) -> None:
    await message.answer("Нужно отправить фотографию.")


@router.callback_query(F.data == "photo:done")
async def finish_photo_management(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext, locale: str = "ru"
) -> None:
    await state.clear()
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.message.answer(
            LocalizationService().get("verification_home", locale), reply_markup=main_menu(locale)
        )
        await callback.answer()
        return
    user = await session.get(User, callback.from_user.id)
    hidden_by_moderation = profile.moderation_locked or profile.moderation_status == ModerationStatus.UNDER_REVIEW
    await _update_message_text(
        callback.message,
        _profile_description(profile, locale),
        reply_markup=profile_keyboard(
            profile.is_visible and not hidden_by_moderation,
            hidden_by_moderation=hidden_by_moderation,
            accepts_confessions=_accepts_confessions(user),
            locale=locale,
        ),
    )
    await callback.answer()


@router.callback_query(F.data == "profile:toggle")
async def toggle(callback: CallbackQuery, session: AsyncSession) -> None:
    service = ProfileService(session)
    p = await service.get_profile(callback.from_user.id)
    if not p:
        await callback.answer()
        return
    user = await session.get(User, callback.from_user.id)
    if (
        p.moderation_locked
        or p.moderation_status == ModerationStatus.UNDER_REVIEW
        or (user is not None and user.status in {UserStatus.SUSPENDED, UserStatus.BANNED})
    ):
        await callback.answer("Анкета скрыта модерацией. Подайте апелляцию или дождитесь решения.", show_alert=True)
        return
    if p.is_visible:
        await _update_message_text(
            callback.message,
            "🙈 Скрыть анкету? Она перестанет показываться другим пользователям до повторного включения.",
            reply_markup=_confirm_keyboard("Да, скрыть", "profile:toggle_confirm"),
        )
        await callback.answer()
        return
    p.is_visible = True
    await session.flush()
    await _safe_edit_reply_markup(
        callback.message,
        profile_keyboard(True, hidden_by_moderation=False, accepts_confessions=_accepts_confessions(user)),
    )
    await callback.answer("👀 Анкета снова видна")


@router.callback_query(F.data == "profile:toggle_confirm")
async def toggle_confirm(callback: CallbackQuery, session: AsyncSession) -> None:
    service = ProfileService(session)
    p = await service.get_profile(callback.from_user.id)
    if not p:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    user = await session.get(User, callback.from_user.id)
    if (
        p.moderation_locked
        or p.moderation_status == ModerationStatus.UNDER_REVIEW
        or (user is not None and user.status in {UserStatus.SUSPENDED, UserStatus.BANNED})
    ):
        await callback.answer("Анкета уже скрыта модерацией и не может быть опубликована.", show_alert=True)
        return
    p.is_visible = False
    await session.flush()
    await _update_message_text(
        callback.message,
        "🙈 Анкета скрыта. Нажмите «👀 Показать анкету», чтобы снова показать её.",
        reply_markup=profile_keyboard(
            False, hidden_by_moderation=False, accepts_confessions=_accepts_confessions(user)
        ),
    )
    await callback.answer("Анкета скрыта")


@router.callback_query(F.data == "profile:toggle_confirm_cancel")
async def toggle_confirm_cancel(callback: CallbackQuery, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    user = await session.get(User, callback.from_user.id)
    await _render_profile_message(
        callback.message, profile, accepts_confessions=_accepts_confessions(user), locale=profile.locale or "ru"
    )
    await callback.answer("Скрытие отменено")


@router.callback_query(F.data == "profile:pause")
async def pause(callback: CallbackQuery, session: AsyncSession) -> None:
    service = ProfileService(session)
    try:
        await service.pause(callback.from_user.id)
    except ValueError:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    user = await session.get(User, callback.from_user.id)
    await _safe_edit_reply_markup(
        callback.message,
        profile_keyboard(False, hidden_by_moderation=False, accepts_confessions=_accepts_confessions(user)),
    )
    await callback.answer("Анкета на паузе")


@router.callback_query(F.data == "profile:delete")
async def delete(callback: CallbackQuery, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    await _update_message_text(
        callback.message,
        "🗑 Вы уверены, что хотите удалить анкету? Это действие нельзя отменить.\n\n"
        "После удаления профиль и связанные данные будут удалены по правилам конфиденциальности.",
        reply_markup=_confirm_keyboard("Да, удалить", "profile:delete_confirm"),
    )
    await callback.answer()


@router.callback_query(F.data == "profile:delete_confirm")
async def delete_confirm(callback: CallbackQuery, session: AsyncSession) -> None:
    service = ProfileService(session)
    if not await service.delete(callback.from_user.id):
        await callback.answer("Анкета уже была удалена.", show_alert=True)
        return
    await _update_message_text(callback.message, "✅ Анкета удалена.")
    await callback.answer()


@router.callback_query(F.data == "profile:delete_confirm_cancel")
async def delete_confirm_cancel(callback: CallbackQuery, session: AsyncSession) -> None:
    profile = await ProfileService(session).get_profile(callback.from_user.id)
    if profile is None:
        await callback.answer("Анкета не найдена", show_alert=True)
        return
    user = await session.get(User, callback.from_user.id)
    await _render_profile_message(
        callback.message, profile, accepts_confessions=_accepts_confessions(user), locale=profile.locale or "ru"
    )
    await callback.answer("Удаление отменено")
````
