#!/usr/bin/env python3
"""Probe the OS restriction without sending application data to the internet."""
import errno,hashlib,json,os,socket,subprocess,sys,threading
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def probe():
    external=[]
    endpoints=[(socket.AF_INET,socket.SOCK_STREAM,('1.1.1.1',443)),
               (socket.AF_INET6,socket.SOCK_STREAM,('2606:4700:4700::1111',443,0,0)),
               (socket.AF_INET,socket.SOCK_DGRAM,('8.8.8.8',53))]
    for family,kind,address in endpoints:
        s=socket.socket(family,kind);s.settimeout(2)
        try:
            if kind==socket.SOCK_DGRAM:s.sendto(b'network-denial-probe',address)
            else:s.connect(address)
            result={'blocked':False,'errno':None}
        except OSError as exc:result={'blocked':exc.errno in (errno.EPERM,errno.EACCES),'errno':exc.errno,'error':exc.strerror}
        finally:s.close()
        external.append({'family':'IPv6' if family==socket.AF_INET6 else 'IPv4','transport':'UDP' if kind==socket.SOCK_DGRAM else 'TCP','destination':str(address),'result':result})
    # Loopback must work. Merely failing every connection is not sufficient.
    server=socket.socket();server.bind(('127.0.0.1',0));server.listen(1);port=server.getsockname()[1]
    def respond():
        conn,_=server.accept()
        with conn:conn.sendall(b'local-only')
        server.close()
    thread=threading.Thread(target=respond);thread.start()
    with socket.create_connection(('127.0.0.1',port),timeout=2) as conn:local_ok=conn.recv(16)==b'local-only'
    thread.join(timeout=2)
    profile=ROOT/'isolation/no-external-network.sb'
    try:wifi=subprocess.check_output(['/usr/sbin/networksetup','-getairportpower','en0'],text=True).strip()
    except (OSError,subprocess.SubprocessError):wifi='unavailable'
    return {'time_utc':datetime.now(timezone.utc).isoformat(),'pid':os.getpid(),'wifi_state':wifi,
            'external_probes':external,'loopback_probe_passed':local_ok,
            'os_denial_verified':all(x['result']['blocked'] for x in external) and local_ok,
            'sandbox_profile_sha256':hashlib.sha256(profile.read_bytes()).hexdigest(),
            'scope':'OS policy denies all non-loopback network operations for this process and inherited children. Probes check IPv4 TCP, IPv6 TCP, UDP and successful local IPC. Wi-Fi can remain connected.'}

def main():
    result=probe();out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
    if not result['os_denial_verified']:sys.exit('External-network denial was not enforced; do not run the model.')

if __name__=='__main__':main()
