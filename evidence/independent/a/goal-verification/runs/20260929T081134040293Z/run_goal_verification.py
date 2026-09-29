#!/usr/bin/env python3
"""Run unchanged A cases plus prespecified held-out cases; no synthetic model output."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

import baseline_evaluator as baseline

HERE = Path(__file__).resolve().parent


class GoalVerification(baseline.Evaluator):
    def __init__(self, config):
        super().__init__(config)
        self.heldout = baseline.read(HERE / 'heldout-cases.json')
        for name in ('heldout-cases.json', 'heldout-plan.md', 'run_goal_verification.py', 'baseline_evaluator.py'):
            shutil.copy2(HERE / name, self.run / name)
        baseline.dump(self.run / 'evaluator-input-manifest.json', {
            name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            for name in ('cases.json', 'test_plan.md', 'heldout-cases.json', 'heldout-plan.md',
                         'baseline_evaluator.py', 'run_goal_verification.py')
        })

    def verify_heldout_expectations(self):
        evidence = []
        for case in self.heldout['ask_cases']:
            for requirement in case['source_requirements']:
                source = self.project / requirement['path']
                text = source.read_text()
                for fragment in requirement['fragments']:
                    if fragment not in text:
                        raise ValueError(case['id'] + ': frozen source missing prespecified fragment: ' + fragment)
                    evidence.append({'case': case['id'], 'path': requirement['path'], 'sha256': baseline.sha(source),
                                     'line_start': text[:text.index(fragment)].count('\n') + 1,
                                     'original_fragment': fragment})
        baseline.dump(self.run / 'expected-heldout-passages.json', evidence)

    def test_heldout_research(self):
        for case in self.heldout['ask_cases']:
            label = case['id']
            for mode, name in [('search', label + '-retrieval'), ('ask', label)]:
                result = self.command(name, [mode, case['question'], '--mode', 'local', '--save', str(self.records / (name + '.json'))])
                self.checks.append(baseline.check(name + ': command succeeds', result['exit_code'] == 0))
                record = self.record(name)
                if not record:
                    continue
                if mode == 'search':
                    self.checks.extend(self.passage_checks(record, name))
                    self.checks.append(baseline.check(name + ': original search without generation', record.get('model_calls') == 0 and 'generation' not in record and 'answer' not in record))
                else:
                    self.assess_ask(case, record)
                    lookup = {p['id']: p for p in record.get('passages', [])}
                    for requirement in case['source_requirements']:
                        matching = [p for p in record.get('passages', []) if p['path'] == requirement['path']]
                        self.checks.append(baseline.check(label + ': required source retrieved ' + requirement['path'], bool(matching)))
                        self.checks.append(baseline.check(label + ': required source excerpts retrieved ' + requirement['path'],
                            all(any(f in p['text'] for p in matching) for f in requirement['fragments'])))
                        self.checks.append(baseline.check(label + ': required source contributes citation ' + requirement['path'],
                            any(lookup.get(c.get('source_id'), {}).get('path') == requirement['path'] for c in record.get('citations', []))))
                    self.results[-1]['semantic_requirements'] = case['semantic_requirements']

    def scripted_chat(self, label, turns, timeout=None):
        script = self.run / (label + '-input.txt')
        script.write_text('\n'.join(turns) + '\n')
        directory = self.records / label
        previous_timeout = self.cfg.get('command_timeout_seconds')
        if timeout is not None:
            self.cfg['command_timeout_seconds'] = timeout
        try:
            result = self.command(label, ['chat', '--script', str(script), '--save-dir', str(directory)])
        finally:
            if previous_timeout is None:
                self.cfg.pop('command_timeout_seconds', None)
            else:
                self.cfg['command_timeout_seconds'] = previous_timeout
        records = [baseline.read(p) for p in sorted(directory.glob('*.json'))] if directory.exists() else []
        self.results.append({'id': label, 'turns': records, 'semantic_review': 'PENDING HUMAN REVIEW'})
        return result, records

    def test_heldout_modes(self):
        route = self.heldout['routing_chat']
        result, records = self.scripted_chat(route['id'], route['turns'])
        self.checks.append(baseline.check(route['id'] + ': command succeeds', result['exit_code'] == 0))
        self.checks.append(baseline.check(route['id'] + ': one saved answer', len(records) == 1))
        if records:
            record = records[-1]
            self.checks.append(baseline.check(route['id'] + ': notes retrieval called', record.get('retrieval_called') is True))
            self.checks.append(baseline.check(route['id'] + ': required evidence retrieved',
                all(any(p['path'] == route['expected_path'] and f in p['text'] for p in record.get('passages', [])) for f in route['expected_fragments'])))
            self.checks.append(baseline.check(route['id'] + ': note claims cited', bool(record.get('citations'))))
            self.checks.extend(self.passage_checks(record, route['id']))
            if 'generation' in record:
                self.checks.extend(self.model_checks(record, route['id']))

        result, _ = self.scripted_chat('heldout-reset-smoke', self.heldout['reset_smoke_turns'], timeout=8)
        self.checks.append(baseline.check('scripted reset advances and exits', result['exit_code'] == 0, 'Timed out' if result['timed_out'] else result['stderr']))
        if result['exit_code'] != 0:
            self.checks.append(baseline.check('stateful reset tested', False, 'Skipped after reset smoke failed to prevent repeating a loop.'))
            return
        reset = self.heldout['reset_chat']
        result, records = self.scripted_chat(reset['id'], reset['turns'], timeout=120)
        self.checks.append(baseline.check(reset['id'] + ': command succeeds', result['exit_code'] == 0))
        self.checks.append(baseline.check(reset['id'] + ': two generated turn records', len(records) == 2))
        if len(records) >= 2:
            final = records[-1]
            self.checks.extend(self.model_checks(final, reset['id']))
            messages = final.get('generation', {}).get('request', {}).get('messages', [])
            self.checks.append(baseline.check(reset['id'] + ': actual post-reset prompt lacks marker', reset['sentinel'] not in json.dumps(messages)))
            self.checks.append(baseline.check(reset['id'] + ': no pre-reset conversational messages', final.get('history_messages') == 0))
            self.checks.append(baseline.check(reset['id'] + ': output does not recover fictional marker', reset['sentinel'] not in final.get('answer', '')))
            self.checks.append(baseline.check(reset['id'] + ': no unnecessary retrieval', final.get('retrieval_called') is False))

    def audit_attempts(self):
        entries = []
        for path in sorted(self.records.rglob('*.json')):
            record = baseline.read(path)
            if 'generation' not in record:
                continue
            attempts = record.get('citation_validation_attempts') or [{'generation': record['generation']}]
            generations = [a['generation'] for a in attempts if 'generation' in a]
            seconds = sum(g.get('metrics', {}).get('wall_seconds', 0) for g in generations)
            entry = {'record': str(path.relative_to(self.run)), 'attempt_count': len(attempts),
                     'completed_generation_count': len(generations), 'all_attempt_seconds': round(seconds, 3),
                     'attempt_errors': [a.get('citation_errors', []) for a in attempts],
                     'repair_errors': [a.get('repair_error') for a in attempts if a.get('repair_error')]}
            entries.append(entry)
            for i, generation in enumerate(generations, 1):
                self.checks.extend(self.model_checks({'generation': generation}, str(path.relative_to(self.records)) + ': attempt ' + str(i)))
        baseline.dump(self.run / 'all-attempts-audit.json', entries)

    def execute(self):
        error = None
        try:
            self.verify_expectations()
            self.verify_heldout_expectations()
            self.test_help_ingestion()
            self.test_asks_search()
            self.test_chat_isolation()
            self.test_heldout_research()
            self.test_heldout_modes()
        except Exception as exc:
            error = type(exc).__name__ + ': ' + str(exc)
        finally:
            self.audit_attempts()
            self.finish(error)
        return 1 if error else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True, type=Path)
    parser.add_argument('--run', action='store_true')
    args = parser.parse_args()
    if not args.run:
        parser.error('No model execution without --run and parent GO.')
    return GoalVerification(baseline.read(args.config)).execute()


if __name__ == '__main__':
    sys.exit(main())
