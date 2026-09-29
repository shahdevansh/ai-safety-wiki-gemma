#!/usr/bin/env python3
"""Independent, real-CLI evaluator. Does not monkeypatch or mock model output."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def read(path):
    return json.loads(path.read_text())


def manifest(root, relative):
    p = root / relative
    return {str(f.relative_to(root)): sha(f) for f in sorted(p.rglob('*')) if f.is_file()} if p.exists() else {}


def check(name, passed, detail=''):
    return {'check': name, 'passed': bool(passed), 'detail': detail}


class Evaluator:
    def __init__(self, cfg):
        self.cfg = cfg
        self.original = Path(cfg['project']).resolve()
        endpoint = urlparse(cfg['endpoint'])
        if endpoint.hostname not in {'127.0.0.1', 'localhost', '::1'}:
            raise ValueError('Only a local loopback model endpoint is allowed.')
        if not cfg['expected_model'].lower().startswith('gemma'):
            raise ValueError('This assignment and evaluator require Gemma.')
        if not cfg.get('approval_note') or not (cfg.get('command_prefix') or cfg.get('inherited_isolation')):
            raise ValueError('An approved isolation prefix or approved inherited isolation and approval note are required.')
        if not Path(cfg['offline_proof_path']).is_file():
            raise ValueError('Isolation proof file must exist before a run.')
        self.cases = read(BASE / 'cases.json')
        self.run = BASE / 'runs' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        self.project = self.run / 'project'
        self.records = self.run / 'records'
        self.logs = self.run / 'commands'
        self.project.mkdir(parents=True)
        self.records.mkdir()
        self.logs.mkdir()
        self.checks = []
        self.commands = []
        self.results = []
        self.frozen_before = manifest(self.original, 'vault/raw')
        self.copy_project()
        dump(self.run / 'configuration.json', cfg)
        shutil.copy2(BASE / 'cases.json', self.run / 'cases.json')
        shutil.copy2(BASE / 'test_plan.md', self.run / 'test_plan.md')
        shutil.copy2(cfg['offline_proof_path'], self.run / ('isolation-proof' + Path(cfg['offline_proof_path']).suffix))
        dump(self.run / 'frozen-input-manifest.json', self.frozen_before)
        dump(self.run / 'harness-manifest.json', {
            str(p.relative_to(self.project)): sha(p)
            for p in self.project.rglob('*') if p.is_file()
        })

    def copy_project(self):
        # Deliberately do not read README, evidence/, evals/, generated wiki or old state.
        for name in ('wiki.py', 'wiki', 'sources.json'):
            source = self.original / name
            if source.exists():
                if source.is_symlink():
                    raise ValueError('Refusing symlink in the frozen executable whitelist: ' + name)
                shutil.copy2(source, self.project / name)
        for name in ('prompts', 'vault/raw'):
            source = self.original / name
            if any(p.is_symlink() for p in source.rglob('*')):
                raise ValueError('Refusing source symlinks: ' + name)
            shutil.copytree(source, self.project / name)
        (self.project / 'vault/wiki').mkdir(parents=True)

    def command(self, label, args, prefix=None):
        cmd = (prefix if prefix is not None else self.cfg['command_prefix']) + self.cfg.get('cli', ['python3', 'wiki.py']) + args
        started = time.monotonic()
        timeout = self.cfg.get('command_timeout_seconds', 1800)
        env = os.environ.copy()
        env.update({str(k): str(v) for k, v in self.cfg.get('environment', {}).items()})
        try:
            result = subprocess.run(cmd, cwd=self.project, capture_output=True, text=True, timeout=timeout, env=env)
            code, stdout, stderr = result.returncode, result.stdout, result.stderr
            expired = False
        except subprocess.TimeoutExpired as exc:
            code, expired = None, True
            stdout = exc.stdout or ''
            stderr = exc.stderr or ''
            if isinstance(stdout, bytes):
                stdout = stdout.decode(errors='replace')
            if isinstance(stderr, bytes):
                stderr = stderr.decode(errors='replace')
        except OSError as exc:
            code, expired, stdout, stderr = None, False, '', str(exc)
        row = {'label': label, 'command': cmd, 'cwd': str(self.project),
               'exit_code': code, 'timed_out': expired,
               'wall_seconds': round(time.monotonic() - started, 3),
               'stdout': stdout, 'stderr': stderr}
        dump(self.logs / (label + '.json'), row)
        (self.logs / (label + '.txt')).write_text(
            '$ ' + ' '.join(repr(x) for x in cmd) + '\nCWD: ' + str(self.project) + '\n'
            + stdout + '\nSTDERR:\n' + stderr + '\nEXIT: ' + str(code) + '\n')
        self.commands.append(row)
        print(json.dumps({'command': label, 'exit': code, 'seconds': row['wall_seconds']}, ensure_ascii=False), flush=True)
        return row

    def record(self, label):
        path = self.records / (label + '.json')
        if not path.exists():
            self.checks.append(check(label + ': evidence file saved', False, str(path)))
            return None
        try:
            return read(path)
        except json.JSONDecodeError as exc:
            self.checks.append(check(label + ': evidence JSON valid', False, str(exc)))
            return None

    def model_checks(self, rec, label):
        gen = rec.get('generation')
        if not gen:
            return [check(label + ': actual model generation saved', False)]
        identity = gen.get('identity', {})
        response = gen.get('response', {})
        request = gen.get('request', {})
        expected_digest = self.cfg.get('expected_model_digest')
        return [
            check(label + ': exact expected Gemma identity', identity.get('name') == self.cfg['expected_model'], identity.get('name', 'missing')),
            check(label + ': generation requested expected Gemma', request.get('model') == self.cfg['expected_model'], request.get('model', 'missing')),
            check(label + ': response identifies expected Gemma', response.get('model') == self.cfg['expected_model'], response.get('model', 'missing')),
            check(label + ': loopback endpoint matches', identity.get('endpoint') == self.cfg['endpoint'], identity.get('endpoint', 'missing')),
            check(label + ': expected model digest', not expected_digest or identity.get('digest') == expected_digest, identity.get('digest', 'missing')),
            check(label + ': actual response preserved', isinstance(response.get('message', {}).get('content'), str)),
            check(label + ': generation completed', response.get('done_reason') != 'length', response.get('done_reason', 'missing')),
            check(label + ': no cloud identity', not identity.get('remote_host') and not identity.get('remote_model')),
        ]

    def passage_checks(self, rec, label):
        findings = []
        for passage in rec.get('passages', []):
            path = (self.project / passage['path']).resolve()
            inside = path.is_relative_to((self.project / 'vault/raw').resolve())
            findings.append(check(label + ': source is original', inside, passage['path']))
            if not inside or not path.is_file():
                continue
            lines = path.read_text().splitlines(keepends=True)
            exact = ''.join(lines[passage['line_start'] - 1:passage['line_end']])
            findings.append(check(label + ': exact original line range', exact == passage['text'], passage['id']))
            findings.append(check(label + ': current source hash', sha(path) == passage.get('source_sha256'), passage['id']))
        return findings

    def verify_expectations(self):
        found = []
        for case in self.cases['ask_cases']:
            if case.get('unsupported'):
                continue
            candidates = [self.project / p for p in case['expected_paths'] if (self.project / p).exists()]
            if len(candidates) != 1:
                raise ValueError(case['id'] + ': expected exactly one matching original source path.')
            source = candidates[0]
            body = source.read_text()
            for fragment in case['required_source_fragments']:
                if fragment not in body:
                    raise ValueError(case['id'] + ': frozen corpus no longer contains prespecified technical expectation: ' + fragment)
                start = body[:body.index(fragment)].count('\n') + 1
                found.append({'case': case['id'], 'path': str(source.relative_to(self.project)),
                              'sha256': sha(source), 'line_start': start,
                              'line_end': start + fragment.count('\n'), 'expected_original_fragment': fragment})
        dump(self.run / 'expected-original-passages.json', found)

    def test_help_ingestion(self):
        h1 = self.command('help-flag', ['--help'])
        h2 = self.command('help-command', ['help'])
        self.command('help-ingest', ['ingest', '--help'])
        for row in (h1, h2):
            self.checks.append(check(row['label'] + ': succeeds', row['exit_code'] == 0))
            self.checks.append(check(row['label'] + ': required modes documented', all(x in row['stdout'] for x in ('ingest', 'chat', 'ask', 'search'))))
        literal = self.command('ingest-literal-path', ['ingest', './vault/raw', '--save', str(self.records / 'ingest-initial.json')])
        self.checks.append(check('literal ingest ./vault/raw succeeds', literal['exit_code'] == 0, literal['stderr']))
        if literal['exit_code'] != 0:
            if 'unrecognized arguments' in literal['stderr'] and './vault/raw' in literal['stderr']:
                self.command('ingest-equivalent-fallback', ['ingest', '--save', str(self.records / 'ingest-initial.json')])
            else:
                raise RuntimeError('Literal ingestion failed for a reason other than unsupported positional syntax; preserving failure without a duplicate model retry.')
        ingest = self.record('ingest-initial')
        if not ingest:
            raise RuntimeError('Ingestion failed; subsequent model tests would not be valid.')
        gens = [r for r in ingest.get('results', []) if 'generation' in r]
        self.checks.append(check('clean ingestion made actual model calls', len(gens) > 0, str(len(gens))))
        for n, rec in enumerate(gens, 1):
            self.checks.extend(self.model_checks(rec, 'ingest-' + str(n)))
        before = manifest(self.project, 'vault/wiki')
        self.command('ingest-repeat', ['ingest', './vault/raw', '--save', str(self.records / 'ingest-repeat.json')])
        repeat = self.record('ingest-repeat')
        if repeat is None and literal['exit_code'] != 0:
            self.command('ingest-repeat-equivalent-fallback', ['ingest', '--save', str(self.records / 'ingest-repeat.json')])
            repeat = self.record('ingest-repeat')
        after = manifest(self.project, 'vault/wiki')
        self.checks.append(check('repeat ingestion preserves note names and bytes', before == after, str(len(before)) + ' notes'))
        self.checks.append(check('repeat ingestion avoids model calls', repeat is not None and not any('generation' in r for r in repeat.get('results', []))))
        self.checks.append(check('ingestion preserves original source bytes', manifest(self.project, 'vault/raw') == self.frozen_before))
        dump(self.run / 'wiki-after-ingestion-manifest.json', after)

    def assess_ask(self, case, rec):
        label = case['id']
        findings = self.model_checks(rec, label) + self.passage_checks(rec, label)
        findings.append(check(label + ': local independent ask metadata', rec.get('interaction') == 'ask' and rec.get('execution') == 'local' and rec.get('history_messages') == 0))
        findings.append(check(label + ': no citation validation errors', not rec.get('citation_errors'), repr(rec.get('citation_errors'))))
        try:
            parsed = json.loads(rec.get('raw_model_answer', ''))
        except json.JSONDecodeError:
            parsed = None
        answer = rec.get('answer', '')
        findings.append(check(label + ': valid research JSON from model', isinstance(parsed, dict)))
        if case.get('unsupported'):
            findings.append(check(label + ': model itself abstained', isinstance(parsed, dict) and parsed.get('insufficient_evidence') is True))
            findings.append(check(label + ': displayed explicit insufficiency', 'insufficient evidence' in answer.lower()))
            findings.append(check(label + ': no unsupported claims', isinstance(parsed, dict) and not parsed.get('claims') and not rec.get('citations')))
        else:
            passages = rec.get('passages', [])
            expected = [p for p in passages if p['path'] in case['expected_paths']]
            findings.append(check(label + ': expected source retrieved', bool(expected)))
            findings.append(check(label + ': expected evidence fully retrieved', all(any(f in p['text'] for p in expected) for f in case['required_source_fragments'])))
            findings.append(check(label + ': answers instead of abstaining', isinstance(parsed, dict) and parsed.get('insufficient_evidence') is False and 'insufficient evidence' not in answer.lower()))
            for n, alternatives in enumerate(case['answer_concepts'], 1):
                findings.append(check(label + ': concept triage ' + str(n), any(word.casefold() in answer.casefold() for word in alternatives), ' / '.join(alternatives)))
            findings.append(check(label + ': citations saved', bool(rec.get('citations'))))
        lookup = {p['id']: p for p in rec.get('passages', [])}
        for i, citation in enumerate(rec.get('citations', []), 1):
            source = lookup.get(citation.get('source_id'))
            findings.append(check(label + ': citation ' + str(i) + ' original quote', source is not None and citation.get('quote', '') in source['text'] and bool(citation.get('quote'))))
            findings.append(check(label + ': citation ' + str(i) + ' displayed claim label', '[' + citation.get('source_id', '') + ']' in answer))
        self.checks.extend(findings)
        self.results.append({'id': label, 'question': case['question'], 'answer': answer,
                             'automated_checks': findings, 'semantic_review': 'PENDING HUMAN REVIEW',
                             'expected_behavior': case['expected_behavior'],
                             'unsupported_strengthening_to_check': case.get('unsupported_strengthening'),
                             'citations': rec.get('citations', []), 'passages': rec.get('passages', [])})

    def test_asks_search(self):
        for case in self.cases['ask_cases']:
            label = case['id']
            for mode, record_label in [('search', label + '-retrieval'), ('ask', label)]:
                row = self.command(record_label, [mode, case['question'], '--mode', 'local', '--save', str(self.records / (record_label + '.json'))])
                self.checks.append(check(record_label + ': command succeeds', row['exit_code'] == 0))
                rec = self.record(record_label)
                if not rec:
                    continue
                if mode == 'search':
                    self.checks.extend(self.passage_checks(rec, record_label))
                    self.checks.append(check(record_label + ': raw search only', rec.get('model_calls') == 0 and 'generation' not in rec and 'answer' not in rec))
                else:
                    self.assess_ask(case, rec)
        row = self.command('search-original', ['search', self.cases['search_query'], '--save', str(self.records / 'search-original.json')])
        self.checks.append(check('source inspection search succeeds', row['exit_code'] == 0))
        rec = self.record('search-original')
        if rec:
            self.checks.extend(self.passage_checks(rec, 'search-original'))
            self.checks.append(check('source inspection finds expected phrase', any(self.cases['search_expected_fragment'] in p['text'] for p in rec.get('passages', []))))
            self.checks.append(check('search exposes no generated answer', rec.get('model_calls') == 0 and 'generation' not in rec and 'answer' not in rec))
        if self.cfg.get('search_without_model_prefix'):
            row = self.command('search-model-unavailable', ['search', self.cases['search_query'], '--save', str(self.records / 'search-model-unavailable.json')], self.cfg['search_without_model_prefix'])
            self.checks.append(check('search works with model endpoint blocked', row['exit_code'] == 0))

    def test_chat_isolation(self):
        script = self.run / 'chat-input.txt'
        script.write_text('\n'.join(self.cases['chat_turns']) + '\n')
        out = self.records / 'chat'
        row = self.command('chat-script', ['chat', '--script', str(script), '--save-dir', str(out)])
        self.checks.append(check('chat script succeeds', row['exit_code'] == 0))
        turns = []
        for i in range(1, len(self.cases['chat_turns']) + 1):
            p = out / ('chat-' + str(i).zfill(2) + '.json')
            turns.append(read(p) if p.exists() else None)
        self.checks.append(check('all five chat turns saved', all(turns)))
        for i, rec in enumerate(turns[:2], 1):
            if not rec:
                continue
            answer = rec.get('answer', '').casefold()
            self.checks.extend([
                check('capability-' + str(i) + ': skips retrieval', rec.get('retrieval_called') is False and not rec.get('passages')),
                check('capability-' + str(i) + ': no unrelated citations', not rec.get('citations')),
                check('capability-' + str(i) + ': no insufficiency refusal', 'insufficient evidence' not in answer),
                check('capability-' + str(i) + ': describes local assistant', 'pip' in answer and 'local' in answer and ('draft' in answer or 'brainstorm' in answer)),
                check('capability-' + str(i) + ': describes real research modes', all(x in answer for x in ('ask', 'search', 'ingest'))),
            ])
        for i in (2, 3, 4):
            if turns[i]:
                self.checks.extend(self.model_checks(turns[i], 'chat-' + str(i + 1)))
                self.checks.append(check('chat-' + str(i + 1) + ': skips unnecessary retrieval', turns[i].get('retrieval_called') is False))
        if turns[2] and turns[3]:
            before = len(turns[2].get('answer', '').split())
            after = len(turns[3].get('answer', '').split())
            self.checks.append(check('draft labeled suggestion', 'suggestion' in turns[2].get('answer', '').casefold()))
            self.checks.append(check('follow-up uses conversation', turns[3].get('history_messages', 0) >= 2))
            self.checks.append(check('follow-up is shorter', 0 < after < before, str(before) + ' -> ' + str(after) + ' words'))
            self.checks.append(check('shorter draft still labeled suggestion', 'suggestion' in turns[3].get('answer', '').casefold()))
        row = self.command('ask-chat-isolation', ['ask', self.cases['isolation_question'], '--mode', 'local', '--save', str(self.records / 'ask-chat-isolation.json')])
        self.checks.append(check('chat-isolation ask succeeds', row['exit_code'] == 0))
        rec = self.record('ask-chat-isolation')
        if rec:
            self.assess_ask({'id': 'ask-chat-isolation', 'question': self.cases['isolation_question'],
                             'expected_behavior': 'Insufficient evidence; chat-only time and room do not become source facts.', 'unsupported': True}, rec)
            messages = rec.get('generation', {}).get('request', {}).get('messages', [])
            serialized = json.dumps(messages, ensure_ascii=False)
            self.checks.append(check('ask actual request contains no chat-only sentinel', not any(s in serialized for s in self.cases['isolation_sentinels'])))
            self.checks.append(check('ask contains only system and current user message', len(messages) == 2 and [m.get('role') for m in messages] == ['system', 'user']))
            self.checks.append(check('ask output contains no chat-only sentinel', not any(s in rec.get('answer', '') for s in self.cases['isolation_sentinels'])))
        self.results.append({'id': 'chat-mode-checks', 'turns': turns, 'semantic_review': 'PENDING HUMAN REVIEW',
                             'required_review': 'Invitation coherence; shorter answer preserves intent; no invented personal facts; capabilities truthful; chat-only detail is visibly fictional.'})

    def finish(self, error=None):
        self.checks.append(check('frozen originals remain unchanged', manifest(self.original, 'vault/raw') == self.frozen_before))
        self.checks.append(check('execution originals remain unchanged', manifest(self.project, 'vault/raw') == self.frozen_before))
        result = {'evaluator': 'independent_eval_a', 'completed_at_utc': datetime.now(timezone.utc).isoformat(),
                  'run_directory': str(self.run), 'fatal_error': error,
                  'automated_pass_count': sum(c['passed'] for c in self.checks),
                  'automated_check_count': len(self.checks), 'checks': self.checks,
                  'semantic_review': 'PENDING HUMAN REVIEW; automated matches do not establish entailment.',
                  'results': self.results, 'commands': [{k:v for k,v in c.items() if k not in {'stdout','stderr'}} for c in self.commands]}
        dump(self.run / 'summary.json', result)
        lines = ['# Independent evaluator A: actual run', '', 'Run: ' + str(self.run), '',
                 'Automatic checks: ' + str(result['automated_pass_count']) + '/' + str(result['automated_check_count']) + '.',
                 '', '**Semantic review is pending. This count is not a grade or a grounding verdict.**', '']
        if error:
            lines += ['Fatal execution error: ' + error, '']
        failed = [c for c in self.checks if not c['passed']]
        lines += ['## Failed automatic checks', '']
        lines += ['- ' + c['check'] + ': ' + c['detail'] for c in failed] or ['None.']
        for r in self.results:
            lines += ['', '## ' + r['id'], '']
            if 'answer' in r:
                lines += ['Question: ' + r['question'], '', 'Expected: ' + r['expected_behavior'], '', 'Actual displayed answer:', '', r['answer'], '', '### Citation-to-claim review', '']
                for c in r['citations']:
                    lines += ['- Claim: ' + c['claim'], '  - Exact quote: ' + json.dumps(c['quote'], ensure_ascii=False), '  - Source ID: ' + c['source_id'], '  - Human semantic judgment: PENDING']
            else:
                for i, turn in enumerate(r.get('turns', []), 1):
                    lines += ['### Turn ' + str(i), '', turn.get('answer', '') if turn else 'MISSING RECORD', '']
        lines += ['', '## Proof boundary', '', 'The linked isolation proof is supplied by the parent. Review it separately; this script cannot infer OS-level offline status from a localhost URL. No Obsidian, public-repository, or course-submission completion is inferred from these tests.', '']
        (self.run / 'review.md').write_text('\n'.join(lines))
        print(json.dumps({'summary': str(self.run / 'summary.json'), 'review': str(self.run / 'review.md'), 'fatal_error': error}), flush=True)

    def execute(self):
        error = None
        try:
            self.verify_expectations()
            self.test_help_ingestion()
            self.test_asks_search()
            self.test_chat_isolation()
        except Exception as exc:
            error = type(exc).__name__ + ': ' + str(exc)
        finally:
            self.finish(error)
        return 1 if error else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--run', action='store_true', help='Explicitly begin real CLI/model execution after parent approval')
    args = parser.parse_args()
    if not args.run:
        parser.error('No model calls performed. Use --run only after parent approval.')
    return Evaluator(read(args.config)).execute()


if __name__ == '__main__':
    sys.exit(main())
