# Evaluator B addendum — final harness regression and publication review

**Final verdict: the four principal assignment answers and B's four principal independent cases pass substantive review. B05, the additional two-source stress case, remains PARTIAL and regresses in completeness.** Every material claim in that final stress answer is supported, but relevant requested content is missing. Do not describe the entire independent suite as passing. Confidence is **high for these observed outputs and comparisons**; these results do not establish broad reliability.

This addendum supplements rather than replaces [the original report](REPORT.md). All earlier expectations, outputs and failures remain intact. Final regression used exactly the frozen B questions, expected passages and settings, a new evaluator-owned workspace with no index/wiki, actual local Gemma, and a fresh externally isolated server. No expected answer was revised after seeing a result. The tested final harness SHA-256 is `bc42a74f3dfcbb4373a75647e80d95cf7ec5be0a03525017d1f9152ad9d13f4b`.

## Integrity of the final change

[Final diff](final-patch.diff) shows three generic changes: research evidence is rendered as JSON records with an explicit source ID/path/line range/text association; a single citation-repair attempt is allowed after strict validation errors; and index wording refers to public aliases instead of private dates. No answer-key string, per-question branch, source change, retrieval change or weakening of the quote validator was introduced. The original support schema was restored after the unsuccessful line-enumeration trial.

Repair receives the original question, unchanged retrieved evidence, the first raw response, validator errors and generic quotation instructions. It does not receive evaluation expectations. First and repaired generations/errors are retained; a RuntimeError during repair now leaves the original failed response saveable. That exception-preservation branch was statically reviewed, not deliberately exercised in this live run. A quote's identity still cannot establish semantic entailment or completeness. Top-level `generation.metrics` describes the last generation; total response work must account for all recorded attempts.

## Earlier failures remain evidence

1. **Initial recorded Q2: FAIL.** The answer used a known but wrong lecture passage ID for fundamentals content and a nonverbatim joined quotation. Strict validation rejected it. Preserved at `evidence/assignment-initial/02-deception-detection.json`.
2. **Line-enumeration schema trial: semantic FAIL.** Q1 supported a goal claim with only the heading “The Assistance Game Model” and omitted uncertainty. Q2 supported a deception claim with the unrelated heading “Hard Problems for the Assistance Game.” Zero mechanical citation errors did not make these answers grounded. Preserved in `evidence/assignment-schema-trial/`.
3. **Bounded repair alone: FAIL on Q2.** Both attempts retained the wrong ID/nonverbatim quote. The initial and repaired raw generations are present in `evidence/assignment-repair-trial/02-deception-detection.json`.
4. **Final JSON-record presentation: the four fixed assignment cases pass on their first attempts.** No repair was needed, so these outcomes are not evidence that repair alone solved the problem.

## Final assignment answers, reviewed independently

| Case | Semantic finding |
|---|---|
| Assistance-game goal and uncertainty | PASS: promoting human interests and uncertainty about those interests are both stated and separately supported by the correct source. |
| Deception comparison | PASS: thinking trace versus explicit model output, with the correct fundamentals passage ID. No claim that the discussion establishes a proven detector. |
| Physical/human controls | PASS: human override, multiple humans and physical shutdown controls are all retained as proposals. |
| Approved treaty budget | PASS: explicit insufficient evidence, with no invented amount. |

All retrieved line ranges and source hashes match the raw originals, and every final citation quote occurs exactly in its identified passage. The completed isolation record has exit status zero with a fresh server stopped afterward. [Detailed final-assignment review](final-assignment-semantic-review.json)

## Unchanged independent B cases on the final harness

| Case | Initial result | Final result |
|---|---|---|
| B01 values obstacles | PASS | PASS: skew and no consensus both covered. |
| B02 mountaintop paraphrase | PASS | PASS: agency and the right to non-optimal choices both covered. |
| B03 oversight comparison | PASS | PASS: regulator oversight, direct inspection and political difficulty covered. |
| B04 missing workshop schedule | PASS | PASS: explicit abstention. |
| B05 cultural skew and preference manipulation | PARTIAL | **PARTIAL, worse coverage.** Final answer covers manipulated/external preference shaping but drops Western/English skew, lack of consensus and conflicting human interests. Both required sources were retrieved; only the lecture source is cited. |

The original B05 answer at least included Western/English skew; the final answer does not. This is an answer-completeness regression, not retrieval failure or fabricated content. There was no attempt to tune the system to B05 after observing it. [Final comparison and claim checks](final-regression-semantic-assessment.json)

The final B suite completed **24 CLI commands and 18 actual Gemma generations**, with the same model tag/digest and settings as the original run. All final research responses used one attempt. Capability questions skipped retrieval; the real Gemma draft shortened from **98 to 43 words** and retained its one-page study-guide purpose. Grounded chat retrieved/cited notes, while the injected hypothetical schedule remained outside searchable evidence and the separate ask abstained. Re-ingestion preserved all source bytes, all six note bytes and paths, with no duplicate notes. A fresh CLI process successfully used the persisted index. [Final suite](final-regression/), [final network proof](isolation-final-regression/)

The earlier direct deny-all search and second-server persistence tests remain recorded in the original report. The final run repeated the affected ask/chat/ingestion paths in a fresh server, without overwriting those earlier artifacts.

## Concrete README review

The reviewed README correctly describes process-scoped external-network denial with Wi-Fi still on, source redaction before the public baseline freeze, local Gemma identity, ordinary and isolated commands, separate modes, and the limits of quote validation. The previously invalid `chat --mode local` command is fixed. All **45 local Markdown targets** existed at the audited revision.

The four published answer timings agree with their saved attempt metrics. The parent RSS sample maximum recomputes to **4.8338 GiB**, uses the final run's server PID, and is accurately labelled a sampled sum rather than a precise peak. The recorded assignment draft's **68-to-28-word** shortening and retained three-step plan are verified. All six current submitted pages carry reviewed status. [README audit](final-readme-audit.json)

One minor wording correction was requested: the generic sentence saying every answer includes resident-memory snapshots should describe memory fields/availability, because in-sandbox runtime RSS is unavailable; the later measured-results section already states that limitation correctly. The final independent-results paragraph must retain B05's regression and distinguish principal-case passes from all-case success. No additional README command, metric or local-link blocker was found in the audited revision.
