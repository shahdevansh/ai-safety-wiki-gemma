# Historical review — earlier source/code revision

This report describes the earlier `assignment-run` revision. For the current frozen code and privacy-revised sources, use [GOAL-REVIEW.md](GOAL-REVIEW.md). Historical evidence copies have disclosed privacy redactions; old hashes refer to the original run. This file is retained to preserve earlier failures and fixes.

# Review record and preserved limitations

The publication corpus consists of three redacted meeting-summary exports. Identifying metadata, biographies, personal follow-ups, and incidental scheduling details were removed before freezing the public sources. The private originals and earlier unredacted evidence remain outside the public repository. Ingestion and evaluation must preserve the redacted source bytes.

## Prior development failures

Earlier runs, before the publication corpus was frozen, exposed three real problems. A generated research response used a filename instead of its passage ID; another changed formatting inside a supposedly exact quote; a third incorrectly abstained on an answerable question. Citation checks rejected the malformed references. JSON Schema constrained valid IDs, and generic instructions clarified that ordinary within-source references could be resolved. A reasoning-only retry had not fixed the abstention. These observations are retained as development history, not counted as current-corpus passes.

Capability answers also overclaimed general research abilities. The harness now supplies a fixed, accurate capability contract for capability prompts. It labels that origin explicitly. Drafting, follow-ups, factual answers and ingestion still invoke actual local Gemma.

Generated summaries can overstate claims recorded in notes. The curated pages are reviewed to distinguish a workshop proposal or compressed lecture claim from independent scientific validation. Graph/computation claims, an unemployment scenario, and physical-access statements especially require this distinction.

Independent evaluators recorded their own prospective expectations, actual outputs, failures, and semantic review. Mechanical citation checks establish source-label and substring integrity; they do not prove entailment.

## Network-isolation proof

A dedicated Ollama server is started inside the macOS sandbox before serving requests. Its launcher verifies external IPv4 TCP, IPv6 TCP and UDP operations receive OS permission errors, then execs Ollama in the same restricted PID. Spawned model runners inherit that restriction. The CLI and its descendants run inside the same policy, with before/after probes. Loopback succeeds so local inference can proceed. Cloud features are disabled separately. The user's ordinary Ollama service and Wi-Fi state are untouched.

This is enforced process isolation, not a mocked inference test. It demonstrates operation without external-network access while the host remains connected. It is not a claim that the host's Wi-Fi was switched off.

## Publication privacy

The candidate uses fresh Git history; private earlier commits are not ancestors. Public evidence is regenerated from the redacted corpus. Public screenshots must show the redacted vault and receive visual review. Text and reachable-history scans supplement that review; they do not prove that every possible indirect identifier is absent.

## Final recorded research tests

1. **Assistance goal/uncertainty — pass.** Both requested parts are explicitly stated. Both quotations are exact substrings of the same lecture passage, and each supports the associated claim.
2. **Deception comparison — pass.** The answer identifies thinking trace versus explicit model output and cites the fundamentals passage. The meeting-note attribution and question framing identify this as a recorded discussion; it does not assert a validated detection method.
3. **Physical controls — pass.** Human override, multiple humans, and physical shutdown controls are all present, separately supported, and explicitly called proposals.
4. **Approved budget — pass.** The actual model returns insufficient evidence, without supplying a number. The retrieved notes contain no approved budget.

See the [final cards and transcript](assignment-run/) and [independent reports](independent/README.md). The final four questions each used one generation. Mechanical verification was followed by semantic comparison against the cited passages.

## Preserved current-corpus failures and changes

- [Initial recorded run](assignment-initial/): Test 2 selected the wrong existing passage ID and joined source lines without their Markdown punctuation. The strict validator rejected it. The other fixed tests passed.
- [Constrained-schema trial](assignment-schema-trial/): an `anyOf` schema restricted quotations to complete lines paired with source IDs. Tests 1 and 2 then cited headings that did not support their claims; Test 1 also omitted uncertainty. These are semantic failures despite valid substring checks. This approach was removed.
- [Bounded-repair trial](assignment-repair-trial/): restoring the original schema and supplying a single validation-repair round did not fix Test 2. Both actual attempts are retained. No successful answer was substituted into that record.
- **Final change:** research evidence is serialized as separate JSON records containing `source_id`, path, line range and original text. The quote instruction requests a short single-line substring from the same record. This addresses the observed passage-boundary confusion without changing retrieval, sources, fixed questions, expected answers, temperature, or model. The final full recorded suite passed. One generic repair remains available for invalid citations; strict validation is never relaxed and attempts stay visible. If repair inference raises an error, the initial response remains saveable.

Each trial had a fresh externally isolated server and its own before/after proof directory. These are iterative development results on the same fixed cases, not a held-out accuracy estimate. The two independent evaluator suites remain separate and include their own incomplete answers.

## Curated-page corrections

The assistant reviewed all six generated pages against the frozen source text and recorded [before/after hashes](editorial-review.json). Corrections distinguish “limited to math” from “mathematical representations,” separate the reasons for using interests instead of values/preferences, restore summary/detail structure, and attribute architecture, hardware, physical-access and unemployment claims as discussion claims or scenarios. Re-ingestion preserves these reviewed pages. This is AI-assisted editorial review, not independent factual verification of the meetings themselves.

## Remaining limitations and improvements

Citation identity does not prove entailment; the failed heading-citation trial makes that concrete. Lexical retrieval and chat's keyword router can miss paraphrases or retrieve unnecessarily. The codename acknowledgment triggered retrieval because its instruction mentioned “wiki,” though no personal fact entered the source index. Chat checks unknown citation IDs but does not strictly enforce per-claim quotation support. Generated draft length and attribution also require review. Next improvements: add a frozen paraphrase/routing regression set, enforce draft structure/length, and evaluate a local reranker plus claim-completeness checks without training on the evaluation answers.
