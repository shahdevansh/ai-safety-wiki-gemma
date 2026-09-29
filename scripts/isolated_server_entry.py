#!/usr/bin/env python3
"""Prove restrictions in this PID, then exec the local model server under them."""
import json,os,sys
from pathlib import Path
from network_guard import probe
result=probe();dest=Path(sys.argv[1]);dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(json.dumps(result,indent=2)+'\n')
if not result['os_denial_verified']:sys.exit('Server network sandbox failed; refusing model startup.')
print('External-network denial verified in server PID before exec.',flush=True)
os.execv(sys.argv[2],[sys.argv[2],'serve'])
