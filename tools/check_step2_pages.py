import argparse,hashlib,json
from pathlib import Path
from urllib.request import Request,ProxyHandler,build_opener
from urllib.parse import quote
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--live',action='store_true');p.add_argument('--output',type=Path,required=True);a=p.parse_args();op=build_opener(ProxyHandler({}));seen=[]
def get(n):
 b=(R/n).read_bytes()
 if a.live:
  with op.open(Request('http://127.0.0.1:8765/'+quote(n),headers={'Cache-Control':'no-cache'}),timeout=10) as r:assert r.status==200 and r.read()==b,n
 seen.append(n);return b.decode()
def js(s,sep):return json.JSONDecoder().raw_decode(s.split(sep,1)[1].lstrip())[0]
c=js(get('网页/catalog.js'),'window.READER_CATALOG=');d={x['topic']:x for x in c['docs'] if x.get('topic')};kids=[x for x in c['docs'] if x.get('topic','').startswith('step-2-experiment-')];assert len(kids)==16
for doc in kids+[d[t] for t in ['step-2','step-2-plan','step-2-commands','step-2-knowledge','multiue-idle-probe-diagnosis','step-1-experiment-5-results','step-1-experiment-5-plans','step-1-experiment-5-commands','step-1-experiment-5-knowledge']]:
 s=get(doc['source']);assert hashlib.sha256(s.encode()).hexdigest()==doc['sha256'];v=js(get('网页/data/'+doc['id']+'.js'),'=');assert v['toc'] and doc['search']
 if doc in kids:
  i=doc['stepExperiment'];assert ('ping' if i<=2 else 'UDP') in doc['title'];assert ('门限 0' if i in [1,3] else '门限 1') in doc['title']
  for other in kids:
   if other['stepExperiment']==i and other!=doc:assert '#/doc/'+other['id'] in v['html']
parent=js(get('网页/data/'+d['step-2']['id']+'.js'),'=')['html']
pilot=parent.index('100 MHz、200 次独立短测');formal=parent.index('6600 次正式三轮');end=parent.index('</table>',formal);load=parent.index('每 UE 目标间隔 20 ms',formal);assert pilot<formal<end<load
for term in ['4.704/4.695','6.327/6.330/6.477','0.0224','0.0448','0.0672','各 6600/6600']:assert term in parent,term
short=json.loads(get('说明/研究结果与分析/数据/第二步_100MHz_200次独立短测汇总_20261124.json'))
assert short['status']=='PASS' and short['legacy_gate0_three_ue']['RTT_ms'] is None
group_keys={(g['gate'],g['tool'],g['ues']) for g in short['groups']}
assert len(short['groups'])==12 and group_keys=={(gate,tool,n) for gate in (0,1) for tool in ('ping','UDP') for n in (1,2,3)}
assert sum(g['source_kind']=='new_measurement' for g in short['groups'])==4
short_table=parent[pilot:parent.index('</table>',pilot)]
for g in short['groups']:
 item={(0,'ping'):1,(1,'ping'):2,(0,'UDP'):3,(1,'UDP'):4}[(g['gate'],g['tool'])]
 payload=js(get('网页/data/'+d[f'step-2-experiment-{item}-results']['id']+'.js'),'=')['html']
 assert len(g['flows'])==g['ues'] and all((f['sent'],f['received'],f['statistical'])==(200,200,180) for f in g['flows'])
 for metric in ['RTT_mean_ms','RTT_p99_ms']:
  values=' / '.join(f'{f[metric]:.3f}' for f in g['flows'])
  assert values in short_table and values in payload,values
assert short_table.count('空闲探测后置')==2 and '原探测顺序未完成共同接入' in parent[pilot:formal]
for gate,n in [(0,2),(1,2),(1,3)]:
 safe=json.loads(get(f'说明/研究结果与分析/数据/第二步_门限{gate}_56B_ping_{n}UE正式_20261119.json'));assert safe['status']=='PASS' and safe['formal_runs']==6
 for regime in ['per-ue','fixed-total']:
  values='/'.join(f"{x['native_RTT_ms']['mean']:.3f}" for x in safe['perUE_pooled'] if x['regime']==regime);assert values in parent,values
udp=json.loads(get('说明/研究结果与分析/数据/第二步_门限0_56B_UDP双UE正式_20261119.json'));assert udp['complete']==26400 and udp['statistical']==24000
for regime in ['per-ue','fixed-total']:
 values='/'.join(f"{x['metrics']['RTT_ms']['mean']:.3f}" for x in udp['perUE_pooled'] if x['regime']==regime);assert values in parent,values
app=get('网页/app.js');assert 'current===multiueDiagnosis' in app and "multiue-idle-probe-diagnosis" in app
assert len([x for x in c['docs'] if x.get('topic','').startswith('step-1-experiment-')])==20
out=dict(status='PASS',live=a.live,pages=25,resources=seen,fourRolesByFourItems=True,sibling=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='resources'}))
