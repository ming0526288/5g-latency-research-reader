#!/usr/bin/env python3
"""Validate offline routes, source hashes, page bounds and equation output."""
import collections,hashlib,json,re,sys,urllib.parse as U
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
errors=[];warnings=[];counts=collections.Counter()
def require(ok,message):
 if not ok:errors.append(message)
def read_data(p):
 s=p.read_text();return json.loads(s[s.index('=')+1:].rstrip(';'))
s=(ROOT/'网页/catalog.js').read_text();catalog=json.loads(s.split('window.READER_CATALOG=',1)[1].rstrip(';'))
docs={d['id']:d for d in catalog['docs']};papers={p['id']:p for p in catalog['papers']};protos={p['id']:p for p in catalog['protocols']}
algorithm_data=(ROOT/'网页/algorithms.js').read_text()
algorithms=json.loads(algorithm_data.split('window.READER_ALGORITHMS=',1)[1].rstrip(';'))
families={f['id']:f for f in algorithms['families']}
require(algorithms['commonKnowledge'] in docs,'missing algorithm common prerequisites')
for family in families.values():
 for kind in ['knowledge','results']:
  require(bool(family[kind]),'empty algorithm category '+family['id'])
  for section in family[kind]:
   for did in section['documents']:
    require(did in docs,'missing algorithm document '+did);counts['algorithm_document_links']+=1
    if kind=='knowledge' and did in docs:require(docs[did]['group']=='knowledge','non-knowledge algorithm link '+did)
 counts['algorithm_families']+=1
specs=collections.defaultdict(list)
for p in protos.values():specs[p['spec']].append(p)
class Scan(HTMLParser):
 def __init__(self,name):super().__init__();self.name=name
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  for attr in ['href','src']:
   v=d.get(attr,'')
   if not v:continue
   if v.startswith('#/'):
    path,_,q=v[1:].partition('?');parts=path.strip('/').split('/');query=U.parse_qs(q)
    if parts[0]=='doc':
     require(parts[1] in docs,f'{self.name}: missing document {v}');counts['document_routes']+=1
     if 'anchor' in query and parts[1] in docs:
      anchor=query['anchor'][0];valid={x['id'] for x in docs[parts[1]]['toc']}
      normalize=lambda s:re.sub(r'[^\w\u4e00-\u9fff]','',s.lower())
      if anchor not in valid and normalize(anchor) not in {normalize(x) for x in valid}:counts['legacy_heading_links_with_fallback']+=1
    elif parts[0]=='paper':
     require(parts[1] in papers,f'{self.name}: unknown PDF {v}');counts['paper_routes']+=1
     if 'page' in query and parts[1] in papers:require(1<=int(query['page'][0])<=papers[parts[1]]['pages'],f'{self.name}: PDF page outside file {v}');counts['page_routes']+=1
    elif parts[0]=='protocol':
     require(parts[1] in specs,f'{self.name}: unknown protocol {v}');counts['protocol_routes']+=1
     if 'clause' in query and parts[1] in specs:
      clause=query['clause'][0]
      if clause and not any(t['clause']==clause for p in specs[parts[1]] for t in p['toc']):counts['protocol_clause_requires_keyword_fallback']+=1
    elif parts[0]=='algorithm':
     require(len(parts)==3 and parts[1] in families and parts[2] in ['knowledge','results'],f'{self.name}: invalid algorithm route {v}')
   elif not U.urlsplit(v).scheme and not v.startswith('#'):
    path=ROOT/U.unquote(v.split('#')[0]);require(path.is_file(),f'{self.name}: missing offline asset {v}');counts['offline_resources']+=1
for d in docs.values():
 p=ROOT/'网页/data'/f'{d["id"]}.js';require(p.is_file(),f'missing payload {p}');payload=read_data(p)
 require('FORMULAHOLDER' not in payload['html'],f'unrendered equation in {d["id"]}')
 require('<script' not in payload['html'].lower(),f'raw executable HTML in {d["id"]}')
 ids=[x['id'] for x in payload['toc']];require(len(ids)==len(set(ids)),f'duplicate document heading {d["id"]}')
 parser=Scan(d['source']);parser.feed(payload['html']);counts['documents']+=1
for p in papers.values():
 f=ROOT/p['file'];require(f.is_file(),f'missing paper {p["id"]}')
 require(hashlib.sha256(f.read_bytes()).hexdigest()==p['sha256'],f'paper hash mismatch {p["id"]}')
 counts['pdf_originals']+=1
for p in protos.values():
 f=ROOT/p['file'];require(hashlib.sha256(f.read_bytes()).hexdigest()==p['sha256'],f'protocol hash mismatch {p["spec"]}')
 payload=read_data(ROOT/'网页/data'/f'{p["id"]}.js');parser=Scan(p['part']);parser.feed(payload['html']);counts['protocol_parts']+=1
 require(len(payload['html'])>1000,f'empty protocol view {p["part"]}')
manifest=json.loads((ROOT/'校验/来源清单.json').read_text())
for a in manifest.get('protocolArchives',[]):
 f=ROOT/a['file'];require(f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest()==a['sha256'],'protocol ZIP missing or altered '+a['file']);counts['protocol_archives']+=1
for feature in catalog['featured']:require(feature['id'] in docs,'missing reading-path document')
foundation=next(d for d in docs.values() if any(a.endswith('算法知识点说明/00_通信与时延基础知识.md') for a in d['aliases']))
foundation_html=read_data(ROOT/'网页/data'/f'{foundation["id"]}.js')['html']
require('mfrac' in foundation_html and 'katex' in foundation_html,'foundation fraction was not typeset')
require('λ=R×10^6/(8L)' not in foundation_html,'requested formula still displayed as plain text')
for name in ['网页/app.js','网页/algorithms.js','网页/typography.js','网页/style.css','网页/assets/闭环测量.svg','网页/assets/阅读地图.svg','网页/vendor/katex/katex.min.css','打开阅读站.html','index.html']:
 require((ROOT/name).is_file(),'missing entry/asset '+name)
require('fetch(' not in (ROOT/'网页/app.js').read_text(),'file:// app must not depend on fetch')
for p in (ROOT/'文档原稿').glob('*.md'):
 text=p.read_text()
 for pattern in [r'\b(?:sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,})',r'-----BEGIN [A-Z ]*PRIVATE KEY-----',r'(?<![A-Za-z0-9])[0-9]{15}(?![A-Za-z0-9])']:
  require(not re.search(pattern,text),'sensitive source value in '+p.name)
all_files=[p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts]
oversize=[str(p.relative_to(ROOT)) for p in all_files if p.stat().st_size>100*1048576]
require(not oversize,'files exceed GitHub 100MiB limit: '+str(oversize))
counts['total_files']=len(all_files);counts['total_bytes']=sum(p.stat().st_size for p in all_files)
report={'status':'PASS' if not errors else 'FAIL','counts':dict(counts),'errors':errors,'warnings':warnings,
 'browserQA':'Latest typography: 校验/字体字号浏览器核验.json (TEST-015), actual font sizes, 200% root text, desktop 1440x1114 / narrow 500x914 / real 320px iframe. Earlier navigation/results: TEST-014 and TEST-011. Not a full WCAG audit or physical-mobile/VPN test. This validator does not rerun screenshots.',
 'scope':'Offline resource/route/page/hash/math/security checks; not a wireless experiment or independent certification of historical conclusions.'}
(ROOT/'校验/离线资源与跳转校验.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
