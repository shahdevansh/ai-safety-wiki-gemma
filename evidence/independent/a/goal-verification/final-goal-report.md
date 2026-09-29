# Independent final goal verification

**The final frozen candidate passes the direct factual, unsupported-question, conversation-isolation, and reset checks, but still has measured explanation-completeness and chat-grounding limitations.** The unchanged A questions yield **2/3 complete supported answers**, plus a correct unsupported-question abstention. The four new held-out questions yield **2/4 complete answers**; the other two omit requested components. Source-intent routing now works, but its actual chat answer includes one unsupported comparison.

Confidence: **high** in these observed findings. The automatic count, 678/683 checks, is not a grade and misses important semantic defects.

## Final evidence identity

The final full run is `20260929T081134040293Z`. It used exactly:

| Artifact | SHA-256 |
|---|---|
| Harness | `640884e09d7be392cad6df4d8d2421d6879006b466bda8e7b5e3101a18da6826` |
| Research prompt | `4d531737c34fc85b5eaa128b96510404a9ce4c7efaff037b4c5e89b69cb2897c` |
| Final lecture source | `76c88bc45bce852e63112fffc2cd94ffd377aa0e4a8b1fe7d7c3713a8afa5d02` |

The original A cases and evaluator were unchanged. The [held-out cases](heldout-cases.json) and [prospective plan](heldout-plan.md) were written before observing new outputs. No expected answer or answer-key file entered the searchable corpus or model prompt. The final corpus removes a biographical anecdote and named-person attribution; none of the expected technical excerpts required revision. Final execution-copy and upstream source hashes remained unchanged throughout the completed run.

Provenance: [design freeze](design-freeze.json), [final freeze](final-core-freeze.json), [tested harness manifest](runs/20260929T081134040293Z/harness-manifest.json), and [actual test-file hashes](runs/20260929T081134040293Z/evaluator-input-manifest.json).

All **22 completed generations** used actual local `gemma4:e2b-it-qat`, Q4_0, Ollama `0.34.4`, with digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`. The two capability responses were harness responses, not additional model calls.

## Semantic verdicts

| Case | Final verdict | Reason |
|---|---|---|
| A1: assistance-game objective and uncertainty | **Pass** | Promoting human interests, uncertainty about them, and inference are all answered and supported. |
| A2: three safeguards | **Pass** | All three requested proposals appear with matching evidence. |
| A3: why alignment and interpretability are linked | **Fail: completeness** | The answer only repeats that they are two sides of one objective. It omits the retrieved explanation about understanding internals and the direction/method analogy. |
| A4: unsupported workshop date | **Pass** | Gemma itself returns insufficient evidence with no claims; this is not an error fallback. |
| H1: separate reasons for terminology | **Pass** | Correctly distinguishes culture-war reactions from manipulability of stated preferences. |
| H2: diversity and conflicting human interests | **Pass** | Explains single-optimum framing and the separate aggregation challenge, using both originals. Its first exact quote is narrower than the full causal claim, but the surrounding cited passage contains the single-optimum rationale. |
| H3: hardware rationale and physical controls | **Fail: completeness** | Lists both physical mechanisms and cites both sources, but merely repeats that hardware regulation is more tractable. It omits why software copying and fabrication constraints create that contrast. |
| H4: scenario versus missing measurement | **Fail: completeness** | Correctly labels 40% as a scenario, but does not explicitly say the measured real-world rate is absent. It does not invent a rate; it simply leaves that requested part unanswered. |

Retrieval returned the prespecified supporting passages for all supported cases. The final displayed ask claims have valid source IDs and exact quotations; independent agent review confirms their factual support in the cited passages. The failing explanation cases demonstrate that source support and completeness are different requirements. H4 also shows why substring-based triage cannot replace review: attribution text can satisfy a loose word check without answering the missing-evidence component.

Actual evidence cards: [A1](runs/20260929T081134040293Z/records/ask-1-assistance-objective.md), [A2](runs/20260929T081134040293Z/records/ask-2-infrastructure-controls.md), [A3](runs/20260929T081134040293Z/records/ask-3-alignment-interpretability.md), [A4](runs/20260929T081134040293Z/records/ask-4-unsupported-schedule.md), [H1](runs/20260929T081134040293Z/records/heldout-1-distinct-reasons.md), [H2](runs/20260929T081134040293Z/records/heldout-2-plural-human-objectives.md), [H3](runs/20260929T081134040293Z/records/heldout-3-hardware-human-override.md), and [H4](runs/20260929T081134040293Z/records/heldout-4-scenario-versus-measurement.md).

## Mode checks and the remaining chat defect

Help, literal `ingest ./vault/raw`, source search, both capability prompts, drafting, and conversational shortening worked. Capabilities and ordinary drafting made no unnecessary retrieval calls. The draft contained 69 whitespace-delimited words despite the requested 70–90 range, and the follow-up shortened it to 49 while preserving its purpose. This minor instruction-following miss remains recorded.

The standalone ask after a fictional chat fact abstained. Its actual request excluded the chat-only sentinel; originals were unchanged. Scripted `/reset` advanced correctly, cleared the prior marker from the actual model request, and left zero prior conversation messages. The reset test establishes history clearing for this case; it did not preload retrieved evidence before resetting, so it is not an independent test of clearing every possible carried-evidence state.

The held-out lecture prompt now triggers retrieval and cites the right original. Its answer gives the supported hardware/fabrication and software-copying contrast, but adds that **“malware costs are relatively low compared to hardware security measures.”** The source contains no such comparison. The citation ID is valid, yet it does not support that added claim. Therefore **routing mechanics pass; chat groundedness fails**. The leading “Suggestion” label does not turn this factual comparison into supported evidence. [Actual routed chat](runs/20260929T081134040293Z/records/heldout-chat-note-routing/chat-01.md)

A direct search under a deny-all-network sandbox also succeeded, returning original passages with zero model calls in **0.075 seconds**. It did not start or use a model daemon. [No-network search record](runs/20260929T081134040293Z/commands/search-model-unavailable-direct.json)

## Repair and latency

H3 required one bounded repair. The first attempt supplied a nonverbatim quote combining a heading and bullet without preserving the original Markdown. The second copied the exact bullet from the same unchanged passage. Quote validation then passed, but the missing explanation remained missing. Both attempts are retained. Every other final ask used one attempt.

| Question | Attempts | Total generation time across all attempts |
|---|---:|---:|
| A1 | 1 | 16.698 s |
| A2 | 1 | 17.548 s |
| A3 | 1 | 9.905 s |
| A4 unsupported | 1 | 10.544 s |
| Chat-to-ask isolation | 1 | 9.054 s |
| H1 | 1 | 18.098 s |
| H2 | 1 | 16.444 s |
| H3 | 2 | 37.859 s |
| H4 | 1 | 13.519 s |

Fresh six-note ingestion took **27.836 seconds** of CLI wall time; unchanged re-ingestion took **0.079 seconds** without new generation. The five-turn baseline chat took **6.631 seconds**. These are individual observations, not a speed benchmark. [All-attempt audit](runs/20260929T081134040293Z/all-attempts-audit.json)

## Offline execution and retained history

A fresh daemon and the evaluator/CLI process tree ran under the approved OS loopback-only policy. The server and the client before and after execution received `EPERM` for external IPv4 TCP, IPv6 TCP, and IPv4 UDP probes; loopback worked. Wi-Fi remained on. The proven condition is external-network denial for the tested processes, not physical disconnection of the computer. The wrapper stopped its isolated server before releasing the port to the other evaluator.

Proof: [server](runs/20260929T081134040293Z/isolation/server-network.json), [client before](runs/20260929T081134040293Z/isolation/client-network-before.json), [client after](runs/20260929T081134040293Z/isolation/client-network-after.json), and [wrapper completion](runs/20260929T081134040293Z/isolation/run.json).

The earlier goal run is retained locally. It had failed lecture routing, a failed H2 citation repair, and an upstream-source immutability failure when the parent performed the disclosed privacy edit; its own execution copy was unchanged. A subsequent run was explicitly interrupted and marked superseded after the final routing-only change arrived. Its partial summary must not be treated as a completed test. The report above relies on one complete final-code/final-corpus run, not stitched results from different versions. Historical raw files may contain removed details and should remain local; any shared historical evidence must be an explicitly redacted export.

## Scope limits

Fresh generated wiki pages remain drafts until reviewed. This evaluator did not inspect the final curated vault, Obsidian UI evidence, repository access, total peak model memory, or course submission. The active instruction requires a private repository, so this report does not claim the assignment's public signed-out-access requirement is satisfied.

The observed limitations justify separate checks for whether all requested components were answered and whether every chat claim is supported, beyond validating citation IDs or verbatim quotes. No prompt or test was retuned in response to these final held-out answers, and no further model rerun was used to replace their failures.
