#!/usr/bin/env python3
"""Verify preview bytes on the existing loopback reader; does not start services."""
from pathlib import Path
import json
from urllib.request import build_opener, ProxyHandler, Request
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]


def main():
    opener = build_opener(ProxyHandler({}))
    checks = []
    for name in ['网页/app.js', '网页/protocol-pdfs.js', '网页/data/kc3e4e8560cabef23.js']:
        request = Request('http://127.0.0.1:8765/'+quote(name)+'?check=protocol-pdf',
                          headers={'Cache-Control':'no-cache'})
        with opener.open(request, timeout=15) as response:
            assert response.status == 200
            assert response.read() == (ROOT/name).read_bytes(), name
        checks.append({'file':name, 'http_status':200, 'matches_local_bytes':True})
    data = json.loads((ROOT/'校验/协议PDF转换清单.json').read_text())
    for pdf in data['documents'].values():
        request = Request('http://127.0.0.1:8765/'+quote(pdf['file']), method='HEAD')
        with opener.open(request, timeout=15) as response:
            assert response.status == 200
            assert int(response.headers['Content-Length']) == pdf['bytes']
            assert response.headers.get_content_type() == 'application/pdf'
        checks.append({'file':pdf['file'], 'http_status':200,
                       'content_type':'application/pdf', 'bytes':pdf['bytes']})
    result = {'status':'PASS', 'checks':checks,
              'scope':'Live loopback resources; not a remote client/VPN access check.'}
    (ROOT/'校验/协议PDF在线显示资源核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('PASS live resources:',len(checks),'including',len(data['documents']),'PDF HEAD responses')


if __name__ == '__main__':
    main()
