from pathlib import Path
import json
import evaluator as E
B=Path(__file__).resolve().parent;R=B/'line-regression';W=R/'workspace';rows=[];gens=[]
files=sorted((R/'records').glob('*.json'))+sorted((R/'required-chat').glob('*.json'))+sorted((R/'heldout-chat').rglob('*.json'))+sorted((R/'source-shortening').glob('*.json'))
for p in files:
 x=E.read_json(p);refs={r['id']:r for r in x.get('passages',[])}
 cite=[]
 for c in x.get('citations',[]):
  if isinstance(c,dict):cite.append({**c,'exact_quote_correct_id':c['source_id']in refs and c['quote']in refs[c['source_id']]['text']})
  else:cite.append({'source_id':c,'id_exists':c in refs})
 gs=[a['generation']for a in x.get('citation_validation_attempts',[])if 'generation'in a]if x.get('citation_validation_attempts')else([x['generation']]if 'generation'in x else[])
 for g in gs:gens.append({'record':str(p.relative_to(R)),'identity':g['identity'],'seconds':g['metrics']['wall_seconds'],'num_predict':g['request']['options']['num_predict'],'structured':'format'in g['request'],'think':g['request']['think'],'request_message_count':len(g['request']['messages'])})
 rows.append({'record':str(p.relative_to(R)),'question':x.get('question'),'answer':x.get('answer'),'interaction':x['interaction'],'history_messages':x.get('history_messages'),'retrieval_called':x.get('retrieval_called'),'model_calls':len(gs),'citation_errors':x.get('citation_errors'),'source_fidelity':E.verify_passages(x,W),'citations':cite})
E.write_json(B/'LINE_REGRESSION_MECHANICAL.json',{'records':rows,'generations':gens,'generation_count':len(gens)})
for r in rows:
 if r['answer']:print(r['record']+'\n'+r['answer']+'\n'+str({'history':r['history_messages'],'retrieval':r['retrieval_called'],'calls':r['model_calls'],'errors':r['citation_errors']})+'\n')
