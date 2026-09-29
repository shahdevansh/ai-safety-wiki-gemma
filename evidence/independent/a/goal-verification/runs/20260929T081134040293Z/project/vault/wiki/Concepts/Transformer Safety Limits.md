---
source: vault/raw/alignment-lecture-notes.md
source_sha256: 76c88bc45bce852e63112fffc2cd94ffd377aa0e4a8b1fe7d7c3713a8afa5d02
review_status: pending
---

# Transformer Safety Limits

Fixed-depth transformers have limitations in solving certain problems, such as graph connectivity, irrespective of scale. Chain-of-thought and recurrent models are considered effectively Turing machines due to unbounded computation per token. Combining transformers with a context window and a wrapping algorithm results in a system functionally equivalent to a Turing machine. A current limitation is that transformers still fail to learn certain regularities, like the Reversal Curse, due to sample complexity. Transformers do not provide a strong safety guarantee, as illustrated by the MCO chess analogy, where a system can win without understanding by bypassing limitations through pattern matching. Recurrent models possess the potential to significantly change this situation with a research breakthrough.

## Useful details
* Fixed-depth transformers cannot solve certain problems (e.g., graph connectivity) regardless of scale.
* Chain-of-thought and recurrent models are effectively Turing machines with unbounded computation per token.
* Transformers plus context window plus wrapping algorithm are functionally a Turing machine.
* Transformers fail to learn certain regularities (e.g., the Reversal Curse) due to sample complexity.
* Recurrent models could flip the situation "almost overnight" with a research breakthrough.

## Source

[[raw/alignment-lecture-notes|Original: alignment-lecture-notes.md]]

## Related notes

- [[Alignment and Interpretability]] — Internal behavior and deceptive outputs require evaluation beyond architecture labels.
- [[Compute Governance]] — Hardware governance is discussed as an alternative to fragile behavioral guarantees.
