# MVP-01 — Implementation Roadmap

| Field | Value |
|---|---|
| **Document ID** | MVP-01 |
| **Title** | Implementation Roadmap (the solo-founder execution plan) |
| **Author role** | Founding Engineer / Technical Co-Founder |
| **Status** | Draft v0.1 — the plan we build from |
| **Created** | 2026-07-23 |
| **Type** | **Engineering execution plan.** NOT architecture, NOT product, NOT an ADR. The architecture corpus (ARCH-01→16) is **frozen and is the North Star**; this plan takes the cheap road toward it. |
| **Team** | 1 founder (full-stack). No employees, no partners, near-zero budget. |
| **Goal** | **A real, usable MVP in users' hands in ~10–12 weeks** — demoable to users and investors, and capable of producing real learning about AS-1. |
| **The question behind every choice** | **"What is the smallest thing that provides learning?"** — never "what is the most scalable thing?" |

---

## 1. MVP Philosophy

**Build to learn.** The MVP is an instrument, not a product launch. Its job is to put evidence-based evaluation in front of real recruiters/hiring managers and candidates and learn: *do they trust it? do they act on it? do candidates find it fairer?* That is AS-1/H3/H4 tested with a working thing — L3 "pilot signal" evidence (VALIDATION-04) — and it doubles as the demo that recruits design partners and investors.

**Optimize for speed of learning.** Every hour goes to the shortest path to "a hiring manager looked at an evidence-based evaluation and reacted." Anything that doesn't shorten that path waits.

**Keep the migration path to ARCH-16.** We simplify *topology and infrastructure*, never the *domain model or product soul*. The module boundaries mirror the frozen bounded contexts, so a module can later become a service without a rewrite. Cheap seams now = a real road home later (§15).

**Avoid premature complexity.** We postpone complexity until a real trigger forces it (§15). No Kafka because "the architecture has Kafka." No microservices because "we'll need to scale." We will not.

### 1.1 The line: what we KEEP (soul) vs what we DROP (scaffolding)

| ✅ KEEP — this *is* the product/thesis (cheap to keep) | North Star ref |
|---|---|
| **AI proposes; a human decides** — the hiring decision is always a human act | INV-1 / AD-88 |
| **Evidence-based, explainable output** — every judgment cites specific evidence; no bare score | INV-2/INV-4 / AD-90 |
| **Consent before evaluation** — candidate consents; recorded | INV-11 |
| **Append-only audit log** of every material action (also = our future event stream) | P8 / AD-32 |
| **`tenant_id` on everything** — isolation by column from day one | INV-10 |
| **PII minimized before the AI sees content** (strip name/contact/employer) — cheap, and it's the bias story | AD-89 |
| **`AIProvider` interface (ACL)** — one provider behind it; AI returns validated *proposals* | AD-52/AD-56 |
| **Platform interfaces** (storage/email/events) as thin abstractions | AD-87 |
| **Module boundaries = bounded contexts** | ARCH-03/06 |

| ❌ DROP for MVP — scaffolding for scale/teams we don't have | Re-adopt when… (§15) |
|---|---|
| 13 microservices → **one modular monolith** | a module needs independent scale/ownership |
| Kafka/event backbone → **in-process events + a `domain_events` table (outbox-lite)** | cross-service async/replay at scale |
| Per-service DBs + event sourcing → **one PostgreSQL, state + audit/event table** | modules need independent data lifecycle |
| Kubernetes/Istio/SPIFFE → **Docker Compose + a managed host** | multi-node, real traffic, a team |
| gRPC/service mesh → **in-process function calls** | services actually separate |
| OpenSearch → **Postgres queries / full-text** | search scale demands it |
| Vault/KMS/crypto-shred → **platform secrets + env; delete-row for now** | real PII scale + compliance need |
| Statistical fairness gate → **fairness-by-construction + mandatory human review** (honest: adverse-impact needs volume) | evaluation volume makes it computable |
| Contract-first codegen (ARCH-09) → **FastAPI-first, auto OpenAPI** | multiple/external API consumers |
| OTel/Prometheus/Tempo/Loki → **structured logs + Sentry** | production scale / incident load |
| Multi-provider AI routing → **one provider (Anthropic Claude)** | need failover/cost/quality diversity |

> **The rule:** if dropping it would stop us testing the thesis, it's soul — keep it. If dropping it only costs us scale we don't have, it's scaffolding — drop it.

---

## 2. Technology Stack *(simplest production-ready)*

| Layer | Choice | Why (solo + cheap + fast) |
|---|---|---|
| **Backend** | **Python 3.12 + FastAPI + Pydantic v2**, async | matches North Star (ARCH-10); fast to build; great AI-lib ecosystem |
| **Frontend** | **Next.js (App Router) + TypeScript + Tailwind + shadcn/ui** | one framework for recruiter + candidate UIs; fast, good-looking defaults for demos |
| **Database** | **PostgreSQL** (managed: **Neon** or **Supabase** free tier) | one DB; no DB ops; generous free tier |
| **Migrations** | **Alembic** | Python-native; matches North Star |
| **ORM/DB access** | **SQLAlchemy 2.0 (async)** | mature; async |
| **Background work** | **FastAPI BackgroundTasks → a `jobs` table + a simple worker loop** when reliability matters | AI eval is slow; start trivial, harden only if needed |
| **AI** | **Anthropic Claude API** (Haiku for cheap tasks, Sonnet for judgment) behind `AIProvider` | single provider (AD-85 lite); cost-controlled |
| **Object storage** | **`ObjectStore` interface** → local disk (dev) / **Cloudflare R2** (prod, free tier, S3 API) | resumes/work samples; cheap; swappable |
| **Auth** | **email + password (argon2) + JWT**, magic-link tokens for candidates | simplest secure auth; no SSO yet |
| **Email** | **`Email` interface** → Resend (free tier) / Mailhog (dev) | invitations/notifications |
| **Deploy** | **Docker Compose** locally; **Render** or **Fly.io** for prod | one-command; cheap; HTTPS included |
| **Errors/obs** | **structlog** JSON logs + **Sentry** (free tier) | enough to debug in prod |
| **Dep mgmt** | **uv** (backend), **pnpm** (frontend) | fast |
| **Repo** | one Git repo, `backend/` + `frontend/` + `infra/` | solo-friendly |

**Cost posture:** everything on free tiers except the Anthropic API (pay-as-you-go). Control AI cost via cheap-model-by-default, content-hash caching of evaluations, and low token budgets. Estimated monthly run cost at MVP: **~$0–50 + AI usage.**

---

## 3. Simplified Architecture *(frozen corpus → modular monolith)*

```
                        ┌──────────────────────────────────────────┐
   Next.js frontend ───▶│  FastAPI app (ONE deployable)             │
   (recruiter + cand.)  │                                          │
                        │  modules/ (= bounded contexts, ARCH-03)  │
                        │   identity  candidate  campaign          │
                        │   evaluation  intelligence(AI/ACL)       │
                        │   trust(consent·audit·fairness-lite)     │
                        │   decision  feedback  delivery  notify   │
                        │                                          │
                        │  platform/ (interfaces + simple impls)   │
                        │   ObjectStore  Email  Events  AIProvider │
                        │                                          │
                        │  in-process event bus → domain_events tbl│
                        └───────────────┬──────────────────────────┘
                                        │
                        ┌───────────────┴───────────┐   ┌─────────────┐
                        │  PostgreSQL (one DB)       │   │ Anthropic   │
                        │  all tables, tenant_id,    │   │ Claude API  │
                        │  append-only audit_log     │   │ (via ACL)   │
                        └────────────────────────────┘   └─────────────┘
                        R2/local disk (files) · Resend (email)
```

**How the mapping preserves the North Star:**
- The **13 services collapse to 13 modules** in one process. Same boundaries (ARCH-06), same ownership, just in-process calls instead of gRPC.
- **Legal interactions (ARCH-04) still hold** — modules call each other only where allowed; forbidden calls (Recommendation→Candidate, cross-tenant) simply aren't coded. This costs nothing and keeps the discipline.
- **The event backbone becomes an in-process bus + a `domain_events` table.** Facts still get emitted and stored (append-only) — that table *is* the audit trail *and* the seed of the future Kafka stream. When we split a service later, it already emits its facts.
- **The gates are functions/modules, not separate deployables.** Consent, audit, PII-minimization, human-decision, explainability all run in-process — but they run. Statistical fairness is honestly deferred (needs volume); fairness-by-construction replaces it (§8).
- **`AIProvider` ACL stays.** One provider, but the boundary is intact, so the AI never becomes authoritative and swapping/adding providers later is trivial.

> This is exactly the "modular monolith of the frozen modules, gates isolated, co-deploy the rest" that ARCH-06 AD-41 explicitly *permitted* as the MVP path. We are not violating the architecture — we're taking the road it left open.

---

## 4. MVP Scope

The scope is the **core evidence-based hiring loop** from PRODUCT-01, trimmed to what tests the thesis. One role at a time, one company at a time.

### 4.1 What EXISTS (MVP features)
1. **Accounts & org** — recruiter/HM sign up, one organization (tenant) per signup.
2. **Create an Evaluation Campaign** for one role, with a **thin role profile / calibration** (what "good" looks like: key competencies, the bar).
3. **Add candidates** — CSV import **and/or** manual add + resume upload (AD-11). No ATS.
4. **Invite a candidate** (email link) → candidate **consents** → candidate completes a **text-first Structured Work Sample** (AD-10): a realistic engineering task, answered in-browser.
5. **AI evaluation** — the work sample is evaluated (PII-minimized first): produces **structured evidence across dimensions** (technical quality, reasoning, debugging, communication, engineering maturity), an **evaluation with cited evidence**, a **confidence** level, and an **explanation** (AI *proposes*).
6. **Recruiter dashboard** — candidates for the campaign, ranked, each with evidence + confidence + explanation. **No bare score** — always with its evidence.
7. **Hiring-manager review & decision** — a human reviews the evidence and **decides** advance/reject (the system never decides). Decision recorded.
8. **Candidate feedback** *(lean)* — recruiter can release simple, dignified, evidence-based feedback to the candidate.
9. **Results view / export** — see and download campaign results.
10. **Audit log** — every material action recorded (visible to admin; our trust story).

### 4.2 What does NOT exist (explicitly out)
- ❌ Benchmarking, Hiring Memory, Outcome Learning, Talent Pool, Evidence Graph (the compounding moat — later).
- ❌ Statistical fairness / adverse-impact **gate** (needs volume; replaced by fairness-by-construction + mandatory human review — §8).
- ❌ ATS/HRIS integrations, SSO/OIDC, enterprise RBAC.
- ❌ Voice/adaptive/live interviews (text-first only, AD-10).
- ❌ Microservices, Kafka, k8s, multi-region, event sourcing.
- ❌ Real-time collaboration, notifications beyond essential emails.
- ❌ Billing/payments.
- ❌ Network effects, candidate afterlife/portable evidence.

### 4.3 The thesis-critical path (build this to *learn*)
> **candidate submits work sample → AI produces evidence-based, explainable evaluation → hiring manager looks at it and reacts.** Everything else supports this. If a hiring manager says "this evidence is genuinely useful — I'd act on it," we've learned the most important thing. Front-load this thread (§13).

---

## 5. Module Structure

Modular monolith. Each module = a bounded context (ARCH-03), internally Clean-Architecture-lite. Modules expose an **application service**; other modules call *that*, never reach into internals.

```
backend/app/
├── modules/
│   ├── identity/        # org, user, auth (tenant source)
│   ├── candidate/       # candidate identity + intake (CSV/resume)
│   ├── campaign/        # evaluation campaign + thin calibration + roster
│   ├── evaluation/      # candidate_evaluation, work_sample, evidence, evaluation, recommendation
│   ├── intelligence/    # AI orchestration: ACL, PII-min, prompt, structured+grounded output, confidence
│   ├── trust/           # consent, audit(event log), fairness-by-construction, PII helpers
│   ├── decision/        # hiring_decision (human)
│   ├── feedback/        # candidate feedback (recruiter-released)
│   ├── delivery/        # export/results
│   └── notification/    # email (invites, releases)
├── platform/            # interfaces + simple impls (AD-87)
│   ├── object_store.py  # interface + local + R2
│   ├── email.py         # interface + Resend + Mailhog
│   ├── events.py        # in-process bus + domain_events persistence
│   └── ai_provider.py   # interface + Anthropic + mock
├── shared/
│   ├── db.py            # async engine/session
│   ├── ids.py           # opaque IDs (uuid/ulid)
│   ├── envelope.py      # tenant/actor/correlation context (lite AD-53)
│   ├── errors.py        # error → HTTP mapping (lite AD-72)
│   └── logging.py       # structlog + correlation id
├── api/                 # FastAPI routers (thin; call module app-services)
└── main.py              # app factory, DI wiring, middleware
```

**Rules (cheap discipline that keeps the migration real):**
- A module never imports another module's internal models — only its application-service interface. (Import-linter enforces; free.)
- Cross-module effects go through the **event bus** where the North Star used events (e.g., `WorkSampleSubmitted` → intelligence reacts). In-process now; a table row logged for audit/replay.
- Every write emits an audit/event row. Every request carries tenant + actor (envelope-lite).

---

## 6. Database Schema *(initial tables only)*

One Postgres. Every table has `id`, `tenant_id`, `created_at`, `updated_at` (except append-only tables: no `updated_at`). Keep it boring.

| Table | Key columns (beyond standard) | Notes |
|---|---|---|
| `organizations` | name | one per signup = tenant |
| `users` | org_id, email, password_hash, role(recruiter/hm/admin) | tenant via org_id |
| `campaigns` | role_title, role_profile(jsonb: competencies/bar), status(draft/active/closed) | thin calibration in `role_profile` |
| `candidates` | name, email, resume_object_key | PII lives here; **AI never reads this directly** |
| `candidate_evaluations` | campaign_id, candidate_id, status(invited/submitted/evaluated/decided/…) | the workhorse; one per candidate×campaign |
| `invitations` | candidate_evaluation_id, token, expires_at, status | tokenized candidate link |
| `consents` | candidate_id, campaign_id, granted_at, scope | gate before evaluation |
| `work_samples` | candidate_evaluation_id, prompt_id, content_object_key, submitted_at | candidate's submission (immutable once submitted) |
| `evidence_items` | candidate_evaluation_id, dimension, observation, source_ref | **append-only, immutable** |
| `evaluations` | candidate_evaluation_id, dimension_scores(jsonb), overall, confidence, model_version, prompt_version | AI proposal (not a decision) |
| `recommendations` | candidate_evaluation_id, level, explanation, status(formed/delivered) | advisory; carries explanation |
| `hiring_decisions` | candidate_evaluation_id, decided_by(user), outcome(advance/hold/reject), justification, decided_at | **human**; immutable once decided |
| `feedback` | candidate_evaluation_id, content, released_by, released_at, status | recruiter-released |
| `exports` | campaign_id, object_key, created_at | results file |
| `audit_log` / `domain_events` | tenant_id, actor, action, entity_ref, payload(jsonb), occurred_at | **append-only**; the audit trail + future event stream |
| `jobs` *(if/when needed)* | type, payload, status, attempts | background AI eval reliability |

**Discipline kept:** `evidence_items`, `audit_log`, and (post-decision) `hiring_decisions` are **append-only** — enforced in code (no update/delete paths). `tenant_id` filtered on every query (a base repository helper). Optimistic concurrency (`version` column) only where concurrent edits are real (campaigns) — skip elsewhere.

---

## 7. API List *(FastAPI; REST; auto-OpenAPI)*

Grouped by module. `[R]`=recruiter/HM auth, `[C]`=candidate token, `[P]`=public.

**Auth / identity**
- `POST /auth/signup` `[P]` — create org + first user
- `POST /auth/login` `[P]` → JWT
- `GET /me` `[R]`

**Campaigns**
- `POST /campaigns` `[R]` — create (draft) + role profile
- `GET /campaigns` / `GET /campaigns/{id}` `[R]`
- `POST /campaigns/{id}/activate` `[R]` — freeze role profile, allow invites
- `GET /campaigns/{id}/results` `[R]` — ranked candidates + evidence
- `POST /campaigns/{id}/export` `[R]`

**Candidates / intake**
- `POST /campaigns/{id}/candidates` `[R]` — add one (+ optional resume upload)
- `POST /campaigns/{id}/candidates/import` `[R]` — CSV
- `GET /campaigns/{id}/candidates` `[R]`

**Invitations / candidate flow**
- `POST /candidate-evaluations/{id}/invite` `[R]` — send email
- `GET /invite/{token}` `[C]` — resolve invite (candidate landing)
- `POST /invite/{token}/consent` `[C]` — record consent (gate)
- `GET /invite/{token}/work-sample` `[C]` — fetch the task
- `POST /invite/{token}/work-sample` `[C]` — submit (triggers async AI eval)
- `GET /invite/{token}/status` `[C]` — "submitted / in review"

**Evaluation (internal-triggered; read for recruiter)**
- `GET /candidate-evaluations/{id}` `[R]` — evaluation + evidence + confidence + explanation
- `POST /candidate-evaluations/{id}/reevaluate` `[R]` — (optional) re-run

**Decision**
- `POST /candidate-evaluations/{id}/decision` `[R]` — human decides advance/hold/reject (+ justification)

**Feedback**
- `POST /candidate-evaluations/{id}/feedback/release` `[R]`
- `GET /invite/{token}/feedback` `[C]` — candidate views released feedback

**Admin / trust**
- `GET /audit` `[R:admin]` — tenant-scoped audit log

*Contract note (migration):* MVP is FastAPI-first (OpenAPI auto-generated). The North Star's contract-first codegen (ARCH-09) is deferred until there's an external/second consumer (§15).

---

## 8. AI Integration *(simplest usable — but soul intact)*

The differentiator. Kept honest, kept cheap.

**Flow (in `intelligence` module, behind `AIProvider` ACL):**
```
work sample submitted
  → [1] load work sample + campaign role_profile
  → [2] PII-MINIMIZE: strip candidate name/contact/employer from anything sent to the model (AD-89)
  → [3] build prompt (versioned, from a prompts/ file) with the role profile + minimized content
  → [4] call Claude (Sonnet for judgment) with STRUCTURED OUTPUT (tool/JSON) → proposal
  → [5] VALIDATE: Pydantic-parse; require cited evidence per dimension; reject/ retry if ungrounded (AD-90)
  → [6] CONFIDENCE: compute from evidence coverage/consistency (not the model's self-report) (AD-91 lite)
  → [7] persist evidence_items (immutable) + evaluation + recommendation + explanation; emit fact/audit
  → recruiter dashboard shows it; a HUMAN decides (never the system)
```

| Concern | MVP decision |
|---|---|
| **Provider** | Anthropic Claude via `AIProvider` interface. **Mock provider** for dev/tests (deterministic) — so dev/CI cost $0 and are reproducible. |
| **Model routing** | Sonnet for the evaluation judgment; Haiku for cheap structuring if needed. A dict in config, not a service. |
| **Prompt** | Versioned prompt files in `intelligence/prompts/` with an id/version stamped onto each evaluation (provenance-lite, AD-95). |
| **Structured output** | Claude tool-use / JSON mode → Pydantic model. No free-text judgments consumed. |
| **Grounding** | Every dimension score must cite specific observations from the work sample; ungrounded output is rejected/retried (AD-90). This is the explainability that makes a HM trust it. |
| **PII minimization** | Names/contact/employer stripped before the model call — cheap, and it's literally the bias-reduction story (Bertrand & Mullainathan). |
| **Fairness (honest)** | No statistical adverse-impact gate at MVP (needs volume). **Fairness-by-construction instead:** PII-minimized inputs + one consistent rubric applied to all + mandatory explanation + **mandatory human decision**. We *log* everything so the real gate can be computed once volume exists (§15). |
| **Cost control** | cheap-model default; **cache evaluations by content-hash** (same work sample → reuse); low max-tokens; a per-day spend cap in dev. |

> **What stays sacred:** the AI returns a *proposal* with *cited evidence* and *honest confidence*; a *human makes the decision*. That is the thesis. We are not building an auto-rejecter.

---

## 9. Authentication

- **Recruiters/HMs:** email + password (**argon2** hash), **JWT** access token (short-lived) + refresh; tenant + role resolved from the user record (tenant = org). Middleware injects tenant/actor into the request envelope (envelope-lite); every query is tenant-scoped.
- **Candidates:** no account. A **signed, expiring invite token** (in the email link) authorizes exactly their work-sample flow — minimal friction, minimal PII, least privilege (candidates see only their own).
- **Deferred (§15):** OIDC/SSO, MFA/passkeys, fine-grained RBAC, SPIFFE workload identity — none needed until enterprise customers or multiple services exist.
- **Kept even now:** tenant isolation (column + query filter), server-side authorization (never trust the client for tenant/role), no secrets in the repo.

---

## 10. Deployment

- **Local:** `docker compose up` → app + Postgres + Mailhog (fake email). One command.
- **Prod:** **Render** (or Fly.io) — a web service (the FastAPI app), the Next.js app (static/SSR on Vercel or same host), **managed Postgres** (Neon/Supabase/Render), **Cloudflare R2** for files. HTTPS provided by the platform.
- **Config/secrets:** platform env vars / secrets (Anthropic key, DB URL, JWT secret, R2 creds). Nothing in the repo. `.env.example` documents them.
- **Migrations:** Alembic runs on deploy.
- **Errors:** Sentry DSN in prod.
- **CI (lean):** GitHub Actions — lint (ruff), typecheck (mypy), tests (pytest), frontend build. No k8s, no signing, no drift-check (no generated code yet). Add rigor when it earns its keep.
- **Cost:** free tiers + Anthropic usage. Deployable for pocket change.

---

## 11. Local Development

- **Backend:** `uv sync`; `alembic upgrade head`; `uvicorn app.main:app --reload`.
- **Frontend:** `pnpm install`; `pnpm dev`.
- **One-command:** a `Makefile` (`make up` = compose up + migrate + seed; `make dev` = run both; `make seed` = synthetic org/user/campaign; `make test`).
- **Seed data:** synthetic, PII-free — one org, one recruiter, one active campaign with a couple of fake candidates and a sample work sample, so you can click through instantly.
- **AI in dev:** default to the **mock provider** (free, deterministic); flip an env flag to hit real Claude when testing the actual evaluation quality.
- **Email in dev:** Mailhog (catches invite emails locally).

---

## 12. Folder Structure

```
repo/
├── backend/
│   ├── app/               # §5 module structure
│   ├── migrations/        # alembic
│   ├── tests/             # unit + a few integration (testcontainers/pytest)
│   ├── prompts/           # versioned AI prompts
│   ├── pyproject.toml     # uv
│   └── Dockerfile
├── frontend/
│   ├── app/               # Next.js App Router (recruiter + candidate areas)
│   ├── components/        # shadcn/ui
│   ├── lib/               # api client (typed off OpenAPI)
│   └── package.json       # pnpm
├── infra/
│   ├── docker-compose.yml # app + postgres + mailhog
│   └── render.yaml        # (or fly.toml)
├── .github/workflows/ci.yml
├── Makefile
├── .env.example
└── README.md
```

*(This can live inside the existing project repo as a new top-level area, or a fresh repo — solo, a fresh clean repo is simplest. Keep the `docs/`, `arch/`, `validation/` corpus in the repo as the North Star reference.)*

---

## 13. Development Order *(what to build first, second, third…)*

Build in **thin vertical slices**, each shippable/demoable. Front-load the thesis-critical thread (§4.3).

1. **Walking skeleton (end-to-end plumbing).** Repo + compose + Postgres + FastAPI app + one migration + `/health` + structlog + envelope middleware + Next.js shell that calls the API. *Deploy it.* (Prove the pipe before filling it.)
2. **Auth + org/tenant.** Signup/login (recruiter), JWT, tenant on every request. A logged-in empty dashboard.
3. **Campaign + role profile.** Create/activate a campaign with a thin role profile. Add a candidate (manual + resume upload → ObjectStore interface, local disk).
4. **Candidate flow + consent + work sample.** Invite (email via Mailhog) → candidate landing → consent → fetch task → submit work sample (stored). No AI yet — just capture.
5. **⭐ AI evaluation (the heart — the thesis).** `intelligence` module: PII-min → mock provider first (wire the whole flow deterministically), then real Claude with structured+grounded output → evidence_items + evaluation + confidence + explanation. This is the learning core — get it working end-to-end even if rough.
6. **Recruiter dashboard.** Campaign results: candidates ranked, each expandable to evidence + confidence + explanation. **This is the demo screen** — make it clear and honest (no bare scores).
7. **Human decision.** HM reviews evidence, records advance/hold/reject + justification. Audit it. (INV-1 made real.)
8. **Audit log view + polish.** Admin sees the trail; the product's trust story is visible.
9. **Feedback (lean) + export.** Recruiter releases candidate feedback; export results.
10. **Harden + deploy for real + invite first users.** Real email (Resend), R2, Sentry, seed removed, a real work-sample task authored, error states, empty states. Ship. Invite 1–3 friendly recruiters/HMs.

> After step 5 you can already **demo the core value** to yourself and a friendly user. After step 7 you have the full thesis loop. Steps 8–10 make it real-world usable.

---

## 14. Milestones *(week-by-week, ~10–12 weeks, solo + AI pairing)*

| Week | Milestone | "Done" = |
|---|---|---|
| **1** | Walking skeleton deployed | health endpoint live in prod; CI green; compose runs locally in one command |
| **2** | Auth + tenant | recruiter signs up/logs in; empty dashboard; every query tenant-scoped |
| **3** | Campaign + candidates | create/activate campaign w/ role profile; add candidate + resume upload |
| **4** | Candidate flow + consent | invite email → landing → consent → submit work sample (stored) |
| **5–6** | ⭐ AI evaluation working | work sample → (mock then real Claude) → evidence + evaluation + confidence + explanation, persisted, PII-minimized, grounded |
| **7** | Recruiter dashboard | ranked candidates w/ evidence/confidence/explanation; the demo screen is compelling |
| **8** | Human decision + audit | HM records decision + justification; audit log captures everything |
| **9** | Feedback + export + polish | candidate feedback release; export; empty/error states; real email + R2 + Sentry |
| **10** | **Ship + first users** | deployed for real; 1–3 friendly users run a real (or realistic) evaluation end-to-end |
| **11–12** | Buffer / learning loop | fix what the first users hit; instrument the key learning questions; iterate |

*Realistic caveats:* week 5–6 (AI quality) is the riskiest and may stretch — the evaluation output being *genuinely useful* is the whole point; spend time on the prompt + rubric + grounding there. Everything else is standard CRUD and moves fast with AI pairing.

---

## 15. Future Migration *(every simplification → its re-adoption trigger)*

The migration path back to ARCH-16 is real because we kept the seams. For each simplification: **when does it become the ARCH-16 version?** — always a *trigger*, never a date.

| MVP simplification | Becomes (ARCH-16) | Trigger to migrate |
|---|---|---|
| Modular monolith | Microservices (ARCH-06) | A module needs independent scaling OR a second team owns it OR its deploy cadence must differ. Split *that* module first (its boundary already exists). |
| In-process events + `domain_events` table | Kafka backbone (ARCH-05/08) | Need durable cross-service async, replay, or a consumer outside the monolith. The table already holds the facts — point a relay at it. |
| One Postgres, shared schema (per-module tables) | Per-service DBs + event sourcing (ARCH-08) | A module's data lifecycle/scale diverges. Carve its tables out behind its app-service. |
| Docker Compose + Render | Kubernetes/EKS (ARCH-10) | Multi-node scale, real traffic, or team ops needs. Not before. |
| In-process calls | gRPC + mesh (ARCH-06/10) | Services actually separate; then mTLS/SPIFFE (ARCH-13) follows. |
| Fairness-by-construction | Statistical fairness gate (INV-3/ARCH-11) | **Evaluation volume** makes adverse-impact computable (roughly: enough candidates per role/tenant). We're already logging the data to enable it. |
| PII strip + delete-row | Crypto-shred + per-tenant keys (ARCH-08 AD-64/84) | Real PII scale + a compliance/enterprise requirement (GDPR erasure at volume). |
| Simple auth (JWT/password) | OIDC/SSO + MFA/passkeys + RBAC (ARCH-13) | First enterprise customer demands SSO, or user/role complexity grows. |
| FastAPI-first (auto OpenAPI) | Contract-first codegen (ARCH-09) | A second/external API consumer (partner integration, public API). |
| Single AI provider | Multi-provider routing (ARCH-11) | Need failover, cost arbitrage, or quality diversity. ACL already in place. |
| Structured logs + Sentry | OTel/Prometheus/Tempo/Loki (ARCH-14) | Production scale / incident volume needs distributed tracing + SLOs. |
| Local/R2 storage | S3 + lifecycle/WORM (ARCH-08/10) | Multi-node durability, audit-WORM/compliance needs. |
| Deferred moat (no memory/benchmark/outcome) | Hiring Memory / Benchmarking / Outcome Learning (ARCH-06 §14) | We have design partners sharing outcomes AND enough data to learn from. This is the flywheel — the *point*, but only after the core is validated. |

> **The migration discipline (ARCH-16):** when a trigger fires, the change is an **ADR against the frozen baseline** reviewed by whoever is the ARB-of-one (you) → then implemented. We evolve *toward* the North Star deliberately, never drift. Because the module boundaries, the audit/event table, the platform interfaces, the ACL, and `tenant_id` all already exist, each migration is a *contained* change, not a rewrite.

---

## Closing: the operating principle

Every day, ask **"what is the smallest thing that provides learning?"** and build that. The architecture corpus is the map of where we're going; MVP-01 is the cheapest honest first step. We keep the product's soul (evidence, explainability, consent, human-decides, audit, PII-minimization) because that soul *is* the thing we're testing — and we drop everything built for a scale we haven't earned. When users touch it and react, we'll have learned more than any document could tell us.

*Next: stop writing, start building — repo → skeleton → auth → campaign → candidate flow → **AI evaluation** → dashboard → decision → ship → invite users. From here, we build and iterate together.*
