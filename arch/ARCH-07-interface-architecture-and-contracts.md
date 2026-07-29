# ARCH-07 — Interface Architecture & Contracts

| Field | Value |
|---|---|
| **Document ID** | ARCH-07 |
| **Title** | Interface Architecture & Contracts (the constitutional contract layer) |
| **Owner** | Principal Software Architect + Enterprise API Architect + Distributed Systems Architect + DDD lead |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture |
| **Depends on** | ARCH-06 (services), ARCH-05 (facts), ARCH-04 (interactions), ARCH-03 (aggregates), ARCH-02 (capabilities), ARCH-01 (context) |
| **Blocks** | ARCH-08 (Database Architecture), ARCH-09 (API/Protobuf/AsyncAPI Specifications), ARCH-10 (Deployment) |
| **The one question** | **"How do independently owned services communicate without violating the business architecture?"** |
| **This document IS** | The architectural **contract model** — commands, queries, event contracts, error model, governance, security envelope, and the external-integration (ACL) architecture. |
| **This document is NOT** | OpenAPI · Protobuf · JSON Schema · GraphQL · endpoint lists · URLs · HTTP verbs · code. **Those are ARCH-09.** |
| **ABSOLUTELY FORBIDDEN** | REST endpoints · URLs · HTTP verbs · gRPC/protobuf · JSON schemas · OpenAPI · GraphQL · Kafka topics · RabbitMQ · DB tables · SQL · ORM · languages · frameworks · infra/cloud specifics. |

---

## 0. Interface Philosophy

### 0.1 Why interfaces exist
A service is only as trustworthy as its boundary. An interface is the **promise** a service makes about what it will accept, what it guarantees in return, and what facts it will assert — *without exposing how it works inside*. Interfaces exist so that thirteen independently-owned services (ARCH-06) can collaborate through the **legal interactions** of ARCH-04 while each remains free to change its internals, its storage (ARCH-08), and eventually its transport, without breaking anyone.

### 0.2 Why contracts outlive implementations
Implementations are rewritten; contracts are inherited. A contract expressed in **business terms** (DOC-04 vocabulary) — "record a Hiring Decision," "a Recommendation was Delivered" — remains valid whether the transport is gRPC today, something else in five years, or a monolithic in-process call under AD-41's co-deployment. The contract is the stable asset; the transport is disposable. This is the same principle that made ARCH-03/04/05 survive re-platforming, now applied at the wire between services.

### 0.3 Why interfaces protect service boundaries
The forbidden interactions of ARCH-04 §2 (Recommendation ✗→ Candidate; Audit ✗→ initiate; cross-tenant ✗) are only real if **no contract exists to express them**. An interface catalog is therefore also a *prohibition* catalog: a conversation with no contract cannot happen. Interfaces are how the choreography of ARCH-04 becomes enforceable at runtime.

### 0.4 The five contract kinds (and why each is distinct)
| Kind | Asserts / does | Direction of truth | Derives from |
|---|---|---|---|
| **Command** | A request to *change state* / perform a business action; may be accepted or refused. | Caller → owning service | ARCH-04 §4 (Initiator/Validator/Responder) |
| **Query** | A request to *read* a business view; never changes state. | Consumer → owner | ARCH-04 §5 (read dependencies) |
| **Business Event** | A statement that *something became true* (immutable fact). | Owner → the world | ARCH-05 (facts) |
| **File Contract** | A bulk import/export of business data across a boundary. | Across the product boundary | AD-11 (CSV/resume in); KD-12.7 (export out) |
| **Administrative Contract** | Operational/governance actions (provision tenant, grant access, query audit) distinct from hiring work. | Admin → platform | ARCH-06 Identity/Audit |

They are distinct because they have **different truth semantics**: a command *might not happen* (it can be refused); a query *reads what is*; an event *already happened and is permanent*; a file contract *crosses the boundary in bulk*; an administrative contract *governs the platform, not the hiring*. Conflating them (e.g., modeling a fact as a command, or a bulk import as a stream of commands) is the classic error that breaks idempotency and audit.

### 0.5 Why transport is separate from contract
A contract says *what* is promised; a transport says *how bytes move*. `RecordHiringDecision` is one contract; whether it arrives via an internal RPC, an edge request, or an in-process call is a transport decision (ARCH-06 §4) that must be swappable without renegotiating the promise. **We bind meaning to the contract, never to the transport.**

> ### AD-51 — Interfaces are business contracts; transport mechanisms are implementation details.
> Every interface is defined in canonical business terms (DOC-04) as a Command, Query, Business Event, File, or Administrative contract with explicit pre/post-conditions and produced facts. The transport (RPC, edge protocol, message log, in-process call) is chosen separately (ARCH-06/ARCH-09) and MUST be replaceable without changing any contract's meaning. **A contract that cannot be honored over a different transport is mis-specified.**

---

## 1. Communication Taxonomy

Every interaction in the platform is exactly one of the following. (Purpose · Owner · Consumer · Lifecycle.)

| Class | Purpose | Owner | Consumer | Lifecycle |
|---|---|---|---|---|
| **Command** | Perform/refuse a business action | The service owning the target aggregate | An authorized caller (user via edge, or a service) | Request → validate → accept/refuse → emit fact(s) |
| **Query** | Read a business view; no state change | The owning service | Authorized reader | Request → authorize → project → return (may be cached) |
| **Business Event** | Publish an immutable fact | The aggregate owner | Any authorized subscriber (within tenant) | Emitted once → durable → replayable → never mutated |
| **Administrative Operation** | Govern the platform (provision, access, audit read) | Identity / Audit | Admins / governance | Request → authorize → apply/record |
| **Bulk Import** | Bring many candidates in at once (CSV + resume, AD-11) | Candidate | Recruiter | Upload → validate → per-row outcome → facts |
| **Bulk Export** | Deliver intelligence back across the boundary (KD-12.7) | Export | Recruiter/customer | Assemble → deliver → status |
| **Streaming** | Progressive delivery of a long computation's partial results (e.g., evaluation progress) | Evaluation / Intelligence Compute | Recruiter UI | Subscribe → incremental updates → completion |
| **Long-running Operation** | A business action that cannot complete synchronously | The orchestrating service | Initiator | Accept → in-progress (poll/subscribe) → async completion |
| **Notification** | Communicate at a meaningful moment (Silence philosophy, DOC-06) | Notification | Candidate / users | Triggered by a fact → sent → delivery receipt |

> **Capability invocation is *not* on this list — deliberately.** Calls to **Intelligence Compute** (ARCH-06 §2.5) are *computations*, not domain interactions: they change no aggregate and assert no fact. They are governed as a special class in §2.4, not as commands. This preserves ARCH-05 AD-35 (the AI never emits an authoritative fact).

---

## 2. Command Catalog

*Each command: Purpose · Owning Service · Caller · Business Preconditions · Business Validation · Success Result · Failure Result · Business Facts Produced · Idempotency · Authorization · Expected Latency. No transport.* Every command traces to an ARCH-04 §4 action (A#).

### 2.1 Administrative & Access commands *(Identity Service)*

**ProvisionOrganization** — *Purpose:* create a tenant. *Caller:* Platform Admin. *Preconditions:* none. *Validation:* org identity unique. *Success:* tenant exists. *Failure:* duplicate/invalid. *Facts:* `OrganizationProvisioned`. *Idempotency:* by org identity key. *Authorization:* platform-admin. *Latency:* interactive.

**GrantUserAccess / RevokeUserAccess** — *Caller:* Org Admin. *Preconditions:* `OrganizationProvisioned`. *Validation:* permissions within tenant scope. *Success:* user may/may-not act. *Facts:* `UserAccessGranted/Revoked`. *Idempotency:* by (user, permission-set) key. *Authorization:* org-admin. *Latency:* interactive.

### 2.2 Campaign commands *(Campaign Service)*

**CreateCampaign** (A1) — *Preconditions:* `OrganizationProvisioned`; Role Reference present. *Validation:* tenant scope; role ref resolvable. *Success:* Campaign in Draft. *Failure:* invalid role ref / unauthorized tenant. *Facts:* `CampaignCreated`. *Idempotency:* by client-supplied campaign key. *Authorization:* Recruiter. *Latency:* interactive.

**SetCalibration** (A3) — *Preconditions:* Campaign in Draft. *Validation:* calibration adjusts the *bar*, never a *gate* (Customization Pyramid; INV-c). *Success:* calibration set (mutable while Draft). *Facts:* none (internal state until Active). *Idempotency:* last-writer within Draft. *Authorization:* Recruiter/HM. *Latency:* interactive.

**ActivateCampaign** (A3) — *Preconditions:* Campaign in Draft; calibration set; roster established. *Validation:* calibration present. *Success:* Campaign Active; **calibration frozen** (INV-c). *Failure:* missing calibration/roster. *Facts:* `CampaignActivated`. *Idempotency:* state-guarded (Draft→Active once). *Authorization:* Recruiter. *Latency:* interactive.

**ConcludeCampaign** — *Preconditions:* `FairnessApproved`; deliveries accounted. *Validation:* fairness passed; no in-flight blocking work. *Success:* Concluded; evidence now permanently historical (AD-09). *Facts:* `CampaignConcluded`. *Idempotency:* state-guarded. *Authorization:* Recruiter. *Latency:* interactive.

**CancelCampaign** *(compensation)* — *Preconditions:* not Concluded. *Validation:* cancellable state. *Success:* Cancelled; in-flight evaluations withdrawn; candidates informed (Recovery Moment). *Facts:* `CampaignCancelled`. *Idempotency:* state-guarded. *Authorization:* Recruiter. *Latency:* interactive.

### 2.3 Candidate, Consent, Evaluation, Trust, Decision, Feedback, Export commands

| Command (A#) | Owner | Caller | Key preconditions | Key validation (may refuse) | Facts produced | Idempotency | Authz | Latency |
|---|---|---|---|---|---|---|---|---|
| **ImportCandidates** (A2) | Candidate | Recruiter | `CampaignCreated`; consent posture | file well-formed; per-row validity; **consent precondition** | `CandidateImported`×n | per-file + per-row key | Recruiter | async (bulk) |
| **RequestConsent** | Consent | Candidate/Consent | `CandidateImported` | scope + retention stated | `ConsentRequested` | by (candidate, campaign) | system | interactive |
| **RecordConsentGrant** (A15) | Consent | **Candidate** | `ConsentRequested` | candidate is the sole grantor | `ConsentGranted` | by consent id | candidate | interactive |
| **WithdrawConsent** *(comp.)* | Consent | **Candidate** | `ConsentGranted` | — | `ConsentWithdrawn` | by consent id | candidate | interactive |
| **InviteCandidate** (A4) | Evaluation | Campaign | `CampaignActivated` ∧ `CandidateImported` ∧ **`ConsentGranted`** | consent active; honest AI disclosure attached | `CandidateInvited` | by (candidate, campaign) | Recruiter/system | async |
| **SubmitWorkSample** (A5) | Evaluation | **Candidate** | invitation Accepted; **consent active** | one submission per campaign (unless restarted); consent gate | `WorkSampleSubmitted` | by (candidate-evaluation, attempt) | candidate | interactive→async |
| **VerifyIntegrity** (A7) | Integrity | Evaluation | `EvidenceRecorded` | authoritative; low integrity flags, never silently passes | `IntegrityVerified` (`IntegrityFlagged`?—OQ) | by evidence-item set | service | async |
| **AssessFairness** (A9) | Fairness | Campaign | sufficient `EvaluationCompleted` across set (trigger point—OQ) | authoritative; set-scoped | `FairnessApproved` \| `FairnessHeld` | by (campaign, assessment round) | service | async (batch) |
| **RecordHiringDecision** (A12) | Decision | **human (HM)** | **`RecommendationDelivered`** (CAR-5) | human actor present (INV-1); Override Justification if divergent | `HiringDecisionRecorded` | by (candidate-evaluation, decision) | HM | interactive |
| **ReleaseFeedback** (A13) | Feedback | **human (Recruiter)** | **`HiringDecisionRecorded`** (EV-INV-11) | candidate-view only (P13) | `FeedbackReleased` | by feedback id | Recruiter | interactive |
| **AssembleExport / DeliverExport** (A14) | Export | Recruiter/Campaign | contents fairness-passed & explained; decided items `HiringDecisionRecorded` | only fairness-passed/explained (CAR-6); boundary (INV-9) | `ExportAssembled` → `ExportDelivered` \| `ExportFailed` | by export id | Recruiter | async |

**Notably absent as external commands (by design):**
- **RecordEvidence** and **CompleteEvaluation** are **intra-aggregate** steps inside the Evaluation Service (ARCH-04 AD-23), not caller-invoked commands. They are internal transitions that emit `EvidenceRecorded` / `EvaluationCompleted`.
- **DeliverRecommendation** is **not** a command anyone issues. It is an **event-triggered internal transition**: when Evaluation observes `FairnessApproved` for the campaign (and Explanation is attached), it delivers — automatically, gated. No human or service "delivers a recommendation." *(AD-58.)* This is how EV-INV-7 becomes structurally unbypassable.
- **DeliverFeedback** is the internal reaction to `FeedbackReleased`.

### 2.4 Capability invocations *(to Intelligence Compute — a distinct class; NOT commands)*

| Invocation | Purpose | Caller | Produces | Emits fact? |
|---|---|---|---|---|
| **StructureEvidence** | turn raw work sample → structured evidence | Evaluation | candidate evidence structure | ❌ (Evaluation commits & emits `EvidenceRecorded`) |
| **Evaluate** | produce evaluation judgment + score + confidence + citations | Evaluation | candidate evaluation result | ❌ (Evaluation commits `EvaluationCompleted`) |
| **Explain** | generate audience-appropriate explanation | Evaluation / Feedback | explanation content | ❌ |
| **IntegritySignals** | authenticity signals | Integrity | signals | ❌ (Integrity owns the verdict) |
| **FairnessSignals** | adverse-impact signals over a set | Fairness | signals | ❌ (Fairness owns the verdict) |

> **Contract law for capabilities:** they are **pure, idempotent-by-input-content** functions that return *proposals*; the **owning service always validates and commits** the result as a fact. A capability invocation carries no authority and produces no truth. *(AD-56; realizes ARCH-05 AD-35 / ARCH-06 AD-47.)*

---

## 3. Query Catalog

*Each: Purpose · Owner · Consumer · Returned Business View · Consistency · Caching · Security · Pagination · Filtering · Sorting · Projection.* All queries are read-only and honor read-vs-reference rules (ARCH-04 §5).

| Query | Owner | Consumer | Returned view | Consistency | Caching | Security / projection |
|---|---|---|---|---|---|---|
| **GetCampaignState** | Campaign | Recruiter/HM | campaign lifecycle, roster summary, fairness status | read-your-writes for owner; else eventual | short TTL | tenant-scoped |
| **GetCandidateEvaluationState** | Evaluation | Recruiter/HM | participation status, evaluation summary (no raw internals to candidate) | eventual | short TTL | tenant + role projection (P13) |
| **GetRecommendationForDecision** | Evaluation | **Decision (HM)** | delivered recommendation + explanation + cited evidence | **must be Delivered** (CAR-5) | none (freshness) | HM only; never candidate (AD-25) |
| **GetCalibration** | Campaign | Evaluation | frozen calibration (post-Active) | strong (immutable post-freeze) | cache freely | service; tenant |
| **GetFairnessVerdict** | Fairness/Campaign | Evaluation, Export | campaign verdict (Passed/Hold) | eventual (delivery gate) | invalidate on verdict change | service; tenant |
| **IsConsentActive** | Consent | Evaluation | boolean + scope (the **synchronous gate**) | **strong / fail-closed** | very short TTL + event-invalidate on `ConsentWithdrawn` | service; tenant |
| **GetCandidateFeedback** | Feedback | **Candidate** | own released, candidate-view feedback ONLY | eventual (post-release) | per-candidate | candidate sees only own; no internals (P13) |
| **ListCampaignCandidates** | Campaign | Recruiter | roster + per-candidate progress | eventual | short TTL | tenant; paginated |
| **GetExportStatus** | Export | Recruiter | assemble/deliver status | eventual | short TTL | tenant |
| **GetAuditTrail** | Audit | Governance | tenant/campaign-scoped fact history | strong (append-only) | none | governed, tenant-scoped, itself audited |

**Cross-cutting query rules:**
- **Pagination:** all list queries use stable, opaque **continuation cursors** (never offset-by-page-number — unstable under change); page size bounded with a hard max.
- **Filtering/Sorting:** only over **business fields** exposed by the view; a query may never filter/sort on another aggregate's private data (would imply a forbidden read).
- **Projection:** each consumer gets an **audience-shaped projection** (P13) — the candidate's projection can never contain evaluation internals; a query cannot be asked to "return more" than the consumer's rights.
- **Consistency default:** **eventual** for cross-service reads (read models off facts); **strong** only where the business requires it (consent gate, calibration post-freeze, audit).

---

## 4. Business Event Contracts

*Derived directly from ARCH-05. Each: Producer · Consumers · Business Meaning · Ordering · Delivery · Versioning · Retention · Replay · Immutability.* Delivery is **at-least-once** with **idempotent consumers** everywhere (ARCH-06 AD-44). All events are **immutable** (ARCH-05 EV-INV-14). Ordering is **per key** (tenant → campaign → candidate-evaluation), not global.

| Event (ARCH-05) | Producer | Primary consumers | Ordering key | Retention | Replay |
|---|---|---|---|---|---|
| `OrganizationProvisioned` | Identity | (all, for tenant setup) | tenant | long (governance) | yes |
| `UserAccessGranted/Revoked` | Identity | (authz caches) | tenant | long | yes |
| `CampaignCreated` | Campaign | Candidate, Audit | campaign | campaign-life + retention | yes |
| `CampaignActivated` | Campaign | Candidate, Evaluation | campaign | " | yes |
| `CandidateImported` | Candidate | Consent, Campaign | candidate | retention/consent | yes |
| `ConsentGranted` | Consent | Candidate, Evaluation | candidate | retention | yes |
| `ConsentWithdrawn/Expired` | Consent | Evaluation, Candidate | candidate | retention | yes |
| `CandidateInvited` | Evaluation | Notification, Candidate | candidate-evaluation | campaign-life | yes |
| `WorkSampleSubmitted` | Evaluation | (internal), Audit | candidate-evaluation | retention | yes |
| `EvidenceRecorded` | Evaluation | Integrity | candidate-evaluation | retention (immutable evidence) | yes |
| `IntegrityVerified` | Integrity | Evaluation | candidate-evaluation | long (compliance) | yes |
| `EvaluationCompleted` | Evaluation | Fairness, Campaign | candidate-evaluation | long | yes |
| `FairnessApproved / FairnessHeld` | Fairness | Evaluation, Campaign, Export | **campaign** | long (compliance) | yes |
| `RecommendationFormed` | Evaluation | (internal) | candidate-evaluation | long | yes |
| `RecommendationDelivered` | Evaluation | Decision, Export, Campaign | candidate-evaluation | long | yes |
| `HiringDecisionRecorded` | Decision | Feedback, Export, Campaign | candidate-evaluation | **longest (accountability)** | yes |
| `FeedbackReleased/Delivered` | Feedback | Notification, Candidate | candidate-evaluation | retention | yes |
| `ExportAssembled/Delivered/Failed` | Export | Campaign | campaign | retention | yes |
| compensations (`…Cancelled/Withdrawn/Superseded/Failed`) | respective owner | affected consumers | as parent | as parent | yes |

**Event contract rules:**
- **Ordering:** guaranteed **within a key** only (a candidate-evaluation's facts are ordered; two different candidates' facts are not globally ordered). This is sufficient because the ordering laws (ARCH-05 §6) are all per-key or campaign-scoped — and it's what makes horizontal scaling possible.
- **Delivery:** at-least-once; consumers dedupe by event id (idempotent). A fact delivered twice must never create two truths.
- **Versioning:** **additive, backward-compatible only** (§6). A new field is optional; removing/renaming a field is a new major event contract that runs in parallel until all consumers migrate. Consumers are **tolerant readers** (ignore unknown fields).
- **Retention & Replay:** facts are retained per policy (compliance-relevant facts — decisions, verdicts, consent, integrity — longest; ARCH-08 sets storage). The stream is **replayable** to rebuild any read model (ARCH-06 §6) and *is* the audit substrate (AD-32).
- **Immutability:** no event edited/deleted; reversal is a compensating fact (ARCH-05 §8).

---

## 5. Long-running Contract Patterns

*When each pattern is appropriate, mapped to our flows.*

| Pattern | Use when… | Where used | Notes |
|---|---|---|---|
| **Request/Response (sync)** | An immediate answer is required to proceed correctly | `IsConsentActive` gate; `RecordHiringDecision`; interactive campaign commands | Strict deadlines (ARCH-06 §7); gate timeout ⇒ hold |
| **Fire-and-Forget** | The caller needs no result, only that the action is accepted | issuing invitations; notifications | Backed by durable accept (outbox) so "accepted" is real |
| **Publish/Subscribe** | Propagating a fact many may react to | every business event (ARCH-05) | Default inter-service style (choreography) |
| **Saga (orchestrated)** | A multi-service process needs a coordinator + compensation state | candidate-evaluation lifecycle; export | Only where choreography alone can't track compensation (ARCH-06 §7) |
| **Polling** | A consumer awaits an async result without a push channel | `GetExportStatus`; evaluation progress fallback | Cursor/status query; bounded frequency |
| **Async Completion** | A command starts work that finishes later, with a completion fact | `ImportCandidates`, `SubmitWorkSample`→evaluation, `AssembleExport` | Accept now → completion event later |
| **Human Approval** | A step **requires** a human before progressing | `RecordHiringDecision`, `ReleaseFeedback` | The pattern that encodes INV-1 / Rule 4 at the contract level — the process *waits* on a human, never auto-advances |
| **Compensation** | A started process becomes impossible | `EvaluationWithdrawn`, `CampaignCancelled`, `ExportFailed` | Forward-only compensating facts (ARCH-05 §8); never rollback |
| **Streaming** | Progressive partial results improve UX for a long computation | evaluation progress to recruiter UI | Non-authoritative; the authoritative fact is still `EvaluationCompleted` |

> **The "Human Approval" pattern is a first-class contract type here, not an afterthought.** It is the interface-level expression of human accountability: certain long-running processes are *defined* to block on a human command, and the contract makes that wait explicit and unskippable.

---

## 6. Interface Governance

| Concern | Policy |
|---|---|
| **Naming** | Commands = imperative verb + aggregate (`ActivateCampaign`); Events = aggregate + past-tense fact (`CampaignActivated`); Queries = `Get…`/`List…` + business view. All names use **DOC-04 canonical terms only** — a forbidden synonym in a contract name is a defect (DOC-04 §9). |
| **Versioning** | Semantic versioning of *contracts*. **Additive changes are backward-compatible** (new optional fields, new events, new queries). **Breaking changes require a new major contract** that runs **in parallel** with the old until consumers migrate. |
| **Backward compatibility** | **Tolerant reader** on every consumer (ignore unknown fields, don't fail on additions). Producers never remove/repurpose a field within a major version. **Expand-contract** migration: add new → migrate consumers → retire old. |
| **Deprecation** | A contract is marked Deprecated with a superseded-by pointer (mirrors DOC-04 lifecycle) and a **sunset window**; removal only after all registered consumers migrate. |
| **Breaking changes** | Defined as: removing/renaming a field, tightening validation, changing semantics of an existing field, or changing event meaning. All are major-version events, never in-place edits. |
| **Consumer-driven contracts** | Each consumer publishes the subset of a contract it relies on; the owning service runs **consumer-driven contract tests** so it cannot break a consumer unknowingly. *(AD-55.)* |
| **Schema evolution** | Governed by additive/tolerant-reader rules above; enforced in CI against every registered consumer contract. |
| **Contract ownership** | A contract is owned by the **service that owns the aggregate** (ARCH-03/ARCH-06). Only the owner may evolve it. This extends DOC-04's "every term has an owning domain" to "every contract has an owning service." |
| **Lifecycle** | Draft → Stable → Deprecated → Retired, with the same governance discipline as DOC-04's Term Registry. A contract registry is the single source of truth for what exists and who owns it. |

---

## 7. Error Architecture

Errors are **business outcomes**, expressed in business terms — not stack traces. Every error carries: category, whether **retry is legal**, and who is responsible to handle it. Grounded in ARCH-04 §9 (gates fail closed, intelligence fails soft) and ARCH-06 §7.

| Category | Meaning | Created by | Handled by | Retry legal? |
|---|---|---|---|---|
| **Business Error** | A valid request that the business refuses (e.g., "cannot conclude: fairness held") | owning service | caller (change intent) | ❌ (state must change first) |
| **Validation Error** | Malformed/invalid input (bad file row, missing field) | owning service | caller (fix input) | ❌ (same input fails again) |
| **Authorization Error** | Caller lacks rights / wrong tenant | owning service / Identity | caller (not retryable) — **security-audited** | ❌ |
| **Conflict Error** | State moved under the caller (e.g., campaign already Active; stale version) | owning service | caller (re-read, reconcile) | ⚠️ only after reconciliation |
| **Precondition/Gate Hold** | A gate is not satisfied (consent inactive, integrity flagged, fairness held) | the gate | caller/process **waits**; not an error to paper over | ❌ retry ≠ progress; the *condition* must change |
| **Retryable Transient Failure** | Temporary unavailability/timeout of a dependency | infra/dependency | caller/consumer with backoff+jitter, bounded | ✅ (idempotent only) |
| **Non-Retryable Permanent Failure** | Deterministic failure that will not self-resolve | owning service | escalate; do not retry | ❌ |
| **Compensation-Required** | A committed step must be undone in business terms | orchestrating saga | saga emits compensating fact (ARCH-05 §8) | n/a (forward-only) |

**Rules:**
- **Retry is legal only for idempotent operations against transient failures.** A Validation/Business/Authorization error is never retried (it will deterministically fail again) — retrying them is a bug.
- **A gate hold is not an error to be retried away.** `FairnessHeld` / inactive consent means *the business is correctly refusing*; the resolution is a state change (human review, new consent), then the natural flow resumes.
- **Errors never leak internals or PII** (§8); a candidate-facing error is dignified and non-technical (DOC-06 Error philosophy).
- **Conflict errors carry the current version** so the caller can reconcile (optimistic concurrency at the contract level; mechanism in ARCH-08).

---

## 8. Security Contracts

Every contract — command, query, or event — carries a mandatory **Contract Envelope** of business/security metadata (transport-independent). This is the interface-level realization of ARCH-06 §10 and the Constitution's Tier-0 gates.

> ### AD-53 — Every contract carries a mandatory Contract Envelope.
> No command, query, or event exists without it. A message missing envelope fields is rejected before any business logic runs.

| Envelope field | Purpose | Rule |
|---|---|---|
| **Tenant context** | The single tenant this interaction belongs to | Mandatory on **everything**; cross-tenant is impossible (INV-10, CAR-7). Enforced before business logic. |
| **Caller identity** | Who/what is acting (user via edge, or workload) | Authenticated (ARCH-06 §10); commands that require a **human** (INV-1, Rule 4) assert a human principal, not a service. |
| **Authorization scope** | What the caller may do | Checked per interaction against the legal-interaction matrix (ARCH-04 §2). |
| **Correlation ID** | Ties a business transaction across services | Minted at the edge; propagated on every downstream call and emitted fact. |
| **Trace ID / span** | Distributed trace linkage | Propagated for observability (ARCH-06 §9). |
| **Idempotency key** | De-dupe commands | **Mandatory on every command** (AD-57); events carry a stable event id. |
| **Replay protection** | Reject stale/replayed requests | Time-bounded + nonce on sensitive commands; events are naturally replay-safe via idempotent consumers. |
| **Rate-limit class** | Protect services / fairness of service | Per-tenant and per-caller classes; bulk imports separated from interactive traffic. |
| **Data classification** | Mark PII / sensitivity | Fields classified; PII-classified content triggers minimization rules at the LLM edge (ARCH-06 §10.6). |
| **PII rules** | Governs handling of personal data | PII never in logs/traces/errors; minimized before external model calls; consent-governed retention. |
| **Audit metadata** | Actor + action + time for the record | Every material command/event contributes to the audit substrate (CAR-3); the actor and time are part of the fact. |

> ### AD-57 — Every command carries an idempotency key; every consumer is idempotent.
> This is what makes at-least-once delivery (AD-44) safe at the contract level: replays and retries converge to one truth.

---

## 9. External Interface Architecture

External systems are **untrusted, foreign-vocabulary** boundaries. They must never shape the canonical domain (ARCH-03). Every one sits behind an **Anti-Corruption Layer (ACL)** — a translating adapter owned by the internal service at that edge.

> ### AD-52 — Every external integration SHALL pass through an Anti-Corruption Layer.
> No external terminology, schema, or model may leak into the canonical domain. The ACL translates external concepts ⇄ canonical domain (DOC-04) in both directions. **No external schema ever becomes an internal schema.** If an external system changes, only its ACL changes; ARCH-03 is untouched. This protects the ubiquitous language as integrations proliferate and vary independently.

| External system | Internal owner (ACL location) | Translates … | Canonical protection |
|---|---|---|---|
| **ATS** *(deferred, AD-11)* | Candidate (in) / Export (out) | ATS candidate/req/offer models ⇄ Candidate, Role Reference, Export | We never adopt ATS entities; `Requisition`/`Offer` stay reference-only (INV-9) |
| **HRIS** *(deferred, outcomes)* | Outcome & Learning (future) | HRIS Employee/performance ⇄ Outcome (reference-only, D-04.A4) | Employee never becomes ours |
| **Identity Provider (OIDC/SSO)** | Identity | external identity claims ⇄ User + tenant + permissions | External claim shapes don't define our authz model |
| **Email / Messaging** | Notification | our notification intent ⇄ provider message format | Provider quirks isolated in the adapter |
| **LLM provider(s)** | Intelligence Compute | canonical evaluation inputs ⇄ provider prompt/response; **PII minimized** | The AI sees minimized, role-relevant content only; its output is a *proposal*, never a fact (AD-56) |
| **Object Storage** | Candidate / Evaluation | files ⇄ evidence/resume references | Storage semantics never leak into the domain |
| **Future integrations** | the service at that edge | external ⇄ canonical | Same rule, no exceptions |

**ACL contract rules:** (1) the ACL is the **only** place foreign vocabulary is allowed; (2) translation is **explicit and total** — no passthrough of untranslated external fields into the domain; (3) an ACL failure is a **transient/permanent external error** (§7), degrading per ARCH-04 §9 (e.g., LLM down ⇒ intelligence fails *soft* to human); (4) each ACL is versioned independently of the canonical contracts it feeds.

---

## 10. Contract Traceability

Every contract traces back through the stack. No orphan contracts. (Representative; the pattern holds for all.)

| Contract | ARCH-04 interaction | ARCH-03 aggregate | ARCH-02 capability | ARCH-01 context |
|---|---|---|---|---|
| `CreateCampaign` (cmd) | A1 | Evaluation Campaign | Evaluation Campaign | SoI / Unit of Work |
| `ImportCandidates` (cmd, file) | A2 | Candidate | Candidate Intake (C2) | Import boundary |
| `RecordConsentGrant` (cmd) | A15 | Consent | Consent (C24) | PII trust boundary |
| `InviteCandidate` (cmd) | A4 | Candidate Evaluation (Invitation) | Invitation/Notification (C4/C5) | Email boundary |
| `SubmitWorkSample` (cmd) | A5 | Candidate Evaluation (Work Sample) | Work Sample (C8) | SoE / AD-10 |
| `VerifyIntegrity` (cmd) | A7 | Candidate Evaluation (Evidence) | Integrity (C9) | Trust boundary |
| `AssessFairness` (cmd) | A9 | Evaluation Campaign (Fairness Verdict) | Fairness (C13) | Gate |
| `IsConsentActive` (query) | §5 read dep | Consent | Consent (C24) | Gate |
| `GetRecommendationForDecision` (query) | §5 read dep | Candidate Evaluation (Recommendation) | Recommendation (C16) | Human-in-loop |
| `RecordHiringDecision` (cmd) | A12 | Hiring Decision | Human-Decision Support (C17) | Human accountability |
| `ReleaseFeedback` (cmd) | A13 | Feedback | Candidate Feedback (C19) | Candidate afterlife |
| `RecommendationDelivered` (event) | A11 | Candidate Evaluation | Recommendation (C16) | Delivery gate |
| `HiringDecisionRecorded` (event) | A12 | Hiring Decision | C17 | Accountability |
| `FairnessApproved` (event) | A9 | Evaluation Campaign | C13 | Gate |
| ACL adapters (external) | ARCH-04 boundaries | reference-only aggregates | C2/C3/C18 | Trust boundaries |

> Every command, query, and event maps to a legal ARCH-04 interaction, an ARCH-03 aggregate, an ARCH-02 capability, and an ARCH-01 context. **No contract exists without a business reason.**

---

## 11. Architecture Decisions *(continuing the log; ARCH-06 ended at AD-50)*

| ID | Decision | Rationale | Alternatives considered |
|---|---|---|---|
| **AD-51** | Interfaces are business contracts; transport is an implementation detail | Contracts outlive transports; must survive re-platforming | Transport-first (rejected: couples meaning to wire) |
| **AD-52** | Every external integration passes through an Anti-Corruption Layer | Protect canonical domain as integrations vary | Direct mapping of external schemas (rejected: vocabulary leak, ARCH-03 rot) |
| **AD-53** | Mandatory Contract Envelope on every command/query/event | Tenant/authz/correlation/idempotency/PII enforced uniformly, pre-logic | Per-contract ad-hoc metadata (rejected: drift, gate gaps) |
| **AD-54** | Additive/backward-compatible evolution; breaking = new parallel major; tolerant readers | Independent service evolution without breakage | In-place breaking changes (rejected: consumer breakage) |
| **AD-55** | Consumer-driven contract testing | Owners cannot break consumers unknowingly | Producer-only tests (rejected: blind to real usage) |
| **AD-56** | Capability invocations (Intelligence Compute) are not commands and produce no facts | AI never becomes truth; owner validates/commits | Treat AI output as authoritative (rejected: INV-1, ARCH-05 AD-35) |
| **AD-57** | Every command idempotency-keyed; every consumer idempotent | Makes at-least-once delivery safe | Exactly-once delivery (rejected: network fiction, AD-44) |
| **AD-58** | Recommendation *delivery* is an event-triggered internal transition, not an external command | Makes EV-INV-7 (no delivery before fairness) structurally unbypassable | A `DeliverRecommendation` command (rejected: invites bypass under pressure) |
| **AD-59** | Cross-service reads default to eventual (read models off facts); strong only where the business requires it | Minimizes coupling; matches ARCH-04 §8 consistency classes | Strong-by-default reads (rejected: coupling, latency, distributed reads) |

## 12. Open Questions *(genuine architectural questions only)*

1. **Integrity outcome shape** (carried, ARCH-05 OQ-3): is a low-integrity result a field on `IntegrityVerified` or a distinct `IntegrityFlagged` event/contract? Affects the Integrity command result and EV-INV-5.
2. **Fairness trigger point** (carried): does `AssessFairness` run once per full set or as interim rounds? Determines whether it's one async completion or a repeated contract with round keys.
3. **Consent-active check: synchronous query vs replicated read model** on the hot path — strong-fail-closed sync call vs locally-replicated consent with event-invalidation. Latency vs freshness; must remain fail-closed either way.
4. **Streaming evaluation progress**: is progress a first-class (non-authoritative) streaming contract at MVP, or deferred? UX value vs added surface.
5. **Bulk import partial-failure contract**: per-row outcomes — is a partially-successful import one async-completion with a result manifest, or per-candidate facts + an error manifest?
6. **Export: point-in-time vs living** (carried from ARCH-05 OQ-4): does a post-export decision change issue a new export contract (supersede)?

## 13. Risks

- **Contract explosion:** too many fine-grained contracts. *Mitigation:* contracts derive strictly from ARCH-04 interactions/§2 commands — no contract without an interaction; capability calls kept out of the domain-contract count.
- **Version drift:** consumers on stale majors. *Mitigation:* consumer-driven contract tests (AD-55) + registry + sunset windows (§6).
- **Consumer coupling / over-fetching:** consumers depending on fields they shouldn't, or fetching whole aggregates. *Mitigation:* audience-shaped projections (§3), reference-by-identity default (ARCH-04 AD-29), CDC tests assert minimal reliance.
- **Chatty interfaces:** many small sync calls. *Mitigation:* facts-over-calls (pub/sub default); only two sync deps on the hot path (ARCH-06 §5).
- **Breaking compatibility:** an accidental breaking change. *Mitigation:* CI compatibility checks against registered consumer contracts; breaking = new major only.
- **ACL bypass:** a service calling an external system directly. *Mitigation:* AD-52 + boundary review; external calls only from the designated ACL-owning service.
- **Event misuse:** using an event as a command ("do X") or a command as a fact. *Mitigation:* the taxonomy (§0.4/§1) + governance review; facts are past-tense and produce no obligation on the producer.
- **Envelope erosion:** teams omitting envelope fields "for internal calls." *Mitigation:* AD-53 rejects envelope-less messages before business logic; enforced centrally.

## 14. Deferred

- **To ARCH-08 (Database Architecture):** per-service datastores, event store, read-model/projection storage, retention/WORM realization, partitioning, encryption at rest, backup/restore/DR, optimistic-concurrency mechanism behind Conflict errors.
- **To ARCH-09 (API/Contract Specifications):** the concrete, generated artifacts — OpenAPI (external), Protobuf/gRPC (internal), AsyncAPI (events), JSON Schemas, endpoint lists, URLs, verbs, wire formats. **ARCH-09 is the mechanical projection of this document onto transports.**
- **To ARCH-10 (Deployment Architecture):** gateway/mesh configuration, rate-limit enforcement mechanics, service discovery, environment/config/secrets wiring, canary/blue-green rollout of contract versions.
- **To AI Orchestration / Evaluation Engine docs:** the internal mechanics behind capability invocations (prompting, model routing, evaluation logic).

---

*End of ARCH-07 v0.1 — the Interface Architecture & Contracts. Contract-first, transport-independent: commands, queries, event contracts, long-running patterns, governance, error architecture, the mandatory security envelope, and the Anti-Corruption Layer for external systems — every one derived from ARCH-01→06, none inventing a new concept, boundary, or term. The contract model remains valid even if every transport technology changes. Next: ARCH-08 — Database Architecture (per-service stores, event store, projections, retention/WORM, partitioning, encryption, backup/DR), then ARCH-09 — the concrete API/Protobuf/AsyncAPI specifications, which become almost mechanical from here.*
