# ARCH-12 — Operational Architecture

| Field | Value |
|---|---|
| **Document ID** | ARCH-12 |
| **Title** | Operational Architecture (running the platform reliably for years) |
| **Owner** | Principal SRE + Platform Operations Architect + Security Architect + AI Operations lead |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture (operations) |
| **Depends on** | ARCH-10 (deployment), ARCH-11 (AI runtime), ARCH-08 (persistence/recovery), ARCH-06 (availability tiers/failure doctrine), DOC-05 (gates), DOC-06 (no-black-hole) |
| **Blocks** | ARCH-13 (Security), ARCH-14 (Observability), ARCH-15 (AI Governance), ARCH-16 (Platform Governance), SPRINT-0 |
| **The one question** | **"How is the platform operated so it stays reliable, recoverable, affordable, and *principle-preserving* under real-world stress — for years?"** |
| **Scope** | Operational procedures and models. Consumes the technology of ARCH-10/11; does **not** re-decide architecture. Security controls → ARCH-13; telemetry pipeline → ARCH-14; governance boards → ARCH-15/16. |

---

## 0. Operational Philosophy

Operations is where architecture meets entropy. Every prior document made a promise (gates hold, facts are immutable, tenants are isolated, the AI proposes and the domain decides); ARCH-12 exists to keep those promises true when a node dies at 3am, a provider degrades, a cost spikes, or an engineer is under pressure to "just ship the fix."

> ### AD-99 — Operations preserve architectural invariants under stress. No operational action may bypass a gate, mutate an immutable fact, cross a tenant, or let the AI decide.
> Incident mitigation, hotfixes, scaling, and break-glass access are all **gate-preserving and audited**. There is **no** operational escape hatch that turns a fairness hold into a pass, edits an audit record, or auto-finalizes a decision. If the only way to mitigate an incident appears to violate an invariant, the correct action is to **hold/degrade** (ARCH-06 §9), not to breach the invariant. *The platform is allowed to be slower or more manual under stress; it is never allowed to be wrong or unfair.*

Two doctrines carried from architecture into operations:
- **Fail-closed gates / fail-soft intelligence** (ARCH-06 AD-24) is also the *operational* posture: when in doubt, gates hold and intelligence escalates to humans.
- **The cluster is disposable; truth is not** (ARCH-10 AD-81): recovery is *rebuild + replay*, routinely drilled, not a theoretical last resort.

---

## 1. Service Levels — SLIs, SLOs, Error Budgets

SLOs are tiered to the ARCH-06 availability classes and include **business** SLOs, not just technical ones.

| Tier / service | Example SLI | Target SLO (illustrative) | Error budget |
|---|---|---|---|
| **Critical — gates** (Consent/Integrity/Fairness/Audit), Decision | gate-check availability; audit-write success | 99.95% avail; **100% audit durability** | very small; audit budget effectively zero |
| **High — core flow** (Candidate/Campaign/Evaluation) | request success; time-to-recommendation | 99.9% | moderate |
| **Standard** (Feedback/Export/Notification/Intelligence Compute) | success; latency | 99.5% | larger (fail-soft absorbs) |
| **Business SLOs** | evaluation completion rate; **held-candidate resolution time**; feedback-release latency; candidate completion rate | targets set with product | — |

**Error-budget policy:**
> ### AD-100 — Error-budget policy governs release velocity; a Critical/gate service that exhausts its budget freezes feature releases until reliability recovers.
> Reliability is a feature, especially for gates. Burning a gate's budget halts new features to that service (reliability work only) until it recovers. Audit has effectively **zero** budget for lost records (a lost audit record is a Tier-0 incident, not a budget spend).

**Business-health as a paging signal:**
> ### AD-105 — Business-health conditions page like technical ones. A candidate stuck "held," a stalled campaign, or a dead-lettered gate fact is a first-class alert — no silent black holes (DOC-06).
> Technical green ≠ business healthy. A perfectly-available system that has left 40 candidates silently held is *failing* the product's promise. Operational alerting watches business progression, not just RED metrics.

---

## 2. Incident Response & Runbooks

| Concern | Decision |
|---|---|
| **Severity levels** | **SEV-1** existential/Tier-0 (tenant leak, PII exposure, audit loss, a gate bypassed, wrong/unfair output shipped) · **SEV-2** major (Critical service down, widespread held candidates) · **SEV-3** degraded (elevated errors, AI degradation) · **SEV-4** minor. **Any suspected gate bypass or tenant/PII leak is automatically SEV-1**, regardless of blast radius. |
| **Incident lifecycle** | detect → declare → triage → mitigate (**gate-preserving**, AD-99) → resolve → **blameless PIR** (§12). |
| **Runbook catalog** | Per Critical service + per common failure. Every runbook states the **principle-preserving** mitigation (e.g., "Fairness Service down → recommendations **hold**, do not deliver; escalate; never manually pass"). |
| **Gate-specific runbooks** | Consent/Integrity/Fairness/Audit each have a runbook whose first rule is *fail closed*: the mitigation is to hold/degrade, never to disable the gate to "unblock." |
| **LLM/AI incident runbook** | Provider outage/degradation → failover (ARCH-11 §8) → if none, **fail soft to human**; cost spike → tiering/back-pressure (ARCH-11 §13); quality/fairness regression → rollback prompt/model (§9). |
| **Communication** | Internal incident channel + status; customer comms for SEV-1/2 per contract; candidate-facing comms preserve dignity (DOC-06). |

> ### AD-101 — Every Critical/gate service has a written runbook and a rehearsed failure drill before GA (an ORR gate, §11). An un-drilled Critical failure mode is treated as unhandled.

---

## 3. On-Call & Escalation

| Concern | Decision |
|---|---|
| **Rotation** | Follow-the-sun where staffing allows; a primary + secondary; humane rotation (sustainable, small team — AD-41 reality). |
| **Escalation ladder** | On-call → service owner → architecture owner → security/exec for SEV-1. **Security is paged immediately** for any tenant/PII/audit incident. |
| **Ownership** | Each service (ARCH-06) has a named owning team; each runbook names its owner (mirrors DOC-04/ARCH-07 ownership discipline). |
| **Alert routing** | Technical alerts → service on-call; **business-health alerts (AD-105)** → service on-call **and** product/CS (a stuck candidate is a customer-experience incident). |
| **Break-glass** | Emergency elevated access is time-boxed, requires a second approver, and is **fully audited** (AD-99); break-glass can never grant the ability to bypass a gate, mutate audit, or cross tenants — it grants *operational* access, not *invariant-breaking* access. |

---

## 4. Release Management

| Concern | Decision |
|---|---|
| **Change classes** | Code deploy · config change · **contract version** (ARCH-07/09) · **prompt/model** (ARCH-11) · infra change. Each has a defined pipeline. |
| **Contract-version rollout** | Old + new majors run in parallel (ARCH-07 §6) until consumers migrate; consumer-driven contract tests (AD-55) + drift-check (AD-75) gate the release. |
| **Prompt/model promotion** | The AI release pipeline (§9): Model Quality Harness gate (AD-97) → canary → monitored promotion → auto-rollback on quality/fairness regression. |
| **Change management** | Low-risk changes flow continuously (GitOps); **gate/Critical and prompt/model changes require review** and the most conservative rollout (ARCH-10 §7). |
| **Operational Readiness Review** | New services/major changes pass an ORR (§11) before GA. |
| **Freeze conditions** | Error-budget exhaustion (AD-100) or an active SEV-1 freezes non-reliability releases to the affected scope. |

---

## 5. Deployment Operations

| Concern | Decision |
|---|---|
| **GitOps workflow** | Argo CD reconciles declared state (ARCH-10); no manual cluster mutation; all changes are versioned and auditable (echoes P8). |
| **Canary promotion criteria** | Automated analysis on RED + **business + fairness** metrics (held rate, override rate) before each promotion step; gates use the smallest, strictest steps. |
| **Rollback** | Argo Rollouts abort + GitOps revert. Because facts are immutable and read models are rebuildable (ARCH-08), rolling back *compute* never corrupts *truth*. |
| **Cluster rebuild + replay drill** | The disposable-cluster model (AD-81) is **routinely exercised**: tear down and rebuild a cluster, reconnect to managed data, replay to rebuild derived stores, verify. A rebuild path that isn't drilled is not trusted. |
| **Config & secrets** | Per-env overlays; secrets via ESO/Vault; rotation on schedule (§8). |

---

## 6. Backup & Restore Procedures

| Store | Backup | Restore procedure | Verified? |
|---|---|---|---|
| Aurora PostgreSQL (transactional + authoritative event streams) | continuous + PITR | restore to point-in-time; reconnect services | **restore-tested on schedule** |
| Kafka/MSK (fact backbone) | tiered storage + replication | restore stream; consumers resume from offsets | tested |
| S3 (files + WORM audit) | versioning + cross-region replication; Object Lock (WORM) | restore/replicate; WORM immutable | tested |
| OpenSearch / read models | **not backed up — rebuilt** | drop + **replay from fact log** (ARCH-08 AD-65) | rebuild-drilled |
| Redis caches | not backed up | warm from source on cold start | n/a |

> **Principle:** authoritative stores are backed up; **derived stores are rebuilt, not restored** (replay). A restore is consistent because authoritative sources are restored first, then derived stores reprojected (ARCH-08 §10). **Untested backups are treated as no backups** — restore is drilled, not assumed.

---

## 7. Disaster Recovery Execution

| Concern | Decision |
|---|---|
| **DR model** | Cross-region: Aurora + S3 replicated; Kafka MirrorMaker; per-tenant keys available in-region (AD-84). Single-region MVP (AD-86) with a documented, drilled cross-region recovery path. |
| **Failover runbook** | Declared DR event → promote replica region → reconnect services → **replay to rebuild derived stores** → validate business health → cut traffic. RPO/RTO per tier (ARCH-08 AD-69). |
| **The replay superpower** | Recovery centers on the immutable fact log: authoritative state restored, then read models/search/AI-derived stores **regenerated by replay** — not restored independently to a divergent point. |
| **Game-days** | Scheduled DR game-days (region loss, backbone loss, gate-service loss, provider outage). |

> ### AD-104 — DR is validated by scheduled game-days; an untested DR plan is treated as no DR plan.

---

## 8. Data Lifecycle Operations

Operationalizes ARCH-08 §11 and the crypto-shred/key model (AD-64/68).

| Operation | Procedure |
|---|---|
| **Retention enforcement** | Scheduled CronJobs expire data at policy windows (ARCH-05 §10.3); expirations are audited. |
| **Legal hold** | Hold flag **suspends** expiration/deletion for its scope; takes precedence; auditable; released only by authorized governance. |
| **Consent-expiry sweeps** | Scheduled job detects expired consent → halts further use → triggers crypto-shred of the subject's PII per policy. |
| **Crypto-shred execution** | On erasure/withdrawal: destroy the subject's per-subject key across **all** stores/caches/indices; **verify** unrecoverability (the shred is "done" only when verified, incl. derived stores). |
| **Key rotation** | Scheduled rotation of envelope/data keys (KMS); per-tenant CMK rotation; rotation is zero-downtime (envelope re-wrap) and audited. |
| **Cold-tiering** | Aged facts/files tiered to cheaper storage, still readable; **never compacted away** (ARCH-08 AD-63). |

> ### AD-102 — Crypto-shred and key-rotation are audited, verifiable procedures with completion proofs. A shred is complete only when unrecoverability is verified across authoritative *and* derived stores (caches, indices, embeddings).
> This closes the AD-64 discipline gap operationally: erasure isn't "we deleted the key" — it's "we verified no readable copy survives anywhere," including AI-derived embeddings/features.

> ### AD-106 — Operational actions are replayable: every consequential operational action leaves a structured, attributable trail alongside the business fact history.
> Just as business events are immutable and replayable (ARCH-05), consequential **operational** actions — restore executed, replay initiated, crypto-shred performed, emergency rollback, prompt/model promotion, key rotation, DR failover, break-glass access — each record **operator · timestamp · reason · linked incident/change · verification result**. *Rationale:* this gives a complete **operational history** running parallel to the business history, so any incident, audit, or compliance review can reconstruct not just *what the business did* but *what operators did to the system and why* — with the same immutability and attributability. It is the operational analog of AD-95 provenance, and it feeds directly into PIRs (§12) and compliance evidence (→ ARCH-13). *(The operational trail is itself tenant-scoped and, for actions touching a tenant's data, contributes to that tenant's audit.)*

---

## 9. AI Operational Workflows

Operationalizes ARCH-11. The AI is the highest-variance operational surface (cost, quality, provider dependency).

| Workflow | Procedure |
|---|---|
| **Model Quality Harness execution** | Every prompt/model change runs offline against governed golden datasets (AD-97); measures judgment quality, calibration, **fairness/adverse-impact**, hallucination-reject rate, cost. Fails the release on threshold breach. |
| **Golden-dataset refresh** | Scheduled, governed curation (consent-compliant, PII-minimized, fairness-representative); dataset is versioned; refresh is reviewed (→ ARCH-15 AI Governance). |
| **Prompt/model promotion** | Harness pass → canary (small slice, monitored) → promote on quality/fairness parity → **auto-rollback** on regression. Provenance recorded (AD-95). |
| **Drift response** | Monitors (§ObservabilityHooks, ARCH-11 §14) watch confidence distribution, override rate, fairness-signal drift; sustained drift triggers investigation + possible model/prompt rollback or recalibration. |
| **Escalation-queue operations** | Human-escalated cases (ARCH-11 §12) have an operational queue with SLAs (held-candidate resolution time, AD-105); no candidate stuck indefinitely. |
| **Provider incident response** | Provider degradation → failover (ARCH-11 §8) → if none, fail-soft to human; provider cost/latency anomalies alert FinOps (§10). |
| **Calibration operations** | As Outcome Learning accrues, recalibrate confidence curves (ARCH-11 §7) on a governed cadence; recalibration is versioned and harness-checked. |

> ### AD-103 — Prompt/model promotion is a controlled release with code-grade rigor: harness gate → canary → monitored promotion → auto-rollback on quality/fairness regression. No prompt or model reaches production by hand.

---

## 10. FinOps & Capacity Management

| Concern | Decision |
|---|---|
| **Cost monitoring** | Cost attributed per **tenant, service, and capability**; AI token/cost per proposal is a first-class metric (ARCH-11 §14). |
| **AI cost governance** | The dominant cost center (ARCH-11 §13): model tiering, content-hash caching, per-tenant token budgets, back-pressure. Budget alerts + anomaly detection; over-budget **degrades**, never drops. |
| **Capacity planning** | Driven by queue-depth trends and business volume (campaigns/candidates); autoscaling (HPA/KEDA/Karpenter) tuned from real data (ARCH-10 §3). |
| **Cost/unit economics** | Cost-per-Candidate-Evaluation tracked against the billing unit (D-04.A2) — operational input to pricing/margin (DOC-03). |
| **Waste control** | Spot/burst for AI workers; cold-tiering; right-sizing; cache-hit-rate as a cost KPI. |

---

## 11. Operational Readiness Review (ORR)

A service or major change reaches GA only after an ORR. Checklist (abridged):
- SLIs/SLOs defined; dashboards live (→ ARCH-14); **business-health alerts** wired (AD-105).
- **Runbook** written; **failure drill rehearsed** (AD-101); gate services proven to **fail closed**.
- Backup verified; **restore/replay drilled** (§6); DR path documented (§7).
- Tenant isolation verified; PII handling reviewed (→ ARCH-13); crypto-shred path tested (§8).
- Autoscaling + back-pressure validated; cost attribution wired (§10).
- For AI changes: Model Quality Harness green (quality + fairness); rollback tested (§9).
- Contract/spec drift-check green (AD-75); consumer contracts satisfied (AD-55).

> Gate/Critical services face the **strictest** ORR; nothing on the gate path goes GA without a rehearsed fail-closed drill.

---

## 12. Post-Incident Review & Continuous Improvement

| Concern | Decision |
|---|---|
| **Blameless PIR** | Every SEV-1/2 gets a blameless post-incident review: timeline, root cause, contributing factors, **whether any invariant was stressed**, corrective actions with owners + dates. |
| **Invariant-integrity check** | Every PIR explicitly answers: *did any gate, isolation, immutability, or human-accountability invariant get bypassed or come close?* A near-miss on an invariant is treated as seriously as an outage. |
| **Corrective actions** | Tracked to completion; systemic fixes preferred over band-aids; runbooks/ORR updated. |
| **Error-budget-driven prioritization** | Reliability work is prioritized by budget burn (AD-100); repeated same-class incidents escalate to architectural review (→ ARCH-16). |
| **Continuous improvement** | Trends feed capacity, SLOs, and governance; learning is institutional (runbooks, drills, harness cases), not tribal. |

---

## 13. Operational Security *(operational surface; controls → ARCH-13)*

- **Secrets rotation** on schedule; short-lived credentials; ESO/Vault (ARCH-10).
- **Access reviews** periodic; least privilege; break-glass audited (§3).
- **Key operations** (rotation, crypto-shred) audited with proofs (§8, AD-102).
- **Audit-log monitoring** for anomalous access (a governed read of Audit is itself audited).
- Full threat model, IAM design, and compliance program → **ARCH-13**.

---

## 14. Architecture Decisions *(continuing the log; ARCH-11 ended at AD-98)*

| ID | Decision | Rationale | Alternatives |
|---|---|---|---|
| **AD-99** | Operations preserve invariants under stress; no action bypasses a gate/mutates a fact/crosses a tenant/lets AI decide | Keeps architecture's promises true under real-world pressure | Pragmatic escape hatches (rejected: defeats the whole design) |
| **AD-100** | Error-budget policy governs release velocity; gate-budget exhaustion freezes features | Reliability is a feature, especially for gates | Ship regardless of reliability (rejected: erodes trust) |
| **AD-101** | Every Critical/gate service GA-gated on a rehearsed failure drill + runbook | Un-drilled failure = unhandled | Assume runbooks suffice (rejected: untested = unknown) |
| **AD-102** | Crypto-shred & key-rotation are audited, verified procedures with completion proofs | Erasure is "verified unrecoverable everywhere," not "key deleted" | Delete-and-assume (rejected: leaves readable copies) |
| **AD-103** | Prompt/model promotion has code-grade rigor (harness→canary→auto-rollback) | Improve AI without silent quality/fairness regression | Hand-promote prompts (rejected: unsafe) |
| **AD-104** | DR validated by scheduled game-days; untested DR = no DR | Confidence requires exercise | Documented-only DR (rejected: fails when needed) |
| **AD-105** | Business-health conditions page like technical ones; no silent black holes | Technical-green ≠ business-healthy (DOC-06) | Only technical alerting (rejected: silent candidate harm) |
| **AD-106** | Operational actions are replayable with a structured, attributable trail | Complete operational history parallel to business history; audit/compliance/PIR value | Untracked ops actions (rejected: unexplainable operations) |

## 15. Open Questions

1. **On-call sustainability at small team size** (AD-41 reality): how much Critical surface can a small team safely operate before platform-team investment is forced?
2. **Held-candidate resolution SLA:** what is the committed max time a candidate may remain "held" before mandatory human action — a business+ethics decision (DOC-06), not just ops.
3. **Golden-dataset curation ownership & cadence** (with ARCH-15): who owns fairness-representativeness, and how often refreshed?
4. **DR RTO commitments per tier** — concrete numbers set with product/commercial (enterprise SLAs).
5. **Multi-region operational model timing** (ties AD-86) — when the first residency customer forces active-active or active-passive.
6. **Cost-per-Candidate-Evaluation target** feeding pricing/margin (with DOC-03) — the unit-economics guardrail.

## 16. Risks

- **Pressure to breach an invariant during an incident:** the most dangerous operational risk. *Mitigation:* AD-99 + gate runbooks whose first rule is fail-closed + PIR invariant-integrity check.
- **Silent business black holes:** stuck held candidates unnoticed. *Mitigation:* AD-105 business-health paging + escalation-queue SLAs.
- **Untested recovery/DR:** confidence without evidence. *Mitigation:* AD-101/AD-104 drills + replay rehearsals.
- **Incomplete crypto-shred:** a surviving PII copy defeats erasure. *Mitigation:* AD-102 verified completion across derived stores/embeddings.
- **AI cost runaway / quality regression:** dominant variable surface. *Mitigation:* §9/§10 controls, AD-103 promotion rigor, budgets + back-pressure.
- **Operational overload vs team size:** too much Critical surface too soon. *Mitigation:* AD-41 co-deploy, managed services (AD-81), platform-team investment before breadth.
- **Alert fatigue:** over-paging erodes response. *Mitigation:* business+technical alert tiering; PIR-driven alert tuning.

## 17. Deferred

- **To ARCH-13 (Security):** threat model, IAM/RBAC design, compliance program (SOC 2 / audits), pen-testing, supply-chain security, detailed key-management controls, prompt-injection defenses.
- **To ARCH-14 (Observability):** the concrete telemetry pipeline, dashboards, alerting rules, SLI instrumentation, business-metric observability, audit correlation at scale (this doc *consumes* observability; ARCH-14 *builds* it).
- **To ARCH-15 (AI Governance):** golden-dataset governance, fairness review board, model approval/retirement, calibration governance, human-review policy, provider approval.
- **To ARCH-16 (Platform Governance):** ADR lifecycle, contract/schema compatibility and deprecation policy, architectural review process for recurring incidents.

---

*End of ARCH-12 v0.1 — the Operational Architecture. The platform can now be run for years without betraying what it is: operations preserve every invariant under stress (AD-99), gates fail closed and intelligence fails soft in practice, the disposable cluster recovers by rebuild+replay, crypto-shred and DR are verified by drills, AI changes ship with code-grade rigor, and business-health — not just technical-green — is a paging signal. Next: ARCH-13 — Security Architecture (threat model, IAM, compliance, supply chain), the first of the two governance-adjacent deep-dives.*
