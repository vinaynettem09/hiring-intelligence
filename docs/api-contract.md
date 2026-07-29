# API Contract (the front door)

A concise, hand-maintained list of externally visible endpoints — the fastest way
to see what the app exposes without reading code or the OpenAPI spec. Update it
when an endpoint changes. Error bodies are `{type, code, message, correlation_id, metadata?}`.

## Auth

### POST /auth/signup — create an organization + first admin user
- **Auth:** none
- **Request:** `{ organization_name, email, password }`
- **Response `201`:** `{ organization: {id, name}, user: {id, email, role, organization_id} }`
- **Errors:** `400 REQUEST_VALIDATION` · `400 ORGANIZATION_NAME_REQUIRED` · `409 USER_ALREADY_EXISTS`

### POST /auth/login — authenticate
- **Auth:** none
- **Request:** `{ email, password }`
- **Response `200`:** `{ access_token, refresh_token, token_type: "bearer", expires_in }`
- **Errors:** `400 REQUEST_VALIDATION` · `401 INVALID_CREDENTIALS`

### POST /auth/refresh — new access token from a refresh token
- **Auth:** the refresh token (in body)
- **Request:** `{ refresh_token }`
- **Response `200`:** `{ access_token, token_type: "bearer", expires_in }`
- **Errors:** `401 INVALID_REFRESH_TOKEN`

### POST /auth/logout — revoke a refresh token
- **Auth:** the refresh token (in body); no access token required
- **Request:** `{ refresh_token }`
- **Response `204`:** (no body). Idempotent.

## Campaigns

### POST /campaigns — create a draft evaluation campaign
- **Auth:** **required** (Bearer access token); tenant taken from the token
- **Request:** `{ role_title, role_profile: { competencies: [{ name, description? }], bar } }`
- **Response `201`:** `{ id, role_title, role_profile, status: "draft", created_at }`
- **Errors:** `400 REQUEST_VALIDATION` · `401 NOT_AUTHENTICATED`
- *A campaign is always created `draft` and owned by the caller's organization (INV-001). List/view arrives in Story 2.3.*

### POST /campaigns/{id}/activate — freeze a draft and make it active
- **Auth:** **required** (Bearer access token); tenant taken from the token
- **Request:** none (id in path)
- **Response `200`:** `{ id, role_title, role_profile, status: "active", created_at }`
- **Errors:** `401 NOT_AUTHENTICATED` · `404 CAMPAIGN_NOT_FOUND` (incl. another org's campaign) · `409 CAMPAIGN_NOT_DRAFT` (already active/concluded — no reopening) · `422 CAMPAIGN_INCOMPLETE`
- *Activation is a one-way gate: it freezes `role_profile` forever (INV-003) and can never be undone (INV-005). Point of no return — to change criteria, create a new campaign.*

### GET /campaigns — list this organization's campaigns (newest first)
- **Auth:** **required** (Bearer access token); tenant taken from the token
- **Query:** `limit` (1–100, default 20) · `offset` (≥0, default 0)
- **Response `200`:** `{ items: [{ id, role_title, status, created_at }], total, limit, offset }`
- **Errors:** `401 NOT_AUTHENTICATED`
- *List rows are lightweight **summaries** (no `role_profile`); fetch full config via the detail endpoint. Only ever the caller's own org (INV-000). `total` is this tenant's campaign count, for paging.*

### GET /campaigns/{id} — one campaign's full detail
- **Auth:** **required** (Bearer access token); tenant taken from the token
- **Response `200`:** `{ id, role_title, role_profile, status, created_at }`
- **Errors:** `401 NOT_AUTHENTICATED` · `404 CAMPAIGN_NOT_FOUND` (incl. another org's campaign — indistinguishable from missing)

## Work Sample (recruiter)

### GET /campaigns/{id}/work-sample — the current definition + coverage
- **Auth:** **required** (Bearer); tenant from token
- **Response `200`:** `{ exists, editable, campaign_id, role_title, title, introduction, tasks: [{ id, prompt, instructions, evidence_intent, task_type, competencies, display_order, expected_effort_minutes }], estimated_minutes, coverage: { total, covered, uncovered } }`
- **Errors:** `401 NOT_AUTHENTICATED` · `404 CAMPAIGN_NOT_FOUND` (incl. another org's)
- *`editable` is true only while the campaign is a draft. `coverage` shows which campaign competencies have ≥1 task.*

### PUT /campaigns/{id}/work-sample — define the whole work sample (replace)
- **Auth:** **required** (Bearer); tenant from token
- **Request:** `{ title, introduction?, tasks: [{ prompt, evidence_intent, competencies: [name], task_type?, instructions?, expected_effort_minutes? }] }`
- **Response `200`:** the `WorkSample` (same shape as GET)
- **Errors:** `400 WORK_SAMPLE_INVALID` (task missing prompt/evidence_intent, or references a competency not in the campaign) · `401 NOT_AUTHENTICATED` · `404 CAMPAIGN_NOT_FOUND` · `409 WORK_SAMPLE_LOCKED` (campaign not a draft)
- *One business operation ("define the work sample"), not per-question CRUD. Every task must map to ≥1 real campaign competency. Editable only while draft; frozen once active (INV-003). Full coverage of every competency is required to **activate** (INV-011), not to save a draft.*

## Candidates

### GET /campaigns/{id}/candidates — the campaign roster
- **Auth:** **required** (Bearer access token); tenant taken from the token
- **Query:** `limit` (1–200, default 50) · `offset` (≥0, default 0)
- **Response `200`:** `{ items: [{ evaluation_id, candidate: { id, name, email }, status, has_resume, created_at }], total, missing_resume, limit, offset }`
- **Errors:** `401 NOT_AUTHENTICATED` · `404 CAMPAIGN_NOT_FOUND` (incl. another org's)
- *Recruiter-facing (includes candidate PII — distinct from the AI's view). `missing_resume` is a "needs attention" count. Works for any campaign status.*

### POST /campaigns/{id}/candidates — add a candidate to a campaign
- **Auth:** **required** (Bearer access token); tenant taken from the token
- **Request:** `{ name, email, resume_object_key? }`
- **Response `201`:** `{ id, campaign_id, candidate: { id, name, email }, status: "invited", created_at }`
- **Errors:** `400 REQUEST_VALIDATION` · `401 NOT_AUTHENTICATED` · `404 CAMPAIGN_NOT_FOUND` (incl. another org's) · `409 CAMPAIGN_NOT_ACTIVE` · `409 CANDIDATE_ALREADY_IN_CAMPAIGN`
- *The `candidate` block is the PII identity record (reused per `(org, email)`); the response envelope is the AI-visible `CandidateEvaluation`. `resume_object_key` is a pointer to object storage, not the file.*

### POST /campaigns/{id}/candidates/import — bulk add from a CSV file
- **Auth:** **required** (Bearer access token); tenant taken from the token
- **Request:** `multipart/form-data` with `file` = a CSV. Headers (case-insensitive): `name`, `email`, `resume_object_key` (optional).
- **Response `200`:** `{ total, imported, skipped, failed, issues: [{ row, email, outcome: "skipped"|"failed", reason }] }`
- **Errors:** `401 NOT_AUTHENTICATED` · `404 CAMPAIGN_NOT_FOUND` (incl. another org's) · `409 CAMPAIGN_NOT_ACTIVE`
- *Each row is processed independently — one bad row never rejects the file. `skipped` = already in the campaign (identity reused); `failed` = row validation. Campaign must be `active` (INV-008).*

## Identity

### GET /me — canonical identity of the authenticated caller
- **Auth:** **required** (Bearer access token)
- **Request:** none
- **Response `200`:** `{ id, email, role, organization: {id, name} }`
- **Errors:** `401 NOT_AUTHENTICATED`

## Invitations

### POST /evaluations/{evaluation_id}/invitation — issue (or re-issue) a candidate invitation
- **Auth:** **required** (recruiter Bearer token); tenant taken from the token
- **Request:** none (id in path)
- **Response `201`:** `{ id, candidate: { id, name, email }, expires_at, created_at, replaced_previous }`
- **Errors:** `401 NOT_AUTHENTICATED` · `404 EVALUATION_NOT_FOUND` (incl. another org's) · `409 CAMPAIGN_NOT_ACTIVE`
- *Sends a magic-link email to the candidate. The raw token is **never** in the response — only in the email. Re-issuing revokes the previous active link (`replaced_previous: true`).*

### POST /candidate/invitation — resolve a magic-link token (candidate; no account)
- **Auth:** none — **possession of the opaque token is the authorization** (separate trust boundary from recruiter JWTs). Token in the body, never the URL.
- **Request:** `{ token }`
- **Response `200`:** `{ candidate_name, organization_name, role_title, next_step: "consent", expires_at }`
- **Errors:** `404 INVITATION_INVALID` · `404 INVITATION_EXPIRED` · `404 INVITATION_REVOKED`
- *Fails safe: an unusable link leaks nothing about candidate/campaign existence. Grants access to exactly one CandidateEvaluation — never another candidate, evaluation, tenant, or recruiter API. First access is recorded (audit).*

## Consent (candidate; magic-link)

### POST /candidate/consent — disclosure + current consent state
- **Auth:** none — the token (body) resolves the evaluation + tenant server-side; the client never sends an evaluation/organization id.
- **Request:** `{ token }`
- **Response `200`:** `{ organization_name, role_title, candidate_name, disclosure: { version, sections: [{ key, title, body }] }, consented, next_step: "work_sample" }`
- **Errors:** `404 INVITATION_INVALID|EXPIRED|REVOKED`

### POST /candidate/consent/grant — grant consent for the token's evaluation
- **Auth:** none (same token model)
- **Request:** `{ token }`
- **Response `200`:** same `ConsentState` shape, with `consented: true`
- **Errors:** `404 INVITATION_INVALID|EXPIRED|REVOKED`
- *Consent is an **append-only versioned fact**, not a boolean. Idempotent for the same active version (returns the existing grant — no duplicate, no mutation). The exact `disclosure.version` agreed to is recorded, with an audit event. Cross-evaluation / cross-tenant consent is structurally impossible.*

## Candidate Work Sample (candidate; magic-link)

### POST /candidate/work-sample — load the frozen work sample + own drafts
- **Auth:** none — the token (body) resolves the evaluation/tenant server-side. Re-checks all three gates every call.
- **Request:** `{ token }`
- **Response `200`:** `{ organization_name, role_title, title, introduction, estimated_minutes, tasks: [{ task_id, order, prompt, instructions, expected_effort_minutes, response_text }] }`
- **Errors:** `403 CONSENT_REQUIRED` · `404 INVITATION_INVALID|EXPIRED|REVOKED` · `409 WORK_SAMPLE_UNAVAILABLE`
- *Candidate-safe DTO — **no** evidence_intent, competency mappings, hiring bar, or internal config.*

### POST /candidate/work-sample/response — save (upsert) a draft response
- **Auth:** none (same token model)
- **Request:** `{ token, task_id, response_text }` (`response_text` ≤ 20000 chars)
- **Response `200`:** `{ task_id, updated_at }`
- **Errors:** `400 REQUEST_VALIDATION` (size) · `403 CONSENT_REQUIRED` · `404 INVITATION_* | TASK_NOT_FOUND` · `409 WORK_SAMPLE_UNAVAILABLE | WORK_SAMPLE_ALREADY_SUBMITTED`
- *Mutable **draft** working state — not Evidence. Upserts (one row per task); the server verifies the task belongs to this evaluation's frozen work sample. Locked once submitted. Autosaves are not audited; `work_sample.started` is recorded once.*

### POST /candidate/work-sample/submit — final submission → immutable Evidence
- **Auth:** none (same token model). **Request:** `{ token }` only — the server owns the drafts and frozen tasks.
- **Response `200`:** `{ organization_name, role_title, submitted_at, evidence_count }`
- **Errors:** `403 CONSENT_REQUIRED` · `404 INVITATION_*` · `409 WORK_SAMPLE_UNAVAILABLE` · `422 WORK_SAMPLE_INCOMPLETE` (metadata `{ total_tasks, answered_tasks, missing_task_positions }`)
- *The authoritative, **atomic** transition: re-checks access + consent + completeness, snapshots each draft into immutable **Evidence** (append-only, PII-free), marks the evaluation `submitted`, audits `work_sample.submitted`. **Idempotent** — a second call returns the existing result (no duplicate Evidence/audit). Irreversible. No AI runs here.*

## Evaluations (Epic 5 — AI proposes, human decides)

*An `Evaluation` is an immutable, evidence-grounded **proposal**, never a `HiringDecision`. `confidence` is a platform-computed evidence-**reliability** signal in `[0,1]`, not a probability of success. The provider is config-driven (`AI_PROVIDER=mock|anthropic`); `mock` is the default and the only provider used in tests/CI. The HTTP contract is identical regardless of provider — a real-provider failure maps to the same `502` reasons. Execution owns its own transaction boundary (no DB transaction is held during the provider call, TD-011).*

### POST /evaluations/{candidate_evaluation_id}/evaluate — run (or return) the evaluation
- **Auth:** **required** (Bearer). Roles: admin · recruiter · hiring_manager. Tenant from token. Optional header **`Idempotency-Key`** guards a double-click.
- **Request:** none (id in the path; tenant/authority server-derived).
- **Response `200`:** an `EvaluationDetail` — `{ id, candidate_evaluation_id, run_number, recommendation (STRONG_PROCEED|PROCEED|MIXED|DO_NOT_PROCEED|ESCALATE), confidence, confidence_rationale, escalation_reason?, competency_assessments:[{ competency, assessment, provider_signal?, citations:[{ evidence_id, task_id }] }], strengths[], concerns[], evidence_coverage:{ competencies_total, competencies_assessed, tasks_total, tasks_with_evidence }, provenance:{ provider, model, model_version, prompt_version, input_schema_version, output_schema_version, confidence_algorithm_version, generated_at }, input_fingerprint, created_at }`
- **Errors:** `401 NOT_AUTHENTICATED` · `403 CONSENT_REQUIRED` · `403 EVALUATION_FORBIDDEN` · `404 CANDIDATE_EVALUATION_NOT_FOUND` (also cross-tenant) · `422 EVALUATION_NOT_SUBMITTED` · `409 EVALUATION_RUN_CONFLICT` (concurrent-run backstop) · `502 <failure reason>` (`PROVIDER_UNAVAILABLE` | `INVALID_PROVIDER_OUTPUT` | `UNGROUNDED_OUTPUT` | `POLICY_VIOLATION` — a system condition, **not** a candidate judgment; nothing is persisted)
- ***Idempotent:*** returns the existing run if one exists (or the same run for a repeated `Idempotency-Key`) — it never creates a second run. Re-checks consent immediately before persistence. Emits one `evaluation.generated` audit fact on success.

### POST /evaluations/{candidate_evaluation_id}/rerun — deliberate new run
- **Auth:** required (same roles/tenant). **Request:** none.
- **Response `201`:** an `EvaluationDetail` for the new run (`run_number` = previous + 1).
- **Errors:** same set as `evaluate`. *Always creates a new immutable run; never mutates a prior run.*

### GET /evaluations/{candidate_evaluation_id} — latest + history
- **Auth:** required (same roles/tenant).
- **Response `200`:** `{ candidate_evaluation_id, run_count, latest: EvaluationDetail | null, runs:[{ id, run_number, recommendation, confidence, model, prompt_version, created_at }] }` (`latest` is `null` before any run; `runs` newest-first).
- **Errors:** `401 NOT_AUTHENTICATED` · `404 CANDIDATE_EVALUATION_NOT_FOUND` (also cross-tenant).

### GET /evaluations/{candidate_evaluation_id}/evidence — submitted evidence behind the citations (Story 5.4B)
- **Auth:** required (same roles/tenant). Recruiter-facing source view — the claim → citation → source trust anchor.
- **Response `200`:** `{ candidate_evaluation_id, items:[{ evidence_id, task_id, task_number, task_prompt, evidence_intent, response_text, captured_at }] }` (ordered by task position; `evidence_id`/`task_id` match the evaluation's citation ids). Verbatim submitted responses — NOT the AI's PII-minimized input, never raw provider output.
- **Errors:** `401 NOT_AUTHENTICATED` · `404 CANDIDATE_EVALUATION_NOT_FOUND` (also cross-tenant).

> **Roster enrichment (Story 5.4B):** `GET /campaigns/{id}/candidates` `RosterEntry` rows now also carry `has_evaluation`, `latest_recommendation` (string | null), and `latest_run_number` (int | null) so the roster can show a contextual *Generate* vs. *View* action + a glanceable recommendation without N+1 reads.

## Human decisions (Story 6.2)

### POST /evaluations/{candidate_evaluation_id}/decisions — record the accountable human decision
- **Auth:** **required** (Bearer). Roles: admin · recruiter · hiring_manager. Tenant + actor from the token.
- **Request:** `{ decision: "ADVANCE" | "HOLD" | "DECLINE", rationale?: string, evaluation_id?: string }`. `evaluation_id` (optional) is the AI run the recruiter decided against — validated to belong to this candidate evaluation; a decision **can** be recorded without one (AI is advisory, never a gate).
- **Response `201`:** `{ id, decision, rationale | null, decided_by_email, decided_at, informed_by_run_number | null, created_at }`.
- **Append-only:** a change of mind is a NEW decision; nothing is overwritten. The referenced Evaluation is **never** mutated. The decision is a human act — no AI path writes it.
- **Errors:** `401 NOT_AUTHENTICATED` · `403 DECISION_FORBIDDEN` · `404 CANDIDATE_EVALUATION_NOT_FOUND` (also cross-tenant) · `404 EVALUATION_NOT_FOUND` (bad/foreign `evaluation_id`).

### GET /evaluations/{candidate_evaluation_id}/decisions — latest + full decision history
- **Auth:** required (same roles/tenant).
- **Response `200`:** `{ candidate_evaluation_id, latest: DecisionView | null, decisions: [DecisionView] }` (newest first; `latest` null before any decision).
- **Errors:** `401 NOT_AUTHENTICATED` · `403 DECISION_FORBIDDEN` · `404 CANDIDATE_EVALUATION_NOT_FOUND`.

> **Review-queue enrichment (Story 6.2):** `GET /review-queue` items now also carry `decision` (`ADVANCE`/`HOLD`/`DECLINE` | null) — the latest human decision as a badge. It does **not** change a row's `stage` or ordering (badge only).

## Audit trail (Story 6.3)

### GET /evaluations/{candidate_evaluation_id}/timeline — the hiring-process audit trail
- **Auth:** required (same roles/tenant). A pure read — assembled from authoritative append-only records (invitations, consent, submission, evaluation runs, decisions); **no new business logic or state**.
- **Response `200`:** `{ candidate_evaluation_id, candidate_name, candidate_email, role_title, entries: [{ kind, at, actor_type, actor | null, summary }] }` — `entries` chronological (oldest first). `kind` ∈ `INVITATION_SENT` · `INVITATION_OPENED` · `CONSENT_GRANTED` · `CONSENT_WITHDRAWN` · `WORK_SAMPLE_SUBMITTED` · `EVALUATION_GENERATED` · `DECISION_RECORDED`. Summaries are factual + PII-minimal (a decision rationale is noted as present, never inlined). Tenant-scoped.
- **Errors:** `401 NOT_AUTHENTICATED` · `404 CANDIDATE_EVALUATION_NOT_FOUND` (also cross-tenant).
- *Frontend offers a **convenience** CSV export of this trail (client-side, from the server-authoritative data) — for recruiter review/sharing, **NOT a compliance-grade audit artifact**. A server-generated, immutable/signed export can be added during hardening (Epic 10) if the product requires one. (Route hangs off `/evaluations` for consistency — see TD-018.)*

## Dashboard

### GET /dashboard — the authenticated tenant's home read model
- **Auth:** **required** (Bearer access token); tenant taken from the token
- **Response `200`:** `{ metrics: { total_campaigns, active_campaigns, draft_campaigns, total_candidates, candidates_missing_resume }, attention: { draft_campaigns, active_campaigns_without_candidates, candidates_missing_resume }, recent_campaigns: [{ id, role_title, status, created_at }], recent_candidates: [{ evaluation_id, name, email, campaign_id, campaign_role_title, created_at }] }`
- **Errors:** `401 NOT_AUTHENTICATED`
- *A purpose-built read model — the frontend does not assemble metrics from many calls. Every field is real (no AI/velocity/confidence). All counts are tenant-scoped.*

## Review queue

### GET /review-queue — the recruiter's operational inbox for evaluation work (Story 6.1)
- **Auth:** **required** (Bearer access token); tenant taken from the token.
- **Query:** `filter` (`all` | `needs_attention` | `ready` | `waiting` | `completed`, default `all`) · `campaign_id` · `search` (candidate name, server-side) · `limit` (1–50, default 20) · `offset` (≥0).
- **Response `200`:** `{ items: [{ candidate_evaluation_id, candidate_name, candidate_email, campaign_id, role_title, stage, needs_attention, recommendation | null, confidence | null, run_number | null, last_activity_at }], summary: { needs_review, ready_to_evaluate, awaiting_invitation, waiting_on_candidate, completed, total }, total, limit, offset }`.
- `stage` ∈ `AWAITING_INVITATION` · `AWAITING_CANDIDATE` · `READY_FOR_EVALUATION` · `NEEDS_REVIEW` · `EVALUATED` — **derived** in SQL from CandidateEvaluation status + submission, latest Evaluation run, and Invitation existence (never a stored/mutable workflow column). Ordered attention-first, deterministic. `summary` reflects the whole tenant queue (independent of `filter`/`search`); `total` matches the current filter/search. `recommendation`/`confidence` are raw — the frontend maps them via `components/ai/presentation.ts`. No model/provider/token data. All rows + counts tenant-scoped (another org's items never appear).
- **Errors:** `401 NOT_AUTHENTICATED`.

## System

### GET /health — structured health
- **Auth:** none
- **Response `200`:** `{ status: "healthy"|"degraded", checks: { application, database }, version }`

---
*JWT access tokens carry only `sub, organization_id, role, jti, iat, exp`. Tenant
context is derived server-side from the verified token — never from headers/query/body.*
