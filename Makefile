.PHONY: install dev test lint backend frontend

POETRY = POETRY_KEYRING_ENABLED=0 poetry

install:
	cd backend && $(POETRY) env use python3.12 && $(POETRY) install

dev:
	cd backend && $(POETRY) run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	cd backend && $(POETRY) run pytest

lint:
	cd backend && $(POETRY) run ruff check .

backend:
	docker compose up --build backend

up:
	docker compose --profile dev up --build

down:
	docker compose down
