# Document 09 — Jobs-To-Be-Done

| Field | Value |
|---|---|
| **Document ID** | DOC-09 |
| **Title** | Jobs-To-Be-Done (Demand-Side Logic) |
| **Owner** | Principal Engineer / Technical Documentation Lead (with Product, GTM, CS) |
| **Status** | **v0.2 — FROZEN** (per CTO). A-09.2 adds Job Dependencies, Failed Jobs, Time-to-Value, and Compounding vs Transactional Jobs. Further changes require *validation evidence*, not more theorizing. |
| **Created** | 2026-07-21 |
| **Depends on** | DOC-02 (pains + JTBD seeds §11), DOC-04 (vocabulary), DOC-05 (Constitution), DOC-06 (Manifesto), DOC-07 (Philosophy), DOC-08 (Personas) |
| **Blocks** | DOC-10 (Service Blueprint), DOC-11 (Customer Journey), DOC-12 (Functional Requirements), and — via the governance rule (§8) — *every* future feature |
| **Why it's high-leverage** | Written well, this backbones Product, Sales, Marketing, Customer Success, Pricing, Roadmap, AI Strategy, and Architecture. Written poorly, everything downstream drifts. It forces the whole company to think in **customer psychology**, not features. |
| **Vocabulary** | Uses DOC-04 frozen terms exactly. Introduces **no** new business terms. |
| **Scope discipline** | Answers **why each party "hires" our product to make progress** — their jobs and the forces around the decision. It does **not** re-describe *who they are* (that is DOC-08) and does **not** specify features (that is DOC-12). |

---

## How to read this document — and the Swap Test

**Personas (DOC-08) answer *who they are*. JTBD (this) answers *why they hire us to make progress*.** These must feel like different documents.

> **The Swap Test (a standing quality bar):** *if any section here could be moved into DOC-08 (Personas) without anyone noticing, the separation is too weak and the section must be rewritten.* Personas describe context and identity; JTBD describes the **job, the forces, and the moment of progress.** If you catch yourself re-describing who Rina *is*, stop — describe the *job she hires us to do* and *why*.

**The frameworks we use** (per the CTO's direction):
1. **Job hierarchy** — every job has three layers: **Functional** (the practical task), **Emotional** (how they want to feel), **Social** (how they want to be seen). Great products serve all three; feature-thinking serves only the functional.
2. **Decision Forces** (Intercom's model, *extended for us*) — the psychology of the switch:
   `Current Situation → Push → Pull → Anxiety → Habit → Trust Moment → Success Moment.`
   We add **Trust Moment** and **Success Moment** because *trust is our moat* (DOC-03, DOC-06) — the decision is not made when they buy, but when they *believe*, and it is not validated until they *feel it was worth it*.
3. **Job classification** — every job is tagged with **Priority** (Mission-Critical / Strategic / Operational / Nice-to-have), **Frequency** (daily / weekly / monthly / quarterly / annual), and a **measurable Success definition.** These become roadmap guidance and product KPIs.
4. **Negative JTBD** — the jobs we **refuse** to be hired for (§7). Naming anti-jobs is as important as naming jobs.

**Decision Forces — what each force means:**
| Force | The question it answers |
|---|---|
| **Current Situation** | What are they doing today (the status quo we're displacing)? |
| **Push** | What pain pushes them *away* from the status quo? |
| **Pull** | What future *attracts* them toward a new solution? |
| **Anxiety** | What fear might stop them from switching / trusting? |
| **Habit** | What inertia keeps them with the current process? |
| **Trust Moment** | What makes them *finally believe* it works? *(our moat)* |
| **Success Moment** | When do they say *"this was worth it"*? *(validation)* |

---

## 1. Why JTBD Is the Backbone

- **It converts the whole company from feature-thinking to progress-thinking.** A feature list asks "what can we build?"; JTBD asks "what progress is someone trying to make, and are we the best way to make it?" That reframing is the difference between a coherent product and a pile of features (DOC-07 C6/§11).
- **It is the demand-side complement to the supply-side philosophy.** DOC-07 says what we *believe*; JTBD says what the *market is trying to accomplish*. Where they meet is the product.
- **It carries a governance rule (§8) that keeps the product coherent for a decade:** every feature must map to exactly one primary Job. That rule, enforced, prevents the drift the CTO warned about.

---

## 2. The Master Job (the one job the whole product serves)

Beneath every persona's jobs is a single overarching Job the product exists to do (derived from DOC-02 §11.6):

> **"Help me make a hiring decision — *after candidates have already applied through my own systems* — that I can trust and defend, based on what each candidate can *actually do* (evidence, not resumes), without forcing anyone to change how they already work."** *(Boundary-clarified: our job begins **after** application and ends when hiring intelligence is delivered back — Product Boundary, DOC-12 KD-12.7.)*

- **Functional:** make better, evidence-based hiring decisions.
- **Emotional:** feel *confident and unexposed* — relief, not anxiety (DOC-06 A2).
- **Social:** be seen (by managers, boards, candidates, regulators) as fair, thorough, and defensible.

Every persona's jobs below are facets of this master job. If a persona job doesn't ladder up to it, question the job.

---

## 3. Rina — Head of Talent Acquisition · *Jobs & Forces*

### 3.1 The jobs she hires us for
- **Functional:** *"Turn a flood of applicants into a small, evidence-backed shortlist I can defend."*
- **Emotional:** *"Feel confident and in control — not overwhelmed, not exposed when challenged."*
- **Social:** *"Be seen by hiring managers and leadership as strategic and rigorous — not a resume-forwarder."*

### 3.2 Decision Forces
| Force | For Rina |
|---|---|
| **Current Situation** | Screening hundreds of applicants per req on weak signal, in the ATS + inbox; blamed for quality she can't see. |
| **Push** | The AI-generated application flood (DOC-02 P-R1); a bad hire she got blamed for; a hiring manager who stopped trusting her shortlists. |
| **Pull** | Shortlists she can *defend with evidence*; her time back; restored credibility with managers. |
| **Anxiety** | *"Will it replace me? Will it be a black box I can't explain? Will it make me look worse when it's wrong? Will managers/candidates reject it?"* |
| **Habit** | Manual keyword screening in the ATS she knows — "better the devil I know." |
| **Trust Moment** | When she sees the **Evidence** behind a **Recommendation**, repeats the reasoning to a hiring manager convincingly, **and the manager agrees.** |
| **Success Moment** | *"The hiring manager accepted my shortlist without re-screening."* → *"Finally — I can defend my shortlist."* |

### 3.3 Job classification
| Job | Type | Priority | Frequency | Success definition (measurable) |
|---|---|---|---|---|
| Build a defensible evidence-based shortlist | F | **Mission-Critical** | **Daily** | Hiring manager accepts the shortlist **without re-screening**. |
| Separate signal from noise at scale | F | Mission-Critical | Daily | Time spent on unqualified candidates ↓ sharply; no strong candidate missed. |
| Defend a decision when challenged | E/S | Strategic | Weekly | She can produce the evidence trail on demand and it holds up. |
| Calibrate a role with the hiring manager | F | Operational | Weekly (per new req) | Manager agrees the captured bar matches their real bar. |

### 3.4 Negative JTBD (Rina)
- ❌ *"Help me auto-reject 10,000 people so I don't have to look."* — **Refused** (violates P2 Human Accountability, P1 fairness). We help her *review the right ones with evidence*, not abdicate the decision.
- ❌ *"Just give me a number to sort by."* — **Refused** (P1/DOC-06 §5 evidence-first; bare "Score" forbidden).

---

## 4. David — VP Engineering / Hiring Manager · *Jobs & Forces*

### 4.1 The jobs he hires us for
- **Functional:** *"Tell me — with evidence, against *my* bar — which candidates can actually do the work, so I stop wasting my engineers' time."*
- **Emotional:** *"Replace the anxiety of gut-based hiring with confidence in a hire I'll live with."*
- **Social:** *"Be seen as a leader who builds a strong team fairly, and be able to defend my hires to my team and peers."*

### 4.2 Decision Forces
| Force | For David |
|---|---|
| **Current Situation** | Distrusts the funnel, so re-screens and over-interviews; debriefs run on memory and gut; his real bar lives only in his head. |
| **Push** | A costly bad hire he lives with; senior-engineer hours wasted on weak candidates; a debrief that went badly. |
| **Pull** | Trustworthy, evidence-backed candidates calibrated to *his* bar; far less re-screening. |
| **Anxiety** | *"Will it lower my bar? Be shallow or wrong? Hand me paper-good candidates who can't build? Waste my team's time?"* |
| **Habit** | Personally re-screening; trusting only his own interviews. |
| **Trust Moment** | When the **Evidence** survives his technical scrutiny **and** a recommended candidate proves genuinely strong in his own interview — *repeatedly*, across hires (Outcome Learning). |
| **Success Moment** | *"No regret after six months."* → *"I stopped re-screening."* |

### 4.3 Job classification
| Job | Type | Priority | Frequency | Success definition |
|---|---|---|---|---|
| Know who can actually do the work (vs. his bar) | F | **Mission-Critical** | Per hiring cycle (weekly/monthly) | Recommended finalists prove strong in his own review; **no regret at 6 months**. |
| Stop wasting engineers' interview time | F | Strategic | Per cycle | Interview hours per hire ↓ without quality ↓. |
| Own and defend the decision | E/S | Mission-Critical | Per hire | He makes the call with full understanding (P2) and stands behind it. |
| Capture and apply his real bar | F | Operational | Weekly (Calibration) | Company Calibration matches his stated bar; pipeline fits it. |

### 4.4 Negative JTBD (David)
- ❌ *"Tell me who to hire so I don't have to think."* — **Refused** (P2, human-is-hero C7). We make him a *better* decider, never a bypassed one.
- ❌ *"Optimize for candidates who look like my current team."* — **Refused** (P1 fairness; bias proxy). We calibrate to his *bar*, never to sameness.

---

## 5. Sofia — CHRO / Chief People Officer · *Jobs & Forces*

### 5.1 The jobs she hires us for
- **Functional:** *"Give me fair, defensible, measurable hiring at scale — and reduce cost and risk."*
- **Emotional:** *"Let me stop worrying about a bias lawsuit or a headline; feel in control of a risk I own but can't currently see."*
- **Social:** *"Let me stand in front of the board — and, if it comes to it, a regulator — and defend how we hire."*

### 5.2 Decision Forces
| Force | For Sofia |
|---|---|
| **Current Situation** | Accountable for fairness she can't see into; can't prove quality-of-hire; managing tool sprawl; watching AI-hiring regulation with dread. |
| **Push** | A near-miss bias scare; a board question she couldn't answer; new regulation (LL144/EU AI Act); a competitor's bias scandal. |
| **Pull** | A fairness/adverse-impact posture, an audit trail, measurable quality-of-hire, and fewer tools. |
| **Anxiety** | *"Will this *add* legal/brand risk instead of reducing it? Will candidates hate it? Will the board trust it? Is the vendor itself secure and trustworthy?"* |
| **Habit** | Managing fairness via policy documents and training, not tooling; the incumbent HR stack. |
| **Trust Moment** | When she sees the fairness posture, the complete audit trail, **and** a respectful candidate experience — and realizes *she could defend all of it.* |
| **Success Moment** | *"I can defend our hiring to the board."* → *"Finally — I have evidence, and hiring is under control."* |

### 5.3 Job classification
| Job | Type | Priority | Frequency | Success definition |
|---|---|---|---|---|
| Ensure hiring is fair & defensible | F/S | **Mission-Critical** | Continuous / reviewed monthly | Passes fairness/adverse-impact review; can defend any decision on demand. |
| Know & improve quality-of-hire | F | **Strategic** | Monthly / quarterly | Quality-of-hire is measured and trending up (the ultimate metric, DOC-02). |
| Reduce legal/brand/tool risk | E/S | Strategic | Quarterly | No incidents; consolidated stack; board confidence. |
| Report hiring health to leadership | S | Operational | Quarterly | Board accepts the hiring narrative without alarm. |

### 5.4 Negative JTBD (Sofia)
- ❌ *"Help us justify hiring decisions we already made"* / *"make the diversity numbers look good."* — **Refused** (P1; we produce *fair* decisions, not post-hoc justification for biased ones).
- ❌ *"Give us plausible deniability if we're sued."* — **Refused**; we provide *genuine* defensibility (real fairness + evidence), not a liability shield over bad practice.

---

## 6. Marcus — Head of IT & Security · *Jobs & Forces*

### 6.1 The jobs he hires us for
- **Functional:** *"Let me verify this vendor won't leak data, won't cross tenant boundaries, integrates cleanly, and is fully auditable."*
- **Emotional:** *"Let me sign off without fear of being the person who approved a breach."*
- **Social:** *"Let me show I did rigorous diligence — a defensible vendor-risk decision."*

### 6.2 Decision Forces
| Force | For Marcus |
|---|---|
| **Current Situation** | Every new vendor is attack surface and integration risk; he runs reviews to *find reasons to say no.* |
| **Push** | A prior vendor incident; a compliance mandate; a required security review he must pass. |
| **Pull** | Verifiable isolation, clean integration boundaries, auditability, and a vendor that *never becomes a system of record* he'd have to migrate off. |
| **Anxiety** | *"Will it leak? Cross tenants? Become an unmaintainable mess? Am I approving a breach-in-waiting?"* |
| **Habit** | Default-deny to new vendors; trust only the already-approved stack. |
| **Trust Moment** | When the isolation model and data flows are *verifiable* and pass his review — SOC 2, residency, least-privilege, clean boundaries all check out. |
| **Success Moment** | *"I verified it can't hurt us."* → **zero incidents** after a year in production. |

### 6.3 Job classification
| Job | Type | Priority | Frequency | Success definition |
|---|---|---|---|---|
| Verify data safety & isolation | F | **Mission-Critical (gating)** | Once per purchase + periodic re-review | Passes security review; per-company isolation verified. |
| Ensure clean, maintainable integration | F | Strategic | Once per purchase + on change | Integration is bounded, documented, non-SoR (P4). |
| Maintain audit/compliance posture | F/S | Operational | Quarterly / on audit | Full auditability; nothing withheld from audit. |

### 6.4 Negative JTBD (Marcus)
- ❌ *"Help us move fast by skipping the security review."* — **Refused** (P8 trust & security first; his own job forbids it).
- ❌ *"Give us broad data access so integration is easier."* — **Refused** (P3 least-privilege/isolation).

---

## 7. Alex — Candidate · *Jobs & Forces (equal rigor — a lifetime participant)*

*Most hiring platforms model the candidate as `apply → hired → done`. We refuse that (DOC-08 A-08.2/A-08.3; DOC-03 §18.4). The candidate hires us for jobs that span a **lifetime relationship with the network**, not a single transaction.*

### 7.1 The jobs Alex hires us for
- **Functional:** *"Give me a fair chance to show what I can actually do — and something useful back, whatever the outcome."*
- **Emotional:** *"Let me feel *seen and respected*, not judged by a machine or dismissed by a keyword filter; end the black-hole anxiety."*
- **Social:** *"Let me be evaluated on merit regardless of my background or pedigree — and be able to trust, even recommend, the process."*

### 7.2 Decision Forces (why a candidate *engages* vs. abandons)
| Force | For Alex |
|---|---|
| **Current Situation** | Applies into resume-first black holes; judged on an artifact; evaluation-fatigued; wary that "AI hiring" means unfair machine judgment. |
| **Push** | Being filtered out before anyone saw their ability; wasted unpaid take-homes; silent rejections. |
| **Pull** | A fair, *ability-based* evaluation; honest treatment; feedback; being *seen for what they can do*. |
| **Anxiety** | *"Will a machine judge me unfairly with no recourse? Reduce me to a number? Hold my non-traditional background against me? Waste my time? Is AI hidden from me?"* |
| **Habit** | The resume-and-hope ritual; deep distrust of automated hiring. |
| **Trust Moment** | When the evaluation *feels fair*, AI involvement is **honestly disclosed** (DOC-06 A1), and — **even in rejection** — they receive respectful, evidence-based feedback that is genuinely useful. |
| **Success Moment** | *"I believe I had a fair chance"* — said **even when rejected**. → *"Finally — someone evaluated what I can actually do."* |

### 7.3 The candidate's lifetime jobs (across the arc)
`Discover → Apply → Evaluate → Decision → (Rejected?) → Learn → Improve → Future Role → Referral → Community → [Hiring Manager] → [Buyer]`

| Stage | The job Alex hires us for | Success definition |
|---|---|---|
| Discover / Apply | "Let me enter without changing how I apply, and trust it's fair" (P11) | Applies with low friction; senses fairness up front. |
| Evaluate | "Let me show real ability, not decode keywords" | Feels the evaluation measured what they can do. |
| Decision / Rejected | "Treat me with dignity even in a no" | Rejection feels fair, not arbitrary; *"not the strongest match,"* never *"not good enough."* |
| Learn / Improve | "Give me something useful to grow" | Leaves with evidence-based feedback + a learning direction (P13). |
| Future Role / Referral / Community | "Keep me as a respected participant, re-engage me fairly" | Returns as a Future Candidate; refers others; advocates (Candidate Afterlife). |
| → Hiring Manager / Buyer | *(evolution, DOC-08 A-08.3)* "Remember I was treated fairly when I'm on the other side" | Becomes a trusting future user/buyer. |

### 7.4 Job classification (Candidate)
| Job | Type | Priority | Frequency | Success definition |
|---|---|---|---|---|
| Get a fair, ability-based evaluation | F/S | **Mission-Critical (the mission)** | Per application | *"I had a fair chance"* — even if rejected. |
| Be treated with dignity, especially in rejection | E/S | **Mission-Critical** | Per outcome | No black hole; respectful, evidence-based feedback. |
| Get useful feedback / a path to improve | F/E | **Strategic** (Afterlife/network) | Per outcome | Leaves with a genuine learning direction (P13). |
| Remain a respected network participant | S | Strategic (moat/flywheel) | Ongoing | Willing to re-engage, refer, advocate. |

### 7.5 Negative JTBD (Alex)
- ❌ *"Tell me exactly how to game the interview/evaluation."* — **Refused** (integrity; protected by Integrity Score, DOC-04; would corrupt fairness for others). We help Alex *show real ability*, never *fake it*.
- ❌ *"Guarantee me a job / pass me through."* — **Refused**; we guarantee a *fair chance*, not an outcome.

---

## 8. The Governance Rule — One Feature, One Primary Job

> **Every feature must map to exactly one *primary* Job-to-be-Done.**
> - Maps to **zero** jobs → **delete it** (it serves no one's progress; DOC-07 §4/§14).
> - Maps to **five** jobs → **split it** (it is really several features; it will confuse and bloat; DOC-07 §A-1 Complexity Budget).

- **Why.** This is the demand-side twin of the Manifesto's *"one decision per screen"* (DOC-06 §4) and the Philosophy's *complexity budget* (DOC-07 §A-1). It keeps the product coherent: every surface exists to advance a specific person's specific progress, and we can always answer *"whose job does this serve?"*
- **How it's used.** Every feature proposal names its **one primary JTBD** (and, optionally, secondary jobs it also helps). Prioritization then flows from the job's **Priority** classification (§9): Mission-Critical jobs earn roadmap; Nice-to-have jobs do not (DOC-07 §6).
- **The refusal test.** If a proposed feature's only honest primary job is a **Negative JTBD** (§3.4–§7.5), it is refused outright — this is where JTBD meets the anti-personas (DOC-08 §7) and the customer-no framework (DOC-07 §12).

---

## 9. Consolidated Job Map (roadmap & KPI backbone)

Mission-Critical and Strategic jobs are where the product must win; Operational jobs support; Nice-to-haves never drive roadmap (DOC-07 §6).

| Job (by persona) | Priority | Frequency | Success metric (→ product KPI) |
|---|---|---|---|
| Rina — defensible evidence-based shortlist | **Mission-Critical** | Daily | Manager accepts shortlist w/o re-screening |
| David — who can actually do the work vs. his bar | **Mission-Critical** | Per cycle | No regret at 6 months |
| Sofia — fair & defensible hiring | **Mission-Critical** | Continuous | Passes fairness review; defensible on demand |
| Alex — fair, ability-based evaluation | **Mission-Critical** | Per application | *"I had a fair chance"* (even if rejected) |
| Alex — dignity in rejection | **Mission-Critical** | Per outcome | No black hole; respectful feedback |
| Marcus — verify data safety & isolation | **Mission-Critical (gating)** | Per purchase + periodic | Passes security review; zero incidents |
| Sofia — know/improve quality-of-hire | **Strategic** | Monthly/Qtly | Quality-of-hire measured & rising |
| David — stop wasting engineer time | **Strategic** | Per cycle | Interview hours/hire ↓, quality steady |
| Alex — useful feedback / remain in network | **Strategic** | Per outcome / ongoing | Learning direction given; re-engages, refers |
| Rina/David — role calibration | **Operational** | Weekly | Captured bar matches real bar |
| Sofia — leadership reporting | **Operational** | Quarterly | Board accepts hiring narrative |
| Marcus — audit/compliance posture | **Operational** | Quarterly | Full auditability |

> **Roadmap guidance:** build for Mission-Critical first, Strategic second (it deepens the moat), Operational as needed; **never let Nice-to-have jobs drive the roadmap** (DOC-07 §6). Frequency guides UX cadence — *daily* jobs must be frictionless and calm (DOC-06 §8); *annual* jobs (renewal) can be heavier.

## Amendment A-09.2 — Dependencies, Failure, Time-to-Value, and Compounding

*Dated 2026-07-21. CTO-ratified; this amendment completes DOC-09, which then **freezes**. Four additions that make the jobs *operational* rather than merely descriptive.*

### A-1 — Job Dependencies (the Job Dependency Graph)

Jobs are not independent — many cannot be done until an upstream job is. Naming these dependencies prevents us from shipping a downstream capability that has nothing to stand on, and it sequences both onboarding and (later) architecture.

**The core value-chain dependency** (each job enables the next):
```
Company Calibration ─▶ Candidate Evaluation ─▶ Evidence Collection ─▶ Recommendation
        ▲                                                                    │
        │                                                                    ▼
   Hiring Memory ◀── Outcome Learning ◀────────────────── Hiring Decision (human, P2)
   (feeds the next Calibration — the loop closes; DOC-03 flywheels)
```

**Key cross-persona dependencies** (Job A blocks Job B):
| Downstream job (blocked) | Depends on (must happen first) | Why |
|---|---|---|
| Rina — build a defensible shortlist | David — define the bar (**Company Calibration**) | Can't evaluate "good" without a bar to evaluate against (INV-5). |
| Alex — trust the process | Marcus — data is protected & isolated (**P3**) | A candidate can't trust a process they fear is unsafe/unfair. |
| Sofia — defend hiring to the board | **Explainability + audit trail** across all decisions (P1/P13) | Nothing to defend with unless the evidence trail exists. |
| Recommendation | Evidence Collection (via Sensors) | No recommendation without evidence (INV-2/INV-4). |
| Outcome Learning / Hiring Memory | Hiring Decision + observed **Outcome** | The loop can't close without a decision and its result. |

- **Why this matters (esp. for DOC-10/architecture):** it reveals the *minimum viable chain* — you cannot deliver Rina's shortlist job without first delivering David's calibration job and the evidence/evaluation jobs beneath it. This is the spine the Service Blueprint (DOC-10) will trace.

### A-2 — Failed Jobs (Failure States → Customer Success triggers)

The most important omission: what happens when a persona *hires the product but never reaches the Trust Moment*? These failure states are the earliest, truest churn signals and become **Customer Success triggers.**

| Persona | Failure state (the job unfulfilled) | Underlying cause to investigate | CS / product response |
|---|---|---|---|
| **Rina** | *"I still don't trust it"* — still manually re-screens | Explanations not convincing; a wrong call eroded trust | Re-establish the Trust Moment: walk the evidence; tighten calibration; show a proven case. |
| **David** | *"I still re-screen the finalists"* | Evaluations felt shallow or missed his bar | Deepen Company Calibration; surface Outcome Learning proof; win one hard case. |
| **Sofia** | *"I still can't confidently defend it to the board"* | Fairness posture/audit trail not visible or credible | Surface adverse-impact reporting + audit artifacts; executive review. |
| **Marcus** | *"I couldn't fully verify it's safe"* | Isolation/audit evidence insufficient | Provide isolation model, SOC 2, data-flow docs; unblock the review. |
| **Alex** | *"I still think it was unfair"* | Experience didn't feel fair; feedback thin; AI felt hidden | Strengthen fairness cues (DOC-06 §3.7), Honest-by-Default disclosure (A1), useful feedback (P13). |

- **The principle:** a **failure state is a signal, not a verdict** — it tells CS and Product exactly which Trust Moment did not land and why. We instrument these as leading churn indicators (they precede renewal risk by months). Persistent failure states are also **product** feedback, not just CS work.

### A-3 — Time-to-Value (Time-to-Trust-Moment)

Every job carries an **expected time to its Trust Moment (TTTM)**. If the Trust Moment takes six months, adoption dies before it arrives. TTTM is a first-class target, tied to First Five Minutes (DOC-06 A5) and time-to-first-relief.

| Persona | The Trust Moment | Target TTTM | If it's too slow… |
|---|---|---|---|
| **Rina** | First defensible shortlist a manager accepts | **Days** (within week 1) | Champion loses faith before internal selling starts. |
| **David** | First recommended finalist who proves strong in his own interview | **First hiring cycle** (weeks) | He keeps re-screening; never climbs past rung 2. |
| **Sofia** | First board-ready fairness/quality report | **First quarter** | The economic sponsor can't justify the spend. |
| **Marcus** | Verified isolation & clean boundaries | **Pre-purchase** (during security review) | The deal never closes (his veto). |
| **Alex** | First evaluation that *feels fair* + honest AI disclosure | **Immediate** (first application) | Candidate abandons; brand/network damage. |

- **The rule:** **shorter TTTM is a design and product priority, not a marketing afterthought.** Each Mission-Critical job's TTTM is a tracked metric; a rising TTTM is an early adoption-failure alarm. (Note the asymmetry: Alex and Marcus must reach trust *immediately/pre-purchase*; Sofia can take a quarter — design cadence accordingly, DOC-08 A-08.2 §A3 frequency.)

### A-4 — Compounding vs. Transactional Jobs *(strategically unique to us)*

Jobs divide into two kinds, and the distinction is the moat:

| | **Transactional Jobs** | **Compounding Jobs** |
|---|---|---|
| Definition | Have a clear end; done when done | Never finish; get better *forever* with use |
| Examples | Build *this* shortlist; make *this* Hiring Decision; run *this* Evaluation | **Hiring Memory**, **Outcome Learning**, **Benchmarking**, the **Evidence Graph** |
| Value shape | Delivered once, per instance | Accrues; each use improves the next (DOC-03 §13 moat) |
| Wins us… | The **day** (immediate relief, adoption) | The **decade** (the moat, defensibility vs. giants) |

- **Why this is strategically load-bearing.** Transactional jobs earn adoption and daily relief; **compounding jobs are the moat** (DOC-03 §13, DOC-07 §7/C4). A competitor can copy a transactional job (build-a-shortlist) but cannot copy a compounding one without our years of accumulated data and outcomes. **We must invest in compounding jobs even though they show little immediate value** — that patience *is* the strategy (DOC-07 §13: long-term over short-term).
- **Design consequence:** transactional jobs are optimized for TTTM and calm (win the day); compounding jobs are optimized for *depth and the closed loop* (win the decade). Never starve the compounding jobs to make a transactional one shinier.

---

## 10. How JTBD Drives Every Function

| Function | How this document backbones it |
|---|---|
| **Product / Roadmap** | Every feature maps to one primary Job (§8); priority classification (§9) sets sequence. |
| **Sales / Marketing** | Message the **Push/Pull** and the **Success Moment**, not features; disqualify Negative-JTBD buyers (anti-personas). |
| **Customer Success** | Activation = reaching each persona's **Trust Moment**; retention = repeated **Success Moments**; maps to the Trust Ladder (DOC-06 A4). |
| **Pricing** | Anchored to the value of the Mission-Critical jobs (defensible decisions), per Candidate Evaluation (KD-03.10) — not to features. |
| **AI Strategy / Evaluation Engine** | Must serve the *evaluation/fairness* jobs (Alex fair chance; David's bar; Sofia's defensibility) — the intelligence exists to do these jobs. |
| **Architecture** | The Service Blueprint (DOC-10) traces how each Mission-Critical job is fulfilled back-stage; architecture serves the jobs, not vice versa. |

---

## 11. Summary

> **Freeze notice (per CTO).** With A-09.2, DOC-09 is **frozen.** JTBD is one of the highest-leverage documents in the company, and it is now complete enough to build and — more importantly — to *validate*. Further changes should be driven by **evidence from real design partners**, not by additional theorizing. At this point we stop *designing* JTBD and start *validating* it.

### 11.1 Key decisions recorded
- **KD-09.1** — Every persona's jobs are modeled at three layers (**Functional / Emotional / Social**) plus extended **Decision Forces** (Current Situation → Push → Pull → Anxiety → Habit → **Trust Moment → Success Moment**). Trust/Success Moments are our moat-driven additions.
- **KD-09.2** — The **Candidate is modeled at equal (greater) rigor** — as a **lifetime network participant**, not a transaction (Discover→…→Buyer).
- **KD-09.3** — **Negative JTBD** are first-class: explicit anti-jobs we refuse per persona (auto-reject, "tell me who to hire," "justify biased hiring," "skip security," "game the interview"), tied to the anti-personas (DOC-08 §7) and gates.
- **KD-09.4** — Every job is classified by **Priority** (Mission-Critical / Strategic / Operational / Nice-to-have), **Frequency**, and a **measurable Success definition** (→ product KPIs).
- **KD-09.5** — **Governance rule:** every feature maps to **exactly one primary JTBD** — zero → delete, five → split. The demand-side twin of "one decision per screen" and the complexity budget.
- **KD-09.6** — The **Master Job** unifies all: *make a hiring decision I can trust and defend, based on what a candidate can actually do, without forcing anyone to change how they work.*
- **KD-09.7** — **Job Dependency Graph** (A-09.2 §A-1): jobs enable jobs (Calibration → Evaluation → Evidence → Recommendation → Decision → Outcome Learning → Memory); downstream jobs can't ship without upstream ones — the spine for DOC-10.
- **KD-09.8** — **Failed Jobs** (A-09.2 §A-2): the un-reached Trust Moment per persona is the earliest churn signal and a first-class **Customer Success + Product** trigger.
- **KD-09.9** — **Time-to-Trust-Moment (TTTM)** (A-09.2 §A-3) is a tracked target per job; Alex/Marcus must reach trust immediately/pre-purchase, Sofia may take a quarter — slow TTTM kills adoption.
- **KD-09.10** — **Compounding vs. Transactional Jobs** (A-09.2 §A-4): transactional jobs win the *day* (adoption); compounding jobs (Hiring Memory, Outcome Learning, Benchmarking) win the *decade* (the moat) and must never be starved for short-term shine.

### 11.2 Open questions (for founder/CTO)
1. **Job-to-KPI instrumentation:** which Success metrics (§9) do we instrument first, and how do we measure the *candidate's* "I had a fair chance" honestly (survey? proxy?) without gaming it?
2. **Panelist/IC jobs:** interviewers pulled into loops have a real job ("run a fair, efficient interview and capture signal") — cover under David now, or add a light JTBD later? *(Recommend: note under David; expand if Service Blueprint reveals a gap.)*
3. **Trust-Moment timing:** for each persona, *when* in the journey should the Trust Moment occur — and is it early enough to survive the first hard test? (A Customer Journey question, DOC-11.)
4. **Negative-JTBD enforcement:** where is the anti-job list enforced operationally — sales qualification, product gating, or both? *(Recommend: both; formalize in GTM + product review.)*

### 11.3 Suggested next document
**DOC-10 — Service Blueprint** (per the revised roadmap). It answers **exactly one question: "What must happen behind the scenes so the user experiences what we promised?"** — front-stage (what the customer/candidate sees) vs. back-stage (**business capabilities only**: application accepted → evidence requested → evaluation orchestrated → recommendation prepared → audit recorded → Hiring Memory updated). **CTO steer (ratified): NO architecture, NO technology** — no Kafka/Redis/Postgres/vector-DB/agents, nothing technical. Only business capabilities. Architecture comes much later (DOC-16). The Job Dependency Graph (A-09.2 §A-1) is its spine.

**Future document logged (CTO):** a **Capability Map** (Capability → Business Service → System → Microservice) to be added after DOC-10/DOC-11 — it bridges business capabilities to architecture and will make DOC-16 much easier. *Placement TBD (roadmap now ~18 docs).*

**Roadmap position:** …08 Personas · **09 JTBD (frozen)** · → **10 Service Blueprint** · 11 Customer Journey · [*Capability Map — TBD*] · 12 Functional · 13 NFRs · 14 AI Strategy · 15 Evaluation Engine · 16 Architecture · 17 Engineering Principles.

---

*End of DOC-09 v0.1. Awaiting founder review of the four open questions (§11.2) before promotion to Ratified.*
