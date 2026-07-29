# Document 12 — Capability Map

| Field | Value |
|---|---|
| **Document ID** | DOC-12 |
| **Title** | Capability Map (Business Layer) |
| **Owner** | Principal Engineer / Technical Documentation Lead |
| **Status** | Draft v0.1 — for founder review |
| **Created** | 2026-07-21 |
| **Depends on** | DOC-04 (Domains), DOC-05 (gates), DOC-08 (Personas), DOC-09 (JTBD), DOC-10 (Service Blueprint + Capability Register A-10.2) |
| **Blocks** | (later) DOC-17 Architecture — *"What logical components must exist to realize these business capabilities?"* This document sets that question up; it does **not** answer it. |
| **Hard scope rule (CTO-ratified)** | Stops at **Capability → Business Service.** **Absolutely NO** systems, microservices, APIs, event buses, databases, deployment topology, AI agents, or technical architecture. Those belong exclusively to DOC-17. |
| **Quality bar** | **Architecture-independent.** If an architecture team could implement this platform as a monolith, microservices, serverless, or anything else *without changing DOC-12*, the abstraction level is correct. This document should be stable for many years. |
| **Vocabulary** | Uses DOC-04 frozen terms exactly. Introduces **no** new business terms. |

---

## How to read this document — Capability vs. Business Service

- A **Capability** is *something the business must be able to do* — an ability, stated at business level (e.g., "verify evidence authenticity," "capture how a company defines good"). It is **not** a feature, a screen, or a component.
- A **Business Service** is a *coherent grouping of capabilities that together deliver a recognizable unit of business value* to consumers (e.g., the "Evidence Service"). It is **not** a microservice, a codebase, or a deployable — it is a *business-architecture* grouping.
- A **Domain** (DOC-04 §3) **owns** capabilities and services — the accountable governor of their meaning and change.

> **The layering, and where we stop:**
> ```
> Domain  ──owns──▶  Business Service  ──groups──▶  Capability      ← DOC-12 STOPS HERE
> ─────────────────────────────────────────────────────────────
> (Logical Component ▶ System ▶ Service ▶ …)                        ← DOC-17 Architecture ONLY
> ```

**Design choice for the Register (§3).** Each capability carries all twelve required attributes. Ten are in the Register table; the two *relational* attributes — **Consumers** and **Dependencies** — are captured in their natural homes: the **Interaction Matrix (§5)** (consumers) and the **Dependency Map (§4)** (dependencies). This avoids an unreadable 12-column table while keeping every attribute present and authoritative.

**Attribute scales used:**
- **Criticality:** **Foundational** (a gate / always-on; non-negotiable) · **Mission-Critical** (a Mission-Critical JTBD depends on it) · **Strategic** (compounding moat) · **Operational** (supporting).
- **Maturity** (DOC-10 A-10.2): L0 Manual → L1 Assisted → L2 Evidence-Driven → L3 Learning → L4 Self-Improving.
- **Lifecycle:** **Permanent** (always exists) · **Evolving** (deepens across maturity) · **Emerging** (new/immature).
- **A/A:** **Advisory** (human can override) vs **Authoritative** (non-overridable gate) — DOC-10 A-10.2 §A-4.

---

## 1. The Business Capability Model (overview)

Ten Business Services group the platform's capabilities. This is the business-architecture skeleton — technology-free.

| Business Service | Purpose (business value) | Owner Domain |
|---|---|---|
| **1. Intake & Integration Service** | Meet every workflow where it is; get roles, applications, and communications in/out without anyone changing how they work. | Company / Work |
| **2. Calibration & Memory Service** | Learn how *this* company hires and accumulate that intelligence over time. | Intelligence |
| **3. Evidence Service** | Collect, verify, and structure genuine evidence of ability. | Evidence |
| **4. Evaluation Service** | Turn evidence into explainable, confidence-qualified judgment and recommendations. | Evaluation |
| **5. Benchmarking Service** | Place a candidate against the network. | Benchmark / Intelligence |
| **6. Explainability Service** | Produce audience-appropriate explanations for every output. | Trust / Fairness / Compliance |
| **7. Decision Service** | Support and record the human decision; reflect it outward. | Hiring |
| **8. Candidate Experience Service** | Serve the candidate as a first-class, lifetime participant. | Candidate |
| **9. Outcome & Learning Service** | Close the loop from decision to real outcome, and improve. | Outcome & Learning |
| **10. Trust, Fairness & Compliance Service** | Enforce the gates: fairness, integrity, consent, audit, isolation. (The "always-on ground.") | Trust / Fairness / Compliance |

---

## 2. The Business Services at a glance

- **Value-producing services** (what the customer feels): Evidence, Evaluation, Benchmarking, Explainability, Decision, Candidate Experience.
- **Compounding services** (the moat): Calibration & Memory, Benchmarking, Outcome & Learning — these climb to L4 (DOC-09 A-4).
- **Foundational service** (the ground, always-on): Trust, Fairness & Compliance — houses every **Authoritative** capability (the gates).
- **Enabling service**: Intake & Integration — the frictionless "never change how you work" surface (P11).

---

## 3. The Capability Register

*Every major business capability from DOC-10. **Consumers → §5; Dependencies → §4.***

| # | Capability | Purpose (business ability) | Business Service | Owner Domain | Criticality | Maturity | Lifecycle | A/A | Gates enforced | Primary JTBD served | Personas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | **Requisition Sync** | Reference the customer's ATS requisition to anchor a Hiring Cycle | Intake & Integration | Company/Work | Operational | L1→L2 | Permanent | Advisory | Neutrality (P5), not-SoR (P4) | Rina: intake/calibrate | Rina, David |
| C2 | **Candidate Intake (Import)** *(renamed from "Application Intake")* | **Import applicants from the customer's systems** (ATS sync / upload) — we do **not** accept job applications ourselves (KD-12.7) | Intake & Integration | Candidate | Mission-Critical | L1→L2 | Permanent | Advisory | No-behavior-change (P11), consent (P3), not-SoR (P4) | Rina: evaluate imported candidates | Alex, Rina |
| C3 | **Integrations** | Connect to ATS/email/API/webhook workflows | Intake & Integration | Company | Mission-Critical | L1→L2 | Permanent | Advisory | Neutrality (P5), not-SoR (P4) | Never change how you work | Rina, Marcus |
| C4 | **Candidate Communication & Status** | Keep candidates informed — never a black hole | Candidate Experience | Candidate | Mission-Critical | L1→L3 | Evolving | Advisory | Dignity (P7), honest disclosure (A1) | Alex: stay informed | Alex |
| C5 | **Notification (internal)** | Notify users at meaningful events, silence otherwise | Intake & Integration | Company | Operational | L1→L2 | Evolving | Advisory | (Waiting/Silence, A8/A9) | Rina: workflow | Rina, David |
| C6 | **Role Calibration Capture** | Capture how this company/manager defines "good" | Calibration & Memory | Intelligence | Mission-Critical | L1→L3 | Evolving | Advisory | Fairness — bar not bias (P1) | David: apply my bar | David, Rina |
| C7 | **Hiring Memory Update** | Accumulate the company's learned hiring intelligence | Calibration & Memory | Intelligence | **Strategic** | L1→L4 | Evolving | Advisory | Isolation (P3) | Compounding decision quality | David, Sofia |
| C8 | **Evidence Request & Collection** | Gather role-relevant evidence via Sensors | Evidence | Evidence | Mission-Critical | L1→L3 | Evolving | Advisory | Fairness (P1), dignity (P7), evidence-first | Alex: show ability | Alex, David |
| C9 | **Integrity / Authenticity Verification** | Ensure evidence is genuine (anti-fraud/impersonation) | Trust/Fairness/Compliance | Trust | **Foundational** | L1→L3 | Evolving | **Authoritative** | Integrity (Integrity Score) | Fair to honest candidates | Alex, Sofia |
| C10 | **Evidence Structuring (Evidence Graph)** | Structure evidence into queryable, explainable form | Evidence | Evidence/Intelligence | **Strategic** | L2→L4 | Evolving | Advisory | Explainability (P1) | Explainable evaluation | Rina, David |
| C11 | **Evaluation Orchestration** | Turn evidence into judgment vs. Calibration & Memory | Evaluation | Evaluation | Mission-Critical | L1→L3 | Evolving | Advisory | Fairness (P1), contextualized (INV-5), confidence (INV-6) | All evaluation jobs | David, Rina, Alex |
| C12 | **Confidence Determination** | Express honest certainty in every output | Evaluation | Evaluation | Mission-Critical | L2→L3 | Evolving | Advisory | Honesty (INV-6) | Honest evaluation | Rina, David |
| C13 | **Fairness / Adverse-Impact Checking** | Ensure no unjustified disparate impact | Trust/Fairness/Compliance | Trust | **Foundational** | L2→L4 | Evolving | **Authoritative** | Fairness gate (P1) | Sofia: defensible; Alex: fair | Sofia, Alex |
| C14 | **Benchmarking** | Place a candidate against the network | Benchmarking | Benchmark/Intelligence | **Strategic** | L1→L4 | Evolving | Advisory | Aggregate-only isolation (INV-8) | Contextual quality | Rina, David, Sofia |
| C15 | **Explanation Generation (audience-aware)** | Produce audience-appropriate explanations | Explainability | Trust | **Foundational** | L1→L3 | Evolving | **Authoritative** (requirement) | Explainability + Progressive (P1/P13) | Defend; candidate feedback | All |
| C16 | **Recommendation Preparation & Delivery** | Deliver evidence-first recommendations in-workflow | Evaluation | Evaluation | Mission-Critical | L2→L4 | Evolving | Advisory | Explainability (INV-2), evidence-first (§5) | Rina: shortlist; David: evidence | Rina, David |
| C17 | **Human-Decision Support & Capture** | Support and record the human decision/override | Decision | Hiring | **Foundational** | L1→L2 | Permanent | Advisory* | Human Accountability (P2) | David: own the decision | David, Rina |
| C18 | **Offer / Rejection Handling** | Reflect the decision to the ATS; trigger candidate outcome | Decision | Hiring | Operational | L1→L2 | Permanent | Advisory | Dignity (P7) | Decision outcome | Rina, Alex |
| C19 | **Candidate Feedback Delivery** | Give constructive, evidence-based feedback (esp. rejection) | Candidate Experience | Candidate | **Strategic** | L1→L3 | Evolving | Advisory | Progressive Explainability (P13), dignity (P7) | Alex: useful outcome | Alex |
| C20 | **Talent Pool / Afterlife Management** | Retain and re-engage candidates over time | Candidate Experience | Candidate | **Strategic** | L1→L3 | Evolving | Advisory | Consent (P3), dignity (P7) | Alex: remain a participant | Alex, Rina |
| C21 | **Outcome Capture** | Reference on-the-job outcomes (never own the HRIS) | Outcome & Learning | Outcome & Learning | **Strategic** | L1→L3 | Evolving | Advisory | Consent/isolation (P3), reference-only | Sofia: quality; learning | Sofia |
| C22 | **Outcome Learning** | Close the loop; improve evaluation/memory from outcomes | Outcome & Learning | Outcome & Learning | **Strategic** | L1→L4 | Evolving | Advisory | Fairness — learn without baking bias (P1) | The system gets smarter | Sofia, David |
| C23 | **Audit Recording** | Defensible trail of every material step | Trust/Fairness/Compliance | Trust | **Foundational** | L2→L3 | Permanent | **Authoritative** | Auditability (P8/INV-2) | Sofia/Marcus: defensibility | Sofia, Marcus |
| C24 | **Consent & Privacy Management** | Govern candidate data by consent; never sell | Trust/Fairness/Compliance | Trust | **Foundational** | L2→L3 | Permanent | **Authoritative** | Privacy/consent (P3), no-sale (KD-03.14) | Alex/Marcus: trust | Alex, Marcus |
| C25 | **Tenant Isolation** | Strict per-company isolation; aggregate-only benchmarks | Trust/Fairness/Compliance | Trust | **Foundational** | L3→L4 | Permanent | **Authoritative** | Isolation (P3/INV-8), security (P8) | Marcus: verify safe | Marcus, Sofia |

`*C17 Advisory:` the *capability* supports/records; the human decision it captures **is** the authoritative act (P2). The system never overrides the human here; the human overrides the system.

> **Pattern to note (unchanged from DOC-10):** every **Authoritative / Foundational** capability lives in the **Trust, Fairness & Compliance Service** and enforces a Tier-0 gate. That is the "architecture of trust" made explicit at capability level.

---

## 4. Capability Dependency Map

*The **Dependencies** attribute for every capability. A capability cannot be delivered before those it depends on. (Layered per DOC-10 A-10.2 §A-3; technology-free.)*

```
GROUND (no dependencies; everything depends on these):
   C25 Tenant Isolation · C24 Consent & Privacy · C23 Audit Recording

INTAKE:
   C1 Requisition Sync        ← depends on: C3 Integrations
   C2 Application Intake       ← C3 Integrations, C24 Consent
   C3 Integrations             ← (Ground)
   C4 Candidate Communication  ← C2 Application Intake
   C5 Notification             ← (Ground)
   C6 Role Calibration Capture ← C1 Requisition Sync

EVIDENCE:
   C8 Evidence Request/Collect ← C6 Calibration, C2 Application Intake
   C9 Integrity Verification   ← C8 Evidence Collection
   C10 Evidence Structuring    ← C8 Evidence Collection, C9 Integrity

INTELLIGENCE:
   C11 Evaluation Orchestration← C10 Evidence Structuring, C6 Calibration, C7 Hiring Memory
   C12 Confidence Determination← C11 Evaluation
   C13 Fairness Check          ← C11 Evaluation  (GATE — blocks C16 if failed)
   C14 Benchmarking            ← C10 Evidence Graph (network-scale), C11 Evaluation

OUTPUT:
   C15 Explanation Generation  ← C11 Evaluation, C13 Fairness, C10 Evidence
   C16 Recommendation Prep/Deliver ← C11 Evaluation, C12 Confidence, C13 Fairness(pass), C14 Benchmark, C15 Explanation

DECISION:
   C17 Human-Decision Support  ← C16 Recommendation
   C18 Offer/Rejection Handling← C17 Decision, C1 Requisition (reference)
   C19 Candidate Feedback      ← C17 Decision, C15 Explanation (candidate view)
   C20 Talent Pool/Afterlife   ← C18 Rejection Handling, C24 Consent

LEARNING (compounding):
   C21 Outcome Capture         ← C18 Offer Handling (a hire exists), C24 Consent
   C22 Outcome Learning        ← C21 Outcome Capture, C11 historical evaluations
   C7  Hiring Memory Update    ← C22 Outcome Learning  (loop back to C6/C11)
   C14 Benchmark (update)      ← C22 Outcome Learning
```

- **The critical dependency (the gate):** **C16 Recommendation cannot be delivered unless C13 Fairness Check passes** — the fairness gate is a hard dependency, not a parallel check (INV-3).
- **The loop:** C22 Outcome Learning feeds C7 Hiring Memory, which feeds C6 Calibration and C11 Evaluation — the compounding loop (INV-12), the moat.

---

## 5. Capability Interaction Matrix

*The **Consumers** attribute: which capabilities/services *consume* the output of which producers. (Read: row **produces for** column-group.)*

| Producer ↓ / Consumer → | Evidence Svc | Evaluation Svc | Explainability Svc | Decision Svc | Candidate Exp Svc | Outcome & Learning | Benchmarking | Trust/Compliance |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Intake & Integration | ● (applications) | | | ● (offer/reject ref) | ● (status) | ● (outcome ref) | | ● (consent) |
| Calibration & Memory | | ● (context) | | | | ● (updates) | ● (norms) | |
| Evidence Svc | | ● (evidence) | ● (evidence cited) | | | ● (evidence↔outcome) | ● (evidence) | ● (integrity) |
| Evaluation Svc | | | ● (what to explain) | ● (recommendation) | ● (feedback basis) | ● (evaluation↔outcome) | ● (scores) | ● (fairness input) |
| Explainability Svc | | | | ● (explanation) | ● (candidate feedback) | | | ● (audit detail) |
| Decision Svc | | | | | ● (offer/reject) | ● (decision→outcome) | | ● (audit) |
| Outcome & Learning | | ● (improves) | | | | | ● (updates) | |
| Benchmarking | | ● (context) | ● (percentile) | ● (context) | | | | |
| Trust/Compliance | ● gates | ● gates | ● gates | ● gates | ● gates | ● gates | ● gates | — |

- **The read:** the **Trust/Compliance Service gates *every* other service** (bottom row) — fairness, consent, integrity, audit, and isolation touch everything. And the **Outcome & Learning Service feeds back into Evaluation, Calibration/Memory, and Benchmarking** — the compounding interactions that are the moat.

---

## 6. Domain-to-Capability Matrix

*Ownership (●) and significant contribution (○) by Domain. Confirms each capability has exactly one accountable owner (no orphans, no conflicts) — the governance point of DOC-04/DOC-08.*

| Domain \ Capability group | Intake | Calibration & Memory | Evidence | Evaluation | Benchmark | Explainability | Decision | Candidate Exp | Outcome/Learning | Trust/Compliance |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **Candidate** | ○ | | | | | | | ● | | ○ |
| **Company / Work** | ● | | | | | | ○ | | | |
| **Evidence** | | | ● | ○ | | | | | ○ | |
| **Evaluation** | | ○ | | ● | ○ | | | | ○ | |
| **Intelligence (Calib. & Memory)** | | ● | ○ | ○ | ○ | | | | ○ | |
| **Benchmark** | | | | | ● | | | | | |
| **Hiring** | ○ | | | | | | ● | | | |
| **Outcome & Learning** | | | | | | | | | ● | |
| **Trust / Fairness / Compliance** | | | ○ (integrity) | ○ (fairness) | ○ (isolation) | ● | | | | ● |
| **Commercial** | (billing per Candidate Evaluation — governs C16 unit, KD-03.10) | | | | | | | | | |

- **Governance guarantee:** every capability has **one** owning Domain (the ● in its column) — so any proposed change has a single accountable approver, preventing the "everyone argues" failure (DOC-04 A-04.2, DOC-08).

---

## 7. Capability Maturity Roadmap

*How capabilities mature across the DOC-01 horizons. What changes is **maturity**, not existence — and the effort concentrates on the compounding capabilities.*

| Capability (group) | Horizon 1 (prove the layer) | Horizon 2 (embed) | Horizon 3 (network/standard) |
|---|---|---|---|
| Intake & Integration (C1–C5) | L1→L2 | L2 | L2 (stable; done well, not deepened) |
| Role Calibration (C6) | L1→L2 | L3 | L3 |
| **Hiring Memory (C7)** | **L1** | **L3** | **L4** |
| Evidence Collection (C8) | L1→L2 | L3 | L3 |
| Integrity Verification (C9) | L1→L2 | L3 | L3 |
| **Evidence Graph (C10)** | **L2** | **L3** | **L4** |
| Evaluation (C11–C12, C16) | L1→L2 | L3 | L3→L4 |
| **Fairness Check (C13)** | **L2** | **L3** | **L4** |
| **Benchmarking (C14)** | **L1** (thin) | **L3** | **L4** |
| Explanation (C15) | L1→L2 | L3 | L3 |
| Decision Support (C17–C18) | L1→L2 | L2 | L2 |
| Candidate Feedback / Afterlife (C19–C20) | L1 | L2→L3 | L3 |
| Outcome Capture (C21) | L1 | L2→L3 | L3 |
| **Outcome Learning (C22)** | **L1** | **L2→L3** | **L4** |
| Audit / Consent / Isolation (C23–C25) | L2→L3 | L3 | L3→L4 |

- **The strategic read:** the **bolded compounding capabilities** (Hiring Memory, Evidence Graph, Fairness, Benchmarking, Outcome Learning) are the ones we push to **L4** — they *are* the moat (DOC-03 §13, DOC-09 A-4). Transactional/enabling capabilities plateau at L2–L3 by design (don't over-build, DOC-10 A-10.2). **Horizon 1 deliberately ships the compounding capabilities *immature* (L1–L2)** — the point of Horizon 1 is to *start the flywheel*, not to perfect the moat.

---

## 8. Architecture-Independence Statement (the quality bar)

This document is deliberately silent on *how* these capabilities are realized. The same Capability Map holds if the eventual architecture (DOC-17) is a **monolith**, **microservices**, **serverless**, an **actor model**, or anything else. Nothing here names a system, service, datastore, protocol, queue, model, or agent. DOC-17's job is to answer *"what logical components must exist to realize these capabilities?"* — and it can answer that many different ways without any change to DOC-12.

> **Self-test applied:** re-reading §1–§7, no cell names a technology or component. If a future edit introduces one, it has broken the abstraction and belongs in DOC-17, not here.

---

## 9. Summary

### 9.1 What this establishes
- A **technology-free business capability model**: 25 capabilities grouped into 10 Business Services, owned by Domains.
- A **Capability Register** with all twelve required attributes per capability (ten in-table; Consumers/Dependencies in §5/§4).
- Four artifacts: **Dependency Map** (§4), **Interaction Matrix** (§5), **Domain-to-Capability Matrix** (§6), **Maturity Roadmap** (§7).
- An explicit **architecture-independence** guarantee (§8).

### 9.2 Key decisions recorded
- **KD-12.1** — The Capability Map stops at **Capability → Business Service**; all technology/architecture is deferred to DOC-17.
- **KD-12.2** — Every capability has **one owning Domain** (§6), a Criticality, a Maturity path, a Lifecycle, an Advisory/Authoritative class, the Gates it enforces, and the JTBD/Personas it serves.
- **KD-12.3** — **Authoritative capabilities = the gates, all in the Trust/Fairness/Compliance Service** (the "architecture of trust").
- **KD-12.4** — **Compounding capabilities (Hiring Memory, Evidence Graph, Fairness, Benchmarking, Outcome Learning) are pushed to L4**; enabling/transactional capabilities plateau by design.
- **KD-12.5** — The **fairness check is a hard dependency** of recommendation delivery (§4), not a parallel warning (INV-3).
- **KD-12.6** — The map is **architecture-independent and intended to be stable for years** (§8).
- **KD-12.7 — PRODUCT BOUNDARY (permanent, constitutional-grade).** *One of the most important decisions in the entire product.*
  - **We are NOT responsible for:** Job creation · Job posting · Candidate sourcing · Resume database · Applicant Tracking · Offer management · HR records. **Those remain the customer's Systems of Record** (reinforces P4; DOC-05 Non-Goals).
  - **Our responsibility BEGINS when:** a candidate has **already applied** (in the customer's systems) and their record is **imported/synchronized** to us.
  - **Our responsibility ENDS when:** **hiring intelligence has been delivered back** to the customer.
  - **Consequence:** capability **C2 is Candidate *Import*, not application acceptance**; the Service Blueprint starts at *sync → Evaluation Campaign* (DOC-10 §0), and the candidate journey starts at *Evaluation Invitation* (DOC-11 J-1). Anything that would make us own a System of Record is out of scope by definition.

### 9.3 Open questions (mostly for Architecture / later)
1. **Business Service boundaries:** are these ten the right *business* groupings, or should (e.g.) Explainability fold into Evaluation? *(A business-architecture question, not a code one; revisit if validation reshapes the jobs.)*
2. **Sensor-agnosticism in C8:** confirmed we keep "Evidence Request & Collection" sensor-agnostic here; specific sensors are Functional Requirements (DOC-13).
3. **Commercial capabilities:** billing/subscription capabilities are noted but not detailed (Commercial domain, generic); expand in a pricing/packaging doc, not here.

### 9.4 Next: **VALIDATION MODE** (not DOC-13)

> **Per CTO direction, documentation now pauses.** We do **not** proceed to Functional Requirements. The strategic + product + capability foundation (DOC-01–12) is complete enough to *test*. The biggest risk is no longer documentation quality — it is **whether real customers behave the way these documents predict** (chiefly **AS-1: evidence beats resumes**, and the JTBD/journey hypotheses).

**The Validation Program (the new phase) will produce:**
1. **Assumption Register** — every load-bearing assumption across DOC-01–12 (AS-1…AS-10, TTTM targets, "I had a fair chance," Rina's days-to-trust, etc.), each with a test and a kill/confirm criterion. *(Recommended first — it's the keystone the rest test.)*
2. **Risk Register** — strategic/product/adoption risks with likelihood, impact, and early-warning signals.
3. **Design Partner Interview Guide** — how we run the 20–30 partner conversations.
4. **Discovery Questions** — the specific questions that surface problems (not solutions).
5. **JTBD Validation Checklist** — does each Job (and Negative JTBD) hold with real people?
6. **Customer Journey Validation Script** — walk partners/candidates through DOC-11 and test the emotional arcs, Moments That Matter, and Trust/Success Moments.
7. **Prototype Validation Plan** — the lightest artifact that tests AS-1 without full build.
8. **Evidence Collection Framework** — how we capture, structure, and weigh what we learn (so validation itself is evidence-based — consistent with our own thesis).

**Revised roadmap:** DOC-01–11 ✅ · **DOC-12 Capability Map** ✅ · **→ Validation Program (new phase)** · then Functional Requirements · AI Strategy · Evaluation Engine · NFRs · Architecture · Engineering Principles.

---

*End of DOC-12 v0.1 — business layer only, architecture-independent. This closes the strategic-and-product foundation. The next phase is validation, not more design.*
