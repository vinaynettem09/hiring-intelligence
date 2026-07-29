# Document 11 — Customer Journey

| Field | Value |
|---|---|
| **Document ID** | DOC-11 |
| **Title** | Customer Journey (Front-stage Experience Over Time) |
| **Owner** | Principal Engineer / Technical Documentation Lead (with Product, Design, CS) |
| **Status** | Draft v0.1 — for founder review |
| **Created** | 2026-07-21 |
| **Depends on** | DOC-06 (Manifesto: emotional journeys, relief, waiting, error), DOC-08 (Personas), DOC-09 (JTBD: Trust/Success Moments, TTTM), DOC-10 (Service Blueprint) |
| **Blocks** | DOC-12 (Capability Map), and the **design-partner validation program** (this + DOC-10 are what we walk partners through) |
| **Relationship to DOC-10** | The Service Blueprint answered *what must happen behind the scenes.* This answers **what the human actually experiences, and feels, over time.** Blueprint = structure; Journey = emotion. |
| **Scope discipline** | **Experience and emotion only.** No implementation, no orchestration, no screens/wireframes, no architecture — those live in the Blueprint (DOC-10) and Architecture (DOC-17). If a sentence describes *how it works* rather than *how it feels*, it belongs elsewhere. |
| **Vocabulary** | Uses DOC-04 frozen terms exactly. Introduces **no** new business terms. |

---

## How to read this document

A journey is not a flow chart of clicks; it is the **emotional arc a real person lives** as they move through hiring with us. We use the tools already established: the **emotional journeys** (DOC-06 A3), the **Trust Moment / Success Moment** (DOC-09), and the **Time-to-Trust-Moment** targets (DOC-09 A-3). Three additions the CTO required make it operational:

- **Moments That Matter** — the 3–5 moments in each journey that *determine trust*. They deserve disproportionate design effort; everything else is supporting cast.
- **Emotional Debt** — trust *erodes over time* when people are left waiting, confused, or unacknowledged. Like technical debt, it accrues silently and must be paid down — or it compounds into churn.
- **Recovery Moments** — how the experience *regains* trust after something goes wrong (a cancellation, a delay, a wrong call). Prevention is better, but recovery is a designed capability, not an apology.

**Structure:** **Part 1** — the shared hiring timeline (context: one hire, everyone appears). **Part 2** — deep per-persona journeys (emotion). Then Emotional Debt and Recovery Moments apply across all.

---

## Part 1 — The Shared Hiring Timeline

One hiring event, all actors visible. This is the *context* within which each persona's private emotional journey unfolds. (The back-stage capabilities behind each beat are in DOC-10; here we show only who is present and how they feel.)

```
TIME →   Role Created   Candidate    Recruiter    Manager      Decision     Offer /       Outcome      Learning
                        Applies      Reviews      Reviews                   Rejection                  (invisible)
─────────────────────────────────────────────────────────────────────────────────────────────────────────────
David    defines the   —            (trusts the  reviews       makes the    —             lives with   (his bar
(HM)     bar; hopeful               shortlist?)  finalists;    call;                      the hire     sharpens)
                                                  calibrated    accountable
Rina     opens the     —            reviews      hands over    supports;    communicates  —            (shortlist
(TA)     req; sets up               evidence-    a shortlist   defensible   with dignity               quality
                                    first;        she trusts                                            proven)
                                    confident
Alex     —             applies as   (waiting —   (waiting —    (waiting)    hears back    onboarded /  (evidence
(Cand.)                he always     the black    trust at                   fairly, w/    or in         may travel
                       does;         hole risk!)  stake)                     feedback      afterlife     w/ consent)
                       informed
Sofia    —             —            —            —            (assured      —             quality      can defend
(CHRO)                                            it's fair)                                trends up    to board
Marcus   (verified     —            —            —            (audit        —             —            (zero
(Sec)    safe pre-req)                            trail intact)                                          incidents)
```

- **What the timeline reveals:** the personas are *interdependent in time* (David's bar precedes Rina's review precedes the decision precedes Alex's outcome) — and **Alex spends most of the timeline *waiting*** (the highest emotional-debt risk, §Emotional Debt). The shared view is why we design the *handoffs* (David→Rina→decision→Alex) as carefully as the steps.
- **Where the moments cluster:** the decision and the *communication back to Alex* are the highest-stakes beats for trust across the whole system.

---

## Part 2 — Deep Persona Journeys

*Each: the arc (feeling over time), the Moments That Matter, and where the Trust & Success Moments land. Emotion-first; mechanics are in DOC-10.*

### J-1 — Alex (Candidate) — *the mission's journey, told in full*

**Product boundary (KD-12.7):** discovery and *applying* happen in the **customer's own ATS/careers site — outside our product.** **Our journey begins when Alex receives the Evaluation Invitation:** `Applied through Company ATS (outside us) → Receives Evaluation Invitation → Completes Evaluation → [outcome] → Feedback/Afterlife`.

**Arc (within our boundary):** `(pre-context: applied in the company's ATS) → Invitation: Hope → Nervousness → Focus → Reflection → [outcome] → Acceptance → Growth` (DOC-06 A3).

**The narrative.** Alex has **already applied in the company's own ATS** (however they normally do — P11; we neither own nor change that step). **Our story starts with the Evaluation Invitation:** it arrives promptly, honestly discloses that AI-assisted analysis is part of the process (A1), and signals the evaluation is about *ability* — so their existing hope doesn't curdle into black-hole dread. Engaging the evaluation, initial **nervousness** resolves into **focus** because the task is clear, calm, and about what they can *do*. Afterward, **reflection**: they feel *understood*, not processed — *whatever the outcome.* Then the outcome, and either handoff to the company's offer process or — for the majority — a rejection that lands as **fair**, with useful, evidence-based feedback, moving them toward **acceptance** and genuine **growth**, remaining a respected participant in the network (Afterlife).

**Moments That Matter (5):**
1. **Evaluation Invitation received** *(having already applied in the company's ATS — our first touch)* — prompt, clear, honest. This is the first signal *we* control; done right = hope; done poorly/slow = the black hole begins. *(Highest leverage; cheapest to get right.)*
2. **Honest AI disclosure** — "this includes automated analysis with human review" (Honest by Default, DOC-06 A1). Sets the trust frame at first contact.
3. **The evaluation itself** — does it *feel* fair and about ability? This is where "I had a fair chance" is won or lost.
4. **The decision moment** — dignity, timeliness, no ghosting.
5. **Rejection feedback** — *the single most defining moment for our brand and network.* "Not the strongest match for this role," with real, useful evidence-based feedback — never "not good enough," never silence.

- **Trust Moment:** the evaluation *feels* fair + AI honestly disclosed + (even in rejection) respectful, useful feedback. **TTTM: immediate** (first application) — Alex cannot be asked to wait for trust (DOC-09 A-3).
- **Success Moment:** *"I had a fair chance"* — said **even when rejected.**

### J-2 — Rina (Head of TA)

**Arc:** `Overwhelmed → Organized → Confident → Certain → Defensible` (DOC-06 A3).

**The narrative.** Rina arrives **overwhelmed** by application volume and weak signal. The product cuts the noise — she feels **organized**. Seeing evidence-first Recommendations she can understand, she grows **confident**; repeating that reasoning to David and having it hold up, she becomes **certain**; able to produce the evidence trail on demand, she feels **defensible.**

**Moments That Matter (4):**
1. **First shortlist** — the noise-to-signal moment; her first taste of relief. *(TTTM target: within week 1.)*
2. **First time she defends a shortlist to David** — and he accepts it. The conversion.
3. **First challenge** — someone questions a pick and she *has the evidence.* Trust cements.
4. **Renewal-season reflection** — "I can't imagine going back." (Dependence — Trust Ladder rung 4.)

- **Trust Moment:** David accepts her evidence-based shortlist without re-screening.
- **Success Moment:** *"Finally — I can defend my shortlist."*

### J-3 — David (VP Engineering / Hiring Manager)

**Arc:** `Uncertain → Calibrated → Confident → Accountable` (DOC-06 A3). *(The hardest skeptic.)*

**The narrative.** David is **uncertain** — he distrusts funnels and re-screens everything. Capturing his real bar, he feels **calibrated** — "it understands how *I* hire." Seeing evidence that survives his technical scrutiny, and a recommended finalist who proves strong in his *own* interview, he grows **confident.** Owning the final call with full understanding, he feels **accountable** — not managed by a tool.

**Moments That Matter (4):**
1. **Calibration capture** — does it get *his* bar, or a generic one? Make-or-break for a skeptic.
2. **First recommended finalist he interviews** — does the evidence hold up live? The technical trust test.
3. **The debrief** — structured evidence vs. gut/memory; a *better* decision than he'd have made alone.
4. **Six months later** — no regret. (The delayed, decisive validation.)

- **Trust Moment:** a recommended candidate proves genuinely strong in his own interview — *repeatedly.*
- **Success Moment:** *"No regret after six months"* → *"I stopped re-screening."* **TTTM: first hiring cycle** (weeks).

### J-4 — Sofia (CHRO)

**Arc:** `Exposed / Skeptical → Informed → Assured → In Command` (DOC-06 A3).

**The narrative.** Sofia feels **exposed** — accountable for fairness she can't see. Shown the fairness posture, audit trail, and a respectful candidate experience, she becomes **informed**; realizing she could *defend all of it*, she feels **assured**; watching quality-of-hire trend up and risk trend down, she feels **in command.**

**Moments That Matter (3):**
1. **First fairness/defensibility review** — can she actually see and trust it?
2. **First board-ready report** — can she tell the hiring story with confidence? *(TTTM: first quarter.)*
3. **A challenge that doesn't materialize into a crisis** — a candidate complaint or audit that the evidence trail cleanly answers. Deep trust.

- **Trust Moment:** she sees the fairness posture + audit trail + respectful candidate experience and realizes she can defend it.
- **Success Moment:** *"I can defend our hiring to the board."*

### J-5 — Marcus (Head of IT & Security)

**Arc:** `Blind / Anxious → Sighted → In Control → Audit-Ready` (DOC-06 A3). *(Gatekeeper; must trust pre-purchase.)*

**The narrative.** Marcus starts **blind/anxious** — a new vendor is risk. Given a verifiable isolation model and clean boundaries, he becomes **sighted**; passing his review, **in control**; with complete audit visibility, **audit-ready.**

**Moments That Matter (3):**
1. **The security review** — can he *verify* isolation and data flows? The gate. *(TTTM: pre-purchase — trust must be earned before the deal.)*
2. **First integration** — clean and bounded, or a mess?
3. **First year, zero incidents** — quiet validation.

- **Trust Moment:** the isolation model and data flows are verifiable and pass his review.
- **Success Moment:** *"I verified it can't hurt us"* → zero incidents.

---

## Part 3 — Emotional Debt

> **Emotional Debt: trust erodes over time when people are left waiting, confused, unacknowledged, or over-interrupted — and, like technical debt, it accrues silently and compounds until it causes failure (abandonment, churn, brand damage).** A functionally correct outcome does not automatically repay it.

- **How it accrues:**
  - **Unexplained waiting** — the black hole (DOC-06 A8). *The single largest source, especially for Alex.* Every silent day adds debt.
  - **Confusion** — a screen that raises "what now?" (violates cognitive-load principles, DOC-06 §8).
  - **Broken promises** — "you'll hear back Friday" and silence on Friday.
  - **Owed-communication silence** — being quiet at a moment that demanded a word (the wrong side of Silence Philosophy, DOC-06 A9).
  - **Over-interruption** — needless notifications (the *other* wrong side of Silence).
- **The compounding nature (the CTO's key point):** *"Candidate waits 14 days without update — even if eventually hired, trust decreases."* Emotional debt taken on early is **partially unrepayable**: a candidate hired after a black-hole experience joins already distrusting how the company hires. Debt against Alex also leaks into the network (brand, referrals, the Afterlife).
- **How it's paid down:** proactive honest communication *before* the person has to ask (DOC-06 A8); acknowledgment; dignity; Recovery Moments (Part 4). But **prevention ≫ repayment** — some debt (a humiliating rejection, DOC-06 §11) is effectively permanent.
- **The principle:** we track and *budget* emotional debt the way we budget complexity (DOC-07 §A-1). Every design that saves us effort by making the user wait or guess is **borrowing against trust** — and trust is the moat. A journey is healthy only if its emotional debt stays near zero.

---

## Part 4 — Recovery Moments

Things will go wrong. **Recovery is a designed experience, not an apology.** Each recovery play regains trust by honoring the Error Philosophy (DOC-06 A7: no panic, increase clarity, no blame, preserve dignity) — and becomes explicit **Customer Success guidance.**

| What went wrong | Trust threat | The recovery play (experience) |
|---|---|---|
| **Interview cancelled / interrupted** | "I'm being messed around; my effort was wasted." | Immediate, blameless acknowledgment; progress preserved; effortless reschedule; explicit reassurance *it won't count against them* (DOC-06 A7). |
| **Delay / long wait** | Emotional debt accruing; the black hole. | **Proactive** honest update *before* they ask; a real reason and a new horizon; never fake progress (DOC-06 A8). |
| **False negative** (a strong candidate wrongly rejected) | "The system is unfair and I have no recourse." | A clear **appeal / re-review** path; a human re-examines with fresh eyes; humility, not defensiveness. Ties to the Evaluation "Contested/Reviewed" state (DOC-04 §6.3) and Human Accountability (P2). |
| **False positive** (a weak candidate advanced) | Hiring manager's trust erodes ("it's shallow"). | Transparent about the miss; use it as Outcome-Learning signal; show the calibration/memory adjustment. Never hide it. |
| **Appeal / dispute** | "No one will listen." | A real, respectful channel to question a decision, with an evidence-based, human response — not a form into a void. |
| **A wrong or confusing communication** | "I can't trust what they tell me." | Correct it plainly and quickly; acknowledge the confusion; restore clarity (DOC-06 A7 law 2). |

- **The recovery principle:** a well-handled recovery can leave trust *higher* than if nothing had gone wrong — because the user learns *how we behave under stress.* This is the Error Philosophy's promise realized at the journey level, and it is core CS doctrine.
- **But:** recovery is the safety net, not the plan. A journey that relies on recovery is a journey accruing emotional debt by design. Prevent first; recover gracefully second.

---

## 5. Summary

### 5.1 What this establishes
- A **shared hiring timeline** (context: all personas, interdependent in time) and **five deep per-persona journeys** (emotion), each with its arc, Trust Moment, Success Moment, and TTTM.
- **Moments That Matter** (3–5 per persona) — the trust-determining moments that earn disproportionate design effort; for Alex, *rejection feedback* is the most defining.
- **Emotional Debt** — trust erodes with waiting/confusion/silence; it compounds like technical debt, is partially unrepayable, and must be budgeted (prevention ≫ repayment).
- **Recovery Moments** — designed trust-recovery plays for cancellations, delays, false negatives/positives, appeals, and bad communications — core CS doctrine.

### 5.2 Key decisions recorded
- **KD-11.1** — The journey is documented in **both** views: a **shared timeline** (context) and **deep per-persona journeys** (emotion). Neither alone suffices.
- **KD-11.2** — Every journey has **3–5 Moments That Matter** that determine trust and receive disproportionate design effort; **Alex's rejection-feedback moment is the most brand-defining.**
- **KD-11.3** — **Emotional Debt is a first-class concept**, budgeted like complexity; waiting/confusion/owed-silence borrow against trust (the moat), and some debt is unrepayable — *prevention over recovery.*
- **KD-11.4** — **Recovery Moments are designed, not improvised**; a great recovery can raise trust above baseline (Error Philosophy at journey scale) and is core Customer Success doctrine.
- **KD-11.5** — **TTTM is asymmetric across personas** (Alex/Marcus immediate/pre-purchase; Rina days; David a cycle; Sofia a quarter) — journeys are paced accordingly.

### 5.3 Open questions (for founder/CTO — many are now *validation* questions)
1. **Do the predicted arcs hold with real people?** Does Alex actually reach "I had a fair chance" — *especially when rejected*? This is the central journey hypothesis to validate with candidates.
2. **Is Rina's TTTM really "days"?** If the first shortlist takes weeks to trust, the champion motion breaks (validate with design-partner recruiters).
3. **Emotional-debt measurement:** can we measure accruing emotional debt (e.g., candidate sentiment vs. wait time) without it becoming a vanity metric?
4. **Recovery-path scope at V1:** which Recovery Moments (esp. candidate appeal/re-review) ship at launch vs. later? (Scope + fairness call — ties P1/P2.)

### 5.4 Suggested next document
**DOC-12 — Capability Map** (now **required**, per CTO): Capability → Business Service → System → Microservice. It takes the business-capability inventory + Capability Register (DOC-10 §5, A-10.2 §A-5) and bridges it toward architecture — so that **architecture implements capabilities, not documents.** After DOC-12, per the plan, we **pivot to the design-partner validation program**, armed with DOC-10 (behind the scenes) and DOC-11 (what they experience) as the artifacts we walk partners through.

**Roadmap position:** …10 Service Blueprint · **11 Customer Journey** · → **12 Capability Map (required)** · 13 Functional · 14 NFRs · 15 AI Strategy · 16 Evaluation Engine · 17 Architecture · 18 Engineering Principles.

---

*End of DOC-11 v0.1 — experience and emotion only. Awaiting founder review of the four open questions (§5.3), several of which are now questions for real customers, not for us.*
