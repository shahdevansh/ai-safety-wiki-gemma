# Evaluator B: grounded-chat regression

**The patch fixes the tested capability paraphrase but fails the two source-dependent chat checks.** Both chat answers end in citation-validation failure after an initial generation and one repair. The strict validator correctly prevents their faulty citations from being displayed, but the user receives no useful answer despite relevant evidence being retrieved. This is a functional regression, not a successful grounded-chat repair. Confidence is **high for these observed records**.

The bounded suite tested core `c40a2ff46ff488cf0d5fead68b7ecafb18142c7ff24cdee51b9e30b76ed1b0e8` in a fresh copy and fresh OS-isolated Ollama server. It completed **8 CLI commands and 10 actual Gemma generations**, plus explicitly labelled deterministic capability responses. Tag/digest and all original passage lines/hashes match. The server stopped normally; external networking was denied before and after the run. No model mocks, quote normalization, validator relaxation or expectation changes were used. [Actual records](chat-regression/) · [Network proof](chat-regression-isolation/) · [Detailed assessment](CHAT_REGRESSION_ASSESSMENT.json)

| Check | Result |
|---|---|
| Required exact capability prompts | PASS: accurate contract, zero retrieval/model calls. |
| Required real-model drafting and shortening | PASS: 99 to 42 words; three-step 5/20/5-minute plan retained. |
| Required assistance-game chat | **FAIL:** both attempts have invalid quotes or wrong passage associations; displayed response is a validation-failure abstention. |
| Unchanged H2 capability paraphrase | **PASS:** correctly includes `chat`, describes `review` as recording an inspected page's review, and `doctor` as model/device information. No invented tool ability or web access. |
| Unchanged H3 preference/interest question | **FAIL:** both attempts synthesize a multiline quotation without the original indentation; validator rejects it. This previously passed as ordinary grounded chat. |
| H3 explicit unrelated topic switch | PASS: three book-club name suggestions, no retrieval or citations. The full two-turn H3 journey is therefore only partial. |
| Chat-only codename search and independent ask | PASS: no matching original passage; ask explicitly abstains with zero chat history. |
| Representative B01 search/ask | PASS: Western/English skew and lack of consensus both supported with exact quotes; no chat history. |

The required source-chat failure initially assigns a correct goal quotation to an additional wrong known passage ID, changes quote characters, and combines hard-problem headings into a nonexistent multiline quote. Repair fixes the goal citation but retains fabricated quote spans. The H3 failure occurs with **zero conversation history**, so the problem cannot be attributed solely to irrelevant earlier chat. Both records retain raw initial and repair responses, validation errors and generation metrics. [Required source-chat record](chat-regression/required-chat/chat-06.json) · [H3 source record](chat-regression/heldout-chat/H3-topic-transition/chat-01.json)

Static comparison confirms the existing claim validator and generation function are unchanged; the research prompt is byte-identical. `ask` supplies no history, while source-dependent chat uses the same structured engine with a distinct prompt. The capability detector uses generic intent/command words and returns an accurate shared contract. No answer key enters generation. These integrity findings do not turn the failed model behavior into a pass. [Static comparison](chat-regression-static-review.json)

The earlier incorrect specific chat citation remains preserved in the documentation audit, and H2's earlier inaccurate capability answer remains preserved in the full-suite report. This targeted regression does **not** rerun or resolve B05's cross-source omissions or H4's missing coordination detail. Do not describe the earlier full independent suite as having been rerun on this core, or claim that the complete grounded-chat fix passed.
