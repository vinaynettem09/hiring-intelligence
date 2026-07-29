# ARCH-08 — Persistence Architecture

| Field | Value |
|---|---|
| **Document ID** | ARCH-08 |
| **Title** | Persistence Architecture (how business information is stored) |
| **Owner** | Principal Data Architect + Distributed Systems Architect + Event-Sourcing Architect + Security Architect |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture (implementation architecture) |
| **Depends on** | ARCH-07 (contracts), ARCH-06 (services), ARCH-05 (facts), ARCH-04 (interactions), ARCH-03 (aggregates), ARCH-02 (capabilities), ARCH-01 (context/trust) |
| **Blocks** | ARCH-09 (API Specs), ARCH-10 (Deployment), ARCH-11 (AI Runtime), ARCH-12 (Operational) |
| **The one question** | **"How is business information stored while preserving ownership, consistency, auditability, performance, and long-term evolution?"** |
| **This document IS** | The persistence **architecture** — persistence boundaries, ownership, lifecycle, retention, recovery, and the security of data at rest. |
| **This document is NOT** | SQL · DDL · indexes · ORM models · migrations · queries · stored procedures · vendor syntax · concrete product selection. **Those are implementation / ARCH-10.** |
| **Quality bar** | After this document, **every byte the platform stores has an owner, a lifecycle, a retention policy, a recovery strategy, and a business justification.** Nothing exists "because the database needs it." |

---

## 0. Persistence Philosophy

The platform stores six categorically different things. Treating them as one ("the database") is the mistake this document exists to prevent.

| Kind | What it is | Truth-semantics | Example |
|---|---|---|---|
| **State** | The current, mutable condition of an aggregate | Authoritative, changeable under invariants | A Campaign's lifecycle status |
| **Facts** | Immutable business events (ARCH-05) | Authoritative, append-only, permanent | `RecommendationDelivered` |
| **Views (Read Models)** | Query-shaped projections of state/facts | **Derived**, disposable, rebuildable | A recruiter dashboard view |
| **Files** | Large binary/opaque content | Authoritative content, referenced by identity | A resume; a raw work sample |
| **Derived Information** | Search indices, aggregates, embeddings | Derived, rebuildable | Candidate search index |
| **Cache** | Hot copies for performance | Non-authoritative, expendable | Consent-status cache |

**Why each exists:**
- **State** exists because aggregates have a *now* (ARCH-03) — a campaign is Active, a consent is Granted. State is the answer to "what is true right now?"
- **Facts** exist because the business has a *history* that must never change (ARCH-05) — and because that history is the audit trail (AD-32) and the substrate for future learning.
- **Views** exist because the shape data is *written* in (owned aggregates) is rarely the shape it must be *read* in (dashboards, decisions). Views are derived so they can be wrong-then-rebuilt without endangering truth.
- **Files** exist because resumes, work samples, and exports are large opaque content that doesn't belong inside an aggregate's state.
- **Derived information** exists to make truth *findable* (search) and, later, *comparable* (embeddings/features) — always rebuildable from the authoritative sources.
- **Cache** exists purely for speed and is always expendable.

> ### AD-60 — Persistence follows ownership. No persistence technology owns business rules.
> A store persists an aggregate's **state** or a service's **facts** or a consumer's **views** — but the **rules** live in the domain model (ARCH-03, AD-17), enforced by the owning service, never by a schema, constraint, trigger, or query. A database is a place to *keep* truth, never the place that *defines* it. The same rule stated in ARCH-03 §0 (against spaghetti in code) now holds at the data tier: **a constraint may reflect an invariant, but it is never the invariant.**

> ### AD-61 — Persistence technologies are selected per data responsibility, not standardized across the platform.
> Transactional state, immutable facts, read models, files, audit, search, and future vector/feature stores each have distinct responsibilities and are backed by the *fit* technology, not a single mandated product. **This is polyglot persistence by principle.** *(MVP pragmatism, consistent with AD-41: "per responsibility" is a **logical** rule — at MVP several services MAY run on the same store **product** in **separate schemas with separate keys**, never a shared schema/dataset. The boundary that must never be crossed is a shared **dataset**, not a shared **product**.)*

---

## 1. Persistence Taxonomy

| Class | Authoritative? | Mutability | Owner | Rebuildable? | Backing model (per AD-61) |
|---|---|---|---|---|---|
| **Transactional State** | ✅ | mutable (under invariants) | the aggregate's service | ❌ (source of truth) | relational transactional store |
| **Immutable Facts** | ✅ | append-only | the fact's producing service | ❌ (source of truth) | append-only ordered event store / log |
| **Read Models** | ❌ derived | rebuilt | the consuming service | ✅ from facts | fit-for-query store (relational/document/search) |
| **Object Storage** | ✅ (content) | write-once / versioned | Candidate / Evaluation / Export | ❌ | object store, content-addressed |
| **Audit Store** | ✅ | append-only, WORM | Audit | ❌ | WORM, tamper-evident (hash-chained) |
| **Search Index** | ❌ derived | rebuilt | search-owning service | ✅ from state/facts | search index (per-tenant scoped) |
| **Vector Store** *(future)* | ❌ derived | rebuilt | Evidence Graph / Hiring Memory (deferred) | ✅ | vector store |
| **Feature Store** *(future)* | ❌ derived | rebuilt | Outcome Learning (deferred) | ✅ | feature store |
| **Cache** | ❌ | expendable | any service | ✅ trivially | in-memory/distributed cache |
| **Temporary Storage** | ❌ | ephemeral | processing services | ✅ | scratch (e.g., in-flight work-sample processing) |
| **Analytics** | ❌ derived | rebuilt | analytics (off the fact stream) | ✅ | warehouse/lakehouse (post-MVP) |

> **The single most important line:** exactly three classes are **authoritative** (Transactional State, Immutable Facts, Object Storage content, plus the Audit WORM projection which is a special immutable curation of facts). **Everything else is derived and rebuildable.** If a derived store is lost, no truth is lost — it is replayed. This is what makes the system operationally safe.

---

## 2. Per-Service Persistence

*For each service (ARCH-06): Authoritative Store · Derived Stores · Read Models · Retention · Encryption · Backup · Recovery · Partitioning · Scalability · Availability · Consistency.* Availability tiers (Critical/High/Standard) and RPO/RTO tiers inherit from ARCH-06 §2.14 (see §10).

| Service | Authoritative store | Derived stores / read models | Retention | Partitioning | Availability / Consistency |
|---|---|---|---|---|---|
| **Identity & Access** | transactional (orgs, users, permissions) | authz-claims cache | long (governance) | tenant | Critical / strong within owner |
| **Candidate** | transactional (candidate identity, afterlife status, roster links) + **object storage** (resume, CSV) | candidate search index; dashboard views | consent/retention-governed | tenant → candidate | High / strong local, eventual cross-service |
| **Campaign** | transactional (campaign lifecycle, **frozen calibration**, roster, fairness-verdict ref) | campaign dashboard read model | campaign-life + retention | tenant → campaign | High / strong local |
| **Evaluation** | **event-sourced** (Candidate Evaluation: invitation → work sample ref → evidence → evaluation → recommendation) + **object storage** (raw work sample) | per-candidate & per-campaign read models; recruiter views | long (evidence immutable; compliance) | tenant → campaign → candidate-evaluation | High / event-sourced, eventual read models |
| **Intelligence Compute** | **none (owns no authoritative data)** | capability-result cache (by input content-hash); model/prompt registry (config) | cache: short; config: versioned | tenant-scoped cache | Standard / n/a (stateless) |
| **Integrity** | event-sourced / state+outbox (integrity verdicts) | verdict read model | long (compliance) | tenant → candidate-evaluation | Critical / authoritative verdicts |
| **Fairness** | event-sourced (campaign fairness verdicts + assessed-set references) | verdict read model | long (compliance) | tenant → campaign | Critical / authoritative verdicts |
| **Consent** | **event-sourced** (consent lifecycle: requested/granted/withdrawn/expired) | **consent-status cache** (very short TTL, event-invalidated) | long (proof of consent) | tenant → candidate | Critical / **strong, fail-closed** |
| **Audit** | **WORM append-only** (curated projection of ALL facts; hash-chained) | governed audit search index | **longest** (regulatory) | tenant → campaign | Critical / append-only, immutable |
| **Decision** | **event-sourced** (Hiring Decision, immutable) | delivered-recommendation read model (input); decision read model | **longest (accountability)** | tenant → candidate-evaluation | Critical / immutable once decided |
| **Feedback** | transactional / state+outbox (feedback draft/release/deliver) | candidate-feedback read model | retention-governed | tenant → candidate-evaluation | Standard |
| **Export** | transactional (export package assembly/status) + **object storage** (export artifact) | export status read model | retention (shorter) | tenant → campaign | Standard / fail-safe |
| **Notification** | delivery log (minimal) | — | short | tenant | Standard / mostly stateless |

**Shared persistence infrastructure (not a domain service — described here for completeness):**
- **Event backbone / fact log** — the durable, ordered (per-key), append-only log carrying all business facts (ARCH-05). It is the source of truth for event-sourced services, the substrate of Audit (AD-32), and the replay source for every read model. Ordering guaranteed **per key** (tenant → campaign → candidate-evaluation), never global (ARCH-07 §4).
- **Projection/read-model stores** — per consumer, derived, rebuildable (§5).
- **Object storage** — files, content-addressed, encrypted, virus-scanned (§6).
- **Cache tier** — distributed cache for hot reads (§7).
- **Search** — derived, tenant-scoped indices (§8).

---

## 3. Transactional Data

For services holding mutable aggregate **state** (Identity, Candidate, Campaign, Feedback, Export):

| Concern | Decision |
|---|---|
| **Aggregate persistence** | One aggregate = one consistency boundary = one local transaction (ARCH-03 §3.0). State + emitted fact commit **atomically via the outbox** (ARCH-06 §7) — no distributed transaction (AD-42). |
| **Optimistic concurrency** | Every aggregate carries a **version**. A write asserts the expected version; a mismatch raises the ARCH-07 **Conflict Error** (caller re-reads and reconciles). No pessimistic locks across services. |
| **Versioning** | Aggregate version is monotonic per aggregate; used for concurrency and for read-your-writes on the owner. |
| **Identity generation** | IDs are **globally-unique, opaque, time-orderable, tenant-scoped, and PII-free**, minted by the **owning** service (ARCH-06 AD-43). IDs are stable and meaningless outside their owner. |
| **Soft delete** | We prefer **status transitions over deletion** (INV-7: candidacy persists; a candidate is Afterlife, not deleted). "Deletion" of personal data is achieved by **crypto-shredding** (§9, AD-64), not row removal — so history/audit stays intact. |
| **Historical records** | Aggregates that need history (calibration changes pre-freeze, status transitions) are **effective-dated / append-a-version**, never destructive overwrite where the past matters. |
| **Temporal data** | Business time (`occurred-at`, ARCH-05) is distinct from processing time; both are retained. Calibration is **frozen at Active** (INV-c) and thereafter read-only — a temporal snapshot bound to the campaign. |

---

## 4. Event Store

For the event-sourced services (Evaluation, Decision, Consent, Integrity, Fairness) and the backbone:

> ### AD-62 — Event-sourcing scope: the gates (Integrity, Fairness, Consent), plus Evaluation and Decision, are event-sourced; other services use state + transactional outbox.
> *Rationale:* these five have the highest audit, replay, and reconstruction value — every gate verdict, every evaluation, every human decision must be reconstructable fact-by-fact for explainability and compliance. State-only services gain little from full sourcing and are simpler with state+outbox. *(Resolves ARCH-06 OQ-1.)*

| Concern | Decision |
|---|---|
| **Fact persistence** | Facts are appended immutably (ARCH-05 EV-INV-14). An event-sourced aggregate's state is the **fold** of its fact stream. |
| **Ordering** | Guaranteed **per key** (tenant → campaign → candidate-evaluation). Sufficient because all ordering laws (ARCH-05 §6) are per-key or campaign-scoped; enables horizontal scale. |
| **Replay** | Any event-sourced state and any read model is reconstructable by replaying facts from a known point. Replay is a first-class recovery mechanism (§10). |
| **Snapshots** | Periodic aggregate **snapshots** bound replay cost (fold from the latest snapshot, not from genesis). Snapshots are **derived and disposable** (rebuildable from facts) — never authoritative. |
| **Retention** | Facts retained per policy; **compliance-critical facts (decisions, verdicts, consent, integrity) retained longest** (§11). Retention is a business policy (ARCH-05 §10.3), not a storage convenience. |
| **Compaction** | ⚠️ **Authoritative fact streams are NEVER log-compacted** (AD-63) — compaction (keeping only latest-per-key) destroys history and defeats audit/replay. Growth is managed by **snapshots + cold-tiering** (older facts to cheaper storage, still readable), not by discarding facts. |
| **Schema evolution** | Facts evolve **additively** with **tolerant readers** (same rule as ARCH-07 AD-54): new optional fields; a breaking change is a new fact version, old readers unaffected. Never rewrite historical facts to a new shape. |
| **Recovery** | The fact log is backed up and (for Critical services) cross-region replicated; state and read models are recovered by **replay** (§10). |

> ### AD-63 — Authoritative business-fact streams are never compacted or mutated; volume is managed by snapshots and cold-tiering.

---

## 5. Read Models

| Concern | Decision |
|---|---|
| **Projection ownership** | A read model is owned by its **consuming** service (e.g., Decision owns its "delivered recommendations" read model; Export owns its "decided items" read model; the recruiter dashboard owns its campaign/candidate views). Owners never write to another service's authoritative store. |
| **Rebuild strategy** | Every read model is **rebuildable by replaying facts** from the log (AD-65). A corrupt or schema-changed projection is **dropped and rebuilt**, never hand-patched. |
| **Materialization** | Projections update **asynchronously** by consuming facts (ARCH-07 AD-59 eventual). Consumers are **idempotent** (dedupe by event id, ARCH-06 AD-44) so at-least-once delivery is safe. |
| **Consistency expectations** | **Eventual** across services; **read-your-writes** only within the authoritative owner. Consumers that need immediate truth use a synchronous query to the owner (the two hot-path exceptions: consent, integrity). |
| **Fan-out** | One fact feeds **many** projections (dashboards, search, decision inputs, future analytics). Fan-out is by subscription; adding a new projection never touches producers (this is how post-MVP moat capabilities attach — ARCH-06 §14). |
| **Projection failures** | A failing projection **degrades reads** (stale/unavailable view) but **never corrupts truth**. Alert + rebuild. A poison fact is dead-lettered per key without blocking others (ARCH-06 §7). |

> ### AD-65 — Read models are always derived and rebuildable from the fact log; never a source of truth. Any projection may be dropped and rebuilt without data loss.

---

## 6. File Persistence

Covers resumes, raw work samples (evidence source), attachments, and export artifacts.

| Concern | Decision |
|---|---|
| **What is a file** | Large opaque content that doesn't belong in an aggregate's state. The aggregate stores a **reference** (identity) to the file (ARCH-04 §5 reference-by-identity); the file lives in object storage. |
| **Content addressing** | Files are **content-addressed** (identified by a content hash). This gives free deduplication and ties directly to Intelligence Compute's **content-hash idempotency** (ARCH-07 AD-56): same work sample → same evidence computation. |
| **Checksums** | The content hash **is** the integrity check; corruption is detectable on read. |
| **Versioning** | File content is **write-once**; a "new version" is new content with a new address. Evidence source files are immutable (supports INV-b). |
| **Virus / malware scanning** | **On ingest, before any processing** — an admission gate. Unscanned/failed content never reaches evidence or the LLM edge. |
| **Retention** | Per consent + retention policy (§11); resume/work-sample files are high-PII and expire with consent. |
| **Encryption** | Envelope-encrypted at rest with **per-tenant data keys** (§9); enables crypto-shred. |
| **PII handling** | Files are the highest-PII asset. Access **only via short-lived, tenant-scoped, audited references** — never public URLs. **PII is minimized before any external model call** (ARCH-06 §10.6); raw files never leave the trust boundary un-minimized. |

---

## 7. Caching Architecture

| Cache | Purpose | Invalidation / TTL | Fail behavior |
|---|---|---|---|
| **Authorization / claims** | avoid re-resolving tenant+permissions per call | short TTL; invalidate on `UserAccessRevoked` | **fail closed** (miss ⇒ re-check authoritative) |
| **Consent status** | make the hot-path gate fast | **very short TTL + event-invalidate on `ConsentWithdrawn/Expired`** | **fail closed** — on miss/uncertainty/staleness, re-check Consent authoritatively; never assume consent |
| **Reference / calibration** | calibration is immutable post-freeze (INV-c) | cache freely; effectively immutable | safe (immutable) |
| **Capability results** | reuse expensive AI computations | keyed by input **content-hash**; long-lived | safe (derived; recompute on miss) |
| **Read-model / dashboard** | fast reads | TTL + event-invalidate | degrade to slightly-stale or refetch |

**Rules:** caches are **never authoritative** (AD-67). A cache for a **gate** (consent, authz) **fails closed**: uncertainty resolves to re-checking the source, never to permitting. **Warmup** for predictable hot data (active-campaign calibration); **cold start** tolerated because misses fall back to authoritative sources, never to wrong answers.

> ### AD-67 — Caches are never authoritative; gate-related caches (consent, authorization) fail closed on miss, staleness, or uncertainty.

---

## 8. Search Architecture

| Search | Purpose | Owner | Rebuild | Tenant safety |
|---|---|---|---|---|
| **Operational search** | find campaigns/candidates in the recruiter UI | search projection off Candidate/Campaign facts | replay/reindex from source | **per-tenant scoping mandatory** |
| **Candidate search** | locate candidates within a tenant | Candidate-owned projection | reindex | tenant-partitioned indices or hard tenant filters |
| **Evidence search** | find evidence within a campaign/tenant | Evaluation-owned projection | reindex from facts | tenant + campaign scoped; **never cross-tenant** |
| **Audit search** | governed investigation | Audit-owned index | reindex from WORM facts | governed, tenant-scoped, itself audited |
| **Semantic / vector search** *(future)* | evidence graph, hiring memory (deferred) | Evidence Graph / Hiring Memory (post-MVP) | rebuild from facts | aggregate/anonymized across tenants (INV-8); per-tenant otherwise |

**Rules:** all indices are **derived and rebuildable** (never authoritative); **index ownership** follows the source's owner; **tenant isolation in the index is a first-class risk** — a shared, unpartitioned index is a cross-tenant leak vector (§9, INV-10), so indices are either per-tenant or hard-filtered by tenant at query time with the tenant claim enforced below the query layer.

---

## 9. Security

Anchored in DOC-05 Tier-0 (isolation, consent, privacy) and ARCH-06 §10.

| Concern | Decision |
|---|---|
| **Encryption at rest** | All stores envelope-encrypted; **per-tenant data keys** (a tenant's data is encrypted under keys unique to that tenant). |
| **Key management** | Central KMS; keys rotated; **per-subject/per-tenant key hierarchy** so a single key's destruction renders a bounded scope unrecoverable (basis for crypto-shred). |
| **Row/record-level security** | Every record carries its tenant; access is authorized and filtered by tenant **below** the application query layer, so a query bug cannot cross tenants. |
| **Tenant isolation** | **Zero cross-tenant access by construction** (INV-10): partition keys + per-tenant encryption keys + record-level scoping. Cross-tenant access is a hard fail + security alert. |
| **Data masking** | PII masked in non-production and in logs/traces (PII never logged — ARCH-06 §9). |
| **PII retention** | Consent-governed (ARCH-05 §10.3); PII-bearing data expires with consent/retention windows. |
| **Legal deletion vs immutability** | Reconciled by **crypto-shredding** (below) — the only correct way to honor erasure over immutable stores. |
| **Consent** | Persistence use is gated by active consent (CAR-2); consent state is itself durably recorded (proof of consent). |
| **Immutable audit** | Audit is **WORM + hash-chained** (tamper-evident): any alteration is detectable; the chain proves completeness and order. |

> ### AD-64 — Crypto-shredding reconciles immutability with the right to erasure and consent withdrawal.
> Personal data is encrypted under **per-subject keys**. To honor erasure/withdrawal, we **destroy the key**, not the record: the immutable fact/evidence remains (so history, audit, and aggregate integrity are preserved), but its PII becomes **permanently unrecoverable**. The *structural* truth ("an evaluation occurred, then was withdrawn") survives; the *personal content* is gone. This is what lets us hold **both** INV-b/INV-e (immutability) **and** DC-3/INV-11 (consent, privacy, erasure) without contradiction. *(Also the persistence-side resolution of the carried consent-withdrawal question: withdrawal shreds the subject's keys; whether it also forces `EvaluationWithdrawn` remains a business-policy OQ.)*
>
> **Discipline this demands:** crypto-shred is only complete if **no un-encrypted PII copy escapes** into logs, caches, search indices, or projections. Therefore PII in derived stores is either absent, minimized, or encrypted under the same per-subject key — so shredding the key shreds the copies too.

---

## 10. Recovery

Recovery tiers map to ARCH-06 availability classes.

> ### AD-69 — Recovery objectives (RPO/RTO) map to availability tiers: Critical (near-zero RPO, minutes RTO, cross-region), High (low RPO, low RTO), Standard (hours acceptable).

| Mechanism | Decision |
|---|---|
| **Backup** | Continuous backup for authoritative stores; the fact log and object storage are continuously replicated. |
| **Restore** | Restore authoritative state (transactional PITR; fact-log restore); **replay** rebuilds all event-sourced state and every read model on top. |
| **Point-in-time recovery** | Transactional stores support PITR; event-sourced services recover to any point by folding facts up to a timestamp. |
| **Disaster recovery** | Critical services (gates, Decision, Audit) + the fact log + object storage replicate **cross-region**; High/Standard per tier. |
| **Replay** | The core recovery superpower: because facts are immutable and complete, **derived stores are never "backed up" so much as rebuilt** — read models, search, snapshots, and (future) vector/feature stores are all replay-reconstructable. |
| **Read-model rebuild** | Drop + replay; no data loss (AD-65). Routinely exercised (not just in DR) so rebuild is a known-good path. |
| **Cross-region recovery** | Async replication of the fact log + object storage; regional failover restores authoritative sources, then replay reconstructs derived stores. |
| **Consistency of a restore** | A restore is consistent across log + files + read models because authoritative sources (log, transactional, object) are restored first and **derived stores are reprojected** from them — never restored independently to a divergent point. |

---

## 11. Data Lifecycle

One coherent lifecycle per data class; every byte moves through it.

```
 Creation ─▶ Mutation (state) / Append (facts) ─▶ Fact Emission (outbox) ─▶ Projection (read models/search)
     │                                                                              │
     └────────────────────────────────────────────────────────────── Archive (cold-tier) ─▶ Retention window
                                                                                    │
                                          Legal Hold (suspends deletion) ◀──────────┤
                                                                                    ▼
                                                    Expiration ─▶ Deletion (crypto-shred PII; structural fact retained)
```

| Stage | Rule |
|---|---|
| **Creation** | Under an owning service, within a tenant, with the Contract Envelope (ARCH-07 AD-53). |
| **Mutation / Append** | State mutates under optimistic concurrency (§3); facts append immutably (§4). |
| **Fact emission** | Atomic with the state change via outbox (no 2PC). |
| **Projection** | Async fan-out to derived stores (§5); idempotent. |
| **Archive** | Aged authoritative data (esp. facts) cold-tiered, still readable; never compacted away (AD-63). |
| **Retention** | Business-policy windows (ARCH-05 §10.3): compliance facts (decisions, verdicts, consent, integrity) longest; candidate PII per consent. |
| **Legal hold** | **Suspends deletion/expiration** for held scopes; takes precedence over retention expiry; itself audited. |
| **Deletion** | PII deletion = **crypto-shred** (AD-64); structural facts/audit retained. True row deletion is reserved for genuinely non-authoritative, non-audit data. |
| **Expiration** | Automatic at window end, unless under legal hold; expiration events are audited. |

---

## 12. Architecture Decisions *(continuing the log; ARCH-07 ended at AD-59)*

| ID | Decision | Rationale | Alternatives considered |
|---|---|---|---|
| **AD-60** | Persistence follows ownership; no store owns business rules | Rules live in the domain (AD-17); stores keep truth, don't define it | Constraint/trigger-enforced rules (rejected: ownerless invariants, drift) |
| **AD-61** | Polyglot persistence per data responsibility; not one standardized product | Six data kinds with different semantics/lifecycle | Single-DB-for-everything (rejected: shared-DB coupling, wrong fit) |
| **AD-62** | Event-source the gates + Evaluation + Decision; state+outbox elsewhere | Highest audit/replay/reconstruction value where sourced | Source everything (rejected: needless complexity) / source nothing (rejected: loses replay/audit) |
| **AD-63** | Authoritative fact streams never compacted/mutated; snapshots + cold-tiering manage volume | Compaction destroys history/audit | Log compaction (rejected: defeats AD-32/replay) |
| **AD-64** | Crypto-shredding reconciles immutability with erasure/consent-withdrawal | Honor both immutability and privacy without contradiction | Hard-delete records (rejected: breaks audit/immutability) / refuse erasure (rejected: violates DC-3/INV-11) |
| **AD-65** | Read models are derived, rebuildable, never source of truth | Lose a projection, lose no truth (replay) | Authoritative denormalized views (rejected: dual sources of truth) |
| **AD-66** | Files content-addressed, per-tenant encrypted, virus-scanned at ingest, accessed via short-lived scoped references | Integrity, dedup, PII containment, idempotency tie-in | Mutable files / public URLs (rejected: PII + integrity risk) |
| **AD-67** | Caches never authoritative; gate caches fail closed | A cache miss must never permit a gated action | Trust-cache-on-miss (rejected: consent/authz bypass) |
| **AD-68** | Per-tenant encryption keys are the substrate for isolation, crypto-shred, and future residency | One mechanism serves three needs | Single platform key (rejected: no crypto-shred, weaker isolation) |
| **AD-69** | Recovery RPO/RTO tiers map to ARCH-06 availability classes | Recovery investment matches business criticality | Uniform recovery (rejected: over/under-invests) |

## 13. Open Questions *(genuine architectural questions)*

1. **Event backbone topology:** one logical fact log with per-service streams, or per-service event stores federated for audit? (Leaning: one logical backbone, per-key partitioned; confirm before ARCH-10.) Concrete **product** deferred to infra (ARCH-10).
2. **Read-model store per projection:** which projections are relational vs document vs search-backed? (Per projection; decide as views are specified in ARCH-09.)
3. **Consent gate: sync authoritative check vs replicated read model** (carried from ARCH-07 OQ-3): both fail-closed; latency vs freshness. Persistence side favors a very-short-TTL cache invalidated by `ConsentWithdrawn`; confirm.
4. **Vector & feature store selection** for the deferred moat capabilities (Evidence Graph, Hiring Memory, Outcome Learning) — reserve boundaries now, select in ARCH-11 (AI Runtime).
5. **Snapshot cadence & cold-tiering thresholds** — tuning parameters; set with real volume data, not upfront.
6. **Cross-region residency model** (DOC-01 global-ready) — per-tenant key + partition substrate is ready (AD-68); residency routing/timing deferred.

## 14. Risks

- **Derived/source divergence:** a projection bug yields wrong reads. *Mitigation:* rebuildability (AD-65), routine rebuild drills, idempotent projections.
- **Crypto-shred leakage:** a stray un-encrypted PII copy (log, cache, index) survives key destruction and defeats erasure. *Mitigation:* PII never in logs/traces (ARCH-06 §9); derived PII encrypted under the same per-subject key or minimized/absent (AD-64 discipline).
- **Event-store growth / replay time:** long streams slow reconstruction. *Mitigation:* snapshots + cold-tiering (AD-63); measured cadence (OQ-5).
- **Search index as cross-tenant leak:** shared unpartitioned index. *Mitigation:* per-tenant scoping enforced below query layer (§8, AD-68).
- **Polyglot operational burden vs team size:** many store types strain a small team. *Mitigation:* AD-61 MVP note — same product/separate schemas at MVP; introduce specialized stores (vector/feature) only when the capability that needs them is built.
- **Restore inconsistency across stores:** authoritative + derived restored to divergent points. *Mitigation:* restore authoritative first, reproject derived (§10) — never restore derived independently.
- **Retention vs legal hold conflict:** expiry deletes data under hold. *Mitigation:* legal hold takes precedence, suspends expiration, is audited (§11).
- **Object-storage PII exposure:** long-lived/public file references. *Mitigation:* short-lived, scoped, audited references only (AD-66).

## 15. Deferred

- **To ARCH-09 (API/Contract Specifications):** the concrete read-model/query shapes as contract projections (this doc names ownership/consistency; ARCH-09 shapes them). Still no SQL/DDL.
- **To ARCH-10 (Deployment Architecture):** concrete store **products**, cluster topology, replication config, backup schedules, region layout, infra/cloud specifics, DDL/migrations/indexes/ORM.
- **To ARCH-11 (AI Runtime Architecture):** vector store, feature store, embedding lifecycle, and Intelligence Compute's caching/registry mechanics for the AI path.
- **To ARCH-12 (Operational Architecture):** backup/restore runbooks, DR drills, retention-enforcement operations, key-rotation and crypto-shred operational procedures, data-lifecycle automation.

---

*End of ARCH-08 v0.1 — the Persistence Architecture. Every byte the platform stores now has an owner (the aggregate/service, AD-60), a kind (state / fact / view / file / derived / cache, §1), a technology chosen for its responsibility (AD-61), a lifecycle (§11), a retention policy (§11), a recovery strategy (§10, via replay for everything derived), and a business justification traced to ARCH-01→07. Immutability and erasure are reconciled by crypto-shredding (AD-64). Nothing exists "because the database needs it." Next: ARCH-09 — API Specifications, the mechanical projection of ARCH-07 contracts and ARCH-08 read models onto concrete transports.*
