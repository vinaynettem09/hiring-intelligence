# Implementation Decisions (DEC log)

Tiny records of **implementation** choices worth remembering. **Not** ADRs and
**not** architecture — the architecture corpus (`arch/`) is frozen. These capture
build-time tradeoffs that don't rise to architectural significance but future-you
will want the reasoning for.

## Format
One file per decision: `DEC-<nnn>-<slug>.md`. Keep it to ~one page:

```
# DEC-<nnn> — <title>
Date · Status (accepted/superseded)
Decision: what we chose (one sentence)
Context: why the choice came up
Reason: why this option
Tradeoffs: what we give up
Revisit when: the trigger to reconsider
```

If a decision turns out to be architectural, escalate it through the frozen
corpus's governance (an ADR against the ARCH-16 baseline), not here.
