# Contributing

Solo for now, but future-you counts. Keep it disciplined.

## Workflow
- Work the backlog in order: `mvp/MVP-02-engineering-backlog.md`.
- **One story = one branch = one PR = one review = one merge.**
- Branch naming: `e<epic>.<story>-<slug>` — e.g. `e0.2-docker-compose`.
- If a story grows beyond its scope, **split it** — don't cram extra work in.

## Before opening a PR
- `make lint` — Ruff + MyPy (backend), `next lint` (frontend). Must be clean.
- `make test` — must pass.
- You have **run it locally**. Never merge code you haven't run.
- The story's Definition of Done (in MVP-02) is met.

## Module layout (convention)
Every business module under `app/modules/<name>/` uses the same file set — even if
some are empty until their story lands. Consistency > perfection.
```
models.py       SQLAlchemy models (tiny — only fields a story needs)
repository.py   persistence; domain-language methods; NEVER owns/commits a session
service.py      application/use-case logic
schemas.py      Pydantic request/response DTOs
api.py          FastAPI routes (thin; call service)
```

## Database invariants (non-negotiable)
> **Session invariant:** A request owns **exactly one** SQLAlchemy session.
> Repositories **never create, commit, or close** sessions.
>
> **Transaction invariant:** Repositories **persist** (`add`/`flush`); **services
> decide transaction boundaries**; the request **commits once** (in `get_session`).

- Engine is created **once** in the app factory; never global, never inside a repository.
- Repositories speak the **domain** ("create organization"), not CRUD. No generic
  `BaseRepository<T>` — just tiny shared tenant-aware helpers.

> **Tenant-isolation invariant (Epic 2+):** Every query returning tenant-owned data
> MUST go through `TenantScopedRepository`. A raw `session.execute(select(SomeTenantModel))`
> outside it is a **review rejection** — isolation is too important to rely on
> developer discipline. Tenant id comes from the verified token (envelope), never the request body.

## Testing layout
- `tests/unit/` — fast, no external services (in-memory SQLite for repos). Primary suite.
- `tests/integration/` — real Postgres via Testcontainers (arrives with CI, Story 0.8).
- Shared fixtures live in `tests/conftest.py`.

## Guardrails
- Don't implement future stories or infrastructure early.
- Keep the frozen architecture (`arch/`) as the North Star; don't redesign it.
- No secrets in the repo (gitleaks will block you).
- Record non-obvious implementation choices in `docs/decisions/` (see its README).
- Log product lessons in `LEARNINGS.md`.
