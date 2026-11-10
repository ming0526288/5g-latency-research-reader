#!/usr/bin/env python3
"""Export the user's existing research into a portable, file:// readable site.

This is a document presentation/export operation, not a communication experiment.
No source documents, models, configuration, or scientific conclusions are edited.
"""
from __future__ import annotations
import argparse, collections, hashlib, html, json, os, re, shutil, subprocess, sys
import urllib.parse as U
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from markdown_it import MarkdownIt
from legacy_protocol import reading_docx

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / '网页'
NS = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'm':'http://schemas.openxmlformats.org/officeDocument/2006/math',
      'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
W = '{'+NS['w']+'}'
M = '{'+NS['m']+'}'
FORMULAS = {
 'PF得分=TBS/历史吞吐状态':r'\text{PF得分}=\frac{\mathrm{TBS}}{\text{历史吞吐状态}}',
 'QUEST得分=(90/Priority)×TBS/max(ε,PDB−HOL)':r'\text{QUEST得分}=\frac{90}{\mathrm{Priority}}\times\frac{\mathrm{TBS}}{\max(\varepsilon,\mathrm{PDB}-\mathrm{HOL})}',
 'EDF得分=1/max(ε,PDB−HOL)':r'\text{EDF得分}=\frac{1}{\max(\varepsilon,\mathrm{PDB}-\mathrm{HOL})}',
 'PB得分=90/Priority Level':r'\text{PB得分}=\frac{90}{\text{Priority Level}}',
 'MT得分=TBS':r'\text{MT得分}=\mathrm{TBS}',
 'WAIT得分=原PF得分×[1+min(a,8)/8]':r'\text{WAIT得分}=\text{原PF得分}\times\left[1+\frac{\min(a,8)}{8}\right]',
 '得分=−ln(γ)×(HOL/PDB)×PF得分':r'\text{得分}=-\ln(\gamma)\times\frac{\mathrm{HOL}}{\mathrm{PDB}}\times\text{PF得分}',
 'λ=R×10^6/(8L)':r'\lambda=\frac{R\times10^{6}}{8L}',
 '平均间隔=8L/(R×10^6)':r'\text{平均间隔}=\frac{8L}{R\times10^{6}}',
 'UL=t1−t0':r'T_{\mathrm{UL}}=t_1-t_0',
 '处理=t2−t1':r'T_{\text{处理}}=t_2-t_1',
 'DL=t3−t2':r'T_{\mathrm{DL}}=t_3-t_2',
 '通信应用闭环=t3−t0':r'T_{\text{通信应用闭环}}=t_3-t_0',
 '闭环=UL+处理+DL':r'T_{\text{闭环}}=T_{\mathrm{UL}}+T_{\text{处理}}+T_{\mathrm{DL}}',
 'B=max(estimated_ul_buffer−sched_ul_bytes,0)':r'B=\max\left(\mathrm{estimated\_ul\_buffer}-\mathrm{sched\_ul\_bytes},0\right)',
 'QUEST_i = (90 / P_i) × TBS_i / max(epsilon, PDB_i − HOL_i)':r'\mathrm{QUEST}_i=\frac{90}{P_i}\times\frac{\mathrm{TBS}_i}{\max(\varepsilon,\mathrm{PDB}_i-\mathrm{HOL}_i)}',
 'L闭环=L上行+L回显处理+L下行':r'L_{\text{闭环}}=L_{\text{上行}}+L_{\text{回显处理}}+L_{\text{下行}}',
 'T_discard=PDB':r'T_{\mathrm{discard}}=\mathrm{PDB}',
 't_RLC=t_PDCP':r't_{\mathrm{RLC}}=t_{\mathrm{PDCP}}',
 'Δ=t_RLC−t_PDCP':r'\Delta=t_{\mathrm{RLC}}-t_{\mathrm{PDCP}}',
 'PDB−HOL_RLC':r'\mathrm{PDB}-\mathrm{HOL}_{\mathrm{RLC}}',
 'PDB−DSR':r'\mathrm{PDB}-\mathrm{DSR}',
 '80(F−1)+(79−4)<80F':r'80(F-1)+(79-4)<80F',
 'RB数×OFDM符号数':r'\text{RB数}\times\text{OFDM符号数}',
 'PDCP剩余时间 = T_discard − HOL_RLC − Δ':r'\text{PDCP剩余时间}=T_{\mathrm{discard}}-\mathrm{HOL}_{\mathrm{RLC}}-\Delta',
}
RAW_FORMULAS = {
 'r_i=8000/P_i，Σr_i≤B':r'r_i=\frac{8000}{P_i},\qquad\sum_i r_i\le B',
 'T_i=.125P_i ms':r'T_i=0.125P_i\ \mathrm{ms}',
 'r_i=8000/P_i次/无线秒':r'r_i=\frac{8000}{P_i}\ \text{次/无线秒}',
 'Σr_i≤B':r'\sum_i r_i\le B',
 'R_i~U[0,T_i]':r'R_i\sim U[0,T_i]',
 'E[R_i]=T_i/2':r'\mathrm{E}[R_i]=\frac{T_i}{2}',
 'Q99(R_i)=.99T_i=990/r_i ms':r'Q_{99}(R_i)=0.99T_i=\frac{990}{r_i}\ \mathrm{ms}',
 'min max_i Q99(R_i)/D_i':r'\min\max_i\frac{Q_{99}(R_i)}{D_i}',
 'min max_i Q99(R_i)':r'\min\max_i Q_{99}(R_i)',
 't≥990N/B':r't\ge\frac{990N}{B}',
 'r_i≥990/t':r'r_i\ge\frac{990}{t}',
 'B≥990N/t':r'B\ge\frac{990N}{t}',
 'Q99=.99T_i=990/r_i ms':r'Q_{99}=0.99T_i=\frac{990}{r_i}\ \mathrm{ms}',
 '990Σ1/D_i/B=.01925':r'\frac{990}{B}\sum_i\frac{1}{D_i}=0.01925',
 'T_SR=P_SR×0.125ms':r'T_{\mathrm{SR}}=P_{\mathrm{SR}}\times0.125\ \mathrm{ms}',
 '8L/C':r'\frac{8L}{C}',
}

def dump(p, d):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def esc(s): return html.escape(str(s),quote=True)
def slug(s):
 s=re.sub(r'<[^>]+>','',s).strip().lower();s=re.sub(r'[\s]+','-',s)
 return re.sub(r'[^\w\-\u4e00-\u9fff]','',s)
def clean(s):
 count=0
 for pattern in [r'\bsk-[A-Za-z0-9_-]{16,}',r'\bgh[pousr]_[A-Za-z0-9]{20,}',
                 r'(?i)(?<=imsi-)[0-9]{14,16}',r'(?i)(?<=imsi=)[0-9]{14,16}',
                 r'(?<![A-Za-z0-9])[0-9]{15}(?![A-Za-z0-9])',
                 r'(?i)(?<=opc=)[a-f0-9]{32}',r'(?i)(?<=key=)[a-f0-9]{32}']:
  s,n=re.subn(pattern,'[凭据已隐藏]',s);count+=n
 return s,count

class Builder:
 def __init__(self, workspace):
  self.ws=workspace.resolve();self.main=self.ws/'oi-wireless-ran-latency-analysis/research/latency-analysis'
  self.docs={};self.paths={};self.byhash={};self.papers={};self.protocols={};self.specs=collections.defaultdict(list)
  self.math=[];self.links=collections.Counter();self.assets={};self.redactions=0;self.warnings=[];self.math_overrides=[];self.archives=[]
  self.md=MarkdownIt('commonmark',{'html':False,'linkify':False,'typographer':False}).enable('table').enable('strikethrough')
  self.md.renderer.rules['text']=self.text_rule
  self.md.renderer.rules['link_open']=self.link_rule
  self.md.renderer.rules['image']=self.image_rule
  def reset_context(tokens,idx,options,env):
   self.paper_context=self.default_paper_context
   return self.md.renderer.renderToken(tokens,idx,options,env)
  self.md.renderer.rules['paragraph_open']=reset_context
  self.md.renderer.rules['tr_open']=reset_context
  self.current=None;self.paper_context=None
 def math_tag(self,tex,display=False):
  i=len(self.math);self.math.append({'tex':tex.strip(),'display':display});return f'FORMULAHOLDER{i}END'
 def equations(self,text,path):
  text=text.replace('`λ=R×10^6/(8L)` 包/秒；`平均间隔=8L/(R×10^6)` 秒。',
   '\n\n'+self.math_tag(FORMULAS['λ=R×10^6/(8L)']+r'\quad\text{包/秒}',True)+'\n\n'+
   self.math_tag(FORMULAS['平均间隔=8L/(R×10^6)']+r'\quad\text{秒}',True)+'\n\n')
  # Only explicitly audited source strings receive an equivalent notation change.
  for old,tex in FORMULAS.items():
   for literal in ['`'+old+'`','```text\n'+old+'\n```']:
    if literal in text:
     self.math_overrides.append({'source':str(path.relative_to(self.ws)),'original':old,'latex':tex})
     text=text.replace(literal,self.math_tag(tex,literal.startswith('```')))
  if path.parent.name in ['算法知识点说明','算法文档']:
   block='HOL_RLC(t)        = t − t_RLC\nQUEST剩余预算    = PDB − HOL_RLC(t)\nPDCP剩余时间     = T_discard − (t − t_PDCP)'
   if '```text\n'+block+'\n```' in text:
    tex=r'\begin{aligned}\mathrm{HOL}_{\mathrm{RLC}}(t)&=t-t_{\mathrm{RLC}}\\\text{QUEST剩余预算}&=\mathrm{PDB}-\mathrm{HOL}_{\mathrm{RLC}}(t)\\\text{PDCP剩余时间}&=T_{\mathrm{discard}}-(t-t_{\mathrm{PDCP}})\end{aligned}'
    text=text.replace('```text\n'+block+'\n```',self.math_tag(tex,True));self.math_overrides.append({'source':str(path.relative_to(self.ws)),'original':block,'latex':tex})
   for old,tex in RAW_FORMULAS.items():
    if old in text:
     text=text.replace(old,self.math_tag(tex));self.math_overrides.append({'source':str(path.relative_to(self.ws)),'original':old,'latex':tex})
  chunks=re.split(r'(^```[^\n]*\n.*?^```[^\n]*$)',text,flags=re.M|re.S)
  for i in range(0,len(chunks),2):
   t=chunks[i]
   t=re.sub(r'(?m)^\\\[\s*\n(.*?)^\\\]\s*$',lambda m:'\n'+self.math_tag(m[1],True)+'\n',t,flags=re.S)
   t=re.sub(r'(?m)^\$\$\s*\n?(.*?)\n?^\$\$\s*$',lambda m:'\n'+self.math_tag(m[1],True)+'\n',t,flags=re.S)
   t=re.sub(r'\\\((.+?)\\\)',lambda m:self.math_tag(m[1]),t)
   t=re.sub(r'(?<![\\$])\$(?!\$)([^$\n]+)\$(?!\$)',lambda m:self.math_tag(m[1]),t)
   chunks[i]=t
  return ''.join(chunks)
 def text_rule(self,tokens,idx,options,env):
  s=tokens[idx].content
  if not env.get('inside_link'):s=self.references(s)
  else:s=esc(s)
  return s
 def references(self,s):
  # Process one continuous prose node without changing its wording.
  pat=re.compile(r'(?P<paper>(?<![A-Za-z0-9])P\d{2}(?![A-Za-z0-9]))|(?P<book>教材|5G移动通信系统设计与标准详解|(?<![A-Za-z0-9])B0[1-6](?![A-Za-z0-9]))|(?P<page>(?:本地\s*)?PDF\s*(?:第\s*)?\d+(?:\s*[–—至\-/、,]\s*\d+(?![\d.]))*(?:\s*页)?)|(?P<spec>(?:TS\s*)?(?<![A-Za-z0-9])\d{2}\.\d{3}(?:-\d)?(?:\s*V\d+\.\d+\.\d+)?(?:\s*§\s*\d+(?:\.\d+)*)?)|(?P<clause>§\s*\d+(?:\.\d+)*)|(?P<more>[/、与及]\s*(?!\d{2}\.\d{3}(?:-\d)?(?=\D|$))\d+(?:\.\d+){1,7})|(?P<ie>SchedulingRequestConfig|SchedulingRequestResourceConfig|TDD-UL-DL-Pattern|TDD-UL-DL-ConfigCommon|PUCCH-Config)')
  out=[];at=0;spec_context=None
  for m in pat.finditer(s):
   out.append(esc(s[at:m.start()]));v=m.group();target=None;title=None
   if m.group('paper') and v in self.papers:
    self.paper_context=v;spec_context=None;target=f'#/paper/{v}';title='打开本地论文'
   elif m.group('book'):
    self.paper_context='book';spec_context=None;target='#/paper/book';title='打开本地教材'
   elif m.group('page') and self.paper_context in self.papers:
    p=int(re.search(r'\d+',v).group());paper=self.papers[self.paper_context]
    if 1<=p<=paper['pages']:
     target=f'#/paper/{self.paper_context}?page={p}';title='按本地PDF页序定位';paper['citedPages'].update(n for n in map(int,re.findall(r'\d+',v)) if 1<=n<=paper['pages']);self.links['pdf_page']+=1
    else:self.warnings.append({'type':'pdf_page_out_of_range','document':str(self.current.relative_to(self.ws)),'paper':self.paper_context,'text':v})
   elif m.group('spec'):
    spec=re.search(r'\d{2}\.\d{3}(?:-\d)?',v).group()
    if spec in self.specs:
     spec_context=spec
     clause=re.search(r'§\s*([\d.]+)',v);version=re.search(r'V([\d.]+)',v)
     target=f'#/protocol/{spec}'+('?' + U.urlencode({'clause':clause[1] if clause else '', 'version':version[1] if version else ''}) if clause or version else '')
     title='打开本地协议条款';self.links['protocol_citation']+=1
   elif m.group('clause') and spec_context:
    clause=re.search(r'[\d.]+',v)[0];target=f'#/protocol/{spec_context}?clause={clause}';title='定位协议条款';self.links['protocol_citation']+=1
   elif m.group('more') and spec_context:
    clause=re.search(r'\d+(?:\.\d+)+',v)[0]
    if clause in self.spec_clauses[spec_context] and not re.search(r'[。；;]',s[at:m.start()]):target=f'#/protocol/{spec_context}?clause={clause}';title='定位同一协议的条款';self.links['protocol_citation']+=1
   elif m.group('ie') and spec_context:
    target=f'#/protocol/{spec_context}?q={U.quote(v)}';title='定位协议中的IE名称'
   if target:out.append(f'<a class="citation" href="{esc(target)}" title="{esc(title)}">{esc(v)}</a>')
   else:out.append(esc(v))
   at=m.end()
  return ''.join(out)+esc(s[at:])
 def asset(self,p):
  p=p.resolve()
  if p in self.assets:return self.assets[p]
  if not p.is_file() or p.suffix.lower() not in ['.png','.jpg','.jpeg','.svg','.webp','.gif']:return None
  name=hashlib.sha256(p.read_bytes()).hexdigest()[:20]+p.suffix.lower();target=WEB/'images'/name
  target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
  url='网页/images/'+name;self.assets[p]=url;return url
 def resolve(self,url):
  raw=U.unquote(url);raw=raw.removeprefix('file://');parts=U.urlsplit(raw)
  if parts.scheme in ['http','https','mailto','tel']:return ('external',url)
  if raw.startswith('#/'):return ('route',raw)
  if raw.startswith('#'):return ('anchor',raw[1:])
  path=Path(parts.path);path=(self.current.parent/path if not path.is_absolute() else path).resolve()
  if path in self.paths:return ('doc',self.paths[path],U.unquote(parts.fragment))
  if path.is_dir():
   if path/'README.md' in self.paths:return ('doc',self.paths[path/'README.md'],'')
   if path.name=='pdf-英文原版':return ('route','#/library/papers')
   if '3GPP协议原文' in str(path):return ('route','#/library/protocols')
  for pid,p in self.papers.items():
   if path==p['_source']:
    pg=re.search(r'page=(\d+)',parts.fragment);return ('route',f'#/paper/{pid}'+(f'?page={pg[1]}' if pg else ''))
  for pid,p in self.protocols.items():
   if path==p['_source']:return ('route',f'#/protocol/{p["spec"]}?part={pid}')
  image=self.asset(path)
  if image:return ('asset',image)
  return ('local',str(path))
 def link_rule(self,tokens,idx,options,env):
  token=tokens[idx];url=token.attrGet('href') or '';r=self.resolve(url)
  # The inline text renderer must never create nested anchors.
  j=idx+1
  while j<len(tokens) and tokens[j].type!='link_close':
   if tokens[j].type=='text':tokens[j].content=tokens[j].content.replace('FORMULAHOLDER','FORMULAHOLDER')
   j+=1
  if r[0]=='doc':
   fragment='?anchor='+U.quote(r[2],safe='') if r[2] else ''
   token.attrSet('href',f'#/doc/{r[1]}{fragment}');self.links['internal']+=1
  elif r[0]=='route':token.attrSet('href',r[1]);self.links['internal']+=1
  elif r[0]=='anchor':token.attrSet('href',f'#/doc/{self.paths[self.current]}?anchor={U.quote(r[1],safe="")}')
  elif r[0]=='external':token.attrSet('target','_blank');token.attrSet('rel','noopener noreferrer')
  elif r[0]=='asset':token.attrSet('href',r[1]);token.attrSet('target','_blank')
  else:
   token.attrSet('href','#/local?path='+U.quote(r[1],safe=''));token.attrSet('class','local-reference');self.links['local_source_reference']+=1
  return self.md.renderer.renderToken(tokens,idx,options,env)
 def image_rule(self,tokens,idx,options,env):
  token=tokens[idx];r=self.resolve(token.attrGet('src') or '')
  if r[0]=='asset':
   dimensions=''
   if r[1].endswith('.svg'):
    viewbox=ET.parse(ROOT/r[1]).getroot().get('viewBox','').split()
    if len(viewbox)==4:dimensions=f' width="{float(viewbox[2]):g}" height="{float(viewbox[3]):g}" style="height:auto"'
   elif r[1].endswith('.png'):
    # Reserve lazy-loaded plot space so heading jumps do not move afterwards.
    with (ROOT/r[1]).open('rb') as stream:header=stream.read(24)
    if header[:8]==b'\x89PNG\r\n\x1a\n' and header[12:16]==b'IHDR':
     width=int.from_bytes(header[16:20],'big');height=int.from_bytes(header[20:24],'big')
     dimensions=f' width="{width}" height="{height}" style="height:auto"'
   return f'<figure class="source-figure"><a href="{esc(r[1])}" target="_blank" rel="noopener"><img loading="lazy" src="{esc(r[1])}" alt="{esc(token.content)}"{dimensions}></a><figcaption>{esc(token.content)} · <a href="{esc(r[1])}" target="_blank" rel="noopener">放大查看</a></figcaption></figure>'
  return f'<span class="local-asset">原文图片：{esc(token.content)}（原文路径未包含可展示图片）</span>'
 def collect_docs(self):
  candidates=[]
  for p in self.main.rglob('*.md'):candidates.append(p)
  for d in sorted(self.ws.glob('oi-wireless-ran-*')):
   if (d/'research/latency-analysis').is_dir():candidates.extend((d/'research/latency-analysis').rglob('*.md'))
  candidates.extend(p for p in self.ws.glob('*.md') if p.name!='AGENTS.md')
  seen=set()
  for p in candidates:
   p=p.resolve()
   if p in seen or p.name in ['AGENTS.md','WORKSPACE_AGENTS_TEMPLATE.md'] or p.name.startswith('TEMPLATE_'):continue
   seen.add(p);text,n=clean(p.read_text(encoding='utf-8',errors='replace'));self.redactions+=n
   digest=hashlib.sha256(text.encode()).hexdigest()
   if digest in self.byhash:
    did=self.byhash[digest];self.docs[did]['aliases'].append(str(p.relative_to(self.ws)));self.paths[p]=did;continue
   did='d'+digest[:16];self.byhash[digest]=did;self.paths[p]=did
   title=re.search(r'^#\s+(.+)',text,re.M);title=title[1].strip() if title else p.stem
   rel=str(p.relative_to(self.ws));group='research'
   if '/records/changes/' in rel:group='changes'
   elif '/records/tests/' in rel:group='tests'
   elif '/算法知识点说明/' in rel:group='knowledge'
   elif '/算法文档/' in rel:group='algorithms'
   elif p.parent==self.ws or '/docs/' in rel or p.name.startswith('START_HERE'):group='guides'
   self.docs[did]={'id':did,'title':title,'source':rel,'aliases':[rel],'group':group,'_text':text,'_path':p,'sha256':sha(p),'toc':[],'redacted':bool(n)}
  for did,d in self.docs.items():
   self.current=d['_path'];self.default_paper_context='P24' if any(s in d['source'] for s in ['QUEST','EDF','M-LWDF','PF_','MT_','PB_']) else None;self.paper_context=self.default_paper_context
   text=self.equations(d['_text'],d['_path']);tokens=self.md.parse(text)
   counts=collections.Counter();inlink=0
   # Resolve headings with GitHub-compatible IDs, preserving Chinese text.
   for i,t in enumerate(tokens):
    if t.type=='heading_open':
     title=tokens[i+1].content;base=slug(title);num=counts[base];counts[base]+=1;anchor=base+(f'-{num}' if num else '')
     t.attrSet('id',anchor);d['toc'].append({'id':anchor,'title':re.sub(r'[`*_]','',title),'level':int(t.tag[1])})
   # Render inline manually to keep the citation context across nodes but avoid nested links.
   original=self.md.renderer.rules['text']
   def inline_renderer(ts,opts,env):
    result='';level=0
    for i,t in enumerate(ts):
     if t.type=='link_open':level+=1
     env['inside_link']=level>0
     if t.type in self.md.renderer.rules:result+=self.md.renderer.rules[t.type](ts,i,opts,env)
     else:result+=self.md.renderer.renderToken(ts,i,opts,env)
     if t.type=='link_close':level-=1
    env['inside_link']=False;return result
   self.md.renderer.renderInline=inline_renderer
   d['html']=self.md.renderer.render(tokens,self.md.options,{})
   d['words']=len(re.sub(r'\s','',d['_text']));d['minutes']=max(1,round(d['words']/650))
   # Store source snapshots separately so the site can be rebuilt without this workstation.
   snap=ROOT/'文档原稿'/f'{did}.md';snap.parent.mkdir(exist_ok=True);snap.write_text(d['_text'],encoding='utf-8');d['snapshot']=str(snap.relative_to(ROOT))
 def collect_papers(self):
  sources=sorted((self.ws/'pdf-英文原版').rglob('*.pdf'))
  for p in sources:
   m=re.match(r'(\d+)[_\s]',p.name)
   if not m:continue
   pid='P'+m[1].zfill(2);self.add_paper(pid,p,'论文')
  for p in self.ws.glob('*.pdf'):
   if '5G移动通信系统设计与标准详解' in p.name:self.add_paper('book',p,'教材')
 def add_paper(self,pid,p,group):
  info=subprocess.run(['pdfinfo',str(p)],capture_output=True,text=True,check=True).stdout
  pages=int(re.search(r'^Pages:\s*(\d+)',info,re.M)[1]);target=ROOT/'文献'/group/p.name
  target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
  self.papers[pid]={'id':pid,'title':p.stem.split('_',1)[-1] if pid!='book' else '5G移动通信系统设计与标准详解','pages':pages,'file':str(target.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,'kind':group,'citedPages':set(),'_source':p.resolve()}
  metadata=ROOT/'说明/materials.json'
  if metadata.is_file():self.papers[pid].update(json.loads(metadata.read_text()).get('papers',{}).get(pid,{}))
 def omml(self,e):
  tag=e.tag.split('}')[-1];cs=list(e)
  def child(n):return next((x for x in cs if x.tag==M+n),None)
  def rr(x):return self.omml(x) if x is not None else '<mrow/>'
  if tag=='t':return '<mi>'+esc(e.text or '')+'</mi>'
  if tag in ['rPr','ctrlPr'] or tag.endswith('Pr'):return ''
  if tag=='f':return '<mfrac>'+rr(child('num'))+rr(child('den'))+'</mfrac>'
  if tag in ['sSup','sSub','sSubSup']:
   nt={'sSup':'msup','sSub':'msub','sSubSup':'msubsup'}[tag];return '<'+nt+'>'+rr(child('e'))+(rr(child('sub')) if tag!='sSup' else '')+(rr(child('sup')) if tag!='sSub' else '')+'</'+nt+'>'
  if tag=='rad':return '<msqrt>'+rr(child('e'))+'</msqrt>' if child('deg') is None or not ''.join(child('deg').itertext()).strip() else '<mroot>'+rr(child('e'))+rr(child('deg'))+'</mroot>'
  if tag=='d':
   pr=child('dPr');beg='(';end=')'
   if pr is not None:
    b=pr.find('m:begChr',NS);z=pr.find('m:endChr',NS)
    if b is not None:beg=b.get(M+'val','(')
    if z is not None:end=z.get(M+'val',')')
   return '<mrow><mo>'+esc(beg)+'</mo>'+''.join(rr(x) for x in cs if x.tag==M+'e')+'<mo>'+esc(end)+'</mo></mrow>'
  if tag=='nary':
   pr=child('naryPr');ch=pr.find('m:chr',NS) if pr is not None else None;symbol=ch.get(M+'val','∑') if ch is not None else '∑'
   return '<mrow><munderover><mo>'+esc(symbol)+'</mo>'+rr(child('sub'))+rr(child('sup'))+'</munderover>'+rr(child('e'))+'</mrow>'
  if tag=='m':return '<mtable>'+''.join(rr(x) for x in cs if x.tag==M+'mr')+'</mtable>'
  if tag=='mr':return '<mtr>'+''.join('<mtd>'+rr(x)+'</mtd>' for x in cs if x.tag==M+'e')+'</mtr>'
  if tag in ['acc','bar','groupChr']:
   pr=next((x for x in cs if x.tag.endswith('Pr')),None);ch=pr.find('m:chr',NS) if pr is not None else None
   return '<mover>'+rr(child('e'))+'<mo>'+esc(ch.get(M+'val','¯') if ch is not None else '¯')+'</mo></mover>'
  return '<mrow>'+''.join(rr(x) for x in cs)+'</mrow>'
 def protocol_doc(self,p,spec,pid):
  reading_source=reading_docx(p,self.ws)
  with zipfile.ZipFile(reading_source) as z:
   bad=z.testzip()
   if bad:raise ValueError(f'Unreadable original DOCX: {p}, {bad}')
   root=ET.fromstring(z.read('word/document.xml'));body=root.find('w:body',NS)
   rels={}
   rp='word/_rels/document.xml.rels'
   if rp in z.namelist():
    rels={e.get('Id'):e.get('Target') for e in ET.fromstring(z.read(rp))}
   plain=''.join(t.text or '' for t in root.findall('.//w:t',NS))
   ver=re.search(r'(?:V|Version\s+)(\d+\.\d+\.\d+)',plain[:5000]);version=ver[1] if ver else '封面版本未识别'
   toc=[];anchors=set();counter=0
   def inline(e):
    if e.tag==W+'t':return esc(e.text or '')
    if e.tag==W+'del':return ''
    if e.tag==W+'tab':return '&emsp;'
    if e.tag==W+'br':return '<br>'
    if e.tag in [M+'oMath',M+'oMathPara']:return '<math xmlns="http://www.w3.org/1998/Math/MathML"'+(' display="block"' if e.tag==M+'oMathPara' else '')+'>'+self.omml(e)+'</math>'
    if e.tag.endswith('}blip') or e.tag.endswith('}imagedata'):
     rid=e.get('{'+NS['r']+'}embed') or e.get('{'+NS['r']+'}id');target=rels.get(rid,'');member='word/'+target.replace('../','')
     if member in z.namelist():
      suffix=Path(target).suffix.lower();raw=z.read(member);name=hashlib.sha256(raw).hexdigest()[:24]+suffix
      if suffix in ['.png','.jpg','.jpeg','.gif','.svg']:
       dest=WEB/'protocol-images'/name;dest.parent.mkdir(exist_ok=True);dest.write_bytes(raw)
       return f'<img loading="lazy" src="网页/protocol-images/{name}" alt="协议原文内嵌图">'
      return '<span class="vector-source">[原文矢量图，请在Word原文中核对]</span>'
    if e.tag in [W+'pPr',W+'rPr',W+'sectPr']:return ''
    return ''.join(inline(x) for x in e)
   def block(e):
    nonlocal counter
    if e.tag==W+'p':
     style=e.find('w:pPr/w:pStyle',NS);st=style.get(W+'val','') if style is not None else ''
     if st.lower().startswith('toc'):return ''
     text=''.join(t.text or '' for t in e.findall('.//w:t',NS));content=inline(e)
     if not content.strip():return ''
     heading=re.search(r'heading(\d)',st,re.I)
     if heading:
      level=min(6,int(heading[1]));m=re.match(r'\s*(\d+(?:\.\d+)*)(?=[A-Za-z\s]|$)',text)
      aid='clause-'+m[1].replace('.','-') if m else slug(text)
      if aid in anchors:aid+='-'+str(counter)
      anchors.add(aid);counter+=1;toc.append({'id':aid,'title':text,'level':level,'clause':m[1] if m else ''})
      return f'<h{level} id="{esc(aid)}">{content}</h{level}>'
     table=re.match(r'Table\s+([\d.]+-\d+)',text)
     aid=' id="table-'+table[1].replace('.','-')+'"' if table else ''
     return f'<p{aid}>{content}</p>'
    if e.tag==W+'tbl':
     rows=[]
     for row in e.findall('w:tr',NS):
      cells=[]
      for cell in row.findall('w:tc',NS):
       span=cell.find('w:tcPr/w:gridSpan',NS);attr=' colspan="'+span.get(W+'val')+'"' if span is not None else ''
       cells.append('<td'+attr+'>'+''.join(block(c) for c in cell if c.tag in [W+'p',W+'tbl'])+'</td>')
      rows.append('<tr>'+''.join(cells)+'</tr>')
     return '<div class="table-scroll"><table>'+''.join(rows)+'</table></div>'
    return ''
   converted=''.join(block(e) for e in body)
   original=ROOT/'协议/官方解压原文'/p.relative_to(self.ws/'3GPP协议原文/官方解压原文');original.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,original)
   archive_name=p.stem.split('_')[0]+'.zip';archive=next((a['file'] for a in self.archives if Path(a['file']).name==archive_name),None)
   return {'id':pid,'spec':spec,'version':version,'title':f'TS {spec} · V{version}','part':p.stem,'file':str(original.relative_to(ROOT)),'archive':archive,'sha256':sha(p),'bytes':p.stat().st_size,'toc':toc,'html':converted,'_source':p.resolve()}
 def collect_protocols(self):
  original=self.ws/'3GPP协议原文'
  for p in sorted(original.rglob('*.zip')):
   with zipfile.ZipFile(p) as z:
    if z.testzip():raise ValueError(f'Invalid protocol ZIP: {p}')
   dest=ROOT/'协议/原始压缩包'/p.relative_to(original);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
   self.archives.append({'file':str(dest.relative_to(ROOT)),'source':str(p.relative_to(self.ws)),'sha256':sha(p),'bytes':p.stat().st_size})
  for p in sorted(p for p in (original/'官方解压原文').rglob('*') if p.suffix.lower() in ('.doc','.docx')):
   m=re.match(r'(\d{2})(\d{3})(-\d)?',p.name)
   if not m:raise ValueError(f'Unrecognized protocol identity: {p}')
   spec=m[1]+'.'+m[2]+(m[3] or '');pid='s'+hashlib.sha256(str(p.relative_to(original)).encode()).hexdigest()[:12]
   d=self.protocol_doc(p,spec,pid)
   metadata=ROOT/'说明/materials.json'
   if metadata.is_file():d.update(json.loads(metadata.read_text()).get('protocols',{}).get(spec,{}))
   self.protocols[pid]=d;self.specs[spec].append(pid)
  self.spec_clauses={s:{h['clause'] for pid in ids for h in self.protocols[pid]['toc']} for s,ids in self.specs.items()}
 def render_math(self):
  inp=ROOT/'校验/math-input.json';out=ROOT/'校验/math-output.json';dump(inp,self.math)
  node=next(self.ws.parent.glob('.vscode-server/cli/servers/Stable-2c33*/server/node'))
  pkg=node.parent/'node_modules/katex'
  result=subprocess.run([str(node),str(ROOT/'tools/render_math.cjs'),str(pkg),str(inp),str(out)],capture_output=True,text=True)
  if result.returncode:raise RuntimeError(result.stdout+result.stderr)
  data=json.loads(out.read_text());rendered=data['html']
  if data['errors']:raise RuntimeError('Math typesetting errors: '+str(data['errors'][:10]))
  dist=pkg/'dist';vendor=WEB/'vendor/katex';vendor.mkdir(parents=True,exist_ok=True)
  shutil.copy2(dist/'katex.min.css',vendor/'katex.min.css');shutil.copytree(dist/'fonts',vendor/'fonts',dirs_exist_ok=True)
  shutil.copy2(pkg/'LICENSE',vendor/'LICENSE')
  for d in self.docs.values():
   d['html']=re.sub(r'FORMULAHOLDER(\d+)END',lambda m:rendered[int(m[1])],d['html'])
   d['html']=re.sub(r'<p>(<span class="math-display".*?</span>)</p>',r'<div class="formula-block">\1</div>',d['html'],flags=re.S)
  self.math_errors=data['errors']
 def finish(self):
  data=WEB/'data';data.mkdir(exist_ok=True)
  for f in (WEB/'protocol-images').iterdir():
   if f.suffix.lower() not in ['.png','.jpg','.jpeg','.gif','.svg']:f.unlink()
  valid=set(self.docs)|set(self.protocols)
  for f in data.glob('*.js'):
   if f.stem not in valid:f.unlink()
  for f in (ROOT/'文档原稿').glob('d*.md'):
   if f.stem not in self.docs:f.unlink()
  docmeta=[]
  for d in self.docs.values():
   public={k:v for k,v in d.items() if not k.startswith('_') and k!='html'}
   public['search']=re.sub(r'[`#*|\[\]<>]',' ',d['_text']);docmeta.append(public)
   (data/(d['id']+'.js')).write_text('window.READER_CONTENT['+json.dumps(d['id'])+']='+json.dumps({'html':d['html'],'toc':d['toc']},ensure_ascii=False)+';',encoding='utf-8')
  protometa=[]
  for d in self.protocols.values():
   public={k:v for k,v in d.items() if not k.startswith('_') and k!='html'};protometa.append(public)
   (data/(d['id']+'.js')).write_text('window.READER_CONTENT['+json.dumps(d['id'])+']='+json.dumps({'html':d['html'],'toc':d['toc']},ensure_ascii=False)+';',encoding='utf-8')
  papers=[{k:(sorted(v) if isinstance(v,set) else v) for k,v in d.items() if not k.startswith('_')} for d in self.papers.values()]
  def did(rel):return self.paths.get((self.main/rel).resolve())
  featured=[('从这里开始','guides',self.paths.get(self.ws/'工作区文件夹与文档用途总览.md')),
   ('通信与时延基础','knowledge',did('算法知识点说明/00_通信与时延基础知识.md')),
   ('五类研究主线','research',did('docs/文档导引/03_五类分析_运行_名词_方法.md')),
   ('算法知识地图','knowledge',did('算法知识点说明/README.md')),
   ('算法实现与结果','algorithms',did('算法文档/README.md')),
   ('最新进度与边界','guides',did('START_HERE_新会话引导.md'))]
  book={'version':1,'title':'5G 通信时延研究阅读站','builtAt':'2026-11-02','docs':docmeta,'papers':papers,'protocols':protometa,'featured':[{'title':t,'group':g,'id':i} for t,g,i in featured if i],
        'stats':{'documents':len(self.docs),'sourceLocations':len(self.paths),'papers':len(papers),'protocolParts':len(protometa),'protocolSpecs':len(self.specs),'formulas':len(self.math),'images':len(self.assets),'pdfJumps':self.links['pdf_page']}}
  (WEB/'catalog.js').write_text('window.READER_CONTENT={};window.READER_CATALOG='+json.dumps(book,ensure_ascii=False,separators=(',',':'))+';',encoding='utf-8')
  dump(ROOT/'校验/来源清单.json',{'documents':[{k:v for k,v in d.items() if k in ['id','source','sha256','snapshot','redacted','aliases']} for d in self.docs.values()],'papers':papers,'protocols':protometa,'protocolArchives':self.archives})
  dump(ROOT/'校验/公式等价排版清单.json',self.math_overrides)
  dump(ROOT/'校验/构建摘要.json',{'status':'PASS','stats':book['stats'],'links':dict(self.links),'redactedMatches':self.redactions,'mathErrors':self.math_errors,'warnings':self.warnings,'scope':'文档转换与链接整理，3GPP/新增数学推导不适用；不代表重新核实通信结论或执行实验。'})
  print(json.dumps(book['stats'],ensure_ascii=False))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--workspace',type=Path,required=True);args=ap.parse_args()
 b=Builder(args.workspace);b.collect_papers();print('PDF library ready',flush=True);b.collect_protocols();print('Protocol original files and reading views ready',flush=True);b.collect_docs();print('Markdown views ready',len(b.docs),flush=True);b.render_math();b.finish()
 if (ROOT/'说明/knowledge.json').is_file():
  from update_knowledge import build
  build()
 if (ROOT/'说明/experiments.json').is_file():
  from update_knowledge import build
  build('experiments')
 if (ROOT/'说明/algorithms.json').is_file():
  from update_algorithm_index import main as update_algorithm_index
  update_algorithm_index()
 if (ROOT/'说明/reading-notes.json').is_file():
  from update_reading_notes import main as update_reading_notes
  update_reading_notes()
if __name__=='__main__':main()
