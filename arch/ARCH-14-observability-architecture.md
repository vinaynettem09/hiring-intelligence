# ARCH-14 — Observability Architecture

| Field | Value |
|---|---|
| **Document ID** | ARCH-14 |
| **Title** | Observability Architecture (seeing the platform — technical, business, AI, and security) |
| **Owner** | Principal SRE + Observability Architect + Security Architect (SIEM) + AI Operations |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture (observability) |
| **Depends on** | ARCH-12 (SLOs/health/ops), ARCH-13 (security signals), ARCH-11 (AI signals), ARCH-08 (fact stream/audit), ARCH-06 (correlation/availability), ARCH-05 (facts), DOC-06 (no-black-hole) |
| **Blocks** | ARCH-15 (AI Governance — quality signals), ARCH-16 (Platform Governance) |
| **The one question** | **"How do we see whether the platform is technically healthy, doing right by the business, keeping its AI honest, and safe — without observability ever becoming a source of truth or a data-leak vector?"** |
| **Scope** | Observability architecture across four planes (technical / business / AI / security). Consumes ARCH-11/12/13 signals; does not re-decide them. Instruments the SLOs (ARCH-12) and the SIEM pipeline deferred from ARCH-13 §14/§18. |

---

## 0. Observability Philosophy

The platform's promise is *decision quality you can trust*. You cannot operate that promise blind: you must **see** not just CPU and latency, but whether candidates are progressing, whether the AI is staying honest and calibrated, and whether anyone is attacking the trust boundaries. Observability here spans **four planes**, not the usual one:

1. **Technical** — is the system up and fast? (RED/USE)
2. **Business** — is the *product* doing its job? (candidates progressing, none silently held — DOC-06/AD-105)
3. **AI** — is the model staying honest, calibrated, non-drifting, affordable? (ARCH-11)
4. **Security** — is anyone attacking an invariant? (ARCH-13 SIEM)

One boundary must be crisp, because getting it wrong corrupts the whole design:

> ### AD-120 — Observability is derived and non-authoritative. The **audit trail is not logging**; telemetry is not the record of truth.
> The **audit trail** (event log = audit, AD-32) is **authoritative, immutable, complete, tamper-evident** — it is a *business record*. **Telemetry** (traces, metrics, logs) is **derived, sampled, and ephemeral** — it exists to *observe*, and may be dropped, sampled, or expired without loss of truth. A compliance question is answered from **audit**, never from logs; an operational question is answered from **telemetry**. Conflating them (treating logs as audit, or audit as "just logs") breaks both: logs get over-retained and PII-laden, and audit gets treated as best-effort. **They are different systems with different guarantees.**

A powerful consequence of the corpus:

> ### AD-121 — Business observability is computed from the immutable fact stream, so business metrics and the audit record share one lineage and can never disagree.
> Metrics like time-to-recommendation, held-rate, and override-rate are derived from the same facts (ARCH-05) that constitute the audit trail. Therefore a business dashboard and a compliance audit tell the **same story by construction** — there is no separate, drift-prone "analytics truth."

---

## 1. The Signals

| Signal | What it captures | Backbone (ARCH-10) |
|---|---|---|
| **Traces** | End-to-end request/flow paths across services (incl. the AI pipeline) | OpenTelemetry → Tempo |
| **Metrics** | Rates, errors, durations, saturation, business counters | OpenTelemetry → Prometheus |
| **Logs** | Structured, tenant-tagged, PII-minimized event logs (operational, **not** audit) | OpenTelemetry → Loki |
| **Business facts** *(observability source, not a signal to emit)* | The immutable fact stream (ARCH-05) — the source of **business** observability (AD-121) | Kafka → projections |
| **Audit** *(distinct — authoritative)* | The immutable record (AD-32) — queried for compliance, **not** an observability signal | WORM (ARCH-08) |

All three telemetry signals use **OpenTelemetry** (vendor-neutral; Datadog as managed alternative — ARCH-10) so the pipeline is portable (AD-78/AD-87 — apps depend on the OTel API, not a vendor SDK).

---

## 2. Telemetry Pipeline

```
 services + workers + AI runtime
        │  (OTel SDK — instrumented once, vendor-neutral)
        ▼
 OTel Collector (per-cluster)  ── enrich (tenant, correlation, business IDs) · PII-minimize · sample
        │
        ├──▶ Metrics  → Prometheus ─┐
        ├──▶ Traces   → Tempo       ├──▶ Grafana (dashboards, all 4 planes)
        ├──▶ Logs     → Loki       ─┘
        └──▶ security-relevant events → SIEM (§9)
 business observability:  Kafka fact stream → projections → Grafana/BI  (AD-121, separate from telemetry)
 audit (authoritative):   WORM store → governed query  (NOT in this pipeline — AD-120)
```

| Concern | Decision |
|---|---|
| **Collection** | OTel SDK in every service; auto + manual instrumentation of gates, the AI pipeline, and business transitions. |
| **Enrichment** | The Collector attaches tenant, correlation ID, and business IDs (campaign/candidate-evaluation) to every signal (§3). |
| **PII minimization** | The Collector **strips/masks PII** before storage (AD-123); raw PII never enters telemetry (ARCH-06 §9). |
| **Sampling** | Tail-based trace sampling (keep errors, slow traces, gate holds, AI escalations); metrics unsampled; logs volume-controlled. |
| **Tenant tagging** | Every signal tenant-tagged for per-tenant views and isolation (§12). |
| **Backends** | Prometheus/Tempo/Loki/Grafana (portable) or Datadog (managed) — behind a platform observability interface (AD-87). |

> ### AD-123 — Telemetry is PII-minimized and tenant-tagged; observability is never a PII-leak or cross-tenant vector.
> No raw candidate PII in traces/metrics/logs; any identity in telemetry is pseudonymized under the tenant boundary. This keeps observability consistent with crypto-shred (AD-64) — there is no un-shreddable PII copy hiding in logs. Cross-tenant telemetry access is impossible (tenant-scoped, §12).

---

## 3. Correlation Model

The thread that ties all four planes together — and the ops-layer expression of explainability (P13/INV-2).

| ID | Purpose | Origin |
|---|---|---|
| **Correlation ID** | One business transaction across all services/signals | minted at the edge (ARCH-06 §9) |
| **Trace/span IDs** | Distributed trace linkage (W3C traceparent) | propagated per hop |
| **Business IDs** | `CampaignId`, `CandidateEvaluationId`, etc. as first-class trace/metric attributes | domain (ARCH-03) |
| **AI provenance** | model + prompt + calibration version on AI spans | ARCH-11 AD-95 |
| **Audit correlation** | the same correlation + business IDs appear on audit facts | ARCH-05/§8 |

> ### AD-122 — Every signal carries correlation, business, and (on AI paths) provenance IDs, so any evaluation or decision is reconstructable end-to-end across telemetry and audit.
> Given a `CandidateEvaluationId`, an operator (or an auditor, within governance) can trace the full path — intake → consent check → work sample → integrity → AI proposal (with model/prompt version) → confidence → fairness → delivery → human decision — across traces, logs, and the audit record, all sharing IDs. This is *how* explainability and incident analysis actually work at runtime.

---

## 4. SLIs / SLOs / Error Budgets

Instruments the SLOs defined in ARCH-12 §1 (this doc *measures* them; ARCH-12 *sets policy*).

| Concern | Decision |
|---|---|
| **SLI instrumentation** | Each SLI (gate availability, audit-write success, time-to-recommendation, etc.) is a concrete metric/trace-derived measure. |
| **SLO dashboards** | Per-service + per-tier SLO dashboards; gate/Critical services most prominent. |
| **Error-budget tracking** | Budget burn computed continuously; drives ARCH-12 AD-100 release-freeze policy. |
| **Burn-rate alerting** | **Multi-window, multi-burn-rate alerts** (fast burn → page; slow burn → ticket) to catch both acute outages and slow degradation without flapping. |

> ### AD-125 — SLO burn-rate alerting (multi-window) is the trigger for error-budget policy; gate/audit budgets are watched most strictly.

---

## 5. Business-Metric Observability

The plane most products lack — derived from the fact stream (AD-121), so it's consistent with audit.

| Business SLI | Why it matters | Source facts |
|---|---|---|
| **Time-to-recommendation** | core value latency | invited → delivered facts |
| **Held-candidate count & age** | **no silent black holes** (DOC-06/AD-105) | fairness/consent/integrity holds without resolution |
| **Override rate** (human vs AI proposal) | ultimate quality signal; feeds calibration (ARCH-11 §7) & AI governance | recommendation vs decision facts |
| **Candidate completion rate** | funnel health; candidate experience | invited → submitted facts |
| **Feedback-release latency** | candidate dignity (brand-defining, DOC-11) | decision → feedback-released facts |
| **Fairness-hold rate** | fairness health; early adverse-impact signal | fairness verdict facts |
| **Cost-per-Candidate-Evaluation** | unit economics vs billing unit (D-04.A2) | AI cost (§7) ÷ evaluations |

These populate a **business-health dashboard** that product, CS, and on-call watch — the operational face of "is the platform doing right by candidates and customers?"

---

## 6. Health Model

Three levels of "healthy," each a distinct question (extends ARCH-12 AD-105):

| Level | Question | Signal |
|---|---|---|
| **Liveness** | Is the process running? | probe |
| **Readiness** | Can it serve (dependencies + gates reachable)? | readiness probe incl. gate reachability |
| **Business health** | Are candidates progressing; is anything stuck? | held-count/age, stalled campaigns, DLQ depth (AD-105) |

> A service can be **live and ready but business-unhealthy** (e.g., quietly leaving candidates held). Business health is a **first-class, paging** health level — instrumented here, paged per ARCH-12.

---

## 7. AI Observability

Instruments ARCH-11 §14; the signals that keep the AI honest and feed AI governance (→ ARCH-15).

| Signal | Detects | Feeds |
|---|---|---|
| **Confidence distribution** | over/under-confidence drift | calibration (ARCH-11 §7), governance |
| **Override rate** | proposals humans reject — the quality ground-truth proxy | calibration, Model Quality Harness cases |
| **Validation-failure / hallucination-reject rate** | model/prompt degradation | prompt/model health, rollback (ARCH-12 §9) |
| **Escalation rate** | how often AI defers to humans | capability health, escalation-queue load |
| **Fairness-signal drift** | emerging adverse-impact patterns | Fairness Service + AI governance (early warning) |
| **Latency / tokens / cost** (with provenance) | performance + FinOps | cost governance (ARCH-12 §10) |
| **Provenance coverage** | proposals missing model/prompt version = invalid | integrity of AD-95 |

> ### AD-126 — AI observability is a governance input, not just an ops dashboard: confidence, override, and fairness-drift signals feed calibration, the Model Quality Harness, and the AI governance loop (ARCH-15).
> This closes the learning loop: the platform *sees* when the AI is drifting or miscalibrated and routes that into governed correction — the observability half of "honesty over confidence" (AD-91).

---

## 8. Audit Correlation

The precise relationship between observability and the authoritative audit trail (AD-120):

| Aspect | Audit (authoritative) | Telemetry (observability) |
|---|---|---|
| **Nature** | immutable, complete, tamper-evident business record (AD-32) | derived, sampled, ephemeral |
| **Retention** | policy/compliance-driven, long (ARCH-08) | shorter, cost-driven (§11) |
| **Used for** | compliance, non-repudiation, explainability of *what happened* | operating, debugging, alerting on *how it's running* |
| **Shared** | **correlation + business IDs** (AD-122) — the bridge between the two | |

**The bridge:** because audit facts and telemetry share correlation/business IDs, an operator debugging a trace can pivot to the authoritative audit record for the same `CandidateEvaluationId`, and an auditor reviewing a decision can pivot to the operational trace of *how* it was produced — **without** either system pretending to be the other. Audit answers "what is true"; telemetry answers "what happened operationally." Governed audit reads are themselves audited (ARCH-13).

---

## 9. Security Observability / SIEM *(the pipeline ARCH-13 deferred here)*

| Concern | Decision |
|---|---|
| **SIEM ingestion** | Security-relevant events (auth failures, authz denials, cross-tenant access *attempts*, egress anomalies, admission-policy blocks, break-glass use, key operations) flow to a SIEM. |
| **Detection rules** | Codified detections for the ARCH-13 threat classes: tenant-escape attempts, PII-egress anomalies, injection patterns, credential anomalies, supply-chain alerts. |
| **Anomaly hunting** | Threat hunting over audit + operational trail (AD-106) + telemetry (ARCH-13 §14). |
| **Correlation with audit** | Security detection correlates against the **immutable** audit/operational trails (attacker cannot erase — AD-112). |
| **Alerting** | Any suspected tenant/PII/audit/gate-bypass detection is **SEV-1** (ARCH-12/13), paging security immediately. |
| **Boundary** | This is the *observability/detection* pipeline; the *controls* live in ARCH-13, the *governance* in ARCH-16. |

---

## 10. Alerting & Escalation

| Concern | Decision |
|---|---|
| **Alert taxonomy** | Three routed classes: **technical** (RED/USE, SLO burn), **business** (held candidates, stalled campaigns — AD-105), **security** (SIEM detections). |
| **Routing** | Technical → service on-call; business → on-call **+ product/CS**; security → security on-call (immediate for SEV-1) — per ARCH-12 §3. |
| **Alert quality** | Alerts must be actionable + tied to a runbook (ARCH-12 §2); multi-window burn-rate to avoid flapping (§4). |
| **Fatigue control** | PIR-driven alert tuning (ARCH-12 §12); no alert without an owner and an action. |
| **Business+security page like technical** | AD-105 (business) and AD-112 (security) conditions are first-class paging signals, not dashboards-only. |

> ### AD-124 — Observability data must never influence authoritative business state directly.
> Telemetry (and SIEM detections, and AI-quality signals) may trigger **alerts, investigations, and governance workflows** — but may **never** mutate domain state, approve a candidate, release feedback, pass a gate, or emit a business fact. All authoritative state changes continue to originate only from **domain commands and immutable facts** (ARCH-04/05). *Rationale:* completes the corpus-wide separation symmetry — **Audit ≠ Telemetry (AD-120), AI ≠ Decision (AD-88), Security ≠ Domain (AD-107), Observability ≠ Business Logic (here).** An observation can *prompt a human or a governed process to act*; it can never *be* the action. (This is why, e.g., a fairness-drift alert routes to AI governance to *decide*, rather than auto-adjusting a live evaluation.)

---

## 11. Data Retention & Cost of Observability

| Concern | Decision |
|---|---|
| **Retention tiers** | Metrics: medium retention (downsampled long-term); traces: short (sampled); logs: short-to-medium; **audit: long — but that's ARCH-08, not here** (AD-120). |
| **Sampling** | Tail-based trace sampling (keep the interesting: errors, holds, escalations); high-cardinality controls on metrics. |
| **Cardinality control** | Business IDs as attributes are bounded/aggregated to avoid metric explosion (tenant/campaign granularity, not per-candidate metric series). |
| **Cost** | Observability is not free; retention/sampling tuned as a cost line (ARCH-12 FinOps); cache/telemetry cost tracked. |
| **PII & shred** | Telemetry is PII-minimized (AD-123) so retention never conflicts with crypto-shred (AD-64). |

---

## 12. Tenant-Aware Observability

| Concern | Decision |
|---|---|
| **Tenant tagging** | Every signal tenant-scoped; internal dashboards filter by tenant. |
| **Isolation** | Cross-tenant telemetry access impossible (INV-10 applies to observability too); telemetry backends enforce tenant scoping. |
| **Per-tenant SLOs** | Enterprise customers may have per-tenant SLO views (supports enterprise SLAs, DOC-03). |
| **Customer-facing observability** *(roadmap)* | A future customer status/metrics surface (their campaigns' health, their SLAs) — derived from **their** facts only; deferred, boundary reserved. |

---

## 13. Architecture Decisions *(continuing the log; ARCH-13 ended at AD-119)*

| ID | Decision | Rationale |
|---|---|---|
| **AD-120** | Observability is derived/non-authoritative; audit ≠ logging | Audit is the immutable record; telemetry is ephemeral observation — different systems, different guarantees |
| **AD-121** | Business observability computed from the immutable fact stream | Business metrics and audit share one lineage; can never disagree |
| **AD-122** | Every signal carries correlation + business + AI-provenance IDs | Any evaluation/decision reconstructable end-to-end across telemetry + audit |
| **AD-123** | Telemetry PII-minimized + tenant-tagged | Observability never a PII-leak or cross-tenant vector; consistent with crypto-shred |
| **AD-125** | Multi-window SLO burn-rate alerting drives error-budget policy | Catches acute + slow degradation without flapping; gate/audit watched strictest |
| **AD-124** | Observability data never influences authoritative business state directly | Completes the separation symmetry; observations prompt action, never *are* the action |
| **AD-126** | AI observability is a governance input, not just a dashboard | Confidence/override/fairness-drift feed calibration + Model Quality Harness + AI governance |

*(ARCH-14 covers AD-120–AD-126; numbering continues at AD-127 in ARCH-15.)*

## 14. Open Questions

1. **Managed vs self-hosted observability** (Grafana stack vs Datadog) — cost/ops/portability tradeoff at team scale (AD-41/AD-87 keep it swappable).
2. **Trace sampling rate for gate/AI paths** — how much to always-keep (gate holds, AI escalations) vs sample.
3. **Customer-facing observability scope & timing** — what health/SLA data enterprises get, and when.
4. **Business-metric latency** — how fresh must the business-health dashboard be (near-real-time vs minutes) to catch a stuck candidate in time (ties held-candidate SLA, ARCH-12 OQ).
5. **SIEM product** and its retention/correlation topology with the audit store.
6. **Metric cardinality budget** — how much per-campaign granularity before cost/cardinality forces aggregation.

## 15. Risks

- **Audit/telemetry confusion:** treating logs as audit (or vice versa). *Mitigation:* AD-120 explicit separation; compliance queries hit audit only.
- **PII in telemetry:** a leak or shred-defeating copy. *Mitigation:* AD-123 Collector-level minimization; no raw PII ever emitted.
- **Alert fatigue:** noisy alerts erode response. *Mitigation:* actionable+runbook-linked alerts, burn-rate windows, PIR tuning.
- **Cardinality/cost explosion:** business IDs as unbounded metric labels. *Mitigation:* aggregation granularity + cardinality budget (§11).
- **Blind spots on business health:** technical-green while candidates are stuck. *Mitigation:* AD-105/§5 business plane as first-class + paging.
- **AI drift undetected:** miscalibration creeping in. *Mitigation:* AD-126 confidence/override/fairness-drift monitoring → governance.
- **Observability as a cross-tenant vector:** shared dashboards leaking across tenants. *Mitigation:* AD-123 tenant scoping in backends (INV-10 extends to telemetry).

## 16. Deferred

- **To ARCH-15 (AI Governance):** how AI observability signals (drift, override, fairness) drive model/prompt/calibration governance decisions, review cadence, and the fairness review board.
- **To ARCH-16 (Platform Governance):** observability standards as governed artifacts (required SLIs per service, dashboard/alert review, metric taxonomy ownership).
- **Implementation:** concrete dashboards, alert rules, Collector configs, sampling policies, SIEM detections — engineering runbooks that consume this architecture.

---

*End of ARCH-14 v0.1 — the Observability Architecture. The platform can now be seen across four planes — technical, business, AI, and security — with one crisp boundary: telemetry observes (derived, ephemeral, PII-minimized) while audit records (authoritative, immutable), the two bridged by shared correlation and business IDs so any decision is reconstructable end-to-end (AD-120/AD-122). Business health is a first-class, paging signal (no silent black holes), and AI observability feeds governance, not just dashboards. Next: ARCH-15 — AI Governance Architecture, where drift, override, and fairness signals become governed decisions. Two documents remain (ARCH-15, ARCH-16), then the corpus is complete.*
