#!/usr/bin/env python3
"""Run a command with externally network-isolated Ollama and CLI descendants.
macOS only. The existing desktop Ollama service is untouched.
"""
import argparse,json,os,shutil,signal,socket,subprocess,sys,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--evidence-dir',default='evidence/isolation')
p.add_argument('command',nargs=argparse.REMAINDER)
a=p.parse_args();command=a.command
if command and command[0]=='--':command=command[1:]
if not command:p.error('Supply a command after --, for example -- ./wiki ask "What do the notes say about human override?"')
if sys.platform!='darwin':sys.exit('This wrapper uses macOS sandbox-exec; no weaker fallback is allowed.')
sandbox='/usr/bin/sandbox-exec';ollama=shutil.which('ollama')
if not ollama:sys.exit('Install Ollama and download the model before this isolated run.')
profile=ROOT/'isolation/no-external-network.sb';evidence=Path(a.evidence_dir).resolve();evidence.mkdir(parents=True,exist_ok=True)
private=ROOT/'.state';private.mkdir(exist_ok=True)
port=11435
with socket.socket() as test:
    if test.connect_ex(('127.0.0.1',port))==0:sys.exit('Isolated port already in use; do not silently reuse an unverified server.')
env=dict(os.environ)
for name in ('HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','http_proxy','https_proxy','all_proxy'):env.pop(name,None)
env.update({'OLLAMA_HOST':f'127.0.0.1:{port}','OLLAMA_NO_CLOUD':'1','OLLAMA_MAX_LOADED_MODELS':'1','OLLAMA_NUM_PARALLEL':'1','WIKI_PORT':str(port),'WIKI_NETWORK_POLICY':'os-enforced-loopback-only'})
logpath=private/'isolated-server.log';log=logpath.open('w')
server=subprocess.Popen([sandbox,'-f',str(profile),sys.executable,str(ROOT/'scripts/isolated_server_entry.py'),str(evidence/'server-network.json'),ollama],env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
env['WIKI_SERVER_PID']=str(server.pid)
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}));status=1
try:
    for _ in range(120):
        if server.poll() is not None:raise RuntimeError('Isolated model server exited; inspect private .state/isolated-server.log.')
        try:
            with opener.open(f'http://127.0.0.1:{port}/api/version',timeout=1):break
        except Exception:time.sleep(.25)
    else:raise RuntimeError('Isolated model server did not become ready.')
    # Execute probes and target in one inherited sandbox process tree.
    target=[sandbox,'-f',str(profile),sys.executable,str(ROOT/'scripts/isolated_client_entry.py'),str(evidence/'client-network-before.json'),str(evidence/'client-network-after.json'),*command]
    print('Local-only run: isolated model server and CLI; external network denied, localhost allowed.',flush=True)
    status=subprocess.call(target,env=env,cwd=ROOT)
finally:
    try:os.killpg(server.pid,signal.SIGTERM)
    except ProcessLookupError:pass
    try:server.wait(timeout=10)
    except subprocess.TimeoutExpired:os.killpg(server.pid,signal.SIGKILL);server.wait()
    log.close()
    proof={'server_pid':server.pid,'server_exit_code':server.returncode,'command_exit_code':status,'endpoint':f'http://127.0.0.1:{port}','cloud_disabled':True,'server_and_cli_share_profile':True,'server_launched_fresh':True,'server_stopped_after_run':True,'model_children_inherit_os_sandbox':True}
    (evidence/'run.json').write_text(json.dumps(proof,indent=2)+'\n')
sys.exit(status)
