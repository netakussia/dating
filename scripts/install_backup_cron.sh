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
