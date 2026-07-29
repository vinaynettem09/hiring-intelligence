# VALIDATION-02 — Risk Register

| Field | Value |
|---|---|
| **Document ID** | VALIDATION-02 |
| **Title** | Risk Register (derived from the Assumption Register) |
| **Owner** | Founder/CEO + CTO |
| **Status** | Draft v0.1 — for founder review |
| **Created** | 2026-07-22 |
| **Phase** | Validation Mode |
| **Depends on** | **VALIDATION-01 (Assumption Register)** — this document is *derived from it*, not written independently. |
| **Construction rule (CTO)** | This is **not** a generic project risk register. **Every risk traces to the assumption(s) that create it.** Structure per risk: **Risk → Source Assumption(s) → Early Warning Signal → Mitigation → Owner → Decision Trigger** (plus Likelihood × Impact for the heat map). If a risk cannot be traced to an assumption, it does not belong here. |

---

## How to read this — risk = "an assumption is false and we didn't catch it in time"

Because we derived this from VALIDATION-01, each risk is fundamentally *"assumption AS-x turns out false, and we discover it late/expensively."* That reframing does two things: it keeps the register honest (no invented risks), and it makes the **Early Warning Signal** and **Decision Trigger** concrete — they come straight from the assumption's failure criteria.

- **Likelihood** and **Impact**: Low / Medium / High (High-Impact ones that are also existential are flagged ★).
- **Decision Trigger** ties to VALIDATION-01's **Kill Criteria (§8)** and **Pivot Triggers (§9)** where applicable — so a tripped signal has a pre-agreed response, not a debate.

---

## 1. Executive Summary

**The existential risks all derive from the Core-Thesis and meta assumptions:**

- **RK-1 (from AS-1)** — the thesis doesn't deliver *materially valuable* improvement → the company shouldn't be built.
- **RK-2 (from AS-21)** — we can't get outcome data → we can't even *test* the thesis (the risk *behind* every other risk).
- **RK-3 (from AS-3/AS-10)** — candidates won't adopt / feel it's unfair → mission and funnel fail.
- **RK-4 (from AS-4)** — no willingness to pay for quality → no business model.
- **RK-6 (from AS-17)** — fairness can't reach a legal standard → can't ship.
- **RK-9 (from AS-5)** — a platform giant subsumes the layer → external existential risk.

**And one meta-risk that is uniquely ours to manage:**
- **RK-15 (from the validation framework itself)** — **confirmation bias**: we see supporting evidence and ignore contradictory evidence, and "validate" a false company. Our Counter-Evidence Register (VALIDATION-01 R4), Pre-Registration (R2), and Evidence Levels (R3) exist specifically to fight this — but only if we honor them.

> **The register's message:** the biggest risks are not execution risks — they are *being wrong about a Core-Thesis assumption and not finding out cheaply.* Every mitigation below is therefore a *learning* action, not a build action.

---

## 2. The Risk Register

*Grouped by tier. Each: Source Assumption(s) · Likelihood · Impact · Early Warning Signal · Mitigation · Owner · Decision Trigger.*

### 2.1 EXISTENTIAL RISKS (tie to Kill Criteria)

**RK-1 ★ — The thesis fails: evidence does not materially improve hiring decisions.**
- *Source:* **AS-1** · *Likelihood:* Medium · *Impact:* **Existential**
- *Early Warning Signal:* Experiment A (retrospective) shows weak/no separation of outcomes; Experiment B shows recruiters don't value or act on the evidence; no compensating trust/adoption.
- *Mitigation:* Run the three parallel experiments *early and cheaply* (VALIDATION-01 R5); define value broadly (accuracy **and** trust/adoption/candidate); pre-register the bar (R2) so we neither fool ourselves nor kill on undramatic-but-valuable results.
- *Owner:* CTO
- *Decision Trigger:* **KILL-1** (de-binarized) — no material improvement *and* no compensating value → stop/pivot.

**RK-2 ★ — We cannot obtain on-the-job outcome data → we cannot validate the thesis at all.** *(the risk behind every risk)*
- *Source:* **AS-21** (+ AS-27 for scale) · *Likelihood:* **Medium–High** · *Impact:* **Existential (meta)**
- *Early Warning Signal:* Design-partner conversations stall on outcome-data sharing (privacy/effort/legal); no partner will commit data in agreements.
- *Mitigation:* Make outcome-data sharing an explicit condition of design-partnership from day one (DOC-03 §21); pursue proxy/public/historical datasets in parallel; reduce the ask (start with a narrow, low-friction outcome signal).
- *Owner:* Founder/CEO
- *Decision Trigger:* **KILL-2** — if neither partner nor proxy data is attainable, we cannot proceed on faith.

**RK-3 ★ — Candidates won't adopt the evaluation, or experience it as unfair (esp. when rejected).**
- *Source:* **AS-3, AS-10** · *Likelihood:* Medium · *Impact:* **Existential**
- *Early Warning Signal:* High drop-off in Experiment/pilot (esp. among strong candidates); rejected-candidate interviews (Experiment C) reveal "judged by a machine / unfair / dismissed."
- *Mitigation:* Candidate-first design (DOC-06 P7); Honest-by-Default disclosure (A1); constructive rejection feedback (P13); ethical validation that gives candidates real value (VALIDATION-01 §10 Q4).
- *Owner:* Head of Product
- *Decision Trigger:* **KILL-3** — unfixable drop-off/unfairness at scale.

**RK-4 ★ — Buyers will pay only for speed/cost, never for decision quality.**
- *Source:* **AS-4** (+ AS-23, AS-24) · *Likelihood:* Medium · *Impact:* **Existential (business model)**
- *Early Warning Signal:* WTP interviews show only efficiency is valued; ROI framed on quality doesn't move buyers; losses to cheaper efficiency tools.
- *Mitigation:* Prepare the **wedge pivot** (attack a severe-*and*-paid problem while delivering quality underneath, DOC-02 §12); build partner-verified ROI on *their* numbers (AS-24).
- *Owner:* Founder/CEO
- *Decision Trigger:* **KILL-4** (no quality demand anywhere) or **Pivot** (quality undervalued but a paid wedge exists).

**RK-6 ★ — Fairness/adverse-impact cannot be brought to a legally-defensible standard.**
- *Source:* **AS-17** (+ AS-7) · *Likelihood:* Low–Medium · *Impact:* **Existential**
- *Early Warning Signal:* Adverse-impact testing shows persistent disparate impact we can't justify/remove; Legal says our approach is unmeetable.
- *Mitigation:* Engage I/O-psychology + employment counsel *early*; treat fairness as an authoritative gate (DOC-05 P1; DOC-12 C13); test fairness on sample data before scale.
- *Owner:* Head of Trust/Compliance + Head of AI
- *Decision Trigger:* **KILL-5** — fairness unsolvable → cannot ship.

### 2.2 PRODUCT / ADOPTION RISKS

**RK-5 — People receive evidence but don't act on it (or HMs keep re-screening).**
- *Source:* **AS-2, AS-8, AS-9** · *Likelihood:* Medium · *Impact:* High
- *Early Warning Signal:* Pilot decisions unchanged vs. resume-first baseline; recruiter TTTM slips past weeks; HMs re-screen regardless (Experiment B).
- *Mitigation:* Deep in-workflow integration (P11); evidence-first + explainability (AS-11); calibration to the HM's real bar (AS-12); First-Five-Minutes design (DOC-06 A5).
- *Owner:* Head of Product
- *Decision Trigger:* **Pivot** — workflow/incentive redesign, or HM-first product (VALIDATION-01 §9).

**RK-7 — Company Calibration can't capture the real bar → evaluations feel generic/wrong.**
- *Source:* **AS-12** · *Likelihood:* Medium · *Impact:* High (blocks RK-5 mitigations)
- *Early Warning Signal:* Blind calibration test — HMs say output doesn't match their judgment on known candidates.
- *Mitigation:* Invest in calibration method; narrow initial scope to role families where the bar is most capturable.
- *Owner:* Head of AI
- *Decision Trigger:* If calibration can't reach HM trust → narrow scope or rework before scaling.

### 2.3 AI / TECHNICAL RISKS

**RK-8 — AI isn't expert-quality (or is too costly) for full SWE evaluation.**
- *Source:* **AS-13** (+ AS-14) · *Likelihood:* Medium · *Impact:* High
- *Early Warning Signal:* Expert-vs-AI benchmark shows a quality gap; unit cost per Candidate Evaluation breaks the pricing model (AS-23).
- *Mitigation:* Model-agnostic architecture (DOC-03 §13); narrow the wedge to the sub-task where AI *is* expert-quality, expand as capability grows; track cost per evaluation as a first-class metric.
- *Owner:* Head of AI
- *Decision Trigger:* **Pivot** — narrow the evaluation scope to where quality/cost work.

**RK-10 — Evidence is gameable (impersonation / AI-assisted cheating) → signal collapses.**
- *Source:* **AS-16** · *Likelihood:* Medium · *Impact:* High
- *Early Warning Signal:* Red-team breaks the evaluation; Integrity Score can't reliably flag gaming.
- *Mitigation:* Invest in integrity verification (authoritative capability, DOC-12 C9); design sensors resistant to gaming; red-team continuously.
- *Owner:* Head of AI
- *Decision Trigger:* If gaming dominates → redesign sensors; the "evidence > artifact" claim is at risk.

**RK-11 — The moat doesn't compound (Outcome Learning shows no gain; no outcome data at scale).**
- *Source:* **AS-15, AS-27** · *Likelihood:* Medium · *Impact:* High (long-term / moat)
- *Early Warning Signal:* Proxy test — adding outcome data doesn't improve predictive accuracy; partners won't sustain outcome-data sharing.
- *Mitigation:* Proxy-test compounding early (don't wait years); secure *ongoing* outcome-data mechanics in partnerships; treat as the defensibility bet to watch.
- *Owner:* Head of AI + CTO
- *Decision Trigger:* **Pivot** — reassess defensibility (VALIDATION-01 §9); moat story weakens.

### 2.4 GTM RISKS

**RK-12 — No internal champion / no budget sponsor.**
- *Source:* **AS-18, AS-19** · *Likelihood:* Medium · *Impact:* High
- *Early Warning Signal:* Recruiters passive or feel threatened ("will AI replace me?"); CHROs won't sponsor/fund a pilot.
- *Mitigation:* Multi-threaded selling (Rina champion + Sofia economic + David quality, DOC-08); position as augmentation not replacement (P7/C7); make the champion look good fast (relief, DOC-06 A2).
- *Owner:* Head of GTM
- *Decision Trigger:* If neither champion nor sponsor emerges across partners → rethink entry motion (HM-led or exec-led).

**RK-13 — Security/procurement blocks or slows deals beyond viability.**
- *Source:* **AS-20, AS-25** · *Likelihood:* Medium · *Impact:* Medium–High
- *Early Warning Signal:* Security reviews stall; procurement cycles run prohibitively long.
- *Mitigation:* Invest early in security posture/certifications (P8; Marcus, DOC-08); predictable pricing (KD-03.10); prepare standard security/vendor-risk answers.
- *Owner:* CTO
- *Decision Trigger:* If cycles are unviable for a startup → adjust segment/motion/pricing.

**RK-14 — Integration-first doesn't remove friction (or integration sprawl becomes a cost sink).**
- *Source:* **AS-22, AS-26** · *Likelihood:* Medium · *Impact:* Medium–High
- *Early Warning Signal:* Prototype integration shows real behavior-change friction; per-ATS integration is fragile/expensive.
- *Mitigation:* Prototype one ATS integration at a partner early; prioritize few ATSs (Greenhouse/Ashby); treat integration depth as a moat metric, not a services cost (DOC-03 §9).
- *Owner:* CTO
- *Decision Trigger:* If friction persists → rethink integration approach before scaling breadth.

### 2.5 MARKET / EXTERNAL RISKS

**RK-9 ★ — A platform giant (Microsoft/LinkedIn, Workday, Google) subsumes the intelligence layer.**
- *Source:* **AS-5** (+ AS-6) · *Likelihood:* Medium · *Impact:* **Existential (external)**
- *Early Warning Signal:* Incumbent ships credible, trusted, bundled AI-hiring; buyers say they'd accept a conflicted incumbent as judge.
- *Mitigation:* Win on neutrality + trust + focus + speed to compound the moat (DOC-03 §24); keep partnership/embedding optionality; move fast on the compounding capabilities (DOC-12 maturity roadmap).
- *Owner:* Founder/CEO
- *Decision Trigger:* **Pivot** — partnership/embedding or defensible niche depth (VALIDATION-01 §9); monitor, don't panic.

**RK-16 — Timing is wrong (too early: buyers not ready; too late: category defined by black boxes).**
- *Source:* **AS-6, AS-7** · *Likelihood:* Low–Medium · *Impact:* Medium–High
- *Early Warning Signal:* Buyer-readiness interviews show indifference; or the category is already trusted/consolidated; or regulation moves in an unbuildable direction.
- *Mitigation:* Buyer-readiness discovery early; ensure a buildable regulatory path (AS-7); be ready to re-time/re-scope.
- *Owner:* Founder/CEO + Head of Trust
- *Decision Trigger:* Re-time / re-position if the window isn't open.

### 2.6 VALIDATION-PROCESS / META RISK *(uniquely ours to manage)*

**RK-15 ★ — Confirmation bias: we count supporting evidence, ignore contradictory evidence, and "validate" a false company.**
- *Source:* **The validation framework itself** (the risk of *misusing* VALIDATION-01) · *Likelihood:* **High** (this is the default human failure mode) · *Impact:* **Existential** (it can mask any of RK-1…RK-4)
- *Early Warning Signal:* The **Counter-Evidence Register (R4) is suspiciously empty**; experiments run without pre-registration (R2); assumptions marked "Validated" on L0–L1 interview evidence (violating R3); goalposts move after results.
- *Mitigation:* Enforce **Pre-Registration (R2)**, **Evidence Quality Levels (R3)**, and the **Counter-Evidence Register (R4)**; assign someone to argue the *disconfirming* case at each checkpoint; review the Counter-Evidence Register at every validation gate.
- *Owner:* Founder/CEO + CTO (jointly — this one cannot be delegated away)
- *Decision Trigger:* If we catch ourselves rationalizing a weak result or the Counter-Evidence log stays empty → **halt and audit the validation process itself** before trusting any "validated" verdict.

---

## 3. Risk Heat Map (Likelihood × Impact)

```
                 LOW IMPACT        MEDIUM IMPACT           HIGH / EXISTENTIAL IMPACT
              ┌──────────────┬───────────────────┬──────────────────────────────────────┐
   HIGH       │              │                   │  ★ RK-15 (confirmation bias)           │
   LIKELIHOOD │              │                   │  RK-2 (no outcome data) ★              │
              ├──────────────┼───────────────────┼──────────────────────────────────────┤
   MEDIUM     │              │  RK-13 · RK-14 ·  │  ★ RK-1 · RK-3 · RK-4 · RK-9           │
   LIKELIHOOD │              │  RK-16            │  RK-5 · RK-7 · RK-8 · RK-10 · RK-11 ·  │
              │              │                   │  RK-12                                 │
              ├──────────────┼───────────────────┼──────────────────────────────────────┤
   LOW        │              │                   │  ★ RK-6 (fairness unsolvable)          │
   LIKELIHOOD │              │                   │                                        │
              └──────────────┴───────────────────┴──────────────────────────────────────┘
   ★ = existential
```

- **Top-right is where the company lives or dies.** Note **RK-15 (confirmation bias)** sits at *high likelihood × existential impact* — because misusing our own validation is the most probable way to reach a wrong "go" decision. It deserves as much vigilance as RK-1.

## 4. The Existential Six (+1) — what to watch hardest

1. **RK-2** — can we get outcome data? *(gates everything)*
2. **RK-1** — does the thesis deliver material value?
3. **RK-3** — will candidates adopt and feel it's fair?
4. **RK-4** — will anyone pay for quality?
5. **RK-6** — can fairness be legally defensible?
6. **RK-9** — will a giant subsume us?
7. **RK-15** — will we lie to ourselves about the above? *(the meta-risk)*

> These map 1:1 to VALIDATION-01's Core Thesis + meta assumptions + Kill Criteria. Everything else is important but not existential.

## 5. Decision-Trigger Summary

| If this signal trips… | …this is the pre-agreed response |
|---|---|
| RK-1 fires (no material value, no compensating value) | **KILL-1** — stop/pivot the company |
| RK-2 fires (no outcome data, incl. proxies) | **KILL-2** — cannot validate → do not proceed on faith |
| RK-3 fires (candidates won't adopt / unfair, unfixable) | **KILL-3** |
| RK-4 fires (no quality demand anywhere) | **KILL-4**; if a paid wedge exists → **Pivot** |
| RK-6 fires (fairness unsolvable) | **KILL-5** — cannot ship |
| RK-5 fires (evidence ignored) | **Pivot** — workflow/incentive or HM-first |
| RK-9 fires (giant moves) | **Pivot** — partner/embed or niche depth |
| RK-8 fires (AI quality/cost gap) | **Pivot** — narrow the wedge |
| RK-15 fires (bias detected) | **Halt & audit the validation process** before trusting any verdict |

## 6. Open Questions

1. **Who owns the Counter-Evidence Register operationally**, and who is designated "red-team" to argue the disconfirming case at each checkpoint? *(RK-15 mitigation needs a named person.)*
2. **Review cadence:** how often do we formally re-score this register against incoming evidence (weekly during active validation)?
3. **Proxy-data plan for RK-2:** concrete list of candidate public/historical datasets to de-risk the outcome-data dependency.
4. **Early-warning instrumentation:** which signals can we monitor *quantitatively* (drop-off, decision-change rate, WTP) vs. qualitatively?

---

## Summary & next step

- **KD-V02.1** — 16 risks, **each derived from a specific assumption** (VALIDATION-01); no generic/untraceable risks.
- **KD-V02.2** — **Seven existential risks** (RK-1/2/3/4/6/9 + the meta-risk RK-15), each with an Early Warning Signal and a pre-agreed Decision Trigger tied to the Kill/Pivot criteria.
- **KD-V02.3** — **RK-15 (confirmation bias) is treated as existential and high-likelihood** — the register that could most easily deceive us is our own; Pre-Registration + Evidence Levels + Counter-Evidence Register are its countermeasures.
- **KD-V02.4** — Every risk has an **Owner** and a **Decision Trigger**, so a tripped signal produces an action, not a debate.

> **Next validation artifacts** (each still derived from VALIDATION-01 assumptions): **VALIDATION-03 Design Partner Interview Guide**, then Discovery Questions, JTBD Validation Checklist, Customer Journey Validation Script, Prototype Validation Plan, Evidence Collection Framework. Recommended next: **the Interview Guide + Discovery Questions**, since AS-21 (get partners) and the interview-based tests (AS-4/AS-10/AS-18/AS-19) are the very first things we run.

*End of VALIDATION-02 v0.1 — derived from the Assumption Register, not written independently. Awaiting founder review.*
