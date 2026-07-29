# ARCH-10 — Deployment Architecture

| Field | Value |
|---|---|
| **Document ID** | ARCH-10 |
| **Title** | Deployment Architecture (how the architecture becomes a running platform) |
| **Owner** | Principal Platform Architect + Cloud Architect + Kubernetes Architect + SRE + Infrastructure Architect |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture → Infrastructure realization |
| **Depends on** | ARCH-01→09 (all). Especially ARCH-06 (services/availability tiers), ARCH-07 (contracts), ARCH-08 (persistence responsibilities), ARCH-09 (interface specs) |
| **Blocks** | ARCH-11 (AI Runtime), ARCH-12 (Operational), ARCH-13 (Security), ARCH-14 (Observability), SPRINT-0 |
| **The one question** | **"How does the architecture become a running production platform?"** |
| **Scope** | **First document to commit concrete technologies.** Logical deployment + technology selection. **Operational procedures (runbooks, on-call, DR drills, capacity/cost governance) are ARCH-12.** Security and observability get dedicated deep-dives in ARCH-13/14. |
| **Reference cloud** | **AWS** (reference implementation). Every product is behind an architectural responsibility with named GCP/Azure/OSS equivalents (§1.3), so the reference is replaceable (AD-78). |

---

## 0. Deployment Philosophy

Infrastructure is the *realization* of the architecture, never a second design. Every product below exists **only** because an ARCH-01→09 responsibility requires it; nothing is here because "you need a database" or "everyone uses X."

> ### AD-77 — Infrastructure exists to realize the architecture, not redefine it.
> A technology choice may satisfy a responsibility (persistence, messaging, isolation, scaling) but may **never** introduce, alter, or constrain a business rule, domain concept, contract, or service boundary. If an infrastructure limitation seems to force a domain change, the infrastructure is wrong — replace it (AD-78), don't bend the domain.

> ### AD-78 — Infrastructure products are replaceable; architectural responsibilities are not.
> PostgreSQL may become another relational store; Kubernetes another orchestrator; Kafka another log. None of these changes may require rewriting the business (ARCH-01/02), domain (ARCH-03), interactions (ARCH-04), facts (ARCH-05), service boundaries (ARCH-06), contracts (ARCH-07), or persistence *responsibilities* (ARCH-08). This is the same principle the whole corpus rests on: **responsibilities are stable; implementations are swappable.** Every product is consumed behind the service's own boundary (never shared, ARCH-06 AD-43) so it can be replaced in one service without touching another.

The payoff already earned: the drift-proof chain **Business → Contract → Specification → Generated Code → Running System** means this document changes *what runs*, never *what the platform means*.

---

## 1. Technology Stack

### 1.1 Selections (each justified by a prior responsibility)

| Layer | Choice (AWS reference) | Justified by |
|---|---|---|
| **Container runtime** | containerd (OCI images) | ARCH-06 AD-40 (independently deployable services) |
| **Orchestration** | Kubernetes — Amazon EKS (managed) | ARCH-06 (13 services, independent scaling, fault isolation); AD-41 (co-deploy low-risk, isolate gates+Compute) |
| **Edge / API Gateway** | Cloud LB + WAF (ALB + AWS WAF) → **Kubernetes Gateway API (Envoy Gateway)** | ARCH-09 (external OpenAPI surface); AD-72 (edge error mapping); rate limiting (envelope, ARCH-07 §8) |
| **Ingress** | Gateway API (Envoy Gateway) | ARCH-09 external transport; ARCH-06 §4 (edge = REST) |
| **Service Mesh** | **Istio (ambient)** — mTLS, SPIFFE/SVID identity, circuit breaking, traffic shifting | ARCH-06 AD-45 (zero-trust internal), §7 (circuit breakers), §11 (canary) |
| **Internal RPC** | **gRPC** over the mesh | ARCH-06 §4; ARCH-09 §2 (protobuf) |
| **Event Backbone** | **Apache Kafka** (MSK managed; tiered storage) — per-key ordering, long retention, replay, cold-tiering | ARCH-05 (facts); ARCH-06 §6 (async facts); ARCH-08 §4 (event store/backbone, AD-63 no-compaction) |
| **Transactional DB** | **PostgreSQL** — Amazon Aurora PostgreSQL (RLS, PITR) | ARCH-08 §3 (transactional state, optimistic concurrency, RLS tenant isolation) |
| **Event store** | **PostgreSQL append-only streams per event-sourced service** (source of truth) + **outbox → Kafka** for distribution | ARCH-08 AD-62 (event-source gates+Evaluation+Decision); ARCH-06 AD-42 (outbox, no 2PC) |
| **Object Storage** | **Amazon S3** — SSE-KMS, Object Lock (WORM), lifecycle tiering, presigned URLs | ARCH-08 §6 (files), AD-66 (content-addressed, short-lived refs); Audit WORM (§9) |
| **Cache** | **Redis** — Amazon ElastiCache | ARCH-08 §7 (authz/consent/calibration/capability caches, fail-closed) |
| **Search** | **OpenSearch** — per-tenant scoped indices | ARCH-08 §8 (operational/candidate/evidence/audit search) |
| **Secrets** | **HashiCorp Vault** (or AWS Secrets Manager) + **External Secrets Operator**; **AWS KMS** for envelope + **per-tenant keys** | ARCH-06 §10; ARCH-08 AD-64/68 (crypto-shred, per-tenant keys) |
| **Identity** | External **OIDC IdP** (Okta/Auth0/Entra) for humans; **SPIFFE/SPIRE** (via mesh) for workloads | ARCH-06 §10; ARCH-09 AD-71 (server-side tenant/authz) |
| **Observability** | **OpenTelemetry** → Prometheus + Grafana + Tempo + Loki (Datadog as managed alt) | ARCH-06 §9; deep-dive → ARCH-14 |
| **CI/CD** | **GitHub Actions** (build, test, scan, SBOM) | ARCH-06 §11; ARCH-09 AD-75 (contract drift-check in CI) |
| **GitOps** | **Argo CD** (declarative) + **Argo Rollouts** (progressive delivery) | ARCH-06 §11 (GitOps, canary/blue-green) |
| **Autoscaling** | **HPA** (request tier) · **KEDA** (Kafka/AI queue-depth) · **Karpenter** (nodes) · GPU pools | ARCH-06 §8 (AI = queue-depth axis) |
| **Background workers** | KEDA-scaled Kafka consumers (projections, notifications, evaluation orchestration) | ARCH-08 §5 (read-model projections); ARCH-06 §7 (choreography) |
| **Artifact registry** | **Amazon ECR** (images) + OCI chart registry + **schema/contract registry** (Apicurio/Confluent) | ARCH-09 (spec governance, AD-73/75) |

### 1.2 Two deployment decisions worth stating explicitly

> ### AD-80 — Event-sourced services keep their authoritative event streams in their own PostgreSQL; Kafka is the distribution backbone, audit substrate, and replay source — not the per-service source of truth.
> Each event-sourced service (gates, Evaluation, Decision, Consent — ARCH-08 AD-62) appends facts to an append-only stream in **its own** Postgres (atomic with state via the transactional **outbox**, ARCH-06 AD-42), then relays to **Kafka** (via CDC). Kafka distributes facts to other services, feeds the Audit WORM store, and is the replay source to rebuild read models. *Rationale:* avoids "Kafka-as-database" pitfalls, keeps each service's truth inside its own boundary (AD-43), yet gives one logical fact backbone. *(Resolves ARCH-08 OQ-1 — one logical backbone, per-service authoritative streams.)*

> ### AD-81 — State lives in managed data services; the Kubernetes cluster runs (almost) only stateless compute.
> Authoritative data (Aurora, MSK/Kafka, ElastiCache, S3, OpenSearch) runs as **managed services outside the cluster's failure domain**. The cluster hosts stateless request handlers and stateless workers. *Rationale:* decouples the hardest operational problem (stateful data, backup, HA) from cluster lifecycle; a cluster rebuild never risks data; matches ARCH-06 "scale out, not up." (Any unavoidable in-cluster state uses StatefulSets + PVs, minimized.) The cluster becomes **disposable**: destroy → recreate → reconnect → **replay** → continue.

> ### AD-87 — Platform services are replaceable independently; application services depend on platform *interfaces*, never on product APIs.
> Each platform capability (gateway, mesh, event backbone, cache, search, secrets/KMS, object storage) exposes an **internal abstraction owned by the platform team**. Application services MUST NOT depend on Kafka client semantics, Redis APIs, OpenSearch DSL, or Vault SDKs directly — they depend on a thin platform interface (`Application → Platform Interface → Concrete Product`). *Rationale:* extends the replaceability principle (AD-78) from persistence/cloud to **platform middleware** — MSK→Redpanda, Redis→another cache, OpenSearch→another search engine become a platform-team change behind a stable interface, invisible to application services. This also keeps the ARCH-04/05/07 contracts free of any product-specific leakage. *(Governance of these platform interfaces → ARCH-15.)*

### 1.3 Cloud portability mapping *(AD-78 made concrete)*

| Responsibility | AWS (reference) | GCP | Azure | Portable / OSS |
|---|---|---|---|---|
| Orchestration | EKS | GKE | AKS | Kubernetes (any) |
| Event backbone | MSK (Kafka) | Pub/Sub or Managed Kafka | Event Hubs (Kafka API) | Kafka / Redpanda |
| Transactional DB | Aurora PostgreSQL | Cloud SQL / AlloyDB | Azure DB for PostgreSQL | PostgreSQL |
| Object storage | S3 | GCS | Blob Storage | MinIO (S3 API) |
| Cache | ElastiCache | Memorystore | Azure Cache | Redis |
| Search | OpenSearch | — | — | OpenSearch/Elastic |
| Secrets/KMS | Secrets Mgr + KMS | Secret Mgr + Cloud KMS | Key Vault | Vault |
| LLM inference | Bedrock / Anthropic | Vertex / Anthropic | Azure AI / Anthropic | behind the ACL (AD-52) |

> Because each product sits behind a service boundary and an ACL for externals (ARCH-07 AD-52), switching a column changes deployment config, **not** the architecture.

---

## 2. Reference Deployments *(logical — ASCII)*

### 2.1 Production
```
                       ┌──────────── Internet ────────────┐
                       │        (customers, candidates)     │
                       ▼                                    
     ┌─────────── AWS WAF + ALB (TLS termination) ───────────┐
     │                       │                                
     ▼                       ▼                                
  Envoy Gateway (Gateway API, external OpenAPI)  ── OIDC authn, per-tenant rate limit
     │  (tenant + authz resolved from token — AD-71)
     ▼
  ┌──────────────────  EKS Cluster (multi-AZ, ≥3 AZ)  ──────────────────┐
  │  Istio ambient mesh: mTLS + SPIFFE identity on ALL internal gRPC     │
  │                                                                       │
  │  ns: identity  ns: candidate  ns: campaign  ns: evaluation            │
  │  ns: gates(consent|integrity|fairness|audit)  ns: decision|feedback|export
  │  ns: intelligence-compute (GPU/burst pool)   ns: platform (gateway/workers)
  │   │            │            │            │            │                │
  │   └── stateless handlers + KEDA workers (Kafka consumers, projections) │
  └───────────────────────────┬───────────────────────────────────────────┘
                               │  (managed data plane — outside cluster, AD-81)
        ┌──────────────┬───────┴────────┬───────────────┬──────────────┐
        ▼              ▼                ▼               ▼              ▼
   Aurora PG      MSK (Kafka)        S3 (+Object      ElastiCache   OpenSearch
   (per-service   fact backbone      Lock/WORM        (Redis)       (per-tenant
    schemas,      + replay +         audit; files;                   indices)
    RLS, PITR)    audit feed)        exports)                        
        │              │                                            
        └── egress gateway (controlled) ──▶ LLM providers (Bedrock/Anthropic)  ◀ PII-minimized (AD-83)
```

### 2.2 Environments (logical)
```
 Dev        → ephemeral namespaces / local (kind) + mocked externals + LLM sandbox
 Integration→ shared cluster, real managed services (small), synthetic tenants
 QA         → prod-like, contract & CDC tests (ARCH-09 AD-75), fairness/gate tests
 Staging    → prod-parity (multi-AZ), canary rehearsal, DR drill target
 Production → multi-AZ, progressive delivery, per-tenant isolation
 DR         → cross-region: Aurora + S3 replicated; Kafka MirrorMaker; replay rebuilds derived
```

---

## 3. Kubernetes Architecture

| Concern | Decision |
|---|---|
| **Namespaces** | Per bounded context / service group: `identity`, `candidate`, `campaign`, `evaluation`, `gates` (consent/integrity/fairness/audit — separate deployments), `decision`, `feedback`, `export`, `intelligence-compute`, `platform`. Namespace = a policy + quota + network boundary. |
| **Node pools** | `general` (stateless handlers); `workers` (KEDA Kafka consumers); `intelligence-burst` (spot/preemptible for AI workers — idempotent, safe to interrupt); `gpu` (only if self-hosting embeddings/integrity models — else none); managed data plane is off-cluster (AD-81). |
| **Affinity / anti-affinity** | Gate services (consent/integrity/fairness/audit) use **pod anti-affinity across AZs** (no two replicas same AZ) — a gate never loses quorum to one AZ. Latency-sensitive pairs (Evaluation ↔ Intelligence Compute) soft co-locate. |
| **Autoscaling** | HPA on request tiers; **KEDA on Kafka consumer lag / AI queue depth** (ARCH-06 §8); Karpenter for node provisioning; scale-to-many for Intelligence Compute, scale-conservatively for gates. |
| **Stateless workloads** | The default: request handlers + workers, horizontally scaled, no local state. |
| **Stateful workloads** | Minimized; authoritative state in managed services (AD-81). Any in-cluster state via StatefulSet + PV (e.g., a self-managed component) is the exception, documented. |
| **Jobs** | One-off: read-model rebuilds (replay), reindex, snapshot creation, crypto-shred execution, import processing. |
| **CronJobs** | Scheduled: retention/expiration enforcement, cold-tiering, DR-drill automation, certificate/key rotation triggers, consent-expiry sweeps. |
| **Persistent volumes** | Only where unavoidable; encrypted (KMS); never the home of authoritative business data (that's managed services). |

---

## 4. Networking

| Concern | Decision |
|---|---|
| **Ingress** | Cloud LB + WAF → Envoy Gateway (Gateway API). Only the external OpenAPI surface (ARCH-09 §1) is exposed; internal gRPC is never internet-reachable. |
| **Egress** | **Controlled egress gateway**, default-deny. The **LLM/PII boundary** (ARCH-01 top risk) egresses only from Intelligence Compute through a dedicated egress path with PII-minimization enforced (AD-83). |
| **Zero Trust** | Istio ambient: **mTLS on every internal call**, SPIFFE/SVID workload identity; no implicit network trust (ARCH-06 AD-45). |
| **DNS** | CoreDNS in-cluster; ExternalDNS + Route 53 for edge. |
| **Certificates** | cert-manager (internal, mesh) + ACM (edge TLS); automated rotation. |
| **Load balancing** | Edge LB (ALB) + mesh-level L7 balancing (Envoy) for internal gRPC. |
| **Rate limiting** | At the gateway, **per-tenant and per-caller classes** (ARCH-07 §8 envelope); bulk import separated from interactive traffic. |
| **Network policies** | **Default-deny**, with explicit allows that mirror the **ARCH-04 legal-interaction matrix**. |

> ### AD-82 — Network policy + mesh authorization mirror the ARCH-04 interaction matrix. A forbidden interaction has no network path.
> The prohibitions (Recommendation ✗→ Candidate; Audit ✗→ initiate; cross-tenant ✗ — ARCH-04 §2) are enforced at **three** layers now: no contract (ARCH-07), no surface (ARCH-09 AD-76), and **no network route** (here). Defense in depth: the illegal conversation is impossible to express, expose, *or* route.

> ### AD-83 — All egress to external AI/LLM providers passes through a controlled egress gateway that enforces PII minimization.
> The sharpest trust boundary (ARCH-01) is a single, audited, default-deny egress path; raw candidate PII never leaves un-minimized (ARCH-06 §10.6). This is where the Intelligence Compute ACL (ARCH-07 AD-52) meets the network.

---

## 5. Data Infrastructure *(every ARCH-08 responsibility → concrete product)*

| ARCH-08 persistence responsibility | Product (AWS reference) | Notes |
|---|---|---|
| Transactional state (Identity, Candidate, Campaign, Feedback, Export) | Aurora PostgreSQL, per-service schemas, RLS | optimistic concurrency (versioned); tenant RLS below query layer |
| Authoritative event streams (gates, Evaluation, Decision, Consent) | Aurora PostgreSQL append-only + outbox | source of truth (AD-80) |
| Fact backbone / distribution / replay | MSK (Kafka), tiered storage, per-key partitioning | ordering key tenant→campaign→candidate-eval; **never compacted** (AD-63) |
| Read models / projections | Aurora PG / OpenSearch / Redis per projection fit | derived, rebuildable via replay (ARCH-08 AD-65) |
| Object storage (resume, CSV, work sample, exports) | S3, SSE-KMS, content-addressed, presigned short-lived URLs | virus-scan on ingest (Job); lifecycle tiering for retention |
| Audit WORM | S3 Object Lock (compliance mode) fed from Kafka; hash-chained; OpenSearch index for governed query | append-only, tamper-evident (ARCH-08 §9); longest retention |
| Cache (authz/consent/calibration/capability) | ElastiCache (Redis) | consent/authz **fail closed** (ARCH-08 AD-67); capability cache keyed by content-hash |
| Search (operational/candidate/evidence/audit) | OpenSearch, per-tenant indices | cross-tenant leak guard (ARCH-08 §8) |
| Encryption keys (per-tenant) | AWS KMS, per-tenant CMKs | crypto-shred + isolation (AD-64/68) |
| Vector / feature store (future moat) | *(reserved → ARCH-11 AI Runtime)* | Evidence Graph / Hiring Memory / Outcome Learning deferred |

> ### AD-84 — Per-tenant KMS keys (CMKs) are the deployment substrate for tenant isolation, crypto-shredding, and future residency.
> Every tenant's data is encrypted under its own key hierarchy; destroying a subject's key executes erasure (ARCH-08 AD-64); key locality anchors future data residency (AD-86).

---

## 6. AI Infrastructure

| Concern | Decision |
|---|---|
| **Inference** | Primary evaluation via **hosted Claude models** (Opus/Sonnet-class) behind the Intelligence Compute **ACL** (ARCH-07 AD-52), accessed through Amazon Bedrock and/or the Anthropic API (multi-provider behind the ACL). No model choice leaks into the domain. |
| **GPU workloads** | Only if self-hosting auxiliary models (embeddings for the future Evidence Graph, some integrity signals): dedicated `gpu` node pool, Karpenter-provisioned, KEDA-scaled. Primary evaluation is hosted (no GPU ops) at MVP. |
| **Autoscaling** | Intelligence Compute scales on **queue depth** (KEDA on Kafka work topics), burst on spot; back-pressure when depth exceeds threshold → business degrades gracefully (ARCH-06 §8), never drops a candidate. |
| **Model registry** | Versioned model configurations + routing (which model per task/tier), governed; a change is a config/version change (ties to ARCH-08 Intelligence Compute config). |
| **Prompt registry** | Versioned, reviewed prompts as governed artifacts (a prompt is **never** a business rule — ARCH-05 AD-30); prompt changes are canaried like code. |
| **Batch inference** | Bulk evaluation of an imported cohort via worker pools consuming Kafka; idempotent by content-hash (cache reuse, AD-66). |
| **Streaming inference** | Progressive `EvaluationProgress` via gRPC server-streaming (ARCH-09 §2); non-authoritative — the authoritative fact remains `EvaluationCompleted`. |

> ### AD-85 — Primary evaluation uses hosted Claude models behind the Intelligence Compute ACL; providers are multi-sourced and swappable; the AI never emits an authoritative fact.
> Consistent with ARCH-05 AD-35 / ARCH-06 AD-47 / ARCH-07 AD-56: the model returns proposals; the owning service validates and commits. Provider/model is a config choice behind the ACL (AD-78), not an architectural commitment. *(Deep AI-runtime mechanics — routing, PII-minimization pipeline, embedding lifecycle, vector/feature stores — are ARCH-11.)*

---

## 7. Deployment Strategy

| Strategy | Decision |
|---|---|
| **Blue/Green** | For gate and decision services where instant rollback matters most (a bad fairness/integrity deploy is a Tier-0 incident). |
| **Canary** | Argo Rollouts with automated analysis on **RED + business metrics** (held-by-fairness rate, override rate, error rate) before promotion; **gates get the most conservative canary** (smallest steps, strictest gates). |
| **Feature flags** | OpenFeature-compatible flag system (e.g., Flagsmith/LaunchDarkly) for progressive feature exposure decoupled from deploy; flags never gate a Constitutional rule (a flag can't disable a gate). |
| **Rollback** | GitOps revert (Argo CD) + Rollouts abort; because facts are immutable and read models are rebuildable (ARCH-08), rollback of *compute* never corrupts *truth*. |
| **Progressive delivery** | Contract-version rollouts (ARCH-09) run old+new majors in parallel (ARCH-07 §6) until consumers migrate. |

---

## 8. Environment Strategy

| Concern | Decision |
|---|---|
| **Environments** | Development → Integration → QA → Staging → Production (§2.2). Staging is prod-parity and the DR-drill target. |
| **Tenant isolation** | Production is multi-tenant with **defense-in-depth isolation**: namespace + network policy (AD-82) + RLS (Aurora) + per-tenant KMS keys (AD-84) + per-tenant search indices. **Dedicated single-tenant deployment** is an enterprise option (same architecture, isolated infra) for customers requiring it. |
| **Configuration** | GitOps (Argo CD) with per-environment overlays (Kustomize/Helm); config is declarative, versioned, and **auditable** (echoes P8). No manual cluster mutation. |
| **Secrets** | Vault/Secrets Manager + External Secrets Operator; per-environment isolation; short-lived, rotated; never in images or manifests (ARCH-06 §11). |

---

## 9. High Availability

| Concern | Decision |
|---|---|
| **Availability zones** | All managed data services multi-AZ; gate/critical services spread across **≥3 AZs** with anti-affinity (§3). |
| **Regional deployment** | **Single region at MVP**; multi-region on the residency/scale roadmap (AD-86). |
| **Backup topology** | Aurora continuous backup + PITR; MSK tiered storage + replication; S3 cross-region replication (audit/files); Kafka MirrorMaker for DR. |
| **Recovery topology** | Restore authoritative sources first (Aurora PITR, Kafka, S3), then **replay to rebuild all derived stores** (read models, search) — ARCH-08 §10. RPO/RTO per availability tier (ARCH-08 AD-69). |
| **Failover** | Managed multi-AZ failover is automatic; cross-region failover is orchestrated (DR runbook → ARCH-12). |

> ### AD-86 — Single-region at MVP; multi-region is a roadmap capability anchored on per-tenant keys and tenant/campaign partitioning.
> The substrate for residency (per-tenant CMKs AD-84, partition keys ARCH-08) is in place now; regional routing and replication topology are added when the first residency-bound enterprise customer requires it (DOC-01 global-ready). Don't pay multi-region complexity before a customer needs it (consistent with AD-41).

---

## 10. Architecture Decisions *(continuing the log; ARCH-09 ended at AD-76)*

| ID | Decision | Rationale | Alternatives |
|---|---|---|---|
| **AD-77** | Infrastructure realizes the architecture, never redefines it | Keeps the domain authoritative over tech | Infra-driven design (rejected: tail wags dog) |
| **AD-78** | Products replaceable; responsibilities not | Swap a product without touching domain/contracts | Lock architecture to a product (rejected: lock-in) |
| **AD-79** | Kubernetes/EKS as orchestration reference; managed data plane | Independent scaling + fault isolation (ARCH-06) with least ops | Serverless-only (rejected: AI/stateful fit) / VMs (rejected: ops) |
| **AD-80** | Per-service Postgres authoritative event streams; Kafka = backbone/audit/replay | Truth inside boundaries; one logical fact log | Kafka-as-database (rejected: pitfalls) |
| **AD-81** | State in managed services; cluster is stateless compute | Decouple hardest ops from cluster lifecycle | In-cluster databases (rejected: operational risk) |
| **AD-82** | Network policy + mesh authz mirror the ARCH-04 interaction matrix | Forbidden interaction has no network route | Open internal network (rejected: violates zero-trust) |
| **AD-83** | Controlled egress gateway enforces PII minimization to LLM providers | Contain the sharpest trust boundary | Direct egress (rejected: PII/compliance risk) |
| **AD-84** | Per-tenant KMS keys = isolation + crypto-shred + residency substrate | One mechanism, three guarantees | Single platform key (rejected: no shred, weaker isolation) |
| **AD-85** | Hosted Claude behind Intelligence Compute ACL; multi-provider, swappable; AI emits no fact | Best model quality without architectural lock; INV-1 preserved | Self-hosted model (rejected: cost/ops at MVP) / model-in-domain (rejected: AD-47) |
| **AD-86** | Single-region MVP; multi-region on residency roadmap | Avoid premature complexity; substrate ready | Multi-region day one (rejected: cost before need) |
| **AD-87** | Platform services replaceable independently; apps depend on platform interfaces, not product APIs | Extends AD-78 replaceability to middleware; no product leakage into apps/contracts | Direct product SDK use in app services (rejected: couples apps to products) |

## 11. Open Questions

1. **Cloud commitment:** AWS reference confirmed, or multi-cloud abstraction required by an early enterprise customer? (Portability mapping §1.3 keeps this cheap to defer.)
2. **Managed Kafka vs Redpanda vs MSK Serverless** — cost/ops/latency at MVP scale; revisit with volume.
3. **Mesh: Istio ambient vs Linkerd** — feature richness vs operational simplicity for a small team (AD-41 tension).
4. **Bedrock vs direct Anthropic API** (or both) behind the ACL — latency, cost, model availability, data-handling terms.
5. **First residency-bound customer timing** → triggers AD-86 multi-region work.
6. **Feature-flag product** selection and governance (must never be able to disable a gate).
7. **GPU footprint** — do MVP integrity/embedding needs justify any self-hosted GPU, or fully hosted?

## 12. Risks

- **Cloud lock-in:** deep managed-service use. *Mitigation:* AD-78 + portability mapping (§1.3); products behind service boundaries/ACLs.
- **Operational burden vs team size:** Kubernetes + Kafka + mesh + many managed services is heavy. *Mitigation:* AD-41 co-deploy low-risk services, AD-81 managed data plane, managed everything possible; grow platform team before service breadth.
- **Cost:** AI inference + Kafka long-retention + multi-AZ. *Mitigation:* content-hash caching (AD-66), tiered storage/cold-tiering (AD-63), spot for AI workers, cost governance → ARCH-12.
- **LLM egress latency/cost/outage:** dependence on external providers. *Mitigation:* multi-provider ACL (AD-85), fail-soft to human (ARCH-06 §7), caching, egress gateway (AD-83).
- **Multi-tenant isolation in a shared cluster:** a misconfig could cross tenants. *Mitigation:* defense-in-depth (AD-82/84 + RLS + per-tenant indices); dedicated-tenant option for enterprise.
- **Kafka ordering/retention misuse:** compaction or wrong partition key would break audit/replay. *Mitigation:* AD-80/AD-63 explicit; partition key = ordering key; no compaction on fact topics.
- **Managed-service limits/quotas** (connections, throughput). *Mitigation:* capacity planning → ARCH-12; back-pressure (ARCH-06 §8).

## 13. Deferred *(operational procedures only — per CTO roadmap)*

- **To ARCH-11 (AI Runtime):** model routing, PII-minimization pipeline internals, embedding lifecycle, vector/feature store selection, prompt engineering/eval harness, inference cost controls.
- **To ARCH-12 (Operational):** runbooks, on-call, incident management, **DR drills**, capacity planning, **cost governance/FinOps**, patching/upgrades, backup/restore/key-rotation/crypto-shred **procedures**, SLO management.
- **To ARCH-13 (Security Architecture):** threat model, IAM detail, key-management procedures, compliance/certification (SOC 2, etc.), pen-test, supply-chain security, data-classification enforcement.
- **To ARCH-14 (Observability Architecture):** telemetry pipeline, dashboards, alerting, SLIs/SLOs, business-metric observability, audit correlation at scale.

---

*End of ARCH-10 v0.1 — the Deployment Architecture. The architecture now has a running form: Kubernetes (EKS) hosting stateless services and workers, a managed data plane (Aurora, Kafka/MSK, S3, Redis, OpenSearch), a zero-trust mesh, per-tenant keys, a controlled LLM egress boundary, and progressive delivery — every product justified by an ARCH-01→09 responsibility and every product replaceable behind it (AD-77/AD-78). Forbidden interactions are now blocked at contract, surface, and network layers. Next: ARCH-11 — AI Runtime Architecture, the internals behind the Intelligence Compute ACL.*
