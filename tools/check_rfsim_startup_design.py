#!/usr/bin/env python3
"""Verify the independent RFsim design page, its image, links and optional live bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import quote
from urllib.request import ProxyHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--live', action='store_true')
    ap.add_argument('--base-url', default='http://127.0.0.1:8765/')
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    report = dict(status='RUNNING', live=args.live, resources=[],
                  scope='Page, navigation, formula markup and numeric evidence boundaries; no new RAN trial')
    opener = build_opener(ProxyHandler({}))

    def get(name):
        local = (ROOT / name).read_bytes()
        if args.live:
            with opener.open(Request(args.base_url.rstrip('/') + '/' + quote(name),
                            headers={'Cache-Control': 'no-cache'}), timeout=8) as response:
                actual = response.read()
            assert actual == local, name
        report['resources'].append(dict(path=name, sha256=hashlib.sha256(local).hexdigest(),
                                        matches_checkout=True))
        return local.decode()

    try:
        catalog = json.loads(get('网页/catalog.js').split('window.READER_CATALOG=', 1)[1].rstrip(';'))
        doc = next(d for d in catalog['docs'] if d.get('topic') == 'rfsim-startup-sync-design')
        assert doc['status'] == 'implemented-startup-validated'
        assert not doc.get('researchStep') and not doc.get('stepExperiment')
        content = json.loads(get('网页/data/' + doc['id'] + '.js').split('=', 1)[1].rstrip(';'))
        assert doc['sha256'] == hashlib.sha256((ROOT / doc['source']).read_bytes()).hexdigest()
        for term in ['循环等待', '方案 A', '方案 B', '真实射频', 'C 实现已完成']:
            assert term in content['html'] and term in doc['search'], term
        assert any('真实射频' in h['title'] for h in content['toc'])
        assert 'katex' in content['html']
        images = re.findall(r'<img[^>]+src="([^"]+)"', content['html'])
        assert len(images) == 1
        svg = get(images[0]); assert '<svg' in svg and 'dummyWrite' in svg
        app = get('网页/app.js')
        assert "const startupSync=C.docs.find(d=>d.topic==='rfsim-startup-sync-design')" in app
        assert "current===startupSync" in app and "'RFsim 启动同步方案'" in app
        for topic in ['research-results-index', 'step-1-experiment-1-knowledge', 'step-1-experiment-1-results']:
            other = next(d for d in catalog['docs'] if d.get('topic') == topic)
            payload = json.loads(get('网页/data/' + other['id'] + '.js').split('=', 1)[1].rstrip(';'))
            assert '#/doc/' + doc['id'] in payload['html']
        startup=json.loads(get('说明/研究结果与分析/数据/RFsim突发末同步_启动验证_20261117.json'))
        assert len(startup['on_cases'])==4 and all(c['registered'] for c in startup['on_cases'])
        assert all(c['activated']['kind']=='mixed' for c in startup['on_cases'])
        report.update(status='PASS', id=doc['id'], body_toc_search_match=True,
                      declared_implemented=True, startup_checks_passed=4,
                      sibling_entry=True, image=images[0])
    except Exception as e:
        report.update(status='FAIL', error_type=type(e).__name__, error=str(e))
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
