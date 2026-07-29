# ARCH-05 — Business Event Model

| Field | Value |
|---|---|
| **Document ID** | ARCH-05 |
| **Title** | Business Event Model (the facts of the business) |
| **Owner** | Principal Software Architect + DDD Event-Modeling lead |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture |
| **Depends on** | ARCH-04 (Domain Interaction Model — frozen), ARCH-03 (Canonical Domain Model), ARCH-02 (Logical Business Architecture), ARCH-01 (Context), DOC-05 (gates), DOC-04 (vocabulary) |
| **Blocks** | ARCH-06 (Microservice Architecture — event ownership becomes service seams), ARCH-07 (API Contracts), ARCH-08 (Database Architecture) |
| **The one question** | **"What has become true in the business — and in what order can truth accumulate?"** |
| **Canonical status** | **This is the single source of truth for business facts.** No future service, message, table, or API may assert a fact this document does not define, nor claim one out of the order this document forbids. |
| **ABSOLUTELY FORBIDDEN** | Kafka · RabbitMQ · Azure Service Bus · Google Pub/Sub · REST · HTTP · Webhooks · Microservices · Queues · Topics · Partitions · Serialization · JSON · Avro · Protobuf · Cloud · Infrastructure · Programming languages · Frameworks · Any technology. **This document defines only business facts.** |

---

## 0. The distinction this document is built on

An event, here, is **not a message**. It is a **business fact**: *something that became true in the business and stays true.*

- `CandidateInvited` does not mean "send an invitation." It means **"from this instant, this candidate is officially invited"** — a permanent truth about the world.
- `FairnessApproved` does not mean "run the fairness check." It means **"this campaign's evaluations have satisfied the fairness gate"** — and that remains a fact regardless of whether anything ever reacts to it.

This distinction is load-bearing for everything after it:

1. **Facts have natural owners.** A fact is *about* something (a campaign, a candidate, a decision); whoever owns that thing owns the fact. In ARCH-06, **fact ownership becomes the seam between microservices** — which is exactly why the CTO's sequence (business → domain → interaction → **facts** → services) produces boundaries that reflect the business, not arbitrary technical splits.
2. **Facts are immutable.** The past cannot change. A fact, once true, is never edited or deleted; if the world moves on, a **new** fact records that (§8 compensation). This is also why the business event log is the natural backbone of the audit trail (§10).
3. **Facts record that rules were satisfied — they never define rules.** `RecommendationDelivered` can only come into existence *because* the rules in ARCH-04 (Explanation attached ∧ Fairness approved) were already satisfied. The event is the **receipt**, not the **rule**. The rule lives in ARCH-03/ARCH-04; the event merely testifies that it held. **(AD-30.)**
4. **Technology will transport them later.** Whether a fact is later carried by a log, a bus, a table, or a phone call is an ARCH-06+ concern. The fact itself is technology-independent and must remain valid across any re-platforming.

---

## 1. Event Philosophy

- **Events describe facts, not requests.** Every event name is **past tense** and asserts a completed truth (`EvidenceRecorded`, not `RecordEvidence`). If a proposed event reads like an instruction, it is a command masquerading as an event and does not belong here.
- **Events are immutable.** A recorded fact is never mutated or retracted. Reversal is expressed only by a later, compensating fact (§8). This is why events can safely be the substrate of audit and of downstream learning: history is stable.
- **Events belong to the business language.** Every event is expressed entirely in DOC-04 vocabulary. There is no event whose meaning requires technical explanation. A recruiter, a lawyer, and an engineer read `RecommendationDelivered` identically.
- **Technology will later transport them.** Transport, ordering guarantees, delivery semantics, and storage are deferred to ARCH-06+. Nothing here assumes any of them.
- **Events never define business rules; they record that rules have been satisfied.** The gates (fairness, integrity, consent, explanation, human accountability) are defined in the Constitution and enforced in the interaction model. The event is the immutable evidence that the gate was passed at a point in time — the *proof*, not the *law*.

> **The test for whether something is a business event:** *Could a domain expert point at it and say "yes, that became true, and it will always have been true"?* If yes, it is a fact and belongs here. If it is really "a component asked another component to act," it is an interaction (ARCH-04) or a future message (ARCH-06), not a business event.

---

## 2. Event Taxonomy

Events are grouped by the **aggregate/context whose truth they assert** (ARCH-03). Grouping by owner — not by workflow phase — is deliberate: it is what makes ownership (and later, service boundaries) fall out naturally.

| Category | Owning context / aggregate | Why these belong together | Events |
|---|---|---|---|
| **Organization** | BC-1 / Organization | Facts about who exists and who may act — the tenant frame every other fact sits inside. | OrganizationProvisioned · UserAccessGranted · UserAccessRevoked |
| **Campaign** | BC-4 / Evaluation Campaign | Facts about the Unit of Work's existence, readiness, and closure. | CampaignCreated · CampaignActivated · CampaignConcluded · **CampaignCancelled** |
| **Candidate** | BC-2 / Candidate (+ intake) | Facts about a person entering and participating in the network. | CandidateImported · CandidateInvited · **InvitationExpired** · **InvitationRevoked** |
| **Consent (Trust)** | BC-6 / Consent | Facts about the candidate's governing permission — the gate ahead of all data use. | ConsentRequested · ConsentGranted · **ConsentWithdrawn** · **ConsentExpired** |
| **Evidence** | BC-4 / Candidate Evaluation (+ BC-6 integrity) | Facts about genuine, authenticity-checked ability being captured. | WorkSampleSubmitted · EvidenceRecorded · IntegrityVerified |
| **Evaluation** | BC-4 / Candidate Evaluation | Facts about evidence becoming explainable judgment. | EvaluationCompleted · **EvaluationWithdrawn** |
| **Trust (Fairness)** | BC-6 / Fairness Assessment (campaign-scoped) | Facts about the campaign satisfying (or being held by) the fairness gate. | FairnessApproved · **FairnessHeld** |
| **Recommendation** | BC-4 / Candidate Evaluation | Facts about advisory conclusions forming and being delivered. | RecommendationFormed · RecommendationDelivered · **RecommendationSuperseded** |
| **Decision** | BC-5 / Hiring Decision | Facts about the accountable human choice. | HiringDecisionRecorded |
| **Feedback** | BC-5 / Feedback | Facts about candidate-facing feedback being released and delivered. | FeedbackReleased · FeedbackDelivered |
| **Export** | BC-5 / Export Package | Facts about hiring intelligence crossing the product boundary back to the customer. | ExportAssembled · ExportDelivered · **ExportFailed** |

*(Bold = compensating facts, §8.)*

> **Note on Audit and Confidence.** There is deliberately **no** `AuditRecorded` event and **no** `ConfidenceCalculated` event. Audit is not a business fact *alongside* the others — **the set of all these events *is* the audit trail** (§10); an "audit event" would be circular. And Confidence is an *attribute* of `EvaluationCompleted`, not a milestone of its own (see AD-31). Modeling discipline: we admit only facts a domain expert would recognize as having "become true," not internal computations.

---

## 3. Business Event Catalog

*For each: Business Meaning · Triggered By · Business Preconditions · Business Consequences · Affected Aggregate · Affected Context · Canonical Payload (business fields only — identities and business values; no serialization, no technical fields).* Payloads reference other facts/entities **by identity** (ARCH-04 §5) and carry an **occurred-at** business time and the **accountable actor** where a human or authority is responsible.

### 2.1 Organization

**OrganizationProvisioned**
- *Meaning:* A customer tenant now exists and may operate.
- *Triggered by:* Platform onboarding (Admin).
- *Preconditions:* None (root fact).
- *Consequences:* Users may be granted access; campaigns may later be created within this tenant.
- *Aggregate / Context:* Organization / BC-1.
- *Payload:* OrganizationId · OrganizationProfile · occurred-at.

**UserAccessGranted / UserAccessRevoked**
- *Meaning:* A named person may / may no longer act within the tenant with stated permissions.
- *Triggered by:* Org Admin.
- *Preconditions:* OrganizationProvisioned.
- *Consequences:* The user may (or may not) initiate the commands their permissions allow (ARCH-04 §4).
- *Aggregate / Context:* Organization(User) / BC-1.
- *Payload:* OrganizationId · UserId · PermissionSet · granting-actor · occurred-at.

### 2.2 Campaign

**CampaignCreated**
- *Meaning:* An Evaluation Campaign for one Role now exists in Draft.
- *Triggered by:* Recruiter (ARCH-04 A1).
- *Preconditions:* OrganizationProvisioned; a Role Reference is present.
- *Consequences:* Candidates may be imported; Calibration may be set.
- *Aggregate / Context:* Evaluation Campaign / BC-4.
- *Payload:* CampaignId · OrganizationId(tenant) · RoleReference · creating-actor · occurred-at.

**CampaignActivated**
- *Meaning:* The campaign is live; **Calibration is now frozen** (INV-c) and evaluation may begin.
- *Triggered by:* Recruiter (ARCH-04 A3).
- *Preconditions:* CampaignCreated; Calibration set; candidate roster established.
- *Consequences:* Candidates may be invited; the frozen bar governs every evaluation in the campaign.
- *Aggregate / Context:* Evaluation Campaign / BC-4.
- *Payload:* CampaignId · frozen-CalibrationReference · activating-actor · occurred-at.

**CampaignConcluded**
- *Meaning:* The campaign's evaluation work is complete and closed; **its evidence is now permanently immutable and historical** (AD-09).
- *Triggered by:* Campaign (ARCH-04), after fairness and delivery.
- *Preconditions:* FairnessApproved for the campaign; all in-scope recommendations delivered or accounted for.
- *Consequences:* No new evaluation activity; results available for export; future capabilities may *reference* but never modify.
- *Aggregate / Context:* Evaluation Campaign / BC-4.
- *Payload:* CampaignId · conclusion-summary(references) · occurred-at.

**CampaignCancelled** *(compensation)*
- *Meaning:* The campaign ended without normal conclusion.
- *Triggered by:* Recruiter.
- *Preconditions:* Campaign not already Concluded.
- *Consequences:* In-flight evaluations withdrawn; candidates communicated to (Recovery Moment, DOC-11); no recommendations delivered from a cancelled campaign.
- *Aggregate / Context:* Evaluation Campaign / BC-4.
- *Payload:* CampaignId · reason · cancelling-actor · occurred-at.

### 2.3 Candidate

**CandidateImported**
- *Meaning:* An already-applied person is now a candidate participant in this tenant/campaign (product boundary begins — KD-12.7).
- *Triggered by:* Recruiter (CSV + resume — AD-11) (ARCH-04 A2).
- *Preconditions:* CampaignCreated; **consent posture established** for lawful processing.
- *Consequences:* The candidate may be invited; a Candidate Evaluation may be opened.
- *Aggregate / Context:* Candidate / BC-2.
- *Payload:* CandidateId · CampaignId · minimal-ContactInfo · source(import) · occurred-at.

**CandidateInvited**
- *Meaning:* **From this point on, this candidate is officially invited to be evaluated.**
- *Triggered by:* Campaign on activation (ARCH-04 A4).
- *Preconditions:* CampaignActivated; CandidateImported; **ConsentGranted** (or consent gate satisfied); honest AI disclosure attached (A1, DOC-06).
- *Consequences:* The candidate may submit a work sample; an Invitation lifecycle begins (may later expire/revoke).
- *Aggregate / Context:* Candidate Evaluation (Invitation) / BC-4.
- *Payload:* CandidateId · CampaignId · CandidateEvaluationId · InvitationWindow(TimeWindow) · occurred-at.

**InvitationExpired / InvitationRevoked** *(compensation)*
- *Meaning:* The invitation lapsed (window elapsed) or was withdrawn (recruiter/consent) before acceptance.
- *Triggered by:* Time (expiry) / Recruiter or ConsentWithdrawn (revoke).
- *Preconditions:* CandidateInvited; not yet accepted.
- *Consequences:* No evaluation proceeds for this invitation; candidate treated with dignity (no black hole — DOC-06).
- *Aggregate / Context:* Candidate Evaluation (Invitation) / BC-4.
- *Payload:* CandidateEvaluationId · reason · occurred-at.

### 2.4 Consent (Trust)

**ConsentRequested → ConsentGranted**
- *Meaning:* The candidate was asked for, and gave, governing permission for data use of stated scope.
- *Triggered by:* Platform (request) → **Candidate** (grant — the sole authority, ARCH-04 §6.3).
- *Preconditions:* CandidateImported; scope and retention window stated.
- *Consequences:* Evidence collection and evaluation may proceed **only** while consent is Granted (CAR-2).
- *Aggregate / Context:* Consent / BC-6.
- *Payload:* ConsentId · CandidateId · CampaignId · ConsentScope · RetentionWindow · granting-actor(candidate) · occurred-at.

**ConsentWithdrawn / ConsentExpired** *(compensation)*
- *Meaning:* Permission ended — by candidate action (withdrawn) or by elapse of the retention window (expired).
- *Triggered by:* Candidate (withdraw) / Time (expire).
- *Preconditions:* ConsentGranted.
- *Consequences:* **All further use of candidate data halts** (fail-closed, ARCH-04 §9); interplay with already-recorded immutable evidence per Open Question OQ-2.
- *Aggregate / Context:* Consent / BC-6.
- *Payload:* ConsentId · CandidateId · reason · occurred-at.

### 2.5 Evidence

**WorkSampleSubmitted**
- *Meaning:* The candidate has submitted their structured work sample (the MVP Sensor — AD-10).
- *Triggered by:* Candidate (ARCH-04 A5).
- *Preconditions:* CandidateInvited (accepted); ConsentGranted.
- *Consequences:* Evidence may be recorded from the submission.
- *Aggregate / Context:* Candidate Evaluation (Work Sample) / BC-4.
- *Payload:* CandidateEvaluationId · WorkSampleId · submission-reference · occurred-at.

**EvidenceRecorded**
- *Meaning:* Discrete, **immutable** Evidence Item(s) of ability now exist (INV-b).
- *Triggered by:* Candidate Evaluation (ARCH-04 A6).
- *Preconditions:* WorkSampleSubmitted; ConsentGranted; role-relevance.
- *Consequences:* Evidence may be integrity-verified; nothing may mutate it thereafter.
- *Aggregate / Context:* Candidate Evaluation (Evidence Item) / BC-4.
- *Payload:* CandidateEvaluationId · EvidenceItemId(s) · EngineeringDimension refs · occurred-at.

**IntegrityVerified**
- *Meaning:* The authenticity of the evidence has been assessed; an **Integrity Score** is now a fact about it (authoritative, un-overridable).
- *Triggered by:* Integrity Verification authority (ARCH-04 A7).
- *Preconditions:* EvidenceRecorded.
- *Consequences:* If integrity holds, evaluation may proceed on trusted evidence; if low, the evidence is flagged and cannot be silently trusted (fail-closed).
- *Aggregate / Context:* Candidate Evaluation (Evidence) / BC-6 authority.
- *Payload:* EvidenceItemId(s) · IntegrityScore · verdict(trusted/flagged) · occurred-at.

### 2.6 Evaluation

**EvaluationCompleted**
- *Meaning:* Integrity-checked evidence has become an explainable **Evaluation**, carrying an Evaluation Score **and its Confidence** (INV-5/6). *(Confidence is part of this fact, not a separate event — AD-31.)*
- *Triggered by:* Candidate Evaluation (ARCH-04 A8).
- *Preconditions:* IntegrityVerified (trusted evidence); frozen Calibration read (CampaignActivated).
- *Consequences:* A Recommendation may be formed; the evaluation contributes to the campaign's fairness assessment set.
- *Aggregate / Context:* Candidate Evaluation (Evaluation) / BC-4.
- *Payload:* CandidateEvaluationId · EvaluationId · EvaluationScore · Confidence · cited-EvidenceReferences · CalibrationReference · occurred-at.

**EvaluationWithdrawn** *(compensation)*
- *Meaning:* An evaluation was retracted (e.g., consent withdrawn, integrity failure surfaced, campaign cancelled) before delivery.
- *Triggered by:* Candidate Evaluation, on a blocking compensation.
- *Preconditions:* EvaluationCompleted; not yet part of a delivered recommendation.
- *Consequences:* No recommendation is delivered from it; the withdrawal is itself a permanent fact.
- *Aggregate / Context:* Candidate Evaluation / BC-4.
- *Payload:* CandidateEvaluationId · reason · occurred-at.

### 2.7 Trust (Fairness) — campaign-scoped

**FairnessApproved**
- *Meaning:* **The campaign's evaluations have satisfied the fairness gate** — no unjustified adverse impact across the candidate set (INV-3). A campaign-level fact.
- *Triggered by:* Fairness Assessment authority, invoked by the Campaign across its set (ARCH-04 A9).
- *Preconditions:* Sufficient EvaluationCompleted facts across the campaign's set (the fairness trigger point — OQ-1).
- *Consequences:* Recommendations in this campaign **may now be delivered** (unblocks RecommendationDelivered).
- *Aggregate / Context:* Evaluation Campaign (Fairness Verdict) / BC-6 authority.
- *Payload:* CampaignId · FairnessVerdict(Passed) · assessed-set-reference · occurred-at.

**FairnessHeld** *(compensation / gate outcome)*
- *Meaning:* The campaign did **not** pass fairness; delivery is held pending review.
- *Triggered by:* Fairness Assessment authority.
- *Preconditions:* Fairness assessed; adverse impact or insufficiency detected.
- *Consequences:* **No RecommendationDelivered may exist for this campaign** until a later FairnessApproved; human review initiated.
- *Aggregate / Context:* Evaluation Campaign / BC-6 authority.
- *Payload:* CampaignId · FairnessVerdict(Hold) · reason · occurred-at.

### 2.8 Recommendation

**RecommendationFormed**
- *Meaning:* An advisory recommendation now exists for the candidate, with Explanation and Confidence attached (INV-2/6). **Formed ≠ delivered.**
- *Triggered by:* Candidate Evaluation (ARCH-04 A10).
- *Preconditions:* EvaluationCompleted; Explanation present.
- *Consequences:* Eligible for delivery **once** the campaign is FairnessApproved (legal "formed but not delivered, awaiting verdict" state — AD-28).
- *Aggregate / Context:* Candidate Evaluation (Recommendation) / BC-4.
- *Payload:* CandidateEvaluationId · RecommendationId · RecommendationLevel · ExplanationReference · Confidence · occurred-at.

**RecommendationDelivered**
- *Meaning:* The recommendation is now available to the human decision-maker — **the point at which advisory intelligence formally reaches the human.**
- *Triggered by:* Candidate Evaluation (ARCH-04 A11).
- *Preconditions:* RecommendationFormed; Explanation attached (INV-2); **campaign FairnessApproved (INV-3)**.
- *Consequences:* A HiringDecision may be recorded against it.
- *Aggregate / Context:* Candidate Evaluation (Recommendation) / BC-4.
- *Payload:* CandidateEvaluationId · RecommendationId · delivered-to(role) · occurred-at.

**RecommendationSuperseded** *(compensation)*
- *Meaning:* A re-evaluation produced a new recommendation; the prior one is superseded (never edited — INV-e).
- *Triggered by:* Candidate Evaluation on re-evaluation.
- *Preconditions:* A prior RecommendationFormed/Delivered exists.
- *Consequences:* The superseding recommendation follows the same gates before its own delivery.
- *Aggregate / Context:* Candidate Evaluation / BC-4.
- *Payload:* priorRecommendationId · newRecommendationId · reason · occurred-at.

### 2.9 Decision

**HiringDecisionRecorded**
- *Meaning:* **A named human made the accountable choice** to advance / hold / reject (INV-1). Immutable once recorded (INV-e).
- *Triggered by:* Human User — Hiring Manager (ARCH-04 A12).
- *Preconditions:* RecommendationDelivered; a human actor present; Override Justification if divergent from the recommendation.
- *Consequences:* Feedback may be released; the decision may be exported.
- *Aggregate / Context:* Hiring Decision / BC-5.
- *Payload:* HiringDecisionId · CandidateEvaluationId · RecommendationId · DecisionOutcome · deciding-actor(human) · OverrideJustification? · occurred-at.

### 2.10 Feedback

**FeedbackReleased**
- *Meaning:* A human recruiter authorized candidate-facing feedback for delivery (Rule 4).
- *Triggered by:* Human User — Recruiter (ARCH-04 A13).
- *Preconditions:* HiringDecisionRecorded (EV-INV-11).
- *Consequences:* Candidate-view feedback may be delivered.
- *Aggregate / Context:* Feedback / BC-5.
- *Payload:* FeedbackId · CandidateEvaluationId · releasing-actor · occurred-at.

**FeedbackDelivered**
- *Meaning:* The candidate has been given their candidate-view feedback (the most brand-defining moment — DOC-11).
- *Triggered by:* Feedback (ARCH-04 A13 responder).
- *Preconditions:* FeedbackReleased.
- *Consequences:* Candidate afterlife posture set (INV-7); nothing internal is exposed (P13).
- *Aggregate / Context:* Feedback / BC-5.
- *Payload:* FeedbackId · CandidateId · candidate-view-content-reference · occurred-at.

### 2.11 Export

**ExportAssembled → ExportDelivered**
- *Meaning:* Hiring intelligence for the campaign was packaged and then handed back across the product boundary (KD-12.7) — **the point at which our responsibility ends** (INV-9).
- *Triggered by:* Campaign / Recruiter (ARCH-04 A14).
- *Preconditions:* Contents are fairness-passed and explained (assemble); a valid destination for hand-back (deliver). Typically HiringDecisionRecorded and/or RecommendationDelivered for the packaged items.
- *Consequences:* Results are in the customer's hands; we never action the Offer.
- *Aggregate / Context:* Export Package / BC-5.
- *Payload:* ExportId · CampaignId · packaged-references(recommendations/decisions/explanations) · destination-ref · occurred-at.

**ExportFailed** *(compensation)*
- *Meaning:* Hand-back could not be completed as a business outcome.
- *Triggered by:* Export Package.
- *Preconditions:* ExportAssembled.
- *Consequences:* Results remain available in-platform (fail-safe/hold — ARCH-04 §9); a new export may be attempted; never a partial/misleading delivery.
- *Aggregate / Context:* Export Package / BC-5.
- *Payload:* ExportId · reason · occurred-at.

---

## 4. Event Timeline *(the complete happy-path lifecycle — ASCII)*

```
   OrganizationProvisioned
          │
   UserAccessGranted
          │
   CampaignCreated
          │
   CandidateImported ─────────────────────────────┐  (per candidate)
          │                                        │
   CampaignActivated  (Calibration frozen)         │
          │                                        │
   ConsentRequested → ConsentGranted               │
          │                                        │
   CandidateInvited ───────────────────────────────┤
          │                                        │
   WorkSampleSubmitted                             │
          │                                        │
   EvidenceRecorded  (immutable)                   │
          │                                        │
   IntegrityVerified  ⟦gate⟧                        │
          │                                        │
   EvaluationCompleted  (Score + Confidence)       │  ← contributes to the
          │                                        │     campaign fairness SET
   RecommendationFormed  (Explanation attached)    │
          │                                        │
          │        ┌───────────────────────────────┘
          ▼        ▼
   FairnessApproved  ⟦campaign-scoped gate⟧   ← assessed ACROSS the set
          │
   RecommendationDelivered   (only now — INV-3)
          │
   HiringDecisionRecorded    (human, accountable — INV-1)
          │
   FeedbackReleased          (recruiter authorizes — Rule 4)
          │
   FeedbackDelivered         (candidate-view only — P13)
          │
   ExportAssembled → ExportDelivered   (boundary ends — KD-12.7)
          │
   CampaignConcluded         (evidence now permanently historical — AD-09)
```

> **Read the fork carefully.** `RecommendationFormed` is **per candidate** and can occur for many candidates *before* `FairnessApproved`, which is **per campaign** and assessed across the whole set. `RecommendationDelivered` sits *after* the join — this is the timeline shape of ARCH-04's "gates immediate, aggregation delayed" doctrine (AD-28). The gap between Formed and Delivered is not a delay to optimize away; it is the business being correct.

---

## 5. Event Causality

*For each event: which earlier facts must already exist (**requires**), and which later facts it makes possible (**enables**).*

| Event | Requires (earlier facts) | Enables (later facts) |
|---|---|---|
| OrganizationProvisioned | — | UserAccessGranted; CampaignCreated |
| UserAccessGranted | OrganizationProvisioned | (all user-initiated commands) |
| CampaignCreated | OrganizationProvisioned | CandidateImported; CampaignActivated |
| CandidateImported | CampaignCreated; consent posture | ConsentRequested; CandidateInvited |
| CampaignActivated | CampaignCreated; Calibration set; roster | CandidateInvited (campaign-wide) |
| ConsentGranted | CandidateImported; ConsentRequested | CandidateInvited; WorkSampleSubmitted; EvidenceRecorded |
| CandidateInvited | CampaignActivated; CandidateImported; ConsentGranted | WorkSampleSubmitted; (InvitationExpired/Revoked) |
| WorkSampleSubmitted | CandidateInvited(accepted); ConsentGranted | EvidenceRecorded |
| EvidenceRecorded | WorkSampleSubmitted; ConsentGranted | IntegrityVerified |
| IntegrityVerified | EvidenceRecorded | EvaluationCompleted (if trusted) |
| EvaluationCompleted | IntegrityVerified(trusted); frozen Calibration | RecommendationFormed; contributes to FairnessApproved set |
| RecommendationFormed | EvaluationCompleted; Explanation | RecommendationDelivered (after FairnessApproved) |
| FairnessApproved | sufficient EvaluationCompleted across the set | RecommendationDelivered (all in campaign) |
| RecommendationDelivered | RecommendationFormed; Explanation; **FairnessApproved** | HiringDecisionRecorded |
| HiringDecisionRecorded | RecommendationDelivered; human actor | FeedbackReleased; ExportAssembled |
| FeedbackReleased | HiringDecisionRecorded | FeedbackDelivered |
| FeedbackDelivered | FeedbackReleased | (candidate afterlife) |
| ExportAssembled | fairness-passed, explained contents | ExportDelivered |
| ExportDelivered | ExportAssembled | CampaignConcluded |
| CampaignConcluded | FairnessApproved; deliveries accounted | (historical reference only) |

**Two dependency chains worth naming explicitly:**
- **The evidence-to-delivery chain (per candidate, joined by campaign fairness):** `ConsentGranted → WorkSampleSubmitted → EvidenceRecorded → IntegrityVerified → EvaluationCompleted → RecommendationFormed ─┤join├─ FairnessApproved → RecommendationDelivered`.
- **The human-accountability chain:** `RecommendationDelivered → HiringDecisionRecorded → FeedbackReleased → FeedbackDelivered` and `→ ExportDelivered`. Every link in this chain requires a **human** at the transition (INV-1, Rule 4).

---

## 6. Event Invariants *(event-ordering laws — facts may accumulate only in a legal order)*

These are **not** new business rules; they are the *observable ordering consequences* of ARCH-03/ARCH-04 rules. Each references the rule it testifies to.

- **EV-INV-1** — `CampaignActivated` never before `CampaignCreated`. *(§6.1)*
- **EV-INV-2** — `CandidateInvited` never before both `CampaignActivated` and `CandidateImported`. *(A4)*
- **EV-INV-3** — `WorkSampleSubmitted` / `EvidenceRecorded` never before `ConsentGranted` (and while consent remains Granted). *(CAR-2)*
- **EV-INV-4** — `IntegrityVerified` never before `EvidenceRecorded`. *(evidence chain)*
- **EV-INV-5** — `EvaluationCompleted` never before `IntegrityVerified` with a trusted verdict. *(INV-4)*
- **EV-INV-6** — `RecommendationFormed` never before `EvaluationCompleted` **and** an attached Explanation. *(INV-2, INV-a)*
- **EV-INV-7** — **`RecommendationDelivered` must never exist before `FairnessApproved`** (for its campaign). *(INV-3 — the flagship ordering law.)*
- **EV-INV-8** — `RecommendationDelivered` must never exist without an attached Explanation. *(INV-2)*
- **EV-INV-9** — **`HiringDecisionRecorded` must never exist before `RecommendationDelivered`.** *(CAR-5)*
- **EV-INV-10** — `HiringDecisionRecorded` must always carry a human actor; the system emits no such fact autonomously. *(INV-1)*
- **EV-INV-11** — **`FeedbackReleased` must never exist before `HiringDecisionRecorded`; `FeedbackDelivered` never before `FeedbackReleased`.** *(Rule 4)*
- **EV-INV-12** — `ExportDelivered` never before its packaged contents are fairness-passed and explained (and, for decided items, `HiringDecisionRecorded`). *(CAR-6, INV-9)*
- **EV-INV-13** — Every fact carries exactly one tenant and (where applicable) one campaign; no fact spans tenants. *(CAR-7, INV-10)*
- **EV-INV-14** — Every fact is immutable and append-only; no fact is edited or deleted — reversal is a **new** compensating fact (§8). *(INV-b/INV-e)*
- **EV-INV-15** — After `ConsentWithdrawn`/`ConsentExpired`, no *new* data-use fact (`WorkSampleSubmitted`, `EvidenceRecorded`, `EvaluationCompleted`) may occur for that candidate. *(CAR-2, fail-closed)*
- **EV-INV-16** — `FairnessHeld` blocks any `RecommendationDelivered` in its campaign until a subsequent `FairnessApproved`. *(INV-3)*

> **These ordering laws are what ARCH-06 must enforce across service boundaries.** They are the reason facts, not messages, are the right substrate: an ordering law over *permanent truths* is checkable; an ordering law over *transient messages* is not.

---

## 7. Long-running Business Processes

Processes that span many facts. Described as **business progression only** — the accumulation of truth over time — not as any technical orchestration.

| Process | Spans (facts) | Business progression | Terminal facts |
|---|---|---|---|
| **Campaign lifecycle** | CampaignCreated → CampaignActivated → …(all evaluation) → FairnessApproved → …(deliveries) → CampaignConcluded | A hiring effort opens, freezes its bar, runs evaluations, satisfies fairness, delivers, and closes — after which its evidence is permanently historical. | CampaignConcluded / CampaignCancelled |
| **Candidate evaluation** | CandidateInvited → WorkSampleSubmitted → EvidenceRecorded → IntegrityVerified → EvaluationCompleted → RecommendationFormed → RecommendationDelivered | One candidate progresses from invited to a delivered, fairness-cleared, explained recommendation. | RecommendationDelivered / EvaluationWithdrawn / InvitationExpired |
| **Consent lifecycle** | ConsentRequested → ConsentGranted → (ConsentWithdrawn / ConsentExpired) | Permission is sought, given, and eventually ends; while granted, data use is lawful; when it ends, use halts. | ConsentWithdrawn / ConsentExpired |
| **Hiring decision** | RecommendationDelivered → HiringDecisionRecorded | Advisory intelligence reaches a human, who makes the accountable, immutable choice. | HiringDecisionRecorded |
| **Feedback delivery** | HiringDecisionRecorded → FeedbackReleased → FeedbackDelivered | After the decision, a human authorizes and the candidate receives dignified, candidate-view feedback. | FeedbackDelivered |
| **Export** | HiringDecisionRecorded → ExportAssembled → ExportDelivered | Decided, fairness-passed intelligence is packaged and handed back; our responsibility ends. | ExportDelivered / ExportFailed |

> **Why name these:** each long-running process has a **beginning fact, a set of legal intermediate facts, and terminal facts** — and nothing outside that set is a legal progression. In ARCH-06 these become the boundaries of coordination; here they are simply the shapes truth is allowed to take over time. Note that the **Candidate evaluation** process joins the **Campaign lifecycle** at the fairness point — the one place a per-candidate process is gated by a campaign-level fact.

---

## 8. Business Compensation

Because facts are immutable, the business never "undoes" an event. When something becomes impossible, it records a **new** fact that states the new truth. Compensation is **forward-only bookkeeping of reality**, not rollback.

| When this becomes impossible… | …this compensating fact records the outcome | Business meaning |
|---|---|---|
| A campaign cannot continue | **CampaignCancelled** | The effort ended without normal conclusion; in-flight evaluations withdrawn; candidates informed with dignity. |
| A candidate never accepts / times out | **InvitationExpired** | The opportunity lapsed; no evaluation proceeds; no black hole. |
| An invitation is pulled | **InvitationRevoked** | Withdrawn by recruiter or by consent loss. |
| The candidate ends permission | **ConsentWithdrawn** | Further data use halts from this instant. |
| Permission times out | **ConsentExpired** | Same halt, by elapse rather than action. |
| An evaluation must be retracted | **EvaluationWithdrawn** | The judgment is withdrawn before delivery (e.g., consent loss, integrity failure, cancellation). |
| A new evaluation replaces an old one | **RecommendationSuperseded** | The prior recommendation is superseded, never edited. |
| Fairness does not pass | **FairnessHeld** | Delivery blocked campaign-wide until a later FairnessApproved. |
| Hand-back cannot complete | **ExportFailed** | Results stay in-platform; may be re-attempted; never partial/misleading. |

> **Rules of compensation:** (1) a compensating fact **never deletes** the facts before it — the history that "an evaluation was completed and then withdrawn" is itself true and retained; (2) a compensating fact **respects the gates** — e.g., a superseding recommendation must itself pass fairness before its own delivery; (3) compensation is expressed in **business terms only** — there is no "retry," "dead-letter," or "rollback" here; those are technology's problem later.

---

## 9. Traceability

Every event traces back through the stack. (Representative mapping; the pattern holds for all.)

| Event | ARCH-04 interaction | ARCH-03 aggregate | ARCH-02 responsibility | DOC-12 | PRODUCT-01 |
|---|---|---|---|---|---|
| CampaignCreated | A1 | Evaluation Campaign | Evaluation Campaign | Evaluation Campaign | S-2 |
| CampaignActivated | A3 | Evaluation Campaign (Calibration freeze) | Calibration | C6 | S-2 |
| CandidateImported | A2 | Candidate | Candidate Intake | C2 | S-1 |
| CandidateInvited | A4 | Candidate Evaluation (Invitation) | Invitation & Notification | C4/C5 | S-4 |
| ConsentGranted | A15 | Consent | Consent (authoritative) | C24 | Rule 9 |
| WorkSampleSubmitted | A5 | Candidate Evaluation (Work Sample) | Work Sample Engine | C8 | S-5 |
| EvidenceRecorded | A6 | Candidate Evaluation (Evidence) | Evidence Collection | C8/C10 | Flow 5 |
| IntegrityVerified | A7 | Candidate Evaluation (Evidence) / Integrity | Integrity Engine (authoritative) | C9 | integrity rule |
| EvaluationCompleted | A8 | Candidate Evaluation (Evaluation) | Evaluation + Confidence Engines | C11/C12 | S-6 / Flow 6 |
| FairnessApproved | A9 | Evaluation Campaign (Fairness Verdict) | Fairness Engine (authoritative) | C13 | Rule 3 |
| RecommendationFormed | A10 | Candidate Evaluation (Recommendation) | Recommendation + Explanation Engines | C15/C16 | S-6 |
| RecommendationDelivered | A11 | Candidate Evaluation (Recommendation) | Recommendation Engine | C16 | S-6 |
| HiringDecisionRecorded | A12 | Hiring Decision | Decision Support | C17 | S-7 / Rule 7 |
| FeedbackReleased / Delivered | A13 | Feedback | Feedback Engine | C19 | S-8 / Rule 4 |
| ExportAssembled / Delivered | A14 | Export Package | Export / Delivery | C18 | S-9 / Flow 11 |

> Every event maps to a legal ARCH-04 interaction, an ARCH-03 aggregate, an ARCH-02 responsibility, a DOC-12 capability, and a PRODUCT-01 flow. **No event exists that does not record a sanctioned conversation about an owned aggregate.** No orphans.

---

## 10. Event Governance

*Who may **create** each fact, who may **observe** it, who may **never** observe it, and retention/audit expectations. (No messaging infrastructure — governance is a business contract.)*

### 10.1 Creation authority *(only the owner of the truth may assert it)*
| Fact(s) | Sole creator |
|---|---|
| Organization/User facts | Platform Admin / Org Admin |
| Campaign facts | Evaluation Campaign (on Recruiter command) |
| CandidateImported / CandidateInvited | Candidate Intake / Campaign (on Recruiter command) |
| ConsentGranted / ConsentWithdrawn | **The candidate** (sole authority over own consent) |
| EvidenceRecorded / WorkSampleSubmitted | Candidate Evaluation / Candidate |
| **IntegrityVerified** | **Integrity Verification authority only** — no human may author it |
| EvaluationCompleted / RecommendationFormed/Delivered | Candidate Evaluation |
| **FairnessApproved / FairnessHeld** | **Fairness Assessment authority only** — no human may author it |
| **HiringDecisionRecorded** | **A named human decision-maker only** (INV-1) — never the system |
| FeedbackReleased | **A human recruiter only** (Rule 4) |
| ExportAssembled / Delivered | Export Package (on Recruiter/Campaign command) |

> The authoritative facts (`IntegrityVerified`, `FairnessApproved`) and the human facts (`HiringDecisionRecorded`, `FeedbackReleased`, `ConsentGranted`) have **narrow, non-transferable creators**. This is the event-layer expression of the authority model (ARCH-04 §6): you cannot forge a gate-pass or a human decision by emitting a fact.

### 10.2 Observation rights
- **Within-tenant, role-scoped** (per ARCH-04 §5 read dependencies): Recruiters/HMs may observe campaign, evaluation, recommendation-delivered, decision, feedback-release, and export facts for **their** tenant.
- **The Candidate** may observe only facts *about themselves* that are candidate-appropriate: their own `CandidateInvited`, `ConsentGranted/Withdrawn`, and `FeedbackDelivered`. **The candidate may never observe** `EvaluationCompleted`, `IntegrityVerified`, `FairnessApproved`, `RecommendationFormed/Delivered`, or `HiringDecisionRecorded` (P7/P13, AD-25).
- **Never (anyone):** facts belonging to **another tenant** (CAR-7/INV-10) — cross-tenant observation is impossible by construction.
- **Aggregate/anonymized only:** any future network/benchmark observation reads facts **only in aggregate** across tenants, never a single tenant's or candidate's private facts (INV-8).

### 10.3 Retention & audit expectations
- **Immutability & completeness:** every fact is append-only and retained; nothing is silently dropped (INV-b/INV-e, P8).
- **The event log *is* the audit trail.** Because every material action produces a permanent, ordered fact carrying its actor, tenant, campaign, and time, the accumulated event history satisfies the audit obligation (ARCH-04 CAR-3) — there is no separate audit fact (AD-32). Audit "expectations" therefore reduce to: *every material action must appear here, exactly once, in order, tamper-evident.*
- **Retention windows** follow the Retention Policy and Consent (ARCH-03 §8): facts about candidate data respect the consent retention window; compliance-relevant facts (decisions, fairness verdicts, consent) are retained for the applicable regulatory window. **Retention is a business policy, not a storage detail** — the *policy* is fixed here; the *mechanism* is ARCH-08.
- **No un-auditable action:** if a fact cannot be durably recorded, the underlying action must not be treated as having happened (fail-closed, ARCH-04 §9).

---

## Architecture Decisions *(continuing the log; ARCH-04 ended at AD-29)*

- **AD-30 — Events are business facts, not messages;** each records that ARCH-03/ARCH-04 rules were satisfied, and never defines a rule (§0/§1).
- **AD-31 — Confidence is an attribute of `EvaluationCompleted`, not a separate `ConfidenceCalculated` event.** We admit only facts a domain expert recognizes as "having become true," not internal computation steps (§2 note).
- **AD-32 — There is no `AuditRecorded` event; the ordered set of all business facts *is* the audit trail** (§10.3). An audit event would be circular.
- **AD-33 — `RecommendationFormed` and `RecommendationDelivered` are distinct facts,** separated by the campaign-scoped `FairnessApproved` join (§4). "Formed but not delivered, awaiting the verdict" is a legal, correct state (realizes ARCH-04 AD-28).
- **AD-34 — Compensation is forward-only:** impossibility is recorded by a *new* fact; no fact is ever edited or deleted (§8, EV-INV-14).
- **AD-35 — Authoritative and human facts have narrow, non-transferable creators** (§10.1): gate-passes and human decisions cannot be forged by emitting an event.
- **AD-36 — Fact ownership (by owning aggregate/context) is the intended seam for ARCH-06 service boundaries** (§2), so boundaries reflect the business.

## Open Questions

1. **Fairness trigger point (carried, now event-shaped):** at what count/fraction of `EvaluationCompleted` facts across the set may `FairnessApproved` first be asserted — full set only, or an interim verdict that finalizes at conclusion? Affects the Formed→Delivered gap (§4) and any interim delivery. *(Business threshold.)*
2. **Consent withdrawal vs. immutable evidence (carried):** after `ConsentWithdrawn`, do already-recorded `EvidenceRecorded` facts remain usable within an in-flight `EvaluationCompleted`, or must an `EvaluationWithdrawn` follow? (Interplay of EV-INV-14 immutability and EV-INV-15 halt.)
3. **Integrity outcome modeling:** is a low-integrity result a field on `IntegrityVerified` (verdict=flagged) or a distinct `IntegrityFlagged` fact that blocks `EvaluationCompleted`? *(Confirm before ARCH-06; affects EV-INV-5.)*
4. **Export point-in-time vs. living:** if a `HiringDecisionRecorded` changes after `ExportDelivered`, is a new export issued (supersede) or is export a point-in-time fact only? *(Carried from ARCH-04 OQ-5.)*
5. **Interim/streaming recommendations:** may a `RecommendationDelivered` ever precede full-set fairness for urgency, under a stricter later re-check? Default answer per gates: **no** (EV-INV-7). Confirm no exception is desired.

## Deferred implementation concerns *(explicitly NOT decided here)*

- **How facts are transported, stored, ordered, or replayed** (log, bus, table, stream) → **ARCH-06 / ARCH-08**.
- **Which service publishes/consumes which fact, and which service owns which fact's aggregate** → **ARCH-06 Microservice Architecture** (derived from §2 ownership + §5 causality + §6 ordering laws).
- **Delivery/consistency guarantees** (at-least-once, exactly-once, ordering enforcement mechanics) that *implement* §6 → ARCH-06.
- **Payload encoding / schemas / versioning of facts** → ARCH-07 (API/contract) and a later schema-evolution decision.
- **Physical retention/tamper-evidence mechanism** realizing §10.3 → ARCH-08 / Security & Trust ARCH doc.

---

*End of ARCH-05 v0.1 — the Business Event Model. Zero technology. It defines only business facts: what can become true, in what order truth may accumulate, how impossibility is recorded, and who may assert or observe each fact. Next: ARCH-06 — Microservice Architecture, where fact ownership (§2) and the ordering laws (§6) become the seams and contracts between services — derived from ARCH-01 through ARCH-05, not invented.*
