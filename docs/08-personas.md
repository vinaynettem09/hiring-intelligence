# Document 08 — Personas

| Field | Value |
|---|---|
| **Document ID** | DOC-08 |
| **Title** | Personas |
| **Owner** | Principal Engineer / Technical Documentation Lead (with Product & GTM) |
| **Status** | v0.3 — A-08.2 (Relationship Map, Success Metrics, Lifecycle States) + **A-08.3 (Persona Conflict Matrix, Persona Evolution, Non-user Stakeholders)** |
| **Created** | 2026-07-21 |
| **Depends on** | DOC-02 (pains), DOC-03 (KD-03.11 buyer map), DOC-04 (vocabulary), DOC-05 (Constitution), DOC-06 (Manifesto: fears, emotional journeys, relief), DOC-07 (Philosophy) |
| **Blocks** | DOC-09 (Jobs-To-Be-Done), DOC-10 (Customer Journey), and all downstream product/GTM work |
| **Scope discipline** | Personas describe **WHO** the users are — their context, goals, pains, fears, and trust conditions. They do **not** describe *why they "hire" the product* (that is DOC-09 JTBD) and do **not** specify features, screens, or implementation. Each persona is validated against the Constitution/Manifesto/Philosophy. |
| **Vocabulary** | Uses DOC-04 frozen terms exactly. Introduces **no** new business terms. |

---

## How to read this document

These are **decision-context personas**, not marketing demographics. We do not care about their favorite apps or their commute; we care about the **decision they are trying to make (or survive), what they fear, what earns their trust, and the emotional journey the product must move them through.** Each persona is grounded in the real pains of DOC-02 and tested against three fixed references:

- **Constitution (DOC-05):** does serving this persona's *wants* ever require violating a gate? (If so, we serve the *need*, not the want — §12 of DOC-07.)
- **Manifesto (DOC-06):** what must this persona *feel* (relief, A2), what fear must we remove (A6), and what emotional transition must we drive (A3)?
- **Philosophy (DOC-07):** we serve the *decision*, and each persona *through* it (C11) — never one persona at the decision's expense.

**Persona ≠ JTBD.** This document answers *who they are*. DOC-09 answers *why they hire us* (their functional, emotional, and social jobs). We keep goals/pains here and reserve the "jobs" framing for DOC-09, deliberately.

**On names and pronouns.** Each persona has a first name for memorability; all are fictional archetypes, referred to with they/them. A name is not a demographic claim.

**The template** (applied identically to all five core personas):
> Identity · Context (their world) · Goals · How they're measured · Pains (DOC-02) · Fears (DOC-06 A6) · What earns their trust · Emotional journey (DOC-06 A3) · The relief moment (DOC-06 A2) · Trust-Ladder position · Relationship to the product · Role in the buying decision (KD-03.11) · What they must NEVER feel · Progressive-Explainability view (P13) · Constitutional check · Representative quote.

---

## 1. Persona overview (the core five)

| # | Persona | Role in hiring | Role in the deal (KD-03.11) | Why they matter most |
|---|---|---|---|---|
| P-1 | **Rina — Head of Talent Acquisition** | Runs the funnel | **Primary buyer & champion** | Feels the pain daily; our first and loudest advocate. |
| P-2 | **David — VP Engineering / Hiring Manager** | Owns the role & the hire | **Engineering-hiring champion; quality authority** | Owns the outcome; his trust makes or breaks adoption. |
| P-3 | **Sofia — CHRO / Chief People Officer** | Owns hiring org, fairness, brand | **Economic approver** | Signs the budget; accountable for fairness & compliance. |
| P-4 | **Marcus — Head of IT & Security** | Guards data & integrations | **Technical approver (can veto)** | Gatekeeper of adoption; a "no" here stops everything. |
| P-5 | **Alex — Candidate (Software Engineer)** | Is evaluated | **First-class user (not the buyer)** | The mission's subject and a network participant (P7); the ethical heart. |

> **The relationship in one line:** *Rina champions it, David must trust it, Sofia funds it, Marcus must clear it, and Alex must feel fairly treated by it.* All five must be served — through the quality of the decision (C11).

---

## 2. P-1 — Rina, Head of Talent Acquisition *(Primary buyer & champion)*

- **Identity.** Rina leads a small talent-acquisition team at a ~900-person mid-market tech company hiring engineers at volume. Experienced, pragmatic, chronically over-capacity. Judged on outcomes they only partly control.
- **Context (their world).** A dozen open engineering reqs at once. Hundreds of applications per role — now amplified by AI-generated mass-applying (DOC-02 P-R1). Juggling sourcing, screening, scheduling, hiring-manager relationships, and candidate experience — mostly in the ATS (Greenhouse/Ashby/Lever) and their inbox.
- **Goals.** Fill reqs with genuinely qualified people, fast; present shortlists they can defend; keep hiring managers happy; protect the employer brand.
- **How they're measured.** Time-to-fill, pipeline volume, cost-per-hire, hiring-manager satisfaction. *Rarely* quality-of-hire (the metric that actually matters — DOC-02 P-R3).
- **Pains (DOC-02).** Drowning in low-signal volume (P-R1); forced to screen on weak signal they distrust (P-R2); measured on speed but blamed for quality (P-R3); manual coordination overhead (P-R4); no end-to-end evidence trail when challenged (P-R5).
- **Fears (DOC-06 A6).** *"Will AI replace me?"* · *"Will I advance the wrong person and be blamed?"* · *"Will I have to defend a decision I can't explain?"*
- **What earns their trust.** Evidence they can *see* and *repeat* to a hiring manager; consistency; the feeling of being made more competent, not sidelined; nothing that embarrasses them in front of a candidate or manager.
- **Emotional journey (DOC-06 A3).** `Overwhelmed → Organized → Confident → Certain → Defensible.` The product must cut the noise, surface trustworthy evidence, and make the shortlist stand up.
- **The relief moment (DOC-06 A2).** *"Finally — I can defend my shortlist."*
- **Trust-Ladder position (DOC-06 A4).** Enters at rung 1 (does it work?) and rung 2 (do the explanations make sense?); becomes a champion at rung 4 (I depend on it). Our job: get Rina to rung 4 fast — they are the internal salesperson for rung 5 (org trust).
- **Relationship to the product.** The heaviest daily user. Needs the full Recommendation + Confidence + Evaluation Score + Integrity Score + Evidence + Benchmark (P13 recruiter view), delivered inside their existing ATS/email workflow (P11), calm and low-load (DOC-06 §8).
- **Role in the buying decision.** **Primary buyer & champion** (KD-03.11). Feels the pain, runs the pilot, sells internally to Sofia (budget) and David (quality). Our GTM lives or dies on Rina's belief.
- **What they must NEVER feel.** Replaced; second-guessed by a black box; buried in an 80-metric dashboard; forced to defend something opaque.
- **Progressive-Explainability view (P13).** Full recommendation, Confidence, Evaluation Score, Integrity Score, the Evidence, and Benchmark — enough to trust *and defend* the shortlist. Not: cross-company data or raw model internals.
- **Constitutional check.** Rina *wants* speed (time-to-fill) — but we serve speed only through **decision quality** (P9), never by re-privileging the resume (C2) or skipping fairness (P1). If Rina asks to "just auto-advance the top scores," we route to Human Accountability (P2) and evidence-first (DOC-06 §5). We make Rina faster *the right way.*
- **Representative quote.** *"I can move fast. What I can't do is stand in front of a hiring manager and explain why I picked these five — until now."*

---

## 3. P-2 — David, VP Engineering / Hiring Manager *(Engineering-hiring champion; the quality authority)*

- **Identity.** David runs engineering (or a large slice of it) and owns the roles being filled. Technical, opinionated, protective of the team's bar, time-starved. Lives with the hire long after the recruiter has moved on.
- **Context (their world).** Owns the outcome of every hire but distrusts top-of-funnel screening, so re-screens and over-interviews — bottlenecking the process (DOC-02 P-H1). Pulls senior engineers into many unstructured interviews (P-H2). Debriefs run on memory and gut (P-H3). Their real bar is in their head, uncaptured (P-H4).
- **Goals.** Hire people who raise the team's output and can grow; stop wasting scarce engineer-hours on weak candidates; trust the shortlist enough to *not* re-screen.
- **How they're measured.** Team delivery and health; (rarely, explicitly) quality-of-hire. Every bad hire is a personal, expensive, months-long problem for them.
- **Pains (DOC-02).** Owns the outcome but distrusts the funnel (P-H1); interview overload & inconsistency (P-H2); decisions on memory/gut in debriefs (P-H3); the calibration gap — their bar never captured (P-H4).
- **Fears (DOC-06 A6).** *"Will this force a decision I don't understand or can't stand behind?"* · *"Will it lower my bar or hand me candidates who look good on paper but can't do the work?"* · *"Will it waste my engineers' time?"*
- **What earns their trust.** Evidence of *actual ability* (not credentials) mapped to *their* bar; the ability to see *why* a candidate meets the standard; being kept in control as the decision-owner. David trusts depth, not dazzle (C3).
- **Emotional journey (DOC-06 A3).** `Uncertain → Calibrated → Confident → Accountable.` The product captures their real bar (Calibration), shows why each candidate meets it, and lets them own the decision (the felt form of P2).
- **The relief moment (DOC-06 A2).** *"Finally — I understand *why* these candidates."*
- **Trust-Ladder position.** The hardest skeptic; will not climb past rung 2 (explanations make sense) until the reasoning survives their technical scrutiny, and reaches rung 3 (predictions prove correct) only via Outcome Learning over real hires. Winning David is winning the quality argument.
- **Relationship to the product.** Reviews finalists; consumes everything Rina sees **plus** Calibration alignment and Hiring Memory insight for their role/team (P13 hiring-manager view). Wants depth-on-demand, not noise. High-risk decisions (finalists) require their direct review (P2).
- **Role in the buying decision.** **Engineering-hiring champion and quality authority.** If David says "the evaluations are shallow/wrong," the deal dies regardless of Rina's enthusiasm. Their endorsement is the quality proof point.
- **What they must NEVER feel.** Managed by the tool; handed a black-box verdict; pushed toward a decision they don't understand; that the product lowered their bar.
- **Progressive-Explainability view (P13).** Everything the recruiter sees **+** Calibration alignment **+** Hiring Memory insights for their Role/team. Not: other companies' data or raw model internals.
- **Constitutional check.** David may *want* to encode idiosyncratic bar preferences — fine, that's the flexible layer of the Customization Pyramid (DOC-07 §8.1). But if a preference edges toward a bias proxy (e.g., pedigree), Fairness (P1) and evidence-over-artifacts (C2/§9) govern; we surface the risk (P13 to compliance) and hold the gate. We adapt to David's *bar*, never to bias.
- **Representative quote.** *"I don't need the tool to decide. I need it to show me, with evidence, why these five are worth my team's afternoon — and be right often enough that I stop re-screening."*

---

## 4. P-3 — Sofia, CHRO / Chief People Officer *(Economic approver)*

- **Identity.** Sofia owns the people function company-wide: hiring quality and cost, fairness and compliance, employer brand, and the executive narrative about talent. Accountable to the CEO and board for all of it.
- **Context (their world).** Answerable for hiring outcomes they don't directly execute; exposed to fairness/legal risk they can't fully see into (DOC-02 P-HR1); unable to prove or improve quality-of-hire (P-HR2); managing tool sprawl and cost (P-HR3); guarding the employer brand against poor candidate experience (P-HR4). Watching AI-hiring regulation (LL144, EU AI Act) with concern.
- **Goals.** Efficient, *fair*, *defensible* hiring at scale; demonstrable quality-of-hire; a protected brand; fewer, better-integrated tools; no legal/reputational surprises.
- **How they're measured.** Cost, compliance, D&I outcomes, retention/quality-of-hire, executive/board confidence in the people function.
- **Pains (DOC-02).** Accountable for fairness they can't see into (P-HR1); can't prove/improve quality-of-hire (P-HR2); tool sprawl (P-HR3); brand risk from candidate experience (P-HR4).
- **Fears (DOC-06 A6).** *"Will this be biased and get us sued or into the headlines?"* · *"Will candidates hate it and hurt our brand?"* · *"Will the board trust our hiring?"* · *"Am I adding risk or reducing it?"*
- **What earns their trust.** Visible fairness safeguards and audit-readiness; a respectful candidate experience; a defensible evidence trail; a credible story to tell the board and regulators. Sofia buys **calm and defensibility** (DOC-06 §1).
- **Emotional journey (DOC-06 A3, Executive).** `Exposed / Skeptical → Informed → Assured → In Command.` Replace risk-anxiety with aggregate evidence of quality and fairness, and a felt sense of control.
- **The relief moment (DOC-06 A2).** *"Finally — I have evidence, and hiring is under control."*
- **Trust-Ladder position.** Cares most about rungs 3–5 (predictions prove correct → org trusts). Sofia is the buyer of *institutional* trust (rung 5): the point at which "this is how we hire" becomes true.
- **Relationship to the product.** Not a daily user; consumes aggregate decision-quality, fairness/adverse-impact posture, pipeline & benchmark health, and ROI/quality-of-hire trends (P13 executive view). Wants assurance, not mechanics.
- **Role in the buying decision.** **Economic approver.** Sofia signs the budget and owns the fairness/compliance risk. Our fairness/explainability gate (P1/P13) is not a feature to Sofia — it is *the* reason they can say yes.
- **What they must NEVER feel.** Exposed to unquantifiable legal/brand risk; that hiring is a black box they're accountable for; drowning in vanity metrics.
- **Progressive-Explainability view (P13).** Aggregate quality, fairness posture, pipeline/benchmark health, ROI trends. Not: per-candidate internal mechanics (unless also acting as a hiring manager).
- **Constitutional check.** Sofia's interests are almost perfectly aligned with our gates — fairness, explainability, defensibility *are* what they need. The risk is the reverse: if we ever weakened a gate for a different persona's convenience, we would betray Sofia. This persona is a living argument for why the gates are non-negotiable.
- **Representative quote.** *"I don't need magic. I need to stand in front of the board — and if it comes to it, a regulator — and show that our hiring is fair, evidence-based, and defensible."*

---

## 5. P-4 — Marcus, Head of IT & Security *(Technical approver — can veto)*

- **Identity.** Marcus owns data protection, vendor risk, and integrations. Professionally skeptical of new vendors touching sensitive data. Not a champion — a **gatekeeper**. Their job is to find reasons to say no.
- **Context (their world).** Every new tool is attack surface, data-handling risk, and integration burden (DOC-02 P-HR3). Accountable if candidate/employee data leaks. Runs security reviews, demands SOC 2, data-residency clarity, SSO, least-privilege, and clean integration boundaries.
- **Goals.** Zero data incidents; minimal attack surface; clean, maintainable integrations; defensible vendor-risk posture. A tool that is powerful but insecure is worse than no tool.
- **How they're measured.** Incidents (ideally zero), audit outcomes, integration stability, compliance posture.
- **Pains (DOC-02).** Tool sprawl and integration/security surface (P-HR3); being asked to approve vendors that handle sensitive data without rigorous controls.
- **Fears (DOC-06 A6).** *"Will this leak candidate or company data?"* · *"Does it cross tenant boundaries?"* · *"Will it become an unmaintainable integration mess?"* · *"Am I signing off on a breach waiting to happen?"*
- **What earns their trust.** Strict per-company data isolation (P3); consent-governed, never-sold candidate data (P3/P7/KD-03.14); clear integration boundaries (we integrate, never become the system of record — P4); auditability; conservative, security-first defaults (P8).
- **Emotional journey (DOC-06 A3, Administrator).** `Blind / Anxious → Sighted → In Control → Audit-Ready.` Full visibility and clean boundaries move Marcus from fear-of-the-unknown to confident sign-off.
- **The relief moment (DOC-06 A2).** *"Finally — a vendor whose data model and boundaries I can actually verify."*
- **Trust-Ladder position.** Blocks the whole ladder at rung 1 (does it work — safely?). Marcus doesn't need to love the product; they need to be unable to find a reason to reject it. Security-first (P8) is what clears them.
- **Relationship to the product.** Not an evaluation user; cares about data flows, isolation, integration surface, and audit. Aligns with the Administrator/Compliance view (full auditability, P13) on the *governance* side.
- **Role in the buying decision.** **Technical approver with veto.** A "no" from Marcus stops the deal regardless of Rina, David, and Sofia. This is precisely why P8 (Trust & Security first among rankables) and P3 (isolation) are Tier-0/Tier-2 — Marcus is their embodiment.
- **What they must NEVER feel.** That data handling is vague; that boundaries are fuzzy; that they're being rushed past a real security question; that we're quietly becoming a system of record they'd have to migrate off later.
- **Progressive-Explainability view (P13).** On the governance axis, Marcus/Admin gets **everything** for audit — complete data-flow and decision-trail visibility; nothing withheld from audit.
- **Constitutional check.** Marcus is the persona the gates were built for. There is no tension to resolve — serving Marcus *is* honoring P3/P8. The only failure mode is under-investing in security to move faster (a P8/P12 conflict where P8 wins).
- **Representative quote.** *"Show me the isolation model and the data flows. I'm not here to be impressed — I'm here to make sure this can't hurt us."*

---

## 6. P-5 — Alex, Candidate (Software Engineer) *(First-class user — equal depth)*

*Per DOC-05 P7 and DOC-03 KD-03.14, the Candidate is a first-class user, not a subject. We profile Alex at the same depth as the buyers — including the **selected** and, critically, the **rejected/afterlife** states.*

- **Identity.** Alex is a software engineer applying for roles — could be early-career or senior, from a linear or non-linear path, from a prestigious or unknown background. The person our entire mission exists to treat fairly (DOC-02).
- **Context (their world).** Applies through whatever channel exists (portal, email, referral) — and must not have to change that (DOC-01, P11). Evaluation-fatigued: multi-round loops, unpaid take-homes, repeated re-explanation, and the "black hole" of silence (DOC-02 P-C3/P-C4). Increasingly aware that AI may be judging them, and wary of it.
- **Goals.** Get a *fair shot* to show what they can actually do; not waste days on opaque processes; understand where they stand; be treated with dignity whether selected or not.
- **How they're measured (by the world).** Offers received — a brutal, binary, opaque signal today.
- **Pains (DOC-02).** Judged on an artifact, not ability (P-C1); systemic bias in screening (P-C2); enormous uncompensated process burden (P-C3); opaque rejection with no feedback or recourse (P-C4); the incentive to inflate because the artifact rewards it (P-C5).
- **Fears (DOC-06 A6).** *"Will a machine judge me unfairly, with no recourse?"* · *"Will I be reduced to a number?"* · *"Will my non-traditional background count against me?"* · *"Is this a waste of my time?"*
- **What earns their trust.** Being evaluated on *what they can do*; fairness they can *feel* (DOC-06 §3.7); honest disclosure that AI is involved (Honest by Default, DOC-06 A1); respect, especially in rejection (DOC-06 §3.3); getting something *useful* back (P13 candidate view). Trust here is fragile and mission-critical.
- **Emotional journey (DOC-06 A3) — including the rejection path.** `Curiosity → Hope → Nervousness → Focus → Reflection → [outcome] → Acceptance → Growth.` The product must make hope *warranted*, resolve nerves into focus, make the experience feel like being *understood*, and — even in rejection — land as fair, leaving genuine motivation.
- **The relief moment (DOC-06 A2).** *"Finally — someone evaluated what I can actually do."*
- **Two outcome states, both first-class:**
  - **Selected/advancing Alex** feels *seen and fairly assessed*; the process respected their time and ability; they enter the company already trusting how it hires.
  - **Rejected Alex (the majority — the Candidate Afterlife, DOC-03 §18.4).** Must **not** hit a black hole. Receives strengths, evidence-based observations, constructive improvement areas, and a learning direction (P13 candidate view) — framed as *"not the strongest match for this role,"* never *"not good enough"* (DOC-06 §10). Becomes a **network participant**: a Silver Medal Candidate, a Talent Pool member, a future applicant, a referral source, an advocate. Emotional target: `Disappointment → Understanding → Motivation`, not resentment.
- **Trust-Ladder position.** Alex's trust is earned per-interaction and is the most fragile: one humiliating or opaque experience destroys it (and, via reputation, the Data/Trust flywheels). Rung 1 for Alex is *"this felt fair and respectful."*
- **Relationship to the product.** Experiences the Sensors (interview/assessment) and, crucially, the *explanation* and *feedback*. Never sees internal thresholds, Calibration, Benchmark formulas, anti-fraud/Integrity mechanics, or weighting logic (P13 candidate view — protects fairness *and* IP).
- **Role in the buying decision.** **Not the buyer** — but the product's legitimacy and the mission depend on Alex. A great buyer experience built on a candidate-hostile foundation is a betrayal (C11) and a brand/regulatory time bomb.
- **What they must NEVER feel.** Processed by a machine; humiliated; ghosted; tricked (dark patterns); reduced to a number; that their background was held against them; that AI was hidden from them.
- **Progressive-Explainability view (P13).** Strengths, evidence-based observations, constructive improvement areas, learning roadmap. Never: internal thresholds, Company Calibration, Benchmark formulas, anti-fraud/Integrity mechanisms, weighting logic.
- **Constitutional check.** Alex is where the gates matter most: Fairness (P1), Progressive Explainability (P13), Human Accountability for high-risk decisions (P2), Privacy/consent and no-data-sale (P3/KD-03.14), and dignity (P7) all converge on this persona. There is a permanent tension between candidate transparency (P7) and IP protection (P6) — resolved by the P13 candidate view. Alex is the reason we exist and the reason the gates are absolute.
- **Representative quote.** *"I don't mind being evaluated. I mind being *dismissed* — by a keyword filter or a black box — before anyone ever looks at what I can actually build."*

---

## 7. Anti-Personas — who we deliberately do NOT optimize for

*Naming who we turn away is as important as naming who we serve (DOC-07 §4, §12, §14). These are real buyer/user types in the market whose core desire conflicts with our Constitution or Philosophy. We do not build for them; we decline or redirect. For each: who they are · what they want · why we refuse · which principle they'd violate · how we respond.*

### AP-1 — The Volume-at-Any-Cost Buyer
- **Who / want.** Wants to process enormous applicant volume as cheaply and fast as possible; indifferent to evidence quality or fairness. "Just filter the pile."
- **Why we refuse.** Optimizes throughput, not decision quality (violates C1/P9); pushes toward crude filtering that re-creates biased screening (P1). We are not an efficiency-at-all-costs tool (Non-Goal, DOC-05 A-05.2 §A4).
- **Violates.** P9/C1 (decision quality), P1 (fairness).
- **Response.** Decline or redirect: we improve *quality* of decisions; if throughput is all they want, a keyword filter is cheaper and we are the wrong vendor.

### AP-2 — The Pedigree-First Screener
- **Who / want.** Wants to rank and filter by school, employer brand, and credentials. "Show me the Stanford/FAANG resumes first."
- **Why we refuse.** This is precisely the artifact-first bias we exist to destroy (C2, §9, DOC-02 P-C1/P-C2). Serving it would betray the founding thesis.
- **Violates.** C2 (evidence over artifacts), P1 (fairness).
- **Response.** Hard decline of the *bias*; we serve the underlying need (find great engineers) with *evidence of ability*, and make pedigree-shortcutting deliberately inconvenient (§9).

### AP-3 — The Auto-Reject Seeker
- **Who / want.** Wants full automation of rejections at scale with no human — "let the AI reject the bottom 90% and don't bother me."
- **Why we refuse.** Violates Human Accountability (P2); "human click theater" and ungoverned high-risk automation are forbidden (DOC-05 A-05.2 §A1).
- **Violates.** P2 (human accountability).
- **Response.** Refuse gates (§12, no negotiation on the gate); offer the *governed* alternative — risk-proportional automation for genuinely low-risk, policy-defined, fairness-intact cases, with human accountability for the policy and high-risk decisions.

### AP-4 — The Black-Box Buyer
- **Who / want.** Wants a single magic score to sort candidates; doesn't care how or why. "Just give me the number."
- **Why we refuse.** Violates Explainability (P1) and evidence-first (DOC-06 §5); a bare "Score" is forbidden (DOC-04 A-04.A5). A black box is disqualified by design (DOC-07 §4).
- **Violates.** P1 (explainability), C9.
- **Response.** Decline the black box; deliver Evidence → Explanation → Recommendation → Evaluation Score with Confidence. If they truly want opacity, we are the wrong vendor.

### AP-5 — The Data-Monetization Partner
- **Who / want.** Wants to buy candidate data, or partner to resell/broker it. "You must be sitting on a goldmine of candidate data."
- **Why we refuse.** Candidate data is never sold (P3/P7/KD-03.14); candidates are users, not inventory (C11).
- **Violates.** P3 (privacy), P7 (candidate dignity).
- **Response.** Hard decline, no negotiation. This is a foundational refusal (DOC-07 §14).

### AP-6 — The AI-Gimmick Buyer
- **Who / want.** Wants visible "AI magic" for marketing/board optics — "make it look cutting-edge, put the AI front and center."
- **Why we refuse.** Violates Invisible-but-honest-AI (DOC-06 §7) and sensors-not-product / product-should-disappear (P6/C8). AI hype commoditizes us and erodes trust.
- **Violates.** P6, C8; DOC-06 §11 (AI hype anti-pattern).
- **Response.** Redirect: we sell hiring-decision quality, not AI theater. The intelligence is felt in the outcome, honestly disclosed, never performed.

> **The unifying rule:** an anti-persona is defined by a *want that requires breaking a gate or a core belief.* We serve their legitimate *need* only if we can do so without the violation; otherwise we decline, and we explain why (§12 "refuse gates, negotiate the rest"). Turning these away is not lost business — it is the moat protecting itself.

---

## 8. How the personas relate

- **The buying committee (KD-03.11).** *Rina champions → Sofia funds → Marcus clears → David validates quality.* A stall at any node stalls the deal; each has effective veto in their domain (Marcus and Sofia most sharply). Our messaging must speak to all four *simultaneously and consistently* (Rina: relief & defensibility; David: depth & his bar; Sofia: fairness & control; Marcus: isolation & boundaries).
- **The usage web.** Rina lives in it daily; David dips in for finalists (high-risk, human-accountable review — P2); Sofia consumes aggregates; Marcus governs data; Alex experiences the sensors and the explanation. The *same* underlying Evaluation is rendered five different ways (Progressive Explainability, P13) — one intelligence, audience-appropriate surfaces.
- **The alignment insight.** The personas' interests *converge* on our gates: Sofia needs fairness/defensibility, Marcus needs isolation, David needs evidence-depth, Alex needs dignity, Rina needs explainable shortlists. **Our non-negotiables are not a tax on the personas — they are the thing every persona actually wants.** That convergence is the deepest validation of the Constitution.
- **The tension we manage forever.** Recruiter/HM desire for *speed and convenience* vs. the *evidence/fairness/human-accountability* the mission demands. We resolve it every time via decision-quality-first (C1/P9) and the Customization Pyramid (serve the want in the flexible layers; never in the immutable base).

---

## Amendment A-08.2 — Relationship Map, Success Metrics, Lifecycle States

*Dated 2026-07-21. CTO-ratified. Adds three sections that make DOC-08 structurally complete: how personas relate (multi-dimensionally), how each measures success (and how we keep that aligned to the Constitution/Manifesto), and how the Candidate progresses as **one persona across lifecycle states** rather than many personas. Uses frozen DOC-04 vocabulary; new lifecycle labels are mapped to existing terms, and any genuinely new term is flagged for a DOC-04 amendment.*

### A1 — Persona Relationship Map

§8 sketched the buying committee; this maps the full web across five relationship dimensions the CTO named — **influence · approve · use · pay · receive value.**

**Per-persona relationship profile:**

| Persona | Influences… | Approves… | Uses… | Pays? | Receives value… |
|---|---|---|---|---|---|
| **Rina (TA)** | David (shortlist credibility), Sofia (business case) | — (champions, doesn't approve budget) | The product **daily** (full recommendations) | No — advocates for spend | Defensible shortlists, time back, credibility, *relief* |
| **David (VP Eng)** | Rina (defines the real bar), Sofia (quality narrative) | **Quality/fit** (validates the evaluations are real) | Finalist review — high-risk, human-accountable (P2) | No | Trustworthy candidates, less re-screening, calibrated pipeline |
| **Sofia (CHRO)** | Board & org (talent narrative) | **Budget** (economic approval) | Aggregate dashboards | **Yes — owns the budget** | Fair, defensible, measurable hiring; reduced legal/brand risk |
| **Marcus (IT/Sec)** | Sofia (risk sign-off), procurement | **Security/data** (technical approval — **veto**) | Governance/audit view | No — part of approval | Verified data safety, clean boundaries, no migration trap |
| **Alex (Candidate)** | Employer brand & referrals (word of mouth) | — (not an approver) | Sensors + explanation/feedback | **No — never pays** (KD-03.14) | Fair evaluation, dignity, useful feedback, portable evidence |

**Directed influence & value flow** (who moves whom, and where value circulates):

```
  Sofia (pays) ──approves budget──▶ [PLATFORM]
     ▲                                  │
  Rina (champions) ──makes business case┘
     │  ▲                               │ delivers evidence-based decisions to
  David (validates quality) ────────────┤ Rina · David · Sofia · Marcus
     │                                  │
  Marcus (clears security) ─veto power──┘
                                        │ delivers fair evaluation + dignity + feedback to
                                        ▼
                                     Alex (candidate)
                                        │ great/fair experience →
                                        ▼
                    employer brand ↑ · referrals ↑ · network ↑ (Data/Trust flywheels, DOC-03)
                                        │
                                        └──▶ attracts more candidates + proves value to future buyers
```

- **The insight the map encodes:** value is *paid* by the Company (via Sofia) but *created* at the point where Alex is fairly evaluated — and Alex's experience loops back as brand, referrals, and network growth (the flywheels). **A candidate-hostile product breaks the loop even if every buyer is delighted** (C11). The map is a standing argument for treating the non-paying candidate as first-class (P7).
- **Veto topology:** Marcus and Sofia hold hard vetoes (security, budget); David holds a quality veto (kills adoption if evaluations are shallow); Rina holds momentum (no champion, no motion). GTM must clear all four *and* honor Alex.

### A2 — Persona Success Metrics *(and how we keep them aligned)*

Each persona measures success their own way — and some of those metrics are *misaligned* with our mission (e.g., raw time-to-fill, raw offer count). This section makes the misalignment explicit and states how we reconcile it: **we serve each persona's underlying need through decision quality, and never optimize their vanity metric at the expense of a gate** (DOC-07 §6 objective function; C11).

| Persona | How **they** measure success | Naive-optimization risk | How **we** serve it (aligned metric) | Constitution / Manifesto alignment |
|---|---|---|---|---|
| **Rina** | Time-to-fill, pipeline volume, HM satisfaction | Chasing speed → crude filtering → bias/black-box | *Speed of a defensible, evidence-backed shortlist* | Speed via Decision Quality (C1/P9); never skip Fairness (P1); *relief* (A2) |
| **David** | Team output; quality-of-hire; less time re-screening | Over-trusting a shiny score | Predictive accuracy validated over Outcomes; calibration-fit | Judged over years (C10); Human Accountability (P2); his bar via the Customization Pyramid (§8.1) |
| **Sofia** | Cost, compliance, D&I, retention/QoH, board confidence | Cost-cutting that raises fairness risk | Fairness/adverse-impact posture + QoH uplift + defensibility | Fairness/Explainability gates (P1/P13); Exec *assurance* (A3) |
| **Marcus** | Zero incidents, audit pass, integration stability | Speed-to-deploy over security | Isolation, auditability, clean integration boundaries | Trust & Security first among rankables (P8); Privacy (P3); Audit-Ready (A3) |
| **Alex** | Offers received; a fair shot; a useful outcome | Optimizing "offers" would mean passing everyone — meaningless | Fairness *felt*, dignity, useful feedback **even in rejection** | Fairness (P1), Dignity (P7), Progressive Explainability (P13); Respect + Remove-Fear + Relief (DOC-06 §3.3/A6/A2) |

- **The alignment rule (critical):** where a persona's felt metric conflicts with our objective function (Rina's time-to-fill; Alex's offer count), **we deliver the *outcome they actually want* (a great, defensible hire; a fair shot) through decision quality — we do not adopt their proxy metric as our goal.** This is C11 ("serve each persona *through* the decision") made measurable, and it is the guardrail against becoming an efficiency/vanity tool (DOC-07 §4/§6).
- **Convergence, again:** every persona's *aligned* metric depends on the same gates (fairness, explainability, evidence, security, dignity) — reconfirming KD-08.4.

### A3 — Persona Lifecycle States (the Candidate as one persona over time)

Alex is **one persona in many states**, not many personas. This resolves §9.3 Q2: we do **not** fragment the candidate into sub-personas; we model lifecycle *states* of the single Alex persona. Each state maps to the frozen **Candidate Lifecycle** (DOC-04 §6.1) and carries an intended feeling (DOC-06 A3) and a product obligation.

| # | Lifecycle state | DOC-04 mapping | Intended feeling (A3) | What the product owes |
|---|---|---|---|---|
| 1 | **Potential Candidate** | Prospect | Curiosity | Honest signals of fairness; low-friction, no-behavior-change entry (P11) |
| 2 | **Applicant** | Applied (Application) | Hope → Nervousness | Clarity, calm; "apply as you always did" (P11) |
| 3 | **Evaluated** | In Evaluation → Evaluated | Focus | Fair-feeling Sensors; evidence-first; **honest AI disclosure** (A1) |
| 4 | **Shortlisted** | Recommended → In Decision | Cautious hope | Dignity; timely, respectful communication |
| 5a | **Offer** | Offer | Relief / validation | Smooth, respectful close |
| 5b | **Rejected** | Rejection → Candidate Afterlife | Disappointment → Understanding → Motivation | Constructive, evidence-based feedback + learning direction (P13 candidate view); *"not the strongest match for this role,"* never *"not good enough"* (DOC-06 §10); Silver Medal / Talent Pool placement |
| 6 | **Employee** | Employee *(reference-only, external HRIS)* | Belonging | Nothing from us directly; we *reference* the Employee for Outcome Learning (DOC-04 A-04.A4) |
| 7 | **Alumni** | *former Employee (reference-only)* — **see note** | Goodwill | Respectful relationship; eligibility for future re-engagement |
| 8 | **Future Candidate** | re-entry via Candidate Afterlife / Talent Pool / Silver Medal | Motivated return | Portable Evidence (with consent); warm, fast re-engagement — closes the network loop (DOC-03 §18.4) |

```
 Potential ─▶ Applicant ─▶ Evaluated ─▶ Shortlisted ─┬─▶ Offer ─▶ Employee ─▶ Alumni ─┐
   (Prospect)                                         │                                │
        ▲                                             └─▶ Rejected ─▶ (Afterlife:       │
        │                                                   Silver Medal / Talent Pool) │
        └───────────────────── Future Candidate ◀───────────────────────────────────────┘
                         (re-engagement — portable evidence, with consent)
```

- **Why states-not-personas matters.** It keeps our obligations to *the same human* continuous across their whole relationship with the network — the emotional-journey (A3) and Candidate-Afterlife (P7) commitments follow Alex through *every* state, including rejection and beyond. Fragmenting into sub-personas would let us quietly drop our duty to the rejected majority; a single-persona lifecycle forbids that.
- **Terminology note (freeze discipline).** "Potential Candidate" = **Prospect** and "Future Candidate" = re-entry, both already in DOC-04 §6.1. **"Alumni"** (a former Employee) is **not yet a formal DOC-04 term**; it behaves like Employee (reference-only, external HRIS). *Flagged for a minor DOC-04 amendment* if it becomes load-bearing (see §9.3). Until then it is a descriptive lifecycle-state label, not a new business term.

---

## Amendment A-08.3 — Persona Conflicts, Evolution, and Non-user Stakeholders

*Dated 2026-07-21. CTO-ratified. Personas were profiled independently; reality is that they conflict, they evolve, and some of the most influential people never touch the product. These three sections capture that dynamism.*

### A-1 — The Persona Conflict Matrix

Personas want different, often opposing things: the recruiter wants speed, the hiring manager wants quality, the candidate wants transparency, security wants restrictions, the CHRO wants compliance. **These conflicts are resolved by the Constitution's priority ladder and by evidence — never by organizational power or by whoever is loudest.** That single rule is what makes us trustworthy to the least powerful party in the room (the candidate).

| Conflict | Winner | Why (the resolving principle) |
|---|---|---|
| **Recruiter (speed) vs Candidate (fair, thorough evaluation)** | **Constitution — Fairness** | P1 gate; we serve the recruiter's *speed need* through decision quality, never by shortchanging fairness. |
| **Speed vs Trust** | **Trust** | DOC-05 P8 (trust first among rankables); DOC-07 §13. |
| **Security vs UX / convenience** | **Security** | Tier-0/Tier-2 (P3/P8); Marcus's veto embodies this. |
| **Hiring Manager (preference / gut) vs Candidate (fair evaluation)** | **Evidence — *not* hierarchy** | Decided by Evidence and decision quality (C1/P9), **never by seniority**. Rank does not win arguments here; evidence does. |
| **CHRO (compliance) vs Recruiter (speed)** | **Compliance / Fairness** | P1; a fast decision that isn't defensible is worthless (Sofia's accountability). |
| **Hiring Manager's idiosyncratic bar vs Fairness** | **Fairness gate** | The *bar* flexes (Customization Pyramid middle, DOC-07 §8.1); *bias* never does (P1). |
| **Candidate (full transparency) vs IP / moat protection** | **Progressive Explainability (P13)** | The balanced resolution: candidate gets constructive evidence-based feedback; internals stay protected. |
| **Buyer's customization demand vs Constitution** | **Constitution** | The immutable base of the Customization Pyramid; refuse gates (DOC-07 §12). |
| **Recruiter/HM (automation convenience) vs Human Accountability** | **Human Accountability (P2)** | Risk-proportional oversight; no click-theater (DOC-05 A-05.2 §A1). |

- **The meta-rule (the emblem of the whole company):** *"Manager vs Candidate → Evidence, not hierarchy."* We do not resolve conflicts by deferring to the most senior or most powerful persona; we defer to the Constitution and to evidence. This is precisely why a candidate can trust us and why a regulator can respect us — power does not bend the outcome. It is C11 ("serve the decision, and every persona *through* it") made enforceable.
- **How to use it.** When two personas' wants collide in a design or deal, name the conflict, find its row (or the governing principle), and apply the winner. Document the call. This prevents "the loudest stakeholder wins."

### A-2 — Persona Evolution

Personas are not fixed points; the *same human* moves through roles, and relationships deepen over time. We design for trajectories, not snapshots.

- **Within-role ascent (the buyer's career).**
  ```
  Recruiter → TA Director → VP Talent → CHRO
  ```
  The same person, over years, needs progressively more: from daily shortlist tooling (Rina) to aggregate fairness/ROI assurance (Sofia). *Today's champion is tomorrow's economic buyer.* The product and relationship must grow with them — a champion who outgrows the product becomes a detractor.
- **Cross-persona evolution (the candidate's arc — the powerful one).**
  ```
  Candidate (Alex) → Employee → Hiring Manager / interviewer → (elsewhere) Champion / Buyer
  ```
  **Today's candidate is tomorrow's hiring manager and, eventually, a buyer at another company.** How we treat Alex-the-candidate (dignity, fairness, useful feedback — even in rejection) directly shapes the buyers and champions of the next decade. This is the Candidate Afterlife (DOC-03 §18.4) as a *talent-and-demand* flywheel, and a hard commercial reason to honor P7.
- **Implications.**
  1. Design for a persona's *trajectory* — don't force re-learning as they grow (relates to First Five Minutes staying true at every level, DOC-06 A5).
  2. Relationship deepening mirrors land-and-expand (DOC-03) and the Trust Ladder ascent (DOC-06 A4).
  3. Reputation compounds across careers: every fairly-treated candidate is a future advocate, hire, referrer, or buyer.

### A-3 — Non-user Stakeholders

Some of the most decisive people **never touch the product** yet can accelerate or kill a deal. They are **stakeholders, not personas** (no usage, no user experience to design) — but GTM, pricing, and trust posture must account for them.

| Stakeholder | Core concern | Influence on the deal | How we address them |
|---|---|---|---|
| **CEO** | Strategic fit; the talent narrative; downside/brand risk | Can sponsor or veto strategically | Vision + risk reduction; "hiring is fair, defensible, under control" (a story Sofia can carry up). |
| **Procurement** | Price, terms, vendor risk, security paperwork | Gate on contracting; can stall for months | Predictable pricing (KD-03.10), SOC 2, standard terms, clean vendor-risk answers (supports Marcus). |
| **Finance** | ROI, budget predictability, cost control | Approves/blocks spend with Sofia | Predictable **per-Candidate-Evaluation** pricing (KD-03.10) + ROI story (quality-of-hire uplift, reduced bad-hire cost — DOC-02 §6). |
| **Board** | Risk, reputation, growth | Shapes exec priorities; sensitive to hiring-AI headlines | Fairness/defensibility posture; we *reduce* the board's risk, not add to it. |
| **Regulators** | Fairness, explainability, auditability | External; can reshape what's permissible (LL144, EU AI Act) | The gates *are* the answer (P1/P13); engage early; convert regulation into moat (DOC-03 §24, Trust flywheel). |

- **Why this section exists.** A perfect buying committee (Rina/David/Sofia/Marcus) can still be blocked by Procurement, starved by Finance, spooked by the Board, or constrained by a Regulator. These stakeholders sit *around and above* the committee (§8). Our strategy already addresses them structurally — predictable pricing (Finance/Procurement), security-first (Procurement/Marcus), and the fairness gates (Regulators/Board) — which is why we surface them explicitly rather than discover them in a stalled deal.

---

## 9. Summary

### 9.1 What this establishes
- Five deep, decision-context personas — **Rina** (recruiter/champion), **David** (VP Eng/quality authority), **Sofia** (CHRO/economic), **Marcus** (IT-Security/veto), **Alex** (candidate/first-class user) — each with goals, pains, fears, trust conditions, emotional journey, relief moment, buying role, Progressive-Explainability view, and a Constitutional check.
- Six **anti-personas** we deliberately refuse, each mapped to the gate/belief they'd violate and how we respond.
- The **buying committee** and **usage web**, and the key insight that persona interests *converge* on our gates.

### 9.2 Key decisions recorded
- **KD-08.1** — The **core five personas** are canonical; product and GTM decisions are tested against them.
- **KD-08.2** — The **Candidate (Alex) is profiled at equal depth to buyers**, with first-class treatment of the **rejected/afterlife** state (P7, KD-03.14).
- **KD-08.3** — **Six anti-personas** are explicit; requests defined by them are declined-or-redirected per DOC-07 §12 ("refuse gates, negotiate the rest").
- **KD-08.4** — Persona interests **converge on the Constitution's gates**, confirming the non-negotiables are what every persona actually wants — not a constraint on serving them.
- **KD-08.5** — The **buying committee map** (Rina champion / Sofia economic / Marcus technical-veto / David quality) governs GTM messaging (KD-03.11 operationalized).
- **KD-08.6** — The **Persona Relationship Map** (A-08.2 §A1) models influence/approve/use/pay/value; value is *paid* by the Company but *created* at Alex's fair evaluation, looping back as brand/referrals/network (the flywheels).
- **KD-08.7** — **Persona Success Metrics** are aligned via one rule (A-08.2 §A2): we deliver each persona's desired *outcome* through decision quality; we never adopt their vanity proxy (time-to-fill, offer count) as our goal or optimize it at a gate's expense.
- **KD-08.8** — The **Candidate is one persona across lifecycle states** (A-08.2 §A3), not sub-personas; our obligations (emotional journey, dignity, afterlife) follow the same human through every state incl. rejection. *(Resolves §9.3 Q2.)*
- **KD-08.9** — **Persona conflicts are resolved by the Constitution and by evidence — never by organizational power** (A-08.3 §A-1). Emblem: *"Manager vs Candidate → Evidence, not hierarchy."*
- **KD-08.10** — **Personas evolve** (A-08.3 §A-2): the same human ascends (Recruiter→CHRO) and crosses personas (Candidate→Employee→Hiring Manager→Buyer). Today's candidate is tomorrow's buyer — a commercial reason to honor P7.
- **KD-08.11** — **Non-user stakeholders** (CEO, Procurement, Finance, Board, Regulators) can accelerate or kill deals without touching the product (A-08.3 §A-3); our pricing/security/fairness posture is structurally built to satisfy them.

### 9.3 Open questions (for founder/CTO)
1. **Secondary personas:** do interview *panelists* (ICs pulled into interviews) and **Legal/Compliance** warrant their own lighter profiles later, or are they covered by David (panelists) and Sofia/Marcus (compliance)? *(Recommend: cover now via those personas; add if a real gap appears.)*
2. ~~**Candidate segmentation**~~ → **Resolved (A-08.2 §A3):** the Candidate is **one persona across lifecycle states**, not sub-personas. (Situational variants like active/passive or junior/senior, if ever needed, are *journey* nuances for DOC-10, not new personas.)
3. **Agency/RPO persona:** deferred (post-beachhead, DOC-01) — confirm we exclude it from V1 personas.
4. **Champion resilience:** if Rina (champion) leaves the customer, what persona sustains the relationship? A GTM/CS question worth flagging for later.
5. **"Alumni" term (freeze discipline):** A-08.2 §A3 introduces "Alumni" (former Employee) as a lifecycle-state label. Should it be formally added to DOC-04 as a reference-only term (like Employee), or remain descriptive? *(Recommend: add to DOC-04 via minor amendment only if/when re-engagement of alumni becomes a real product surface; descriptive for now.)*

### 9.4 Suggested next document
**DOC-09 — Jobs-To-Be-Done.** With *who* the users are now fixed, DOC-09 defines *why they "hire" our product* — their functional, emotional, and social jobs — turning these personas into the demand-side logic that drives functional requirements (DOC-12). Keeping JTBD separate (per the roadmap) lets it be a sharp, framework-driven deep-dive rather than a footnote to personas.

**Roadmap position (revised — Service Blueprint inserted at 10, per CTO):** 01 Vision · 02 Problem · 03 Strategy · 04 Domain · 05 Constitution · 06 Manifesto · 07 Philosophy · **08 Personas** · → **09 JTBD** · **10 Service Blueprint** *(NEW — back-stage: what happens behind the scenes)* · **11 Customer Journey** *(front-stage: what the customer sees)* · 12 Functional Requirements · 13 NFRs · 14 AI Strategy · 15 Evaluation Engine · 16 Architecture · 17 Engineering Principles.
> *Why Service Blueprint before/with Customer Journey:* the Customer Journey shows **what the customer sees**; the Service Blueprint shows **what happens behind the scenes** (e.g., candidate applies → front-stage "application submitted"; back-stage ATS sync, evidence pipeline, evaluation queue, compliance logging, memory updates, audit trail). That front-stage/back-stage bridge makes the later architecture (DOC-16) far cleaner.

---

*End of DOC-08 v0.1. Awaiting founder review of the four open questions (§9.3) before promotion to Ratified.*
