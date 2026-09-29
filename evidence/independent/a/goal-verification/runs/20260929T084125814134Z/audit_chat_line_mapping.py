#!/usr/bin/env python3
"""Read-only provenance audit of a completed bounded chat run; no model calls."""
import argparse
import hashlib
import json
from pathlib import Path


def audit(run):
    checks = []
    selections = []

    def check(label, passed, **details):
        checks.append({'check': label, 'passed': bool(passed), **details})

    for path in sorted((run / 'records').rglob('*.json')):
        record = json.loads(path.read_text())
        catalog = record.get('citation_line_catalog') or {}
        if not catalog:
            continue
        label = str(path.relative_to(run))
        passages = {p['id']: p for p in record['passages']}
        for line_id, entry in catalog.items():
            source_path = run / 'project' / entry['path']
            source = source_path.read_text().splitlines()
            passage = passages.get(entry['source_id'])
            number = entry['line_number']
            check(label + ': catalog line has exact original text',
                  0 < number <= len(source) and source[number - 1] == entry['quote'], line_id=line_id)
            check(label + ': catalog line has exact passage provenance',
                  passage and passage['path'] == entry['path']
                  and passage['line_start'] <= number <= passage['line_end']
                  and passage['text'].splitlines()[number - passage['line_start']] == entry['quote'],
                  line_id=line_id)
            check(label + ': catalog source hash matches',
                  passage and hashlib.sha256(source_path.read_bytes()).hexdigest() == passage['source_sha256'],
                  line_id=line_id)
        attempts = record.get('citation_validation_attempts', [])
        for i, attempt in enumerate(attempts, 1):
            raw = json.loads(attempt['raw_model_answer'])
            for claim in raw.get('claims', []):
                for support in claim.get('supports', []):
                    line_id = support.get('line_id')
                    entry = catalog.get(line_id)
                    check(label + ': model selected a supplied line', entry is not None,
                          attempt=i, line_id=line_id)
                    if entry:
                        selections.append({'record': label, 'attempt': i,
                                           'claim': claim['text'], 'line_id': line_id, **entry})
                        if i == len(attempts) and not record.get('citation_errors'):
                            check(label + ': final citation exactly resolves selected line',
                                  {'claim': claim['text'], 'source_id': entry['source_id'],
                                   'quote': entry['quote']} in record['citations'], line_id=line_id)
    return {'scope': 'Original-line identity/provenance only; entailment is independently reviewed in the report.',
            'check_count': len(checks), 'passed_count': sum(c['passed'] for c in checks),
            'checks': checks, 'selected_lines': selections}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    args = parser.parse_args()
    result = audit(args.run)
    (args.run / 'line-mapping-audit.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({key: result[key] for key in ('check_count', 'passed_count')}))
