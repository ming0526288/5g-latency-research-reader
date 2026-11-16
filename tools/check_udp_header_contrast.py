#!/usr/bin/env python3
"""Check measured format comparison and all twenty renumbered reader pages."""
import argparse,hashlib,json
from pathlib import Path
from urllib.request import ProxyHandler,build_opener
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--live',action='store_true');ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    opener=build_opener(ProxyHandler({}));resources=[]
    def get(name):
        local=(ROOT/name).read_bytes()
        actual=opener.open('http://127.0.0.1:8765/'+quote(name,safe='/'),timeout=10).read() if a.live else local
        assert actual==local,name
        resources.append(name);return actual.decode()
    cat=json.loads(get('网页/catalog.js').split('window.READER_CATALOG=',1)[1].strip().rstrip(';'))
    data=json.loads(get('说明/研究结果与分析/数据/第一步_80与16字节UDP同条件对照_20261116.json'))
    assert data['status']=='PASS' and data['unique_runs']==6 and data['complete_transactions']==13200 and data['statistical_transactions']==12000
    assert [(v['repeat'],v['header_bytes']) for v in data['cases']]==[(1,16),(1,80),(2,80),(2,16),(3,16),(3,80)]
    docs=[d for d in cat['docs'] if d.get('stepExperiment')]
    assert len(docs)==20 and len({(d['stepExperiment'],d['documentRole']) for d in docs})==20
    for d in docs:
        p=ROOT/d['source'];assert p.exists() and d['sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
        page=json.loads(get('网页/data/'+d['id']+'.js').split('=',1)[1].strip().rstrip(';'))
        assert '<h1' in page['html'] and '#/local' not in page['html'],d['source']
        if d['stepExperiment']==2:assert d['title'].startswith('2. 16 B 数据区') and p.name.startswith('2_16B')
        if d['stepExperiment']==3:assert d['title']=='3. 80 B 与 16 B 的 UDP 对比' and p.name.startswith('3_80B')
        for role in ['plans','knowledge','commands','results']:
            if role==d['documentRole']:continue
            peer=next(v for v in docs if v['stepExperiment']==d['stepExperiment'] and v['documentRole']==role)
            assert '#/doc/'+peer['id'] in page['html'],(d['source'],role)
        if d['stepExperiment']==3 and d['documentRole']=='results':
            assert d['status']=='complete'
            for f in data['formats']:
                for number in [f['mean_RTT_ms'],f['max_RTT_ms']]:assert f'{number:.3f}' in page['html'] and f'{number:.3f}' in d['search']
            assert '13200' in page['html'] and '12000' in page['html'] and '没有测到' in page['html']
            assert len(p.read_text())<2200 and '2.219019' not in page['html']
            assert any('本次实测结果' in h['title'] for h in page['toc'])
    report=dict(status='PASS',live=a.live,resources=len(resources),independent_pages=20,order='2=16B total-data ping/UDP; 3=80B/16B header UDP',formal_runs=6,complete=13200,statistical=12000,all_peer_links=True,new_result3_id=next(d['id'] for d in docs if d['stepExperiment']==3 and d['documentRole']=='results'))
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
