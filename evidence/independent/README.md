# Independent evaluation evidence

These are two independent agents, not human graders. Each wrote prospective questions and supporting expectations, ran actual local Gemma under OS external-network denial, then assessed the answers against original sources. Evaluation answers were not supplied as retrieval evidence.

## Final bounded regressions

Final harness SHA-256: `a00342076c80b8142fd456c842fcc25f11e940a2f2d7e70cfee449cb8a35b444`. Grounded-chat prompt: `d45dc84da09787da9c8af2d4304cafde7698bea8234fcd713c6acc67b81e9ebe`. Both use the current source manifest and actual isolated Gemma. Source-dependent chat selects original line IDs; the harness resolves exact quotations and source locations.

- [A's final line-selection regression](a/goal-verification/final-chat-lines-regression-report.md): eight actual generations, no repair. Required ordinary chat/shortening, representative A1 research, chat/ask isolation, reset, and lecture comparison/citations pass. All 426 original-line provenance checks pass. **An extra source-shortening case fails: the 61-word answer repeats verbatim.** Diagnostic check totals are not an accuracy or grade estimate.
- [B's final line-selection regression](b/goal-verification/LINE_REGRESSION_ADDENDUM.md): nine CLI commands, ten actual generations, no repairs. Required grounded chat, zero-history source question, capability paraphrase, drafting/shortening, source topic switching, representative B01 research, isolation and reset pass. B's different source-shortening case passes at 71→48 words. [Detailed assessment](b/goal-verification/LINE_REGRESSION_ASSESSMENT.json).

Both independently inspect whether each claim follows from its selected original lines, beyond automatic quote identity. Representative research requests are identical to the prior full suites. These are bounded regressions, **not full research-suite reruns or proof that all prior completeness failures are fixed**.

## Full suites before the final chat correction

The full suites below use core `640884e09d7be392cad6df4d8d2421d6879006b466bda8e7b5e3101a18da6826`, research prompt `4d531737c34fc85b5eaa128b96510404a9ce4c7efaff037b4c5e89b69cb2897c`, and the current privacy-revised sources.

- [A full-suite report](a/goal-verification/final-goal-report.md): 2/3 original answerable questions complete; unsupported and chat-isolation checks pass. New held-outs: 2/4 complete. Routing/reset pass; extra chat contains an unsupported comparison. 22 actual generations.
- [B full-suite report](b/goal-verification/FINAL_REPORT.md): B01–B04 pass; B05 remains partial. Five fresh held-outs: three pass, one partial, one fail. A capability paraphrase misstates commands; an intervention answer omits coordination detail. 32 commands, 24 actual generations. [Semantic assessment](b/goal-verification/SEMANTIC_ASSESSMENT.json).
- [B's requirement audit](b/goal-verification/REQUIREMENT_AUDIT.md) records checks at that revision; the root [current review](../GOAL-REVIEW.md) records subsequent demonstration, documentation and delivery checks.

The intermediate `c40a2ff…` free-quote chat repair also failed: [A](a/goal-verification/final-chat-regression-report.md) and [B](b/goal-verification/CHAT_REGRESSION_ADDENDUM.md) preserve nonverbatim-quotation failures. The final line-selection correction passes affected citation cases, while incomplete research answers and A's source-shortening failure remain documented.

## Historical development evidence

[A initial report](a/independent-report.md), [A earlier final report](a/final-independent-report.md), [B initial report](b/REPORT.md), and [B earlier addendum](b/FINAL_ADDENDUM.md) preserve previous outcomes. Goal-verification directories also retain failed and explicitly superseded runs; only the final run identified in each final report supports the current verdict. Interrupted runs are not passes.

Shared copies replace local account paths with `<submission>`, `<evaluation>`, `<local-home>` and legacy source aliases. [Earlier export hashes](export-redactions.json) and [current export hashes](goal-export-redactions.json) document those substitutions. A further [privacy ledger](../privacy/context-redactions.json) documents removal of identifying biographical context from historical source excerpts and generated outputs. Exact private originals remain archived outside Git. Old source hashes, IDs and frozen-file hashes describe the original run; redacted historical copies are not a byte-identical reproduction. Scores and failure verdicts were not changed. Final-corpus model answers are preserved; `.state`, private runtime files and private indexes are excluded. Recorded commands using path placeholders require local path substitution when replayed.
