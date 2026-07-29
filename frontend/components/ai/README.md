# AI Components — Design Contract

> **Status: IMPLEMENTED (Story 5.4B).** The recruiter intelligence experience is built
> against this contract. Shipped here as `.tsx`: `ai-recommendation-card`,
> `confidence-meter`, `reasoning-summary` + `grounded-observation`,
> `competency-reasoning-card`, `evidence-citation` + `evidence-sheet` + `evidence-context`
> (the citation → source drawer), `escalate-panel`, `evaluation-history`,
> `evaluation-technical-details`, `evaluation-generating-state`, `mock-evaluation-notice`,
> and the shared `presentation.ts` (enum → humane copy + tone/confidence mapping). The
> workspace lives at `app/campaigns/[id]/candidates/[evaluationId]/page.tsx`.
>
> Semantics honored: recommendation is a PROPOSAL (never a decision — no Hire/Reject);
> confidence is rendered as a semantic **level** ("High/Moderate/Low evidence confidence"),
> never as a percentage (1.0 ≠ "100%"); every claim is grounded to inspectable source
> evidence; ESCALATE reads as uncertainty, not failure; mock output is unmistakably marked.
> The original design language below is retained for reference.

## Why a separate language
Anything the AI produces must **look unmistakably different** from ordinary form
fields and user-entered data. A recruiter should glance at a screen and know "this was
proposed by AI" — without it feeling gimmicky. This reinforces the product's core law:
**AI proposes, a human decides.** AI surfaces are *advisory*, evidence-cited, and never
rendered as a bare number.

## Shared visual traits (all AI components)
- A subtle, consistent **AI treatment**: a faint indigo (primary) tint / left accent or
  a small `Sparkles` marker — distinct from neutral cards. Never loud.
- **Never a bare score.** A score always appears with its **confidence** and a path to
  its **evidence**. (Backend guarantees this — payloads always include evidence links.)
- Honest states: `pending` (AI still working — progressive reveal, not a spinner-blank),
  `low-confidence` (visually de-emphasized + "needs human review"), `failed` (soft — ask
  for a human, never fabricate).
- Fully accessible: meaning never conveyed by color alone (icon + label + text).

## Components

### `AIRecommendationCard`
The headline AI output for one candidate evaluation. Shows the proposal (e.g. Strong /
Mixed / Weak match), the score **with** its `ConfidenceMeter`, and a summary line — plus
a clear affordance into the evidence. Visually marked as AI. Never the final word: pairs
with a human decision action.
- *Contract (conceptual):* `{ recommendation, score, confidence, summary, evidenceRef, status }`

### `ConfidenceMeter`
Communicates how much to trust a proposal (high / medium / low). Calm, non-alarming;
low confidence reads as "a human should look," not "error."
- *Contract:* `{ level: "high" | "medium" | "low", value?: number }`

### `EvidenceTimeline`
The cited evidence behind a recommendation — the trust anchor. An ordered, scannable
list of evidence items (each linking to the underlying work-sample moment). This is what
makes the evaluation defensible.
- *Contract:* `{ items: Array<{ competency, verdict, excerptRef }> }`

### `ReasoningCard`
The AI's step-by-step reasoning, progressively revealed. Clearly labeled as the model's
reasoning (advisory), not fact.
- *Contract:* `{ steps: Array<{ label, detail }>, status }`

### `RiskBadge`
Flags a specific concern to a human (e.g. low confidence, missing competency, integrity
signal). Small, informative, never punitive toward the candidate.
- *Contract:* `{ kind, severity: "info" | "attention" | "high", label }`

### `DecisionSummary` — IMPLEMENTED as `decision-panel.tsx` (Story 6.2)
Bridges AI proposal → human decision. The recruiter records ADVANCE / HOLD / DECLINE with
an optional rationale; the panel shows the current decision (who · when · informed-by-run)
and the append-only history. Deliberately **not** marked as AI — this is the person's act,
recorded independently; the AI recommendation above it is input, never the mechanism.
- *Backend:* `POST/GET /evaluations/{id}/decisions`; decisions are append-only and
  reference (never mutate) the immutable Evaluation.

## Not here yet
Charts/analytics for AI throughput belong under `components/charts/` and should prefer
plain counts (evaluated / waiting / blocked / calibration-needed) over decorative
visualizations. Add when Epic 4–5 give them a real consumer.
