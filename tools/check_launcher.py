"""Exercise the actual launcher on owned loopback servers; never opens a browser."""
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
import json
import os
from pathlib import Path
import select
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
steps=[]
def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1',0));return s.getsockname()[1]
def start(port):
    p=subprocess.Popen([sys.executable,str(ROOT/'启动阅读站.py'),'--port',str(port),'--no-open'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        buffered=''
        for _ in range(4):
            ready,_,_=select.select([p.stdout],[],[],5)
            if not ready:raise AssertionError('launcher did not print a ready address')
            buffered+=os.read(p.stdout.fileno(),65536).decode('utf-8',errors='replace')
            for line in buffered.splitlines():
                if line.startswith('http://'):return p,line.strip()
        raise AssertionError('no URL from launcher')
    except BaseException:
        p.terminate();p.wait(timeout=5);raise
def stop(p):
    p.send_signal(signal.SIGINT);p.wait(timeout=5)
    assert p.returncode==0,p.stderr.read()
try:
    port=free_port();p,url=start(port)
    try:
        with opener.open(url,timeout=3) as response:actual=response.read()
        assert hashlib.sha256(actual).digest()==hashlib.sha256((ROOT/'index.html').read_bytes()).digest()
        steps.append('启动实际脚本后HTTP200，入口字节与仓库一致')
        reused=subprocess.run([sys.executable,str(ROOT/'启动阅读站.py'),'--port',str(port),'--no-open'],capture_output=True,text=True,timeout=5)
        assert reused.returncode==0 and '已在运行' in reused.stdout
        assert p.poll() is None
        steps.append('重复执行复用同一个阅读服务，不报端口占用、不启动第二份服务')
    finally:stop(p)
    steps.append('Ctrl+C对应SIGINT使自建服务正常退出，exit0')
    with tempfile.TemporaryDirectory(prefix='reader-launcher-') as td:
        Path(td,'index.html').write_text('Unrelated temporary test server')
        foreign=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=td))
        thread=threading.Thread(target=foreign.serve_forever,daemon=True);thread.start()
        try:
            port=foreign.server_port;p,url=start(port)
            try:
                assert f':{port}/' not in url
                with opener.open(url,timeout=3) as response:assert response.status==200
                with opener.open(f'http://127.0.0.1:{port}/index.html',timeout=3) as response:assert b'Unrelated' in response.read()
                steps.append('不相关端口被占用时自动选择后续端口，原测试服务不受影响')
            finally:stop(p)
        finally:foreign.shutdown();foreign.server_close()
    result={'status':'PASS','steps':steps,'browser_open':'not invoked: --no-open; Remote CLI flag verified in installed server-cli.js; actual local browser handoff awaits user execution'}
except BaseException as error:
    result={'status':'FAIL','steps':steps,'error':str(error)}
(ROOT/'校验/一键启动校验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
sys.exit(result['status']!='PASS')
