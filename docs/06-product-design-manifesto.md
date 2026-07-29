# Document 06 — Product Design Manifesto

| Field | Value |
|---|---|
| **Document ID** | DOC-06 |
| **Title** | Product Design Manifesto (The Experiential Constitution) |
| **Owner** | Principal Engineer / Technical Documentation Lead (with CTO & Design) |
| **Status** | **v0.3 — RATIFIED** (per CTO) — A-06.2 (Honest by Default, Relief over Delight, Emotional Journeys, Trust Ladder, First Five Minutes, Remove Fear) + A-06.3 (Error, Waiting, Silence philosophies) |
| **Created** | 2026-07-21 |
| **Depends on** | DOC-01 (Vision + A-0.2), DOC-03 (Strategy), DOC-04 (frozen vocabulary), DOC-05 (Constitution, esp. P1/P2/P7/P8/P13) |
| **Blocks** | DOC-07 (Product Philosophy), and every future UX, UI, design review, usability study, and product decision |
| **Nature** | The **experiential constitution.** DOC-05 governs *decisions*; this governs *feelings*. It is not a UX spec, not a design system, not a screen inventory. It defines **how every user should feel** — and what we will never make them feel. |
| **Vocabulary** | Uses DOC-04 frozen terms exactly (Evidence, Evaluation, Recommendation, Evaluation Score, Confidence, Integrity Score, Benchmark, Candidate, Hiring Decision, Progressive Explainability…). Introduces **no** new business terms. |
| **Scope discipline** | **No implementation. No specific screens. No component/library choices.** Examples are *experiential illustrations*, never designs. |

---

## How to read this document — Philosophy vs. Manifesto

Two sibling documents, deliberately separate:

| | **DOC-07 Product Philosophy** (next) | **DOC-06 Product Design Manifesto** (this) |
|---|---|---|
| Answers | *What do we believe?* | *What should every user feel?* |
| Lives in | Conviction | Experience |
| Example unit | "Evidence beats artifacts." | "I felt the evaluation was fair." |

This document exists because of a truth most companies never write down:

> **Engineers build features. Designers build interfaces. Users experience *feelings*. And for us, the feeling is the product — because Trust is literally the moat (DOC-03).**

Everything here is downstream of a single reframe:

| The user should NOT feel (technology) | The user SHOULD feel (experience) |
|---|---|
| "An AI interviewed me." | "I felt understood." |
| "An AI scored me." | "The evaluation was fair." |
| "This looks smart / high-tech." | "I trust this recommendation." |
| "The AI is doing something." | "This company built a genuinely great hiring product." |

One column is *technology*. The other is *experience*. This manifesto is a machine for producing the right column, on every screen, for every user, for the next decade.

---

## Amendment A-06.2 — Trust-Driven Disclosure, Relief, and the Temporal Experience

*Dated 2026-07-21. CTO-ratified. Adds six sections that move the manifesto from a *static* description of feeling to a *temporal* one — how the product should move users from one emotional state to another over time. Resolves §13.3 Q1 (AI disclosure) and Q3 (delight). Authoritative where it differs from earlier text.*

### A1 — Honest by Default *(refines §7 Invisible AI and P13)*

We were framing AI disclosure as a *legal* question. It is a **trust** question. The rule:

> **Don't ask "Should we disclose AI?" Ask "Would a reasonable user feel *misled* if they discovered AI involvement later?"**
> - If **yes** → **disclose, clearly and plainly.**
> - If disclosure adds no value and would only distract → **don't force it into the user's attention.**

- **Why this is better than a legal rule.** A legal rule produces either over-disclosure (hype/noise that breaks calm) or minimal-compliance (which can still feel like concealment). The "would I feel misled?" test produces *exactly* the disclosure that preserves trust — no more, no less. It is the honest middle between AI hype and hidden AI (§7's "invisible, not hidden").
- **The canonical candidate disclosure** (tone reference, not a screen spec):
  > *"This evaluation included automated analysis together with human review, according to the company's hiring process."*
  Simple. No model names. No hype. No hidden AI. It tells the truth a candidate would want to know, in a way that reassures rather than alarms.
- **Decisions it enables.** Disclosing AI involvement wherever a person's outcome was shaped by it; omitting AI-badging on internal surfaces where it adds nothing but noise.
- **Decisions it rejects.** Burying AI involvement a candidate would care about; *and* decorating every surface with AI callouts. Both fail the trust test.
- **Resolves §13.3 Q1.**

### A2 — Relief over Delight *(resolves §13.3 Q3 — the emotional target)*

Consumer products optimize for **delight**. Infrastructure optimizes for **relief.** We optimize for relief.

> **Delight creates novelty. Relief creates trust.** Novelty fades and must be constantly re-manufactured (engagement mechanics, dark patterns). Relief compounds into dependence and loyalty — exactly the embeddedness an infrastructure company needs.

The emotion we design for, per persona, is a quiet exhale — *"Finally."*

| Persona | The relief ("Finally…") |
|---|---|
| **Candidate** | *"Finally — someone evaluated what I can actually do."* |
| **Recruiter** | *"Finally — I can defend my shortlist."* |
| **Hiring Manager** | *"Finally — I understand *why* these candidates."* |
| **Executive** | *"Finally — I have evidence, and hiring is under control."* |
| **Administrator / Compliance** | *"Finally — I can prove this was fair."* |

- **The design consequence.** We never chase "wow." We chase the disappearance of a burden the user has carried for years. A feature that produces *delight* but not *relief* is a consumer instinct we distrust; a feature that produces *relief* is on-mission even if it never dazzles. (This is the disciplined answer to "should the product have delight?" — warmth is expressed as *relief, respect, and usefulness*, never as cheerfulness or gamification, §3.5/§11.)

### A3 — Emotional Journeys *(experience over time, not a static state)*

"The product should feel calm" is too static. The product should **intentionally move each persona from an entering emotional state to an earned one.** Each transition is a design responsibility, not an accident.

**Candidate** (including the rejection path — the hardest and most important):
```
Curiosity → Hope → Nervousness → Focus → Reflection → [outcome] → Acceptance → Growth
```
| From → To | The product's job at this transition |
|---|---|
| Curiosity → Hope | Signal fairness immediately ("you'll be evaluated on what you can do") so hope is *warranted*, not naive. |
| Hope → Nervousness → Focus | Reduce anxiety; make the task clear and calm so nerves resolve into focus, not dread. |
| Focus → Reflection | Let the experience feel meaningful — the candidate senses they were *understood*, not processed. |
| Reflection → Acceptance (esp. on rejection) | Respectful, evidence-based feedback (P13 candidate view) so even a "no" lands as fair, not arbitrary. |
| Acceptance → Growth | Leave the candidate with a genuine learning direction — the Afterlife emotion is *motivation*, not resentment. |

**Recruiter:**
```
Overwhelmed → Organized → Confident → Certain → Defensible
```
*Product's job:* cut the low-signal noise (Overwhelmed→Organized), surface trustworthy evidence (→Confident), make the shortlist stand up (→Certain), and make it presentable/explainable to the hiring manager and, if needed, a regulator (→Defensible).

**Hiring Manager:**
```
Uncertain → Calibrated → Confident → Accountable
```
*Product's job:* capture their real bar (→Calibrated), show why each candidate meets it (→Confident), and let them *own* the decision with full understanding (→Accountable — the felt form of P2 Human Accountability).

**Executive:**
```
Exposed / Skeptical → Informed → Assured → In Command
```
*Product's job:* replace risk-anxiety with aggregate evidence of quality and fairness (→Informed/Assured) and a felt sense of control over hiring outcomes and risk (→In Command).

**Administrator / Compliance:**
```
Blind / Anxious → Sighted → In Control → Audit-Ready
```
*Product's job:* full visibility and complete, exportable decision trails, so the persona moves from fear-of-the-unprovable to confident audit-readiness.

> **Principle:** design every experience as a *transition*, and name the from-state and to-state. If a surface doesn't move the user toward a better emotional state, ask what it's for (§4).

### A4 — The Trust Ladder *(how trust is earned over time)*

Trust is not granted; it is climbed, rung by rung. We design for the whole ascent, and we never skip a rung.

| Rung | The user believes… | The product's job to earn it |
|---|---|---|
| **1. It works** | *"This is reliable."* | Flawless reliability, speed, no surprises. Trust starts with competence. |
| **2. The explanations make sense** | *"I understand *why*."* | Evidence-first (§5), Progressive Explainability (§6) — reasoning that holds up to scrutiny. |
| **3. Predictions prove correct** | *"It was right."* | Outcome Learning made visible over time — the recommendations track reality. |
| **4. The recruiter depends on it** | *"I rely on this."* | Consistent relief (A2); the individual can no longer imagine working without it. |
| **5. The organization trusts it** | *"We hire this way now."* | Institutional trust — fairness track record, auditability, executive assurance. The platform is how the company hires (infrastructure). |

- **Why it matters.** It sequences the entire experience and business: you cannot sell rung 5 (org trust) before delivering rung 1 (it works). It maps directly onto the Trust flywheel (DOC-03 §16) and embeddedness. **Design for the next rung the user is on — never assume a rung they haven't climbed.**

### A5 — The First Five Minutes *(onboarding philosophy)*

> **Every new enterprise customer should feel, within five minutes: "I already understand this."** No training, no manual, no consultant required to *get it.*

| Milestone | The intended experience |
|---|---|
| **First impression** | Calm, serious, unmistakably *for hiring* — feels like professional infrastructure, not an AI gadget. Zero intimidation. |
| **First action** | Obvious and low-stakes — the user does one meaningful thing without instruction (guided by §8 defaults and single-primary-action). |
| **First recommendation** | Evidence-first (§5): the user sees *why* before any score, and immediately thinks *"I understand how this thinks — and it thinks the way I'd want to."* |
| **First success** | The first "Finally…" (A2): a moment of genuine relief — a defensible shortlist, an understood candidate — that proves the value proposition, fast. |

- **The standard.** Time-to-first-relief is a first-class experience metric. If a new customer needs a training session to feel oriented, the onboarding experience has failed — infrastructure should feel *immediately legible.*

### A6 — Remove Fear *(a first-class design principle)*

Every enterprise product *introduces* anxiety. Ours must **actively reduce** it. Fear is the enemy of both adoption and good decisions; removing it is a design mandate, not a nicety.

| Persona | Core fear(s) | How the experience removes it |
|---|---|---|
| **Recruiter** | *"Will AI replace me?"* | Position and *feel* as augmentation: the product makes the recruiter more credible and defensible (relief, A2), never sidelined. It hands them evidence to *own*, not a verdict that replaces them. |
| **Candidate** | *"Will a machine judge me unfairly? Will I have no recourse?"* | Fairness felt (§3.7), evidence-based respect (§3.3), honest disclosure (A1), and constructive feedback even in rejection (P13). The candidate feels *seen*, not processed. |
| **Hiring Manager** | *"Will this force a decision I don't understand or can't stand behind?"* | Calibration to *their* bar and full explanation (§6) — they end up *more* in control and accountable (P2), never managed by the tool. |
| **HR / People Leader** | *"Will this be biased? Will candidates hate it? Will it embarrass us?"* | Visible fairness safeguards, respectful candidate experience, and a defensible trail — the leader feels *protected*, not exposed. |
| **Executive / Legal** | *"Will we get sued? Will leadership/regulators trust it?"* | Auditability, explainability, and fairness posture surfaced as assurance (Exec journey, A3); the product reduces legal/reputational risk rather than adding it. |
| **Administrator / Compliance** | *"Can I prove this if challenged?"* | Complete, exportable decision trails; nothing withheld from audit (§6) — moves them to Audit-Ready (A3). |

- **The principle.** *Before a persona can feel relief (A2) or climb the Trust Ladder (A4), their fear must be named and removed.* Fear-removal is the precondition for trust. Every persona-facing experience must be tested against: **"What is this person afraid of here, and does this reduce that fear?"** (Now part of the §12 checklist.)

---

## Amendment A-06.3 — Error, Waiting, and Silence Philosophies

*Dated 2026-07-21. CTO-ratified. The manifesto described the ideal experience but not the *failure*, the *waiting*, and the *negative space*. These three philosophies complete it. A product's maturity is revealed most in how it fails, how it makes you wait, and when it chooses to stay quiet.*

### A7 — Error Philosophy *(how failure should feel)*

Failure is not an edge case in hiring software — it is routine: the AI is momentarily unavailable, an interview is interrupted, evidence is incomplete, confidence is low, the network drops, a candidate leaves halfway. We design the failure experience as deliberately as the success one.

**The four laws of failure** (non-negotiable):
1. **Failure must never create panic.** Calm, plain, reassuring — never alarming red walls or blame-language.
2. **Failure must increase clarity.** Every failure explains what happened, what it means, and what happens next. (An error that confuses is a second failure.)
3. **Failure must never feel like blame.** Never imply the user (or candidate) did something wrong when the system failed.
4. **Failure must always preserve dignity** — especially the candidate's (P7).

Add three corollaries from our principles:
5. **Failure never silently harms fairness.** A failure that drops or corrupts Evidence must *never* be allowed to bias a result — it degrades gracefully to lower Confidence or a human hand-off (P1/P2), never to a wrong-but-confident answer.
6. **Failure preserves work.** Nothing the user or candidate did is lost; recovery is always offered (no dead ends, undo — §8).
7. **Failure is honest** (A1) — we never fake success to hide a failure, and never fake certainty when evidence is incomplete (§3.4).

| Failure mode | How it should feel / what the product does |
|---|---|
| **AI unavailable** | Calm honesty: "we can't complete this right now; nothing is lost; here's what happens next." No panic, no blame. |
| **Interview interrupted** | Progress preserved; the candidate is *reassured it won't count against them* (dignity, no blame); a clear, easy resume path. |
| **Evidence incomplete** | Surfaced as honest low Confidence (not hidden, not fabricated); shows what's missing; routes to human accountability (P2). |
| **Low confidence** | Treated as information, not failure — surfaced plainly (§3.4) so the human weights it correctly; never smoothed into false certainty. |
| **Network issue** | Graceful, recoverable, work preserved; a calm "try again," never a catastrophe. |
| **Candidate leaves halfway** | No penalty framing; dignity preserved; a warm, low-friction way to return (ties to Waiting, A8). |

> **The standard (Stripe-grade):** a great failure experience leaves the user *more* oriented and *less* anxious than before the failure — clear, blameless, recoverable, and honest.

### A8 — Waiting Philosophy *(how waiting should feel)*

Hiring is mostly waiting: applied → wait; interviewed → wait; decided → wait; offered → wait. Waiting is the *dominant* experience, and today it is the "black hole" (DOC-02 P-C4) — the single most damaging candidate experience. We treat waiting as a designed state, not dead air.

**The laws of waiting:**
1. **Never abandon.** The user/candidate always knows *where they stand* and *what's next* — waiting is *communicated*, never silent-by-neglect. (The black hole is the anti-pattern.)
2. **Be honest about time.** Set real expectations; never fake progress or imply speed we can't deliver (A1, §3.4).
3. **Waiting should feel *held*, not ghosted** — especially for candidates. Dignity persists through the wait (P7).
4. **Communicate at meaningful moments, not constantly.** Updates mark genuine state changes (DOC-04 Hiring Events), not manufactured touchpoints for engagement (reconciles with Silence, A9; never an attention trap, §11).
5. **Waiting has a next step.** Even "we're still reviewing" tells the user what to expect and when — no dead ends (§8).

- **Per persona:** the *candidate's* wait is the most anxious and most important (design it with the most care); the recruiter waits on Evaluations; the hiring manager waits on the shortlist. Each deserves honest status and a clear horizon.
- **The felt goal:** transform waiting from *anxiety* (the black hole) into *calm confidence that the process is moving and I have not been forgotten.* Waiting well is a major driver of the candidate's Curiosity→Hope→…→Acceptance journey (A3).

### A9 — Silence Philosophy *(when the best UX is nothing)*

Product maturity is knowing when **not** to act. Sometimes the best experience is no popup, no notification, no AI suggestion, no interruption.

**The laws of silence:**
1. **Default to silence; earn the right to interrupt.** The burden of proof is on the interruption, not on staying quiet.
2. **Interrupt only to serve the user's decision** (Decision-Centric §4) — never to serve *our* engagement metrics (attention traps are forbidden, §11; Non-Goal, DOC-05 A-05.2 §A4).
3. **Every notification clears a high bar:** *is this worth breaking their focus right now?* If not, it waits or disappears.
4. **Calm requires silence** (§3.1). A product that constantly pings is not calm, however useful each ping feels in isolation.
5. **No chatty AI.** The intelligence does not narrate itself ("✨ I noticed…"); it stays quiet infrastructure (Invisible AI, §7). Silence is part of how AI *disappears*.

- **Reconciling Silence and Waiting:** they are not in conflict — Waiting (A8) says *communicate at meaningful state changes*; Silence (A9) says *be quiet between them.* Together: **speak exactly when it matters, and not otherwise.** Meaningful Hiring Events warrant a word; everything else warrants quiet.
- **The felt goal:** the product feels like a calm, trustworthy professional who speaks when there's something worth saying and is comfortable saying nothing when there isn't — never a needy app fighting for attention.

---

## 1. Why Product Experience Matters

1. **Trust is the moat, and trust is a feeling before it is a fact.** DOC-03 stakes the company on trust (the Trust flywheel, §16). A recruiter, hiring manager, or candidate does not compute our fairness — they *feel* whether to trust a Recommendation. If the experience feels manipulative, opaque, or gimmicky, the underlying fairness never gets a chance to matter. **The experience is the delivery mechanism for trust.**

2. **We are asking people to change what they rely on.** We are replacing gut-and-resume with evidence-based judgment (DOC-02). That is an emotional ask, not just a functional one. People adopt a new basis for high-stakes decisions only when the experience makes them feel *more* confident and *more* accountable, not less.

3. **The stakes are human and asymmetric.** A hiring decision changes a person's livelihood. A candidate's experience of being evaluated — especially of being *rejected* — is one of the most emotionally charged interactions in professional life. Getting the *feeling* wrong isn't a UX blemish; it's a betrayal of the mission (P7: candidate as user).

4. **Enterprise buyers buy calm.** Our buyers (VP TA, CHRO, CIO — KD-03.11) are accountable, risk-averse professionals. They do not want dazzle; they want to feel that this is *serious infrastructure* that will not embarrass them in front of a candidate, a regulator, or their board. Calm, professional, explainable experience *is* the enterprise sales argument made tactile.

5. **Feelings compound or corrode — like the flywheels.** Every screen either deposits trust or withdraws it. Consistent, calm, honest experience compounds into reputation (the Data/Trust flywheels); inconsistency and hype corrode it faster than features can rebuild it.

> **Principle Zero:** *We do not design interfaces. We design the feeling of making a decision you can trust and defend.*

---

## 2. Experience Vision — how each stakeholder should feel

Every persona (detailed later in DOC-08) must leave every interaction with a specific, intended feeling. If they feel anything else, the design has failed — regardless of how functional it is.

| Stakeholder | Should feel… | Should NEVER feel… |
|---|---|---|
| **Candidate** | *"I was seen for what I can actually do. This was fair, respectful, and worth my time — even if I wasn't selected."* Understood, respected, given a fair shot, and left with something useful. | Judged by a machine; processed; humiliated; ghosted; tricked; reduced to a number. |
| **Recruiter / TA** | *"I can trust this shortlist and defend it. It made me look competent and thorough."* In control, credible, unburdened of low-signal noise, confident presenting to the hiring manager. | Overwhelmed by dashboards; second-guessed by a black box; forced to defend something they can't explain. |
| **Hiring Manager** | *"I understand why these candidates, against my bar. I can make this call with confidence."* Informed, calibrated, respected as the decision-owner. | Managed by the tool; buried in data; pushed toward a decision they don't understand or own. |
| **Executive** | *"Hiring here is fair, high-quality, and defensible. This is under control."* Assured, in command of the big picture, unexposed to risk. | Alarmed; drowning in vanity metrics; unsure whether the company is legally/reputationally safe. |
| **Administrator / Compliance** | *"I can see everything, audit anything, and prove this was fair."* Fully sighted, in control, audit-ready. | Blind; unable to explain a decision when challenged; surprised. |

> The unifying feeling across all five: **calm, earned confidence.** Not excitement. Not delight-for-its-own-sake. The quiet confidence of a professional who trusts their instrument.

---

## 3. Emotional Design Principles

*The nine feelings every experience must produce. Each: **Description · Why it matters · Good (experiential) examples · Bad (experiential) examples.** These are feelings, not screens.*

### 3.1 Calm
- **Description.** The experience is quiet, focused, and unhurried. One thing at a time. Space, not density. No noise, no clamor for attention.
- **Why it matters.** Hiring decisions are high-stakes; anxiety degrades judgment. Calm signals seriousness and control — the opposite of a consumer app fighting for engagement. Enterprise buyers equate calm with trustworthy.
- **Good.** A decision surface that shows the *one* thing that matters now, with everything else a deliberate click away. A quiet, confident summary a busy hiring manager can absorb in seconds.
- **Bad.** An 80-metric dashboard on login. Ten competing calls-to-action. Notification badges demanding attention. Motion and color used to excite rather than to inform.

### 3.2 Trustworthy
- **Description.** Everything feels reliable, consistent, and honest. Nothing surprises the user unpleasantly. The product behaves the same way every time and never hides the ball.
- **Why it matters.** Trust is the moat (DOC-03; P8). Trust is built by a thousand consistent, honest moments and destroyed by one manipulative or opaque one.
- **Good.** A Recommendation always shows its Evidence first; the same action always lives in the same place; the system says what it will do before it does it.
- **Bad.** A confident-looking score with no basis; behavior that changes unpredictably; anything that feels like it's steering the user for the company's benefit rather than the decision's.

### 3.3 Respectful (especially to rejected candidates)
- **Description.** Every person is treated as a professional whose time and dignity matter — most of all the people we *don't* select.
- **Why it matters.** Candidates are first-class users (P7), and the rejected are the majority and the Candidate Afterlife (DOC-03 §18.4). Respect here is both ethics and network growth. It is the single sharpest test of whether we mean what we say.
- **Good.** A rejection that leads with what the candidate genuinely demonstrated well, offers constructive, evidence-based observations and a learning direction (P13 candidate view), and thanks them for their time.
- **Bad.** "Unfortunately you were not selected." and nothing else. A cold auto-message. Any implication that the person is deficient rather than "not the strongest match for *this* role."

### 3.4 Honest
- **Description.** The system tells the truth, including about its own uncertainty. It never manufactures confidence it does not have.
- **Why it matters.** Confidence is a defined, first-class concept (DOC-04) precisely so we can be honest about it. Fake certainty is the fastest way to lose the trust of a sophisticated user — and a legal liability.
- **Good.** "High Confidence" and "Low Confidence — limited evidence gathered for this competency" shown plainly and differently. The system visibly *knows what it doesn't know.*
- **Bad.** Presenting a low-Confidence Evaluation Score with the same authority as a high-Confidence one. Rounding away uncertainty. Implying precision the evidence doesn't support (confusing Confidence with certainty — an explicit anti-pattern, §11).

### 3.5 Professional
- **Description.** Enterprise-grade seriousness. The register of a trusted advisor, not a consumer app or a game.
- **Why it matters.** Our buyers and the gravity of hiring demand it; it differentiates us from gamified, hype-driven tools (P6, anti-patterns).
- **Good.** Clean typography, precise language, restraint. It feels like it belongs in a boardroom and in front of a candidate.
- **Bad.** Emojis in the product chrome, celebratory confetti, badges, streaks, achievements, "You're on fire!" — any consumer-gamification vocabulary.

### 3.6 Transparent
- **Description.** The user can always see *why*. Nothing consequential is a black box to the audience entitled to understand it.
- **Why it matters.** Explainability is a Tier-0 gate (P1), delivered audience-appropriately (P13). Transparency is how fairness becomes *felt*.
- **Good.** Every score and Recommendation is one glance away from the Evidence and reasoning behind it, at the depth appropriate to that audience.
- **Bad.** "Trust us, the algorithm decided." Hiding the basis of a decision from someone entitled to it. (Note: transparency is audience-aware — hiding proprietary internals from *candidates/competitors* is correct, §6; hiding the *basis of the decision* from those entitled is not.)

### 3.7 Fair
- **Description.** The experience actively *feels* even-handed — no candidate feels advantaged or disadvantaged by anything other than evidence of ability.
- **Why it matters.** Fairness is the mission and a gate (P1). It must be experienced, not merely engineered; a fair system that *feels* arbitrary still fails.
- **Good.** Consistent structure across candidates; evidence-anchored language; visible, role-relevant criteria. The candidate feels the same rules applied to everyone.
- **Bad.** Anything that feels arbitrary, personality-driven, or pedigree-driven; inconsistent experiences between candidates for the same Role.

### 3.8 Confident without arrogance
- **Description.** The product is self-assured enough to be relied upon, humble enough to defer to the human and to admit limits.
- **Why it matters.** We are decision *support*, not decision *maker* (P2). Arrogant software that "knows best" violates human accountability and repels professionals.
- **Good.** "Here is the evidence and our Recommendation; the decision is yours." Strong where evidence is strong; explicitly tentative where it isn't.
- **Bad.** "The AI recommends you reject this candidate." delivered as verdict. Overriding tone. Implying the human is a formality (that is the "human click theater" P2 forbids — felt as arrogance).

### 3.9 Helpful without controlling
- **Description.** The product guides and reduces effort, but never manipulates, coerces, or removes the human's agency.
- **Why it matters.** Guidance reduces cognitive load (§8) and builds trust; control (dark patterns, forced paths, coercive defaults) destroys it and violates P7.
- **Good.** Smart defaults the user can always change; a clear suggested next step the user is free to ignore; gentle warnings before mistakes.
- **Bad.** Forcing a path; hiding the exit; defaults that serve the company over the user; nudges engineered to increase our metrics rather than the user's success.

---

## 4. Decision-Centric Design

> **Every screen exists to support exactly ONE decision. If it doesn't, delete it.**

- **The philosophy.** We are Hiring Intelligence Infrastructure; our product is Decision Quality (P9). It follows that the atomic unit of our experience is not a "page" or a "feature" — it is a **decision**. Every surface must be able to answer, in one sentence: *"What decision is this helping the user make right now?"*
- **The test (applied to every surface).** *What decision? Whose decision? What would help them make it well? What is the one next step?* If a screen supports zero decisions, it is decoration and is removed. If it tries to support many, it is split until each supports one.
- **Why this matters.** It is the antidote to feature-creep, dashboard-sprawl, and vanity metrics. It keeps the experience calm (§3.1) and low-load (§8) by construction, and it keeps the product honest about its own purpose.
- **Good.** A candidate-review surface that exists to help *this* human make *this* advance/reject decision, showing exactly the evidence that bears on it.
- **Bad.** A "analytics hub" that shows everything and helps no specific decision; a screen that exists because "it looks comprehensive."

---

## 5. Evidence-First Design

> **The order is fixed and never reversed: Evidence → Explanation → Recommendation → Score.**

```
   1. EVIDENCE        (what the candidate actually demonstrated)
          ↓
   2. EXPLANATION     (what that evidence means, in plain language)
          ↓
   3. RECOMMENDATION  (the suggested action, owned by a human — P2)
          ↓
   4. EVALUATION SCORE (the quantified summary — LAST, never first)
```

- **Why the order is sacred.** Leading with a number ("Score: 82") trains everyone — recruiter, manager, candidate — to trust the *number* instead of the *reasoning*. That is exactly the black-box behavior we exist to replace (DOC-02, P1). Evidence-first design makes the score the *conclusion of an argument the user has already seen*, not a verdict they must take on faith. It operationalizes Explainability (P1) as a *sequence*, not a footnote.
- **Consequence.** A bare score with the evidence hidden "below the fold" or one click away is an evidence-*last* design in disguise. The evidence and its explanation must be encountered *before* the number, not merely be *available*.
- **Good.** The user reads what the candidate did and what it means, and *then* sees the Evaluation Score as a natural summary — with Confidence and Integrity Score alongside it.
- **Bad.** A big "82" at the top with a "see details" link. A ranked list of scores with evidence buried. Any surface where the number arrives before the reasoning.

---

## 6. Progressive Explainability (Constitutional P13, as experience)

This section translates **Constitutional Principle P13** (DOC-05 A-05.2 §A2) from governance into felt experience: **different audiences receive different depths of explanation — by design, not by omission.**

| Audience | The experience they should have | What they must never encounter |
|---|---|---|
| **Candidate** | Feels *seen and helped*: strengths, evidence-based observations, constructive improvement areas, a learning direction. Leaves with something valuable even in rejection. | Internal thresholds, Company Calibration, Benchmark formulas, anti-fraud/Integrity mechanics, weighting logic. |
| **Recruiter** | Feels *equipped and credible*: full Recommendation, Confidence, Evaluation Score, Integrity Score, the Evidence, Benchmark — enough to trust and defend the shortlist. | Cross-company data; raw model internals. |
| **Hiring Manager** | Feels *calibrated and in command*: everything the recruiter sees, plus how it aligns to *their* bar (Calibration) and relevant Hiring Memory insight. | Other companies' data; raw internals. |
| **Executive** | Feels *assured*: aggregate decision-quality, fairness posture, pipeline & Benchmark health, ROI — the big picture, under control. | Per-candidate mechanics (unless also the hiring manager). |
| **Compliance / Admin** | Feels *fully sighted*: complete evidence, reasoning, fairness tests, and decision trail — able to prove fairness on demand. | Nothing withheld from audit. |

- **The felt principle:** *Transparency does not require exposing every internal mechanism.* Each audience feels they received exactly the explanation they needed — never too little (which breaks trust) and never a firehose (which breaks calm) and never our IP (which breaks the moat).
- **The design tension it resolves:** candidate respect (P7) vs. IP protection (P6) vs. fairness (P1). Progressive Explainability is how a single experience honors all three simultaneously.

---

## 7. Invisible AI — *invisible, not hidden*

> **The platform must never feel like an AI demo. AI is infrastructure — like electricity. You feel the light, not the current.**

- **The stance.** Users should think *"this company built a genuinely great hiring product,"* never *"the AI is doing something."* We do not decorate the product with AI. The experience focuses on **hiring quality**, not **AI capability**.
- **The critical distinction — invisible ≠ hidden.** "Invisible" means *unhyped and unobtrusive.* It does **not** mean *concealed.* Where trust, fairness, and law require it, we **honestly disclose** that AI was involved (P1, P13, regulatory reality). We never *hide* the use of AI from a candidate or regulator; we simply never *market* it or turn it into spectacle. **Honest disclosure, zero hype.**

### 7.1 Rules for AI visibility

**Forbidden (hype):**
- No "✨ AI-Powered," "🤖 AI-Generated," "🔥 Smart AI," "Powered by [model]" badges or decoration.
- No AI mascot, no anthropomorphized assistant persona, no "the AI thinks…" voice.
- No framing a capability as impressive *because* it's AI. The user cares about the hiring outcome, not the technology.
- No "sparkle" iconography signaling "magic happened here."

**Required (honesty & trust):**
- Where a person's evaluation involved AI, that fact is **available and clear** in plain, non-hyped language (candidate right-to-know; audit).
- The *outcome* is branded (evidence, fairness, defensible decision), never the *mechanism*.
- When AI is uncertain, that is surfaced honestly (§3.4), not smoothed over.

- **Why.** Hyping AI (a) commoditizes us into "an AI tool" a giant can clone (P6, DOC-03), (b) invites the "black-box hype" distrust the first AI-hiring wave created (DOC-02), and (c) distracts from the only thing that matters — the quality and fairness of the decision. Making AI *disappear as spectacle while remaining honest as disclosure* is the mature, trustworthy posture.
- **Good.** "Here is the evidence and the recommendation." (The intelligence is felt, not announced.) A quiet, honest note that the evaluation used automated analysis, available to the candidate.
- **Bad.** A glowing "✨ AI Analyzed!" banner. A robot avatar "thinking." Marketing the model. *Also bad:* concealing from a candidate that AI was involved (that's "hidden," which we reject as strongly as hype).

---

## 8. Cognitive Load Principles

> **The user's attention is sacred and finite. Every screen should make the next right action obvious and effortless.**

| Principle | The felt experience |
|---|---|
| **One question per screen** | Each surface answers *one* question; the user is never asked to hold ten things in their head. |
| **One primary action** | At most one obvious primary action; secondary actions are visibly subordinate. The user never wonders "what's the main thing here?" |
| **Progressive disclosure** | Depth is available on demand, never dumped upfront. Start simple; reveal complexity only when asked. |
| **Defaults over configuration** | The right thing happens by default (P7-safe defaults); configuration is optional, never a prerequisite. The user isn't forced to set up before they can benefit. |
| **Evidence before charts** | Understanding (evidence/explanation) precedes visualization; charts illustrate a point already made, never substitute for it. |
| **Warnings before errors** | The product prevents mistakes gently *before* they happen rather than scolding after. |
| **No dead ends** | Every state offers a way forward; the user is never stranded with "now what?" |
| **Always show the next step** | The UI guides; the user should never have to ask "what do I do now?" |
| **Undo wherever possible** | Actions are reversible; the user can explore without fear. Confidence comes from safety. |

- **Why this matters.** Cognitive load is the enemy of calm (§3.1) and of good decisions. A tired, overloaded hiring manager makes worse, more biased decisions — the opposite of our mission. Low load is not a nicety; it is a *fairness and quality* mechanism.
- **The overarching rule:** *If a user has to think about the interface, we have failed. They should only have to think about the decision.*

---

## 9. Accessibility Principles

> **Accessibility is product quality, not a compliance checkbox. An experience that excludes people is a broken experience — and, for a fairness company, a hypocritical one.**

- **Why it belongs here (not in a legal appendix).** We exist to make hiring *fair* (P1). A product that is itself inaccessible discriminates against candidates and users with disabilities — an unacceptable contradiction of the mission. Accessibility is fairness made concrete in the interface.
- **Felt principles:**
  - **Color is never the only signal.** Meaning is always carried by more than color (text, shape, label) — so a colorblind user loses nothing.
  - **Keyboard works everywhere.** Every action is reachable and operable without a mouse.
  - **Readable.** Sufficient contrast, humane type sizes, plain language. No one squints or strains.
  - **Fast.** Performance is accessibility — slow interfaces exclude people on poor connections and older devices, and erode calm.
  - **Inclusive by default.** Designed for the widest range of humans from the start, not retrofitted.
- **The standard:** we design for the person having the hardest time, not the easiest. If it works well for them, it works well for everyone.

---

## 10. Product Tone & Voice

> **The product speaks like a trusted, precise, respectful professional advisor — never a hype-machine, a game, or a salesperson.**

- **We are:** Professional. Clear. Precise. Respectful. Plain-spoken. Calm.
- **We are never:** Dramatic. Manipulative. Overly cheerful. Coercive. Falsely certain. Jargon-y. Cute.

| Voice principle | Do | Don't |
|---|---|---|
| **Precise** | "Limited evidence was gathered for this competency." | "Hmm, not sure about this one!" |
| **Respectful** | "You demonstrated strong system-design reasoning." | "You failed the system-design round." |
| **Honest about certainty** | "Low Confidence — treat as preliminary." | "This candidate is definitely a top performer." |
| **Calm** | "Recommendation ready for your review." | "🎉 Your results are in!!!" |
| **Non-coercive** | "You can advance, hold, or decline." | "Act now — top candidates go fast!" |
| **Plain** | "This candidate is stronger on backend than frontend." | "Candidate exhibits heterogeneous competency variance." |

- **On rejection language specifically (the highest-stakes voice moment):** always frame as *"not the strongest match for this role,"* never *"not good enough."* Lead with what was demonstrated. Never dramatize, never patronize, never falsely encourage.
- **Never pretend certainty.** The voice always distinguishes an Evaluation Score from a fact, a Recommendation from a decision, Confidence from truth.

---

## 11. Experience Anti-patterns — what we will NEVER build

A closed, explicit list. These are not "avoid where possible" — they are **forbidden**, because each one trades trust (our moat) for a cheap short-term metric.

| Anti-pattern | Why it's forbidden |
|---|---|
| **Gamification** (points, XP, levels) | Trivializes life-changing decisions; unprofessional; corrupts evidence with game-incentives. |
| **Leaderboards / badges / streaks / achievements** | Consumer-engagement mechanics that cheapen a serious instrument and pressure candidates. |
| **Fake urgency** ("act now," countdowns) | Manipulative; degrades decision quality; violates helpful-without-controlling (§3.9). |
| **Dark patterns** (hidden exits, coercive defaults, forced paths) | Directly violate P7 and trust (P8); antithetical to our entire posture. |
| **Attention traps** (engagement-maximizing notifications, infinite feeds) | We optimize decisions, not time-on-app (Non-Goal, DOC-05 A-05.2 §A4). |
| **AI hype** (✨/🤖 badges, "magic," model name-drops) | Commoditizes us, invites distrust, distracts from hiring quality (§7, P6). |
| **Flashy dashboards / 80-metric walls** | Destroy calm (§3.1) and cognitive economy (§8); vanity over decision-support. |
| **Vanity metrics** (numbers that impress but don't help a decision) | Violate Decision-Centric Design (§4); noise masquerading as insight. |
| **Confusing Confidence with certainty** | Dishonest (§3.4); a legal and trust liability; misrepresents the system's own knowledge. |
| **Leading with the score** (evidence-last) | Violates Evidence-First (§5); trains black-box trust — the thing we exist to kill. |
| **Hidden AI** (concealing that AI was involved) | The *opposite* failure from hype — violates honesty/disclosure (§7); breaks P1/P13. |
| **Humiliating rejection** | Violates respect (§3.3) and P7; destroys the Candidate Afterlife and our reputation. |

> If a proposed experience appears on this list, it is not a debate — it is a **no.** Amending this list requires the Constitution Lifecycle process (DOC-05 A-05.2 §A5).

---

## 12. Product Review Checklist

Every new feature/surface must answer **yes** to these before approval. A "no" is a blocker, not a suggestion.

**Purpose & decision**
1. **What ONE decision does this help, and whose?** (If none → it should not exist. §4)
2. Does it earn its place, or is it decoration/vanity?

**Feeling**
3. What is the *intended feeling* here, and does the design produce it? (§2, §3)
4. Is it **calm** — one question, one primary action, no metric-wall? (§3.1, §8)
5. Is it **respectful** to everyone it touches, *especially rejected candidates*? (§3.3)
5a. **Fear:** what is this persona afraid of here, and does this *reduce* that fear? (A6)
5b. **Emotional transition:** does this *move* the user toward a better state — toward **relief** — not merely inform? (A2, A3)
5c. **Trust rung:** which Trust-Ladder rung is this user on, and does this design serve *that* rung (not one they haven't climbed)? (A4)

**Evidence & honesty**
6. Is it **evidence-first** — Evidence → Explanation → Recommendation → Score, never reversed? (§5)
7. Does it express **Confidence honestly** and never fake certainty? (§3.4, §11)
8. Is the explanation **audience-appropriate** (Progressive Explainability)? (§6)

**AI posture**
9. Does it **avoid AI hype** *and* **honestly disclose** AI where required? (invisible, not hidden — §7)

**Load & flow**
10. One primary action? Clear next step? No dead end? Undo where sensible? (§8)
11. Defaults over required configuration? Progressive disclosure? (§8)

**Fairness & access**
12. Is it **accessible** (not color-only, keyboard-operable, readable, fast)? (§9)
13. Does it *feel* fair and consistent across candidates? (§3.7)

**Voice & integrity**
14. Is the **tone** professional, precise, respectful, non-manipulative? (§10)
15. Does it avoid **every** anti-pattern in §11?

**Failure, waiting & silence** *(A-06.3)*
15a. **Failure:** if this fails, is the experience calm, clear, blameless, dignity-preserving, and recoverable — and does it never bias a result? (A7)
15b. **Waiting:** if this involves waiting, does the user always know where they stand and what's next — never a black hole? (A8)
15c. **Silence:** does any interruption/notification here clear the "worth breaking focus?" bar — or should the product stay silent? (A9)

**Trust (the meta-question)**
16. **Does this deposit trust or withdraw it?** If it withdraws trust for any short-term gain, it fails — trust is the moat. (P8)

---

## 13. Summary

### 13.1 What this establishes
- The **experiential constitution**: how every user must *feel* (calm, earned confidence; understood; fairly treated; respected), and what they must never feel.
- Seven experiential pillars: **Decision-Centric** (§4), **Evidence-First** (§5), **Progressive Explainability** (§6), **Invisible-not-Hidden AI** (§7), **Low Cognitive Load** (§8), **Accessibility-as-quality** (§9), and a disciplined **Tone & Voice** (§10).
- A **closed anti-pattern list** (§11) and a **16-point review checklist** (§12) that operationalize the manifesto into every feature decision.

### 13.2 Key decisions recorded
- **KD-06.1** — The product's unit of design is the **feeling of a trustworthy decision**, not the interface; the experience is the delivery mechanism for the Trust moat.
- **KD-06.2** — **Evidence-First order is sacred:** Evidence → Explanation → Recommendation → Score, never reversed.
- **KD-06.3** — **Invisible AI = invisible, not hidden:** zero hype, honest disclosure. AI is infrastructure; hiring quality is the story.
- **KD-06.4** — **Decision-Centric Design:** every screen supports exactly one decision or is deleted.
- **KD-06.5** — **Accessibility is product quality**, framed as fairness, not compliance.
- **KD-06.6** — A **closed experience anti-pattern list** (gamification, dark patterns, AI hype, vanity metrics, evidence-last, humiliating rejection, hidden AI…) — forbidden, amendable only via the Constitution Lifecycle.
- **KD-06.7** — Every feature must pass the **Product Review Checklist** (§12, expanded by A-06.2); question 16 (does this deposit or withdraw trust?) is decisive.
- **KD-06.8** — **Honest by Default:** AI disclosure is a *trust* test, not a legal one — "would a reasonable user feel misled if they learned later?"; disclose plainly if yes, don't force emphasis if no. (A-06.2 §A1.)
- **KD-06.9** — **Relief over Delight:** we optimize for *relief* ("Finally…"), the infrastructure emotion, not consumer *delight*. Relief creates trust; delight creates novelty. (A-06.2 §A2.)
- **KD-06.10** — **Emotional Journeys:** the product intentionally *moves* each persona from an entering state to an earned one (e.g., recruiter Overwhelmed→Defensible; candidate Curiosity→Growth). Design transitions, not static states. (A-06.2 §A3.)
- **KD-06.11** — **Trust Ladder:** trust is climbed in five rungs (it works → explanations make sense → predictions prove correct → recruiter depends → org trusts); design for the user's current rung. (A-06.2 §A4.)
- **KD-06.12** — **First Five Minutes:** a new customer must feel "I already understand this" within minutes; time-to-first-relief is a first-class metric. (A-06.2 §A5.)
- **KD-06.13** — **Remove Fear** is a design principle: name and reduce each persona's fear as the precondition for trust. (A-06.2 §A6.)
- **KD-06.14** — **Error Philosophy:** failure must never create panic or blame, must increase clarity, must preserve dignity and work, must never bias a result, and must be honest. (A-06.3 §A7.)
- **KD-06.15** — **Waiting Philosophy:** waiting is a designed state — communicated, honest about time, never a black hole; the user always knows where they stand and what's next. (A-06.3 §A8.)
- **KD-06.16** — **Silence Philosophy:** default to silence; interrupt only to serve the decision, never engagement; speak at meaningful events, be quiet otherwise. (A-06.3 §A9.)

### 13.3 Open questions (for founder/CTO & Design)

**Resolved by Amendment A-06.2 (CTO, 2026-07-21):**
- ~~Q1 AI-disclosure~~ → **Resolved: Honest by Default (A-06.2 §A1)** — trust test, not legal; plain disclosure where a user would feel misled otherwise.
- ~~Q3 "Delight"~~ → **Resolved: Relief over Delight (A-06.2 §A2)** — warmth is expressed as relief/respect/usefulness, never cheerfulness or gamification.

**Still open:**
1. **Product voice ownership:** who owns and guards the tone/voice standard (§10) and the emotional-journey intent (A3) as the team scales — a design-writing/experience function? *(Recommend: yes, eventually.)*
2. **Rejection-experience depth:** how much learning/feedback do we invest in the candidate rejection experience (Acceptance→Growth, A3) at V1 vs. later? (Ethics vs. scope; ties to P7 and Candidate Afterlife.)
3. **First-relief instrumentation:** how do we *measure* "time-to-first-relief" (A5) without it degrading into a vanity metric? *(Defer to metrics work; principle stands.)*

### 13.4 Suggested next document
**DOC-07 — Product Philosophy** — per the revised roadmap. With *what every user should feel* now fixed (this manifesto), DOC-07 defines *what we believe* about product — the convictions (evidence over artifacts, depth over breadth, opinionated defaults, the product's point of view) that, together with this manifesto and the Constitution, fully govern product before we ever profile a user (DOC-08 Personas).

**Revised, ratified roadmap:**
> 01 Vision · 02 Problem · 03 Business Strategy · 04 Domain Model · 05 Constitution · **06 Product Design Manifesto** · 07 Product Philosophy · 08 Personas · 09 Jobs-To-Be-Done · 10 Customer Journey · 11 Functional Requirements · 12 Non-Functional Requirements · 13 AI Strategy · 14 Evaluation Engine · 15 Architecture · 16 Engineering Principles.
> *(Personas and JTBD are now separate documents — personas = who the users are; JTBD = why they "hire" the product.)*

---

*End of DOC-06 v0.1. This is the experiential constitution — the intended feeling of using the platform, meant to guide UX for the next decade. Awaiting founder review of the four open questions (§13.3) before promotion to Ratified.*
