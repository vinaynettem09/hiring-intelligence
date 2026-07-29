# PRODUCT-01 — MVP Specification (Version 0.1)

| Field | Value |
|---|---|
| **Document ID** | PRODUCT-01 |
| **Title** | MVP Specification — Version 0.1 |
| **Owner** | Head of Product + CTO (jointly) |
| **Status** | Draft v0.1 — for founder approval; **this is the contract between Product and Engineering** |
| **Created** | 2026-07-22 |
| **Phase** | **Phase 3 — Product Definition** (see §0) |
| **Depends on** | DOC-01–12 (foundation), VALIDATION-01–03 (what must be learned), esp. **KD-12.7 Product Boundary** and the Capability Register (DOC-12 §3) |
| **The single goal** | **NOT completeness.** Build the *smallest possible product* that lets a real company evaluate real candidates end-to-end and thereby **validate AS-1, AS-2, AS-3, AS-4, and AS-10.** |

---

## 0. Phase context — where we are

We are transitioning from **Product Design** to **Product Implementation.** The project phases:

| Phase | Name | Artifacts | Status |
|---|---|---|---|
| **1** | Strategy & Product Design | DOC-01 → DOC-12 | ✅ Complete (frozen unless evidence demands change) |
| **2** | Validation Framework | VALIDATION-01 → 03 | ✅ Complete (execute in parallel) |
| **3** | **Product Definition** | **PRODUCT-01 (this)** | 🔄 Now |
| **4** | Engineering | Architecture · Database · APIs · AI pipelines · Backend · Frontend | Next (only after PRODUCT-01 approved) |
| **5** | Pilot | Deploy to 2–3 design partners · collect evidence · iterate | After Phase 4 |

> **This document ends the era of strategy documents and begins documents that translate directly into code.** Every section here is meant to be buildable.

---

## 1. MVP Objective & Non-Objectives

- **Objective:** the minimum product that lets a real company **evaluate real candidates end-to-end** — from importing already-applied candidates to delivering an explainable, fair recommendation back — so we can **test the Core-Thesis and mission assumptions with real behavior (evidence level L2–L3), not interviews.**
- **The MVP is a validation instrument, not a finished product.** Its success is measured in *learning* (did AS-1/2/3/4/10 survive contact with reality?), not in feature count.
- **Non-objective:** completeness, scale, breadth, polish beyond what trust requires, or any compounding/network capability. Those are Phase 4+/post-MVP.

**The one rule that overrides "minimum":**
> **The MVP cuts *compounding and scale*, never the Constitution's gates.** Fairness (P1), Explainability/Progressive Explainability (P1/P13), Human Accountability (P2), Consent/Privacy (P3), Audit (P8), and Tenant Isolation (P3) are **in scope for v0.1** — they are *authoritative* capabilities (DOC-12 A-10.2 §A-4) and are never an MVP shortcut. A "faster MVP" that skips a gate is not our MVP.

---

## 2. Explicitly Out of Scope (v0.1)

Deferred, by decision — **do not build these for the MVP:**

- **Systems of Record (permanently ours-never — KD-12.7):** Job board · ATS · Career pages · Resume database · Applicant tracking · Offer management · Internal HR · Payroll.
- **Compounding / network capabilities (deferred to post-MVP):** Benchmarking · Outcome Learning · Hiring Memory (beyond a *thin* per-campaign calibration) · Network intelligence · Talent Pool / Afterlife automation · Referrals · Marketplace.
- **Scale / sophistication (deferred):** Multi-tenancy *optimizations* (basic isolation is in scope; optimization is not) · Advanced analytics/dashboards · Multi-ATS breadth (one ATS + upload is enough) · Multi-role-family generalization (SWE beachhead only) · Non-US compliance modules.

> Note the split: **Systems-of-Record items are out *forever* (boundary); compounding items are out *for now* (sequencing).** DOC-12's Maturity Roadmap already says Horizon 1 ships compounding capabilities immature — the MVP is Horizon 1.

---

## 3. Actors

| Actor | Role in the MVP | Persona (DOC-08) |
|---|---|---|
| **Company Admin** | Connects the ATS / configures the account / manages users. Setup only. | (subset of Marcus/Rina) |
| **Recruiter** | Imports candidates, creates the Evaluation Campaign, reviews recommendations, releases candidate feedback, exports results. Primary daily user. | Rina |
| **Hiring Manager** | Reviews finalists' evidence and makes/records the hiring decision. | David |
| **Candidate** | Receives the invitation, completes the evaluation, receives feedback. First-class user. | Alex |

*(CHRO/Security are buyers/approvers, not MVP screen-users — DOC-08. No CHRO/Security screens in v0.1.)*

---

## 4. The MVP Flow (end-to-end)

*Bounded by KD-12.7: starts at **import**, ends at **export**. "Evaluation Campaign" per DOC-04 A-04.4.*

```
[ Candidates already applied in the customer's ATS — OUTSIDE our boundary ]
                              │
 1. Recruiter connects ATS  ── OR ──  uploads candidates      (Candidate Intake/Import, C2/C3)
                              ▼
 2. Recruiter creates an Evaluation Campaign for the Role      (Role Calibration — thin, C6)
                              ▼
 3. Candidates automatically receive Evaluation Invitations    (Candidate Communication, C4)
                              ▼
 4. Candidates complete the evaluation                         (Evidence Request & Collection, C8)
                              ▼
 5. Evidence generated & structured (+ integrity checked)      (C9, C10)
                              ▼
 6. AI evaluates the evidence  →  Fairness gate  →  Confidence  (C11, C13*, C12)   *GATE — must pass
                              ▼
 7. Recommendation prepared (evidence-first + explanation)      (C15, C16)
                              ▼
 8. Recruiter dashboard: review the evidence-backed shortlist   (Recruiter view — P13)
                              ▼
 9. Hiring Manager review: finalists' evidence + decision       (Human-Decision Support, C17 — P2)
                              ▼
10. Candidate feedback (released by recruiter)                  (Candidate Feedback, C19 — P13)
                              ▼
11. Export results back to the customer's ATS                  (Export — reference, C18/C3)
                              │
[ Offer / rejection actioned in the customer's ATS — OUTSIDE our boundary ]
   … Audit, Consent/Privacy, and Tenant Isolation run under EVERY step (C23/C24/C25) …
```

---

## 5. Screens

*Each: **Purpose · Actor · Inputs · Outputs · Success criteria.** Screens only; no visual/implementation detail (that's Phase 4 + the Manifesto governs the *feel*, DOC-06).*

**S-1 · Connect ATS / Import Candidates** — *Purpose:* bring already-applied candidates into the platform (C2/C3). *Actor:* Company Admin / Recruiter. *Inputs:* ATS connection **or** candidate upload; the Role/req reference. *Outputs:* imported candidate list tied to a Role. *Success:* candidates import cleanly with no manual re-keying; recruiter confirms the list matches the ATS.

**S-2 · Create Evaluation Campaign** — *Purpose:* start an evaluation run for a Role and capture a *thin* calibration of the bar (C6). *Actor:* Recruiter (+ optional HM input). *Inputs:* Role, imported candidates, minimal calibration (what "good" means for this role). *Outputs:* an active Evaluation Campaign. *Success:* campaign starts; calibration captured well enough that the HM later agrees it reflects their bar (tests AS-12).

**S-3 · Campaign Monitor** — *Purpose:* see invitation/completion status calmly (DOC-06 §8, no metric-wall). *Actor:* Recruiter. *Inputs:* campaign state. *Outputs:* per-candidate status (invited / accepted / in-progress / completed / evaluated). *Success:* recruiter always knows where each candidate stands (no black hole — A8).

**S-4 · Candidate Invitation** — *Purpose:* invite the candidate honestly and calmly (C4; A1). *Actor:* Candidate. *Inputs:* invitation (name, role, what to expect, honest AI disclosure, consent request). *Outputs:* accepted/declined + consent captured. *Success:* high acceptance; candidate feels informed, not processed (tests AS-3, AS-10 entry).

**S-5 · Candidate Evaluation** — *Purpose:* elicit evidence of ability (C8) via the MVP Sensor(s). *Actor:* Candidate. *Inputs:* the evaluation task(s) for the role. *Outputs:* candidate's responses → Evidence. *Success:* completion without unacceptable drop-off, esp. among strong candidates (tests AS-3); the task feels fair and about ability (tests AS-10).

**S-6 · Recruiter Recommendation Dashboard** — *Purpose:* present the evidence-first, ranked shortlist the recruiter can trust and defend (C16; recruiter P13 view). *Actor:* Recruiter. *Inputs:* completed evaluations. *Outputs:* per candidate — Evidence → Explanation → Recommendation → **Evaluation Score**, with **Confidence** and **Integrity Score**; ranked shortlist. *Success:* recruiter trusts and can defend the shortlist within days (tests AS-2, AS-8); evidence appears *before* the score (DOC-06 §5).

**S-7 · Hiring Manager Review** — *Purpose:* let the HM review finalists' evidence against their bar and **make/record the decision** (C17; HM P13 view). *Actor:* Hiring Manager. *Inputs:* finalists + evidence + calibration alignment. *Outputs:* a **human-made** advance/hold/reject decision, captured with any override. *Success:* HM reduces re-screening and owns the decision (tests AS-9, AS-2; honors P2).

**S-8 · Candidate Feedback (post-release)** — *Purpose:* deliver constructive, evidence-based feedback — *only after the recruiter releases it* (C19; candidate P13 view). *Actor:* Candidate. *Inputs:* released evaluation feedback. *Outputs:* strengths, evidence-based observations, improvement areas; framed "not the strongest match for this role," never "not good enough" (DOC-06 §10). *Success:* candidates — *including rejected ones* — report the process felt fair (tests AS-10, the mission).

**S-9 · Export to ATS** — *Purpose:* deliver the hiring intelligence back to the customer's system (boundary end — KD-12.7). *Actor:* Recruiter. *Inputs:* recommendations/decisions. *Outputs:* results written/exported to the ATS (reference). *Success:* results land in the customer's workflow with no manual re-entry.

**S-10 · Account & User Setup** — *Purpose:* basic account, users, roles, consent/data settings (C24/C25 basics). *Actor:* Company Admin. *Inputs:* org, users, data settings. *Outputs:* configured tenant. *Success:* isolation and consent configured; security can verify the basics (supports AS-20).

---

## 6. APIs (high-level only — capability operations, **no implementation**)

*Logical operations, not protocols/tech (no REST/GraphQL/DB/queue — Phase 4). Each: operation · purpose · inputs · outputs.*

- **Candidate Import** — bring candidates from ATS/upload. *In:* ATS connection or file + Role ref. *Out:* imported candidate records. *(C2/C3)*
- **Campaign** — create/read/close an Evaluation Campaign. *In:* Role, candidates, calibration. *Out:* campaign + status. *(C6)*
- **Invitation** — issue/track candidate invitations + consent. *In:* candidate, campaign. *Out:* invitation state + consent. *(C4/C24)*
- **Evidence** — receive/structure candidate evidence + integrity check. *In:* candidate responses. *Out:* structured Evidence + Integrity Score. *(C8/C9/C10)*
- **Evaluation** — evaluate evidence → recommendation, fairness-gated. *In:* Evidence + calibration. *Out:* Evaluation Score + Confidence + Explanation + Recommendation (only if fairness passes). *(C11/C12/C13/C15/C16)*
- **Decision** — capture the human decision/override. *In:* HM decision. *Out:* recorded decision. *(C17)*
- **Feedback** — generate/release candidate feedback. *In:* evaluation + recruiter release flag. *Out:* candidate-appropriate feedback. *(C19)*
- **Export** — deliver results to the ATS. *In:* recommendations/decisions. *Out:* export confirmation. *(C18/C3)*
- **Audit / Consent / Isolation** — always-on, under every operation. *(C23/C24/C25)*

---

## 7. Business Rules (MVP invariants)

*These must hold in v0.1. The first four are the CTO's; the rest are gate-derived (DOC-05 / DOC-04 invariants) and are non-negotiable even in MVP.*

1. **A candidate cannot be evaluated twice in the same campaign.**
2. **An evaluation cannot start before the invitation is accepted (and consent captured).**
3. **A recommendation cannot be produced/delivered unless the Fairness gate passes** (C13; INV-3 — a hard dependency, not a warning).
4. **Candidate feedback is generated/sent only after the recruiter releases it.**
5. **No recommendation without attached Evidence and Explanation** — nothing ships as a bare score (INV-2; bare "Score" forbidden, DOC-04 A-04.A5).
6. **Every material action is audit-logged** (C23; P8/INV-2).
7. **The hiring decision is captured from a human; the system never auto-advances/rejects a finalist** (C17; P2 — high-risk decisions require human review).
8. **Confidence is always attached to an Evaluation** (INV-6); low-confidence is surfaced honestly, never hidden.
9. **Candidate data is governed by consent and never used beyond the campaign without consent; never sold** (P3/KD-03.14).
10. **One company's data never crosses to another** (C25; tenant isolation, INV-8).
11. **We never store or own a System-of-Record artifact** (job, requisition, offer, employee record) — only reference them (KD-12.7).

---

## 8. Success Metrics *(and the assumption each tests)*

| Metric | What it measures | Tests | Evidence level |
|---|---|---|---|
| **Candidate completion rate** | % invited candidates who finish the evaluation (esp. strong candidates) | **AS-3** | L2 (behavior) |
| **Candidate fairness score** | Perceived-fairness survey, **including rejected candidates** | **AS-10** | L2 |
| **Recruiter trust** | Do recruiters accept & defend the shortlist without re-doing it? (+ TTTM in days) | **AS-2, AS-8** | L2 |
| **Decision changes** | Do evidence-based recommendations change decisions vs. the resume-first baseline? | **AS-2, AS-1** | L2–L3 |
| **Time saved** | Recruiter/HM time per hire vs. baseline (supporting efficiency signal) | (supports AS-24) | L2 |
| **HM re-screening reduction** | Does the HM stop re-screening over successive hires? | **AS-9** | L2–L3 |

> **AS-1 (does evidence predict *quality*?)** and **AS-4 (will they *pay* for quality?)** are *not fully* answered by the MVP alone: AS-1 needs the **retrospective study + longitudinal outcomes** (run in parallel — §12), and AS-4 needs **pricing/WTP conversations** during the pilot. The MVP gives us the *behavioral* half (decisions change, candidates complete, recruiters trust); the parallel track gives us the *predictive* and *commercial* halves.

---

## 9. Deferred Features (explicit)

*Everything not required to evaluate real candidates end-to-end. Mapped to the Capability Register (DOC-12) so nothing is lost — just sequenced.*

- **Benchmarking (C14)** — needs network scale.
- **Hiring Memory beyond thin per-campaign calibration (C7)** — compounding; post-MVP.
- **Outcome Capture & Outcome Learning (C21/C22)** — needs longitudinal data; *the learning loop is Phase 5+* (but we start *collecting* outcome data in the pilot to seed it).
- **Talent Pool / Afterlife automation (C20)** — post-MVP (candidates are still treated with dignity in MVP; automation of re-engagement is deferred).
- **Advanced analytics / executive dashboards** — Sofia's aggregate view is post-MVP.
- **Multi-ATS breadth (C3 beyond one)** — one ATS + upload for MVP.
- **Multi-role-family generalization** — SWE beachhead only.
- **Non-US compliance modules** — US-first (DOC-01 §5).
- **Multi-tenancy optimizations** — basic isolation only.
- **Referrals, Marketplace, Network intelligence** — Horizon 2–3.

---

## 10. MVP ↔ Assumption Map

| MVP element | Primary assumption(s) validated |
|---|---|
| S-4/S-5 Candidate invitation + evaluation, completion metric | **AS-3** (candidates adopt/complete) |
| S-8 Candidate feedback + fairness survey (incl. rejected) | **AS-10** (fair chance, even rejected) |
| S-6 Recruiter dashboard + recruiter-trust metric | **AS-2, AS-8** (act on evidence; trust fast) |
| S-7 HM review + re-screening metric | **AS-9, AS-2** |
| Decision-change metric + parallel retrospective (§12) | **AS-1** (evidence improves decisions) |
| Pilot pricing conversations (parallel) | **AS-4** (pay for quality) |
| Fairness gate (rule 3), explanation (rule 5), human decision (rule 7) | Gates hold under a real build (P1/P13/P2) |

---

## 11. Exit Criteria

> **The MVP is complete when a real company can evaluate real candidates end-to-end** — import already-applied candidates → create an Evaluation Campaign → invite → candidates complete → evidence generated → AI evaluates (fairness-gated) → evidence-first recommendation on the recruiter dashboard → HM reviews and records a decision → candidate feedback released → results exported to the ATS — **with the audit trail, consent, isolation, explainability, and fairness gate all intact**, for at least one real requisition at a design partner.

**Not required for "complete":** scale, polish beyond trust, benchmarking, outcome learning, multi-ATS, or analytics. Those are explicitly deferred (§9).

## 12. Parallel Zero-Build Validation *(do NOT wait for the MVP)*

The MVP tests the *behavioral* assumptions, but two of the most important tests need **no code** and must start **immediately, in parallel** (per VALIDATION-01 R5 / VALIDATION-03):
- **Experiment A — Historical Retrospective (AS-1):** with the first design partner's *past* hires and known outcomes, run blind evidence-based evaluation and check separation vs. the resume screen. *(No product; the cheapest, most decisive test.)*
- **Experiment C — Rejected-Candidate Interviews (AS-10):** understand what "fair" means to real rejected candidates. *(No product; needs the Research Playbook, VALIDATION-03.)*

> **Guardrail:** do not let "build the MVP" become an excuse to delay the zero-cost experiments. If AS-1 fails the retrospective, we may not need to finish the MVP at all (KILL-1). Cheap learning first.

---

## Summary

- **KD-P01.1** — The MVP is the **smallest product that validates AS-1/2/3/4/10** — a validation instrument, not a finished product; success = learning, not features.
- **KD-P01.2** — **Gates are never cut**, even in v0.1 (fairness, explainability, human accountability, consent, audit, isolation are in scope); only *compounding/scale* is deferred.
- **KD-P01.3** — The MVP flow is **bounded by KD-12.7**: starts at candidate *import*, ends at results *export*; we never own a System of Record.
- **KD-P01.4** — Ten screens, logical APIs, and **eleven business-rule invariants** define the build; exit = a real company evaluates real candidates end-to-end with all gates intact.
- **KD-P01.5** — **Two decisive tests (AS-1 retrospective, AS-10 rejected-candidate interviews) run in parallel with zero build** — cheap learning is not gated behind engineering.

### Open questions (for founder/CTO)
1. **The MVP Sensor:** which single evaluation Sensor do we build first for SWE (e.g., an adaptive technical evaluation vs. a structured work sample)? *(This is the one place the blueprint's sensor-agnosticism must resolve to a concrete choice — needs a decision to start Phase 4.)*
2. **First design partner + ATS:** which partner and which ATS (Greenhouse/Ashby/Lever) do we build the first integration against?
3. **Thin calibration scope:** how minimal can S-2 calibration be while still passing HM trust (AS-12)?
4. **Voice vs. text evaluation** (Unknown Unknown, VALIDATION-01): does the MVP Sensor use voice or text? — likely resolve empirically, but a starting choice is needed.

### Next: **Phase 4 — Engineering** *(only after PRODUCT-01 is approved)*
Once approved, the next artifacts are production-oriented and, for the first time, **allowed to name technology**: **Architecture** (answering DOC-12's *"what logical components must exist?"*) → Database → APIs → Event model → AI orchestration → Backend modules → Frontend. Everything they build must satisfy this spec and the gates.

*End of PRODUCT-01 v0.1 — the Product↔Engineering contract. Approve, choose the MVP Sensor + first partner (open questions), and Phase 4 (Architecture) begins.*
