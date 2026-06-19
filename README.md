# Dev Landing API

Backend-сервис для лендинг-презентации разработчика: форма обратной связи, AI-анализ, email, rate limiting, метрики.

## 1. Как запустить проект

### Требования

- Python 3.12
- Poetry
- Docker (опционально)

### Локальный запуск

```bash
cp .env.example .env
make install
make migrate
make dev
```

- API: http://localhost:8000/api/health
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Виртуальное окружение: `backend/.venv`

### Docker

```bash
cp .env.example .env
make up
```

- API через nginx: http://localhost/api/health
- MailHog (письма): http://localhost:8025
- Frontend (заглушка): http://localhost

### Переменные окружения

Скопируйте `.env.example` в `.env`. Основные переменные:

| Переменная | Назначение |
|------------|------------|
| `OPENAI_API_KEY` | Ключ OpenAI (пустой = AI fallback) |
| `SMTP_HOST`, `SMTP_PORT` | SMTP (`localhost:1025` локально, `mailhog` в Docker) |
| `EMAIL_FROM`, `EMAIL_OWNER` | Адреса отправителя и владельца |
| `RATE_LIMIT_REQUESTS`, `RATE_LIMIT_WINDOW_SEC` | Лимит запросов с одного IP |
| `CORS_ORIGINS` | Разрешённые origins для фронтенда |

### Тесты

```bash
make test
make lint
```

### Деплой

Публичный URL будет добавлен на этапе 4. Пока — локальный запуск или туннель:

```bash
make dev
# в другом терминале:
ngrok http 8000
```

## 2. Стек технологий

| Слой | Технология |
|------|------------|
| Backend | Python 3.12, FastAPI, Uvicorn |
| Зависимости | Poetry |
| Валидация | Pydantic, email-validator |
| БД | SQLite, SQLAlchemy 2 (async), Alembic |
| AI | OpenAI API (`openai`) |
| Email | aiosmtplib, Jinja2 (HTML-шаблоны писем) |
| Rate limit | JSON-файл + `fcntl` |
| Логирование | stdlib `logging` |
| Тесты | pytest, httpx |
| Линтер | Ruff |
| Frontend | Vue 3, Vite, Tailwind (этап 4 — в работе) |
| Инфра | Docker Compose, nginx, MailHog |

**Почему так:** монолит с чёткими слоями — проще сопровождать для pet-проекта; SQLite без отдельного сервера; stdlib logging вместо structlog (KISS).

## 3. Архитектура

Слоистая структура (Controllers → Services → Repositories):

```
router → service → repository
```

Модули:

| Модуль | Назначение |
|--------|------------|
| `contact/` | Форма: валидация, AI, email, сохранение |
| `metrics/` | Статистика обращений (читает БД, не зависит от `contact.service`) |
| `health/` | Проверка сервиса и БД |
| `core/` | config, сессия БД, логи, ошибки, rate limit |

Сессия БД: `ContextVar` + `DbSessionMiddleware` — репозитории вызывают `get_session()` без протаскивания сессии через все функции.

Полный цикл `POST /api/contact`:

```
rate limit → валидация → AI (fallback) → SQLite → email → ответ 201
```

## 4. Реализация API

Базовый URL: `http://localhost:8000/api` (или `http://localhost/api` через nginx).

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/health` | Статус сервиса + ping БД |
| POST | `/contact` | Форма обратной связи |
| GET | `/metrics?days=30` | Статистика за N дней |

### POST `/contact`

**Запрос:**

```bash
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Иван Петров",
    "phone": "+79991234567",
    "email": "ivan@example.com",
    "comment": "Интересует сотрудничество на FastAPI."
  }'
```

**Ответ 201:**

```json
{
  "id": "uuid",
  "message": "Thank you! Your message was received.",
  "ai_status": "ok",
  "sentiment": "positive",
  "request_category": "collaboration",
  "created_at": "2026-06-19T12:00:00Z"
}
```

**Валидация:** имя (2–100), телефон (regex), email, комментарий (10–5000), `strip` пробелов.

**Ошибки:**

| Код | Ситуация |
|-----|----------|
| 422 | Ошибка валидации |
| 429 | Rate limit (`Retry-After`) |
| 502 | Ошибка SMTP (заявка уже в БД) |
| 500 | Неожиданная ошибка |

### GET `/health`

```bash
curl http://localhost:8000/api/health
```

### GET `/metrics`

```bash
curl "http://localhost:8000/api/metrics?days=30"
```

```json
{
  "total": 10,
  "by_category": {"collaboration": 3},
  "by_sentiment": {"positive": 5},
  "ai_unavailable_count": 1
}
```

Postman: `postman/dev-landing-api.json`

## 5. AI-интеграция

- **Провайдер:** OpenAI (`OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_TIMEOUT_SEC`)
- **Файл:** `backend/app/contact/ai.py` → `analyze_comment()`
- **Функции:** анализ тональности, классификация типа запроса, черновик ответа
- **Промпт (system):** JSON с полями `sentiment`, `request_category`, `draft_reply`; без обещаний сроков в ответе

**Fallback:** нет ключа или ошибка API → `ai_status: "unavailable"`, сервис возвращает **201**, форма и email работают.

`draft_reply` сохраняется в БД и уходит в письме владельцу, клиенту не отдаётся.

## 6. Что сделано с помощью AI

| Область | С помощью AI | Ручная доработка |
|---------|--------------|------------------|
| План проекта | Структура, этапы, стек | Сокращение scope, YAGNI |
| Backend-каркас | FastAPI, Docker, тесты | Паттерн сессии, 502 + commit |
| Contact flow | Разбиение на слои | Rate limit с блокировкой файла |
| Документация | Черновик README, Postman | Проверка по ТЗ, curl-примеры |

Промпты ориентировали на: модульный монолит, Poetry, простой код без лишних абстракций. Весь код проверен и упрощён вручную.

## 7. Хранение данных

| Хранилище | Путь | Назначение |
|-----------|------|------------|
| SQLite | `data/app.db` | Таблица `contact_submissions` |
| Rate limit | `data/rate_limit.json` | Счётчики запросов по IP |
| Access log | `logs/requests.log` | method, path, status, duration |
| App log | `logs/app.log` | События приложения |
| Статистика | SQLite | Агрегация через `GET /api/metrics` |

Миграции: `backend/alembic/versions/`
