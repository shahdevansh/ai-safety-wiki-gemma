from pathlib import Path
import hashlib, json, datetime
project=Path('<submission>')
out=Path('<evaluation>')
def passage(path,start,end):
    text=(project/path).read_text()
    return {'source':path,'lines_at_design':[start,end],'exact_passage':'\n'.join(text.splitlines()[start-1:end]),'source_sha256_at_design':hashlib.sha256(text.encode()).hexdigest()}
cases=[
 {'id':'B01-values','kind':'answerable-direct','question':'Which two obstacles do the alignment notes identify when aligning AI to general human values?', 'expected_claims':['Western/English skew in outputs','No consensus on the human values to target'], 'required_passages':[passage('vault/raw/alignment-fundamentals-notes.md',27,30)],'forbidden_claims':['A consensus value system is already solved','Universal general human values are known']},
 {'id':'B02-mountaintop','kind':'answerable-paraphrase','question':'Why might taking someone straight to the mountaintop fail to respect what they want from the climb?', 'expected_claims':['Agency, process, striving or achievement matter in addition to the final outcome','Removing non-optimal choices can violate autonomy'], 'required_passages':[passage('vault/raw/alignment-lecture-notes.md',39,43)],'forbidden_claims':['The notes establish a literal mountaineering safety recommendation','An optimal final outcome makes agency irrelevant']},
 {'id':'B03-oversight','kind':'answerable-comparison','question':'How do the notes contrast the ICAO/IMO and IAEA approaches to AI oversight?', 'expected_claims':['ICAO/IMO regulates national regulators and is less intrusive','IAEA has direct inspection powers including entering facilities and seizing files','Stronger inspection is politically harder'], 'required_passages':[passage('vault/raw/alignment-lecture-notes.md',52,54)],'forbidden_claims':['The IAEA currently has legal AI inspection authority','The described governance proposal has already been enacted']},
 {'id':'B04-next-workshop','kind':'missing-evidence','question':'What is the date, start time, and room number of the next AI safety workshop?', 'expected_claims':['Explicitly says the source evidence is insufficient or does not contain the requested details'],'required_passages':[],'forbidden_claims':['A specific calendar date, start time, room, organizer contact or external lookup stated as known']},
 {'id':'B05-two-source','kind':'answerable-cross-source-stress','question':'According to these notes, how do cultural skew and preference manipulation complicate deciding whose interests an AI should serve?', 'expected_claims':['General human value alignment can be Western/English-skewed and lacks consensus','Observed or stated preferences can be manipulated or shaped against interests','Multiple people can have conflicting interests'], 'required_passages':[passage('vault/raw/alignment-fundamentals-notes.md',27,34),passage('vault/raw/alignment-lecture-notes.md',33,38)], 'forbidden_claims':['A complete solution to aggregation or pluralistic alignment is already established']}
]
obj={'evaluator':'B','frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'basis':'Assignment and original raw files only. No evals/, evidence/, existing tests, implementation, README or evaluator A contents read before this freeze. Directory inventory exposed filenames but not contents.','cases':cases}
p=out/'expectations.json'
if p.exists():raise SystemExit('Refusing to overwrite frozen expectations')
p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
(out/'expectations.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'  expectations.json\n')
