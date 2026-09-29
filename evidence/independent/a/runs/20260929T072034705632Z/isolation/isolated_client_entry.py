#!/usr/bin/env python3
"""Prove client restrictions before and after executing the inherited CLI tree."""
import json,subprocess,sys
from pathlib import Path
from network_guard import probe
before,after=map(Path,sys.argv[1:3]);command=sys.argv[3:]
def save(path):
 result=probe();path.write_text(json.dumps(result,indent=2)+'\n')
 if not result['os_denial_verified']:sys.exit('Client OS network denial failed.')
 print('Network guard: external IPv4/IPv6 TCP and UDP denied; loopback works.',flush=True)
save(before)
code=subprocess.call(command)
save(after)
sys.exit(code)
