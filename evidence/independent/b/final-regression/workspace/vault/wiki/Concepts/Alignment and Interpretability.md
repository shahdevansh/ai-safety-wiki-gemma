---
source: vault/raw/alignment-fundamentals-notes.md
source_sha256: d9097717f4c977fadeef5b03d44566ab7b5e04dc1f2784bd1e5079872bbef9b8
review_status: pending
---

# Alignment and Interpretability

Defining alignment remains unsolved, with challenges including aligning to individual risks, the skew of outputs from aligning to "general human values," and a lack of consensus on what those values are. Reward modeling is a fundamental bottleneck because standard methods like SGD assume a single optimum, failing to capture cultural and individual diversity. While pluralistic alignment is explored, it is not yet effective. Existing process reward models are limited to mathematical representations and are trained on traces that reach a "correct" answer, rather than capturing the actual process. Agents also struggle with misreading intent and failing to request clarification, unlike human collaborators. Interpretability is considered the other half of alignment, as understanding internals is necessary to align models. Active research directions include detecting deception in reasoning models by tracking discrepancies between thinking traces and explicit model outputs, targeting hidden states that lead to deceptive outputs.

## Source

[[raw/alignment-fundamentals-notes|Original: alignment-fundamentals-notes.md]]

## Related notes

- [[Assistance Games]] — Uncertain human interests provide another framing of alignment.
- [[Transformer Safety Limits]] — Connects internal understanding to claims about model limitations.
