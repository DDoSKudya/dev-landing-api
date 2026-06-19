.PHONY: help up down test dev lint typecheck pre-commit

.DEFAULT_GOAL := help

POETRY = POETRY_KEYRING_ENABLED=0 poetry

help:
	@echo "Доступные команды:"
	@echo ""
	@echo "  make up    — полное поднятие в Docker (backend, frontend, nginx, MailHog)"
	@echo "  make down  — полная остановка Docker-стека"
	@echo "  make dev   — локальная разработка: зависимости, миграции, backend + frontend"
	@echo "  make test  — тесты backend (pytest) и frontend (vitest)"
	@echo "  make lint  — ruff (backend) + eslint (frontend)"
	@echo "  make typecheck — mypy в backend"
	@echo "  make pre-commit — pre-commit run --all-files"
	@echo ""
	@echo "Перед первым запуском: cp .env.example .env"

up:
	docker compose up --build

down:
	docker compose down --remove-orphans

test:
	cd backend && $(POETRY) env use python3.12 && $(POETRY) install && $(POETRY) run pytest
	cd frontend && npm install && npm run test

lint:
	cd backend && $(POETRY) run ruff check .
	cd backend && $(POETRY) run ruff format --check .
	cd frontend && npm run lint

typecheck:
	cd backend && $(POETRY) run mypy app tests

pre-commit:
	pre-commit run --all-files

dev:
	cd backend && $(POETRY) env use python3.12 && $(POETRY) install
	cd frontend && npm install
	cd backend && $(POETRY) run alembic upgrade head
	@trap 'kill 0' EXIT INT TERM; \
	(cd backend && $(POETRY) run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000) & \
	(cd frontend && npm run dev) & \
	wait
