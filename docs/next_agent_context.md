# Next Agent Context

Документ отражает фактическое состояние проекта после регистрации, профиля и matching-модуля.

## 1. Что реализовано

### Registration/Profile

- FSM-регистрация: пол, целевой пол, имя, возраст, район, учреждение, интересы, bio, фото и preview.
- `ProfileService`, `ProfileDraft`, `ProfileValidationError`, нормализация интересов и базовая JSON-локализация.
- Пауза, возобновление, удаление, редактирование и управление фотографиями.

### Recommendation Engine

- `RecommendationService` строит очередь совместимых профилей и сортирует их по Score 0–100.
- `RecommendationStrategy` — асинхронный контракт стратегии оценки.
- `WeightedRecommendationStrategy` — текущая детерминированная реализация.
- Веса задаются через `MATCHING_WEIGHTS_JSON`; текущие значения: gender 35, target_gender 25, age 10, district 10, institution 10, interests 7, bio 3.
- `RecommendationQueue` — сменяемый контракт очереди; `MemoryRecommendationQueue` — текущий адаптер.
- После показа выполняется повторная DB-проверка активности, видимости, лайка и блока, чтобы устаревшая очередь не отдала невалидную анкету.
- Пропуск переносит профиль в конец очереди; лайк/блок/жалоба удаляют его из текущей очереди. При исчерпании очередь пересчитывается.
- Пользователь видит только итоговый процент совместимости.

### Likes/Matches

- `LikeService` создаёт однонаправленный Like, валидирует сообщение, запрещает self-like и повторные операции.
- `MatchService` проверяет reciprocal Like, выставляет `is_mutual` и создаёт нормализованный Match один раз.
- Уведомления о новом Like анонимны; контакты раскрываются только при новом Match.
- Вкладка «💕 Мои симпатии» читает Match через `MatchService`.

### Diagnostics/Statistics

- `RecommendationView` сохраняет viewer, candidate и Score.
- `MatchingStatsService` агрегирует пользователей, активные профили, просмотры, лайки, матчи, жалобы, CTR и среднюю совместимость.
- Админская команда `/debug_matching` показывает агрегаты и причины исключения кандидатов.

## 2. Добавленные или расширенные таблицы

- `profiles`: `moderation_locked`, `photo_file_ids`, `main_photo_file_id`, `locale`, `extra_data`.
- `likes`: уникальная направленная пара и комментарий.
- `matches`: уникальная нормализованная пара пользователей.
- `dislikes`: аналитическая запись пропуска; больше не означает вечное исключение из выдачи.
- `recommendation_views`: UUID, `viewer_id`, `candidate_id`, `score`, timestamps; индексы `(viewer_id, created_at)` и `(candidate_id, created_at)`.

Для `recommendation_views` добавлена `database/migrations/versions/20260805_matching_engine.py`. Полного baseline Alembic для старых таблиц ещё нет.

## 3. Сервисы и репозитории

- `RecommendationService`, `WeightedRecommendationStrategy`, `RecommendationQueue`.
- `LikeService`, `MatchService`, `MatchingStatsService`, `MatchingDebugService`.
- `RecommendationRepository`, `LikeRepository`, `MatchRepository`, `MatchingStatsRepository`.
- `ProfileService`, `ConfessionService`, `NotificationService`, `LocalizationService`, `InterestNormalizer` существовали ранее и остаются действующими контрактами.

## 4. Интерфейсы, которые нельзя менять без миграции потребителей

- `RecommendationStrategy.score(viewer, candidate)`.
- `RecommendationService.next_recommendation`, `next_profile`, `rebuild_queue`, `skip`, `remove_candidate`.
- `RecommendationQueue.replace/pop/move_to_end/remove/clear`.
- `LikeService.create` и `LikeResult.created`.
- `MatchService.create_if_mutual`, `matches_for` и `MatchResult.created`.
- `ProfileService` и `ProfileDraft.to_payload()`.
- FSM registration/dating states и callback data `like:*`, `comment:*`, `skip:*`, `block:*`, `report:*`.
- Поля `Profile.gender`, `target_gender`, `photo_file_ids`, `main_photo_file_id`, `locale`, `extra_data`.

Новые стратегии должны подключаться через `strategy=` и не должны добавлять условные ветки в handlers.

## 5. Принятые решения

- Фильтры eligibility находятся в repository/SQL, а ранжирование — в strategy. Так ML/AI не сможет случайно обойти требования безопасности и модерации.
- Score нормализуется в 0–100 и округляется до одной десятичной доли; UI показывает целый процент.
- Memory queue выбрана как минимальный адаптер без жёсткой зависимости от Redis. Источником истины остаётся PostgreSQL.
- Like и Match защищены DB unique constraints, предварительным поиском и savepoint-операциями для конкурирующих запросов.
- Пропуск не является вечным blacklist: он перемещается в конец текущей временной очереди.
- Просмотры записываются отдельной таблицей, потому что без них нельзя корректно считать CTR и среднюю совместимость.

## 6. Потенциальные проблемы

- Memory queue не синхронизируется между несколькими процессами и теряется при рестарте; для production нужен Redis-адаптер с атомарными операциями.
- Нет полноценного Alembic baseline; `main.py` всё ещё использует `create_all` и inline SQL для совместимости.
- События просмотров пока не имеют retention/партиционирования и могут расти бесконечно.
- Статистика агрегируется за всю историю, без временных окон и сегментации.
- Локализация покрывает не весь UI; часть строк находится в handlers.
- `NSFWService` остаётся заглушкой.
- Нет отдельной domain-event/observability модели и полноценной retry-политики уведомлений.
- Конкурентный `report_count` и уникальность повторных жалоб требуют отдельного production migration с уникальным ограничением `(reporter_id, target_user_id)`.

## 7. Критически важные места

- `services/recommendation_strategy.py`: контракт расширения алгоритмов и веса.
- `services/recommendation.py`: orchestration, queue lifecycle и повторная eligibility-проверка.
- `repositories/recommendation.py`: SQL-фильтры видимости, статуса, лайков и блоков.
- `services/like_service.py`, `services/match_service.py`: privacy, idempotency и порядок уведомлений.
- `models/like.py`, `models/match.py`, `models/recommendation_view.py`: ограничения целостности и аналитическая схема.
- `handlers/dating.py`: callback-контракты и пользовательский сценарий.
- `config.py`: внешняя конфигурация весов и порога жалоб.
- `main.py` и миграции: порядок инициализации схемы.

## 8. Рекомендуемый следующий модуль

Следующий приоритет — production hardening: baseline Alembic, Redis queue, временные окна статистики, observability и integration-тесты с PostgreSQL/Redis. После этого можно добавить `PopularityRecommendationStrategy`, `ActivityRecommendationStrategy`, а затем `HybridRecommendationStrategy` или ML-адаптер. Верификацию фото и реальный NSFW-провайдер следует реализовать до публичного запуска.

## 9. Обязательная проверка перед изменениями

Прочитать `PROJECT_RULES.md`, `ROADMAP.md`, `docs/architecture.md`, `docs/database.md`, `docs/matching.md`, `handlers/dating.py`, `services/recommendation.py`, `services/recommendation_strategy.py`, `repositories/recommendation.py`, `models/profile.py`, `models/like.py`, `models/match.py` и `main.py`.
