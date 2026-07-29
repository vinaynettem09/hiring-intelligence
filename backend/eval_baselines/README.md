# Evaluation quality baselines (A–G)

Reference snapshots produced by `scripts/run_quality_eval.py` — the raw structured
outputs and a compact table for the seven **synthetic** fixtures (A strong … G concise),
keyed by `provider__model__promptversion`.

**Purpose:** compare a later prompt/model version against the *same* inputs, instead of
judging by whether a new output "feels better." When you change the prompt (VERSION bump)
or the model, re-run the harness and diff the new baseline file against the old one.

**Rules:**
- **Synthetic only.** These fixtures contain no real person's name, résumé, email, or
  answers. Never point the harness at real candidate material.
- These are **behavioral regression references, not validation.** They do not prove
  predictive validity, fairness, or hiring quality.
- Real-model baselines require `AI_PROVIDER=anthropic` + an API key and cost money; the
  mock baseline is free/offline and only exercises the pipeline shape.
