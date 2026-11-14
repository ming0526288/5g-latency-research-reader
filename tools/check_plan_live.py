#!/usr/bin/env python3
"""Verify deployed planning catalogue and payload bytes without credentials."""
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
    report = {'status': 'RUNNING', 'base_url': args.base_url, 'resources': [],
              'scope': 'Live byte/source agreement only; not user browser cache verification or radio testing.'}
    opener = build_opener(ProxyHandler({}))
    try:
        def get(name):
            with opener.open(Request(args.base_url.rstrip('/') + '/' + quote(name),
                                     headers={'Cache-Control': 'no-cache'}), timeout=8) as response:
                body = response.read()
                report['resources'].append({'path': name, 'status': response.status,
                                            'sha256': hashlib.sha256(body).hexdigest(),
                                            'matches_checkout': body == (ROOT / name).read_bytes()})
                assert response.status == 200 and body == (ROOT / name).read_bytes(), name
            return body.decode('utf-8')
        raw = get('网页/catalog.js')
        catalog = json.loads(raw.split('window.READER_CATALOG=', 1)[1].rstrip(';'))
        topics = {doc.get('topic'): doc for doc in catalog['docs'] if doc.get('topic')}
        checks = {'algorithm-experiment-plan': ['0.1024', '0.3072', '优先核验授权时机'],
                  'paper-plan': ['通信 RTT', '同预算非预测主动授权'],
                  'step-2-plan': ['R/N', 'Nr', '0.1024'],
                  'step-5-plan': ['第二步'], 'step-6-plan': ['第二步'],
                  'step-7-plan': ['两条对照轴'], 'step-8-plan': ['优先关注的授权时机']}
        for topic, terms in checks.items():
            doc = topics[topic]
            payload = json.loads(get('网页/data/' + doc['id'] + '.js').split('=', 1)[1].rstrip(';'))
            for term in terms:
                assert term in payload['html'] and term in doc['search'], (topic, term)
        assert catalog['readingNoteUpdatedAt'] == '2026-11-14'
        report.update(status='PASS', checked_topics=list(checks), search_and_body_agree=True)
    except Exception as error:
        report.update(status='FAIL', error_type=type(error).__name__, error=str(error))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report['status'] != 'PASS'


if __name__ == '__main__':
    raise SystemExit(main())
