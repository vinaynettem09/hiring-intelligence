# VALIDATION-04 — Design Partner Validation Kit

| Field | Value |
|---|---|
| **Document ID** | VALIDATION-04 |
| **Title** | Design Partner Validation Kit (the operational package to test AS-1 with zero build) |
| **Owner** | Founder/CEO + Head of Research (I/O psychology) + Product |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-23 |
| **Type** | **Operational validation kit — NOT architecture, NOT product.** Executes the program defined in VALIDATION-01/02/03. |
| **Depends on** | VALIDATION-01 (Assumption Register — AS-1, pre-registration, evidence levels, counter-evidence, kill criteria), VALIDATION-02 (Risk Register — esp. RK-1, RK-2, RK-15), VALIDATION-03 (Research Playbook — persona guides, interview rules), DOC-02 (research grounding), DOC-06 (candidate dignity) |
| **The one question** | **"Does evidence-based evaluation predict hiring outcomes materially better than resume-first screening — enough to justify adoption — and can we prove it to ourselves without fooling ourselves?"** |
| **Hard rule** | **Zero build.** No product, no code, no AI. This tests the *thesis*, not the platform. If the thesis fails, we learn it in weeks and cheaply — before Sprint 1. |
| **The adversary** | **RK-15 — our own confirmation bias.** This kit is designed first to make us *right about reality*, not right about our idea. Its success condition includes the possibility of discovering we are **wrong**. |

> **How to use this kit.** Read §0–§2 (what we're testing and the anti-bias protocol), pre-register each experiment (§2) with an I/O psychologist + statistician **before collecting any data**, recruit partners (§4–§5), run the three parallel experiments (§3, §6–§9), analyze against pre-committed criteria (§10–§12), log disconfirming evidence continuously (§13), and route the outcome through governance (§16). Templates are in the appendices and inline — they are meant to be copied and used.

---

## 0. Purpose, Scope & the Evidence Bar

**Purpose.** Produce **decision-grade evidence** on AS-1 fast and cheaply, before committing engineering effort. This kit is the execution layer for the "3 parallel zero-build experiments" mandated in VALIDATION-01 (A-V01.2).

**Scope.** Test the *hypothesis* (evidence beats resumes for predicting outcomes, and stakeholders will trust/adopt it, and candidates find it fairer). **Out of scope:** building anything; validating the specific UI/flows (PRODUCT-01); scaling.

**The evidence bar (VALIDATION-01 Evidence Quality Levels).** We rank every finding:
- **L0 Opinion** — "recruiters say resumes are bad." *Nearly worthless alone.*
- **L1 Stated Interview** — "a VP Eng says they'd trust work samples." *Weak; intention ≠ behavior.*
- **L2 Observed Behavior** — we watched what they actually did / decided. *Moderate.*
- **L3 Pilot Signal** — a small real-world test with a real decision. *Strong.*
- **L4 Longitudinal Outcome** — evidence-based scores correlate with real on-the-job outcomes over time. *Decisive.*

> **Rule (from A-V01.2):** AS-1 **cannot** be "validated" on L0–L1 alone. The retrospective study (Exp A) is our path toward **L4-adjacent** evidence; interviews (Exp C) and shadowing (Exp B) are **L2** and triangulate. A confident conclusion requires **convergence across experiments at L2+**, anchored by Exp A.

---

## 1. The Hypothesis Under Test

### 1.1 AS-1, stated precisely (de-binarized per A-V01.2)
> **AS-1:** *Structured, evidence-based evaluation of a candidate's actual work predicts hiring outcomes (on-the-job performance and retention) **materially better** than resume-first screening — by a margin large enough, across accuracy and/or trust and/or candidate value, to justify a company adopting it.*

**"Materially better" is not a p-value.** Per A-V01.2, success = *"a materially valuable improvement, enough to justify adoption."* It is judged across **three dimensions** (any of which, sufficiently strong, can carry adoption — §10):
1. **Predictive validity** — does evidence-based scoring correlate with real outcomes better than resume-based screening did?
2. **Trust & adoption** — would the quality authority (VP Eng) and champion (Head of TA) actually change a decision based on it, and buy it?
3. **Candidate value & fairness** — do candidates experience it as fairer and more respectful (supporting the network/brand thesis)?

### 1.2 Sub-hypotheses (each independently testable)
- **H1 (validity):** Blind evidence-based re-scores of past candidates correlate with actual outcomes **more strongly** than the original resume-first screen did. *(Exp A)*
- **H2 (resume noise):** Resume-first screening systematically **mis-ranks** candidates vs. outcomes (false negatives who succeeded elsewhere; false positives who failed). *(Exp A, C)*
- **H3 (behavioral trust):** When shown evidence, hiring managers/recruiters **change or strengthen** decisions they'd have made on resumes. *(Exp B — observed, L2)*
- **H4 (candidate value):** Rejected candidates report resume screening as opaque/unfair and evidence-based evaluation as fairer — and would re-engage. *(Exp C)*
- **H5 (bias):** Resume signals correlate with demographic-adjacent proxies (name, school, employer) more than evidence does (Bertrand & Mullainathan grounding). *(Exp A, exploratory)*

### 1.3 Effect-size-before-number (RK-15 defense)
> **We do NOT pick a target number after seeing data.** Before any data collection, the **I/O psychologist + statistician** set, in the pre-registration (§2): the **minimum meaningful effect size** for H1 (e.g., a validity-coefficient improvement the field considers material — grounded in Sackett et al. 2022 selection-validity literature), the **required sample size / power**, and the **decision rule**. The number is a *scientific* commitment made *in advance*, not a goalpost we move.

---

## 2. Pre-Registration Protocol *(do this BEFORE collecting data)*

Every experiment is **pre-registered** — the analysis plan is locked before data exists, so we cannot rationalize whatever we find. This is the primary structural defense against RK-15.

### 2.1 Pre-registration template *(one per experiment, signed off by Research + statistician + a designated skeptic)*
```
EXPERIMENT: [A / B / C]
DATE LOCKED: ____   SIGNED: Research lead ___  Statistician ___  Skeptic (red-team) ___

1. HYPOTHESIS (from §1.2): __________
2. PRIMARY METRIC: __________ (exactly how computed)
3. SECONDARY METRICS: __________
4. POPULATION & UNIT: __________ (which roles, which candidates, what counts as one data point)
5. SAMPLE SIZE / POWER: N = ___ ; power analysis: __________ (set by statistician)
6. MINIMUM MEANINGFUL EFFECT SIZE: __________ (set by I/O psychologist BEFORE data)
7. BLINDING: __________ (how outcome is hidden from scorers)
8. ANALYSIS METHOD: __________ (exact statistical test / coding scheme; no post-hoc changes)
9. CONFOUNDS & CONTROLS: __________
10. SUCCESS CRITERION (validate): __________
11. FAILURE CRITERION (falsify / KILL-1 trigger): __________
12. STOPPING RULE: __________ (when we stop collecting; no peeking-and-stopping)
13. WHAT WOULD CHANGE OUR MIND: __________ (pre-committed disconfirming result)
```

### 2.2 Rules
- **Locked = locked.** Any change after data collection begins is documented as a deviation and weakens the finding (disclosed in the report).
- **A designated skeptic** (internal or external) co-signs each pre-registration and owns the Counter-Evidence Register (§13).
- **No peeking-and-stopping**: the stopping rule is set in advance; we don't stop the moment results look favorable.

---

## 3. The Three Parallel Experiments

Run **in parallel** (A-V01.2) — not one retrospective in sequence — so results **triangulate** and no single method's weakness dominates. All three are **zero-build**.

| Exp | Name | Tests | Evidence level | Answers |
|---|---|---|---|---|
| **A** | **Retrospective Outcome Study** | H1, H2, H5 | **L4-adjacent** (real outcomes) | *Does evidence predict outcomes better than the resume did?* |
| **B** | **Recruiter/Manager Screening Study** | H3 | **L2** (observed behavior) | *Do decision-makers actually change decisions on evidence?* |
| **C** | **Rejected-Candidate Interviews** | H2, H4 | **L2** (behavior + experience) | *Does resume screening miss good people, and do candidates find evidence fairer?* |

**Why all three:** Exp A is the strongest but hardest (needs outcome data, AS-21). Exp B tests whether validity even *matters* to buyers (a valid signal nobody acts on is worthless). Exp C tests the candidate-value/brand half of the thesis and surfaces false negatives Exp A's dataset may not contain. Convergence across all three at L2+ is far more credible than any one.

### Experiment A — Retrospective Outcome Study
- **Objective:** With a design partner's historical data, blindly re-evaluate past candidates on *evidence of ability* and test whether those scores predict real outcomes better than the original resume-first screen.
- **Design (blinded, retrospective cohort):**
  1. Partner provides, for one role family (e.g., backend eng) over 12–24 months: the candidate pool, resume/screen decisions, who was hired, and **outcome data** (performance rating, retention, manager assessment) — de-identified where possible.
  2. **Reconstruct an evidence signal** for as many candidates as feasible from artifacts the partner *already has* (work samples, take-homes, structured interview notes, code, portfolios). *We do not run new evaluations — we use existing artifacts.*
  3. **Blind expert re-scoring:** trained evaluators (I/O-guided rubric, §9) score each candidate's *evidence* **without seeing the outcome** (hindsight-bias blinding).
  4. Compare: correlation of **evidence score ↔ outcome** vs. correlation of **original resume/screen decision ↔ outcome**.
- **Data collected:** §8.1 schema.
- **Analysis:** validity coefficients (evidence vs. resume, each vs. outcome); base rates; false-negative/positive analysis; exploratory demographic-proxy analysis (H5). Method locked at pre-registration.
- **Validate:** evidence↔outcome validity exceeds resume↔outcome by the pre-set minimum meaningful margin (§1.3), across ≥N candidates.
- **Falsify (KILL-1 trigger):** evidence↔outcome is **not** materially better than resume↔outcome (and B/C don't compensate on trust/candidate-value) → the core thesis is in question → §16.
- **Honest caveat (logged):** mid-market sample sizes are small; outcome measures are noisy; this is **suggestive, not definitive** at MVP scale — which is exactly why we triangulate and why longitudinal L4 continues into the pilot.

### Experiment B — Recruiter/Manager Screening Study
- **Objective:** Observe (not ask) whether decision-makers change decisions when shown evidence vs. resumes. Tests H3 — that validity is *actionable*, not just real.
- **Design (within-subject, counterbalanced):**
  1. Assemble anonymized candidate packets for a real (or recent) req.
  2. A recruiter/VP Eng first screens on **resume-only**, records advance/reject + confidence.
  3. Later (counterbalanced order across participants), they see **evidence** (work sample/structured artifacts) for the same candidates and record advance/reject + confidence again.
  4. Measure **decision changes**, confidence changes, and reasoning (think-aloud).
- **Data collected:** §8.2 form.
- **Analysis:** rate of decision reversals; direction (did evidence rescue false negatives / catch false positives?); confidence delta; qualitative reasons (coded).
- **Validate:** decision-makers meaningfully change decisions on evidence **and** report they would trust/act on it in real hiring (behavioral L2 + stated adoption).
- **Falsify:** evidence rarely changes decisions, or decision-makers distrust/ignore it ("I still go with the resume/pedigree") → adoption risk (RK-1/RK-4) even if validity holds.

### Experiment C — Rejected-Candidate Interviews
- **Objective:** Surface false negatives (strong people resume-screening missed, H2) and test candidate-experienced fairness (H4). **Handled with maximum care** (§7).
- **Design (structured qualitative + light quant):**
  1. With partner + candidate consent, interview a sample of *rejected* candidates from a role family.
  2. Establish where they landed and how they've performed since (self-report + any verifiable signal) — surfacing "rejected-but-thrived-elsewhere" cases.
  3. Explore their experience of resume screening (opacity, perceived fairness) and reaction to an evidence-based approach (VALIDATION-03 candidate guide).
- **Data collected:** §8.3 capture form.
- **Analysis:** count/qualify false negatives; thematic coding of fairness perceptions; willingness to re-engage (network thesis).
- **Validate:** a meaningful fraction of rejects succeeded elsewhere (resume screening missed them) **and** candidates report evidence-based evaluation as fairer/worth re-engaging.
- **Falsify:** rejects broadly failed elsewhere too (resume screening was fine) **and/or** candidates are indifferent to the approach.

---

## 4. Design Partner Recruitment *(AS-21 — the first domino)*

Recruiting partners **who will share outcome data** is the prerequisite for Exp A and the meta-assumption AS-21. This is the hardest, highest-leverage step.

### 4.1 Ideal design partner profile
- US mid-market tech (100–5,000 employees), hiring **engineering** roles at volume (the beachhead, DOC-03).
- On a modern ATS (Greenhouse/Ashby/Lever) — data is accessible.
- A **motivated champion**: a Head of TA (Rina) or VP Eng (David) who *feels the pain* of bad hires/slow screening.
- **Willing and able to share outcome data** (performance/retention) — the defining trait of a design partner (DOC-04), and the gate for Exp A.
- Enough historical volume in one role family for a minimally-powered retrospective (statistician sets N; realistically 30–100+ candidates).

### 4.2 The mutual value exchange (what they give / get)
| They give | They get |
|---|---|
| Historical candidate + screen + **outcome** data (Exp A) | Early, deep influence on the product roadmap |
| Access to recruiters/HMs for the screening study (Exp B) | Preferential pricing / founding-partner terms (later) |
| Consent to interview a sample of rejected candidates (Exp C) | A **free, rigorous validity study of their own hiring** (independently valuable to them) |
| ~4–6 weeks of light collaboration | Evidence on whether *their* screening is missing talent |

> **Reframe the ask:** we're not asking them to test our product (we have none). We're offering to **run a scientific study of their hiring's predictive validity** — something they'd pay a consultancy for — in exchange for the data and access to do it. That reframe dramatically lowers the barrier and is honest (zero-build).

### 4.3 Qualification checklist (before committing to a partner)
- [ ] Has outcome data (or can get it) for ≥1 role family over ≥12 months.
- [ ] Champion has authority + motivation.
- [ ] Legal/privacy path exists for de-identified data sharing (§7).
- [ ] Willing to let findings be *honest* (including "your screening was fine").
- [ ] Realistic sample size (statistician confirms minimally useful).

**Target:** 3–5 qualified partners (redundancy: some will drop; Exp A needs data quality).

---

## 5. Recruitment Materials *(copy-and-use templates)*

### 5.1 Cold outreach email (to Head of TA / VP Eng)
```
Subject: A free validity study of your engineering hiring

Hi [Name],

Quick, unusual offer. I'm researching how well resume-based screening actually
predicts on-the-job success for engineers — and I'm looking for a few companies to
study with (not sell to; there's nothing to buy).

In ~4–6 weeks, working with your existing hiring + outcome data, we'd produce a
rigorous, independent answer to: "Is your screening advancing the people who
actually succeed — or missing them?" You keep the analysis. We learn from the pattern.

No tool to install, no product pitch. If you've ever suspected great engineers slip
through resume screens (or weak ones get through), this tells you.

Worth 20 minutes to see if your data fits the study?

[Name] — [role]
```

### 5.2 One-pager (leave-behind) — headline points
- *The problem:* resumes are weak predictors of engineering performance (cite Sackett 2022; DOL bad-hire cost ≥30% of first-year earnings, DOC-02).
- *The study:* blind, retrospective, uses your existing data; independent I/O-guided methodology.
- *Your value:* a real answer about your own hiring; founding-partner standing.
- *The ask:* de-identified historical data (Exp A), a few recruiter/HM sessions (Exp B), consent to interview some past candidates (Exp C).
- *Our promise:* honest findings — even if they say your screening is fine; strict privacy (§7).

### 5.3 Discovery call script (20 min) — *behavior-first, no pitching* (VALIDATION-03 rules)
```
- Their pain (listen): "Walk me through how you screen engineers today. When has it
  gone wrong — someone great you almost missed, or a hire that didn't work out?"
  [past behavior, not opinions]
- Data reality: "For one role, do you have who you screened, who you hired, and how
  they've done since?" [Exp A feasibility]
- Motivation: "If a study showed your screening was missing strong people, what would
  you do with that?"
- The exchange (§4.2). Qualify (§4.3). No product promises.
- Close: agree on data scope + next step, or disqualify kindly.
```

### 5.4 Partner agreement (plain-language summary; legal drafts the actual)
Founding-partner collaboration; data shared is de-identified where feasible and used **only** for this study; strict confidentiality; findings shared back with the partner; either side can withdraw; **candidate data handled per §7**; no candidate data is sold or reused beyond the study (KD-03.14).

---

## 6. Research & Interview Guides

Persona interview guides live in **VALIDATION-03** (Candidate/Recruiter/HM/CHRO/Security). This kit adds the **experiment-specific** guides:

- **Exp A — Data-request guide:** exact data dictionary to request (§8.1), de-identification instructions, artifact inventory (what evidence artifacts they already hold), outcome-measure definition workshop (align on what "success" means at *this* company before scoring).
- **Exp B — Screening-study protocol:** packet prep, counterbalancing, think-aloud prompts, decision/confidence capture (§8.2); facilitator neutrality rules (never lead the participant toward evidence).
- **Exp C — Rejected-candidate guide:** the VALIDATION-03 candidate guide, **plus** the ethics framing (§7): explicitly *not* a re-application, no false hope, dignity-first (DOC-06), consent-gated.

**Universal interviewer rules (VALIDATION-03):** ask about *past behavior*, not future intentions; never pitch, lead, or defend; silence is a tool; **log contradictions immediately** (§13).

---

## 7. Consent & Ethics *(we apply P7 to ourselves)*

Validating a fairness product unethically would be self-refuting. This section is non-negotiable.

| Concern | Rule |
|---|---|
| **Partner data consent** | Written agreement; de-identified where feasible; purpose-limited to this study; deletion on request. |
| **Candidate consent (Exp C)** | **Explicit, informed, opt-in consent** before any interview; candidates told exactly what the study is, that it is **not a re-application and creates no hiring obligation or expectation**, and that participation/refusal has zero effect on any future opportunity. |
| **Dignity (DOC-06)** | Rejected-candidate contact is respectful, low-pressure, never re-opens rejection as a wound; framed as "we're studying how to make hiring fairer, and your experience matters." |
| **PII minimization** | Even in validation: collect the minimum; de-identify early; store encrypted; access-limited. **No raw PII in analysis artifacts** beyond what's essential. (Mirrors AD-89 discipline, applied pre-product.) |
| **No demographic misuse** | Demographic-proxy analysis (H5) is aggregate, for bias detection only, never individual-level judgment. |
| **Right to withdraw** | Any participant (partner or candidate) can withdraw; their data is removed. |
| **Ethics review** | A lightweight IRB-style review of the protocol (esp. Exp C) before fielding; a designated ethics owner signs off. |

### Consent language (candidate, Exp C — plain)
```
We're doing independent research on how to make hiring fairer and more accurate.
You were selected because you interviewed with [company] for [role]. This is a
RESEARCH conversation only — it is NOT a job application, it will NOT affect any
current or future opportunity in any way, and no one is reconsidering a decision.
We'll ask about your experience and views for ~30 minutes. It's voluntary; you can
skip any question or stop anytime. With your permission we'll take notes (no
recording without separate consent). Your responses are confidential and
de-identified in our analysis. May we proceed?
```

---

## 8. Data Collection Forms & Instruments

### 8.1 Exp A — Retrospective data schema (request from partner)
```
per CANDIDATE (one role family, de-identified ID):
  candidate_id (opaque)              role_family
  screen_decision (advance/reject)   screen_basis (resume/other)
  screener_confidence (if available) hired? (y/n)
  evidence_artifacts_available [work_sample | take_home | structured_interview_notes | code | portfolio | none]
  OUTCOME (for hired):  perf_rating (scale) | manager_assessment | retention_months | regretted_attrition (y/n)
  demographic_proxies (aggregate-only, optional): school_tier | prior_employer_tier | name-based signal
  NEVER collected: unnecessary PII, protected-class data at individual level
```

### 8.2 Exp B — Screening-study capture form
```
participant_id | role_family | round (1=resume-only | 2=+evidence) | order (counterbalance)
per candidate:  decision (advance/reject) | confidence (1–5) | reason (free text / think-aloud)
derived: decision_changed_r1_to_r2 (y/n) | change_direction (rescued FN / caught FP / no change)
post-session: "Would you act on this evidence in a real hire?" (y/n + why) [stated adoption]
```

### 8.3 Exp C — Rejected-candidate capture form
```
candidate_id (opaque, consented) | role_family | outcome_since (where landed, self-report)
performing_well_elsewhere? (y/n/unknown) + any verifiable signal
false_negative_candidate? (rejected here, thriving in similar role elsewhere) (y/n)
experience_of_screening: fairness (1–5) | opacity (1–5) | themes (coded)
reaction_to_evidence_approach: fairer? (1–5) | would_re-engage? (y/n) | themes
```

### 8.4 Master evidence log & Counter-Evidence Register → §13.

---

## 9. Scoring Templates *(the blind evidence-scoring rubric)*

The heart of Exp A's rigor: score *evidence of ability* **without outcome knowledge**.

| Rule | Detail |
|---|---|
| **Blinding** | Scorers receive evidence artifacts with **outcomes and identity removed**; a separate custodian holds the outcome key; scores are locked before any outcome linkage. |
| **Rubric** | Multi-dimensional (mirrors AD-10 dimensions): technical quality, reasoning, debugging, communication, engineering maturity — each on a defined anchored scale. *(This is a research rubric, not the product's evaluation logic — no product exists.)* |
| **Calibration** | Scorers train on shared examples to align; inter-rater reliability measured (report it — low reliability weakens findings). |
| **Multiple raters** | ≥2 independent raters per candidate where feasible; disagreements adjudicated per protocol. |
| **No outcome leakage** | Any accidental outcome exposure disqualifies that data point (logged). |

> **Anti-bias note:** the scoring rubric is designed and reviewed by the I/O psychologist to avoid embedding the very resume proxies (pedigree, keywords) we're testing against — otherwise we'd smuggle resume bias into the "evidence" score and rig the result toward H1.

---

## 10. Success Metrics & Measurement

AS-1 success is **multi-dimensional** (A-V01.2); any dimension, sufficiently strong, can carry adoption — but each has a **pre-registered** bar.

| Dimension | Primary metric | Bar (set at pre-registration by I/O + statistician) |
|---|---|---|
| **Predictive validity (H1)** | evidence↔outcome validity vs. resume↔outcome validity | evidence exceeds resume by ≥ [minimum meaningful margin], N ≥ [power-based] |
| **Actionable trust (H3)** | decision-change rate + stated willingness to act | evidence meaningfully changes decisions AND decision-makers say they'd act on it |
| **Candidate value (H4)** | fairness perception delta + false-negative count + re-engagement willingness | candidates find evidence fairer AND real false negatives exist |
| **Bias (H5, exploratory)** | resume-proxy correlation vs. evidence-proxy correlation | evidence less correlated with demographic proxies (directional) |

**The "materially valuable improvement" definition (pre-committed):** AS-1 is **supported** if Exp A shows a materially better validity margin **OR** (Exp B + Exp C together show strong actionable-trust + candidate-value even with a modest/underpowered A) — i.e., the *total* case for adoption is compelling, not a single dramatic statistic (A-V01.2: "KILL-1 fires on total value, not delta").

---

## 11. Analysis Methodology

- **Owned by the I/O psychologist + statistician**, not the founders (RK-15 defense — no motivated analyst).
- **Exp A:** validity coefficients (correlation of each signal with outcome), corrected for range restriction/reliability where the statistician deems valid; base-rate and false-positive/negative breakdown; effect sizes with confidence intervals; **report power and limitations honestly** (small N is expected).
- **Exp B:** McNemar-style within-subject change analysis; confidence deltas; qualitative coding of reasons (two coders, reconciled).
- **Exp C:** thematic analysis (pre-defined + emergent codes, double-coded); false-negative tally with verifiability grading.
- **Triangulation:** convergence/divergence across A/B/C explicitly assessed — *do the three independent methods point the same way?*
- **Confounds:** controlled/documented (role variation, time, manager-rating subjectivity, survivorship in outcome data).
- **All deviations from pre-registration disclosed.**

---

## 12. Validate / Falsify Criteria & Kill Conditions

Pre-committed decision rules (no moving goalposts):

| Outcome | Condition | Action (→ §16) |
|---|---|---|
| **AS-1 SUPPORTED** | Exp A meets its pre-set validity margin **OR** the combined A+B+C case clears the "materially valuable improvement" bar (§10), with L2+ convergence | Proceed: Evaluation Engine design → Sprint 1, carrying findings + limitations |
| **AS-1 PARTIALLY SUPPORTED** | Mixed: e.g., validity modest but trust/candidate-value strong (or vice versa) | Refine positioning/thesis via **ADR + DOC amendment** (ARB, ARCH-16) before heavy build; possibly re-scope beachhead |
| **AS-1 NOT SUPPORTED (KILL-1)** | Evidence does **not** predict outcomes materially better than resumes **AND** trust/candidate-value don't compensate | **Halt implementation.** Trigger KILL-1 (VALIDATION-01). Pivot decision through governance (§16). This is the kit succeeding, not failing. |
| **INCONCLUSIVE** | Underpowered / data-quality too poor to decide | Do **not** default to "supported." Get more/better data (more partners) before proceeding; explicitly resist the bias to proceed. |

> **The hardest discipline:** an *inconclusive* result must **not** be read as *supported*. Ambiguity is not permission. (RK-15.)

---

## 13. Counter-Evidence Register *(RK-15's teeth)*

A living log, **owned by the designated skeptic**, recording every piece of evidence that **contradicts** AS-1 — with equal rigor to supporting evidence.

```
COUNTER-EVIDENCE REGISTER
date | source (Exp A/B/C, interview, data) | disconfirming observation | strength (L0–L4)
     | does it challenge which sub-hypothesis? | our current response | unresolved? (y/n)
```
Rules: (1) at every readout, the skeptic presents the counter-evidence **first**; (2) a supporting conclusion is only accepted after the counter-evidence is explicitly addressed; (3) "we haven't found disconfirming evidence" is itself a red flag prompting harder search (absence of counter-evidence usually means we didn't look).

---

## 14. The Confirmation-Bias Defense *(RK-15 — summary)*

Everything above composes into a defense against fooling ourselves:
- **Pre-registration** (§2) — can't rationalize post-hoc.
- **Blinding** (§9) — hindsight bias removed from scoring.
- **Effect-size-before-number** (§1.3) — no moving goalposts.
- **Independent analyst** (§11) — founders don't run the stats.
- **Designated skeptic + Counter-Evidence Register** (§13) — someone paid to find us wrong.
- **Triangulation** (§3) — three independent methods must converge.
- **Evidence levels** (§0) — interviews alone can't "validate."
- **Inconclusive ≠ supported** (§12) — ambiguity isn't permission.
- **Success includes being wrong** — the kit is a success if it *correctly* tells us to stop.

---

## 15. Timeline & Operating Plan (30/60/90, indicative)

| Window | Milestones |
|---|---|
| **Weeks 0–3** | Finalize + pre-register protocols (I/O + statistician); recruit/qualify 3–5 partners (§4–5); legal/ethics sign-off (§7). |
| **Weeks 3–6** | Exp A data ingest + de-identification + outcome-measure workshop; begin blind scoring; run Exp B sessions; consent + schedule Exp C interviews. |
| **Weeks 6–9** | Complete scoring; Exp A analysis; complete B; conduct C interviews + code. |
| **Weeks 9–10** | Triangulated analysis (§11); skeptic-first readout (§13); apply decision rules (§12); governance routing (§16). |

Cadence: weekly readout where the **Counter-Evidence Register is presented first**; a locked decision date to avoid indefinite "one more data point."

---

## 16. Feedback into Governed Architecture *(ARCH-16)*

The validation outcome feeds the **frozen** architecture through the governed process — this is exactly what ARCH-16 was built for.

```
Validation outcome (§12)
   ├── SUPPORTED ──────────▶ proceed to Evaluation Engine design + Sprint 1
   │                          (findings + limitations recorded; no arch change needed)
   ├── PARTIALLY ──────────▶ ADR against baseline + DOC-01/02/03 amendment
   │                          → ARB review (AD-139) → adjust thesis/beachhead → then build
   ├── NOT SUPPORTED ──────▶ KILL-1 (VALIDATION-01): HALT build
   │                          → pivot decision → major ADR + DOC amendments → ARB
   │                          → the frozen arch is NOT extended until the thesis is re-established
   └── INCONCLUSIVE ───────▶ gather more evidence; do NOT proceed on ambiguity
```

**Rules:** no implementation proceeds past Sprint-0 while AS-1 is unsupported or inconclusive; any thesis change is a **governed** change (ADR + DOC amendment + ARB, AD-136/AD-139), never an ad-hoc pivot; the architecture's coherence is preserved *even through a pivot* because change flows through governance.

---

## 17. Roles & Responsibilities

| Role | Owns |
|---|---|
| **Founder/CEO** | Partner recruitment, the value exchange, the honest ask |
| **Head of Research (I/O psychologist)** | Methodology, rubric, effect-size + analysis, scientific integrity |
| **Statistician** | Power/sample size, analysis plan, honest limitations |
| **Designated Skeptic (red-team)** | Counter-Evidence Register; skeptic-first readouts; pre-registration co-sign |
| **Ethics owner** | Consent, dignity, IRB-style review (esp. Exp C) |
| **Product** | Translating findings into the go/adjust/halt decision + governance routing |

---

## 18. Appendices — Templates Index
- A. Pre-registration form (§2.1)
- B. Cold email / one-pager / discovery script / partner-agreement summary (§5)
- C. Consent language — partner + candidate (§7)
- D. Data schemas + capture forms — Exp A/B/C (§8)
- E. Blind evidence-scoring rubric (§9)
- F. Counter-Evidence Register (§13)
- G. Decision-rule sheet (§12)

---

*End of VALIDATION-04 v0.1 — the Design Partner Validation Kit. A complete, zero-build package to test AS-1 (evidence beats resumes for predicting outcomes, and stakeholders trust it, and candidates find it fairer) through three parallel triangulating experiments — engineered first against our own confirmation bias (RK-15), with pre-committed validate/falsify criteria that route through the governed architecture (ARCH-16). The kit succeeds if it tells us the truth — including, if it is the truth, that we are wrong. Recommended next: pre-register the protocols and begin partner recruitment (AS-21).*
