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

## Ключевые правила
- Profiles связаны с пользователями через unique constraint по user_id.
- Likes и dislikes имеют уникальные пары (from_user_id, to_user_id).
- Matches хранят пару пользователей без дублирования.
- Recommendation views хранят viewer, candidate и Score; индексы покрывают viewer/candidate вместе с created_at.
- Reports и appeals связаны с пользователями и могут быть обработаны администратором.
- Confessions хранят sender_hash для защиты от спама.

## Текущая схема запуска
- PostgreSQL запускается в контейнере.
- Таблицы создаются автоматически при старте через Base.metadata.create_all.
- Для совместимости со старыми инсталляциями в [main.py](main.py) применяются минимальные `ALTER TABLE`/`ALTER TYPE`-расширения схемы.
- Для продакшна обязательно перейти на Alembic-миграции как на основной путь обновления схемы.

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
- `blocks` имеет уникальную пару `(blocker_id, blocked_id)`; блокировка персональная и не скрывает автора блока от другого пользователя автоматически.
- `profiles.user_id`, `profiles.is_visible`, `users.status`, `likes.from_user_id`, `blocks.blocker_id` используются в фильтрах выдачи.
- `recommendation_views` индексирована по `(viewer_id, created_at)` и `(candidate_id, created_at)` для аналитики и будущего retention.

## Миграция matching

Добавлена `database/migrations/versions/20260805_matching_engine.py` для `recommendation_views`. Исторического baseline для ранее созданных таблиц пока нет; перед production необходимо зафиксировать baseline и перевести запуск схемы с `create_all`/inline SQL на Alembic upgrade.
