#!/usr/bin/env python3
"""Create a portable local snapshot. Never publishes or uploads anything."""
import argparse,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('destination');a=p.parse_args();dest=Path(a.destination).resolve()
if dest.exists():raise SystemExit('Choose a new directory; existing snapshots are never overwritten.')
dest.mkdir(parents=True)
for name in ['README.md','wiki','wiki.py','sources.json','source-manifest.json','.gitignore','requirements.txt','prompts','evals','scripts','tests','isolation']:
 src=ROOT/name
 if src.is_dir():shutil.copytree(src,dest/name,ignore=shutil.ignore_patterns('__pycache__'))
 else:shutil.copy2(src,dest/name)
# Dereference the working-vault symlink; only source + curated pages + landing pages.
(dest/'vault').mkdir()
for name in ['raw','wiki','index.md','Source Catalog.md']:
 src=ROOT/'vault'/name
 if src.is_dir():shutil.copytree(src,dest/'vault'/name)
 else:shutil.copy2(src,dest/'vault'/name)
# Keep all evidence, including failed runs, except private implementation-state backups.
shutil.copytree(ROOT/'evidence',dest/'evidence',ignore=shutil.ignore_patterns('state-snapshot','__pycache__'))
print('Local review snapshot created at '+str(dest))
print('It includes meeting notes. This command does not grant or imply permission to publish them.')
