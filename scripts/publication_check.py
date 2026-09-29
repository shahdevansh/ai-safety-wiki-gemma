#!/usr/bin/env python3
"""Follow local Markdown links from the README and verify final vault integrity."""
import json,re,subprocess,sys,urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
missing=[]
pending=[ROOT/'README.md'];seen=set()
while pending:
 p=pending.pop().resolve()
 if p in seen:continue
 seen.add(p)
 if not p.exists():missing.append(str(p.relative_to(ROOT)));continue
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in link or link.startswith('#'):continue
  target=(p.parent/urllib.parse.unquote(link.split('#')[0])).resolve()
  if not target.is_relative_to(ROOT):
   missing.append(str(p.relative_to(ROOT))+': outside repository: '+link)
  elif not target.exists():missing.append(str(p.relative_to(ROOT))+':'+link)
  elif target.suffix=='.md' and target.is_file():pending.append(target)
check=subprocess.run([sys.executable,'scripts/verify_vault.py'],cwd=ROOT,capture_output=True,text=True)
print(json.dumps({'readme_links_pass':not missing,'markdown_files_followed':len(seen),'missing':missing,'vault_checks_pass':check.returncode==0},indent=2))
if missing or check.returncode:raise SystemExit(1)
