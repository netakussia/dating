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
- `RecommendationQueue.replace/pop/move_to_end/remove/clear`.
- `LikeService.create`, `MatchService.create_if_mutual`, `MatchService.matches_for`.
- `ProfileService.create_or_update` и `ProfileDraft.to_payload()`.
- `PhotoSafetyProvider.assess(photo_file_id)`.
- FSM/callback data: `like:*`, `comment:*`, `skip:*`, `block:*`, `report:*`, `verify:*`, `case:*`, `appeal:*`.

## Принятые решения

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
