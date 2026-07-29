# ARCH-09 — Interface Specifications

| Field | Value |
|---|---|
| **Document ID** | ARCH-09 |
| **Title** | Interface Specifications (the generated projection of the contract model) |
| **Owner** | Principal API Architect + Enterprise Integration Architect + Distributed Systems Architect (OpenAPI / Protobuf / AsyncAPI designers) |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture → Implementation projection |
| **Depends on** | **ARCH-07 (contracts — the source of truth)**, ARCH-08 (persistence/read models), ARCH-06 (services/transports), ARCH-05 (facts), ARCH-04 (interactions), ARCH-03 (domain), ARCH-01/02 |
| **Blocks** | Code generation, ARCH-10 (Deployment), service implementation |
| **The one question** | **"What are the concrete, implementation-ready specifications that project the ARCH-07 contracts onto their transports — without becoming a second source of truth?"** |
| **This document IS** | Four synchronized specification families — **OpenAPI** (external REST), **Protobuf/gRPC** (internal RPC), **AsyncAPI** (business events), **JSON Schema** (payloads + the envelope) — each a *projection* of an ARCH-07 contract. |
| **This document is NOT** | A place to invent contracts, endpoints, fields, or behavior. **ARCH-07 is authoritative; this regenerates from it.** |

> **How to read this document.** The specifications below are **representative, fully-worked projections** that fix the generation rules unambiguously. The **Contract Registry (§5)** is the *complete* enumeration of every contract, and the **Cross-Reference Matrix (§6)** maps each to its four artifacts. Because the projection rules are deterministic (§0.3), every contract not shown in full projects **mechanically** by the same rules — that is the point: ARCH-09 is generatable, not authored.

---

## 0. Specification Philosophy

### 0.1 The chain
```
 Business (ARCH-01/02) → Domain (ARCH-03) → Interactions (ARCH-04) → Facts (ARCH-05)
        → Distributed Services (ARCH-06) → CONTRACTS (ARCH-07)  ← the source of truth
                                              │
                                              ▼   projection (this document)
        Specifications (OpenAPI · Protobuf · AsyncAPI · JSON Schema)
                                              │
                                              ▼
                                   Code → Deployment
```
Every artifact in ARCH-09 is **downstream** of an ARCH-07 contract. A specification adds *transport detail* (verbs, status codes, wire shapes, streaming) but **never** business meaning. If a spec seems to need a rule that isn't in ARCH-07, the rule is missing from ARCH-07 — fix it there, then regenerate here.

### 0.2 Why specifications must be projections, not sources
A contract stated once (ARCH-07) and projected four ways stays consistent. A contract *duplicated* into four hand-maintained spec files drifts — the exact failure mode ARCH-03 §0 warned about, now at the wire. So:

> ### AD-70 — Specifications are generated artifacts, not authoritative artifacts.
> OpenAPI, Protobuf, AsyncAPI, and JSON Schema are **projections** of ARCH-07 contracts. They never redefine business behavior. If ARCH-07 changes, ARCH-09 is **regenerated**; a spec is never edited in isolation. CI enforces this: a spec that diverges from its contract fails the build (drift check). **The contract is truth; the spec is a view of truth.**

### 0.3 The deterministic projection rules *(what makes this generatable)*
| ARCH-07 concept | Projects to |
|---|---|
| **Command** (state-changing) | OpenAPI operation (write) **and/or** Protobuf unary RPC; JSON Schema for its payload; produces event(s) in AsyncAPI |
| **Query** (read) | OpenAPI operation (read) **and/or** Protobuf unary RPC; JSON Schema for request/response |
| **Business Event** (fact) | AsyncAPI message on a channel; JSON Schema for its payload |
| **Capability invocation** (Intelligence Compute) | Internal Protobuf RPC only (never external; produces no event) |
| **File contract** | OpenAPI multipart (external) / reference exchange |
| **Contract Envelope** (AD-53) | Shared JSON Schema `$ref`; REST headers; gRPC metadata; AsyncAPI message header |
| **Error category** (ARCH-07 §7) | HTTP status + `problem+json` / gRPC status code (§0.5) |

**Transport binding (from ARCH-06 §4):**
> ### AD-74 — External surface = OpenAPI/REST at the edge; internal service-to-service = Protobuf/gRPC; business events = AsyncAPI over the fact log. One contract may project to more than one transport; its meaning is identical across all.

### 0.4 Envelope is server-resolved where it must be trusted
> ### AD-71 — Tenant context is derived from the authenticated principal, never from a client-supplied header, field, or path.
> A client can assert an idempotency key and a correlation id (untrusted-but-harmless), but **tenant and authorization are resolved server-side from the access token** (ARCH-06 §10). This closes the obvious cross-tenant spoofing hole (INV-10) at the specification layer, before any handler runs.

### 0.5 Canonical error mapping *(ARCH-07 §7 → transports)*
> ### AD-72 — Business error categories map to a fixed status set; error bodies are `application/problem+json` (RFC 9457) with a stable machine-readable `type`.

| ARCH-07 error | HTTP | gRPC | Retry |
|---|---|---|---|
| Validation Error | `400` | `INVALID_ARGUMENT` | ❌ |
| Authentication missing/invalid | `401` | `UNAUTHENTICATED` | ❌ |
| Authorization Error | `403` | `PERMISSION_DENIED` | ❌ (security-audited) |
| Not found (identity) | `404` | `NOT_FOUND` | ❌ |
| Conflict (version/state) | `409` | `ABORTED` (carries current version) | ⚠️ after reconcile |
| Business Error / Gate Hold / Precondition | `422` | `FAILED_PRECONDITION` | ❌ (state must change) |
| Rate limited | `429` | `RESOURCE_EXHAUSTED` | ⚠️ backoff |
| Retryable transient | `503` | `UNAVAILABLE` | ✅ (idempotent) |
| Permanent internal | `500` | `INTERNAL` | ❌ |

---

## 1. OpenAPI Specification *(external REST — the edge surface)*

**Conventions (projection rules):** OpenAPI 3.1; base path carries the **major** version (`/v1`); resources are plural nouns named in DOC-04 canonical terms; **write commands** are POST to a resource/sub-resource (imperative business actions modeled as sub-resource creations, e.g., `…/activation`, `…/decision`); **queries** are GET; cursor pagination (`cursor`,`limit`,`next_cursor`); `Idempotency-Key` header mandatory on every write (AD-57); `traceparent` (W3C) + optional `X-Correlation-Id`; **no `X-Tenant` header** (tenant from token, AD-71); errors as `problem+json` (AD-72).

```yaml
openapi: 3.1.0
info:
  title: Hiring Intelligence Platform — External API
  version: "1.0.0"            # projects ARCH-07 contract major.minor.patch
  description: >
    Generated projection of ARCH-07 contracts. NOT a source of truth.
    Regenerate on ARCH-07 change (AD-70).
servers:
  - url: https://api.{tenant-domain}/v1
security:
  - oauth2: [platform.act]     # tenant + permissions resolved from token (AD-71)

paths:
  /campaigns:
    post:                                   # ← ARCH-07 command: CreateCampaign (A1)
      operationId: createCampaign
      summary: Create an Evaluation Campaign (Draft)
      parameters:
        - $ref: '#/components/parameters/IdempotencyKey'
        - $ref: '#/components/parameters/TraceParent'
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/CreateCampaignPayload' }
            examples:
              default:
                value:
                  roleReference: { externalRoleId: "req-8842", title: "Senior Backend Engineer" }
                  clientCampaignKey: "camp-key-0001"
      responses:
        '201':
          description: Campaign created (Draft). Emits CampaignCreated.
          headers:
            Location: { schema: { type: string } }
          content:
            application/json:
              schema: { $ref: '#/components/schemas/CampaignView' }
        '409': { $ref: '#/components/responses/Conflict' }
        '422': { $ref: '#/components/responses/BusinessError' }
        '403': { $ref: '#/components/responses/Forbidden' }

  /campaigns/{campaignId}/activation:
    post:                                   # ← command: ActivateCampaign (A3); freezes calibration (INV-c)
      operationId: activateCampaign
      parameters:
        - $ref: '#/components/parameters/CampaignId'
        - $ref: '#/components/parameters/IdempotencyKey'
      responses:
        '200':
          description: Campaign Active; calibration frozen. Emits CampaignActivated.
          content: { application/json: { schema: { $ref: '#/components/schemas/CampaignView' } } }
        '422': { $ref: '#/components/responses/BusinessError' }   # e.g., calibration missing

  /campaigns/{campaignId}/candidates:
    post:                                   # ← command: ImportCandidates (A2) — file contract (CSV + resumes)
      operationId: importCandidates
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                manifest: { type: string, format: binary, description: "CSV" }
                resumes:  { type: array, items: { type: string, format: binary } }
      responses:
        '202':
          description: Import accepted (async). Per-row outcomes via import status. Emits CandidateImported×n.
          content: { application/json: { schema: { $ref: '#/components/schemas/ImportAccepted' } } }
    get:                                    # ← query: ListCampaignCandidates (roster)
      operationId: listCampaignCandidates
      parameters:
        - $ref: '#/components/parameters/CampaignId'
        - $ref: '#/components/parameters/Cursor'
        - $ref: '#/components/parameters/Limit'
      responses:
        '200':
          content:
            application/json:
              schema: { $ref: '#/components/schemas/CandidatePage' }

  /candidate-evaluations/{candidateEvaluationId}/work-sample:
    post:                                   # ← command: SubmitWorkSample (A5) — candidate actor
      operationId: submitWorkSample
      security: [ { oauth2: [candidate.submit] } ]
      parameters:
        - $ref: '#/components/parameters/IdempotencyKey'
      requestBody:
        content: { application/json: { schema: { $ref: '#/components/schemas/WorkSamplePayload' } } }
      responses:
        '202': { description: "Submitted (async evaluation). Emits WorkSampleSubmitted." }
        '422': { $ref: '#/components/responses/BusinessError' }   # consent inactive → gate hold

  /candidate-evaluations/{candidateEvaluationId}/decision:
    post:                                   # ← command: RecordHiringDecision (A12) — HUMAN (HM) only
      operationId: recordHiringDecision
      security: [ { oauth2: [hiring_manager.decide] } ]          # human principal required (INV-1)
      parameters:
        - $ref: '#/components/parameters/IdempotencyKey'
      requestBody:
        content: { application/json: { schema: { $ref: '#/components/schemas/HiringDecisionPayload' } } }
      responses:
        '201': { description: "Decision recorded (immutable). Emits HiringDecisionRecorded." }
        '422':
          $ref: '#/components/responses/BusinessError'            # no RecommendationDelivered → precondition (CAR-5)

components:
  securitySchemes:
    oauth2:
      type: oauth2
      flows: { authorizationCode: { authorizationUrl: "…", tokenUrl: "…", scopes: {} } }
  parameters:
    CampaignId: { name: campaignId, in: path, required: true, schema: { type: string } }
    IdempotencyKey:
      name: Idempotency-Key, in: header, required: true            # AD-57
      schema: { type: string, maxLength: 128 }
    TraceParent: { name: traceparent, in: header, required: false, schema: { type: string } }
    Cursor: { name: cursor, in: query, required: false, schema: { type: string } }
    Limit:  { name: limit, in: query, required: false, schema: { type: integer, maximum: 100, default: 25 } }
  responses:
    Conflict:
      description: State moved under the caller (optimistic concurrency).
      content:
        application/problem+json:
          schema: { $ref: '#/components/schemas/Problem' }
          example: { type: "https://errors.platform/conflict", title: "Version conflict", status: 409, currentVersion: 7 }
    BusinessError:
      description: Valid request the business refuses (incl. gate hold / unmet precondition).
      content: { application/problem+json: { schema: { $ref: '#/components/schemas/Problem' } } }
    Forbidden:
      description: Authorization failed (tenant/permission).
      content: { application/problem+json: { schema: { $ref: '#/components/schemas/Problem' } } }
  schemas:
    Problem:                                # RFC 9457 (AD-72)
      type: object
      required: [type, title, status]
      properties:
        type: { type: string, format: uri }
        title: { type: string }
        status: { type: integer }
        detail: { type: string }
        correlationId: { type: string }
        currentVersion: { type: integer }
    CreateCampaignPayload: { $ref: 'jsonschema/CreateCampaign.command.json' }
    CampaignView:          { $ref: 'jsonschema/Campaign.view.json' }
    WorkSamplePayload:     { $ref: 'jsonschema/SubmitWorkSample.command.json' }
    HiringDecisionPayload: { $ref: 'jsonschema/RecordHiringDecision.command.json' }
    # …remaining schemas $ref the JSON Schemas in §4 (single definition, reused everywhere)
```

**External-surface scope (projection completeness):** the external API exposes only what an external actor may legally invoke (ARCH-04 §2): campaign management, candidate import, invitations, candidate work-sample submission, candidate consent, HM decision, recruiter feedback release, candidate feedback view, export, and admin (org/user). **It exposes nothing a candidate may not see** — there is deliberately *no* external path returning a Recommendation, Evaluation, Integrity, or Fairness internal to a candidate (AD-25/P13). Those forbidden reads have **no endpoint**, which is how the prohibition is enforced at the edge.

---

## 2. Protobuf Specification *(internal gRPC — service-to-service)*

**Conventions:** proto3; one package per service, versioned (`platform.consent.v1`); unary RPCs for commands/queries; **server-streaming** for progressive results (evaluation progress); the **Envelope** is a shared message included on every request; enums are closed and additive (never renumber); backward compatibility by additive fields only (never reuse field numbers).

```protobuf
syntax = "proto3";
package platform.common.v1;

// Shared Contract Envelope (AD-53). Present on every internal request.
// Tenant + principal are populated from the authenticated call context by the
// receiving service's interceptor — a caller-supplied tenant is IGNORED (AD-71).
message Envelope {
  string correlation_id   = 1;   // propagated
  string trace_id         = 2;   // W3C
  string idempotency_key  = 3;   // mandatory on commands (AD-57)
  string caller_identity  = 4;   // workload identity (mTLS/SVID); server-verified
  // tenant_id and authorization are NOT wire fields — resolved server-side (AD-71)
  DataClassification data_class = 5;
}
enum DataClassification { DATA_CLASS_UNSPECIFIED = 0; NON_PII = 1; PII = 2; SENSITIVE_PII = 3; }
```

```protobuf
syntax = "proto3";
package platform.consent.v1;
import "platform/common/v1/envelope.proto";

// ← ARCH-07 query IsConsentActive — the synchronous, fail-closed gate (ARCH-07 §3)
service ConsentService {
  rpc IsConsentActive (IsConsentActiveRequest) returns (IsConsentActiveResponse);
  rpc RecordConsentGrant (RecordConsentGrantRequest) returns (ConsentView);  // candidate-authored
}
message IsConsentActiveRequest {
  platform.common.v1.Envelope envelope = 1;
  string candidate_id = 2;
  string campaign_id  = 3;
}
message IsConsentActiveResponse {
  bool active = 1;                 // on ANY uncertainty the caller treats as false (fail closed, AD-67)
  ConsentScope scope = 2;
  string consent_id = 3;
}
```

```protobuf
syntax = "proto3";
package platform.fairness.v1;
import "platform/common/v1/envelope.proto";

// ← ARCH-07 command AssessFairness (A9) — authoritative, campaign-scoped gate
service FairnessService {
  rpc AssessFairness (AssessFairnessRequest) returns (FairnessVerdict);
}
message AssessFairnessRequest {
  platform.common.v1.Envelope envelope = 1;
  string campaign_id = 2;
  string assessment_round = 3;     // supports interim-vs-full trigger point (OQ)
}
message FairnessVerdict {
  string campaign_id = 1;
  Verdict verdict = 2;             // PASSED / HELD — authoritative; delivery-gating (INV-3)
  string reason = 3;               // present when HELD
}
enum Verdict { VERDICT_UNSPECIFIED = 0; PASSED = 1; HELD = 2; }
```

```protobuf
syntax = "proto3";
package platform.intelligence.v1;
import "platform/common/v1/envelope.proto";

// ← ARCH-07 CAPABILITY invocations (AD-56): NOT commands, produce NO facts.
// Pure, idempotent-by-input-content; owning service validates & commits the fact.
service IntelligenceCompute {
  rpc StructureEvidence (StructureEvidenceRequest) returns (EvidenceProposal);
  rpc Evaluate (EvaluateRequest) returns (stream EvaluationProgress);   // server-streaming progress
  rpc Explain (ExplainRequest) returns (ExplanationProposal);
}
message EvaluateRequest {
  platform.common.v1.Envelope envelope = 1;   // data_class MUST be minimized before external model (ARCH-06 §10.6)
  string candidate_evaluation_id = 2;
  string content_hash = 3;                     // idempotency + cache key (AD-66)
  CalibrationRef calibration = 4;
}
message EvaluationProgress {
  ProgressStage stage = 1;
  EvaluationProposal partial = 2;              // NON-authoritative; the fact is EvaluationCompleted, emitted by Evaluation Service
}
enum ProgressStage { PROGRESS_UNSPECIFIED = 0; STRUCTURING = 1; SCORING = 2; EXPLAINING = 3; DONE = 4; }
```

**Protobuf compatibility rules (projection of ARCH-07 §6):** never renumber/reuse a field; new fields optional and additive; new enum values appended (unknown values tolerated by readers); a breaking change ⇒ a **new package version** (`…v2`) running in parallel until consumers migrate (ARCH-07 AD-54).

---

## 3. AsyncAPI Specification *(business events — the fact log)*

**Conventions:** AsyncAPI 3.0; each business fact (ARCH-05) is a message; channels are named by aggregate; **ordering key** = tenant→campaign→candidate-evaluation (per-key, not global — ARCH-07 §4); messages carry the Envelope header; retention/replay are documented metadata (realized in ARCH-08). Delivery is **at-least-once**, consumers idempotent (ARCH-06 AD-44).

```yaml
asyncapi: 3.0.0
info:
  title: Hiring Intelligence Platform — Business Events
  version: "1.0.0"
  description: Projection of ARCH-05 facts via ARCH-07 event contracts. NOT a source of truth (AD-70).

defaultContentType: application/json

channels:
  recommendations:
    address: fact.evaluation.recommendation           # logical channel (ARCH-08 backbone)
    messages:
      RecommendationDelivered: { $ref: '#/components/messages/RecommendationDelivered' }
      RecommendationFormed:    { $ref: '#/components/messages/RecommendationFormed' }
  fairness:
    address: fact.campaign.fairness
    messages:
      FairnessApproved: { $ref: '#/components/messages/FairnessApproved' }
      FairnessHeld:     { $ref: '#/components/messages/FairnessHeld' }
  decisions:
    address: fact.decision
    messages:
      HiringDecisionRecorded: { $ref: '#/components/messages/HiringDecisionRecorded' }

operations:
  onRecommendationDelivered:
    action: receive
    channel: { $ref: '#/channels/recommendations' }
    summary: Decision & Export subscribe; enables HiringDecisionRecorded (EV-INV-9)
  publishFairnessApproved:
    action: send
    channel: { $ref: '#/channels/fairness' }
    summary: Fairness Service publishes; Evaluation reacts to DELIVER recommendations (EV-INV-7)

components:
  messages:
    RecommendationDelivered:
      name: RecommendationDelivered
      title: A recommendation became available to the human decision-maker
      headers: { $ref: 'jsonschema/Envelope.json' }
      payload: { $ref: 'jsonschema/RecommendationDelivered.event.json' }
      x-producer: EvaluationService
      x-consumers: [DecisionService, ExportService, CampaignService, AuditService]
      x-ordering-key: candidateEvaluationId        # per-key ordering
      x-retention: long-compliance
      x-replayable: true
      x-immutable: true                             # ARCH-05 EV-INV-14
    FairnessApproved:
      name: FairnessApproved
      title: A campaign's evaluations satisfied the fairness gate
      headers: { $ref: 'jsonschema/Envelope.json' }
      payload: { $ref: 'jsonschema/FairnessApproved.event.json' }
      x-producer: FairnessService                    # authoritative creator only (ARCH-05 AD-35)
      x-consumers: [EvaluationService, CampaignService, ExportService, AuditService]
      x-ordering-key: campaignId                     # campaign-scoped
      x-retention: long-compliance
      x-replayable: true
    HiringDecisionRecorded:
      name: HiringDecisionRecorded
      title: A named human recorded the accountable decision
      headers: { $ref: 'jsonschema/Envelope.json' }
      payload: { $ref: 'jsonschema/HiringDecisionRecorded.event.json' }
      x-producer: DecisionService                    # human-authored only (INV-1)
      x-consumers: [FeedbackService, ExportService, CampaignService, AuditService]
      x-ordering-key: candidateEvaluationId
      x-retention: longest-accountability
      x-replayable: true
```

> **Note:** `RecommendationDelivered` has a producer but its *emission* is an event-triggered internal transition, never an external command (AD-58) — there is no operation anywhere that "delivers." Consumers only *receive* it. This is EV-INV-7 made unbypassable at the spec layer.

---

## 4. JSON Schemas *(payloads + the shared envelope)*

**Conventions:** JSON Schema 2020-12; one schema file per payload, referenced (`$ref`) by OpenAPI/AsyncAPI so there is a **single definition** reused across transports; the **Envelope** is one shared schema; all business field names use DOC-04 canonical terms; IDs are opaque strings; no PII field is ever `required` beyond what the contract needs.

```json
// Envelope.json — shared across REST headers, gRPC metadata, and event headers (AD-53)
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.platform/Envelope.json",
  "type": "object",
  "required": ["correlationId", "occurredAt"],
  "properties": {
    "correlationId":  { "type": "string" },
    "traceId":        { "type": "string" },
    "idempotencyKey": { "type": "string", "maxLength": 128 },
    "occurredAt":     { "type": "string", "format": "date-time" },
    "dataClass":      { "enum": ["NON_PII", "PII", "SENSITIVE_PII"] }
  },
  "comment": "tenantId and authorization are NOT in payloads/headers — resolved server-side (AD-71)."
}
```

```json
// RecordHiringDecision.command.json — ← ARCH-07 command A12
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.platform/RecordHiringDecision.command.json",
  "type": "object",
  "required": ["candidateEvaluationId", "recommendationId", "outcome"],
  "properties": {
    "candidateEvaluationId": { "type": "string" },
    "recommendationId":      { "type": "string" },
    "outcome":               { "enum": ["ADVANCE", "HOLD", "REJECT"] },
    "overrideJustification": { "type": "string" }
  },
  "allOf": [
    { "if":   { "properties": { "outcome": { "const": "REJECT" } } },
      "then": { "required": ["overrideJustification"],
                "$comment": "required when divergent from the delivered Recommendation (INV-d / CAR-5)" } }
  ]
}
```

```json
// RecommendationDelivered.event.json — ← ARCH-05 fact
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.platform/RecommendationDelivered.event.json",
  "type": "object",
  "required": ["candidateEvaluationId", "recommendationId", "occurredAt"],
  "properties": {
    "candidateEvaluationId": { "type": "string" },
    "recommendationId":      { "type": "string" },
    "recommendationLevel":   { "enum": ["ADVANCE", "HOLD", "NOT_A_FIT_HERE"] },
    "explanationReference":  { "type": "string" },
    "occurredAt":            { "type": "string", "format": "date-time" }
  },
  "$comment": "No Evaluation Score / Confidence here — those are not in the candidate-adjacent fact; consumers needing them query the owner (audience projection, P13)."
}
```

**Schema evolution (projection of ARCH-07 AD-54):** additive optional fields only; **tolerant readers** ignore unknown fields; a breaking change is a new `$id`/major version run in parallel. Schemas are validated in CI against the contract registry (§5) and against every registered consumer contract (ARCH-07 AD-55).

---

## 5. Contract Registry *(the complete enumeration — this is the exhaustive list)*

*Every contract from ARCH-07, its owner (ARCH-06 service), version, consumers, and lifecycle. `EXT`=OpenAPI, `RPC`=Protobuf, `EVT`=AsyncAPI, `JS`=JSON Schema. Status per DOC-04 lifecycle discipline.*

| Contract | Kind | Owner | Projects to | Consumers | Ver | Status |
|---|---|---|---|---|---|---|
| ProvisionOrganization | cmd | Identity | EXT·JS | platform-admin | 1.0 | Stable |
| GrantUserAccess / RevokeUserAccess | cmd | Identity | EXT·JS·EVT | org-admin | 1.0 | Stable |
| CreateCampaign | cmd | Campaign | EXT·JS·EVT | Recruiter | 1.0 | Stable |
| SetCalibration | cmd | Campaign | EXT·JS | Recruiter/HM | 1.0 | Stable |
| ActivateCampaign | cmd | Campaign | EXT·JS·EVT | Recruiter | 1.0 | Stable |
| ConcludeCampaign | cmd | Campaign | EXT·JS·EVT | Recruiter | 1.0 | Stable |
| CancelCampaign | cmd | Campaign | EXT·JS·EVT | Recruiter | 1.0 | Stable |
| ImportCandidates | cmd (file) | Candidate | EXT·JS·EVT | Recruiter | 1.0 | Stable |
| ListCampaignCandidates | query | Campaign | EXT·JS | Recruiter | 1.0 | Stable |
| RequestConsent | cmd | Consent | EXT·JS·EVT | system | 1.0 | Stable |
| RecordConsentGrant | cmd | Consent | EXT·RPC·JS·EVT | candidate | 1.0 | Stable |
| WithdrawConsent | cmd | Consent | EXT·JS·EVT | candidate | 1.0 | Stable |
| IsConsentActive | query | Consent | RPC·JS | Evaluation | 1.0 | Stable |
| InviteCandidate | cmd | Evaluation | RPC·JS·EVT | Campaign/system | 1.0 | Stable |
| SubmitWorkSample | cmd (file) | Evaluation | EXT·JS·EVT | candidate | 1.0 | Stable |
| VerifyIntegrity | cmd | Integrity | RPC·JS·EVT | Evaluation | 1.0 | Stable |
| AssessFairness | cmd | Fairness | RPC·JS·EVT | Campaign | 1.0 | Stable |
| StructureEvidence / Evaluate / Explain | capability | Intelligence Compute | RPC·JS | Evaluation/Feedback | 1.0 | Stable |
| GetCalibration | query | Campaign | RPC·JS | Evaluation | 1.0 | Stable |
| GetRecommendationForDecision | query | Evaluation | RPC·JS | Decision | 1.0 | Stable |
| RecordHiringDecision | cmd | Decision | EXT·JS·EVT | HM (human) | 1.0 | Stable |
| ReleaseFeedback | cmd | Feedback | EXT·JS·EVT | Recruiter (human) | 1.0 | Stable |
| GetCandidateFeedback | query | Feedback | EXT·JS | candidate | 1.0 | Stable |
| AssembleExport / DeliverExport | cmd | Export | EXT·JS·EVT | Recruiter | 1.0 | Stable |
| GetExportStatus | query | Export | EXT·JS | Recruiter | 1.0 | Stable |
| GetAuditTrail | query | Audit | EXT(admin)·JS | governance | 1.0 | Stable |
| **Events** (all ARCH-05 facts) | event | respective owner | EVT·JS | see AsyncAPI x-consumers | 1.0 | Stable |

> The registry is the **single index** of what exists and who owns it (mirrors DOC-04 Term Registry / ARCH-07 contract ownership). A specification file not traceable to a registry row does not belong in the build.

---

## 6. Cross-Reference Matrix *(nothing exists without tracing to ARCH-07 → ARCH-05/04/03)*

| Business Contract (ARCH-07) | OpenAPI | Protobuf | AsyncAPI | JSON Schema | Origin (ARCH-04/05) → aggregate (ARCH-03) |
|---|---|---|---|---|---|
| CreateCampaign | `POST /campaigns` | — | `CampaignCreated` | `CreateCampaign.command` | A1 → Evaluation Campaign |
| ActivateCampaign | `POST …/activation` | — | `CampaignActivated` | — | A3 → Campaign (calibration freeze INV-c) |
| ImportCandidates | `POST …/candidates` | — | `CandidateImported` | multipart | A2 → Candidate |
| RecordConsentGrant | `POST …/consent` | `ConsentService.RecordConsentGrant` | `ConsentGranted` | `…command` | A15 → Consent |
| IsConsentActive | — | `ConsentService.IsConsentActive` | — | `…query` | §5 read dep → Consent (gate) |
| SubmitWorkSample | `POST …/work-sample` | — | `WorkSampleSubmitted` | `…command` | A5 → Candidate Evaluation |
| VerifyIntegrity | — | `IntegrityService.Verify` | `IntegrityVerified` | `…command` | A7 → Integrity verdict |
| AssessFairness | — | `FairnessService.AssessFairness` | `FairnessApproved`/`Held` | `…command` | A9 → Campaign Fairness Verdict |
| Evaluate (capability) | — | `IntelligenceCompute.Evaluate` | — (no fact) | `…request/proposal` | AD-56 → (no aggregate) |
| GetRecommendationForDecision | — | `EvaluationService.GetRecommendationForDecision` | — | `…query` | §5 → Candidate Evaluation |
| RecordHiringDecision | `POST …/decision` | — | `HiringDecisionRecorded` | `…command` | A12 → Hiring Decision (human, INV-1) |
| ReleaseFeedback | `POST …/feedback/release` | — | `FeedbackReleased` | `…command` | A13 → Feedback |
| GetCandidateFeedback | `GET …/feedback` | — | — | `…view` | §5 → Feedback (candidate-only, P13) |
| AssembleExport/DeliverExport | `POST …/exports` | — | `Export…` | `…command` | A14 → Export Package |
| (all facts) | — | — | AsyncAPI messages | `*.event` | ARCH-05 |

> Every row terminates in an ARCH-07 contract and an ARCH-05/04 origin bound to an ARCH-03 aggregate. **No orphan specifications.** The forbidden reads (Recommendation→Candidate, cross-tenant) appear **nowhere** in any of the four artifacts — absence is the enforcement.

---

## 7. Architecture Decisions *(continuing the log; ARCH-08 ended at AD-69)*

| ID | Decision | Rationale | Alternatives |
|---|---|---|---|
| **AD-70** | Specifications are generated projections, not authoritative | One source of truth (ARCH-07); no drift | Hand-authored specs (rejected: dual truth) |
| **AD-71** | Tenant/authorization resolved server-side from the principal, never wire-supplied | Closes cross-tenant spoofing (INV-10) at the spec layer | Client `X-Tenant` header (rejected: spoofable) |
| **AD-72** | Fixed error-category → status mapping; `problem+json` bodies | Consistent, machine-readable errors across services | Ad-hoc per-service errors (rejected: inconsistent) |
| **AD-73** | Single shared Envelope + payload JSON Schemas `$ref`'d by all transports | One definition, reused → no divergence between REST/gRPC/events | Per-transport duplicated schemas (rejected: drift) |
| **AD-74** | External=OpenAPI/REST, internal=Protobuf/gRPC, events=AsyncAPI; a contract may project to several, meaning identical | Right tool per surface (ARCH-06 §4) | One protocol everywhere (rejected: poor fit) |
| **AD-75** | CI drift-check: a spec diverging from its contract fails the build | Enforces AD-70 mechanically | Manual review only (rejected: drift inevitable) |
| **AD-76** | Forbidden interactions are enforced by **absence** — no endpoint/RPC/channel exists for them | The strongest enforcement is no surface at all | Runtime-only checks (rejected: surface invites misuse) |

## 8. Open Questions

1. **External read surface for recruiters/HMs:** REST + polling vs a push channel (server-sent updates) for live campaign/evaluation progress — UX vs surface. (Persistence-side streaming already possible; confirm external transport.)
2. **GraphQL for the recruiter dashboard read side?** Many audience-shaped read models (ARCH-08 §5) could suit a query aggregation layer; risk is over-fetching/coupling (ARCH-07 §13). Decide as read models are specified.
3. **File upload transport at scale:** direct multipart vs pre-signed direct-to-object-storage upload with a reference exchange (ARCH-08 AD-66). Likely the latter for large resumes/work samples.
4. **Event schema registry tooling** (how AsyncAPI/JSON-Schema versions are enforced at runtime) — a build/infra choice → ARCH-10.
5. **Capability streaming granularity:** how fine-grained `EvaluationProgress` should be (UX value vs chattiness).
6. **API version cadence** (when a `/v2` is warranted vs additive `/v1` evolution) — governance detail.

## 9. Risks

- **Spec-as-second-source-of-truth:** the core risk AD-70/AD-75 exist to prevent; a hand-edit that skips regeneration reintroduces drift. *Mitigation:* CI drift-check + generation from the contract registry.
- **Schema duplication across transports:** REST/gRPC/event schemas diverging. *Mitigation:* single shared JSON Schema `$ref`'d everywhere (AD-73).
- **Breaking-change leakage:** an "additive" change that is actually breaking (tightened validation, changed enum semantics). *Mitigation:* consumer-driven contract tests (ARCH-07 AD-55) run against registered consumers in CI.
- **Envelope erosion / tenant spoofing:** a service trusting a wire-supplied tenant. *Mitigation:* AD-71 — tenant never on the wire; interceptors resolve server-side.
- **Forbidden-surface creep:** a well-meaning endpoint that exposes a recommendation to a candidate. *Mitigation:* AD-76 (absence) + cross-reference matrix review; no registry row → no surface.
- **Over-fetching / chatty external reads:** clients pulling whole aggregates. *Mitigation:* audience-shaped views (ARCH-08 §5), pagination, projection limits.
- **Version proliferation:** many parallel majors. *Mitigation:* additive-first + sunset windows (ARCH-07 §6).

## 10. Deferred *(implementation concerns only)*

- **Code generation** from these specs (server stubs, client SDKs, typed models) → build tooling / SPRINT-0.
- **Concrete transport/runtime wiring** (gateway config, mesh, schema-registry product, event backbone product) → ARCH-10 (Deployment).
- **AI-path spec internals** (prompt/model contracts behind Intelligence Compute capabilities) → ARCH-11 (AI Runtime).
- **Operational spec governance** (registry hosting, deprecation automation, contract-test pipelines) → ARCH-12 (Operational).
- **Actual endpoint-by-endpoint completion** for every registry row → mechanical generation from ARCH-07 by the rules in §0.3 (this document fixes the rules and the representative projections; the remainder is generated, not authored).

---

*End of ARCH-09 v0.1 — the Interface Specifications. Four synchronized specification families (OpenAPI · Protobuf · AsyncAPI · JSON Schema), each a projection of an ARCH-07 contract, sharing one Envelope and one set of payload schemas, tracing through the Contract Registry (§5) and Cross-Reference Matrix (§6) back to ARCH-07 → ARCH-05/04 → ARCH-03. Specifications are generated, never authoritative (AD-70); forbidden interactions are enforced by the absence of any surface (AD-76). If ARCH-07 changes, ARCH-09 regenerates. Next: ARCH-10 — Deployment Architecture (concrete products, cluster topology, regions, rollout), where these specifications meet running infrastructure.*
