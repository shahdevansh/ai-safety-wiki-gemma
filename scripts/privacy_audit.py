#!/usr/bin/env python3
"""Audit publication candidates and reachable Git content for identifying patterns.
A private optional denylist strengthens the generic scan; its values never enter reports.
"""
import argparse,json,re,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--denylist');p.add_argument('--output',default='evidence/privacy/audit.json');a=p.parse_args()
known=json.loads(Path(a.denylist).read_text()) if a.denylist else []
patterns={
 'home_directory':re.compile(r'/(?:Users|home)/[^/\s<>]+',re.I),
 'email_address':re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',re.I),
 'private_meeting_link':re.compile(r'(?:notes\.granola\.ai/d/|granola://meeting/)[a-z0-9-]+',re.I),
 'phone_like':re.compile(r'(?<!\d)(?:\+1[- .]?)?\(?\d{3}\)?[- .]\d{3}[- .]\d{4}(?!\d)'),
 'credential_like':re.compile(r'\b(?:ghp_|github_pat_|sk-proj-)[a-zA-Z0-9_]{12,}')}
# Privacy-scanning source contains intentional pattern literals, not real user data.
excluded={'scripts/privacy_audit.py'}
def scan(data,label):
 try:text=data.decode('utf-8')
 except UnicodeDecodeError:return []
 issues=[]
 for name,pattern in patterns.items():
  for m in pattern.finditer(text):
   if name=='email_address' and m.group().endswith('@users.noreply.github.com'):continue
   issues.append({'file':label,'category':name,'line':text[:m.start()].count('\n')+1})
 for term in known:
  if term.casefold() in text.casefold():issues.append({'file':label,'category':'private_identifier_denylist','identifier_not_disclosed':True})
 return issues
issues=[];files=[]
for path in ROOT.rglob('*'):
 if not path.is_file() or any(part in {'.git','.state','__pycache__'} for part in path.relative_to(ROOT).parts):continue
 rel=path.relative_to(ROOT).as_posix()
 if rel in excluded or path.resolve()==Path(a.output).resolve():continue
 files.append(rel)
def scan_file(rel):return scan((ROOT/rel).read_bytes(),rel)
with ThreadPoolExecutor(max_workers=16) as pool:
 for findings in pool.map(scan_file,files):issues.extend(findings)
history_objects=0
if (ROOT/'.git').exists():
 result=subprocess.run(['git','rev-list','--objects','--all'],cwd=ROOT,capture_output=True,text=True)
 rows=[row.split(' ',1) for row in result.stdout.splitlines()]
 # One Git batch stream retains exact object bytes and avoids a process per blob.
 proc=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 try:
  for row in rows:
   oid=row[0];label=row[1] if len(row)>1 else '(git object)'
   if label in excluded:continue
   proc.stdin.write((oid+'\n').encode());proc.stdin.flush()
   header=proc.stdout.readline().decode().strip().split()
   if len(header)!=3:raise RuntimeError('Cannot read reachable Git object: '+oid)
   _,kind,size=header;data=proc.stdout.read(int(size));separator=proc.stdout.read(1)
   if len(data)!=int(size) or separator!=b'\n':raise RuntimeError('Truncated Git object: '+oid)
   if kind not in {'blob','commit','tag'}:continue
   history_objects+=1;issues.extend(scan(data,'history:'+label))
 finally:
  proc.stdin.close();proc.stdout.close()
  if proc.wait()!=0:raise RuntimeError('Git object scan failed')
report={'passed':not issues,'files_scanned':len(files),'reachable_git_objects_scanned':history_objects,
        'known_identifier_checks':len(known),'issues':issues,
        'scope':'Text/JSON/code and reachable Git blobs/metadata. Images require separate visual review; no regex scan proves absence of every possible indirect identifier.'}
out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if issues:raise SystemExit(1)
