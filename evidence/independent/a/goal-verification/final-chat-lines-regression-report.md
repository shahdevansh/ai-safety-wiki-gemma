# Independent bounded chat regression — original-line selection

**Required ordinary chat, draft shortening, the checked original ask, chat-to-ask isolation, and reset pass. The lecture answer now covers both sides of the comparison with supporting original-line citations. The extra source-based shortening still fails: it repeats the same 61-word answer.**

Confidence: **high** for these observed results. This is a bounded regression on a new code version, not a new full-suite result. Earlier failures and the separate C40 report remain preserved.

The run is `20260929T084125814134Z`, using core SHA-256 `a00342076c80b8142fd456c842fcc25f11e940a2f2d7e70cfee449cb8a35b444` and grounded-chat prompt `d45dc84da09787da9c8af2d4304cafde7698bea8234fcd713c6acc67b81e9ebe`. The research prompt and final original corpus are unchanged. The [same prospective cases](chat-regression-cases.json) and unchanged runner were used; [freeze record](chat-lines-regression-freeze.json) records their hashes. The execution copy was freshly indexed; ingestion and the broader question suite were not repeated.

| Check | Independent semantic verdict | Actual result |
|---|---|---|
| Both required capability prompts | Pass | Accurate local capabilities and all eight commands; no retrieval. These responses are supplied by the harness. |
| Invitation draft | Pass | 70 words, labeled as a suggestion, coherent 30-minute agenda, no invented time/place/organizer. |
| Ordinary “make that shorter” | Pass | 70 → 51 words; preserves the invitation and agenda using recent history. |
| Chat-only fictional appointment | Pass | Repeated as a suggestion without source writes. |
| Independent appointment ask | Pass | Gemma returned insufficient evidence with no claims; the request contained no chat-only detail. |
| Original A1 assistance-game ask | Pass | Promoting human interests, uncertainty about those interests, and the need to infer them are all supported by the cited original line. |
| Lecture source question | Pass | Retrieves originals, explains software copying versus fabrication-facility barriers, and supports all three claims. |
| Extra source-based shortening | **Fail: usability** | Same displayed answer, 61 → 61 words. Citation validation passes, but the requested edit is not performed. |
| Reset | Pass | Actual request has only the system and current user message, zero history, and no carried passages. It does not recall the cleared discussion. |

Evidence: [original chat transcript](runs/20260929T084125814134Z/commands/chat-script.json), [isolation ask](runs/20260929T084125814134Z/records/ask-chat-isolation.md), [A1](runs/20260929T084125814134Z/records/ask-1-assistance-objective.md), [lecture answer](runs/20260929T084125814134Z/records/source-followup-reset/chat-01.md), [source shortening](runs/20260929T084125814134Z/records/source-followup-reset/chat-02.md), and [reset](runs/20260929T084125814134Z/records/source-followup-reset/chat-04.md).

## Citation meaning and provenance

Independent agent review confirms the factual support of the lecture response. The model selected `L009`, `L010`, and `L011`; the retained catalog maps them to passage `P4f87872fbb73`, original lecture lines 49, 50, and 51 respectively. The first line explicitly describes compute governance as more tractable. The second says software can be copied and transmitted freely and is largely uncontrolled; “easier to bypass” is a reasonable comparative inference from that line in context. The third states that bypassing embedded chip safety checks would require building a fabrication facility from scratch. These lines support the response's comparison. It makes no unsupported comparison of malware cost with hardware-security cost.

The harness resolves the model's selected line IDs to exact original text; the model does not supply or rewrite the quote. The retained raw response, complete line catalog, source path, line number, passage ID, and source hash make that transformation inspectable. The independent [line-mapping audit](runs/20260929T084125814134Z/line-mapping-audit.json) passes 426/426 identity and provenance checks across both source turns. That mechanical result is separate from the semantic assessment above; selecting a real line alone cannot prove entailment.

The shortening turn had two history messages and carried the same original evidence without new retrieval. It selected the same three supporting lines and repeated the same displayed answer. It is grounded but does not shorten. This must remain a failed edit request, not be counted as success because its citations pass.

## Research equivalence and comparison with C40

The `ask`, `assess_claims`, and `generate` function source is identical to the C40 version. `prompts/research.md` is byte-identical, SHA-256 `4d531737c34fc85b5eaa128b96510404a9ce4c7efaff037b4c5e89b69cb2897c`. For A1, the **entire actual model request** equals the earlier full-suite request: prompt, original-evidence records, current question, schema, and options. It has two messages and canonical JSON SHA-256 `9a64045602b3742d35edfd1a7924572097f46846b80479c3ddbacc2e017f4816`. This establishes request equivalence for the checked case; it is not a rerun of every prior question. [Equivalence audit](runs/20260929T084125814134Z/research-equivalence-audit.json)

The [preserved C40 report](final-chat-regression-report.md) recorded a grounded but incomplete first lecture answer and a source-shortening refusal after two nonverbatim-quote attempts. This version supplies the missing software side and fixes that quotation-format failure on both source turns. Source shortening remains unsuccessful for a different reason: exact repetition. The required ordinary drafting follow-up continues to pass. Earlier full-suite explanation and multipart-answer limitations are not erased by this bounded regression.

## Actual runtime and isolation

| Operation | Actual generations | Total generation time |
|---|---:|---:|
| Ordinary draft, shortening, fictional detail | 3 | 7.275 s |
| Chat-isolation ask | 1 | 8.881 s |
| Original A1 | 1 | 16.533 s |
| Lecture explanation | 1 | 17.739 s |
| Failed source shortening | 1 | 19.349 s |
| Reset response | 1 | 0.908 s |

All eight generations used real local `gemma4:e2b-it-qat`, Q4_0, Ollama `0.34.4`, digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`. No repair was invoked. Total measured generation time was 70.685 seconds; original chat CLI wall time was 7.383 seconds and the source conversation plus reset was 38.105 seconds. [All-attempt audit](runs/20260929T084125814134Z/all-attempts-audit.json)

The wrapper freshly launched the isolated server; server and client probes showed external IPv4 TCP, IPv6 TCP, and UDP denied with `EPERM`, while loopback worked and Wi-Fi stayed on. The server and CLI inherited the same OS profile, and the server stopped after execution. The reserved port was released directly to evaluator B. This evidence concerns these processes and their descendants, not unrelated host applications. [Server proof](runs/20260929T084125814134Z/isolation/server-network.json), [client before](runs/20260929T084125814134Z/isolation/client-network-before.json), [client after](runs/20260929T084125814134Z/isolation/client-network-after.json), [completion](runs/20260929T084125814134Z/isolation/run.json).

Automatic diagnostics passed 208/209 checks; the failure is precisely the 61 → 61 source-shortening result. This fraction is not an assignment grade. Original sources were unchanged, all raw responses are retained, and no additional model run replaced this result. This report makes no claim about Obsidian display, repository visibility, or course submission.
