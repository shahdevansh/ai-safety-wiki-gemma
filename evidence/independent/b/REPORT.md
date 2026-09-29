# Independent evaluator B — completed runtime review

**Result:** all four principal research tests pass: three answerable questions produce supported cited answers, and the missing-evidence question abstains. The additional two-source stress case is **PARTIAL** because it omits expected points despite retrieving them. Confidence is **high for these observed tests**, **moderate for similar questions**, and **unknown for broad reliability**.

## Independence and execution scope

Questions, expected claims and verbatim source passages were frozen in [expectations.json](expectations.json) before reading implementation or README. The [hash](expectations.sha256) remains unchanged. Only assignment and original-source contents informed question selection. Directory inventory exposed earlier evidence filenames but no existing evaluation contents were read. No evaluator A outputs were read. No harness or source files were edited by this evaluator, and no stubs or alternative models were used.

Privacy cleanup renamed one raw source. [Reconciliation](privacy-source-reconciliation.json) verifies that every frozen expected technical passage remains byte-for-byte present under the disclosed alias. Test intent and expected answers were not changed after observing results.

The evaluator copied only code, prompts, catalog and raw sources into its own clean [workspace](isolated-first/workspace/), initially with no index or wiki pages. All expectations and output records remained outside the searchable vault. There were **24 main CLI commands, 2 direct deny-all checks, and 1 fresh-server restart check**. The CLI and real Ollama server were both OS-isolated from external networking while loopback remained available. This is **process-level external-network denial**, not physical Wi-Fi disconnection; Wi-Fi stayed on.

Actual model: **gemma4:e2b-it-qat**, **Q4_0**, Ollama **0.34.4**, digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`. All **19 actual generations** used this model at the isolated loopback endpoint. Two capability responses came from the explicitly labelled deterministic harness contract and are not counted as model generations.

## Fixed research results

| Case | Retrieval | Answer and citation assessment |
|---|---|---|
| [B01: value-alignment obstacles](isolated-first/records/B01-values.md) | PASS | PASS: Western/English skew and lack of consensus; both exact quotes support the claims. |
| [B02: mountaintop paraphrase](isolated-first/records/B02-mountaintop.md) | PASS | PASS: agency matters beyond outcome, and removing non-optimal choices violates autonomy. |
| [B03: ICAO/IMO versus IAEA](isolated-first/records/B03-oversight.md) | PASS | PASS: regulator oversight versus direct inspection; stronger powers are politically harder. It answers what the notes say, without asserting enacted AI inspection law. |
| [B04: next-workshop schedule](isolated-first/records/B04-next-workshop.md) | Expected absence | PASS: explicitly insufficient evidence; no invented date, time or room. |
| [B05: cultural skew plus preference manipulation](isolated-first/records/B05-two-source.md) | PASS, both sources | PARTIAL: every generated claim is grounded, but lack of consensus and conflicting interests among multiple humans are omitted despite appearing in retrieved context. |

This separates retrieval success from answer completeness. B05 is not a citation failure or hallucination; it is a failure to cover the full independently frozen expectation. No setting was changed and no favorable replacement result was substituted. [Claim-by-claim assessments](semantic-assessment.json) preserve the distinction.

## Mode boundaries and persistence

- Both exact capability checks pass without retrieval, unrelated citations, or an insufficient-evidence response. They accurately describe supported capabilities and limitations.
- Real Gemma drafting and `make that shorter` pass. Output falls from **98 to 43 words**, retains extract/condense/structure for a one-page guide, labels the proposal Suggestion, and skips retrieval. [Chat records](isolated-first/chat/)
- Notes chat retrieves originals and gives supporting citation IDs. Its second broad obstacle is reward-model limitations rather than the Western/English-skew point used by the fixed ask; this is a framing/completeness observation, not a retroactively invented test failure.
- An explicitly hypothetical date/time/room inserted only into chat does not become source evidence. The subsequent standalone ask abstains, and searching the distinctive room label returns no passages. [Separation evidence](isolated-first/records/B04-after-chat.md)
- Exact assignment-style `search "workshop location"` returns original passages with no synthesized answer; `ask "Where is the workshop?" --mode local` correctly abstains for this corpus.
- Search succeeds under an OS profile denying **all networking including loopback**, returning two exact original passages with zero model calls. Ask under the same profile fails with a useful local-Ollama-unavailable/EPERM error and no cloud fallback. [Direct denial assessment](no-model-direct/assessment.json)
- Initial missing-index search, missing ingestion directory, and unsupported online mode each produce explicit errors. These intentional negative outcomes are retained in [command logs](isolated-first/commands/).
- Fresh `ingest ./vault/raw` makes six readable notes and an eight-passage index using six real generations, in **25.994 seconds**. [Ingestion](isolated-first/records/fresh-ingest.md)
- Re-ingestion makes no model calls, creates no duplicates, leaves all original bytes and all six note bytes unchanged, and preserves the same note paths. [Hash audit](isolated-first/reingestion-assessment.json)
- All six filenames are readable and match their first headings; internal/source links resolve unambiguously, topic index and source catalog exist, and machine files remain outside the vault. Freshly generated pages are correctly pending review; this test does not pretend generation itself supplies editorial review.
- Fresh CLI processes read the persisted index successfully. A second isolated model server with a different PID loads the local weights and reproduces B01's grounded answer using the same persisted workspace. Both servers are stopped afterward and port 11435 was verified closed. [Restart response](isolated-first/restart-check/records/B01-after-server-restart.md)

## Offline proof and measurements

The first and restart launches preserve server-side probes, client probes before/after, sandbox-profile hashes and fresh-server lifecycle records: [first run](isolation-first/) and [restart](isolation-restart/). External probes fail with EPERM; loopback succeeds. The evaluator also independently required IPv4/IPv6 TCP/UDP denial before inference. [Inherited-policy check](isolated-first/inherited-isolation-check.json)

Model calls report local identity, digest, prompts, raw responses, token counts and timing. Across 9 actual asks, recorded model-call latency spans **7.367–19.662 seconds**, median **14.139 seconds**. These are sequential observations, not a controlled performance benchmark. The restarted answer reports a **3,734,492,937-byte runtime model allocation** at 8,192 context. Process RSS is unavailable inside this sandbox and should not be reported as a measured value for this run. Runtime allocation is not total application or peak unified-memory use.

## Assignment and README audit boundaries

The runtime portions independently verified here cover local Gemma, fresh ingestion, separate modes, original-source retrieval/citation fidelity, three supported asks, one unsupported ask, source isolation, re-ingestion and restart persistence. Installation/download of Ollama and weights was not repeated; local availability was tested under external-network denial.

The README read after expectation freeze was still an older working draft. It contained a stale renamed source link, old unchanged-originals/provenance wording, a fixed-port claim, prior resource measurements, and pending Wi-Fi-disconnection language. The parent is rewriting it; those observations are not claims about its eventual final version. Final documentation must distinguish sanitized source baselines from historical originals and process isolation from physical disconnection, link this run's evidence, and include B05's observed limitation.

Existing screenshots, prior evals, prior evidence cards and evaluator A's results were deliberately not used in this independent evaluation. Consequently **current Obsidian GUI navigation/screenshots, final README link integrity, signed-out public-repository accessibility and portal submission are not certified by this report**. No publication or submission occurred in this evaluator.

One observed ingestion limitation remains visible: the fresh Alignment and Interpretability draft omits the requested Useful details section and phrases the individual-alignment point awkwardly. Other generated drafts sometimes present discussion claims as declarative statements. The pages remain pending review, appropriately; editorial checking is still required before treating these fresh drafts as final wiki notes.

A concrete next improvement is to test answer coverage against each requested subquestion, alongside existing citation checks. B05 demonstrates why quote-valid claims alone do not ensure a complete answer. Evaluate such a change on this unchanged test and additional held-out cases, preserving the initial partial result.
