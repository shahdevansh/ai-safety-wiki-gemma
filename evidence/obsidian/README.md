# Obsidian inspection of the sanitized vault

These are actual Obsidian 1.13.7 screenshots, captured after opening this repository's `vault/` folder. They show only the sanitized vault, not the private original vault. No screenshot content was redrawn or altered.

- [Open reviewed note](reviewed-note.png): actual filename and heading, coherent subject, source reference and explained related-note links.
- [Topic index and full page list](index.png): Concepts and Governance, six readable note names.
- [Graph](graph.png): six topic nodes with meaningful cross-links and readable labels.
- [Graph filter settings](graph-filter.png): `path:wiki/`, attachments off, existing files only enabled.
- [Source catalog](source-catalog.png): three public source aliases and hashes.
- [Original passage](source-passage.png): the supporting text reached by a source link, including the disclosure that biographies and follow-ups were removed.

Observed navigation: index → Source Catalog → Human Control and Defenses → related Assistance Games → related Alignment and Interpretability → original alignment-fundamentals-notes. Each link opened the existing intended page; no missing-note creation prompt appeared. The source screenshot shows the alignment/interpretability passage. The source bytes were hash-checked after navigation. All six pages had `review_status: reviewed`; [editorial review hashes](../goal-editorial-review.json) identify them.

Visual privacy review: all six images show generic source aliases and subject names, with no account name, local home path, private meeting link, biography or contact details visible. Regex scanning alone does not inspect image pixels.

The source-catalog screenshot was recaptured after the final privacy-only source revision. Its lecture hash matches the current source manifest. Other screenshots show unchanged note content/navigation; final reviewed-page hashes are recorded in the current review. No pixels were edited.
