#!/usr/bin/env python3
"""Bounded real-Gemma regression; preserves the original required chat script."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import baseline_evaluator as baseline
from run_goal_verification import GoalVerification

HERE = Path(__file__).resolve().parent


class ChatRegression(GoalVerification):
    def execute(self):
        error = None
        try:
            cases = baseline.read(HERE / 'chat-regression-cases.json')
            for name in ('chat-regression-cases.json', 'chat_regression_runner.py'):
                shutil.copy2(HERE / name, self.run / name)
            baseline.dump(self.run / 'regression-kind.json', {'scope':'bounded final grounded-chat regression',
                'prospective_case_sha256':hashlib.sha256((HERE/'chat-regression-cases.json').read_bytes()).hexdigest()})
            self.verify_expectations()
            result = self.command('reindex', ['reindex'])
            self.checks.append(baseline.check('reindex original corpus succeeds without generation', result['exit_code'] == 0))
            if result['exit_code'] != 0:
                raise RuntimeError('Cannot evaluate without index.')
            self.test_chat_isolation()
            case = next(c for c in self.cases['ask_cases'] if c['id'] == cases['original_ask_case'])
            label = case['id']
            result = self.command(label, ['ask', case['question'], '--mode', 'local', '--save', str(self.records/(label+'.json'))])
            self.checks.append(baseline.check(label + ': command succeeds', result['exit_code'] == 0))
            record = self.record(label)
            if record:
                self.assess_ask(case, record)
            result, turns = self.scripted_chat('source-followup-reset', cases['source_conversation'], timeout=240)
            self.checks.append(baseline.check('source follow-up and reset script succeeds', result['exit_code'] == 0))
            self.checks.append(baseline.check('source follow-up and reset has three answer records', len(turns)==3))
            if len(turns)==3:
                first, followup, reset = turns
                self.checks.append(baseline.check('lecture request retrieves originals', first.get('retrieval_called') is True and bool(first.get('passages'))))
                self.checks.append(baseline.check('lecture response has structured claim citations', bool(first.get('citations')) and all(isinstance(c,dict) for c in first['citations'])))
                self.checks.append(baseline.check('lecture citation validator accepts', not first.get('citation_errors')))
                self.checks.append(baseline.check('follow-up has recent history', followup.get('history_messages',0)>=2))
                self.checks.append(baseline.check('follow-up uses carried original evidence', followup.get('retrieval_called') is False and bool(followup.get('passages'))))
                self.checks.append(baseline.check('follow-up is shorter', len(followup.get('answer','').split())<len(first.get('answer','').split()), str(len(first.get('answer','').split()))+' -> '+str(len(followup.get('answer','').split()))))
                self.checks.append(baseline.check('follow-up citation validator accepts', not followup.get('citation_errors')))
                self.checks.append(baseline.check('reset clears history and carried passages', reset.get('history_messages')==0 and not reset.get('passages')))
                reset_messages=reset.get('generation',{}).get('request',{}).get('messages',[])
                self.checks.append(baseline.check('reset actual request has system and current turn only',len(reset_messages)==2 and [m['role'] for m in reset_messages]==['system','user']))
                self.checks.append(baseline.check('reset actual request lacks prior source material','fabrication' not in json.dumps(reset_messages).lower() and 'EVIDENCE (JSON' not in json.dumps(reset_messages)))
                for i,r in enumerate(turns,1):
                    self.checks.extend(self.passage_checks(r,'source-followup-reset-'+str(i)))
                    for c in r.get('citations',[]):
                        if isinstance(c,dict):
                            source=next((p for p in r.get('passages',[]) if p['id']==c.get('source_id')),None)
                            self.checks.append(baseline.check('source-followup-reset-'+str(i)+': quote belongs to cited passage',source is not None and bool(c.get('quote')) and c['quote'] in source['text']))
            prior=HERE/'runs/20260929T081134040293Z/records'/ (label+'.json')
            if record and prior.exists():
                old=baseline.read(prior)
                old_request=old['generation']['request'];new_request=record['generation']['request']
                self.checks.append(baseline.check('original ask complete model request unchanged after refactor',old_request==new_request))
                baseline.dump(self.run/'ask-request-comparison.json', {'identical_request':old_request==new_request,
                    'current_request_message_count':len(new_request['messages']),
                    'prior_request_sha256':hashlib.sha256(json.dumps(old_request,sort_keys=True).encode()).hexdigest(),
                    'current_request_sha256':hashlib.sha256(json.dumps(new_request,sort_keys=True).encode()).hexdigest()})
        except Exception as exc:
            error=type(exc).__name__+': '+str(exc)
        finally:
            self.audit_attempts()
            self.finish(error)
        return 1 if error else 0


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config',required=True,type=Path)
    p.add_argument('--run',action='store_true')
    a=p.parse_args()
    if not a.run:p.error('Requires explicit --run after parent GO.')
    return ChatRegression(baseline.read(a.config)).execute()


if __name__=='__main__':sys.exit(main())
