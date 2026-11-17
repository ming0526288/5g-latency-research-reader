#!/usr/bin/env python3
"""Check the new first-step cohort and all 20 page roles, optionally over local HTTP."""
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
    a = ap.parse_args()
    out = dict(status='RUNNING', live=a.live, resources=[],
               scope='Reader bytes, new cohort values, body/TOC/search and role links; no RAN test or browser-cache guarantee')
    opener = build_opener(ProxyHandler({}))
    seen = {}

    def get(name):
        if name in seen:
            return seen[name]
        raw = (ROOT/name).read_bytes()
        if a.live:
            with opener.open(Request(a.base_url.rstrip('/')+'/'+quote(name),
                            headers={'Cache-Control':'no-cache'}), timeout=10) as response:
                assert response.status==200 and response.read()==raw, name
        out['resources'].append(dict(path=name, sha256=hashlib.sha256(raw).hexdigest()))
        seen[name] = raw.decode()
        return seen[name]

    try:
        catalog=json.loads(get('网页/catalog.js').split('window.READER_CATALOG=',1)[1].rstrip(';'))
        data=json.loads(get('说明/研究结果与分析/数据/第一步_槽边界同步修复后_27条件_20261117.json'))
        assert data['unique_runs']==27 and data['complete_transactions']==59400 and data['statistical_transactions']==54000
        assert data['original_formal_runs']==0 and data['conditions']['sync_at_burst_end']==1
        docs=[d for d in catalog['docs'] if d.get('documentRole') and d.get('stepExperiment')]
        assert len(docs)==20 and len({d['id'] for d in docs})==20
        for d in docs:
            assert d['sha256']==hashlib.sha256((ROOT/d['source']).read_bytes()).hexdigest()
            body=json.loads(get('网页/data/'+d['id']+'.js').split('=',1)[1].rstrip(';'))
            assert body['toc'] and '<h1' in body['html'] and d['search']
            for peer in docs:
                if peer['stepExperiment']==d['stepExperiment'] and peer['id']!=d['id']:
                    assert '#/doc/'+peer['id'] in body['html']
            if d['documentRole']=='results':
                number=d['stepExperiment']
                groups=[g for g in data['groups'] if
                    (number==1 and g['tool']=='ping' and g['data_bytes']==56) or
                    (number==2 and g['data_bytes']==16) or
                    (number==3 and g['tool']=='udp' and g['data_bytes']==256) or
                    (number==4 and g['data_bytes'] in [56,256,1200] and g['header_bytes']!=80) or
                    (number==5 and g['tool']=='udp' and g['data_bytes']==256 and g['header_bytes']==16)]
                for g in groups:
                    term=f"{g['pooled']['RTT_ms']['mean']:.3f}"
                    assert term in body['html'] and term in d['search'], (number,term)
                for path in re.findall(r'<img[^>]+src="([^"]+)"',body['html']):
                    get(path)
        command=next(d for d in docs if d['documentRole']=='commands' and d['stepExperiment']==1)
        assert 'sync1.dpdk.conf' in json.loads(get('网页/data/'+command['id']+'.js').split('=',1)[1].rstrip(';'))['html']
        out.update(status='PASS', independentPages=20, uniqueRuns=27, currentComplete=59400,
                   currentStatistical=54000, originalFormalComplete=False, radioTestingRunByThisCheck=False)
    except Exception as e:
        out.update(status='FAIL', error_type=type(e).__name__, error=str(e))
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='resources'},ensure_ascii=False,indent=2))
    return 0 if out['status']=='PASS' else 1


if __name__=='__main__':
    raise SystemExit(main())
