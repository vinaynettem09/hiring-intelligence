# Document 10 — Service Blueprint

| Field | Value |
|---|---|
| **Document ID** | DOC-10 |
| **Title** | Service Blueprint (Front-stage / Back-stage) |
| **Owner** | Principal Engineer / Technical Documentation Lead (with Product, Ops) |
| **Status** | v0.2 — **Amendment A-10.2 added: Capability Maturity, Ownership, Dependencies, and Manual Override (Advisory vs Authoritative)** |
| **Created** | 2026-07-21 |
| **Depends on** | DOC-04 (vocabulary), DOC-05 (Constitution/gates), DOC-06 (Manifesto/feelings), DOC-08 (Personas), DOC-09 (JTBD + Job Dependency Graph) |
| **Blocks** | DOC-11 (Customer Journey), the future **Capability Map**, and (much later) DOC-16 (Architecture) |
| **The one question this document answers** | **"What must happen behind the scenes so that the user experiences what we've promised?"** — nothing more. |
| **Hard scope rule (CTO-ratified)** | **NO architecture. NO technology.** No Kafka, Redis, Postgres, vector DBs, agents, queues, services, or any implementation. **Business capabilities only.** If a sentence names a technology, it does not belong in this document. Architecture comes much later (DOC-16). |
| **Vocabulary** | Uses DOC-04 frozen terms exactly. Introduces **no** new business terms. |

---

## How to read this document — what a Service Blueprint is (and isn't)

A **Customer Journey** (DOC-11, next) shows **what the customer sees** — the front-stage experience. A **Service Blueprint** (this) also shows **what happens behind the scenes** — the back-stage business capabilities that must fire so the front-stage promise comes true. It is the bridge between *the experience we promised* (Manifesto, JTBD) and *how the service delivers it* — **without** yet saying *how it's engineered.*

- **It is business capabilities, not systems.** "Evidence requested," "Evaluation orchestrated," "Audit recorded," "Hiring Memory updated" — these are *things the service must do*, described as business capabilities. *How* they're built is DOC-16.
- **It is the JTBD made operational.** Every back-stage capability exists to fulfil a Job (DOC-09) and must honor the gates (DOC-05). We annotate each with both.
- **The canonical example** (the CTO's, expanded below):
  > **Front-stage:** Candidate submits application → feels informed → receives evaluation.
  > **Back-stage:** application accepted → evidence requested → evaluation orchestrated → recommendation prepared → audit recorded → Hiring Memory updated.
  > *No implementation. Only business capabilities.*

**The blueprint layers we use** (top = most visible):
| Layer | What it captures |
|---|---|
| **① Front-stage** | What each actor *does and sees*, and the *feeling* it must produce (Manifesto). |
| — *line of interaction* — | where the user touches the service |
| **② Back-stage** | The **business capabilities** the platform performs *out of sight* to keep the front-stage promise. |
| — *line of visibility* — | separates what the user sees from what they don't (Invisible-but-honest AI, DOC-06 §7) |
| **③ Support & Compounding capabilities** | The always-on enabling capabilities the back-stage draws on — Company Calibration, Hiring Memory, Outcome Learning, Fairness checks, Compliance/Audit, Integrations, Consent/Privacy. |

For each stage we also record: **Gate honored** (DOC-05), **JTBD served** (DOC-09), and **Promise kept** (the Manifesto feeling).

---

## 0. Product Boundary *(where this blueprint starts and stops — KD-12.7)*

> **Our responsibility begins *after* a candidate has already applied in the customer's own systems, and ends when hiring intelligence has been delivered back.** We do **not** own job creation, job posting, career pages, the application portal, candidate sourcing, the resume database, applicant tracking, offer management, or HR records — those are the customer's **Systems of Record** (P4, DOC-12 KD-12.7).

So the blueprint's true first back-stage action is **not** "receive an application" — it is:
```
   (Customer's ATS receives applications)   ← OUTSIDE our boundary
                 ↓
   Applications synchronized / candidates imported   ← our boundary BEGINS here
                 ↓
   Evaluation Campaign started
                 ↓
        … (S2 → S6 below) …
                 ↓
   Hiring intelligence delivered back to the customer   ← our boundary ENDS here
```

## 1. The Master Blueprint — the Hiring Cycle spine

This is the end-to-end spine (following the Job Dependency Graph, DOC-09 A-1). Read each stage top-to-bottom: what the user sees, then what must happen behind the scenes for that to be true.

```
STAGE →      S0 Calibrate   S1 Apply        S2 Collect       S3 Evaluate      S4 Recommend     S5 Decide        S6 Outcome
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
① FRONT-     HM/Rina set    Alex applies    Alex engages     (invisible;      Rina/David see   David/Rina make  (later) Alex
   STAGE     the bar        as they always  sensors; feels   Alex sees calm   evidence-first   the decision;    is onboarded;
   (sees)    (calm setup)   do (P11); feels  focused, fairly  "in progress"    Recommendation   Alex hears back  outcome unfolds
                            informed         evaluated                         + Evidence       (with dignity)
──────────────────────────────── line of interaction ──────────────────────────────────────────────────────────────────
② BACK-      Capture the    Application     Evidence         Evaluation        Recommendation   Decision         Outcome
   STAGE     Role & bar;    accepted (any   requested;       orchestrated;     prepared;        support &        captured
   (business connect to     channel);       Evidence         Fairness check;   Explanation      capture;         (referenced);
    capabil- the ATS req    candidate        collected &      Confidence set;   generated        Offer/Rejection  Outcome
    ities)   (reference)    acknowledged     structured;      Benchmark drawn   (audience-aware) handled          Learning runs
                                             Integrity checked                                   (reference)
──────────────────────────────── line of visibility ────────────────────────────────────────────────────────────────────
③ SUPPORT &  Company        Consent &       Integrity/       Company           Progressive      Human            Outcome
   COMPOUND-  Calibration    Privacy mgmt;   authenticity     Calibration +     Explainability;  Accountability   Learning →
   ING        (starts)       Integrations    verification;    Hiring Memory;    Benchmarking     policy;          Hiring Memory
   (always-on)               (ATS/email)     Evidence Graph   Fairness engine                    Audit recording  update; Benchmarks
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   AUDIT & COMPLIANCE recording, CONSENT/PRIVACY, and TENANT ISOLATION run under EVERY stage (never off).
```

> **The reading:** the front-stage is deliberately calm and sparse (DOC-06); the back-stage is where the real work happens, invisibly (but honestly disclosed, DOC-06 A1). Audit, consent, and isolation are *always on, under everything* — they are not a stage, they are the ground.

---

## 2. Stage-by-stage detail

*For each stage: front-stage (what actors see + the promised feeling) · back-stage business capabilities · support/compounding capabilities · gate honored · JTBD served.*

### S0 — Role opened & calibrated
- **Front-stage.** The Hiring Manager (David) and Recruiter (Rina) set up the Role and its bar in a calm, guided, low-effort way. *Feeling:* "this understands how *we* hire" (First Five Minutes, DOC-06 A5).
- **Back-stage capabilities.** Connect to the customer's Requisition in the ATS (reference, never own — DOC-04); capture the Role definition; begin **Company Calibration** (the bar, values, priorities).
- **Support/compounding.** Company Calibration initialized (and enriched over time from Hiring Memory); Integrations established.
- **Gate honored.** Neutrality (works with their ATS, P5); we reference the requisition, never become the system of record (P4).
- **JTBD served.** David: *capture & apply my real bar*; Rina: *calibrate the role*. **Dependency:** everything downstream needs this first (DOC-09 A-1).

### S1 — Applications synchronized & Evaluation Campaign started *(our boundary begins)*
- **Front-stage.** The candidate **already applied in the customer's own ATS/portal** (outside our boundary — §0). From our side, the Recruiter connects the ATS (or imports candidates) and starts an **Evaluation Campaign**; each candidate then receives an **evaluation invitation** and feels *informed*: told what to expect and when (Waiting Philosophy, A8), and honestly told AI-assisted analysis is part of the process (Honest by Default, A1). *Feeling:* hope + calm, not a black hole. The candidate never has to change how they applied (P11).
- **Back-stage capabilities.** Applications **synchronized / candidates imported** from the customer's ATS; an **Evaluation Campaign** created for the Role; candidates placed into the campaign; consent captured; invitations issued.
- **Support/compounding.** Consent & Privacy management (P3); Integrations (ATS/email) so nothing changes for the customer.
- **Gate honored.** Privacy/consent (P3); candidate dignity (P7); honest disclosure (A1); we do **not** become the system of record (P4/KD-12.7).
- **JTBD served.** Alex: *get a fair chance without changing how I apply*; Rina: *evaluate imported candidates without manual overhead*.

### S2 — Evidence collected
- **Front-stage.** Alex engages the Sensors (interview/assessment) and feels *focused and fairly evaluated* — the task is clear, calm, and about *ability*, not trick questions. *Feeling:* "I'm being seen for what I can do."
- **Back-stage capabilities.** **Evidence requested** (the right sensors for this Role); **Evidence collected**; **Evidence structured** (into the Evidence Graph); **Integrity checked** (authenticity — Integrity Score).
- **Support/compounding.** Integrity/authenticity verification; the Evidence Graph accumulates (a compounding capability, DOC-09 A-4).
- **Gate honored.** Fairness (P1 — role-relevant evidence, not proxies); dignity (P7); evidence-first (DOC-06 §5).
- **JTBD served.** Alex: *show real capability*; David: *evidence of actual ability*.

### S3 — Evaluation orchestrated
- **Front-stage.** Mostly *invisible* (Invisible AI, DOC-06 §7). Alex/Rina see a calm, honest "evaluation in progress" — never a spinning "AI thinking" spectacle. *Feeling:* trust that something serious and fair is happening, without noise (Silence Philosophy, A9).
- **Back-stage capabilities.** **Evaluation orchestrated** across the collected evidence; contextualized by **Company Calibration** and **Hiring Memory**; **Confidence** determined; **Fairness / adverse-impact check** performed; **Benchmark** drawn from the network.
- **Support/compounding.** Company Calibration + Hiring Memory (compounding); Fairness engine; Benchmarking (compounding, network-scale).
- **Gate honored.** Fairness gate (P1/INV-3 — *no result proceeds without the fairness check*); contextualized evaluation (INV-5); honest Confidence (INV-6).
- **JTBD served.** All Mission-Critical evaluation jobs (Alex fair chance; David's bar; Sofia's defensibility).

### S4 — Recommendation prepared & delivered
- **Front-stage.** Rina and David receive an **evidence-first** Recommendation: Evidence → Explanation → Recommendation → Evaluation Score, with Confidence, Integrity Score, and Benchmark — at their audience-appropriate depth (Progressive Explainability). *Feeling:* Rina — "I can defend this"; David — "I understand *why*."
- **Back-stage capabilities.** **Recommendation prepared**; **Explanation generated** audience-aware (candidate/recruiter/HM/exec/audit — P13); recommendation delivered into the customer's workflow.
- **Support/compounding.** Progressive Explainability; Benchmarking; delivery via Integrations (in-workflow, P11).
- **Gate honored.** Explainability (P1/INV-2 — *nothing ships as a bare score*); Progressive Explainability (P13); evidence-first order (DOC-06 §5).
- **JTBD served.** Rina: *defensible shortlist*; David: *evidence vs. my bar*.

### S5 — Human decision
- **Front-stage.** David/Rina **make the decision** (advance / offer / reject), informed by — not dictated by — the Recommendation (P2). Alex hears the outcome **with dignity and, if rejected, useful evidence-based feedback** (P13 candidate view). *Feeling:* David — accountable and confident; Alex — "that was fair," even in a no.
- **Back-stage capabilities.** **Decision support & capture** (record the human decision and any override); **Offer or Rejection handled** (referenced to the customer's ATS); for rejection, **candidate feedback delivered** and **Talent Pool / Afterlife** placement; **Audit recorded**.
- **Support/compounding.** **Human Accountability policy** (risk-proportional oversight, DOC-05 A-05.2 §A1); Audit recording; Talent Pool/Afterlife management.
- **Gate honored.** Human Accountability (P2 — high-risk decisions get direct human review; no click-theater); dignity in rejection (P7); auditability (P8/INV-2).
- **JTBD served.** David: *own & defend the decision*; Alex: *dignity + useful outcome*; Sofia: *defensible trail*.

### S6 — Outcome recorded & learning
- **Front-stage.** (Later, and mostly invisible to daily users.) Sofia sees hiring **quality trends** over time; a hired Alex is onboarded elsewhere (Employee, reference-only). *Feeling:* Sofia — "hiring is improving and under control."
- **Back-stage capabilities.** **Outcome captured** (performance/retention — *referenced* from the customer's HRIS, never owned, DOC-04 A-04.A4); **Outcome Learning** runs; **Hiring Memory updated**; **Benchmarks updated**.
- **Support/compounding.** Outcome Learning + Hiring Memory + Benchmarking — the **compounding capabilities that are the moat** (DOC-09 A-4, DOC-03 §13). *This stage closes the loop* (INV-12).
- **Gate honored.** Privacy/isolation (P3 — one company's outcomes never leak; benchmarks aggregate-only, INV-8).
- **JTBD served.** Sofia: *know & improve quality-of-hire*; the whole system: *get smarter for the next candidate*.

---

## 3. The always-on ground (under every stage)

Three capabilities are never a "stage" — they run continuously beneath the entire blueprint:
- **Audit & Compliance recording** — every material step leaves a defensible trail (P8/P1; Sofia/Marcus). *Nothing is un-auditable.*
- **Consent & Privacy management** — candidate data governed by consent, never sold; retention respected (P3/P7/KD-03.14).
- **Tenant isolation** — one company's Calibration/Memory/Evidence never crosses to another; only aggregate Benchmarks do (P3/INV-8; Marcus's core concern).

> These are the "ground" precisely because they are the gates Marcus and Sofia veto on (DOC-08). A blueprint that treated them as optional stages would fail the security/compliance personas.

## 4. How the blueprint handles failure (business level)

Per the Error Philosophy (DOC-06 A7), failure is designed, not incidental — at the *capability* level (never technical here):
| Failure | Back-stage business response | Front-stage promise kept |
|---|---|---|
| A sensor can't complete (interview interrupted) | Preserve collected Evidence; mark the gap | Candidate reassured it won't count against them; clear resume path (no blame, no loss). |
| Evidence is incomplete | Evaluation proceeds only to *honest low Confidence*, or routes to a human | Never a confident-but-baseless result; surfaced honestly (INV-6). |
| Fairness check flags a concern | Recommendation is **held**, not delivered | We never ship an unfair result (INV-3) — the gate is a real stop, not a warning. |
| Outcome data unavailable | Learning simply doesn't run for that case | No fabricated learning; the loop waits for real data. |

> **Principle:** a failure degrades to *less confidence and more human involvement* — **never** to a wrong-but-confident or unfair result. The gates hold even when things break.

## 5. Business capabilities surfaced (seed for the future Capability Map)

The blueprint reveals the platform's **business capabilities** (not systems). This inventory is the *input* to the future **Capability Map** (which will link Capability → Business Service → System → Microservice — DOC-09 §11.3); we list them here at pure business level and go no further:

- Requisition Sync (reference to ATS) · Role Calibration Capture · Application Intake (any channel) · Candidate Communication & Status · Consent & Privacy Management · Evidence Request & Collection · Integrity/Authenticity Verification · Evidence Structuring (Evidence Graph) · Evaluation Orchestration · Fairness / Adverse-Impact Checking · Confidence Determination · Benchmarking · Explanation Generation (audience-aware) · Recommendation Preparation & Delivery · Human-Decision Support & Capture · Offer/Rejection Handling (reference) · Candidate Feedback Delivery · Talent Pool / Afterlife Management · Outcome Capture (reference) · Outcome Learning · Hiring Memory Update · Audit Recording · Tenant Isolation · Notification/Communication (governed by Waiting & Silence philosophies).

> **Discipline held:** every item above is a *business capability* (a thing the service must do), not a component. Turning these into systems is the Capability Map + Architecture, deliberately later.

---

## Amendment A-10.2 — Capability Maturity, Ownership, Dependencies & Override

*Dated 2026-07-21. CTO-ratified. Turns the flat capability inventory (§5) into a governed capability model — still business-level, still zero technology. These four annotations make capabilities plannable and un-ambiguous, and they seed the required Capability Map (DOC-12).*

### A-1 — Capability Maturity Levels

Every capability evolves; naming the levels lets us plan the journey rather than pretend a capability is "done."

| Level | Name | What it means |
|---|---|---|
| **L0** | **Manual** | A human does it entirely; the platform only records. |
| **L1** | **Assisted** | The platform helps; the human still drives. |
| **L2** | **Evidence-Driven** | The platform acts on structured Evidence, consistently and explainably. |
| **L3** | **Learning** | The capability improves from Outcomes over time. |
| **L4** | **Self-Improving** | The capability compounds across the network, improving continuously (the moat, DOC-09 A-4). |

- **Example.** **Hiring Memory** begins at **L1** (assisted, thin) and must reach **L4** (self-improving) — its whole strategic value is the climb. **Benchmarking** is only meaningful at **L3–L4** (needs network scale). By contrast, **Application Intake** is fine at **L2** forever — not everything needs to reach L4.
- **Use.** Maturity targets drive sequencing: we invest the climb-to-L4 effort in the *compounding* capabilities (Hiring Memory, Outcome Learning, Benchmarking, Evidence Graph) and leave transactional capabilities at the level that serves their Job (DOC-09 A-4; don't over-build).

### A-2 — Capability Ownership

Like DOC-04 term ownership: every capability is owned by a **Domain** (DOC-04 §3), so change has a clear approver and org confusion is prevented as we scale.

### A-3 — Capability Dependencies (the layered stack)

Capabilities are not flat; they are layered. A higher layer cannot be delivered before the layers beneath it — this is the **release-planning stack** (and mirrors the JTBD Job Dependency Graph, DOC-09 A-1).

```
   L6  LEARNING        Outcome Capture → Outcome Learning → Hiring Memory Update → Benchmark Update
                                              ▲
   L5  DECISION        Human-Decision Support & Capture → Offer/Rejection Handling · Candidate Feedback · Talent Pool
                                              ▲
   L4  OUTPUT          Explanation Generation → Recommendation Preparation & Delivery
                                              ▲
   L3  INTELLIGENCE    Evaluation Orchestration ← (Fairness Check · Confidence · Benchmarking)
                                              ▲
   L2  EVIDENCE        Evidence Request & Collection → Integrity Verification → Evidence Structuring
                                              ▲
   L1  INTAKE          Requisition Sync · Role Calibration Capture · Application Intake · Integrations
                                              ▲
   L0  GROUND (always-on)   Tenant Isolation · Consent & Privacy · Audit Recording
```

- **Use.** You cannot ship the Recommendation (L4) without Evaluation (L3), which needs Evidence (L2) and Calibration (L1), all resting on the always-on Ground (L0). This sequences MVP and every release.

### A-4 — Manual Override: Advisory vs. Authoritative

Every capability must answer: **"Can a human override this?"** The answer splits capabilities cleanly into two kinds — and the split *is* the Constitution:

- **Advisory** (human **can** override) — the platform informs; the human decides. *The human is the override* (Human Accountability, P2). e.g., Evaluation, Recommendation, Confidence, Benchmarking, Decision Support.
- **Authoritative** (human **cannot** override) — the non-negotiable gates. e.g., Fairness checking (P1), Explanation requirement (P1/P13), Integrity verification, Consent/Privacy (P3), Audit (P8), Tenant Isolation (P3).

> **The insight:** **Authoritative capabilities are exactly the Tier-0 gates** (the immutable base of the Customization Pyramid, DOC-07 §8.1). You can override an evaluation; you can *never* override fairness, consent, audit, integrity, or isolation. Advisory-vs-Authoritative is the runtime expression of "what flexes vs. what never does."

### A-5 — Consolidated Capability Register *(the seed for DOC-12 Capability Map)*

| Capability | Owner Domain | Maturity (now→target) | Advisory / **Authoritative** |
|---|---|---|---|
| Requisition Sync (ATS reference) | Work / Company | L1→L2 | Advisory |
| Role Calibration Capture | Intelligence (Calibration & Memory) | L1→L3 | Advisory |
| Application Intake (any channel) | Candidate | L1→L2 | Advisory |
| Candidate Communication & Status | Candidate | L1→L3 | Advisory |
| Consent & Privacy Management | Trust/Fairness/Compliance | L2→L3 | **Authoritative** |
| Evidence Request & Collection | Evidence | L1→L3 | Advisory |
| Integrity / Authenticity Verification | Trust/Fairness/Compliance | L1→L3 | **Authoritative** |
| Evidence Structuring (Evidence Graph) | Evidence / Intelligence | L2→L4 | Advisory |
| Evaluation Orchestration | Evaluation | L1→L3 | Advisory |
| Fairness / Adverse-Impact Checking | Trust/Fairness/Compliance | L2→L4 | **Authoritative** |
| Confidence Determination | Evaluation | L2→L3 | Advisory |
| Benchmarking | Benchmark / Intelligence | L1→L4 | Advisory |
| Explanation Generation (audience-aware) | Trust/Fairness/Compliance | L1→L3 | **Authoritative** *(requirement to explain; content is advisory)* |
| Recommendation Preparation & Delivery | Evaluation | L2→L4 | Advisory |
| Human-Decision Support & Capture | Hiring | L1→L2 | Advisory *(the human IS the override, P2)* |
| Offer / Rejection Handling (reference) | Hiring | L1→L2 | Advisory |
| Candidate Feedback Delivery | Candidate | L1→L3 | Advisory |
| Talent Pool / Afterlife Management | Candidate | L1→L3 | Advisory |
| Outcome Capture (HRIS reference) | Outcome & Learning | L1→L3 | Advisory |
| Outcome Learning | Outcome & Learning | L1→L4 | Advisory |
| Hiring Memory Update | Intelligence | L1→L4 | Advisory |
| Audit Recording | Trust/Fairness/Compliance | L2→L3 | **Authoritative** |
| Tenant Isolation | Trust/Fairness/Compliance | L3→L4 | **Authoritative** |
| Notification / Communication | Candidate / Company | L1→L2 | Advisory *(governed by Waiting & Silence, DOC-06 A8/A9)* |

> Note the pattern: **every Authoritative capability is owned by the Trust/Fairness/Compliance domain** and maps to a Tier-0 gate. That is not a coincidence — it is the architecture of trust.

---

## 6. Summary

### 6.1 What this establishes
- The **end-to-end Service Blueprint** of the hiring cycle: front-stage (what each actor sees + the promised feeling) vs. back-stage (**business capabilities**), following the JTBD Job Dependency Graph.
- Stage-by-stage mapping of **capability → gate honored → JTBD served → promise kept**, so every behind-the-scenes capability traces to a Constitution gate and a real Job.
- The **always-on ground** (Audit, Consent/Privacy, Isolation) and a **capability-level failure model** (failures degrade to less confidence / more human involvement, never to wrong-or-unfair results).
- A **business-capability inventory** as the clean input to the future Capability Map — with zero architecture.

### 6.2 Key decisions recorded
- **KD-10.1** — The Service Blueprint answers exactly one question — *what must happen behind the scenes so the promise comes true* — at **business-capability level only; no technology** (CTO-ratified scope).
- **KD-10.2** — Every back-stage capability **traces to a Constitution gate and a JTBD**; capabilities that serve neither do not belong.
- **KD-10.3** — **Audit, Consent/Privacy, and Tenant Isolation are always-on ground**, never optional stages (the security/compliance vetoes, DOC-08).
- **KD-10.4** — **Failure degrades to less confidence / more human involvement — never to a wrong-or-unfair result**; the gates hold under failure (Error Philosophy, DOC-06 A7).
- **KD-10.5** — The blueprint yields a **business-capability inventory** that seeds the (now required) Capability Map (DOC-12); we deliberately stop at capabilities, not systems.
- **KD-10.6** — Capabilities are governed by a **Capability Register** (A-10.2 §A-5): each has an **Owner Domain**, a **Maturity level** (L0 Manual → L4 Self-Improving), and an **Advisory/Authoritative** classification.
- **KD-10.7** — **Compounding capabilities climb to L4** (Hiring Memory, Outcome Learning, Benchmarking, Evidence Graph); transactional ones stay at the level their Job needs — don't over-build.
- **KD-10.8** — **Advisory vs. Authoritative = the Constitution at runtime:** Authoritative (non-overridable) capabilities are exactly the Tier-0 gates (fairness, explanation, integrity, consent, audit, isolation); everything else is Advisory, where the human is the override (P2).
- **KD-10.9** — **Capability Dependency stack** (A-10.2 §A-3): L0 Ground → L1 Intake → L2 Evidence → L3 Intelligence → L4 Output → L5 Decision → L6 Learning; sequences MVP and every release.

### 6.3 Open questions (for founder/CTO)
1. **Sensor set at V1:** which Sensors does the beachhead (SWE screening) actually require first — and does the blueprint's "Evidence Request & Collection" capability need to name them, or stay sensor-agnostic here? *(Recommend: stay sensor-agnostic in the blueprint; specify in Functional Requirements, DOC-12.)*
2. **Rejection-feedback depth at V1:** how rich is "Candidate Feedback Delivery" at launch vs. later? (Carried from DOC-06/DOC-08; a scope call for validation.)
3. **Outcome-data acquisition:** the S6 "Outcome captured (reference)" capability depends on design partners sharing HRIS performance data — the same dependency as AS-1 (DOC-02). Flag for the validation program.
4. ~~**Capability Map timing**~~ → **Resolved (CTO):** the **Capability Map is now a REQUIRED document at DOC-12**, immediately after Customer Journey — *"Architecture should implement Capabilities, not documents."*

### 6.4 Suggested next document
**DOC-11 — Customer Journey.** The blueprint showed front-stage *and* back-stage; DOC-11 zooms into the **front-stage narrative** — the actual, emotional, step-by-step journey each persona lives (especially Alex's, including rejection and afterlife), with the Trust Moments and Success Moments (DOC-09) placed on a timeline. Together, DOC-10 (behind the scenes) + DOC-11 (what they see) are exactly the pair you walk a **design partner** through — which is why finishing them readies us for validation.

**Roadmap position (revised — Capability Map now REQUIRED at 12):** …09 JTBD (frozen) · **10 Service Blueprint** · → **11 Customer Journey** · **12 Capability Map** *(required — bridges capabilities to architecture)* · 13 Functional Requirements · 14 NFRs · 15 AI Strategy · 16 Evaluation Engine · 17 Architecture · 18 Engineering Principles.

---

*End of DOC-10 v0.1 — business capabilities only, zero architecture. Awaiting founder review of the four open questions (§6.3) before promotion to Ratified.*
