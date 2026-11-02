"""Verify multiple editable accounts using only temporary credentials/listeners."""
from functools import partial
from http.server import ThreadingHTTPServer
import base64
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
def module(name,filename):
    spec=importlib.util.spec_from_file_location(name,ROOT/filename)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value
manager=module('account_manager','常驻阅读站.py');launcher=module('account_server','启动阅读站.py')
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}));steps=[]
def check_http(auth,expected):
    server=ThreadingHTTPServer(('127.0.0.2',0),partial(launcher.reader_handler(launcher.load_access(auth)),directory=str(ROOT)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        for username,password,status in expected:
            header='Basic '+base64.b64encode((username+':'+password).encode()).decode()
            request=urllib.request.Request(f'http://127.0.0.2:{server.server_port}/index.html',headers={'Authorization':header})
            try:
                with opener.open(request,timeout=3) as response:actual=response.status
            except urllib.error.HTTPError as error:actual=error.code
            assert actual==status,(username,actual,status)
    finally:server.shutdown();server.server_close();thread.join(timeout=2)
try:
    with tempfile.TemporaryDirectory(prefix='reader-multiple-accounts-') as td:
        directory=Path(td)/'private';auth=manager.ensure_access(directory);login=directory/'login.json'
        original=json.loads(login.read_text());unchanged=auth.read_bytes();manager.ensure_access(directory);assert auth.read_bytes()==unchanged
        steps.append('旧单账号格式仍可读，重复配置不会随机改口令')
        accounts={'users':[original,{'username':'second-test-reader','password':'temporary-second-secret'}]}
        login.write_text(json.dumps(accounts));manager.ensure_access(directory)
        assert len(json.loads(auth.read_text())['users'])==2
        stable=auth.read_bytes();manager.ensure_access(directory);assert auth.read_bytes()==stable
        check_http(auth,[(original['username'],original['password'],200),('second-test-reader','temporary-second-secret',200),('second-test-reader','incorrect',401),('unknown-user','temporary-second-secret',401)])
        steps.append('两个独立账号各自登录200，错误口令和未知账号401；再次同步不改变口令')
        login.write_text(json.dumps({'users':[accounts['users'][1]]}));manager.ensure_access(directory)
        check_http(auth,[(original['username'],original['password'],401),('second-test-reader','temporary-second-secret',200)])
        steps.append('移除账号后，其旧凭据被拒绝，保留账号仍可登录')
        try:manager.login_users({'users':[accounts['users'][1],accounts['users'][1]]})
        except ValueError:pass
        else:raise AssertionError('duplicate usernames were accepted')
        steps.append('拒绝重复用户名；未读取或修改真实登录配置')
    result={'status':'PASS','steps':steps}
except BaseException as error:result={'status':'FAIL','steps':steps,'error':str(error)}
(ROOT/'校验/多账号配置校验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(result['status']!='PASS')
