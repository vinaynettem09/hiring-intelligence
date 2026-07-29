# MVP-02 — Engineering Backlog

| Field | Value |
|---|---|
| **Document ID** | MVP-02 |
| **Title** | Engineering Backlog (the last planning artifact) |
| **Author role** | Founding Engineer / Technical Co-Founder |
| **Status** | Working backlog — becomes GitHub issues |
| **Created** | 2026-07-23 |
| **Type** | **Executable work only.** Derived from MVP-01. No architecture, no ADRs. **This is the final document; after this, everything is issues + code.** |
| **The product** | **One amazing workflow**, not a platform: *Recruiter → Create Campaign → Invite Candidate → Candidate completes work sample → AI evaluates → Recruiter reviews evidence → Recruiter decides → Candidate receives feedback.* |
| **Estimation basis** | Hours, solo founder + AI pairing (Claude generates, you integrate/decide/test). ~**216h** total ≈ 10–12 weeks at a sustainable solo pace. Estimates are for *building + basic tests*, not gold-plating. |

---

## How to use this backlog

- Each **Story** below becomes **one GitHub issue** (title = story title, body = tasks + DoD + estimate).
- **Epics** become GitHub **labels** (`epic:auth`, `epic:ai-eval`, …); **weeks** become **milestones** (`Week 1`…`Week 12`).
- Build **top-to-bottom** — the order is the critical path. Don't start an epic before its predecessors unless noted "parallel-ok."
- **Definition of Done is non-negotiable per story.** If a DoD item is cut, it's a scope decision made explicitly, not by accident.

### Global Definition of Done *(applies to EVERY story — the product soul, kept cheap)*
Every mutating endpoint: **tenant-scoped** (INV-10), **authorized** (server-side, never trust client), **writes an `audit_log` row** (P8), **error-handled** (typed → JSON). Every AI output: **PII-minimized before the model** (AD-89), **grounded in cited evidence** (AD-90), **never auto-decides** (INV-1). Every candidate-facing surface: shows **only their own** data (P13). No secrets in the repo. Code passes ruff + mypy + tests in CI.

---

## Epic & effort rollup

| Epic | Title | Est. | Week(s) | Core workflow? |
|---|---|---|---|---|
| **E0** | Project Foundation (Walking Skeleton) | 24h | 1 | enabler |
| **E1** | Authentication & Tenancy | 18h | 2 | enabler |
| **E2** | Campaign Management | 16h | 3 | ✅ step 1 |
| **E3** | Candidate Intake | 16h | 3 | ✅ step 2 |
| **E4** | Candidate Flow (Invite→Consent→Work Sample) | 24h | 4 | ✅ steps 3–4 |
| **E5** | **AI Evaluation (THE HEART)** | 40h | 5–6 | ✅ step 5 |
| **E6** | Recruiter Dashboard (evidence review) | 20h | 7 | ✅ step 6 |
| **E7** | Human Decision | 14h | 8 | ✅ step 7 |
| **E8** | Candidate Feedback | 12h | 9 | ✅ step 8 |
| **E9** | Audit & Trust surface | 8h | 8–9 | supporting |
| **E10** | Ship & Harden | 24h | 9–10 | ship |
| | **Total** | **~216h** | ~10–12 | |

---

## E0 — Project Foundation (Walking Skeleton) · Week 1 · 24h
*Goal: an empty app deployed and green before any feature. Prove the pipe.*

### Story 0.1 — Repo & tooling · 3h
- **Backend:** init repo; `uv` project; ruff + mypy config; `pytest`.
- **Frontend:** Next.js (App Router, TS) + Tailwind + shadcn/ui + `pnpm`.
- **Shared:** `Makefile` (`up/dev/seed/test/migrate`); `.env.example`; pre-commit (ruff, gitleaks).
- **DoD:** `make dev` runs backend + frontend locally; pre-commit blocks a planted secret.

### Story 0.2 — Docker Compose + one-command up · 3h
- **Tasks:** compose with `app` + `postgres` + `mailhog`; `make up` = compose up + migrate + seed.
- **DoD:** `make up` yields a running stack from a clean clone in < 10 min.

### Story 0.3 — FastAPI app factory + observability-lite · 4h
- **Backend:** app factory; Pydantic `Settings`; **structlog** JSON; **correlation-id middleware**; **envelope context** (tenant/actor/correlation) as a request-scoped object (lite AD-53).
- **DoD:** every request logs a correlation id; envelope available to handlers.

### Story 0.4 — DB layer + Alembic + first migration · 3h
- **Backend:** SQLAlchemy 2.0 async engine/session; Alembic init; migration for `organizations`; a **tenant-scoped base repository** helper (auto-filters `tenant_id`).
- **DoD:** `alembic upgrade head` creates the schema; base repo enforces tenant filter.

### Story 0.5 — Error model + handlers · 2h
- **Backend:** typed app errors (Validation/Auth/Conflict/NotFound/BusinessRule) → JSON responses with stable `type` (lite AD-72); no stack traces / PII leaked.
- **DoD:** a raised app error returns the right status + shape.

### Story 0.6 — Health + `/me` stub · 1h
- **DoD:** `GET /health` returns ok; `GET /me` returns 401 unauthenticated (auth lands in E1).

### Story 0.7 — Next.js shell · 4h
- **Frontend:** layout (recruiter area + candidate area routes), typed **API client** (fetch wrapper), theme, a health-check page hitting the backend.
- **DoD:** frontend renders and successfully calls `/health`.

### Story 0.8 — CI · 2h
- **Tasks:** GitHub Actions: ruff, mypy, pytest, frontend build.
- **DoD:** CI green on `main`; red blocks merge.

### Story 0.9 — Deploy walking skeleton · 2h
- **Tasks:** Render (or Fly) web service + **Neon** Postgres; run migrations on deploy; env/secrets in platform.
- **DoD:** `GET /health` live over HTTPS in prod; frontend deployed (Vercel or same host).

---

## E1 — Authentication & Tenancy · Week 2 · 18h

### Story 1.1 — Signup (org + first user) · 4h
- **Backend:** `POST /auth/signup` → create `organization` (tenant) + `user` (argon2 hash, role=recruiter/admin).
- **Frontend:** signup page.
- **Tests:** dup-email rejected; password hashed.
- **DoD:** signing up creates a tenant + user; can't sign up twice with same email.

### Story 1.2 — Login + JWT · 4h
- **Backend:** `POST /auth/login` → verify argon2 → short-lived access JWT + refresh; `POST /auth/refresh`.
- **Frontend:** login page; token storage (httpOnly cookie preferred).
- **DoD:** valid creds return a working token; invalid → 401.

### Story 1.3 — Auth middleware + tenant injection · 4h
- **Backend:** JWT validation middleware; inject tenant + actor + role into the **envelope**; **every** query goes through tenant-scoped repo.
- **Tests:** a request without token → 401; tenant leakage test (user A can't read org B).
- **DoD:** protected routes require a valid token; cross-tenant read is impossible.

### Story 1.4 — `/me` + frontend auth · 4h
- **Backend:** `GET /me`. **Frontend:** protected route wrapper; redirect to login; logout.
- **DoD:** logged-in user sees a (empty) dashboard; logout works.

### Story 1.5 — Roles (minimal) · 2h
- **Backend:** role on user (recruiter / hm / admin); a simple `require_role` dependency.
- **DoD:** an admin-only endpoint rejects a non-admin.

---

## E2 — Campaign Management · Week 3 · 16h · *workflow step 1*

### Story 2.1 — Create campaign + role profile · 4h
- **Backend:** `campaigns` table (role_title, `role_profile` jsonb: competencies + bar, status=draft); `POST /campaigns`.
- **DoD:** recruiter creates a draft campaign with a role profile.

### Story 2.2 — Activate campaign · 2h
- **Backend:** `POST /campaigns/{id}/activate` → status=active; **freeze role_profile** (no edits after active); audit.
- **DoD:** activation locks the role profile; edits after active are rejected.

### Story 2.3 — List / view campaigns · 3h
- **Backend:** `GET /campaigns`, `GET /campaigns/{id}` (tenant-scoped).
- **DoD:** recruiter sees only their org's campaigns.

### Story 2.4 — Frontend: campaign UI · 7h
- **Frontend:** create form (role title + competencies/bar builder), campaign list, campaign detail (roster placeholder).
- **DoD:** full create → activate → view flow works in the UI.

---

## E3 — Candidate Intake · Week 3 · 16h · *workflow step 2* · parallel-ok with E2

### Story 3.1 — ObjectStore interface + impls · 3h
- **Backend:** `ObjectStore` interface; local-disk impl (dev); **Cloudflare R2** impl (prod); short-lived signed URLs.
- **DoD:** a file uploads + downloads via the interface in both impls.

### Story 3.2 — Candidate model + add one · 4h
- **Backend:** `candidates` (name, email, resume_object_key — **PII table; AI never reads it directly**); `candidate_evaluations` (campaign_id, candidate_id, status=invited); `POST /campaigns/{id}/candidates` (+ optional resume upload).
- **DoD:** adding a candidate creates candidate + candidate_evaluation; resume stored.

### Story 3.3 — CSV import · 3h
- **Backend:** `POST /campaigns/{id}/candidates/import` (CSV → many candidates); per-row validation + error report.
- **DoD:** a CSV of N candidates imports; bad rows reported, good rows created.

### Story 3.4 — Frontend: candidate intake · 6h
- **Frontend:** add-candidate modal (+ resume drag-drop), CSV upload, candidate list on campaign detail with status badges.
- **DoD:** recruiter adds candidates manually + via CSV and sees them listed.

---

## E4 — Candidate Flow (Invite → Consent → Work Sample) · Week 4 · 24h · *workflow steps 3–4*

### Story 4.1 — Email interface + impls · 3h
- **Backend:** `Email` interface; Mailhog impl (dev); **Resend** impl (prod).
- **DoD:** an email sends to Mailhog in dev.

### Story 4.2 — Invitation + send · 4h
- **Backend:** `invitations` (candidate_evaluation_id, signed token, expires_at, status); `POST /candidate-evaluations/{id}/invite` → create token + send email with link; audit.
- **Frontend:** "Invite" action + status badge + copy-link.
- **DoD:** inviting sends an email containing a working tokenized link.

### Story 4.3 — Candidate landing (resolve token) · 3h
- **Backend:** `GET /invite/{token}` → resolve (valid/expired/used) → minimal candidate + role context (no internal data).
- **Frontend:** candidate landing page (role, what to expect, honest AI disclosure).
- **DoD:** a valid link shows the landing; expired/used links show a clean message.

### Story 4.4 — Consent (the gate) · 3h
- **Backend:** `consents` table; `POST /invite/{token}/consent`; **no work sample served before consent** (INV-11); audit.
- **Frontend:** consent screen (clear, plain-language).
- **DoD:** work sample is inaccessible until consent is recorded.

### Story 4.5 — Work sample fetch + submit · 5h
- **Backend:** `work_samples` (prompt_id, content_object_key, submitted_at); `GET /invite/{token}/work-sample` (the task); `POST /invite/{token}/work-sample` (store content, mark submitted, **emit `WorkSampleSubmitted` event** → triggers E5); one-submission rule.
- **DoD:** candidate fetches the task, submits once; submission stored + event emitted; re-submit blocked.

### Story 4.6 — Frontend: candidate work-sample area · 6h
- **Frontend:** work-sample editor (text/code editor, task prompt, save-in-progress, submit), post-submit status ("submitted, in review").
- **DoD:** candidate completes and submits a work sample end-to-end in the browser.

---

## E5 — AI Evaluation (THE HEART) · Weeks 5–6 · 40h · *workflow step 5*
*The differentiator and the thesis. Spend the time here.*

### Story 5.1 — AIProvider interface + mock + Anthropic · 5h
- **Backend:** `AIProvider` interface (`invoke(capability, minimized_input, model_ref) -> proposal`); **deterministic mock** (fixed by content-hash — dev/CI $0); **Anthropic Claude** impl (Sonnet).
- **DoD:** the same evaluation flow runs against mock (default) and real Claude via an env flag.

### Story 5.2 — PII-minimization helper · 3h
- **Backend:** strip/pseudonymize name, contact, employer names from anything sent to the model; keep a tenant-side re-association map (not sent).
- **Tests:** assert **no PII string** ever appears in the provider payload.
- **DoD:** provider input is provably PII-minimized.

### Story 5.3 — Prompt + structured output schema · 5h
- **Backend:** versioned prompt file (`prompts/evaluate_work_sample.vN.md`) with id/version; Pydantic proposal schema (dimensions: technical quality, reasoning, debugging, communication, engineering maturity; each with score + **cited observations**; overall; rationale).
- **DoD:** Claude returns JSON conforming to the schema; version stamped on output.

### Story 5.4 — Evaluation orchestration · 8h
- **Backend (`intelligence` + `evaluation`):** on `WorkSampleSubmitted` → load work sample + frozen role_profile → PII-min → provider.invoke → validate → confidence → **persist** `evidence_items` (immutable), `evaluations`, `recommendations` (with explanation) → emit `EvaluationCompleted` fact + audit.
- **DoD:** a submitted work sample produces a complete, persisted, evidence-cited evaluation.

### Story 5.5 — Background job + status · 4h
- **Backend:** run 5.4 async (FastAPI BackgroundTasks now; a `jobs` table + worker loop if reliability bites); candidate/recruiter status reflects in-progress → done.
- **DoD:** submission returns immediately; evaluation completes in background; status updates.

### Story 5.6 — Grounding validation · 4h
- **Backend:** reject evaluations whose dimension claims lack cited observations traceable to the work sample; bounded retry; on persistent failure → mark for human review (no fabricated evidence).
- **Tests:** an ungrounded mock output is rejected.
- **DoD:** no evaluation is persisted without grounded, cited evidence (AD-90).

### Story 5.7 — Confidence computation · 3h
- **Backend:** compute confidence from evidence coverage/consistency (NOT the model's self-report); low confidence flagged for extra human attention.
- **DoD:** every evaluation carries a computed confidence; thin evidence → low confidence.

### Story 5.8 — Evaluation caching (cost control) · 2h
- **Backend:** cache proposals by content-hash(minimized input + prompt version + model version); reuse on re-run.
- **DoD:** re-evaluating identical input hits cache (no new API cost).

### Story 5.9 — Tests for the heart · 6h
- **Tests:** full mock-based flow (submit → evaluation persisted); grounding rejection; PII-never-sent; confidence low on sparse input; cache hit.
- **DoD:** the evaluation pipeline is covered end-to-end with the mock; CI runs it for free.

---

## E6 — Recruiter Dashboard (evidence review) · Week 7 · 20h · *workflow step 6*
*The demo screen. Make it clear and honest.*

### Story 6.1 — Campaign results API · 4h
- **Backend:** `GET /campaigns/{id}/results` → candidate evaluations ranked, each with overall + confidence + status (tenant-scoped). **Never a bare score** — payload always includes the evidence link.
- **DoD:** results return ranked evaluations with confidence.

### Story 6.2 — Evaluation detail API · 2h
- **Backend:** `GET /candidate-evaluations/{id}` → evidence_items by dimension + evaluation + explanation + confidence.
- **DoD:** full evidence detail returned (recruiter/HM only, never candidate).

### Story 6.3 — Frontend: results table · 6h
- **Frontend:** campaign results — ranked list, confidence indicator, status; click → detail. Score never shown without its evidence.
- **DoD:** recruiter sees ranked candidates and can open any.

### Story 6.4 — Frontend: evaluation detail (the demo screen) · 8h
- **Frontend:** evidence grouped by dimension, each score with its **cited observations**, the explanation, and honest confidence; clean, trustworthy, skimmable.
- **DoD:** a hiring manager can look at this screen and understand *why*, from evidence — the "would I act on this?" moment.

---

## E7 — Human Decision · Week 8 · 14h · *workflow step 7*

### Story 7.1 — Record decision · 4h
- **Backend:** `hiring_decisions` (decided_by, outcome advance/hold/reject, justification, decided_at — **immutable**); `POST /candidate-evaluations/{id}/decision`; audit. **System never auto-decides** (INV-1).
- **DoD:** a human records a decision; it's immutable and audited.

### Story 7.2 — Decision guards · 2h
- **Backend:** decision requires a completed evaluation; recommendation is advisory only; justification required when diverging from the recommendation.
- **DoD:** can't decide before evaluation exists; divergent decision requires a reason.

### Story 7.3 — Frontend: decision UI · 5h
- **Frontend:** advance / hold / reject buttons on the evaluation detail; justification field (required for reject/override); confirmation.
- **DoD:** recruiter/HM decides from the evidence screen; decision persists + shows.

### Story 7.4 — Tests · 3h
- **DoD:** decision flow + guards covered; no code path auto-decides.

---

## E8 — Candidate Feedback · Week 9 · 12h · *workflow step 8*

### Story 8.1 — Release feedback · 3h
- **Backend:** `feedback` (content, released_by, released_at, status); `POST /candidate-evaluations/{id}/feedback/release`; delivered **only after** a decision (recruiter-released, dignified, evidence-based, candidate-view only). Audit.
- **DoD:** recruiter releases feedback after a decision.

### Story 8.2 — Candidate views feedback · 2h
- **Backend:** `GET /invite/{token}/feedback` (only released, candidate-view content).
- **DoD:** candidate sees their feedback only after release; never internal mechanics.

### Story 8.3 — Frontend: feedback · 7h
- **Frontend:** recruiter feedback composer (pre-filled from evaluation, editable, "not the strongest match" framing not "not good enough"); candidate feedback page.
- **DoD:** the full release → candidate-view loop works with dignified framing.

---

## E9 — Audit & Trust surface · Weeks 8–9 · 8h · supporting

### Story 9.1 — Audit write helper (ensure coverage) · 3h
- **Backend:** a single `record_event(action, entity, payload)` helper writing `audit_log`/`domain_events`; audit sweep — assert every mutating endpoint calls it.
- **DoD:** every material action produces an audit row (test asserts coverage on key flows).

### Story 9.2 — Audit API · 2h
- **Backend:** `GET /audit` (tenant-scoped, admin) with filters (campaign, candidate).
- **DoD:** admin can query the tenant's audit trail.

### Story 9.3 — Frontend: audit view · 3h
- **Frontend:** simple audit table (who/what/when).
- **DoD:** the trust story is visible in-product.

---

## E10 — Ship & Harden · Weeks 9–10 · 24h

### Story 10.1 — Real email + storage in prod · 3h
- **Tasks:** wire Resend + R2 with prod secrets.
- **DoD:** a real invite email arrives; a real resume/work sample stores in R2.

### Story 10.2 — Sentry + prod logging · 2h
- **DoD:** an exception in prod appears in Sentry with correlation id.

### Story 10.3 — Author the real work-sample task + role template · 4h *(you + Claude — product content)*
- **Tasks:** write one strong, realistic engineering work-sample task; a starter role-profile template. *(This is product quality work, not boilerplate.)*
- **DoD:** a real candidate could do a meaningful task; the evaluation of it is genuinely useful.

### Story 10.4 — Empty / error / loading states · 5h
- **Frontend:** every screen handles empty, loading, error; no dead-ends (DOC-06 no-black-hole spirit).
- **DoD:** no screen shows a raw error or infinite spinner.

### Story 10.5 — Security pass · 4h
- **Tasks:** verify authz + tenant scope on **every** endpoint; basic rate limit on auth + candidate endpoints; secrets audit; input validation review.
- **DoD:** a checklist pass; no endpoint missing tenant/authz; no secret in repo.

### Story 10.6 — Prod deploy + smoke · 3h
- **Tasks:** remove dev seed from prod; run the full workflow in prod once end-to-end.
- **DoD:** the eight-step workflow completes in prod with real infra.

### Story 10.7 — First-user onboarding · 3h
- **Tasks:** a minimal "getting started" + optional sample data toggle for demos.
- **DoD:** a new recruiter can go from signup to first evaluation without hand-holding.

---

## MVP Definition of Done *(the whole thing)*
The MVP ships when a real recruiter can, in production, unassisted: **sign up → create a campaign → invite a candidate → the candidate consents and completes a work sample → the AI produces an evidence-based, explainable, PII-minimized evaluation → the recruiter reviews the evidence and makes a human decision → the candidate receives dignified feedback** — with every action audited and tenant-isolated. Then: **invite 1–3 friendly users and watch them use it.**

## NOT in this backlog (v2 — say no on purpose)
Benchmarking · Hiring Memory · Outcome Learning · Evidence Graph · Talent Pool/afterlife · statistical fairness dashboard · ATS/HRIS integrations · SSO/OIDC/MFA · enterprise RBAC · multi-region · billing · analytics dashboards · voice/adaptive/live interviews · public API · mobile app · microservices/Kafka/k8s. *(Each has a migration trigger in MVP-01 §15. Not now.)*

## GitHub setup (do this once, then live in issues)
- Labels: `epic:foundation|auth|campaign|intake|candidate-flow|ai-eval|dashboard|decision|feedback|audit|ship`, `type:backend|frontend|tests`, `priority:critical-path`.
- Milestones: `Week 1` … `Week 12`.
- One issue per Story (copy tasks + DoD + estimate). One project board (Todo / Doing / Done).
- Branch per story (`e5.4-evaluation-orchestration`), PR → review (with Claude) → merge → CI deploys.

---

## 🚪 Documentation phase — CLOSED

This is the final planning artifact. The corpus is complete: **DOC-01→12 · VALIDATION-01→04 · PRODUCT-01 · ARCH-01→16 · SPRINT-0 · MVP-01 · MVP-02.** From here, no more documents — we build, review, test, and ship. The next words in this project should be **code**, starting with **Story 0.1**.

*Team from here: Claude generates code/UI/boilerplate/refactors + reviews; you own architecture calls, AI-evaluation quality, prompts, security, and scope discipline; you integrate, decide, test, ship. Let's build.*
