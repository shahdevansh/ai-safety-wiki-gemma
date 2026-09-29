# AI Safety Wiki — local Gemma and RAG

**Pip** is a personal wiki CLI built from three anonymized AI safety meeting-summary exports. It provides conversational `chat`, independent factual `ask`, original-passage `search`, and local-model `ingest`. The custom [Python harness](wiki.py) connects instructions, retrieval, conversation, Gemma, citations, errors and saved outputs. RAG supplies context at inference time; it does not train the model.

**Delivery:** this repository is private at the owner's explicit request. That overrides the assignment's public/signed-out-access requirement; authorized GitHub access is needed. Course-portal submission is not claimed. All model demonstrations run with OS-enforced denial of external network access while host Wi-Fi remains on, as requested. Local loopback connects the CLI to Ollama. This is workload isolation, not evidence of physically disabling Wi-Fi or blocking other applications.

## Start here

- [Wiki index](vault/index.md), [source catalog](vault/Source%20Catalog.md), [three frozen sources](vault/raw), [six reviewed notes](vault/wiki).
- [Harness code](wiki.py), [mode instructions](prompts), [prospective four-question design](evals/design.md), [fixed expectations](evals/cases.json).
- [Current terminal recording](evidence/goal-run/terminal.cast), [self-contained replay](evidence/goal-run/terminal.html), [transcript](evidence/goal-run/terminal.txt), [current review](evidence/GOAL-REVIEW.md).
- [Independent reports and original failures](evidence/independent/README.md), [Obsidian screenshots and navigation](evidence/obsidian/README.md), [requirement checklist](evidence/assignment-checklist.md).
- [Network-enforcement evidence](evidence/goal-isolation), [privacy audit](evidence/privacy/audit.json), [private-delivery verification](evidence/private-delivery.json).

The HTML recording has no external resources. Download it and open it locally; GitHub normally displays HTML source rather than executing it. Earlier directories named `assignment-run` or reports titled “final” describe the earlier revision; the **goal-run** evidence and linked current review supersede them without hiding their failures.

## Setup and exact commands

Tested dependencies: **Python 3.9.6** with SQLite FTS5, **Ollama 0.34.4**, macOS 26.6.2. The harness uses the Python standard library only. No pip packages, hosted embeddings or API key are required. Obsidian is needed to inspect the vault, not to run the CLI. The isolation launcher requires macOS `/usr/bin/sandbox-exec` and refuses a weaker fallback.

While online, install [Ollama](https://ollama.com/download) and download the exact [Gemma tag](https://ollama.com/library/gemma4/tags):

```bash
ollama pull gemma4:e2b-it-qat
ollama --version
ollama list
python3 --version
```

Clone this private repository with an authorized GitHub account, then run all commands from its root. Weights stay in Ollama's local model store and are not committed. This project does not install or download anything during inference.

Verify the full downloaded model digest with `./wiki doctor` (after starting the local service) against the digest below; tags can change. The implemented assignment examples are:

```bash
./wiki --help
./wiki help
./wiki ingest ./vault/raw --mode local
./wiki search "workshop location"
./wiki ask "Where is the workshop?" --mode local
./wiki chat
```

In chat, type `what can we do?`, `what can you help me with?`, `Draft a three-step study plan.`, then `make that shorter`. `/reset` clears the session; `/exit` ends it. The example workshop-location query correctly finds no recorded location; `ask` must report insufficient evidence. Useful corpus queries include `physical fail-safes human override` and `What is the assistance-game AI uncertain about?`.

Bare commands use an existing local Ollama service on `127.0.0.1:11434`; they do not themselves install an OS network policy. If that service is not running, start `OLLAMA_NO_CLOUD=1 ollama serve` in another terminal, or use the launcher below, which starts its own server. For **enforced offline execution**, use the launcher. It starts a new isolated server on port 11435, runs the command under the same policy, then stops only that server. Your usual Ollama service is untouched:

```bash
python3 scripts/local_only.py --evidence-dir .state/chat-isolation -- ./wiki chat
python3 scripts/local_only.py --evidence-dir .state/ask-isolation -- ./wiki ask "What physical controls did the workshop propose?" --mode local
```

Run the complete demonstration in a new evidence directory:

```bash
python3 scripts/record_terminal.py evidence/new-run/terminal.cast python3 scripts/local_only.py --evidence-dir evidence/new-isolation -- bash scripts/assignment_demo.sh evidence/new-run
```

This forces six real local Gemma ingestion generations, runs all four fixed asks, the chat/search checks, literal example commands and re-ingestion. It leaves generated pages marked **pending review**. Open each generated note beside its original, correct omissions or misleading claims, then explicitly record the review and validate:

```bash
./wiki review "Assistance Games"
./wiki review "Alignment and Interpretability"
./wiki review "Transformer Safety Limits"
./wiki review "Compute Governance"
./wiki review "Human Control and Defenses"
./wiki review "Power and Disempowerment"
python3 scripts/verify_vault.py
```

`review` records your inspection; it cannot perform semantic review for you. Ordinary `ingest` preserves existing pages when source hashes are unchanged. `--force` regenerates drafts and backs up prior pages in ignored `.state/note-backups`. A clean clone bootstraps the reviewed-page manifest from the included notes; use `--force` only when you actually want to regenerate.

Search requires an index but no model. Rebuild and run with **all network operations, including loopback, denied**:

```bash
./wiki reindex
/usr/bin/sandbox-exec -f isolation/no-network-at-all.sb ./wiki search "physical fail-safes human override"
```

`--save evidence/example.json` on ask/search/ingest saves JSON plus a Markdown evidence card. `./wiki chat --script evals/chat.txt --save-dir evidence/chat-example` replays explicit turns. Without a save path, outputs remain in ignored `.state/runs`. Evidence writes inside the vault are rejected. Missing sources, stale indexes, unavailable local models and invalid citations produce useful errors; there is no cloud fallback.

## Sources, wiki and privacy

The three sources cover an alignment lecture, an alignment/interpretability session and a risk/defenses workshop. They are existing **AI-generated meeting-summary exports**, not verbatim transcripts or independently validated scientific references. Names, account paths, private meeting links/IDs, dates, biographies, personal follow-ups and an identifying career anecdote were removed before the final source corpus was frozen. Private originals remain outside this repository. The submitted redacted copies are preserved byte-for-byte through ingestion and tests, verified against [source-manifest.json](source-manifest.json); they are not claimed to match unredacted originals.

Six notes cover assistance games, alignment/interpretability, transformer safety limits, compute governance, human controls, and disempowerment. Actual filenames contain two to four natural words, matching their first heading. `Concepts/` and `Governance/` supply useful browsing groups. Each note has a coherent subject, traceable source link, and related links with explanations. Source IDs and hashes live in metadata/catalogs; passages and evaluation outputs stay outside the vault.

Open **`vault/` itself** in Obsidian. [Screenshots](evidence/obsidian/README.md) show the reviewed note, topic index/page list, source catalog, original passage, and graph filtered to `path:wiki/` with attachments hidden. The recorded navigation follows an index entry through a related note to its source. Editorial review checks summaries against these notes; it does not establish that the notes' scientific claims are true.

[Privacy records](evidence/privacy) disclose the redaction categories and historical-export transformations. Earlier actual outputs remain as disclosed redacted copies; unredacted originals remain privately archived. Their old source IDs/hashes describe their original run, not the later redacted bytes. Final results use the current source manifest. Text and reachable Git content are scanned for account paths, contact details, private links, credentials and a private identifier denylist; screenshots are reviewed visually. These checks cannot prove that no reader could infer an identity from topic context.

## Model, retrieval and harness

| Component | Role |
|---|---|
| Gemma | Generates from the messages supplied to it; cannot automatically read files or operate tools. |
| Retrieval | SQLite FTS5 with Porter stemming and BM25 over registered raw sources only. Eight deduplicated contiguous passages, target roughly 1,500 characters, three-line overlap. Returns path, lines and content-derived passage ID. |
| RAG | Ask sends at most four retrieved passages (roughly 6,000 characters) with explicit research instructions. It does not train Gemma or index expected answers. |
| CLI | Parses `chat`, `ask`, `search`, `ingest`, `help` and supporting review/reindex/doctor commands. Local execution is the only mode. |
| Harness | Chooses instructions, history and retrieval; calls Gemma, validates citations, handles errors and saves evidence. |

**Chat** uses [Pip's persona](prompts/persona.md) and the last eight history messages. Capability requests, including generic requests to list supported commands, return an accurate [harness capability contract](prompts/capabilities.md), explicitly recorded as zero model calls. Ordinary drafting and conversation use Gemma. A small intent heuristic retrieves for source-dependent questions and explicit requests to use notes; source-free drafting skips retrieval. Original evidence is carried only for referential follow-ups, with explicit topic switches clearing it. Chat suggestions are labelled; personal facts are not automatically saved. Source-dependent chat uses separate grounded-chat instructions and a JSON Schema of original line IDs. Gemma selects supporting line IDs; the harness attaches each line’s exact original text, passage ID and location, then runs the shared claim/quote validator and bounded repair. Raw selections and the line catalog are saved. This avoids model copying errors; it does not prove that the selected line entails the claim. Conversation may resolve references but cannot serve as source evidence. Semantic correctness still requires review. Heuristic routing and model-generated prose are limitations, not universal guarantees.

**Ask** always starts with fresh research context and zero chat messages. It loads [research rules](prompts/research.md), asks for every supported part of the question, and requires material claims with exact source IDs and verbatim supporting quotations. Unknown IDs or quotations absent from the indicated passage fail validation. One bounded citation-repair attempt may use the unchanged evidence and error messages; the initial output and both attempts remain saved. An uncorrected citation failure yields insufficient evidence. Valid quote identity does not establish entailment or answer completeness, which are reviewed separately.

**Search** stops after original retrieval and never calls Gemma. **Ingest** sends each registered source's topic sections (maximum 20,000 characters) with [ingestion instructions](prompts/ingest.md), writes a draft, adds provenance/related links and rebuilds the source-only index. Filenames come from the [six-topic/source mapping](sources.json); repeated ingestion reuses paths and preserves reviewed edits when source hashes match.

Trace `./wiki ask "What physical controls did the workshop propose?"`: argument parsing → source-hash freshness check → FTS5 retrieval → JSON evidence records with path/line/ID boundaries → new research prompt without chat → loopback Ollama request → claim/quote validation and optional bounded repair → displayed cited answer → JSON/Markdown evidence. Requests, raw model responses, retrieved text, validation errors, identity and timing are retained.

## Device and measured run

| Item | Configuration |
|---|---|
| Model | `gemma4:e2b-it-qat` |
| Digest | `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c` |
| Format | GGUF, Q4_0; quantization-aware-trained tag |
| Size | E2B effective; runtime reports 4.6B stored parameters including extra embeddings |
| Model disk bytes | 4,336,358,185 (4.04 GiB) |
| Runtime/device | Ollama 0.34.4, Apple Metal; Apple M3 Pro, macOS 26.6.2 |
| Memory | 36 GiB unified CPU/GPU memory; no separate dedicated VRAM |
| Settings | 8,192 context tokens, temperature 0, seed 42; ask and grounded chat 2,400 output tokens with reasoning/JSON Schema; ordinary chat 650; ingestion 600 |

This small quantized Gemma leaves room for the OS and other applications and completed ingestion/research on the actual device. E2B's effective count is not its stored-memory footprint. No larger model comparison is claimed. Official background: [Gemma documentation](https://ai.google.dev/gemma/docs/core) and [Ollama model tags](https://ollama.com/library/gemma4/tags). Ollama is a runtime, not a substitute Llama model: its internal executable may be called `llama-server`, but the measured weights are Gemma. No simulated answers substitute for actual model evidence.

The current [device snapshot](evidence/goal-device.json) recorded **12.28 GiB free disk**, 2.02 GiB free RAM, 10.50 GiB inactive RAM and 1.55 GiB speculative RAM. macOS `memory_pressure -Q` reported 73% system-wide memory free; this OS indicator and the page categories have different meanings and are not a guaranteed single available-memory allocation. The [snapshot script](scripts/device_snapshot.py) makes those measurements reproducible.

| Current operation | Observed time |
|---|---:|
| Six-note ingestion, whole operation | 36.710 s |
| Six ingestion generation calls, summed | 27.866 s |
| Assistance-game ask | 13.030 s |
| Deception-comparison ask | 14.460 s |
| Physical-controls ask | 11.832 s |
| Unsupported-budget ask | 12.687 s |
| Reviewed unchanged re-ingestion, zero generations | 0.010 s |

Ingestion's CLI peak RSS was 18.98 MiB; the first ask's was 19.33 MiB. Ollama reported a 3.48 GiB loaded allocation. The parent monitor's maximum sampled sum of isolated model-process RSS was **4.82 GiB**. It samples roughly every 0.5 seconds and may double-count shared pages; it is not an exact peak or a separate dedicated-VRAM measurement. In-sandbox process-RSS inspection was unavailable and is not reported as zero. See [measurements](evidence/goal-measurements.json) and [samples](evidence/goal-isolation/resource-samples.json).

Ask times cover inference HTTP calls, summing every recorded attempt; they exclude some CLI setup/saving overhead. Each required ask used one attempt. Where a repair occurs in independent cases, total latency includes both attempts. These are individual observations, not a controlled speed benchmark.

## Current evaluation results

| Fixed test | Expected behavior | Actual evidence |
|---|---|---|
| Assistance-game goal/uncertainty | Promote human interests while uncertain what those interests are | [Card 1](evidence/goal-run/01-assistance-game.md) |
| Deception comparison | Thinking trace versus explicit model output; no claimed proven detector | [Card 2](evidence/goal-run/02-deception-detection.md) |
| Physical/human controls | Human override, multiple humans, buttons/levers to shut off software, as proposals | [Card 3](evidence/goal-run/03-physical-defenses.md) |
| Approved treaty budget | Explicit insufficient evidence; no invented dollar figure | [Card 4](evidence/goal-run/04-unsupported.md) |

The required recorded suite has **3/3 complete supported answers plus the correct unsupported abstention**, with zero citation errors. The exact two capability prompts correctly skip retrieval, the study plan shortens from 99 to 42 words, note-based chat cites the source, source search makes no model call, and the independent codename ask rejects the chat-only fact. [Current semantic review](evidence/GOAL-REVIEW.md) distinguishes source/quote checks from claim support. [Reviewed re-ingestion](evidence/goal-reingest-integrity.json) preserves all six pages byte-for-byte without duplicates or new generations.

The two independent agents tested additional prospective questions on the privacy-revised corpus before the final chat correction (core `640884e…`). Their later bounded regressions use the final `a003420…` core; version boundaries and retained failures are explicit in the reports. **Their entire suites do not pass.** [A](evidence/independent/a/goal-verification/final-goal-report.md) reports 2/3 original answerable questions and 2/4 fresh held-outs complete, with explanation omissions and one unsupported factual comparison in an extra chat response. [B](evidence/independent/b/goal-verification/FINAL_REPORT.md) reports its four principal cases passing, an extra two-source question partial, and fresh held-outs at three pass/one partial/one fail; a capability paraphrase misdescribes `review` and `doctor`. Unsupported-question and chat/ask isolation checks pass. Read the reports for precise per-case distinctions.

On the final revision, [A's targeted regression](evidence/independent/a/goal-verification/final-chat-lines-regression-report.md) and [B's targeted regression](evidence/independent/b/goal-verification/LINE_REGRESSION_ADDENDUM.md) pass required chat, source citation, capability, representative research and isolation checks. A's extra source-shortening case repeats 61 words; B's different case shortens 71→48. These bounded reruns do not erase the broader research omissions above.

A real limitation is that a valid quote or source ID does not ensure a complete or fully grounded answer. The generic completeness prompt still misses requested explanations, and citation validation alone cannot establish semantic support. Source-dependent chat now selects original lines and shares the strict quotation validator. The original wrong-passage citation and the unsuccessful free-quote repair are retained. Evaluator A’s final regression also finds that a source-based “make that shorter” can repeat the same answer, even though ordinary draft shortening passes. A concrete next improvement is a separate requested-component and claim-support check evaluated on newly frozen cases, and checking additional paraphrases of the capability contract. The final chat correction already routes generic command/capability intent to that accurate contract. Prior failures and unsuccessful fixes remain preserved as labelled, privacy-redacted historical evidence.

## Network proof and verification

The [macOS policy](isolation/no-external-network.sb) denies network operations except loopback. Before replacing itself with Ollama, the restricted server entry process verifies OS permission errors for external IPv4 TCP, IPv6 TCP and UDP; its model-runner children inherit the policy. A separately restricted client probes before and after the CLI suite. Local echo and inference are positive controls. `OLLAMA_NO_CLOUD=1` disables cloud functionality, proxy variables are cleared, and the harness hardcodes a loopback host. The launcher refuses an occupied isolated port rather than reusing an unverified server.

[Server probe](evidence/goal-isolation/server-network.json), [client before](evidence/goal-isolation/client-network-before.json), [client after](evidence/goal-isolation/client-network-after.json) and [run status](evidence/goal-isolation/run.json) record policy hash, PIDs, fresh startup, Wi-Fi state and exit status. This is OS enforcement with active probes, not a packet capture or a physical air gap. The policy permits loopback services and ports; this harness uses its configured local Ollama endpoint. External inference/search services are inaccessible to the restricted workload.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/verify_vault.py
python3 scripts/publication_check.py
python3 scripts/privacy_audit.py
```

The privacy command uses generic patterns by default; the additional private denylist stays in ignored local state. Do not commit model weights, credentials, `.state`, private archives or private evaluator originals. The final snapshot has fresh sanitized history, and the private remote is verified separately from the local checks. This project was implemented and evaluated with AI assistance. The two independent evaluators are agents, not human graders; no course grade or portal receipt is asserted.
