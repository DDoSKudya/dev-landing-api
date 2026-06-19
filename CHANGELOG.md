# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-06-19

First production-ready release of Dev Landing API: developer landing page with contact form, AI analysis, email notifications, and metrics.

### Added

#### Platform and infrastructure

- Monorepo: FastAPI backend and Vue 3 frontend
- `docker-compose.yml`: backend, frontend build, nginx, MailHog
- Makefile targets: `help`, `up`, `down`, `dev`, `test`
- nginx reverse proxy: `/` → frontend, `/api/` → backend (host port **8080** by default)
- `.env.example` with grouped variables (OpenAI, SMTP, rate limit, CORS)
- Postman collection: `postman/dev-landing-api.json`
- Structured logging: `logs/requests.log`, `logs/app.log`

#### Backend

- FastAPI app with layered architecture: `router → service → repository`
- `POST /api/contact` — contact form with Pydantic validation
- `GET /api/metrics?days=N` — submission statistics for the last N days
- `GET /api/health` — status, version, database ping
- SQLite via SQLAlchemy 2 (async), Alembic migrations
- OpenAI integration: sentiment, category, draft reply (`analyze_comment`)
- AI fallback when key is missing or API fails (`ai_status: unavailable`)
- SMTP email to owner and auto-reply to user (Jinja2 HTML templates)
- IP rate limiting via JSON file (`data/rate_limit.json`)
- Unified API error responses: validation (422), rate limit (429), email delivery (502)
- DB session via `ContextVar` + middleware

#### Frontend

- Vue 3 SPA: Hero, About, Portfolio, Experience, Contact sections
- Profile data in `frontend/src/data/profile.js`
- Portfolio tabs: work projects and pet projects
- `ContactForm` with field-level validation errors and rate-limit hints
- Theme switcher: dark/light mode and accent colors (cyan, violet, emerald) with `localStorage` persistence
- Tailwind CSS 4, glass-style UI, mesh background
- API client with handling for 422, 429, 502 and non-JSON errors

#### Tests

- **Backend:** pytest with equivalence-class coverage (validation boundaries, submit flows, rate limit, metrics, health)
- **Frontend:** Vitest + Vue Test Utils (`client`, `ContactForm`, `PortfolioSection`, `ThemeSwitcher`, `validationErrors`)
- `make test` runs backend and frontend test suites

### Changed

- Project version set to `1.0.0` across backend (`pyproject.toml`, `/api/health`) and frontend (`package.json`)
- Backend tests reorganized by equivalence classes instead of a single monolithic contact test file
- `mapValidationErrors` extracted to `frontend/src/utils/validationErrors.js` for reuse and unit tests

## [0.1.0] - 2026-06-18

Initial repository scaffold.

### Added

- Project layout, `.env.example`, `.gitignore`
- Basic FastAPI skeleton and README
