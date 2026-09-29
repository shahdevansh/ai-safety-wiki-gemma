# Current verification and known limitations

The final recorded assignment demonstration has **three complete supported answers and one correct insufficient-evidence answer**. Required capability prompts, conversation shortening, note-based chat, original-passage search and separation of chat-only facts from research evidence pass. The broader independent suites have genuine failures, detailed below; this is not an all-tests-pass claim.

Confidence is high for the recorded execution, source/citation checks and explicit semantic assessments. Neither these tests nor the privacy scan establishes a universal guarantee.

## Exact current revision

- Harness SHA-256: `a00342076c80b8142fd456c842fcc25f11e940a2f2d7e70cfee449cb8a35b444`.
- Research prompt: `4d531737c34fc85b5eaa128b96510404a9ce4c7efaff037b4c5e89b69cb2897c`.
- [Input freeze](goal-run/freeze.json) and [source manifest](../source-manifest.json) identify all three current redacted originals.
- Every generation uses actual local `gemma4:e2b-it-qat`, digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`, Q4_0, Ollama 0.34.4. No synthetic/model-stub output substitutes for these records.
- [Terminal recording](goal-run/terminal.cast), [standalone replay](goal-run/terminal.html), [complete transcript](goal-run/terminal.txt), [model/device measurements](goal-measurements.json).

Changes include generic coverage instructions, source-intent routing, clearing irrelevant carried evidence, advancing scripted `/reset`, generic capability-intent handling and original-line selection plus shared per-claim quote validation for source-dependent chat. No answer-key string or question-specific answer branch was introduced. Tests and expected answers remain outside retrieval. Capability prompts use a disclosed deterministic harness description; ordinary chat, ingestion and all research questions use Gemma.

## Required four-question semantic review

| Case | Actual outcome and support assessment |
|---|---|
| [Assistance goal/uncertainty](goal-run/01-assistance-game.md) | **Pass.** Both requested aspects are explicit: promote human interests; remain uncertain about them and infer them. Each quote is an exact substring of the identified lecture passage and supports its claim. |
| [Deception comparison](goal-run/02-deception-detection.md) | **Pass.** Identifies thinking trace versus explicit model output. It is attributed to retrieved meeting notes and does not assert a proven detector or measured efficacy. |
| [Physical/human controls](goal-run/03-physical-defenses.md) | **Pass.** Names all three proposals: human override, multiple humans in decision loops, and physical buttons/levers to shut off software. Each has a supporting quote from the workshop passage; proposals are not presented as guaranteed defenses. |
| [Approved annual budget](goal-run/04-unsupported.md) | **Pass.** Gemma returns insufficient evidence without a dollar amount. The retrieved notes contain governance proposals, not an approved annual budget. This is an actual model abstention, not a citation-error fallback. |

All four use one generation and zero citation errors. Expected passages were retrieved for all three answerable questions. [Automatic checks](goal-automatic-checks.json) verify source bytes, line ranges, ID/quote membership and execution fields. The material-claim assessments above are separate AI-assisted semantic review, not a claim that substring checking proves entailment.

## Required mode checks

Both exact capability prompts return the correct Pip contract, with `retrieval_called=false`, no citations, no insufficient-evidence refusal and zero model calls explicitly recorded. Gemma's three-step study draft shortens from **99 to 42 words**, preserving the 5/20/5-minute sequence. These drafting turns and the chat-only codename acknowledgment make no retrieval calls.

The sixth chat turn retrieves original assistance-game material and cites the core goal, uncertainty, separate terminology reasons and the challenge of conflicting human interests. Those claims are supported by the retrieved lecture passages and attributed as notes. A separate [codename ask](goal-run/chat-isolation.md) returns insufficient evidence; its request contains no chat history. The synthetic codename remains absent from the raw corpus and searchable index.

[Source search](goal-run/search.md) displays original passages and locations with zero model calls. The literal sample [workshop-location search](goal-run/literal-search.md) finds workshop-related passages without a location, and the [standalone workshop ask](goal-run/literal-ask.md) correctly abstains. Additional [deny-all-network checks](goal-no-model/assessment.json) show reindex/search succeed without access even to localhost; answerable ask fails with a useful local-model-unavailable error and no fallback.

## Editorial review and re-ingestion

Six actual Gemma drafts were generated before review. They contained real defects: assistance terminology reasons were conflated; a hardware-governance sentence could imply that adding checks, rather than bypassing them, required a new fab; “limited to math” became “mathematical representations”; and architecture, physical-access and unemployment claims needed explicit attribution/qualification. The final curated notes correct these against the unchanged sources. This is editorial checking, not independent scientific validation of the original meetings.

[Before/after review hashes](goal-editorial-review.json) identify the actual draft and reviewed pages. A separate fresh isolated [reviewed re-ingestion](goal-reviewed-reingest.json) preserved all six note hashes and paths, made zero generation calls and introduced no duplicates. [Integrity comparison](goal-reingest-integrity.json), [final vault check](goal-vault-check.json) and [recording](goal-reviewed-reingest.cast) support that claim. The earlier re-ingestion inside the main demonstration preserved still-pending drafts; it is not counted as proof of completed editorial review. The default vault checker now rejects pending pages; `--allow-pending` is explicit for draft inspection.

[Obsidian evidence](obsidian/README.md) shows note/source/related links, the index/page list, and meaningful graph labels. The source-catalog screenshot was refreshed to match the final privacy revision; the unchanged readable-note/navigation screenshots remain valid.

## Independent full-suite findings before the final chat correction

[A's final report](independent/a/goal-verification/final-goal-report.md) uses one complete pre-chat-correction/final-corpus run with 22 actual generations. Its exact core hash is recorded in the report. Two of its three original answerable questions are complete; its why question merely restates the relationship instead of explaining it. Its unsupported and chat-isolation questions pass. Two of four new held-outs are complete; another omits the hardware/software rationale, and a mixed supported/missing question omits an explicit statement that a requested measurement is absent. A repaired citation becomes valid without fixing the missing explanation. An extra routed chat response adds an unsupported comparison about costs, despite having a valid source ID. Routing mechanics and reset pass; that chat grounding test fails.

[B's final report](independent/b/goal-verification/FINAL_REPORT.md) covers 32 commands and 24 actual generations. B01–B04 pass; its additional two-source question remains partial, omitting lack of consensus and conflicting human interests. Of five new held-outs, three pass, one is partial and one fails. The paraphrased capability question omits a command and misdescribes `review`/`doctor`; an intervention question covers four headline proposals but omits education/company/government coordination. These omissions and inaccuracies are preserved in [B's semantic assessment](independent/b/goal-verification/SEMANTIC_ASSESSMENT.json).

These observed failures explain why the required demonstration's 4/4 result is not a held-out accuracy estimate. The generic completeness prompt did not reliably solve explanation or coverage. At that revision, chat checked source-ID membership without per-claim quotes. The final correction has Gemma select original line IDs, resolves literal source text in the harness, and applies strict quote validation to source-dependent chat; semantic support and completeness still require review. The next concrete improvement would be a separate requested-component/claim-support check, evaluated on newly frozen cases, and testing additional unseen capability paraphrases. The final correction now routes generic capability intent through the accurate command contract. No successful output was substituted for a failed response, and expectations were not weakened to raise scores.

## Preserved required-chat failure and final correction

The [previous main recording](goal-run-before-chat-fix/CHAT-CITATION-FAILURE.md) contained one true statement with the wrong passage citation. Independent review caught what ID-membership checking missed. That actual response and its completed run remain preserved. A first correction asked chat to copy quotes and failed even after bounded repair; both agents retained those `c40a2ff…` failures. The final `a003420…` harness instead asks Gemma to select request-local original line IDs. The harness resolves exact text and passage provenance, then shares the research claim/quote validator and single bounded repair with source-dependent chat. A separate prompt allows history only to interpret references. Exact provenance does not prove semantic entailment. Ordinary conversational drafting remains unstructured. Generic capability requests now use the accurate command contract, including the precise meanings of `review` and `doctor`.

The four-question research prompt, retrieval, schema validation and model settings remain unchanged. [A's final bounded regression](independent/a/goal-verification/final-chat-lines-regression-report.md) uses eight real generations, with no repair: required chat, ordinary shortening, representative A1, isolation, reset and the lecture comparison all pass. Its 426 line-provenance checks pass. An additional source-based shortening still fails at 61→61 words. [B's final bounded regression](independent/b/goal-verification/LINE_REGRESSION_ADDENDUM.md) uses nine commands and ten generations, no repairs; required chat, the zero-history source question, capabilities, representative B01, isolation and reset pass. Its different source-shortening case passes 71→48. Both review semantic support, not just line identity. Research request equivalence is checked for A1 and B01. Earlier broad research-completeness failures are not claimed resolved by this chat-only correction.

## Independent final documentation checks

[A’s read-only audit](independent/a/goal-verification/final-parent-documentation-audit.md) and [B’s read-only audit](independent/b/goal-verification/FINAL_PARENT_AUDIT.md) independently checked the final main answers, grounded-chat claims, measured times and memory, 99→42-word follow-up, reviewed-note hashes and version/failure disclosures. Neither found a substantive mismatch. Their export/upload timing notes describe the audit moment; the final [publication check](goal-publication-check.json) and [authenticated delivery receipt](private-delivery.json) record completion of those later steps. The [17 unit tests](goal-unit-tests.json) separately check control flow and source/citation boundaries; stubs are not counted as model evaluations.

## Isolation, privacy and delivery boundaries

[OS policy evidence](goal-isolation/) records a fresh restricted server, inherited model-runner restrictions, client probes before/after, failed external IPv4 TCP/IPv6 TCP/UDP operations with permission errors, successful loopback, and a zero-exit completed run. Wi-Fi remains on by user request. This demonstrates external-network denial for the workload, not a host-wide air gap or a packet capture. GitHub upload occurs separately from isolated model execution.

The final corpus removes a speaker-specific biographical fingerprint and remaining named-person attribution. The [context-redaction ledger](privacy/context-redactions.json) records historical-copy changes; exact unredacted originals remain outside Git. Historical source IDs/hashes describe their original run, and their redacted copies are not claimed to be byte-identical. Failed and superseded runs remain labelled. [Historical review](REVIEW.md) retains earlier failures and fixes.

The repository is **private** under the user's latest instruction, overriding the assignment's public/signed-out clause. Course-portal submission has not been performed. [Requirement checklist](assignment-checklist.md) and [private-delivery verification](private-delivery.json) distinguish those boundaries from the demonstrated implementation.
