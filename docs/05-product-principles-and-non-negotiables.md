# Document 05 — Product Principles & Non-Negotiables (The Constitution)

| Field | Value |
|---|---|
| **Document ID** | DOC-05 |
| **Title** | Product Principles & Non-Negotiables (The Constitution) |
| **Status** | v0.2 — **Amendment A-05.2 ratified: Human Accountability Framework (reframes P2), Progressive Explainability (new P13), Constitutional Interpretation, Non-Goals, Constitution Lifecycle** |
| **Owner** | Principal Engineer / Technical Documentation Lead (with CTO) |
| **Created** | 2026-07-21 |
| **Depends on** | DOC-01 (Vision + A-0.2), DOC-02 (Problem), DOC-03 (Business Strategy + KD-03.10–14), **DOC-04 (Domain Model — frozen vocabulary)** |
| **Blocks** | DOC-06 (Personas) and every downstream product/engineering/design/GTM decision |
| **Nature** | **An operational decision framework, not a values poster.** Every principle is written to *decide real trade-offs*, per the CTO's directive: statement · why · decisions it enables · decisions it rejects · trade-offs · exceptions · conflict priority. |
| **Vocabulary** | All terms are used as defined and **frozen** in DOC-04. This document introduces **no** new business terms. |

---

## How to read this document — the Constitution is a decision tool

This is the company's constitution: the fixed rules every future decision must obey, and — crucially — the **tie-breaker** for when two good rules conflict. It exists so that a product manager, an engineer, a designer, an account executive, and a founder, facing the same trade-off independently, reach the **same** decision without escalation.

Three things make this operational rather than decorative:

1. **Every principle names the decisions it *rejects*, not just the ones it enables.** A principle that never says "no" is a slogan.
2. **Every principle has an explicit priority.** When principles collide (they will), the priority ladder (§2) is deterministic — there is always a defined winner.
3. **Exceptions are named and bounded.** Some principles admit *no* exceptions (the Gates); others admit narrow, documented ones. "It depends" is not allowed to be silent.

> **How to use it in a real decision** (see §4 for the full protocol): identify which principles the decision touches → if a Tier-0 Gate is implicated, it wins, full stop → otherwise apply the highest-tier principle in play → document the call and any exception. If two principles in the *same* tier conflict, the tie-break rule in §4 applies.

---

## Amendment A-05.2 — Human Accountability, Progressive Explainability, Interpretation, Non-Goals & Lifecycle

*Dated 2026-07-21. CTO-ratified. This amendment is authoritative where it differs from the original text. It (1) reframes **P2** from "Human-in-the-Loop" to a **Human Accountability Framework**, (2) adds a new Tier-0 principle **P13 — Progressive Explainability**, (3) adds **Constitutional Interpretation** (§A3), (4) adds an explicit **Non-Goals** section (§A4), and (5) adds a **Constitution Lifecycle** section (§A5). It also resolves both open questions from §7 and triggers a lockstep amendment to DOC-04 (INV-1, DC-7) for consistency. This remains a governance document — no implementation detail.*

### A1 — P2 (reframed) — Human Accountability Framework *(Tier 0 · Absolute Gate)*
*Supersedes the original "The human makes the decision (Human-in-the-Loop)". The stub at §3/P2 points here.*

- **Statement.** Humans are **accountable** for hiring decisions and for the **decision policies** that govern them. Automation may *assist and execute* within an approved governance framework, with **oversight proportional to decision risk.** High-impact decisions require **direct human review**; routine low-risk decisions may be automated **only** where policy, fairness (P1), Progressive Explainability (P13), and auditability remain fully intact. **The company rejects "human click theater" in favor of meaningful human oversight.**
- **Why it exists.** Regulators increasingly demand *meaningful* human oversight, not a rubber-stamp click; blanket "a human reviews every rejection" is neither scalable (100,000-applicant funnels) nor genuinely protective. Accountability for *policy + high-impact decisions* is both more honest and more defensible than mechanical click-through. (Refines DOC-01 non-goal on autonomous decisions; DOC-04 INV-1/DC-7 amended to match.)
- **Risk-proportional oversight model** *(the operative rule)*:

  | Decision risk | Example | Required human involvement |
  |---|---|---|
  | **Low** | Candidate clearly does not meet hard, role-relevant, bias-audited criteria | Automated workflow permitted **within approved policy** (fairness + explainability + audit intact) |
  | **Medium** | Borderline / ambiguous evidence | **Recruiter** reviews |
  | **High** | Finalists / advance-to-offer | **Hiring Manager** reviews |
  | **Very High** | Executive / senior leadership hiring | **Panel** reviews |

- **Decisions it enables.** Automating clearly-out-of-policy, low-risk screening steps at scale (with audit trails); focusing scarce human attention on borderline and high-impact decisions; making humans own the *policy* and the *thresholds*; treating overrides as Outcome-Learning signal.
- **Decisions it rejects.** "Human click theater" (a person rubber-stamps thousands of decisions they cannot meaningfully review); *fully* autonomous high-impact decisions (finalists/executives without human review); automation of *any* decision where fairness, explainability, or auditability is not intact; marketing "AI that hires for you."
- **Trade-offs.** Requires a rigorous, auditable **decision-policy and risk-tiering mechanism** (defined later — AI Strategy / Evaluation Engine / Compliance, see §A3), which is more complex than either "always human" or "always automated." We accept this complexity as the price of *meaningful* oversight.
- **Exceptions.** No exception to **human accountability for policy** and to **human review of High/Very-High-risk decisions**. Low/Medium automation is *permitted-within-governance*, not an exception to the gate.
- **Conflict priority.** **Tier 0.** Beats Integration Ease (P11) and Velocity (P12). Automation convenience never overrides accountability, fairness, or explainability.

### A2 — P13 (new) — Progressive Explainability *(Tier 0 · companion to P1)*

- **Statement.** **Explainability is audience-aware.** Different stakeholders receive different *levels* of explanation appropriate to their role. **Transparency does not require exposing every internal mechanism.** We protect both fairness (everyone affected gets a meaningful, honest explanation) *and* our intellectual property / moat (internal calibration, weighting, anti-fraud, and proprietary intelligence stay protected).
- **Why it exists.** Resolves the real tension between P1 (fair & explainable), P7 (candidate as user, deserves feedback), P6 (sensors/intelligence are the product — don't hand over the method), and P3 (protect data/IP). Full transparency to everyone would leak the moat and aid gaming; opacity to everyone would violate fairness and law. Audience-appropriate explanation is the correct middle.
- **Audience matrix** *(what each audience receives / never receives)*:

  | Audience | Receives | Never receives |
  |---|---|---|
  | **Candidate** | Strengths; improvement areas; evidence-backed observations; a constructive learning roadmap | Internal hiring thresholds; Company Calibration; Benchmark formulas; anti-fraud/Integrity mechanisms; weighting/algorithm logic |
  | **Recruiter** | Full Recommendation; Confidence; Evaluation Score; Integrity Score; the Evidence; Benchmark | Cross-company data (P3); proprietary model internals |
  | **Hiring Manager** | Everything the Recruiter sees **+** Calibration alignment **+** Hiring Memory insights for their Role/team | Other companies' data; raw model internals |
  | **Executive** | Aggregate decision-quality, fairness/adverse-impact posture, pipeline & Benchmark health, ROI / quality-of-hire trends | Per-candidate internal mechanics (unless also acting as the Hiring Manager) |
  | **Compliance / Audit** | **Everything** — full evidence, reasoning, fairness tests, policy, and decision trail (full auditability) | — (nothing withheld from audit) |

- **Decisions it enables.** Giving rejected candidates genuinely useful, evidence-based feedback (serving P7) *without* exposing IP; tailoring explanations per surface/persona; full, unredacted auditability for compliance.
- **Decisions it rejects.** "Rejected." with no explanation (violates P1/P7); dumping full internal mechanics to candidates or competitors (violates P6/P3); a one-size explanation that either leaks the moat or starves fairness; withholding anything from *audit*.
- **Trade-offs.** Building multiple, role-appropriate explanation views is more work than one view; candidate-facing feedback must be carefully designed to be constructive yet non-exploitable.
- **Exceptions.** None to the *principle*. The *exact depth* per audience is an implementation matter for the Evaluation Engine / Fairness work (§A3) — but the commitments above are fixed.
- **Conflict priority.** **Tier 0, companion to P1.** P13 *refines* P1: P1 requires meaningful explanation; P13 defines to whom and how deep. Where P13 (limit exposure) meets P7 (candidate transparency), the matrix is the resolution — candidates always get constructive, evidence-based feedback; they never get internal mechanisms.

### A3 — Constitutional Interpretation

- **The Constitution defines *intent and principles* — the "what" and "why." It does not define *mechanism* — the "how."**
- **Implementation lives in later documents:** AI Strategy (DOC-11 in the revised roadmap), Evaluation Engine (DOC-12), Non-Functional Requirements (DOC-10), Security, and Compliance documents. Those documents specify *how* the principles are realized (e.g., *how* risk-tiering under P2 works, *how* Progressive Explainability is rendered per surface, *how* isolation under P3 is enforced).
- **Precedence.** When intent and mechanism appear to conflict: **the Constitution's principle governs the intent; the implementation must conform.** If an implementation seems to require violating a principle, the implementation is wrong and must change — or a formal Constitutional amendment (§A5) is required first. **Vocabulary always comes from DOC-04** (freeze discipline).
- **Reading rule.** No implementation document may quietly reinterpret a principle. If a later doc needs a principle to mean something new, it must trigger an amendment here, not redefine it locally.

### A4 — Non-Goals *(what we explicitly do NOT do)*

Stated plainly so no roadmap, deal, or feature can drift into them:

1. **We do not optimize for recruiter speed alone.** (Speed is Tier 5; decision quality is the product — P9.)
2. **We do not replace human judgment.** (Human Accountability — P2.)
3. **We do not maximize interview automation.** (Sensors are inputs, not the goal — P6; oversight is proportional — P2.)
4. **We do not become an ATS.** (P4.)
5. **We do not become a job board / portal.** (P4/P5.)
6. **We do not sell candidate data.** (P3/P7; KD-03.14.)
7. **We do not optimize for engagement at the expense of trust.** (Trust is Tier 2 — P8; no dark patterns — P7.)
8. **We do not become a system of record or own the Employee record.** (P4; Employee is reference-only — DOC-04 A-04.A4.) **Product Boundary (DOC-12 KD-12.7):** we are not responsible for job creation, job posting, sourcing, resume database, applicant tracking, offer management, or HR records; our responsibility **begins** when a candidate has already applied (and is imported) and **ends** when hiring intelligence is delivered back.
9. **We do not position or price "the AI interview" as the product.** (P6; KD-03.10/13.)
10. **We do not make autonomous High/Very-High-risk hiring decisions.** (P2.)
11. **We do not expose internal calibration, weighting, or anti-fraud mechanics to candidates or competitors.** (P13/P6.)

### A5 — Constitution Lifecycle *(governance only)*

- **How principles evolve.** Via versioned amendments (v0.2, v0.3…) with a dated changelog, exactly as DOC-01–04 amendments are handled. Each amendment states what changed, why, and any downstream documents that must change in lockstep.
- **Who may amend.**
  - **Tier 0 gates (P1, P2, P3, P13)** are effectively immutable: amending one changes the company's reason to exist and requires **founder + (eventually) board** sign-off with documented rationale.
  - **Tiers 1–5 (P4–P12)** may be amended with **CTO** sign-off and a changelog.
  - **New business vocabulary** never originates here — it must be added to **DOC-04** first (freeze discipline).
- **Review cadence.** Reviewed at each major company milestone (fundraise, market/segment expansion, major regulatory change) and **at least annually**. A regulatory shift affecting P1/P2/P3/P13 triggers an out-of-cycle review.
- **Versioning rules.** *Major* version = a change to a principle's meaning or the priority ladder; *minor* version = clarification, example, or wording that does not change intent. Every version is dated and attributed.
- **Backward compatibility.** Superseded principles/interpretations are **retained** with a *superseded-by* pointer (not deleted), mirroring DOC-04's deprecation model, so prior documents, APIs, and customer commitments remain interpretable. Prior versions are archived, never overwritten.
- **Scope guard.** This section governs *how the Constitution changes* — it introduces no implementation detail and no product mechanism.

### A6 — Roadmap update (ratified)
- **DOC-06 — Product Philosophy** is inserted **before** Personas (rationale: personas define *who* we build for; product philosophy defines *how everything should feel* — experience intent belongs before user profiling). Revised sequence: **01 Vision → 02 Problem → 03 Strategy → 04 Domain → 05 Constitution → 06 Product Philosophy → 07 Personas & JTBD → 08 User Journeys → 09 Functional Requirements → 10 NFRs → 11 AI Strategy → 12 Evaluation Engine → 13 Architecture.**
- **Engineering Principles** will be a **separate future document** (distinct from these Product Principles), in the spirit of Amazon/Google/Stripe/Datadog/Snowflake — covering build-for-observability, fail-safely, backward compatibility, "APIs are forever," immutable data, events-are-facts, security-by-default, etc. Placement TBD (likely alongside/after NFRs); flagged now so it isn't forgotten.

### A7 — Consistency actions triggered by this amendment
- **DOC-04 INV-1 and DC-7 amended (A-04.3)** to reflect Human Accountability (proportional automation within governance) instead of an absolute "never autonomous" reading.
- **§7 open questions RESOLVED:** rejection-explanation → Progressive Explainability (P13); human-in-the-loop granularity → Human Accountability Framework (P2, risk-tiered).

---

## 1. The two classes of principle

The principles divide into two classes, which behave differently:

- **Non-Negotiables (Gates & Identity, Tiers 0–1).** These are not traded, ranked against ROI, or "balanced." They either hold or we have violated the mission / become a different company. Some (Tier 0) admit **zero** exceptions.
- **Ranked Priorities (Tiers 2–5).** These are all genuinely good and frequently in tension; the ladder tells us which yields to which. This ranking is the ratified refinement of DOC-01 §9 (the fairness/explainability *gate* model) plus DOC-03's "Security & Trust first among rankables."

---

## 2. The Principle Hierarchy (the priority ladder at a glance)

When principles conflict, **higher tier wins.** Within a tier, apply §4's tie-break.

```
TIER 0 — ABSOLUTE GATES  (never traded · ZERO exceptions · a violation is disqualifying)
   P1  Fair & Explainable, or it doesn't ship
   P2  Human Accountability Framework   (reframed by A-05.2 — accountability & proportional oversight, not click-theater)
   P3  Guard candidate & company data like our own (Privacy · Consent · Isolation)
   P13 Progressive Explainability — audience-aware  (added by A-05.2; companion to P1)

TIER 1 — IDENTITY NON-NEGOTIABLES  (violating one means we became a different company)
   P4  We are infrastructure, never a system of record
   P5  Neutral by construction
   P6  Sensors are inputs; intelligence is the product
   P7  The candidate is a user, never inventory

TIER 2 — TRUST & SECURITY  (first among the rankable)
   P8  Trust is the company — protect it above growth

TIER 3 — DECISION QUALITY  (why the product exists)
   P9  Decision quality is the product
   P10 Build the compounding moat, not the demo (close the loop)

TIER 4 — INTEGRATION EASE
   P11 Never make anyone change how they work

TIER 5 — VELOCITY & SIMPLICITY  (win only when nothing above is at stake)
   P12 Earn trust fast, then compound — and speak one language
```

> **Mnemonic:** *Legal/ethical gates → who we are → trust → decision quality → fit into workflows → speed.* Speed never beats trust; trust never beats fairness.

---

## 3. The Principles

*Each principle follows the CTO's framework exactly: **Statement · Why it exists · Decisions it enables · Decisions it rejects · Trade-offs · Exceptions · Conflict priority.***

---

### TIER 0 — ABSOLUTE GATES

---

### P1 — Fair & Explainable, or it doesn't ship
- **Statement.** No Evaluation, Recommendation, Evaluation Score, or Benchmark is delivered unless (a) it carries the specific Evidence and reasoning behind it (Explainability) and (b) it has passed fairness / adverse-impact safeguards. A black-box or bias-unchecked output is not a lesser product — it is *not our product at all.*
- **Why it exists.** It is the mission (replace biased resume screening, DOC-02), the law in our markets (EEOC/Title VII adverse impact, NYC LL144, EU AI Act — DOC-02 §9), and the foundation of trust. It encodes DOC-01 §9's ratified gate and DOC-04 INV-2/INV-3.
- **Decisions it enables.** Investing in evidence-citation and adverse-impact testing before launch; refusing customers who demand opaque scoring; publishing our fairness methodology; building audit artifacts by default.
- **Decisions it rejects.** Shipping a higher-accuracy model we can't explain; "we'll add explainability later"; hiding reasoning as a trade secret; launching in a jurisdiction before we can meet its fairness bar.
- **Trade-offs.** May block a tempting accuracy gain; explainability and bias-testing cost engineering time and can slow launches. We accept this cost as the price of the category.
- **Exceptions.** **None. Zero. Ever.** This is the reason the company can exist.
- **Conflict priority.** **Tier 0 — beats everything,** including accuracy (P9), integration (P11), and speed (P12). If P1 and any other principle conflict, P1 wins and the decision stops there.

### P2 — Human Accountability Framework  *(reframed — see Amendment A-05.2 §A1, which is authoritative)*
> **This principle was reframed from the original "Human-in-the-Loop."** The full, authoritative statement — including the risk-proportional oversight model (Low/Medium/High/Very-High) and the rejection of "human click theater" — is in **Amendment A-05.2 §A1**. In brief: **humans are accountable for hiring decisions and decision policies; automation may execute within approved governance with oversight proportional to risk; High/Very-High-risk decisions require direct human review; and no automation is permitted where fairness, explainability, or auditability is compromised.** Tier 0.

### P13 — Progressive Explainability  *(new — see Amendment A-05.2 §A2, which is authoritative)*
> **Explainability is audience-aware.** Candidates receive constructive, evidence-based feedback and a learning roadmap; recruiters/hiring managers receive full recommendation, scores, evidence, benchmark (and, for HMs, calibration/memory insight); executives receive aggregates; compliance/audit receives everything. Internal calibration, weighting, anti-fraud, and proprietary intelligence are never exposed to candidates or competitors. Full statement and audience matrix in **A-05.2 §A2**. Tier 0, companion to P1.

### P3 — Guard candidate & company data like our own (Privacy · Consent · Isolation)
- **Statement.** Candidate Evidence is governed by consent and never sold (KD-03.14). One Company's Calibration, Hiring Memory, and Evidence are **never** exposed to another; only aggregate, anonymized Benchmarks cross the company boundary (DOC-04 INV-8, DC-6).
- **Why it exists.** Trust is the moat (DOC-03); a single leak or misuse is existential; regulatory necessity (privacy law, residency); ethical duty to candidates as users (P7).
- **Decisions it enables.** Consent-first data handling; strict per-Company isolation; aggregate-only benchmarking; data-residency-aware design for expansion (DOC-01 §5).
- **Decisions it rejects.** Selling or brokering candidate data; using Company A's memory to benefit Company B; benchmarks that could re-identify a person or company; retaining evidence beyond consented/retention limits.
- **Trade-offs.** Isolation and consent constrain some network features and add engineering complexity; we forgo data-monetization revenue lines.
- **Exceptions.** **None** on selling candidate data or cross-company leakage. (Aggregate, non-identifying network benchmarks are explicitly permitted — that is not an exception, it is the designed boundary.)
- **Conflict priority.** **Tier 0.** Beats Decision Quality (P9) and every revenue/velocity argument.

---

### TIER 1 — IDENTITY NON-NEGOTIABLES

---

### P4 — We are infrastructure, never a system of record
- **Statement.** We are Hiring Intelligence Infrastructure — the intelligence layer. We integrate with ATSs and HRIS; we never become an ATS, a job portal, or the owner of Requisitions/Offers/Employees (DOC-03 §10–11; DOC-04 INV-9, "reference-only" boundaries).
- **Why it exists.** Being a system of record destroys Neutrality (P5), traps us in the incumbents' innovator's dilemma, forces customer migration, and downgrades our valuation (DOC-03). It is the strategic core of the company.
- **Decisions it enables.** Referencing (not owning) requisitions/offers/employees; making every ATS smarter; building connectors, not storage.
- **Decisions it rejects.** "Let's just add applicant tracking / a job board / offer management"; owning the employee record; competing with Greenhouse/Workday on their turf.
- **Trade-offs.** We give up the stickiness and TAM of owning the system of record; we depend on integrating with systems we don't control.
- **Exceptions.** None in identity. (We may store *our own* intelligence artifacts — evidence, evaluations — that is being the intelligence layer, not becoming a system of record.)
- **Conflict priority.** **Tier 1.** Yields to Tier 0 gates; beats Tiers 2–5. A feature that would make us a system of record is rejected even if it improves trust/quality/speed.

### P5 — Neutral by construction
- **Statement.** We are neutral across systems of record and Sensors. We **partner by default** (LinkedIn, Workday, Greenhouse, Ashby, Lever) and **compete only on the intelligence layer, never on the system of record** (KD-03.12; DOC-04 DC-1).
- **Why it exists.** Neutrality is a position no ATS or platform giant can hold (DOC-03 §2) — it is our structural advantage and the basis of cross-system Benchmarking and trust.
- **Decisions it enables.** Integrating with every major ATS equally; refusing exclusivity that would compromise neutrality; being the customer's cross-platform source of truth.
- **Decisions it rejects.** An exclusive deal that ties us to one ATS; privileging one Sensor vendor for commercial reasons; features that only work if the customer abandons a competitor's system.
- **Trade-offs.** We may decline lucrative exclusive partnerships; neutrality requires maintaining many integrations (cost).
- **Exceptions.** Narrow and documented: *sequencing* (we can build the Greenhouse integration first) is fine — that is prioritization, not favoritism. A *permanent* exclusivity is not.
- **Conflict priority.** **Tier 1.** Yields to Tier 0; beats Tiers 2–5. Neutrality beats a bigger/faster deal.

### P6 — Sensors are inputs; intelligence is the product
- **Statement.** Interviews, Assessments, and all Sensors are interchangeable evidence-collection inputs. The product is Decision Quality via the intelligence layer — never "the AI interview" (DOC-03 §3; DOC-04 INV-10).
- **Why it exists.** Positioning a Sensor as the product invites commoditization and platform absorption (DOC-03 §24) and misaligns pricing (we bill per Candidate Evaluation, not per interview — KD-03.10).
- **Decisions it enables.** Staying Sensor-agnostic; adding/retiring sensors without changing our identity; pricing and marketing the *intelligence*, not the interview.
- **Decisions it rejects.** Marketing/selling "the AI interviewer" as the headline; betting the roadmap on one sensor; per-interview pricing; letting a sensor's UX define the company.
- **Trade-offs.** "AI interview" is easier to demo and sell than "hiring intelligence"; we sacrifice some early explanatory ease.
- **Exceptions.** Transitional messaging may *lead with* a tangible sensor for buyer comprehension (aligns with KD-03.13's "AI Hiring Intelligence Platform" external framing) — but never *price or architect* the sensor as the product.
- **Conflict priority.** **Tier 1.** Yields to Tier 0; beats Tiers 2–5.

### P7 — The candidate is a user, never inventory
- **Statement.** Candidates are first-class users of the network — served with transparency, feedback, fair treatment, and (long-term) Portable Evidence, including in the Candidate Afterlife. They are never attention/inventory to be monetized (KD-03.14; DOC-04 DC-5).
- **Why it exists.** Ethics, trust, and network growth (the afterlife is a growth vector, DOC-03 §18.4); it differentiates us from job-portal/attention models (P4/P5).
- **Decisions it enables.** Explaining rejections where feasible; letting candidates carry evidence (with consent); designing for candidate experience and re-engagement; treating the rejected majority as durable network value.
- **Decisions it rejects.** Selling candidate data; charging candidates for access to opportunities; treating candidates as leads to be resold; dark-pattern experiences.
- **Trade-offs.** Serving candidates costs money before it pays; some candidate-facing transparency may reveal method details we must manage carefully (balanced against P1, not against secrecy for its own sake).
- **Exceptions.** Future *optional* premium career services for candidates are permitted (KD-03.14) — opt-in, never coercive, never data-sale.
- **Conflict priority.** **Tier 1.** Yields to Tier 0 (esp. P3 privacy); beats Tiers 2–5. A revenue idea that treats candidates as inventory is rejected.

---

### TIER 2 — TRUST & SECURITY

---

### P8 — Trust is the company — protect it above growth
- **Statement.** Enterprise security, data protection, and reliability come before feature velocity and growth. When a choice risks trust, trust wins. (This is DOC-03's "Security & Trust first among rankables" and the Trust flywheel, §16.)
- **Why it exists.** In hiring AI a single breach or scandal is existential (DOC-02, DOC-03 §24 SR-6); trust is the asymmetric moat giants can't easily match. Trust compounds; it is slow to build and instant to lose.
- **Decisions it enables.** Investing early in security (SOC 2, isolation, auditability) ahead of flashy features; declining a fast growth tactic that risks a trust incident; conservative defaults.
- **Decisions it rejects.** "Ship now, harden later" on security; growth hacks that spam candidates or over-promise; cutting security review to hit a date.
- **Trade-offs.** Slower feature shipping and slower growth than a trust-careless competitor; higher upfront security cost.
- **Exceptions.** Narrow, time-boxed, documented (e.g., a design-partner sandbox with explicit consent and no real candidate data) — never in production with real data.
- **Conflict priority.** **Tier 2 — first among rankables.** Yields to Tier 0/1; **beats Decision Quality (P9), Integration (P11), and Velocity (P12).** A more accurate feature that weakens security loses to security.

---

### TIER 3 — DECISION QUALITY

---

### P9 — Decision quality is the product
- **Statement.** We optimize the **quality of the Hiring Decision** — evidence-backed, fair, explainable, predictive — not recruiter convenience, not speed, not raw activity. Evidence beats artifacts; the Resume never gates a decision (DOC-02; DOC-04 INV-4/INV-5; DOC-03 KD-03.7).
- **Why it exists.** It *is* the product and the North Star (evidence-backed decisions); it is what customers ultimately pay for and what compounds into the moat.
- **Decisions it enables.** Prioritizing features that measurably improve decisions; investing in Company Calibration and Hiring Memory; measuring evidence-reliance and (ultimately) quality-of-hire; saying no to "recruiters will like it but it doesn't improve the decision."
- **Decisions it rejects.** Optimizing time-to-hire/cost-per-hire *at the expense of* decision quality; resume-keyword shortcuts; convenience features that dilute evidence rigor; vanity metrics.
- **Trade-offs.** Harder to demo and measure than efficiency; sometimes a higher-quality path is slower or less convenient for the recruiter.
- **Exceptions.** None to the *definition* of the product. Prioritization may temporarily favor an efficiency feature for adoption, but never one that *degrades* decision quality.
- **Conflict priority.** **Tier 3.** Yields to Tier 0/1/2; **beats Integration Ease (P11) and Velocity (P12).** A deeper, better evaluation beats an easier integration or a faster ship — but never overrides a Gate or Trust.

### P10 — Build the compounding moat, not the demo (close the loop)
- **Statement.** Favor the compounding assets — Evidence Graph, Hiring Memory, Outcome Learning, Benchmarking, Trust — over one-off features and demo-shine. Close the loop: wherever Outcomes are available, feed them back (DOC-04 INV-12; DOC-03 §13, §17). **The moat is the system, not the LLM.**
- **Why it exists.** Durable advantage lives in compounding, network-earned assets, not in copyable features or model quality (DOC-03 §13); this is what survives the giants (SR-1/2).
- **Decisions it enables.** Investing in outcome-data pipelines and memory even when they don't demo well; choosing the architecture that compounds; prioritizing design-partner outcome-data access (DOC-03 §21).
- **Decisions it rejects.** Shipping a flashy feature that doesn't compound over a boring one that deepens memory/outcomes; betting the moat on a proprietary model; skipping the outcome loop because it's hard.
- **Trade-offs.** Compounding assets pay off *slowly*; early on they cost more than they visibly return; less demo dazzle.
- **Exceptions.** Early-stage: some non-compounding features are needed to win the first customers who *supply* the data that starts the flywheel — acceptable as a means to ignite compounding, not as the strategy.
- **Conflict priority.** **Tier 3** (with P9). Yields to Tier 0/1/2; beats Tiers 4–5. Within Tier 3, P9 (is the decision better?) leads; P10 (does it compound?) is the close second — see §4 tie-break.

---

### TIER 4 — INTEGRATION EASE

---

### P11 — Never make anyone change how they work
- **Statement.** The candidate applies as they always did; the recruiter works where they always worked. We meet every workflow where it is — ATS, no-ATS/email, API, webhook (DOC-01; DOC-03 §9). Integration depth is a core moat metric, not a services cost.
- **Why it exists.** Frictionless, migration-free adoption is how infrastructure spreads and how we avoid procurement death (DOC-03); embeddedness is switching cost.
- **Decisions it enables.** Building into existing ATS/email flows; landing via ATS marketplaces; low-friction onboarding; deep, maintained integrations.
- **Decisions it rejects.** Requiring customers to migrate or adopt a new system of record (also P4); candidate-facing friction that changes how they apply; "rip and replace" motions.
- **Trade-offs.** Supporting many integration modes is real, ongoing engineering and support cost; we sometimes accept a harder build to spare the customer change.
- **Exceptions.** When Integration Ease conflicts with Decision Quality (P9) or a Gate — e.g., a genuinely better evaluation needs a small new step — the higher tier wins, but we always seek the *least-intrusive* way to achieve it.
- **Conflict priority.** **Tier 4.** Yields to Tiers 0–3; **beats Velocity (P12).** Ease-of-integration loses to fairness, trust, and decision quality — but a smoother integration beats shipping faster-but-clunkier.

---

### TIER 5 — VELOCITY & SIMPLICITY

---

### P12 — Earn trust fast, then compound — and speak one language
- **Statement.** When (and only when) nothing higher is at stake, bias to shipping value quickly and simply: reduce time-to-value, prefer the simpler design, and **use the frozen DOC-04 vocabulary everywhere** (no new terms without amending DOC-04). Speed and simplicity are real goods — they are just the *lowest-priority* goods.
- **Why it exists.** Velocity compounds learning and revenue; simplicity reduces defects and cost; language discipline prevents drift (DOC-04 §11.2). But each must never override trust, quality, identity, or the gates.
- **Decisions it enables.** Cutting scope to ship a valuable slice sooner; choosing the simpler architecture when quality is equal; enforcing consistent terminology in docs/APIs/UI.
- **Decisions it rejects.** Speed that skips fairness/security (P1/P8) — forbidden; complexity for its own sake; inventing synonyms for DOC-04 terms; "move fast and break trust."
- **Trade-offs.** Prioritizing speed can accrue some product debt; simplicity can defer power features. Acceptable *only* when no higher principle is implicated.
- **Exceptions.** None needed — this tier *yields to everything*, so it is self-limiting.
- **Conflict priority.** **Tier 5 — lowest.** Yields to all other principles. Speed never wins a real conflict; it only decides when nothing above is at stake.

---

## 4. Conflict-Resolution Protocol

When a decision implicates more than one principle:

1. **Gate check (Tier 0).** Does the decision risk P1 (fair/explainable), P2 (human decides), or P3 (privacy/isolation)? If yes and it would violate any of them → **the decision is rejected outright.** Stop. No ROI argument reopens a Tier-0 gate.
2. **Identity check (Tier 1).** Would it make us a system of record (P4), break neutrality (P5), make a sensor the product (P6), or treat candidates as inventory (P7)? If yes → rejected, unless reframed to preserve identity.
3. **Apply the highest tier in play.** Among the remaining principles the decision touches, the highest tier wins (Trust P8 > Decision Quality P9/P10 > Integration P11 > Velocity P12).
4. **Same-tier tie-break.** If two principles in the *same* tier conflict:
   - Tier 3: **P9 (is the decision better?) leads P10 (does it compound?)** — quality of the decision first, then compounding value.
   - Otherwise: choose the option that best serves **Decision Quality (P9)**, since that is the product; document the reasoning.
5. **Document the decision and any exception.** Especially any Tier-2+ exception invoked — record what, why, scope, and expiry. Exceptions are visible, bounded, and reviewable; silent exceptions are forbidden.

### 4.1 Worked examples

| Situation | Principles in tension | Resolution |
|---|---|---|
| A customer offers a big contract if we enable **auto-reject** of low scorers to save recruiter time. | P2 (human decides, T0) vs P8/P11/P12 | **P2 wins. Declined.** No exception — Tier 0. We offer decision-support, not auto-reject. |
| A new model is **more accurate but not explainable**. | P9 (quality, T3) vs P1 (fair/explainable, T0) | **P1 wins.** Do not ship until explainable. Accuracy never beats the gate. |
| An ATS offers a lucrative **exclusive** partnership. | P5 (neutrality, T1) vs P8/P12 | **P5 wins.** Decline exclusivity; partner non-exclusively. Sequencing one integration first is fine; permanent exclusivity is not. |
| A deeper Evaluation needs **one extra candidate step** the ATS doesn't natively support. | P9 (quality, T3) vs P11 (integration ease, T4) | **P9 wins**, but implement the *least-intrusive* integration; never make the candidate change how they apply (P11 spirit preserved). |
| A revenue team proposes **selling anonymized-ish candidate data**. | P3/P7 (T0/T1) vs P12 | **P3/P7 win. Rejected.** Candidate data is never sold; only aggregate non-identifying Benchmarks are allowed. |
| We could **ship 3 weeks sooner** by skipping adverse-impact testing. | P12 (velocity, T5) vs P1 (T0) | **P1 wins.** Never. |
| A **flashy demo feature** vs a **boring outcome-loop investment** for the quarter. | P12/P9 vs P10 (compounding, T3) | If the demo feature doesn't improve decisions, **P10 wins** (build the moat). If it *ignites the data flywheel* by winning a data-supplying customer, that's P10's own early-stage exception — document it. |

---

## 5. How each function uses this Constitution

- **Product:** every spec cites the principles it serves and the ones it trades; roadmap prioritization uses the tier ladder.
- **Engineering:** architectural choices (DOC-12) must satisfy Tier-0 gates by construction (explainability, isolation, human-in-the-loop) — these are not features to add later.
- **Design:** candidate- and recruiter-facing flows embody P2 (human decides), P7 (candidate as user), and P1 (explainable to the person).
- **Sales & Marketing:** messaging obeys P6 (sell intelligence, not the sensor) and KD-03.13 naming; never promises auto-hiring (P2) or data resale (P3/P7); qualifies every score (DOC-04 A-04.A5).
- **Leadership:** uses the ladder to resolve cross-functional conflict without re-litigating values; approves and time-boxes exceptions.

---

## 6. Amendment Process

This Constitution can evolve, but not casually:
- **Tier 0 gates (P1–P3) are effectively immutable.** Changing one is changing the company's reason to exist; requires founder + (eventually) board sign-off and a documented rationale.
- **Tiers 1–5** may be amended via a versioned change (v0.2, v0.3…) with a changelog and CTO sign-off, exactly as DOC-01–04 amendments were handled.
- **No new business vocabulary** may enter here; terms come from (or are added to) DOC-04 first (freeze discipline, DOC-04 §11.2).

---

## 7. Open Questions

**Resolved by Amendment A-05.2 (CTO, 2026-07-21):**
- ~~Q1 Explaining rejections to candidates~~ → **Resolved: Progressive Explainability (P13)** — candidates get constructive, evidence-based feedback + learning roadmap; never internal mechanisms.
- ~~Q2 Human-in-the-loop granularity~~ → **Resolved: Human Accountability Framework (P2)** — risk-proportional oversight; no "human reviews every rejection"; humans accountable for policy + High/Very-High-risk decisions.

**Still open:**
1. **Exception log ownership:** Who owns and audits the exception log (§4.5) *and* the P2 decision-policy/risk-tiering governance? *(Recommend: CTO / Trust function; confirm.)*
2. **"Culture/values fit" (P1/P13 risk):** Carried from DOC-04 §10 — any "fit" evaluation must be engineered to *not* become a bias vector; flagged under P1, mechanism deferred to the Evaluation Engine / Fairness work.
3. **Candidate premium services (P7 exception):** When/if we offer optional candidate career services, what guardrails keep them non-coercive and non-conflicted? *(Defer; post-V1 per KD-03.14.)*
4. **Risk-tier thresholds (P2 mechanism):** Who sets and audits the Low/Medium/High/Very-High thresholds, and how are they kept bias-safe? *(Implementation — deferred to AI Strategy / Evaluation Engine / Compliance per A-05.2 §A3; the *principle* is fixed.)*

---

## 8. Summary

### 8.1 Key decisions recorded
- **KD-05.1** — Twelve principles across a **strict priority ladder** (Tier 0 gates → Tier 5 velocity); higher tier always wins conflicts.
- **KD-05.2** — **Three absolute gates with zero exceptions:** P1 (fair & explainable), P2 (human decides), P3 (privacy/consent/isolation).
- **KD-05.3** — **Four identity non-negotiables:** infrastructure-not-SoR (P4), neutrality (P5), sensors-not-product (P6), candidate-as-user (P7).
- **KD-05.4** — **Ranked priorities:** Trust & Security (P8) > Decision Quality (P9/P10) > Integration Ease (P11) > Velocity & Simplicity (P12) — the ratified refinement of DOC-01 §9.
- **KD-05.5** — A **deterministic conflict-resolution protocol** (§4) with same-tier tie-break (Decision Quality leads) and a mandatory, bounded, documented **exception log**.
- **KD-05.6** — The Constitution is an **operational decision framework** used by every function (§5); Tier-0 gates must be satisfied *by construction* in architecture, not bolted on.
- **KD-05.7** — **Human Accountability Framework (P2, reframed):** humans accountable for decisions + policies; automation permitted with **risk-proportional** oversight; High/Very-High-risk decisions need direct human review; **no "human click theater."** (A-05.2 §A1; DOC-04 INV-1/DC-7 amended in lockstep.)
- **KD-05.8** — **Progressive Explainability (P13, new Tier-0):** explainability is **audience-aware** per the A-05.2 §A2 matrix; candidates get constructive evidence-based feedback, never internal mechanisms; compliance/audit gets everything.
- **KD-05.9** — Constitution now includes **Constitutional Interpretation** (intent here, mechanism in later docs), an explicit **Non-Goals** list, and a **Constitution Lifecycle** (amendment authority, cadence, versioning, backward-compat). **Engineering Principles** will be a separate future document.

### 8.2 Unresolved questions (for founder/CTO)
The five in §7 — most consequentially: **(a)** the standard for explaining rejections to candidates, and **(b)** human-in-the-loop granularity in high-volume funnels (must a human review every rejection?). Both have recommended directions; both need explicit ratification (likely alongside DOC-06/DOC-11).

### 8.3 Suggested next document
*(Roadmap revised again after A-05.2: a **Product Design Manifesto** was inserted at 06, and Personas/JTBD split. The authoritative current roadmap now lives in DOC-06 §13.4. A-05.2 §A6's sequence is superseded by it.)*

**DOC-06 — Product Design Manifesto** (the *experiential* constitution — how every user should *feel*) comes first, then **DOC-07 — Product Philosophy** (what we *believe* about product).
- **Why this order.** Governance (this Constitution) → experience intent (Manifesto, feeling) → product convictions (Philosophy, belief) → *then* who we serve (Personas) and why they "hire" us (JTBD).
- **Current roadmap:** 01 Vision · 02 Problem · 03 Strategy · 04 Domain · 05 Constitution · **06 Product Design Manifesto** · 07 Product Philosophy · 08 Personas · 09 Jobs-To-Be-Done · 10 Customer Journey · 11 Functional Requirements · 12 NFRs · 13 AI Strategy · 14 Evaluation Engine · 15 Architecture · 16 Engineering Principles.

> **Alternative:** the standalone **Moat Strategy** deep-dive (CTO-flagged) remains available as a parallel near-term doc; its spine already exists in DOC-03 §13.

---

*End of DOC-05 v0.1. This is the company's constitution and decision framework. Awaiting founder review of the five open questions (§7) — especially rejection-explanation standard and human-in-the-loop granularity — before promotion to Ratified.*
