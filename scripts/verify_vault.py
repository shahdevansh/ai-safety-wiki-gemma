#!/usr/bin/env python3
"""Check curated links, heading/title identity, original hashes and source isolation."""
import argparse,json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import wiki
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--allow-pending',action='store_true',help='Inspect freshly generated drafts before editorial review')
args=parser.parse_args()
vault=wiki.ROOT/'vault'; errors=[]; checks=[]
all_files=list(vault.rglob('*.md'))
for e in wiki.catalog():
 path=vault/'wiki'/e['folder']/(e['title']+'.md')
 if not path.exists():errors.append('Missing '+str(path));continue
 text=path.read_text()
 if '# '+e['title']+'\n' not in text:errors.append('Heading mismatch '+e['title'])
 if 'source_sha256: '+wiki.digest((wiki.ROOT/e['path']).read_bytes()) not in text:errors.append('Source hash mismatch '+e['title'])
 if not re.search(r'## Related notes\s+.*?\[\[',text,re.S):errors.append('Missing meaningful links '+e['title'])
 if 'review_status: reviewed' not in text and not args.allow_pending:errors.append('Editorial review pending: '+e['title'])
 checks.append({'title':e['title'],'reviewed':'review_status: reviewed' in text})
for path in [vault/'index.md',vault/'Source Catalog.md',*list((vault/'wiki').rglob('*.md'))]:
 for target in re.findall(r'\[\[([^]|]+)(?:\|[^]]*)?\]\]',path.read_text()):
  target=target.split('#')[0]
  hits=[p for p in all_files if (p.relative_to(vault).with_suffix('').as_posix()==target if '/' in target else p.stem==target)]
  if len(hits)!=1:errors.append(f'{path.name}: {target} resolves to {len(hits)} notes')
original=json.loads((wiki.ROOT/'source-manifest.json').read_text())
for path,expected in original.items():
 if wiki.digest((wiki.ROOT/path).read_bytes()) != expected:errors.append('Original export changed: '+path)
# Only the eight original passages are in the searchable index.
import sqlite3
with sqlite3.connect(wiki.STATE/'index.sqlite3') as db:
 paths=[x[0] for x in db.execute('SELECT DISTINCT path FROM passages')]
 count=db.execute('SELECT count(*) FROM passages').fetchone()[0]
allowed=sorted({e['path'] for e in wiki.catalog()})
if sorted(paths)!=allowed:errors.append('Searchable paths differ from registered originals')
print(json.dumps({'passed':not errors,'errors':errors,'curated_note_count':len(checks),'original_source_count':len(allowed),'passage_count':count,'pages':checks,'source_paths':paths},indent=2))
if errors:sys.exit(1)
