#!/usr/bin/env python3
"""Read-only checks of new bilingual resources on the existing loopback reader."""
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def main():
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    catalog = json.loads((ROOT/'网页/catalog.js').read_text().split('window.READER_CATALOG=',1)[1].rstrip(';'))
    papers = json.loads((ROOT/'说明/paper-translations.json').read_text())['papers']
    protocols = json.loads((ROOT/'说明/protocol-translations.json').read_text())['papers']
    pdfs = json.loads((ROOT/'校验/协议PDF转换清单.json').read_text())['documents']
    originals = [p for p in catalog['papers'] if p['id'] in ['P36','P37','P38','P39']]
    standard = next(p for p in catalog['protocols'] if p['spec']=='22.104')
    entries = [p['file'] for p in originals] + [papers[p['id']]['file'] for p in originals]
    entries += [pdfs[standard['id']]['file'],protocols[standard['id']]['file']]
    checks = []
    for name in ['网页/app.js','网页/catalog.js','网页/paper-translations.js','网页/protocol-translations.js','网页/protocol-pdfs.js'] + entries:
        is_pdf = name.endswith('.pdf')
        request = urllib.request.Request('http://127.0.0.1:8765/'+urllib.parse.quote(name),method='HEAD' if is_pdf else 'GET')
        with opener.open(request,timeout=15) as response:
            assert response.status==200,(name,response.status)
            assert int(response.headers['Content-Length'])==(ROOT/name).stat().st_size,name
            if is_pdf:
                assert response.headers.get_content_type()=='application/pdf',name
            else:
                assert hashlib.sha256(response.read()).hexdigest()==hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),name
        checks.append({'file':name,'status':200,'method':request.method})
    result={'status':'PASS','checks':checks,'scope':'Existing loopback HTTP resources only; no VPN/client verification or server restart.'}
    (ROOT/'校验/机器人补充资料在线资源核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('PASS:',len(checks),'resources including 10 original/Chinese PDFs')


if __name__=='__main__':
    main()
