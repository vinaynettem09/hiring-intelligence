# ARCH-01 — System Context

| Field | Value |
|---|---|
| **Document ID** | ARCH-01 |
| **Title** | System Context |
| **Owner** | Principal Software Architect |
| **Status** | v0.2 — added §1A "Evaluation Campaign as the Unit of Work" + diagram update |
| **Created** | 2026-07-22 |
| **Phase** | **Phase 4 — Architecture** (strategy/validation/product-definition are frozen) |
| **Depends on** | PRODUCT-01 (MVP), DOC-12 (Capabilities + **KD-12.7 Product Boundary**), DOC-05 (gates), DOC-04 (vocabulary) |
| **Blocks** | ARCH-02 (Logical Architecture) and all downstream ARCH docs |
| **Hard scope rule** | **Context only.** NO technology, frameworks, microservices, databases, APIs, protocols, or deployment. This document defines *every external system, actor, boundary, responsibility, and interaction* — and nothing about *how* anything is built. If a sentence names a technology, it does not belong here. |

---

## How to read this — and the boundary that governs everything

System context answers: *what is our system, what sits around it, and where are the lines?* It is the outermost architectural view — the map before any building.

> **The constitutional Product Boundary (KD-12.7) is the organizing principle of this entire document:**
> - We are **NOT** an ATS. We do **NOT** create jobs, post jobs, or receive applications.
> - We begin **only after** candidates already exist inside the customer's ATS.
> - **Our responsibility begins when candidates are *imported*.**
> - **Our responsibility ends when hiring intelligence is *delivered back*.**

Everything below — every boundary, flow, and failure mode — is drawn against that line.

---

## 1. System Vision *(one page)*

Our system is a **System of Intelligence** for hiring. It sits *between* a customer's existing Systems of Record (their ATS, later their HRIS) and turns candidates who have *already applied* into **explainable, fair, evidence-based hiring intelligence** — recommendations a human can trust, defend, and act on — then delivers that intelligence **back** into the customer's systems.

It is **neutral** (it works alongside any ATS and favors none), **embedded** (it changes no one's existing workflow), and **gate-enforcing** (fairness, explainability, human accountability, consent, audit, and tenant isolation are enforced *at the boundary* and cannot be bypassed).

Its lifecycle in one line: **Import already-applied candidates → run an Evaluation Campaign → collect evidence → evaluate (fairness-gated) → produce an explainable recommendation → support a human decision → deliver intelligence and feedback back out.** Everything before import (jobs, postings, sourcing, applications) and everything after delivery (offers, HR records) belongs to the customer's Systems of Record — never to us.

The system depends on a small set of external systems — the customer's **ATS**, an **Email Provider**, an **LLM Provider**, an immutable **Audit Store**, and (later) the customer's **HRIS** — but it is *coupled to none of them*: each is a replaceable, well-bounded dependency, and the system degrades safely when any is unavailable.

---

## 1A. Evaluation Campaign as the Unit of Work

*A context-level architectural clarification — not logical design, not implementation. It names the fundamental business container that organizes everything downstream.*

> **The Evaluation Campaign is the fundamental business container of the platform.** Every evaluation activity happens *inside* a campaign; the campaign is the unit of scope, lifecycle, fairness, audit, reporting, and export.

- **Everything belongs to exactly one campaign.** Every invitation, evaluation, piece of evidence, recommendation, and candidate feedback belongs to **exactly one Evaluation Campaign** (DOC-04 A-04.4). There is no evaluation activity that exists outside a campaign.
- **The campaign is the boundary of six things:**
  - **Scope** — which Role, which imported candidates, which calibration apply.
  - **Lifecycle** — a campaign has a clear beginning (after import) and end (after delivery/cancel).
  - **Auditability** — the audit trail is organized *by campaign*; a campaign is the natural unit of "show me what happened."
  - **Fairness boundary** — adverse-impact/fairness is assessed *within* a campaign (a coherent candidate set for one Role).
  - **Reporting boundary** — results and metrics are reported per campaign.
  - **Export boundary** — hiring intelligence is delivered back to the customer *per campaign*.
- **Candidate participation:** a Candidate may participate in **many campaigns over time** (they are a lifetime network participant — DOC-08 A-08.3), but **never in more than one active evaluation within the same campaign** unless the campaign explicitly restarts theirs (e.g., after an interruption — Error Philosophy, DOC-06 A7). *(This mirrors MVP business rule #1, PRODUCT-01 §7.)*
- **One tenant only.** A campaign **belongs to exactly one organization and can never cross a tenant boundary** (tenant isolation, INV-8; §6/§7 trust & data boundaries). There is no such thing as a cross-company campaign.
- **Boundary-bounded (KD-12.7):** a campaign **begins only after Candidate Import** and **ends only after recommendations have been delivered back** — or the campaign is **explicitly cancelled.** It never reaches before application (jobs/sourcing) or after delivery (offers/HR records).
- **Historical evidence is immutable.** Future compounding capabilities — **Hiring Memory, Benchmarking, Outcome Learning** — may **reference** a completed campaign's outputs, but must **never modify a historical campaign's evidence, evaluations, or recommendations.** A campaign, once concluded, is a fixed record (this protects auditability and defensibility, and makes Outcome Learning trustworthy).
- **It is the primary organizing boundary of downstream architecture.** Scope, lifecycle, isolation, fairness, audit, and export all attach to the campaign — so the logical architecture (ARCH-02+) organizes around it. *(Recorded as AD-09.)*

> Why this matters at the context level: naming the campaign as the unit of work *now* means every later boundary (fairness, audit, isolation, export, reporting) has a single, coherent container to attach to — rather than being scattered across ad-hoc scopes. It is the contextual keystone the rest of the architecture hangs from.

## 2. System Context Diagram

```
                                   ┌──────────────────────────────────────────┐
                                   │            ACTORS (humans)                 │
                                   │                                            │
   Candidate ──────invited / evaluates / gets feedback──────────┐              │
                                   │                             │              │
   Recruiter ──imports · runs campaigns · reviews · exports──┐   │              │
   Hiring Manager ──reviews finalists · records decision──┐  │   │              │
   Company Admin ──connects ATS · manages users/consent─┐ │  │   │              │
                                   └───────────────────┼─┼──┼───┼──────────────┘
                                                        │ │  │   │
                                                        ▼ ▼  ▼   ▼
                     ┌───────────────────────────────────────────────────────────────┐
                     │   HIRING INTELLIGENCE PLATFORM  (System of Intelligence)        │
                     │   — boundary: IMPORT ➜ … ➜ DELIVER BACK —                       │
                     │   ┌───────────────────────────────────────────────────────────┐ │
                     │   │  EVALUATION CAMPAIGN  ── the Unit of Work ──                │ │
                     │   │  every evaluation activity lives inside exactly one          │ │
                     │   │  scope · lifecycle · fairness · audit · reporting · export   │ │
                     │   └───────────────────────────────────────────────────────────┘ │
                     │   one tenant only · campaigns never cross organizations          │
                     └───────────────────────────────────────────────────────────────┘
              import candidates ▲        │ deliver intelligence back   │ evaluate/explain
              (inbound)         │        ▼ (outbound export)           ▼ (outbound calls)
        ┌───────────────────────┴───┐  ┌─┴──────────────────┐   ┌─────┴───────────────┐
        │   ATS  (customer SoR)      │  │  ATS (export back) │   │   LLM Provider      │
        │  candidates · requisitions │  │  results/results   │   │  (3rd-party, swap-  │
        │  offers (out of scope)     │  │  written back      │   │   able; PII-bounded)│
        └────────────────────────────┘  └────────────────────┘   └─────────────────────┘

        ┌────────────────────┐   ┌──────────────────────┐   ┌───────────────────────────┐
        │  Email Provider     │   │  Audit Store          │   │  Future HRIS (post-MVP)    │
        │  invitations /      │   │  immutable, append-   │   │  on-the-job OUTCOMES       │
        │  notifications (out)│   │  only trail (write)   │   │  referenced inbound (async)│
        └────────────────────┘   └──────────────────────┘   └───────────────────────────┘

   Legend:  inbound = data enters our boundary · outbound = leaves it · SoR = System of Record (customer's)
```

- The platform is the single box in the center; **actors interact with it, and it integrates with external systems** — but it *owns* none of the external systems, and it never becomes one.

---

## 3. System Boundaries

| Boundary | Contents |
|---|---|
| **INSIDE (we own & are responsible for)** | Candidate import handling · Evaluation Campaign management · Evidence collection, integrity, and structuring · Evaluation, confidence, fairness checking · Explanation generation · Recommendation preparation · Human-decision support (capture) · Candidate feedback · Calibration & (later) Hiring Memory · The **System of Intelligence** and its proprietary evidence/evaluation assets. |
| **OUTSIDE (we never own — customer Systems of Record)** | Job creation · Job posting · Candidate sourcing · Application intake (the *act* of applying) · Resume database · Applicant tracking · Offer management · HR records · Employee records · Payroll. *(KD-12.7 — permanent.)* |
| **SHARED (crosses the boundary; jointly relevant)** | Candidate records (imported *from* the ATS) · Requisition/Role reference (referenced, not owned) · Evaluation results (delivered *back to* the ATS) · Outcome data (referenced *from* the HRIS, post-MVP) · Identity of the human users (authenticated, possibly via the customer's identity system) · Consent (captured by us, honored across the boundary). |

> **The boundary test for any future capability:** *does it require us to own a System of Record?* If yes, it is OUTSIDE — full stop (KD-12.7). If it produces or explains hiring intelligence, it is INSIDE. If it moves data across, it is SHARED and must respect the gates.

---

## 4. External Systems

| System | Purpose | Ownership | Integration Direction | Sync / Async |
|---|---|---|---|---|
| **ATS** | Customer's System of Record for candidates & requisitions; source of imports and destination of results. | **Customer** | **Bidirectional** — inbound (import candidates/req reference) + outbound (deliver results back) | **Async-first** (synchronization/batch), with near-real-time where needed. We tolerate it being briefly unavailable. |
| **Email Provider** | Deliver candidate invitations and status/notifications (governed by Waiting & Silence philosophies). | Third-party (ours) or customer's mail | **Outbound** | **Async** |
| **LLM Provider** | External AI reasoning used by evaluation and explanation. **Model-agnostic & replaceable** — not the moat. | **Third-party** | **Outbound** (we call it) | **Sync per call**, orchestrated **async** overall; PII-bounded at this edge. |
| **Audit Store** | Immutable, append-only record of every material action for defensibility. | Ours (isolated) or external trust store — *decision deferred (§AD/OQ)* | **Outbound (write)** | **Append/async**, but write-durability is critical. |
| **Future HRIS** | Source of on-the-job **outcomes** (performance/retention) that feed Outcome Learning. **Post-MVP; boundary reserved.** | **Customer** | **Inbound (reference)** | **Async** |
| **Identity Provider (customer SSO)** *(implied by auth)* | Authenticate the customer's human users (Admin/Recruiter/HM). | **Customer** | **Inbound (trust)** | **Sync (at login)** |

> **Coupling principle:** each external system is a *replaceable dependency behind a boundary*, never a hard-wired part of us. The LLM Provider especially is swappable (DOC-03 §13 — the model is not the moat).

---

## 5. Primary User Flows *(context level — who touches what across boundaries)*

**5.1 Candidate Evaluation flow** *(the mission)*
Candidate (already in the ATS) → **receives invitation** (Email Provider) → **completes evaluation** with the platform (System of Engagement) → evidence enters the platform → platform evaluates (calls **LLM Provider**, fairness-gated) → later **receives feedback** (after recruiter release). *The candidate never touches the ATS through us and never leaves the customer's application flow to apply.*

**5.2 Recruiter flow**
Recruiter → **connects ATS / imports candidates** (from **ATS**) → **creates Evaluation Campaign** → monitors status → **reviews evidence-first recommendations** on the platform → **releases candidate feedback** → **exports results back** (to **ATS**). *Authenticated via the customer's Identity Provider.*

**5.3 Hiring Manager flow**
Hiring Manager → **reviews finalists' evidence** (platform) → **records the hiring decision** (human-accountable; platform captures it, never decides high-risk itself). *The offer itself is actioned in the ATS — outside our boundary.*

**5.4 Admin flow**
Company Admin → **connects the ATS**, configures **users, roles, consent, and tenant settings** → establishes the trust boundary (isolation, data handling). Setup only; not a daily user.

---

## 6. Trust Boundaries

*Where trust changes hands. Each is a line the architecture must defend (mechanisms are later docs; here we name the boundaries).*

| Trust boundary | What crosses it | The rule at this boundary |
|---|---|---|
| **Authentication** | Human users entering the system (Admin/Recruiter/HM), likely via the customer's Identity Provider. | Only authenticated, known users cross; identity is established at the edge. |
| **Authorization** | Every action, scoped to a tenant and a role. | Actions are permitted only within the user's tenant and role; **cross-tenant access is impossible by construction** (tenant isolation, INV-8). |
| **PII (candidate data)** | Candidate personal data entering (from ATS) and being processed. | PII is consent-governed; **minimized at every outward boundary**, never sold (P3/KD-03.14). The most sensitive boundary. |
| **Evidence** | Candidate evidence produced during evaluation. | Sensitive, integrity-checked, tenant-isolated; the proprietary core of the System of Intelligence. |
| **Audit** | Every material action, written outward to the Audit Store. | **Append-only, immutable, complete** — nothing material escapes the audit boundary (P8/INV-2); nothing is withheld from audit. |
| **LLM Calls** | Data leaving our boundary to a third-party model. | **The critical outward boundary.** What candidate data crosses to the LLM Provider must be controlled/minimized; this edge carries the highest privacy/compliance exposure (see Risks). |

> **The sharpest trust boundary is the LLM edge** — it is the one place candidate data leaves our control to a third party. It gets disproportionate architectural attention in later docs (ARCH-06/08).

---

## 7. Data Boundaries — the three systems

A clean context-level separation of *where data lives and who owns it*:

| | **System of Record (SoR)** | **System of Intelligence (SoI)** | **System of Engagement (SoE)** |
|---|---|---|---|
| **Owns** | The **customer** | **Us** | Us (transient interaction surfaces) |
| **Holds** | Jobs, requisitions, applications, candidates (canonical), offers, employees, outcomes | Evidence, evaluations, calibration, confidence, recommendations, (later) Hiring Memory & benchmarks | Invitations, the evaluation experience, recruiter/HM dashboards, candidate feedback |
| **Our stance** | **Reference, never own** (KD-12.7); import candidates, export results | **Our proprietary, compounding core** — the moat lives here | The *how they experience it* layer (governed by the Manifesto, DOC-06) |
| **Boundary rule** | Data flows in (import) and out (deliver back); we hold references, not the source of truth | Tenant-isolated; never leaks across companies; only aggregate benchmarks ever cross (INV-8) | Ephemeral relative to SoI; serves the interaction, not the record |

> **The one-line data doctrine:** *the customer's ATS/HRIS is the System of Record; we are the System of Intelligence; the interaction surfaces are the System of Engagement.* We turn *their* records into *our* intelligence and hand the intelligence back — we never try to be their record.

---

## 8. High-Level Capabilities *(mapped to DOC-12 — no implementation)*

The context hosts the DOC-12 capabilities, grouped by where they sit relative to the boundary:

- **Boundary/Integration (touch external systems):** Candidate Intake/Import (C2), Integrations (C3), Requisition reference (C1), Export/Offer-Rejection handoff (C18), Notification (C5), Candidate Communication (C4) — *these cross to ATS/Email.*
- **System of Intelligence (inside, core):** Role Calibration (C6), Evidence Request/Collection (C8), Integrity Verification (C9), Evidence Structuring (C10), Evaluation Orchestration (C11), Confidence (C12), Explanation Generation (C15), Recommendation (C16), Benchmarking (C14, post-MVP), Hiring Memory (C7, post-MVP), Outcome Capture/Learning (C21/C22, post-MVP via HRIS).
- **Decision (inside, human-in-loop):** Human-Decision Support & Capture (C17), Candidate Feedback (C19), Talent Pool/Afterlife (C20, post-MVP).
- **Always-on Ground (authoritative gates — enforced at the boundary):** Fairness/Adverse-Impact (C13), Consent & Privacy (C24), Audit Recording (C23), Tenant Isolation (C25).

> The **authoritative capabilities (C9/C13/C15/C23/C24/C25)** are the ones that must be enforced *at the boundary* and cannot be bypassed — they are the runtime form of the Constitution's gates (DOC-12 A-10.2 §A-4). Everything else is advisory (the human can override).

---

## 9. Failure Boundaries

*Per the Error Philosophy (DOC-06 A7): failure degrades to **less confidence / more human involvement — never a wrong-or-unfair result.** Context-level behavior for each dependency failure:*

| Failure | Contextual behavior (what must be true) |
|---|---|
| **ATS unavailable** | Import/export is *deferred and retried*; nothing is lost; the recruiter is told plainly. We are async-first, so a brief ATS outage never blocks in-flight evaluation. |
| **Email unavailable** | Invitations/notifications *queue and retry*; the candidate is never penalized for a delivery failure (dignity, P7); status stays honest. |
| **LLM Provider unavailable** | Evaluation *pauses*, not fabricates. No recommendation is invented. Honest "in progress / temporarily delayed" (A8). Because we are model-agnostic, we can fail over to an alternative provider where available. **A wrong-but-confident result is never acceptable.** |
| **Candidate abandons mid-evaluation** | Progress is *preserved*; **no penalty framing**; a clear, dignified way to resume (P7/A7). Partial evidence yields *lower confidence*, never a fabricated complete evaluation. |
| **Fairness Gate fails** | The recommendation is **HELD, not delivered** (INV-3 — a hard stop, not a warning). This is a *correct* failure: it protects the candidate and the customer. Escalates to human review. |
| **Explainability fails** | **No recommendation ships** — a bare score is forbidden (INV-2). If we cannot explain it, we do not deliver it. |

> **The failure doctrine (context level):** every dependency failure resolves toward *pause, preserve, and hand to a human with honest status* — never toward *guess, penalize, or ship an unexplained/unfair result.* The gates hold even when everything else breaks.

---

## 10. Architectural Principles *(context level — no technology)*

1. **The Product Boundary is inviolable (KD-12.7).** We are a System of Intelligence, never a System of Record. Import in, intelligence out.
2. **Neutrality.** We integrate with any ATS and favor none; no external system may become a hard dependency we cannot replace.
3. **Model-agnostic.** The LLM Provider is a replaceable external dependency, not part of our identity or moat.
4. **Gates enforced at the boundary.** Fairness, explainability, human accountability, consent, audit, and tenant isolation are *authoritative* — they cannot be bypassed by any flow, integration, or configuration.
5. **Reference, never absorb.** We hold references to Systems-of-Record data (candidates, requisitions, outcomes); we are never their source of truth.
6. **Fail safe, not silent.** Every failure degrades to less confidence / more human / honest status — never to a wrong, unfair, or fabricated result.
7. **PII minimization at every outward boundary** — especially the LLM edge; the least candidate data that can cross, does.
8. **Tenant isolation is a boundary, not a feature.** One company's data cannot reach another by construction; only aggregate, non-identifying benchmarks ever cross (post-MVP).
9. **Everything material is auditable.** Nothing consequential happens outside the audit boundary.
10. **The System of Intelligence is the core; SoR and SoE are interfaces.** Our proprietary, compounding value lives in the SoI; the others are how data enters/leaves and how humans experience it.

---

## Architecture Decisions

- **AD-01** — We are a **System of Intelligence** that integrates with external **Systems of Record**; we never become an SoR (KD-12.7).
- **AD-02** — **Model-agnostic**: the LLM Provider is an external, replaceable dependency; the architecture must not couple to any single provider.
- **AD-03** — **Gates are enforced at the boundary** and are non-bypassable (authoritative capabilities).
- **AD-04** — **Async-first integration** with the ATS (synchronization model), so external unavailability never blocks in-flight work or corrupts results.
- **AD-05** — **PII is minimized at the LLM boundary**; controlling what candidate data crosses to third parties is a first-class architectural concern.
- **AD-06** — **Audit is append-only and complete**; nothing material escapes it. *(Internal-vs-external location deferred — see OQ.)*
- **AD-07** — **The HRIS/outcome boundary is reserved but deferred** to post-MVP; the context accounts for it now so it needn't be retrofitted.
- **AD-08** — **The three-systems data model (SoR / SoI / SoE)** is the canonical data-ownership frame for all downstream architecture.
- **AD-09** — **The Evaluation Campaign is the fundamental Unit of Work** and the primary business boundary (scope · lifecycle · fairness · audit · reporting · export · tenant isolation); every evaluation activity belongs to exactly one campaign, and downstream architecture organizes around it (§1A). Historical campaign evidence is immutable; compounding capabilities reference it, never modify it.

## Open Questions

1. **Audit Store — internal (isolated) or external (third-party immutable)?** Affects trust posture and the trust boundary (§6). *(Decide in ARCH-08 Security & Trust.)*
2. **Identity Provider** — do we standardize on the customer's SSO/IdP for human users, and how do candidates (who have no customer account) authenticate to the evaluation? *(ARCH-08.)*
3. **How much candidate PII may cross the LLM boundary** — full evidence, or minimized/redacted? A privacy/compliance decision with big downstream impact. *(ARCH-06/08.)*
4. **ATS integration granularity** — is import/export batch-synchronization, or near-real-time? And which ATS first (PRODUCT-01 open question)? *(ARCH-09 API Contracts / ARCH-05.)*
5. **Where the boundary sits for "results delivered back"** — do we write structured results into the ATS, or present them for the recruiter to push? *(ARCH-09.)*

## Assumptions

- The customer's ATS exposes candidate data for import and can receive results back (integration is feasible — AS-26).
- Customers will permit candidate data to be processed (incl. by an LLM Provider) under appropriate consent/agreements (a live privacy assumption — ties AS-17/AS-20).
- Candidates can complete an evaluation without a pre-existing account in *our* system (they exist in the customer's ATS, not ours).
- Email is an acceptable channel for candidate invitations at MVP.
- Outcome data (HRIS) is *not* required for the MVP context, only reserved for post-MVP (AS-21/AS-27 govern its eventual availability).

## Risks

- **The LLM boundary is the top architectural risk** — candidate PII crossing to a third-party model raises privacy, compliance (AS-17/RK-6), and trust exposure. Mitigation direction: PII minimization (AD-05), model-agnosticism (AD-02), consent (P3). *(Deep treatment: ARCH-08.)*
- **ATS integration fragility/breadth** (RK-14/AS-26) — many ATSs, brittle interfaces; async-first (AD-04) and one-ATS-first (PRODUCT-01) reduce it.
- **Audit immutability/completeness** — if the audit boundary leaks or gaps, defensibility (Sofia/Marcus, AS-17/AS-20) collapses; append-only + complete (AD-06).
- **Over-coupling to an external system** would violate neutrality (AD-02/03) and re-introduce platform risk (RK-9) — the architecture must keep every external system replaceable.
- **Boundary creep** — the standing risk that a future "helpful" feature quietly pulls a System-of-Record responsibility inside (KD-12.7). Every ARCH doc must re-apply the boundary test (§3).

---

*End of ARCH-01 v0.1 — context only, zero technology. Next: **ARCH-02 — Logical Architecture** (still no technology choices — the logical components that must exist to realize the DOC-12 capabilities within these boundaries).*
