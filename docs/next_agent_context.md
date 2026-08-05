# Next Agent Context

Документ отражает фактическое состояние после аудита matching и Trust System.

## Что реализовано

- Регистрация и редактирование профиля через FSM, DTO `ProfileDraft`, валидатор, нормализацию интересов, паузу и управление фото.
- Recommendation Engine строит совместимую выборку в SQL, ранжирует её стратегией и записывает показы. Лайк/пропуск/жалоба обновляют очередь; блокировка исключается в обоих направлениях.
- Like Engine и Match Engine используют уникальные пары и savepoint, поэтому создание лайка и матча идемпотентно.
- Trust System: Video Note verification, уникальные жалобы, автоматический Under Review, апелляции, Trust Score, аудит модераторов и очереди NSFW/лица. Высокий NSFW score скрывает анкету до решения.
- Redis используется для FSM и rate limit. `MemoryRecommendationQueue` является текущим single-process адаптером.

## Добавленные и расширенные таблицы

- `profiles`: профиль, `moderation_locked`, фото, locale/extra_data, `verification_status`, `moderation_status`, `report_count`.
- `likes`, `matches`, `dislikes`, `blocks`: направленные действия; Like/Match/Block защищены уникальными парами.
- `recommendation_views`: viewer/candidate/score, индексы `(viewer_id, created_at)` и `(candidate_id, created_at)`.
- `reports`, `appeals`, `admin_logs`: модерация и аудит; Report имеет уникальную пару reporter/target в миграции Trust.
- `verification_requests`, `moderation_cases`, `photo_moderations`, `trust_score_events`: расширяемые данные Trust.

Миграции: `20260805_matching_engine.py`, `20260805_trust_system.py`. Полного baseline для исторической схемы нет.

## Сервисы и репозитории

- Matching: `RecommendationService`, `RecommendationStrategy`, `WeightedRecommendationStrategy`, `RecommendationQueue`, `RecommendationRepository`.
- Social: `LikeService`/`LikeRepository`, `MatchService`/`MatchRepository`, `ProfileService`, `DiscoveryRepository`.
- Trust: `VerificationService`, `ReportService`, `ModerationService`, `PhotoModerationService`, `TrustScoreService`, `TrustStatsService`, `TrustRepository`.
- Cross-cutting: `NotificationService`, `LocalizationService`, `MatchingStatsService`, rate-limit middleware.

## Интерфейсы, которые нельзя менять без миграции потребителей

- `RecommendationStrategy.score(viewer, candidate)`, `RecommendationService.next_recommendation`, `rebuild_queue`, `skip`, `remove_candidate`.
- `RecommendationQueue.replace/pop/move_to_end/remove/clear`.
- `LikeService.create`, `MatchService.create_if_mutual`, `MatchService.matches_for`.
- `ProfileService.create_or_update` и `ProfileDraft.to_payload()`.
- `PhotoSafetyProvider.assess(photo_file_id)`.
- FSM/callback data: `like:*`, `comment:*`, `skip:*`, `block:*`, `report:*`, `verify:*`, `case:*`, `appeal:*`.

## Принятые решения

- Eligibility (visibility, active status, likes, двусторонние блоки) остаётся SQL-обязанностью; стратегия отвечает только за score. ML/AI не должен обходить этот фильтр.
- Веса matching меняются через `MATCHING_WEIGHTS_JSON`; неизвестные/отрицательные значения отклоняются, нулевые допустимы при положительной сумме.
- Внутренний Trust Score хранится вместе с неизменяемым журналом событий; действия модератора пишутся в `AdminLog`.
- NSFW/face — сменяемый provider-контракт, текущий dependency-free provider годится только для разработки.

## Потенциальные проблемы

- Memory queue не синхронизируется между процессами и теряется при рестарте.
- Нет baseline Alembic; `main.py` всё ещё применяет `create_all` и inline ALTER.
- `report_count` не обновляется атомарно при конкурирующих жалобах; требуется SQL `UPDATE ... RETURNING`.
- Событийные таблицы не имеют retention/партиционирования; статистика не имеет временных окон.
- Внешняя/batch ML-стратегия потребует отдельного batch API: текущий контракт вызывает score для каждого кандидата.
- UI локализован частично, уведомления не имеют outbox/retry очереди; NSFW/face provider необходимо заменить реальной локальной моделью до production.

## Критически важные места

- `repositories/recommendation.py` — safety/visibility SQL-фильтры.
- `services/recommendation.py` и `services/recommendation_strategy.py` — жизненный цикл очереди и расширяемое ранжирование.
- `services/like_service.py`, `services/match_service.py`, их репозитории — идемпотентность и приватность.
- `services/report_service.py`, `services/moderation_service.py`, `repositories/trust.py` — Trust policy и аудит.
- `main.py` и `database/migrations/` — порядок и безопасное обновление схемы.

## Следующий рекомендуемый модуль

Production hardening: Alembic baseline и удаление inline schema changes, Redis-backed recommendation queue, атомарный счётчик жалоб, реальный локальный NSFW/face provider, outbox для уведомлений, retention/observability и PostgreSQL/Redis integration + load tests.
