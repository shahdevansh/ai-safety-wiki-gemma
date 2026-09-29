#!/usr/bin/env python3
"""Record real subprocess output in asciicast v2 and an offline HTML player."""
import html,json,os,pty,select,subprocess,sys,time
from pathlib import Path
out=Path(sys.argv[1]); command=sys.argv[2:];out.parent.mkdir(parents=True,exist_ok=True)
start=time.monotonic();master,slave=pty.openpty()
p=subprocess.Popen(command,stdin=subprocess.DEVNULL,stdout=slave,stderr=slave,close_fds=True)
os.close(slave);events=[]
header={'version':2,'width':110,'height':38,'timestamp':int(time.time()),'env':{'TERM':'xterm-256color'},'title':'Pip local Gemma assignment demonstration','command':' '.join(command)}
with out.open('w') as f:
 f.write(json.dumps(header)+'\n');f.flush()
 while True:
  ready,_,_=select.select([master],[],[],0.2)
  if ready:
   try: data=os.read(master,65536)
   except OSError: break
   if not data:break
   text=data.decode('utf-8',errors='replace');event=[round(time.monotonic()-start,3),'o',text]
   events.append(event);f.write(json.dumps(event)+'\n');f.flush();sys.stdout.write(text);sys.stdout.flush()
  elif p.poll() is not None:break
os.close(master);code=p.wait()
# All text is rendered as textContent: source passages cannot execute HTML or script.
payload=json.dumps(events).replace('<','\\u003c')
page='''<!doctype html><html><head><meta charset="utf-8"><title>Pip terminal evidence</title><style>body{background:#121720;color:#d5ddeb;font:15px system-ui;margin:28px}button{padding:10px;margin-right:8px}pre{white-space:pre-wrap;font:13px/1.5 ui-monospace,monospace;background:#080c12;padding:24px}h1{font-size:25px}</style></head><body><h1>Actual CLI terminal recording</h1><p>Local Gemma • recorded subprocess output • no external resources</p><button id="play">Replay (10×)</button><button id="all">Show full transcript</button><span id="clock"></span><pre id="screen"></pre><script>const events=EVENTS;let timers=[];const screen=document.getElementById('screen');function stop(){timers.forEach(clearTimeout);timers=[]}function all(){stop();screen.textContent=events.map(x=>x[2]).join('')}document.getElementById('all').onclick=all;document.getElementById('play').onclick=()=>{stop();screen.textContent='';events.forEach(e=>timers.push(setTimeout(()=>{screen.textContent+=e[2];document.getElementById('clock').textContent=e[0]+' s';},e[0]*100)))};all();</script></body></html>'''.replace('EVENTS',payload)
out.with_suffix('.html').write_text(page)
out.with_suffix('.txt').write_text(''.join(event[2] for event in events))
sys.exit(code)
