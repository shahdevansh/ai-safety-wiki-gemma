# Prospective evaluation design

This is an AI Safety learning wiki built from three existing meeting-note summaries. Before publication, source copies were redacted to remove personal identifiers, private meeting metadata, participant biographies, and personal follow-ups. Private originals remain local. The redacted public sources are frozen by source-manifest.json before ingestion and evaluation.

The original four AI Safety research questions are retained, with venue labels generalized solely for privacy. Their expected passages and behaviors are in cases.json and remain outside retrieval. They test assistance-game goals, deception-detection research directions, physical control proposals, and an absent approved governance budget.

Two independent evaluators additionally wrote their own cases before execution, without reading this answer key or earlier outputs. Their complete cases, scripts, outputs and assessments belong under evidence/independent/. Their tests are not training data or retrieval sources.

The model is local Gemma 4 E2B QAT (Q4_0) through Ollama. The CLI and a fresh model server run inside an OS policy that denies external networking while allowing loopback. Model outputs are real; no mock or cloud fallback is used. This substitutes enforced per-process disconnection for changing the host's Wi-Fi state.

Retrieval is SQLite FTS5 with Porter stemming and BM25. It reads only the registered raw sources, using contiguous original-line passages and source labels. Expected limits include synonym misses and small-model false abstentions. Citation substring validation does not establish semantic support; reviewers assess each material claim.
