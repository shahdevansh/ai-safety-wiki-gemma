from pathlib import Path
import ast,copy,datetime,hashlib,json
B=Path.cwd();old=json.loads((B/'chat-regression-plan.json').read_text());new=copy.deepcopy(old)
new['frozen_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();new['scope']='Same bounded regression on original-line selection design plus explicitly requested source-shortening/reset check; previous plan and c40 failures remain unchanged.'
new['core_sha256']='a00342076c80b8142fd456c842fcc25f11e940a2f2d7e70cfee449cb8a35b444'
new['grounded_chat_prompt_sha256']='d45dc84da09787da9c8af2d4304cafde7698bea8234fcd713c6acc67b81e9ebe'
new['source_shortening']={'turns':['What do my notes say about preferences versus interests?','make that shorter','/reset','what can we do?'],'expected':['First factual answer meets unchanged H3 expectation.','Follow-up uses conversation and original carried evidence; no new retrieval required.','Fewer words than previous answer while retaining supported preference-versus-interest explanation and correct citations.','Reset clears history and source carry; following capability record has zero history, no retrieval, no model call.'],'design_note':'Added before executing the new patch, at parent request to check source-dependent shortening/reset; not an original held-out case.'}
for key in ['required_chat_script','required_chat_expectations','heldout_cases','representative_ask','isolation_question','isolation_expectation','source_only_search','source_only_expectation','raw_manifest']:
 assert old[key]==new[key],key
p=B/'line-regression-plan.json';p.write_text(json.dumps(new,indent=2,ensure_ascii=False)+'\n');(B/'line-regression-plan.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  line-regression-plan.json\n')
s=(B/'chat_regression.py').read_text().replace("R=B/'chat-regression'","R=B/'line-regression'").replace('chat-regression-plan','line-regression-plan')
s=s.replace("assert E.sha(W/'prompts/research.md')==plan['research_prompt_sha256']","assert E.sha(W/'prompts/research.md')==plan['research_prompt_sha256']\nassert E.sha(W/'prompts/grounded-chat.md')==plan['grounded_chat_prompt_sha256']")
s=s.replace("r.record('chat-only-codename-search'","shortening_script=R/'source-shortening.txt';shortening_script.write_text('\\n'.join(plan['source_shortening']['turns']+['/exit'])+'\\n')\nr.command('source-shortening-reset',['chat','--script',str(shortening_script),'--save-dir',str(R/'source-shortening')],timeout=600)\nr.record('chat-only-codename-search'")
ast.parse(s);(B/'line_regression.py').write_text(s)
print('Same prior questions/expectations preserved. New source-shortening/reset case frozen. No model calls.')
