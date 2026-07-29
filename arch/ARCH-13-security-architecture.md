# ARCH-13 — Security Architecture

| Field | Value |
|---|---|
| **Document ID** | ARCH-13 |
| **Title** | Security Architecture (protecting every invariant against adversaries) |
| **Owner** | CISO + Principal Security Architect (Zero-Trust / Cloud / AppSec / AI-Security / IAM / Compliance) |
| **Status** | Draft v0.1 — for review |
| **Created** | 2026-07-22 |
| **Phase** | Phase 4 — Architecture (security) |
| **Depends on** | ARCH-01→12 (all). Especially ARCH-06 (zero-trust/tenant), ARCH-08 (keys/crypto-shred), ARCH-10 (mesh/egress), ARCH-11 (AI runtime), ARCH-12 (ops/break-glass), DOC-05 (Tier-0 gates) |
| **Blocks** | ARCH-14 (Observability — security telemetry), ARCH-15 (AI Governance), ARCH-16 (Platform Governance) |
| **The one question** | **"How is the platform secured so every architectural invariant stays true against malicious actors, operational mistakes, insider threats, and AI-specific attacks?"** |
| **Security philosophy** | **Security is not a layer; it is a cross-cutting property.** Every control traces to an architectural responsibility (ARCH-01→12) and **protects** it. Security may never redefine business rules, aggregates, contracts, gates, ownership, or AI responsibilities. |
| **Scope** | Security architecture. Security **telemetry/SIEM** pipeline → ARCH-14; **governance boards/policies** → ARCH-15/16; implementation procedures → deferred (§18). |

---

## 0. Security Philosophy

The platform's value is *trust* — fair, explainable, defensible hiring decisions. A single breach (tenant leak, PII exposure, a bypassed gate, a poisoned model) is not a "security bug"; it is an **existential trust failure** (RK-6/RK-9). Security therefore is not a bolt-on layer but a property woven through every prior document: tenant isolation (INV-10), consent (INV-11), immutable audit (P8/AD-32), human accountability (INV-1), PII minimization (ARCH-01/11), zero-trust networking (ARCH-06/10). ARCH-13 makes those explicit as a **defensive system** against adversaries.

> ### AD-107 — Security preserves architectural invariants; no security control may redefine business behavior.
> A control may *protect* an aggregate, contract, gate, or AI responsibility, but may never alter one. **If a security design appears to require changing the domain, the security design is wrong** — redesign the control, not the domain. (Direct analog of AD-77 for infrastructure: security realizes and defends the architecture, it does not re-author it.)

A second, quietly powerful consequence of the corpus:

> ### AD-118 — Compliance is largely *emergent* from the architecture, not bolted on.
> The immutable, complete audit trail (event log = audit, AD-32) is **SOC 2 / ISO 27001 evidence**; first-class Consent (INV-11) is the **GDPR/CCPA lawful-basis** mechanism; crypto-shredding (AD-64) **is** right-to-erasure; per-tenant keys (AD-84) are the **data-residency** substrate; the operational trail (AD-106) is **audit-of-operations**. Compliance work becomes largely *demonstrating* properties the architecture already guarantees, rather than retrofitting controls. This is a strategic moat property (DOC-03): trust and auditability are structural, not aspirational.

---

## 1. Threat Model *(STRIDE)*

A complete STRIDE pass, each threat mapped to the invariant it attacks and the control that defends it. Actors: **external attacker, malicious insider, compromised developer, compromised workload, LLM provider, supply-chain adversary.**

| STRIDE | Representative threats (from the brief) | Invariant attacked | Primary defense (traces to) |
|---|---|---|---|
| **Spoofing** | credential theft; forged service identity; impersonating a human decider | INV-1 (human accountability), INV-10 (tenant) | OIDC + MFA/passkeys (humans); **SPIFFE/SVID + mTLS** (workloads, ARCH-06/10); human-scope required for `RecordHiringDecision` (ARCH-09) |
| **Tampering** | altering evidence, decisions, audit; retrieval/context poisoning; data poisoning | INV-b/INV-e (immutability), P8 (audit), AD-90 (grounding) | append-only + WORM + hash-chain (ARCH-08); immutable facts; evidence grounding + hallucination reject (ARCH-11 AD-90) |
| **Repudiation** | "I didn't make that decision"; "we never had consent" | INV-1, INV-11, P8 | immutable audit with actor+time (AD-32); operational trail (AD-106); consent as recorded fact (ARCH-05) |
| **Information Disclosure** | tenant escape; PII exposure; model inversion; prompt/model exfiltration; secrets leakage | INV-10, INV-11, ARCH-01 LLM boundary | tenant isolation defense-in-depth (§7); PII minimization (§9, AD-89); per-tenant encryption (AD-84); egress control (AD-83); secrets mgmt (§12) |
| **Denial of Service** | flooding; AI-cost exhaustion (economic DoS); queue saturation | availability tiers (ARCH-06) | rate limiting (ARCH-07/10); AI budgets + back-pressure (ARCH-11 §13); autoscaling; fail-soft (ARCH-06 §9) |
| **Elevation of Privilege** | tenant escape; break-glass abuse; compromised workload pivot; tool abuse (AI) | INV-10, least privilege, AD-99 | RBAC/ABAC (§5); JIT + audited break-glass (§3, AD-99); mesh authz (§6); AI capability isolation (§9) |

**AI-specific threat class** (expanded in §9): prompt injection, **indirect** prompt injection (via candidate-supplied work-sample content), context/retrieval poisoning, model supply-chain compromise, provider compromise, PII leakage to provider, prompt leakage, tool abuse.

**Environmental/operational:** region failure (ARCH-12 §7 DR), misconfiguration (GitOps + policy-as-code §11), secrets leakage (§12), infrastructure compromise (defense-in-depth + least privilege).

> ### AD-116 — Prompt injection (direct and indirect) is treated as an expected, ever-present attack class, not an edge case.
> Because candidates supply the work-sample content the model reads, **indirect prompt injection is a first-class threat**: the model must be assumed to be attacked on every invocation. Defenses (§9) are designed accordingly, and — critically — even a *fully successful* injection cannot bypass a gate or produce a fact, because the AI proposes and the domain decides (AD-88): the blast radius of a compromised model is bounded by architecture.

---

## 2. Security Principles

| Principle | Meaning here | Traces to |
|---|---|---|
| **Zero Trust** | No implicit trust from network position; every call authenticated + authorized | ARCH-06 AD-45, §6 |
| **Least Privilege** | Every human/workload gets the minimum; JIT elevation | §3/§5 |
| **Defense in Depth** | Multiple independent layers; no single control is load-bearing alone | §7 tenant isolation |
| **Secure by Default** | Default-deny networks, deny-by-default authz, gates fail closed | ARCH-06/10 |
| **Fail Closed** | Under doubt, gates hold; security controls deny | ARCH-06 AD-24 |
| **Immutable Audit** | Security & business events are append-only, tamper-evident | AD-32/AD-112 |
| **Human Accountability** | The human decides; security never automates the accountable act away | INV-1 |
| **Tenant Isolation** | Cross-tenant is impossible by construction | INV-10 |
| **Privacy by Design** | PII minimized, consent-governed, crypto-shreddable | INV-11, AD-64/89 |
| **AI proposes; domain decides** | A compromised model cannot decide or produce a fact | AD-88 |

### 2.1 Trust Assumptions Register *(making implicit trust explicit)*

Every architecture trusts something; unstated trust is unmanaged risk. These are the platform's **roots of trust** — if any changes, the security architecture must be re-reviewed against it.

| Trust root | What we assume | If it changes / is compromised, reconsider… |
|---|---|---|
| **KMS** | Key generation, storage, and access control are sound | All encryption at rest, per-tenant isolation, **crypto-shred** (AD-64) — the erasure guarantee rests here |
| **Identity Provider (OIDC)** | Authenticates humans correctly; claims are trustworthy | All human authN/authZ (§3–5); MFA/passkey assurance |
| **SPIFFE/SPIRE CA** | Issues/validates workload identities honestly | All internal mTLS + service authZ (§4/§6); zero-trust east-west |
| **Kubernetes control plane** | Orchestrates and isolates workloads as declared | Namespace/network segmentation, admission control, pod isolation (ARCH-10) |
| **Managed data services** (Aurora/MSK/S3/…) | Durability, isolation, and encryption behave as contracted | Persistence integrity, backup/DR (ARCH-08/12), residency |
| **Time synchronization** | Clocks are accurate + monotonic enough for ordering/expiry | Token expiry, event `occurred-at`, replay-protection, cert validity |
| **Cryptographic primitives** | Standard algorithms remain unbroken | All encryption, signing, hashing, WORM hash-chain, mTLS |
| **Audit substrate (WORM)** | Append-only, tamper-evident storage cannot be silently altered | The entire non-repudiation + compliance posture (AD-112/AD-118) |

> ### AD-119 — Trust assumptions are explicit architectural artifacts, maintained in a Trust Assumptions Register.
> The platform's roots of trust (KMS, IdP, SPIFFE CA, K8s control plane, managed data services, time sync, crypto primitives, WORM audit) are documented, not implicit. Any change to a trust root triggers a targeted security re-review of exactly the guarantees that depend on it. *Rationale:* implicit trust is the most common source of "we didn't know that could break us"; making it explicit turns a hidden dependency into a governed one (register maintained under ARCH-16). *(Governance of the register → ARCH-16.)*

---

## 3. Identity & Access Management

| Concern | Decision |
|---|---|
| **Human identities** | Federated via external OIDC IdP (Okta/Auth0/Entra); the platform never stores passwords. |
| **Service identities** | **SPIFFE/SPIRE** workload identities (SVIDs); every service has a cryptographic identity (AD-110). |
| **RBAC** | Coarse roles map to DOC-08 personas (Recruiter, Hiring Manager, Admin, Candidate) and their legal interactions (ARCH-04 §2). |
| **ABAC** | Fine-grained attributes (tenant, campaign, ownership) layered over RBAC for object-level decisions (§5). |
| **Just-in-Time access** | Standing privilege minimized; elevation is time-boxed, reason-bound, approved, and audited (AD-106). |
| **Break-glass** | Emergency access requires a second approver, is time-boxed, fully audited, and — per AD-99 — grants operational access **only**, never the ability to bypass a gate, mutate audit, or cross tenants. |
| **Service accounts** | No shared static service accounts; workload identity replaces them. |
| **Session management** | Short-lived tokens; refresh with rotation; revocation on anomaly. |
| **Credential lifecycle** | Issued short-lived, rotated automatically, revocable centrally (§12). |
| **Approval workflows** | Sensitive grants and break-glass route through approval with audit. |

> ### AD-108 — Identity is the security perimeter (not the network). Every access decision is made from verified identity + attributes, regardless of network location.

> ### AD-110 — Every workload has a cryptographic identity (SPIFFE/SVID); there are no anonymous services and no shared service credentials.

---

## 4. Authentication

| Concern | Decision |
|---|---|
| **User authentication** | OIDC via enterprise IdP; **MFA mandatory**; **passkeys/WebAuthn** preferred (phishing-resistant). |
| **Candidate authentication** | Scoped, minimal-friction, tenant-bound auth for candidates (submit work sample, view own feedback) — least privilege by design (candidates see only their own, P13). |
| **Service authentication** | **mTLS everywhere internally**; SVID-based; no plaintext internal traffic (ARCH-06/10). |
| **Token validation** | Every service validates tokens locally (signature, audience, expiry, tenant claim); **tenant is derived from the token, never the wire** (ARCH-09 AD-71). |
| **Refresh strategy** | Short-lived access tokens + rotating refresh; revocation propagated. |
| **Machine identities** | SPIFFE/SPIRE-issued, short-lived, auto-rotated SVIDs. |

> ### AD-109 — Every request — human or service, north-south or east-west — is authenticated and authorized before any business logic runs. No implicit trust, ever.

---

## 5. Authorization

| Concern | Decision |
|---|---|
| **Role hierarchy** | Personas → roles (ARCH-04 actors); roles grant *legal interactions only* (a role can never grant a forbidden interaction, ARCH-04 §2). |
| **Permission model** | RBAC (role → allowed operations) + ABAC (attributes: tenant, campaign, object ownership). |
| **Resource ownership** | Every object is tenant-scoped and owned by an aggregate (ARCH-03); authorization checks tenant + ownership below the query layer (ARCH-08). |
| **Tenant boundaries** | Every authorization decision is tenant-scoped; cross-tenant is structurally impossible (§7). |
| **Object ownership** | A recruiter accesses their tenant's campaigns; a candidate accesses only their own evaluation's feedback (P13) — enforced, not assumed. |
| **Fine-grained authorization** | A **policy engine** (e.g., OPA/Cedar-style) evaluates ABAC policies centrally-defined, locally-enforced; policies are versioned artifacts (governance → ARCH-16). |
| **Interaction-matrix enforcement** | The authorization layer is a *third* enforcement of ARCH-04's legal-interaction matrix (after: no contract, no surface, no network route — AD-76/AD-82). Defense in depth on the prohibitions. |

---

## 6. Zero Trust Architecture

| Concern | Decision |
|---|---|
| **Identity-based networking** | Access is identity-driven (SVID), not IP/network-driven (AD-108). |
| **Mesh authorization** | Istio ambient enforces service-to-service authz policies (who may call whom) mirroring ARCH-04 §2 — a service can only call services it is legally permitted to (AD-82). |
| **mTLS** | All internal traffic mutually authenticated + encrypted (ARCH-06 AD-45). |
| **Default deny** | Network policies default-deny; only explicitly-allowed flows exist (AD-82). |
| **Segmentation** | Namespace + network-policy segmentation; gates in isolated failure/trust domains (ARCH-10 §3). |
| **East-West protection** | mTLS + mesh authz + network policy on internal traffic. |
| **North-South protection** | WAF + gateway (OIDC, rate limit) + TLS at the edge; only the external OpenAPI surface is exposed (ARCH-09/10). |

---

## 7. Tenant Isolation *(defense-in-depth — the most-defended invariant)*

INV-10 is defended at **every** layer independently, so no single failure crosses tenants.

| Layer | Isolation control |
|---|---|
| **Application** | Tenant claim mandatory (server-resolved, AD-71); every handler tenant-scopes; interaction-matrix authz (§5). |
| **Database** | Row-level security + tenant partition keys; queries tenant-filtered below the app layer (ARCH-08 §9). |
| **Storage** | Per-tenant prefixes + per-tenant encryption keys (AD-84); short-lived scoped references (AD-66). |
| **Cache** | Tenant-namespaced keys; no cross-tenant key collision. |
| **Search** | Per-tenant indices or hard tenant filters below the query layer (ARCH-08 §8). |
| **Message bus** | Tenant in the ordering key + envelope; consumers tenant-scope; no cross-tenant subscription. |
| **AI Runtime** | Per-invocation tenant scoping; content-hash cache tenant-namespaced; **capability isolation** (§9). |
| **Logs / Metrics** | Tenant-tagged; access tenant-scoped; PII-minimized (ARCH-06 §9). |
| **Backups** | Tenant-scoped restore; per-tenant keys mean a backup is useless without the tenant's key. |
| **Key hierarchy** | **Per-tenant CMKs (AD-84)** are the cryptographic root of isolation: even a misrouted read is unreadable without the tenant's key. |

> ### AD-115 — Tenant isolation is defense-in-depth: enforced independently at application, data, storage, cache, search, bus, AI, logs, and key layers. No single control is the isolation boundary; the per-tenant key is the last-resort cryptographic guarantee.

---

## 8. Data Protection

| Concern | Decision |
|---|---|
| **Classification** | Every field classified (NON_PII / PII / SENSITIVE_PII — ARCH-09 envelope); classification drives handling (logging, minimization, retention). |
| **Encryption in transit** | TLS at edge; **mTLS internally** (ARCH-06/10). |
| **Encryption at rest** | Envelope encryption via KMS on all stores (ARCH-08 §9). |
| **Encryption in memory** | Sensitive material minimized in memory, zeroized after use; no PII in dumps/logs; confidential-compute considered for the most sensitive paths (deferred). |
| **Key hierarchy** | KMS root → per-tenant CMKs → per-subject keys (crypto-shred granularity). |
| **Per-tenant keys** | AD-84 — isolation + residency substrate. |
| **Crypto-shredding** | AD-64/AD-102 — right-to-erasure by key destruction, verified across authoritative + derived stores. |
| **Data masking** | PII masked in non-prod and in logs/traces; test data synthetic or masked. |
| **Secrets handling** | §12. |

> ### AD-117 — Privacy is a security control: PII minimization, per-subject keys, and crypto-shredding are enforced as security mechanisms, not just compliance features.

---

## 9. AI Security

The highest-novelty attack surface (ARCH-01 top risk). The architectural safety net: **AI proposes; domain decides (AD-88)** — so even total model compromise cannot decide, pass a gate, or emit a fact. Controls harden the model path *and* rely on that bounded blast radius.

| Threat | Defense (traces to) |
|---|---|
| **Prompt injection (direct)** | Input treated as hostile; strict prompt/role separation; structured-output validation (AD-90); model output is only a *proposal*. |
| **Indirect prompt injection** (via candidate-supplied work sample) | Candidate content is **untrusted data, never instructions**; content/instruction separation; PII-minimized (AD-89); output grounded + validated; **AD-116 assumes this attack always**. |
| **Context / retrieval poisoning** | Retrieval sources are tenant-scoped, integrity-checked; embeddings derived from immutable, integrity-verified facts (ARCH-11 §9/§10); poisoned context cannot mutate a fact (immutability). |
| **Model supply chain** | Providers vetted; model/prompt versions pinned + provenance (AD-95); changes gated by Model Quality Harness (AD-97). |
| **Provider trust** | **Providers are untrusted execution environments (AD-113)**: PII-minimized before egress (AD-89), controlled egress (AD-83), output validated on return, no secrets/PII in prompts. |
| **Output validation** | Schema + grounding validation (AD-90); hallucinated citations hard-rejected. |
| **Tool-calling safety** | The AI has **no authoritative tools** — no capability decides, passes a gate, writes a fact, or mutates state (capability isolation); tools, if any, are read-only/proposal-only. |
| **Hallucination safety** | Grounding + confidence calibration (AD-90/91); low confidence escalates (AD-88). |
| **PII leakage** | Minimization (AD-89); no PII in logs; per-tenant keys; egress control. |
| **Model exfiltration / prompt leakage** | Prompts are governed artifacts, access-controlled; no secrets in prompts; output filtered for prompt/secret leakage. |
| **Training-data protection** | We do not train provider models on tenant data (contractual + technical); golden datasets are governed, consented, PII-minimized (ARCH-11 §15 → ARCH-15). |
| **Inference isolation** | Intelligence Compute is a separate trust/failure domain (ARCH-06); per-invocation tenant scoping. |
| **Capability isolation** | Each AI capability is narrow, stateless, proposal-only; none can escalate to a decision or a fact (AD-47/56/88). |

> ### AD-113 — External AI providers are untrusted execution environments. Nothing sensitive crosses to them un-minimized; everything returned is validated; and no provider output is ever authoritative.

---

## 10. Application Security

| Concern | Decision |
|---|---|
| **OWASP Top 10** | Systematically addressed; AppSec is part of the SDLC and CI (SAST/DAST). |
| **Input validation** | All input validated against contract schemas (ARCH-09); reject-by-default. |
| **Output encoding** | Context-aware encoding; candidate-facing content sanitized (XSS). |
| **SQL injection** | Parameterized access only; no dynamic SQL from input (implementation standard). |
| **SSRF** | Egress default-deny (ARCH-10); no user-controlled outbound URLs; the only sanctioned external egress is the controlled LLM/provider path (AD-83). |
| **CSRF** | Anti-CSRF on state-changing edge operations; SameSite; token-based APIs. |
| **XSS** | Output encoding + CSP + sanitization of any rendered candidate/user content. |
| **Command injection** | No shell interpolation of input; safe APIs only. |
| **Rate limiting** | Per-tenant/per-caller at the gateway (ARCH-07/10), plus AI-cost back-pressure (economic-DoS defense). |
| **File upload security** | Content-addressed, **virus/malware scanned at ingest** before processing (ARCH-08 AD-66); type/size validation; scanned files only reach evidence/LLM. |
| **Secure headers** | HSTS, CSP, X-Content-Type-Options, etc., at the edge. |

---

## 11. Supply Chain Security

| Concern | Decision |
|---|---|
| **SBOM** | Generated for every image; tracked and scanned continuously. |
| **Dependency scanning** | Continuous vulnerability scanning; policy on criticality + remediation SLAs. |
| **Container signing** | Images signed (e.g., Sigstore/cosign); only signed images admitted. |
| **Image scanning** | Vulnerability + secret scanning in CI and registry (ARCH-10 ECR). |
| **SLSA** | Build provenance to a SLSA level; tamper-evident build pipeline. |
| **Artifact provenance** | Every deployed artifact traces to a signed, provenanced build (parallels AD-95 for AI). |
| **Admission controllers** | Kubernetes admission policy (e.g., OPA Gatekeeper/Kyverno) enforces signed images, no privileged pods, required labels, network-policy presence. |
| **Policy enforcement** | Policy-as-code in CI + admission; misconfiguration blocked before deploy (defense against the "misconfiguration" threat). |

> ### AD-114 — Every external dependency and deployed artifact is verified (signed, scanned, provenanced) before it runs. Unverified artifacts are not admitted.

---

## 12. Secrets Management

| Concern | Decision |
|---|---|
| **Vault** | Central secrets manager (Vault / cloud Secrets Manager) + External Secrets Operator (ARCH-10). |
| **Rotation** | Automatic, scheduled rotation; short-lived by default. |
| **Dynamic secrets** | Prefer dynamically-issued, short-lived credentials (DB, provider) over static. |
| **Certificates** | cert-manager + mesh CA (SPIRE) issue/rotate mTLS certs automatically. |
| **KMS** | Envelope encryption + per-tenant CMKs (AD-84); key policies least-privilege. |
| **Envelope encryption** | Data keys wrapped by KMS; per-subject keys enable crypto-shred (AD-64). |
| **Recovery** | Key backup/escrow with strict controls; loss of a tenant key = crypto-shred (by design), so escrow policy is deliberate. |
| **Revocation** | Central, immediate revocation on compromise; propagated to mesh/services. |

> ### AD-111 — Every secret is centrally managed, short-lived, rotated, and revocable; no static secrets in images, code, config, or prompts.

---

## 13. Compliance Architecture

Built on AD-118 (compliance is largely emergent). This section maps regimes to the **existing** architectural mechanisms that satisfy them.

| Regime / requirement | Satisfied by (existing architecture) |
|---|---|
| **SOC 2 / ISO 27001** | Immutable audit trail (AD-32) + operational trail (AD-106) = control evidence; access controls (§3–6); change management (ARCH-12 §4); DR (ARCH-12 §7). |
| **GDPR / CCPA** | Consent as first-class lawful basis (INV-11); PII minimization (AD-89); **right-to-erasure = crypto-shred** (AD-64); data classification (§8). |
| **Audit evidence** | The event log *is* the audit trail (AD-32); every material action + operational action attributable (AD-106). |
| **Data residency** | Per-tenant keys + partitioning substrate (AD-84/86); regional routing on roadmap. |
| **Consent** | ConsentGranted/Withdrawn facts (ARCH-05); consent gate (CAR-2). |
| **Retention** | Policy-driven retention + legal hold (ARCH-08/12 §8). |
| **Legal hold** | Suspends deletion/expiration; auditable (ARCH-12 §8). |
| **Right to erasure** | Crypto-shred, verified across derived stores (AD-102). |
| **Fairness / adverse-impact (EEOC-adjacent)** | Fairness gate (INV-3) + fairness signals + Model Quality Harness fairness thresholds (AD-97) — auditable non-discrimination evidence. |

> The strategic point: because trust and auditability are **structural**, passing an enterprise security review or a compliance audit is largely a matter of *demonstrating* guarantees the architecture already enforces — a direct contributor to the enterprise-sales motion (DOC-03) and the moat.

---

## 14. Security Operations *(architecture; SIEM pipeline → ARCH-14)*

| Concern | Decision |
|---|---|
| **SOC / monitoring** | Security monitoring over the immutable audit + operational trails + telemetry (pipeline in ARCH-14). |
| **Incident classification** | Aligns with ARCH-12 severities; **any tenant/PII/audit/gate-bypass event is SEV-1**. |
| **Security runbooks** | Per threat class (tenant-escape suspicion, PII exposure, credential compromise, prompt-injection incident, provider compromise, supply-chain alert); mitigation is always **gate-preserving** (AD-99). |
| **Threat hunting** | Proactive hunting over audit/telemetry for anomalies (cross-tenant access attempts, unusual egress, injection patterns). |
| **Vulnerability & patch management** | Continuous scanning (§11); remediation SLAs by severity; patching via GitOps (ARCH-12). |
| **Pen testing / Red / Blue / Purple** | Regular external pen tests; red-team (incl. **AI red-teaming**: injection, exfiltration, jailbreaks); blue-team detection; purple-team collaboration. |
| **Security game days** | Scheduled exercises: tenant-escape attempt, secret-leak, provider compromise, prompt-injection campaign — validating that invariants hold (parallels ARCH-12 DR game-days). |

> ### AD-112 — Every security event is immutable and attributable. Security and operational events share the append-only, tamper-evident substrate as business facts (AD-32/AD-106), so an attacker cannot erase their tracks.

---

## 15. Architecture Decisions *(continuing the log; ARCH-12 ended at AD-106)*

| ID | Decision | Rationale |
|---|---|---|
| **AD-107** | Security preserves architecture; no control redefines business behavior | Security defends invariants; if it needs a domain change, the control is wrong |
| **AD-108** | Identity is the security perimeter (not network) | Zero trust; access from verified identity+attributes regardless of location |
| **AD-109** | Every request authenticated + authorized before business logic | No ambient/implicit trust anywhere |
| **AD-110** | Every workload has a cryptographic identity (SPIFFE/SVID); no shared creds | Spoofing/lateral-movement defense |
| **AD-111** | Every secret centrally managed, short-lived, rotated, revocable; none static | Secrets-leakage defense |
| **AD-112** | Every security & operational event is immutable + attributable | Attacker cannot erase tracks; audit integrity |
| **AD-113** | AI providers are untrusted execution environments | PII-min before egress, validate on return, never authoritative |
| **AD-114** | Every external dependency/artifact verified (signed/scanned/provenanced) before running | Supply-chain defense |
| **AD-115** | Tenant isolation is defense-in-depth across all layers; per-tenant key is last-resort guarantee | No single isolation boundary; existential-risk mitigation |
| **AD-116** | Prompt injection (direct + indirect) is an expected, ever-present attack class | Candidate content is hostile input; blast radius bounded by AD-88 |
| **AD-117** | Privacy (minimization, per-subject keys, crypto-shred) is enforced as a security control | Privacy-by-design, not just compliance |
| **AD-118** | Compliance is largely emergent from the architecture, not bolted on | Audit/consent/crypto-shred/keys already satisfy SOC2/GDPR/CCPA; strategic moat |
| **AD-119** | Trust assumptions are explicit architectural artifacts (Trust Assumptions Register) | Unstated trust is unmanaged risk; a changed root of trust triggers targeted re-review |

## 16. Open Questions

1. **Confidential computing** for the most sensitive in-memory paths (PII pre-minimization, key operations) — worth the complexity at what scale?
2. **Candidate authentication friction vs. security** — passkeys vs. magic-link vs. IdP for candidates who are not enterprise users; UX (DOC-06) vs. assurance.
3. **Provider data-processing assurances** — contractual + technical proof that tenant data is not retained/trained on; which providers meet the bar (ties ARCH-11 OQ, ARCH-15).
4. **Policy engine choice** (OPA vs Cedar vs other) and central-authoring/local-enforcement topology.
5. **Bring-your-own-key (BYOK)/HYOK** for enterprise tenants demanding key control — how it interacts with per-tenant CMK + crypto-shred.
6. **AI red-team cadence and scope** — how continuously we adversarially test the model path.

## 17. Risks

- **Technical:** a novel tenant-escape via a shared component. *Mitigation:* AD-115 defense-in-depth + per-tenant keys.
- **Operational:** break-glass abuse / misconfiguration. *Mitigation:* AD-99 gate-preserving break-glass + audit (AD-106) + policy-as-code admission (§11).
- **Compliance:** a regime we haven't mapped. *Mitigation:* AD-118 emergent posture + governance (ARCH-15/16) tracks new regimes.
- **AI:** a successful prompt injection. *Mitigation:* AD-116 expected-attack posture; **blast radius bounded by AD-88** (cannot decide/emit a fact/pass a gate).
- **Supply chain:** a poisoned dependency/image. *Mitigation:* AD-114 signing/scanning/provenance + admission control.
- **Cloud:** provider/region compromise. *Mitigation:* least-privilege IAM, encryption with our keys, DR (ARCH-12), cloud-agnostic core (AD-78).
- **Human:** phishing, insider threat. *Mitigation:* passkeys/MFA, least privilege, JIT, immutable audit, anomaly hunting.

## 18. Deferred *(implementation procedures / other docs)*

- **To ARCH-14 (Observability):** SIEM pipeline, security dashboards, detection rules, anomaly alerting, audit-correlation at scale.
- **To ARCH-15 (AI Governance):** provider approval/retirement, golden-dataset governance, fairness review board, model-risk governance.
- **To ARCH-16 (Platform Governance):** authorization-policy lifecycle, security-control change management, exception governance, ADR review.
- **Implementation procedures:** concrete IAM role definitions, WAF rules, scanner configs, incident-response playbooks, pen-test scheduling — engineering/security-ops runbooks (consume this architecture).

---

*End of ARCH-13 v0.1 — the Security Architecture. Security is a cross-cutting property that defends every invariant (AD-107): identity is the perimeter, every request is authenticated and authorized, tenants are isolated in depth down to per-tenant keys, AI providers are untrusted and the model's blast radius is bounded by "AI proposes; domain decides," the supply chain is verified, and — because audit, consent, crypto-shred, and keys are structural — compliance is largely emergent (AD-118). Next: ARCH-14 — Observability Architecture (telemetry, SLIs/SLOs, business-metric and security observability, audit correlation).*
