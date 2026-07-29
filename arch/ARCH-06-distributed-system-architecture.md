# ARCH-06 — Distributed System Architecture

| Field | Value |
|---|---|
| **Document ID** | ARCH-06 |
| **Title** | Distributed System Architecture (the first implementation document) |
| **Owner** | Principal Software Architect + Distributed Systems Architect |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture (implementation begins here) |
| **Depends on** | ARCH-05 (Business Events — fact ownership), ARCH-04 (Interactions), ARCH-03 (Aggregates), ARCH-02 (Responsibilities), ARCH-01 (Context + trust/failure boundaries), DOC-05 (gates) |
| **Blocks** | ARCH-07 (API Contracts), ARCH-08 (Database Architecture), and all engineering |
| **The one question** | **"What is the smallest set of independently-deployable services whose boundaries are the business's boundaries — and how do they stay correct, fast, and safe at scale?"** |
| **What changes here** | **Technology is now permitted.** Every technical choice must be *derived* from ARCH-01→05, never invented. Where a choice is a genuine option, it is recorded as a decision with alternatives. |

---

## 0. The rule that governs this document

Every service boundary in ARCH-06 is **derived**, not designed from scratch:

- **Aggregate ownership** (ARCH-03) → *what state a service is authoritative for.*
- **Business interactions** (ARCH-04) → *who a service may talk to, and how.*
- **Business event ownership** (ARCH-05 §2) → *what facts a service may assert.*

> **No arbitrary services.** If a proposed service does not own an aggregate (ARCH-03) or a stateless capability explicitly identified in ARCH-02/04, it does not exist. If a proposed call is not a legal interaction (ARCH-04 §2), it is not built. If a proposed message is not a business fact (ARCH-05) or a sanctioned command/query, it is not sent. **The distributed system is the business model, deployed.**

---

## 1. Architectural Philosophy

### 1.1 Why distributed

The platform has three workloads with fundamentally different physics:

1. **Transactional/coordination** (campaigns, candidates, decisions) — low CPU, strong-consistency, latency-sensitive, modest volume.
2. **AI-heavy inference** (structuring evidence, producing evaluations and explanations, integrity signals) — extremely CPU/GPU- and token-cost-heavy, latency-tolerant, spiky, the dominant cost center.
3. **Authoritative gates** (integrity, fairness, consent, audit) — must be independently fault-isolated so that no failure elsewhere can cause a gate to be *skipped* rather than *held*.

A single deployment unit forces these three to share a failure domain, a scaling policy, and a release cadence. That is precisely wrong: a burst of AI evaluation must not degrade the fairness gate; a bug in export must not take down consent. **Distribution lets each workload fail, scale, and deploy independently** — which, for a product whose entire value is *never being wrong-or-unfair* (ARCH-01), is not a luxury.

### 1.2 Why microservices

Because we already did the hard part. Microservices fail when boundaries are guessed; ours are **already proven** through five documents of domain work. Each service owns a bounded context's aggregate(s) (ARCH-03) and the facts about them (ARCH-05). The seams are the business's seams, so the classic microservice pathologies — chatty cross-service calls, distributed transactions, entity anemia — are avoidable *by construction*: ARCH-04 already told us which conversations are legal and which are forbidden, and ARCH-03 already told us which invariants live inside one aggregate (hence one service, one local transaction).

### 1.3 Why *not* a modular monolith (argued fairly)

A modular monolith is a legitimate and often-underrated choice, and I will not strawman it. Its real advantages here would be: **one transaction manager** (the cross-aggregate fairness rule could be a local transaction), **one deployable** (radically simpler ops for a small team), **one datastore** (no read-model duplication), and **far cheaper day-one validation**. For a pre-product-market-fit company, those are serious.

We still choose microservices as the **target** architecture for three product-specific reasons the monolith cannot satisfy:
- **AI-workload isolation.** The evaluation inference tier must scale 10–100× independently of everything else and must be back-pressurable without stalling coordination. In a monolith, inference threads and transaction threads contend in one process.
- **Gate fault-isolation.** Fairness/integrity/consent/audit must be isolated failure domains; a monolith couples their availability to every other module's stability.
- **Compliance blast-radius.** The sharpest trust boundary (PII to an external LLM — ARCH-01) is easier to contain, audit, and independently harden as a dedicated service.

But because the monolith's day-one advantages are real, we manage the tradeoff explicitly (AD-41): **boundaries are microservice boundaries now; physical co-deployment of low-risk services at MVP is a permitted, reversible optimization.** We get monolith-like simplicity early *without* betting the domain model, because the seams are contracts, not deploy units.

### 1.4 Why boundaries follow domain ownership

If boundaries followed technical layers ("a data service, a logic service, a UI service"), every business change would cut across all services and every feature would need a distributed transaction. Because boundaries follow **aggregate ownership**, a business change is almost always *inside one service*, and the only cross-service rules are the ones the business already tolerates as eventual (ARCH-04 §8). This is the entire payoff of the sequencing — see §5.

### 1.5 Why every service owns its own data

Shared databases recreate the monolith's coupling while paying the network's cost — the worst of both. A shared table is a shared invariant with no owner (the exact spaghetti ARCH-03 §0 forbade, now at the data tier). **Each service is the sole writer of its aggregate's data**; others get facts (events) or query it through its API. This makes the ordering laws (ARCH-05 §6) enforceable and keeps tenant isolation checkable at one place per aggregate.

> ### AD-40 — The platform SHALL be implemented as a microservice architecture.
> Service boundaries are derived exclusively from bounded-context/aggregate ownership (ARCH-03), legal interactions (ARCH-04), and business-fact ownership (ARCH-05). Each service is independently deployable, owns its authoritative data, and communicates only through sanctioned APIs (commands/queries) and business events (facts). **Rationale:** independent scaling of the AI-heavy workload, hard fault-isolation of the Constitutional gates, and containment of the LLM/PII trust boundary — none achievable in a single failure/scaling/release domain — combined with domain seams already proven crisp by ARCH-01→05.

> ### AD-41 — Boundaries are fixed; MVP deployment topology is a reversible optimization.
> The *logical* service boundaries (AD-40) are frozen. Their *physical* packaging is not: at MVP, low-risk, co-changing services MAY be co-deployed in a shared runtime (a "modulith" of the frozen modules) to reduce operational load, provided (a) each retains its own datastore/schema and API, (b) no forbidden interaction (ARCH-04) is enabled by co-location, and (c) the four gates — Consent, Integrity, Fairness, Audit — plus the Intelligence Compute tier are deployed as **separate** units from day one. Splitting a co-deployed module later requires no domain change, only an ops change. **Rationale:** capture the monolith's early simplicity without forfeiting the domain-aligned seams; spend runway on validating AS-1, not on premature ops.

---

## 2. Service Identification

Thirteen services. Twelve own an aggregate and its facts (ARCH-05 §2); one — **Intelligence Compute** — deliberately owns *no* aggregate and *no* authoritative fact (it is stateless capability; see §2.5). Cross-cutting infrastructure (API gateway, event backbone, secrets, mesh) is described in §4/§7/§10/§11, not as domain services.

**Legend:** *Stateful* = owns an authoritative datastore; *Stateless* = owns none. *Availability* tiers: **Critical** (gate/decision path), **High** (core flow), **Standard**.

### 2.1 Identity & Access Service *(BC-1)*
- **Purpose:** Establish tenants, users, roles/permissions; issue and validate access; anchor tenant isolation.
- **Owned aggregates:** Organization, User.
- **Owned events:** `OrganizationProvisioned`, `UserAccessGranted/Revoked`.
- **Published APIs (cmd/query):** provision org; grant/revoke access; introspect token; resolve tenant+permissions.
- **Consumed APIs:** external IdP (OIDC) for authentication.
- **Published events:** the three above.
- **Consumed events:** none (root of authority).
- **Dependencies:** external IdP/SSO.
- **Scaling:** read-heavy (token/claims validation); horizontal, cache-friendly. **Availability: Critical** (everything needs authz). **Stateful** (small).
- **Why it exists:** authority and tenancy are orthogonal to hiring work (ARCH-03 BC-1); one place owns "who may act," so isolation (INV-10) is enforceable at one seam.

### 2.2 Candidate Service *(BC-2)*
- **Purpose:** Durable candidate identity; file-based intake (CSV + resume, AD-11); afterlife status.
- **Owned aggregates:** Candidate.
- **Owned events:** `CandidateImported`, `CandidateInvited`* , `InvitationExpired/Revoked`* (*invitation facts are about a candidate's participation; see boundary note §3).
- **Published APIs:** import candidates; fetch candidate; update afterlife status.
- **Consumed APIs:** Consent (gate check at intake); Campaign (roster linkage).
- **Published events:** `CandidateImported`.
- **Consumed events:** `CampaignActivated` (to enable invitations), `ConsentGranted` (to permit invite).
- **Dependencies:** object storage (resume/CSV files), Consent, Campaign.
- **Scaling:** bursty at import (batch); otherwise light. **Availability: High.** **Stateful.**
- **Why it exists:** a candidate outlives any campaign (INV-7); modeling the person once enables afterlife/silver-medal/portable evidence later without duplicating people per campaign.

### 2.3 Campaign Service *(BC-4 — the organizing hub)*
- **Purpose:** Own the Unit of Work: campaign lifecycle, scope, roster, and the (thin) Calibration; freeze calibration at Active; hold the campaign-scoped Fairness Verdict reference.
- **Owned aggregates:** Evaluation Campaign (+ Calibration entity, roster).
- **Owned events:** `CampaignCreated`, `CampaignActivated`, `CampaignConcluded`, `CampaignCancelled`.
- **Published APIs:** create/activate/conclude/cancel campaign; set calibration; manage roster; query campaign state.
- **Consumed APIs:** Candidate (roster); Fairness (verdict status).
- **Published events:** the four campaign facts.
- **Consumed events:** `EvaluationCompleted` (to know set readiness for fairness), `FairnessApproved/Held` (to gate conclusion), `RecommendationDelivered` (rollup), `ExportDelivered` (to conclude).
- **Dependencies:** Candidate, Fairness, Evaluation.
- **Scaling:** moderate; one coordination point per hiring effort. **Availability: High.** **Stateful.**
- **Why it exists:** the Campaign is the business Unit of Work (AD-09); centralizing its lifecycle keeps CAR-4/CAR-8 (roster uniqueness, calibration freeze) inside one owner. *(Chokepoint risk acknowledged — §13.)*

### 2.4 Evaluation Service *(BC-4 — the workhorse)*
- **Purpose:** Own the Candidate Evaluation aggregate and orchestrate its internal lifecycle: invitation → work sample → evidence → (integrity) → evaluation → recommendation → delivery. Commit all authoritative evaluation state and facts.
- **Owned aggregates:** Candidate Evaluation (Invitation, Work Sample, Evidence Item, Evaluation, Recommendation).
- **Owned events:** `WorkSampleSubmitted`, `EvidenceRecorded`, `EvaluationCompleted`, `RecommendationFormed`, `RecommendationDelivered`, `RecommendationSuperseded`, `EvaluationWithdrawn`.
- **Published APIs:** open evaluation; accept work sample; query evaluation/recommendation state.
- **Consumed APIs:** **Intelligence Compute** (request evidence structuring / evaluation / explanation — a *computation*, not a fact); **Consent** (immediate gate check before evidence use); **Integrity** (submit evidence for verdict); Campaign (calibration read, fairness-verdict read).
- **Published events:** the seven above.
- **Consumed events:** `ConsentWithdrawn` (→ `EvaluationWithdrawn`), `FairnessApproved` (→ enables `RecommendationDelivered`), `IntegrityVerified` (→ enables `EvaluationCompleted`).
- **Dependencies:** Intelligence Compute, Consent, Integrity, Campaign.
- **Scaling:** moderate transactional core; **delegates heavy compute** to Intelligence Compute (so this service itself stays light and consistent). **Availability: High.** **Stateful.**
- **Why it exists:** the Candidate Evaluation is a single consistency boundary (ARCH-03 §3.0); its authoritative state must have exactly one writer. The internal choreography (ARCH-04 AD-23) is *intra-service*, not split — precisely why we do **not** create separate Evidence/Recommendation services.

### 2.5 Intelligence Compute Service *(stateless AI capability — owns NO aggregate)*
- **Purpose:** Perform the AI-heavy inference: structure raw work samples into evidence, produce evaluation judgments (score + confidence + cited evidence), generate audience-appropriate explanations, and compute integrity/fairness *signals*. Returns **candidate results**; never commits a fact.
- **Owned aggregates:** **none.** **Owned events:** **none.**
- **Published APIs:** `structureEvidence`, `evaluate`, `explain`, `integritySignals`, `fairnessSignals` (all pure functions of inputs; idempotent by content hash).
- **Consumed APIs:** external LLM provider(s) — the **PII-minimization trust boundary** (ARCH-01 AD; §10.6).
- **Published/Consumed events:** none (it is invoked, it returns; owning services emit the facts).
- **Dependencies:** external LLM providers; model registry/prompt store.
- **Scaling:** **the dominant scaling axis** — horizontal, queue-depth-driven (KEDA), worker pools per model, back-pressured, spot/burst-capable. **Availability: Standard** (its unavailability degrades to *low confidence / more human*, never to a wrong result — ARCH-04 §9). **Stateless.**
- **Why it exists:** AI inference has radically different physics (cost, latency, burst) and the sharpest compliance boundary. Isolating it lets it scale and fail independently, and enforces ARCH-05 AD-35: **the AI never emits an authoritative fact** — an owning service always validates and commits, so a model hallucination cannot *become* a business truth.

### 2.6 Integrity Service *(BC-6 — authoritative gate)*
- **Purpose:** Produce the authoritative, un-overridable Integrity Score / verdict on evidence authenticity.
- **Owned aggregates:** — (owns the Integrity verdict as authoritative output attached to evidence). **Owned events:** `IntegrityVerified` (and, if adopted, `IntegrityFlagged` — OQ).
- **Published APIs:** `verifyIntegrity(evidence)`.
- **Consumed APIs:** Intelligence Compute (integrity signals).
- **Published events:** `IntegrityVerified`. **Consumed events:** `EvidenceRecorded`.
- **Scaling:** follows evidence volume. **Availability: Critical** (gate — fails *closed*: no trusted evidence without a verdict). **Stateful** (verdict store).
- **Why it exists:** the gate must be independent of the thing it judges (ARCH-04 AD-27 analog); a dedicated failure domain guarantees integrity is *held*, never skipped.

### 2.7 Fairness Service *(BC-6 — authoritative, campaign-scoped gate)*
- **Purpose:** Assess adverse impact across a campaign's candidate set; produce the campaign-scoped Fairness Verdict.
- **Owned aggregates:** — (owns the campaign Fairness Verdict). **Owned events:** `FairnessApproved`, `FairnessHeld`.
- **Published APIs:** `assessFairness(campaign)`, query verdict.
- **Consumed APIs:** Evaluation (read the set of evaluations); Intelligence Compute (fairness signals).
- **Published events:** `FairnessApproved/Held`. **Consumed events:** `EvaluationCompleted` (set readiness).
- **Scaling:** per-campaign, batch-like. **Availability: Critical** (gate — no delivery without approval; fails *closed*). **Stateful.**
- **Why it exists:** fairness is a property of the **set** (ARCH-03 §3.0); only a campaign-scoped owner can assess it, and it must gate delivery without owning recommendations (AD-27).

### 2.8 Consent Service *(BC-6 — authoritative gate)*
- **Purpose:** Own consent grant/scope/withdrawal/expiry; be the immediate gate ahead of all candidate-data use.
- **Owned aggregates:** Consent. **Owned events:** `ConsentRequested`, `ConsentGranted`, `ConsentWithdrawn`, `ConsentExpired`.
- **Published APIs:** request/record consent; **synchronous `isConsentActive(candidate,campaign)`** gate check.
- **Published events:** the four consent facts. **Consumed events:** `CandidateImported`.
- **Scaling:** read-heavy gate checks (cache with short TTL + event-invalidation). **Availability: Critical** (fails *closed*: no consent → no processing). **Stateful.**
- **Why it exists:** consent governs candidate data (INV-11) and must be checkable immediately at the evidence boundary (ARCH-04 §8 immediate-consistency).

### 2.9 Audit Service *(BC-6 — the ledger)*
- **Purpose:** Provide the immutable, complete, tamper-evident, tenant/campaign-organized record. **The event backbone *is* the audit substrate** (ARCH-05 AD-32); this service curates, indexes, retains, and serves it for governance.
- **Owned aggregates:** Audit Record (append-only projection of all facts). **Owned events:** none of its own (it consumes all).
- **Published APIs:** governed, tenant-scoped audit query.
- **Consumed events:** **every** business fact.
- **Scaling:** write-heavy append; read rare/governed. **Availability: Critical** (no material action may proceed unauditable — §7). **Stateful** (append-only store, WORM-capable).
- **Why it exists:** auditability is Tier-0 (P8); a neutral, passive ledger that never initiates (ARCH-04 AD-26) is the trust backbone.

### 2.10 Decision Service *(BC-5)*
- **Purpose:** Capture the accountable **human** Hiring Decision; record overrides; immutable once decided.
- **Owned aggregates:** Hiring Decision. **Owned events:** `HiringDecisionRecorded`.
- **Published APIs:** present finalists (query recommendations+explanations); record decision.
- **Consumed events:** `RecommendationDelivered` (precondition).
- **Scaling:** light (human-paced). **Availability: Critical** (accountability path). **Stateful.**
- **Why it exists:** the human decision must be its own thing with its own actor/time/immutability (INV-1, ARCH-03 AGG-5); the system never emits this fact (AD-35).

### 2.11 Feedback Service *(BC-5)*
- **Purpose:** Generate candidate-view feedback; deliver only after recruiter release (Rule 4).
- **Owned aggregates:** Feedback. **Owned events:** `FeedbackReleased`, `FeedbackDelivered`.
- **Published APIs:** draft/release feedback; deliver.
- **Consumed APIs:** Intelligence Compute (candidate-view explanation); Notification (delivery).
- **Consumed events:** `HiringDecisionRecorded` (precondition, EV-INV-11).
- **Scaling:** light. **Availability: Standard.** **Stateful.**
- **Why it exists:** distinct release-gate rule and candidate-view-only exposure (P13) warrant a dedicated owner; the most brand-defining moment (DOC-11) deserves isolation.

### 2.12 Export Service *(BC-5 — boundary end)*
- **Purpose:** Assemble and deliver fairness-passed, explained intelligence back to the customer (KD-12.7).
- **Owned aggregates:** Export Package. **Owned events:** `ExportAssembled`, `ExportDelivered`, `ExportFailed`.
- **Published APIs:** assemble/deliver export; query status.
- **Consumed events:** `HiringDecisionRecorded`, `RecommendationDelivered`.
- **Scaling:** light/batch. **Availability: Standard** (fails *safe*: results stay in-platform). **Stateful.**
- **Why it exists:** the deliver-back boundary is where our responsibility ends (INV-9); a dedicated owner keeps "we never action the offer" enforceable.

### 2.13 Notification Service *(Engagement)*
- **Purpose:** Send invitations and status notifications at meaningful moments only (Silence/Waiting philosophy, DOC-06).
- **Owned aggregates:** — (owns delivery records). **Owned events:** none authoritative (delivery receipts internal).
- **Published APIs:** send invitation/notification.
- **Consumed APIs:** external email/messaging providers.
- **Consumed events:** `CandidateInvited`, `FeedbackReleased`, meaningful campaign lifecycle facts.
- **Scaling:** bursty; horizontal. **Availability: Standard.** **Stateless** (aside from delivery log).
- **Why it exists:** communication is a cross-cutting engagement responsibility (ARCH-02 D8); isolating it prevents notification failures from touching the evaluation path.

### 2.14 Service map (at a glance)

| Service | Context | Owns aggregate? | Availability | Stateful | Scaling driver |
|---|---|---|---|---|---|
| Identity & Access | BC-1 | ✅ Org, User | Critical | ✅ | authz reads |
| Candidate | BC-2 | ✅ Candidate | High | ✅ | import bursts |
| Campaign | BC-4 | ✅ Campaign | High | ✅ | # campaigns |
| Evaluation | BC-4 | ✅ Candidate Evaluation | High | ✅ | # candidates |
| **Intelligence Compute** | (capability) | ❌ none | Standard | ❌ | **AI tokens/inference** |
| Integrity | BC-6 | ✅ verdict | Critical | ✅ | evidence volume |
| Fairness | BC-6 | ✅ campaign verdict | Critical | ✅ | # campaigns |
| Consent | BC-6 | ✅ Consent | Critical | ✅ | gate-check reads |
| Audit | BC-6 | ✅ ledger | Critical | ✅ | all facts |
| Decision | BC-5 | ✅ Hiring Decision | Critical | ✅ | human-paced |
| Feedback | BC-5 | ✅ Feedback | Standard | ✅ | # decisions |
| Export | BC-5 | ✅ Export Package | Standard | ✅ | # campaigns |
| Notification | Engagement | ❌ (delivery log) | Standard | ~ | event bursts |

---

## 3. Service Boundary Justification

**Why each boundary exists / why not merged / why not split further:**

- **Identity vs everything.** *Exists* to own tenancy/authz at one seam (INV-10). *Not merged* into services that consume claims — that would scatter isolation enforcement. *Not split* (auth vs users) at this scale — one small aggregate cluster.
- **Candidate vs Evaluation.** *Exists* because a candidate is durable and cross-campaign (INV-7) while an evaluation is per-campaign. *Not merged* — merging would tie a person's lifetime record to a single campaign's lifecycle (breaks afterlife/portability). *Not split* (identity vs intake) — intake is just how a candidate enters; same aggregate.
- **Campaign vs Evaluation.** *Exists* because the Campaign is the organizing set (owns fairness scope, roster, calibration freeze) while each Candidate Evaluation is a separate aggregate (ARCH-03 §3.0, AD-16). *Not merged* — that would recreate the "120 candidates in one giant aggregate" consistency problem. *Not split* — Campaign's own concerns (lifecycle/roster/calibration) cohere.
- **Evaluation vs Intelligence Compute.** *Exists* to separate authoritative state (must be consistent, one writer) from stateless inference (must scale/fail independently). *Not merged* — inference bursts would contend with transactional consistency and couple failure domains. *Not split further* (no separate Evidence/Recommendation services) — those are **intra-aggregate** responsibilities (ARCH-04 AD-23); splitting them would create chatty distributed calls inside one consistency boundary and invite distributed transactions. **This is the single most important "do not over-decompose" boundary.**
- **Integrity vs Fairness vs Consent vs Audit (four separate gates).** *Exist* separately because each is an independent authoritative failure domain that must fail *closed* without taking the others down; each has a distinct scope (evidence / campaign-set / candidate / everything). *Not merged* into one "Trust service" — a single trust service is a single point of failure for all four gates, and couples their very different scaling and data. *Not split further* — each is already a single responsibility.
- **Decision vs Feedback vs Export (three BC-5 services).** *Exist* separately: Decision is the human-accountable, immutable core (Critical); Feedback is candidate-facing and release-gated (brand-critical, different consumers); Export is the outward boundary. *Could be co-deployed at MVP* (AD-41) since they're low-risk and co-changing, but kept as distinct logical services because their authority, consumers, and availability tiers differ. *Not merged permanently* — Decision's accountability must not share a failure domain with Export's outward I/O.
- **Notification vs Feedback.** *Exists* separately because Notification is transactional messaging (no release gate) while Feedback carries the recruiter-release rule and candidate-view content. *Not merged* — a notification outage must never block or leak candidate feedback.

---

## 4. Communication Model

Two transport styles, chosen by **what the interaction is** (ARCH-04) and **whether it needs an answer now**:

| Style | Mechanism (proposed) | When appropriate | Examples |
|---|---|---|---|
| **Synchronous command** | internal RPC (gRPC), mTLS | Immediate-consistency gate checks and user-initiated actions needing an immediate result/rejection | `isConsentActive` (Consent), `verifyIntegrity` (Integrity), record decision (Decision) |
| **Synchronous query** | gRPC / read API; GraphQL/REST at the edge | Reading another service's state for a decision, with freshness needs | Evaluation reads calibration; Decision reads recommendation+explanation |
| **Asynchronous event (fact)** | durable, ordered, append-only log (event backbone) | Propagating **business facts** (ARCH-05); anything a consumer reacts to without the producer needing an answer | `EvaluationCompleted`, `FairnessApproved`, `HiringDecisionRecorded` |
| **Long-running workflow** | event choreography (default) + orchestration saga only where a process needs a coordinator | Multi-service business processes (ARCH-05 §7) | Candidate-evaluation → fairness → delivery; export |

**Rules of the model:**
- **Facts are events; requests are commands/queries.** This maps ARCH-05 exactly: a business fact is *always* an async event on the backbone (immutable, ordered, replayable → also the audit substrate). A request for someone to *do* something now is a synchronous command. Never model a fact as a command or vice-versa.
- **Prefer choreography; use orchestration sparingly.** Most processes advance by services reacting to facts (loose coupling). A saga *orchestrator* is introduced only where a process genuinely needs a single coordinator to track state and drive compensation (candidate-evaluation lifecycle is the main candidate — §5/§7).
- **Gates that must be immediate are synchronous** (consent, integrity-before-trust) so the fail-closed default is enforced in-band; **rules the business tolerates as eventual are events** (fairness gating delivery — ARCH-04 §8). *This is why we need almost no synchronous cross-service coupling: the immediate rules are intra-service, the eventual ones are events.*
- **Queries never cross a forbidden boundary** (ARCH-04 §2). E.g., no service exposes a query that would let a Recommendation reach a Candidate; the Candidate's only read is released feedback.
- **The edge** (API gateway) speaks REST/GraphQL to clients; **internal** traffic is gRPC over the mesh. Clients never talk to services directly.

---

## 5. Consistency Strategy

**The payoff of ARCH-03/04:** we sorted rules into *immediate* (must hold at the instant) and *delayed* (business tolerates a gap) in ARCH-04 §8. It is not a coincidence that **every immediate rule lives inside one aggregate — hence one service — and every cross-service rule is one the business already tolerates as eventual.** Therefore:

> ### AD-42 — No distributed transactions. Immediate consistency is always intra-service (local ACID); cross-service consistency is always eventual via events + sagas + compensation.
> We never use two-phase commit or a distributed transaction manager. If a proposed rule seems to need one, it is a signal the boundaries are wrong — re-derive from ARCH-03, don't reach for 2PC.

**Per cross-service business rule (from ARCH-04 CAR-1…8):**

| Rule | Consistency requirement | Coordination strategy | Failure behavior | Recovery |
|---|---|---|---|---|
| **CAR-1** RecommendationDelivered ⇐ campaign FairnessApproved | **Eventual** (Formed can precede; Delivered waits) | Choreography: Evaluation forms recommendation, holds; Fairness emits `FairnessApproved`; Evaluation reacts and delivers | If Fairness never approves (`FairnessHeld`): recommendations stay Formed, **held** (fail-closed) | On later `FairnessApproved`, held recommendations deliver; no data lost |
| **CAR-2** No evidence use without active consent | **Immediate** | Synchronous `isConsentActive` at the evidence boundary (in Evaluation) | Fail **closed**: no consent → no evidence recorded | `ConsentWithdrawn` event → Evaluation emits `EvaluationWithdrawn` (compensation) |
| **CAR-3** Every action audited | **Eventual (guaranteed, lossless)** | Transactional **outbox**: state + fact committed atomically, then relayed to backbone → Audit | If relay lags: fact still durable in outbox; no loss | Outbox relay resumes; Audit projects all facts in order |
| **CAR-4** One active evaluation per candidate per campaign | **Immediate** | Intra-service: Campaign roster is single owner/writer | Local uniqueness constraint | n/a (local) |
| **CAR-5** HiringDecision ⇐ RecommendationDelivered | **Immediate at decision time** | Decision synchronously verifies delivered recommendation exists before recording | Fail closed: no delivered rec → cannot record decision | n/a |
| **CAR-6** Export contains only fairness-passed, explained | **Eventual** | Export consumes only `RecommendationDelivered`/`HiringDecisionRecorded` facts | Missing preconditions → not assembled | Re-assemble when facts arrive |
| **CAR-7** Single-tenant everywhere | **Immediate, always** | Tenant claim propagated; every service authorizes + partitions by tenant | Fail closed on any cross-tenant access | n/a (invariant) |
| **CAR-8** Calibration frozen at Active binds all evaluations | **Immediate at freeze; then read-only** | Campaign freezes calibration in a local transaction; evaluations read the frozen version | Post-freeze writes rejected locally | n/a |

**The shape of the whole:** exactly **two** synchronous cross-service dependencies sit on the hot path (Consent check, Integrity verdict) — both gates, both fail-closed, both cacheable. Everything else advances by facts. That is a deliberately small synchronous surface.

---

## 6. Data Ownership

> ### AD-43 — One authoritative data boundary per service. No shared databases. Ever.
> Each service is the **sole writer** of its aggregate's data. Others obtain that data as **facts** (events) or via the owner's **query API** — never by reaching into its store.

| Concern | Rule |
|---|---|
| **Authoritative owner** | The service owning the aggregate (ARCH-03) owns its data outright. Integrity/Fairness own their verdicts; Consent owns consent; Audit owns the append-only ledger. |
| **Read models** | A consuming service that needs another's data builds a **local read model** by subscribing to facts (e.g., Decision maintains a read model of delivered recommendations; Export maintains one of decisions). Read models are **derived, disposable, and rebuildable** by replaying facts — never authoritative. |
| **Shared references** | Cross-service links are **by identity only** (ARCH-04 §5, AD-29): a service stores another aggregate's **ID**, not its content. Content is fetched via API or received via fact. |
| **Cross-service identity** | Global, opaque, tenant-scoped IDs (e.g., `CampaignId`, `CandidateEvaluationId`) minted by the owning service; IDs are stable, meaningless outside their owner, and never encode PII. |
| **Polyglot persistence** | Each service picks storage fit for its shape (transactional aggregates → relational; the fact log → an append-only/event store; work samples & resumes → object storage; future Evidence Graph → graph/vector, deferred). Chosen per service in ARCH-08. |
| **No cross-service joins** | Reporting/analytics read from **projections** off the fact stream (a read side), never by joining service databases. |

**Event backbone & the audit substrate.** Because facts are immutable and ordered (ARCH-05) and the log *is* the audit trail (AD-32), the backbone is modeled as a **durable, ordered, append-only log** partitioned by tenant+campaign. Core aggregates may be **event-sourced** where replay/audit value is highest (Evaluation, Decision, Consent, gates); others may persist state + emit facts via **outbox** (simpler, chosen per service in ARCH-08). Either way, **no fact is lost and none is mutated.**

---

## 7. Reliability Architecture

Grounded in ARCH-04 §9 (gates fail *closed*, intelligence fails *soft*) and ARCH-01 (degrade to less-confidence/more-human, never wrong-or-unfair).

| Mechanism | Decision |
|---|---|
| **Timeouts** | Every synchronous call has a strict deadline (propagated via gRPC deadlines). A gate call that times out ⇒ **hold** (fail closed). An Intelligence Compute call that times out ⇒ **low confidence / escalate to human** (fail soft). |
| **Retries** | Only for **idempotent** operations, with exponential backoff + jitter and a bounded budget. Gates: retry then hold. Compute: retry then degrade. Never retry a non-idempotent command blindly. |
| **Circuit breakers** | Service-mesh circuit breakers on every dependency. Open breaker on a gate ⇒ hold; on Compute ⇒ degrade to human; on Notification ⇒ queue and continue (non-critical). |
| **Idempotency** | Every command carries an **idempotency key**; every event a stable **event ID**. Consumers dedupe by ID. Compute results are idempotent by **input content hash** (same work sample → same evaluation reference), which also caches cost. |
| **Duplicate events** | **At-least-once delivery assumed.** All consumers are **idempotent** (dedupe by event ID + effect check). Producing a fact twice must never produce two truths. |
| **Poison messages** | Bounded retries, then route to a **dead-letter** channel with full context; a poison business fact **never blocks the ordered stream** for other keys (per-key isolation). |
| **Dead-letter** | DLQ per consumer with alerting and a governed replay tool. A dead-lettered *gate* fact escalates (a held candidate must not be silently stuck — surfaced to ops + recruiter). |
| **Outbox** | Transactional outbox is the **standard** pattern: aggregate state and its emitted fact commit in one **local** transaction; a relay publishes to the backbone. This is how we get atomic "state changed ⇒ fact exists" **without** distributed transactions (AD-42). |
| **Saga** | Long-running processes (§5) advance by **choreography**; a saga **orchestrator** is used only for the candidate-evaluation lifecycle and export, to own compensation state (`EvaluationWithdrawn`, `ExportFailed`). Compensation is **forward-only** business facts (ARCH-05 §8), never rollback. |
| **Compensation** | Realizes ARCH-05 §8: impossibility ⇒ a new compensating fact. No event is deleted; the saga emits the compensating fact and stops the chain. |
| **"Exactly-once" myth** | We explicitly reject exactly-once *delivery* as a fiction over an unreliable network. We achieve **effectively-once *processing*** = at-least-once delivery + idempotent consumers + dedupe. **(AD-44.)** |
| **Degradation philosophy** | Codified: **gates degrade to HOLD; intelligence degrades to LOW-CONFIDENCE + HUMAN; delivery degrades to STAY-IN-PLATFORM.** The system is allowed to be *slower* or *more manual*; it is never allowed to be *wrong or unfair* (ARCH-01). |

---

## 8. Scalability

| Concern | Decision |
|---|---|
| **Independent scaling** | Each service scales on its own signal (§2.14). No service is scaled to satisfy another's load. |
| **AI-heavy workloads** | Intelligence Compute is the primary scaling axis: **horizontal worker pools per model**, autoscaled on **queue depth** (KEDA), not CPU — because the bottleneck is inference latency/token throughput, not local CPU. Burst-capable (spot/preemptible) since work is idempotent and retryable. |
| **Horizontal scaling** | All services stateless at the request tier; state in the owned datastore. Scale out, not up. Tenant+campaign partitioning gives natural sharding keys. |
| **Caching** | Read-through caches for hot reads: authz claims (Identity), **consent status** (short TTL + event invalidation on `ConsentWithdrawn`), calibration (immutable post-freeze → cache freely). Compute results cached by input hash (cost + latency). |
| **Back-pressure** | Compute requests flow through a bounded work queue; when depth exceeds threshold, producers see back-pressure and the business **degrades gracefully** (queue rather than drop; surface "evaluation in progress"). Never silently drop a candidate's work. |
| **Queue depth** | The core autoscaling and health signal for the async tier; sustained growth triggers scale-out then alert; a hard ceiling triggers admission control (new campaigns queue) rather than collapse. |
| **Worker pools** | Segmented by model/capability and by **tenant tier** (so one tenant's bulk import can't starve another — fairness of *service*, mirroring fairness of *product*). |
| **Burst handling** | Import and invitation bursts absorbed by async intake + queue; evaluation bursts absorbed by Compute autoscaling; delivery is naturally paced by the (human) decision step. |

---

## 9. Observability

| Concern | Decision |
|---|---|
| **Logging** | Structured, tenant-tagged, PII-minimized logs (never log candidate PII or raw work-sample content). Centralized aggregation. |
| **Tracing** | OpenTelemetry distributed tracing across every hop (edge → services → Compute → LLM boundary). Every gate decision is a span with its verdict. |
| **Metrics** | RED/USE per service (rate/errors/duration; utilization/saturation/errors); queue depth and Compute token-cost as first-class metrics. |
| **Business metrics** | Facts (ARCH-05) are the source of truth for business observability: time-to-recommendation, held-by-fairness rate, override rate, feedback-release latency, candidate completion rate. These derive from the fact stream, not ad-hoc instrumentation. |
| **Audit correlation** | Every fact carries tenant, campaign, candidate-evaluation, actor, and a **correlation ID**; the Audit projection and traces share these IDs, so any decision is reconstructable end-to-end (explainability at the ops layer). |
| **Distributed correlation IDs** | A correlation ID is minted at the edge and propagated through every sync call and onto every emitted fact; business IDs (CampaignId, CandidateEvaluationId) are first-class trace attributes. |
| **Health model** | Liveness (process up) vs **readiness** (dependencies + gates reachable) vs **business health** (are candidates progressing? is anything stuck held/dead-lettered?). A "held" candidate that never resolves is a business-health alert, not just an error. |

---

## 10. Security

Anchored in DOC-05 Tier-0 (isolation, consent, privacy) and ARCH-01 trust boundaries.

| Concern | Decision |
|---|---|
| **Authentication** | Clients authenticate at the edge via OIDC/OAuth2 (external IdP/SSO). No service authenticates end-users itself. |
| **Authorization** | Tenant + role claims resolved by Identity; every service enforces authorization on every request (no ambient trust). Interaction legality (ARCH-04 §2) is enforced in code, not assumed. |
| **Tenant isolation** | **Zero cross-tenant access by construction** (INV-10): tenant claim mandatory on every call and fact; data partitioned by tenant; queries scoped by tenant at the data layer (row-level security / per-tenant keys). Cross-tenant access is a hard fail + security alert. |
| **Encryption** | TLS in transit at the edge; **mTLS between all internal services** (zero trust — no implicit trust from network position). Encryption at rest (envelope encryption via KMS) for all stores; per-tenant data keys where feasible. |
| **Secrets** | Central secrets manager / Vault; short-lived, rotated credentials; no secrets in images, env files, or code. |
| **PII protection** | **The LLM edge is the sharpest boundary** (ARCH-01). Intelligence Compute **minimizes PII before any external model call** (strip/pseudonymize identity; send only role-relevant content); PII never in logs/traces; retention per consent (ARCH-05 §10.3). |
| **Zero trust** | Every internal call authenticated (mTLS + service identity) and authorized; a compromised service cannot impersonate another or cross tenants. |
| **Internal service authentication** | Workload identities (SPIFFE/SVID via the mesh); service-to-service calls carry both the workload identity and the propagated tenant/user context; gates verify caller identity before honoring a request. |

> ### AD-45 — Zero-trust internal networking (mTLS + workload identity) and PII minimization at the LLM edge are mandatory, not optional hardening.
> Because a single cross-tenant leak or a PII-to-LLM exposure is an existential trust failure (RK-6/RK-9), these are day-one requirements, not backlog items.

---

## 11. Deployment

| Concern | Decision (proposed; reversible per AD-41) |
|---|---|
| **Containers** | All services containerized; immutable images; SBOM + image scanning in CI. |
| **Orchestration** | Kubernetes. Namespaces per environment; the four gates + Intelligence Compute in dedicated node pools/failure domains (AD-41). |
| **Autoscaling** | HPA for request-tier services; **KEDA (queue-depth)** for Intelligence Compute and async consumers; cluster autoscaler for nodes; GPU/accelerator pools for inference where used. |
| **Blue/Green** | For stateful gate/decision services where instant rollback matters most. |
| **Canary** | Progressive delivery (Argo Rollouts / Flagger) for core services; canary analysis on business + RED metrics before promotion; **gates get the most conservative rollout** (a bad fairness/integrity deploy is a Tier-0 incident). |
| **Service discovery** | Kubernetes DNS + service mesh (Istio/Linkerd) for discovery, mTLS, retries, circuit breaking, and traffic shifting. |
| **Configuration** | GitOps (declarative, versioned, auditable — config changes are themselves auditable, echoing P8). Per-tenant config isolated. |
| **Secrets** | External secrets operator → Vault/cloud secrets; never in manifests. |

> ### AD-46 — Cloud-agnostic core, managed where it de-risks.
> Kubernetes + open standards (OTel, OIDC, mTLS) keep the core portable (echoing "domain stable across re-platforming"); managed services (event backbone, datastores, KMS) are used where they reduce ops burden, isolated behind the service's own boundary so they remain swappable. Concrete provider selection deferred to a deployment/infra decision doc.

---

## 12. Architecture Decision Record

| ID | Decision | Rationale (short) |
|---|---|---|
| **AD-40** | Platform SHALL be microservices | Independent AI scaling, gate fault-isolation, LLM/PII containment; seams already proven (ARCH-01→05) |
| **AD-41** | Boundaries fixed; MVP co-deployment permitted (gates + Compute always separate) | Capture monolith's early simplicity without forfeiting seams; spend runway on AS-1 |
| **AD-42** | No distributed transactions; immediate=intra-service ACID, cross-service=eventual (events+sagas+compensation) | The immediate rules are already intra-aggregate; 2PC signals a wrong boundary |
| **AD-43** | One authoritative data boundary per service; no shared DBs; read models via facts | Shared data = ownerless invariant = spaghetti at the data tier |
| **AD-44** | Reject exactly-once delivery; achieve effectively-once processing (at-least-once + idempotent consumers) | Exactly-once delivery is a network fiction |
| **AD-45** | Zero-trust internal (mTLS + workload identity) + PII minimization at LLM edge, day one | A single cross-tenant/PII leak is existential |
| **AD-46** | Cloud-agnostic core; managed services behind service boundaries | Portability + reduced ops, swappable |
| **AD-47** | Intelligence Compute owns no aggregate and emits no authoritative fact | AI never *becomes* business truth; an owner always validates/commits (ARCH-05 AD-35) |
| **AD-48** | Facts→async events on a durable ordered log (also the audit substrate); requests→sync commands/queries | Direct mapping of ARCH-05; log = audit (AD-32) |
| **AD-49** | Gates (Consent/Integrity/Fairness/Audit) are separate Critical services, each fail-closed | Independent failure domains; a gate must be *held*, never skipped |
| **AD-50** | Degradation is codified: gates→hold, intelligence→low-confidence+human, delivery→stay-in-platform | Never wrong-or-unfair (ARCH-01) |

## 13. Risks

- **Campaign as chokepoint/coupling** (carried from ARCH-02/04): the organizing hub sees many flows. *Mitigation:* Campaign owns *coordination facts* only, not evaluation content; per-candidate work lives in Evaluation; watch its fan-in.
- **Over-decomposition creep:** pressure to split Evaluation's internal steps (evidence/recommendation) into services would reintroduce distributed transactions. *Mitigation:* AD-23/§3 forbid it; enforce in review.
- **Operational burden vs team size:** 13 services + mesh + backbone is heavy for an early team. *Mitigation:* AD-41 co-deployment; invest in platform/CI before breadth.
- **Eventual-consistency confusion for gates:** engineers may "optimize away" the Formed→Delivered fairness wait under pressure (RK-6/RK-15). *Mitigation:* EV-INV-7 enforced in Evaluation; delivery physically gated on the `FairnessApproved` fact; canary/tests assert it.
- **LLM boundary is the top risk** (ARCH-01 unchanged): cost blow-ups, latency, PII exposure, provider outage. *Mitigation:* Compute isolation, PII minimization (AD-45), content-hash caching, multi-provider abstraction, fail-soft to human.
- **Dead-lettered gate facts stranding candidates:** a poison fact could leave a candidate silently held. *Mitigation:* held/DLQ business-health alerts (§9); no silent stalls (DOC-06 no-black-hole).
- **Distributed debugging difficulty:** correctness bugs span services. *Mitigation:* end-to-end tracing + correlation on the fact stream (§9); the immutable log makes replay/repro possible.

## 14. Future Evolution

- **Post-MVP core capabilities** (Hiring Memory, Benchmarking, Outcome Learning, Evidence Graph, Talent Pool) become **new services** consuming the existing fact stream — no change to current services (facts are already emitted). This is the compounding-moat path, unlocked by the event backbone.
- **ATS integrations** (deferred, AD-11): add integration adapters at the Candidate/Export edges without touching the core (the core never assumed an ATS — INV-9). *Every such integration passes through an **Anti-Corruption Layer** so no external domain model leaks into the canonical domain (ARCH-03); this principle is committed and formalized as **AD-52 in ARCH-07**. (ARCH-06 is frozen; its ADR ends at AD-50, so the authoritative ACL decision is recorded in ARCH-07 to avoid a numbering collision.)*
- **Read-side/analytics** and the future Evidence Graph are **projections** off the fact log; add freely without impacting write paths.
- **Splitting co-deployed MVP modules** (AD-41) into fully independent deployments is an ops migration along pre-existing seams — no domain change.
- **Multi-region / data residency** (DOC-01 global-ready): tenant+campaign partitioning and per-tenant keys are the substrate; residency routing added at the edge and data layer later.
- **Sensor expansion** (voice/adaptive/live — deferred beyond AD-10): new sensors plug into Evidence collection and Intelligence Compute as new capabilities; the Candidate Evaluation aggregate and its facts are unchanged.

---

## Open Questions *(feed ARCH-07 / ARCH-08)*

1. **Event-sourcing scope:** which services are fully event-sourced vs state+outbox? (Lean: gates + Evaluation + Decision + Consent sourced; others outbox.) → ARCH-08.
2. **Fairness trigger point** (carried from ARCH-05 OQ-1): full-set vs interim verdict — determines whether Fairness runs once per campaign or rolls. Affects saga design.
3. **Consent-withdrawal vs in-flight evaluation** (carried): does `ConsentWithdrawn` force `EvaluationWithdrawn` mid-flight, and what of already-immutable evidence? → policy + saga compensation.
4. **Integrity outcome as field vs distinct `IntegrityFlagged` fact** (carried from ARCH-05 OQ-3) → affects Integrity Service API + EV-INV-5.
5. **Backbone technology** (log choice) and **datastore per service** → ARCH-08.
6. **Synchronous consent check vs replicated consent read-model** on the hot path — latency vs freshness tradeoff. → ARCH-07/08.

## Deferred to later ARCH docs

- **API contracts** (schemas, versioning of commands/queries/events) → **ARCH-07**.
- **Database architecture** (per-service stores, event store, projections, retention/WORM) → **ARCH-08**.
- **AI orchestration internals** (prompting, model routing, evaluation-engine mechanics) → AI Orchestration / Evaluation Engine docs.
- **Concrete cloud provider & infra** (managed service selection, regions) → deployment/infra doc.

---

*End of ARCH-06 v0.1 — the Distributed System Architecture. The business model, deployed: thirteen services whose boundaries are the business's boundaries (ARCH-03), whose conversations are the legal interactions (ARCH-04), and whose messages are the business facts (ARCH-05). No arbitrary services, no distributed transactions, gates fail closed, intelligence fails soft. Next: ARCH-07 — API Contracts, deriving the concrete command/query/event contracts from the interactions (ARCH-04) and facts (ARCH-05) named here.*
