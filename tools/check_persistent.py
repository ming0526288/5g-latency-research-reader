"""Check this reader's user service and one controlled automatic recovery."""
import json
import os
from pathlib import Path
import signal
import subprocess
import time
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
NAME='5g-latency-reader.service'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
def command(*args):return subprocess.check_output(args,text=True).strip()
def pid():return int(command('systemctl','--user','show',NAME,'--property=MainPID','--value'))
def http_ok():
    try:
        with opener.open('http://127.0.0.1:8765/index.html',timeout=.5) as response:
            return response.status==200 and response.read()==(ROOT/'index.html').read_bytes()
    except OSError:return False
result={}
try:
    assert command('systemctl','--user','is-active',NAME)=='active'
    assert command('systemctl','--user','is-enabled',NAME)=='enabled'
    assert command('loginctl','show-user',str(os.getuid()),'-p','Linger','--value')=='yes'
    assert http_ok()
    before=pid();argv=Path(f'/proc/{before}/cmdline').read_bytes().split(b'\0')
    assert str(ROOT/'启动阅读站.py').encode() in argv and b'--service' in argv
    os.kill(before,signal.SIGTERM)
    after=0
    for _ in range(50):
        after=pid()
        if after>1 and after!=before and http_ok():break
        time.sleep(.2)
    else:raise AssertionError('service did not recover on the same port')
    result={'status':'PASS','active':'active','enabled':'enabled','linger':'yes','url':'http://127.0.0.1:8765/index.html','http_status':200,'old_pid':before,'new_pid':after,'recovery':'Controlled SIGTERM to verified reader process; systemd restored a new process on port 8765.','browser_open':'Not invoked. Windows browser handoff needs user execution in the VS Code terminal.'}
except BaseException as error:result={'status':'FAIL','error':str(error)}
(ROOT/'校验/常驻与自动恢复校验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(result['status']!='PASS')
