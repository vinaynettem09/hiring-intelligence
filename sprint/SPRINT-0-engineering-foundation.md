# SPRINT-0 — Engineering Foundation

| Field | Value |
|---|---|
| **Document ID** | SPRINT-0 |
| **Title** | Engineering Foundation (the bridge from frozen architecture to Sprint 1) |
| **Owner** | Staff Engineer (platform) + tech leads |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-23 |
| **Type** | **Implementation document — NOT architecture.** The architecture corpus (DOC-01→12, VALIDATION-01→03, PRODUCT-01, ARCH-01→16) is **frozen under AD-143.** |
| **Depends on** | The frozen corpus. Especially ARCH-06 (services), ARCH-07 (contracts), ARCH-09 (specs), ARCH-10 (deployment), ARCH-11 (AI runtime), ARCH-16 (governance/monorepo AD-137) |
| **The one question** | **"What engineering work must exist before writing business features?"** |
| **Hard scope rule** | **Scaffolding only.** No business functionality, no Candidate Evaluation, no AI reasoning, no domain logic. Every service is an empty, deployable shell; every platform capability is an interface with no body; the AI provider is a deterministic mock. |
| **Decision discipline** | SPRINT-0 introduces **no ADRs** (architecture frozen). Tooling picks are **Foundational Tooling Decisions (FTD)** — implementation choices below the ARB threshold (AD-139), consistent with the corpus. Any choice that rises to architectural significance is escalated as an ADR against the baseline (AD-136). |

> **How to read this.** This document tells a staff team *exactly* what to stand up so that Sprint 1 opens with: a one-command dev environment, green CI, contract-driven codegen with drift detection, thirteen empty-but-deployable services, scaffolded platform interfaces, and observability/security/AI-dev baselines — all wired to the frozen architecture and **containing no business logic.**

---

## 1. Sprint-0 Goals

### 1.1 Definition of Done
Sprint-0 is done when **a new engineer clones the repo, runs one command, and has the entire platform running locally** (all 13 service shells, data plane, observability, mock AI), **CI is green**, **specs generate code with drift detection**, and **nothing business-specific has been implemented.**

### 1.2 Success criteria
- ✅ One-command bootstrap (`make bootstrap && make up`) yields a running local platform.
- ✅ 13 service shells (ARCH-06) build, start, pass health checks, emit a traced request with a correlation ID (ARCH-14 AD-122).
- ✅ Contracts (ARCH-07) → specs (ARCH-09) → **generated code**; CI **drift-check** fails if generated code diverges (AD-70/AD-75).
- ✅ `buf` breaking-change detection + `spectral` + `asyncapi validate` gate contract changes in CI (AD-138/AD-54).
- ✅ Platform interfaces (AD-87) defined as typed contracts with **no implementation** and an in-memory fake for tests.
- ✅ Envelope middleware (AD-53) rejects envelope-less requests; tenant is resolved server-side (AD-71) — enforced by a stub authenticator.
- ✅ A migration runs against a per-service Postgres schema; observability shows the trace end-to-end.
- ✅ Mock AI provider returns deterministic structured proposals; Model Quality Harness scaffold loads a **synthetic** golden dataset.
- ✅ Security scans (SAST, deps, secrets, image) run in CI and block on criticals.

### 1.3 Deliverables
A monorepo (AD-137) containing: repo scaffolding + CODEOWNERS + branch policy; dev environment (devcontainer, Tilt/compose, one-command startup); CI/CD pipelines; 13 service shells (Clean Architecture skeleton); the 9 platform interfaces + fakes; infra scaffolding (Terraform/Helm/Argo CD/network policies); DB + migration foundation; observability stack; security bootstrap; codegen toolchain; testing foundation (unit/integration/contract/e2e); AI-dev foundation (prompt/model registries, mock provider, harness scaffold); DX tooling (Makefile, CLI, pre-commit, VS Code).

### 1.4 Foundational Tooling Decisions (FTD) *(engineering, not architecture)*
| FTD | Choice | Rationale (consistent with frozen arch) |
|---|---|---|
| FTD-1 | **Python 3.12+, FastAPI, Pydantic v2, async everywhere** | ARCH-10 stack; async fits I/O-bound gate/AI-orchestration services |
| FTD-2 | **uv** (deps + workspaces) + **Ruff** (lint+format) + **mypy** (types) | fast, modern, low-ceremony (AD-41 small-team) |
| FTD-3 | **Monorepo via uv workspaces + Make**, with **Pants** adopted when build/test-selection scale demands | AD-137; start light, scale to Pants/Bazel later (AD-41) |
| FTD-4 | **buf** (protobuf lint/breaking/gen), **spectral** (OpenAPI), **asyncapi-cli** (events), **datamodel-code-generator** (JSON Schema/OpenAPI→Pydantic) | mechanical codegen + CI-enforced breaking-change detection (AD-138) |
| FTD-5 | **Alembic** per-service migrations | Python-native; per-service schema ownership (ARCH-08 AD-43) |
| FTD-6 | **Testcontainers** + **Tilt** (k8s dev) / **docker-compose** (lightweight) | real dependencies in tests; fast k8s inner loop |
| FTD-7 | **OTel SDK** → Collector → Prometheus/Tempo/Loki/Grafana | ARCH-14 |
| FTD-8 | **structlog** structured logging + correlation | ARCH-14 AD-122/AD-123 |
| FTD-9 | **Typer** CLI + **pre-commit** + **Makefile** | DX |

*(FTDs are recorded here, not in the AD log; if any proves architecturally significant it becomes an ADR per AD-136.)*

---

## 2. Repository Setup

### 2.1 Monorepo structure (AD-137)
```
platform/                              # single monorepo (AD-137)
├── services/                          # 13 independently-deployable shells (ARCH-06)
│   ├── identity/  candidate/  campaign/  evaluation/  intelligence-compute/
│   ├── integrity/ fairness/  consent/   audit/       decision/
│   └── feedback/  export/    notification/
│       └── <service>/
│           ├── app/
│           │   ├── domain/            # entities/VOs (EMPTY at S0 — no rules)
│           │   ├── application/       # use-cases (EMPTY at S0)
│           │   ├── adapters/          # inbound (api/grpc) + outbound (persistence/platform)
│           │   ├── interface/         # FastAPI app / gRPC server wiring
│           │   └── main.py            # composition root
│           ├── migrations/            # Alembic (schema shell only)
│           ├── tests/
│           ├── Dockerfile
│           └── pyproject.toml
├── libs/
│   ├── platform/                      # AD-87 platform INTERFACES (no impl) + fakes
│   │   ├── event_bus/ object_storage/ cache/ search/ secret_store/
│   │   └── email/ notification/ ai_provider/ identity/
│   ├── envelope/                      # Contract Envelope (AD-53)
│   ├── errors/                        # error model → status mapping (AD-72)
│   ├── telemetry/                     # OTel setup, correlation middleware (AD-122)
│   ├── domain_primitives/             # opaque IDs, TimeWindow, tenant scoping (no business rules)
│   └── testing/                       # fixtures, fakes, synthetic-data helpers
├── contracts/                         # ARCH-07 contract definitions (human-authored inputs)
├── specs/                             # ARCH-09 specs (source for codegen)
│   ├── openapi/  proto/  asyncapi/  jsonschema/
├── generated/                         # codegen OUTPUT (checked in, CI drift-verified)
│   ├── python/{models,grpc,events,clients}/
├── infra/
│   ├── terraform/  helm/  argocd/  k8s/{namespaces,network-policies,mesh}/
├── ai/
│   ├── prompts/                       # Prompt Registry (versioned, metadata) — no judgment prompts yet
│   ├── models/                        # Model Registry (routing config, approved versions)
│   ├── datasets/golden/               # golden-dataset LOADER + SYNTHETIC sample only
│   └── harness/                       # Model Quality Harness scaffold (AD-97) — no real eval
├── tools/                             # CLI (Typer), codegen scripts, dev utilities
├── tests/e2e/                         # cross-service smoke (health/trace only at S0)
├── .github/workflows/                 # CI/CD
├── .devcontainer/  .vscode/  .pre-commit-config.yaml
├── Makefile  Tiltfile  docker-compose.yml
├── CODEOWNERS  pyproject.toml  uv.lock  README.md
```

### 2.2 CODEOWNERS
Maps directories → owning teams, mirroring service/aggregate ownership (ARCH-03/06) and enabling the ARB/derivation-integrity review (AD-139).
```
/services/consent/        @team-trust
/services/integrity/      @team-trust
/services/fairness/       @team-trust
/services/audit/          @team-trust
/services/evaluation/     @team-core
/services/intelligence-compute/ @team-ai
/contracts/ /specs/       @architecture-review-board   # contract/schema changes → ARB (AD-138)
/libs/platform/           @team-platform               # platform interfaces (AD-87)
/ai/                      @team-ai @ai-governance-board # AI artifacts (ARCH-15)
/infra/                   @team-platform @team-security
```

### 2.3 Branch strategy
- **Trunk-based**: short-lived feature branches → PR → `main`. `main` always releasable (GitOps reconciles from `main`, ARCH-10).
- **Required checks** on `main`: lint, types, drift-check, contract-validation, tests, security scans, CODEOWNERS review (ARB review required for `/contracts`, `/specs`).
- **Conventional Commits** (enforced) → automated changelog + semver of contracts.
- **No direct pushes** to `main`; no merge with red CI.

### 2.4 Directory & generated-code conventions
- **`specs/` is input; `generated/` is output.** `generated/` is **checked in** (so diffs are reviewable) and **CI-verified** by regenerating and asserting no diff (drift-check, AD-70/AD-75). Hand-editing `generated/` is a build failure.
- Each service follows the same Clean Architecture layout (§11) so the 13 shells are structurally identical.

---

## 3. Development Environment

| Concern | Decision |
|---|---|
| **Local development** | `uv` virtual env per workspace; services run via `uvicorn`/gRPC locally or in a local `kind` cluster via **Tilt** (live-reload). |
| **Dev containers** | `.devcontainer/` pins Python 3.12, uv, buf, protoc, docker, kubectl, helm, tilt — identical env for every engineer + CI. |
| **Docker** | Multi-stage Dockerfiles (distroless runtime); one base image; images built reproducibly and signed in CI (§9). |
| **Environment variables** | Typed config via Pydantic `BaseSettings` per service; `.env.example` documents every var; **no secrets in env files** committed. |
| **Secrets (local)** | Local dev uses a **fake secret store** (in-memory, from `.env.local` gitignored); real secrets never on laptops (Vault in cloud, §9). |
| **One-command startup** | `make bootstrap` (installs toolchain, generates code, builds) then `make up` (Tilt → local cluster with data plane + observability + mock AI). `make down` tears down. Target: **< 10 min cold, < 60s warm reload.** |

Local data plane (containers): PostgreSQL, **Redpanda** (Kafka-API, lighter than Kafka for local — FTD), Redis, OpenSearch, LocalStack (S3), a fake OIDC issuer, and the OTel/Grafana stack. Managed cloud equivalents (Aurora/MSK/…) are wired only in higher environments (ARCH-10).

---

## 4. CI/CD Foundation

**GitHub Actions**, pipeline-as-code. Every PR runs the full gate; `main` merges trigger image build + Argo CD sync (dev).

### 4.1 Pipeline stages (in order; fail-fast)
```
setup (uv sync, cache)
 → format-check (ruff format --check)
 → lint (ruff check)
 → typecheck (mypy)
 → codegen + DRIFT-CHECK   # regenerate from specs; git diff --exit-code → fail on drift (AD-70/75)
 → contract-validation:
      buf lint + buf breaking (against main)      # protobuf breaking-change gate (AD-138/54)
      spectral lint specs/openapi
      asyncapi validate specs/asyncapi
 → unit tests (pytest -m unit)
 → integration tests (pytest -m integration, testcontainers)
 → consumer-contract tests (pact/schemathesis)   # AD-55
 → security:
      bandit + semgrep (SAST)
      pip-audit / safety (deps)
      gitleaks (secrets)
      trivy (image + fs)
 → build images (multi-arch, distroless) → SBOM (syft) → sign (cosign)  # AD-114
 → push to registry
 → deploy: Argo CD syncs dev (main only)
```

### 4.2 Notes
- **Drift-check** is the mechanical enforcement of "specs are projections" (AD-70): CI regenerates `generated/` and fails on any diff.
- **`buf breaking`** enforces contract compatibility (AD-138/AD-54) — a breaking proto change fails unless it's a governed new major.
- **OpenAPI/Protobuf/AsyncAPI generation** all run in the `codegen` stage (§10); the same command runs locally (`make gen`).
- **Consumer-contract testing** (AD-55) starts as a harness with placeholder pacts (no real consumers yet) so the mechanism exists from day one.
- Security-scan **criticals block**; the pipeline is the first enforcement point of ARCH-13.

---

## 5. Platform Interfaces *(scaffold only — AD-87)*

Each capability is a typed **Protocol** (structural interface) in `libs/platform/`, with **no production implementation** and an **in-memory fake** for tests. Application services depend on the interface, never a product SDK (AD-87). Concrete adapters are Sprint-1+ work.

```python
# libs/platform/event_bus/interface.py
from typing import Protocol, runtime_checkable
from platform_lib.envelope import Envelope

@runtime_checkable
class EventBus(Protocol):
    async def publish(self, *, channel: str, fact: bytes, envelope: Envelope, ordering_key: str) -> None: ...
    async def subscribe(self, *, channel: str, group: str, handler) -> None: ...
    # facts only (ARCH-05); at-least-once + idempotent consumers (AD-44). NO impl at S0.

# libs/platform/ai_provider/interface.py
class AIProvider(Protocol):
    async def invoke(self, *, capability: str, minimized_input: dict, model_ref: str) -> dict: ...
    # the ACL boundary (AD-52). PII already minimized upstream (AD-89). Returns a PROPOSAL (AD-56). NO real model at S0.
```

Interfaces to scaffold (all with a fake + tests, no impl): **EventBus, ObjectStore, Cache, Search, SecretStore, Email, Notification, AIProvider, Identity.** Each interface's docstring cites the ADs it must honor (e.g., Cache fakes must fail-closed for gate caches — AD-67; SecretStore is central — AD-111; Identity resolves tenant server-side — AD-71).

> **Rule:** a service imports `from platform_lib.cache import Cache` (the Protocol) and receives an implementation via DI (§11). At S0 the injected implementation is the fake. Swapping to a real adapter later is a platform-team change, invisible to the service (AD-87).

---

## 6. Infrastructure Bootstrap

Scaffolding only — cloud resources declared but minimal; the goal is the *shape*, not production capacity.

| Concern | Decision |
|---|---|
| **Kubernetes** | `kind` locally; EKS via Terraform for cloud envs (ARCH-10). Cluster hosts stateless shells only (AD-81). |
| **Terraform** | `infra/terraform/` modules: cluster, node pools (general/workers/gpu-reserved), KMS (per-tenant key hierarchy scaffold, AD-84), managed data services (stubbed for dev). State remote + locked. |
| **Helm** | One chart per service (templated from a shared library chart) + umbrella chart; values per environment. |
| **Argo CD** | `infra/argocd/` app-of-apps; reconciles `main` → dev automatically; higher envs gated (ARCH-10 §7). |
| **Namespaces** | Per service-group (ARCH-10 §3): `identity`, `candidate`, `campaign`, `evaluation`, `gates`, `decision-delivery`, `intelligence-compute`, `platform`, `observability`. |
| **Network policies** | **Default-deny**, explicit allows mirroring the ARCH-04 interaction matrix (AD-82) — forbidden interactions have **no** NetworkPolicy allowing them. Scaffolded even for empty services. |
| **Service mesh** | Istio ambient installed; mTLS strict; authz policies scaffolded (deny-by-default) (AD-45/AD-82). |
| **Secrets** | External Secrets Operator + Vault (cloud) / fake (local); no secrets in manifests (AD-111). |
| **ConfigMaps** | Non-secret config via ConfigMaps, generated from typed settings; GitOps-versioned. |

---

## 7. Database Foundation

| Concern | Decision |
|---|---|
| **PostgreSQL** | One logical Postgres, **per-service schema** (no shared datasets — ARCH-08 AD-43); local container, Aurora in cloud. |
| **Migrations** | **Alembic** per service (`services/<svc>/migrations/`); forward-only, reviewed; CI runs migrations against an ephemeral DB. |
| **Migration strategy** | Expand-contract for compatibility (mirrors contract evolution AD-54); RLS + tenant column scaffolded on every table template (INV-10); an `outbox` table template per service (AD-42) — **structure only, no business tables.** |
| **Local seed** | Deterministic, **synthetic**, PII-free seed (tenants/users for dev) — **no candidate/evaluation data** (that's business logic). |
| **Dev database** | Reset/recreate via `make db-reset`; testcontainers spins a fresh Postgres per integration-test run. |

> At S0 the only migrations are: schema creation, the `outbox` table template, an example `_health` table, and RLS scaffolding. **No aggregate tables** (those arrive with domain logic in Sprint 1+).

---

## 8. Observability Bootstrap

| Concern | Decision |
|---|---|
| **OpenTelemetry** | OTel SDK auto-instruments FastAPI, gRPC, asyncpg, httpx, kafka client in every shell. |
| **Collector** | OTel Collector deployment; enriches with tenant + correlation + business-ID attributes; **PII-minimization processor** (AD-123). |
| **Prometheus** | `kube-prometheus-stack`; RED/USE dashboards per service; SLO recording rules scaffolded (ARCH-14 §4). |
| **Tempo** | Traces backend; tail-sampling config (keep errors/holds/AI-escalations) scaffolded. |
| **Loki** | Structured logs (structlog JSON), tenant-tagged, **PII-minimized** (AD-123). |
| **Grafana** | Provisioned dashboards: per-service RED, a **business-health** dashboard shell (AD-105 — panels defined, fed once facts exist), and a trace-explorer. |
| **Correlation IDs** | `libs/telemetry` FastAPI/gRPC middleware mints/propagates a correlation ID + W3C traceparent and attaches business IDs as span attributes (AD-122). |

**S0 proof:** a request to any shell produces a distributed trace with a correlation ID visible in Grafana/Tempo, and a structured, PII-free log line in Loki. No business metrics yet (no facts), but the pipeline and the business-health dashboard shell exist.

---

## 9. Security Bootstrap

| Concern | Decision |
|---|---|
| **OIDC** | Auth middleware validates JWTs (fake issuer locally); **tenant + permissions resolved from the token** (AD-71); a stub returns a dev principal. No real IdP integration logic beyond validation scaffolding. |
| **Envelope enforcement** | `libs/envelope` middleware rejects any request/message lacking the Contract Envelope (AD-53) before business logic — enforced on empty shells too. |
| **SPIFFE** | SPIRE installed with Istio; workloads receive SVIDs; mTLS strict (AD-110/AD-45). |
| **Vault** | Cloud secrets via Vault + ESO; local fake (AD-111). |
| **Certificate management** | cert-manager (edge) + SPIRE (mesh) auto-issue/rotate. |
| **Static scanning** | bandit + semgrep in CI (SAST). |
| **Dependency scanning** | pip-audit/safety + trivy (deps + images); criticals block (AD-114). |
| **Secret scanning** | gitleaks pre-commit + CI. |
| **Supply chain** | SBOM (syft) + image signing (cosign) + admission policy (only signed images) scaffolded (AD-114). |

> S0 proves: an envelope-less request is rejected; a request with a token has its tenant resolved server-side; mTLS is enforced between two shells; a planted secret fails gitleaks; a known-CVE dependency fails the scan.

---

## 10. Code Generation

The mechanical projection ARCH-09 promised: **specs → code**, one command (`make gen`), CI drift-verified.

| Artifact | Tool | Output (`generated/python/`) |
|---|---|---|
| **OpenAPI** (external REST) | `datamodel-code-generator` + FastAPI route stubs | `models/`, `clients/` (typed client SDKs) |
| **Protobuf/gRPC** (internal) | `buf generate` (grpcio) | `grpc/` (stubs + messages) |
| **AsyncAPI** (events) | `asyncapi` generator (or template) | `events/` (typed event classes) |
| **JSON Schema** (payloads + Envelope) | `datamodel-code-generator` | `models/` (shared Pydantic models, incl. Envelope) |
| **SDKs** | derived from above | internal typed client per service |

**Rules:** `generated/` is checked in and **never hand-edited**; drift-check (§4) regenerates and asserts no diff; a spec change → regenerate → review the generated diff in the same PR (AD-137 atomic change). This makes the Business→Contract→Spec→Code chain (AD-138) mechanical from day one.

---

## 11. Coding Standards

**Clean Architecture** inside every service (identical layout across all 13). Business logic stays out at S0; the *structure* is enforced now.

```
app/
├── domain/        # entities, value objects, invariants  (pure; no I/O)      [EMPTY at S0]
├── application/   # use-cases / command+query handlers, ports                [EMPTY at S0]
├── adapters/
│   ├── inbound/   # FastAPI routers, gRPC servicers (call application)
│   └── outbound/  # persistence repos, platform-interface impls (via DI)
├── interface/     # app assembly (FastAPI app, gRPC server), middleware
└── main.py        # composition root: wires adapters → application (DI)
```

| Standard | Rule |
|---|---|
| **Python/FastAPI** | 3.12+, FastAPI, Pydantic v2; one app factory per service. |
| **Async** | Async end-to-end (asyncpg, httpx, aiokafka); no blocking I/O in the event loop. |
| **Error handling** | Domain/application raise typed errors; an edge handler maps them to the **AD-72 error model** (`problem+json` / gRPC status). No leaking stack traces or PII (AD-123). |
| **Logging** | `structlog` JSON, correlation + business IDs bound to context; **never log PII** (AD-123). |
| **Validation** | Pydantic models (generated from specs, §10) validate every inbound payload; reject-by-default. |
| **Dependency injection** | Constructor injection; platform interfaces injected (fakes at S0); FastAPI `Depends` at the edge, explicit wiring in `main.py`. **No service imports a product SDK directly** (AD-87). |
| **Clean Architecture** | Dependencies point inward (adapters → application → domain); domain imports nothing external. Enforced by an import-linter contract in CI. |
| **Tenancy** | Every entry point requires envelope + tenant (AD-53/AD-71); a base handler enforces it. |

---

## 12. Testing Foundation

The test pyramid, wired but mostly empty of business assertions at S0.

| Level | Tooling | S0 scope |
|---|---|---|
| **Unit** | pytest, pytest-asyncio | test scaffolding (e.g., envelope middleware, error mapping, fakes) — no domain rules yet |
| **Integration** | pytest + **Testcontainers** (Postgres, Redpanda, Redis, OpenSearch, LocalStack) | a shell can start, migrate, publish/consume a dummy fact via the EventBus fake→real adapter smoke |
| **Contract** | `buf breaking`, `schemathesis` (fuzz OpenAPI), `pact` (consumer-driven, AD-55) | mechanism live with placeholder pacts; breaking-change gate active |
| **End-to-end** | kind + Tilt (or compose) | cross-service **health + trace propagation** smoke only (no business flows) |
| **Synthetic data** | `faker` + typed builders in `libs/testing` | **PII-free, synthetic** fixtures; **never real candidate data** (ARCH-13); crypto-shred-friendly |

Conventions: markers (`unit`/`integration`/`contract`/`e2e`); coverage gate on `libs/` (not on empty services); every platform-interface fake ships with a conformance test suite so real adapters can be verified against the same suite later.

---

## 13. AI Development Foundation *(scaffold — no reasoning, ARCH-11/15)*

| Component | S0 scaffold |
|---|---|
| **Prompt Registry** | `ai/prompts/` — versioned prompt files with metadata (id, version, capability, model_ref, effective_date, status) and a loader; **no judgment prompts** authored (that's Evaluation-Engine work). Immutable-version discipline (ARCH-11 §5) enforced by the loader. |
| **Model Registry** | `ai/models/` — routing config (capability → approved model version, by tier) + version pinning (ARCH-15 §4); points only at the **mock** at S0. |
| **Local mock provider** | An `AIProvider` implementation returning **deterministic, schema-valid proposals** (fixed by input content-hash) — so dev/CI/tests never call a real LLM, are reproducible (AD-98), and cost nothing. The seam for the real ACL adapter later (AD-52/AD-85). |
| **Model Quality Harness** | `ai/harness/` — scaffold that loads a golden dataset, runs a capability against the mock, and computes placeholder quality/fairness metrics (AD-97). **No real thresholds/judgment** yet; proves the harness pipeline exists (ARCH-15 gate for future changes). |
| **Golden dataset loading** | `ai/datasets/golden/` — schema + loader + a **tiny synthetic, consented-by-construction, PII-free** sample; real dataset curation is governed later (ARCH-15 §5, crypto-shred-aware AD-132). |

> **Hard line:** structured-output *validation* (AD-90) and PII-minimization *hooks* (AD-89) are scaffolded as pass-through stubs; **no evaluation reasoning, scoring, calibration, or fairness logic** is implemented at S0.

---

## 14. Developer Experience

| Tool | Provides |
|---|---|
| **Makefile** | `bootstrap`, `up`, `down`, `gen` (codegen), `lint`, `typecheck`, `test`, `test-int`, `db-reset`, `fmt`, `scan`, `new-service` (scaffold a shell). Single memorable entry point. |
| **CLI** (`platformctl`, Typer) | Scaffolding + dev tasks: `platformctl new service`, `platformctl gen`, `platformctl seed`, `platformctl trace <id>`; wraps the toolchain for humans. |
| **Pre-commit hooks** | ruff (format+lint), mypy (fast), gitleaks, conventional-commit check, spec-lint (spectral/buf), no-hand-edit-generated guard. |
| **VS Code settings** | `.vscode/` — interpreter, Ruff/mypy integration, launch configs to debug any service (attach to uvicorn/gRPC in Tilt), recommended extensions. |
| **Debugging** | debugpy wired in dev images; Tilt exposes debug ports; one-click "Debug <service>" per shell. |

Goal: **a new engineer is productive in under an hour** — clone, open in devcontainer, `make bootstrap && make up`, set a breakpoint, hit a health endpoint, see the trace.

---

## 15. Sprint Exit Criteria

Sprint-0 is complete when **all** of the following are true — and **no business logic exists**:

**Repo & DX**
- [ ] Monorepo (AD-137) with all 13 service shells, `libs/`, `contracts/`, `specs/`, `generated/`, `infra/`, `ai/`, CODEOWNERS, branch protection.
- [ ] `make bootstrap && make up` brings up the full local platform in one command; `platformctl new service` scaffolds a compliant shell.
- [ ] Pre-commit + VS Code + devcontainer working; a new engineer reaches "breakpoint hit on a health request" in < 1 hour.

**Contracts & codegen**
- [ ] `make gen` produces OpenAPI/proto/AsyncAPI/JSON-Schema code into `generated/`; **CI drift-check fails on divergence** (AD-70/75).
- [ ] `buf breaking` + spectral + asyncapi validation gate contract changes (AD-138/54); consumer-contract harness runs (AD-55).

**Services (empty, deployable)**
- [ ] All 13 shells build, containerize (signed + SBOM), pass health/readiness, and deploy to the local cluster via Argo CD.
- [ ] Each shell enforces the Contract Envelope (AD-53) and server-side tenant resolution (AD-71); envelope-less requests are rejected.
- [ ] Clean Architecture layout enforced by import-linter; domain/application layers are **empty**.

**Platform interfaces (AD-87)**
- [ ] All 9 interfaces defined as typed Protocols with **no production impl** + an in-memory fake + a conformance test suite.

**Infra / data / security / observability**
- [ ] Terraform/Helm/Argo CD scaffolds apply; namespaces + **default-deny network policies mirroring ARCH-04** (AD-82) + Istio mTLS.
- [ ] Per-service Postgres schema + Alembic migration (schema/outbox/RLS scaffolding only) runs in CI and locally.
- [ ] OTel → Collector → Prometheus/Tempo/Loki/Grafana up; a request yields an end-to-end trace with correlation + business IDs; logs are PII-free (AD-122/123).
- [ ] Security scans (SAST/deps/secrets/image) block on criticals; mTLS + SVID between two shells; secrets via ESO/Vault(fake locally).

**AI dev foundation (scaffold)**
- [ ] Prompt + Model registries load; **mock AI provider** returns deterministic schema-valid proposals; Model Quality Harness runs against a **synthetic** golden dataset producing placeholder metrics. No reasoning/scoring/fairness logic.

**Governance**
- [ ] `/contracts` and `/specs` require ARB review (CODEOWNERS); the FTD table is recorded; **no new ADRs** were created (architecture frozen, AD-143).

> **Explicit non-goals confirmed absent:** no Candidate Evaluation, no evaluation/scoring, no AI reasoning, no fairness/integrity logic, no domain rules, no business tables, no real LLM calls. **Scaffolding only.**

---

## Transition to Sprint 1

With Sprint-0 met, Sprint 1 opens on solid ground and the recommended sequencing holds:
- **Validation runs in parallel and leads on risk** (design partners, zero-build experiments for AS-1) — it needs none of this code.
- **Evaluation Engine design** (judgment rubric for the Structured Work Sample) precedes coding the `evaluation` + `intelligence-compute` business logic.
- **Sprint 1** implements the first vertical slice *within the frozen architecture* — likely Consent + Candidate intake + Campaign create — each new aggregate/contract/term flowing through the governed path (ADR only if it evolves the baseline, AD-136).

*End of SPRINT-0 v0.1 — the Engineering Foundation. It stands up the entire machine (repo, dev env, CI/CD, 13 deployable shells, 9 platform interfaces, infra, data, observability, security, codegen, testing, AI-dev scaffolding, DX) with the frozen architecture wired through every layer — and zero business logic. When the exit criteria are green, feature development can begin on a foundation that will not shift beneath it.*
