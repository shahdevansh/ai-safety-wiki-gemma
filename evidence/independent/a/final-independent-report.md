# Independent evaluator A — final regression

**The final candidate produces complete answers for 2 of the 3 source-answerable questions. The third fails explanatory completeness despite an authentic citation. The unsupported question passes.** Chat, conversational shortening, original search, ingestion, and the tested chat-to-ask isolation case continue to work.

Confidence: **high** in these observed results. The citation-repair change does not justify claiming that all independent questions now pass.

This is a separate regression report. The [initial report](independent-report.md), its original responses, and its failed checks remain preserved. No question, expected excerpt, or evaluator check was weakened. No further model runs were made after this final regression.

## What stayed fixed and what changed

The original [prospective cases](cases.json) and [evaluator](evaluate.py) are byte-identical to those used in the initial run. All three frozen source hashes are identical. The final run used a fresh copy of the candidate and generated its own wiki and index, excluding previous outputs and answer keys. Both the source files in the frozen project and those in the execution copy remained unchanged.

The reviewed research-code changes format evidence as JSON records with explicit source IDs, paths, line ranges, and text; permit at most one citation repair using the same passages and schema; and retain the initial response and validation errors. The repair prompt supplies neither expected answers nor additional evidence. A separate source-catalog sentence was clarified. This evaluator did not read or use the parent's other tests or another evaluator's results.

The final run directory is [20260929T074038279878Z](runs/20260929T074038279878Z/summary.json). The initial run remains [20260929T072034705632Z](runs/20260929T072034705632Z/summary.json). The [machine-readable comparison](runs/20260929T074038279878Z/before-after.json) preserves both actual answers and timings.

## Research results: before and after

| Fixed case | Initial result | Final result |
|---|---|---|
| Assistance-game objective and uncertainty | Complete and grounded, with repeated citations to overlapping chunks. | **Pass: complete and grounded.** Both required facts remain; each now cites one relevant passage. |
| Three proposed safeguards for human intervention | Complete and grounded. | **Pass: complete and grounded.** The final displayed answer is identical to the initial answer. |
| Why alignment and interpretability are two sides of one objective | Grounded but incomplete: gave the direction/method analogy while omitting the explicit model-internals rationale. | **Fail: explanatory completeness.** The answer only restates the question's premise. Its one claim is supported, but it supplies no explanation. |
| Exact date of the next infrastructure workshop | Explicit model abstention. | **Pass: explicit model abstention.** Raw response reports insufficient evidence and no claims. |

Final evidence cards: [Question 1](runs/20260929T074038279878Z/records/ask-1-assistance-objective.md), [Question 2](runs/20260929T074038279878Z/records/ask-2-infrastructure-controls.md), [Question 3](runs/20260929T074038279878Z/records/ask-3-alignment-interpretability.md), and [unsupported question](runs/20260929T074038279878Z/records/ask-4-unsupported-schedule.md). Each links its raw model request, response, retrieved originals, source IDs, and timing.

For Question 3, the fixed question was:

> Why do the notes describe alignment and interpretability as two sides of the same objective?

The entire substantive final answer was:

> Interpretability and alignment are two sides of the same objective [Pd3902efa8beb]

Retrieval did find the necessary explanation, including “Hard to align models without understanding their internals” and “Need to know what direction to go, and how to get there.” The final answer omits both. This is an answer-generation failure, not a retrieval failure or a false citation. The initial answer's direction/method explanation is also absent, so the final candidate regressed on this fixed case.

The final answers' displayed material claims were checked against their quotations and original passages. All retained claims are supported, and all original passage text, line ranges, source hashes, IDs, and verbatim quotes passed integrity checks. Those checks cannot determine whether an answer adequately addresses the question. Question 3 demonstrates the difference directly.

## Repair behavior and retained attempts

Each of the four research questions and the additional chat-isolation ask completed with **one recorded generation attempt and zero citation-validation errors**. All attempt identities and returned model names match the expected Gemma. No repair was needed in this independent regression, so these cases do **not** exercise or establish the repair branch's effectiveness.

There were 14 actual generations: six ingestion calls, five ask calls including the isolation check, and three generative chat turns. The two capability responses were supplied by the harness without generation. Initial and final outputs remain separate; no failed answer was replaced by an invented success or by a rerun of that question.

## Modes, source integrity, and wiki drafts

- Help and the literal `ingest ./vault/raw` command succeeded. Fresh ingestion produced six notes in **28.720 seconds**; repeat ingestion took **0.078 seconds**, preserved filenames and bytes, and made zero generation calls.
- All six fresh note files are byte-identical to the initial run's generated notes. The previously documented defects therefore remain: meaning drift from “limited to math” to “limited to mathematical representations”; conflated reasons for avoiding “values” versus stated preferences; inconsistent attribution; a missing `Useful details` section; six bullets instead of three to five; and a 234-word body despite an under-220-word prompt. These are pending-review drafts in the evaluator's copy, not a review of the separately curated submission wiki.
- Both capability prompts, the invitation draft, its shorter follow-up, and the fictional-detail chat turn produced the same displayed text as initially. They made no unnecessary retrieval calls. The draft again contains **69 words**, followed by a **49-word** revision. The one-word miss against the requested 70–90 range remains a minor instruction-following failure.
- Original search returned exact original passages and paths without an answer-generation record. The nested deny-all sandbox attempt again failed before the CLI launched, with `sandbox_apply: Operation not permitted`; that infrastructure failure is retained. A separate direct host launch under the approved deny-all-network profile succeeded in **0.084 seconds**, with no model daemon started and zero model calls. [Failed nested attempt](runs/20260929T074038279878Z/commands/search-model-unavailable.json); [successful direct attempt](runs/20260929T074038279878Z/commands/search-model-unavailable-direct.json).
- The standalone ask after the fictional chat appointment again returned explicit insufficient evidence. Its actual model request contained the research system instruction and current evidence/question, without the chat-only time or room. Originals remained unchanged. [Isolation answer](runs/20260929T074038279878Z/records/ask-chat-isolation.md)

## Isolation and model identity

The final run used local `gemma4:e2b-it-qat`, family `gemma4`, Q4_0, Ollama `0.34.4`, with the same exact digest as the initial run:

```text
07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c
```

The approved wrapper launched a fresh daemon and the CLI/evaluator tree under OS-enforced loopback-only networking. External IPv4 TCP, IPv6 TCP, and IPv4 UDP probes were denied with `EPERM` for the server and for the client before and after execution. Loopback worked. Wi-Fi remained on; the measured condition is external-network denial for the tested process trees. The wrapper stopped its isolated server afterward.

Final proof: [server](runs/20260929T074038279878Z/isolation/server-network.json), [client before](runs/20260929T074038279878Z/isolation/client-network-before.json), [client after](runs/20260929T074038279878Z/isolation/client-network-after.json), and [wrapper completion](runs/20260929T074038279878Z/isolation/run.json). These files are retained independently of the initial run's proof.

## Latency, including every attempt

The final generation column sums every saved attempt for each question. All final cases happened to require exactly one attempt; the reported values do not omit repair time. CLI time additionally includes retrieval, model identity/metrics calls, validation, and saving.

| Case | Initial generation time | Final all-attempt generation time | Final attempts | Final CLI wall time |
|---|---:|---:|---:|---:|
| Question 1 | 16.674 s | 17.933 s | 1 | 18.013 s |
| Question 2 | 13.774 s | 13.481 s | 1 | 13.563 s |
| Question 3 | 12.646 s | 12.301 s | 1 | 12.380 s |
| Unsupported question | 5.206 s | 4.823 s | 1 | 4.900 s |
| Chat-isolation ask | 5.336 s | 6.254 s | 1 | 6.334 s |

The five-turn chat session took **6.588 seconds** of CLI wall time. These are individual observations, not performance distributions or proof that the code change caused a speed improvement.

## Limits and final assessment

The preserved automatic summary reports **295 of 299 checks** passing. Three failures concern the missing Question 3 concepts; the fourth is the nested-sandbox infrastructure failure. The direct search check later succeeded. The initial count was 303 of 305; the denominators differ because per-citation checks depend on the number of citations produced. Neither fraction is an assignment grade or a semantic-completeness score.

The final candidate retains working local Gemma execution and the tested mode boundaries, but the correct independent result is **2/3 answerable questions complete, 1/3 failing explanation, and the unsupported question passing**. Valid citations alone did not prevent the explanatory failure, and the citation-only repair trigger did not address it. A future improvement should assess whether an answer supplies the components requested by the question, separately from quote integrity, while retaining the original response and evaluating on unchanged unseen cases.

This regression does not verify Obsidian UI screenshots, reviewed submission-note quality, peak total model/unified memory, public accessibility, or portal submission. Those require separate evidence. The earlier code-derived chat limitations also remain: vocabulary-based retrieval routing and citation-ID checks without enforcement of claim coverage or semantic support. No additional live notes-based chat case was added during this fixed regression.

All links in this report are relative and use sanitized source names. Raw local execution logs preserve local filesystem paths and require redaction before public distribution.
