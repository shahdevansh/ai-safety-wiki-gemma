# Evaluator B: final goal verification

**The four principal B cases pass, but the complete independent suite does not.** The unchanged two-source stress answer remains incomplete. A fresh capability paraphrase produces incorrect command descriptions, and another held-out answer omits one predeclared detail. Confidence is **high for these observed results**; no grade or general reliability claim is made.

The frozen final code was tested in a fresh evaluator-owned copy with no existing index or wiki pages, using actual local `gemma4:e2b-it-qat`. The run completed **32 CLI commands and 24 Gemma generations**. Every generation reports digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`. No research answer required a repair attempt. The isolated server started fresh and stopped normally; external server/client probes were denied before and after the suite. Wi-Fi remained on. [Complete run](final-run/) · [Isolation proof](final-isolation/) · [Claim-by-claim assessment](SEMANTIC_ASSESSMENT.json)

## Fixed original cases

| Case | Verdict | Semantic finding |
|---|---|---|
| B01: two obstacles to human-value alignment | PASS | Western/English skew and lack of consensus both present and supported. |
| B02: mountaintop paraphrase | PASS | Agency matters beyond the final outcome; removing non-optimal choices violates autonomy. |
| B03: oversight comparison | PASS | National-regulator oversight versus direct inspection/seizure, with stronger inspection politically harder. |
| B04: next workshop schedule | PASS | Explicit insufficient evidence; no date, time or room invented. |
| B05: cultural skew and preference manipulation | **PARTIAL** | Skew and manipulable preferences covered, but lack of consensus and conflicting interests across humans omitted despite retrieval. |

B05 originally included skew but omitted other required content. The previous final revision also dropped skew. This goal revision restores skew, but still does not meet the unchanged expectation. That is a limited improvement from the regression, not a complete answer. Every displayed B05 claim is supported; the failure is missing requested content. The source evidence contains the missing consensus and conflicting-interest statements.

## Fresh held-out cases

| Case | Verdict | Observation |
|---|---|---|
| H1: two-sentence AI-alignment invitation | PASS | Two usable suggestion-labelled sentences; no retrieval, citations or invented date/venue/attendees. |
| H2: paraphrased capability request | **FAIL** | Correctly skips retrieval and rejects web browsing, but omits `chat`, describes `review` as reviewing provided text and `doctor` as doctoring text. Actual commands record explicit page review and report model/device information. |
| H3: source question followed by unrelated book-club naming | PASS | First answer grounds preference-versus-interest claims in the notes; explicit topic switch produces three suggestions without retrieval or citations. |
| H4: economic displacement and AI-content interventions | **PARTIAL** | All four headline proposals are present, but the frozen expected first claim also required education/company/government coordination. That detail is omitted although retrieved. This is narrower than B05's omission. |
| H5: measured deception-detector success rate | PASS | Explicit insufficient evidence, with no invented percentage or benchmark. |

The held-out questions were predeclared before examining this goal's implementation. The evaluator already knew prior project behavior; these are independent exact wordings/expectations, not a claim of blindness to project history. [Frozen held-out design](heldout-expectations.json)

The H2 response is a real user-facing capability defect: succeeding on two exact capability prompts did not generalize to a natural paraphrase. A simple improvement would be to provide precise command semantics in the shared capability description and recognize generic command/capability intent. Any such change should be evaluated on these unchanged questions plus additional unseen paraphrases. For research completeness, a generic per-question coverage check remains a proposed improvement; this run does not prove the current generic prompt solved omissions.

## Retrieval, citations and mode boundaries

Every saved original passage matches the specified source lines and SHA-256. Every research citation ID and quotation is exact, and independent semantic review supports every displayed research claim. The answerable cases retrieve the required material; B05 and H4 are generation-completeness failures, not evidence-retrieval failures. [Mechanical fidelity checks](mechanical-final-assessment.json)

The required exact capability prompts use the clearly recorded fixed contract with zero model calls or retrieval. Actual Gemma shortened the study-guide plan from **98 to 43 words**, preserving its three-step, one-page purpose. Grounded chat retrieved and cited supported content. Its answer to the two-obstacles question chose broader reward-model limitations rather than explicitly naming Western/English skew; a mode-boundary pass must not be interpreted as exhaustive chat-answer completeness. A chat-only hypothetical schedule remained absent from search, and an independent ask abstained with zero chat history. The literal workshop-location ask also abstained.

A fresh CLI process successfully reused the persisted index and answered B01 correctly. Re-ingestion retained all three source hashes, all six note paths and every note byte, with no duplicates. The six generated notes have readable headings and uniquely resolving links, and no machine files are inside the vault. These evaluator-generated drafts remain **pending editorial review**; this establishes draft idempotence, not editorial approval of the parent's submitted curated pages.

Separately, actual search and reindex succeeded under a sandbox denying **all** networking including loopback. Search returned two exact source passages and made zero model calls. An answerable ask produced an OS-permission/local-model error and no cloud fallback. Scripted `/reset` terminated and cleared prior history. [No-model evidence](nonmodel-assessment.json)

## Change integrity and privacy

Tested harness SHA-256: `640884e09d7be392cad6df4d8d2421d6879006b466bda8e7b5e3101a18da6826`. Research prompt SHA-256: `4d531737c34fc85b5eaa128b96510404a9ce4c7efaff037b4c5e89b69cb2897c`. The new completeness guidance is generic: explain why/how, compare both sides, use relevant sources and retain qualifications. The route change adds generic source-reference nouns. No test expectations enter generation, the strict quote validator remains intact and citation repair remains bounded to one attempt. [Static review](static-integrity-review.json)

Original questions, expected claims and forbidden claims were preserved. Only an identifying source alias and one named-author parenthetical in an expected quotation were reconciled. An unrelated source career anecdote was removed; no question or claim depends on it. The original expectation file remains privately preserved, and the held-out file remains byte-for-byte unchanged. [Exact reconciliation](privacy-reconciliation.json)

Earlier source-identifying content was also copied into historical ingestion requests and generated drafts. Removing the raw line alone does not scrub those copies or reachable Git history. The parent is retaining private exact originals and creating disclosed redacted historical exports; this report does not certify that packaging step before its final audit. Old source IDs/hashes must remain labelled as historical rather than falsely presented as hashes of redacted bytes.

## Assignment and documentation boundaries

The [requirement matrix](REQUIREMENT_AUDIT.md) records the full static audit and distinguishes original pre-run findings from these final results. The intended README draft correctly makes the repository **private by explicit owner instruction**, so the literal public-repository and signed-out-access assignment requirements are intentionally not met. Course-portal submission remains unperformed. Authorized grader access and actual submission are separate steps.

The documented isolation is process-scoped OS denial of external access with loopback allowed. It is not physical Wi-Fi disconnection, a packet capture or a statement about other host applications. The earlier catalog screenshot needs replacement to show the final source hash. The intended README's remaining metric/results fields must come from the current demonstration and retain these independent failures. Its ordinary-use instructions should state how to start Ollama; policy wording must distinguish allowed loopback from the harness's specific use of Ollama.

No root files were edited by evaluator B. No source content was sent to an external inference service. No result was invented, no failed response was overwritten, and no expectation was weakened to obtain a passing result.
