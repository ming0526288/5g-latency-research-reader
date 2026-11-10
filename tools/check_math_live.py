#!/usr/bin/env python3
"""Verify all live local paper PDFs against the finalized reader manifest."""
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request

ROOT=Path(__file__).resolve().parents[1]


def main():
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    manifest=json.loads((ROOT/'说明/paper-translations.json').read_text())['papers']
    assert len(manifest)==39
    resources=['网页/catalog.js','网页/paper-translations.js']
    resources += [entry['file'] for entry in manifest.values()]
    checks=[]
    for name in resources:
        request=urllib.request.Request('http://127.0.0.1:8765/'+urllib.parse.quote(name),headers={'Cache-Control':'no-cache'})
        with opener.open(request,timeout=20) as response:
            data=response.read()
            assert response.status==200
            actual=hashlib.sha256(data).hexdigest()
            assert actual==hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),name
            if name.endswith('.pdf'):
                assert data.startswith(b'%PDF-') and response.headers.get_content_type()=='application/pdf'
            checks.append({'file':name,'status':200,'sha256':actual})
    result={'status':'PASS','papers':39,'checks':checks,
            'scope':'Actual existing loopback service GET bytes; no external client or VPN reachability certification'}
    (ROOT/'校验/论文公式修正版在线核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('PASS: actual GET and SHA for 39 translated PDFs and 2 runtime resources')


if __name__=='__main__':
    main()
