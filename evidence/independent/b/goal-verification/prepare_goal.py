from pathlib import Path
import ast,copy,datetime,hashlib,json,re
BASE=Path(__file__).resolve().parent
OLD=BASE.parent
SOURCE=Path('<submission>')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(name,value):(BASE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
original=json.loads((OLD/'expectations.json').read_text())
derivative=copy.deepcopy(original)
reconciled=[]
for case in derivative['cases']:
    for passage in case['required_passages']:
        oldpath=passage['source']
        if Path(oldpath).name not in ['alignment-fundamentals-notes.md','risk-defenses-notes.md']:
            passage['source']='vault/raw/alignment-lecture-notes.md'
        before=passage['exact_passage']
        if case['id']=='B02-mountaintop':
            passage['exact_passage']=re.sub(r'(Strivings and achievements) \([^)]*\)',r'\1',before)
        raw=(SOURCE/passage['source']).read_text()
        assert passage['exact_passage'] in raw,(case['id'],'expected passage missing')
        reconciled.append({'case':case['id'],'final_source':passage['source'],'source_alias_changed':oldpath!=passage['source'],'exact_excerpt_changed':before!=passage['exact_passage'],'change_reason':'Remove named-author parenthetical only' if before!=passage['exact_passage'] else 'No excerpt change','original_excerpt_sha256':hashlib.sha256(before.encode()).hexdigest(),'final_excerpt_sha256':hashlib.sha256(passage['exact_passage'].encode()).hexdigest(),'final_source_sha256':sha(SOURCE/passage['source'])})
for a,b in zip(original['cases'],derivative['cases']):
    assert a['question']==b['question'] and a['expected_claims']==b['expected_claims'] and a['forbidden_claims']==b['forbidden_claims']
derivative['privacy_reconciliation']='Derived from unchanged privately preserved evaluator B expectations. Questions, expected claims and forbidden claims unchanged; source alias and one author parenthetical reconciled for privacy. See privacy-reconciliation.json.'
out('expectations.json',derivative)
(BASE/'expectations.sha256').write_text(sha(BASE/'expectations.json')+'  expectations.json\n')
heldout=json.loads((BASE/'heldout-expectations.json').read_text())
assert sha(BASE/'heldout-expectations.json')==(BASE/'heldout-expectations.sha256').read_text().split()[0]
heldout_rows=[]
for c in heldout['cases']:
    entries=list(c.get('expected_passages',[]))
    for t in c.get('turns',[]):entries.extend(t.get('expected',{}).get('expected_passages',[]))
    if c.get('nearby_nonanswer_passage'):entries.append(c['nearby_nonanswer_passage'])
    for e in entries:
        assert e['text'] in (SOURCE/e['source']).read_text()
        heldout_rows.append({'case':c['id'],'source':e['source'],'exact_expected_text_unchanged':True,'frozen_source_sha256':e['source_sha256'],'final_source_sha256':sha(SOURCE/e['source'])})
out('privacy-reconciliation.json',{'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_expectations_sha256':sha(OLD/'expectations.json'),'privacy_reconciled_expectations_sha256':sha(BASE/'expectations.json'),'questions_claims_and_forbidden_claims_unchanged':True,'privacy_edits':'An identifying source filename was aliased; one author parenthetical was omitted. An unrelated speaker-specific career anecdote was removed from the source; no expected claim depends on it. Originals remain privately preserved.','existing_cases':reconciled,'heldout_cases':heldout_rows,'heldout_expectations_unchanged_sha256':sha(BASE/'heldout-expectations.json')})
src=(OLD/'evaluator.py').read_text()
src=re.sub(r"def renamed\(path\): return .*",'def renamed(path): return path',src)
src=src.replace('import argparse, datetime, errno, hashlib, json, os, re, shutil, socket, subprocess, sys, time','import argparse, datetime, errno, hashlib, json, os, re, shlex, shutil, socket, subprocess, sys, time')
src=src.replace("'$ '+ ' '.join(cmd)","'$ '+ shlex.join(cmd)")
src=src.replace("    source_before=hashes(workspace/'vault/raw');runner=Runner(args,run,workspace)","    assert sha(workspace/'wiki.py') == '640884e09d7be392cad6df4d8d2421d6879006b466bda8e7b5e3101a18da6826', 'Core freeze changed'\n    assert sha(workspace/'prompts/research.md') == '4d531737c34fc85b5eaa128b96510404a9ce4c7efaff037b4c5e89b69cb2897c', 'Prompt freeze changed'\n    assert sha(workspace/'vault/raw/alignment-lecture-notes.md') == '76c88bc45bce852e63112fffc2cd94ffd377aa0e4a8b1fe7d7c3713a8afa5d02', 'Data freeze changed'\n    source_before=hashes(workspace/'vault/raw');runner=Runner(args,run,workspace)")
insert='''    # Fresh exact held-out questions were frozen before reviewing this implementation.
    heldout_path = BASE/'heldout-expectations.json'
    assert sha(heldout_path) == (BASE/'heldout-expectations.sha256').read_text().split()[0]
    heldout = read_json(heldout_path)
    for case in heldout['cases']:
        if case['mode']=='chat':
            turns = [t['message'] for t in case['turns']] if 'turns' in case else [case['message']]
            runner.command(case['id'],['chat','--save-dir',str(run/'heldout-chat'/case['id'])],stdin='\\n'.join(turns+['/exit'])+'\\n',timeout=600)
        else:
            runner.record(case['id']+'-retrieval','search',case['question'])
            runner.record(case['id'],'ask',case['question'])
    # Deterministic capability contract on both sides of reset; no model or retrieval.
    reset_script = run/'reset-script.txt'
    reset_script.write_text('what can we do?\\n/reset\\nwhat can you help me with?\\n/exit\\n')
    runner.command('scripted-reset',['chat','--script',str(reset_script),'--save-dir',str(run/'reset-chat')],timeout=15)
'''
src=src.replace("    write_json(run/'run-summary.json'",insert+"    write_json(run/'run-summary.json'")
ast.parse(src)
(BASE/'evaluator.py').write_text(src)
out('evaluator-preparation.json',{'original_evaluator_sha256':sha(OLD/'evaluator.py'),'goal_evaluator_sha256':sha(BASE/'evaluator.py'),'changes':['Use privacy-reconciled expectation derivative; original expectations remain untouched.','Display commands with shell quoting.','Assert declared core/prompt/data freeze before inference.','Append unchanged held-out mode/coverage cases after original full suite.','Add deterministic scripted reset check.'],'model_calls_during_preparation':0})
print(json.dumps({'expectations':sha(BASE/'expectations.json'),'heldout':sha(BASE/'heldout-expectations.json'),'evaluator':sha(BASE/'evaluator.py'),'model_calls':0}))
