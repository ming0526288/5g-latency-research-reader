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
            for term in ['348','0.834','直接','--continuous-tx']:
                assert term in payload['html'] and term in doc['search'],(topic,term)
            assert '2.358' in payload['html'] and '2.358' in doc['search'],topic
            if topic=='step-1-experiment-1-knowledge':
                for term in ['依次启动与等待接入','根本没有执行 ping','影响尚未单因素隔离','正式时延统计预热']:
                    assert term in payload['html'] and term in doc['search'],(topic,term)
                assert any('依次启动与等待接入' in h['title'] for h in payload['toc'])
            assert any(terms[0] in h['title'] for h in payload['toc']),topic
            assert doc['sha256']==hashlib.sha256((ROOT/doc['source']).read_bytes()).hexdigest()
            ids.append(doc['id'])
        latest=json.loads((ROOT/'说明/研究结果与分析/数据/第一步_原始程序默认供样复测_20261116.json').read_text())
        assert latest['status']=='VERIFIED_FAILURES_BEFORE_BUSINESS'
        assert latest['natural_attempts']==2 and latest['access_successes']==0
        assert all(not v['continuous_tx_gnb'] and not v['continuous_tx_ue'] and not v['business_started'] and v['RTT_ms'] is None for v in latest['attempts'])
        direct=json.loads((ROOT/'说明/研究结果与分析/数据/第一步_原命令直接启动复测_20261116.json').read_text())
        assert direct['status']=='ORIGINAL_DIRECT_COMMAND_PING_SUCCESS'
        assert not direct['continuous_tx_gnb'] and not direct['continuous_tx_ue']
        assert direct['ping']['transmitted']==direct['ping']['received']==direct['ping']['all_reply_lines']==348
        assert direct['ping']['avg_ms']==0.834 and direct['ping']['max_ms']==1.251
        assert direct['ping']['warmup_removed']==0 and direct['ping']['p99_9_ms'] is None
        assert direct['original_runtime_file_check']=={'files':14,'unchanged':True}
        current=json.loads((ROOT/'说明/研究结果与分析/数据/第一步_现在代码直接命令复测_20261116.json').read_text())
        assert current['status']=='CURRENT_DIRECT_COMMAND_PING_SUCCESS'
        assert current['ping']['transmitted']==current['ping']['received']==60
        assert current['ping']['avg_ms']==2.358 and current['ping']['p99_9_ms'] is None
        assert not current['continuous_tx_gnb'] and not current['continuous_tx_ue']
        assert current['carrier_frequency_hz']==27547560000 and current['SCS_kHz']==120
        assert current['runtime_declarations']['private_hol_bsr']==0
        assert current['unchanged_runtime_and_base_configs']==12
        historical=json.loads((ROOT/'说明/研究结果与分析/数据/第一步_原始程序原核心网复测.json').read_text())
        assert historical['new_complete_transactions']==13320
        report.update(status='PASS',topics=list(checks),document_ids=ids,body_toc_search_match=True,earlier_script_failures_preserved=2,latest_direct_command_success=True,latest_ping_replies=348,latest_avg_rtt_ms=0.834,historical_transactions_preserved=13320)
        report.update(current_direct_command_success=True,current_ping_replies=60,current_avg_rtt_ms=2.358)
    except Exception as e:
        report.update(status='FAIL',error_type=type(e).__name__,error=str(e))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report['status']!='PASS'

if __name__=='__main__':raise SystemExit(main())
