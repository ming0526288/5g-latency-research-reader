#!/usr/bin/env python3
"""Check the startup explanation in body, TOC, search and optional live bytes."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import ProxyHandler, Request, build_opener

ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--live',action='store_true')
    ap.add_argument('--base-url',default='http://127.0.0.1:8765/')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    report={'status':'RUNNING','live':args.live,'resources':[],
            'scope':'Reader content/links/bytes only; no radio testing or user-browser-cache claim.'}
    opener=build_opener(ProxyHandler({}))
    try:
        def get(name):
            body=(ROOT/name).read_bytes()
            if args.live:
                url=args.base_url.rstrip('/')+'/'+quote(name)
                with opener.open(Request(url,headers={'Cache-Control':'no-cache'}),timeout=8) as response:
                    assert response.status==200 and response.read()==body,name
            report['resources'].append({'path':name,'sha256':hashlib.sha256(body).hexdigest(),'matches_checkout':True})
            return body.decode()
        catalog=json.loads(get('网页/catalog.js').split('window.READER_CATALOG=',1)[1].strip().rstrip(';'))
        checks={'step-1-experiment-1-knowledge':['为什么现在能启动','--continuous-tx','18','readFrame','根治','是否需要恢复原始启动方式或源码','启动选项','全部源码'],
                'original-startup-diagnosis':['为什么现在代码能启动','--continuous-tx','18','根治','2026-11-16','未开始 ping'],
                'step-1-experiment-1-results':['2026-11-16','35 s','RTT 未测','2026-11-13'],
                'step-1-experiment-1-commands':['2026-11-16','attempt-01','attempt-02','verify_failed_startups.py']}
        ids=[]
        for topic,terms in checks.items():
            doc=next(d for d in catalog['docs'] if d.get('topic')==topic)
            payload=json.loads(get('网页/data/'+doc['id']+'.js').split('=',1)[1].strip().rstrip(';'))
            for term in terms:
                assert term in payload['html'] and term in doc['search'],(topic,term)
            assert any(terms[0] in h['title'] for h in payload['toc']),topic
            assert doc['sha256']==hashlib.sha256((ROOT/doc['source']).read_bytes()).hexdigest()
            ids.append(doc['id'])
        latest=json.loads((ROOT/'说明/研究结果与分析/数据/第一步_原始程序默认供样复测_20261116.json').read_text())
        assert latest['status']=='VERIFIED_FAILURES_BEFORE_BUSINESS'
        assert latest['natural_attempts']==2 and latest['access_successes']==0
        assert all(not v['continuous_tx_gnb'] and not v['continuous_tx_ue'] and not v['business_started'] and v['RTT_ms'] is None for v in latest['attempts'])
        historical=json.loads((ROOT/'说明/研究结果与分析/数据/第一步_原始程序原核心网复测.json').read_text())
        assert historical['new_complete_transactions']==13320
        report.update(status='PASS',topics=list(checks),document_ids=ids,body_toc_search_match=True,latest_natural_failures=2,latest_business_started=False,historical_transactions_preserved=13320)
    except Exception as e:
        report.update(status='FAIL',error_type=type(e).__name__,error=str(e))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report['status']!='PASS'

if __name__=='__main__':raise SystemExit(main())
