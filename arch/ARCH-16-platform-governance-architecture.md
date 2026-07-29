# ARCH-16 — Platform Governance Architecture

| Field | Value |
|---|---|
| **Document ID** | ARCH-16 |
| **Title** | Platform Governance Architecture (governing the architecture itself) — **the capstone** |
| **Owner** | Chief Architect + Architecture Review Board + Principal Engineers (platform, contracts, data, security) |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture (governance) — **final architecture document** |
| **Depends on** | ARCH-01→15 (the entire corpus), DOC-04 (ubiquitous language), DOC-05 (Constitution) |
| **Blocks** | **Architecture Freeze → SPRINT-0 → implementation** |
| **The one question** | **"Who owns the architecture's evolution, and how does it change over years without losing the coherence and derivation-integrity that make it work?"** |
| **The reflexive point** | The discipline that kept all 16 documents coherent — **strict derivation + explicit, numbered decisions** — must itself be governed, or it erodes the moment implementation pressure arrives. This document governs that discipline. |
| **Scope** | Governance of the architecture itself: ADR lifecycle, the Architecture Review Board, contract/schema evolution, compatibility & deprecation, repository strategy, technology adoption/retirement, the Trust Assumptions Register, ubiquitous-language governance, and the interface with AI Governance (ARCH-15). |

---

## 0. Platform Governance Philosophy

Sixteen documents cohere because of two habits: **every decision derived from the one before it** (never a parallel concept), and **every consequential choice was made explicit and numbered** (AD-01…AD-134). Those habits are the reason the corpus is a *system* and not a pile. But habits decay under pressure — a deadline, a new hire, a "just this once" hotfix. Platform Governance exists to make those habits **institutional**: to ensure the architecture keeps deriving, keeps recording its decisions, and keeps its language and contracts coherent for years.

> ### AD-135 — The architecture is a living system that changes only through governed decisions. Ad-hoc architectural change is prohibited; coherence is maintained by governance, not by hope.
> Post-freeze, no service boundary, contract, schema, domain term, gate, or ADR changes except through the governed process (ADR + Architecture Review Board). The corpus is *living* — it will evolve — but every evolution must still **derive** from what precedes it and be **recorded**. Governance's job is to protect derivation-integrity: a change that introduces a parallel concept instead of deriving from the existing model is rejected on principle, not on taste.

> ### AD-144 — Governance itself is versioned and auditable (extends AD-130 to platform governance).
> Just as AI-governance decisions are versioned artifacts (AD-130), platform-governance decisions — ADR acceptances, ARB rulings, compatibility-policy changes, deprecations, technology adoptions/retirements — are versioned, dated, attributed, and supersession-tracked. The governance record is as reconstructable as the business record (AD-32) and the operational record (AD-106). *Nothing about how this platform is governed is undocumented.*

---

## 1. Scope & the Two-Governance Model

Two governance functions, cleanly separated, with a defined interface (§10):

| | **AI Governance (ARCH-15)** | **Platform Governance (ARCH-16)** |
|---|---|---|
| **Governs** | the AI *lifecycle* | the *architecture* itself |
| **Artifacts** | prompts, models, datasets, calibration, fairness thresholds, providers | ADRs, contracts, schemas, service boundaries, domain terms, tech choices, repo, trust assumptions |
| **Body** | AI Governance Board + Fairness Review Board | **Architecture Review Board (ARB)** |
| **Question** | how is the AI allowed to evolve? | how is the architecture allowed to evolve? |
| **Cannot** | touch domain/contracts/gates (AD-127) | force-pass a gate or edit a business rule (defers to the domain/Constitution) |

Neither governs the **business rules** themselves — those belong to the domain (DOC-04 term owners, DOC-05 Constitution). Governance protects and evolves the *architecture that serves* the business; it never re-authors the business.

---

## 2. ADR Lifecycle & the Decision Record

The numbered AD-xx log we have used throughout **is** the authoritative architectural decision record. ARCH-16 formalizes it.

> ### AD-136 — The ADR is the atomic unit of architectural decision. ADRs are immutable and versioned; a decision is *superseded*, never edited. The AD-xx log is the single authoritative decision record.
> Every consequential architectural choice is an ADR with: **decision, rationale, alternatives considered, consequences, status, and (if applicable) supersession pointer.** An ADR is never rewritten; a changed decision is a *new* ADR that supersedes the old (which is retained — mirrors DOC-04 term lifecycle and AD-133 artifact retention). This is why any past state of the architecture is reconstructable.

| ADR lifecycle stage | Meaning |
|---|---|
| **Proposed** | drafted; under ARB review |
| **Accepted** | ratified by the ARB; in force |
| **Superseded** | replaced by a newer ADR (pointer retained) |
| **Deprecated** | no longer applies; retained for history |

**Proposal → acceptance flow:** RFC/ADR drafted → derivation-integrity check (does it *derive*, or introduce a parallel concept?) → ARB review → accept/reject/revise → recorded (AD-144). Emergency ADRs may be fast-tracked but are reviewed post-hoc.

---

## 3. The Architecture Review Board (ARB)

| Concern | Decision |
|---|---|
| **Authority** | The ARB owns the architecture corpus (ARCH-01→16) and the ADR log. Substantive architectural change requires an ADR reviewed by the ARB. |
| **Membership** | Chief Architect + principal engineers across platform, contracts, data, security, AI; product + compliance consulted for cross-cutting changes. |
| **What requires ARB review** | New/changed service boundary; new/breaking contract or schema; new domain term or gate change; new persistence responsibility; technology adoption/retirement; trust-assumption change; any change touching a Tier-0 gate. |
| **What does NOT** | Routine within-boundary implementation; additive backward-compatible contract changes (governed by policy §4/§5, not per-change ARB); low-risk config. |
| **Cadence** | Regular review + async for low-risk; emergency path for incidents (post-hoc ratification). |
| **The ARB's prime directive** | **Protect derivation-integrity.** A change is judged first on "does it derive from and stay consistent with the corpus?" — not merely "is it a good idea in isolation?" |

> ### AD-139 — The Architecture Review Board owns the corpus and is the steward of derivation-integrity. A change that introduces a parallel concept instead of deriving from the existing model is rejected as an architectural regression, regardless of local merit.

---

## 4. Contract & Schema Evolution Governance

Governs the evolution of ARCH-07 contracts and ARCH-09 specifications.

| Concern | Decision |
|---|---|
| **Registry ownership** | The contract/schema registry (ARCH-09 §5) is ARB-governed; every contract has an owning service (ARCH-07) and a lifecycle status. |
| **Additive by default** | Backward-compatible additive changes flow under policy (tolerant readers, ARCH-07 AD-54) without per-change ARB. |
| **Breaking changes** | Require ARB approval + a new parallel major running until consumers migrate (ARCH-07 §6); consumer-driven contract tests (AD-55) + drift-check (AD-75) gate them in CI. |
| **Spec-as-projection** | ARCH-09 specs remain generated projections (AD-70); a spec edit that isn't a projection of a contract is a governance violation caught by drift-check. |
| **Single source of truth** | The Business→Contract→Spec→Code chain is enforced: contracts derive from ARCH-04/05, specs project from contracts, code generates from specs. Governance guards each arrow. |

> ### AD-138 — Contract and schema evolution is centrally governed (registry + compatibility policy + consumer-driven tests + drift-check). Breaking changes require ARB approval and a parallel-major migration; the projection chain is never bypassed.

---

## 5. Backward Compatibility & Deprecation Policy

| Concern | Decision |
|---|---|
| **Compatibility contract** | Within a major version: additive-only, tolerant readers, no field removal/semantic change (ARCH-07 §6). |
| **Deprecation lifecycle** | Stable → Deprecated (superseded-by pointer + sunset window) → Retired — mirroring DOC-04 term lifecycle and ARCH-15 AD-133 artifact retention. |
| **Sunset windows** | Deprecated contracts/specs run in parallel for a defined window; removal only after all registered consumers migrate (consumer registry). |
| **No silent breaks** | A breaking change without a parallel-major + migration path is prohibited (governance-enforced in CI + ARB). |
| **Retention** | Retired contract/schema versions are retained for reproducibility (a past interaction remains interpretable) — the reproducibility principle applied to interfaces. |

---

## 6. Repository Governance

> ### AD-137 — Repository strategy: a monorepo hosting all services, contracts, specifications, and infrastructure-as-code — with services remaining independently deployable (ARCH-06).
> **Monorepo + microservices** (not a contradiction): one repository so that a cross-cutting change — a contract + its spec + its consumers + its tests — is an **atomic, reviewable commit**, and the Business→Contract→Spec→Code chain (AD-70/AD-138) is enforced in one place with one CI. Yet each service is independently *deployable* (ARCH-06 AD-40) and independently *ownable* (CODEOWNERS). *Rationale:* the monorepo is how derivation-integrity is mechanically enforced (a contract change and its projections travel together); independent deployability is preserved by build/deploy tooling, not by repository fragmentation. *(This is a platform-governance decision, not a domain one — AD-77/AD-78 hold: the repo is infrastructure for coherence, replaceable in mechanism, fixed in responsibility.)*

| Concern | Decision |
|---|---|
| **Ownership** | CODEOWNERS maps directories → owning teams (mirrors service/aggregate ownership, ARCH-03/06). |
| **Generated code** | Generated from specs (AD-70); generation is CI-enforced and never hand-edited (drift-check). |
| **Cross-cutting change** | Atomic commits across contract + spec + consumers + tests; ARB-reviewed when boundary/contract-breaking. |
| **Contracts & IaC in-repo** | Contracts, schemas, IaC, and policies live alongside code so the whole system is versioned together and auditable (echoes P8). |

---

## 7. Technology Adoption & Retirement

Exercises the replaceability principles (AD-78 products, AD-87 platform interfaces) through governance rather than ad hoc drift.

| Concern | Decision |
|---|---|
| **Adoption** | A new technology enters via RFC/ADR: what responsibility it serves (must map to an existing architectural responsibility — AD-77), what it replaces, trial/spike results, exit strategy. ARB-approved. |
| **Retirement** | A technology is retired deliberately (migration plan, parallel run, cutover); the responsibility it served is re-homed to its replacement behind the same platform interface (AD-87). |
| **Platform-interface catalog** | The platform interfaces (AD-87: event backbone, cache, search, secrets, etc.) are an ARB-owned catalog; application services depend on interfaces, so a product swap is a platform-team change, not an app change. |
| **No responsibility drift** | A technology change may never change a *responsibility* (AD-78) — only its implementation. The ARB enforces this. |

> ### AD-140 — Technology adoption and retirement are governed exercises of the replaceability principles (AD-78/AD-87), owned by the ARB. A product may be swapped; a responsibility may not drift.

---

## 8. Trust Assumptions Register Ownership

Building on ARCH-13 AD-119:

| Concern | Decision |
|---|---|
| **Ownership** | The Trust Assumptions Register (KMS, IdP, SPIFFE CA, K8s control plane, managed data services, time sync, crypto primitives, WORM audit) is **ARB + security-owned**. |
| **Change triggers review** | Any change to a root of trust (new KMS, new IdP, CA migration, provider change) triggers a **targeted security + architecture re-review** of exactly the guarantees that depend on it (AD-119). |
| **Periodic review** | The register is reviewed on a cadence, not only on change — assumptions can silently become false (a deprecated crypto primitive, a provider policy change). |
| **Versioned** | Register changes are versioned governance decisions (AD-144). |

---

## 9. Ubiquitous Language Governance

The entire corpus rests on DOC-04's frozen vocabulary. Sustaining that freeze is platform governance.

> ### AD-142 — Ubiquitous-language governance is platform governance. The DOC-04 terminology freeze is ARB-enforced: a new business term or a changed meaning requires a formal DOC-04 amendment, and no contract, schema, service, event, prompt, or UI may introduce a synonym or redefine a term.
> This extends the DOC-04 freeze (and its Term Registry with owner + lifecycle) into the architecture/implementation era. A forbidden synonym in a contract name, a schema field, an event, or a prompt variable is a **defect** the drift-check and ARB reject. Language coherence is the substrate of everything; governing it is non-negotiable. *(The Model Quality Harness naming guard — "not eval harness" — ARCH-11, is an instance of this governance.)*

---

## 10. The AI-Governance ↔ Platform-Governance Interface

Where the two functions meet, ownership is explicit to prevent gaps and turf.

| Shared/overlapping artifact | Primary owner | Consulted | Rule |
|---|---|---|---|
| **Model routing policy** (an AI artifact *and* a config artifact) | AI Governance (it decides which models) | Platform (config mechanism) | AI-Gov decides *what*; Platform-Gov governs *how it's expressed/deployed* |
| **A schema change affecting an AI capability contract** | Platform Governance (it's a contract/schema) | AI Governance | ARB owns the contract; AI-Gov consulted for AI-quality impact |
| **PII-minimization pipeline change** | shared | security | Platform (pipeline) + AI-Gov (what's minimized) + Security (ARCH-13) |
| **A fairness-threshold change that requires a schema/contract field** | AI Governance (the threshold) + Platform (the field) | — | AI-Gov owns the policy; ARB owns the contract change enabling it |
| **Escalation between boards** | — | — | Cross-cutting decisions with both AI-lifecycle and architectural impact go to a **joint review** (ARB + AI Governance Board) |

> ### AD-141 — The two-governance model is explicit. AI Governance owns the AI lifecycle; Platform Governance owns the architecture. Shared artifacts have a defined primary owner and consulted party; genuinely cross-cutting decisions get a joint ARB + AI-Board review. No governance gap, no turf war.

---

## 11. Governance of Governance *(the meta-layer)*

| Concern | Decision |
|---|---|
| **Policy change** | Governance policies themselves (compatibility policy, ADR process, review cadence) change only via a governance ADR — governance eats its own dog food. |
| **Versioned** | All governance decisions versioned/attributed (AD-144). |
| **Auditable** | The governance record shares the immutability/reproducibility discipline of the rest (AD-32/106/130/133). |
| **Review of governance** | Periodic retrospective: is governance protecting coherence, or becoming bureaucracy? Risk-tiered depth (like ARCH-15 §10) keeps low-risk fast and only high-risk heavy. |

---

## 12. Architecture Freeze & Change After Freeze

> ### AD-143 — The corpus (ARCH-01→16 + foundational DOC/VALIDATION/PRODUCT documents) is frozen as the architectural baseline. Freeze enables SPRINT-0. Post-freeze change is governed-only (ADR + ARB), never ad hoc.
> **"Freeze" does not mean "immutable forever"** — it means the corpus is coherent, complete, and the **stable baseline** against which implementation proceeds. It will evolve, but only through the governed process (§2/§3), so evolution preserves coherence. Freeze is the signal that **discovery is done and construction may begin** — implementation builds on a foundation that won't shift under it without deliberate, recorded, reviewed decision.

**What changes after freeze, and how:**
- A learning from the pilot (VALIDATION program) that contradicts an assumption → an ADR + possibly a DOC amendment → ARB review → recorded.
- A new capability (Hiring Memory, Benchmarking) → derives from existing facts/services (ARCH-06 §14) → ADR → ARB.
- A technology swap → §7 governance.
- **Never:** a boundary/contract/term/gate changed in code without a corresponding governed decision.

---

## 13. Corpus Completeness

The architecture corpus is **complete**. The full derivation chain, each layer deriving from the last:

```
 DOC-01 Vision → DOC-02 Problem → DOC-03 Strategy → DOC-04 Ubiquitous Language (frozen)
   → DOC-05 Constitution → DOC-06..12 (Manifesto, Philosophy, Personas, JTBD, Blueprint, Journey, Capability Map)
     → VALIDATION-01..03 (assumptions, risks, research)  → PRODUCT-01 (MVP)
       → ARCH-01 Context → 02 Business Architecture → 03 Canonical Domain → 04 Interactions
         → 05 Business Events → 06 Distributed System → 07 Interface Contracts → 08 Persistence
           → 09 Interface Specifications → 10 Deployment → 11 AI Runtime → 12 Operational
             → 13 Security → 14 Observability → 15 AI Governance → 16 Platform Governance (this)
```

| Layer | Documents | What it fixes |
|---|---|---|
| **Business** | DOC-01→12 | what is true, valuable, principled |
| **Validation** | VALIDATION-01→03 | what must be proven |
| **Product** | PRODUCT-01 | the smallest thing to build |
| **Domain & interaction** | ARCH-03/04/05 | meaning, choreography, facts |
| **System** | ARCH-01/02/06 | context, responsibilities, services |
| **Contracts & data** | ARCH-07/08/09 | how components talk, what's authoritative, concrete specs |
| **Runtime** | ARCH-10/11 | where it runs, how AI is constrained |
| **Assurance** | ARCH-12/13/14 | operability, security, observability |
| **Governance** | ARCH-15/16 | how AI and architecture evolve |

**The invariants that thread all of it** (traceable end-to-end): the AI proposes and the domain decides; gates fail closed and are unbypassable across four independent layers (contract, surface, network, authorization); every action is single-tenant, consented, audited, and human-accountable where it must be; facts are immutable and the source of truth; everything else is derived and rebuildable; compliance is emergent; and every technology is replaceable behind a stable responsibility.

> **The corpus stops here.** ARCH-16 is the final architecture document. There is no ARCH-17: the architecture is coherent, bounded, and complete. What remains is construction.

---

## 14. Architecture Decisions *(continuing the log; ARCH-15 ended at AD-134)*

| ID | Decision | Rationale |
|---|---|---|
| **AD-135** | Architecture is a living system changed only through governed decisions; ad-hoc change prohibited | Coherence maintained by governance, not hope |
| **AD-136** | The ADR is the atomic decision unit; immutable, versioned, superseded-not-edited; the AD-xx log is authoritative | Any past architectural state reconstructable |
| **AD-137** | Monorepo hosting services + contracts + specs + IaC; services independently deployable | Atomic cross-cutting change enforces the derivation chain; deployability preserved by tooling |
| **AD-138** | Contract/schema evolution centrally governed; breaking = ARB + parallel-major; projection chain never bypassed | Safe interface evolution without drift |
| **AD-139** | ARB owns the corpus and stewards derivation-integrity; parallel-concept changes rejected | Protect the property that makes the corpus a system |
| **AD-140** | Technology adoption/retirement is governed replaceability (AD-78/AD-87); product swaps, responsibilities don't drift | Replaceability exercised deliberately, not by drift |
| **AD-141** | Two-governance model explicit (AI-Gov vs Platform-Gov) with defined interface + joint review | No governance gap, no turf war |
| **AD-142** | Ubiquitous-language governance is platform governance; DOC-04 freeze ARB-enforced | Language coherence is the substrate of everything |
| **AD-143** | Corpus frozen as baseline; freeze enables SPRINT-0; post-freeze change is governed-only | Discovery done; construction may begin on stable ground |
| **AD-144** | Governance itself is versioned and auditable (extends AD-130) | Nothing about how the platform is governed is undocumented |

## 15. Open Questions

1. **ARB composition & cadence at startup scale** — how heavyweight before it becomes a bottleneck (AD-41 team-size reality); likely lightweight + risk-tiered initially.
2. **AI-Board / ARB overlap in practice** — early on the same people may sit on both; when to formally separate (§10).
3. **Monorepo tooling** — build/deploy system that gives monorepo coherence *and* independent deployability at scale (Bazel/Nx/Turborepo-class) — a SPRINT-0 selection.
4. **Post-freeze amendment threshold** — what magnitude of pilot learning triggers a DOC amendment vs. a local ADR.
5. **External architecture review** — whether/when to bring independent architectural audit (parallels external bias audit, ARCH-15).

## 16. Risks

- **Governance as bureaucracy:** heavy process slowing a small team. *Mitigation:* risk-tiered depth (low-risk fast, only high-risk heavy); §11 governance-of-governance retrospective.
- **Derivation-integrity erosion under delivery pressure:** parallel concepts sneaking in. *Mitigation:* AD-139 ARB prime directive + monorepo atomic review (AD-137) + drift-check.
- **Governance gap between AI-Gov and Platform-Gov:** an artifact nobody owns. *Mitigation:* AD-141 explicit ownership + joint review.
- **Freeze misread as "immutable":** teams afraid to evolve, or evolving in code without governance. *Mitigation:* AD-143 clarifies freeze = governed evolution, not stasis.
- **Language drift in code:** synonyms creeping into fields/prompts. *Mitigation:* AD-142 + drift-check + ARB.
- **Trust-assumption blind spot:** a root of trust silently becoming false. *Mitigation:* AD-119/§8 periodic register review.

## 17. Deferred → Transition to SPRINT-0

With the corpus frozen (AD-143), the remaining work is **construction**, not architecture:

- **Evaluation Engine detail** — the judgment logic/rubric for the Structured Work Sample (deferred from ARCH-11) — a build-time design within the frozen architecture.
- **Engineering Standards** — coding standards, testing strategy, CI gates — consume ARCH-16 governance.
- **SPRINT-0** — monorepo + tooling (AD-137), CI/CD, generated APIs from specs (AD-70), database migrations from persistence responsibilities (ARCH-08), platform-interface scaffolding (AD-87), observability/security baselines.
- **Then:** backend → frontend → AI runtime integration → testing → **pilot** (with 2–3 design partners, running the VALIDATION program against real outcomes — AS-1).

All of it builds on a foundation that will not shift without a deliberate, recorded, reviewed decision.

---

*End of ARCH-16 v0.1 — the Platform Governance Architecture, and the capstone of the corpus. The architecture now governs its own evolution: the ADR is the atomic decision unit (AD-136), the ARB stewards derivation-integrity (AD-139), contracts/schemas/language/technology evolve only under governance (AD-138/AD-140/AD-142), the two governance functions interface cleanly (AD-141), and governance itself is versioned and auditable (AD-144). The corpus — DOC-01→12, VALIDATION-01→03, PRODUCT-01, ARCH-01→16 — is coherent, bounded, and **complete**. There is no ARCH-17. Recommendation: **freeze the architecture (AD-143) and begin SPRINT-0.***
