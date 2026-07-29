# Document 01 — Vision & Product Thesis (North Star)

| Field | Value |
|---|---|
| **Document ID** | DOC-01 |
| **Title** | Vision & Product Thesis (North Star) |
| **Status** | Draft v0.2 — core approved (9.8/10) pending minor changes; **amended for the infrastructure reframe, see Amendment A-0.2** |
| **Owner** | Principal Engineer / Technical Documentation Lead |
| **Author** | Founding engineering (this document) |
| **Created** | 2026-07-21 |
| **Reviewers** | Founders / CTO (pending) |
| **Supersedes** | — (foundational document) |
| **Depends on** | Nothing. This is document zero-plus-one; everything depends on it. |
| **Blocks** | DOC-02 through DOC-11 |

> **How to read this document.** This is the constitution's preamble — the *why* the company exists. It intentionally does not contain architecture, schemas, or implementation. If a future decision anywhere in the company contradicts the thesis stated here, either the decision is wrong or this document must be formally amended (with a version bump and founder sign-off). Nothing downstream gets to silently drift from it.

---

## Amendment A-0.2 — Strategic Reframe: "Hiring Intelligence Infrastructure," not an "AI Hiring Platform"

*Dated 2026-07-21. CTO-directed, issued after DOC-01/02 review. This amendment is authoritative: wherever earlier language in this document says "AI Hiring Platform" or implies our product is an "AI interview," read it as superseded by the framing below. The vocabulary here must propagate into every downstream document.*

**A. We are infrastructure, not a SaaS app, and not an "AI interview" tool.**
The correct mental model is Stripe (payments infrastructure), Twilio (communications infrastructure), Datadog (observability infrastructure), Snowflake (data infrastructure) — companies that became *embedded in the customer's workflow* and command premium, durable, expansion-driven valuations precisely because ripping them out is unthinkable. We are **Hiring Intelligence Infrastructure**. The target perception is exact and non-negotiable:
> *"Our ATS **manages** hiring. This platform **makes hiring decisions better**."*

**B. The product is hiring-decision quality — not recruiter productivity.** *(This is subtle and massive.)*
We are not "helping recruiters." We are improving hiring *decisions*. The recruiter is **one customer**; hiring *quality* is **the product**. Any future feature justified only by "recruiters will like it" — rather than "this makes the decision better/fairer/more defensible" — is suspect. This distinction reorders product, pricing, sales, and valuation.

**C. AI interviews, coding tests, and assessments are *sensors*, not the product.**
They are evidence-collection instruments that feed the intelligence layer. If we ever *sell* "AI interviews," we have reduced ourselves to a commoditizable feature that a platform giant can clone in a quarter (see F). We sell *intelligence*; we *use* interviews and assessments as inputs to it.

**D. The vision is a compounding Hiring Intelligence Network, not a static evidence layer.**
```
      Company A ──▶ Hiring Intelligence ──▶ Candidate ──▶ Evaluation ──▶ Outcome
          ▲                                                                  │
          └──────────────────  Learning  ◀───────────────────────────────────┘
                                   │
                                   ▼
                            Next Candidate  (the system is now smarter)
```
Three network concepts are now Day-1 canon:
- **Hiring Memory** — the system learns *how a company hires, how a specific manager thinks, how its successful employees behave, and how its failed hires behaved* — then evaluates new candidates against that living memory. This is the single most defensible capability we can build.
- **Benchmarking** — because evaluations accumulate across the network, we can tell a customer things no single company could ever know alone, e.g., *"This candidate is in the top 2% of 10,000 Python engineers evaluated in the last 12 months."*
- **Candidate afterlife** — rejection is not the end of the relationship. A rejected candidate remains a **network participant**: a future applicant, a future hire elsewhere, a referral source, and a future advocate. (This also resolves DOC-01 §14 Q4 / DOC-02 §14 Q4 in favor of **"the candidate is a first-class user of the network."**)

**E. Moat preview — the moat is NOT the AI.**
LLMs are a commoditizing input available to every competitor, including the giants. Our moat is the *compounding system* that AI alone cannot reproduce: **Evidence Graph + Evaluation Engine + Company Calibration + Hiring Memory + Outcome Learning + Explainability + Trust + Enterprise Integrations + Network Effects + Data Flywheel.** Nobody copies that overnight, because most of it is *earned over time and across a network*, not built. Full treatment in DOC-03 and a dedicated future **Moat Strategy** document.

**F. Platform Risk is a first-class, possibly existential risk.**
Our most dangerous competitor is not HireVue, Mercor, or CodeSignal. It is a platform giant — **Microsoft, Google, Amazon, LinkedIn, Workday, SAP** — bundling "good-enough" AI evaluation into a channel they already own (e.g., "AI Interview" inside LinkedIn). If that happens, a large share of the market could vanish overnight. This risk was under-weighted in DOC-01/02 and receives a full **Platform Risk Analysis** in DOC-03.

**New decisions ratified by this amendment** (added to §13):
- **D-01.6** — We are **Hiring Intelligence Infrastructure**, positioned and priced as infrastructure (Stripe/Twilio/Datadog/Snowflake class), not as a SaaS app or an AI-interview tool.
- **D-01.7** — **Hiring-decision quality is the product**; recruiters (and every other role) are customers of it.
- **D-01.8** — **AI interviews/assessments are sensors**, never the headline product.
- **D-01.9** — We are building a **Hiring Intelligence Network** with **Hiring Memory, Benchmarking, and Candidate Afterlife** as Day-1 concepts; the candidate is a first-class user.
- **D-01.10** — The **moat is the compounding system, not the LLM** (full treatment DOC-03 + Moat Strategy doc).
- **D-01.11** — **Platform Risk** (giants bundling hiring intelligence) is a first-class strategic risk requiring an explicit survival strategy (DOC-03).

---

## 1. Purpose of this document

To state, from first principles, the following and nothing else:

1. The **problem** we exist to solve, and why it is real.
2. The **bet** (thesis) we are making about how to solve it.
3. What we **are** and, just as importantly, what we **refuse to be**.
4. The **beachhead** — the narrow market and use case we will win first.
5. What **"winning"** concretely means (success definition + North Star).
6. The **prime directive** that breaks ties when good principles conflict.
7. The **strategic bets, risks, and non-goals** a new engineer must internalize on day one.

A new engineer who reads only this document should be able to explain, in an elevator, *what we are building and why it will win* — without ever using the word "resume" as a noun of praise.

---

## 2. The problem (first principles)

Hiring today is **resume-first**. The resume is a candidate-authored, unverified, keyword-optimized marketing document, and it is the primary gate through which nearly every professional opportunity flows. This creates four compounding failures:

1. **It measures the wrong thing.** A resume measures a candidate's ability to *describe* work, their access to prestigious signals (schools, brand-name employers), and their skill at keyword optimization. It does not measure their ability to *do* the work. The correlation between "good resume" and "good hire" is weak and heavily confounded by privilege.

2. **It is trivially gamed and increasingly synthetic.** Keyword stuffing, embellishment, and — as of the last few years — LLM-generated resumes and cover letters have collapsed whatever weak signal the resume carried. Recruiters now filter AI-generated text with more AI. The arms race has made the artifact nearly meaningless.

3. **It is unfair and legally fragile.** Resume screening (human or automated) encodes bias: name-based discrimination, school pedigree, employment-gap penalties, non-linear career paths. In the US this is not merely unethical — it is legally actionable (Title VII disparate impact, EEOC scrutiny, NYC Local Law 144). Yet almost no one can *explain* why a given resume was rejected. The decision is a black box made of gut feel.

4. **It is not evidence-based.** The single most predictive practice in hiring research — structured, work-sample and skills-based evaluation — is expensive, inconsistent, and applied late in the funnel (if at all), because it does not scale with human effort. So the highest-signal evaluation happens last and least, while the lowest-signal artifact (the resume) gates everything.

**The core injustice and inefficiency:** the highest-signal information about a candidate (can they actually do the job?) is collected last, at greatest cost, and to the fewest people — while the lowest-signal information (a self-authored document) decides who ever gets that far.

> First-principles restatement: *Hiring optimizes for the legibility of the candidate to a busy human skimming a document, not for the candidate's ability to do the work.* We intend to invert that.

---

## 3. The bet (thesis)

> **We bet that hiring will move from resume-first to evidence-first, and that the winning company will be the one that owns the neutral, explainable *intelligence layer* that produces and connects that evidence — not a new place to store jobs or applicants.**

Three sub-bets sit underneath this:

- **3.1 — Evidence beats artifacts.** Structured evidence of ability (adaptive technical evaluation, work-sample reasoning, calibrated behavioral signal) will out-predict resumes, and once it is cheap to produce at scale, buyers will demand it. AI is what makes it cheap at scale for the first time in history. This is *why now.*

- **3.2 — The value is in the connective layer, not any single evaluation.** Coding assessments exist. Interview bots exist. Resume parsers exist. None of them wins, because a point solution is a feature, not a system. The durable value is the **intelligence layer** that unifies: resume understanding → company & role context → hiring-manager calibration → adaptive interviews → technical assessment → behavioral assessment → explainable evidence → a defensible recommendation. Whoever owns that connective tissue owns the decision.

- **3.3 — Adoption requires invisibility.** The candidate must not have to change how they apply. The recruiter must not have to change how they hire. We integrate into existing workflows (ATS, no-ATS, email, API, webhooks) rather than demanding migration. A platform that requires behavior change dies in procurement; a platform that slots into the existing motion spreads.

If all three sub-bets are true, the company is inevitable. If sub-bet 3.1 is false (evidence does *not* out-predict resumes, or buyers never demand it), the entire thesis collapses — this is the bet to validate earliest and hardest.

---

## 4. What we are — and what we refuse to be

### 4.1 What we are

> **Hiring Intelligence Infrastructure: the neutral, explainable intelligence layer that turns how a candidate actually thinks and performs into evidence, and turns that evidence — through company calibration, hiring memory, and outcome learning — into a defensible hiring decision, embedded into the hiring systems companies already use.**

We are the *layer of judgment*, not the system of record. We plug into the systems of record (ATS, email, HRIS) and make the decisions running through them better. (See Amendment A-0.2: we are *infrastructure*, our product is *decision quality*, and interviews/assessments are *sensors* feeding the intelligence layer — not the product itself.)

### 4.2 What we refuse to be (non-negotiable)

| We are NOT | Why the distinction matters |
|---|---|
| **An ATS** | We do not want to own applicant storage, requisition management, or offer workflows. Competing with Workday/Greenhouse on their turf is a losing, capital-intensive war and forces customer migration — violating sub-bet 3.3. We make the incumbent ATS better; we don't replace it. |
| **A job board / portal** | We are not in the candidate-sourcing or job-listing business. We do not monetize attention or applications. Our value is evaluation quality, not traffic. |
| **A resume parser / keyword matcher** | That is the very thing we exist to kill. If we ship a better keyword matcher, we have failed at the mission. |
| **A single-purpose coding-test vendor** | Point solutions (HackerRank, CodeSignal) are features we will subsume, not the category we compete in. |
| **A black box** | An unexplainable score is legally and ethically indefensible in hiring. If we cannot show the evidence behind a recommendation, we do not ship the recommendation. |

> **Decision D-01.1:** We are *integration-native Hiring Intelligence Infrastructure* — a neutral, embedded intelligence layer — never a system of record. This is a permanent architectural, commercial, and valuation commitment, not a phase. (Extended by D-01.6–D-01.11 in Amendment A-0.2.)

---

## 5. Beachhead — where we win first

Winning a market means dominating a narrow front before broadening. Our confirmed beachhead:

| Dimension | Beachhead choice |
|---|---|
| **Customer segment** | Mid-market technology companies, ~100–5,000 employees, with meaningful hiring velocity and (usually) an existing ATS. |
| **Roles evaluated** | Software Engineering, Product, Data, DevOps, QA, and AI roles. |
| **Regulatory center of gravity** | **US-first** (EEOC / OFCCP / Title VII adverse-impact, NYC LL144 bias-audit regime), on a **privacy- and compliance-aware architecture** designed so global expansion (GDPR, EU AI Act, India DPDP) needs *no major redesign* — only added modules. |
| **First commercial use case (the wedge)** | **AI-powered first-round screening & evaluation for software engineering roles.** |

**Why this beachhead** — *(required framing)*

- **Why.** Mid-market tech firms hire fast, feel screening pain acutely, already trust developer tooling, have real budgets, and have far shorter sales cycles than the enterprise. Engineering roles are where evidence-based evaluation is most tractable (skills are demonstrable and relatively objective) and where the "resume is meaningless" pain is sharpest. US-first concentrates our compliance investment on the largest single market.
- **Advantages.** Fast feedback loops, high hiring frequency (more data, faster learning), technically literate buyers, a domain where "prove you can do it" is culturally accepted by candidates.
- **Tradeoffs.** We deliberately underserve non-tech roles, SMB/high-volume hourly hiring, and large enterprises at launch. We will be told "but what about sales roles / hourly roles / Europe?" — and we will say *not yet, on purpose.*
- **Risks.** (a) Engineering-hiring evaluation is a crowded, opinionated space with strong incumbents and skeptical candidates ("not another LeetCode gate"). (b) Over-fitting the platform to engineering could create architecture that doesn't generalize to other roles later. (c) Mid-market budgets can evaporate in downturns.
- **Alternatives considered.** Enterprise-first (rejected: 12–18mo sales cycles kill a startup's learning loop); SMB/high-volume (rejected: thin margins, low willingness to pay for "intelligence"); staffing/RPO (rejected: multi-tenant-within-tenant complexity on day one); end-to-end from launch (rejected: unfocused, unshippable). See DOC-02 for full competitive treatment.

> **Decision D-01.2:** Beachhead = mid-market US tech companies, engineering roles, first-round screening & evaluation. Everything else is post-beachhead.

---

## 6. The Intelligence Layer (the heart of the product)

This section captures the founding insight that the product is *not* any single capability but the layer that connects them. It is the single most important concept in the company.

```
                         THE INTELLIGENCE LAYER
                         (neutral · explainable · evidence-producing)

  INPUTS (from the world, unchanged)          THE LAYER (what we own)                 OUTPUTS (into existing systems)
  ─────────────────────────────────          ───────────────────────────            ──────────────────────────────
  • Candidate application (resume,     ┌───────────────────────────────────┐         • Explainable recommendation
    profile, however it arrives)  ───► │ 1. Resume / candidate understanding│  ───►     (with evidence trail)
  • Job & role definition        ───►  │ 2. Company & role context          │         • Structured evidence record
  • Company context / values     ───►  │ 3. Hiring-manager calibration      │         • Ranked, defensible shortlist
  • Hiring-manager preferences   ───►  │ 4. Adaptive interview / evaluation  │  ───►   • Audit artifact (fairness,
  • Candidate responses/work     ───►  │ 5. Technical assessment             │           reasoning, provenance)
                                       │ 6. Behavioral assessment            │
                                       │ 7. Evidence synthesis               │  ───►   Delivered via:
                                       │ 8. Explainable recommendation       │         ATS · email · API · webhook
                                       └───────────────────────────────────┘
```

Key properties the layer must hold (elaborated in DOC-03 and DOC-08):

- **Neutral.** It does not care which ATS, which email system, or which workflow the customer uses. Inputs and outputs are adapters; the intelligence is the same.
- **Explainable by construction.** Every output carries the evidence and reasoning that produced it. Explainability is not a report generated after the fact — it is a property of how the recommendation is built.
- **Composable.** Each capability (1–8) is independently valuable but exponentially more valuable connected. The MVP lights up a subset; the architecture must never preclude the rest.
- **The wedge is a slice, not a different product.** First-round SWE screening exercises capabilities 1, 2, 4, 5, 7, 8 in a thin vertical. The platform we architect is the full layer; the product we *sell first* is one honest slice of it.

> **Decision D-01.3:** The unit of value is the intelligence layer, not any single evaluation. No roadmap or architecture decision may treat a capability (1–8) as a standalone product that forecloses the others.

---

## 7. Vision across three horizons

To keep focus without losing ambition, we hold the vision in three horizons. Only Horizon 1 is a commitment; Horizons 2–3 are direction, not roadmap.

- **Horizon 1 — Prove the layer (the beachhead).** Own first-round SWE screening & evaluation for US mid-market tech. Deliver explainable, evidence-based shortlists that recruiters trust more than resumes, integrated invisibly into their existing ATS/email flow. **Success = customers stop reading resumes first for these roles.**

- **Horizon 2 — Broaden the layer.** Extend across the full funnel (deeper interviews, behavioral depth, hiring-manager calibration loops) and across role families (product, data, then beyond engineering). Add connector breadth (more ATSs, more workflows). Begin international (EU) on the compliance-ready foundation.

- **Horizon 3 — Become the standard of hiring judgment.** The neutral, auditable evidence standard that enterprises and regulators point to — the "credit score, but explainable and fair" of hiring ability. Serve millions of candidates and thousands of enterprises. Evidence is portable, candidate-owned, and reusable.

---

## 8. What "winning" means (success definition + North Star)

A vision without a definition of winning is a wish. We define winning at two levels.

### 8.1 The mission-level success condition
> **A hiring decision in our domain is considered "won" when the recruiter/hiring manager made it primarily on explainable evidence of ability — and would be comfortable defending that decision to a rejected candidate, a regulator, and their own conscience.**

### 8.2 North Star metric (proposed — requires validation)

> **Proposed North Star: "Evidence-Backed Decisions" — the number (and %) of hiring decisions made through our platform that are backed by an explainable evidence trail rather than resume/gut-feel.**

- **Why this metric.** It is the most direct measurable proxy for the mission (kill resume-first hiring). It is a *value* metric, not a *vanity* metric — it grows only when we deliver the core promise. It aligns every team: producing more trustworthy evidence and getting recruiters to actually rely on it.
- **Advantages.** Ties revenue to mission; hard to game without delivering real value; understandable to founders, engineers, and customers alike.
- **Tradeoffs / risks.** Harder to instrument than a raw usage count; "backed by evidence" needs a rigorous, non-gameable definition (see unresolved questions); a recruiter can *receive* evidence and still ignore it, so we may need a companion "evidence-reliance" signal.
- **Alternatives considered.** *Quality-of-Hire uplift* (the truest outcome metric, but slow — feedback takes 6–18 months and is noisy); *time-to-shortlist* (efficiency, but a faster black box is not our mission); *recruiter adoption/seats* (leading indicator, but vanity-prone). We will likely track Quality-of-Hire as the *ultimate* validation metric and Evidence-Backed Decisions as the *operational* North Star. **To be confirmed in a dedicated metrics document.**

---

## 9. The Prime Directive (tie-breaker) — and a recommended refinement

When two good principles conflict, the company needs a *deterministic* tie-breaker so decisions don't devolve into whoever argues loudest. You provided this ordering:

> **Stated order:** Enterprise Security & Trust → Evaluation Accuracy → Fairness & Explainability → Integration Ease → Time-to-Value.

I am adopting Security & Trust as #1 without reservation — for an enterprise hiring platform holding sensitive candidate data, that is correct and non-negotiable. But I must formally challenge the placement of **Evaluation Accuracy above Fairness & Explainability**, because in *this specific domain* that ordering is internally inconsistent with putting Trust first. My reasoning *(this is me doing my job, not overruling you — the decision remains yours)*:

**Why the stated order is risky:**

1. **Explainability is frequently a legal precondition, not a quality attribute.** NYC Local Law 144 mandates bias audits of automated employment decision tools; EEOC disparate-impact doctrine requires you to justify screening criteria; the EU AI Act (Horizon 2) classifies hiring AI as "high-risk" and mandates transparency and human oversight. A more-accurate model you cannot explain is, in several of our own target jurisdictions, *illegal to deploy.* Ranking accuracy above explainability can produce a product we are not allowed to sell — which directly violates "Security & Trust first," since trust includes legal defensibility.

2. **"Accuracy" in hiring is philosophically contested.** Accurate against *what label?* The only cheap ground-truth labels are historical hiring outcomes — which encode exactly the biased, resume-first decisions we exist to replace. Naively maximizing accuracy-to-historical-outcomes launders yesterday's bias into an algorithm. In hiring, **fairness is partly constitutive of correctness**; they are not cleanly separable priorities you can rank.

3. **A single bias headline or lawsuit is existential for a hiring-AI startup.** The asymmetry of harm is enormous: a marginal accuracy gain is worth little against the tail risk of being the cautionary-tale defendant.

**Recommended refinement (my proposal, for your decision):** Treat Fairness & Explainability not as a *rankable* priority but as a **non-negotiable gate** — a floor every solution must clear — and *then* rank the remaining priorities. Formally:

> **Proposed Prime Directive:**
> **Gate (must pass, non-negotiable): Fairness & Explainability.** No recommendation ships without a defensible, auditable evidence trail and adverse-impact safeguards.
> **Then, among solutions that clear the gate, rank:** (1) Security & Trust → (2) Evaluation Accuracy → (3) Integration Ease → (4) Time-to-Value.

This preserves almost all of your intent — Security first, and accuracy prized well above convenience — while removing the scenario where we knowingly ship a more-accurate-but-indefensible system. It converts a dangerous ordering into a safe one at essentially no cost to velocity, because the gate is something we must build anyway to sell to enterprise legal teams.

- **Advantages of the gate model.** Legally safe by construction; consistent with "Trust first"; still lets accuracy dominate day-to-day engineering tradeoffs.
- **Tradeoffs.** The gate can occasionally block a tempting high-accuracy approach; defining "clears the gate" rigorously is real work (DOC-11).
- **Risk if we keep the stated order instead.** We build toward a black box, hit a legal/enterprise-procurement wall, and have to re-architect explainability in late — the most expensive possible time.

> **This is the headline unresolved question of DOC-01 (see §13).** I have written the rest of the company's documents to assume the *gate model* unless you direct otherwise.

---

## 10. Strategic bets & assumptions (must be validated)

| # | Assumption | If false, what breaks | How we'll test it |
|---|---|---|---|
| A1 | Evidence-based evaluation out-predicts resumes *and* buyers will pay for it. | The entire thesis (§3.1). | Earliest customer pilots; measure recruiter trust + downstream hire quality. |
| A2 | Recruiters will *act on* AI evidence, not just receive it. | North Star; adoption. | Instrument evidence-reliance in pilots. |
| A3 | Candidates will accept richer evaluation without dropping out. | Top-of-funnel volume; fairness. | Measure completion & drop-off vs. resume-only baseline. |
| A4 | We can integrate invisibly into existing ATS/email flows. | Sub-bet 3.3; go-to-market. | Connector spikes in DOC-06; design partners. |
| A5 | US-first compliance-aware architecture can extend globally without redesign. | Horizon 2 economics. | Architecture review gates in DOC-09/10/11. |

> A new engineer should treat these as *hypotheses under test*, not settled facts. The company's job in Horizon 1 is to convert A1–A4 from assumptions into evidence.

---

## 11. Risks (company-level) — *why / impact / mitigation*

| Risk | Why it's serious | Mitigation direction |
|---|---|---|
| **Regulatory / bias liability** | Hiring AI is high-scrutiny; a disparate-impact finding is existential. | Fairness gate (§9); DOC-11 governance; auditability by construction. |
| **"Just another assessment tool" perception** | Candidates and buyers are fatigued by LeetCode gates and interview bots. | Lead with the *intelligence layer* + explainability + fairness story, not a test. |
| **Incumbent response** | ATS vendors bolt on "AI screening." | Stay integration-native and neutral (we make *all* ATSs smarter); depth of explainable evidence as moat. |
| **Candidate trust / gaming** | If candidates distrust or game the evaluation, signal degrades. | Adaptive, work-sample-oriented evaluation; transparency to candidates; anti-gaming design (later docs). |
| **Over-fitting to engineering** | Beachhead architecture may not generalize. | Design the layer role-agnostic even while the wedge is SWE-only (D-01.3). |
| **Model/vendor dependency & cost** | Core value rides on LLM capability/cost curves. | Provider-abstracted architecture; evidence pipeline not tied to one model (later docs). |

---

## 12. Non-goals (explicitly out of scope, and why)

- **Building an ATS or system of record** — violates D-01.1.
- **Candidate sourcing / job advertising** — not our category (§4.2).
- **Non-engineering roles at launch** — beachhead discipline (§5).
- **Non-US regulatory regimes at launch** — architecture must be *ready*, product need not *ship* them yet (§5).
- **Fully autonomous hire/reject decisions** — we produce *evidence and recommendations for humans*; human-in-the-loop is a permanent principle (reinforces the fairness gate and EU AI Act readiness). *(Flagged for confirmation in DOC-03.)*

---

## 13. Summary of key decisions

- **D-01.1** — We are an integration-native **intelligence layer**, never a system of record (not an ATS, not a job board, not a resume parser, not a black box).
- **D-01.2** — **Beachhead**: US mid-market tech companies, engineering roles, first-round screening & evaluation as the commercial wedge; global-ready but US-first on compliance.
- **D-01.3** — The **unit of value is the connective intelligence layer**, not any single capability; the wedge is a thin vertical slice of the full layer, and architecture must never foreclose the rest.
- **D-01.4 (proposed)** — **North Star = Evidence-Backed Decisions**, with Quality-of-Hire as the ultimate validation metric. *Pending confirmation.*
- **D-01.5 (proposed)** — **Prime Directive = Fairness & Explainability as a non-negotiable gate**, then Security & Trust → Accuracy → Integration Ease → Time-to-Value. *Pending your decision (headline open question).*

---

## 14. Unresolved questions (need your input)

1. **[HEADLINE] Prime Directive:** Do you accept the refinement in §9 — Fairness & Explainability as a *gate* rather than ranked below Accuracy? Or do you want to hold the original strict ordering? Everything downstream currently assumes the gate model.
2. **North Star:** Do you accept "Evidence-Backed Decisions" as the operational North Star, with Quality-of-Hire as the long-term validation metric? Or do you prefer a different primary metric?
3. **Human-in-the-loop:** Confirm that we will *never* make fully autonomous hire/reject decisions — only evidence + recommendations for a human. (Strongly recommended; affects legal posture and product design.)
4. **Candidate as a stakeholder:** Is the candidate a *user* we serve (transparency, feedback, portable evidence) or only a subject we evaluate? This materially changes product scope and our fairness story. *(I recommend "user.")*
5. **Design partners:** Do we already have (or can we get) 3–5 mid-market tech design partners? Assumption A1–A4 validation depends on it.
6. **Naming:** The company/product currently has no name. Not blocking, but we'll want one before external-facing documents.

---

## 15. Suggested next document

**DOC-02 — Market, Competitive Landscape & Positioning.**

- **Why next.** Before we design principles (DOC-03) or personas (DOC-04), we must rigorously map who exists (ATS incumbents, assessment vendors, AI-screening startups, interview-intelligence tools), *precisely* where each fails the thesis, and articulate our defensible wedge and anti-positioning. This sharpens the beachhead into a battle plan and stress-tests whether our "intelligence layer" claim is genuinely differentiated or merely a nicer black box.
- **What it will produce.** A competitor teardown, a positioning statement, our explicit anti-positioning ("we are not X"), moats/defensibility analysis, and the buyer's alternatives (including "do nothing / keep reading resumes").

> **Alternative next step**, if you'd rather lock the constitution before looking outward: jump to **DOC-03 — Product Principles & Non-Negotiables**. My recommendation is DOC-02 first, because good principles are partly a *response* to the competitive reality, and I'd rather not codify principles in a vacuum.

---

*End of DOC-01 v0.1. Awaiting founder sign-off on the five decisions and six unresolved questions above before this is promoted from Draft to Ratified.*
