# Hiring Intelligence — developer commands.
# First run:  make install   then   make dev
.DEFAULT_GOAL := help
COMPOSE = docker compose -f infra/docker-compose.yml
.PHONY: help install dev dev-backend dev-frontend test test-int lint check check-int fmt precommit clean up down logs migrate seed

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## Install backend + frontend deps and pre-commit hooks
	cd backend && uv sync
	cd frontend && pnpm install
	uv run --project backend pre-commit install || true

dev: ## Run backend + frontend together (Ctrl-C stops both)
	@$(MAKE) -j2 dev-backend dev-frontend

dev-backend: ## Run the FastAPI backend (http://localhost:8000)
	cd backend && uv run uvicorn app.main:create_app --factory --reload --port 8000

dev-frontend: ## Run the Next.js frontend (http://localhost:3000)
	cd frontend && pnpm dev

test: ## Run fast unit tests
	cd backend && uv run pytest tests/unit

test-int: ## Run integration tests (needs Postgres: make up + make migrate)
	cd backend && uv run pytest tests/integration -m integration

lint: ## Lint + type-check backend, lint frontend
	cd backend && uv run ruff check . && uv run mypy .
	cd frontend && pnpm lint

check: ## Full merge gate (mirrors CI: backend-quality + frontend-quality)
	cd backend && uv run ruff format --check . && uv run ruff check . && uv run mypy . && uv run pytest tests/unit --cov=app --cov-report=term-missing --cov-fail-under=80
	cd frontend && pnpm check   # single source of truth: typecheck -> lint -> Vitest -> build

check-int: ## Postgres gate (mirrors CI postgres-integration): migrate -> single-head -> tests
	cd backend && uv run alembic upgrade head
	cd backend && test "$$(uv run alembic heads | grep -c '(head)')" -eq 1 || (echo "Expected exactly one Alembic head" && exit 1)
	cd backend && uv run pytest tests/integration -m integration

fmt: ## Auto-format backend
	cd backend && uv run ruff format . && uv run ruff check --fix .

precommit: ## Install pre-commit hooks
	cd backend && uv run pre-commit install

clean: ## Remove caches + build artifacts
	find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/.pytest_cache backend/.mypy_cache backend/.ruff_cache backend/dist backend/build
	rm -rf frontend/.next

# --- Docker Compose stack (Story 0.2): db + mailhog + backend ---
up: ## Start the local stack (db + mailhog + backend) in Docker
	$(COMPOSE) up --build

down: ## Stop the local stack
	$(COMPOSE) down

logs: ## Tail the stack logs
	$(COMPOSE) logs -f

migrate: ## Run DB migrations (Alembic) — needs Postgres up (make up)
	cd backend && uv run alembic upgrade head

# --- Placeholder wired up by a later story ---
seed: ## (Story 0.4+) Seed synthetic dev data
	@echo "make seed arrives with signup/campaign data (Epic 1+)."
