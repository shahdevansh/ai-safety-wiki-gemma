# Evaluator B: requirement audit before the final real-model run

Status: **static and no-model checks complete; final real-model verdict pending**. This is an independent agent review, not a grade. Confidence is high for directly inspected code/files and executed checks; model behavior remains unassessed for this revision until the frozen suite runs.

## Scope and independence

The assignment was read from the newly supplied specification. The five original B cases remain fixed, including the previously failing two-source completeness case. Five fresh held-out cases were predeclared from assignment/source content before inspecting the goal revision. The evaluator already knew prior project behavior; this is independence of exact test wording/expectations, not evaluator blindness. No evaluator-A results were used to construct expectations. No model responses are substituted, mocked or inferred from static code.

`privacy-reconciliation.json` records the permitted source-alias and author-parenthetical edits. Questions, required claims and forbidden claims are identical to the original B design. The removed source career anecdote is irrelevant to all expectations. All fresh held-out passages remain exactly present; their original predeclaration file remains unchanged. Prior B files and failures are preserved privately outside this directory.

## Requirement-by-requirement assessment

| Assignment requirement | Current assessment and evidence | Remaining verification |
|---|---|---|
| Own CLI and connecting harness | PASS static: small Python standard-library harness; explicit parsing, retrieval, prompts, local generation, validation, persistence and errors. No ready-made document-chat app. | Final actual user journeys. |
| `help`, `ingest`, `chat`, `ask`, `search` | PASS implemented; top help directly executed under deny-all network. Literal source directory is accepted; unsupported directories give a useful error. | Full fresh ingestion and mode transcript in upcoming suite. |
| Local Gemma, exact identity and runtime | Implemented fixed Gemma tag and loopback endpoint; stored digest, metrics and request/response logging. Prior actual runs used Gemma. | Verify final records still contain required tag/digest and real calls. |
| Download/setup completed before isolation | Ollama launcher never downloads, refuses missing runtime and starts already-local weights. README draft supplies official model download command. | Fresh server run verifies availability without network. |
| Model/device fit and measurements | README draft identifies CPU, unified memory, quantization, context and output budgets; new device snapshot excludes serials. | Final timing/resource figures are explicitly placeholders until measured. |
| Smallest useful model rationale | Documented E2B choice with room for OS/apps; stored/effective parameter counts and unified-memory distinction. No unsupported larger-model comparison. | Tie rationale to final measured results, retaining limitations. |
| At least three source originals | Three frozen sanitized source files and manifest. Privacy preprocessing is disclosed. | Exact bytes checked through final run. These are not unchanged unredacted private originals. |
| Separate raw evidence from generated notes | PASS static: raw-only registration/index, wiki pages separate, tests/results outside vault, vault evidence writes rejected. | Independent index/source/hash checks after ingestion. |
| Actual model-generated wiki followed by review | Ingest produces six real model drafts with pending markers; review is explicit; prior curated pages inspected. | Final curated pages need restoration/review after forced demo, fresh hashes and checked reviewed re-ingestion. |
| Readable note names and headings | Inspected six coherent subject pages with two-to-four-word filenames, matching headings, useful Concepts/Governance folders. | Recheck final restored pages. |
| Topic index, source links, meaningful related links | Inspected topic descriptions, source catalog and explained related links. Existing graph is substantive rather than arbitrary connectivity. | Recheck all targets on final version. |
| Obsidian note/index/graph/screenshots | Six actual Obsidian screenshots independently viewed: readable note, index, graph, filter, catalog, original passage; no visible direct PII. | Catalog screenshot had prior lecture hash and must be recaptured after privacy edit. |
| Source path/line/ID fidelity | PASS executed on final data: deny-all search returned two passages; both exact source-line matches and SHA-256 matches. | All answer/retrieval records checked again in final run. |
| Local inspectable retrieval | PASS executed: FTS5 reindex builds eight original passages without a model; search succeeds when all sockets, including loopback, are denied. | Retrieval completeness evaluated separately for all frozen questions. |
| Chunk/context limits explained | README draft accurately explains roughly 1,500-character target, 3-line overlap, top 4 passages and topic-limited ingestion. | No further static gap identified. |
| Prospective three-answerable + missing-evidence set | Original B expectations include three principal answerable, one unsupported and one cross-source stress case; held-out expectations are immutable and timestamped. Root fixed set exists separately. | Actual semantic results must be reported without weakening cases. |
| Ask independent of chat | PASS static: fresh research messages; prior actual evidence showed no contamination. | Upcoming hypothetical chat-only location and independent asks test final version. |
| Ask grounded, neutral, cited or abstaining | Strict source-ID/quote checks and one bounded repair are intact. Attempts remain recorded. Generic completeness instructions contain no answer key. | Citation identity alone cannot certify entailment/completeness; manually assess every final case. |
| Chat personality and accurate capabilities | Separate persona and explicit capability contract; exact required prompts bypass model honestly and record zero calls. | Fresh paraphrase checks model-generated capabilities without relying only on exact regex. |
| Chat useful drafting, follow-up and selective retrieval | Generic routing distinguishes source questions/drafting; follow-up evidence is not automatically carried to unrelated topics. | Frozen held-out source-free domain draft and unrelated topic shift plus original shortening journey. |
| Chat history reset | PASS executed under deny-all: scripted `/reset` terminates correctly, both capability records have zero prior history and no generation/retrieval. | Real-model history follow-up remains in full suite. |
| Search without generation | PASS executed: no model calls and no synthesized answer. | Full-suite search/ask pairing. |
| No unsupported online fallback | PASS executed: `--mode online` rejected; answerable ask under deny-all gives real EPERM/local-model error, no fallback. | Final isolated model suite. |
| Fresh startup and offline full demo | OS wrapper starts a fresh model server, probes server and client before/after, preserves loopback for local inference. | Final B wrapper proofs and complete command records. Wi-Fi stays on by explicit user instruction. |
| Exact physical disconnection | INTENTIONAL DIFFERENCE: workload external networking is denied; host Wi-Fi remains on. README draft explicitly distinguishes this. | Do not claim a physically disconnected host or packet capture. |
| Re-ingestion idempotence | Code reuses intended filenames and preserves reviewed pages when current source hashes match. Earlier B runs passed unchanged bytes. | Fresh run checks unchanged generated pages; final root check must additionally prove reviewed edits persist. |
| Saved actual outputs and failures | Records retain requests/raw responses, retrieval/citations, attempts and metrics. Prior initial/schema/repair and B completeness failures are preserved. | Historical artifacts containing removed identifying context must be redacted and labelled, with private originals retained. |
| README as entry point and exact runnable commands | Intended README draft links code/wiki/questions/cards/modes/recording/privacy; commands correspond to implemented flags. macOS-only isolation scope explicit. | Fill only measured results; add ordinary server startup step and precise loopback wording; verify all final links. |
| One observed failure and proposed improvement | Earlier B05 omitted requested cross-source claims despite successful retrieval; this must remain visible even if final prompt improves coverage. | Current reflection must distinguish observed result, implemented generic fix and still-proposed improvements. |
| Private-data scrub | Direct-pattern and known-name scans did not find identifiers; a contextual career anecdote was discovered independently of regex and removed from source. | Clean 13 historical copied occurrences, reachable Git history and recaptured catalog screenshot. Repeat scans after packaging. |
| Public repository and signed-out access | INTENTIONAL USER OVERRIDE: remote verified PRIVATE. New README explicitly states authorized access needed; public access requirement is not met. | Final private-delivery record must not cite old anonymous access as current. |
| Portal submission | NOT PERFORMED. No receipt or submission claimed. | Owner must submit with suitable grader access; no tool action authorized here. |
| Optional online mode/web UI/training | Not required and appropriately omitted. Simplicity matches assignment scope. | None. |

## Concrete remaining issues communicated to the parent

1. Final actual-model evidence, current metrics and semantic review are pending; do not relabel historical results as current.
2. Removed identifying source context remains in historical generated copies and reachable prior Git objects until packaging cleanup. Preserve exact originals privately, publish only disclosed redacted derivatives, and rebuild clean reachable history before a scrubbed-snapshot claim.
3. The source-catalog screenshot displays the previous lecture hash and needs replacement after the data change.
4. The intended README should state how to start ordinary Ollama before bare model commands. The enforced launcher already supplies a complete alternative.
5. Sandbox policy permits all loopback; describe the harness's actual local Ollama use separately from policy scope.
6. Public repository/signed-out access and portal delivery are not satisfied. The former is intentionally overridden by the owner's private-repository request; the latter remains an unperformed user action.

No additional architecture or framework is needed to resolve these gaps. The principal remaining implementation question is whether actual small-model responses cover all requested aspects after the generic prompt/routing changes.

## Direct evidence in this directory

- `heldout-expectations.json` and SHA: unchanged prospective exact questions and passages.
- `expectations.json` and `privacy-reconciliation.json`: privacy-only derivative of original B expectations.
- `evaluator.py`: unchanged original question journeys, appended held-outs, explicit freeze assertions and no-model scripted reset.
- `nonmodel-assessment.json`: actual deny-all-network commands, output/errors, source fidelity and reset checks; zero model generations.
- `indirect-identifier-audit.json`: local inventory of historical copies requiring scrub, without reproducing the removed passage.
