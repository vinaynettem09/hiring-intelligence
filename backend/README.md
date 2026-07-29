# Backend — Hiring Intelligence (MVP)

FastAPI service. Module structure mirrors the frozen bounded contexts
(`app/modules/*`); platform interfaces live in `app/platform/*`; cross-cutting
helpers in `app/shared/*`. See `mvp/MVP-01` §5.

## Run
```bash
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

## Quality
```bash
uv run ruff check .   # lint
uv run ruff format .  # format
uv run mypy .         # types (strict)
uv run pytest         # tests
```

## Status
**Story 0.1** — tooling + a placeholder app factory only. Real wiring (config,
logging, middleware, DB, routers) arrives in Stories 0.3+. Do not add feature
code ahead of the backlog.
