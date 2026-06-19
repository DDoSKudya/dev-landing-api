# Dev Landing API

Backend API для лендинг-презентации разработчика.

## Быстрый старт (локально)

Требуется **Python 3.12** (`python3.12` в PATH). Зависимости ставятся в `backend/.venv` через Poetry — не создавайте отдельный `venv/` в корне.

```bash
cp .env.example .env
make install
make dev
```

В Cursor/VS Code интерпретатор: `backend/.venv/bin/python` (см. `.vscode/settings.json`).

API: http://localhost:8000/api/health  
OpenAPI: http://localhost:8000/docs

## Docker

```bash
cp .env.example .env
docker compose up --build
```

- API через nginx: http://localhost/api/health
- Frontend: http://localhost

## Тесты

```bash
make test
```

Подробная документация будет дополнена на этапе 3.
