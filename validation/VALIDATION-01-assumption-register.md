# VALIDATION-01 — Assumption Register

| Field | Value |
|---|---|
| **Document ID** | VALIDATION-01 |
| **Title** | Assumption Register (the master validation artifact) |
| **Owner** | Founder/CEO + CTO (jointly accountable) |
| **Status** | v0.2 — **Amendment A-V01.2: AS-1 de-binarized, Pre-Registration Protocol, Evidence Quality Levels, Counter-Evidence Register, three-parallel first experiments, Unknown Unknowns appendix** |
| **Created** | 2026-07-21 |
| **Phase** | **Validation Mode** — the strategic foundation (DOC-01–12) is frozen unless customer evidence proves otherwise. |
| **Depends on** | DOC-01 through DOC-12 (the entire foundation) |
| **Blocks** | Every other validation artifact (Risk Register, Interview Guide, Discovery Questions, JTBD Checklist, Journey Script, Prototype Plan, Evidence Framework) references this. **Do not begin the Risk Register until this is approved.** |
| **Purpose** | Capture every load-bearing assumption across DOC-01–12, make each **explicit, testable, and falsifiable**, and tell a founder: *"If I only have time to test ten things before building, these are the ten."* |

---

## How to read this — and the one rule

> **The rule of this register: if an assumption cannot be *falsified*, it does not belong here.** Every entry has an objective **success criterion** *and* an explicit **failure criterion**. A belief we cannot imagine being proven wrong is faith, not an assumption — and faith is not testable.

**This document is designed to be uncomfortable.** It lists, in plain language, every belief the company is betting on. If the list is alarming, that is the point — better alarmed now, at the cost of a conversation, than after building for two years.

**Validation philosophy — four outcomes, never forced binary:**
Every assumption resolves (over time) to one of: **Validated · Invalidated · Needs More Evidence · Deferred.** At this moment, *all are Unvalidated* — we have documentation, not evidence. We will not pretend otherwise, and we will not force a premature "validated."

**Defaults (to avoid repetition).** Unless a card says otherwise: **Status = Unvalidated**, **Last reviewed = 2026-07-21**. Owners are founding roles (the org is small).

**Field key per card:** *Classification · Category · Impact-if-false · Confidence-now · Cost-to-validate · Priority · Owner*, then *Why we believe it · Sources · Risk if false · Validation method / smallest experiment · Evidence required · Success criteria · Failure criteria · If validated · If invalidated.*

**Priority scale:** **P0** (test in the next 30 days) · **P1** (test during early pilots) · **P2** (after MVP) · **P3** (opportunistic/long-horizon).

---

## Amendment A-V01.2 — Five Refinements + Unknown Unknowns

*Dated 2026-07-22. CTO-ratified. Five changes that make validation more honest and more disciplined, plus a new appendix. These are authoritative where they differ from the original text.*

### R1 — AS-1 is NOT binary *(de-risking the master kill switch)*

The original AS-1 treated "evidence beats resumes" almost as True/False. Reality is graded. **A modest statistical improvement that customers *trust and adopt* can still build a huge company;** a dramatic statistical improvement no one acts on cannot. So:

> **AS-1 (reframed): Evidence-based evaluation improves hiring decisions *enough to justify adoption* — a *materially valuable* improvement in decision quality **and/or** in trust, adoption, and candidate experience — not necessarily dramatic statistical superiority.**

- **Success is "materially valuable improvement," not "perfect superiority."** Judge the *whole* value: accuracy uplift **plus** whether recruiters trust it, managers stop re-screening, and candidates value it (i.e., AS-1 is validated in concert with AS-2/AS-8/AS-9/AS-10, not in a vacuum).
- **KILL-1 accordingly reframed** (see §8): we kill only if evidence offers **no materially valuable improvement *and* no compensating trust/adoption/candidate value** — *not* merely because the accuracy delta was undramatic.
- **Threshold discipline (see R2):** we do **not** invent a number ("15% better") today. We define the *effect size qualitatively* now — *statistically credible, practically meaningful for decisions, and consistent across multiple partners* — and let an I/O psychologist + statistician set the exact numeric threshold **during pre-registration, before the study.**

### R2 — Pre-Registration Protocol *(our scientific discipline)*

**Every experiment pre-registers, before it runs.** No moving the goalposts afterward. Required fields:

| Pre-registration field | Meaning |
|---|---|
| **Hypothesis** | The specific, falsifiable claim being tested. |
| **Metric** | The single primary measure (plus any secondary). |
| **Sample Size** | Minimum N for the result to be credible (set with the statistician). |
| **Success Threshold** | The pre-agreed bar for "supported." |
| **Failure Threshold** | The pre-agreed bar for "refuted." |
| **Analysis Method** | How the data will be analyzed (chosen before seeing it). |
| **Decision Rule** | What we *do* at each outcome — decided in advance. |

> Rule: an experiment without a completed pre-registration does not start. This prevents the most common startup self-deception — reinterpreting a weak result as a win.

### R3 — Evidence Quality Levels *(not all evidence is equal)*

> **L0 Opinion → L1 Interview → L2 Observed Behavior → L3 Pilot Results → L4 Longitudinal Outcomes.**

- **Interviews (L0–L1) generate *hypotheses*; behavior (L2+) *validates* them.** You cannot "validate" an assumption on five interviews.
- **Rule: no assumption may be marked *Validated* on L0–L1 evidence alone.** Minimum evidence level per assumption type:
  - Core Thesis (AS-1, AS-2, AS-4): require **L3–L4**.
  - Candidate fairness/adoption (AS-3, AS-10): require **L2+** (observed completion/behavior, not just "candidates said they'd like it").
  - AI feasibility/fairness (AS-13, AS-17): require **L2–L3** (benchmarks/red-teams/pilots).
  - GTM/Commercial (AS-18/19/23/24): interviews (L1) *inform*; a signed pilot/purchase (L2–L3) *validates*.
- Every finding logged (incl. Counter-Evidence, R4) is tagged with its Evidence Level.

### R4 — Counter-Evidence Register *(the biggest omission — fixed)*

Startups record supporting evidence and quietly ignore contradictory evidence. We do the opposite on purpose. A **living log**, reviewed at every validation checkpoint:

| Date | Finding | Supports / **Contradicts** | Assumption(s) | Evidence Level | Action taken |
|---|---|---|---|---|---|
| *(to be populated as evidence arrives)* | | | | | |

- **Rule: disconfirming evidence is logged with *equal or greater* rigor than confirming evidence.** A suspiciously empty Contradicts column is itself a red flag (see the confirmation-bias risk in VALIDATION-02).
- Each entry forces a decision: does this move an assumption toward *Invalidated* or *Needs More Evidence*? We never let a contradiction sit unrecorded.

### R5 — The first experiments: THREE in parallel (not one retrospective)

A single retrospective tests the thesis but misses *behavior* and *candidate meaning*. Run three in parallel to de-risk faster:

| Exp | Name | Question | Tests | Evidence Level |
|---|---|---|---|---|
| **A** | **Historical Retrospective** | Can evidence separate good hires from bad, better than the resume screen did? | AS-1 | L3→L4 |
| **B** | **Recruiter Shadowing** | How do recruiters/HMs *actually* decide — vs. what they *say*? (Sit beside them.) | AS-2, AS-8, AS-9 (+ AS-1 baseline) | L2 (observed behavior) |
| **C** | **Rejected-Candidate Interviews** | What does *"fair"* actually mean to candidates who were **rejected**? | AS-10, AS-3 | L1→ (informs; pair with L2 behavior) |

> Together, A+B+C test the thesis, real decision behavior, and the mission's candidate meaning *simultaneously* — cutting risk far faster than any one alone. (Supersedes the single-retrospective framing in §5/§7.)

### Appendix — Unknown Unknowns *(not assumptions — acknowledged gaps)*

Questions we **don't yet know how to answer** — and importantly, **not** assumptions (they are not yet falsifiable beliefs). We hold them here rather than pretend they're settled or force them into the register prematurely.

- Do candidates trust **voice AI** more or less than **text**? (Unknown.)
- What evaluation *length/format* candidates tolerate before it feels burdensome? (Unknown until observed.)
- Which role families beyond SWE generalize the intelligence layer best? (Unknown.)
- How does candidate trust in AI evaluation shift as AI-in-hiring becomes normalized? (Unknown, moving target.)
- What "quality-of-hire" definition design partners will actually accept and share? (Unknown.)

> **Rule: do not promote an Unknown to an Assumption until we can state a *falsifiable belief* about it.** Unknowns generate discovery questions (VALIDATION-04); assumptions generate experiments. Keeping them separate prevents inventing false certainty.

---

## 1. Executive Summary *(read this even if you read nothing else)*

**The whole company rests on four Core-Thesis assumptions. If any one is decisively false, the company as conceived should not be built:**

- **AS-1 — Evidence predicts hiring quality better than resumes.** *The foundational bet.* If false, everything else is irrelevant. **Currently: believed on the strength of academic meta-analysis (Sackett 2022), not on our own customers' data.**
- **AS-2 — Recruiters and hiring managers will actually *act* on evidence** (change decisions), not just receive and ignore it.
- **AS-3 / AS-10 — Candidates will complete a richer evaluation *and* feel it was fair** — even when rejected.
- **AS-4 — Buyers will pay for decision *quality*, not just speed/cost.**

**The uncomfortable truths this register exposes:**
1. **We cannot even *test* AS-1 without AS-21** — securing design partners who will share on-the-job **outcome data.** That data dependency is the true first domino. *If we can't get it, we're flying blind on the entire thesis.*
2. **Our confidence is "Medium" on almost everything that matters, and "Low–Medium" on the moat itself** (AS-15 outcome-learning compounding; AS-5 durability vs. giants).
3. **The mission-defining candidate assumption (AS-10, "I had a fair chance" even when rejected) has never been tested on a single real rejected candidate.**
4. **The most expensive-to-validate assumptions (AI feasibility AS-13, fairness-to-legal-standard AS-17, outcome-learning AS-15) are also among the most critical** — we must find cheap *proxies* for them or we validate nothing until we've spent heavily.

**If you have time to test only ten things before building, test the Top 10 (§7).** The single most important experiment is a **retrospective study (AS-1)**: take a design partner's past hires with known outcomes, run blind evidence-based evaluation on those historical candidates, and check whether it separates the good hires from the bad *better than the resume screen did.* It is cheap, fast, requires no product build, and it either lights the green light for the entire company or saves us years.

> **Bottom line for the founder:** the documentation quality is high; the *evidence* is currently zero. This register is the bridge from *belief* to *proof*, and it names — bluntly — the four beliefs that, if wrong, mean we stop.

---

## 2. The Assumption Register

*Grouped by Classification. All Status = Unvalidated (2026-07-21) unless noted.*

### 2.1 CORE THESIS — *if false, the company probably should not exist*

**AS-1 — Evidence-based evaluation improves hiring decisions *enough to justify adoption* — a materially valuable improvement in decision quality **and/or** in trust, adoption, and candidate experience.** *(Reframed, A-V01.2 R1 — not binary.)*
- *Classification:* Core Thesis · *Category:* Evaluation · *Impact-if-false:* **Critical** · *Confidence:* Medium · *Cost:* **Low–Medium** · *Priority:* **P0** · *Owner:* CTO · *Min evidence level:* **L3–L4** (R3)
- *Why we believe it:* Meta-analytic evidence that structured/work-sample/skills methods out-predict resume-derived signals (Sackett 2022); the whole problem analysis.
- *Sources:* DOC-01 §3.1 (sub-bet), DOC-02 §5.1/§7/AS-1, DOC-03.
- *Risk if false:* The core thesis loses its foundation; the product may have no reason to exist (but see de-binarized kill logic, §8 KILL-1).
- *Validation / experiments:* **The three parallel experiments (A-V01.2 R5): A Historical Retrospective (does evidence separate good hires better than the resume screen?), B Recruiter Shadowing (do they act on it?), C Rejected-Candidate Interviews (is it experienced as fair?).** Pre-registered per R2. (Retrospective needs no product build.)
- *Evidence required:* Historical candidate set + real performance/retention outcomes for ≥2 partners **(L3–L4)**, plus observed decision behavior (L2) and candidate fairness signal.
- *Success criteria (effect-size-before-number, R1/R2):* the improvement is **statistically credible, practically meaningful for hiring decisions, and consistent across multiple partners** — OR the accuracy delta is modest but is accompanied by **compensating, materially valuable** trust/adoption/candidate-experience gains. Exact numeric threshold set by I/O psychologist + statistician *during pre-registration.*
- *Failure criteria:* Evidence provides **no materially valuable improvement** over resume screening **and** wins **no** compensating trust/adoption/candidate value, across partners.
- *If validated:* Green-light the thesis; proceed to build + live pilots. *If invalidated (per the de-binarized bar):* **Stop / pivot** (see KILL-1, §8, and pivots §9).

**AS-2 — Recruiters and hiring managers will *change hiring decisions* based on our evidence (act on it, not ignore it).**
- *Classification:* Core Thesis · *Category:* Customer · *Impact:* **Critical** · *Confidence:* Medium · *Cost:* Medium · *Priority:* **P0** · *Owner:* Head of Product
- *Why we believe it:* JTBD Trust/Success Moments (DOC-09); the pain is real (DOC-02).
- *Sources:* DOC-02 AS-3, DOC-09 (Rina/David).
- *Risk if false:* North Star (evidence-backed decisions) never moves; we're a report no one uses.
- *Validation / smallest experiment:* Early pilot on live reqs — compare the shortlist a recruiter/HM *would* have chosen (resume-first) vs. what they *do* choose with our evidence; measure override/adoption behavior.
- *Evidence required:* Observed decision behavior across ≥10 reqs, ≥3 partners.
- *Success criteria:* Evidence materially changes ≥a meaningful share of decisions *and* users report relying on it.
- *Failure criteria:* Users receive evidence but decisions are unchanged / they revert to resume-and-gut.
- *If validated:* Proceed. *If invalidated:* Pivot to workflow/incentive redesign or reposition (§10).

**AS-3 — Candidates will complete a richer evaluation without unacceptable drop-off.**
- *Classification:* Core Thesis · *Category:* Customer (Candidate) · *Impact:* **Critical** · *Confidence:* Medium · *Cost:* Low · *Priority:* **P0** · *Owner:* Head of Product
- *Why we believe it:* Candidates hate resume black holes and want a fair shot (DOC-02); "get a fair chance" JTBD.
- *Sources:* DOC-02 AS-4/P-C, DOC-09 (Alex).
- *Risk if false:* Top of funnel collapses; no evidence to evaluate; fairness undermined.
- *Validation / smallest experiment:* Lightweight evaluation offered to real candidates for a live role; measure completion vs. drop-off vs. resume-only baseline; segment by candidate strength.
- *Evidence required:* Completion/drop-off data for ≥100 candidates.
- *Success criteria:* Completion is high enough that funnels don't collapse; the *strongest* candidates don't drop off disproportionately.
- *Failure criteria:* Material drop-off, *especially* among strong candidates, vs. resume-only.
- *If validated:* Proceed. *If invalidated:* Redesign evaluation weight/length; if unfixable, core mission at risk.

**AS-4 — Buyers will pay for decision *quality*, not just speed/cost.**
- *Classification:* Core Thesis · *Category:* Commercial · *Impact:* **Critical** · *Confidence:* Medium · *Cost:* Low · *Priority:* **P0** · *Owner:* Founder/CEO
- *Why we believe it:* The largest cost is the invisible wrong-decision cost (DOC-02 §6); trust-first positioning (DOC-03).
- *Sources:* DOC-02 AS-2/§12, DOC-03.
- *Risk if false:* We're forced to compete as a commoditized efficiency tool — an incumbent-favoring game we lose.
- *Validation / smallest experiment:* Buyer willingness-to-pay interviews + a pricing test framed on decision quality vs. efficiency.
- *Evidence required:* WTP signals from ≥15 buyers (VP TA / CHRO).
- *Success criteria:* Buyers articulate quality/defensibility as a paid priority and accept quality-based pricing.
- *Failure criteria:* Buyers only value speed/cost; won't pay a premium for quality/defensibility.
- *If validated:* Proceed with quality pricing. *If invalidated:* Pivot wedge to a felt-and-paid problem while delivering quality underneath (DOC-02 §12).

### 2.2 MARKET / TRUST

**AS-5 — The neutral intelligence-layer position is durable; platform giants/ATS won't trivially subsume it within our window.**
- *Classification:* Market · *Category:* Market · *Impact:* **Critical** · *Confidence:* **Low–Medium** · *Cost:* **High** (plays out over years) · *Priority:* **P2** · *Owner:* Founder/CEO
- *Why we believe it:* Neutrality is structurally unavailable to conflicted incumbents; moat compounds (DOC-03 §2/§13/§24).
- *Sources:* DOC-03 §12/§13/§24 (SR-1/2/3), MR-11.
- *Risk if false:* A giant (Microsoft/LinkedIn, Workday) bundles "good-enough" and erases the market (existential platform risk).
- *Validation / smallest experiment:* Ongoing competitive intelligence; watch incumbent AI-hiring roadmaps, acquisitions, betas; test whether buyers *would* trust a conflicted incumbent as a neutral judge (interview question).
- *Evidence required:* Incumbent roadmap signals + buyer trust preferences.
- *Success criteria:* Buyers express preference for a neutral, non-ATS judge; incumbents remain slow/conflicted.
- *Failure criteria:* A giant ships credible, trusted, bundled hiring intelligence at speed.
- *If validated:* Continue independent path. *If invalidated:* Pivot toward partnership/acquisition posture or defensible niche depth (§10).

**AS-6 — The "why now" window (AI capability + resume-signal collapse + regulation + trust vacuum) is real and open.**
- *Classification:* Market · *Category:* Market · *Impact:* High · *Confidence:* Medium–High · *Cost:* Low · *Priority:* P1 · *Owner:* Founder/CEO
- *Why we believe it:* DOC-02 §9 (five converging vectors), current adoption data.
- *Sources:* DOC-02 §8/§9.
- *Risk if false:* Either too early (buyers not ready) or too late (category defined by black-boxes).
- *Validation / smallest experiment:* Buyer-readiness interviews ("are you actively shopping for AI hiring? what do you distrust?").
- *Success criteria:* Buyers are actively evaluating AI hiring *and* distrust black boxes (our wedge). *Failure:* Indifference, or the category already trusted/consolidated.
- *If validated:* Move fast. *If invalidated:* Re-time / re-position.

**AS-7 — Regulation (LL144, EU AI Act, etc.) is navigable and becomes a moat, not a blocker.**
- *Classification:* Trust · *Category:* Trust · *Impact:* High · *Confidence:* Medium · *Cost:* Medium · *Priority:* P1 · *Owner:* Head of Trust/Compliance (+ external counsel)
- *Why we believe it:* Fairness/explainability gates align with regulation; regulation punishes black boxes (DOC-02 §9, DOC-05).
- *Sources:* DOC-02 §9, DOC-05 P1/P13.
- *Risk if false:* Compliance cost/complexity exceeds a startup's capacity, or rules forbid our approach.
- *Validation / smallest experiment:* Legal review of LL144/EU AI Act against our approach; talk to buyers' Legal/Compliance about what would satisfy them.
- *Success criteria:* A clear, buildable compliance path; buyers' Legal say our gates would satisfy them. *Failure:* Requirements are unmeetable at our stage or contradict the model.
- *If validated:* Compliance = moat. *If invalidated:* Re-scope jurisdictions/approach.

### 2.3 PRODUCT

**AS-8 — Recruiters reach their Trust Moment (trust an evidence-first shortlist) within *days*.**
- *Classification:* Product · *Category:* Product · *Impact:* High · *Confidence:* Medium · *Cost:* Low–Med · *Priority:* **P0** · *Owner:* Head of Product
- *Why:* DOC-09 A-3 TTTM target; DOC-11 J-2. *Sources:* DOC-09/DOC-11.
- *Risk if false:* Champion motion breaks before internal selling starts; adoption dies (DOC-11).
- *Smallest experiment:* Early pilot; measure days-to-first-accepted-shortlist and recruiter-reported trust.
- *Success:* Recruiters trust and defend a shortlist within the first week. *Failure:* Trust takes weeks/months or never comes.
- *If validated:* Proceed. *If invalidated:* Redesign onboarding/first-five-minutes; investigate why.

**AS-9 — Hiring managers stop re-screening once they trust the evidence.**
- *Classification:* Product · *Category:* Product · *Impact:* High · *Confidence:* **Low–Medium** · *Cost:* Medium · *Priority:* P1 · *Owner:* Head of Product
- *Why:* DOC-09 J-3 (David). *Risk if false:* No efficiency/quality gain realized; HM remains bottleneck.
- *Smallest experiment:* In pilots, measure HM re-screening behavior over successive hires.
- *Success:* HMs measurably reduce re-screening as trust builds. *Failure:* HMs keep re-screening regardless.
- *If validated:* Proceed. *If invalidated:* Pivot to HM-first product/experience.

**AS-10 — Candidates feel "I had a fair chance" — *even when rejected*.** *(the mission-defining assumption)*
- *Classification:* Product/Trust · *Category:* Customer (Candidate) · *Impact:* **Critical (mission)** · *Confidence:* Medium · *Cost:* Low · *Priority:* **P0** · *Owner:* Head of Product
- *Why:* DOC-06 (respect/relief), DOC-09 (Alex Success Moment), DOC-11 (J-1).
- *Risk if false:* The mission fails ethically *and* commercially (brand/network damage; the Afterlife flywheel reverses).
- *Smallest experiment:* Run real candidates (incl. rejected) through an evaluation + feedback; survey/interview on perceived fairness.
- *Evidence required:* Fairness-perception data from ≥50 candidates, *including rejected ones*.
- *Success:* A strong majority — *including rejected candidates* — report it felt fair. *Failure:* Rejected candidates feel judged unfairly / dismissed by a machine.
- *If validated:* Core mission validated. *If invalidated:* Redesign the evaluation & rejection experience; if unfixable, the mission is in question.

**AS-11 — Explainability (evidence-first) increases trust more than a bare score would.**
- *Classification:* Product · *Category:* Trust · *Impact:* High · *Confidence:* Medium–High · *Cost:* Low · *Priority:* P1 · *Owner:* Head of Product
- *Why:* DOC-06 §5, DOC-05 P1/P13. *Risk if false:* Our core differentiator (explainability) adds cost without trust payoff.
- *Smallest experiment:* Comparison test — same recommendation with evidence-first explanation vs. bare score; measure user trust/adoption.
- *Success:* Evidence-first materially increases trust vs. bare score. *Failure:* No difference / users just want the number.
- *If validated:* Double down on explainability. *If invalidated:* Reconsider effort allocation (but note regulatory floor still requires explainability).

**AS-12 — Company Calibration can capture a company's/manager's *real bar* well enough to be trusted.**
- *Classification:* Product · *Category:* Product/AI · *Impact:* High · *Confidence:* Medium · *Cost:* Medium · *Priority:* **P0** · *Owner:* Head of AI
- *Why:* Calibration is a dependency of trusted evaluation (DOC-09/DOC-12). *Risk if false:* Evaluations feel generic/wrong; HMs reject them (blocks AS-8/AS-9).
- *Smallest experiment:* Calibration sessions with HMs; blind-test whether calibrated evaluations match the HM's own judgment on known candidates.
- *Success:* HMs agree calibrated output reflects their bar. *Failure:* Output feels generic or misaligned.
- *If validated:* Proceed. *If invalidated:* Invest in calibration method or narrow scope.

### 2.4 AI

**AS-13 — AI can produce expert-quality, fair, explainable evaluations for SWE roles at *acceptable cost*.**
- *Classification:* AI · *Category:* AI/Evaluation · *Impact:* **Critical** · *Confidence:* Medium · *Cost:* **High** (needs build) · *Priority:* P1 · *Owner:* Head of AI
- *Why:* AI capability inflection (DOC-02 §8). *Risk if false:* The solution is infeasible/uneconomic even if the thesis is true.
- *Smallest experiment:* Technical spike — benchmark AI evaluations against expert human evaluations on a sample role; measure quality, fairness, cost per Candidate Evaluation.
- *Evidence required:* Expert-vs-AI benchmark on ≥1 role family.
- *Success:* AI matches/approaches expert quality, passes fairness checks, at a unit cost that supports pricing (KD-03.10). *Failure:* Quality gap, bias, or cost too high.
- *If validated:* Build. *If invalidated:* Re-scope role/depth or reconsider feasibility.

**AS-14 — Confidence calibration is reliable enough that "low confidence" is a trustworthy, useful signal.**
- *Classification:* AI · *Category:* AI/Trust · *Impact:* Medium–High · *Confidence:* Medium · *Cost:* Medium · *Priority:* P1 · *Owner:* Head of AI
- *Why:* Honest uncertainty is core to trust (DOC-06 §3.4). *Risk if false:* "Confidence" misleads; honesty backfires.
- *Smallest experiment:* Check whether stated confidence correlates with actual accuracy on a labeled set.
- *Success:* Confidence tracks accuracy (well-calibrated). *Failure:* Confidence is noise.
- *If validated:* Surface confidence. *If invalidated:* Rework or suppress confidence claims.

**AS-15 — Outcome Learning measurably improves recommendations over time (the loop actually compounds).**
- *Classification:* AI · *Category:* Evaluation · *Impact:* High (**the moat**) · *Confidence:* **Low–Medium** · *Cost:* **High** (needs time + data) · *Priority:* P2 · *Owner:* Head of AI
- *Why:* The compounding-moat thesis (DOC-03 §13/§17, DOC-09 A-4). *Risk if false:* The moat is weaker than claimed; we're more copyable.
- *Smallest experiment:* Proxy — retrospective test whether adding outcome data improves predictive accuracy on held-out cases (before waiting years of live data).
- *Success:* Recommendations improve as outcomes accrue. *Failure:* No improvement from outcome data.
- *If validated:* The moat is real. *If invalidated:* Reassess defensibility (§10 pivot).

**AS-16 — Integrity verification can detect gaming/impersonation/AI-misuse well enough to keep evidence trustworthy.**
- *Classification:* AI · *Category:* Trust · *Impact:* High · *Confidence:* **Low–Medium** · *Cost:* High · *Priority:* P2 · *Owner:* Head of AI
- *Why:* Integrity Score / anti-fraud (DOC-04, DOC-02 fraud data). *Risk if false:* Evidence is gameable → signal collapses (the resume problem returns).
- *Smallest experiment:* Red-team the evaluation with gaming/impersonation/AI-assisted cheating; measure detection.
- *Success:* Detection is good enough that gaming doesn't dominate. *Failure:* Easily gamed; integrity unreliable.
- *If validated:* Proceed. *If invalidated:* Redesign sensors/verification; the "evidence > artifact" claim weakens.

**AS-17 — Fairness/adverse-impact can be controlled to a *legally-defensible* standard.**
- *Classification:* AI · *Category:* Trust · *Impact:* **Critical** · *Confidence:* Medium · *Cost:* **High** · *Priority:* P1 · *Owner:* Head of Trust/Compliance + Head of AI
- *Why:* Fairness gate (DOC-05 P1); legal necessity (DOC-02 §9). *Risk if false:* Existential legal/brand exposure; can't sell.
- *Smallest experiment:* Adverse-impact testing on evaluation outputs across protected groups (with I/O-psych/legal input) on sample data.
- *Success:* Outputs meet adverse-impact standards (e.g., four-fifths) with role-relevant justification. *Failure:* Persistent disparate impact we can't justify/remove.
- *If validated:* Proceed. *If invalidated:* This is close to a kill (fairness is a gate) — must be solved before shipping.

### 2.5 GTM

**AS-18 — VP TA / recruiters can and will become internal champions.**
- *Classification:* GTM · *Category:* GTM · *Impact:* High · *Confidence:* Medium · *Cost:* Low · *Priority:* **P0** · *Owner:* Head of GTM
- *Why:* Buyer map (DOC-03 KD-03.11, DOC-08 Rina). *Risk if false:* No internal engine to drive adoption.
- *Smallest experiment:* Design-partner conversations — do recruiters lean in and offer to champion?
- *Success:* Recruiters volunteer to run pilots and sell internally. *Failure:* Recruiters are passive or threatened (AS "will AI replace me?").
- *If validated:* Champion-led GTM. *If invalidated:* Rethink entry motion (maybe HM-led or exec-led).

**AS-19 — CHROs will sponsor and *fund* pilots.**
- *Classification:* GTM · *Category:* GTM/Commercial · *Impact:* High · *Confidence:* Medium · *Cost:* Low · *Priority:* **P0** · *Owner:* Founder/CEO
- *Why:* CHRO = economic approver (KD-03.11, DOC-08 Sofia). *Risk if false:* No budget path.
- *Smallest experiment:* Exec conversations with CHROs on sponsorship & budget.
- *Success:* CHROs express willingness to sponsor + budget a pilot. *Failure:* No budget/priority.
- *If validated:* Proceed. *If invalidated:* Find alternative budget owner / motion.

**AS-20 — Security teams (CISO/IT) approve within acceptable timelines.**
- *Classification:* GTM · *Category:* Operational/GTM · *Impact:* High · *Confidence:* Medium · *Cost:* Medium · *Priority:* P1 · *Owner:* CTO
- *Why:* Marcus veto (DOC-08). *Risk if false:* Deals die in security review; sales cycle unviable.
- *Smallest experiment:* Walk 3–5 security teams through our (planned) isolation/data model; time-to-comfort.
- *Success:* Security teams see a clearable path in acceptable time. *Failure:* Chronic security blocking.
- *If validated:* Proceed. *If invalidated:* Invest early in security posture / certifications.

**AS-21 — We can secure 20–30 design partners who will share on-the-job *outcome data*.** *(the meta-assumption — everything depends on it)*
- *Classification:* GTM · *Category:* Operational/GTM · *Impact:* **Critical** · *Confidence:* **Low–Medium** · *Cost:* **Low** (just go ask) · *Priority:* **P0 (first)** · *Owner:* Founder/CEO
- *Why:* Design-partner strategy (DOC-03 §21). *Risk if false:* **We cannot validate AS-1** — we can't even learn whether the thesis is true.
- *Smallest experiment:* Directly recruit design partners *now*; explicitly ask for outcome-data sharing in the agreement.
- *Success:* ≥ a handful of partners commit, including outcome-data sharing. *Failure:* Companies won't share outcomes (privacy/effort/legal).
- *If validated:* Validation program can run. *If invalidated:* **Near-kill** — find proxy data (public datasets, historical) or the whole validation program stalls (§9).

**AS-22 — Integration-first genuinely removes adoption friction (no behavior change needed).**
- *Classification:* GTM · *Category:* Product/GTM · *Impact:* High · *Confidence:* Medium · *Cost:* Medium · *Priority:* P1 · *Owner:* CTO
- *Why:* DOC-01/DOC-03 §9 (never change how you work). *Risk if false:* Adoption friction we claimed to avoid reappears.
- *Smallest experiment:* Prototype an integration with one ATS (Greenhouse/Ashby) at a design partner; observe adoption friction.
- *Success:* Adoption requires no meaningful behavior change. *Failure:* Users must change workflows to get value.
- *If validated:* Proceed. *If invalidated:* Rethink integration approach.

### 2.6 COMMERCIAL

**AS-23 — Customers accept per-Candidate-Evaluation pricing (and it doesn't suppress evaluation volume).**
- *Classification:* Commercial · *Category:* Commercial · *Impact:* High · *Confidence:* Medium · *Cost:* Low · *Priority:* P1 · *Owner:* Founder/CEO
- *Why:* KD-03.10 pricing + data-flywheel guardrail (DOC-03 §19). *Risk if false:* Pricing model misaligns or starves the flywheel.
- *Smallest experiment:* Pricing interviews + willingness-to-pay tests on the per-Candidate-Evaluation unit.
- *Success:* Buyers accept the unit *and* wouldn't ration evaluations because of it. *Failure:* Resistance, or they'd evaluate fewer candidates to save cost.
- *If validated:* Proceed. *If invalidated:* Revisit pricing model.

**AS-24 — Demonstrable ROI (reduced bad-hire cost + efficiency) compellingly exceeds evaluation cost.**
- *Classification:* Commercial · *Category:* Commercial · *Impact:* High · *Confidence:* Medium · *Cost:* Medium · *Priority:* P1 · *Owner:* Founder/CEO
- *Why:* DOC-02 §6 cost model. *Risk if false:* No compelling business case; churn.
- *Smallest experiment:* Build an ROI model with a design partner using *their* numbers; test whether it's compelling.
- *Success:* Partner-verified ROI is clearly compelling. *Failure:* ROI is marginal or unmeasurable.
- *If validated:* Proceed. *If invalidated:* Rethink value story / target.

**AS-25 — The buying process fits mid-market/enterprise procurement (cycle length acceptable).**
- *Classification:* Commercial · *Category:* Commercial/GTM · *Impact:* Medium–High · *Confidence:* Medium · *Cost:* Low · *Priority:* P2 · *Owner:* Head of GTM
- *Why:* Buyer map + beachhead (DOC-03). *Risk if false:* Sales cycles too long for a startup.
- *Smallest experiment:* Map real procurement steps with 3–5 mid-market buyers.
- *Success:* Viable cycle length + predictable steps. *Failure:* Procurement is prohibitively slow/complex.
- *If validated:* Proceed. *If invalidated:* Adjust segment/motion/pricing.

### 2.7 OPERATIONAL

**AS-26 — We can integrate with major ATSs at acceptable cost/maintenance.**
- *Classification:* Operational · *Category:* Operational · *Impact:* Medium–High · *Confidence:* Medium–High · *Cost:* Medium · *Priority:* P2 · *Owner:* CTO
- *Why:* DOC-06 integration strategy. *Risk if false:* Integration sprawl becomes a cost/quality sink.
- *Smallest experiment:* Build one real integration; measure effort + fragility.
- *Success:* Bounded, maintainable. *Failure:* Fragile/expensive per ATS.
- *If validated:* Scale integrations. *If invalidated:* Prioritize few ATSs / rethink approach.

**AS-27 — We can reliably acquire outcome/performance data (HRIS reference) at scale over time.**
- *Classification:* Operational · *Category:* Operational · *Impact:* High (moat/learning) · *Confidence:* **Low** · *Cost:* High · *Priority:* P2 · *Owner:* CTO
- *Why:* Outcome Learning depends on it (DOC-12 C21/C22). *Risk if false:* The learning loop/moat can't run at scale even if AS-21 gets pilot data.
- *Smallest experiment:* With pilot partners, test the actual mechanics/willingness of ongoing outcome-data sharing.
- *Success:* Sustainable outcome-data flow. *Failure:* One-off only; no ongoing loop.
- *If validated:* Moat feasible. *If invalidated:* The compounding thesis weakens (relates to AS-15).

---

## 3. Assumption Dependency Graph

Many assumptions **only matter if upstream ones hold.** Don't burn time validating downstream ideas before the foundation. *(→ means "is a precondition for / must hold first.")*

```
                         AS-21  (can we get design partners + OUTCOME DATA?)
                            │  ── the true first domino; without it we can't test AS-1 at all
                            ▼
                         AS-1   (evidence predicts hiring quality > resumes)   ◀── AS-13 (AI can produce quality evals)
                            │                                                   ◀── AS-17 (fairness controllable)
                            │                                                   ◀── AS-16 (integrity holds)
                            ▼
        ┌───────────────────┼───────────────────────────┐
        ▼                   ▼                             ▼
  AS-3/AS-10          AS-2  (people ACT on evidence)   AS-12 (calibration captures the bar)
 (candidates adopt        │                                 │
  + feel fair)            ▼                                 ▼
        │            AS-8 (recruiter trust)  ─────▶  AS-9 (HMs stop re-screening)
        │                 │                                 │
        └────────┬────────┘                                 │
                 ▼                                           ▼
            AS-11 (explainability→trust)              AS-24 (ROI compelling)
                 │                                           │
                 ▼                                           ▼
            AS-4 / AS-23  (pay for quality / accept pricing)
                 │
                 ▼
            AS-19 (CHRO funds) ─▶ AS-20 (security clears) ─▶ AS-25 (procurement fits) ─▶ RENEWAL/EXPANSION
                 
  Longer-horizon / moat (only matter if the above hold):
     AS-15 (outcome learning compounds) · AS-27 (outcome data at scale) · AS-5 (durable vs. giants) · AS-7 (regulation=moat)
  Context (gates the opportunity):
     AS-6 (why-now window) · AS-26 (ATS integration feasible) · AS-22 (integration removes friction) · AS-18 (recruiters champion)
```

- **The critical reading:** **AS-21 → AS-1** is the spine's root. **If we cannot get outcome data (AS-21), we cannot test the thesis (AS-1), and nothing downstream is worth validating yet.** Every dollar of validation effort should start at the top of this graph.

---

## 4. Prioritization Matrix (Impact-if-false × Cost-to-validate)

> **Rule: High-Impact + Low-Cost is always tested first.**

```
                    LOW COST TO VALIDATE                 HIGH COST TO VALIDATE
             ┌───────────────────────────────────┬───────────────────────────────────┐
   CRITICAL/ │  ★ TEST FIRST (P0)                 │  TEST CAREFULLY / PROXY (P1–P2)    │
   HIGH      │  AS-21 · AS-1 · AS-3 · AS-10 ·      │  AS-13 (AI feasibility) · AS-17    │
   IMPACT    │  AS-4 · AS-2 · AS-8 · AS-19 ·       │  (fairness→legal) · AS-15 (outcome │
             │  AS-18 · AS-11 · AS-23 · AS-12*     │  learning) · AS-5 (durability) ·   │
             │                                     │  AS-27 (outcome data scale) · AS-9 │
             ├───────────────────────────────────┼───────────────────────────────────┤
   LOW/MED   │  DO OPPORTUNISTICALLY (P2)          │  DEPRIORITIZE (P2–P3)              │
   IMPACT    │  AS-6 · AS-25                       │  AS-26 · AS-7 · AS-14 · AS-16 ·    │
             │                                     │  AS-20 · AS-22 · AS-24             │
             └───────────────────────────────────┴───────────────────────────────────┘
   *AS-12 cost is medium; placed with P0 because it blocks AS-8/AS-9.
```

- **Top-left is the goldmine:** critical assumptions that are cheap to test. **Start there. Always.**
- **Top-right is the trap:** critical *and* expensive — find cheap **proxies** (retrospective data, red-teams, benchmarks) rather than building the whole thing to learn.

---

## 5. Recommended Validation Order

1. **AS-21** — recruit design partners *and* secure outcome-data sharing. *(Gate to everything.)*
2. **AS-1** — the **three parallel experiments** (A Historical Retrospective, B Recruiter Shadowing, C Rejected-Candidate Interviews; A-V01.2 R5), pre-registered. *(The thesis + behavior + candidate meaning.)*
3. **AS-10 / AS-3** — candidate fairness perception + completion (interviews + light eval).
4. **AS-4 / AS-23 / AS-24** — buyer WTP, pricing, ROI (interviews).
5. **AS-2 / AS-8** — do recruiters/HMs act on evidence and trust it fast (early pilot).
6. **AS-12** — calibration captures the real bar (HM sessions).
7. **AS-11** — explainability vs. bare-score trust test.
8. **AS-18 / AS-19** — champion + CHRO sponsorship (sales conversations).
9. **AS-13 / AS-17** (proxy) — AI feasibility + fairness benchmarks (technical spike). 
10. Then: AS-20, AS-22, AS-6, AS-25; later AS-15, AS-16, AS-27, AS-5, AS-7, AS-14, AS-26.

## 6. Assumptions that can wait until AFTER MVP

- **AS-15** (outcome learning compounds) — needs longitudinal data; proxy-test only for now.
- **AS-27** (outcome data at scale) — post-pilot operational question.
- **AS-5** (durability vs. giants) — plays out over years; monitor, don't "test."
- **AS-7** (regulation → moat) — ongoing; ensure a buildable path, defer full proof.
- **AS-16** (integrity at scale) — red-team early, but scale-hardening is post-MVP.
- **AS-25 / AS-26** (procurement fit / ATS breadth) — emerge with the motion.
- **AS-14** (confidence calibration) — refine during build.

## 7. Top 10 to Test in the Next 30 Days

*If you can only test ten things before building, these are the ten.*

| # | Assumption | Why now | Smallest experiment | Green light if… |
|---|---|---|---|---|
| 1 | **AS-21** design partners + outcome data | Gate to everything | Go recruit; ask for outcome-sharing | Several commit incl. outcome data |
| 2 | **AS-1** evidence improves decisions enough to adopt | The thesis | 3 parallel experiments (A retrospective · B recruiter shadowing · C rejected-candidate interviews) | Materially valuable improvement — in accuracy and/or trust/adoption/candidate value |
| 3 | **AS-10** candidates feel fair (incl. rejected) | The mission | Candidate eval + fairness survey | Majority incl. rejected say "fair chance" |
| 4 | **AS-3** candidate completion | Funnel viability | Completion vs. resume-only baseline | No collapse; strong candidates don't drop |
| 5 | **AS-4** pay for quality | Business model | Buyer WTP interviews | Buyers pay a premium for quality/defensibility |
| 6 | **AS-2** act on evidence | North Star | Pilot decision-behavior observation | Evidence changes decisions |
| 7 | **AS-8** recruiter trust in days | Champion motion | Early pilot TTTM measurement | Trust within week 1 |
| 8 | **AS-19** CHRO funds pilots | Budget path | Exec conversations | CHROs commit to sponsor/fund |
| 9 | **AS-12** calibration captures the bar | Blocks HM trust | Blind calibration test with HMs | HMs agree it reflects their bar |
| 10 | **AS-11** explainability → trust | Core differentiator | Evidence-first vs. bare-score test | Evidence-first wins trust |

## 8. Kill Criteria for the Company

*The founder should know exactly what would mean "stop." Stated bluntly:*

- **KILL-1 — AS-1 decisively invalidated (de-binarized, A-V01.2 R1).** If, after the three parallel experiments *and* early pilots across multiple partners, evidence-based evaluation offers **no materially valuable improvement** over resume screening **AND** wins **no** compensating trust/adoption/candidate value → **the company as conceived should not be built.** *Note: a modest-but-trusted-and-adopted improvement is NOT a kill — it may still be a large company.* This is the master kill switch, but it fires on *total value*, not on statistical drama.
- **KILL-2 — AS-21 unattainable.** If **no** company will share outcome data (proxy sources also fail) → we **cannot validate the thesis** → do not proceed on faith. (A "we can't even learn" kill.)
- **KILL-3 — AS-3/AS-10 invalidated at scale.** If candidates **won't complete** evaluations or **consistently experience them as unfair** (esp. rejected candidates), and it proves unfixable → the mission and funnel both fail.
- **KILL-4 — AS-4 invalidated.** If buyers will **only** pay for speed/cost and **never** for decision quality, across the segment → there is no business for *this* product (would force becoming a commoditized efficiency tool we said we won't be).
- **KILL-5 — AS-17 unsolvable.** If fairness/adverse-impact **cannot** be brought to a legally-defensible standard → we cannot ship in our markets (a gate we can't clear).

> Note: KILL-1 and KILL-2 are the ones to confront in the next 30–90 days. The rest are slower but no less real.

## 9. Pivot Triggers *(not kill — change course)*

- **AS-2 weak, AS-1 holds** → evidence has signal but people won't act: pivot to workflow/incentive redesign, or a format that forces engagement with evidence.
- **AS-4 partial** (pay for speed, not quality) → pivot the *wedge* to a severe-and-paid problem (screening speed/volume) while delivering quality underneath (DOC-02 §12); keep the mission as the deeper value.
- **AS-9 weak, AS-8 holds** → recruiters trust it but HMs still re-screen: pivot to an HM-first experience.
- **AS-5 weakening** (a giant moves fast) → pivot toward partnership/embedding or a defensible niche depth (DOC-03 §24).
- **AS-23 nuance** (per-eval pricing suppresses volume) → pivot pricing to platform-fee-heavy to protect the data flywheel.
- **AS-13 gap** (AI not expert-quality yet for full eval) → narrow the wedge to the sub-task where AI *is* expert-quality; expand as capability grows.

## 10. Open Questions

1. ~~What numeric threshold for AS-1?~~ → **Resolved (A-V01.2 R1/R2): effect-size-before-number.** Success is defined qualitatively now (statistically credible, practically meaningful, consistent across partners, *or* modest-but-compensated-by-trust/adoption); the exact numeric threshold is set by an **I/O psychologist + statistician during pre-registration**, before the study. *(Still needs: engage that advisor.)*
2. **Proxy data for AS-1 if AS-21 is slow:** are there usable public/historical datasets to begin testing evidence-vs-outcome before partners commit?
3. **Who is accountable for each validation experiment operationally** (beyond the "Owner" role here) once partners are engaged?
4. **How do we run candidate-fairness testing (AS-10) ethically** — real candidates deserve real value, not to be experimented on. (A P7 obligation even in validation.)
5. **What sample sizes make each result credible vs. anecdotal?** (Set minimums per experiment.)

---

## Summary & next step

- **KD-V01.1** — 27 load-bearing assumptions captured, each falsifiable with explicit success *and* failure criteria; all currently **Unvalidated**.
- **KD-V01.2** — **Four Core-Thesis assumptions (AS-1, AS-2, AS-3/AS-10, AS-4)** gate the company's right to exist; **AS-21 (outcome data) is the meta-prerequisite** to testing them.
- **KD-V01.3** — Validation starts **top-left of the matrix** (high-impact, low-cost) and **top-of-graph** (AS-21 → AS-1); expensive-critical assumptions get **proxies**, not full builds.
- **KD-V01.4** — **Five explicit Kill Criteria** and **six Pivot Triggers** are on the record; the founder now knows what "stop" and "change course" look like.

> **This register is the master validation artifact.** Per CTO instruction, **the Risk Register (VALIDATION-02) will not begin until this is reviewed and approved.** Once approved, the remaining validation artifacts (Interview Guide, Discovery Questions, JTBD Checklist, Journey Script, Prototype Plan, Evidence Framework) each trace back to the assumptions and priorities defined here.

*End of VALIDATION-01 v0.1 — intentionally uncomfortable. If it didn't make the risks vivid, it failed. Awaiting founder review and approval before proceeding.*
