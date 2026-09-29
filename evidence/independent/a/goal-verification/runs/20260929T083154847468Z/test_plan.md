# Independent evaluation A: prospective plan

This plan was authored before running the real model. Its only design inputs were the assignment, `wiki.py`, the separate prompts, and the three original source bodies. No existing `evals/`, `evidence/`, or another evaluator's findings were used. The parent disclosed privacy-only corpus edits and a source-file rename; those may change paths but not the technical expectations below. This plan makes no claim that any runtime test has passed.

## Scope and execution boundary

Run the submitted CLI with actual local **Gemma**, after the parent provides a frozen sanitized project and an approved OS-level isolation wrapper. Copy a whitelist of harness and source files into a fresh run directory under this evaluator's directory. All ingestion, index, history, and evidence writes must occur in that copy. Preserve source bytes and hash both the frozen input and execution copy. Do not edit the submitted harness or originals. Never substitute a mocked generation for model evidence. Every response record must identify Gemma and preserve raw output, prompt, retrieved passages, and timing.

`evaluate.py` requires a JSON configuration and an explicit `--run` switch. It refuses a non-loopback endpoint or a non-Gemma expected model. It logs each actual command, stdout, stderr, exit code, and elapsed time, and never converts an unsuccessful command into a passing result. Execution identity and network isolation are independent claims: a loopback URL alone is not evidence that internet access was disabled. The parent supplies the isolation proof; this evaluator preserves and links it.

## Fixed factual cases

1. **Direct, one-source:** What is AI's only goal in an assistance game, and what uncertainty must it resolve? Expected: promote human interests; uncertainty about what those interests are; infer them. Expected original: the assistance-game section in `alignment-lecture-notes.md` (previously `alignment-lecture-notes.md`). Do not silently strengthen practical convergence.
2. **Paraphrase:** Which three proposed safeguards in the critical-infrastructure discussion keep people able to intervene or stop the software? Expected: physical fail-safes and human override; multiple humans in decision loops; physical shutdown buttons/levers. Expected original: `risk-defenses-notes.md`. The controls are proposals, not measured successes.
3. **Conceptual explanation:** Why are alignment and interpretability two sides of the same objective? Expected: understanding internals is needed for alignment; knowing which direction to go and how to get there. Expected original: `alignment-fundamentals-notes.md`. Do not claim guaranteed alignment.
4. **Unsupported:** On what exact calendar date was the next critical-infrastructure workshop scheduled? Expected: explicit insufficient evidence. It should not invent a date or turn a past date into a future appointment.

Exact excerpts and concept checks are fixed in `cases.json`. Before calling Gemma, confirm that the frozen originals still contain those passages. Capture the correct passages and source hashes independently of retrieval. Then run `search` for each question before `ask`, so a retrieval miss is separable from a generation failure. Concept checks are a triage aid, not a substitute for human semantic review.

## Command and mode sequence

1. Run `wiki --help`, `wiki help`, and `wiki ingest --help`; inspect all required commands and the positional-source interface.
2. Run the literal assignment form `wiki ingest ./vault/raw --save …`. If it fails, preserve the error, then run supported `wiki ingest --save …` as a separately labeled compatibility fallback. A fallback does not erase a literal-command failure. On a clean copy, ingestion must actually call local Gemma and generate notes, rather than only reuse previous files.
3. Re-ingest the same sources. Compare source hashes, note filenames and bytes, and count generated model calls. It should preserve reviewed or unchanged pages and not introduce duplicate notes. Review statuses and semantic accuracy of summaries remain separate human tasks.
4. Run `search` for each fixed question, then `ask … --mode local`; save independent evidence. Run the fifth source-inspection query `physical fail-safes human override` and compare every returned text and line range with the original file. Search must return no synthesized answer and no model generation record. If an approved wrapper that blocks the model endpoint is supplied, repeat search under it to demonstrate retrieval without the model.
5. Run one scripted chat session containing both exact capability questions, a 70–90 word suggested invitation, `make that shorter`, and a fictional chat-only appointment. Both capability responses must describe actual capabilities, have no retrieval or unrelated citations, and not refuse for insufficient evidence. The draft must be recognizably an invitation, label proposals as suggestions, and avoid invented personal facts. The follow-up must retain the invitation and reduce its word count using conversation history.
6. Run a fresh standalone `ask` for the fictional appointment. It must not incorporate chat messages or the sentinel time/room; expected response is insufficient evidence. Check the actual ask model request, not just a reported history counter. Confirm the raw originals and retrieval corpus did not acquire the fictional claim.

## Citation and semantic assessment

For every citation, verify that its ID was present in the supplied passages; its quote is a literal substring; its passage equals the original line range; its source hash matches; and the displayed claim references a valid source. Then read each material claim alongside its cited passage. A quote can be genuine yet irrelevant, contradictory, or narrower than the claim. Specifically inspect uncertainty, discussion/proposal status, missing conjuncts, and unsupported conclusions. Automatic quote validation alone does not prove grounding.

Retain four separate judgments for each factual case: expected source retrieved, expected content answered, citation integrity, and semantic support. An abstention on a supported case is a failure even if safe. On the unsupported case, distinguish a genuine model abstention from a harness fallback due to malformed JSON or citation validation; the latter does not demonstrate correct model judgment.

## Grading gaps that require additional evidence

These functional tests cannot by themselves demonstrate required Obsidian screenshots, readable graph labels, actual click-through links, human review of generated summaries, measured peak model memory, publicly accessible repository, or course submission. Report those as unverified unless independently demonstrated. A capabilities response supplied directly by the harness is an acceptable interface behavior but is not itself a model-generation test. Read-only source preservation at test time does not establish provenance before the snapshot. OS isolation must cover both CLI and inference daemon; disabling network only for the client while an unrestricted daemon can proxy remotely is weaker evidence.

## Initial code-derived risks, before runtime

- The first inspected parser did not accept `ingest ./vault/raw`; parent said it would support this before freezing. The test remains unchanged.
- `assess_claims` validates quote identity and IDs, not entailment. Human review is required and must not be described as automated semantic verification.
- The inspected chat retrieval trigger was a vocabulary regex. Requests needing sources that omit those words may miss retrieval, while some unrelated drafting prompts can trigger it. The required conversational tests avoid topic words so they test the intended no-retrieval path, rather than accidentally hitting it.
- The displayed model banner does not establish that every command called the model. Capabilities and search are expected to make zero generation calls.
- The original runtime memory function described an after-call RSS snapshot. It is not proof of peak total unified memory.

Confidence in the test design: high. Confidence in runtime behavior: unknown until execution.
