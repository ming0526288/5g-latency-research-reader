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
ix=parent.index('四项 × UE 数结果速览');end=parent.index('</table>',ix);load=parent.index('这张表采用的业务负载');assert ix<end<load
for term in ['4.704/4.695','6.327/6.330/6.477','0.0224','0.0448','0.0672','先导各200/200']:assert term in parent,term
app=get('网页/app.js');assert 'current===multiueDiagnosis' in app and "multiue-idle-probe-diagnosis" in app
assert len([x for x in c['docs'] if x.get('topic','').startswith('step-1-experiment-')])==20
out=dict(status='PASS',live=a.live,pages=25,resources=seen,fourRolesByFourItems=True,sibling=True);a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='resources'}))
