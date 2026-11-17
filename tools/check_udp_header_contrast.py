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
    small=json.loads(get('说明/研究结果与分析/数据/第一步_16B数据区ping与UDP对照_20261117.json'))
    current=json.loads(get('说明/研究结果与分析/数据/第一步_当前程序56B三轮ping_20261117.json'))
    assert small['status']=='PASS' and small['unique_runs']==6
    assert small['complete_transactions']==13200 and small['statistical_transactions']==12000
    assert small['data_bytes']==16 and small['inner_IP_bytes']==44
    assert [(v['repeat'],v['tool']) for v in small['cases']]==[(1,'ping'),(1,'udp'),(2,'udp'),(2,'ping'),(3,'ping'),(3,'udp')]
    assert all(v['N3_QFI_counts']=={'type1_qfi9':2200,'type0_qfi9':2200} for v in small['cases'])
    udp=[v['application_metrics'] for v in small['cases'] if v['tool']=='udp']
    assert all(abs(v['UL_ms']['mean']+v['reply_ms']['mean']+v['DL_ms']['mean']-v['RTT_ms']['mean'])<1e-12 for v in udp)
    result2=next(d for d in docs if d['stepExperiment']==2 and d['documentRole']=='results')
    page2=json.loads((ROOT/('网页/data/'+result2['id']+'.js')).read_text().split('=',1)[1].strip().rstrip(';'))
    assert result2['status']=='complete'
    for g in small['groups']:
        for n in [g['mean_tool_RTT_ms'],g['max_tool_RTT_ms'],g['mean_common_TUN_RTT_ms'],g['mean_actual_interarrival_ms']]:
            assert f'{n:.3f}' in page2['html'] and f'{n:.3f}' in result2['search']
    assert any('同一 TUN' in h['title'] for h in page2['toc'])
    assert current['status']=='CURRENT_ONLY' and current['unique_runs']==3
    assert current['complete_transactions']==6600 and current['statistical_transactions']==6000
    assert not current['original_current_contrast_complete']
    assert all(not v['business_started'] and v['RTT_ms'] is None for v in current['original_attempts'])
    basic=next(d for d in cat['docs'] if d.get('topic')=='basics')
    bp=json.loads(get('网页/data/'+basic['id']+'.js').split('=',1)[1].strip().rstrip(';'))
    for term in ['127.0.0.1','192.169.0.4','172.11.200.25','不是 3GPP 规定的地址值']:
        assert term in bp['html'] and term in basic['search']
    assert any('RFsim 地址' in h['title'] for h in bp['toc'])
    assert basic['sha256']==hashlib.sha256((ROOT/basic['source']).read_bytes()).hexdigest()
    report=dict(status='PASS',live=a.live,resources=len(resources),independent_pages=20,order='2=16B total-data ping/UDP; 3=80B/16B header UDP',formal_runs=6,complete=13200,statistical=12000,small_data_formal_runs=6,small_data_complete=13200,small_data_statistical=12000,current_ping56_runs=3,original_formal_comparison_complete=False,address_explanation_in_body_toc_search=True,all_peer_links=True,new_result3_id=next(d['id'] for d in docs if d['stepExperiment']==3 and d['documentRole']=='results'))
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
