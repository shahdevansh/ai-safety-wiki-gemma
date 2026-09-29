---
source: vault/raw/alignment-fundamentals-notes.md
source_sha256: d9097717f4c977fadeef5b03d44566ab7b5e04dc1f2784bd1e5079872bbef9b8
review_status: reviewed
---

# Alignment and Interpretability

The fundamentals-session notes connect alignment with understanding model internals. They record unresolved disagreement about whose values should guide a model and describe interpretability as complementary to choosing an alignment objective. These are compressed discussion notes, not a comprehensive account of current research.

## Useful details

- The session contrasts individual alignment with alignment to “general human values,” recording concern about Western/English-skewed outputs and a lack of consensus on values.
- The notes describe reward modeling and pluralistic alignment as open challenges; their compressed characterization of numerical optimization should not be treated as a general mathematical theorem.
- Process reward models are described in the session as limited to math and trained on traces reaching a correct answer. “Limited to math” does not mean “mathematical representations.”
- The interpretability rationale is explicit: it is hard to align models without understanding their internals; the notes pair knowing a direction with knowing how to get there.
- A research direction compares thinking traces with explicit model outputs and studies hidden states associated with deceptive outputs. The notes do not establish a reliable deception detector.

## Source

[[raw/alignment-fundamentals-notes|Original: alignment-fundamentals-notes.md]]

## Related notes

- [[Assistance Games]] — Uncertain human interests provide another framing of alignment.
- [[Transformer Safety Limits]] — Connects internal understanding to claims about model limitations.
