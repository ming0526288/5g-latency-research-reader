#!/usr/bin/env python3
"""Check the shared-56B cohort, four role pages, navigation, search and optional HTTP bytes."""
import argparse,hashlib,json,re
from pathlib import Path
from urllib.parse import quote
from urllib.request import ProxyHandler,build_opener,Request
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--live',action='store_true');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
out={'status':'RUNNING','live':a.live,'resources':[]};opener=build_opener(ProxyHandler({}))
def get(n):
 b=(R/n).read_bytes()
 if a.live:
  with opener.open(Request('http://127.0.0.1:8765/'+quote(n),headers={'Cache-Control':'no-cache'}),timeout=10) as resp:assert resp.status==200 and resp.read()==b,n
 out['resources'].append(n);return b.decode()
try:
 cat=json.loads(get('网页/catalog.js').split('window.READER_CATALOG=',1)[1].rstrip(';'))
 data=json.loads(get('说明/研究结果与分析/数据/第一步_56B共用基线重测_20261118.json'))
 assert (data['unique_runs'],data['complete_transactions'],data['statistical_transactions'])==(21,46200,42000)
 docs=[d for d in cat['docs'] if d.get('documentRole') and d.get('stepExperiment')]
 assert len(docs)==20 and len({d['id'] for d in docs})==20
 roles=['plans','knowledge','commands','results'];bodies={}
 for d in docs:
  src=get(d['source']);assert d['sha256']==hashlib.sha256(src.encode()).hexdigest()
  payload=json.loads(get('网页/data/'+d['id']+'.js').split('=',1)[1].rstrip(';'))
  assert payload['toc'] and '<h1' in payload['html'] and d['search'];body=payload['html'];bodies[d['documentRole'],d['stepExperiment']]=body
  for peer in docs:
   if peer['stepExperiment']==d['stepExperiment'] and peer['id']!=d['id']:assert '#/doc/'+peer['id'] in body,(d['topic'],peer['topic'])
  if d['stepExperiment']==2:
   assert '2_56B数据区的ping与UDP.md' in d['source'] and '56 B' in d['title']
   assert '40 B' in body and '56 B' in body and '56 B' in d['search']
  if d['documentRole']=='results':
   n=d['stepExperiment']
   gs=[g for g in data['groups'] if (n==1 and g['tool']=='ping' and g['data_bytes']==56) or (n==2 and g['data_bytes']==56) or (n==3 and g['tool']=='udp' and g['data_bytes']==256) or (n==4 and g['data_bytes'] in [56,256,1200] and g['header_bytes']!=80) or (n==5 and g['tool']=='udp' and g['data_bytes']==56)]
   for g in gs:
    mean=f"{g['pooled']['RTT_ms']['mean']:.3f}";assert mean in body and mean in d['search'],(n,mean)
   for img in re.findall(r'<img[^>]+src="([^"]+)"',body):get(img)
 for tool,nums in [('ping',[1,2,4]),('udp',[2,4,5])]:
  g=next(g for g in data['groups'] if g['tool']==tool and g['data_bytes']==56)
  for n in nums:assert f"{g['pooled']['RTT_ms']['mean']:.3f}" in bodies['results',n]
 for n in [1,2,3,4,5]:assert all((role,n) in bodies for role in roles)
 assert not any('2_16B测量字段的ping与UDP.md' in d['source'] for d in docs)
 out.update(status='PASS',pages=20,renamedExperiment2Pages=4,meanReuseGroups=2,uniqueCurrentRuns=21)
except Exception as e:out.update(status='FAIL',error_type=type(e).__name__,error=str(e))
a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='resources'},ensure_ascii=False));raise SystemExit(0 if out['status']=='PASS' else 1)
