# CI & Local Quality Gates (Story 8.1)

Every change gets one reproducible answer: **is this repository safe to merge?**

CI and developers run the *same* underlying commands — the canonical definitions live in
package scripts and the `Makefile`, never duplicated inside workflow YAML.

## What CI runs automatically

Workflow: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml). Triggers: every pull
request, and pushes to `main`. Read-only token; superseded PR commits are auto-cancelled
(the default branch is never cancelled mid-build).

| Job (check name) | Failure domain | What it proves |
|---|---|---|
| **`backend-quality`** | Python correctness/style/types | `ruff format --check` · `ruff check` · **`mypy --strict`** · `pytest tests/unit` with **≥80% coverage** |
| **`frontend-quality`** | Web app | the exact `pnpm check` contract — **typecheck · lint · Vitest/RTL · production build** |
| **`postgres-integration`** | Real-DB semantics | migrate an **empty** Postgres → head · assert **exactly one Alembic head** · run the Postgres-only tests (uniqueness, idempotency, citation FK) against the migrated schema |
| **`compose-boot`** | Container image | the Docker image builds and serves `/health` |

These four are the intended **required** branch-protection checks. (This repo is not yet a
GitHub remote; the founder selects these in *Settings → Branches* once it is pushed.)

## Zero live AI in CI

No job contacts Gemini, Anthropic, or any model provider, and **no API key is required**.
Protection is structural, not "we just didn't set the key":

- `AI_PROVIDER` defaults to `mock` (the deterministic in-process provider); an unknown value
  fails loudly rather than silently falling back.
- Real adapters are **lazy-imported** only when their provider is selected; the Anthropic SDK
  is an optional extra that CI never installs.
- `AI_PROVIDER=mock` is set explicitly on the backend jobs (belt-and-suspenders).
- A regression guard — `tests/unit/test_ai_egress_guard.py` — asserts the default is `mock`,
  that `get_ai_provider()` returns the mock, and (by AST) that the seam imports no vendor SDK
  at module scope.

The live A–G model quality harness (`scripts/run_quality_eval.py`) is a **founder/manual**
exercise on synthetic fixtures — never CI.

## Run it locally

Fastest inner loop first; the full set mirrors CI.

```bash
# Fast pre-commit/pre-push (seconds)
cd backend  && uv run ruff check . && uv run mypy .      # lint + types
cd frontend && pnpm typecheck && pnpm test               # types + behavioral tests

# Full local equivalent of CI (what the merge gate enforces)
make check          # backend: format+lint+mypy+unit+coverage ; frontend: pnpm check
make check-int      # postgres-integration: migrate -> single-head -> Postgres tests

# By domain
cd backend  && uv run pytest tests/unit --cov=app --cov-fail-under=80   # backend only
cd frontend && pnpm check                                               # frontend only

# PostgreSQL integration + migration verification (needs a Postgres)
make up             # start local Postgres (host 5433) + mailhog + backend
DATABASE_URL=postgresql+asyncpg://app:app@localhost:5433/hiring \
  uv run --project backend alembic upgrade head          # empty -> head
cd backend && uv run alembic heads                       # expect exactly one "(head)"
make check-int                                            # runs the -m integration tests
```

> Windows note: the project `.venv` python may be WDAC-blocked. Point `uv` at a
> writable-location venv (`UV_PROJECT_ENVIRONMENT=…`) and use `uv run --python 3.12`.
> CI (Linux) is the **authoritative** environment for `mypy` and the coverage gate.

## Determinism

- Installs respect lockfiles and fail rather than rewrite them: `uv sync --frozen`,
  `pnpm install --frozen-lockfile`.
- Runtimes are pinned: Python `3.12` (`UV_PYTHON`), Node `20`, pnpm `9` (matches
  `pnpm-lock.yaml`), Postgres `16.9`.
- Caching: uv cache and the pnpm store are cached; no generated app state (`.next`, DBs) is
  cached — that could make tests nondeterministic.

## Artifacts & secrets

- On failure, only `backend-quality` uploads `coverage.xml` (7-day retention). No `.env`, DB
  dumps, AI payloads, or invitation tokens are ever uploaded.
- No secrets live in the workflow. The integration DB uses deterministic, **non-secret**
  throwaway credentials for an ephemeral service container only.

## Known CI risks / follow-ups (for Epic 8.2 / 8.3)

- **Not yet observed on GitHub.** The workflow is validated locally + statically; it has not
  run on GitHub Actions because there is no remote yet. First push should confirm a green run.
- `compose-boot` pulls `mailhog/mailhog:latest` (unpinned) — pin at first real deploy (Epic 9).
- `next lint` is deprecated (Next 16 removes it); migrate to the ESLint CLI later.
- Deeper security/architecture gates (secret scanning, dependency audit, forbidden-import
  and tenant-isolation enforcement, a live-egress guard at the network layer) are **Story 8.2**.
