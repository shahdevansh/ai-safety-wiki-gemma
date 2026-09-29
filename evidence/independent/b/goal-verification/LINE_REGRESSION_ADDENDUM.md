# Evaluator B: final line-reference chat regression

**All selected checks in this bounded regression pass on the new line-reference design.** The required assistance-game chat and the unchanged zero-history H3 question now produce useful answers with supporting citations on their first attempts. The earlier capability and quote-copying failures remain preserved; this addendum does not erase them or certify the full earlier suite on a new code version. Confidence is **high for these observed outputs**.

Tested core: `a00342076c80b8142fd456c842fcc25f11e940a2f2d7e70cfee449cb8a35b444`. Grounded-chat prompt: `d45dc84da09787da9c8af2d4304cafde7698bea8234fcd713c6acc67b81e9ebe`. The run used a fresh evaluator-owned copy and a fresh externally isolated local Ollama server, with **9 CLI commands, 10 actual Gemma generations and zero repairs**. Every generation reports the required Gemma tag and digest. The wrapper completed successfully and stopped its server. [Actual run](line-regression/) · [Isolation evidence](line-regression-isolation/) · [Detailed assessment](LINE_REGRESSION_ASSESSMENT.json)

| Check | Result and observed behavior |
|---|---|
| Required exact capabilities | PASS: accurate implemented commands and limits, no retrieval or model call. |
| Required ordinary draft/shortening | PASS: 99 to 42 whitespace-delimited words; three-step 5/20/5-minute plan retained. |
| Required assistance-game chat | PASS: goal, uncertainty, terminology reasons and conflicting-interest problem are all supported by the selected original lines. |
| Unchanged H2 capability paraphrase | PASS: accurate contract includes `chat`, properly describes `review` and `doctor`, and denies web browsing. This is labelled deterministic harness output, not model generation. |
| Unchanged H3 source question with zero history | PASS: preferences can be manipulated/shaped against interests, supported by correct source lines. |
| H3 unrelated topic switch | PASS: three book-club names as suggestions, no retrieval or source citations. |
| Added source-dependent shortening | PASS in this case: 71 to 48 words; preserves preference-versus-interest explanation and correct citations, using two history messages and carried original evidence without new retrieval. |
| Explicit reset after source dialogue | PASS: following capability record has zero history, no retrieval and no generation. |
| Representative B01 research | PASS: cultural skew and lack of consensus both retained with supporting exact quotes; no history. Its model-request payload is identical to the preceding core's B01 request. |
| Codename search and independent ask | PASS: chat-only fact is absent from original search; standalone ask explicitly abstains with zero history. |

The source-shortening case was added prospectively at the parent's request. The previous required script, H2/H3 wording, representative research question and expected claims were unchanged. The earlier complete independent suite was not rerun here. B05's cross-source omissions and H4's missing coordination detail remain reported limitations. This successful shortening example is not a guarantee for other requests.

## Citation integrity and semantic review

For source-dependent chat, Gemma now chooses request-local `L` identifiers. The harness resolves each selection to the literal original line, its passage ID, source path and absolute source line number. The full line catalog and raw model selections are saved. It does not normalize model-written quotations or substitute an expected answer: the model does not write the final quote at all.

Every saved catalog line was independently compared with the actual original file and its indicated retrieved passage. Every final passage text/hash and citation ID/quote passes exact checks. Each material factual claim was then manually assessed against its selected lines; all claims in this bounded run are supported. Combined claims use all necessary supporting lines. The required terminology claim, for example, selects the preference/interest framing plus both terminology-reason lines; it no longer joins them into a fabricated quotation.

The unchanged shared validator establishes exact provenance, not entailment. Some selectable list labels can still be insufficient support for a substantive claim, so semantic review remains necessary. No heading-only support was accepted as sufficient in this evaluation. [Mechanical checks](LINE_REGRESSION_MECHANICAL.json) · [Catalog and claim checks](LINE_REGRESSION_ASSESSMENT.json) · [Static integrity review](line-regression-static-review.json)

## Preserved failure history and scope

The preceding `c40a2f...` structured-quote attempt failed required chat and H3 after both initial and repair generations. Those actual responses remain in [the earlier addendum](CHAT_REGRESSION_ADDENDUM.md) and [raw records](chat-regression/). The earlier wrong specific passage citation and inaccurate capability paraphrase also remain in the full-suite and documentation-audit records. No failed response or expectation was overwritten.

This addendum supports the new chat line-selection path, its selected conversational follow-ups, the tested capability paraphrase and representative research isolation. It does not establish an all-tests-pass project, fix the older research completeness omissions, certify unseen paraphrases, or replace the parent's new full required demonstration and final documentation audit.
