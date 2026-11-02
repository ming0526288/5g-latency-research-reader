"""Verify local deployment; never prints the reader's access secret."""
import base64
import json
from pathlib import Path
import subprocess
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
CONFIG=Path.home()/'.config/5g-latency-reader'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
def get(host,header=None,path='/index.html'):
    req=urllib.request.Request('http://'+host+':8765'+path,headers={'Authorization':header} if header else {})
    try:
        with opener.open(req,timeout=3) as r:return r.status,r.read()
    except urllib.error.HTTPError as e:return e.code,e.read()
try:
    data=json.loads((CONFIG/'login.json').read_text());login=data['users'][0] if 'users' in data else data
    token='Basic '+base64.b64encode((login['username']+':'+login['password']).encode()).decode()
    assert get('127.0.0.1')[0]==200
    assert get('10.29.156.152')[0]==401
    status,body=get('10.29.156.152',token)
    assert status==200 and body==(ROOT/'index.html').read_bytes()
    assert get('10.29.156.152',token,'/.git/config')[0]==404
    for name in ['access.json','login.json','service.json']:
        assert ((CONFIG/name).stat().st_mode&0o777)==0o600
    ss=subprocess.check_output(['ss','-ltn','sport = :8765'],text=True)
    assert '127.0.0.1:8765' in ss and '10.29.156.152:8765' in ss
    assert '0.0.0.0:8765' not in ss
    result={'status':'PASS','loopback_http':200,'private_address_unauthenticated':401,'private_address_authenticated':200,'hidden_git_path':404,'listens':['127.0.0.1:8765','10.29.156.152:8765'],'credential_file_modes':'0600; outside repository','client_8765_test':'not yet received','scope':'Server-side probe only. User has confirmed aTrust TCP22 succeeds; TCP8765 and phone entitlement remain to verify.'}
except BaseException as error:result={'status':'FAIL','error':str(error)}
(ROOT/'校验/VPN部署本机校验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(result['status']!='PASS')
