# ARCH-15 — AI Governance Architecture

| Field | Value |
|---|---|
| **Document ID** | ARCH-15 |
| **Title** | AI Governance Architecture (governing the AI lifecycle without touching the domain) |
| **Owner** | Chief AI/Responsible-AI Officer + Principal AI Governance Architect + Fairness/Model-Risk leads + Security & Compliance |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture (AI governance) |
| **Depends on** | ARCH-14 (AI observability signals), ARCH-11 (AI runtime/harness/calibration), ARCH-12 (ops/release), ARCH-13 (security/compliance), DOC-05 (Human Accountability, gates), DOC-02 (research grounding) |
| **Blocks** | ARCH-16 (Platform Governance — the final document) |
| **The one question** | **"Who decides — with what evidence and authority — how the AI is allowed to change, and how do we keep it honest, fair, and accountable over years, without ever letting governance touch the domain or override a gate?"** |
| **The handoff** | ARCH-14 **observes** AI quality; ARCH-15 **governs** it. This document closes the **observe → govern → act** loop. |
| **The cardinal boundary** | **Governance sets policy; it never force-passes a gate and never edits the domain.** A board may change thresholds, approve/retire models, or drive a re-assessment — it can **never** flip a live `FairnessHeld` to passed, decide a hire, or alter an aggregate/contract (those are ARCH-16 / the domain). |
| **Scope** | Governance of the AI lifecycle: prompts, models, datasets, benchmarks, calibration, providers, fairness, human-review policy, model risk. **Platform/ADR/contract/schema governance → ARCH-16.** |

---

## 0. AI Governance Philosophy

The platform's differentiation is AI-driven judgment; its trust depends on that AI staying **honest, fair, calibrated, and accountable** as models, prompts, and the world change. ARCH-11 built the runtime; ARCH-14 gave us eyes on it; ARCH-15 gives it **governance** — the human and procedural authority that decides how the AI is allowed to evolve.

The reason AI needs *its own* governance (distinct from platform governance) is that it has properties ordinary software doesn't: it is **probabilistic**, it **drifts**, it can be **attacked** (ARCH-13), it carries **fairness and regulatory** weight (hiring is high-risk AI), and its quality is **empirical** (measured against data, not proven). Those demand a fairness review board, model-risk management, dataset governance, and calibration governance that platform governance (ADRs, schemas, contracts) neither covers nor should.

Yet governance must never become a backdoor around the architecture:

> ### AD-127 — AI Governance governs the AI lifecycle only; it has no authority over domain rules, contracts, gates, or authoritative state.
> The AI governance bodies decide **what the AI is allowed to be** (which models/prompts/datasets/calibrations are approved, what fairness thresholds apply, when human review is required). They **cannot** change a business rule (domain), a contract/schema (ARCH-16), or a live gate verdict (runtime). Governance shapes *what the AI proposes*; the domain still decides. This preserves AD-88 at the governance layer: even the governance function cannot make the AI authoritative.

> ### AD-131 — The observe → govern → act loop is closed and auditable. Observability signals trigger governed decisions; every governed decision is recorded on the operational trail (AD-106).
> Drift, override-rate, and fairness signals (ARCH-14) do not auto-correct anything (AD-124) — they **trigger a governed decision** (recalibrate / roll back / retrain a prompt / retire a model / tighten human review), which is deliberated by the right body, recorded with operator·reason·verification (AD-106), and executed through the normal release pipeline (ARCH-12). Governance is a *loop*, not a one-time approval.

---

## 1. Governance Scope & Boundaries

Three governance domains, cleanly separated (no overlap):

| Governs… | Owned by | Examples |
|---|---|---|
| **Business rules & meaning** | The domain (DOC-04 term owners; product) | what a Recommendation is; gate definitions |
| **The AI lifecycle** | **AI Governance (this doc)** | prompts, models, datasets, calibration, providers, fairness thresholds, human-review policy |
| **The platform contract/architecture** | Platform Governance (ARCH-16) | ADRs, contracts, schemas, compatibility, deprecation, trust-assumptions register |

**AI Governance owns:** prompt lifecycle, model approval/retirement, provider approval, golden-dataset & benchmark governance, calibration governance, fairness policy & review, human-review policy, AI model-risk management, AI incident governance.

**AI Governance does NOT own (explicit):** domain rules; contracts/schemas/APIs (ARCH-16); live gate verdicts (runtime — Fairness/Integrity/Consent Services); authoritative state; deployment products (ARCH-10); the *decision* to hire (INV-1, always human).

---

## 2. Governance Bodies

| Body | Authority | Membership (roles) |
|---|---|---|
| **AI Governance Board** | Approves model/prompt/dataset/calibration changes by risk tier; owns AI model-risk policy; owns AI incident post-mortems | AI/ML lead, product, security, legal/compliance, a fairness expert |
| **Fairness Review Board** | Owns fairness *policy* and thresholds; reviews adverse-impact patterns and fairness-hold trends; commissions bias audits; drives correction (never force-passes a gate) | I/O psychologist / fairness expert, legal, product, AI lead, (external auditor as needed) |
| **Human-Review Policy owner** | Owns when human review is mandatory (risk tiers, DOC-05 Human Accountability Framework); owns held-candidate resolution SLA | product + compliance + ops |
| **Provider Approval authority** | Vets and approves LLM/AI providers (security, data-handling, quality) | security, AI lead, legal, procurement |

> Bodies deliberate and set **policy**; the **runtime enforces** it. This mirrors DOC-05's "the Constitution at runtime" — the boards are the constitutional convention, the gates are the constitution enforced.

---

## 3. Prompt Governance

Operationalizes ARCH-11 §5 as governance.

| Concern | Decision |
|---|---|
| **Lifecycle** | Draft → reviewed → **Model Quality Harness pass (AD-97)** → approved (by risk tier) → canary → promoted → (eventually) retired. |
| **Versioning** | Immutable, semver-versioned in the Prompt Registry; every proposal records the prompt version (provenance, AD-95). |
| **Review** | Peer review + board approval for high-risk prompt changes (those affecting judgment or fairness). |
| **Retirement** | Retired prompt versions are **retained** (not deleted) so any past evaluation made under them remains reproducible/explainable (AD-133). |
| **What a prompt may never do** | Encode a gate, an invariant, or a decision (ARCH-05 AD-30). Governance enforces this in review. |

---

## 4. Model Governance

| Concern | Decision |
|---|---|
| **Model approval** | A new model (or version) is approved only after the Model Quality Harness (quality + fairness + calibration + hallucination + cost) and board sign-off by risk tier. |
| **Provider approval** | Providers pass §7 security/data-handling/quality vetting before use (ties AD-113 untrusted-provider). |
| **Model registry** | Versioned; routing policy (ARCH-11 §4) references approved models only; unapproved models cannot be routed to. |
| **Model risk assessment** | Each model change is risk-classified (§10) determining approval depth. |
| **Model retirement** | Deliberate, governed; retired model versions **retained for reproducibility** of past decisions (AD-133); routing updated; provenance preserved. |
| **Version pinning** | Production pins exact model versions; "silent" provider-side model updates are treated as unapproved changes and blocked/flagged (a provider auto-upgrading a model is a governance event, not a free ride). |

> ### AD-133 — Retired prompts/models/calibrations are retained (never deleted); any past decision made under a now-retired version remains fully reproducible and explainable.
> Because a hiring decision may be questioned months or years later (legally, ethically), the platform must be able to reconstruct *exactly* how the AI proposed at that time — the model, prompt, and calibration version (AD-95). Retirement removes a version from *future use*, never from the *reproducibility record*.

---

## 5. Dataset Governance

| Concern | Decision |
|---|---|
| **Golden datasets** | Curated, versioned datasets of representative work samples + known-good judgments, used by the Model Quality Harness (AD-97). |
| **Consent & privacy** | Datasets are **consent-governed and PII-minimized** (INV-11, AD-89); a subject who withdraws consent / is crypto-shredded (AD-64) is **removed from datasets** — data lineage tracks dataset membership so shred propagates. |
| **Fairness representativeness** | Datasets are curated for representativeness so the harness's fairness thresholds are meaningful; the Fairness Board owns representativeness criteria. |
| **Access control** | Datasets are access-controlled, tenant-boundary-respecting, and their use is audited. |
| **Provider training** | **We do not permit providers to train on tenant data** (contractual + technical, §7); golden datasets are never sent for provider training. |
| **Versioning** | Datasets are versioned; a harness result cites the dataset version (reproducibility). |

> ### AD-132 — Golden datasets and benchmarks are consent-governed, PII-minimized, fairness-representative, versioned artifacts; crypto-shred propagates into datasets (a shredded subject leaves the dataset).

---

## 6. Benchmark Governance *(deferred capability — governance reserved)*

| Concern | Decision |
|---|---|
| **Aggregate-only** | Network benchmarks (the future moat) are **aggregate/anonymized only** (INV-8); no single tenant's or candidate's private data is exposed to another. |
| **Consent & opt-in** | Benchmark participation is tenant opt-in and consent-governed (ARCH-08 §8 policies). |
| **Fairness of benchmarks** | The Fairness Board reviews benchmarks for representativeness and adverse-impact potential before they influence anything. |
| **Governance-before-build** | Deferred to post-MVP, but the governance rules are set now so the capability cannot be built ungoverned. |

---

## 7. Calibration Governance

Confidence calibration (ARCH-11 §7) is the honesty mechanism (INV-6) — and honesty is governed.

| Concern | Decision |
|---|---|
| **Calibration as artifact** | Confidence calibration curves/parameters are **versioned, governed artifacts** (like prompts/models). |
| **Recalibration cadence** | As Outcome Learning accrues, recalibration is scheduled + triggered by drift signals (ARCH-14 AD-126); each recalibration is board-reviewed and harness-checked. |
| **Approval** | A calibration change is risk-classified (§10); it changes how honestly the system expresses certainty, so it is treated as a significant change. |
| **The honesty floor** | Governance owns the **escalation floor**: below a confidence threshold the system **always** escalates to a human (ARCH-11 §7 / DOC-05 P2). The floor is a governed policy, not a tunable someone can quietly lower. |

---

## 8. Fairness Governance & the Fairness Review Board

The most consequential governance function — hiring fairness is the product's ethical and legal core (DOC-01/02/05).

| Concern | Decision |
|---|---|
| **Fairness policy ownership** | The Fairness Review Board owns fairness **policy**: adverse-impact thresholds, the fairness metrics used, the harness fairness gates (AD-97), and what "held" triggers. |
| **Standing review** | The board reviews fairness-hold trends and fairness-signal drift (ARCH-14) on a cadence — not just per-incident. |
| **Bias audits** | Commissions periodic bias audits (internal + external), supporting NYC LL144-style requirements (§13); audit evidence is emergent from audit + fairness facts (AD-118). |
| **Correction, not override** | When a campaign is **held** by the Fairness gate, the board **cannot force-pass it**. It drives **correction**: investigate → fix (calibration/prompt/data/threshold) → **re-assess** → a *new* authoritative `FairnessApproved` from the Fairness Service, **or** a documented, audited human decision on individual cases. The bit is only ever flipped by the runtime gate, never by a board. |
| **Threshold changes** | A threshold change is a governed policy change applied **going forward**; it never retroactively rewrites a past verdict (immutability, INV-e). |

> ### AD-128 — The Fairness Review Board owns fairness policy and thresholds but cannot override a live gate verdict. A hold is resolved by correction and re-assessment (a new authoritative verdict) or a documented human decision — never by force-passing.
> This preserves INV-3 and AD-99 at the governance layer: governance can make the system *fairer* (better thresholds, better calibration, corrected data) but can never make it *unfair-by-fiat*. The gate remains the only thing that can pass a gate.

---

## 9. Human-Review Policy

Governs *when a human must review*, operationalizing DOC-05's Human Accountability Framework (risk-tiered oversight).

| Concern | Decision |
|---|---|
| **Risk-tiered review** | Higher-stakes/lower-confidence/flagged cases require deeper human review (DOC-05 P2 tiers); the policy defines the tiers and triggers. |
| **Mandatory-review triggers** | Low calibrated confidence (below floor, §7), integrity flags, fairness holds, novel/ambiguous cases, high-impact decisions. |
| **Held-candidate resolution SLA** | Governance owns the committed maximum time a candidate may remain held before mandatory human action (ARCH-12 OQ) — a governed business+ethics commitment (DOC-06 no-black-hole). |
| **Human never rubber-stamps** | Review must be substantive (evidence presented, P13); the policy guards against click-theater (DOC-05 A-05.2). |
| **The human still decides** | No policy change ever removes the human from the accountable decision (INV-1). Governance can require *more* review, never *less than* accountable human ownership. |

---

## 10. Model Risk Management

Hiring AI is **high-risk AI**; changes are governed by a model-risk framework (NIST AI RMF / EU AI Act-aligned, §13).

| Risk tier | Examples | Governance depth |
|---|---|---|
| **High** | new model family; judgment-prompt change; calibration change; fairness-threshold change; new provider | Full board approval + harness (quality+fairness+calibration) + conservative canary + rollback plan |
| **Medium** | non-judgment prompt tweak; routing policy change | Reviewer + harness + canary |
| **Low** | explanation-phrasing change with no judgment impact | Peer review + harness regression |

**Framework elements:** risk classification of every AI change; approval thresholds by tier; rollback authority (who can order an emergency AI rollback — ties ARCH-12 §9); model-risk register; periodic model-risk review; AI incident governance (a fairness/quality incident gets a governed post-mortem alongside the ARCH-12 PIR).

> ### AD-129 — Every AI artifact change (prompt, model, dataset, calibration, routing, threshold) is risk-classified and change-managed; high-risk changes require board approval + a passing Model Quality Harness (quality *and* fairness) before canary. No AI change reaches production ungoverned.

---

## 11. The Observe → Govern → Act Loop

The heart of ongoing AI governance (closes ARCH-14 → ARCH-15 → ARCH-12):

```
 ARCH-14 signals            ARCH-15 governance                 ARCH-12 execution
 ───────────────           ──────────────────                 ─────────────────
 confidence drift    ─┐
 override-rate rise   ├─▶  triage → risk-classify (§10)  ─▶   recalibrate / roll back /
 fairness-signal drift│    → right body decides (§2)          retrain prompt / retire model /
 hallucination-reject │    → Model Quality Harness (AD-97)     tighten human review
 cost anomaly        ─┘    → recorded on op-trail (AD-106)  ─▶ via normal release pipeline (canary→promote/rollback)
                                    │
                                    └────────── governed decision is itself auditable ──────────┐
                                                                                                 ▼
                                                                              back to ARCH-14 (verify effect)
```

**Rules of the loop:** signals **never auto-mutate** the runtime (AD-124); a signal triggers a **governed decision** by the right body; the decision executes through the **normal, canaried release pipeline** (never a hand-hack); the decision and its **verified effect** are recorded (AD-106) and re-observed (ARCH-14). The loop is continuous, not a one-time gate.

---

## 12. AI Change Management

| Concern | Decision |
|---|---|
| **Pipeline** | proposed change → risk classification (§10) → Model Quality Harness (AD-97) → body approval by tier (§2) → canary (ARCH-12 §9) → monitored promotion → auto-rollback on quality/fairness regression. |
| **Provenance** | Every promoted change carries model+prompt+calibration+dataset versions (AD-95); the change itself is on the operational trail (AD-106). |
| **Emergency changes** | An emergency AI rollback (e.g., discovered fairness regression) is fast-tracked but still recorded and reviewed post-hoc (ARCH-12 §12); emergency ≠ ungoverned. |
| **No hand-promotion** | Reaffirms AD-103: no prompt/model reaches production by hand; governance is the *approval*, the pipeline is the *mechanism*. |

> ### AD-130 — Governance decisions are versioned artifacts.
> Every approval, rejection, retirement, threshold change, and board decision has its own **immutable version, effective date, rationale, approvers, and supersession history**. Past governance decisions remain reconstructable exactly as past AI behavior remains reproducible. *Rationale:* completes the reproducibility family — **AD-95** (AI provenance) + **AD-106** (operational trail) + **AD-133** (retained AI artifacts) make *what the system did* reconstructable; AD-130 makes *what governance decided, when, and why* reconstructable. So a bias audit or customer dispute years later can reconstruct not just the exact model/prompt/calibration (AD-133) but the exact **governance state** — which thresholds and approvals were in force at the time. Governance is itself an auditable, versioned record.

---

## 13. Regulatory Alignment

Hiring/employment AI is among the most heavily regulated AI categories. Governance maps to the regimes — and much evidence is **emergent** (AD-118).

| Regime / requirement | How this architecture aligns |
|---|---|
| **EU AI Act (high-risk AI — employment)** | Risk management (§10), data governance (§5), transparency/explainability (P13, evidence grounding AD-90), human oversight (§9, INV-1), accuracy/robustness (harness AD-97), logging (audit AD-32), fairness (§8). |
| **NIST AI RMF** | Govern/Map/Measure/Manage: this document *is* Govern; ARCH-14 is Measure; §10 is Manage; §1 is Map. |
| **NYC Local Law 144 (bias audit for AEDTs)** | Bias audits commissioned by the Fairness Board (§8); adverse-impact evidence emergent from fairness + audit facts. |
| **EEOC / Uniform Guidelines (adverse impact)** | Fairness gate (INV-3) + adverse-impact monitoring + documented validity (DOC-02 research grounding: Sackett; Bertrand & Mullainathan). |
| **GDPR/CCPA (automated decision-making, art. 22-adjacent)** | Human accountability (INV-1) means no *solely*-automated hiring decision; consent, minimization, erasure (ARCH-13). |

> Because oversight, explainability, audit, fairness gating, and human accountability are **structural** (not retrofitted), regulatory alignment is largely a matter of *evidencing* what the architecture already enforces — extending AD-118 to the AI-specific regimes. A strategic advantage in a tightening regulatory landscape (DOC-02 MR-11 platform risk).

---

## 14. Architecture Decisions *(continuing the log; ARCH-14 ended at AD-126)*

| ID | Decision | Rationale |
|---|---|---|
| **AD-127** | AI Governance governs the AI lifecycle only; no authority over domain/contracts/gates/state | Governance shapes what the AI proposes, never what the platform decides (preserves AD-88) |
| **AD-128** | Fairness Board owns fairness policy/thresholds but cannot override a live gate verdict | Governance can make the system fairer, never unfair-by-fiat; only the gate passes a gate (INV-3/AD-99) |
| **AD-129** | Every AI change is risk-classified + change-managed; high-risk needs board approval + harness (quality+fairness) | No AI change reaches production ungoverned |
| **AD-130** | Governance decisions are versioned, immutable artifacts (approvers, rationale, effective date, supersession) | Governance itself is reproducible; completes AD-95/AD-106/AD-133 reproducibility family |
| **AD-131** | Observe→govern→act loop is closed + auditable; signals trigger governed decisions, never auto-mutation | Governance is a continuous loop; signals never self-apply (AD-124) |
| **AD-132** | Golden datasets/benchmarks are consent-governed, PII-min, fairness-representative, versioned; crypto-shred propagates in | Data governance + privacy + reproducibility |
| **AD-133** | Retired prompts/models/calibrations retained; past decisions remain reproducible/explainable | A decision can be questioned years later; must reconstruct exactly how the AI proposed then |
| **AD-134** | Hiring is high-risk AI; the platform aligns to a recognized AI risk framework (NIST AI RMF / EU AI Act / LL144) as first-class | Regulatory alignment is structural + emergent (AD-118); a strategic moat |

## 15. Open Questions

1. **Golden-dataset bootstrapping before outcome data** (carried, ARCH-11 OQ): how to build a representative, consented, fair golden dataset pre-scale (AS-21 dependency)? Who signs off representativeness on day one?
2. **External bias-audit cadence & auditor selection** (LL144 and beyond) — how often, by whom, published to whom.
3. **Provider "silent model update" handling** — contractual pinning vs. detection; what happens when a provider deprecates a pinned version.
4. **Fairness metric selection** — which adverse-impact metric(s) the Fairness Board standardizes on (four-fifths rule vs. others), and per-jurisdiction variation.
5. **Held-candidate resolution SLA value** (carried) — the governed maximum, a business+ethics commitment.
6. **Board composition & independence** — how much external/independent membership on the Fairness Board to ensure credibility.

## 16. Risks

- **Governance-as-backdoor:** a board pressured to force-pass a hold or lower the honesty floor. *Mitigation:* AD-127/AD-128 — governance cannot pass a gate or edit the domain; only correction+re-assessment; all decisions audited (AD-131).
- **Fairness theater:** a board that rubber-stamps. *Mitigation:* external audits, standing trend review, independent membership (OQ-6), auditable decisions.
- **Dataset bias:** an unrepresentative golden dataset makes the harness's fairness gate meaningless. *Mitigation:* §5 representativeness governance + external review.
- **Reproducibility loss:** deleting a retired model breaks the ability to explain a past decision. *Mitigation:* AD-133 retention.
- **Regulatory drift:** new AI regulation. *Mitigation:* AD-134 framework alignment + emergent evidence (AD-118); governance tracks regimes.
- **Provider opacity:** a provider changing a model under us. *Mitigation:* version pinning + change detection (§4, OQ-3).
- **Slow governance vs. delivery pressure:** boards becoming a bottleneck. *Mitigation:* risk-tiered depth (§10) — low-risk changes move fast; only high-risk gets full board.

## 17. Deferred

- **To ARCH-16 (Platform Governance):** ADR lifecycle, contract/schema compatibility + deprecation, architectural review board, trust-assumptions-register ownership, and how AI Governance and Platform Governance **interface** (e.g., a routing-policy change that is both an AI artifact *and* a config artifact).
- **Implementation:** board charters, RACI, audit schedules, dataset-curation runbooks, model-risk register tooling — governance operations that consume this architecture.
- **Deferred capabilities:** benchmark/outcome-learning governance activates when those capabilities are built (§6, governance reserved now).

---

*End of ARCH-15 v0.1 — the AI Governance Architecture. The AI lifecycle — prompts, models, datasets, benchmarks, calibration, providers, fairness, human review, model risk — is now governed by the right bodies with the right evidence, closing the observe→govern→act loop (AD-131) without ever touching the domain or overriding a gate (AD-127/AD-128). Governance can make the AI better, fairer, and more honest; it can never make it authoritative or unfair-by-fiat. Regulatory alignment (high-risk AI) is structural and largely emergent (AD-134/AD-118). One document remains: **ARCH-16 — Platform Governance Architecture**, which governs the architecture itself (ADRs, contracts, schemas, compatibility, evolution) and completes the corpus.*
