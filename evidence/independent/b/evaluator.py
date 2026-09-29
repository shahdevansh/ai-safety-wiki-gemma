#!/usr/bin/env python3
"""Independent black-box evaluator B. No importing or editing the submitted harness."""
import argparse, datetime, errno, hashlib, json, os, re, shutil, socket, subprocess, sys, time
from pathlib import Path

BASE=Path(__file__).resolve().parent
EXPECT=BASE/'expectations.json'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write_json(path, obj): path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def hashes(root,glob='**/*'): return {str(p.relative_to(root)):sha(p) for p in sorted(root.glob(glob)) if p.is_file()}
def renamed(path): return path.replace('alignment-lecture-notes.md','alignment-lecture-notes.md')
def read_json(path): return json.loads(path.read_text())
def verify_passages(record,workspace):
    rows=[]
    for p in record.get('passages',[]):
        target=(workspace/p['path']).resolve()
        safe=target.is_relative_to((workspace/'vault/raw').resolve())
        lines=target.read_text().splitlines(keepends=True) if safe and target.is_file() else []
        exact=''.join(lines[p['line_start']-1:p['line_end']]) if lines else None
        rows.append({'id':p['id'],'path':p['path'],'safe_raw_path':safe,'exact_line_match':exact==p['text'],'source_hash_match':safe and target.is_file() and sha(target)==p.get('source_sha256')})
    return rows

def structural(workspace):
    vault=workspace/'vault'; notes=sorted((vault/'wiki').rglob('*.md')); allmd=sorted(vault.rglob('*.md'))
    rows=[]; link_rows=[]
    for p in notes:
        txt=p.read_text(); heading=re.search(r'^# (.+)$',txt,re.M)
        rows.append({'path':str(p.relative_to(vault)),'words':len(p.stem.split()),'heading_match':bool(heading and heading.group(1)==p.stem),'readable_name':bool(re.fullmatch(r'[A-Za-z][A-Za-z -]{2,60}',p.stem)),'has_source_section':'## Source' in txt,'has_related_section':'## Related notes' in txt,'reviewed':'review_status: reviewed' in txt})
    for p in allmd:
        for raw in re.findall(r'\[\[([^\]]+)\]\]',p.read_text()):
            target=raw.split('|')[0].split('#')[0]
            matches=[q for q in allmd if str(q.relative_to(vault).with_suffix(''))==target or q.stem==target]
            link_rows.append({'from':str(p.relative_to(vault)),'target':target,'matches':[str(q.relative_to(vault)) for q in matches],'unambiguous':len(matches)==1})
    return {'note_count':len(notes),'note_paths':[str(p.relative_to(vault)) for p in notes],'notes':rows,'links':link_rows,'all_links_resolve_unambiguously':all(x['unambiguous'] for x in link_rows),'index_exists':(vault/'index.md').is_file(),'source_catalog_exists':(vault/'Source Catalog.md').is_file(),'machine_files_inside_vault':[str(p.relative_to(vault)) for p in vault.rglob('*') if p.is_file() and p.suffix not in {'.md','.txt'}]}

class Runner:
    def __init__(self,args,run,workspace):self.args=args;self.run=run;self.workspace=workspace;self.commands=[]
    def command(self,label,argv,stdin=None,closed=False,timeout=240):
        prefix=json.loads(self.args.no_model_prefix_json if closed else self.args.launch_prefix_json)
        cmd=prefix+[self.args.python,str(self.workspace/'wiki.py')]+argv
        start=time.monotonic(); begun=datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:
            cp=subprocess.run(cmd,cwd=self.workspace,text=True,input=stdin,capture_output=True,timeout=timeout,env=os.environ.copy())
            row={'label':label,'argv':cmd,'cwd':str(self.workspace),'stdin':stdin,'returncode':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr,'started_at_utc':begun,'wall_seconds':round(time.monotonic()-start,3),'network_profile':'no-network-including-model' if closed else 'external-network-denied','timeout':False}
        except subprocess.TimeoutExpired as exc:
            row={'label':label,'argv':cmd,'cwd':str(self.workspace),'stdin':stdin,'returncode':None,'stdout':str(exc.stdout or ''),'stderr':str(exc.stderr or ''),'started_at_utc':begun,'wall_seconds':round(time.monotonic()-start,3),'timeout':True}
        self.commands.append(row);write_json(self.run/'commands'/f'{len(self.commands):02d}-{label}.json',row)
        (self.run/'commands'/f'{len(self.commands):02d}-{label}.txt').write_text('$ '+ ' '.join(cmd)+'\n'+('STDIN:\n'+stdin+'\n' if stdin else '')+row['stdout']+'\nSTDERR:\n'+row['stderr'])
        print(json.dumps({'label':label,'returncode':row['returncode'],'wall_seconds':row['wall_seconds']},ensure_ascii=False),flush=True)
        return row
    def record(self,label,mode,question,closed=False):
        dest=self.run/'records'/f'{label}.json'
        row=self.command(label,[mode,question,'--mode','local','--save',str(dest)],closed=closed)
        return read_json(dest) if dest.exists() else None

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=Path('<submission>'))
    p.add_argument('--python',default=sys.executable)
    p.add_argument('--launch-prefix-json',default='[]',help='Parent-supplied OS isolation prefix; no shell evaluation')
    p.add_argument('--no-model-prefix-json',default='[]',help='Parent-supplied prefix that also blocks loopback for unavailable-server checks')
    p.add_argument('--execute-real-model',action='store_true')
    p.add_argument('--run-name',default='run-'+datetime.datetime.now().strftime('%Y%m%dT%H%M%S'))
    p.add_argument('--restart-check',type=Path,help='Run an additional ask after parent confirms server restart; existing run directory')
    args=p.parse_args()
    if not args.execute_real_model: p.error('No model runs authorized: wait for source freeze and use --execute-real-model with parent-supplied isolation.')
    outer_isolation={}
    if not json.loads(args.launch_prefix_json):
        if os.environ.get('WIKI_NETWORK_POLICY')!='os-enforced-loopback-only' or not os.environ.get('WIKI_SERVER_PID'):
            p.error('Empty launch prefix requires the parent OS-isolated wrapper environment.')
        probes=[]
        for family,address in [(socket.AF_INET,('198.51.100.1',443)),(socket.AF_INET6,('2001:db8::1',443))]:
            for kind in [socket.SOCK_STREAM,socket.SOCK_DGRAM]:
                with socket.socket(family,kind) as probe:
                    probe.settimeout(1)
                    try:probe.connect(address);result={'denied':False,'errno':None}
                    except OSError as exc:result={'denied':exc.errno==errno.EPERM,'errno':exc.errno,'error':str(exc)}
                probes.append({'family':family,'kind':kind,**result})
        if not all(x['denied'] for x in probes):p.error('Inherited external-network denial did not produce EPERM for every TCP/UDP IPv4/IPv6 probe.')
        outer_isolation={'inherited_profile_verified_by_direct_probes':True,'probes':probes,'WIKI_PORT':os.environ.get('WIKI_PORT'),'server_pid':os.environ.get('WIKI_SERVER_PID'),'server_policy_proof':'Parent isolation server-network.json required'}
    expected=read_json(EXPECT)
    if sha(EXPECT)!=(BASE/'expectations.sha256').read_text().split()[0]:raise RuntimeError('Frozen expectations changed')
    if args.restart_check:
        run=args.restart_check.resolve()
        if not run.is_relative_to(BASE):raise ValueError('Writes must stay inside evaluator B directory')
        runner=Runner(args,run/'restart-check',run/'workspace')
        rec=runner.record('B01-after-server-restart','ask',expected['cases'][0]['question'])
        write_json(run/'restart-check'/'summary.json',{'note':'Execution after parent-announced server restart; restart proof is parent-owned and must be linked.','record_saved':bool(rec),'record_model':rec.get('generation',{}).get('identity') if rec else None})
        return
    run=(BASE/args.run_name).resolve()
    if not run.is_relative_to(BASE) or run.exists():raise ValueError('Use a fresh run name within evaluator directory')
    workspace=run/'workspace';workspace.mkdir(parents=True)
    write_json(run/'inherited-isolation-check.json',outer_isolation)
    for rel in ['wiki.py','wiki','requirements.txt','sources.json','source-manifest.json']:
        src=args.source/rel
        if src.exists():shutil.copy2(src,workspace/rel)
    shutil.copytree(args.source/'prompts',workspace/'prompts')
    shutil.copytree(args.source/'vault/raw',workspace/'vault/raw')
    (workspace/'vault/wiki').mkdir()
    reconciliation=[]
    for c in expected['cases']:
        for exp in c['required_passages']:
            path=renamed(exp['source']); txt=(workspace/path).read_text()
            reconciliation.append({'case':c['id'],'original_path':exp['source'],'final_path':path,'expected_exact_passage_present':exp['exact_passage'] in txt,'final_sha256':sha(workspace/path)})
    write_json(run/'source-freeze.json',{'source_project':str(args.source),'copied_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'expectations_sha256':sha(EXPECT),'copied_files':hashes(workspace),'reconciliation':reconciliation,'source_readme_sha256':sha(args.source/'README.md')})
    if not all(x['expected_exact_passage_present'] for x in reconciliation):raise RuntimeError('Privacy/source change altered expected passage; preserve this run and reconcile before model calls')
    source_before=hashes(workspace/'vault/raw');runner=Runner(args,run,workspace)
    runner.command('help-top',['--help'])
    runner.command('help-command',['help'])
    runner.command('missing-ingest-path',['ingest','./does-not-exist'])
    runner.command('fresh-no-index',['search','autonomy'])
    runner.command('fresh-ingest',['ingest','./vault/raw','--save',str(run/'records'/'fresh-ingest.json')],timeout=600)
    if not (workspace/'.state/index.sqlite3').exists():
        write_json(run/'early-failure.json',{'reason':'Fresh documented ingestion did not create persisted index','commands':runner.commands});return
    write_json(run/'structural-after-ingest.json',structural(workspace))
    runner.record('assignment-search','search','workshop location')
    runner.record('topic-search','search','autonomy')
    cases=[]
    for c in expected['cases']:
        search=runner.record(c['id']+'-retrieval','search',c['question'])
        answer=runner.record(c['id'],'ask',c['question'])
        retrieval_expected=[]
        for exp in c['required_passages']:
            # Full expected span may cross chunks: inspect overlap and exact underlying source evidence separately.
            matches=[x for x in (search or {}).get('passages',[]) if x['path']==renamed(exp['source']) and any(line.strip() and line.strip() in x['text'] for line in exp['exact_passage'].splitlines())]
            retrieval_expected.append({'expected_source':renamed(exp['source']),'matching_passage_ids':[x['id'] for x in matches],'match_is_candidate_not_semantic_verdict':True})
        cites=[]
        for citation in (answer or {}).get('citations',[]):
            if isinstance(citation,dict):
                refs={x['id']:x for x in answer.get('passages',[])};ref=refs.get(citation.get('source_id'))
                cites.append({'claim':citation.get('claim'),'source_id':citation.get('source_id'),'quote':citation.get('quote'),'id_and_quote_valid':bool(ref and citation.get('quote') and citation['quote'] in ref['text'])})
        cases.append({'id':c['id'],'question':c['question'],'expected_claims':c['expected_claims'],'retrieval_source_candidates':retrieval_expected,'retrieval_fidelity':verify_passages(search or {},workspace),'answer_fidelity':verify_passages(answer or {},workspace),'answer':(answer or {}).get('answer'),'citations':cites,'model_identity':(answer or {}).get('generation',{}).get('identity'),'citation_errors':(answer or {}).get('citation_errors'),'history_messages':(answer or {}).get('history_messages'),'semantic_verdict':'REQUIRES INDEPENDENT REVIEW'})
        write_json(run/'mechanical-case-assessment.json',cases)
    chat_turns=['what can we do?','what can you help me with?','Suggest a three-step plan for turning my reading notes into a one-page study guide.','make that shorter','According to my notes, what are the two main obstacles to aligning AI to general human values?','For this conversation only, my next AI safety workshop is on 17 March 2031 at 09:37 in Room Z-814. Please acknowledge this as an unverified hypothetical.','/exit']
    runner.command('interactive-chat',['chat','--save-dir',str(run/'chat')],stdin='\n'.join(chat_turns)+'\n',timeout=600)
    runner.record('B04-after-chat','ask',expected['cases'][3]['question'])
    runner.record('chat-fact-not-indexed','search','Z-814')
    runner.record('assignment-ask','ask','Where is the workshop?')
    notes_before=hashes(workspace/'vault/wiki');runner.command('unchanged-reingest',['ingest','./vault/raw','--save',str(run/'records'/'reingest.json')])
    notes_after=hashes(workspace/'vault/wiki')
    write_json(run/'reingestion-assessment.json',{'source_hashes_before':source_before,'source_hashes_after':hashes(workspace/'vault/raw'),'originals_unchanged':source_before==hashes(workspace/'vault/raw'),'note_hashes_before':notes_before,'note_hashes_after':notes_after,'same_note_paths':notes_before.keys()==notes_after.keys(),'notes_byte_identical':notes_before==notes_after,'structure':structural(workspace)})
    runner.record('B01-after-cli-restart','ask',expected['cases'][0]['question'])
    runner.command('invalid-online-mode',['ask','What do the notes say?','--mode','online'])
    if json.loads(args.no_model_prefix_json):
        runner.record('search-without-model','search','autonomy',closed=True)
        runner.record('ask-without-model','ask',expected['cases'][0]['question'],closed=True)
    else:
        write_json(run/'unavailable-model-NOT-RUN.json',{'reason':'No OS prefix that denies loopback was provided; did not edit endpoint or stub model'})
    write_json(run/'run-summary.json',{'command_count':len(runner.commands),'command_outcomes':[{'label':x['label'],'returncode':x['returncode'],'wall_seconds':x['wall_seconds']} for x in runner.commands],'source_unchanged':source_before==hashes(workspace/'vault/raw'),'isolation_prefix':json.loads(args.launch_prefix_json),'server_isolation_proof':'Must be supplied by parent; evaluator prefix alone does not prove model server isolation.','model_server_restart':'NOT YET VERIFIED; use --restart-check after parent-controlled restart','semantic_verdict':'REQUIRES INDEPENDENT REVIEW'})
    print('RUN COMPLETE '+str(run),flush=True)
if __name__=='__main__':main()
