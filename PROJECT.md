# FilmTracker

## ----------- Идея проекта 
Веб-приложение для поиска фильмов, их оценки и обсуждения.
Фильмы подгружаются из внешнего API (TMDB или OMDb, предпочтительно TMDB для бесплатного доступа с поиском, деталями и постерами),
пользовательский контент хранится локально. Проект охватывает все ключевые концепции из изученных книг: базовый Django (setup, apps, forms, auth, templates, permissions, deployment), APIs (REST, serializers, viewsets, routers, auth, docs), профессиональные практики (Docker, Postgres, env vars, email, uploads, search, performance, security) и TDD (unit/functional tests с mindset failing-green-refactor, Selenium для e2e).

## ----------- Основные сущности

### User
- Кастомная модель пользователя (CustomUser с AUTH_USER_MODEL)
- Регистрируется, авторизуется, меняет/сбрасывает пароль
- Может оценивать, комментировать фильмы, управлять профилем

### Film
- Глобальная сущность
- Создаётся при первом запросе через API
- Содержит общие данные (название, год, рейтинг TMDB, постер — ImageField для uploads/media)

### UserFilm
- Связь User ↔ Film (ManyToOne или ForeignKey)
- Хранит:
  - Оценку
  - Комментарий
  - Статус просмотра

## ----------- Основные пользовательские сценарии (MVP) 
- Пользователь регистрируется (advanced registration с email verification)
- Пользователь ищет фильм (с advanced search, e.g., по названию/году)
- Если фильма нет в локальной БД — добавляется через API, с защитой от дубликатов
- Пользователь ставит оценку и комментарий (forms с redirect/no resubmit, PRG pattern)
- На странице фильма видна средняя оценка сайта, количество просмотров (динамические агрегаты с performance optimizations: select_related/prefetch_related)
- Оцененный фильм появляется в профиле пользователя
- Админка для управления (custom admin с register, list_display, search_fields)
- Password change/reset через email
- API для всех операций (с docs и schemas)

## ----------- Архитектурные решения
- Используется кастомная модель пользователя (AUTH_USER_MODEL)
- Фильмы не принадлежат пользователю
- Пользовательские данные хранятся в UserFilm
- Агрегаты (средняя оценка, просмотры) считаются динамически (с SerializerMethodField в API)
- Web-интерфейс и REST API используют одну доменную модель
- Templates с blocks/extend для inheritance
- Bootstrap для UI
- Permissions: global (auth basics) и object-level (e.g., IsOwner для UserFilm)
- Security: SSL/headers, middleware (SecurityMiddleware, CSP)
- Performance: query optimizations для N+1 проблем
- Deployment: Docker + production config (static/media, env vars)

## ----------- Инженерные компоненты

### Backend 
- Django (full setup: apps как pages, accounts, films, reviews)
- Django ORM (models syntax с relations, ImageField/Media)
- Кастомная модель пользователя
- Django Rest Framework (ViewSets, Routers, APIView methods get/post, Permissions classes)

### API
- REST API для фильмов, оценок, пользователей (endpoints с serializers, SerializerMethodField)
- JWT / session-based аутентификация (разница Token vs Session)
- API используется:
  - Веб-интерфейсом
  - Потенциально внешними клиентами (e.g., optional React frontend)
- Schemas and documentation (drf-spectacular для OpenAPI)

### Внешние сервисы
- Внешний API фильмов (TMDB/OMDb)
- Данные кэшируются в локальной БД
- Email backend (e.g., console/file/SendGrid для password reset)

### База данных
- PostgreSQL (DATABASES config с env vars)

### Контейнеризация
- Docker (Dockerfile с ENV/CMD, multi-stage build)
- docker-compose (отдельные контейнеры: web, database — Postgres)

### Тестирование
- TDD mindset: failing test → minimal code → green → refactor
- Unit tests для моделей, views, serializers
- Functional tests для пользовательских сценариев (Selenium для e2e, как FT для user stories)
- Тесты API endpoints (expected crashes как часть цикла)

### Деплой 
- Запуск проекта в Docker
- Подготовка к production-конфигурации (static/uploads, security settings)
- Минимальный деплой на хостинг (e.g., Render/Heroku с Postgres)

### UI/Frontend
- Bootstrap integration (для forms, pages)
- Optional: Todo-like React frontend для API consumption

## ----------- Этапы реализации

### Этап 1. Базовый Django-проект (Initial setup, personal/company/blog-like websites)
- Кастомный User (AUTH_USER_MODEL) +
- Базовые модели (Film, UserFilm) +
- Админка (custom: register models, admin details как list_display, search_fields) + 
- Миграции +
- Apps: pages (home/about), accounts (user auth), films (Film model), reviews (UserFilm как comments/reviews)

### Этап 2. Доменные модели (Models syntax, relations)
- Film (с ImageField для постеров, media details)
- UserFilm (one-to-one/many-to-one checks, оценка/комментарий)
- Базовые запросы и связи (ForeignKey, aggregations)

### Этап 3. Внешний API (Integration, caching)
- Интеграция с TMDB/OMDb API (fetch data, headers in requests)
- Сохранение данных в БД (защита от дубликатов)
- Кэширование (e.g., simple cache for API calls)

### Этап 4. Web-интерфейс (Templates, forms, bootstrap, password change/reset)
- Поиск фильмов (search app с SearchVector или forms)
- Страница фильма (details, average rating)
- Профиль пользователя (list of UserFilms)
- Forms handling (redirect/no resubmit, PRG pattern)
- Templates с blocks/extend
- Bootstrap для стилей (CDN/integration)
- Password change and reset (built-in views/forms)
- Articles/comments-like: отзывы как comments app
- Permissions and authorization (groups, object-level)

### Этап 5. REST API (Web APIs, library/todo/blog API, permissions, viewsets/routers, schemas/docs)
- DRF setup
- Endpoints для фильмов/оценок/пользователей (APIView get/post, ViewSets преимущества)
- Аутентификация (Token vs Session, JWT)
- Serializers (ModelSerializer, SerializerMethodField)
- Routers (router.register)
- Permissions classes (code: IsAuthenticated, custom)
- Schemas and documentation (drf-spectacular)
- Optional: React frontend для API (как todo React)

### Этап 6. Тестирование (TDD with Python: full cycle)
- Unit tests для моделей/views/serializers (failing → green → refactor)
- Functional tests для сценариев (Selenium для user stories: e.g., registration → search → rate)
- Тесты API endpoints (REST principles, auth)
- Ожидаемые краши как часть цикла

### Этап 7. Docker и Professional setup (Docker, PostgreSQL, env vars, email, uploads, performance, security)
- Dockerfile (code: ENV/CMD, multi-stage)
- docker-compose (web, Postgres database)
- DATABASES env (environs для config)
- Static assets/prod (collectstatic)
- File/image uploads (Media для постеров)
- Email backend (setup для reset)
- Performance: queries (select/prefetch, N+1 fixes)
- Security settings (SSL/headers, middleware)

### Этап 8. Финализация (Deployment, refactoring)
- Минимальный деплой (e.g., на Render с Postgres, env vars)
- Документация (README, API docs)
- Рефакторинг (clean code, optimizations)

## Осознанно отложенные фичи
- Социальные взаимодействия между пользователями (лайки профилей, retweets-like)
- Рекомендации (на основе оценок)
- Сложная аналитика (stats beyond averages)
- Страница с последними оценками пользователей
- Полный React frontend (если не добавить в этап 5)