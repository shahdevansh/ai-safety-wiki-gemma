from pathlib import Path
import json,datetime
import evaluator as E
B=Path(__file__).resolve().parent;R=B/'chat-regression';m=E.read_json(B/'CHAT_REGRESSION_MECHANICAL.json');rows={r['record']:r for r in m['records']}
source_cases=[]
for f in ['required-chat/chat-06.json','heldout-chat/H3-topic-transition/chat-01.json']:
 x=E.read_json(R/f);refs={p['id']:p for p in x['passages']};attempts=[]
 for a in x['citation_validation_attempts']:
  p=json.loads(a['raw_model_answer']);failures=[]
  for c in p.get('claims',[]):
   for s in c['supports']:
    if s['quote']not in refs.get(s['source_id'],{}).get('text',''):
     failures.append({'claim':c['text'],'source_id':s['source_id'],'quote':s['quote'],'exact_quote_found_in_other_retrieved_ids':[k for k,v in refs.items()if s['quote']in v['text']]})
  attempts.append({'errors':a['citation_errors'],'failed_supports':failures,'seconds':a['generation']['metrics']['wall_seconds']})
 source_cases.append({'record':f,'question':x['question'],'verdict':'FAIL: evidence was retrieved, but no usable grounded answer displayed after failed validation and repair','answer':x['answer'],'history_messages':x['history_messages'],'attempts':attempts})
report={'reviewed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'core_sha256':E.sha(R/'workspace/wiki.py'),'scope':'Bounded affected-path regression only. Prior full-suite results are not relabelled as results on this new core.','command_count':E.read_json(R/'run-summary.json')['command_count'],'actual_model_generations':m['generation_count'],'all_model_tag_digest_correct':all(g['identity']['name']=='gemma4:e2b-it-qat'and g['identity']['digest']=='07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c'for g in m['generations']),'all_retrieved_line_hash_fidelity_pass':all(p['exact_line_match']and p['source_hash_match']and p['safe_raw_path']for r in m['records']for p in r['source_fidelity']),'required_source_chat':'FAIL','H2_capability_paraphrase':'PASS: accurate deterministic contract, zero model/retrieval, includes all implemented commands and no web search','H3_topic_transition':'PARTIAL overall: first source question FAILS; subsequent unrelated three-name suggestion PASSES','representative_B01_ask':'PASS: both skew and no consensus, correct source quotes, no history','codename_isolation':'PASS: ask abstains with no history; search returns no matching passage','draft_followup':{'verdict':'PASS','draft_words':len(rows['required-chat/chat-03.json']['answer'].split()),'shorter_words':len(rows['required-chat/chat-04.json']['answer'].split()),'retained_plan':'Three steps; 5/20/5 minutes total 30.'},'grounded_chat_failures':source_cases,'isolation':E.read_json(B/'chat-regression-isolation/run.json'),'unretested_limitations':['B05 two-source completeness','H4 coordination detail','Broader unseen capability paraphrases'],'confidence':'High for observed output and direct support checks; no reliability/grade extrapolation.'}
E.write_json(B/'CHAT_REGRESSION_ASSESSMENT.json',report)
print(json.dumps({'commands':report['command_count'],'generations':report['actual_model_generations'],'required_source_chat':'FAIL','H2':'PASS','H3':'PARTIAL source FAIL/topic PASS','B01':'PASS','isolation':'PASS'}))
