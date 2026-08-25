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
