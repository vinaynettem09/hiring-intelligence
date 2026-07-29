# Backend image (Story 0.2; deployable in Story 9.1).
# Further production hardening (distroless, non-root, multi-stage slimming) is Story 10.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# uv (fast, reproducible installs from uv.lock)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Dependency layer (cached until pyproject/lock change).
# uv.lock must be committed (created by `make install`).
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Migrations + app. The migration files and alembic.ini MUST be in the image so the
# entrypoint can run `alembic upgrade head` on startup (Story 9.1). App code is overlaid
# by a volume mount in docker-compose for local hot reload.
COPY alembic.ini ./
COPY migrations ./migrations
COPY app ./app
COPY docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

EXPOSE 8000
# Entrypoint applies migrations, then runs the CMD. CMD binds to $PORT (Render sets it;
# defaults to 8000 for local/compose) via a shell so the variable expands.
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["sh", "-c", "uv run uvicorn app.main:create_app --factory --host 0.0.0.0 --port ${PORT:-8000}"]
