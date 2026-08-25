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
