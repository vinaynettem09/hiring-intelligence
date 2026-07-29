# ARCH-11 — AI Runtime Architecture

| Field | Value |
|---|---|
| **Document ID** | ARCH-11 |
| **Title** | AI Runtime Architecture (the internals behind the Intelligence Compute ACL) |
| **Owner** | Principal AI Platform Architect + ML Systems Architect + Distributed Systems Architect + Security Architect |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture (AI realization) |
| **Depends on** | ARCH-10 (deployment/egress/AD-85), ARCH-08 (persistence/caches), ARCH-07 (capability contracts AD-56), ARCH-06 (Intelligence Compute AD-47), ARCH-05 (facts AD-35), ARCH-03 (domain), ARCH-01 (LLM trust boundary), DOC-05 (gates) |
| **Blocks** | Evaluation Engine detail, ARCH-12 (Operational), ARCH-14 (Observability), ARCH-15 (Governance) |
| **The one question** | **"How does the AI layer produce high-quality proposals — safely, honestly, affordably, and replaceably — without ever becoming a source of business truth?"** |
| **The cardinal rule** | **The AI proposes; the domain decides.** Every output of this layer is a **validated proposal** consumed by an owning service, never an authoritative fact (ARCH-05 AD-35 / ARCH-06 AD-47 / ARCH-07 AD-56 / ARCH-10 AD-85). |
| **Terminology guard** | ⚠️ **"Evaluation" is a frozen domain term** (a candidate judgment — DOC-04). The AI-testing apparatus is therefore named the **Model Quality Harness**, **never** an "eval(uation) harness," to avoid corrupting the ubiquitous language. |

---

## 0. AI Runtime Philosophy

This is where the product becomes differentiated — and where the architecture is most tempted to betray itself. Every prior document worked to ensure the AI can be *excellent* without being *authoritative*. ARCH-11 must preserve that under the pressure of making the AI actually good.

Four commitments:

1. **The AI proposes; the domain decides.** The runtime returns *proposals* (structured evidence, an evaluation judgment, an explanation, integrity/fairness *signals*). The owning service **validates and commits** the fact; the authoritative gates (Integrity, Fairness — BC-6) own their verdicts. A model output is never, at any point, a business fact.
2. **Honesty over confidence.** The product sells *decision quality*, which depends on **honest uncertainty** (INV-6). The runtime must express *calibrated* confidence and must be willing to say "insufficient evidence — escalate to a human." A confident wrong answer is the worst possible output.
3. **The model is a replaceable component.** Behind the ACL (ARCH-07 AD-52), the model/provider is config (AD-85). Prompts, models, and datasets are versioned artifacts, not code and never rules.
4. **PII never leaks to the model un-minimized.** The sharpest trust boundary (ARCH-01) is enforced *before* every invocation (AD-83).

> ### AD-88 — The AI Runtime emits only validated proposals; it never produces an authoritative business fact, and it may always return "escalate to human."
> Reaffirms AD-35/47/56/85 at the runtime layer and adds the corollary: **"escalate" is a first-class, expected output, not a failure** (fail-soft, ARCH-06 §9). The runtime is architecturally incapable of finalizing anything.

---

## 1. AI Capability Decomposition

The Intelligence Compute service (ARCH-06 §2.5) exposes a small set of **pure, stateless capabilities** (ARCH-07 §2.4). Each takes minimized, role-relevant input and returns a validated proposal; **none owns an aggregate or emits a fact.**

| Capability | Proposes | Consumed by (owner commits) | Owns a fact? |
|---|---|---|---|
| **StructureEvidence** | raw work sample → structured Evidence Items (per engineering dimension, AD-10) | Evaluation Service → `EvidenceRecorded` | ❌ |
| **Evaluate** | integrity-checked evidence → evaluation judgment (score + cited evidence + candidate confidence signals) | Evaluation Service → `EvaluationCompleted` | ❌ |
| **Explain** | evaluation → audience-appropriate explanation (candidate/recruiter/HM/audit — P13) | Evaluation/Feedback | ❌ |
| **IntegritySignals** | evidence → authenticity signals (not a verdict) | **Integrity Service** owns the verdict | ❌ |
| **FairnessSignals** | campaign set → adverse-impact signals (not a verdict) | **Fairness Service** owns the verdict | ❌ |
| **Embed** *(future)* | evidence/role → vector embeddings | Evidence Graph / semantic search (deferred) | ❌ |

> **Decomposition rule:** a capability is admitted only if it maps to an ARCH-07 capability contract and produces a proposal an owning service turns into a fact. The AI is **never** given a capability that would let it decide (no `MakeDecision`, no `PassFairness`) — those are structurally impossible here.

---

## 2. The Inference Pipeline

Every model invocation passes through the same governed pipeline. Stages are fixed; the model call is one stage in the middle.

```
 request (from owning service, via ACL)
     │
 [1] Intake & authorize      ── envelope (ARCH-07 AD-53); tenant server-resolved (AD-71)
     │
 [2] Content-hash & cache    ── idempotency + cost (AD-66); cache hit → return proposal, skip model
     │  (miss ↓)
 [3] PII MINIMIZATION        ── §3; strip/pseudonymize identity; role-relevant content only  ⟦trust boundary⟧
     │
 [4] Context assembly        ── minimized content + frozen Calibration + versioned Prompt (registry)
     │
 [5] Model ROUTING           ── §4; pick model by task/tier/policy (provider-abstracted, AD-92)
     │
 [6] Invocation (egress)     ── controlled egress gateway (AD-83); timeout/deadline; retry (idempotent)
     │
 [7] STRUCTURED-OUTPUT       ── §6; constrain + validate against schema; invalid → repair → retry → escalate
         VALIDATION
     │
 [8] CONFIDENCE CALIBRATION  ── §7; runtime-computed (evidence sufficiency + calibration), NOT model self-report
     │
 [9] Proposal assembly       ── attach citations, confidence, model/prompt version (provenance)
     │
 [10] Cache store + observ.  ── store by content-hash; emit model-observability metrics (§14)
     │
 return PROPOSAL  ── owning service validates & commits the fact (or escalates to human)
         │
   (any stage may short-circuit to → ESCALATE-TO-HUMAN: fail-soft, never fabricate)
```

**Pipeline invariants:** PII minimization (3) always precedes egress (6); validation (7) always precedes use; confidence (8) is always attached; provenance (model + prompt version) always travels with the proposal (§14/§15). No stage may be skipped except by a cache hit (2), which returns a previously-validated proposal.

> ### AD-98 — Runtime orchestration is deterministic; model reasoning is the single intentionally-opaque step.
> Every pipeline stage **except the model invocation itself** (stages 1–5 and 7–10) is **deterministic and reproducible**: given the same input, prompt version, model version, calibration version, and evidence, the orchestration behaves identically. Consequently, when two executions differ, the cause is **always attributable** to a *named* variable — different input, prompt, model, calibration, or evidence — and **never** to the orchestration behaving differently. *Rationale:* debugging, audits, incident analysis, and explainability (P13/INV-2) all require that the machinery around the model be a fixed function; the model is the one deliberately-opaque box, and provenance (AD-95) records exactly which versions produced any proposal so any difference is explainable, never mysterious.

---

## 3. PII Minimization & the Trust Boundary

The single sharpest risk in the whole platform (ARCH-01). Enforced as a **mandatory pre-invocation stage** and a **network egress control** (AD-83), belt-and-suspenders.

| Concern | Decision |
|---|---|
| **What is minimized** | Direct identifiers (name, contact, employer names where irrelevant, demographic-adjacent signals) are stripped or pseudonymized before any model sees content. Only **role-relevant work content** crosses. |
| **When** | Pipeline stage [3], *before* context assembly and egress. No path reaches a model without passing it. |
| **Bias-safety tie-in** | Minimization also removes demographic-adjacent cues (name, photos, affiliations) — reducing model bias at the source, supporting the fairness posture (Bertrand & Mullainathan grounding). |
| **Reversibility** | A minimization map (pseudonym ↔ real identity) is held **inside the tenant boundary**, never sent out, encrypted under the per-tenant key (AD-84) — so proposals can be re-associated internally without the model ever knowing identity. |
| **Enforcement** | Stage [3] in-process + egress gateway (AD-83) network-level default-deny; PII-classified content that reaches egress un-minimized is blocked and alerted (security incident). |
| **Logging** | Minimized content only in traces; **raw PII never logged** (ARCH-06 §9); crypto-shred discipline (ARCH-08 AD-64) preserved. |

> ### AD-89 — Every model invocation is preceded by a mandatory PII-minimization stage; raw candidate PII never reaches a model, enforced in-process and at the network egress.

---

## 4. Model Routing & Selection

| Concern | Decision |
|---|---|
| **Primary model** | Hosted **Claude** (Opus-class for the hardest judgments, Sonnet-class for cheaper/faster tasks) behind the ACL (AD-85). |
| **Routing policy** | A **governed config artifact** (versioned, §15) maps *(capability, task complexity, tenant tier)* → model. E.g., StructureEvidence → cheaper tier; Evaluate (final judgment) → strongest tier; Explain → mid tier. |
| **Provider abstraction** | Routing sits behind the ACL; a model/provider is selected by policy, never referenced by domain/contract. Swapping providers is a policy change (AD-78/AD-85). |
| **Multi-provider** | The routing layer supports multiple providers for failover (§8) and for capability fit; provider-specific quirks are isolated in the ACL adapter. |
| **Determinism controls** | Low/zero temperature for judgment tasks; sampling controls are part of the versioned prompt/model config, not ad hoc. |

> ### AD-92 — Model routing is a governed, provider-abstracted config artifact; changing a model or provider never changes a contract, boundary, or domain concept.

---

## 5. Prompt Lifecycle & Governance

A prompt is a **versioned artifact**, never a business rule (ARCH-05 AD-30) and never code.

| Concern | Decision |
|---|---|
| **Registry** | Prompts live in a versioned **Prompt Registry** (semver), each bound to a capability + model config. |
| **Review** | Prompt changes are peer-reviewed and pass the **Model Quality Harness** (§ below / AD-97) before release. |
| **Rollout** | Prompt changes are **canaried** like code (ARCH-10 §7): a new prompt version runs on a small traffic slice with quality/fairness monitoring before promotion. |
| **Provenance** | Every proposal records the exact prompt version + model version that produced it (§14) — so any evaluation is reproducible and any regression is traceable to a version. |
| **Immutability** | A released prompt version is immutable; a change is a new version (mirrors contract/schema evolution, ARCH-07 AD-54). |
| **What a prompt may not do** | A prompt may not encode a gate, an invariant, or a decision. It shapes *how the model proposes*, never *what the business permits*. |

---

## 6. Structured Output Validation

Free-text model output is never trusted. Every capability returns **schema-constrained** output validated before use.

| Concern | Decision |
|---|---|
| **Constrained generation** | The model is instructed/constrained to produce output conforming to the capability's proposal schema (the JSON Schemas of ARCH-09, e.g., an evidence/evaluation proposal shape). |
| **Validation** | Output is validated against that schema at pipeline stage [7]; malformed output is **repaired/retried** within a bounded budget. |
| **Failure handling** | Persistent invalid output ⇒ **escalate to human** (AD-88), never pass through unvalidated, never fabricate a shape. |
| **Semantic checks** | Beyond shape: citations must reference **real** Evidence Items (no invented evidence — anti-hallucination); scores must be within range; every claim must trace to cited evidence (supports INV-2 explainability). |
| **Grounding** | Evaluations must cite specific Evidence Items; an evaluation that cannot ground its claims in evidence is rejected (the product refuses ungrounded judgment). |

> ### AD-90 — All model output is schema-validated and evidence-grounded before use; invalid or ungrounded output is retried then escalated, never passed through. Hallucinated citations are a hard reject.

---

## 7. Confidence Calibration

Confidence (the domain VO, INV-6) is **computed by the runtime**, not taken from the model's self-report — because models are systematically overconfident and a self-reported "95%" is not evidence of anything.

| Concern | Decision |
|---|---|
| **What confidence measures** | The system's certainty in *its own* judgment, given **evidence sufficiency and coverage** — not the model's mood. |
| **MVP calibration** | Heuristic: confidence derives from evidence **coverage** (how many role-relevant dimensions have strong evidence), **consistency** (agreement across signals), and **integrity** (authenticity). Thin/ambiguous evidence ⇒ low confidence ⇒ escalate. |
| **Roadmap calibration** | As **Outcome Learning** (deferred moat) accumulates, confidence is **calibrated against real outcomes** — a proper calibration curve (predicted vs. actual). This is a compounding advantage: confidence gets *honestly* better over time. |
| **Never hidden** | Low confidence is surfaced honestly (INV-6), never smoothed away; low-confidence proposals route to human (§12). |
| **Model self-assessment** | May be *an input signal*, but never *the* confidence; the runtime owns the calibrated value. |

> ### AD-91 — Confidence is computed and calibrated by the runtime from evidence sufficiency (MVP) and, later, real outcomes — never taken from the model's self-report. Low confidence escalates.

---

## 8. Provider Failover & Fallback

| Concern | Decision |
|---|---|
| **Failover** | On provider error/timeout/unavailability, the router retries (idempotent) then **fails over** to an alternate provider/model of comparable capability (multi-provider, §4). |
| **Circuit breaking** | Mesh + client circuit breakers (ARCH-06 §7) open on a failing provider; traffic shifts; breaker state is observable. |
| **Fallback (degradation)** | If no provider can serve within budget/deadline: the capability **fails soft** — return low/no confidence and **escalate to human** (AD-88). The candidate is never dropped; the work waits or routes to a person (ARCH-06 §9, DOC-06 no-black-hole). |
| **Never fail-open on gates** | For integrity/fairness *signals*, provider failure means the **authoritative gate holds** (fail-closed at the gate, ARCH-04 §9) — the AI's unavailability can never cause a gate to pass. |
| **Quality parity** | Failover targets must meet a minimum quality bar (validated via the Model Quality Harness) so failover never silently degrades judgment quality below threshold. |

---

## 9. Embedding Lifecycle *(future capability — reserve the boundary)*

For the deferred moat (Evidence Graph, semantic evidence search, Hiring Memory), embeddings are a **derived, rebuildable** artifact (ARCH-08 §1).

| Concern | Decision |
|---|---|
| **Generation** | The `Embed` capability produces vectors from minimized evidence/role content (post-PII-minimization, §3). |
| **Versioning** | Embeddings are tagged with the **embedding-model version**; a model change means **re-embedding** (a Job, ARCH-10 §3). Mixed-version vectors are never compared. |
| **Rebuildability** | Embeddings are derived from immutable facts/evidence and can be fully regenerated by replay (ARCH-08 AD-65) — never a source of truth. |
| **Deferral** | Not built at MVP (AD-10 text-first work sample; benchmarking/memory deferred). Boundary reserved so it attaches to the fact stream later without core change (ARCH-06 §14). |

---

## 10. Vector & Feature Stores *(future moat substrate — reserved)*

| Store | Serves (deferred capability) | Nature |
|---|---|---|
| **Vector store** | Evidence Graph, semantic evidence search, Hiring Memory retrieval | derived from facts; rebuildable; per-tenant scoped (or aggregate/anonymized for network features, INV-8) |
| **Feature store** | Outcome Learning (features linking evidence → outcomes), confidence calibration curves | derived; rebuildable; consent-governed (INV-11) |

**Rules (reserved now, built later):** both are **derived and rebuildable** (never authoritative); both respect **tenant isolation** (per-tenant) except explicitly **aggregate/anonymized** network features (INV-8); both are **consent-governed** (INV-11) and crypto-shred-compatible (embeddings/features of a shredded subject are regenerated-from-nothing, i.e., gone). Product selection deferred (ARCH-08 OQ-4); the boundary is reserved so the compounding moat attaches to the existing fact stream.

---

## 11. Caching Strategy for AI Workloads

| Concern | Decision |
|---|---|
| **Content-hash cache** | Capability results cached by **input content-hash** (minimized content + prompt version + model version + calibration) in Redis (ARCH-08 §7). Same input ⇒ same validated proposal ⇒ cache hit skips the model (pipeline stage [2]). |
| **Why it's safe** | Because capabilities are **pure and idempotent** (AD-56), a cache hit returns an identical proposal — the cache is a cost/latency optimization, **never a source of truth** (AD-94). |
| **Cost impact** | The dominant cost lever: re-evaluating the same work sample, or re-running after a transient failure, reuses the cached proposal instead of re-invoking the model. |
| **Invalidation** | Keyed by version — a new prompt/model/calibration version yields a new key (old entries age out); no manual invalidation of business meaning. |
| **What is NOT cached** | Anything identity-bearing pre-minimization; anything a gate must freshly assess (integrity/fairness verdicts are owned by their services, not cached here). |

> ### AD-94 — AI capability results are cached by content-hash as a pure optimization; the cache is never authoritative and never a fact.

---

## 12. Human-in-the-Loop Escalation

Escalation is not an error path — it is a **designed, first-class output** that expresses the platform's honesty (INV-1/INV-6, DOC-05 P2).

| Trigger | Escalation behavior |
|---|---|
| **Low calibrated confidence** (§7) | Proposal returned marked low-confidence; owning service routes to human review with cited evidence. |
| **Integrity flag** (authenticity doubt) | Integrity Service holds; human reviews (fail-closed at the gate). |
| **Fairness hold** (campaign) | Fairness Service holds delivery; human review (ARCH-04 §9). |
| **Validation failure** (§6, after retries) | Escalate; never fabricate. |
| **Ambiguity / novel case** | The model may itself signal "insufficient basis"; runtime escalates. |
| **Provider unavailability** (§8) | Fail soft to human. |

**Contract:** escalation surfaces to the human via the normal decision path (Decision Support presents evidence; the human decides — INV-1). The AI's "I'm not sure" is a *valuable* output that protects decision quality, not a defect to engineer away.

---

## 13. AI Cost Controls

The AI tier is the dominant cost center (ARCH-06 §8). Cost is a **first-class runtime control**, enforced without ever silently dropping a candidate.

| Control | Decision |
|---|---|
| **Model tiering** | Cheaper models for structuring/explanation; strongest model reserved for final judgment (§4). Never over-spend on easy tasks. |
| **Content-hash caching** | The biggest lever (§11): don't pay twice for the same input. |
| **Token budgets** | Per-tenant and per-task token/cost budgets; approaching a budget triggers **degradation** (cheaper model / queue / batch), never a silent drop. |
| **Batch vs streaming** | Bulk cohort evaluation batched through worker pools (ARCH-10 §6); streaming only where UX needs progress. |
| **Back-pressure** | Queue-depth back-pressure (KEDA, ARCH-06 §8): when overloaded, work queues and the business shows "in progress," never loses a submission. |
| **Cost observability** | Token/cost per proposal, per tenant, per capability are first-class metrics (§14); FinOps procedures → ARCH-12. |

> ### AD-96 — AI cost is a first-class control (tiering + caching + per-tenant budgets + back-pressure); exceeding budget degrades gracefully, never silently drops or fabricates.

---

## 14. Model Observability Hooks

Every proposal carries provenance and emits telemetry (deep pipeline → ARCH-14).

| Signal | Why |
|---|---|
| **Provenance** (model version, prompt version, calibration version, content-hash) | reproducibility; regression tracing; audit of *how* a proposal was formed |
| **Latency & tokens/cost** | performance + FinOps (§13) |
| **Confidence distribution** | detect over/under-confidence drift (§7) |
| **Validation-failure / repair rate** | model/prompt health; hallucination-reject rate (§6) |
| **Override rate** (humans overriding proposals) | the ultimate quality signal — feeds calibration and the Model Quality Harness |
| **Escalation rate** | how often the AI defers to humans; trend = capability health |
| **Fairness-signal drift** | early warning on adverse-impact patterns (feeds Fairness Service + governance) |

> **Provenance is mandatory (AD-95):** a proposal without model+prompt+calibration version is invalid. Because facts are immutable and provenance travels with them, any past evaluation is fully reproducible and explainable — the ops-layer expression of P13/INV-2.

---

## 15. Governance of Prompts, Models & Evaluation Datasets

*(⚠️ "Model Quality Harness" — deliberately **not** "eval harness" — to avoid colliding with the domain term "Evaluation.")*

| Artifact | Governance |
|---|---|
| **Prompts** | Versioned registry; peer review; Model Quality Harness gate; canary rollout; immutable versions (§5). |
| **Models / routing policy** | Versioned; a model or routing change is quality-and-fairness gated before canary (AD-97). |
| **Golden datasets** | Curated, versioned, **consent-and-privacy-compliant** datasets of representative work samples with known-good judgments, used to regression-test prompt/model changes offline. Datasets are governed artifacts (access-controlled, PII-minimized, tenant-consent-respecting). |
| **Model Quality Harness** | An **offline** harness that runs a candidate prompt/model version against the golden datasets, measuring judgment quality, calibration, **fairness/adverse-impact**, hallucination rate, and cost — **before** any production canary. |

> ### AD-97 — No prompt or model change reaches production without passing the offline Model Quality Harness against a governed golden dataset, with quality AND fairness thresholds.
> This is how the AI improves **without** regressing quality or fairness silently. It is the AI-layer analog of consumer-driven contract tests (ARCH-07 AD-55): change is gated by evidence, not confidence. *(Harness operations, dataset curation cadence, and review board → ARCH-12/ARCH-15.)*

---

## 16. Architecture Decisions *(continuing the log; ARCH-10 ended at AD-87)*

| ID | Decision | Rationale | Alternatives |
|---|---|---|---|
| **AD-88** | AI emits only validated proposals; "escalate to human" is a first-class output | Preserves "AI proposes, domain decides" at runtime; honesty over confidence | AI-authoritative outputs (rejected: INV-1, whole thesis) |
| **AD-89** | Mandatory PII-minimization before every model call (in-process + egress) | Contain the sharpest trust boundary; reduce bias at source | Trust provider data handling (rejected: existential risk) |
| **AD-90** | Schema-validated + evidence-grounded output; hallucinated citations hard-rejected | No ungrounded/hallucinated judgment ever used | Trust free-text output (rejected: hallucination) |
| **AD-91** | Confidence runtime-computed & outcome-calibrated, not model self-report | Honest uncertainty (INV-6); models are overconfident | Use model self-confidence (rejected: miscalibrated) |
| **AD-92** | Model routing is governed, provider-abstracted config | Swap model/provider without touching domain/contracts | Hard-wired model (rejected: lock-in) |
| **AD-93** | Prompts/models/datasets are versioned governed artifacts; never rules/code | Reproducibility; safe evolution; a prompt is never an invariant | Ad-hoc prompts in code (rejected: drift, un-auditable) |
| **AD-94** | AI results cached by content-hash as pure optimization, never authoritative | Dominant cost lever, safe because capabilities are pure | Cache as source of truth (rejected: violates AD-56) |
| **AD-95** | Provenance (model+prompt+calibration version) mandatory on every proposal | Reproducibility, regression tracing, explainability | Untracked outputs (rejected: unexplainable, un-auditable) |
| **AD-96** | AI cost is a first-class control; over-budget degrades, never drops | Dominant cost center managed without harming candidates | Uncontrolled spend (rejected: runaway cost) / silent drop (rejected: DOC-06) |
| **AD-97** | Prompt/model changes gated by offline Model Quality Harness (quality + fairness) vs golden datasets | Improve without silent quality/fairness regression | Ship-and-observe (rejected: fairness/quality risk in prod) |
| **AD-98** | Orchestration deterministic; model reasoning the single opaque step | Any run-to-run difference is attributable to a named variable, never the pipeline | Nondeterministic orchestration (rejected: un-debuggable, un-auditable) |

## 17. Open Questions

1. **Confidence calibration at MVP without outcomes:** how good can evidence-coverage heuristics be before Outcome Learning exists? What's the honest floor below which we *always* escalate?
2. **Golden dataset bootstrapping:** how do we build a representative, consented, fair golden dataset for the Model Quality Harness before we have design-partner outcome data (AS-21 dependency)?
3. **Structured-output enforcement mechanism:** provider-native constrained decoding vs. schema-validate-and-retry vs. tool-use forcing — per provider, behind the ACL.
4. **PII-minimization fidelity vs. signal loss:** how aggressively can we strip identity before evaluation quality degrades? Needs measurement.
5. **Multi-provider quality parity:** can failover targets meet the judgment-quality bar, or is failover "degraded mode → escalate more"?
6. **Fairness signals vs. verdict boundary:** exactly what the AI computes vs. what the Fairness Service decides (carried; confirm with the fairness methodology owner).
7. **Prompt/model canary metrics:** which online signals safely gate promotion without exposing candidates to an under-tested version?

## 18. Risks

- **Betraying the cardinal rule under pressure:** a shortcut that lets an AI output flow through as a fact. *Mitigation:* AD-88 + capability contracts (AD-56) + owner-commits-fact (AD-35/47); structurally no `Decide`/`PassGate` capability exists.
- **Overconfidence / miscalibration:** confident wrong answers erode trust (RK-1/RK-15). *Mitigation:* AD-91 runtime calibration + escalate-on-low-confidence + override-rate monitoring.
- **Hallucinated evidence/citations:** ungrounded judgment. *Mitigation:* AD-90 grounding + hard-reject invented citations.
- **PII leakage to provider:** existential (RK-6/RK-9). *Mitigation:* AD-89 dual enforcement (in-process + egress gateway AD-83); no raw PII in logs.
- **Prompt/model regression:** a "better" prompt that's worse or less fair. *Mitigation:* AD-97 offline harness with fairness thresholds + canary.
- **Cost runaway:** the dominant cost center. *Mitigation:* AD-96 tiering/caching/budgets/back-pressure; cost observability (§14).
- **Provider dependency/outage:** external reliance. *Mitigation:* multi-provider failover (§8), fail-soft to human, caching.
- **Terminology corruption:** "eval harness" colliding with domain "Evaluation." *Mitigation:* the Model Quality Harness naming guard (§0/§15) — governance-enforced (ARCH-15).
- **Fairness-at-the-model vs fairness-gate confusion:** teams thinking the AI "does fairness." *Mitigation:* AI produces *signals*; Fairness Service owns the *verdict* (§1/§8).

## 19. Deferred

- **To Evaluation Engine doc:** the detailed judgment logic, rubric design, dimension scoring methodology, and prompt engineering for the Structured Work Sample (AD-10) — the *content* of evaluation, distinct from this *runtime*.
- **To ARCH-12 (Operational):** Model Quality Harness operations, golden-dataset curation cadence, model/prompt release process, AI FinOps, on-call for AI degradation, escalation-queue operations.
- **To ARCH-13 (Security):** AI-specific threat model (prompt injection, data exfiltration via prompts, model supply-chain), provider data-processing agreements.
- **To ARCH-14 (Observability):** the concrete AI telemetry pipeline, dashboards, drift alerting, override/confidence dashboards.
- **To ARCH-15 (Governance):** prompt/model/dataset review board, change-approval workflow, versioning policy for AI artifacts, the AI governance lifecycle.
- **Deferred capabilities:** Embed, vector/feature stores, Hiring Memory retrieval, Benchmarking, Outcome-calibrated confidence — reserved (§9/§10), built post-MVP on the existing fact stream.

---

*End of ARCH-11 v0.1 — the AI Runtime Architecture. The AI layer produces high-quality, PII-minimized, schema-validated, evidence-grounded, honestly-calibrated **proposals** through a fixed inference pipeline, with model/prompt/dataset governance and first-class human escalation — and it remains architecturally incapable of producing a business fact or deciding anything (AD-88). The cardinal rule holds: the AI proposes; the domain decides. Next: ARCH-12 — Operational Architecture (runbooks, DR drills, FinOps, key-rotation/crypto-shred procedures, SLOs, and the operations of the Model Quality Harness).*
