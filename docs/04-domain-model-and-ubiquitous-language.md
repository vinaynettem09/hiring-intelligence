# Document 04 — Domain Model & Ubiquitous Language

| Field | Value |
|---|---|
| **Document ID** | DOC-04 |
| **Title** | Domain Model & Ubiquitous Language |
| **Status** | v0.3 — A-04.2 (five term decisions + Owner/Lifecycle governance); **A-04.3 aligns INV-1 & DC-7 with DOC-05's Human Accountability Framework**; terminology FREEZES on ratification (§11.2) |
| **Owner** | Principal Engineer / Technical Documentation Lead |
| **Created** | 2026-07-21 |
| **Depends on** | DOC-01 (Vision + Amendment A-0.2), DOC-02 (Problem), DOC-03 (Business Strategy, incl. ratified KD-03.10–14) |
| **Blocks** | DOC-05 (Product Principles) and every subsequent document, diagram, API, data model, UI, sales/legal artifact |
| **Canonical status** | **This is the single source of truth for company vocabulary.** Future documents must *reference* terms defined here, not redefine them. After ratification, new terms require a formal amendment to this document (§11.2). |
| **Scope discipline** | **Business-domain language only.** No implementation, no architecture, no APIs, no database schemas, no technology choices. "Relationships" and "state machines" here are *conceptual*, not data models or code. |

---

## How to read this document

This is a dictionary and a map, not an argument. Its job is to make one word mean exactly one thing across the entire company, so that a recruiter, an engineer, a lawyer, a salesperson, and an investor all mean the same thing when they say "evaluation" or "signal." Where two terms are commonly confused (e.g., *skill* vs. *competency* vs. *capability*; *role* vs. *job* vs. *position*; *recommendation* vs. *decision*), the document draws the line explicitly and names what must **never** be conflated.

Notation used throughout:
- **Term** — a canonical business term (also in the glossary, §4).
- *[Context: X]* — the bounded context (§2) that owns the term's definition.
- ⚠️ **Never confuse with** — a hard disambiguation.

---

## Amendment A-04.2 — Ratified Term Decisions + Governance (Owner & Lifecycle Status)

*Dated 2026-07-21. CTO-ratified. This amendment (a) settles five term decisions, (b) adds two governance attributes to every term — **Owner** and **Lifecycle Status** — maintained in the Term Registry (§C), and (c) confirms the Terminology Freeze (§11.2). Where this amendment and an earlier glossary entry differ, this amendment wins; affected glossary entries below have been updated to match.*

### A. Ratified term decisions

**D-04.A1 — The measurement triad is disambiguated by name.** Three distinct concepts, three unmistakable names, so no one ever again wonders "which score means how-good-is-the-candidate?":

| Term | Answers the question | Example |
|---|---|---|
| **Evaluation Score** | *How good is this candidate for this role?* (quality, derived from evidence) | Evaluation Score: **89** |
| **Confidence** | *How certain is the system about its own judgment?* | Confidence: **High (94%)** |
| **Integrity Score** | *How authentic/trustworthy is the evidence?* (fraud, impersonation, AI misuse, verification) | Integrity Score: **98** |

"Trust Score" is **renamed → Integrity Score**, and retained as **Deprecated** (superseded by Integrity Score) for backward-compatibility.

**D-04.A2 — Billing unit = Candidate Evaluation.** *One Candidate + one Role + one final Recommendation*, regardless of how many Evaluation Sessions were required to produce it. We **never** bill per session (a candidate interviewed twice must not be billed twice). Advantages: impossible to game, predictable pricing, easy procurement/invoicing, stable ARR. (Cross-ref DOC-03 KD-03.10; full glossary entry added below.)

**D-04.A3 — Company Calibration ⊂ Hiring Memory.** Hiring Memory is the *complete* learned intelligence; Calibration is *one component* of it. Components of Hiring Memory: Company Calibration · Hiring Manager Patterns · Outcome Learning · Historical Decisions · Successful-Employee Patterns · Failed-Hire Patterns · Organizational Preferences · Learned Hiring Behaviors. (Reflected in the Hiring Memory entry.)

**D-04.A4 — Employee is Reference-Only.** We are not building an HRIS. "Employee" exists in our vocabulary *solely* because Outcome Learning needs on-the-job performance signals; the Employee entity belongs to the customer's HRIS (Workday, SuccessFactors, Rippling…), which we reference, never own.

**D-04.A5 — "Score" is never used bare.** Every score-type term must be qualified. **Allowed:** Evaluation Score, Integrity Score, Benchmark Percentile, Confidence. **Forbidden everywhere (docs, APIs, UI, sales):** the bare word **"Score."** One-word names become impossible to disambiguate once customers integrate.

### B. Governance fields — Owner & Lifecycle Status *(per CTO)*

Every term now carries two governance attributes, maintained centrally in the Term Registry (§C):

- **Owner** — the Domain (§3) that governs the term's meaning. **Any proposed change to a term must be approved by its owning Domain.** This is what prevents "everyone argues" once the team grows past ~20–30 engineers: ownership tells you *who decides.*
- **Lifecycle Status** — one of:
  - **Stable** — ratified, in active use, safe to build on.
  - **Emerging** — accepted direction, still being shaped (e.g., long-term-vision terms).
  - **Experimental** — provisional; may change or be removed.
  - **Deprecated** — superseded; retained for backward-compatibility with a *superseded-by* pointer; not for new use.

> *Design note:* Owner + Status are maintained in **one** authoritative Registry rather than duplicated into all ~45 entries, so governance has a single source of truth and cannot drift entry-to-entry. This is a deliberate maintainability choice; the Registry is authoritative. (If per-entry inlining is ever preferred, the Registry still governs.)

### C. Term Registry

| Term | Owner (Domain) | Status | Note |
|---|---|---|---|
| Candidate | Candidate | Stable | |
| Application | Candidate | Stable | |
| Resume | Candidate | Stable | Weak Signal input only |
| Silver Medal Candidate | Candidate | Stable | |
| Talent Pool | Candidate / Hiring | Stable | |
| Candidate Afterlife | Candidate | Emerging | |
| Portable Evidence | Candidate | Emerging | Long-term vision |
| Company | Company | Stable | |
| Organization | Company | Stable | |
| Recruiter / Talent Acquisition | Company | Stable | Primary buyer/champion |
| Hiring Manager | Company | Stable | |
| Design Partner | Commercial | Stable | |
| Enterprise Customer | Commercial | Stable | |
| Job | Work | Stable | |
| Role | Work | Stable | |
| Position | Work | Stable | |
| Requisition | Work | Stable | Reference-only (owned by ATS) |
| Sensor | Evidence | Stable | Input, never product |
| Evidence | Evidence | Stable | |
| Evidence Item | Evidence | Stable | |
| Signal | Evidence | Stable | |
| Assessment | Evidence | Stable | A type of Sensor |
| Interview | Evidence | Stable | A type of Sensor |
| Verification | Evidence | Stable | |
| Skill | Skills | Stable | |
| Competency | Skills | Stable | |
| Capability | Skills | Stable | |
| Evaluation | Evaluation | Stable | |
| Evaluation Session | Evaluation | Stable | Not a billing unit |
| **Candidate Evaluation** | Evaluation (+ Commercial for billing) | Stable | **Billing unit (D-04.A2)** |
| **Evaluation Campaign** | Evaluation / Hiring | Stable | **Added A-04.4** — a run of Candidate Evaluations for one Role/req |
| Recommendation | Evaluation | Stable | Advisory, never a decision |
| **Evaluation Score** | Evaluation | Stable | **NEW — candidate quality (D-04.A1)** |
| Confidence | Evaluation | Stable | System's certainty |
| Decision Quality | Evaluation | Stable | *The product* |
| Hiring Intelligence Layer | Intelligence | Stable | |
| Hiring Intelligence Network | Intelligence / Benchmark | Stable | |
| Company Calibration | Intelligence (Calibration & Memory) | Stable | Component of Hiring Memory |
| Hiring Memory | Intelligence | Stable | Complete learned intelligence |
| Evidence Graph | Intelligence / Outcome & Learning | Stable | |
| Outcome Learning | Outcome & Learning | Stable | |
| Outcome | Outcome & Learning | Stable | |
| Employee | External (Reference-Only) | Stable (Reference) | Belongs to customer HRIS (D-04.A4) |
| Benchmark | Benchmark | Stable | |
| Hiring Cycle | Hiring | Stable | |
| Hiring Event | Hiring | Stable | |
| Hiring Decision | Hiring | Stable | Human-owned |
| Offer | Hiring | Stable | Reference-only (owned by customer) |
| Rejection | Hiring | Stable | Transition to Afterlife |
| Explainability | Trust, Fairness & Compliance | Stable | Gate |
| Fairness | Trust, Fairness & Compliance | Stable | Gate |
| Bias | Trust, Fairness & Compliance | Stable | The defect |
| Adverse Impact | Trust, Fairness & Compliance | Stable | Measured effect |
| **Integrity Score** | Trust, Fairness & Compliance | Stable | **RENAMED from Trust Score (D-04.A1)** |
| ~~Trust Score~~ | Trust, Fairness & Compliance | **Deprecated** | **Superseded by → Integrity Score** |
| Human Accountability (Framework) | Trust, Fairness & Compliance | Stable | Invariant INV-1; reframed A-04.3 |
| ~~Human-in-the-Loop~~ | Trust, Fairness & Compliance | **Deprecated** | **Superseded by → Human Accountability** |
| ~~Score~~ (bare) | — | **Forbidden** | Must always be qualified (D-04.A5) |

---

## 1. Why Ubiquitous Language Matters

**Ubiquitous Language** (a term from Domain-Driven Design) is a single, shared, rigorously-defined vocabulary used *identically* by domain experts and builders — in conversation, documents, diagrams, code, UI, contracts, and sales. It is "ubiquitous" because it appears everywhere and admits no dialects.

Why this is worth an entire document *before* principles or architecture:

1. **Ambiguity compounds into defects.** If "evaluation" means "the interview" to one engineer and "the final scored assessment" to another, every downstream artifact inherits the confusion — the data model, the API, the UI, the sales deck, and eventually the customer's mental model. Language drift is the cheapest bug to prevent and the most expensive to fix later.

2. **Our product *is* the language.** We are selling *hiring-decision quality* built on *evidence*, *calibration*, *memory*, and *outcome learning* (DOC-03). If those words are fuzzy, the product is fuzzy. Precision in the vocabulary is precision in the value proposition.

3. **Explainability requires exact terms.** Our fairness/explainability gate (DOC-01 §9) demands that every recommendation be defensible to a candidate, a hiring manager, and a regulator. You cannot explain a decision in words whose meaning is contested. **Explainability is impossible without a fixed vocabulary.**

4. **It prevents strategic drift.** DOC-01–03 made hard distinctions the company's identity depends on: *sensor* ≠ *product*; *recommendation* ≠ *decision*; *intelligence layer* ≠ *system of record*. If the language blurs these, the strategy blurs with it. The vocabulary is a guardrail on the mission.

5. **It scales the organization.** As the company grows to thousands of employees (DOC-01), a shared language is how a new engineer, a new AE, and a new counsel align without re-litigating meaning. The glossary is onboarding infrastructure.

> **Principle:** *One term, one meaning, everywhere.* When reality forces a new concept, we **name it here first**, then use it — never the reverse.

---

## 2. Bounded Context Overview

A **Bounded Context** is a boundary within which a term has one precise meaning. The same English word can legitimately mean different things in different contexts (e.g., "position" means a *job opening* in the Work context but could mean *ranking* in the Benchmarking context) — bounded contexts make those boundaries explicit so we never accidentally equate them.

*(These are conceptual/business boundaries for language ownership. They are NOT services, modules, or architecture — that is DOC-12.)*

| Bounded Context | Owns the meaning of… | One-line responsibility |
|---|---|---|
| **Candidate Context** | Candidate, Application, Resume, Portable Evidence, Silver Medal Candidate, Candidate Afterlife | Who the person is and how they enter/remain in the network. |
| **Company Context** | Company, Organization, Enterprise Customer, Design Partner, Hiring Team, Recruiter, Hiring Manager | Who the customer is and their internal hiring actors. |
| **Work Context** | Job, Role, Position, Requisition | What is being hired for. |
| **Evidence Context** | Sensor, Evidence, Evidence Item, Signal, Assessment, Interview, Verification | How raw truth about a candidate's ability is captured and structured. |
| **Skills Context** | Skill, Competency, Capability | The vocabulary of ability itself. |
| **Evaluation & Intelligence Context** | Evaluation, Evaluation Session, Recommendation, Confidence, Decision Quality, Hiring Intelligence Layer | Turning evidence into explainable, comparable judgment. |
| **Hiring Context** | Hiring Cycle, Hiring Event, Hiring Decision, Offer, Rejection, Talent Pool | The funnel and the human decision. |
| **Calibration & Memory Context** | Company Calibration, Hiring Memory | Learning how a specific company/manager defines "good." |
| **Outcome & Learning Context** | Outcome, Outcome Learning, Evidence Graph | Closing the loop from decision to on-the-job result. |
| **Benchmarking Context** | Benchmark, Hiring Intelligence Network | Placing a candidate against the network. |
| **Trust, Fairness & Compliance Context** | Explainability, Progressive Explainability, Fairness, Bias, Adverse Impact, Integrity Score, Human Accountability | Ensuring decisions are fair, explainable, and defensible. |
| **Commercial Context** | Enterprise Customer, Design Partner, Subscription, Candidate Evaluation (as billing unit) | The business relationship (pricing/packaging detail deferred). |

**Why bounded contexts here (and not just a flat glossary):** they let us *legitimately* reuse a word in two places without contradiction, and they assign each term an owner so that if the meaning ever needs to change, we know which context governs it. When a term appears in the glossary, its owning context is noted.

---

## 3. Business Domains

Using DDD strategic classification, we sort the domains the CTO listed into **Core** (our differentiation and moat — invest most here), **Supporting** (necessary, specific to us, but not the moat), and **Generic/Shared** (necessary, but not where we differentiate). This classification guides where the company concentrates its best effort.

### 3.1 Core Domains (the moat — DOC-03 §13)

| Domain | What it covers | Why it is core |
|---|---|---|
| **Evaluation** | Turning evidence into structured, explainable judgment of ability. | The heart of "decision quality is the product." |
| **Intelligence** | The connective layer: calibration + memory + benchmarking + reasoning across everything. | This *is* the company (Hiring Intelligence Layer). |
| **Evidence** | Capturing, structuring, and verifying truth about candidates (via sensors). | Raw material of all judgment; the Evidence Graph. |
| **Outcome Learning** | Connecting decisions to real results and improving from them. | The Learning flywheel; unique, hard-to-copy (DOC-03 §17). |
| **Benchmarking** | Network-wide comparison of candidates. | Only possible at network scale; a network-effect moat. |

### 3.2 Supporting Domains (specific to us, but not the differentiation)

| Domain | What it covers |
|---|---|
| **Candidate** | The person, their application, their journey and afterlife. |
| **Company / Organization** | The customer, its hiring teams and actors. |
| **Roles (Work)** | Jobs, roles, positions, requisitions being hired for. |
| **Hiring** | The funnel, hiring cycle, events, and the human decision. |
| **Skills** | The vocabulary of ability (skill/competency/capability). |

### 3.3 Cross-cutting / Governing Domain

| Domain | What it covers | Note |
|---|---|---|
| **Compliance, Trust & Fairness** | Explainability, fairness, bias mitigation, auditability, human-in-the-loop, consent, data protection. | Cross-cuts *everything*. Per DOC-01 §9 it is a **non-negotiable gate**, not a feature — it constrains all other domains. Deep treatment deferred to DOC-11-era compliance/governance work. |

### 3.4 Generic Domain

| Domain | Note |
|---|---|
| **Commercial** | Customers, contracts, subscription, billing units. Necessary but not differentiating; pricing model ratified (KD-03.10) with detail deferred. |

> **Strategic read:** the company should concentrate its scarcest talent on the **Core** domains (Evaluation, Intelligence, Evidence, Outcome Learning, Benchmarking) — the moat — while being merely *excellent-enough* on Supporting domains and pragmatic on Generic ones. This mirrors DOC-03's "invest disproportionately in the compounding moat."

---

## 4. Glossary

*Every term includes: **Definition · Why it exists · Examples · Common misunderstandings · Related terms · Never confuse with.** Owning bounded context noted in brackets.*

### 4.A — People & Organizations

---

#### Candidate  *[Candidate Context]*
- **Definition:** A person who is being, has been, or may be evaluated for a Role through the network. Candidacy begins at first evaluation-relevant interaction and *persists* beyond any single hiring outcome (see Candidate Afterlife).
- **Why it exists:** The candidate is a first-class user of the network (DOC-01 A-0.2, DOC-03 KD-03.14), not a transient applicant record. We need a term that outlives a single application.
- **Examples:** A software engineer evaluated for a backend role; a rejected applicant later re-surfaced for a different role; a prospect who completed an evaluation but never formally "applied."
- **Common misunderstandings:** That "candidate" = "applicant to one job." A candidate is a durable network participant, not a per-req record.
- **Related terms:** Application, Silver Medal Candidate, Talent Pool, Portable Evidence.
- ⚠️ **Never confuse with:** **Application** (an *event/act* of applying, not a person) or **Employee** (post-hire; a different lifecycle stage).

#### Company  *[Company Context]*
- **Definition:** A business entity that uses the platform to make hiring decisions; the customer of hiring intelligence.
- **Why it exists:** Distinguishes the *customer entity* from its internal structure (Organization) and its people (Recruiters, Hiring Managers).
- **Examples:** A 900-person mid-market SaaS company; a design-partner startup.
- **Common misunderstandings:** Treating "Company" and "Organization" as synonyms (see Organization).
- **Related terms:** Organization, Enterprise Customer, Design Partner, Company Calibration, Hiring Memory.
- ⚠️ **Never confuse with:** **Candidate** (the other side of the network) or **Organization** (internal structure of a Company).

#### Organization  *[Company Context]*
- **Definition:** The internal structure of a Company — its teams, departments, and hierarchy — within which hiring happens and against which Company Calibration and Hiring Memory are scoped.
- **Why it exists:** Calibration and memory are often *team-* or *manager-*specific, not company-wide; we need to model internal structure conceptually.
- **Examples:** The "Platform Engineering" org; a specific Hiring Manager's team.
- **Common misunderstandings:** That there is one calibration per Company. Calibration can be scoped to Organization units.
- **Related terms:** Company, Hiring Team, Hiring Manager, Company Calibration.
- ⚠️ **Never confuse with:** **Company** (the legal/customer entity as a whole).

#### Recruiter / Talent Acquisition  *[Company Context]*
- **Definition:** A person at a Company responsible for running hiring processes and moving candidates through the funnel. The **primary buyer/champion** (KD-03.11).
- **Why it exists:** A named actor with distinct jobs-to-be-done (DOC-02) and the primary user of the layer's outputs.
- **Examples:** In-house recruiter, sourcer, TA lead.
- **Common misunderstandings:** That the recruiter is "the customer we serve" in the mission sense. *Recruiters are one customer; decision quality is the product* (DOC-03 KD-03.7).
- **Related terms:** Hiring Manager, Hiring Team, Recommendation.
- ⚠️ **Never confuse with:** **Hiring Manager** (owns the role and the hire; different incentives).

#### Hiring Manager  *[Company Context]*
- **Definition:** The person who owns a Role, will manage the hire, and holds the true "bar" for the Role. Champion for engineering hiring is often a VP Eng/Eng Director (KD-03.11).
- **Why it exists:** The hiring manager's implicit standard is what Company Calibration and Hiring Memory try to capture.
- **Examples:** An engineering director hiring a senior backend engineer.
- **Common misunderstandings:** That the hiring manager and recruiter want the same thing measured the same way — they frequently don't (DOC-02).
- **Related terms:** Company Calibration, Hiring Memory, Role.
- ⚠️ **Never confuse with:** **Recruiter** (runs the process; does not own the role).

#### Design Partner  *[Commercial Context]*
- **Definition:** An early customer who works closely with us in exchange for early access, influence, and preferential pricing — and who, critically, **shares outcome data** (DOC-03 §21).
- **Why it exists:** Design partners validate the core thesis (evidence beats resumes, DOC-02 AS-1) and seed the Data/Trust flywheels.
- **Examples:** 5–8 mid-market tech companies on Greenhouse/Ashby hiring engineers at volume.
- **Common misunderstandings:** That a design partner is just an early paying customer. The defining trait is *deep collaboration + outcome-data sharing*, not the discount.
- **Related terms:** Enterprise Customer, Outcome, Outcome Learning.
- ⚠️ **Never confuse with:** **Enterprise Customer** (a scaled commercial relationship, not a co-development one).

#### Enterprise Customer  *[Commercial Context]*
- **Definition:** A large Company on a scaled commercial agreement (enterprise tier per KD-03.10), typically with security review, procurement, and multi-org deployment.
- **Why it exists:** A distinct commercial and go-to-market motion (DOC-03 §22) with distinct approvers (CHRO economic, CIO/Security technical — KD-03.11).
- **Examples:** A 10,000-employee company deploying across multiple hiring orgs.
- **Common misunderstandings:** That "enterprise" is just "big." It denotes the *commercial motion and requirements*, not merely headcount.
- **Related terms:** Design Partner, Subscription, Company.
- ⚠️ **Never confuse with:** **Design Partner** (co-development, early stage).

### 4.B — Work Definitions

---

#### Job  *[Work Context]*
- **Definition:** The general, market-level concept of a kind of work (e.g., "Backend Software Engineer") — role-family-level, not company-specific and not a specific opening.
- **Why it exists:** We need a stable, cross-company concept to attach Skills, Competencies, Benchmarks, and network intelligence to.
- **Examples:** "Data Engineer," "Product Manager" as general categories.
- **Common misunderstandings:** Equating "job" with a single opening at one company (that's a Position/Requisition).
- **Related terms:** Role, Position, Skill, Benchmark.
- ⚠️ **Never confuse with:** **Position** (a specific opening) or **Role** (a company-specific shaping of a Job).

#### Role  *[Work Context]*
- **Definition:** A *specific Company's* interpretation of a Job — the same Job shaped by that Company's context, calibration, level, and expectations.
- **Why it exists:** Company A's "Senior Backend Engineer" ≠ Company B's; Company Calibration operates at the Role level.
- **Examples:** "Senior Backend Engineer, Payments team, Company X" with X's specific bar.
- **Common misunderstandings:** Using "role" and "job" interchangeably. Role is company-contextualized; Job is generic.
- **Related terms:** Job, Position, Company Calibration, Hiring Manager.
- ⚠️ **Never confuse with:** **Job** (generic/market-level) or **Position** (a countable opening for a Role).

#### Position  *[Work Context]*
- **Definition:** A specific, countable opening for a Role that a Company intends to fill (headcount = number of positions).
- **Why it exists:** Hiring is planned and tracked per opening; a Role may have many open Positions.
- **Examples:** "3 open positions for the Senior Backend Engineer role."
- **Common misunderstandings:** Confusing a Position (the opening) with the Requisition (its formal record/authorization).
- **Related terms:** Role, Requisition, Hiring Cycle.
- ⚠️ **Never confuse with:** **Requisition** (the formal authorization/record of a Position) or **Role** (the kind of work).

#### Requisition  *[Work Context]*
- **Definition:** The formal, authorized record in the customer's system of record (usually the ATS) that opens a Position for hiring.
- **Why it exists:** It is the integration anchor between the customer's ATS and our layer, and the trigger that begins a Hiring Cycle.
- **Examples:** "REQ-1043 opened in Greenhouse for the Senior Backend Engineer role."
- **Common misunderstandings:** That we *own* requisitions. We do not — the ATS owns them (we are never a system of record, DOC-03 §10). We *reference* them.
- **Related terms:** Position, Hiring Cycle, ATS (system of record).
- ⚠️ **Never confuse with:** **Position** (the opening itself) or **Hiring Cycle** (the end-to-end process the requisition starts).

### 4.C — Candidate Interaction & Funnel Artifacts

---

#### Application  *[Candidate Context]*
- **Definition:** The act/event of a Candidate expressing interest in a specific Position, in whatever way they already do it (portal, email, referral) — DOC-01's "candidate never changes how they apply."
- **Why it exists:** A named event that begins a candidate's participation in a specific Hiring Cycle, distinct from the person (Candidate).
- **Examples:** Submitting a resume via the ATS; a referral; an email application.
- **Common misunderstandings:** That the application *is* the candidate or the evidence. It is an *entry event*, not a person and not an evaluation.
- **Related terms:** Candidate, Resume, Hiring Cycle, Hiring Event.
- ⚠️ **Never confuse with:** **Candidate** (the person) or **Evidence** (what we actually evaluate).

#### Resume  *[Candidate Context]*
- **Definition:** A candidate-authored, unverified self-description of background and experience. In our worldview it is **one low-signal input**, never the basis of a decision (DOC-02).
- **Why it exists:** It still arrives (the world runs on it); we ingest it as a weak Signal and a Sensor input — while explicitly refusing to let it gate decisions.
- **Examples:** A PDF CV, a LinkedIn profile export.
- **Common misunderstandings:** That the resume is a form of Evidence of *ability*. It is Evidence of *self-presentation*, a weak Signal — not verified ability (this distinction is the company's founding thesis).
- **Related terms:** Signal, Evidence, Sensor, Verification.
- ⚠️ **Never confuse with:** **Evidence** (verified/observed truth about ability). A resume is a *claim*, not evidence of ability.

#### Offer  *[Hiring Context]*
- **Definition:** A Company's formal proposal to hire a Candidate for a Position, following a Hiring Decision.
- **Why it exists:** A distinct milestone after the decision; owned in the customer's system, referenced by us.
- **Examples:** A written offer with compensation for the accepted candidate.
- **Common misunderstandings:** That making the offer is the same as the Hiring Decision (the decision precedes and authorizes the offer).
- **Related terms:** Hiring Decision, Rejection, Hiring Cycle.
- ⚠️ **Never confuse with:** **Hiring Decision** (the judgment) — the offer is its *consequence*.

#### Rejection  *[Hiring Context]*
- **Definition:** The outcome in which a Candidate is not advanced/hired for a specific Position. In our model, rejection **does not end candidacy** — it transitions the candidate into the afterlife (Silver Medal / Talent Pool).
- **Why it exists:** To reframe rejection from a dead-end into a network-preserving transition (DOC-03 §18.4).
- **Examples:** A strong candidate not selected because another was stronger for *this* role.
- **Common misunderstandings:** That rejection = removal from the network. It is a state transition, not an exit.
- **Related terms:** Silver Medal Candidate, Talent Pool, Candidate Afterlife, Explainability.
- ⚠️ **Never confuse with:** **Silver Medal Candidate** (a *reason* for a specific rejection, not rejection itself).

#### Silver Medal Candidate  *[Candidate Context]*
- **Definition:** A Candidate who was strong and rejected *only because someone else was selected for that specific Position* — i.e., a high-quality near-miss worth re-engaging for future Roles.
- **Why it exists:** Encodes real network value: these are the highest-priority candidates for the afterlife and future Hiring Cycles.
- **Examples:** The #2 finalist for a role who would be an immediate top candidate for the next similar opening.
- **Common misunderstandings:** That any rejected candidate is a silver medalist. Only strong, "lost-to-competition" candidates qualify.
- **Related terms:** Rejection, Talent Pool, Candidate Afterlife, Benchmark.
- ⚠️ **Never confuse with:** a generic **Rejection** (most rejections are not silver-medal quality).

#### Talent Pool  *[Candidate/Hiring Context]*
- **Definition:** A curated, re-engageable set of Candidates (often including Silver Medal Candidates) with retained Evidence, available for future Roles.
- **Why it exists:** Operationalizes the candidate afterlife and reduces future sourcing cost/time (DOC-02).
- **Examples:** "Backend engineers evaluated in the last 12 months, top quartile, open to re-engagement."
- **Common misunderstandings:** That a talent pool is a mailing list. It is an *evidence-backed, benchmarked* set, not raw contacts.
- **Related terms:** Silver Medal Candidate, Candidate Afterlife, Portable Evidence, Benchmark.
- ⚠️ **Never confuse with:** a job-board **candidate database** (attention/volume-oriented; we are evidence-oriented).

#### Portable Evidence  *[Candidate Context]*
- **Definition:** Verified Evidence about a Candidate's ability that the candidate can carry and (with consent) reuse across Roles/Companies over time.
- **Why it exists:** Long-term network vision (DOC-03 §18/§25): candidate-owned, reusable evidence — "the credit score, but fair and explainable."
- **Examples:** A candidate's verified capability evidence reused for a new opportunity a year later (with consent).
- **Common misunderstandings:** That portability means selling candidate data. It is candidate-controlled and consent-based (KD-03.14 forbids selling candidate data).
- **Related terms:** Evidence, Candidate Afterlife, Consent, Trust.
- ⚠️ **Never confuse with:** a **Resume** (unverified self-claim) — portable evidence is *verified*.

### 4.D — Evidence & Measurement

---

#### Sensor  *[Evidence Context]*
- **Definition:** Any instrument that *collects* Evidence about a Candidate — an interview, a coding/work task, a behavioral evaluation, resume/portfolio ingestion, etc. **A sensor is an input, never the product** (DOC-03 §3, KD-03.2).
- **Why it exists:** To hold the line that interviews/tests are interchangeable *inputs* to the intelligence layer, not the company's value.
- **Examples:** An adaptive technical interview; an asynchronous work sample; a structured behavioral evaluation.
- **Common misunderstandings:** That "the AI interview" is our product. It is a sensor (this is a founding strategic distinction).
- **Related terms:** Evidence, Signal, Assessment, Interview, Evaluation.
- ⚠️ **Never confuse with:** **Evaluation** (what the intelligence layer *does* with sensor output) or **Product** (our product is decision quality, not any sensor).

#### Evidence  *[Evidence Context]*
- **Definition:** Observed or verified information about a Candidate's actual ability, produced by Sensors and structured for reasoning. Evidence is the raw material of judgment.
- **Why it exists:** The company's entire thesis is *evidence-based* (not resume-based) hiring; evidence is the atomic unit of that thesis.
- **Examples:** How a candidate reasoned through a system-design problem; the quality of a submitted work sample; a verified skill demonstration.
- **Common misunderstandings:** Equating Evidence with the Resume or with a raw Signal. Evidence is *observed ability*; a resume is a *claim*; a signal is an *interpreted indicator*.
- **Related terms:** Signal, Sensor, Evidence Item, Evidence Graph, Verification.
- ⚠️ **Never confuse with:** **Signal** (an interpreted indicator derived *from* evidence) or **Resume** (unverified claim).

#### Evidence Item  *[Evidence Context]*
- **Definition:** A single, discrete unit of Evidence (one observation), the smallest citable element of an explanation.
- **Why it exists:** Explainability requires that recommendations cite *specific* evidence items; it is the granular unit of the Evidence Graph.
- **Examples:** "Candidate correctly identified the race condition and proposed a lock-free fix" as one cited item.
- **Common misunderstandings:** That an evidence item is a whole interview. It is *one observation* within it.
- **Related terms:** Evidence, Evidence Graph, Explainability, Signal.
- ⚠️ **Never confuse with:** **Evidence** in aggregate (the collection) — an item is one element.

#### Signal  *[Evidence Context]*
- **Definition:** An interpreted indicator of ability or fit *derived from* Evidence — a step of meaning between raw evidence and a scored Evaluation. Signals have strength/quality (high-signal vs. low-signal).
- **Why it exists:** DOC-02's core framing is "signal vs. noise"; we need a term for the *interpreted* layer distinct from raw evidence.
- **Examples:** "Strong systems-design signal"; "weak signal from resume keywords."
- **Common misunderstandings:** Using "signal" and "evidence" interchangeably. Evidence is observed; a signal is *what the evidence indicates*.
- **Related terms:** Evidence, Evaluation, Confidence, Competency.
- ⚠️ **Never confuse with:** **Evidence** (the observation) or **Score** (a quantified evaluation output).

#### Assessment  *[Evidence Context]*
- **Definition:** A structured Sensor designed to elicit Evidence about specific Skills/Competencies (e.g., a coding assessment, a work sample). A *type* of sensor.
- **Why it exists:** Distinguishes purpose-built evidence-elicitation instruments from other sensors.
- **Examples:** A take-home work sample; a structured coding exercise.
- **Common misunderstandings:** That an assessment *is* the evaluation. An assessment *produces evidence*; the Evaluation interprets it.
- **Related terms:** Sensor, Interview, Evidence, Evaluation.
- ⚠️ **Never confuse with:** **Evaluation** (interpretation/judgment) — an assessment is a *sensor*.

#### Interview  *[Evidence Context]*
- **Definition:** A conversational Sensor (human- or AI-conducted) that elicits Evidence through adaptive questioning. A *type* of sensor.
- **Why it exists:** Interviews are a primary evidence source; naming them as sensors keeps them subordinate to the intelligence layer.
- **Examples:** An adaptive technical interview; a structured behavioral interview.
- **Common misunderstandings:** That "AI interview" is the product (it is a sensor — KD-03.2); that interviews *are* the evaluation.
- **Related terms:** Sensor, Assessment, Evidence, Evaluation Session.
- ⚠️ **Never confuse with:** **Evaluation** (judgment) or **Product** (decision quality).

#### Verification  *[Evidence Context]*
- **Definition:** The act of confirming that a piece of Evidence or a claim is genuine/authentic (e.g., that work was actually done by the candidate; that a credential is real).
- **Why it exists:** Trust and the fight against resume fraud (DOC-02) require distinguishing verified from unverified information.
- **Examples:** Confirming a work sample was produced by the candidate; validating a claimed credential.
- **Common misunderstandings:** That verification = evaluation. Verification confirms *authenticity*; evaluation judges *quality/ability*.
- **Related terms:** Evidence, Trust Score, Resume, Portable Evidence.
- ⚠️ **Never confuse with:** **Evaluation** (judging ability) — verification only judges *authenticity*.

### 4.E — Skills Vocabulary *(the most commonly-confused trio — read together)*

---

#### Skill  *[Skills Context]*
- **Definition:** A specific, teachable, demonstrable ability, usually narrow and often technical/tool-specific.
- **Why it exists:** The most granular unit of ability; the building block of Competencies.
- **Examples:** "Writing SQL," "using React," "unit testing in Python."
- **Common misunderstandings:** Treating skills as the whole picture of ability (they are the narrowest layer).
- **Related terms:** Competency, Capability, Evidence, Benchmark.
- ⚠️ **Never confuse with:** **Competency** (a broader cluster of applied skills + behaviors) or **Capability** (highest-level potential).

#### Competency  *[Skills Context]*
- **Definition:** A broader, applied cluster of Skills, knowledge, and behaviors that produces effective performance in a domain (skill *applied in context*).
- **Why it exists:** Real job performance depends on applied competencies, not isolated skills; evaluation targets competencies.
- **Examples:** "System design," "debugging complex production issues," "technical communication."
- **Common misunderstandings:** Using "skill" and "competency" interchangeably. A competency *integrates* multiple skills with judgment and behavior.
- **Related terms:** Skill, Capability, Evaluation, Role.
- ⚠️ **Never confuse with:** **Skill** (narrow, specific) or **Capability** (potential/trajectory).

#### Capability  *[Skills Context]*
- **Definition:** The highest-level, more durable capacity — including potential, adaptability, and learning ability — to perform and grow in a Role over time (competency *plus trajectory/potential*).
- **Why it exists:** Great hiring predicts future performance and growth, not just current skills; capability captures potential.
- **Examples:** "Can grow into a staff-level engineer," "learns unfamiliar domains quickly."
- **Common misunderstandings:** Reducing capability to current skills; capability includes *potential and adaptability*.
- **Related terms:** Competency, Skill, Outcome Learning, Decision Quality.
- ⚠️ **Never confuse with:** **Competency** (current applied ability) or **Skill** (specific ability). *Hierarchy: Skill ⊂ Competency ⊂ Capability.*

### 4.F — Evaluation & Intelligence

---

#### Evaluation  *[Evaluation & Intelligence Context]*
- **Definition:** The structured, explainable **judgment of a Candidate's ability for a Role**, produced by the intelligence layer by interpreting Evidence (from Sensors) in light of Company Calibration and Hiring Memory. The evaluation is *analysis and judgment*, not a decision.
- **Why it exists:** The central act of the product; the thing "decision quality" is built on.
- **Examples:** A structured, evidence-cited assessment of a candidate's competencies for a specific role, with confidence and benchmarks.
- **Common misunderstandings:** (1) That the interview *is* the evaluation (the interview is a sensor). (2) That an evaluation *is* a decision (it *informs* a human decision). (3) That evaluation = a single score (it is evidence-cited judgment).
- **Related terms:** Evidence, Recommendation, Hiring Decision, Evaluation Session, Confidence.
- ⚠️ **Never confuse with:** **Interview/Assessment** (sensors), **Recommendation** (the layer's suggested action), or **Hiring Decision** (the human's choice).

#### Evaluation Session  *[Evaluation & Intelligence Context]*
- **Definition:** A single, time-bounded instance in which Evidence is collected and/or an Evaluation is conducted for a Candidate (e.g., one interview sitting, one assessment session).
- **Why it exists:** Operational unit of evidence collection; the natural boundary for candidate experience and (per KD-03.10) the countable act underlying the billing unit "candidate evaluation."
- **Examples:** A 45-minute adaptive technical interview session.
- **Common misunderstandings:** Conflating a session (one sitting) with the overall Evaluation (the judgment across all evidence).
- **Related terms:** Evaluation, Interview, Assessment, Candidate Evaluation (billing).
- ⚠️ **Never confuse with:** **Evaluation** (the judgment), **Candidate Evaluation** (the billing unit — many sessions can roll up into one), or a billing unit — a session is one *evidence-collection instance*, **never billed on its own** (D-04.A2).

#### Candidate Evaluation  *[Evaluation & Intelligence Context / Commercial Context]*  · **Owner: Evaluation Domain (+ Commercial for billing) · Status: Stable** *(the billing unit, D-04.A2)*
- **Definition:** A **complete evaluation of one Candidate for one Role, resulting in one final Recommendation — regardless of how many Evaluation Sessions were required to produce it.** This is the platform's **billing unit** (DOC-03 KD-03.10): *one Candidate + one Role + one final Recommendation; everything inside is included.*
- **Why it exists:** To give pricing a unit that is impossible to game, predictable for procurement, easy to invoice, and produces stable ARR — and that never penalizes a customer for running more sessions on the same candidate.
- **Examples:** A backend candidate who does a technical interview + a behavioral interview + a system-design session + a reference check, producing **one** Recommendation = **one** Candidate Evaluation (one billable unit).
- **Common misunderstandings:** That each Evaluation Session or each Sensor is billed (it is not — D-04.A2); that re-evaluating the *same candidate for a different Role* is free (that is a new Candidate Evaluation).
- **Related terms:** Evaluation, Evaluation Session, Recommendation, Role, Candidate, Subscription.
- ⚠️ **Never confuse with:** **Evaluation Session** (one sitting; not billed alone) or **Evaluation** (the judgment; a Candidate Evaluation is the *commercial/complete* wrapper around it for one candidate-role pair).

#### Evaluation Campaign  *[Evaluation & Intelligence / Hiring Context]*  · **Owner: Evaluation / Hiring · Status: Stable** *(added A-04.4)*
- **Definition:** A bounded, organized **run of Candidate Evaluations initiated for a specific Role/requisition** — the operational container that groups the *imported* candidates (see Product Boundary, DOC-12 KD-12.7), their invitations, evaluations, and results for one hiring effort.
- **Why it exists:** Recruiters evaluate candidates in batches per role; the campaign is the unit they start, monitor, and close. It is where our product boundary *begins* (after candidates are imported).
- **Examples:** "Start an Evaluation Campaign for the Senior Backend Engineer req, importing the 120 applicants from Greenhouse."
- **Common misunderstandings:** It is **not** a marketing "campaign," and it is **not** the customer's Hiring Cycle (which spans req→offer in *their* systems).
- **Related terms:** Candidate Evaluation, Role, Requisition, Candidate Intake (C2), Hiring Cycle.
- ⚠️ **Never confuse with:** **Candidate Evaluation** (one candidate-role-recommendation; a campaign *contains many*) or **Hiring Cycle** (the customer's end-to-end process; a campaign is our evaluation run *within* it).

#### Recommendation  *[Evaluation & Intelligence Context]*
- **Definition:** The intelligence layer's explainable *suggested course of action* regarding a Candidate (e.g., "advance," "strong hire for this role," "not a fit for this role but strong for X"), always accompanied by its Evidence and reasoning. **A recommendation is advisory to a human; it is never an autonomous decision.**
- **Why it exists:** Encodes the human-in-the-loop principle (DOC-01): we recommend; humans decide.
- **Examples:** "Advance to onsite — top-decile system-design evidence; see cited items."
- **Common misunderstandings:** That a recommendation is the decision, or that the system decides. **The system never makes the Hiring Decision** (invariant, §8).
- **Related terms:** Hiring Decision, Evaluation, Explainability, Confidence.
- ⚠️ **Never confuse with:** **Hiring Decision** (the human's binding choice). This distinction is legally and ethically load-bearing.

#### Hiring Decision  *[Hiring Context]*
- **Definition:** The **human** choice by the Company to advance, hire, or reject a Candidate for a Position, informed by (but not dictated by) the layer's Recommendation and Evidence.
- **Why it exists:** The accountable, human-owned act; the thing whose *quality* is our product.
- **Examples:** A hiring manager deciding to extend an offer after reviewing the recommendation and evidence.
- **Common misunderstandings:** That the platform makes it. It never does (human-in-the-loop invariant). We improve the *quality* of this human act.
- **Related terms:** Recommendation, Offer, Rejection, Decision Quality, Outcome.
- ⚠️ **Never confuse with:** **Recommendation** (advisory) — the decision is the human's and is binding.

#### Confidence  *[Evaluation & Intelligence Context]*
- **Definition:** The degree of certainty the intelligence layer has in a given Signal, Evaluation, or Recommendation, given the quantity/quality of Evidence. A property *of the system's own outputs.*
- **Why it exists:** Honest, explainable judgment must express uncertainty; low-confidence outputs should be treated differently by humans.
- **Examples:** "High confidence in coding competency (strong direct evidence); low confidence in leadership (little evidence gathered)."
- **Common misunderstandings:** Confusing Confidence (system's certainty in *its own* output) with Trust Score (see below) or with a candidate's quality score.
- **Related terms:** Signal, Evaluation, Evaluation Score, Integrity Score, Explainability.
- ⚠️ **Never confuse with:** **Integrity Score** (authenticity of the evidence, not the system's certainty) or **Evaluation Score** (candidate quality, not certainty).

#### Evaluation Score  *[Evaluation & Intelligence Context]*  · **Owner: Evaluation Domain · Status: Stable** *(NEW, D-04.A1)*
- **Definition:** A quantified expression of a **Candidate's quality for a specific Role**, derived from Evidence via the Evaluation. Always accompanied by Explainability (the evidence behind it), Confidence (certainty), and — where relevant — Benchmark and Integrity Score. It is *one* facet of an Evaluation, never a standalone bare "score."
- **Why it exists:** Buyers and users need a comparable quality figure; naming it explicitly (and forbidding bare "Score", D-04.A5) prevents the meaningless one-word "score" from colliding with Confidence and Integrity Score.
- **Examples:** Evaluation Score: 89 for a backend candidate against Role X, with cited evidence and High Confidence.
- **Common misunderstandings:** Treating the Evaluation Score as *the* Evaluation (it is one output of the evidence-cited Evaluation) or as a decision (it informs a human Hiring Decision).
- **Related terms:** Evaluation, Confidence, Integrity Score, Benchmark, Explainability, Decision Quality.
- ⚠️ **Never confuse with:** **Confidence** (certainty about the judgment), **Integrity Score** (authenticity of evidence), or a bare **"Score"** (forbidden, D-04.A5).

#### Decision Quality  *[Evaluation & Intelligence Context]*
- **Definition:** How good a Hiring Decision is — measured by whether it was evidence-backed, fair, explainable/defensible, and (ultimately) predictive of a good Outcome. **This is the product** (DOC-03 KD-03.2/3).
- **Why it exists:** It is the company's definition of the value it sells; the North Star (evidence-backed decisions) and ultimate metric (quality-of-hire) both express it.
- **Examples:** A decision made on cited evidence, passing fairness checks, that led to a successful hire.
- **Common misunderstandings:** Equating decision quality with speed or cost (those are efficiency, not quality) or with a single good outcome (quality is about the *process and evidence*, validated over many outcomes).
- **Related terms:** Hiring Decision, Outcome, Outcome Learning, Explainability, Fairness.
- ⚠️ **Never confuse with:** **Time-to-hire / cost-per-hire** (efficiency metrics, explicitly *not* our product — DOC-02).

### 4.G — Core Platform Concepts *(the moat vocabulary)*

---

#### Hiring Intelligence Layer  *[Evaluation & Intelligence Context]*
- **Definition:** The neutral, explainable intelligence that sits between the world's inputs and the Company's systems of record, turning Evidence into Evaluations, Recommendations, and Benchmarks — via Company Calibration, Hiring Memory, and Outcome Learning. The layer *for one company at one time.*
- **Why it exists:** The core product concept (DOC-01, DOC-03 §5).
- **Examples:** The intelligence embedded in a customer's Greenhouse workflow that produces evidence-backed recommendations.
- **Common misunderstandings:** That it is an ATS, a job portal, or "the AI interviewer." It is none of these (DOC-03 §10–11, §3).
- **Related terms:** Hiring Intelligence Network, Evidence Graph, Company Calibration, Hiring Memory.
- ⚠️ **Never confuse with:** **Hiring Intelligence Network** (the *cross-company, compounding* whole) or a **system of record**.

#### Hiring Intelligence Network  *[Benchmarking Context]*
- **Definition:** The compounding, cross-company whole — all Evaluations, Evidence, Outcomes, and Benchmarks across all customers — that makes the layer smarter for everyone with each additional evaluation and outcome (DOC-03 §5.1). The **network** is the moat.
- **Why it exists:** Names the network-effect asset that a single-company layer cannot provide (e.g., benchmarking).
- **Examples:** The network that enables "top 2% of 10,000 Python engineers evaluated in 12 months."
- **Common misunderstandings:** Confusing it with the per-company Layer, or thinking it means sharing one company's private data with another (it enables *aggregate* benchmarks, governed by strict privacy — §9).
- **Related terms:** Hiring Intelligence Layer, Benchmark, Evidence Graph, Data Flywheel.
- ⚠️ **Never confuse with:** **Hiring Intelligence Layer** (single-company view) or a candidate **Talent Pool** (one company's re-engageable set).

#### Evidence Graph  *[Outcome & Learning Context]*
- **Definition:** The connected, structured, queryable body of Evidence relating Candidates, Skills/Competencies/Capabilities, Roles, Companies, and Outcomes — enriched by every Evaluation and every Outcome across the Network.
- **Why it exists:** The structural asset that makes evidence *relatable* and *explainable* and that compounds (DOC-03 §13).
- **Examples:** The graph linking a candidate's demonstrated competencies to role requirements and later outcomes.
- **Common misunderstandings:** Treating it as a database schema (it is a *conceptual* asset here; architecture is DOC-12) or as a candidate list.
- **Related terms:** Evidence, Evidence Item, Hiring Memory, Benchmark, Outcome Learning.
- ⚠️ **Never confuse with:** a **database** (this is the business concept) or **Hiring Memory** (company-specific learned wisdom, a distinct concept).

#### Company Calibration  *[Calibration & Memory Context]*  · **Owner: Intelligence Domain · Status: Stable**
- **Definition:** The learned model of how a *specific Company (or Organization unit)* defines "good" for its Roles — its bar, values, and role-specific priorities — used to contextualize Evaluations. **It is one component of Hiring Memory** (D-04.A3), not a synonym for it: Calibration is the *standard of good*; Memory is the *complete* learned intelligence that contains Calibration plus manager patterns, outcomes, and success/failure patterns.
- **Why it exists:** The same evidence should be judged against *this* company's standard, not a generic one (DOC-03 §5).
- **Examples:** Learning that Company X weights systems-design and pragmatism over algorithmic puzzle speed.
- **Common misunderstandings:** Confusing Calibration (the company's *standard of good*) with Hiring Memory (the company's *accumulated hiring experience and patterns*). Calibration is closely related to but narrower than Memory.
- **Related terms:** Hiring Memory, Role, Hiring Manager, Evaluation.
- ⚠️ **Never confuse with:** **Hiring Memory** (broader: includes how managers think and how successes/failures behaved over time).

#### Hiring Memory  *[Calibration & Memory Context]*  · **Owner: Intelligence Domain · Status: Stable**
- **Definition:** The **complete living, accumulated intelligence of how a Company hires** — the whole; Company Calibration is only *one component* of it (D-04.A3). Hiring Memory comprises:
  - **Company Calibration** (the standard of "good")
  - **Hiring Manager Patterns** (how specific managers think/decide)
  - **Outcome Learning** (what actually predicted success)
  - **Historical Decisions** (past advance/reject choices)
  - **Successful-Employee Patterns** (how thrivers behaved)
  - **Failed-Hire Patterns** (how mis-hires behaved)
  - **Organizational Preferences** (team/org-specific priorities)
  - **Learned Hiring Behaviors** (accumulated, evolving patterns)
  Used to evaluate new Candidates against this memory. The single most defensible moat asset (DOC-01 A-0.2, DOC-03 §13).
- **Why it exists:** Encodes a customer's hard-won hiring wisdom so evaluations improve over time and cannot be cloned by a competitor.
- **Examples:** "This company's successful senior engineers consistently showed X; its failed ones showed Y — this candidate resembles the former."
- **Common misunderstandings:** Reducing it to Calibration (the bar). Memory is broader: it includes *outcome-informed patterns of success and failure*, not just the standard.
- **Related terms:** Company Calibration, Outcome Learning, Evidence Graph, Decision Quality.
- ⚠️ **Never confuse with:** **Company Calibration** (the standard of good) — Memory *contains and extends* calibration with outcome-based patterns.

#### Outcome Learning  *[Outcome & Learning Context]*
- **Definition:** The process of connecting Hiring Decisions to actual on-the-job Outcomes and feeding that back to improve Evaluation, Calibration, and Hiring Memory. Closes the loop DOC-02 identified as broken (Root cause C).
- **Why it exists:** Turns the system from a static scorer into a learning system; the Learning flywheel (DOC-03 §17).
- **Examples:** Learning that candidates the system rated highly on a competency did in fact outperform, and adjusting accordingly.
- **Common misunderstandings:** That any analytics = outcome learning. It specifically requires *decision → real outcome → feedback into the model.*
- **Related terms:** Outcome, Hiring Memory, Evidence Graph, Decision Quality.
- ⚠️ **Never confuse with:** generic **reporting/analytics** (descriptive, not loop-closing).

#### Outcome  *[Outcome & Learning Context]*  · **Owner: Outcome & Learning Domain · Status: Stable**
- **Definition:** The observed on-the-job result of a Hiring Decision — e.g., performance, ramp, retention, or attrition of a hired Candidate — used by Outcome Learning to close the loop.
- **Why it exists:** Decision Quality can only be validated against real results; the Outcome is the ground-truth signal Outcome Learning consumes.
- **Examples:** "Hired candidate reached full productivity in 2 months and was rated top-quartile at first review"; "left within 6 months."
- **Common misunderstandings:** That we generate or own performance reviews (we don't — see Employee); the Outcome is *referenced* from the customer's world.
- **Related terms:** Outcome Learning, Employee, Hiring Decision, Decision Quality.
- ⚠️ **Never confuse with:** **Recommendation/Evaluation** (predictions *before* the hire) — an Outcome is what actually happened *after*.

#### Employee  *[External — Reference-Only]*  · **Owner: External (customer HRIS) · Status: Stable (Reference-Only)** *(D-04.A4)*
- **Definition:** A hired Candidate in their post-hire role at the Company. **A reference-only term in our domain** — the Employee entity is owned by the customer's HRIS (Workday, SuccessFactors, Rippling, etc.), not by us.
- **Why it exists (for us):** *Only* because Outcome Learning needs post-hire performance signals. We reference the Employee to obtain Outcomes; we never manage employment. (We are not an HRIS — DOC-03 §10 spirit.)
- **Examples:** A hired backend engineer whose 6-month performance signal feeds Outcome Learning.
- **Common misunderstandings:** That building "Employee" features drifts us toward HRIS. It must not — Employee is a reference boundary, like Requisition and Offer.
- **Related terms:** Outcome, Outcome Learning, Candidate (pre-hire), Requisition (also reference-only).
- ⚠️ **Never confuse with:** **Candidate** (pre-hire, our domain) — Employee is post-hire and *external*.

### 4.H — Trust, Fairness & Compliance

---

#### Explainability  *[Trust, Fairness & Compliance Context]*
- **Definition:** The property that every Signal, Evaluation, Recommendation, and Hiring Decision-support output carries the specific Evidence and reasoning that produced it — auditable by candidates, hiring managers, and regulators. **A non-negotiable gate** (DOC-01 §9).
- **Why it exists:** Legally required (LL144, EU AI Act) and central to trust; a black box is disqualified by design.
- **Examples:** A recommendation that cites the exact evidence items and reasoning behind it.
- **Common misunderstandings:** Confusing explainability (evidence + reasoning behind an output) with transparency about the *algorithm*. We explain the *decision's basis*, not necessarily model internals.
- **Related terms:** Evidence Item, Fairness, Trust, Recommendation.
- ⚠️ **Never confuse with:** **Confidence** (the system's certainty) — explainability is about *showing the basis*, not the certainty level.

#### Fairness  *[Trust, Fairness & Compliance Context]*
- **Definition:** The property that Evaluations and Recommendations do not produce unjustified disparate treatment or disparate impact across protected groups, and are based on legitimate, role-relevant Evidence. Part of the non-negotiable gate.
- **Why it exists:** Ethical mission (replace biased resume screening) and legal necessity (Title VII, adverse-impact doctrine).
- **Examples:** Ensuring a competency evaluation does not systematically disadvantage a protected group without job-related justification.
- **Common misunderstandings:** Equating fairness with identical outcomes, or assuming AI is automatically fair (it is not — DOC-02, §7.4). Fairness is engineered and audited, not assumed.
- **Related terms:** Bias, Adverse Impact, Explainability, Trust.
- ⚠️ **Never confuse with:** **Bias** (fairness is the *goal/property*; bias is the *defect* that violates it).

#### Bias  *[Trust, Fairness & Compliance Context]*
- **Definition:** A systematic error or unjustified influence in Evidence, Signals, or Evaluations that leads to unfair outcomes — whether inherited from data, sensors, models, or process.
- **Why it exists:** We must name the defect precisely to detect, measure, and mitigate it (DOC-02 P-C2; the resume-screening bias we exist to replace).
- **Examples:** A model that penalizes employment gaps; a signal correlated with a protected attribute rather than ability.
- **Common misunderstandings:** That bias only means human prejudice; it includes statistical/data bias and proxy variables.
- **Related terms:** Fairness, Adverse Impact, Verification, Trust.
- ⚠️ **Never confuse with:** **Fairness** (the property bias violates) or **Signal** (a legitimate indicator — a signal becomes bias only when it is unjustified/proxy).

#### Adverse Impact  *[Trust, Fairness & Compliance Context]*
- **Definition:** A measurable, disproportionately negative effect of a selection practice on a protected group (e.g., failing the four-fifths rule), regardless of intent.
- **Why it exists:** The legal/technical standard by which fairness is tested (DOC-02); central to our compliance posture.
- **Examples:** A selection step whose pass rate for one group is <80% of the highest group's rate.
- **Common misunderstandings:** That adverse impact requires intent to discriminate. It does not — it is about *effect*.
- **Related terms:** Fairness, Bias, Compliance, Explainability.
- ⚠️ **Never confuse with:** **Bias** (the cause/defect) — adverse impact is the *measured effect*.

#### Integrity Score  *[Trust, Fairness & Compliance Context]*  · **Owner: Trust Domain · Status: Stable** *(renamed from "Trust Score", D-04.A1)*
- **Definition:** A measure of how **authentic and trustworthy the Evidence is** — i.e., protection against fraud, impersonation, AI misuse, and un-verified claims. It measures the *integrity of the evidence*, **not** the candidate's ability and **not** the system's certainty in its own judgment.
- **Why it exists:** Anti-fraud/anti-gaming (DOC-02: resume fraud, cheating, impersonation, AI-generated submissions) requires an integrity measure distinct from quality (Evaluation Score) and from system certainty (Confidence).
- **Examples:** Integrity Score: 98 for a verified, proctored work sample; a lowered Integrity Score when impersonation or AI misuse is suspected.
- **Common misunderstandings:** Conflating it with Confidence (system certainty) or Evaluation Score (candidate quality). These are three different concepts (see the triad, A-04.1).
- **Related terms:** Verification, Confidence, Evaluation Score, Evidence, Bias.
- ⚠️ **Never confuse with:** **Confidence** (system's certainty) or **Evaluation Score** (candidate quality). *The triad Evaluation Score / Confidence / Integrity Score is disambiguated by design (A-04.1) precisely to end this confusion.*

#### ~~Trust Score~~ *(DEPRECATED)*  · **Owner: Trust Domain · Status: Deprecated · Superseded by → Integrity Score**
- **Definition:** Former name for **Integrity Score**. Retained only for backward-compatibility of pre-freeze documents/discussions. **Do not use in any new document, API, or UI** — use **Integrity Score**.

#### Human Accountability (Framework)  *[Trust, Fairness & Compliance Context]*  · **Owner: Trust Domain · Status: Stable** *(reframed from "Human-in-the-Loop", A-04.3 / DOC-05 A-05.2 §A1)*
- **Definition:** The principle that humans are **accountable** for Hiring Decisions and decision policies, with **oversight proportional to decision risk** — High/Very-High-risk decisions require direct human review, while Low/Medium-risk decisions may be automated within approved governance provided fairness, explainability, and auditability stay intact. Rejects "human click theater."
- **Why it exists:** Regulators demand *meaningful* human oversight, not rubber-stamping; blanket "a human reviews every rejection" is neither scalable nor genuinely protective. Legal defensibility (EU AI Act human-oversight), ethics, trust.
- **Examples:** A clearly-out-of-policy, low-risk screen auto-progresses with an audit trail; a borderline candidate is routed to a recruiter; finalists go to the hiring manager; executive hiring goes to a panel.
- **Common misunderstandings:** (1) That it means a human must click "approve" on every decision — it does not (that is the click-theater we reject). (2) That it permits autonomous High/Very-High-risk decisions — it does not.
- **Related terms:** Hiring Decision, Recommendation, Explainability, Fairness, Confidence.
- ⚠️ **Never confuse with:** **Recommendation** (advisory, automated). ⚠️ *Deprecated prior name:* "Human-in-the-Loop" (superseded by Human Accountability — the earlier absolute "human decides every time" reading is retired).

### 4.I — Process & Time Units

---

#### Hiring Cycle  *[Hiring Context]*
- **Definition:** The end-to-end process of filling a specific Position — from Requisition opening through Evaluations to Hiring Decision, Offer, and close (accepted/declined/closed).
- **Why it exists:** The primary process container that Hiring Events occur within; the unit of "a hire."
- **Examples:** The full process for filling REQ-1043.
- **Common misunderstandings:** Confusing the Hiring Cycle (one position's process) with a Hiring Event (one occurrence within it).
- **Related terms:** Requisition, Position, Hiring Event, Hiring Decision.
- ⚠️ **Never confuse with:** **Hiring Event** (a discrete occurrence *within* a cycle).

#### Hiring Event  *[Hiring Context]*
- **Definition:** A discrete, meaningful occurrence within a Hiring Cycle that changes state or produces information (e.g., Candidate Applied, Evaluation Started, Recommendation Generated, Hiring Decision Made). *(These are the Business Events enumerated in §7.)*
- **Why it exists:** Names the atomic occurrences that drive lifecycles and that the business reasons about.
- **Examples:** "Candidate Applied"; "Outcome Recorded."
- **Common misunderstandings:** Confusing a business Hiring Event (domain-level occurrence) with a technical/system event (implementation — not our concern here).
- **Related terms:** Hiring Cycle, Business Events (§7), state machines (§6).
- ⚠️ **Never confuse with:** a **system/technical event** (DOC-12 territory) — here "event" means a *business* occurrence.

#### Candidate Afterlife  *[Candidate Context]*
- **Definition:** The set of states and value a Candidate holds *after* a Rejection — as a Silver Medal Candidate, Talent Pool member, referral source, future applicant, or advocate. Rejection is a transition, not an exit (DOC-03 §18.4).
- **Why it exists:** Reframes the funnel's largest population (the rejected) as a durable network/growth asset.
- **Examples:** A rejected finalist re-engaged nine months later for a better-fit role.
- **Common misunderstandings:** That rejection ends the relationship. It begins the afterlife.
- **Related terms:** Rejection, Silver Medal Candidate, Talent Pool, Portable Evidence.
- ⚠️ **Never confuse with:** **Rejection** (the transition event) — the afterlife is what follows it.

#### Benchmark  *[Benchmarking Context]*
- **Definition:** A network-derived comparison that places a Candidate (or an Evaluation) against a relevant population across the Hiring Intelligence Network (e.g., "top 2% of 10,000 Python engineers evaluated in the last 12 months").
- **Why it exists:** A headline network-effect capability (DOC-01 A-0.2, DOC-03 §5) impossible without scale.
- **Examples:** Percentile placement of a candidate's system-design competency against the network.
- **Common misunderstandings:** That benchmarks expose other companies' or candidates' private data — they are *aggregate/anonymized* by strict constraint (§9).
- **Related terms:** Hiring Intelligence Network, Confidence, Competency, Evaluation.
- ⚠️ **Never confuse with:** **Score** (a single candidate's evaluation output) — a benchmark is *relative to a population*.

---

## 5. Domain Relationships (Conceptual)

*How the major concepts relate, in business terms. No data models, no cardinalities-as-schema — these are conceptual relationships.*

```
A Company operates within an Organization structure, and defines Jobs.
A Job, shaped by a Company, becomes a Role.
A Role has one or more Positions (headcount), each authorized by a Requisition (in the ATS).
A Requisition opening begins a Hiring Cycle.

A Candidate submits an Application to a Position, entering that Hiring Cycle.
Within the cycle, Sensors (Interviews, Assessments) run in Evaluation Sessions.
Sensors produce Evidence (composed of Evidence Items).
Evidence is interpreted into Signals and structured into the Evidence Graph.

The Hiring Intelligence Layer interprets Evidence — contextualized by the Company's
Company Calibration and Hiring Memory — to produce an Evaluation.
An Evaluation (with Confidence, Explainability, Fairness checks, Trust Score, and Benchmarks
drawn from the Hiring Intelligence Network) yields a Recommendation.

A human uses the Recommendation + Evidence to make a Hiring Decision (human-in-the-loop).
A Hiring Decision leads to an Offer (→ hire) or a Rejection (→ Candidate Afterlife:
Silver Medal / Talent Pool / Portable Evidence).

A hire produces an Employee, whose on-the-job Outcome is recorded.
Outcome Learning feeds Outcomes back into Hiring Memory, Company Calibration, the Evidence
Graph, and Benchmarks — making the next Evaluation smarter (the flywheels, DOC-03 §14–17).
```

**Key relationship rules (business-level):**
- **Sensors → Evidence → Signals → Evaluation → Recommendation → (human) Hiring Decision → Outcome → Learning.** This is the master value chain; every term sits somewhere on it.
- **Company Calibration and Hiring Memory contextualize every Evaluation** for that Company. Nothing is judged "generically."
- **Benchmarks come from the Network, not a single Company.**
- **Outcome Learning is the only backward arrow** — it is what makes the chain a *loop*, not a pipeline.

---

## 6. Business State Machines (Conceptual)

*Business states and transitions only — not technical states. Each lifecycle lists states and the Hiring Events (§7) that transition them.*

### 6.1 Candidate Lifecycle
`Prospect → Applied → In Evaluation → Evaluated → Recommended → In Decision → [ Hired | Rejected ]`
- From **Rejected** → `Silver Medal / Talent Pool` (Candidate Afterlife) → may re-enter as **Applied**/**In Evaluation** for a new Role.
- From **Hired** → `Employee` → (later) `Outcome Known`.
- *Invariant:* a candidate never silently disappears; rejection transitions to the afterlife, not to nothing.

### 6.2 Company Lifecycle
`Prospect → Design Partner | Trial → Onboarding & Calibrating → Active Customer → Expanding → [ Renewing | Churned ]`
- **Onboarding & Calibrating** is where initial Company Calibration and early Hiring Memory form.
- *Note:* the moat (Hiring Memory, Outcome Learning) deepens across **Active → Expanding**, raising switching cost.

### 6.3 Evaluation Lifecycle
`Requested → Evidence Collection (Evaluation Sessions) → Evidence Structured → Interpreted (Signals) → Scored/Judged → Recommendation Generated → Delivered → [ Acted-upon | Contested/Reviewed ] → Finalized → Outcome-Linked`
- **Contested/Reviewed** exists because explainability implies the right to question (candidate/HM/regulator).
- *Invariant:* no Evaluation reaches **Delivered** without Explainability and Fairness checks (the gate).

### 6.4 Hiring (Cycle) Lifecycle
`Requisition Opened → Role Calibrated → Candidates Entering → Evaluating → Shortlist Formed → Interviewing → Decision → [ Offer → (Accepted | Declined) | No Hire ] → Closed`
- Runs inside the customer's system of record; we participate, we do not own it (DOC-03 §10).

### 6.5 Evidence Lifecycle
`Captured (by Sensor) → Structured (Evidence Graph) → Verified → Interpreted (Signals) → Benchmarked → Retained → [ Refreshed | Aged ] → Archived/Expired (per retention & consent)`
- *Invariant:* Evidence is never silently discarded; expiry follows explicit retention/consent rules (§9).

### 6.6 Recommendation Lifecycle
`Generated → Explained (evidence attached) → Delivered → [ Accepted | Overridden ] by human → Decision-Linked → Outcome-Linked → Learned-From`
- **Overridden** is a first-class, expected state (human-in-the-loop); overrides are themselves signal for Outcome Learning.

---

## 7. Business Events

*Domain-level occurrences (Hiring Events) that drive the state machines and the flywheels. Business meaning only — not technical event schemas.*

| Business Event | Meaning | Primarily advances / feeds |
|---|---|---|
| **Candidate Applied** | A Candidate entered a Hiring Cycle for a Position. | Candidate Lifecycle → Applied |
| **Evaluation Started** | Evidence collection/evaluation began for a Candidate. | Evaluation Lifecycle → Evidence Collection |
| **Evidence Produced** | A Sensor generated new Evidence (Evidence Items). | Evidence Lifecycle; Evidence Graph |
| **Evidence Verified** | Evidence authenticity confirmed. | Trust Score; Evidence Lifecycle |
| **Evaluation Completed** | The layer produced a structured, explainable Evaluation. | Evaluation Lifecycle → Judged |
| **Recommendation Generated** | An explainable Recommendation was produced. | Recommendation Lifecycle → Generated |
| **Recommendation Delivered** | The Recommendation + Evidence reached the human. | Recommendation Lifecycle → Delivered |
| **Hiring Decision Made** | A human made the binding advance/hire/reject choice. | Hiring Lifecycle → Decision; Candidate Lifecycle |
| **Offer Extended / Accepted / Declined** | Offer milestones. | Hiring Lifecycle |
| **Candidate Rejected** | Candidate not advanced; enters Afterlife. | Candidate Lifecycle → Rejected/Afterlife |
| **Employee Joined** | A hire started the job. | Candidate → Employee; enables Outcome |
| **Outcome Recorded** | On-the-job performance/retention data captured. | Outcome & Learning |
| **Hiring Memory Updated** | Calibration/memory refined from evidence + outcomes. | Calibration & Memory |
| **Benchmark Updated** | Network benchmarks recomputed with new data. | Benchmarking; Network |
| **Evidence Expired/Archived** | Evidence aged out per retention/consent. | Evidence Lifecycle |

> These events are the vocabulary of "what happened" in the business. Every future document describing behavior should use *these* event names, not invented synonyms.

---

## 8. Invariants (Business Rules That Must Always Be True)

These are inviolable. A design, feature, or model that breaks one is wrong by definition. *(Enforcement/architecture is later docs; these are the business truths.)*

1. **INV-1 — Human accountability.** *(Amended A-04.3 to match DOC-05 P2, the Human Accountability Framework.)* Humans are accountable for Hiring Decisions and for the decision policies that govern them. Automation may execute decisions **only within an approved governance framework, with oversight proportional to decision risk**: High/Very-High-risk decisions (finalists, executive hiring) require **direct human review**; Low/Medium-risk decisions may be automated **only** where fairness (INV-3), explainability (INV-2), and auditability remain fully intact. The platform never makes an *unaccountable* or *ungoverned* decision, and rejects "human click theater." *(See DOC-05 A-05.2 §A1.)*
2. **INV-2 — No unexplained output.** Every Signal, Evaluation, and Recommendation carries the specific Evidence and reasoning behind it. Nothing ships as a bare score. *(Explainability gate.)*
3. **INV-3 — No recommendation without fairness safeguards.** No Recommendation is delivered without passing fairness/adverse-impact safeguards. *(Fairness gate.)*
4. **INV-4 — Evidence over claims.** A Hiring Decision supported by our layer is grounded in Evidence of ability, never in the Resume alone. *(Founding thesis.)*
5. **INV-5 — Every Evaluation is contextualized.** No candidate is judged "generically"; every Evaluation is against a Role, contextualized by Company Calibration/Hiring Memory.
6. **INV-6 — Confidence is always expressed.** Every Evaluation/Recommendation states its Confidence; low-evidence outputs are never presented as certain.
7. **INV-7 — Candidacy persists.** A Rejected Candidate transitions to the Afterlife; they are never silently erased from the network (subject to consent/retention).
8. **INV-8 — Benchmarks are aggregate.** Benchmarks derive from the Network in aggregate/anonymized form; one Company's or Candidate's private data is never exposed to another.
9. **INV-9 — We are never the system of record.** The platform references Requisitions/Positions/Offers owned by the customer's systems; it does not become the ATS or job portal. *(DOC-03 §10–11.)*
10. **INV-10 — Sensors are inputs, never the product.** No sensor (interview/assessment) is positioned, sold, or modeled as the product; the product is Decision Quality.
11. **INV-11 — Consent governs candidate data.** Candidate Evidence use, retention, and portability are governed by consent; candidate data is never sold (KD-03.14).
12. **INV-12 — The loop closes.** Where Outcomes are available, they feed back via Outcome Learning; the system is designed to learn, not merely score.

---

## 9. Domain Constraints

*Boundaries the domain imposes on any future design — the "outer fence."*

- **DC-1 — Neutrality.** The domain is neutral across systems of record and sensors; no term or model may privilege one ATS, one sensor, or one vendor. *(KD-03.12: compete only on the intelligence layer.)*
- **DC-2 — Sensor-agnostic.** The vocabulary must remain valid as sensors change or new ones emerge; nothing binds the domain to "the interview."
- **DC-3 — Privacy & residency-aware.** Evidence and candidate data handling must respect consent, retention limits, and (for expansion) data-residency regimes; benchmarks are aggregate-only (INV-8). *(US-first, global-ready — DOC-01 §5.)*
- **DC-4 — Regulatory-bounded.** All evaluation/recommendation concepts operate within employment law (adverse impact, explainability mandates); fairness/explainability are gates, not options.
- **DC-5 — Candidate is not inventory.** No term or model may treat candidates as attention/inventory to be monetized; candidate value is experience, growth, reputation, referrals, portable evidence (KD-03.14).
- **DC-6 — Company scope for calibration/memory.** Calibration and Hiring Memory are scoped to a Company/Organization and never leak across Companies (only aggregate network benchmarks cross the boundary, INV-8).
- **DC-7 — Recommendation ≠ decision, and decisions are governed.** *(Amended A-04.3.)* A Recommendation is always distinct from a Hiring Decision. A Recommendation may only become an executed decision **through an approved, risk-proportional governance policy with human accountability** (INV-1 / DOC-05 P2) — never as a silent, ungoverned, or unaccountable automatic act. High/Very-High-risk decisions require direct human review.

---

## 10. Open Questions

**Resolved by Amendment A-04.2 (CTO, 2026-07-21):**
- ~~Q1 Score as a term~~ → **Resolved:** define **Evaluation Score**; bare "Score" **forbidden** (D-04.A5).
- ~~Q2 Calibration vs. Memory~~ → **Resolved:** Company Calibration **⊂** Hiring Memory (D-04.A3).
- ~~Q3 Employee~~ → **Resolved:** **Reference-Only** (D-04.A4).
- ~~Q5 Billing unit~~ → **Resolved:** **Candidate Evaluation** = one Candidate + one Role + one final Recommendation (D-04.A2).
- ~~Q7 Trust Score naming~~ → **Resolved:** renamed **Integrity Score**; measurement triad disambiguated (D-04.A1); "Trust Score" Deprecated.

**Still open:**
1. **"Fit" vocabulary.** We reference "fit" informally (role fit, company fit). Do we need formal terms (Role Fit, Values Fit) — and how do we keep "culture fit" from becoming a bias vector? *(Recommend deferring formal definition to the Fairness/Evaluation-Engine work, DOC-11, so it is designed with adverse-impact safeguards from the start. Flag: "culture fit" is a known bias risk.)*
2. **Signal-strength vocabulary.** Do we standardize canonical terms for signal strength (e.g., High/Medium/Low Signal), or leave it qualitative? *(Recommend a small canonical scale once the Evaluation Engine is designed, DOC-11.)*
3. **Benchmark Percentile as a formal term?** A-04.A5 lists "Benchmark Percentile" as an allowed qualified score. Should it be a formal glossary entry distinct from **Benchmark**? *(Recommend: yes, add as a sub-term of Benchmark in a future amendment when Benchmarking is specified.)*

---

## 11. Summary

### 11.1 What this document establishes
- The **canonical vocabulary** of the company: ~45 defined terms across 12 bounded contexts and 3 domain tiers (Core/Supporting/Generic).
- The **hard disambiguations** the strategy depends on: *Sensor ≠ Product; Recommendation ≠ Hiring Decision; Evidence ≠ Signal ≠ Resume; Skill ⊂ Competency ⊂ Capability; Job ≠ Role ≠ Position; Confidence ≠ Trust Score ≠ Score; Calibration ⊆ Memory; Layer ≠ Network.*
- The **conceptual relationships**, **six business lifecycles**, **fifteen business events**, **twelve invariants**, and **seven domain constraints** that govern all future design.

### 11.2 Terminology Freeze (governance — per CTO directive)
> **Upon ratification of DOC-04, company terminology FREEZES.** From that point:
> 1. No future document, diagram, API, data model, UI, sales, or legal artifact may introduce a new business term without either (a) it already existing here, or (b) a formal **amendment to DOC-04** that adds/extends the term (with definition + the six fields + owning context).
> 2. No future document may *redefine* a term — it must *reference* DOC-04.
> 3. Extending the domain model (new context, new term) is allowed and expected as the company grows — but only *through* this document, never around it.
> 4. Amendments are versioned (v0.2, v0.3…) with a short changelog, exactly as DOC-01/02/03 amendments were handled.
>
> **Rationale:** this discipline prevents the documentation — and therefore the product, the data model, and the customer's mental model — from drifting as the company scales. The glossary is a living document with a controlled process, not a frozen stone tablet and not a free-for-all.

### 11.3 Key decisions recorded here
- **KD-04.1** — Ubiquitous Language is canonical; all future artifacts reference DOC-04 rather than redefining terms.
- **KD-04.2** — Domains classified Core (Evaluation, Intelligence, Evidence, Outcome Learning, Benchmarking) / Supporting / Generic; invest disproportionately in Core (mirrors DOC-03 §13).
- **KD-04.3** — Twelve invariants (§8) are inviolable business truths (esp. INV-1 human-decides, INV-2 explainability, INV-3 fairness, INV-10 sensors-not-product).
- **KD-04.4** — Terminology freezes on ratification, with a controlled amendment process (§11.2).
- **KD-04.5** — Measurement triad ratified (A-04.A1): **Evaluation Score** (candidate quality) · **Confidence** (system certainty) · **Integrity Score** (evidence authenticity, renamed from Trust Score). Bare "Score" forbidden.
- **KD-04.6** — Billing unit ratified (A-04.A2): **Candidate Evaluation** = one Candidate + one Role + one final Recommendation, sessions included.
- **KD-04.7** — **Company Calibration ⊂ Hiring Memory** (A-04.A3); **Employee is Reference-Only** (A-04.A4).
- **KD-04.8** — Every term carries **Owner (governing Domain)** and **Lifecycle Status** (Stable/Emerging/Experimental/Deprecated), maintained in the Term Registry (A-04.C); term changes require owning-Domain approval.

### 11.4 Unresolved questions (for founder/CTO)
The seven open questions in §10 — most consequentially: (a) whether to formally define "Score," (b) confirming the Calibration⊆Memory hierarchy, (c) the precise billing-unit definition of "candidate evaluation" (cross-ref KD-03.10), and (d) whether to rename "Trust Score" → "Integrity Score" to kill a dangerous naming collision.

### 11.5 Suggested next document
**DOC-05 — Product Principles & Non-Negotiables (the Constitution)** — per the ratified roadmap:
`DOC-01 Vision → DOC-02 Problem → DOC-03 Business Strategy → DOC-04 Domain Model → DOC-05 Product Principles → DOC-06 Personas → DOC-07 User Journeys → DOC-08 Functional Requirements → DOC-09 NFRs → DOC-10 AI Strategy → DOC-11 Evaluation Engine → DOC-12 Architecture.`
- **Why next.** With the vision, problem, strategy, and now a fixed language in hand, we can finally codify the *rules every future decision must obey* — the fairness/explainability gate, sensors-not-product, decision-quality-is-the-product, integration-first, neutrality, never-an-ATS, human-in-the-loop, candidate-as-user — expressed precisely in the now-frozen vocabulary. Principles written *after* the language are unambiguous; principles written before it drift.

---

*End of DOC-04 v0.1. Upon ratification this becomes the canonical language of the company and terminology freezes per §11.2. Awaiting founder review of the seven open questions (§10) before promotion to Ratified.*
