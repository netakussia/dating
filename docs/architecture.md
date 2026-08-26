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
