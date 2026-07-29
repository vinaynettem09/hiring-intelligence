# Deployment Runbook — Story 9.1 (Production Deployment Foundation)

Goal: one **public, invite-only MVP** where the full lifecycle works —
recruiter signup → campaign → work sample → activate → invite a real email → candidate magic
link → consent → work sample → submit → AI evaluates immutable Evidence → recruiter sees
recommendation + confidence + citations → human decision → timeline.

> Status legend: ✅ done in-repo · ⏳ needs founder action (account/secret) · 🔒 stop-for-money

## 1. Architecture (simplest credible; free-tier, no card required)

| Component | Choice | Open-source app? | Hosted service? | Free? | Card? |
|---|---|---|---|---|---|
| Frontend (Next.js) | **Vercel** (Hobby) | app code is ours/OSS frameworks | yes (Vercel) | ✅ | ❌ |
| Backend (FastAPI) | **Render** (Docker web service, Free) | app code is ours/OSS | yes (Render) | ✅ | ❌ |
| Database (PostgreSQL) | **Neon** (Free) | Postgres is OSS | yes (Neon) | ✅ | ❌ |
| Email (SMTP) | **Brevo** (Free 300/day) | — | yes (Brevo) | ✅ | ❌ |
| AI | **Gemini** (Google AI Studio key) | — | yes (Google) | ✅* | ❌* |

\* Gemini free tier is free/no-card **but may train on submitted data** — see §9. We deploy on
the **mock** provider first; you switch to Gemini deliberately.

**Open-source vs hosted (be precise):** our application and its frameworks (FastAPI, Next.js,
SQLAlchemy, PostgreSQL engine) are open source. **Hosting is not** — Vercel/Render/Neon/Brevo
are commercial services offering free tiers. "Free tier" ≠ "open-source hosting."

No Kubernetes/Terraform/ECS/Redis/queues/multi-env — the app doesn't need them for an MVP.

## 2. What's ✅ done in this branch (`deploy/9.1-production-deployment`)
- **Migrations run on container start** — `docker-entrypoint.sh` runs `alembic upgrade head`
  (idempotent, additive, never drops data) then starts the app; a failed migration aborts the
  boot so a bad deploy fails visibly. `migrations/` + `alembic.ini` are now baked into the image.
- **Real SMTP** — `SmtpEmailProvider` now supports STARTTLS + SMTP AUTH (username/password),
  behind the existing seam; Mailhog still works with no auth (local). Password is read from
  env only, never logged.
- **`$PORT` binding** — image CMD honors Render's `$PORT` (defaults 8000 locally).
- **`render.yaml`** blueprint (backend) + **`.env.production.example`** (env template, no secrets).

## 3. Environment-variable matrix (no real values printed)

| Variable | Component | Secret? | Purpose | Source |
|---|---|---|---|---|
| `APP_ENV` | backend | no | marks prod | `production` |
| `DATABASE_URL` | backend | **yes** | Postgres (asyncpg + `sslmode=require`) | Neon dashboard |
| `JWT_SECRET` | backend | **yes** | signs recruiter access tokens (TD-005) | `openssl rand -hex 32` |
| `FRONTEND_BASE_URL` | backend | no | builds candidate magic-link URLs | the Vercel URL |
| `EMAIL_FROM` | backend | no | invitation sender | your address |
| `SMTP_HOST`/`SMTP_PORT` | backend | no | SMTP endpoint | Brevo |
| `SMTP_USERNAME`/`SMTP_PASSWORD` | backend | **yes** | SMTP AUTH | Brevo SMTP keys |
| `SMTP_USE_TLS` | backend | no | STARTTLS on | `true` |
| `AI_PROVIDER` | backend | no | `mock` \| `gemini` | you decide (§9) |
| `GEMINI_API_KEY` | backend | **yes** | Gemini access (only if `gemini`) | Google AI Studio |
| `BACKEND_URL` | frontend (build) | no | `/api/*` proxy target | the Render URL |

Secret model: secrets live **only** in Render/Vercel dashboards (and Neon/Brevo/Google). Never
in git, the Docker image, or Next.js bundles. `GEMINI_API_KEY` is server-side only — the
frontend never sees it (all AI calls are backend-side via the governed provider path).

## 4. Founder action required (⏳ / 🔒) — do these to go live
1. ⏳ **Neon**: create a free project → copy the connection string → prepend `+asyncpg` and
   ensure `sslmode=require` → this is `DATABASE_URL`.
2. ⏳ **Render**: New → Blueprint → connect the `HiringIntelligence/hiring-intelligence` repo
   (Render reads `render.yaml`). Set the `sync: false` secrets in the dashboard. Deploy.
3. ⏳ **Vercel**: New Project → import the repo → **Root Directory = `frontend`** → add env
   `BACKEND_URL = https://<your-backend>.onrender.com` → deploy. Copy the resulting URL into
   the backend's `FRONTEND_BASE_URL`, then redeploy the backend.
4. ⏳ **Brevo**: create account → SMTP & API → generate an SMTP key → fill `SMTP_*`.
5. 🔒/⏳ **AI decision (§9)** — keep `mock` to start (nothing to buy), or set Gemini.
6. Nothing here requires a credit card or a purchased domain. Provider subdomains
   (`*.vercel.app`, `*.onrender.com`) are sufficient. **Stop and ask me** if any provider
   prompts for a card — a free path exists for every component above.

## 5. Database & migrations
PostgreSQL only (no SQLite in prod — CI already proves PG-specific behavior). Migrations apply
automatically on backend start (§2), to the **single expected Alembic head**. A failed
migration aborts startup (visible failure). `alembic upgrade head` is additive — it never
drops/recreates data. Backups: Neon keeps point-in-time history on its free tier; still, treat
real submissions as precious (§8 risk).

## 6. Frontend ↔ backend connectivity / CORS
The browser talks **only to the frontend origin**; Next.js proxies `/api/*` to `BACKEND_URL`
server-side (`next.config.mjs` rewrite). So there is **no browser→backend cross-origin call and
no CORS to configure** — and we deliberately do **not** open `Access-Control-Allow-Origin: *`.
Candidate magic links use `FRONTEND_BASE_URL`, so they always land on the deployed frontend.

## 7. Authentication / security findings
- **TD-006 (recruiter access token in `localStorage`)**: acceptable for a **small invite-only**
  MVP — there is no `dangerouslySetInnerHTML` and no known XSS (verified in 7.4). It is **not a
  hard blocker** for friends-and-family, but it **must be revisited in Epic 10 before any public
  / broader exposure**. Not redesigned here (out of 9.1 scope).
- **Candidate magic links**: unchanged — only the token *hash* is stored, raw tokens are never
  logged/audited, links carry the token in the path to a single evaluation. Preserved.
- **JWT_SECRET** must be a strong random value in prod (TD-005) — set via env, never the dev default.

## 8. Friends-and-family readiness checklist (for when you invite 5–10 people)
- **Recruiter URL you share:** `https://<your-app>.vercel.app` (they sign up there).
- **What candidates receive:** an email from `EMAIL_FROM` with a magic link to
  `https://<your-app>.vercel.app/invite/<token>` — no account needed.
- **Email:** sent via Brevo SMTP; check Brevo's dashboard for delivery/bounces. Ask friends to
  check spam the first time.
- **Which AI is active:** whatever `AI_PROVIDER` is set to — the evaluation UI shows a **"mock"
  banner** when it's the mock, so you'll never mistake mock output for real judgment.
- **Where you inspect failures:** Render → Logs (backend), Vercel → Logs (frontend), Neon →
  Monitoring (DB). Logs are structured and PII-minimized (no Evidence text, tokens, prompts,
  or rationale — §12).
- **DB health:** backend `/health` returns `{"checks":{"database":"healthy"}}`; Neon shows the
  connection/monitoring.
- **If the app goes down:** Render free sleeps — the first request wakes it (~50s). If a deploy
  is bad, use **Rollback** (§11).
- **Avoid losing submissions:** don't run destructive DB ops; migrations are additive only; keep
  Neon's history; take a manual Neon snapshot before any risky change.

## 9. Gemini (AI) configuration
Production uses the governed provider path (backend-only key, no fallback to mock, provenance
records provider/model/prompt/confidence versions — unchanged; **no prompt/confidence tuning in
9.1**). The one real decision: the **free tier may use submissions to improve Google's
products** (TD-017). Options: (a) deploy on **mock** first (labelled; zero data egress);
(b) **Gemini free + explicit candidate/friend consent**; (c) **Gemini paid** (no training on
data, needs billing 🔒). Recommendation: ship on mock, prove the whole flow, then switch.

## 10. CI/CD → deployment path
Existing GitHub Actions stays authoritative. **Do not deploy a red commit.** Because branch
protection needs a paid plan (deferred), the discipline is manual: merge to `main` only on green,
and Render is set `autoDeploy: false` so you click **Deploy** after confirming the green run.
(If you later want auto-deploy-on-green, we can add a deploy workflow gated on the CI job.)

## 11. Rollback
- **Backend/Frontend:** Render and Vercel both keep previous deploys — use **Rollback** to the
  last green deploy in their dashboards (instant).
- **Database:** migrations are additive; if a migration is bad, fix-forward with a new migration.
  Restore from a Neon snapshot only as a last resort (may lose recent submissions).

## 12. Logging / diagnostics
Structured logs (structlog) with correlation IDs. Sensitive payloads — Evidence text, raw AI
prompts/responses, consent content, invitation tokens, decision rationale — are **not** written
to normal logs/audit metadata. Platform logs (Render/Vercel/Neon) are enough for 9.1; no
observability stack introduced.

## 13. Smoke test (run after deploy; synthetic data only)
Use throwaway identities/answers — never real candidate data to test infra. Steps:
`/health` 200 → recruiter signup/login → create campaign → define work sample → activate →
add candidate (a test email you control) → invite → open the magic link → consent → answer →
submit → (evaluate) → recruiter sees recommendation/confidence/citations → record decision →
timeline shows the lifecycle. Record each step as **auto-verified / manually-verified /
blocked**.

## 14. Costs, limits, risks
- **Recurring cost now: $0.** Future paid upgrades (optional): Render Starter ~$7/mo (no
  sleep), Gemini paid (usage-based), a domain (~$10-15/yr) — none required for F&F.
- **Free-tier limits:** Render backend **sleeps** (~50s cold start); Brevo 300 emails/day;
  Neon free storage/compute caps (ample for MVP); Vercel Hobby is non-commercial.
- **Risks:** cold-start latency on candidate link clicks; Gemini free-tier data retention;
  TD-006 token storage before broader exposure; single free DB (snapshot before risky changes).

## 15. Technical debt
- Resolved-for-deploy: migrations-in-image, SMTP auth. 
- Still open: TD-001/002 (root, single-stage image — Epic 10 hardening), TD-005 (set real
  JWT secret via env — do at deploy), TD-006 (localStorage token — Epic 10), TD-017 (Gemini
  free-tier retention). None block a careful invite-only MVP except the AI decision (§9).

## 16. Remaining blockers before inviting 5–10 users
1. Founder creates the four accounts + sets secrets (§4).
2. AI decision (§9).
3. First green **live** smoke test (§13) executed against the real URLs.
Until the live environment exists, the deploy itself is **blocked pending founder action** —
everything code-side is ready and CI-verified.
