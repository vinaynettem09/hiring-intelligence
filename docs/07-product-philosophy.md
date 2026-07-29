# Document 07 — Product Philosophy (The Product Bible)

| Field | Value |
|---|---|
| **Document ID** | DOC-07 |
| **Title** | Product Philosophy (The Product Bible) |
| **Owner** | CTO / Principal Engineer / Technical Documentation Lead |
| **Status** | v0.3 — §8.1 Customization Pyramid + **Amendment A-07.2: Complexity Budget, Product Deletion Philosophy, Innovation Philosophy** |
| **Created** | 2026-07-21 |
| **Depends on** | DOC-01 (Vision + A-0.2), DOC-02 (Problem), DOC-03 (Strategy + KDs), DOC-04 (frozen vocabulary), DOC-05 (Constitution), DOC-06 (Manifesto) |
| **Blocks** | DOC-08 (Personas), DOC-09 (JTBD), and **every roadmap and prioritization discussion, indefinitely** |
| **Nature** | **The product DNA.** The most slowly-changing document we own. Where the Constitution governs *decisions* and the Manifesto governs *feelings*, this governs **beliefs about product** — what "good," "quality," and "worth building" mean to us. |
| **Half-life** | Deliberately long. Technology changes yearly; this should change over *years*. If we edit it often, we are getting it wrong. |
| **Vocabulary** | Uses DOC-04 frozen terms exactly. Introduces **no** new business terms. |
| **Scope discipline** | **Does NOT answer "what features should we build?"** It answers what a good product *is*, what quality *means*, what we *optimize*, what we *refuse*, when we say *no*, and the *trade-offs that define us*. Implementation, features, and architecture are downstream and out of scope. |

---

## How to read this — the three governing documents, and why this one changes least

Three documents govern all product work, in a deliberate division of labor:

| Document | Governs | The question it answers | Change frequency |
|---|---|---|---|
| **DOC-05 Constitution** | Decisions | *What must always be true? Who wins a conflict?* | Rare (gates ≈ immutable) |
| **DOC-06 Manifesto** | Feelings | *How should every user feel?* | Rare |
| **DOC-07 Philosophy** (this) | **Beliefs about product** | *What is a good product? What is quality? What do we build and refuse?* | **Rarest — the product DNA** |

> **Why the product bible outlives the architecture.** Architecture is an answer to *today's* technology; it will be rewritten many times. Product philosophy is an answer to *what we value*; it should hold for a decade. That is why the CTO instructed us to invest more here than in architecture: a wrong architecture costs a rewrite; a wrong or absent product philosophy costs a decade of incoherent roadmaps, feature-bloat, and mission drift. This document is the constant against which every future "should we build X?" is measured.

**How to use it in practice.** When someone proposes a feature, a roadmap, a customer accommodation, or a "quick win," hold it against this document: *Is this what we mean by a good product? Does it raise or lower quality as we define it? Does it optimize what we optimize? Would we refuse it? Does saying yes require breaking a trade-off we've already chosen?* If the proposal loses against the bible, the proposal is wrong — not the bible (unless the bible is formally amended via DOC-05's Lifecycle process).

---

## 1. Purpose

To define, permanently and explicitly, **what we believe a product is for and what makes one good** — so that thousands of future decisions, made by people who never met the founders, remain coherent with the company we intend to build.

This document does three things and refuses a fourth:
1. It states our **convictions** about product (§2) and turns them into operational definitions of **good** (§3), **bad** (§4), and **quality** (§5).
2. It declares what we **optimize** (§6) and the **stances and trade-offs** that follow (§7–§13).
3. It draws the hard line of what we **refuse to build** (§14) and **when we say no to customers** (§12).
4. It **refuses to specify features or architecture** — those are downstream, and a philosophy that reaches into them dates itself and constrains the wrong layer.

---

## 2. Core Product Convictions

The foundational beliefs. Everything else in this document is derived from these. Each is a *belief*, stated plainly, with why we hold it and the belief it replaces.

- **C1 — The product is the quality of the decision, not the software.** We believe we are not shipping an app; we are shipping better, fairer, more defensible Hiring Decisions. *Why:* it is the mission (DOC-01) and the moat (DOC-03). *Replaces:* "the product is the features/UI."

- **C2 — Evidence beats artifacts.** We believe observed ability is worth more than claimed credentials, always. *Why:* the founding thesis (DOC-02). *Replaces:* "the resume is the starting point."

- **C3 — A good product is one you trust, not one that dazzles.** We believe trust is the highest product value; dazzle is a liability. *Why:* trust is the moat and the emotion we design for — *relief, not delight* (DOC-06 A2). *Replaces:* "great products delight."

- **C4 — Depth beats breadth.** We believe doing one thing with compounding depth beats doing ten things shallowly. *Why:* depth compounds into the moat; breadth commoditizes (DOC-03 §13, §18). *Replaces:* "a platform should do everything."

- **C5 — A product should have a point of view.** We believe the product should embody strong, evidence-based opinions about good hiring — offered as defaults, adaptable within guardrails. *Why:* a product with no opinion is a configurable black box that improves nothing (ratified: opinionated defaults, deep flexibility). *Replaces:* "the product should do whatever the customer configures."

- **C6 — Less is more; subtraction is a feature.** We believe the best product is the smallest one that fully serves the decision. Every feature is a permanent cost. *Why:* cognitive load is the enemy of good decisions (DOC-06 §8); complexity is a debt users pay. *Replaces:* "more features = more value."

- **C7 — The human is the hero; the product is the instrument.** We believe we make humans better and more accountable decision-makers — never replace or de-skill them. *Why:* Human Accountability (P2); trust; augmentation over automation. *Replaces:* "AI should do the job."

- **C8 — The product should disappear.** We believe the best infrastructure is felt, not seen; the user should think about the decision, not the tool or the AI. *Why:* invisible-not-hidden (DOC-06 §7); infrastructure, not a demo. *Replaces:* "show off the technology."

- **C9 — Correctness includes fairness.** We believe an unfair result is a *wrong* result, not merely an unethical one. *Why:* in hiring, fairness is constitutive of correctness (DOC-01 §9, DOC-02). *Replaces:* "accuracy first, fairness later."

- **C10 — A product is judged over years, not demos.** We believe the real measure is whether decisions proved right over time (Outcome Learning), not how impressive a demo looked. *Why:* the Learning flywheel (DOC-03 §17); quality-of-hire is the ultimate metric. *Replaces:* "win the demo."

- **C11 — We serve the decision, and every stakeholder through it.** We believe the recruiter, hiring manager, executive, admin, and candidate are all served *by making the decision better* — not by pleasing any one of them at the decision's expense. *Why:* decision quality is the product (P9); recruiters are one customer (DOC-03). *Replaces:* "the user (recruiter) is the customer to please."

- **C12 — Trust compounds and must never be spent for growth.** We believe trust is capital that accrues slowly and can be destroyed instantly; we never trade it for a short-term metric. *Why:* the Trust flywheel; a single scandal is existential (DOC-03 §24). *Replaces:* "growth first."

---

## 3. What Is a GOOD Product (our positive definition)

For us, a product is **good** to the exact degree that it does the following. This is our rubric — not the industry's.

A good product:
1. **Measurably improves the Hiring Decision** — more evidence-backed, more predictive of good Outcomes (C1, C10).
2. **Is trusted** by the people who rely on it — it produces *relief*, and it climbs the Trust Ladder (DOC-06 A2/A4).
3. **Is explainable** to everyone entitled to understand it, at the right depth (Progressive Explainability, P13).
4. **Is fair, and feels fair** — the same evidence-based rules for everyone (C9, P1).
5. **Is calm and low-load** — it makes the next right action obvious; it reduces fear (DOC-06 §8, A6).
6. **Compounds** — every use makes it better (Evidence Graph, Hiring Memory, Outcome Learning); it deepens the moat (C4).
7. **Is defensible** — a decision it supports can be stood behind before a candidate, a hiring manager, and a regulator.
8. **Disappears** — the user thinks about the decision, not the tool or the AI (C8).
9. **Respects everyone it touches** — most of all the rejected (P7, DOC-06 §3.3).
10. **Does less, deeply** — it earns its surface area; nothing is decoration (C6).

> **The one-line test of a good product:** *"Did this make the hiring decision better, fairer, and more trusted — and would we be proud to defend it?"* If yes across the rubric, it is good. If it merely shipped, demoed well, or pleased a user without improving the decision, it is not.

---

## 4. What Is a BAD Product (the anti-definition)

Naming "bad" explicitly is as important as naming "good," because most industry defaults are things we consider bad. A product is **bad** — for us — when it:

1. **Optimizes vanity or engagement** — time-on-app, clicks, interview volume — rather than decision quality.
2. **Is a black box** — produces outputs no one can explain (violates C9/P1). *A more accurate black box is still a bad product.*
3. **Dazzles without helping** — impressive, "smart-looking," AI-flaunting, but doesn't improve the decision (violates C3/C8).
4. **Is broad and shallow** — many features, none deep; a mile wide and an inch of moat (violates C4).
5. **Adds anxiety** — overwhelms, confuses, or increases fear (violates DOC-06 §8/A6).
6. **Lets you configure away fairness** — flexibility that can disable the gates (violates C5's guardrails, P1).
7. **Is feature-bloated** — accretes options because customers asked, until it serves no decision well (violates C6).
8. **Is demo-driven** — built to win a sales demo rather than to be right over years (violates C10).
9. **Extracts from candidates** — treats them as inventory/data to monetize (violates C11/P7).
10. **Is fast but untrustworthy** — ships speed at the cost of trust (violates C12).

> **The one-line test of a bad product:** *"Did this optimize something other than the decision — engagement, dazzle, breadth, speed, or extraction — at the expense of trust or quality?"* If yes, it is bad, no matter how well it sells or demos.

---

## 5. What "Quality" Means to Us

The industry conflates quality with **features and speed**. We reject that. For us, **quality is multi-dimensional, and trust dominates.** A product cannot be high-quality if it is untrusted, however feature-rich or fast.

| Dimension of quality | What it means | How we know it's high |
|---|---|---|
| **Decision Quality** *(the apex)* | The Hiring Decisions we support are better — evidence-backed, fair, predictive. | Evidence-backed-decision rate ↑; quality-of-hire uplift over time. |
| **Evidence Quality** | The Evidence is high-signal, verified, role-relevant, and sufficient. | Strong Signals, high Integrity Scores, appropriate Confidence. |
| **Explanation Quality** | Explanations are honest, audience-appropriate, and actually understood. | Users can restate *why*; candidates find feedback useful; audit is complete. |
| **Experience Quality** | Calm, low-load, relief-producing, fear-reducing (DOC-06). | Time-to-first-relief ↓; fear signals ↓; trust rungs climbed. |
| **Trust Quality** | Consistency, fairness track record, absence of manipulation. | No trust incidents; fairness audits pass; NRR/embeddedness ↑. |
| **Outcome Quality** | Recommendations prove correct over time. | Predictions track real Outcomes (Learning flywheel). |

- **The rule of dominance:** a product that scores high on features/speed but low on Trust or Decision Quality is, by our definition, **low quality.** We would rather ship a smaller thing that is high across these dimensions than a larger thing that is high only on features.
- **Quality is not a QA gate at the end.** It is these six dimensions, designed in from the first sketch. A defect in Trust Quality is a worse bug than a crash.

---

## 6. What We Optimize For (the objective function)

A company's real values are revealed by what it optimizes. Ours, explicitly:

**We optimize for:**
1. **Evidence-backed decisions** (the North Star, DOC-01 D-01.4).
2. **Trust** (the moat, C12) — measured by reliance and the Trust Ladder.
3. **Quality-of-hire uplift over time** (the ultimate validation, DOC-02).
4. **Compounding** — depth of Evidence Graph, Hiring Memory, Outcome Learning (C4, DOC-03 §13).

**We explicitly do NOT optimize for:**
1. **Engagement / time-on-app** (that is a consumer-attention goal; ours is the opposite — get the user to a confident decision and out).
2. **Interview or evaluation *volume* for its own sake** (a sensor metric; C7/P6).
3. **Recruiter speed *alone*** (efficiency ≠ our product; Non-Goal, DOC-05 A-05.2 §A4).
4. **Feature count** (C6).
5. **Demo impressiveness** (C10).
6. **Short-term revenue at the cost of trust** (C12).

> **The objective-function test:** for any proposed metric or goal, ask *"is this on the optimize list, or the do-not list?"* Teams that optimize the wrong number produce the wrong product, however competent the execution. This list is the tie-breaker for goal-setting.

---

## 7. Defining Stance: Depth over Breadth

- **The belief (C4).** We go *deep* on the intelligence layer before we go *broad* across features, roles, or segments. One thing, compounding, beats ten things, shallow.
- **Why.** Depth is where the moat lives (Hiring Memory, Outcome Learning compound with depth, not breadth — DOC-03 §13). Breadth is where commoditization lives — a broad, shallow product is exactly what a platform giant can clone (DOC-03 §24). Depth also serves quality: a deep capability can be made trustworthy and explainable; a broad-shallow one rarely can.
- **What it enables.** Saying "not yet" to adjacent features/roles/segments to perfect the core; investing in unglamorous depth (outcome pipelines) over shiny breadth.
- **What it rejects.** "Let's add module X to close this deal"; roadmap-by-feature-request; becoming a suite.
- **Trade-off accepted.** Slower apparent surface-area growth; we will lose some deals to broader competitors in the short term — and win the category in the long term.
- **The belief we reject.** "A platform must do everything." No — a *platform* earns breadth by first being irreplaceable at depth.

---

## 8. Defining Stance: Opinionated Defaults, Deep Flexibility *(ratified)*

- **The belief (C5).** The product embodies **strong, evidence-based opinions about good hiring**, delivered as **defaults** — but customers can **adapt within guardrails.** *"Strong opinions, loosely held — except the gates, which are held absolutely."*
- **The precise boundary — what flexes vs. what never does:**

  | Flexes (deep flexibility) | Never flexes (the guardrails) |
  |---|---|
  | The **bar**: how high, what a Role prioritizes (via Company Calibration) | **Fairness** (P1) — cannot be configured off |
  | The **context**: company values, role-specific weightings, Hiring Memory | **Explainability / Progressive Explainability** (P1/P13) |
  | Which **sensors** are used, workflow integration | **Human Accountability** for high-risk decisions (P2) |
  | Depth of evaluation, thresholds within policy | **Evidence-first order** (DOC-06 §5) |
  | Surfacing, reporting, terminology-in-UI (within DOC-04) | **Privacy / candidate dignity** (P3/P7) |

### 8.1 The Customization Pyramid *(the one-diagram mental model)*

This is the single picture that explains to every employee, salesperson, product manager, and customer **what can change and what never will.** Read it bottom-up: the higher the layer, the more it flexes; the base is load-bearing and immutable, and nothing above may ever be customized in a way that undermines it.

```
                     ┌───────────────────────────────┐
                     │      CUSTOMER PREFERENCES       │   ▲ most flexible
                     │      branding · notifications   │   │ customer-owned
                 ┌───┴───────────────────────────────┬─┴───┐
                 │        WORKFLOW & CONFIGURATION      │     │ flexible within
                 │  calibration · reports · integrations│     │ guardrails
             ┌───┴─────────────────────────────────────┴─────┴───┐
             │        EVIDENCE-BASED PRODUCT DEFAULTS              │   we set the
             │     recommended behavior · evaluation logic         │   default; you
             │     (opinionated; adaptable within guardrails)      │   may adapt it
         ┌───┴─────────────────────────────────────────────────────┴───┐
         │              CONSTITUTION  (IMMUTABLE)                        │   ▼ never flexes,
         │   Fairness · Explainability · Privacy ·                       │     for anyone,
         │   Human Accountability · Neutrality                           │     ever
         └───────────────────────────────────────────────────────────────┘
```

| Layer | What it governs | Who controls it | How mutable | Examples |
|---|---|---|---|---|
| **Customer Preferences** | Cosmetic and communication choices | The customer, freely | Fully flexible | Branding, notification settings, display options |
| **Workflow & Configuration** | How the product fits the customer's process | The customer, within guardrails | Flexible, bounded | Company Calibration (their bar), report configuration, ATS/email integrations |
| **Evidence-Based Product Defaults** | How the product behaves and evaluates by default | **We** set it (opinionated); customers may adapt | Adaptable, not arbitrary | Recommended evaluation behavior, default evaluation logic, evidence-first flows |
| **Constitution (Immutable)** | The non-negotiable foundation | **No one** — not us, not the customer | **Never** | Fairness (P1), Explainability/Progressive Explainability (P1/P13), Privacy (P3), Human Accountability (P2), Neutrality (P5) |

- **How to use it.** For any request or configuration ask: *"Which layer does this touch?"* Top two layers → generally yes (that's the "deep flexibility"). Third layer → yes, but you are adapting *our opinion*, so we guide toward the evidence-based default. Base layer → **no, never** (this is the hard "refuse gates" of §12).
- **Why this diagram is load-bearing.** It reconciles two things that sound contradictory — *"highly customizable"* and *"strongly principled"* — into one intuitive model. It tells a salesperson what they can promise, a PM what they can build, and a customer what they can expect, without anyone re-reading the whole Constitution. It is the visual grammar of "opinionated defaults, deep flexibility."
- **The rule the pyramid encodes:** *you can restyle the top, reshape the middle, and adapt our defaults — but you can never dig into the foundation.* Flexibility increases as you climb; immutability is absolute at the base.

- **Why this middle.** Pure opinionation (no flexibility) fails enterprise reality and our own Company Calibration concept — every company's bar differs. Pure flexibility (no opinion) makes us the configurable black box we exist to replace (§4.6). Opinionated defaults with bounded flexibility is the only stance consistent with *both* "decision quality is the product" *and* "Company Calibration adapts to each customer."
- **What it enables.** Shipping a strong, correct default experience out of the box (fast time-to-first-relief, DOC-06 A5); letting customers tune the *bar and context* deeply; refusing configuration that would disable a gate.
- **What it rejects.** "Make everything configurable"; and equally, "our way or nothing." Also rejects any "flexibility" that is really a request to turn off fairness/explainability.
- **Trade-off accepted.** Some customers will want to configure things we won't let them (the gates); we accept that friction as the price of the mission.

---

## 9. Defining Stance: Evidence over Artifacts (as product belief)

- **The belief (C2).** Beyond strategy, this is a *product design conviction*: the product must always make **evidence of ability the easy, default path** and **artifacts (resumes, credentials, pedigree) the deprecated, hard path.**
- **Why.** If the product quietly re-privileges the resume (e.g., leads with it, ranks by it, lets it gate), we have rebuilt the thing we exist to destroy (DOC-02). The belief must be *built into what the product makes easy.*
- **Enables.** Surfaces that lead with demonstrated ability; treating the resume as one weak Signal, never a gate; making it *harder*, not easier, to decide on pedigree.
- **Rejects.** Any feature that makes artifact-based shortcutting the path of least resistance; "sort by school/employer" as a first-class action.
- **Trade-off.** Some users *want* to screen on pedigree out of habit; we will make that deliberately less convenient, and explain why.
- **Belief rejected.** "Meet users where they are (resume-first)." We meet users in their *workflow* (P11) but not in their *bias.*

---

## 10. Defining Stance: The Human Is the Hero

- **The belief (C7).** The product exists to make the *human* a better, more confident, more accountable decision-maker. The AI is the instrument; the human is the hero of every story the product tells.
- **Why.** Human Accountability (P2); trust (professionals reject software that de-skills or overrides them); and it is the honest truth of what we do — we augment judgment, we don't replace it.
- **Enables.** Framing every output as decision-support the human owns; making the human *more* capable (calibrated, evidenced) rather than bypassed; celebrating the recruiter's/manager's judgment, never the AI's.
- **Rejects.** "The AI decided"; automation that reduces the human to a rubber-stamp (click-theater, P2); marketing that makes the AI the protagonist.
- **Trade-off.** We forgo the efficiency and demo-appeal of "full autonomy"; we accept that on purpose.
- **Belief rejected.** "AI should replace human judgment in hiring." Never — not ethically, not legally, not as product.

---

## 11. Defining Stance: Simplicity & Subtraction

- **The belief (C6).** The best product is the smallest one that fully serves the decision. **Subtraction is a feature.** Every added feature is a permanent tax on clarity, trust, maintenance, and user attention.
- **Why.** Cognitive load degrades decisions and calm (DOC-06 §8); complexity compounds into the "80-metric dashboard" we forbid; simplicity is how infrastructure stays legible for a decade.
- **Enables.** Saying no to most feature requests (§12); removing features that don't earn their place; defaulting to fewer options; the "delete the screen" test (DOC-06 §4).
- **Rejects.** Feature-accretion to satisfy requests; "it's just one more toggle"; configuration sprawl.
- **Trade-off.** We will sometimes lack a feature a customer wants; we prefer a coherent product to a complete one.
- **Belief rejected.** "More features = more value." The opposite is usually true.

---

## 12. When We Say No to Customers *(ratified: "Refuse gates, negotiate the rest")*

Saying no well is a core product competency. We say no *more* than most companies, and we *explain* why — a principled no builds trust with serious enterprise buyers (it signals we won't compromise *their* fairness/defensibility either).

**The customer-request decision tree:**

```
Customer requests X
      │
      ▼
1. Does X violate a Tier-0 gate or identity non-negotiable? (P1–P7:
   fairness, explainability, human accountability, privacy, neutrality,
   sensors-not-product, candidate dignity, not-an-ATS/job-board)
      │
      ├─ YES ──▶ HARD NO. No negotiation. Explain the principle. Offer nothing that
      │          approximates the violation. (e.g., "auto-reject finalists with no human",
      │          "sell us candidate data", "turn off bias checks", "just be our ATS")
      │
      └─ NO ──▶ 2. Would X degrade Decision Quality or Trust? (§5)
                     │
                     ├─ YES ──▶ NO by default — but first seek a principle-respecting
                     │          ALTERNATIVE that meets the underlying need. Decline if none.
                     │
                     └─ NO ──▶ 3. Is X breadth-creep / off-core / not-yet? (C4, §7)
                                    │
                                    ├─ YES ──▶ "Not now." Explain roadmap/depth discipline;
                                    │          log the signal; revisit if it recurs and fits.
                                    │
                                    └─ NO ──▶ 4. Does X genuinely improve the decision
                                                 AND respect all principles?
                                                     │
                                                     └─ YES ──▶ Consider it. Prioritize by
                                                                impact on the objective function (§6).
```

- **The posture.** Gates are non-negotiable and get a clear, explained no. Everything else, we look for a way to serve the *real* need without compromising principles *before* we decline. We never say yes by *default* to revenue pressure (that is the "customer-led" posture we rejected).
- **Why.** Protects the moat, the mission, and — critically — the customer's own defensibility. A vendor that will bend *its* fairness for you will bend *your* fairness for the next customer; serious buyers understand this.
- **Trade-off.** We will lose some deals to a principled no. We accept this as the cost of being trustworthy infrastructure (C12).
- **What we never do.** Silently accommodate a gate violation for a big logo; accrete features via many small "yeses" until the product is incoherent (§11).

---

## 13. The Trade-offs That Define Us

A company is defined less by what it values than by *which value it sacrifices when two collide.* Here is where we stand, permanently. (These are the product-level expression of DOC-05's priority ladder.)

| When these collide… | We choose… | Because… |
|---|---|---|
| Quality ↔ Speed | **Quality** (ship the smallest *quality* slice fast) | Decision quality is the product (C1, P9); but we still move fast on the *quality* increment. |
| Depth ↔ Breadth | **Depth** | Depth compounds the moat; breadth commoditizes (C4, §7). |
| Trust ↔ Growth | **Trust** | Trust is the moat; it is spent instantly and rebuilt slowly (C12, P8). |
| Opinionated ↔ Configurable | **Opinionated defaults, bounded flexibility** | A product with no opinion improves nothing; gates never flex (C5, §8). |
| Evidence ↔ Convenience | **Evidence** | Convenience that re-privileges artifacts rebuilds what we kill (C2, §9). |
| Explainable ↔ Accurate-but-opaque | **Explainable** | Correctness includes fairness/defensibility; opacity is disqualifying (C9, P1). |
| Fewer-done-deeply ↔ Many-features | **Fewer, deeper** | Subtraction is a feature (C6, §11). |
| Long-term compounding ↔ Short-term win | **Long-term** (ignite the flywheel early, then compound) | We are judged over years, not demos (C10). |
| Candidate dignity ↔ Throughput | **Dignity** | Candidates are users, not inventory (C11, P7). |
| Human accountability ↔ Automation convenience | **Accountability** | The human is the hero; click-theater is forbidden (C7, P2). |
| AI visibility ↔ AI invisibility | **Invisible (but honest)** | The product, not the AI, is the story (C8, DOC-06 §7). |

> **The meta-trade-off:** whenever unsure, choose the option that a thoughtful customer would still thank us for in *three years*, not the one that wins *this quarter*. That single heuristic reproduces most of the table.

---

## 14. What We Will Refuse to Build (product-level)

Complementing the Manifesto's experience anti-patterns (DOC-06 §11) and the Constitution's non-goals (DOC-05 A-05.2 §A4), these are *product* refusals — things we will not build regardless of demand:

1. **An ATS, HRIS, or job board / portal.** (P4; C-level identity.) We integrate; we never become the system of record.
2. **A black-box scorer** — any evaluation output without its evidence and reasoning. (P1, C9.)
3. **A "better resume keyword matcher"** — a faster version of the broken gate we exist to replace. (C2.)
4. **An "AI interviewer" sold/priced as the product.** (P6, C8.) The sensor is never the product.
5. **Full autonomous hire/reject for high-risk decisions.** (P2.) Humans are accountable.
6. **A candidate-data marketplace or any candidate-data sale.** (P3/P7/C11.)
7. **Gamified or engagement-maximizing experiences** — points, streaks, attention traps. (DOC-06 §11.)
8. **Vanity analytics** — impressive dashboards that serve no decision. (§4, DOC-06 §4/§11.)
9. **Configuration that can disable a gate** — "turn off fairness/explainability." (§8.)
10. **Anything that trades trust for growth.** (C12.)

> This list is closed-by-default; adding an exception requires the Constitution Lifecycle process (DOC-05 A-05.2 §A5). "A big customer will pay for it" is *not* sufficient grounds (§12).

---

## 15. How the Product Should Evolve Over Time

The *beliefs* here are constant; the *product's form* evolves across the DOC-01 horizons. What changes is surface and scope; what never changes is the convictions (§2).

| Era | The product is… | Philosophy emphasis (what we lean on most) | What must NOT change |
|---|---|---|---|
| **Horizon 1 — Prove the layer** | A focused tool that proves *evidence beats resumes* in the beachhead (SWE screening). | Depth over breadth (§7); First Five Minutes (DOC-06 A5); igniting the Data flywheel. | The gates; evidence-first; human-as-hero. |
| **Horizon 2 — Embed the infrastructure** | Embedded Hiring Intelligence across the funnel and more roles. | Compounding (C4); Trust Ladder rungs 4–5; opinionated defaults at scale. | The gates; decision-quality-is-the-product; subtraction discipline. |
| **Horizon 3 — Become the standard / network** | The neutral standard of hiring judgment; portable candidate evidence; benchmarking network. | Trust as institutional/regulatory standard; candidate-as-user (portable evidence). | The gates; candidate dignity; neutrality; invisible-but-honest AI. |

- **The evolution rule:** we add surface only as depth earns it (C4, §7). We never let the product's *growth* outrun the *trust* that supports it (C12). Every era, the same one-line test of a good product (§3) applies.

---

## 16. Anti-Philosophies We Reject

Common industry beliefs we consciously reject — naming them inoculates the company against absorbing them by default.

| Industry belief | Our counter-belief |
|---|---|
| "The customer is always right." | The customer is right about their *need*, not always about the *solution* — and the candidate and the decision also have standing. We refuse gate-violating requests (§12). |
| "More features = more value." | More features usually = more cost, confusion, and eroded trust. Subtraction is a feature (C6). |
| "Move fast and break things." | Move deliberately and *don't break trust* — trust doesn't un-break (C12). We move fast on quality increments, never on trust. |
| "AI-first." | Decision-first, trust-first. AI is infrastructure that should disappear (C8). "AI-first" is how you build a demo, not a hiring product. |
| "Growth at all costs." | Trust over growth, always (C12). Growth bought with trust is a loan against the moat. |
| "Ship the demo." | Ship the *outcome.* We are judged over years (C10). |
| "Data is the new oil — extract it." | Candidate data is a *responsibility*, not a resource to exploit (P3/P7/C11). |
| "Delight the user." | *Relieve* the user (DOC-06 A2). Delight is novelty; relief is trust. |
| "Meet users where they are." | Meet users in their *workflow* (P11), never in their *bias* (§9). |

---

## Amendment A-07.2 — Product Economics: Complexity Budget, Deletion, and Innovation Source

*Dated 2026-07-21. CTO-ratified. The bible defined good/bad/quality but not the *economics* of building: what a feature truly costs, when features should die, and where ideas legitimately come from. These three complete the product DNA. Resolves §17.3 Q4 (subtraction governance).*

### A-1 — The Complexity Budget

> **Every feature spends from a finite Complexity Budget. Complexity is a finite, exhaustible resource. Every new feature must justify — explicitly — the complexity it introduces.**

- **The belief.** Teams routinely price a feature at its *build* cost. That is a fraction of its true cost. A feature is a *permanent liability* across many dimensions, paid every day it exists, by many people who never asked for it. Treating complexity as free is how great products rot into bloated ones (violates C6).
- **The full cost of a feature** (the "complexity bill" — account for *all* of it before adding):

  | Cost dimension | Paid by | Paid when |
  |---|---|---|
  | Engineering | Builders | Once + forever (it never stops needing care) |
  | Maintenance | Builders | Every release, forever |
  | Testing | QA/eng | Every change, forever |
  | Security | Security | Every audit; it is new attack surface (P8/Marcus persona) |
  | Support | Support/CS | Every confused customer |
  | Documentation | Writers | Creation + every change |
  | Training | CS/customers | Every new user, forever |
  | Migration | Eng + customers | Every future change to it |
  | Customer confusion | *Every user* | Every session (cognitive load — DOC-06 §8) |
  | API surface | Builders + integrators | Forever ("APIs are forever") |
  | Future debt | Everyone | Compounding, forever |

- **The budget rule.** A feature may be built only if its value **to the hiring decision** (C1/§6) clearly exceeds its *total* complexity bill — not just its build cost. When the budget is tight, **we delete before we add** (→ Deletion, A-2). Every option in the Customization Pyramid (§8.1) also spends budget; flexibility is not free.
- **Why (Linear/Stripe).** The most respected product companies stay small on purpose: they treat "no" as the default and make features *compete* for a scarce complexity budget. That discipline — not feature count — is why they feel fast, clear, and trustworthy for years.
- **Trade-off accepted.** We will ship *fewer* features than competitors and decline many reasonable-sounding ones. That is the point (C6, §11).
- **The belief rejected.** "If a customer will use it, build it." No — *if its full lifetime value to the decision beats its full complexity bill,* build it; otherwise decline (§12) or delete something first.

### A-2 — Product Deletion Philosophy

> **Features are born, evolve, become obsolete, and must be removed. Deletion is product quality. A roadmap that only grows is a product that is dying slowly.**

- **The belief.** Most companies have a rich vocabulary for *adding* and none for *removing* — so products only accrete, complexity compounds (A-1), and clarity dies. We give deletion equal standing. **Nothing is permanent except the Constitution's gates** (DOC-05 Tier 0).
- **When a feature should die** (deletion criteria):
  - It no longer serves a clear decision (fails Decision-Centric, DOC-06 §4).
  - Its complexity bill (A-1) now exceeds its value.
  - It is superseded by a better path.
  - Usage is negligible and doesn't justify the carrying cost.
  - It has drifted into conflict with the Philosophy/Constitution.
- **How we delete (with dignity — trust, C12).** Deprecate with a *superseded-by* pointer and backward-compatibility (mirroring DOC-04's term deprecation and DOC-05's Lifecycle), give customers notice and a migration path, then remove. Deletion respects users; it is not abandonment.
- **Cadence.** Regular **subtraction reviews** (a standing ritual, not a one-off) that ask of each surface: *does this still earn its complexity?* (This is the governance §17.3 Q4 asked for.)
- **The belief rejected.** "Removing features angers customers, so never remove." The greater harm is a bloated product that serves no one well; done respectfully, subtraction *increases* trust and clarity.

### A-3 — Innovation Philosophy *(where ideas legitimately come from)*

> **Ideas have a source hierarchy. We innovate from mission and problems downward — never by copying competitors.**

**The idea-source hierarchy (highest authority first):**
```
   1. MISSION            ── does this advance evidence-based, fair hiring? (DOC-01)
        ↓
   2. CUSTOMER PROBLEMS  ── real pains and jobs (DOC-02, DOC-09), not requested solutions
        ↓
   3. EVIDENCE           ── what Outcome Learning / data actually show works
        ↓
   4. PRODUCT VISION     ── our opinionated view of where hiring is going (C5)
        ↓
   5. CUSTOMER REQUESTS  ── a signal about a need — never a directive for a solution
        ↓
   6. COMPETITORS        ── watched to DIFFERENTIATE, the lowest source, never to copy
```

- **Why this order.** Mission-first keeps us from being pulled off-course by the loudest customer or the latest competitor. **Customer *problems* rank far above customer *requests*** because a request is a proposed *solution*, and customers are right about their *need* but often wrong about the *solution* (DOC-07 §12/§16). Evidence disciplines vision with reality (the Learning flywheel). Competitors are *last* — we study them to be *different* (DOC-03), never to imitate.
- **The forbidden path:** `Competitor → Copy.` We never build something merely because a competitor has it. Copying cedes our point of view (C5), commoditizes us (DOC-03 §24), and violates "AI-first/me-too" anti-philosophies (§16).
- **The belief rejected.** "Ship what customers ask for and match what competitors ship." That is how a product loses its soul and becomes a shallow feature-clone (DOC-03, §16).

---

## 17. Summary

### 17.1 The bible in one paragraph
We believe the product is the **quality of the hiring decision**, not the software; that **evidence beats artifacts**, **trust beats dazzle**, **depth beats breadth**, and **less beats more**; that the product should have a **point of view** (opinionated defaults, deep flexibility — with gates that never flex), should make the **human the hero** and the **AI invisible-but-honest**, and should be judged over **years, not demos**. A **good** product measurably improves and is trusted to make fair, explainable, defensible decisions; a **bad** product optimizes engagement, dazzle, breadth, speed, or extraction at the expense of trust. We optimize **evidence-backed decisions and trust**, and when values collide we choose **quality, depth, trust, evidence, explainability, dignity, and the long term.** We say **no** to gate-violating requests without negotiation, and we refuse to build the ATS, the black box, the resume-matcher, the data marketplace, the gamified experience, or anything that trades trust for growth.

### 17.2 Key decisions recorded
- **KD-07.1** — Twelve core product convictions (§2) are the product DNA; all product decisions derive from them.
- **KD-07.2** — Explicit, company-specific definitions of **good** (§3), **bad** (§4), and **quality** (§5, six dimensions, trust-dominant) — replacing the industry's feature/speed defaults.
- **KD-07.3** — We optimize **evidence-backed decisions, trust, quality-of-hire, and compounding** — and explicitly *not* engagement, volume, speed-alone, feature-count, or demo-shine (§6).
- **KD-07.4** — **Opinionated defaults, deep flexibility**, with an explicit flex/never-flex boundary (§8, ratified), visualized as **The Customization Pyramid** (§8.1) — the canonical mental model for what can change (top) vs. what never does (immutable Constitution base).
- **KD-07.5** — **Refuse gates, negotiate the rest** — a customer-no decision tree; principled no over revenue (§12, ratified).
- **KD-07.6** — The **defining trade-off table** (§13): quality/depth/trust/evidence/explainability/dignity/long-term/human-accountability/invisible-AI all win their conflicts.
- **KD-07.7** — A **closed product-refusal list** (§14) amendable only via the Constitution Lifecycle.
- **KD-07.8** — Nine **anti-philosophies** explicitly rejected (§16).
- **KD-07.9** — **Complexity Budget:** complexity is a finite resource; every feature must justify its *full lifetime cost* (11 dimensions), not its build cost; when tight, delete before adding. (A-07.2 §A-1.)
- **KD-07.10** — **Product Deletion Philosophy:** deletion is product quality; features can die; nothing is permanent except the gates; deprecate-with-dignity + standing subtraction reviews. (A-07.2 §A-2.)
- **KD-07.11** — **Innovation source hierarchy:** Mission → Customer Problems → Evidence → Product Vision → Customer Requests → Competitors; **never Competitor→Copy.** (A-07.2 §A-3.)

### 17.3 Open questions (for founder/CTO)
1. **Quality measurement:** which of the six quality dimensions (§5) do we instrument first, and how do we measure Trust Quality without gaming it? *(Ties to metrics work; principle stands.)*
2. **"Not now" memory:** how do we track repeatedly-declined breadth requests (§12) so a genuine pattern can later reshape the roadmap without eroding depth discipline?
3. **Opinionation calibration:** where exactly is the line between "our opinionated default" and "the customer's legitimate context" for *specific* evaluation choices? (Deferred to the Evaluation Engine, DOC-14; the *stance* is fixed here.)
4. ~~**Subtraction governance**~~ → **Resolved (A-07.2 §A-2):** Product Deletion Philosophy — deprecate-with-dignity + standing **subtraction reviews**; nothing permanent except the gates.

### 17.4 Suggested next document
**DOC-08 — Personas** — per the revised roadmap. With the full product-governance layer now complete — **Constitution** (decisions), **Manifesto** (feelings), **Philosophy** (beliefs) — we can finally profile *who* we build for, and then (DOC-09) *why they "hire" us* (JTBD). Every persona want can now be tested against three fixed references: does serving it respect the Constitution, produce the intended feeling, and honor the product philosophy? Personas built on that foundation stay honest.

**Roadmap position:** 01 Vision · 02 Problem · 03 Strategy · 04 Domain · 05 Constitution · 06 Manifesto · **07 Product Philosophy** · → **08 Personas** · 09 JTBD · 10 Customer Journey · 11 Functional · 12 NFRs · 13 AI Strategy · 14 Evaluation Engine · 15 Architecture · 16 Engineering Principles.

---

*End of DOC-07 v0.1 — the Product Bible. Intended to change over years, not months. Awaiting founder review of the four open questions (§17.3) before promotion to Ratified.*
