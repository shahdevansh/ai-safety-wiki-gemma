#!/usr/bin/env python3
"""Record non-identifying macOS capacity and available-memory indicators."""
import json,platform,re,shutil,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path

def command(*args):
    return subprocess.check_output(args,text=True).strip()

vm=command('vm_stat');page=int(re.search(r'page size of (\d+)',vm)[1])
memory={}
for label,key in [('Pages free','free_bytes'),('Pages inactive','inactive_bytes'),('Pages speculative','speculative_bytes')]:
    memory[key]=int(re.search(re.escape(label)+r':\s+(\d+)',vm)[1])*page
memory['note']='Free is immediately unused memory. Inactive and speculative pages include reclaimable caches; these are not a single guaranteed available-memory value. CPU/GPU share the installed unified-memory pool.'
pressure=command('memory_pressure','-Q')
match=re.search(r'System-wide memory free percentage:\s*(\d+)%',pressure)
if match:memory['os_reported_free_percentage']=int(match[1])
result={'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'os':command('sw_vers'),'cpu':command('sysctl','-n','machdep.cpu.brand_string'),'unified_memory_bytes':int(command('sysctl','-n','hw.memsize')),'gpu':'Apple Silicon integrated GPU; shared unified memory, no separate dedicated VRAM','python':platform.python_version(),'disk_free_bytes':shutil.disk_usage('.').free,'memory_snapshot':memory}
out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
