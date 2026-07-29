# Document 02 — Problem Statement & Market Opportunity

| Field | Value |
|---|---|
| **Document ID** | DOC-02 |
| **Title** | Problem Statement & Market Opportunity |
| **Status** | Draft v0.2 — core approved (9.5/10); **amended to add Platform Risk (MR-11); full Platform Risk Analysis moved to DOC-03** |
| **Owner** | Principal Engineer / Technical Documentation Lead |
| **Created** | 2026-07-21 |
| **Depends on** | DOC-01 (Vision & Product Thesis, ratified) |
| **Blocks** | DOC-03 (Product Principles), DOC-04 (Personas & JTBD) |
| **Scope discipline** | This document explains **the problem** and **the opportunity**. It proposes **no product features**, no architecture, and no solution design. Where the temptation to solution arises, it is deferred with a forward-reference. |

---

## How to read this document — evidence discipline

This is the document that must survive a skeptical board member, a due-diligence analyst, and a new engineer who asks "prove it." To that end, every material claim is tagged:

- **[FACT]** — supported by external research or published data. A source is cited inline and listed in §References. Figures reflect data available as of mid-2026 and are subject to the usual caveats about self-reported surveys and vendor-published market reports (see §Methodology & caveats).
- **[ESTIMATE]** — a figure we derived by combining facts with stated arithmetic. The derivation is shown so it can be checked or challenged.
- **[ASSUMPTION]** — a belief we currently hold **without** sufficient evidence. Every assumption is restated in §13 with a validation plan. Assumptions are load-bearing until disproven and must never be quoted externally as fact.

> **Methodology & caveats.** Market-size figures come from commercial research firms whose numbers diverge by 15–40% depending on segment definitions; we therefore cite ranges and name the firm. Behavioral statistics (e.g., resume lying) are largely self-reported surveys with known social-desirability bias — we treat them as directional, not precise. Academic validity coefficients come from peer-reviewed meta-analysis and are our most reliable evidence class. When facts conflict, we say so rather than cherry-picking.

---

## 1. Executive Summary

Hiring is one of the highest-stakes, highest-frequency, and most economically consequential decisions an organization makes — and it is still made primarily on the basis of a **self-authored, unverified, and increasingly synthetic document: the resume.** This document establishes, from evidence, that the resume-first paradigm is not merely imperfect but structurally broken, that the breakage imposes large and measurable costs, and that a specific convergence of technology, regulation, and market conditions makes *now* the moment to build an evidence-first alternative.

**The problem in one paragraph.** The highest-signal information about a candidate — whether they can actually do the work — is collected last in the funnel, at the greatest cost, and for the fewest candidates, while the lowest-signal artifact (the resume) gates everyone. This inversion produces four simultaneous failures: it *mismeasures* candidates, it is *trivially gamed* (and now AI-generated at scale), it is *unfair and legally fragile*, and it is *not evidence-based* despite a century of research on what actually predicts job performance.

**The evidence, in brief.**
- The methods research says are most predictive of job performance — structured interviews, work samples, cognitive/skills assessment — are precisely the ones applied *least* and *latest*, because they don't scale with human effort. Meta-analytic work (Sackett et al., 2022) ranks structured interviews, general mental ability, work samples, and integrity tests at the top; it ranks unstructured interviews and years of experience — the things resumes feed — near the bottom. **[FACT]**
- Resume-based screening encodes bias: identical resumes with White-sounding names received ~50% more callbacks than those with Black-sounding names (Bertrand & Mullainathan, 2004), a finding that has anchored two decades of labor-market discrimination research. **[FACT]**
- The artifact is unreliable: roughly **1 in 3** Americans admit to lying on a resume, and in one 2024 survey **63%** of self-identified resume fraudsters received a job offer while **96%** said they were never caught. **[FACT]**
- The cost of getting it wrong is large: the U.S. Department of Labor is widely cited as estimating a bad hire costs **at least 30% of the employee's first-year earnings**; SHRM figures put mid-level bad hires at **100–150%** of annual salary. **[FACT]**
- The efficiency tax is real: U.S. cost-per-hire averaged **~$5,475** (non-executive) and time-to-hire **~42 days** in SHRM's 2025 benchmarking. **[FACT]**

**Why now.** AI — specifically large language models and multimodal reasoning — has, for the first time in history, made high-signal, structured, work-sample-style evaluation *cheap to produce at scale*. Simultaneously, AI-generated resumes have destroyed whatever residual signal the resume carried, and a new wave of regulation (NYC Local Law 144, the EU AI Act) is forcing hiring decisions to become auditable and explainable. The tool that broke the old signal is the same tool that can manufacture a new, better one — but only if it is built to be explainable and fair, which most current entrants are not.

**The opportunity.** The talent-acquisition software market is large and growing (talent-acquisition software ~**$25.7B in 2025**, projected ~**$51B by 2032** at ~9% CAGR; the narrower recruitment-software segment ~**$3.4B in 2025**). **[FACT]** But market-size is the smaller story. The larger story is that **no incumbent owns the neutral, explainable *intelligence layer*** that connects evaluation into a defensible hiring recommendation. ATS vendors own storage; assessment vendors own point-tests; job boards own attention. The judgment layer is unclaimed. That is the opening this company exists to take (per DOC-01).

**What this document does not do.** It does not describe our product, our features, or our architecture. It builds the shared, evidence-grounded understanding of the problem that all subsequent design must answer to. If a later feature does not trace back to a pain point or job documented here, that feature is suspect.

---

## 2. The Current Hiring Ecosystem (end-to-end)

To locate the problem precisely, we must first map the system as it actually operates today — not as org charts pretend it does. The modern hiring funnel is a sequence of loosely coupled stages, spanning multiple software systems, multiple human roles, and multiple incentive structures that are frequently in conflict.

### 2.1 The canonical funnel (as it exists today)

```
STAGE                     PRIMARY ACTOR         PRIMARY SYSTEM(S)          DOMINANT SIGNAL USED
─────────────────────────────────────────────────────────────────────────────────────────────
0. Workforce planning     HR leader / Finance   HRIS, spreadsheets         Headcount budget, attrition
1. Requisition creation   Hiring manager + HR   ATS                        Job description (often stale/templated)
2. Sourcing               Recruiter / sourcer   LinkedIn, job boards, ATS  Keywords, titles, pedigree
3. Application            Candidate             ATS portal, email, referral Resume + form fields
4. Screening (resume)     Recruiter / ATS rules Resume parser / ATS filters RESUME KEYWORDS  ← the broken gate
5. Recruiter phone screen Recruiter             Phone, ATS notes           Communication, basic fit
6. Assessment (if any)    Candidate             HackerRank/CodeSignal/etc. Skills test (siloed, late)
7. Hiring-mgr interviews  Hiring manager + team  Video/onsite, ATS notes    Unstructured impressions
8. Debrief / decision     Panel + HM            Email, ATS, meetings       Memory, gut, loudest voice
9. Reference / background Recruiter / vendor    Checkr/HireRight/etc.       Verification (post-decision)
10. Offer / negotiation   Recruiter / HM        ATS, email, DocuSign       Comp bands, candidate leverage
11. Onboarding            HR / IT               HRIS, onboarding tools     —
12. Outcome (quality)     HM / HR               Performance systems        RARELY fed back to hiring
```

### 2.2 Structural observations about the funnel

1. **The highest-signal stages (6, 7) come after the lowest-signal gate (4).** Skills assessment and deep interviewing — the predictive methods — are gated by resume screening, which is the least predictive method. The funnel is inverted with respect to signal quality. **[FACT — validity ranking per Sackett et al., 2022; the sequencing observation is ours, [ASSUMPTION] as a universal claim but strongly supported by practitioner accounts.]**

2. **The funnel spans many disconnected systems.** A single hire touches the ATS, LinkedIn, one or more assessment tools, email, calendar, video, a background-check vendor, and e-signature — each with its own data model. No system holds the *end-to-end evidence* of why a candidate advanced or was rejected. **[FACT — this fragmentation is well documented across the HR-tech landscape; see §7.]**

3. **The feedback loop from stage 12 (actual job performance) back to stage 4 (screening criteria) is almost always broken.** Companies rarely measure whether the people they screened *in* outperformed those they screened *out*, because the screened-out are unobservable and performance data lives in a different system owned by a different team. Without this loop, screening criteria cannot self-correct. **[ASSUMPTION — widely believed and consistent with the absence of "quality-of-hire" instrumentation in most ATSs; to be validated with design partners, see §13.]**

4. **Each stage optimizes a local metric that conflicts with the global goal.** Recruiters are measured on time-to-fill and pipeline volume; hiring managers on team output; HR leaders on cost and compliance. "Quality of hire" — the only metric that matters at the company level — is owned by no one and measured by almost no one. **[ASSUMPTION, strongly supported by the fact that cost-per-hire and time-to-hire are the industry's standard benchmarks while quality-of-hire has no standard definition.]**

### 2.3 Two ecosystems, not one

Critically, the ecosystem bifurcates by company maturity — a distinction that matters enormously for our integration strategy (DOC-06):

- **ATS-centric companies** (most mid-market and enterprise): The ATS (Greenhouse, Lever, Ashby, iCIMS, Workday, SuccessFactors) is the system of record. Everything routes through it. Integration means connecting *to* the ATS.
- **ATS-light / no-ATS companies** (many SMBs, some fast-growing startups): Hiring runs on email, spreadsheets, and calendars. There is no system of record; there is an inbox. Integration means working *through email and lightweight workflows.*

DOC-01's commitment — the candidate never changes how they apply, the recruiter never changes how they hire — requires us to serve **both** ecosystems without forcing either into the other. This is a defining constraint, not a feature request.

### 2.4 The developer-hiring sub-ecosystem (our beachhead)

Because our beachhead is engineering roles at mid-market tech companies (DOC-01, D-01.2), we note its specific texture:

- Candidates are **evaluation-fatigued**: multi-round LeetCode-style gates, unpaid take-home projects, and 5–8 interview loops are common and widely resented. **[ASSUMPTION — well-attested in developer community sentiment; to be quantified.]**
- Skills are **relatively demonstrable and objective** compared to many roles, which is exactly why assessment tooling (HackerRank, CodeSignal, Codility) emerged here first. But those tools are **siloed point solutions** applied late (stage 6), disconnected from the rest of the evidence.
- Salaries are **high**, which magnifies the financial stakes of a bad hire (see §6). A mislaid senior engineer is a six-figure error. **[ESTIMATE, derived in §6.]**

---

## 3. Stakeholders

Hiring is a multi-sided problem. A solution that delights one party while burdening another fails. This section maps every actor, their goal, their success metric, and their structural pain. (Deep persona work — motivations, day-in-the-life, JTBD — is DOC-04; this is the map, not the territory.)

### 3.1 Primary stakeholders (directly in the funnel)

| Stakeholder | Core goal | How they're measured today | Structural tension |
|---|---|---|---|
| **Candidate** | Get a fair shot at a role they can do; not waste weeks. | (Self) offers received, time spent. | They have the *least* power and the *least* information, yet bear the most process burden. |
| **Recruiter / Talent Acquisition** | Fill reqs fast with qualified people; keep pipeline moving. | Time-to-fill, pipeline volume, cost-per-hire. | Rewarded for *speed and volume*, not for *quality* — which they can't see until long after. |
| **Hiring Manager** | Get a great teammate who raises team output. | Team delivery; (rarely) quality-of-hire. | Owns the outcome but not the process; drowns in interviews; distrusts recruiter screening. |
| **HR / People Leader** | Efficient, compliant, defensible hiring at scale; good employer brand. | Cost-per-hire, time-to-fill, compliance, D&I metrics. | Accountable for fairness and cost but dependent on tools and behaviors they don't fully control. |
| **The Company (as an entity)** | Maximize quality-of-hire per dollar and per day; minimize legal/brand risk. | Ultimately: revenue/output per employee; legal exposure. | No single owner of "quality of hire"; the metric that matters most is orphaned. |

### 3.2 Secondary stakeholders (shape or constrain the system)

| Stakeholder | Role in the ecosystem | Why they matter to us |
|---|---|---|
| **Interview panelists / ICs** | Conduct interviews, produce (unstructured) signal. | Their time is the scarcest, most expensive input; inconsistency here is a core failure. |
| **Executives / Finance** | Approve headcount, budget, tooling. | Buyers/budget-holders for enterprise deals; care about ROI and risk. |
| **Legal / Compliance** | Ensure hiring withstands EEOC/OFCCP/LL144 scrutiny. | Gatekeepers of enterprise adoption; explainability is *their* requirement (DOC-01, §9 gate). |
| **IT / Security** | Approve data flows, integrations, vendors. | Gatekeepers of integration; tenant isolation and data handling are their veto (DOC-10). |
| **ATS / HR-tech vendors** | Own the systems of record. | Simultaneously integration partners *and* potential competitors (§7). |
| **Regulators** | Define what "fair" and "explainable" legally mean. | Set the constraints that become our moat if we meet them early (DOC-01, DOC-11). |
| **Staffing / RPO agencies** | Hire on behalf of others at scale. | A post-beachhead channel and a future segment (DOC-01 §5). |

### 3.3 The critical insight from the stakeholder map

**The party with the most at stake (the company's quality-of-hire) is represented by no single role, and the party with the least power (the candidate) bears the most burden.** Every incumbent tool is bought by and built for the recruiter or HR leader, optimizing their *local* metrics (speed, cost, volume). This is *why* the market is full of tools that make bad hiring faster rather than making hiring better. Our thesis (DOC-01) is that owning the orphaned metric — evidence-based quality of decision — is the defensible position precisely because no one else is structurally incentivized to own it.

---

## 4. Detailed Pain Points

Each pain point below is stated as: **the pain**, **who feels it**, **evidence**, and **the cost of the status quo**. Solutions are deliberately withheld.

### 4.1 Candidates

**P-C1 — Judged on an artifact, not on ability.**
The resume gates everything, yet it measures self-presentation and pedigree, not capability. Capable people with non-linear paths, non-prestigious schools, or weak writing are filtered out before anyone assesses whether they can do the work.
- *Evidence:* The most predictive selection methods (structured interviews, work samples, GMA) are applied *after* the resume gate, if at all (Sackett et al., 2022). **[FACT for validity ranking; the causal "filtered out" claim is [ASSUMPTION] pending funnel data.]**
- *Cost:* Qualified candidates never get evaluated; the labor market misallocates talent.

**P-C2 — Systemic bias in screening.**
Identical resumes yield materially different outcomes based on name-signaled race and gender.
- *Evidence:* White-sounding names received ~50% more interview callbacks than Black-sounding names on otherwise identical resumes (Bertrand & Mullainathan, 2004); the effect persists across replications. **[FACT]**
- *Cost:* Discrimination (moral and legal), lost opportunity, eroded trust in the system.

**P-C3 — Enormous, uncompensated process burden.**
Multi-round loops, unpaid take-home projects, repeated re-explanation of the same background across companies. Developer hiring is a notorious offender.
- *Evidence:* Average U.S. time-to-hire ~42 days (SHRM 2025); developer loops of 5–8 stages are common. **[FACT for 42 days; loop counts [ASSUMPTION], to be quantified.]**
- *Cost:* Candidate drop-off, worse experience for the best (most-optioned) candidates first, employer-brand damage.

**P-C4 — Opaque rejection; no feedback, no recourse.**
Candidates are rejected with no explanation and cannot improve or contest. The "black hole" application experience.
- *Evidence:* Practitioner consensus; consistent with the fact that no mainstream ATS surfaces per-candidate reasoning to the applicant. **[ASSUMPTION, strongly held.]**
- *Cost:* Candidate frustration, reputational harm, and — increasingly — legal exposure as regulators demand explainability.

**P-C5 — Incentive to lie, because the artifact rewards it.**
When the gate is a keyword-matched self-report, the rational move is to optimize (and inflate) the self-report.
- *Evidence:* ~1 in 3 admit to lying on resumes; 63% of self-identified fraudsters got offers and 96% were never caught (2024 surveys). **[FACT, directional — self-reported.]**
- *Cost:* Honest candidates are disadvantaged; the signal degrades for everyone (a lemons market).

### 4.2 Recruiters / Talent Acquisition

**P-R1 — Drowning in low-signal volume.**
A single req can draw hundreds to thousands of applications, now amplified by one-click and AI-assisted mass applying. Recruiters cannot meaningfully evaluate them.
- *Evidence:* AI-generated applications have sharply increased volume per req (widely reported across 2024–2026 recruiting coverage). **[FACT directionally; magnitude [ASSUMPTION].]**
- *Cost:* Recruiters resort to cruder keyword filters, which worsens P-C1/P-C2 — a doom loop.

**P-R2 — Forced to screen on signal they know is weak.**
Recruiters often lack the domain depth to judge engineering ability, so they proxy with keywords, titles, and pedigree — and know it's unreliable.
- *Evidence:* Consistent with the low validity of resume-derived signals (Sackett et al., 2022). **[FACT for validity; the practice is [ASSUMPTION], well-attested.]**
- *Cost:* Good candidates rejected, bad candidates advanced, hiring-manager trust eroded.

**P-R3 — Measured on speed and volume, blamed for quality.**
Time-to-fill and pipeline are the metrics; quality-of-hire is the unspoken expectation. The incentives are misaligned with the goal.
- *Evidence:* Cost-per-hire (~$5,475) and time-to-hire (~42 days) are the industry's standard benchmarks; quality-of-hire has no standard metric (SHRM 2025). **[FACT — the metrics that exist; absence of a quality metric is the tell.]**
- *Cost:* Optimizing the measurable local metric at the expense of the unmeasured global one.

**P-R4 — Manual, repetitive coordination overhead.**
Scheduling, chasing panelists, collating scattered feedback, re-keying data between systems.
- *Evidence:* Screening and interviewing alone average ~8–9 days each within the ~42-day cycle (SHRM 2025). **[FACT.]**
- *Cost:* Recruiter time spent on logistics instead of judgment; slower cycles lose candidates.

**P-R5 — No end-to-end evidence trail.**
When asked "why did this candidate advance?", the honest answer is often scattered across notes, memories, and inboxes.
- *Cost:* Poor decisions, no auditability, legal fragility (ties directly to §5 and DOC-11).

### 4.3 Hiring Managers

**P-H1 — Owns the outcome, doesn't trust the funnel.**
The hiring manager lives with the hire but distrusts recruiter screening, so they re-screen, over-interview, and bottleneck the process.
- *Cost:* Duplicate work, slow cycles, manager time drained.

**P-H2 — Interview overload and inconsistency.**
Managers and their teams conduct many unstructured interviews; quality varies wildly by interviewer skill and mood.
- *Evidence:* Unstructured interviews rank well below structured interviews in predictive validity (Sackett et al., 2022). **[FACT.]**
- *Cost:* The most expensive input (engineer time) produces low-reliability signal.

**P-H3 — Decisions made on memory and gut in the debrief.**
Panel debriefs are frequently swayed by recency, the loudest voice, and unexamined bias rather than structured evidence.
- *Cost:* Inconsistent, biased, and undefensible decisions.

**P-H4 — Calibration gap.**
The hiring manager's real bar is rarely captured explicitly, so recruiters and panelists guess at it, and it drifts across hires.
- *Cost:* Misaligned pipelines, wasted interviews, inconsistent hiring standards across a team/org.

### 4.4 HR / People Leaders

**P-HR1 — Accountable for fairness and compliance they can't see into.**
HR owns D&I outcomes and legal defensibility, but the actual screening decisions happen in recruiters' heads and vendors' black boxes.
- *Evidence:* Regulatory pressure is rising (NYC LL144 mandates bias audits of automated employment-decision tools; EU AI Act classifies hiring AI as high-risk). **[FACT.]**
- *Cost:* Legal exposure, audit cost, brand risk from a single discrimination finding.

**P-HR2 — Can't prove or improve quality-of-hire.**
Without a definition or instrument for quality-of-hire, HR cannot demonstrate ROI or improve the system.
- *Cost:* Hiring is managed on proxy metrics (speed, cost) that don't correlate with the real goal.

**P-HR3 — Tool sprawl and integration burden.**
ATS + sourcing + assessment + scheduling + background check + analytics = a fragmented, expensive, poorly integrated stack.
- *Evidence:* The funnel spans 6+ disconnected systems (§2.2). **[FACT.]**
- *Cost:* Cost, data fragmentation, no single source of truth, security surface area.

**P-HR4 — Employer-brand damage from candidate experience.**
Poor, opaque candidate experience is visible (Glassdoor, social) and hurts future sourcing.
- *Cost:* Higher sourcing cost, declined offers, reputational harm.

### 4.5 Companies (the entity)

**P-CO1 — Systematic misallocation of talent.**
The company hires and rejects on weak signal, so it systematically hires some who can't do the job and rejects many who could.
- *Evidence:* The predictive-validity gap between methods used early (resume) vs. late/rarely (work samples, structured interviews) (Sackett et al., 2022). **[FACT.]**
- *Cost:* Quantified in §6 — this is the largest cost in the system.

**P-CO2 — Direct financial cost of bad hires.**
- *Evidence:* DOL widely cited at ≥30% of first-year earnings; SHRM 50–75% (entry), 100–150% (mid), 200–213% (executive). **[FACT.]**
- *Cost:* See §6.

**P-CO3 — Legal and regulatory exposure.**
Undefensible, unexplainable, potentially discriminatory decisions in a tightening regulatory climate.
- *Evidence:* Title VII disparate-impact doctrine; NYC LL144; EU AI Act. **[FACT.]**
- *Cost:* Litigation, fines, consent decrees, brand damage.

**P-CO4 — Speed cost / opportunity cost of open roles.**
A role open for ~42 days is ~42 days of lost output, overloaded teammates, and (for revenue roles) lost revenue.
- *Evidence:* ~42-day average time-to-hire (SHRM 2025); ~40% of senior roles take >90 days. **[FACT.]**
- *Cost:* See §6.

**P-CO5 — No organizational learning loop.**
Because outcomes (§2.2, point 3) don't feed back to criteria, the company never learns *which* of its signals actually predicted success. It repeats the same mistakes at scale.
- *Cost:* Compounding misallocation; inability to improve.

---

## 5. Root Cause Analysis — Five Whys

The pain points above are symptoms. The Five Whys technique drives to root cause. We run it along three independent chains, because a system this broken has more than one root.

### 5.1 Chain A — "Why do companies hire the wrong people?"

1. **Why do companies hire the wrong people?** → Because they decide on weak signals (resumes, unstructured impressions) rather than strong evidence of ability.
2. **Why do they decide on weak signals?** → Because strong evidence (structured evaluation, work samples) is expensive and slow, so it's applied late and to few, while the cheap weak signal gates everyone.
3. **Why is strong evidence expensive and slow?** → Because producing it has historically required scarce, expensive human expert time (engineers interviewing, experts grading work samples), which doesn't scale with applicant volume.
4. **Why must it require scarce human expert time?** → Because until recently, no technology could conduct or evaluate a rich, adaptive, role-relevant assessment at human-expert quality *at scale and low marginal cost.*
5. **Why is that now changing?** → Because AI (LLMs + multimodal reasoning) can now conduct and evaluate structured, adaptive, evidence-producing evaluations at near-zero marginal cost — **removing the economic constraint that forced the funnel to be inverted.** *(This is the root cause and the "why now"; see §8–9.)*

> **Root cause A:** *The funnel is inverted (weak signal first, strong signal last) because, until AI, strong evidence could not be produced cheaply at scale. That constraint is now lifting.*

### 5.2 Chain B — "Why is hiring unfair and undefensible?"

1. **Why is hiring unfair?** → Because screening decisions encode human and proxy bias (name, pedigree, gaps).
2. **Why do they encode bias?** → Because they rely on holistic human judgment over biased artifacts, with no structured, consistent, evidence-based criteria.
3. **Why is there no structured, consistent criteria?** → Because criteria are implicit (in recruiters' and managers' heads), not explicit, and vary per person and per day.
4. **Why are criteria implicit?** → Because the systems of record (ATS) store *artifacts and statuses*, not *reasoning and evidence*; there is no place where "why" is captured in a structured, comparable form.
5. **Why do systems store artifacts but not reasoning?** → Because they were built as **systems of record (databases of applicants)**, not **systems of judgment (engines of evidence-based decision)**. No one built the judgment layer.

> **Root cause B:** *Hiring is unfair and undefensible because the reasoning behind decisions is never captured in a structured, explainable form — because the industry built systems of record, not systems of judgment.* (This is precisely the gap DOC-01 stakes the company on.)

### 5.3 Chain C — "Why doesn't hiring improve over time?"

1. **Why doesn't hiring improve?** → Because companies don't learn which signals predicted good hires.
2. **Why don't they learn?** → Because the outcome (job performance) is never connected back to the hiring signal.
3. **Why is it never connected?** → Because performance data and hiring data live in different systems, owned by different teams, with no shared identifier or feedback loop.
4. **Why is there no shared loop?** → Because no one owns "quality of hire" end-to-end; recruiters own speed, managers own output, HR owns cost/compliance.
5. **Why does no one own quality-of-hire?** → Because there is no tool or role that spans the full arc from evaluation to outcome — the **intelligence layer** is missing.

> **Root cause C:** *Hiring doesn't improve because no system spans evaluation-to-outcome, so the learning loop is never closed — again, the missing intelligence layer.*

### 5.4 Synthesis of root causes

All three chains converge on a single structural absence:

> **THE ROOT CAUSE: The hiring industry built systems of record (where applicants are stored) but never built the system of judgment (where evidence is produced, reasoning is captured, and outcomes are learned from). That layer was economically impossible to build at scale until AI removed the cost constraint on producing high-signal evidence.**

This is the problem DOC-01 commits the company to solving, and it is why "not another ATS / job board / point-test" (DOC-01 §4.2) is the correct framing: those are all systems of record or point solutions. The judgment layer is the unclaimed root.

---

## 6. Financial Impact of Current Hiring Inefficiencies

We quantify the cost of the status quo along four vectors. Where we compute, we show the arithmetic so it can be challenged. **All dollar figures are illustrative models built on cited facts, labeled [ESTIMATE]; they are not claims about any specific customer.**

### 6.1 Cost of a bad hire (the largest and least-visible cost)

**Cited facts:**
- U.S. DOL widely cited: a bad hire costs **≥30% of the employee's first-year earnings**. **[FACT]**
- SHRM: **50–75%** of salary (entry/hourly), **100–150%** (mid-level technical/managerial), **200–213%** (C-suite). **[FACT]**

**Modeled impact for our beachhead (mid-market tech, engineering):**
- Assume a mid-level software engineer total first-year cost ≈ **$150,000** (salary + benefits/overhead). **[ASSUMPTION — plausible mid-market US SWE figure; must be validated per segment.]**
- Bad-hire cost at DOL's conservative 30% ≈ **$45,000**. At SHRM's mid-level 100–150% ≈ **$150,000–$225,000**. **[ESTIMATE]**
- If a mid-market company makes **100 engineering hires/year** and industry evidence suggests a meaningful share of hires underperform or fail (bad-hire rates are commonly cited in the ~20–30% range in practitioner literature — **[ASSUMPTION, to validate]**), then even at the conservative 30% figure and a 20% bad-hire rate: `100 × 20% × $45,000 =` **$900,000/year** in bad-hire cost alone; at the SHRM mid-level figure, **$3M–$4.5M/year**. **[ESTIMATE]**

> **Takeaway:** The dominant cost of broken hiring is not recruiter time or software spend — it is the **wrong-decision cost**, which is 1–2 orders of magnitude larger and almost entirely unmeasured. This is the cost our thesis targets, and it is why "evaluation accuracy" and "quality of hire" sit so high in DOC-01's priorities.

### 6.2 Cost-per-hire (the visible efficiency cost)

- SHRM 2025: non-executive cost-per-hire **~$5,475**; executive **~$35,879**. **[FACT]**
- Modeled: 100 hires × $5,475 ≈ **$547,500/year** in direct recruiting cost for a mid-market company. **[ESTIMATE]**

This is the cost buyers *see* and budget for — which is why incumbents sell to it — but per §6.1 it is the *smaller* problem.

### 6.3 Time-to-hire (the opportunity cost)

- SHRM 2025: **~42 days** average; ~40% of senior roles **>90 days**. **[FACT]**
- Opportunity cost of an open role = lost output + overloaded teammates + (for revenue roles) lost revenue. A crude model: if an open engineering role represents **$150,000/year** in foregone value-add, then 42 days ≈ **$17,300 per role** in opportunity cost; 100 roles ≈ **$1.7M/year**. **[ESTIMATE — value-add-per-role is a strong assumption and varies enormously; shown only to establish order of magnitude.]**

### 6.4 Compliance, legal, and brand risk (the tail cost)

- Hard to model as an expected value; behaves as a **low-probability, high-severity tail risk**. A single class-action disparate-impact suit, regulatory consent decree, or viral bias story can cost millions and inflict lasting brand damage. **[FACT that the exposure exists; magnitude is scenario-dependent, [ESTIMATE].]**
- This is precisely why DOC-01 makes fairness/explainability a **non-negotiable gate**: the tail risk dominates the expected-value math for a hiring-AI company.

### 6.5 Aggregate picture (illustrative, one mid-market company)

| Cost vector | Modeled annual cost (100 eng hires) | Visibility to buyer today |
|---|---|---|
| Bad-hire (wrong decision) | **$0.9M – $4.5M** [ESTIMATE] | **Low** — mostly unmeasured |
| Cost-per-hire (efficiency) | ~$0.55M [ESTIMATE] | High — budgeted |
| Time-to-hire (opportunity) | ~$1.7M [ESTIMATE] | Medium — felt, rarely quantified |
| Compliance/legal/brand | Tail risk (M+ per event) [ESTIMATE] | Low until it happens |

> **The strategic implication:** the market's attention (and incumbent product focus) is on the *smallest, most visible* cost (cost-per-hire), while the *largest, least visible* cost (bad-hire / wrong-decision) is orphaned. Our opportunity is to make the invisible cost visible and then reduce it — which is only possible with an evidence-and-outcome layer that spans the funnel.

---

## 7. Existing Solutions & Where They Fall Short

We catalog the incumbent categories, what they do well, and precisely where each fails the thesis. The pattern to notice: **every category is either a system of record, a point solution, or an attention marketplace — none is the neutral, explainable judgment layer.**

### 7.1 Applicant Tracking Systems (ATS) — Workday, SuccessFactors, Greenhouse, Lever, Ashby, iCIMS

- **What they do well:** System of record for applicants and reqs; workflow, status tracking, compliance recordkeeping; deep enterprise integration.
- **Where they fall short:** They store *artifacts and statuses*, not *evidence and reasoning* (Root cause B). Their "AI" is typically resume parsing / keyword matching — automating the broken gate rather than fixing it. They are built to *track*, not to *judge*.
- **Relationship to us:** **Integration partner, not competitor** (DOC-01 D-01.1). We make the ATS smarter; we do not replace it.

### 7.2 Job boards & sourcing — LinkedIn, Indeed, ZipRecruiter

- **What they do well:** Attention and reach; matching candidates to openings at the top of funnel.
- **Where they fall short:** They monetize attention/volume, not decision quality. More applicants ≠ better hires; in fact they worsen P-R1 (volume overload).
- **Relationship to us:** Upstream of us; not our category.

### 7.3 Assessment / testing vendors — HackerRank, CodeSignal, Codility, HireVue (assessments), Criteria, Wonderlic

- **What they do well:** Produce *some* real skills signal — closer to work samples, which have genuine predictive validity (Sackett et al., 2022). **[FACT]**
- **Where they fall short:** **Point solutions applied late and in a silo.** They test one dimension (usually coding) at one stage, disconnected from resume understanding, role context, interviews, and outcomes. They don't produce an *end-to-end, explainable recommendation*, and candidates experience them as yet another disconnected gate (P-C3). They are features of the intelligence layer, not the layer (DOC-01 §4.2).
- **Relationship to us:** The capability we subsume and connect, not the category we compete in.

### 7.4 AI screening / matching startups — a crowded 2023–2026 wave

- **What they do well:** Automate resume screening and candidate-to-job matching with ML/LLMs; fast, high-volume.
- **Where they fall short — and this is the critical one:** Most are **faster black boxes.** They automate the *broken gate* (resume screening) at higher speed, often with *less* explainability, and frequently import the very bias they claim to remove. Research on LLM-based resume screening has already documented racial bias in model outputs. **[FACT — emerging arXiv literature on LLM resume-screening bias.]** They optimize DOC-01's *lowest* priorities (speed, integration ease) while failing its *gate* (fairness, explainability).
- **Relationship to us:** Our most direct competitors *and* the clearest illustration of why our differentiation (explainable, evidence-based, fair-by-construction) matters. Winning here is a positioning and trust argument, not just a technology one (full treatment in DOC-03/DOC-08/DOC-11).

### 7.5 Interview-intelligence tools — Metaview, BrightHire, HireVue (video), Pillar

- **What they do well:** Record, transcribe, and summarize interviews; nudge toward structure; capture notes.
- **Where they fall short:** They operate at one stage (the interview), depend on interviews already happening, and largely *assist* the existing unstructured process rather than producing independent, end-to-end evidence. Valuable, but a slice.
- **Relationship to us:** Adjacent capability; a slice of the layer.

### 7.6 Background / verification — Checkr, HireRight

- **What they do well:** Verify credentials and history — *after* the decision is essentially made.
- **Where they fall short:** Verification is not evaluation; it confirms facts, not ability, and it happens too late to shape selection.
- **Relationship to us:** Downstream; complementary.

### 7.7 The "do nothing" alternative — keep reading resumes

The most common competitor is inertia. Its "advantage" is zero switching cost; its cost is everything in §4–§6. Any solution must beat *do-nothing* on a metric the buyer already feels (§12 prioritization).

### 7.8 The category gap — summarized

| Category | System of record? | Point solution? | Attention market? | The judgment layer? |
|---|---|---|---|---|
| ATS | ✅ | | | ❌ |
| Job boards | | | ✅ | ❌ |
| Assessment vendors | | ✅ | | ❌ |
| AI screeners | | ✅ (the broken gate) | | ❌ (black box) |
| Interview intel | | ✅ (one stage) | | ❌ |
| Background check | | ✅ (post-decision) | | ❌ |
| **This company** | **No (by design)** | **No** | **No** | **✅ — the unclaimed position** |

> **Conclusion:** The neutral, explainable, evidence-producing, outcome-learning **intelligence layer is a genuine white space.** No incumbent is structurally positioned or incentivized to occupy it (§3.3). This is the defensible opening.

---

## 8. Why AI Has Changed the Hiring Landscape

AI is not a feature we're bolting onto hiring; it is the force that has **broken the old equilibrium and made a new one possible.** Two things happened at once.

### 8.1 AI destroyed the old signal (the forcing function)

- LLMs made resumes and cover letters **cheap to generate and optimize at scale.** The resume, already weak, is now often synthetic. AI-assisted mass-applying floods reqs (P-R1). **[FACT directionally.]**
- The result: the resume's residual signal has collapsed, and recruiters increasingly fight AI-generated applications with AI filters — an arms race that produces no signal, only noise.
- **This is a forcing function, not a nice-to-have:** the old paradigm is actively degrading *right now*, which creates urgency that didn't exist five years ago.

### 8.2 AI created the possibility of a new, better signal (the enabler)

This is the deeper point and the root-cause reversal from §5.1:

- Historically, high-signal evaluation (structured interviews, work samples, adaptive technical assessment) required **scarce, expensive human expert time** and thus couldn't scale — forcing the inverted funnel.
- LLMs + multimodal reasoning can now **conduct and evaluate rich, adaptive, role-relevant evaluations at near-zero marginal cost**: understand a candidate's actual reasoning, probe adaptively, evaluate work samples, and produce structured evidence.
- For the first time, **the most predictive methods can be applied first and to everyone**, not last and to few. The economic constraint that inverted the funnel (Root cause A) is lifting.

### 8.3 AI made explainability both necessary and achievable

- **Necessary:** regulators (LL144, EU AI Act) now demand that automated hiring decisions be auditable and explainable. **[FACT]**
- **Achievable:** modern AI can produce not just a score but the *reasoning and evidence* behind it — *if the system is designed for explainability from the start* (DOC-01 §9 gate, DOC-08 to specify).
- **The trap:** most current AI entrants use AI to make the *black box faster* (§7.4), which is exactly backwards. The winning use of AI is to make evaluation *more transparent*, not less.

### 8.4 The net effect

> AI is simultaneously the **problem's accelerant** (killing the resume) and the **solution's enabler** (making evidence cheap and explainable). A company that uses AI to *replace* the broken artifact with explainable evidence rides both waves. A company that uses AI to *automate* the broken artifact faster is building on sand.

---

## 9. Why Now

"Why now" is the question that separates a real opportunity from a perennial one. Hiring has been broken for decades; what makes *2026* the moment? Five converging vectors:

1. **Technology inflection (the enabler).** LLM/multimodal capability crossed the threshold where expert-quality, adaptive evaluation at scale is finally economical (§8.2). This was not true even 3–4 years ago. **[FACT — capability trajectory.]**

2. **Signal collapse (the forcing function).** AI-generated resumes/applications have destroyed the resume's residual signal and flooded funnels *now*, creating acute, present-tense pain (§8.1). **[FACT directionally.]**

3. **Regulatory forcing (the moat-maker).** NYC LL144 is in force; the EU AI Act designates hiring AI high-risk; more jurisdictions are following. Explainability and bias-auditing are shifting from optional to mandatory — rewarding whoever builds them in early and punishing black-box entrants. **[FACT.]**

4. **Market adoption readiness (the demand signal).** AI adoption in HR roughly doubled year-over-year (SHRM: **26% → 43%**; other surveys higher, e.g., HireVue **72%**); a majority of employers expect AI across most hiring stages within a year. Buyers are no longer asking *whether* to use AI in hiring but *which* AI to trust. **[FACT.]** This is the ideal timing: demand is real but trust is unsettled — a market actively shopping for a credible, explainable option.

5. **Trust vacuum (the wedge).** The first AI-hiring wave produced black-box tools and bias headlines, creating skepticism. A trustworthy, explainable, fairness-first entrant enters a market that has been *primed to want exactly that* by the failures of the first wave. **[ASSUMPTION, strongly supported by regulatory and press activity.]**

> **The "why now" thesis:** the enabling technology, the collapse of the old signal, the regulatory mandate for explainability, the surge in buyer demand, and the trust vacuum left by first-wave black boxes have arrived *simultaneously*. Miss this window and either an incumbent bolts on "good-enough" AI or a black-box entrant defines the category badly. The window is open now and will not stay open.

---

## 10. Market Opportunity

We size the opportunity conservatively and label every figure. Market sizing is directional, not precise (see §Methodology). We compute TAM/SAM/SOM two ways — top-down (analyst market reports) and bottom-up (from company/hire economics) — and reconcile them.

### 10.1 Top-down (analyst reports)

- **Talent-acquisition software market (broad TAM):** ~**$25.7B (2025)**, projected ~**$51.2B by 2032** at ~**9.1% CAGR** (SNS Insider, via reporting). **[FACT — vendor research, treat as directional.]**
- **Recruitment-software segment (narrower):** ~**$3.4B (2025)**, ~9% CAGR, roughly doubling by early 2030s across multiple firms (Fortune Business Insights, SkyQuest, Coherent, MRFR — estimates range $3.0–3.6B for 2025). **[FACT — directional; note the 15–20% inter-firm variance.]**

> Interpretation: the software market we integrate into and partly compete for is a **multi-tens-of-billions** category growing at high-single-digit CAGR. But this *understates* our opportunity, because our value target (§6.1) is the **wrong-decision cost**, which is far larger than software spend.

### 10.2 Bottom-up (from hire economics)

- U.S. hires per year number in the tens of millions; even restricting to our beachhead there is substantial volume. Let us build the beachhead SOM explicitly.
- **Beachhead definition (DOC-01):** US mid-market tech companies (~100–5,000 employees), engineering-family roles, first-round screening & evaluation.
- **[ESTIMATE] Bottom-up SOM sketch:**
  - Suppose ~**X** thousand US mid-market tech companies in scope. *(Exact count to be sourced; placeholder — see §14.)*
  - Suppose an average of **~100 engineering-family hires/year** per such company, evaluating **~10–20× that many candidates** at first-round.
  - If we price on evaluation volume or per-hire value, and capture even a modest fraction of the cost-per-hire (~$5,475) or the far larger bad-hire cost (§6.1), the **per-customer annual contract value plausibly ranges from tens to low-hundreds of thousands of dollars.** **[ESTIMATE — pricing model is DOC-later; shown only for order-of-magnitude.]**
  - The math shows the beachhead alone can support a venture-scale business *before* any expansion to other roles, segments, or geographies.

> The precise SOM requires a sourced count of in-scope companies and a pricing model, both flagged in §14. The point here is directional: **the beachhead is large enough to build a serious company, and the full vision (all roles, all segments, global) is a multi-tens-of-billions horizon.**

### 10.3 Expansion vectors (post-beachhead, per DOC-01 horizons)

| Vector | Direction | Multiplier on TAM |
|---|---|---|
| **Role expansion** | Engineering → product, data → all knowledge work → all roles | Large |
| **Funnel expansion** | First-round screening → full-funnel evaluation → outcome learning | Large |
| **Segment expansion** | Mid-market → enterprise → SMB → staffing/RPO | Large |
| **Geographic expansion** | US → EU → India → global (on compliance-ready base) | Large |
| **Data-network effects** | More evaluations → better calibration → portable candidate evidence | Compounding / moat |

### 10.4 Why the market structure favors a new entrant

- Incumbents are structurally disincentivized to own the judgment layer (§3.3, §7): ATS vendors profit from being the system of record; assessment vendors from point-tests; job boards from attention.
- The judgment layer requires being **neutral across ATSs** — which no ATS vendor can be, because they compete with each other. Our neutrality is a structural advantage an incumbent cannot easily copy (DOC-01 D-01.1). **[ASSUMPTION — a core strategic bet, to be pressure-tested in DOC-03/competitive strategy.]**

---

## 11. Jobs-to-be-Done Analysis

JTBD describes the *progress a stakeholder is trying to make* — independent of any product. (This anchors DOC-04's persona work and, later, every feature's justification.) We express each as: *When [situation], I want to [motivation], so I can [expected outcome].* Note: JTBD ≠ features (DOC-01 scope discipline preserved).

### 11.1 Candidate

- **JTBD-C1:** *When I find a role I believe I can do, I want to be evaluated on my actual ability, so I can get a fair shot regardless of my resume, background, or pedigree.*
- **JTBD-C2:** *When I apply, I want to spend my effort proving I can do the work (not decoding ATS keywords or redoing the same take-home for every company), so I can invest my time where it counts.*
- **JTBD-C3:** *When I'm rejected, I want to understand why (and ideally how to improve), so I don't feel I've fallen into a black hole.*
- **JTBD-C4:** *When I apply, I want to do it the way I already do (email, LinkedIn, the company portal), so I don't have to learn a new system to be considered.* (Directly encodes DOC-01's "candidate never changes how they apply.")

### 11.2 Recruiter / TA

- **JTBD-R1:** *When a req opens, I want to identify the candidates most likely to succeed — with evidence I can trust and defend — so I can present a strong, defensible shortlist quickly.*
- **JTBD-R2:** *When I'm flooded with applications, I want the signal separated from the noise on ability (not keywords), so I can spend my judgment where it matters.*
- **JTBD-R3:** *When a hiring manager challenges my shortlist, I want to show the evidence behind each advance/reject, so I can build trust and defend the decision.*
- **JTBD-R4:** *When I run my process, I want it to fit my existing ATS/workflow, so I don't have to change how I work or migrate systems.* (Encodes "recruiter never changes how they hire.")

### 11.3 Hiring Manager

- **JTBD-H1:** *When I need to fill a role, I want to trust that the shortlist is genuinely qualified, so I can stop re-screening and spend my scarce time only on strong candidates.*
- **JTBD-H2:** *When I evaluate candidates, I want consistent, structured, comparable evidence across them, so I can make a fair, defensible choice rather than relying on gut and memory.*
- **JTBD-H3:** *When I define what "great" means for this role, I want that calibration captured and applied consistently, so my real bar drives the pipeline.*

### 11.4 HR / People Leader

- **JTBD-HR1:** *When I'm accountable for hiring, I want every decision to be fair, explainable, and audit-ready, so I can withstand regulatory and legal scrutiny.*
- **JTBD-HR2:** *When I report on hiring, I want to measure and improve quality-of-hire (not just speed and cost), so I can prove and grow the function's value.*
- **JTBD-HR3:** *When I choose tools, I want fewer, better-integrated systems, so I reduce cost, fragmentation, and security surface.*

### 11.5 Company (entity)

- **JTBD-CO1:** *When we hire, we want to reliably select people who will succeed, so we maximize output-per-hire and minimize the enormous cost of wrong decisions.*
- **JTBD-CO2:** *When we hire at scale, we want the system to learn which signals actually predict success, so our hiring improves over time instead of repeating mistakes.*
- **JTBD-CO3:** *When we hire, we want to do so defensibly and fairly, so we protect the company from legal, regulatory, and brand risk.*

### 11.6 The unifying job

> **The overarching JTBD:** *"Help me make hiring decisions I can trust and defend — based on what a candidate can actually do — without forcing anyone (candidate, recruiter, or manager) to change how they already work."* Every stakeholder's job is a facet of this. This is the job the intelligence layer exists to do.

---

## 12. Problem Prioritization Matrix

Not all pains are equal. We score each major problem on **Severity** (how much pain/cost), **Frequency** (how often it bites), **Reach** (how many are affected), **Willingness-to-pay** (does someone with budget feel it?), and **Our leverage** (how uniquely can an evidence/intelligence layer address it, vs. incumbents). Scores are 1–5, **[ASSUMPTION]**-grade (informed judgment, to be validated with design partners). "Priority" is a guided synthesis, not a raw sum.

| # | Problem | Sev | Freq | Reach | WTP | Leverage | Priority |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | Wrong-decision / bad-hire cost (P-CO1/2) | 5 | 4 | 5 | 3* | 5 | **Highest** |
| 2 | Weak-signal screening / inverted funnel (P-R2, P-C1) | 5 | 5 | 5 | 4 | 5 | **Highest** |
| 3 | Volume overload / signal-vs-noise (P-R1) | 4 | 5 | 5 | 5 | 4 | **High** |
| 4 | Undefensible / unexplainable decisions (P-R5, P-HR1, P-CO3) | 4 | 4 | 4 | 4 | 5 | **High** |
| 5 | Bias / unfairness (P-C2) | 5 | 4 | 5 | 3* | 5 | **High** |
| 6 | Interview overload / inconsistency (P-H2/3) | 4 | 4 | 4 | 3 | 4 | **Medium-High** |
| 7 | Candidate burden / experience (P-C3/4) | 4 | 5 | 5 | 2* | 3 | **Medium** |
| 8 | Calibration gap (P-H4) | 3 | 4 | 3 | 3 | 4 | **Medium** |
| 9 | No learning loop / no QoH metric (P-CO5, P-HR2) | 4 | 3 | 4 | 3 | 5 | **Medium (strategic)** |
| 10 | Tool sprawl (P-HR3) | 3 | 3 | 3 | 3 | 2 | **Low-Medium** |
| 11 | Coordination overhead (P-R4) | 3 | 5 | 4 | 3 | 2 | **Low-Medium** |

`*` **Willingness-to-pay caveats worth flagging now:** Problems 1 and 5 (bad-hire cost, bias) are *high severity but low current WTP* because they are **unmeasured/invisible** (§6) or treated as tail risk — buyers under-pay for problems they can't see. Problem 7 (candidate experience) has low WTP because *the sufferer (candidate) is not the buyer* (§3.3). This gap between *severity* and *willingness-to-pay* is itself a central strategic problem: **our commercial entry (the wedge) must attack a problem that is both severe AND felt/paid-for today** — which points at problems 2, 3, and 4 as the *commercial* wedge, while problems 1, 5, 9 are the *mission and long-term moat* we make visible over time.

> **Prioritization synthesis (for DOC-03/DOC-04, not a product decision here):**
> - **Lead commercially with:** #2 (evidence-based screening) + #3 (signal-from-noise) + #4 (defensibility) — severe *and* paid-for today, and exactly the beachhead wedge (DOC-01).
> - **Deliver as the deeper value:** #1 (reduce wrong-decision cost) + #5 (fairness) + #9 (learning loop) — the mission, the moat, and the reason the category will consolidate around whoever owns the judgment layer.
> - **De-prioritize as primary wedges:** #10, #11 (efficiency conveniences incumbents already chase).

---

## 13. Assumptions We Need to Validate

Every assumption below is load-bearing. Each has an **owner-less** status until DOC-04+/pilots assign validation. Ranked by *how catastrophic it is if false.*

| ID | Assumption | If false… | How we validate | Severity if false |
|---|---|---|---|---|
| **AS-1** | Evidence-based evaluation meaningfully out-predicts resume-based screening *for our roles*, and the improvement is large enough to matter. | The entire thesis collapses (DOC-01 §3.1). | Design-partner pilots: compare downstream performance/retention of evidence-selected vs. resume-selected cohorts. | **Fatal** |
| **AS-2** | Buyers (mid-market TA/HR) will pay for *decision quality*, not just speed/cost. | Business model fails; we're forced to sell efficiency like incumbents. | Pricing interviews; willingness-to-pay tests; pilot conversions. | **Fatal** |
| **AS-3** | Recruiters/HMs will *act on* AI evidence, not just receive and ignore it. | North Star (evidence-backed decisions) doesn't move; adoption stalls. | Instrument evidence-reliance in pilots (do shortlists change behavior?). | High |
| **AS-4** | Candidates will complete richer evaluation without unacceptable drop-off. | Top-of-funnel collapses; fairness undermined. | Measure completion/drop-off vs. resume-only baseline; segment by candidate quality. | High |
| **AS-5** | We can integrate invisibly into existing ATS + email/no-ATS workflows without forcing behavior change. | DOC-01 sub-bet 3.3 fails; adoption friction kills growth. | Connector spikes (DOC-06); design-partner integrations. | High |
| **AS-6** | Neutrality across ATSs is a durable advantage incumbents can't easily copy. | Competitive moat weaker than believed; an ATS could bundle "good-enough." | Competitive war-gaming (DOC-03); watch incumbent AI roadmaps. | Medium-High |
| **AS-7** | Explainable/fair-by-construction is a decisive buying criterion (not just compliance box-ticking). | Our core differentiation matters less than assumed vs. faster black boxes. | Buyer interviews; win/loss analysis in pilots. | Medium-High |
| **AS-8** | The beachhead (US mid-market tech, eng roles) is large enough and reachable enough to build a venture-scale business. | Wrong beachhead; go-to-market misfires. | Source in-scope company count; pipeline/pilot conversion (§14). | Medium |
| **AS-9** | Bad-hire rates and costs in our segment are high enough that reducing them is a compelling ROI story. | The biggest value claim (§6.1) weakens. | Segment-specific data from design partners; published benchmarks. | Medium |
| **AS-10** | AI can produce *expert-quality, fair, explainable* evaluations for our roles at acceptable cost. | Solution feasibility in question (DOC-08 territory). | Technical spikes and expert-benchmark comparisons (later docs). | High (deferred to solution phase) |

---

## 14. Open Questions

Questions that must be answered to complete the problem picture (distinct from §13's beliefs-to-test):

1. **Segment sizing:** What is the *sourced* count of US mid-market (100–5,000 employee) tech companies, and their annual engineering-hiring volume? (Blocks a rigorous SOM in §10.2.) — *Needs a data source (e.g., Census/BLS, LinkedIn, Crunchbase, PitchBook).*
2. **Bad-hire rate ground truth:** What is the actual bad-hire/underperformance rate for engineering hires in our segment? The ~20–30% figure is practitioner lore, not rigorous. (Blocks §6.1 credibility.)
3. **Quality-of-hire definition:** Is there any workable, measurable definition of quality-of-hire our design partners already use or would accept? (Blocks the North Star instrumentation from DOC-01 D-01.4.)
4. **Candidate-as-user question (carried from DOC-01 §14 Q4):** How much of the candidate's pain (JTBD-C1–C4) is in scope for us to serve directly vs. serve indirectly via the employer? Materially changes problem scope.
5. **Regulatory specifics:** Precisely which regulations bind our beachhead customers *today* (LL144 applies to NYC; what about other states/cities), and what evidence must a decision carry to be defensible? (Feeds DOC-11.)
6. **Buyer identity:** In mid-market tech, who actually buys and champions a tool like this — Head of Talent, VP People, VP Eng, or the founder/CEO? (Feeds DOC-04 and GTM.)
7. **Incumbent AI trajectory:** How fast are Greenhouse/Ashby/Workday et al. shipping their own AI evaluation, and how good/explainable is it? (Feeds AS-6, DOC-03.)
8. **Data access for AS-1:** Can we get outcome data (performance/retention) from design partners to actually prove evidence beats resumes? Without it, AS-1 stays unvalidated.

---

## 15. Risks (problem- and market-level)

These are risks to *the problem framing and market thesis* — distinct from company-level risks (DOC-01 §11) and future product/technical risks. Framed as *risk → why it matters → early mitigation direction.*

| ID | Risk | Why it matters | Early mitigation direction |
|---|---|---|---|
| **MR-1** | **The core thesis (evidence beats resumes) fails to validate (AS-1).** | Existential; everything rests on it. | Make AS-1 the *first* thing design partners test; be willing to kill/pivot if it doesn't hold. |
| **MR-2** | **Buyers pay for speed/cost, not quality (AS-2).** | Forces us to compete as an efficiency tool — a commoditized, incumbent-favoring game. | Find the wedge problems that are *both* severe and paid-for (§12: #2/#3/#4); prove quality ROI early. |
| **MR-3** | **Incumbents bolt on "good-enough" AI and bundle it free.** | ATS vendors have distribution; "good-enough + free + already-integrated" can beat "better + standalone." | Lean on neutrality (AS-6) and depth of explainable evidence; be the layer *across* ATSs, not a feature *of* one. |
| **MR-4** | **Black-box AI entrants define the category badly and poison trust / trigger backlash.** | A bias scandal by a competitor could tar the whole category and invite blunt regulation. | Be visibly the fair/explainable option; help shape standards (DOC-11); differentiate hard on trust. |
| **MR-5** | **Regulation moves faster or differently than expected.** | Could raise compliance cost or reshape what's permissible in AI hiring. | Compliance-aware architecture from day one (DOC-01 §5); treat regulation as moat, not just cost. |
| **MR-6** | **Candidate backlash against "being evaluated by AI."** | If candidates distrust or refuse AI evaluation, funnels collapse (AS-4). | Transparency to candidates; human-in-the-loop (DOC-01 non-goal on autonomous decisions); frame as *fairer* than resume screening. |
| **MR-7** | **Beachhead too small or unreachable (AS-8).** | Wrong initial market wastes the first, most precious years. | Source the sizing (§14 Q1); validate reachability with early pipeline. |
| **MR-8** | **Measurement problem: we can't prove quality-of-hire, so we can't prove our value.** | If the value is real but unmeasurable, sales and North Star both stall. | Invest early in a workable QoH definition and instrumentation (§14 Q3); use leading proxies (evidence-reliance). |
| **MR-9** | **Data access blocked — can't get outcome data to prove AS-1.** | Undermines the whole validation program. | Structure design-partner agreements to include outcome-data sharing; consider proxy validations. |
| **MR-10** | **Solution turns out infeasible at acceptable cost/quality (AS-10).** | The problem is real but we can't solve it economically. | Deferred to solution phase (DOC-08); flagged so it isn't forgotten. |
| **MR-11** | **PLATFORM RISK — a giant bundles hiring intelligence into a channel it already owns** (e.g., Microsoft/LinkedIn "AI Interview," Workday native intelligence, Google, Amazon). | **Potentially existential.** Not another competitor — a distribution monopoly that could erase a large share of the market overnight. This was under-weighted in v0.1; the CTO correctly flagged it as the single biggest missing business risk. | **Full treatment in DOC-03 (Platform Risk Analysis + survival strategy).** Direction: neutrality no giant can offer, depth of compounding moat (Evidence Graph/Hiring Memory/Outcome Learning), trust/explainability leadership, and being the layer *across* all platforms rather than a feature *of* one. |

---

## Summary of Key Decisions

DOC-02 is primarily an *analysis* document, but it ratifies several framings that constrain all downstream design:

- **KD-02.1** — **The root cause is the missing "system of judgment."** The industry built systems of record (ATS), point solutions (assessment), and attention markets (job boards), but never the neutral, explainable **intelligence layer** — because producing high-signal evidence at scale was economically impossible until AI. This is the definitive problem statement. *(§5.4)*
- **KD-02.2** — **The largest cost is the invisible wrong-decision (bad-hire) cost**, 1–2 orders of magnitude above the visible cost-per-hire. Incumbents sell to the small visible cost; our opportunity is to make the large invisible cost visible and reduce it. *(§6)*
- **KD-02.3** — **The commercial wedge and the mission are different problems, and both must be served.** Lead commercially with severe-*and*-paid-for problems (evidence-based screening, signal-from-noise, defensibility); deliver the mission/moat through the harder-to-monetize-but-larger problems (wrong-decision cost, fairness, the learning loop). *(§12)*
- **KD-02.4** — **AI is both the forcing function (killing the resume) and the enabler (cheap, explainable evidence).** The winning use of AI is to make evaluation *more* transparent; automating the black box faster is the losing move. *(§8)*
- **KD-02.5** — **"Why now" is a genuine, closing window** created by five simultaneous vectors (tech inflection, signal collapse, regulatory forcing, adoption surge, trust vacuum). *(§9)*
- **KD-02.6** — **The beachhead can support a venture-scale business on its own**, with large role/funnel/segment/geographic expansion beyond it — pending a sourced SOM. *(§10)*

## Unresolved Questions (consolidated for founder input)

1. **Data-source approvals:** Which sources may we use to size the beachhead rigorously (Census/BLS, LinkedIn, Crunchbase, PitchBook)? *(§14 Q1)* — blocks a defensible SOM.
2. **Candidate-as-user (still open from DOC-01):** Confirm scope — do we serve candidate JTBD directly? *(§14 Q4)*
3. **Design-partner outcome data:** Can we secure agreements that include performance/retention data, without which AS-1 (the whole thesis) cannot be proven? *(§14 Q8, MR-9)*
4. **Buyer identity:** Who is the economic buyer and champion in mid-market tech? *(§14 Q6)* — shapes DOC-04 and GTM.
5. **Quality-of-hire definition:** Do we have (or can we build) a workable QoH metric with design partners? *(§14 Q3, MR-8)*

## Suggested Next Document

**DOC-03 — Product Principles & Non-Negotiables (the Constitution).**

- **Why next.** We now have (a) the vision and thesis (DOC-01) and (b) a deep, evidence-grounded understanding of the problem and market (DOC-02). The next step is to codify the **principles and non-negotiable rules** that every future decision must obey — the fairness/explainability *gate*, the integration-native/neutrality commitments, the human-in-the-loop stance, the "systems of judgment not record" identity, and the tie-breakers. These principles are now well-informed by the competitive reality (§7) and the root cause (§5.4), exactly as DOC-01 intended (principles should respond to reality, not be written in a vacuum).
- **What it will produce.** A ratified set of ~8–15 principles, each with rationale, implications, and explicit non-goals; the codified Prime Directive gate; and the rules that let us say "no" consistently.

> **Alternative next step:** DOC-04 (Personas & JTBD deep-dive) if you'd rather sharpen *who* before *rules*. My recommendation is **DOC-03 first**, because personas should be evaluated against principles we've already committed to (e.g., is "serve the candidate directly" consistent with our constitution?).

---

## References

*(Figures reflect data available as of mid-2026. Vendor market-research numbers are directional and vary by firm; academic meta-analytic figures are the most reliable class. See §Methodology & caveats.)*

- **Selection-method validity:** Sackett, Zhang, Berry & Lievens (2022), *Revisiting Meta-Analytic Estimates of Validity in Personnel Selection* — reanalysis revising validity estimates and ranking structured interviews, GMA, work samples, and integrity tests among top predictors. Summaries: [SIOP](https://www.siop.org/tip-article/is-cognitive-ability-the-best-predictor-of-job-performance-new-research-says-its-time-to-think-again/), [Master-HR](https://www.master-hr.com/insights/insights-from-sackett-et-al-2023/).
- **Hiring bias / callback discrimination:** Bertrand & Mullainathan (2004), *Are Emily and Greg More Employable than Lakisha and Jamal?*, American Economic Review 94(4):991–1013 — White-sounding names received ~50% more callbacks. [NBER w9873](https://www.nber.org/papers/w9873), [AEA](https://www.aeaweb.org/articles?id=10.1257%2F0002828042002561).
- **Cost of a bad hire:** U.S. DOL ≥30% of first-year earnings (widely cited); SHRM 50–75% / 100–150% / 200–213% by level. [inop.ai summary w/ DOL & SHRM citations](https://inop.ai/the-true-cost-of-a-bad-hire-in-2026/), [Frontline/Kasko on the DOL 30% rule](https://ceoblog.frontlinesourcegroup.com/2025/10/18/the-30-rule-what-u-s-dol-bad-hire-costs-mean-for-your-pl-and-how-to-prevent-them/).
- **Cost-per-hire & time-to-hire:** SHRM 2025 Recruiting Benchmarking — non-exec CPH ~$5,475, exec ~$35,879; avg time-to-hire ~42 days. [SHRM 2025 Benchmarking Report (PDF)](https://www.shrm.org/content/dam/en/shrm/research/2025-recruiting-benchmarking-report.pdf), [SHRM press release](https://www.shrm.org/about/press-room/shrm-releases-2025-benchmarking-reports--how-does-your-organizat).
- **AI adoption in HR/recruiting:** SHRM 43% (up from 26%); HireVue ~72%; ~67% use some form; variation by company size. [SHRM via herohunt review](https://www.herohunt.ai/blog/ai-adoption-in-recruiting-2025-year-in-review/), [Pin 2026 report](https://www.pin.com/blog/ai-adoption-recruiting-report/), [SelectSoftwareReviews](https://www.selectsoftwarereviews.com/blog/ai-recruiting-statistics).
- **Resume fraud / lying:** ~1 in 3 admit lying (ResumeBuilder); 63% of self-identified fraudsters got offers, 96% never caught (Resume.org, 2024). [ResumeBuilder](https://www.resumebuilder.com/1-in-3-americans-admit-to-lying-on-resume/), [Resume.org survey](https://www.resume.org/research/6-in-10-resume-fraudsters-landed-a-job-in-2024/).
- **Market size:** Talent-acquisition software ~$25.7B (2025) → ~$51.2B (2032), ~9.1% CAGR (SNS Insider via [Yahoo Finance](https://finance.yahoo.com/news/talent-acquisition-software-market-surpass-080000323.html)); recruitment-software segment ~$3.0–3.6B (2025), ~9% CAGR ([Fortune Business Insights](https://www.fortunebusinessinsights.com/industry-reports/recruitment-software-market-100081), [SkyQuest](https://www.skyquestt.com/report/recruitment-software-market), [Coherent Market Insights](https://www.coherentmarketinsights.com/industry-reports/recruitment-software-market)).
- **LLM resume-screening bias (emerging):** arXiv preprints documenting racial bias in LLM-based resume screening (illustrative of §7.4 black-box risk). *(Preprint; treat as directional pending peer review.)*

---

*End of DOC-02 v0.1. This document is analysis, not decision; it constrains but does not pre-empt DOC-03. Awaiting founder review of the five consolidated unresolved questions before promotion to Ratified.*
