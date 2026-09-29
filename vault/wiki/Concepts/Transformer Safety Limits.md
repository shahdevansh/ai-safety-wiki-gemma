---
source: vault/raw/alignment-lecture-notes.md
source_sha256: 76c88bc45bce852e63112fffc2cd94ffd377aa0e4a8b1fe7d7c3713a8afa5d02
review_status: reviewed
---

# Transformer Safety Limits

The lecture notes question whether architectural limitations provide durable AI safety guarantees. They contrast fixed-depth transformers with systems that perform additional computation through recurrence, chain-of-thought or a surrounding algorithm. The theoretical claims below are reported as lecture claims; their assumptions and proofs are not supplied by this source.

## Useful details

- The notes claim fixed-depth transformers have limits on problems such as graph connectivity, regardless of scale. This page does not generalize that claim beyond its unstated assumptions.
- They describe recurrence and a transformer-plus-context-plus-wrapper system in Turing-machine terms. This is the source's characterization, not a proof of unrestricted capability in a finite deployed system.
- The Reversal Curse appears as an example of regularities the notes say models fail to learn; sample complexity is offered as an explanation.
- A chess analogy illustrates the concern that pattern matching can bypass an apparent limitation. The notes therefore reject relying on such limitations as a strong safety guarantee.

## Source

[[raw/alignment-lecture-notes|Original: alignment-lecture-notes.md]]

## Related notes

- [[Alignment and Interpretability]] — Internal behavior and deceptive outputs require evaluation beyond architecture labels.
- [[Compute Governance]] — Hardware governance is discussed as an alternative to fragile behavioral guarantees.
