# Hiring Intelligence — MVP

> **Project status:** Epic 0 ✓ · Epic 1 auth lifecycle ✓ · Epic 2 ✓ (create → activate → list/view → **campaign UI**) · design system standardized (`frontend/DESIGN.md`) · **Epic 3 — candidates**: a recruiter adds candidates to an active campaign — single, **bulk CSV import** (per-row imported/skipped/failed), and a **premium roster workspace** (3.3: TanStack Table, density header, add-candidate modal, CSV import with a dismissible results panel) — with **identity (PII) separated from evaluation from day one** (`Candidate` = PII, `CandidateEvaluation` = AI-visible; INV-006). Recruiter dashboard (D1) is the premium logged-in home. **Epic 4 in progress** — 4.1 candidate invitation (secure magic link, INV-009) · 4.2 consent (append-only versioned fact; `has_active_consent` gate — INV-010) · **4.3 Structured Work Sample**: a recruiter designs the evidence-collection instrument (text-first tasks, each mapping to campaign competencies with an evidence intent) in a premium Work Sample Designer with live competency-coverage. Activation requires a work sample covering every competency (INV-011); the instrument freezes with the campaign (INV-003). **4.4 candidate work-sample experience**: the candidate opens the frozen work sample (behind 3 server-side gates — valid invitation · active consent · active campaign), works task-by-task with **autosave**, can leave and return (server-authoritative drafts), and reviews before submitting. Draft responses are mutable working state; **4.5 submission** promotes them — atomically, consent-gated, idempotently, irreversibly — into an **immutable `Evidence`** snapshot (append-only, PII-free), marks the evaluation `submitted`, and locks editing. **INV-012: Evidence is the only candidate-authored input the AI may evaluate** — never drafts or PII. **✅ Epic 4 complete: a full evidence-generation pipeline** — role → work sample → invite → consent → complete → submit → immutable Evidence — with **no AI yet**. **Epic 5 — AI Evaluation (the moat) in progress.** **5.1 the AI boundary + provider seam**: the *only* legal AI input is `Frozen Role Profile + Frozen Work-Sample Tasks + Immutable Evidence`, assembled by `EvaluationInputAssembler` (which cannot reach Candidate PII or mutable drafts) and passed through a `PIIMinimizer` (because candidate free-text can contain PII even though Evidence has no PII columns). A narrow `AIProvider` seam has one implementation — a **deterministic mock** (no real model, no network, no cost). Untrusted provider output is schema/grounding/policy-validated; the **platform** computes confidence (a reliability signal, *not* a success probability); a governed **honesty floor** forces `ESCALATE` under uncertainty. AI **proposes** (`STRONG_PROCEED…ESCALATE`), a human **decides** — there is no `HiringDecision` type (INV-013). **5.2 evaluation execution + immutable persistence**: a recruiter triggers `POST /evaluations/{id}/evaluate` (consent re-checked, submitted-evidence required); the validated proposal is persisted as an **immutable `Evaluation`** (run/rerun history, grounded competency assessments, durable citations to Evidence, flattened provenance, a SHA-256 `input_fingerprint`) with `evaluate` idempotent and `rerun` explicit (INV-014). **5.3 first real Claude provider + production-safe boundary**: real providers live behind the `AIProvider` seam (config-driven `AI_PROVIDER=mock|anthropic|gemini`, **mock is default + the only provider in tests**; **no silent fallback**). `GeminiAIProvider` (free tier, **synthetic fixtures only** — the free tier may train on data, TD-017) is a portability path for the first real-model A–G quality run without buying credits; `AnthropicAIProvider` (paid) stays intact, live verification pending, rendering the governed prompt with **pseudonymous evidence ids** so no internal UUIDs/PII egress; its output stays untrusted and re-runs our validators. **TD-011 resolved** — evaluation execution owns its transaction boundary, so **no DB transaction is held during the provider call**. PII minimization hardened before egress; token usage persisted; **no caching** (deliberate). See **`docs/ai-boundary.md`**. `docs/domain-invariants.md` INV-001..014. API: `docs/api-contract.md`. **User capabilities: 12 recruiter + 4 candidate.** **Next: Epic 5 review, then the recruiter Evaluation UI / prompt-quality iteration** — after a deliberate review. Backlog: `mvp/MVP-02`.

Evidence-based hiring intelligence: a candidate completes a text-first work sample, the
system produces an **evidence-cited, explainable** evaluation (AI *proposes*), and a
**human decides**. This repo is the MVP build; the frozen design corpus in
`docs/`, `arch/`, `validation/`, `product/`, `sprint/`, and `mvp/` is the long-term
North Star (read-only reference — see `mvp/MVP-01` and `mvp/MVP-02`).

## Stack
- **Backend:** Python 3.12, FastAPI, uv, Ruff, MyPy, pytest
- **Frontend:** Next.js (App Router), TypeScript, Tailwind + design system (Geist, Motion, React Hook Form + Zod, Sonner, next-themes, Lucide), pnpm — premium SaaS quality, see `frontend/DESIGN.md`
- (later) PostgreSQL, Anthropic Claude, Cloudflare R2, Docker Compose

## Prerequisites
- [uv](https://docs.astral.sh/uv/) · Python 3.12 · Node 20+ · [pnpm](https://pnpm.io/)

## Quick start
```bash
make install     # deps + pre-commit hooks

# Option A — host processes (fastest reload for active coding):
make dev         # backend :8000  +  frontend :3000

# Option B — full stack in Docker (db + mailhog + backend):
make up          # backend :8000, Postgres :5432, Mailhog UI :8025
make dev-frontend  # frontend still runs on the host
```
Other commands: `make test`, `make lint`, `make fmt`, `make clean`, `make down`, `make help`.
> Prereqs: uv · Python 3.12 · Node 20+ · pnpm · Docker (for `make up`). On Windows, use WSL2/Git Bash for `make`.

## Layout
```
backend/    FastAPI app (module structure mirrors the bounded contexts)
frontend/   Next.js app (recruiter + candidate UIs)
mvp/        MVP-01 roadmap + MVP-02 backlog (what we build)
docs/ arch/ validation/ product/ sprint/   frozen North Star (reference)
```

## How we build
One story = one branch = one PR = one review. See `mvp/MVP-02-engineering-backlog.md`.
Currently implemented: **Story 0.1 — Repo & Tooling** (scaffold only).
