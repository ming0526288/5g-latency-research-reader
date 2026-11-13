#!/usr/bin/env python3
"""Read the deployed reader's index, catalogue and diagnosis pages, without credentials."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import ProxyHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', default='http://127.0.0.1:8765/')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    opener = build_opener(ProxyHandler({}))
    report = {'status': 'RUNNING', 'base_url': args.base_url, 'resources': [],
              'scope': 'Live server bytes and routes; does not identify the user browser or diagnose its cache.'}
    try:
        def get(name):
            url = args.base_url.rstrip('/') + '/' + quote(name)
            with opener.open(Request(url, headers={'Cache-Control': 'no-cache'}), timeout=8) as response:
                body = response.read()
                row = {'path': name, 'status': response.status,
                       'sha256': hashlib.sha256(body).hexdigest(),
                       'matches_checkout': body == (ROOT / name).read_bytes(),
                       'cache_control': response.headers.get('Cache-Control', '')}
            report['resources'].append(row)
            assert row['status'] == 200 and row['matches_checkout'], name
            return body.decode('utf-8')

        index = get('index.html')
        get('打开阅读站.html')
        if '网页/bootstrap.js' in index:
            get('网页/bootstrap.js')
        app = get('网页/app.js')
        assert "planningByTopic('original-startup-diagnosis')" in app or "d.topic==='original-startup-diagnosis'" in app
        assert "nav(docUrl(startupDiagnosis),'↗','启动失败原因与排查过程')" in app
        raw = get('网页/catalog.js')
        catalog = json.loads(raw.split('window.READER_CATALOG=', 1)[1].strip().rstrip(';'))
        topic = {doc.get('topic'): doc for doc in catalog['docs'] if doc.get('topic')}
        hub = topic['research-results-index']
        detail = topic['original-startup-diagnosis']
        first = topic['step-1-experiment-1-results']
        pages = {}
        for doc in [hub, detail, first]:
            raw = get('网页/data/' + doc['id'] + '.js')
            pages[doc['id']] = json.loads(raw.split('=', 1)[1].strip().rstrip(';'))
        assert '#/doc/' + detail['id'] in pages[hub['id']]['html']
        assert '#/doc/' + detail['id'] in pages[first['id']]['html']
        for term in ['原因定位与控制变量全过程', '第三次是关键反例', '8703']:
            assert term in pages[detail['id']]['html'], term
        report.update(status='PASS', hub_id=hub['id'], detail_id=detail['id'],
                      detail_title=detail['title'], direct_route='#/doc/' + detail['id'],
                      hub_contains_link=True, first_result_contains_link=True,
                      sidebar_peer_entry_code_served=True)
    except Exception as error:
        report.update(status='FAIL', error_type=type(error).__name__, error=str(error))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report['status'] != 'PASS'


if __name__ == '__main__':
    raise SystemExit(main())
