# Backend image (Story 0.2). Dev-oriented: compose mounts source + runs --reload.
# Production hardening (distroless, non-root, multi-stage slimming) is Story 10.
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

# App code (overlaid by a volume mount in docker-compose for hot reload).
COPY app ./app

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
