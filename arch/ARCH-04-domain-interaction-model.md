# ARCH-04 — Domain Interaction Model

| Field | Value |
|---|---|
| **Document ID** | ARCH-04 |
| **Title** | Domain Interaction Model (the choreography of the business) |
| **Owner** | Principal Software Architect |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture |
| **Depends on** | ARCH-03 (Canonical Domain Model — frozen), ARCH-02 (Logical Business Architecture), ARCH-01 (Context + Campaign-as-Unit-of-Work), DOC-05 (Constitution/gates), DOC-04 (vocabulary) |
| **Blocks** | ARCH-05 (Business Event Model), ARCH-06 (Microservice Architecture), ARCH-07 (API Contracts), ARCH-08 (Database Architecture) |
| **The one question** | **"Who is allowed to talk to whom — and who must never?"** — the legal interactions between business components that realize the platform. |
| **Canonical status** | **This is the single source of truth for legal business interactions.** No future event, service call, API, or message may express a collaboration this document forbids, nor omit an authority this document requires. |
| **ABSOLUTELY FORBIDDEN** | Events · REST · Messaging · Queues · Databases · Microservices · Programming languages · Frameworks · Deployment · Infrastructure · Any technology. **This document defines only the choreography of the business.** |

---

## 0. What this document adds — and why it comes before events

After ARCH-03 we know **what the business is** (contexts), **what things exist** (aggregates/entities/value objects), and **who owns what** (rules). We do **not** yet know **who is allowed to invoke whom.**

That gap is dangerous precisely in a decision-intelligence platform. Consider the questions ARCH-03 cannot answer on its own:

- *Should a Recommendation talk directly to a Candidate?* — **No.** A candidate must never receive a raw recommendation; only *released, candidate-view Feedback*.
- *Should Audit call Evaluation?* — **No.** Audit is written *to*; it never initiates work.
- *Should Fairness own the Recommendation?* — **No.** Fairness *gates* a recommendation's delivery; it never owns it.

None of these are ownership questions. They are **interaction questions**. Ownership says "the Recommendation lives inside Candidate Evaluation"; interaction says "no path from Recommendation reaches the Candidate." If we let events or microservices answer these implicitly, they will be answered by convenience under deadline — and the gates will leak. So we answer them here, as business law, before anything technical exists.

> **The rule of this document:** every legal conversation is listed; everything not listed is forbidden by default. Events (ARCH-05) will merely *record* these conversations happening; services (ARCH-06) will merely *host* the participants. Neither may invent a conversation this document does not sanction.

---

## 1. Interaction Philosophy

### 1.1 Ownership and interaction are different concepts

**Ownership** answers *"where does this rule/state live, and who may change it?"* (ARCH-03). **Interaction** answers *"who may ask whom to do something, and who may look at what?"* They are orthogonal:

- Two aggregates can each *own* their state and still be **forbidden** to talk (Recommendation and Candidate — both real, never connected).
- One aggregate can be *depended upon* by many without *initiating* anything (Audit is referenced by all, initiates nothing).
- An authority can *gate* another's action without *owning* any of its state (Fairness gates Recommendation delivery, owns none of the Recommendation).

Conflating the two is the classic error: teams assume "if A owns data B needs, A and B should call each other freely." That assumption is how a clean domain model degrades into a call graph where everything eventually talks to everything. **Interaction must be designed as deliberately as ownership was.**

### 1.2 Two honest levels of collaboration *(reconciling ARCH-03)*

Collaboration in this domain happens at exactly two levels. Naming both prevents us from pretending every internal step is a cross-component call:

> **AD-23 — Collaboration exists at two levels only:**
> **(A) Cross-aggregate collaboration** — between the nine aggregates (ARCH-03 §3), and between an aggregate and the **Trust context's authoritative domain services** (Integrity Verification, Fairness Assessment). These are the interactions this document governs.
> **(B) Intra-aggregate choreography** — the *ordered sequence of responsibilities inside a single aggregate* (most visibly inside **Candidate Evaluation**: work sample → evidence → evaluation → confidence → recommendation → explanation). This is **not** cross-component interaction and needs no interaction permission; it is one aggregate doing its own job in order. We document the sequence for clarity, but it introduces **no** collaboration rights.

Why this matters: the CTO's example chain "Evidence → Evaluation → Confidence → Fairness → Recommendation" is *mostly level (B)* — Evidence, Evaluation, Confidence, Recommendation are all responsibilities **inside Candidate Evaluation** — with **one** genuine level-(A) crossing: the **Fairness Assessment** (a campaign-scoped Trust authority) and the reading of its **Fairness Verdict**. Modeling it this way stops us from re-inflating ARCH-02's ~20 logical engines into 20 chatty pseudo-services in ARCH-06. Most of them are internal responsibilities, not collaborators.

### 1.3 The collaborators

| Collaborator | Kind | Context | Initiates? | Authoritative? |
|---|---|---|---|---|
| **Organization** (+ User) | Aggregate | BC-1 | Users initiate | — (grants authority) |
| **Candidate** | Aggregate | BC-2 | Yes (consent, submission) | — |
| **Evaluation Campaign** | Aggregate (primary) | BC-4 | Yes (orchestrates) | organizing authority |
| **Candidate Evaluation** | Aggregate | BC-4 | Yes | advisory output |
| **Hiring Decision** | Aggregate | BC-5 | via human | **human authority** |
| **Feedback** | Aggregate | BC-5 | via human release | — |
| **Export Package** | Aggregate | BC-5 | Yes (at conclusion) | — |
| **Consent** | Aggregate | BC-6 | Candidate initiates | **authoritative (gate)** |
| **Audit Record** | Aggregate | BC-6 | **never initiates** | authoritative (record) |
| **Integrity Verification** | Domain service | BC-6 | responds only | **authoritative (gate)** |
| **Fairness Assessment** | Domain service | BC-6 | Campaign invokes | **authoritative (gate)** |
| **Tenant Isolation** | Pervasive rule | BC-6 | — | **authoritative (always-on)** |

---

## 2. Collaboration Matrix

**Legend:** ✅ = may initiate a direct collaboration; 👁 = may read/reference only (no command; see §5); ⛔ = forbidden entirely; — = self/not applicable. Rows initiate; columns receive.

| initiates → receives | Org/User | Candidate | Campaign | Cand. Eval | Hiring Decision | Feedback | Export | Consent | Integrity Verif. | Fairness Assess. | Audit |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Org / User** | — | ✅ (intake) | ✅ (create/activate) | 👁 | ✅ (decide) | ✅ (release) | ✅ (export) | 👁 | ⛔ | ⛔ | 👁 (governed) |
| **Candidate** | ⛔ | — | ⛔ | ✅ (submit work) | ⛔ | 👁 (own feedback) | ⛔ | ✅ (grant/withdraw) | ⛔ | ⛔ | ⛔ |
| **Campaign** | 👁 (tenant) | 👁 (roster) | — | ✅ (create/scope) | ⛔ | ⛔ | ✅ (assemble) | 👁 | ⛔ | ✅ (assess set) | →writes |
| **Cand. Evaluation** | 👁 | 👁 (identity) | 👁 (calibration, verdict) | ⛔ (peer) | ⛔ | ⛔ | 👁 | 👁 (gate) | ✅ (verify) | ⛔ (campaign's job) | →writes |
| **Hiring Decision** | 👁 (actor) | 👁 | 👁 | 👁 (reads rec.) | — | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ | →writes |
| **Feedback** | 👁 (releaser) | ✅ (deliver) | ⛔ | 👁 (cand. view) | ⛔ | — | ⛔ | 👁 | ⛔ | ⛔ | →writes |
| **Export** | 👁 | ⛔ | 👁 | 👁 | 👁 | ⛔ | — | ⛔ | ⛔ | 👁 (verdict) | →writes |
| **Consent** | ⛔ | 👁 | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ | — | ⛔ | ⛔ | →writes |
| **Integrity Verif.** | ⛔ | ⛔ | ⛔ | 👁 (evidence) | ⛔ | ⛔ | ⛔ | ⛔ | — | ⛔ | →writes |
| **Fairness Assess.** | ⛔ | ⛔ | 👁 (candidate set) | 👁 (evaluations) | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ | — | →writes |
| **Audit** | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ | ⛔ | — |

*("→writes" = the actor appends an Audit Record as a mandatory side effect of every material action; this is not Audit being "called," it is the pervasive audit obligation, §7 CAR-3. Audit itself initiates nothing — its entire row is ⛔.)*

### 2.1 The forbidden interactions — stated as law, with reasons

- **Recommendation / Candidate Evaluation ⛔→ Candidate.** A candidate never receives a recommendation or raw evaluation. Only **Feedback** may address a candidate, and only its **released, candidate-view** content (P13, Rule 4). *Reason: candidates must be protected from internal mechanics and from unreleased judgments; a direct path would defeat both the explainability posture and the recruiter's release control.* **(AD-25.)**
- **Audit ⛔→ anyone.** Audit never initiates a collaboration. It is written to and read (under governance); it never asks another component to do anything. *Reason: a record that can act is no longer a neutral record; audit must be a pure, passive, tamper-evident ledger.* **(AD-26.)**
- **Fairness Assessment ⛔ owns Recommendation.** Fairness produces a campaign-scoped **verdict**; it never holds or edits a Recommendation. *Reason: the gate must be independent of the thing it gates; if fairness owned the recommendation it could not be a neutral check on it.* **(AD-27.)**
- **Candidate Evaluation ⛔→ Candidate Evaluation (peer).** No candidate's evaluation may read or influence another's. *Reason: each candidate is judged on their own evidence (INV-5); peer influence is a fairness and leakage hazard. Cross-candidate comparison is a **campaign-level** concern (Fairness/benchmarking), never peer-to-peer.*
- **Candidate Evaluation ⛔→ Fairness Assessment (directly).** A single evaluation cannot invoke fairness, because adverse impact is a property of the **set**, not the individual. Only the **Campaign** invokes Fairness Assessment across its candidate set. *Reason: fairness assessed one-candidate-at-a-time is meaningless.*
- **Anyone ⛔→ a collaborator in another tenant.** All interaction is single-tenant by construction (INV-10, §7 CAR-7).
- **Decision / Export ⛔→ act on the Offer.** Our boundary ends at deliver-back (KD-12.7, INV-9); no collaborator reaches into the customer's offer/SoR.
- **User ⛔→ Integrity / Fairness / Audit (to alter).** No human may command a gate to pass, alter an Integrity Score, or edit Audit. Humans decide *hires* (authoritative); humans never overrule *gates* (P1/P2/P3, DOC-05 Tier 0).

---

## 3. Aggregate Collaboration Diagrams

*ASCII. Each shows one legal business flow. `──▶` = initiates; `··▷` = reads/references; `⟦gate⟧` = authoritative gate; `[[audit]]` = mandatory audit side-effect on every step.*

### 3.1 The primary evaluation flow *(happy path, one candidate, within a campaign)*
```
User(Recruiter) ──create──▶ CAMPAIGN ──create/scope──▶ CANDIDATE EVALUATION
                               │  (calibration frozen at Active)
                               │
CANDIDATE ──grant──▶ CONSENT ⟦gate⟧ ··▷ (must be Granted before any evidence)
                               │
CAMPAIGN ──invite──▶ CANDIDATE EVALUATION (Invitation)
CANDIDATE ──submit work──▶ CANDIDATE EVALUATION
   │  [intra-aggregate choreography — NOT cross-component:]
   │     work sample ─▶ evidence ─▶ (evaluate) ─▶ confidence ─▶ (recommend) ─▶ explanation
   │        │
   │        └── evidence ──verify──▶ INTEGRITY VERIFICATION ⟦gate⟧ ──Integrity Score──▶ (attached)
   │
CAMPAIGN ──assess set──▶ FAIRNESS ASSESSMENT ⟦gate⟧ ──Fairness Verdict──▶ CAMPAIGN
                               │
CANDIDATE EVALUATION ··▷ reads Campaign Fairness Verdict
   └── deliver Recommendation  ONLY IF (Explanation attached ∧ Verdict = Passed)
                               │
User(HM) ··▷ reads Recommendation+Explanation+Evidence ──decide──▶ HIRING DECISION (human)
                               │
User(Recruiter) ──release──▶ FEEDBACK ──deliver──▶ CANDIDATE (candidate-view only)
CAMPAIGN/User ──assemble──▶ EXPORT PACKAGE ··▷ (fairness-passed, explained) ──deliver──▶ [customer SoR]
        [[audit]] appended at EVERY step ; TENANT ISOLATION around EVERY arrow
```

### 3.2 The consent-and-evidence flow *(the CTO's second example, made precise)*
```
CANDIDATE ──grant──▶ CONSENT ⟦gate⟧
                        │  (Granted)
CANDIDATE EVALUATION ··▷ checks CONSENT  ── if not Granted ⇒ HALT (no evidence) ──
                        │
CANDIDATE EVALUATION ──record──▶ EVIDENCE (immutable)     [[audit]]
                        │
EVIDENCE ──verify──▶ INTEGRITY VERIFICATION ⟦gate⟧ ──Integrity Score──▶ (attached)   [[audit]]
                        │
CANDIDATE EVALUATION ──(evaluate, internal)──▶ EVALUATION      [[audit]]
```
*Note: Audit does not sit "between" Evidence and Evaluation as an actor (the CTO's sketch placed it inline). Audit is a **side-effect of each step**, never a step that hands work onward — hence `[[audit]]` annotations rather than an arrow **from** Audit.*

### 3.3 The campaign–calibration loop *(the CTO's third example)*
```
CAMPAIGN ──create/scope──▶ CANDIDATE EVALUATION
CAMPAIGN ──owns/freezes──▶ CALIBRATION (entity inside Campaign; frozen at Active — INV-c)
CANDIDATE EVALUATION ··▷ reads CALIBRATION (context for the judgment — INV-5)
CANDIDATE EVALUATION ──(evaluation formed)──▶ back into CAMPAIGN scope (roster/verdict rollup)
```
*Calibration is **not** a peer aggregate the evaluation "calls"; it is owned by the Campaign and **read** by each Candidate Evaluation. The loop is Campaign → (its own Calibration) → read-by → Candidate Evaluation → rolls-up-to → Campaign.*

### 3.4 The human-decision flow *(authority handoff)*
```
CANDIDATE EVALUATION ──Recommendation (Delivered: explained + fairness-passed)──▶
User(Hiring Manager) ··▷ reads Recommendation + Explanation + cited Evidence
        │  (system presents; system NEVER finalizes — INV-1)
        └──▶ HIRING DECISION (Advance | Hold | Reject) [human, accountable]
                 │  divergent from Recommendation ⇒ Override Justification required
                 ▼
        HIRING DECISION (immutable once Decided)      [[audit]]
```

---

## 4. Command Responsibilities

For each business action (command): **Initiator** (who may start it) · **Validator** (who guards its business rules — the authority that may refuse) · **Responder** (who performs it / holds the result). *No command is valid unless its Validator's rules pass; validators are where the gates live.*

| # | Business action | Initiator | Validator (may refuse) | Responder |
|---|---|---|---|---|
| A1 | Create Campaign | User (Recruiter) | Campaign (tenant scope, role ref present) | Campaign (Draft) |
| A2 | Import / Intake candidates | User | Candidate + **Consent precondition** | Candidate; Campaign roster |
| A3 | Set calibration / Activate campaign | User | Campaign (calibration present ⇒ freeze, INV-c) | Campaign (Active) |
| A4 | Invite candidate | Campaign (on Active) | **Consent** state | Candidate Evaluation (Invitation) |
| A5 | Submit work sample | Candidate | Candidate Evaluation (Invitation accepted; **Consent**) | Candidate Evaluation (Work Sample) |
| A6 | Record evidence | Candidate Evaluation | **Consent**; role-relevance | Candidate Evaluation (Evidence, immutable) |
| A7 | Verify integrity | Candidate Evaluation | **Integrity Verification** (authoritative) | Integrity Score on Evidence |
| A8 | Produce evaluation | Candidate Evaluation | integrity-checked evidence present; calibration read (INV-4/5) | Evaluation + Evaluation Score + Confidence |
| A9 | Assess fairness | **Campaign** (across set) | **Fairness Assessment** (authoritative) | Fairness Verdict on Campaign |
| A10 | Form recommendation | Candidate Evaluation | evaluation + confidence + **explanation** present (INV-2/6) | Recommendation (Formed) |
| A11 | **Deliver recommendation** | Candidate Evaluation | **Explanation attached ∧ Campaign Fairness Verdict = Passed** (INV-2/3) | Recommendation (Delivered) |
| A12 | Record hiring decision | **human** User (HM) | Hiring Decision (references delivered Rec.; human present INV-1; override justified) | Hiring Decision (Decided, immutable) |
| A13 | Release feedback | **human** User (Recruiter) | Feedback (candidate-view only; release gate, Rule 4) | Feedback (Released → Delivered) |
| A14 | Export / deliver back | User / Campaign (conclusion) | Export (only fairness-passed, explained; boundary INV-9) | Export Package (Delivered) |
| A15 | Grant / withdraw consent | **Candidate** | Consent | Consent (Granted / Withdrawn) |
| A16 | Append audit | *every command above* (side-effect) | — (records, never refuses business) | Audit Record (append-only) |

> **Reading the table:** the **Validator** column is where refusal power lives. Notice that every *authoritative* validator (Consent, Integrity, Fairness, Explanation-presence, human-presence) can **refuse** to let a command complete — and none of them can be refused *by* the initiator. That asymmetry is the runtime shape of the Constitution's Tier-0 gates.

---

## 5. Read Dependencies

Interaction is not only commands; it is also *who may look at what*. Two rights are distinct: **Read** (may inspect another's content) vs **Reference-by-identity** (may hold a pointer, may **not** inspect content).

| Reader | May READ (content) | May only REFERENCE (identity) | May NOT read |
|---|---|---|---|
| **Candidate Evaluation** | Campaign's **Calibration** (context); Campaign's **Fairness Verdict** (delivery gate); **Consent** state | Candidate; Campaign | Other Candidate Evaluations; Audit internals |
| **Fairness Assessment** | **All evaluations in the campaign's candidate set** (needs the set) | Campaign | Anything cross-tenant; individual candidate PII beyond what fairness requires |
| **Integrity Verification** | The **Evidence** + integrity signals under scrutiny | Candidate Evaluation | Evaluation judgment; other candidates |
| **Hiring Decision** | Delivered **Recommendation + Explanation + cited Evidence** | Candidate; User; Campaign | Unreleased/undelivered recommendations; other candidates' evidence |
| **Feedback** | **Candidate-view Explanation only** | Candidate Evaluation; Candidate | Internal evaluation mechanics; scores not meant for candidates (P13) |
| **Export Package** | Fairness-passed **Recommendations + Decisions + Explanations** | Campaign; Candidate Evaluations | Anything not fairness-passed/explained |
| **Candidate** | **Own released Feedback** only | — | Recommendations; evaluations; other candidates; internals |
| **Audit / Governance** | Everything, **for the record** (append) and under governed read | All (by identity) | *(reads are governed, tenant-scoped, and themselves audited)* |

**Principles:**
- **Reference-by-identity is the default; read is a privilege that must be justified by a business need named above.** If a collaborator only needs to *point at* another (e.g., "this evaluation belongs to that candidate"), it gets identity, not content. This is what keeps PII and judgments from spreading.
- **The Candidate's read surface is deliberately the narrowest** — released feedback only — because the candidate is a first-class user we protect, not a party to internal deliberation (P7/P13).
- **Fairness's read surface is deliberately the widest within a campaign** (the whole set) and **zero across campaigns/tenants** — because fairness *needs* the set and must never see beyond it.

---

## 6. Authority Model

Three authority kinds, mutually exclusive per action:

### 6.1 Authoritative (may refuse; may not be overridden — the gates)
- **Consent** — refuses any candidate-data use without an active grant (INV-11).
- **Integrity Verification** — its Integrity Score cannot be overridden; low integrity flags, never silently passes.
- **Fairness Assessment** — its campaign Verdict gates delivery; a *Hold* cannot be bypassed (INV-3).
- **Explanation-presence** — no delivery without an audience-appropriate Explanation (INV-2).
- **Tenant Isolation** — refuses any cross-tenant access, always (INV-10).
- **Audit** — authoritative as a *record* (append-only, complete); it compels recording but performs no business.

> These are authoritative because DOC-05 places them at **Tier 0**. Authoritative means: **no human and no other component may command them to yield.** A recruiter cannot tell Fairness to pass; a hiring manager cannot edit an Integrity Score; an admin cannot delete an Audit Record.

### 6.2 Advisory (informs a human; never binding)
- **Evaluation / Evaluation Score** — advisory judgment of ability.
- **Recommendation / Recommendation Level** — advisory suggested action.
- **Confidence** — advisory qualifier on the above.
- **Calibration** — advisory context that shapes the bar (then frozen), never a gate.

> Advisory authorities produce *inputs to a human decision*. They are load-bearing for **decision quality** but carry **no** binding force. This is the structural meaning of "we recommend; humans decide."

### 6.3 Human authority (only a human may perform)
- **Hiring Decision** — advance/hold/reject (INV-1); the accountable act.
- **Feedback release** — a human recruiter decides when/whether feedback is delivered (Rule 4).
- **Calibration sign-off** — a human sets the bar before it freezes.
- **Consent grant/withdrawal** — the **candidate** (a human) is the sole authority over their own consent.

### 6.4 Organizing authority
- **Campaign** — not a gate and not advisory; it holds **organizing** authority: it scopes, sequences, invokes fairness across its set, and bounds audit/export. It commands within its scope but cannot override any Tier-0 gate.

---

## 7. Cross-Aggregate Rules

Rules that span **more than one** aggregate, and therefore **cannot** be owned by any single aggregate's boundary. Each is owned by a **domain policy** (a rule with a named owner) rather than living inside one aggregate.

| ID | Rule | Spans | Why it cannot belong to one aggregate | Owner |
|---|---|---|---|---|
| **CAR-1** | A Recommendation may be **Delivered** only if its Campaign's Fairness Verdict = Passed. | Candidate Evaluation + Campaign | Fairness is a property of the **candidate set** (Campaign), but the gated thing (Recommendation) lives per-candidate. Neither aggregate can see both sides alone. | **Fairness policy** (BC-6 + Campaign) |
| **CAR-2** | No evidence collection/evaluation without an **active Consent**. | Candidate Evaluation + Consent | Consent lives with the Candidate; the action lives in the evaluation. The precondition bridges them. | **Consent policy** (BC-6) |
| **CAR-3** | Every material action produces exactly one **Audit Record**. | All + Audit | Auditing is universal; no single aggregate can assert it for the others. | **Audit invariant** (BC-6, pervasive) |
| **CAR-4** | A Candidate has **at most one active Candidate Evaluation per Campaign**. | Candidate + Campaign + Candidate Evaluation | Uniqueness spans the person, the campaign scope, and the evaluation instance. | **Campaign roster policy** |
| **CAR-5** | A Hiring Decision must reference a **Delivered** (explained, fairness-passed) Recommendation. | Hiring Decision + Candidate Evaluation | The decision aggregate cannot itself guarantee the recommendation's delivery status. | **Decision policy** (BC-5) |
| **CAR-6** | An Export contains **only** fairness-passed, explained outputs. | Export + Candidate Evaluation + Campaign | Export must verify properties held across evaluations and the campaign verdict. | **Export policy** (BC-5) |
| **CAR-7** | Every interaction is **single-tenant**. | All | Tenancy is a property of the whole graph, not any node. | **Tenant Isolation** (pervasive) |
| **CAR-8** | Freezing **Calibration** at Campaign Active binds **all** its Candidate Evaluations. | Campaign + all its Candidate Evaluations | The freeze is a campaign fact that constrains many evaluations at once (comparability/fairness). | **Campaign** |

> **Why name these separately:** every CAR is a rule that a naïve design would try to cram into one aggregate — and get wrong. CAR-1 is the archetype: put it inside Candidate Evaluation and you have an evaluation trying to reason about the whole set it cannot see; put it inside Campaign and you have the campaign reaching into per-candidate delivery it does not own. It belongs to **neither** — it is a **policy** the two obey. ARCH-05 will express each CAR's satisfaction as observable events; ARCH-06 will decide *where the policy runs*. **Here we only fix that the policy exists and what it requires.**

---

## 8. Consistency Boundaries

*Which rules must hold **at the instant** of an action (immediate), and which may tolerate a **bounded gap** (delayed) — judged purely by **business correctness**, not by any technical mechanism.*

### 8.1 Immediate consistency required *(violating this at the instant = a wrong or unfair outcome)*
- **Consent must be active at the moment evidence is collected/used** (CAR-2). A gap here is a real breach, not a nuisance.
- **Evidence immutability** — an Evidence Item is never in a "half-mutable" state (INV-b).
- **Explanation must be attached before a Recommendation is Delivered** (INV-2) — within the Candidate Evaluation, no delivery precedes its explanation.
- **A Hiring Decision must reference a Delivered Recommendation at the instant it is made** (CAR-5); a human must be the actor at that instant (INV-1).
- **Tenant isolation** holds on **every** access, always (CAR-7). There is no tolerated window of cross-tenant visibility.
- **Feedback exposes only candidate-view content** at the instant of delivery (P13).

### 8.2 Delayed consistency tolerated *(business meaning survives a bounded gap)*
- **Fairness Verdict across the set (CAR-1).** A Recommendation may legitimately sit **Formed but not Delivered** while the campaign waits for enough of its candidate set to be evaluated before Fairness can assess the set. **This gap is not a defect — it is the business correctly refusing to deliver before it can be fair.** The tolerated state is "formed, awaiting verdict"; the forbidden state is "delivered without a passed verdict."
- **Audit completeness.** Audit must be **complete and lossless**, but the business tolerates that a record is appended *immediately after* its action rather than in the identical instant — provided **no material action can be lost from the record**. (Loss is *not* tolerated; tiny lag is.)
- **Roster/aggregate rollup.** A Campaign's view of "how many evaluations are complete" may lag slightly behind the individual evaluations; no decision depends on this being instantaneous.
- **Outcome Learning / Benchmark updates** *(deferred capabilities)* — inherently delayed (weeks/months); correctness never depends on immediacy (INV-8/INV-12).

> **The doctrine:** *gates are immediate; intelligence and aggregation may be delayed.* You may never be *briefly* unfair, un-consented, un-isolated, or unexplained. You **may** briefly not-yet-know the fairness verdict, not-yet-have-rolled-up counts, or not-yet-learned from outcomes — because in those states the business simply **waits or withholds**, which is always safe. **(AD-28.)**

---

## 9. Failure Semantics

*If a collaborator cannot complete its responsibility, what is the correct **business** behavior? (Not the technical retry/recovery — that is ARCH-06+.)* The governing principle from ARCH-01: **degrade to less-confidence / more-human; never to wrong-or-unfair.** Refined here into a two-mode doctrine:

> **AD-24 — Gates fail *closed*; intelligence fails *soft*.**
> A **gate** that cannot complete must **stop or hold** the action (never wave it through). An **advisory intelligence** step that cannot complete must **reduce confidence and escalate to a human** (never fabricate).

| Collaborator | If it cannot complete… | Correct business behavior | Mode |
|---|---|---|---|
| **Consent** | can't confirm active consent | **Do not collect or use evidence.** Halt; surface the block. | fail **closed** |
| **Integrity Verification** | can't judge authenticity | **Do not treat evidence as trusted.** Hold/flag; route to human. Never silently pass. | fail **closed** |
| **Fairness Assessment** | can't produce a Verdict | **Hold all recommendations** in the campaign (Formed, undelivered). Never deliver un-assessed. | fail **closed** |
| **Explanation** | can't produce an explanation | **Do not deliver** the recommendation (no bare score). | fail **closed** |
| **Tenant Isolation** | can't guarantee the boundary | **Hard stop.** Never proceed under isolation doubt. | fail **closed** |
| **Audit** | can't record the action | **Do not perform the material action.** An un-auditable action must not happen (Tier-0). | fail **closed** |
| **Evaluation** | insufficient/ambiguous evidence | **Express low/no Confidence; escalate to human.** Never fabricate a score. | fail **soft** |
| **Confidence** | can't be determined | **Treat as low confidence, stated honestly.** | fail **soft** |
| **Recommendation** | can't be formed | **Produce no recommendation; hand evidence to the human.** | fail **soft** |
| **Hiring Decision (human)** | human unavailable | **Nothing auto-finalizes; the work waits** (INV-1). | fail **safe (wait)** |
| **Feedback** | can't generate sound feedback | **Do not deliver misleading feedback; hold**; inform recruiter. | fail **closed** |
| **Export** | can't complete hand-back | **Results remain available in-platform; retry;** never a partial/misleading export. | fail **safe (hold)** |
| **Campaign** | can't be established/scoped | **No evaluation begins** (everything belongs to a campaign, AD-09). | fail **closed** |

> **Why the split is load-bearing:** if gates failed *soft* (proceeding on doubt) we would occasionally be unfair, un-consented, or unexplained — the one thing the product may never be. If intelligence failed *closed* (stopping on doubt) the product would be brittle and useless whenever evidence is thin — but thin evidence is *normal*, and the honest response is *low confidence + a human*, not a halt. The two modes encode "never wrong-or-unfair; always willing to say 'I'm not sure, you decide.'"

---

## 10. Traceability

| ARCH-04 element | Traces to |
|---|---|
| Collaborators (§1.3) | ARCH-03 §3 aggregates (AGG-1…9) + ARCH-03 §2 BC-6 authorities |
| Two-level collaboration (AD-23) | ARCH-03 §3.0 (Candidate Evaluation as own aggregate); ARCH-02 §7 cross-cutting |
| Forbidden interactions (§2.1) | ARCH-02 §6 boundaries; INV-1/INV-10; P13; KD-12.7 |
| Command responsibilities (§4) | ARCH-03 state machines §6; PRODUCT-01 flows/rules; DOC-05 Tier-0 gates |
| Read vs reference (§5) | ARCH-03 "references by identity" rule; P7/P13; INV-10 |
| Authority model (§6) | DOC-05 priority ladder (Tier 0 gates); INV-1; ARCH-03 §6.2 advisory/authoritative |
| Cross-aggregate rules (§7) | ARCH-03 §3.0 (INV-3 cross-aggregate) + INV-a…e; ARCH-02 §9 constraints |
| Consistency boundaries (§8) | ARCH-03 AD-16 consequence; ARCH-01 failure boundary |
| Failure semantics (§9) | ARCH-01 §failure ("degrade to less-confidence/more-human"); DOC-05 P1/P2/P3/P8 |

> Every collaboration, command, read, authority, cross-aggregate rule, consistency class, and failure behavior above traces to a frozen ARCH-03 element or a Constitutional gate. No new domain concept is introduced here — only the **rules of conversation** among concepts that already exist.

---

## Architecture Decisions *(continuing the log; ARCH-03 ended at AD-22)*

- **AD-23 — Collaboration exists at two levels:** cross-aggregate (+ Trust authoritative services) and intra-aggregate choreography; only the former is governed by interaction rules (§1.2). *Prevents re-inflating internal responsibilities into pseudo-services in ARCH-06.*
- **AD-24 — Gates fail closed; intelligence fails soft** (§9). The two-mode failure doctrine.
- **AD-25 — Recommendations never reach a Candidate directly;** only released, candidate-view Feedback does (§2.1).
- **AD-26 — Audit never initiates a collaboration;** it is written-to and governed-read only, and no material action may proceed unauditable (§2.1/§9).
- **AD-27 — Fairness gates but never owns the Recommendation;** the gate is independent of what it gates (§2.1/§6).
- **AD-28 — Gates are immediate; intelligence and aggregation may be delayed** (§8). "Formed but not Delivered, awaiting verdict" is a legal, correct state.
- **AD-29 — Reference-by-identity is the default; content-read is a justified privilege** (§5).

## Open Questions

1. **Fairness trigger point:** at what fraction of the candidate set may Fairness Assessment first run — full set, or a rolling/interim assessment that finalizes at conclusion? *(Business threshold; resolve with the fairness/IO-psych approach, feeds ARCH-05 event timing.)*
2. **Consent withdrawal mid-flight:** does withdrawal invalidate *use* of already-recorded immutable evidence going forward only, or also require its retirement from the current evaluation? *(Interplay of INV-b immutability, INV-11 consent, retention policy.)*
3. **Integrity vs Fairness ordering** at the evidence→evaluation→delivery path — both authoritative; confirm whether integrity failure short-circuits evaluation entirely or flags through to a held state. *(Carried from ARCH-02 OQ-4 / ARCH-03 OQ-2.)*
4. **Explanation authority placement:** is Explanation a responsibility *inside* Candidate Evaluation (this doc's assumption) or a Trust-governed service? Audience-scoping (P13) may argue for shared governance. *(Carried; resolve before ARCH-06.)*
5. **Export re-delivery semantics:** if a decision changes after an export, is a new Export Package issued (supersede) or is export point-in-time only? *(Business rule; feeds ARCH-05.)*

## Risks

- **Premature service-thinking:** readers may treat every arrow here as a future network call. §1.2/AD-23 explicitly warns that intra-aggregate choreography is **not** interaction; ARCH-06 must resist turning internal steps into chatty services.
- **Fairness-as-delayed tempting a shortcut:** the legal "Formed, awaiting verdict" state could tempt teams to deliver early under pressure (RK-6/RK-15). CAR-1 + AD-24 (fail closed) + AD-28 guard against it; ARCH-05/06 must make the held state observable and enforced.
- **Audit treated as passive-and-optional:** "write-only, never initiates" can be misread as "nice-to-have." §9 makes audit **fail-closed** (no un-auditable action) to keep it Tier-0.
- **Campaign as collaboration chokepoint:** the Campaign is the hub of many flows (echoing ARCH-02's risk). Correct for business coherence, but ARCH-06 must ensure it does not become a physical bottleneck or a single point of coupling.
- **Read-privilege creep:** over time, collaborators may request content-reads "for convenience." §5/AD-29 make reference-by-identity the default so each new read must be justified against a named business need.

## Deferred implementation concerns *(explicitly NOT decided here)*

- **How** conversations are realized (synchronous invocation vs asynchronous messaging vs shared state) → **ARCH-06 Microservice Architecture**.
- **Events** that *record* these conversations (`FairnessApproved`, `RecommendationDelivered`, …) → **ARCH-05 Business Event Model**.
- **Consistency mechanisms** (transactions, compensations, coordination) that *implement* §8's immediate/delayed classes → ARCH-06+.
- **Where each policy (CAR-1…8) physically runs** and how a gate is technically enforced → ARCH-06 / Security & Trust ARCH doc.
- **Service boundaries** derived from these interactions → ARCH-06 (the CTO's expectation: with §2/§7 fixed, service boundaries "almost write themselves").

---

*End of ARCH-04 v0.1 — the Domain Interaction Model. Zero technology. It defines only the choreography of the business: who may talk to whom, who validates, who reads, who has authority, which rules span aggregates, what must be immediate, and how the business behaves when a part cannot complete. Next: ARCH-05 — Business Event Model, which records these legal conversations as domain events.*
