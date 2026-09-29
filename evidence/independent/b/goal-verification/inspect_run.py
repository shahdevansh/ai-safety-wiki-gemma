from pathlib import Path
import hashlib,json,sys
B=Path(__file__).resolve().parent;R=B/'final-run';W=R/'workspace'
files=sorted((R/'records').glob('*.json'))+sorted((R/'chat').glob('*.json'))+sorted((R/'heldout-chat').rglob('*.json'))+sorted((R/'reset-chat').glob('*.json'))
rows=[];generations=[]
for p in files:
 x=json.loads(p.read_text());refs={r['id']:r for r in x.get('passages',[])};fidelity=[];citations=[]
 for r in refs.values():
  f=W/r['path'];fidelity.append({'id':r['id'],'exact_text':''.join(f.read_text().splitlines(keepends=True)[r['line_start']-1:r['line_end']])==r['text'],'hash_matches':hashlib.sha256(f.read_bytes()).hexdigest()==r['source_sha256']})
 for c in x.get('citations',[]):
  if isinstance(c,dict):
   ref=refs.get(c.get('source_id'));citations.append({'claim':c['claim'],'id_and_quote_exact':bool(ref and c.get('quote') in ref['text']),'source_id':c.get('source_id'),'quote':c.get('quote')})
  else:citations.append({'id_exists':c in refs,'source_id':c})
 gs=[a['generation'] for a in x.get('citation_validation_attempts',[]) if 'generation'in a] if x.get('citation_validation_attempts') else ([x['generation']] if 'generation'in x else [a['generation'] for a in x.get('results',[]) if 'generation'in a])
 for g in gs:generations.append({'record':str(p.relative_to(R)),'name':g['identity']['name'],'digest':g['identity']['digest'],'wall_seconds':g['metrics']['wall_seconds'],'done_reason':g['metrics'].get('done_reason'),'endpoint':g['identity']['endpoint']})
 row={'record':str(p.relative_to(R)),'interaction':x['interaction'],'question':x.get('question'),'answer':x.get('answer'),'history_messages':x.get('history_messages'),'retrieval_called':x.get('retrieval_called'),'model_calls_actual_recorded':len(gs),'citation_errors':x.get('citation_errors'),'fidelity':fidelity,'citations':citations}
 rows.append(row)
(B/'mechanical-final-assessment.json').write_text(json.dumps({'records':rows,'generations':generations,'generation_count':len(generations),'all_model_identity_correct':all(g['name']=='gemma4:e2b-it-qat' and g['digest']=='07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c'for g in generations),'all_fidelity_pass':all(f['exact_text'] and f['hash_matches'] for r in rows for f in r['fidelity']),'model_seconds':sum(g['wall_seconds'] for g in generations)},indent=2,ensure_ascii=False)+'\n')
for r in rows:
 if r['answer'] is not None:print(r['record']+'\n'+r['answer']+'\n'+str({'history':r['history_messages'],'retrieval':r['retrieval_called'],'calls':r['model_calls_actual_recorded'],'errors':r['citation_errors']})+'\n')
