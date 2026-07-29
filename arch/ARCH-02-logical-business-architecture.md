# ARCH-02 — Logical Business Architecture

| Field | Value |
|---|---|
| **Document ID** | ARCH-02 |
| **Title** | Logical Business Architecture |
| **Owner** | Principal Software Architect |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture |
| **Depends on** | ARCH-01 (Context + boundaries + Campaign-as-Unit-of-Work), PRODUCT-01 (MVP), DOC-12 (Capabilities), DOC-05 (gates), DOC-04 (vocabulary) |
| **Blocks** | ARCH-03 (Domain Model / DDD) and all downstream |
| **The one question** | **"What logical business responsibilities must exist to realize the platform?"** — organized around the **Evaluation Campaign as the Unit of Work** (AD-09). |
| **ABSOLUTELY FORBIDDEN** | Microservices · REST/APIs · Events · Databases · Queues · Frameworks · Programming languages · Deployment · Cloud · Containers · Any technology name. **This is business architecture only.** |

---

## Locked prerequisite decisions *(extend the ARCH decision log)*

- **AD-10 — MVP Sensor = Structured Work Sample.** Text-first. Evaluates *engineering work* (not interview performance). Produces evidence across multiple dimensions — **technical quality, reasoning, debugging, communication, engineering maturity.** Voice, adaptive interviews, pair-programming, and live AI interviews are **deferred beyond MVP.** *(Resolves PRODUCT-01 OQ-1.)*
- **AD-11 — First Intake = CSV Import + Resume Upload.** ATS integration is a **later optimization**. **The logical architecture MUST NOT assume an ATS integration exists.** *(Resolves PRODUCT-01 OQ-2; supersedes any implied ATS dependency in the Blueprint for MVP.)*

> Consequence for this document: the intake responsibility is **file-based (CSV + resume), not ATS-coupled**; the evidence responsibility centers on the **Work Sample**; and "deliver back" is an **export**, not necessarily an ATS write-back, at MVP.

---

## 1. Architecture Philosophy

**This architecture is organized around business responsibilities, not technical layers — and specifically around the Evaluation Campaign as the Unit of Work.**

Traditional architectures organize by technical tier (presentation / logic / data). We reject that as the *primary* organizing principle because:

- **Our value is business meaning, not technical mechanism.** The moat is Evidence, Evaluation, Calibration, Outcome Learning (DOC-03) — *business* capabilities. Organizing by business responsibility keeps the architecture aligned to the mission and the Constitution's gates, rather than to a technology fashion that will change.
- **Business responsibilities are stable for years; technical layers are not** (DOC-07 half-life logic). A logical architecture built from business responsibilities survives re-platforming; one built from a technical stack does not.
- **The gates are business responsibilities.** Fairness, explainability, consent, audit, isolation, human accountability — these are *responsibilities that must be owned*, not layers. Organizing by responsibility makes each gate an explicit owner, not an afterthought bolted onto a tier.
- **The Evaluation Campaign gives us a natural business boundary** (AD-09) around which responsibilities cohere: scope, lifecycle, fairness, audit, reporting, export all attach to it.

> **The rule:** every logical component in this document is a *business responsibility with a clear owner*, and each traces to a DOC-12 capability, a PRODUCT-01 flow/rule, and an ARCH-01 boundary (§10). If a component can't be traced, it doesn't belong.

---

## 2. Business Capability Map — Logical Domains

Eight logical business domains group all capabilities. *(Logical owners, not people or technology.)*

| Domain | Purpose | Key Responsibilities | Inputs | Outputs | Logical Owner | Depends on |
|---|---|---|---|---|---|---|
| **D1 · Organization & Access** | Establish who the customer is and who may act. | Org setup; users & roles; tenant scope; consent configuration. | Admin configuration; user identity. | Authorized, tenant-scoped context. | Organization Management | Trust & Fairness (isolation, consent) |
| **D2 · Candidate** | Bring candidates in and serve them as first-class users. | Candidate identity; **file-based intake (CSV + resume, AD-11)**; candidate communication/status; feedback delivery. | CSV/resume uploads; evaluation results; recruiter release. | Candidate records; invitations; feedback. | Candidate Identity + Candidate Intake + Feedback | Campaign; Consent; Engagement |
| **D3 · Campaign** *(the Unit of Work)* | Organize **all** evaluation activity. | Campaign lifecycle; scope; **thin calibration** of the bar; boundary of fairness/audit/reporting/export. | Role reference; imported candidates; calibration. | Campaign scope & lifecycle state; delivery boundary. | Evaluation Campaign | Candidate; Evidence; Evaluation Intelligence; Trust |
| **D4 · Evidence** | Produce and structure genuine evidence of ability. | **Work Sample administration (AD-10)**; evidence collection; integrity verification; structuring. | Candidate work-sample responses. | Structured, integrity-checked Evidence. | Evidence Collection + Work Sample Engine + Integrity Engine | Campaign; Consent |
| **D5 · Evaluation Intelligence** | Turn evidence into explainable, confidence-qualified judgment. | Evaluation; confidence; recommendation; explanation. *(Benchmarking, Hiring Memory deferred.)* | Structured Evidence + Calibration. | Evaluation Score; Confidence; Recommendation; Explanation. | Evaluation Engine (+ Confidence, Recommendation, Explanation Engines) | Evidence; Calibration; **Fairness (gate)**; Trust |
| **D6 · Trust, Fairness & Compliance** | Enforce the gates (the authoritative ground). | Fairness/adverse-impact checking; consent; audit; tenant isolation. | Evaluations; every material action. | Fairness verdict (gate); audit trail; isolation; consent state. | Fairness Engine + Audit + Consent + Tenant Isolation | (Depended-on by all; depends on none) |
| **D7 · Decision & Delivery** | Support the human decision; deliver intelligence back. | Decision support & capture; feedback release; **export (not ATS-write at MVP, AD-11)**. | Recommendations; human decisions. | Recorded decisions; released feedback; exported results. | Decision Support + Feedback Engine + Export/Delivery | Evaluation Intelligence; Candidate; Campaign; Trust |
| **D8 · Engagement** | Communicate at the right moments (Waiting & Silence, DOC-06). | Invitations; notifications. | Campaign lifecycle signals. | Invitations; notifications. | Notification | Candidate; Campaign |

---

## 3. Logical Responsibility Model

*Each: Purpose · Responsibilities · Consumes · Produces · Business invariants · Interactions. Components are business responsibilities, not services.*

**Organization Management** — *Purpose:* establish the customer tenant and its users/roles. *Responsibilities:* org & user/role setup; consent configuration; hold the tenant scope. *Consumes:* admin configuration, authenticated identity. *Produces:* authorized, tenant-scoped context. *Invariants:* every action occurs within exactly one tenant; roles gate authority. *Interactions:* provides tenant/role context to all domains; relies on Tenant Isolation & Consent.

**Candidate Identity** — *Purpose:* represent a candidate as a durable participant. *Responsibilities:* uniquely identify a candidate within a tenant; link a candidate to the campaigns they participate in. *Consumes:* imported candidate records. *Produces:* candidate identity referenced by campaigns/evidence. *Invariants:* a candidate belongs to a tenant; a candidate may join many campaigns but has one active evaluation per campaign (AD-09). *Interactions:* referenced by Campaign, Evidence, Feedback.

**Candidate Intake** — *Purpose:* bring already-applied candidates in **via CSV + resume upload (AD-11)**. *Responsibilities:* accept file imports; create candidate records; **never** accept a job application (KD-12.7). *Consumes:* CSV files, resume files, role reference. *Produces:* imported candidates tied to a Role/campaign. *Invariants:* intake is file-based, not ATS-coupled; imported candidates already applied elsewhere; consent captured before evaluation. *Interactions:* feeds Campaign; governed by Consent.

**Evaluation Campaign** *(Unit of Work)* — *Purpose:* organize all evaluation activity for one Role. *Responsibilities:* own campaign lifecycle (create → active → concluded/cancelled); define scope (role, candidates, calibration); be the boundary of fairness/audit/reporting/export. *Consumes:* imported candidates, calibration, role reference. *Produces:* campaign scope & lifecycle; the delivery boundary. *Invariants:* every evaluation activity belongs to exactly one campaign; one tenant only; begins after import, ends after delivery/cancel; historical campaign evidence is immutable (AD-09). *Interactions:* the hub — coordinates Candidate, Evidence, Evaluation Intelligence, Decision & Delivery; observed by Trust.

**Calibration** — *Purpose:* capture how this company/manager defines "good" for the Role (thin, at MVP). *Responsibilities:* elicit and hold the role bar/priorities. *Consumes:* recruiter/HM input. *Produces:* calibration context for evaluation. *Invariants:* calibration adjusts the *bar*, never the *gates* (bias never — P1; Customization Pyramid). *Interactions:* consumed by Evaluation Engine; belongs to a campaign.

**Invitation & Notification** — *Purpose:* invite candidates and communicate status honestly. *Responsibilities:* issue evaluation invitations; send status/notifications at meaningful moments only. *Consumes:* campaign lifecycle signals. *Produces:* invitations, notifications. *Invariants:* honest AI disclosure at invitation (A1); communicate at meaningful events, silent otherwise (A8/A9); never a black hole. *Interactions:* triggered by Campaign; addresses Candidate.

**Evidence Collection** — *Purpose:* gather and structure evidence of ability. *Responsibilities:* administer the evidence-gathering; structure responses into evidence. *Consumes:* candidate work-sample responses. *Produces:* structured evidence. *Invariants:* evidence is role-relevant; evidence belongs to a campaign; consent required first. *Interactions:* receives from Work Sample Engine; passes to Integrity then Evaluation.

**Work Sample Engine** *(the MVP Sensor — AD-10)* — *Purpose:* administer the **structured, text-first work sample** and elicit multi-dimensional engineering evidence. *Responsibilities:* present the work-sample task; capture the candidate's work and reasoning across dimensions (technical quality, reasoning, debugging, communication, engineering maturity). *Consumes:* the campaign's task/role. *Produces:* raw candidate work → evidence input. *Invariants:* text-first; evaluates *work*, not interview performance; a candidate completes it once per campaign unless restarted (AD-09/PRODUCT-01 rule 1). *Interactions:* feeds Evidence Collection.

**Integrity Engine** — *Purpose:* judge the **authenticity** of evidence (anti-fraud/impersonation/AI-misuse). *Responsibilities:* assess whether the work is genuinely the candidate's; produce an Integrity Score. *Consumes:* evidence + signals. *Produces:* Integrity Score attached to evidence. *Invariants:* **authoritative** — integrity cannot be overridden (DOC-12); low integrity flags, never silently passes. *Interactions:* gates evidence quality before Evaluation trusts it.

**Evaluation Engine** — *Purpose:* turn integrity-checked evidence into judgment, contextualized by calibration. *Responsibilities:* evaluate evidence against the Role bar; produce an Evaluation Score with cited evidence. *Consumes:* structured evidence + calibration. *Produces:* evaluation (evidence-cited) + Evaluation Score. *Invariants:* every evaluation is contextualized (INV-5); no evaluation without integrity-checked evidence; every evaluation carries confidence (INV-6). *Interactions:* consumes Evidence; invokes Confidence; **submits to Fairness (gate)**; feeds Recommendation.

**Confidence Engine** — *Purpose:* express honest certainty. *Responsibilities:* determine and attach confidence to evaluations/recommendations. *Consumes:* evidence sufficiency/quality. *Produces:* confidence level. *Invariants:* confidence always attached; low confidence surfaced honestly, never hidden (INV-6). *Interactions:* attaches to Evaluation & Recommendation.

**Fairness Engine** *(authoritative gate)* — *Purpose:* ensure no unjustified disparate impact. *Responsibilities:* assess fairness/adverse-impact within the campaign; **approve or hold** recommendations. *Consumes:* evaluations across the campaign's candidate set. *Produces:* a fairness verdict (pass/hold). *Invariants:* **authoritative — cannot be bypassed or overridden**; **a recommendation cannot be delivered unless fairness passes** (INV-3; PRODUCT-01 rule 3). *Interactions:* the mandatory gate between Evaluation and Recommendation delivery.

**Recommendation Engine** — *Purpose:* prepare the suggested course of action (advisory). *Responsibilities:* assemble the evidence-first recommendation; rank/shortlist. *Consumes:* evaluations (fairness-passed) + confidence + benchmark (deferred). *Produces:* Recommendation (advisory, human-owned). *Invariants:* advisory only (P2); requires fairness pass; requires explanation before delivery (no bare score — INV-2). *Interactions:* consumes Evaluation+Fairness; requires Explanation; feeds Decision Support.

**Explanation Engine** *(authoritative requirement)* — *Purpose:* produce audience-appropriate explanations (Progressive Explainability, P13). *Responsibilities:* generate the evidence-and-reasoning behind every output, per audience (candidate/recruiter/HM/exec/audit). *Consumes:* evaluation + evidence + recommendation. *Produces:* audience-specific explanations. *Invariants:* nothing ships unexplained (INV-2); candidates never see internal mechanics (P13). *Interactions:* pervades every delivered output (recommendation, feedback).

**Decision Support** — *Purpose:* support and capture the **human** decision. *Responsibilities:* present finalists + evidence to the human; capture the advance/hold/reject decision and any override. *Consumes:* recommendations + explanations. *Produces:* a recorded human decision. *Invariants:* **the system never auto-decides high-risk** (P2); the human is accountable; overrides are captured. *Interactions:* consumes Recommendation; feeds Feedback & Export.

**Feedback Engine** — *Purpose:* deliver constructive candidate feedback (esp. rejection). *Responsibilities:* generate candidate-appropriate feedback; deliver **only after recruiter release**. *Consumes:* evaluation + explanation (candidate view). *Produces:* released candidate feedback. *Invariants:* **feedback delivered only after recruiter release** (PRODUCT-01 rule 4); framed "not the strongest match," never "not good enough" (DOC-06 §10); candidate view only (P13). *Interactions:* consumes Explanation; addresses Candidate; triggered by Decision/release.

**Export / Delivery** — *Purpose:* deliver hiring intelligence back to the customer (boundary end — KD-12.7). *Responsibilities:* package and hand back recommendations/decisions. *Consumes:* decisions + recommendations. *Produces:* exported results (file/export at MVP, AD-11 — not necessarily ATS write-back). *Invariants:* delivery ends our boundary; we never action the offer. *Interactions:* consumes Decision; hands to the customer's systems.

**Audit** *(cross-cutting, authoritative)* — *Purpose:* immutable, complete record of every material action. *Responsibilities:* record what happened, organized by campaign. *Consumes:* all material actions. *Produces:* append-only audit trail. *Invariants:* **append-only, complete, nothing withheld** (P8/INV-2). *Interactions:* observes every component (see §7).

**Consent** *(cross-cutting, authoritative)* — *Purpose:* govern candidate data use. *Responsibilities:* capture and enforce consent; forbid sale/misuse. *Consumes:* candidate consent, data-use requests. *Produces:* consent state that gates data use. *Invariants:* no evaluation without consent; data never sold (P3/KD-03.14). *Interactions:* gates Intake, Evidence, LLM-bound data (see §7).

**Tenant Isolation** *(cross-cutting, authoritative)* — *Purpose:* guarantee one company's data never reaches another. *Responsibilities:* enforce tenant boundaries on every access. *Consumes:* every access request. *Produces:* isolation enforcement. *Invariants:* **cross-tenant access impossible by construction** (INV-8). *Interactions:* pervades all domains (see §7).

---

## 4. Interaction Model *(ASCII — logical collaboration, organized around the Campaign)*

```
   [ D1 Organization & Access ] ── authorized, tenant-scoped context ──▶ (all domains)

                         ┌──────────────────────────────────────────────────────┐
   CSV + Resume ──▶ Candidate Intake ──▶ Candidate Identity                       │
   (AD-11)              │                        │                                │
                        ▼                        ▼                                │
                 ┌────────────────  EVALUATION CAMPAIGN (Unit of Work)  ─────────┐│
                 │   Calibration ──┐                                             ││
                 │                 ▼                                             ││
                 │   Invitation ─▶ Work Sample Engine ─▶ Evidence Collection      ││
                 │       (AD-10)              │                 │                ││
                 │                            ▼                 ▼                ││
                 │                     Integrity Engine ─▶ Evaluation Engine      ││
                 │                                                │  ▲            ││
                 │                                    Confidence ─┤  │ calibration││
                 │                                                ▼  │            ││
                 │                                    ┌── FAIRNESS ENGINE (GATE) ─┤│  ◀ pass required
                 │                                    │        │ pass             ││
                 │                                    │        ▼                  ││
                 │                          Explanation ◀─▶ Recommendation Engine ││
                 │                                             │                  ││
                 │                                             ▼                  ││
                 │                                     Decision Support (human)   ││  ◀ P2: human decides
                 │                                        │             │         ││
                 │                             Feedback Engine     Export/Delivery ││  ◀ boundary end
                 │                             (after release)      (to customer)  ││
                 └──────────────────────────────────────────────────────────────┘│
                         └──────────────────────────────────────────────────────┘
        ═══ pervasive ground (observe/gate EVERY step) ═══
        [ Audit ]  [ Consent ]  [ Tenant Isolation ]  ── and Fairness/Confidence/Explanation as cross-cutting (see §7)
        [ D8 Engagement/Notification ] communicates at meaningful campaign moments only
```

---

## 5. Responsibility Matrix *(one primary owner per DOC-12 capability — no overlaps)*

| DOC-12 Capability | Primary Logical Owner | MVP? |
|---|---|---|
| C1 Requisition reference | Evaluation Campaign *(role ref; ATS sync deferred — AD-11)* | ref only |
| C2 Candidate Intake (Import) | **Candidate Intake** (CSV + resume) | ✅ |
| C3 Integrations | Candidate Intake *(file-based; ATS deferred — AD-11)* | file only |
| C4 Candidate Communication & Status | Invitation & Notification (+ Candidate) | ✅ |
| C5 Notification | Invitation & Notification | ✅ |
| C6 Role Calibration | **Calibration** | ✅ (thin) |
| C7 Hiring Memory | Evaluation Intelligence *(deferred)* | ❌ |
| C8 Evidence Request & Collection | **Evidence Collection** | ✅ |
| C9 Integrity Verification | **Integrity Engine** | ✅ |
| C10 Evidence Structuring | Evidence Collection | ✅ |
| C11 Evaluation Orchestration | **Evaluation Engine** | ✅ |
| C12 Confidence | **Confidence Engine** | ✅ |
| C13 Fairness / Adverse-Impact | **Fairness Engine** | ✅ |
| C14 Benchmarking | Evaluation Intelligence *(deferred)* | ❌ |
| C15 Explanation | **Explanation Engine** | ✅ |
| C16 Recommendation | **Recommendation Engine** | ✅ |
| C17 Human-Decision Support | **Decision Support** | ✅ |
| C18 Offer/Rejection Handling → Export | **Export / Delivery** | ✅ (export) |
| C19 Candidate Feedback | **Feedback Engine** | ✅ |
| C20 Talent Pool / Afterlife | Candidate *(deferred)* | ❌ |
| C21 Outcome Capture | Outcome & Learning *(deferred; via HRIS)* | ❌ |
| C22 Outcome Learning | Outcome & Learning *(deferred)* | ❌ |
| C23 Audit | **Audit** | ✅ |
| C24 Consent & Privacy | **Consent** | ✅ |
| C25 Tenant Isolation | **Tenant Isolation** | ✅ |

> Every capability has **exactly one** primary owner. No overlaps, no ambiguity (the DOC-04/DOC-08 governance guarantee, now at the component level).

---

## 6. Business Boundaries

**May communicate directly (bounded flows):**
- Candidate Intake → Campaign; Campaign → (Calibration, Invitation, Evidence, Evaluation, Decision, Export).
- Work Sample Engine → Evidence Collection → Integrity → Evaluation → Confidence → Fairness → Recommendation → Explanation → Decision Support → (Feedback, Export).

**Must never communicate directly (forbidden):**
- **Candidate Intake ✗→ Evaluation Engine** — evidence must flow through the Campaign and Evidence/Integrity path; you cannot evaluate a raw import.
- **Recommendation Engine ✗→ Candidate** — candidates never receive recommendations directly; only *released, candidate-view feedback* via Feedback Engine.
- **Any component ✗→ a component in another tenant** — cross-tenant communication is impossible (Tenant Isolation).
- **Decision Support ✗→ auto-finalize** — it cannot conclude a high-risk decision without the human (P2).
- **Work Sample / Evidence ✗→ external model with un-minimized PII** — the LLM boundary (ARCH-01 §6) requires PII minimization (governed in ARCH-06/08).

**Interactions that REQUIRE an authoritative gate:**
- **Evaluation → Recommendation delivery** requires **Fairness pass** (Fairness Engine gate; INV-3). *Hard dependency.*
- **Any output → delivery** requires **Explanation attached** (Explanation Engine; no bare score, INV-2).
- **Intake/Evidence → use of candidate data** requires **Consent** (Consent gate; P3).
- **Feedback → candidate** requires **recruiter release** (PRODUCT-01 rule 4).
- **Every material action** requires **Audit** (append-only; P8).

---

## 7. Cross-Cutting Responsibilities *(aspects that flow through — not services)*

These are **not** components you call; they are responsibilities that **pervade** the logical architecture and attach at defined points:

- **Audit** — flows *under every action*: every component's material action is recorded, organized by campaign. It is an omnipresent obligation, not a step in the flow. *Nothing material happens outside audit.*
- **Consent** — flows *ahead of every candidate-data use*: intake, evidence, and any outward data movement must first satisfy consent. It gates, it doesn't sequence.
- **Fairness** — flows as a **mandatory gate** between evaluation and recommendation-delivery; it is *both* an identifiable engine (§3) *and* a pervasive rule that no delivered judgment escapes.
- **Tenant Isolation** — flows *around every access*: every read/write/interaction is tenant-scoped by construction; it is the invisible wall around every domain.
- **Confidence** — flows *with every judgment*: every evaluation and recommendation carries its confidence; it is an attribute that travels, not a stage.
- **Explainability** — flows *with every delivered output*: every recommendation and feedback carries its audience-appropriate evidence-and-reasoning; unexplained outputs cannot exist.

> **How to think about them:** the *flow* (§4) moves work forward (intake → evidence → evaluation → recommendation → decision → delivery); the *cross-cutting responsibilities* are the **rules and records that pervade that flow** — they don't advance the work, they *govern* it. In DOC-12 terms, these are the **authoritative** capabilities, and their pervasiveness is exactly why they can't be bypassed.

---

## 8. Logical Dependency Graph *(dependencies point toward business ownership, never infrastructure)*

```
                        Trust, Fairness & Compliance (D6)
                        (Audit · Consent · Fairness · Isolation)
                                   ▲   ▲   ▲   ▲
        depends-on ────────────────┘   │   │   └──────────────── depends-on
                                        │   │
   Organization & Access (D1) ─────────▶│   │◀───────── Engagement (D8)
        ▲                               │   │
        │                     EVALUATION CAMPAIGN (D3)  ◀── the center of gravity
        │                        ▲    ▲     ▲    ▲
   Candidate (D2) ───────────────┘    │     │    └────────── Decision & Delivery (D7)
        ▲                              │     │                      ▲
        └──────── Evidence (D4) ───────┘     └── Evaluation Intelligence (D5) ──┘
                                                        ▲
                                          Evidence (D4) ┘
```

- **Everything depends toward D3 (Campaign) and D6 (Trust/Fairness/Compliance)** — the two centers: the *Unit of Work* and the *gates*. Dependencies point at **business ownership** (campaign, trust), **not** at infrastructure. D6 depends on *nothing* (it is the foundation); D3 is the hub that coordinates.
- **No dependency points "downward" to a technical layer** — because there are none here (ARCH-05 will introduce structure). Business responsibility is the only thing depended upon.

---

## 9. Architectural Constraints *(imposed on ALL future architecture)*

1. **Every evaluation belongs to exactly one Evaluation Campaign** (AD-09).
2. **Every recommendation requires Fairness approval before delivery** (INV-3; hard gate).
3. **Every candidate/material action is auditable** (append-only; P8).
4. **Historical campaign evidence is immutable** — referenced, never modified (AD-09).
5. **Human accountability cannot be bypassed** — the system never auto-finalizes a high-risk decision (P2).
6. **No output is delivered without an audience-appropriate explanation** — no bare score (INV-2; P13).
7. **No candidate data is used without consent; never sold** (P3/KD-03.14).
8. **Cross-tenant access is impossible by construction** (INV-8).
9. **Confidence accompanies every judgment** (INV-6).
10. **Intake is file-based (CSV + resume); no component may assume an ATS integration exists** (AD-11).
11. **The MVP evidence instrument is the text-first Structured Work Sample** (AD-10); components must not assume voice/adaptive/live interview.
12. **We never own a System of Record; our boundary is import → deliver-back** (KD-12.7).

---

## 10. Traceability *(nothing exists without it)*

| Logical Component | PRODUCT-01 | DOC-12 | ARCH-01 |
|---|---|---|---|
| Organization Management | S-10 Account/User Setup | C24/C25 basics | D1; tenant/trust boundary |
| Candidate Intake | S-1 Import; Flow step 1 | C2 (Candidate Import) | Import boundary begins |
| Candidate Identity | Actors: Candidate | C2 | SoR→SoI reference |
| Evaluation Campaign | S-2 Create Campaign; whole flow | Evaluation Campaign (DOC-04 A-04.4) | §1A Unit of Work / AD-09 |
| Calibration | S-2 (calibration) | C6 | SoI |
| Invitation & Notification | S-4 Invitation; Flow 3 | C4/C5 | Email boundary |
| Work Sample Engine | S-5 Evaluation; Flow 4 | C8 (sensor) | SoE / AD-10 |
| Evidence Collection | Flow 5 | C8/C10 | SoI |
| Integrity Engine | Rule (integrity) | C9 (authoritative) | Trust boundary |
| Evaluation Engine | Flow 6; S-6 | C11 | SoI |
| Confidence Engine | S-6 (confidence) | C12 | SoI |
| Fairness Engine | Rule 3; Flow 6 | C13 (authoritative) | Gate / Trust boundary |
| Recommendation Engine | S-6 dashboard | C16 | SoI |
| Explanation Engine | S-6/S-8 | C15 (authoritative) | Progressive Explainability |
| Decision Support | S-7 HM review; Rule 7 | C17 | Human-in-loop |
| Feedback Engine | S-8; Rule 4 | C19 | Candidate afterlife |
| Export / Delivery | S-9 Export; Flow 11 | C18 | Deliver-back boundary ends |
| Audit | Rule 6 | C23 (authoritative) | Audit trust boundary |
| Consent | Rule 9 | C24 (authoritative) | PII trust boundary |
| Tenant Isolation | Rule 10 | C25 (authoritative) | Tenant/data boundary |

> Every row traces to a product need, a capability, and a context boundary. No orphans.

---

## Architecture Decisions

- **AD-10** — MVP Sensor = **text-first Structured Work Sample** (multi-dimensional engineering evidence); voice/adaptive/pair/live deferred. *(Locked above.)*
- **AD-11** — First intake = **CSV + Resume upload**; **no ATS integration assumed**. *(Locked above.)*
- **AD-12** — The architecture is organized by **business responsibility around the Evaluation Campaign**, not technical layers (§1).
- **AD-13** — **Every capability has exactly one primary logical owner** (§5); no shared ownership.
- **AD-14** — **Cross-cutting responsibilities (Audit, Consent, Fairness, Tenant Isolation, Confidence, Explainability) pervade the flow as governing aspects** (§7), and are the authoritative, non-bypassable gates.
- **AD-15** — **Dependencies point toward business ownership (Campaign, Trust)**, never toward infrastructure (§8).

## Open Questions

1. **Calibration ownership vs. Evaluation:** is Calibration its own logical component or a responsibility of the Campaign? *(This doc treats it as a distinct component within D3; confirm in ARCH-03.)*
2. **Where the LLM-bound PII minimization responsibility logically lives** — a responsibility of Evidence/Evaluation, or a distinct cross-cutting "data-minimization" aspect? *(Resolve in ARCH-06/08.)*
3. **Export granularity at MVP** — file export vs. structured hand-back, given no ATS assumption (AD-11). *(ARCH-09.)*
4. **Integrity vs. Fairness sequencing** at the evidence/evaluation boundary — both authoritative; confirm order in ARCH-03/04.

## Risks

- **Over-decomposition risk:** naming many logical components could tempt premature microservice-thinking later — ARCH-05 must decide *physical* structure independently; logical ≠ physical.
- **Cross-cutting leakage:** if Audit/Consent/Fairness are treated as optional steps rather than pervasive aspects, gates get bypassed (RK-15/RK-6). §7 + §9 constrain against this.
- **Campaign as bottleneck (conceptual):** centering everything on the Campaign is correct for coherence but must not become a single point of coupling in the physical design (a note for ARCH-05).
- **AD-11 drift:** teams may assume an ATS integration; constraint §9.10 explicitly forbids it for MVP.

## Intentionally Deferred to ARCH-03 and later

- **Entities, Aggregates, Value Objects, State Machines, Invariants as a model** → **ARCH-03 (Domain Model / DDD).**
- **Events / event model** → **ARCH-04 (Event Model).**
- **Services / modules / physical structure** → **ARCH-05 (Physical Architecture).**
- **Databases, APIs, AI orchestration mechanics, deployment, observability, standards** → later ARCH docs.
- Benchmarking, Hiring Memory, Outcome Learning, Talent Pool/Afterlife components → post-MVP (owners named, build deferred).

---

## Revised ARCH sequence *(per CTO)*

> ARCH-01 Context ✅ · **ARCH-02 Logical Business Architecture** ✅ · **ARCH-03 Domain Model (DDD)** — entities, aggregates, value objects, state machines, invariants · **ARCH-04 Event Model** · **ARCH-05 Physical Architecture** (services/modules) · then Database · AI Orchestration · Evaluation Engine · Security & Trust · API Contracts · Deployment · Observability · Engineering Standards → SPRINT-0 → CODE.
> *(Rationale: business concepts → domain model → events → physical structure is a cleaner progression than jumping to the database.)*

*End of ARCH-02 v0.1 — logical business architecture, zero technology. Next: ARCH-03 — Domain Model (DDD), giving the Evaluation Campaign and its collaborators formal entities, aggregates, value objects, state machines, and invariants.*
