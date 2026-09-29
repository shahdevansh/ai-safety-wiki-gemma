# Final chat regression — independent assessment

**The original required chat script passes, the checked ask remains grounded and independent, and the current source-chat citation is supported. The extra source-based shortening follow-up fails usability: both attempts fail quote validation and the displayed answer is a refusal. Suppressing an invalid citation does not make that follow-up pass.**

Confidence: **high** in these observed results. This is a bounded regression, separate from the earlier full-suite report; it does not erase earlier explanation or multipart-answer limitations.

## Frozen scope and execution

The run is `20260929T083154847468Z`, on harness SHA-256 `c40a2ff46ff488cf0d5fead68b7ecafb18142c7ff24cdee51b9e30b76ed1b0e8`. The research prompt and final source corpus are unchanged from the prior full run. The code now shares a structured per-claim citation validator and one bounded repair between ask and source-dependent chat; ordinary chat still uses the persona prompt. The [case plan](chat-regression-cases.json) and [freeze record](chat-regression-freeze.json) were saved before execution.

The original five-turn chat script was unchanged. The bounded suite also ran its existing chat-isolation ask, original A1, the exact previously failing lecture question, a source-based shortening follow-up, and reset. It rebuilt retrieval in a fresh whitelist copy without repeating ingestion. Original sources stayed unchanged. Actual local Gemma was used throughout: `gemma4:e2b-it-qat`, Q4_0, Ollama `0.34.4`, digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`.

## Required chat and ask checks

| Check | Verdict | Actual evidence |
|---|---|---|
| Both original capability prompts | **Pass** | Accurate local capabilities and all eight commands; no retrieval, irrelevant citations, or insufficient-evidence refusal. |
| Original invitation draft | **Pass** | 70 whitespace-delimited words, labeled Suggestion, coherent 30-minute agenda, no invented time/place/organizer. |
| Original “make that shorter” | **Pass** | Reduced the invitation to 51 words while retaining its purpose and agenda; used recent history without retrieval. |
| Fictional chat-only appointment | **Pass** | Treated as an explicit conversational suggestion; no source writes. |
| Independent ask about that appointment | **Pass** | Actual model abstention with no claims; actual research request contained no chat-only sentinel. |
| Original A1 assistance-game ask | **Pass** | Complete, neutral answer with quotes supporting the objective, uncertainty, and inference requirement. |
| Reset after the source conversation | **Pass** | Actual request had only the system prompt and current user turn, with zero history and no carried source passages. The answer did not recall the cleared discussion. |

Evidence: [original chat transcript](runs/20260929T083154847468Z/commands/chat-script.json), [isolation ask](runs/20260929T083154847468Z/records/ask-chat-isolation.md), [A1](runs/20260929T083154847468Z/records/ask-1-assistance-objective.md), and [post-reset answer](runs/20260929T083154847468Z/records/source-followup-reset/chat-04.md).

For A1, the **complete model request is identical** to the prior full run: system instructions, JSON evidence records, current question, schema, and options. Both requests contain exactly two messages. Their canonical JSON SHA-256 is `9a64045602b3742d35edfd1a7924572097f46846b80479c3ddbacc2e017f4816`. This verifies the intended ask request design for the checked case after the shared-helper refactor. [Comparison record](runs/20260929T083154847468Z/ask-request-comparison.json)

## Current source-chat citation assessment

The exact lecture question now retrieves original evidence and returns a structured, cited claim explaining that embedded chip safety checks would require a new fabrication facility to bypass. Independent agent review confirms that the exact quotation from its cited passage supports this claim. The source path, line range, hash, passage ID, and verbatim quote all match the original.

**Citation grounding passes for this response.** The prior unsupported comparison between malware costs and hardware security costs is absent. The displayed answer remains narrower than the prospective comparison expectation because it does not explicitly state the software-copying side. That is a coverage limitation, separate from the now-supported citation. [Actual source-chat response](runs/20260929T083154847468Z/records/source-followup-reset/chat-01.md)

## Extra source-follow-up failure

The next turn was “Make that explanation shorter.” The harness supplied two prior conversation messages and carried the original retrieved evidence, without doing a fresh search. The model returned quotes on both attempts that changed the source's literal Markdown spelling around the approximate cost expression. The validator correctly rejected those nonverbatim quotations; the repair repeated the error.

The actual displayed result was:

> Insufficient evidence: citation validation failed; inspect the saved raw Gemma response.

**This follow-up fails.** It did not deliver a shorter source-based explanation, despite the needed context being available. Its lower word count is the refusal's length and must not be counted as successful shortening. This is a quotation-format/validation failure, not genuinely missing source evidence. The raw attempts also expanded the source discussion instead of shortening the initial answer. Both attempts remain preserved. [Failed follow-up and raw attempts](runs/20260929T083154847468Z/records/source-followup-reset/chat-02.md)

## Timings and proof boundaries

| Operation | Attempts | Total generation time |
|---|---:|---:|
| Original A1 | 1 | 16.558 s |
| Chat-isolation ask | 1 | 8.905 s |
| Source lecture answer | 1 | 13.683 s |
| Failed source shortening | 2 | 33.759 s |
| Post-reset answer | 1 | 0.899 s |

The original five-turn chat script took 6.902 seconds of CLI wall time. The source conversation plus reset took 48.452 seconds. There were nine actual generations, including the unsuccessful repair; capability responses were supplied by the harness. [All-attempt audit](runs/20260929T083154847468Z/all-attempts-audit.json)

The approved wrapper freshly launched the isolated model server. Server and client probes verified external IPv4 TCP, IPv6 TCP, and UDP denial while loopback worked. Wi-Fi stayed on. The server stopped after the run, and the reserved port was released to the other evaluator. [Server proof](runs/20260929T083154847468Z/isolation/server-network.json), [client before](runs/20260929T083154847468Z/isolation/client-network-before.json), [client after](runs/20260929T083154847468Z/isolation/client-network-after.json), [completion](runs/20260929T083154847468Z/isolation/run.json).

The automatic result was 211/212 checks, with the follow-up validator check failing. Independent agent review additionally distinguishes a real shortened answer from a short refusal and notes incomplete comparative coverage in the first source answer. The automatic fraction is not an assignment grade. No additional model rerun replaced this failure, and the earlier full report and raw responses remain intact.
