from pathlib import Path
import ast,hashlib,json,os,shutil,subprocess,sys
B=Path(__file__).resolve().parent
S=Path('<submission>')
W=B/'nonmodel-workspace';W.mkdir(exist_ok=False)
for f in ['wiki.py','wiki','sources.json','source-manifest.json','requirements.txt']:shutil.copy2(S/f,W/f)
for f in ['prompts','vault/raw']:shutil.copytree(S/f,W/f)
(W/'vault/wiki').mkdir()
profile=S/'isolation/no-network-at-all.sb'
rows=[]
def run(label,args):
    cmd=['/usr/bin/sandbox-exec','-f',str(profile),sys.executable,'-B',str(W/'wiki.py'),*args]
    p=subprocess.run(cmd,cwd=W,capture_output=True,text=True,timeout=20,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    rows.append({'label':label,'argv':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    return p
run('help',['--help'])
run('reindex',['reindex'])
run('source-only-search-no-network',['search','autonomy','--save',str(B/'nonmodel-search.json')])
script=B/'nonmodel-reset.txt';script.write_text('what can we do?\n/reset\nwhat can you help me with?\n/exit\n')
run('scripted-reset-no-network',['chat','--script',str(script),'--save-dir',str(B/'nonmodel-reset-chat')])
run('online-refused',['ask','Example','--mode','online'])
# This check intentionally makes a real socket attempt under total denial; no stub.
run('ask-denied-no-network',['ask','What are the obstacles to human value alignment?','--save',str(B/'nonmodel-denied-ask.json')])
records=[json.loads(p.read_text()) for p in sorted((B/'nonmodel-reset-chat').glob('*.json'))]
search=json.loads((B/'nonmodel-search.json').read_text())
fidelity=[]
for p in search['passages']:
    f=W/p['path'];actual=''.join(f.read_text().splitlines(keepends=True)[p['line_start']-1:p['line_end']])
    fidelity.append({'id':p['id'],'exact_text':actual==p['text'],'hash':hashlib.sha256(f.read_bytes()).hexdigest()==p['source_sha256']})
result={'network_policy':'macOS deny-all sandbox including loopback; no model stubs','model_generations':0,'commands':rows,'reset':{'two_records':len(records)==2,'history_zero_before_and_after':all(r['history_messages']==0 for r in records),'no_retrieval_or_generation':all(not r['retrieval_called'] and r['model_calls']==0 for r in records)},'search':{'model_calls':search['model_calls'],'passages':len(search['passages']),'fidelity':fidelity},'source_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (W/'vault/raw').glob('*')}}
(B/'nonmodel-assessment.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'commands':[(r['label'],r['returncode']) for r in rows],'reset':result['reset'],'search':result['search']}))
