# ARCH-03 — Canonical Domain Model

| Field | Value |
|---|---|
| **Document ID** | ARCH-03 |
| **Title** | Canonical Domain Model |
| **Owner** | Principal Software Architect + Domain-Driven Design lead |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture |
| **Depends on** | DOC-04 (Ubiquitous Language — frozen), ARCH-02 (Logical Business Architecture), ARCH-01 (Context + Campaign-as-Unit-of-Work), PRODUCT-01 (MVP), DOC-05 (Constitution/gates), DOC-12 (Capabilities) |
| **Blocks** | ARCH-04 (Business Event Model), ARCH-05 (Physical Architecture), and **every** future API, data model, UI screen, AI prompt, report, and engineering decision |
| **Canonical status** | **This is the single source of truth for the business language and for where business rules live.** Every future artifact must *trace back* to this document. A business rule that is not expressed here does not officially exist; a business rule expressed here may be *enforced* elsewhere but may never be *redefined* elsewhere. |
| **The one question** | **"What is a Candidate, an Evidence, a Recommendation, a Campaign — exactly — and what rules can never be violated about them?"** |
| **ABSOLUTELY FORBIDDEN** | Databases · ORM · Tables · Columns · Primary/Foreign Keys · REST · GraphQL · Microservices · Queues · Programming languages · Frameworks · Any technology. **This document must remain valid even if the entire technology stack is replaced.** |

---

## 0. The problem this document exists to prevent

Most enterprise systems rot in the same way. A business rule — *"a Recommendation cannot exist without an Evaluation"* — is first written in a service. Later someone re-asserts it as a database constraint "to be safe." A front-end engineer adds a form check. An integration engineer adds an API guard. Someone tunes an AI prompt to "usually" respect it. Now the rule lives in **five places, owned by no one**, and the five copies drift. The system still runs, but nobody can say what the rule *is* anymore — only what each layer happens to do. This is the spaghetti that kills long-lived platforms, and it is almost always caused by the same root error: **the business rules were never given a home.**

ARCH-03 gives them a home. It declares, as an architectural law:

> **Business rules live in the domain model. Everything else enforces or reflects them; nothing else defines them.**
> - The **database** may *persist* domain state, but a rule is never "in" a schema.
> - An **API** may *reject* an invalid request, but the definition of "invalid" comes from here.
> - The **UI** may *guide* a user away from an illegal action, but it is a convenience, never the source of truth.
> - An **AI prompt** may *operate within* the rules, but a prompt can never *be* a rule (prompts are probabilistic; invariants are absolute).

If a future engineer asks *"where is it decided that a delivered Recommendation must carry an Explanation?"* — the answer is one place: **here (INV-2)**. The API, UI, and persistence layer each *honor* it; none of them *own* it.

This is why ARCH-03 is more than a DDD exercise. **It is the constitution for every engineer.**

---

## 1. Domain Philosophy

### 1.1 Why a ubiquitous language is essential (and why we already froze one)

DOC-04 froze the company's vocabulary. ARCH-03 does not restate that dictionary — it **operationalizes** it into a formal model (aggregates, entities, value objects, state machines, invariants) so the language becomes *structural*, not merely definitional. The value of one-word-one-meaning is that the model, the code, the API, the UI, the report, and the sales deck all use the same nouns with the same boundaries. When a product manager says "Candidate Evaluation," an engineer, a lawyer, and a customer all mean the same bounded thing — **the billing unit: one Candidate × one Role × one Recommendation** — and no code path can quietly mean something else.

### 1.2 Why every business term has exactly one meaning

A term with two meanings is two latent defects: every place that reads it must guess which meaning was intended, and every place that writes it can violate the other meaning silently. The model below assigns each term to exactly one **bounded context** (its owner) and exactly one **structural role** (aggregate root / entity / value object). That dual assignment — *who owns the meaning* and *what kind of thing it is* — is what makes the language unambiguous in practice, not just on paper.

### 1.3 Why business rules belong in the domain model — not in APIs, databases, UI, or prompts

Four reasons, in priority order:

1. **Single source of truth.** A rule stated once cannot drift. A rule copied into four layers will.
2. **Explainability (Constitutional).** Our Fairness/Explainability gate (DOC-05) requires that every recommendation be defensible to a candidate, a hiring manager, and a regulator. You can only defend a decision against rules that are *written down as rules*. A rule buried in a prompt or a query is undefendable because it is unfindable.
3. **Technology independence.** Stacks change; the business does not. "Evidence belongs to exactly one Campaign" is true whether we run a monolith or microservices, SQL or graph, this year's framework or next year's. Putting the rule in the domain model lets the technology underneath be replaced without renegotiating the business.
4. **Ownership and governance.** DOC-04 gave every term an owning Domain. ARCH-03 extends that: every **rule** has an owning aggregate. Ownership is what lets a 200-engineer organization change a rule safely — you know exactly who decides and exactly what else is affected.

> **The domain model is authoritative over meaning and rules. All technology is subordinate to it.** This sentence is the spine of the entire architecture.

---

## 2. Bounded Contexts

A **bounded context** is a boundary within which each term has exactly one meaning and one owner. These are the same conceptual boundaries introduced in DOC-04 §2, now sharpened into *modeling* boundaries: each context owns specific aggregates, references others by identity, and never owns what belongs to another. (These are **not** services, modules, or deployables — that is ARCH-05.)

For each context: **Purpose · Responsibilities · Shared Language · Owns · References · Never Owns · Interactions · Why the boundary exists.**

### BC-1 · Organization & Access Context
- **Purpose:** Establish who the customer is and who is permitted to act.
- **Responsibilities:** Tenant establishment; users and their roles/permissions; consent configuration at the org level; holding the tenant scope that every other context operates inside.
- **Shared Language:** Organization, User, Role (permission sense), Tenant.
- **Owns (aggregates):** **Organization** (root), **User**.
- **References:** Nothing outside itself (it is the root of authority).
- **Never Owns:** Candidates, Evaluations, Decisions — it owns *actors and scope*, not *work*.
- **Interactions:** Supplies the authorized, tenant-scoped context to all other contexts.
- **Why the boundary exists:** Authority and tenancy are orthogonal to hiring work; conflating "who may act" with "what happened" is how tenant leaks and permission bugs are born. Isolating them makes tenant isolation (INV-10) enforceable at one boundary.

### BC-2 · Candidate Context
- **Purpose:** Represent the candidate as a durable, first-class network participant, not a per-req record.
- **Responsibilities:** Candidate identity within a tenant; durable status across the afterlife; contact information; the candidate's participation *links* to campaigns.
- **Shared Language:** Candidate, Silver Medal Candidate, Talent Pool, Candidate Afterlife, Portable Evidence *(afterlife/portable = deferred vocabulary, owned here for the future)*.
- **Owns (aggregates):** **Candidate** (root).
- **References:** Organization (tenant); the Campaigns / Candidate Evaluations the person participates in (by identity).
- **Never Owns:** The *evaluation* of the candidate (that is a Candidate Evaluation), the *evidence* (owned within Candidate Evaluation), or the *decision* (Hiring Decision). The Candidate is the person; it does not own judgments about the person.
- **Interactions:** Referenced by Evaluation Campaign, Candidate Evaluation, Feedback, Consent.
- **Why the boundary exists:** A candidate outlives any single hiring effort (DOC-04). Modeling the person separately from any one evaluation is what makes the afterlife, silver-medal re-engagement, and (later) portable evidence possible without duplicating a person per campaign.

### BC-3 · Work Context *(reference-only)*
- **Purpose:** Name what is being hired for.
- **Responsibilities:** Provide the **Role** reference an evaluation is contextualized against.
- **Shared Language:** Job, Role, Position, Requisition.
- **Owns (aggregates):** None as a first-class mutable aggregate at MVP. **Role** enters our model as a **Role Reference (value object)** — we reference the customer's role/req; we do not own it (INV-9).
- **References:** The customer's ATS/req (externally owned).
- **Never Owns:** Requisitions, Positions, Offers — these belong to the customer's system of record (INV-9).
- **Interactions:** A Role Reference is attached to every Evaluation Campaign and contextualizes every Evaluation (INV-5).
- **Why the boundary exists:** We are the System of Intelligence, never the System of Record (ARCH-01). Keeping Work as reference-only structurally forbids us from drifting into being an ATS.

### BC-4 · Evaluation Context *(Core / the heart of the product)*
- **Purpose:** Turn evidence into explainable, confidence-qualified, fairness-gated judgment.
- **Responsibilities:** Organize evaluation work (Campaign); collect and structure evidence; verify integrity; evaluate against the calibrated bar; attach confidence; produce advisory recommendations; produce explanations.
- **Shared Language:** Evaluation Campaign, Candidate Evaluation, Evaluation Session, Sensor, Work Sample, Evidence, Evidence Item, Signal, Evaluation, Evaluation Score, Confidence, Recommendation, Explanation, Calibration.
- **Owns (aggregates):** **Evaluation Campaign** (root, primary organizing aggregate), **Candidate Evaluation** (root), and the entities within them (Invitation, Work Sample submission, Evidence Item, Evaluation, Recommendation, Calibration).
- **References:** Candidate (by identity), Role Reference, Organization (tenant), and — for the delivery gate — the Campaign's Fairness Verdict (BC-6).
- **Never Owns:** The **Hiring Decision** (human-owned, BC-5), **Fairness/Integrity verdicts as authority** (governed by BC-6 even though scores travel with evidence/evaluation), the **Candidate** person (BC-2).
- **Interactions:** The productive core; consumes Candidate + Role + Calibration, submits to the Fairness gate, hands Recommendations to Decision.
- **Why the boundary exists:** This *is* the moat (DOC-03). It must be the richest, most protected context — and it must be kept structurally distinct from the *human decision*, because "we recommend; humans decide" (INV-1) is only credible if recommendation and decision are different things owned in different places.

### BC-5 · Decision & Delivery Context
- **Purpose:** Capture the accountable **human** decision and deliver hiring intelligence back to the customer.
- **Responsibilities:** Present finalists + evidence to a human; record the human Hiring Decision and any override; release candidate feedback; export results across the product boundary.
- **Shared Language:** Hiring Decision, Decision Outcome, Feedback, Export Package, Offer/Rejection *(reference-only)*.
- **Owns (aggregates):** **Hiring Decision** (root), **Feedback** (root), **Export Package** (root).
- **References:** Candidate Evaluation / Recommendation (by identity), Candidate, User (the decision-maker), Campaign.
- **Never Owns:** The Recommendation (advisory; owned in BC-4), the Offer (customer-owned, INV-9), the evaluation logic.
- **Interactions:** Consumes fairness-passed, explained Recommendations; produces the binding decision and the deliver-back artifact.
- **Why the boundary exists:** Accountability is legally and ethically load-bearing (DOC-05 P2, INV-1). The human decision must be its **own** modeled thing — with its own identity, actor, timestamp, and audit — so that "a human decided this" is a fact in the model, not an assumption.

### BC-6 · Trust, Fairness & Compliance Context *(the authoritative ground)*
- **Purpose:** Enforce the non-negotiable gates.
- **Responsibilities:** Fairness / adverse-impact assessment across a campaign's candidate set; integrity (authenticity) verification of evidence; consent governance; tenant isolation; the append-only audit ledger.
- **Shared Language:** Fairness, Fairness Verdict, Bias, Adverse Impact, Integrity Score, Explainability, Consent, Audit, Tenant Isolation, Human Accountability.
- **Owns (aggregates):** **Consent** (root), **Audit Record** (append-only root). Owns the **Fairness Verdict** (value object, campaign-scoped) and the **Integrity Score** (value object, evidence-scoped) as authoritative outputs.
- **References:** Everything, by identity (it observes/gates all contexts).
- **Never Owns:** The evaluation judgment itself, the candidate, or the decision — it *governs* them without *being* them.
- **Interactions:** Pervades every context as gate and record (ARCH-02 §7): consent gates data use; integrity gates evidence trust; fairness gates recommendation delivery; audit records everything; isolation walls every access.
- **Why the boundary exists:** Gates that are "features inside other contexts" get bypassed under deadline pressure (RK-15/RK-6). Making Trust its **own** authoritative context — that everything depends on and nothing can override — is what makes the gates structural rather than optional.

### BC-7 · Commercial Context *(generic; thin at MVP)*
- **Purpose:** Frame the business relationship and the billing unit.
- **Responsibilities:** Recognize the **Candidate Evaluation** as the billing unit (one Candidate × one Role × one Recommendation); hold subscription/entitlement context.
- **Shared Language:** Enterprise Customer, Design Partner, Subscription, Candidate Evaluation *(as billing unit)*.
- **Owns (aggregates):** None new at MVP (billing detail deferred). It *observes* the Candidate Evaluation defined in BC-4 for metering.
- **References:** Organization, Candidate Evaluation.
- **Never Owns:** The evaluation logic; it only *counts* completed Candidate Evaluations.
- **Why the boundary exists:** Pricing must never distort the domain. Isolating commerce ensures the billing unit *reflects* a real domain concept (a completed evaluation) rather than the domain being shaped to bill.

> **Deferred contexts** (vocabulary owned, model deferred post-MVP): **Calibration & Memory** (Company Calibration, Hiring Memory), **Outcome & Learning** (Outcome, Outcome Learning, Evidence Graph), **Benchmarking** (Benchmark, Hiring Intelligence Network). Their terms are frozen (DOC-04); their aggregates are intentionally not modeled here (see §12).

---

## 3. Aggregates

An **aggregate** is a cluster of domain objects treated as a single unit for the purpose of business-rule consistency. Each aggregate has one **root** — the only object the outside world holds a reference to — and a **boundary** inside which all invariants must always hold true. Objects in one aggregate reference objects in another **only by identity**, never by direct containment.

### 3.0 The central modeling decision (and an honest tradeoff)

The CTO's instinct is correct: **the Evaluation Campaign is the primary aggregate root** — it is the Unit of Work (AD-09) around which scope, lifecycle, fairness, audit, reporting, and export all cohere. But a campaign may contain 120 candidates, each with a work sample, evidence, an evaluation, and a recommendation. If all of that lived *inside* one Campaign aggregate, the consistency boundary would be enormous: every candidate's evidence change would contend on the whole campaign, and the model would be unusable at scale.

Therefore:

> **AD-16 — The Evaluation Campaign is the primary *organizing* aggregate; each Candidate Evaluation is its own aggregate that references the Campaign by identity.**
> The Campaign owns campaign-level truth (lifecycle, scope, calibration, the campaign roster, and the campaign-level **Fairness Verdict**). Each Candidate Evaluation owns one candidate's evaluation truth (invitation → work sample → evidence → evaluation → recommendation).

**The consequence — a genuine cross-aggregate invariant.** Fairness is assessed *across the campaign's candidate set* (adverse impact is a property of the set, not of one candidate — INV-3), so the Fairness Verdict is **campaign-scoped**. But the thing gated *by* fairness — delivery of a Recommendation — lives in the per-candidate aggregate. This means **INV-3 is a cross-aggregate invariant**: it cannot be enforced inside a single aggregate's boundary. We name this openly rather than hide it. It is enforced by a **domain policy/service** ("a Recommendation may not transition to *Delivered* unless its Campaign's Fairness Verdict is *Passed*"), and its coordination mechanics (immediate vs. eventual) are an ARCH-04/ARCH-05 concern — **but the rule itself is owned here.**

### 3.1 Aggregate Roots — overview

| # | Aggregate Root | Context | One-line purpose | Billing / gate significance |
|---|---|---|---|---|
| AGG-1 | **Organization** | BC-1 | The tenant and its users. | Tenant boundary (INV-10). |
| AGG-2 | **Candidate** | BC-2 | The durable person. | Persists across afterlife (INV-7). |
| AGG-3 | **Evaluation Campaign** | BC-4 | **Primary** organizing unit of work. | Owns Fairness Verdict; scope of audit/export. |
| AGG-4 | **Candidate Evaluation** | BC-4 | One candidate × one role × one recommendation. | **The billing unit** (D-04.A2). |
| AGG-5 | **Hiring Decision** | BC-5 | The accountable human choice. | Human accountability (INV-1). |
| AGG-6 | **Feedback** | BC-5 | Released candidate-facing feedback. | Release gate (Rule 4). |
| AGG-7 | **Export Package** | BC-5 | Deliver-back artifact. | Product boundary end (KD-12.7). |
| AGG-8 | **Consent** | BC-6 | Governs candidate-data use. | Consent gate (INV-11). |
| AGG-9 | **Audit Record** | BC-6 | Append-only ledger entry. | Auditability (INV-2 record; P8). |

### 3.2 Each aggregate in detail

---

**AGG-1 · Organization** *(root)*
- **Purpose:** Establish the customer tenant and the users/roles permitted to act within it.
- **Responsibilities:** Hold tenant identity; manage Users and their permissions; hold org-level consent configuration.
- **Lifecycle:** Provisioned → Active → Suspended → Closed.
- **Owned entities:** **User** (identity + role/permissions within this tenant).
- **Owned value objects:** Tenant Id, Organization Profile, Permission/Role (authorization sense — *distinct from the Work "Role"*), Consent Configuration.
- **References other aggregates:** None (root of authority).
- **Business invariants:** Every User belongs to exactly one Organization; every downstream action carries this Organization's Tenant Id (INV-10); a User may act only within permissions granted here.

---

**AGG-2 · Candidate** *(root)*
- **Purpose:** Represent a person as a durable participant within a tenant.
- **Responsibilities:** Hold candidate identity and contact info; hold durable afterlife status; link (by identity) to the Candidate Evaluations the person has participated in.
- **Lifecycle:** *(see §6 Candidate state machine)* Prospective → Active-in-Campaign → Evaluated → (Advanced | Rejected→Afterlife) — candidacy **persists** (INV-7).
- **Owned entities:** none required at MVP beyond the root (contact records modeled as value objects).
- **Owned value objects:** Candidate Id, Contact Info, Candidate Afterlife Status.
- **References other aggregates:** Organization (tenant); Candidate Evaluations (by identity — not owned).
- **Business invariants:** A Candidate belongs to exactly one tenant (INV-10); a Candidate is never silently erased — rejection transitions to afterlife (INV-7); a Candidate may participate in **many** Campaigns but has **at most one active Candidate Evaluation per Campaign** (AD-09).

---

**AGG-3 · Evaluation Campaign** *(root — PRIMARY organizing aggregate)*
- **Purpose:** Organize **all** evaluation activity for one Role into a bounded unit of work.
- **Responsibilities:** Own campaign lifecycle; define scope (Role Reference + candidate roster); hold the (thin) Calibration of the bar; own the campaign-level Fairness Verdict; be the boundary for audit, reporting, and export.
- **Lifecycle:** *(see §6)* Draft → Active → Evaluating → Fairness-Review → Concluded | Cancelled.
- **Owned entities:** **Calibration** *(resolves ARCH-02 OQ-1: Calibration is an entity **owned within the Campaign** at MVP — it is meaningless outside its campaign; company-level calibration is deferred)*; **Campaign Roster** entry per participating candidate (a lightweight participation link, referencing Candidate + its Candidate Evaluation by identity).
- **Owned value objects:** Campaign Id, Campaign Status, Role Reference, Time Window, **Fairness Verdict** *(campaign-scoped; authored under BC-6 authority)*.
- **References other aggregates:** Organization (tenant); Candidate (by identity, via roster); Candidate Evaluation (by identity, via roster).
- **Business invariants:** Every evaluation activity belongs to **exactly one** Campaign (AD-09); a Campaign belongs to exactly one Organization/tenant (INV-10); a Campaign begins **after** candidate import and ends **after** delivery/cancel (KD-12.7); **historical campaign evidence is immutable** — referenced, never modified (AD-09); a Campaign cannot reach *Concluded* unless its Fairness Verdict is *Passed* (INV-3, cross-aggregate — see §3.0).

---

**AGG-4 · Candidate Evaluation** *(root — the workhorse and the billing unit)*
- **Purpose:** Hold the complete evaluation of **one Candidate for one Role**, culminating in **one** Recommendation. *This is the billing unit* (D-04.A2).
- **Responsibilities:** Sequence one candidate's participation from invitation through recommendation; own the evidence and judgment for that candidate; carry confidence, integrity, and explanation with the judgment.
- **Lifecycle:** *(see §6)* Invited → Started → Submitted → Evidence-Structured → Evaluated → Recommended → (Delivered | Withdrawn/Expired).
- **Owned entities:** **Invitation**; **Work Sample** (the candidate's submission — the MVP Sensor, AD-10); **Evidence Item** (one or more discrete observations); **Evaluation** (the judgment); **Recommendation** (the advisory output).
- **Owned value objects:** Candidate Evaluation Id, Participation Status, Evaluation Score, Confidence, Integrity Score *(authored under BC-6 authority, travels with the evidence)*, Recommendation Level, Explanation, Engineering Dimension Score (per dimension: technical quality, reasoning, debugging, communication, engineering maturity — AD-10), Evidence Reference.
- **References other aggregates:** Evaluation Campaign (by identity — the owning unit of work); Candidate (by identity); the Campaign's Fairness Verdict (read, for the delivery gate).
- **Business invariants:**
  - A **Recommendation cannot exist without an Evaluation** (INV-a below); an **Evaluation cannot exist without integrity-checked Evidence** (INV-4/§7); Evidence belongs to **exactly one** Candidate Evaluation and thereby **exactly one** Campaign (AD-09).
  - Every Evaluation is **contextualized** by the Campaign's Calibration/Role (INV-5); every Evaluation and Recommendation **carries Confidence** (INV-6).
  - A Recommendation is **advisory only** — it can never transition itself into a Hiring Decision (INV-1).
  - A Recommendation may **not** transition to *Delivered* without (a) an attached **Explanation** (INV-2) and (b) a *Passed* Campaign Fairness Verdict (INV-3).
  - One Candidate Evaluation = one Candidate + one Role + one final Recommendation, regardless of how many Evaluation Sessions occurred (D-04.A2); a second Role for the same candidate is a **new** Candidate Evaluation.

---

**AGG-5 · Hiring Decision** *(root — the accountable human act)*
- **Purpose:** Record the binding, **human** choice to advance / hold / reject a candidate, informed by (never dictated by) the Recommendation.
- **Responsibilities:** Bind a decision to a human actor, a time, and a justification; capture any override of the Recommendation.
- **Lifecycle:** *(see §6)* Pending → Decided (Advance | Hold | Reject) → [Recorded/immutable].
- **Owned entities:** none beyond the root.
- **Owned value objects:** Decision Id, Decision Outcome, Decision-Maker (User reference), Decision Timestamp, Override Justification (present iff the decision diverges from the Recommendation).
- **References other aggregates:** Candidate Evaluation / Recommendation (by identity); Candidate; User (the accountable human); Campaign.
- **Business invariants:** A Hiring Decision is **always** made by a named human User (INV-1); the system **never** creates a Hiring Decision autonomously for a high-risk decision (INV-1 / DC-7 / P2); a decision that diverges from the Recommendation **must** carry an Override Justification; once Decided, a Hiring Decision is **immutable** (a new decision supersedes; it does not edit history — audit integrity).

---

**AGG-6 · Feedback** *(root — candidate-facing release)*
- **Purpose:** Deliver constructive, candidate-appropriate feedback (especially on rejection), on the customer's terms.
- **Responsibilities:** Generate candidate-view feedback from the evaluation; hold the release lifecycle; deliver only after explicit recruiter release.
- **Lifecycle:** *(see §6)* Draft → Released → Delivered *(never auto-delivered)*.
- **Owned value objects:** Feedback Id, Feedback Content (candidate-view Explanation only), Release State, Release Actor (User), Delivery Timestamp.
- **References other aggregates:** Candidate Evaluation (by identity); Candidate; User (releaser).
- **Business invariants:** Feedback is **delivered only after recruiter release** (PRODUCT-01 Rule 4); Feedback exposes **only** the candidate-appropriate Explanation, never internal mechanics (P13); framing is "not the strongest match," never "not good enough" (DOC-06 §10).

---

**AGG-7 · Export Package** *(root — deliver-back boundary)*
- **Purpose:** Package hiring intelligence for hand-back to the customer — the point at which our product boundary **ends** (KD-12.7).
- **Responsibilities:** Assemble recommendations + human decisions + explanations for a campaign into a deliverable; record what was delivered and to whom.
- **Lifecycle:** *(see §6)* Requested → Assembled → Delivered.
- **Owned value objects:** Export Id, Export Scope (campaign reference), Export Contents (references to decisions/recommendations/explanations), Delivery Record.
- **References other aggregates:** Campaign; Hiring Decisions; Candidate Evaluations (by identity).
- **Business invariants:** An Export Package delivers **only** fairness-passed, explained outputs (INV-2/INV-3); delivery **ends** our responsibility — we never action the Offer (INV-9, KD-12.7); every export is auditable (P8).

---

**AGG-8 · Consent** *(root — governs candidate-data use)*
- **Purpose:** Govern whether and how a candidate's data may be used.
- **Responsibilities:** Capture consent grant/scope; enforce withdrawal and expiry; gate every candidate-data use.
- **Lifecycle:** *(see §6)* Requested → Granted → (Withdrawn | Expired).
- **Owned value objects:** Consent Id, Consent Scope, Grant State, Grant/Withdrawal Timestamps, Retention Window.
- **References other aggregates:** Candidate (by identity); optionally Campaign (scope).
- **Business invariants:** **No evidence collection or evaluation may proceed without an active Consent** (INV-11); candidate data is **never sold** (INV-11 / KD-03.14); withdrawal is honored going forward and recorded (P3).

---

**AGG-9 · Audit Record** *(root — append-only ledger)*
- **Purpose:** Provide an immutable, complete record of every material action.
- **Responsibilities:** Record what happened, by whom, when, in which tenant, organized by campaign.
- **Lifecycle:** Appended → *(never mutated, never deleted within retention)*.
- **Owned value objects:** Audit Id, Actor Reference, Action Descriptor, Tenant Id, Campaign Reference, Timestamp, Before/After references *(by identity, not content copies)*.
- **References other aggregates:** All, by identity.
- **Business invariants:** **Append-only, complete, nothing withheld** (P8); every material action across every aggregate produces exactly one Audit Record; audit is scoped by tenant and organized by campaign (INV-10).

---

## 4. Entities

An **entity** has **identity** (it is the same thing over time even as its attributes change) and **mutable state** with a **lifecycle**. Value objects (§5) do not — they are defined entirely by their values. Below, each entity: **Identity · Mutable State · Lifecycle · Relationships · Business Rules.** Entities are listed under their owning aggregate.

| Entity | Owning Aggregate | Identity | Mutable? |
|---|---|---|---|
| Organization | AGG-1 (root) | Organization Id | Yes |
| User | AGG-1 | User Id (within tenant) | Yes |
| Candidate | AGG-2 (root) | Candidate Id (within tenant) | Yes (afterlife status) |
| Evaluation Campaign | AGG-3 (root) | Campaign Id | Yes (lifecycle) |
| Calibration | AGG-3 | Calibration Id (within campaign) | Yes (until campaign Active) |
| Candidate Evaluation | AGG-4 (root) | Candidate Evaluation Id | Yes (lifecycle) |
| Invitation | AGG-4 | Invitation Id | Yes (status) |
| Work Sample | AGG-4 | Work Sample Id | Yes until Submitted, then immutable |
| Evidence Item | AGG-4 | Evidence Item Id | **No after creation** (immutable, AD-09) |
| Evaluation | AGG-4 | Evaluation Id | Yes until Recommended, then immutable |
| Recommendation | AGG-4 | Recommendation Id | Yes (status), content immutable once formed |
| Hiring Decision | AGG-5 (root) | Decision Id | Immutable once Decided |
| Feedback | AGG-6 (root) | Feedback Id | Yes (release state) |
| Export Package | AGG-7 (root) | Export Id | Yes until Delivered |
| Consent | AGG-8 (root) | Consent Id | Yes (grant state) |
| Audit Record | AGG-9 (root) | Audit Id | **No** (append-only) |

Selected entities in detail (those with non-trivial rules):

**Candidate** — *Identity:* Candidate Id, unique within tenant. *Mutable State:* contact info, afterlife status. *Lifecycle:* durable (never deleted within consent/retention; INV-7). *Relationships:* participates in many Campaigns via roster; each participation is one Candidate Evaluation. *Rules:* one active Candidate Evaluation per Campaign; belongs to exactly one tenant.

**Evaluation Campaign** — *Identity:* Campaign Id. *Mutable State:* status, roster, calibration (mutable only before Active), fairness verdict. *Lifecycle:* §6.1. *Relationships:* owns Calibration + roster; references Role + Candidates + Candidate Evaluations. *Rules:* the AGG-3 invariants; calibration is frozen once the campaign goes Active (you cannot move the bar mid-campaign — fairness/comparability).

**Calibration** — *Identity:* Calibration Id (within campaign). *Mutable State:* the role bar/priorities. *Lifecycle:* editable in Draft; **frozen when the Campaign becomes Active.** *Relationships:* owned by exactly one Campaign; consumed by every Evaluation in it. *Rules:* Calibration adjusts the **bar**, never the **gates** — it can never weaken fairness, integrity, explainability, or consent (Customization Pyramid; P1).

**Candidate Evaluation** — *Identity:* Candidate Evaluation Id. *Mutable State:* participation status, and (until finalized) the owned Evaluation/Recommendation. *Lifecycle:* §6.3. *Relationships:* owns Invitation/Work Sample/Evidence/Evaluation/Recommendation; references Campaign + Candidate. *Rules:* the AGG-4 invariants (recommendation⇐evaluation⇐evidence; confidence always; advisory only; delivery requires explanation + fairness pass).

**Evidence Item** — *Identity:* Evidence Item Id. *Mutable State:* **none** — an Evidence Item is **immutable once recorded** (AD-09). *Lifecycle:* Created → (referenced forever). *Relationships:* produced from a Work Sample; belongs to exactly one Candidate Evaluation/Campaign; cited by an Evaluation/Explanation. *Rules:* immutable; carries its Integrity Score; role-relevant; never silently discarded (retention governs expiry, not deletion-at-will).

**Recommendation** — *Identity:* Recommendation Id. *Mutable State:* status (Formed → Delivered); its *content* is immutable once formed. *Lifecycle:* §6.4. *Relationships:* one per completed Candidate Evaluation; consumed by Decision Support + Export. *Rules:* advisory only (never a decision, INV-1); no bare score — carries Explanation + Confidence (INV-2/INV-6); undeliverable without a Passed Campaign Fairness Verdict (INV-3).

**Hiring Decision** — *Identity:* Decision Id. *Mutable State:* none once Decided (immutable). *Lifecycle:* §6.5. *Relationships:* references one Recommendation/Candidate Evaluation + one accountable User. *Rules:* human-made (INV-1); override justified if divergent; immutable once made.

---

## 5. Value Objects

A **value object** has **no identity** and is **immutable**: two value objects with the same values are the same value (an Evaluation Score of 89 is an Evaluation Score of 89 — it has no separate existence to track). Value objects are where much of the domain's *meaning* lives, and modeling them explicitly (rather than as bare numbers/strings) is what stops "a bare score" from ever existing.

| Value Object | Owning Context | What it captures | Key rule |
|---|---|---|---|
| **Tenant Id** | BC-1 | The isolation boundary. | Present on every action; never crosses tenants (INV-10). |
| **Permission / Access Role** | BC-1 | What a User may do. | *Distinct from Work "Role."* Never conflated (DOC-04). |
| **Contact Info** | BC-2 | How to reach a candidate. | Consent-governed use (INV-11). |
| **Candidate Afterlife Status** | BC-2 | Durable post-outcome status. | Rejection ⇒ afterlife, never erasure (INV-7). |
| **Role Reference (Role Profile)** | BC-3 | The referenced role/req + its profile. | Reference-only; we never own it (INV-9). |
| **Campaign Status** | BC-4 | Where a campaign is in its lifecycle. | Legal transitions only (§6.1). |
| **Participation Status** | BC-4 | Where one candidate is in a campaign. | Legal transitions only (§6.3). |
| **Engineering Dimension Score** | BC-4 | Evidence quality on one dimension (technical quality / reasoning / debugging / communication / engineering maturity). | Multi-dimensional, never collapsed to a single opaque number (AD-10). |
| **Evaluation Score** | BC-4 | Candidate quality for a role. | Never bare — always with Explanation + Confidence (INV-2, D-04.A5). |
| **Confidence** | BC-4 | The system's certainty in *its own* judgment. | Always attached; low confidence surfaced honestly (INV-6). |
| **Recommendation Level** | BC-4 | The advisory action (e.g., advance / hold / not-a-fit-here). | Advisory only; never a decision (INV-1). |
| **Explanation** | BC-4/BC-6 | Audience-appropriate evidence + reasoning. | Nothing ships unexplained (INV-2); audience-scoped (P13). |
| **Evidence Reference** | BC-4 | A citation to an immutable Evidence Item. | Points to immutable evidence (AD-09). |
| **Integrity Score** | BC-6 | Authenticity/trustworthiness of evidence. | Authoritative; cannot be overridden; low integrity flags, never silently passes. |
| **Fairness Verdict** | BC-6 | Pass / Hold for a campaign's candidate set. | **Campaign-scoped**; authoritative; delivery-gating (INV-3). |
| **Decision Outcome** | BC-5 | Advance / Hold / Reject. | Set only by a human (INV-1). |
| **Consent Grant** | BC-6 | Scope + state of candidate consent. | Gates all candidate-data use (INV-11). |
| **Time Window** | shared | A bounded period (e.g., campaign window, consent retention, invitation validity). | Explicit; no open-ended retention (DC-3). |
| **Audit Entry** | BC-6 | Actor + action + tenant + time. | Append-only; complete (P8). |

> **Modeling note.** Evaluation Score, Confidence, and Integrity Score are three **separate** value objects precisely because DOC-04 (D-04.A1) forbids collapsing them. The type system of the domain — even before any code — must keep them distinct so no report, API, or screen can ever present one where another is meant. A bare "Score" is **not a value object in this model**; it is forbidden (D-04.A5).

---

## 6. State Machines

Every entity that changes state has a formal state machine: **States · Transitions · Forbidden transitions · Terminal states.** These are *conceptual* business lifecycles, not workflow-engine definitions.

### 6.1 Evaluation Campaign
- **States:** Draft → Active → Evaluating → Fairness-Review → Concluded · Cancelled.
- **Transitions:** Draft→Active (calibration frozen, roster set); Active→Evaluating (evaluations underway); Evaluating→Fairness-Review (all in-scope evaluations formed); Fairness-Review→Concluded (**only if Fairness Verdict = Passed**); any non-terminal→Cancelled.
- **Forbidden:** Fairness-Review→Concluded when Fairness Verdict ≠ Passed (INV-3); Concluded→any (terminal); editing Calibration after Active; Draft→Concluded (cannot skip evaluation/fairness).
- **Terminal:** Concluded, Cancelled.

### 6.2 Invitation
- **States:** Issued → Accepted · Expired · Revoked.
- **Transitions:** Issued→Accepted (candidate starts); Issued→Expired (Time Window elapsed); Issued→Revoked (recruiter/consent withdrawal).
- **Forbidden:** Expired/Revoked→Accepted; Accepted→Expired.
- **Terminal:** Accepted (hands off to Candidate Evaluation), Expired, Revoked.

### 6.3 Candidate Evaluation *(participation lifecycle)*
- **States:** Invited → Started → Submitted → Evidence-Structured → Evaluated → Recommended → Delivered · Withdrawn/Expired.
- **Transitions:** each forward step requires the prior artifact (Submitted requires a Work Sample; Evaluated requires integrity-checked Evidence; Recommended requires an Evaluation + Confidence; **Delivered requires Explanation + Passed Campaign Fairness Verdict**).
- **Forbidden:** Evaluated without Evidence (INV-4); Recommended without Evaluation (INV-a); Delivered without Explanation (INV-2) or without fairness pass (INV-3); any state→auto-Decision (there is no "Decided" state here — the Hiring Decision is a *separate aggregate*, INV-1); re-opening a Delivered evaluation to modify historical evidence (AD-09).
- **Terminal:** Delivered, Withdrawn/Expired.

### 6.4 Recommendation
- **States:** Formed → Delivered · Superseded.
- **Transitions:** Formed→Delivered (Explanation attached + fairness passed); Formed→Superseded (a re-evaluation forms a new Recommendation).
- **Forbidden:** Formed→Delivered without Explanation (INV-2) or fairness pass (INV-3); Delivered→edited (content immutable); Recommendation→Decision (it can never *become* a decision — a Decision is made *about* it, INV-1).
- **Terminal:** Delivered, Superseded.

### 6.5 Hiring Decision
- **States:** Pending → Decided(Advance|Hold|Reject).
- **Transitions:** Pending→Decided by a **named human User**; a divergent decision requires Override Justification.
- **Forbidden:** system-initiated Decided for high-risk (INV-1/DC-7); Decided→edited (immutable; supersede via a new decision); Decided without a referenced Recommendation + Evaluation.
- **Terminal:** Decided.

### 6.6 Feedback
- **States:** Draft → Released → Delivered.
- **Transitions:** Draft→Released (explicit recruiter release, Rule 4); Released→Delivered (sent to candidate).
- **Forbidden:** Draft→Delivered (no auto-delivery, Rule 4); Delivered→edited; exposing non-candidate-view content (P13).
- **Terminal:** Delivered.

### 6.7 Export Package
- **States:** Requested → Assembled → Delivered.
- **Transitions:** Requested→Assembled (gather fairness-passed, explained outputs); Assembled→Delivered (hand back to customer).
- **Forbidden:** Assembled with any unexplained/fairness-failing output (INV-2/INV-3); Delivered→our further action on the Offer (INV-9).
- **Terminal:** Delivered.

### 6.8 Consent
- **States:** Requested → Granted → Withdrawn · Expired.
- **Transitions:** Requested→Granted; Granted→Withdrawn (candidate action); Granted→Expired (retention Time Window elapsed).
- **Forbidden:** evidence/evaluation while state ≠ Granted (INV-11); Withdrawn/Expired→silently-Granted.
- **Terminal:** Withdrawn, Expired.

> **Cross-cutting note:** the Candidate lifecycle (Prospective → Active → Evaluated → Advanced|Rejected→Afterlife) sits *above* these; it is durable (INV-7) and is not terminated by any single campaign's terminal states.

---

## 7. Business Invariants — the single authoritative list

**These are the rules that can never be violated, gathered in one place so they exist exactly once.** They are inherited from DOC-04 §8 (INV-1…INV-12, the frozen truths) and extended with the structural invariants this domain model introduces (INV-a…INV-e). **No invariant appears twice; where a rule was implied in ARCH-02, it is stated here canonically and referenced there, not re-defined.**

*Inherited (frozen in DOC-04 — authoritative):*
1. **INV-1 — Human accountability is mandatory.** A Hiring Decision is always a human act; the system recommends, it never decides (esp. high-risk). *(Owner: AGG-5 + BC-6.)*
2. **INV-2 — No unexplained output.** Every Signal, Evaluation, and Recommendation carries its specific Evidence and reasoning; nothing ships as a bare score. *(Owner: AGG-4 / Explanation.)*
3. **INV-3 — No recommendation without fairness.** No Recommendation is *delivered* without a Passed (campaign-scoped) Fairness Verdict. *(Owner: AGG-3 Fairness Verdict; enforced cross-aggregate — §3.0.)*
4. **INV-4 — Evidence over claims.** A supported decision is grounded in Evidence of ability, never the Resume alone; no Evaluation without integrity-checked Evidence. *(Owner: AGG-4.)*
5. **INV-5 — Every Evaluation is contextualized.** No generic judgment; every Evaluation is against a Role, contextualized by Calibration. *(Owner: AGG-4 + AGG-3 Calibration.)*
6. **INV-6 — Confidence is always expressed.** Every Evaluation/Recommendation states its Confidence; low-evidence outputs are never presented as certain. *(Owner: AGG-4 / Confidence.)*
7. **INV-7 — Candidacy persists.** A rejected Candidate transitions to the afterlife; never silently erased (subject to consent/retention). *(Owner: AGG-2.)*
8. **INV-8 — Benchmarks are aggregate.** Benchmarks derive from the network in aggregate/anonymized form; one party's private data is never exposed to another. *(Owner: BC-Benchmarking — deferred, but the invariant is binding when built.)*
9. **INV-9 — Never the system of record.** We reference Requisitions/Positions/Offers owned by the customer; we never become the ATS/job portal. *(Owner: BC-3 + AGG-7.)*
10. **INV-10 — Tenant isolation & single tenancy of action.** Every action belongs to exactly one tenant; cross-tenant access is impossible by construction. *(Owner: BC-1 + BC-6.)* *(Consolidates DOC-04's INV-8 tenancy aspect with the "every action, one tenant" rule.)*
11. **INV-11 — Consent governs candidate data.** Candidate evidence use, retention, and portability are consent-governed; candidate data is never sold. *(Owner: AGG-8.)*
12. **INV-12 — The loop closes (when outcomes exist).** Where Outcomes are available they feed Outcome Learning; the system is designed to learn, not merely score. *(Owner: BC-Outcome — deferred; binding when built.)*
13. **INV-13 — Sensors are inputs, never the product.** No sensor (work sample/interview/assessment) is modeled, sold, or positioned as the product; the product is Decision Quality. *(Owner: BC-4.)* *(From DOC-04 INV-10.)*

*Structural (introduced by this model):*
- **INV-a — Recommendation ⇐ Evaluation ⇐ Evidence.** A Recommendation cannot exist without an Evaluation; an Evaluation cannot exist without integrity-checked Evidence. *(Owner: AGG-4.)*
- **INV-b — Evidence immutability & single ownership.** An Evidence Item is immutable once recorded and belongs to exactly one Candidate Evaluation, hence exactly one Campaign. *(Owner: AGG-4; realizes AD-09.)*
- **INV-c — Calibration frozen at Active.** A Campaign's Calibration cannot change once the Campaign is Active (comparability/fairness). *(Owner: AGG-3.)*
- **INV-d — Recommendation and Decision are different aggregates.** A Recommendation can never transition into a Hiring Decision; a Decision is a separate, human-owned aggregate that *references* it. *(Owner: AGG-4/AGG-5; realizes INV-1 structurally.)*
- **INV-e — Immutability of accountable/audited facts.** A recorded Hiring Decision and every Audit Record are immutable; corrections supersede, never edit. *(Owner: AGG-5/AGG-9.)*

> **These invariants are technology-independent.** They must hold whether enforced in a database, a service, an API, a UI, or a prompt. Downstream layers *enforce* them; only this document *defines* them.

---

## 8. Business Policies *(changeable — deliberately separated from invariants)*

**Policies are rules that may change without violating the domain.** Invariants (§7) may *never* change; policies are configuration/decisions that evolve with the business or per customer (within the Customization Pyramid — never weakening a gate). Keeping them separate is what prevents a changeable setting from being mistaken for an inviolable truth, and vice versa.

| Policy | What it governs | May vary by | Constraint (what it may never do) |
|---|---|---|---|
| **Retention Policy** | How long Evidence/candidate data is kept before expiry. | Tenant, jurisdiction. | Never open-ended; never overrides consent withdrawal (INV-11, DC-3). |
| **Invitation Expiry Policy** | The Invitation Time Window. | Campaign, tenant. | Never zero (candidate must have fair opportunity). |
| **Reminder Timing Policy** | When/whether to nudge candidates. | Campaign, tenant. | Never violates "communicate at meaningful moments only / no black hole" (DOC-06). |
| **Feedback Release Policy** | Default posture for releasing candidate feedback. | Tenant. | Never auto-delivers before recruiter release (Rule 4 — an invariant boundary the policy operates *within*). |
| **Calibration Policy** | How the role bar is elicited/expressed (thin at MVP). | Campaign/Role. | Never adjusts a **gate** (fairness/integrity/explainability/consent) — only the bar (INV-c, P1). |
| **Outcome Learning Policy** *(deferred)* | How/whether outcomes feed learning. | Tenant (opt-in). | Never uses data without consent; never exposes cross-tenant data (INV-8/INV-11). |
| **Benchmark Participation Policy** *(deferred)* | Whether a tenant contributes to/consumes network benchmarks. | Tenant (opt-in). | Aggregate-only; never exposes private data (INV-8). |

> **The test:** if changing the rule would make the product *unfair, unexplainable, unaccountable, or non-consensual*, it is an **invariant**, not a policy. If changing it merely tunes behavior within those guarantees, it is a **policy**.

---

## 9. Domain Glossary — canonical terms (one word, one meaning)

This section is the **enforcement summary** of DOC-04's frozen vocabulary as it applies to the model. DOC-04 remains the full dictionary; here we restate the load-bearing terms with their forbidden synonyms, because these are the ones engineers, APIs, UIs, and prompts most often corrupt.

| Canonical term | Means (exactly) | **Forbidden synonyms — never use** |
|---|---|---|
| **Evaluation Campaign** | The bounded run of Candidate Evaluations for one Role — the Unit of Work. | ~~Assessment~~ · ~~Hiring Process~~ · ~~Session~~ · ~~Batch~~ · ~~Project~~ · ~~Drive~~ |
| **Candidate Evaluation** | One Candidate × one Role × one Recommendation — the **billing unit**. | ~~Interview~~ · ~~Screening~~ · ~~Assessment~~ · ~~Test~~ (these are sensors, not the evaluation) |
| **Evaluation Session** | One time-bounded evidence-collection sitting. | ~~Evaluation~~ (a session is not the judgment) · never a billing unit |
| **Evaluation** | The evidence-cited judgment of ability for a Role. | ~~Decision~~ · ~~Score~~ · ~~Interview~~ |
| **Recommendation** | The advisory suggested action. | ~~Decision~~ · ~~Verdict~~ · ~~Ruling~~ (it is never binding) |
| **Hiring Decision** | The binding **human** choice. | ~~Recommendation~~ · ~~System decision~~ · ~~Auto-decision~~ (there is no such thing — INV-1) |
| **Evidence** | Observed/verified information about actual ability. | ~~Resume~~ · ~~Claim~~ · ~~Data~~ (a resume is a claim, not evidence of ability) |
| **Evidence Item** | One discrete, immutable observation. | ~~Record~~ · ~~Row~~ · ~~Log~~ |
| **Signal** | An interpreted indicator derived *from* Evidence. | ~~Evidence~~ (evidence is observed; a signal is interpreted) |
| **Sensor** | An instrument that collects Evidence (e.g., Work Sample). | ~~Product~~ · ~~The AI interview~~ (a sensor is never the product — INV-13) |
| **Evaluation Score** | Candidate quality for a Role. | bare ~~Score~~ (forbidden — D-04.A5) · ~~Rating~~ · ~~Grade~~ |
| **Confidence** | The system's certainty in its own judgment. | ~~Accuracy~~ · ~~Integrity Score~~ · ~~Score~~ |
| **Integrity Score** | Authenticity/trustworthiness of Evidence. | ~~Trust Score~~ (deprecated) · ~~Confidence~~ · ~~Fraud score~~ |
| **Fairness Verdict** | Campaign-level pass/hold on adverse impact. | ~~Bias check~~ (informal) · ~~Compliance flag~~ |
| **Calibration** | The learned/elicited standard of "good" for a Role. | ~~Config~~ · ~~Settings~~ · ~~Weights~~ (it is a business standard, not a knob) |
| **Consent** | The candidate's governed permission for data use. | ~~Terms~~ · ~~Agreement~~ · ~~Flag~~ |

> **Rule:** if a future API field, table, screen label, report column, or prompt variable uses a forbidden synonym, it is a **defect**, regardless of whether the software "works." The word is part of the contract.

---

## 10. Domain Traceability

Every element of this model traces back to its origin. No orphans.

### 10.1 Aggregates → sources
| Aggregate | ARCH-02 owner(s) | DOC-12 capability | PRODUCT-01 | ARCH-01 |
|---|---|---|---|---|
| Organization | Organization Management | C24/C25 basis | S-10 Setup | Tenant/trust boundary |
| Candidate | Candidate Identity | C2 | Actors: Candidate | SoR→SoI reference |
| Evaluation Campaign | Evaluation Campaign (Unit of Work) | Evaluation Campaign (A-04.4) | S-2; whole flow | §1A / AD-09 |
| Candidate Evaluation | Evidence+Evaluation chain | C8–C16 | Flows 4–6; S-5/S-6 | SoI core |
| Hiring Decision | Decision Support | C17 | S-7; Rule 7 | Human-in-loop |
| Feedback | Feedback Engine | C19 | S-8; Rule 4 | Candidate afterlife |
| Export Package | Export / Delivery | C18 | S-9; Flow 11 | Deliver-back boundary ends |
| Consent | Consent | C24 (authoritative) | Rule 9 | PII trust boundary |
| Audit Record | Audit | C23 (authoritative) | Rule 6 | Audit trust boundary |

### 10.2 Value objects / verdicts → gates
| VO / Verdict | Gate/authority (DOC-05) | ARCH-02 |
|---|---|---|
| Fairness Verdict | Fairness gate (INV-3) | Fairness Engine (authoritative) |
| Integrity Score | Integrity (authoritative) | Integrity Engine |
| Explanation | Explainability (INV-2, P13) | Explanation Engine (authoritative) |
| Confidence | Honesty (INV-6) | Confidence Engine |
| Consent Grant | Consent (INV-11, P3) | Consent (authoritative) |
| Tenant Id | Isolation (INV-10) | Tenant Isolation (authoritative) |

### 10.3 State machines & invariants → sources
- State machines §6.1–6.8 realize DOC-04 §6 conceptual lifecycles + ARCH-02 component lifecycles.
- Invariants §7 = DOC-04 §8 (INV-1…12, frozen) consolidated + structural INV-a…e; the fairness cross-aggregate rule realizes ARCH-02 §6/§9 constraint 2.
- Policies §8 = ARCH-02 deferred/config items + DOC-05 Customization Pyramid.

> Every aggregate, entity, value object, state machine, invariant, and policy above appears in exactly one of these traces. If a future element cannot be traced here, it does not belong in the system.

---

## Architecture Decisions *(continuing the ARCH log; ARCH-02 ended at AD-15)*

- **AD-16 — Campaign is the primary *organizing* aggregate; Candidate Evaluation is its own aggregate referencing the Campaign by identity** (§3.0). Rationale: keep the consistency boundary usable at scale; keep the Unit-of-Work coherent. Tradeoff: INV-3 becomes an explicit cross-aggregate invariant (accepted, named).
- **AD-17 — Business rules live in the domain model; all other layers enforce or reflect, never define** (§0/§1.3). This is the anti-spaghetti law.
- **AD-18 — Recommendation and Hiring Decision are distinct aggregates** (INV-d). Structurally guarantees "we recommend; humans decide" (INV-1).
- **AD-19 — Evidence Items are immutable and single-owned** (INV-b), realizing AD-09's historical-immutability at the entity level.
- **AD-20 — Calibration is owned within the Campaign and frozen at Active** (§4, INV-c). *Resolves ARCH-02 OQ-1.*
- **AD-21 — Evaluation Score, Confidence, and Integrity Score are three separate value objects** (§5), structurally preventing the collapse DOC-04 D-04.A1/A5 forbids.
- **AD-22 — Invariants vs. Policies are formally separated** (§7 vs §8), with the "unfair/unexplainable/unaccountable/non-consensual ⇒ invariant" test.

## Open Questions

1. **Cross-aggregate fairness enforcement (INV-3):** immediate consistency (block Recommendation delivery synchronously on the Campaign verdict) vs. eventual (deliver on verdict event)? — **defer the *mechanism* to ARCH-04/ARCH-05; the *rule* is fixed here.**
2. **Integrity vs. Fairness ordering** at the evidence→evaluation→delivery path: both authoritative; confirm whether integrity failure short-circuits before evaluation or flags through. *(Carried from ARCH-02 OQ-4; resolve in ARCH-04.)*
3. **Consent scope granularity:** candidate-level vs. campaign-level vs. data-use-level Consent aggregate boundaries — modeled here as its own aggregate; confirm scope in ARCH-04.
4. **Silver Medal / Talent Pool / Portable Evidence** afterlife modeling — vocabulary owned (BC-2), aggregates deferred; when built, must not violate INV-7/INV-11.
5. **Where LLM-bound PII-minimization lives** as a domain responsibility vs. cross-cutting rule. *(Carried from ARCH-02 OQ-2; resolve in Security/Trust ARCH doc.)*

## Deferred Concepts *(vocabulary frozen, model intentionally not built at MVP)*

- **Company Calibration (company-level) & Hiring Memory** — MVP has only thin, campaign-owned Calibration (AD-20). Company-level calibration and the eight Hiring Memory components (DOC-04 D-04.A3) are post-MVP aggregates.
- **Benchmarking / Hiring Intelligence Network** — INV-8 binding when built; aggregate deferred.
- **Outcome & Learning / Evidence Graph** — INV-12 binding when built; aggregate deferred.
- **Candidate Afterlife / Talent Pool / Portable Evidence** — BC-2 owns the terms; aggregates deferred.
- **Subscription/billing internals** — BC-7 thin; only the Candidate Evaluation *count* matters at MVP.

---

## The two-document split going forward *(CTO-approved)*

> **ARCH-04 — Business Event Model:** domain events (what *happened* in the business — e.g., `CampaignActivated`, `EvidenceRecorded`, `EvaluationCompleted`, `FairnessVerdictPassed`, `RecommendationDelivered`, `HiringDecisionRecorded`, `FeedbackReleased`, `ExportDelivered`, `ConsentWithdrawn`). Captures business semantics, independent of implementation.
> **ARCH-05 — Physical Architecture:** modules, services, deployment boundaries — *how* software components communicate.
>
> **Why the split matters:** the Business Event Model captures *what happens in the business*; the Physical Architecture captures *how software components communicate*. Separating them means that if, in five years, we move from a modular monolith to microservices (or back), the Business Event Model — and this Canonical Domain Model beneath it — remain valid. The domain stays stable while the technology evolves. This is a deliberate long-lived-system pattern.

*End of ARCH-03 v0.1 — the Canonical Domain Model. Zero technology. This document defines the business language and the home of every business rule; it must remain valid even if the entire technology stack changes. Next: ARCH-04 — Business Event Model.*
