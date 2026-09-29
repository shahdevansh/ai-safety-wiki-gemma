#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${1:-evidence/assignment-run}"
mkdir -p "$OUT"
run() { printf '$'; printf ' %q' "$@"; printf '\n'; "$@"; }
run ./wiki --help
run ./wiki ingest ./vault/raw --force --save "$OUT/ingest.json"
python3 scripts/evaluate.py --out "$OUT"
run ./wiki search "workshop location" --save "$OUT/literal-search.json"
run ./wiki ask "Where is the workshop?" --mode local --save "$OUT/literal-ask.json"
run ./wiki ingest ./vault/raw --save "$OUT/reingest.json"
run python3 scripts/verify_vault.py --allow-pending
echo 'Freshly generated pages are pending editorial review. Review them against raw sources before marking them reviewed.'
