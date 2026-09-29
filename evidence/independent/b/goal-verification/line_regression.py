from pathlib import Path
from types import SimpleNamespace
import errno,hashlib,json,os,shutil,socket,sys
import evaluator as E
B=Path(__file__).resolve().parent;S=Path('<submission>');R=B/'line-regression';W=R/'workspace'
plan=E.read_json(B/'line-regression-plan.json')
assert E.sha(B/'line-regression-plan.json')==(B/'line-regression-plan.sha256').read_text().split()[0]
assert not R.exists(),'Keep earlier runs; choose a new directory for a new authorized run.'
assert os.environ.get('WIKI_NETWORK_POLICY')=='os-enforced-loopback-only'and os.environ.get('WIKI_SERVER_PID')
R.mkdir();probes=[]
for family,address in [(socket.AF_INET,('198.51.100.1',443)),(socket.AF_INET6,('2001:db8::1',443))]:
 for kind in [socket.SOCK_STREAM,socket.SOCK_DGRAM]:
  with socket.socket(family,kind)as p:
   try:p.connect(address);denied=False;err=None
   except OSError as x:denied=x.errno==errno.EPERM;err=x.errno
   probes.append({'family':family,'kind':kind,'denied':denied,'errno':err})
assert all(p['denied']for p in probes)
E.write_json(R/'network-inherited.json',{'probes':probes,'server_pid':os.environ['WIKI_SERVER_PID']})
W.mkdir()
for f in ['wiki.py','wiki','sources.json','source-manifest.json','requirements.txt']:shutil.copy2(S/f,W/f)
for f in ['prompts','vault/raw']:shutil.copytree(S/f,W/f)
(W/'vault/wiki').mkdir()
assert E.sha(W/'wiki.py')==plan['core_sha256']
assert E.sha(W/'prompts/research.md')==plan['research_prompt_sha256']
assert E.sha(W/'prompts/grounded-chat.md')==plan['grounded_chat_prompt_sha256']
assert all(E.sha(W/p)==v for p,v in plan['raw_manifest'].items())
E.write_json(R/'source-freeze.json',{'copied_files':E.hashes(W),'expectations_sha256':E.sha(B/'line-regression-plan.json')})
a=SimpleNamespace(python=sys.executable,launch_prefix_json='[]',no_model_prefix_json='[]');r=E.Runner(a,R,W)
r.command('reindex',['reindex'])
script=R/'required-chat.txt';script.write_text('\n'.join(plan['required_chat_script'])+'\n')
r.command('required-chat',['chat','--script',str(script),'--save-dir',str(R/'required-chat')],timeout=600)
for c in plan['heldout_cases']:
 turns=[x['message']for x in c['turns']]if 'turns'in c else[c['message']]
 r.command(c['id'],['chat','--save-dir',str(R/'heldout-chat'/c['id'])],stdin='\n'.join(turns+['/exit'])+'\n',timeout=600)
shortening_script=R/'source-shortening.txt';shortening_script.write_text('\n'.join(plan['source_shortening']['turns']+['/exit'])+'\n')
r.command('source-shortening-reset',['chat','--script',str(shortening_script),'--save-dir',str(R/'source-shortening')],timeout=600)
r.record('chat-only-codename-search','search',plan['source_only_search'])
r.record('codename-isolation','ask',plan['isolation_question'])
r.record('B01-retrieval','search',plan['representative_ask']['question'])
r.record('B01-research','ask',plan['representative_ask']['question'])
E.write_json(R/'run-summary.json',{'command_count':len(r.commands),'outcomes':[{'label':x['label'],'returncode':x['returncode'],'wall_seconds':x['wall_seconds']}for x in r.commands],'source_bytes_preserved':all(E.sha(W/p)==v for p,v in plan['raw_manifest'].items()),'semantic_verdict':'REQUIRES INDEPENDENT REVIEW'})
print('BOUNDED REGRESSION COMPLETE',flush=True)
