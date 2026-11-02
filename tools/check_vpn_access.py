"""Test the actual protected listener using temporary, owned loopback addresses."""
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import select
import signal
import socket
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('reader_manager',ROOT/'常驻阅读站.py')
manager=importlib.util.module_from_spec(spec);spec.loader.exec_module(manager)
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
steps=[]
def request(host,port,path='/index.html',header=None):
    req=urllib.request.Request(f'http://{host}:{port}{path}',headers={'Authorization':header} if header else {})
    try:
        with opener.open(req,timeout=3) as response:return response.status,response.read()
    except urllib.error.HTTPError as error:return error.code,error.read()
try:
    with tempfile.TemporaryDirectory(prefix='reader-vpn-test-') as td:
        directory=Path(td)/'private';auth=manager.ensure_access(directory)
        login=json.loads((directory/'login.json').read_text())
        assert (auth.stat().st_mode&0o777)==0o600
        assert ((directory/'login.json').stat().st_mode&0o777)==0o600
        assert login['password'] not in auth.read_text()
        steps.append('口令哈希与独立登录信息仅写临时私有目录，文件权限0600')
        with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
        process=subprocess.Popen([sys.executable,str(ROOT/'启动阅读站.py'),'--service','--no-open','--port',str(port),'--bind','127.0.0.1','--bind','127.0.0.2','--auth-file',str(auth)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            output=b''
            for _ in range(10):
                ready,_,_=select.select([process.stdout],[],[],3)
                if not ready:raise AssertionError('listener did not start')
                output+=os.read(process.stdout.fileno(),65536)
                if f'127.0.0.2:{port}'.encode() in output:break
            assert request('127.0.0.1',port)[0]==200
            assert request('127.0.0.2',port)[0]==401
            bad='Basic '+base64.b64encode(b'reader:incorrect').decode()
            assert request('127.0.0.2',port,header=bad)[0]==401
            good='Basic '+base64.b64encode((login['username']+':'+login['password']).encode()).decode()
            status,body=request('127.0.0.2',port,header=good)
            assert status==200 and body==(ROOT/'index.html').read_bytes()
            steps.append('原127.0.0.1访问保持200；受保护监听无口令/错误口令401，正确口令200且入口字节不变')
            assert request('127.0.0.2',port,'/.git/config',good)[0]==404
            assert request('127.0.0.2',port,'/%2egit/config',good)[0]==404
            assert request('127.0.0.2',port,'/tools/',good)[0]==404
            assert request('127.0.0.2',port,'/%E7%BD%91%E9%A1%B5/app.js',good)[0]==200
            steps.append('隐藏Git路径和目录列表404；登录后网页资源正常200')
        finally:
            process.send_signal(signal.SIGINT);process.wait(timeout=5)
            assert process.returncode==0,process.stderr.read().decode()
        steps.append('双监听测试进程正常回收，未操作既有常驻服务')
    result={'status':'PASS','steps':steps,'scope':'Uses127.0.0.2 as a protected-listener surrogate. Does not prove the organization VPN permits port8765 or mobile access.'}
except BaseException as error:result={'status':'FAIL','steps':steps,'error':str(error)}
(ROOT/'校验/VPN访问保护校验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(result['status']!='PASS')
