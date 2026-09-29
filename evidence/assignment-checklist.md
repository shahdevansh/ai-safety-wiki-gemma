# Assignment requirements and delivery scope

This checklist refers to the current `goal-run` code/data revision. Older reports and recordings are development history; their privacy-redacted copies preserve failures, and their old hashes describe the original run.

| Requirement | Evidence and status |
|---|---|
| Own CLI/harness: help, ingest, chat, ask, search | [wiki.py](../wiki.py), [current recording/transcript](goal-run/), actual literal workshop search/ask examples. |
| Local Gemma and exact identity | Actual `gemma4:e2b-it-qat` requests with full digest, Ollama version and settings in every generation record. Internal runtime executable name does not change the Gemma weights into Llama. |
| Device fit, available capacity, memory and time | [Device snapshot](goal-device.json), [measurements](goal-measurements.json), [model-process samples](goal-isolation/resource-samples.json), README rationale and measurement boundaries. |
| Three original sources preserved | Three redacted source copies frozen before final tests, checked against [manifest](../source-manifest.json). Private originals remain outside Git. Privacy preprocessing is disclosed. |
| Generated and reviewed linked wiki | Six actual local-model drafts, then editorial correction against originals; [review hashes](goal-editorial-review.json), [final vault check](goal-vault-check.json), [reviewed re-ingestion](goal-reviewed-reingest.json). |
| Readable filenames, headings, page list, graph and meaningful links | Concepts/Governance folders, matching headings, source references and explained related links; [Obsidian screenshots/navigation](obsidian/README.md). Source catalog screenshot matches final hashes. |
| Raw-only retrieval | Eight passages from three registered raw files. Generated wiki pages, chat, expectations, prompts and evidence outputs are excluded. Passage text, paths and line ranges are independently checked. |
| Three answerable asks and one unsupported ask | Four fixed prospective expectations and [current semantic assessment](GOAL-REVIEW.md), with actual retrieved passages, answers, citations and failures. |
| Chat capabilities, conversation follow-up, note citations, source search, chat/ask separation | [Recorded checks](goal-run/terminal.txt), [search](goal-run/search.json), [separate codename ask](goal-run/chat-isolation.json); independent additional stress cases and limitations are disclosed. |
| Search without model | [Actual deny-all-network test](goal-no-model/assessment.json) succeeds for reindex/search; answerable ask fails usefully without local model access or fallback. |
| Offline ingestion and tests after fresh startup | [New server/client probes and run status](goal-isolation/), IPv4/IPv6/UDP denial, successful loopback control, before/after checks, inherited OS policy. Host Wi-Fi remains on by explicit user instruction. |
| Actual saved outputs and recording | Asciicast, standalone HTML replay, full plain transcript, Markdown cards and JSON containing original requests/responses; all current and historical failures are disclosed. |
| README entrypoint and exact setup/commands | [README](../README.md); entrypoint links and vault integrity checked by publication_check.py. |
| Independent evaluation | Two agents independently authored/froze questions, ran actual isolated local Gemma, checked source support and wrote [reports](independent/README.md). Additional failures are not relabelled as passes. |
| PII/account scrubbing | [Redaction scope](privacy/redaction-report.json), [historical-export redactions](privacy/context-redactions.json), [text/reachable-history audit](privacy/audit.json), visually reviewed screenshots, fresh sanitized Git history. No universal guarantee about contextual inference is asserted. |
| Public repository and signed-out accessibility | **Intentionally overridden by the user's private-repository instruction.** [Private delivery verification](private-delivery.json). Authorized access is required; historic public-access receipts do not describe the current state. |
| Course portal | **Not submitted.** This handoff delivers the verified private repository. No portal receipt or grader-access approval is claimed. |

The demonstrated required tests and independently observed limitations are reported separately. These are evidence-backed execution checks, not an asserted course grade or a claim of universal answer reliability.
