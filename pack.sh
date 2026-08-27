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