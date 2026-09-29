# Independent evaluator A — actual Gemma run

The tested harness completes ingestion, source search, ordinary chat, conversational revision, and independent cited research with local Gemma under OS-enforced external-network denial. Two factual answers were complete and directly grounded. The third was grounded but incomplete. The unsupported question and chat-to-ask isolation test both produced explicit abstentions from Gemma itself. Fresh generated wiki drafts still require substantive human review.

**Confidence:** high in the observed command behavior, source integrity, citation identity, and process-level network isolation; moderate in the completeness of the third factual answer. No overall assignment grade is inferred from the automatic check count.

## Independence and reproducibility

The [prospective plan](test_plan.md) and [fixed cases](cases.json) were written before the real-model run, using only the assignment, harness, separate prompts, and originals. Existing submission evaluations and other evaluators' results were not consulted. The only later expectation adjustment accepted was a disclosed privacy-only source-path rename; the technical questions and expected excerpts stayed fixed.

The evaluator made a fresh whitelist copy of the sanitized frozen harness, prompts, source catalog, and three originals. It excluded existing wiki pages, state, evidence, and answer keys. All test-state and generated files were written in that copy. The frozen originals and execution originals retained identical SHA-256 hashes throughout. The [input manifest](runs/20260929T072034705632Z/frozen-input-manifest.json), [harness manifest](runs/20260929T072034705632Z/harness-manifest.json), and [prespecified original excerpts](runs/20260929T072034705632Z/expected-original-passages.json) identify exactly what was tested.

This report uses portable relative links and sanitized source names. Raw local command logs preserve absolute execution paths for reproducibility; they should be privacy-reviewed before public distribution.

## Actual model and isolation

All 14 generation calls requested and returned `gemma4:e2b-it-qat`, family `gemma4`, GGUF `Q4_0`, running through Ollama `0.34.4` at `http://127.0.0.1:11435`. Digest:

```text
07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c
```

Runtime metadata reports `parameter_size: 4.6B`; the model identifier is E2B, not a claim that total stored parameters equal two billion. Recorded generation settings were an 8,192-token context, temperature 0, seed 42, and the harness's mode-specific output limits. Capabilities responses came from the harness contract with zero generation calls; they are interface tests, not additional Gemma generations.

The approved wrapper launched a fresh Ollama daemon and the evaluator/CLI process tree under the same loopback-only macOS sandbox. The server performed network probes before `exec` into Ollama. Client probes ran before and after the test. External IPv4 TCP, IPv6 TCP, and IPv4 UDP operations received `EPERM`; local IPC succeeded. Wi-Fi remained **on**. The demonstrated property is denied external network access for the tested processes, not physical disconnection of the computer.

Evidence: [server probe](runs/20260929T072034705632Z/isolation/server-network.json), [client before](runs/20260929T072034705632Z/isolation/client-network-before.json), [client after](runs/20260929T072034705632Z/isolation/client-network-after.json), [wrapper completion](runs/20260929T072034705632Z/isolation/run.json), and [actual sandbox profile](runs/20260929T072034705632Z/isolation/no-external-network.sb). The isolated server was stopped when the run finished. No model rerun was used to replace an answer.

## Four independent research tests

| Test | Retrieval | Actual answer assessment | Citation semantics |
|---|---|---|---|
| Assistance-game objective and uncertainty | Expected original and full supporting statement retrieved. | **Complete.** States that the goal is promoting human interests, uncertainty concerns those interests, and they must be inferred. Does not invent practical convergence. | Both material claims follow directly from quoted text. Two overlapping chunks contain the same statement, producing duplicate citations to one original. This is repetition, not independent corroboration. |
| Three safeguards for human intervention | All three source proposals retrieved. | **Complete.** Lists physical fail-safes with human override, multiple humans in decision loops, and physical shutdown buttons/levers. Its framing attributes them to the meeting notes, and the question supplies their proposed status. It does not claim deployment or proven effectiveness. | Each of the three list items has the corresponding exact source quote. |
| Why alignment and interpretability are two sides of one objective | The expected original, including the internals rationale and direction/method analogy, was retrieved. | **Partial completeness; no unsupported material claim.** It repeats that they are two sides of one objective, then says understanding them provides direction and method. It omits the explicit reason that alignment is hard without understanding model internals. The phrase “these aspects” is vague. | Both claims have relevant exact quotations. “Method” is a reasonable paraphrase of “how to get there,” so the automatic keyword failure is not a citation or factual failure. The omitted causal detail is a separate answer-quality limitation. |
| Exact date of the next infrastructure workshop | Related source material retrieved, with no supporting schedule. | **Correct abstention.** Displays “Insufficient evidence: the provided sources do not answer this question.” | Raw Gemma JSON is `{"insufficient_evidence": true, "claims": []}`. This was not an error fallback or a citation-validation refusal. |

Full actual answer, prompt, original passages, quote/claim mapping, model identity, and timing are saved in [Test 1](runs/20260929T072034705632Z/records/ask-1-assistance-objective.md), [Test 2](runs/20260929T072034705632Z/records/ask-2-infrastructure-controls.md), [Test 3](runs/20260929T072034705632Z/records/ask-3-alignment-interpretability.md), and [Test 4](runs/20260929T072034705632Z/records/ask-4-unsupported-schedule.md). A separate search preceded each ask; those records remain alongside the answers.

For every returned passage, this evaluator checked the literal original line range and source hash. For every ask citation, it checked the supplied passage ID, exact quote, displayed citation, and claim. Human review then compared the material claims with their quotations and surrounding original source. Quote validation alone would not establish semantic support; the harness correctly describes that limitation.

## CLI and mode checks

- **Help and literal ingestion:** `--help`, `help`, `ingest --help`, and the literal assignment form `ingest ./vault/raw` succeeded. Clean ingestion made six actual Gemma calls and generated six subject-named notes. It did not reuse an existing wiki. [Initial ingestion](runs/20260929T072034705632Z/records/ingest-initial.md)
- **Re-ingestion:** A second ingestion preserved the six note filenames and bytes and made zero generation calls. The three originals remained unchanged. This verifies idempotence for unchanged sources; it does not establish behavior for edited originals. [Repeat record](runs/20260929T072034705632Z/records/ingest-repeat.json)
- **Wiki structure:** All six generated filenames matched their first headings. All 36 checked wiki/index/catalog internal links resolved to exactly one Markdown target. This is a file-level link check, not an Obsidian click-through or visual review. [Supplemental audit](runs/20260929T072034705632Z/supplemental-audit.json)
- **Capabilities:** Both exact prompts, “what can we do?” and “what can you help me with?”, described the real local assistant and modes, suggested a starting point, made no retrieval calls, returned no citations, and did not refuse for insufficient evidence. [Chat transcript records](runs/20260929T072034705632Z/commands/chat-script.txt)
- **Draft and follow-up:** The suggested invitation included a coherent 30-minute agenda and no invented time, place, organizer, or confirmed event. `make that shorter` retained the invitation and agenda using chat history, with no retrieval. Whitespace-delimited word count fell from **69 to 49**. The initial draft therefore missed the requested 70–90-word minimum by one word; shortening itself worked. Both outputs were labeled “Suggestion.”
- **Original search:** Search returned exact source passages and locations, without a synthesized answer or model call. [Search record](runs/20260929T072034705632Z/records/search-original.md)
- **Search with no network/model access:** The first auxiliary attempt failed before reaching the CLI because macOS rejected a nested `sandbox-exec` invocation: `sandbox_apply: Operation not permitted`, exit 71. That failed attempt is [preserved](runs/20260929T072034705632Z/commands/search-model-unavailable.json). A separately authorized direct host launch under the deny-all-network profile then succeeded in **0.070 seconds**, returned four original passages, and made zero model calls. No model daemon was started for this retry. [Direct retry](runs/20260929T072034705632Z/commands/search-model-unavailable-direct.json), [result](runs/20260929T072034705632Z/records/search-model-unavailable-direct.md)
- **Chat-to-ask isolation:** Chat received an explicitly fictional appointment with a sentinel time and room. The subsequent standalone ask returned insufficient evidence. Its actual model request contained only the research system instruction and current evidence/question, with neither sentinel. The original sources stayed unchanged. This is evidence for this explicit isolation case, not a universal proof against every possible leakage mechanism. [Actual independent ask](runs/20260929T072034705632Z/records/ask-chat-isolation.md)

## Fresh wiki drafts: defects requiring review

These findings concern the newly generated, `review_status: pending` pages in the evaluator's copy. They do not establish the condition of previously reviewed submission pages, which this independent evaluator did not read.

1. **Meaning drift in process reward models.** [Alignment and Interpretability](runs/20260929T072034705632Z/project/vault/wiki/Concepts/Alignment%20and%20Interpretability.md) changes the source's “limited to math” into “limited to mathematical representations.” A restriction to a problem domain is not the same as a restriction on representation. The draft also omits the requested `Useful details` section entirely.
2. **Reasons conflated.** The [Assistance Games](runs/20260929T072034705632Z/project/vault/wiki/Concepts/Assistance%20Games.md) introduction associates both “preference” and “values” with susceptibility to manipulation, blurring the original's separate reasons: culture-war reactions for “values,” manipulation for stated preferences. The subsequent bullet partly recovers the distinction, but the introduction remains misleading. The draft also contains six detail bullets despite the requested three to five.
3. **Attribution not consistently retained.** Several generated drafts present the meeting notes' technical or institutional assertions directly, despite instructions to attribute discussion claims. Examples include transformer capability limits, global malware cost, and AI's claimed lack of physical-world access. The original source reference makes them traceable, but does not by itself make these claims independently established. A reviewer should qualify the summary bodies.
4. **Length control is only advisory.** [Compute Governance](runs/20260929T072034705632Z/project/vault/wiki/Governance/Compute%20Governance.md) contains **234 whitespace-delimited body words**, excluding the title and harness-added source/related links, despite an under-220-word prompt. The harness did not reject or shorten it. This is a formatting limitation, separate from the semantic issues above.

A concrete improvement is to validate summary structure and length before saving a draft, while retaining the first failed output; then use a human review checklist to catch claim strengthening, attribution loss, and meaning drift. For research answers, a completeness review should check each requested component against the retrieved supporting passage. Automatically detecting authentic quotations is insufficient for either task.

## Observed timings and memory boundaries

| Operation | Measured elapsed time |
|---|---:|
| Clean six-note ingestion, CLI wall time | 26.764 s |
| Unchanged re-ingestion, CLI wall time | 0.106 s |
| Test 1 Gemma call | 16.674 s |
| Test 2 Gemma call | 13.774 s |
| Test 3 Gemma call | 12.646 s |
| Unsupported question Gemma call | 5.206 s |
| Chat-to-ask isolation Gemma call | 5.336 s |
| Five-turn chat session, CLI wall time | 6.106 s |

These are one observed run, not a benchmark distribution. The run spans about 88 seconds between the client pre/post network probes.

For Test 1, the recorded CLI peak RSS was **20,217,856 bytes**. Ollama's `/api/ps` reported a loaded allocation of **3,734,492,937 bytes**, also reported as `size_vram`, with context length 8,192. That runtime-reported allocation is not a measured system-wide peak. `runtime_rss_after` was `{"available": false}` in this record, so this run supplies no after-call process-RSS observation for the model daemon. The reason for that unavailable measurement was not established here. [Raw metrics](runs/20260929T072034705632Z/records/ask-1-assistance-objective.json)

## What these results do and do not establish

The untouched automatic output recorded **303 of 305 checks** passing. The two failed checks were the narrow keyword triage and the nested-sandbox launch described above. The direct search retry resolves the latter behavior check; it does not erase the earlier execution failure. Manual review additionally found the incomplete third answer, the one-word drafting miss, and the unreviewed wiki defects. An automatic fraction is therefore a poor summary of deliverable quality.

These tests establish a working local Gemma CLI workflow on the frozen sanitized corpus, with traceable original passages and observed mode separation. They do not verify required Obsidian screenshots or actual UI navigation, the condition of the submission's reviewed wiki, comprehensive semantic validity of every source claim, total peak model/unified memory, public repository accessibility, or a course-portal submission. Those items require their own evidence. No publication or external communication was performed by this evaluator.

Two additional code-derived gaps remain distinct from observed failures. First, chat decides whether to retrieve using a fixed vocabulary regex; note-dependent paraphrases outside that vocabulary are not covered by these conversational cases. Second, chat rejects unknown citation IDs but does not enforce that every note-based material claim has a citation or that the cited passage supports it. The stricter ask quote checks do not automatically extend to chat. A future notes-based chat test should inspect those behaviors explicitly. This evaluation does not claim to have demonstrated a live failure for either gap.
