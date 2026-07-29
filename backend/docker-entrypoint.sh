#!/bin/sh
# Container entrypoint (Story 9.1). Applies pending Alembic migrations to `DATABASE_URL`,
# then hands off to the given command (uvicorn). `alembic upgrade head` is idempotent and
# additive — it NEVER drops/recreates data. If it fails, `set -e` aborts before the app
# starts, so a bad migration fails the deploy visibly instead of booting a half-migrated app.
set -e

echo "[entrypoint] applying database migrations (alembic upgrade head)..."
uv run alembic upgrade head
echo "[entrypoint] migrations applied; starting: $*"

exec "$@"
