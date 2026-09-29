# Prospective held-out goal verification

This plan is frozen before the parent's next harness freeze and before observing any new model output. The original four A research cases, source search, capability prompts, draft/shortening, and chat-to-ask isolation case remain unchanged in `cases.json`. The baseline evaluator is an unchanged copy of the previously run evaluator. New cases are in `heldout-cases.json`; their answers and excerpts are never supplied to the model or included in the searchable source tree.

## New research coverage

1. A single-source why question requiring two distinct explanations. Passing requires assigning each explanation to the correct term, rather than repeating the premise or merging the reasons.
2. A two-source question linking single-optimum diversity limitations with aggregation of conflicting human interests. Both sources must be retrieved and must contribute citations; answering only one conjunct fails completeness.
3. A two-source question that asks both why hardware regulation was proposed and what physical human controls were proposed. Preserve proposal/attribution status. Both explanation and mechanisms must appear.
4. A mixed supported/missing-evidence question. Report the supported scenario and explicitly distinguish it from the absent real-world measurement. A wholesale abstention or fabricated measurement fails.

Each case has literal prospective source excerpts, a required source set, concept triage, semantic requirements, and unsupported-strengthening checks. Exact-string and concept checks only flag issues. The final decision comes from independently reading the actual answer, every material claim, the cited quotation, and its original context. A grounded restatement can still fail to answer a why question.

## Additional mode checks

The lecture-based chat prompt deliberately describes the source and asks a substantive question without relying on the old topic-trigger vocabulary. It should retrieve, explain, and cite the original. This assesses semantic routing for one held-out phrase, not all possible requests.

Reset is tested twice: first a bounded `/reset` then `/exit` smoke test, then a stateful fictional marker test if the smoke test exits. The reset must advance scripted input, clear actual model conversation context and carried evidence, and avoid making the marker searchable. The guard prevents a reset loop from consuming the whole evaluation. Timeout is an explicit failure, not a successful reset. Exact marker retention or absence is checked in the actual model request as well as the displayed answer.

## Execution plan

Wait for parent GO and final frozen code. Run a fresh whitelist copy under the approved OS isolation wrapper using actual local Gemma. The parent starts and stops the isolated daemon; this evaluator never alters global networking or repository privacy. All artifacts stay under this directory. Run the unchanged A suite first, then the four new held-out searches/asks, routing, and reset checks. Preserve every raw generation and repair attempt, including failures. Sum elapsed time across all generation attempts separately from total CLI wall time.

Search without model access will run under the approved deny-all-network profile as a direct host command after the main wrapper exits. Do not nest macOS sandbox-exec inside an existing sandbox: earlier evidence already demonstrates that launch is rejected before the CLI starts. This changes only execution placement, not the search query or required no-model behavior.

Check source hashes before/after, exact line ranges, expected source coverage, citation identity, and model identity/digest. Test sources, harness code, prompts, original cases, and held-out cases receive immutable manifests. No mocks, remote generation, external transmission, or publication.

## Verification limits and instruction precedence

The new attached assignment is identical to the earlier assignment after trimming surrounding whitespace. It still specifies a public repository, while the active user instruction requires a private repository. Honor the private instruction; do not claim signed-out public accessibility or publish the repository. Repository access, Obsidian screenshots, documentation, PII audit, and course submission are separate parent-owned checks. This bounded evaluator assesses actual local behavior and reports limitations honestly.

No runtime result is claimed by this prospective plan. Confidence in expected evidence: high; confidence in the future candidate's behavior: unknown until execution.
