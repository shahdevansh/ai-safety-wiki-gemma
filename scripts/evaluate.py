#!/usr/bin/env python3
"""Run fixed expectations via fresh CLI processes; retain exact terminal output."""
import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(); p.add_argument('--out', default='evidence/assignment-run'); a = p.parse_args()
out = ROOT / a.out; out.mkdir(parents=True, exist_ok=True)
transcript = out / 'terminal.txt'

def run(args):
    command = [sys.executable, '-u', 'wiki.py', *args]
    shown = shlex.join(['./wiki', *args])
    print('\n$ ' + shown, flush=True)
    process = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(process.stdout, flush=True)
    with transcript.open('a') as f:
        f.write('\n$ ' + shown + '\n' + process.stdout)
    if process.returncode: raise SystemExit(process.returncode)

run(['help'])
results = []
for case in json.loads((ROOT/'evals/cases.json').read_text()):
    dest = out / (case['id'] + '.json')
    run(['ask', case['question'], '--save', str(dest.relative_to(ROOT))])
    result = json.loads(dest.read_text())
    expected = case['expected_source']
    hit = any(x['path'] == expected and case['expected_quote'] in x['text'] for x in result['passages']) if expected else None
    outcome = {'id':case['id'], 'expected':case, 'retrieval_hit':hit,
               'valid_citations':not result['citation_errors'],
               'abstained':'Insufficient evidence' in result['answer'],
               'semantic_review':'See evidence/GOAL-REVIEW.md for the current reviewed demonstration; new runs need fresh semantic review. Automated checks do not establish entailment', 'answer':result['answer']}
    results.append(outcome)
    with dest.with_suffix('.md').open('a') as f:
        f.write('\n## Fixed expectation\n\n' + case['expected_behavior'] + '\n\nExpected source: ' + str(expected) + '\n\nExpected passage: ' + str(case['expected_quote']) + '\n')
run(['chat', '--script', 'evals/chat.txt', '--save-dir', str(out.relative_to(ROOT))])
run(['search', 'physical fail-safes human override', '--save', str((out/'search.json').relative_to(ROOT))])
run(['ask', 'What is my project codename?', '--save', str((out/'chat-isolation.json').relative_to(ROOT))])
(out/'summary.json').write_text(json.dumps(results, indent=2) + '\n')
print('Saved evidence: ' + str(out.relative_to(ROOT)))
