/* A portable reader: classic scripts deliberately support file://, without fetch. */
(() => {
 'use strict';
 const A=window.READER_ALGORITHMS;
 const archivedIds=new Set(A.publication?.archivedDocumentIds||[]);
 const legacyModulesVisible=A.publication?.legacyModulesVisible!==false;
 const rawCatalog=window.READER_CATALOG;
 const publishedDocs=rawCatalog.docs.filter(d=>!archivedIds.has(d.id));
 const planningByTopic=topic=>publishedDocs.find(d=>d.topic===topic);
 const featured=rawCatalog.featured.map(item=>{
  if(legacyModulesVisible)return item;
  const replacements={'算法知识地图':['algorithm-experiment-plan','算法实验规划'],'算法实现与结果':['literature-priority','文献阅读指南'],'最新进度与边界':['paper-plan','论文规划与研究路线']};
  const replacement=replacements[item.title],doc=replacement&&planningByTopic(replacement[0]);
  return doc?{id:doc.id,title:replacement[1],group:'guides'}:item;
 }).filter(item=>publishedDocs.some(d=>d.id===item.id));
 const C={...rawCatalog,docs:publishedDocs,featured,
  knowledgeTopics:Object.fromEntries(Object.entries(rawCatalog.knowledgeTopics||{}).filter(([,id])=>!archivedIds.has(id))),
  experimentStages:Object.fromEntries(Object.entries(rawCatalog.experimentStages||{}).filter(([,id])=>!archivedIds.has(id))),
  stats:{...rawCatalog.stats,documents:publishedDocs.length}};
 window.READER_VISIBLE_CATALOG=C;
 const $=s=>document.querySelector(s);
 const E=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const groups={guides:'入口与导引',knowledge:'知识点','algorithm-knowledge':'算法知识点',algorithms:'算法说明',research:'研究报告',changes:'修改记录',tests:'测试记录'};
 const state={sequence:0,route:'',doc:null,observer:null,searchTimer:null};
 const storage={get(k,f){try{return JSON.parse(localStorage.getItem('latency-reader:'+k))??f;}catch{return f;}},set(k,v){try{localStorage.setItem('latency-reader:'+k,JSON.stringify(v));}catch{}}};
 const docs=new Map(C.docs.map(d=>[d.id,d]));
 const find=s=>C.docs.find(d=>d.aliases.some(a=>a.endsWith(s)));
 const docUrl=d=>'#/doc/'+(typeof d==='string'?d:d.id);
 const main=$('#main');
 const algorithmFamilies=legacyModulesVisible?A.families:[];
 const algorithmUrl=(family,kind)=>'#/algorithm/'+family.id+'/'+kind;
 const algorithmIndexUrl=kind=>kind==='knowledge'?'#/browse/algorithm-knowledge':'#/browse/algorithms';
 const familyDocumentIds=(family,kind)=>family[kind].flatMap(section=>section.documents);
 const familyForDoc=id=>algorithmFamilies.filter(f=>['knowledge','results'].some(kind=>familyDocumentIds(f,kind).includes(id)));
 let bookmarks=storage.get('bookmarks',[]),history=storage.get('history',[]);
 const studyDocs=[
  ['basics','⌘','通信与时延基础','算法知识点说明/00_通信与时延基础知识.md'],
  ['tdd','⇄','不同 TDD 知识点','docs/03_TDD配比与周期分析.md'],
  ['scs','≋','不同 SCS 知识点','docs/04_SCS分析与支持边界.md'],
  ['multi-ue','♧','多 UE 知识点','docs/05_多UE与负载分析.md'],
  ['layers','▤','分层时延知识点','docs/02_时延定义与分层测量.md'],
  ['tail','⌁','尾时延知识点','docs/06_尾时延与机制归因.md']
 ].map(([topic,icon,label,source])=>({icon,label,doc:docs.get(C.knowledgeTopics?.[topic])||find(source)})).filter(entry=>entry.doc);
 // One current reading entry per algorithm; historical variants remain in the
 // complete catalogue and search. Prefer reader-owned notes, then main sources.
 const knowledgeByFile=new Map();
 const knowledgeRank=d=>d.source.startsWith('说明/')?2:Number(d.aliases.some(a=>a.startsWith('oi-wireless-ran-latency-analysis/')));
 for(const d of C.docs.filter(d=>d.group==='knowledge'&&(!d.topic||d.topic==='algorithms')&&!/\/(?:00_通信与时延基础知识|README)\.md$/.test(d.source))){
  const key=d.source.split('/').pop(),previous=knowledgeByFile.get(key);
  if(!previous||knowledgeRank(d)>knowledgeRank(previous))knowledgeByFile.set(key,d);
 }
 const algorithmKnowledge=[...knowledgeByFile.values()];
 const outline=[...studyDocs.map(entry=>entry.doc),...algorithmKnowledge];
 const researchStages=Object.values(C.experimentStages).map(id=>docs.get(id)).filter(Boolean).map(doc=>({
  icon:doc.experimentStage==='source-changes'?'⌘':'↗',
  label:doc.experimentStage==='source-changes'?'原始源码与当前版本':doc.title,doc
 }));
 const paperPlan=C.docs.find(d=>d.topic==='paper-plan');
 const experimentPlan=C.docs.find(d=>d.topic==='algorithm-experiment-plan');
 const stepPlans=C.docs.filter(d=>d.group==='guides'&&d.researchStep).sort((a,b)=>a.researchStep.localeCompare(b.researchStep,'en',{numeric:true}));
 function notify(s){$('#toast').textContent=s;$('#toast').classList.add('show');setTimeout(()=>$('#toast').classList.remove('show'),2300);}
 function header(category,title,description=''){return `<div class="library-heading"><div class="eyebrow">${category}</div><h1>${E(title)}</h1>${description?`<p>${E(description)}</p>`:''}</div>`;}
 function breadcrumbs(label){return `<nav class="breadcrumbs"><a href="#/">阅读首页</a><span>／</span><span>${E(label)}</span></nav>`;}
 function sidebar(){
  const route=state.route;
  let algorithmMode=route.startsWith('/algorithm/')?route.split('/')[3]:null;
  if(state.doc&&familyForDoc(state.doc).length)algorithmMode=docs.get(state.doc).group==='knowledge'?'knowledge':'results';
  const nav=(url,icon,label,count)=>`<a href="${url}" class="nav-link ${route===url.slice(1)||algorithmMode&&url===algorithmIndexUrl(algorithmMode)?'active':''}"><span class="nav-icon">${icon}</span>${label}${count?`<span class="nav-count">${count}</span>`:''}</a>`;
  $('#sidebar').innerHTML=nav('#/','⌂','阅读首页')+nav('#/bookmarks','☆','我的书签',bookmarks.filter(id=>docs.has(id)).length)+
   (paperPlan||experimentPlan||stepPlans.length?'<div class="nav-heading">论文规划与研究路线</div>'+(paperPlan?nav(docUrl(paperPlan),'↗','时延优化与算法对照'):'')+(experimentPlan?nav(docUrl(experimentPlan),'↗','算法实验规划'):'')+stepPlans.map(d=>nav(docUrl(d),'↗',d.title)).join(''):'')+
   '<div class="nav-heading">知识点</div>'+studyDocs.map(entry=>nav(docUrl(entry.doc),entry.icon,entry.label)).join('')+
   (legacyModulesVisible?nav('#/browse/algorithm-knowledge','◇','算法知识点',algorithmFamilies.length):'')+
   '<div class="nav-heading">研究结果与分析</div>'+researchStages.map(entry=>nav(docUrl(entry.doc),entry.icon,entry.label)).join('')+
   (legacyModulesVisible?nav('#/browse/algorithms','<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false" style="vertical-align:-3px"><rect x="2.5" y="3.5" width="19" height="17" rx="3"/><path d="m9 9-3 3 3 3m6-6 3 3-3 3"/></svg>','算法实现与结果',algorithmFamilies.length):'')+
   '<div class="nav-heading">研究资料</div>'+nav('#/library/papers','▥','文献与材料',C.papers.length)+nav('#/library/protocols','▦','3GPP 协议',C.stats.protocolSpecs)+
   '<div class="nav-heading">过程与依据</div>'+nav('#/browse/changes','↳','修改记录 CHG',C.docs.filter(d=>d.group==='changes').length)+nav('#/browse/tests','✓','测试记录 TEST',C.docs.filter(d=>d.group==='tests').length)+nav('#/browse/all','☷','全部文档',C.docs.length)+
   '<div class="nav-note"><strong>一份可以带走的研究资料</strong>资料快照 · '+E(C.builtAt)+'<br>历史结论请结合对应版本阅读。</div>';
 }
 function home(){
  const descriptions=legacyModulesVisible?['了解文件用途，找到自己的阅读起点。','从单位、包长与负载，读到单向时延与P99。','查看五类已做实验、结果图片与错误案例。','先读概念与例子，再进入调度公式。','连接原理、代码改动、实验结果与限制。','查看最新工作点，以及尚未完成的部分。']:['了解文件用途，找到自己的阅读起点。','从单位、包长与负载，读到单向时延与P99。','查看对应的第一步结果入口；实验尚未执行。','从通信RTT场景和PF基线开始，按阶段推进。','了解文献的方法、用途和版本边界。','查看论文主线、对比算法与研究路线。'];
  const recent=history.filter(h=>docs.has(h.id)).slice(0,3);
  const latest=legacyModulesVisible?['docs/22_ALG005不同负载验证与69代价分析.md','docs/24_ALG005同业务编号慢包配对分析.md','docs/28_上行重传RB预算指针修复与旧数据影响.md'].map(find).filter(Boolean):[experimentPlan,paperPlan].filter(Boolean);
  main.innerHTML=`<section class="hero"><div class="hero-grid"><div><div class="eyebrow">5G LATENCY · RESEARCH NOTEBOOK</div><h1>从基础开始，<br>读懂每一次改动。</h1><p>把分散的知识点、算法、实验记录和原始文献连起来。<br>沿着阅读路线学习，遇到公式与引用，随时向下追溯。</p><div class="stats"><span><b>${C.stats.documents}</b>篇研究文档</span><span><b>${C.papers.length}</b>份论文与教材</span><span><b>${C.stats.protocolSpecs}</b>个协议编号</span></div></div><img class="hero-art" src="网页/assets/阅读地图.svg" alt="从知识点到算法、实验与原文的阅读关系图"></div></section>
   ${recent.length?`<section><div class="section-title"><h2>继续上次阅读</h2><small>保存在这台电脑的浏览器中</small></div><div class="list-panel">${recent.map(h=>`<a class="list-row" href="${docUrl(h.id)}"><span>◷</span><span>${E(docs.get(h.id).title)}<small>${h.percent||0}% 已读</small></span><span>↗</span></a>`).join('')}</div></section>`:''}
   <section><div class="section-title"><h2>从头阅读的六个步骤</h2><small>按照理解顺序，而不是文件创建时间</small></div><div class="path-grid">${C.featured.map((d,i)=>`<a class="path-card" href="${d.group==='algorithms'?algorithmIndexUrl('results'):d.title==='算法知识地图'?algorithmIndexUrl('knowledge'):docUrl(d.id)}"><div class="step-no">STEP ${String(i+1).padStart(2,'0')}</div><h3>${E(d.title)}</h3><p>${descriptions[i]}</p><span class="card-arrow">↗</span></a>`).join('')}</div></section>
   <div class="home-columns"><section><div class="section-title"><h2>近期研究入口</h2><a href="#/browse/research">全部报告 →</a></div><div class="list-panel">${latest.map(d=>`<a class="list-row" href="${docUrl(d)}"><span>${E(d.source.split('/').pop().replace(/\.md$/,''))}<small>${d.minutes} 分钟 · 阅读原有结果与边界</small></span><span>↗</span></a>`).join('')}</div></section><section><div class="section-title"><h2>随时查看原文</h2></div><div class="list-panel"><a class="list-row" href="#/library/papers"><span>论文与教材<small>支持PDF页序定位与返回原文档</small></span><span>↗</span></a><a class="list-row" href="#/library/protocols"><span>3GPP协议库<small>条款阅读、分册选择与Word原文</small></span><span>↗</span></a><a class="list-row" href="${docUrl(find('docs/10_协议文献教材依据与参数溯源.md'))}"><span>协议、论文与参数溯源<small>查变量和工程选择的实际依据</small></span><span>↗</span></a></div></section></div><footer class="home-foot"><span>已有研究资料的阅读副本 · 保留原始版本与历史边界</span><span>按 <kbd>/</kbd> 或 <kbd>Ctrl K</kbd> 搜索全文</span></footer>`;
 }
 const loading=new Map();
 async function content(id){
  if(window.READER_CONTENT[id])return window.READER_CONTENT[id];
  if(!loading.has(id))loading.set(id,new Promise((resolve,reject)=>{const s=document.createElement('script');s.async=true;s.src='网页/data/'+encodeURIComponent(id)+'.js';s.onload=()=>resolve(window.READER_CONTENT[id]);s.onerror=()=>reject(new Error('未能读取文档，请确认网页/data目录与入口文件一起复制。'));document.head.appendChild(s);}));
  return loading.get(id);
 }
 function setToc(toc,url,linkFor){
  const list=toc.filter(h=>h.level<=3);document.body.classList.add('has-toc');
  $('#pageToc').innerHTML='<div class="toc-label">本页目录</div><div class="reading-progress"><span id="progressBar"></span></div>'+list.map(h=>`<a class="toc-link ${h.level>2?'sub':''}" data-target="${E(h.id)}" href="${E(linkFor?linkFor(h):url+(url.includes('?')?'&':'?')+'anchor='+encodeURIComponent(h.id))}">${E(h.title)}</a>`).join('');
  if(state.observer)state.observer.disconnect();
  state.observer=new IntersectionObserver(entries=>{for(const e of entries){if(!e.isIntersecting)continue;document.querySelectorAll('.toc-link').forEach(a=>a.classList.toggle('active',a.dataset.target===e.target.id));}},{rootMargin:'-90px 0px -65% 0px'});
  main.querySelectorAll('h1[id],h2[id],h3[id]').forEach(h=>state.observer.observe(h));
 }
 function attachArticle(){
  main.querySelectorAll('a[href^="#/doc/"],a[href^="#/algorithm/"],a[href="#/browse/algorithms"],a[href="#/browse/algorithm-knowledge"]').forEach(a=>{
   const href=a.getAttribute('href'),id=href.startsWith('#/doc/')?href.slice(6).split('?')[0]:null;
   if(archivedIds.has(id)||!legacyModulesVisible&&/^#\/(?:algorithm\/|browse\/algorithm)/.test(href)){
    const span=document.createElement('span');span.textContent=a.textContent;span.title='历史内容已保留本地副本，当前不在阅读站展示。';a.replaceWith(span);
   }
  });
  main.querySelectorAll('pre').forEach(pre=>{const b=document.createElement('button');b.className='copy-code';b.textContent='复制';b.onclick=()=>copy(pre.querySelector('code')?.textContent||pre.textContent.replace(/复制$/,''));pre.appendChild(b);});
  main.querySelectorAll('a[href^="#/paper/"]').forEach(a=>a.addEventListener('click',()=>storage.set('returnTo',location.hash)));
 }
 async function docView(id,params,seq){
  if(archivedIds.has(id))return archivedView();
  const d=docs.get(id);if(!d)return missing('没有找到这篇文档。');
  state.doc=id;const c=await content(id);if(seq!==state.sequence)return;
  const families=familyForDoc(id),family=families.length===1?families[0]:null;
  const kind=d.group==='knowledge'?'knowledge':'results';
  const sequence=d.experimentStage?researchStages.map(entry=>entry.doc):family?familyDocumentIds(family,kind).map(did=>docs.get(did)):outline;
  const pos=sequence.findIndex(x=>x.id===id);const prev=sequence[pos-1];const next=sequence[pos+1];
  const docGroupLabel=['paper-plan','algorithm-experiment-plan'].includes(d.topic)||d.researchStep&&d.group==='guides'?'论文规划与研究路线':d.experimentStage?'研究结果与分析':groups[d.group]||'文档';
  main.innerHTML=`<div class="doc-view">${breadcrumbs(docGroupLabel)}${algorithmContext(d)}<div class="doc-toolbar"><span class="pill">${E(docGroupLabel)}</span><span class="pill warm">约 ${d.minutes} 分钟</span><button class="soft-button" id="bookmarkDoc">${bookmarks.includes(id)?'★ 已收藏':'☆ 加入书签'}</button><a class="soft-button" href="${encodeURI(d.snapshot)}" download>Markdown原稿</a><span class="source-label" title="${E(d.source)}">${E(d.source)}</span></div><article class="article">${c.html}</article>${pos>=0?`<nav class="doc-pagination">${prev?`<a href="${docUrl(prev)}"><small>← 上一篇</small>${E(prev.title)}</a>`:'<span></span>'}${next?`<a href="${docUrl(next)}"><small>下一篇 →</small>${E(next.title)}</a>`:family?`<a href="${algorithmUrl(family,kind)}"><small>返回算法目录 →</small>${E(family.name)} · ${kind==='knowledge'?'算法知识点':'实现与结果'}</a>`:`<a href="#/browse/research"><small>继续探索 →</small>研究报告与实验结果</a>`}</nav>`:''}</div>`;
  if(d.source.endsWith('算法知识点说明/00_通信与时延基础知识.md')){
   const h=Array.from(main.querySelectorAll('h2')).find(x=>x.textContent.startsWith('5.'));
   if(h)h.insertAdjacentHTML('afterend','<figure class="diagram-panel"><img src="网页/assets/闭环测量.svg" alt="同一事务的四个应用时间戳：t0、t1、t2、t3，以及UL、处理、DL三个区间"><figcaption>根据本节已有四个应用时间戳绘制。区间边界与计时条件以正文为准。</figcaption></figure>');
  }
  $('#bookmarkDoc').onclick=()=>{bookmarks=bookmarks.includes(id)?bookmarks.filter(v=>v!==id):[id,...bookmarks];storage.set('bookmarks',bookmarks);$('#bookmarkDoc').textContent=bookmarks.includes(id)?'★ 已收藏':'☆ 加入书签';sidebar();};
  const old=history.find(h=>h.id===id);history=[{id,percent:old?.percent||0},...history.filter(h=>h.id!==id)].slice(0,30);storage.set('history',history);
  setToc(c.toc,docUrl(id));attachArticle();sidebar();
  const anchor=params.get('anchor');if(anchor)jump(anchor);else if(old?.scroll>100)window.scrollTo({top:old.scroll,behavior:'instant'});
 }
 function jump(anchor){
  let el=document.getElementById(anchor);
  if(!el){const normalize=s=>s.toLowerCase().replace(/[^\w\u4e00-\u9fff]/g,'');const a=normalize(anchor);el=Array.from(main.querySelectorAll('[id]')).find(n=>normalize(n.id)===a);}
  if(el)setTimeout(()=>el.scrollIntoView({block:'start',behavior:'instant'}),40);
  else notify('未找到原链接的标题，可使用右侧目录或本页查找。');
 }
 function missing(message){main.innerHTML=header('READING NOTE','暂时无法打开')+`<div class="empty-state">${E(message)}<br><a href="#/">返回阅读首页</a></div>`;}
 function archivedView(){main.innerHTML=header('RESEARCH RESET','历史内容已归档','旧说明和历史结果已保留本地副本，当前阅读站暂不展示。')+`<div class="empty-state">${experimentPlan?`<a href="${docUrl(experimentPlan)}">从算法实验规划开始 →</a>`:'<a href="#/">返回阅读首页 →</a>'}</div>`;}
 function row(d){return `<a class="record-row" href="${docUrl(d)}"><strong>${E(d.title)}</strong><small>${E(d.source)} · ${d.minutes} 分钟${d.aliases.length>1?' · 已合并 '+d.aliases.length+' 个相同副本':''}</small></a>`;}
 function algorithmContext(d){
  const families=familyForDoc(d.id);if(!families.length)return '';
  return `<nav class="algorithm-context" aria-label="所属算法">${families.map(f=>`<span>${E(f.name)}</span><a href="${algorithmUrl(f,'knowledge')}">算法知识点</a><a href="${algorithmUrl(f,'results')}">实现与结果</a>`).join('')}</nav>`;
 }
 function algorithmIndex(kind){
  if(!legacyModulesVisible)return archivedView();
  const label=kind==='knowledge'?'算法知识点':'算法实现与结果';
  main.innerHTML=breadcrumbs(label)+header('ALGORITHM LIBRARY',label,'先选择一个算法方向，再进入它的知识、实现说明与已有实验结果。')+
   `<div class="algorithm-common"><span>开始前先读</span><a href="${docUrl(A.commonKnowledge)}">算法实验的共同前置条件 →</a></div><div class="library-tools"><input id="algorithmFilter" class="library-input" placeholder="查找算法，例如 QUEST、SR、授权时机…" aria-label="筛选算法"></div><div id="algorithmCards" class="algorithm-grid"></div><p id="algorithmCount" class="result-limit"></p>`;
  function update(){
   const q=$('#algorithmFilter').value.trim().toLowerCase();
   const list=algorithmFamilies.filter(f=>[f.name,f.code,f.subtitle,f.description,...f.keywords].join(' ').toLowerCase().includes(q));
   $('#algorithmCards').innerHTML=list.length?list.map(f=>`<a class="algorithm-card" href="${algorithmUrl(f,kind)}"><span class="algorithm-code">${E(f.code)}</span><h2>${E(f.name)}</h2><p class="algorithm-subtitle">${E(f.subtitle)}</p><p>${E(f.description)}</p><div class="algorithm-card-foot"><span>${familyDocumentIds(f,'knowledge').length} 篇知识 · ${familyDocumentIds(f,'results').length} 篇实现与结果</span><span>进入 →</span></div></a>`).join(''):'<div class="empty-state">没有找到这个算法，请换一个名称。</div>';
   $('#algorithmCount').textContent=`共 ${list.length} 个算法方向`;
  }
  update();$('#algorithmFilter').addEventListener('input',update);
 }
 function algorithmView(id,kind){
  if(!legacyModulesVisible)return archivedView();
  const family=algorithmFamilies.find(f=>f.id===id);
  if(!family||!['knowledge','results'].includes(kind))return missing('没有找到这个算法分类。');
  const label=kind==='knowledge'?'算法知识点':'实现与结果';
  main.innerHTML=breadcrumbs((kind==='knowledge'?'算法知识点':'算法实现与结果')+' / '+family.name)+
   `<div class="algorithm-back"><a href="${algorithmIndexUrl(kind)}">← 选择其他算法</a><span>${E(family.code)}</span></div>`+
   header('ALGORITHM · '+family.code,family.name+' · '+label,family.description)+
   `<nav class="algorithm-tabs" aria-label="算法阅读方式"><a href="${algorithmUrl(family,'knowledge')}" ${kind==='knowledge'?'aria-current="page"':''}>算法知识点</a><a href="${algorithmUrl(family,'results')}" ${kind==='results'?'aria-current="page"':''}>实现与结果</a></nav>`+
   (kind==='results'?`<aside class="algorithm-learning"><strong>读结果时遇到不熟悉的知识点</strong><a href="${algorithmUrl(family,'knowledge')}">学习 ${E(family.name)} 的算法知识点 →</a><div>${family.knowledge[0].documents.map(did=>`<a href="${docUrl(did)}">${E(docs.get(did).title)} ↗</a>`).join('')}</div></aside>`:`<div class="algorithm-common"><span>共同基础</span><a href="${docUrl(A.commonKnowledge)}">实验前置条件与对照口径 →</a></div>`)+
   family[kind].map(section=>`<section class="algorithm-section"><div class="section-title"><h2>${E(section.title)}</h2><small>${section.documents.length} 篇</small></div><div class="record-list">${section.documents.map(did=>row(docs.get(did))).join('')}</div></section>`).join('');
  document.title=family.name+' · '+label+' · '+C.title;
 }
 function browse(group){
  if(group==='algorithm-knowledge'||group==='algorithms')return algorithmIndex(group==='algorithm-knowledge'?'knowledge':'results');
  let list=group==='all'?C.docs:group==='algorithm-knowledge'?algorithmKnowledge:C.docs.filter(d=>d.group===group);
  if(group==='research')list=researchStages.map(entry=>entry.doc);
  if(group==='bookmarks')list=bookmarks.map(id=>docs.get(id)).filter(Boolean);
  list=list.slice().sort((a,b)=>{
   if(group==='algorithm-knowledge'&&Boolean(a.prerequisite)!==Boolean(b.prerequisite))return Number(Boolean(b.prerequisite))-Number(Boolean(a.prerequisite));
   if(group==='changes'||group==='tests')return parseInt((b.source.match(/(?:CHG|TEST)-(\d+)/)||[])[1]||0)-parseInt((a.source.match(/(?:CHG|TEST)-(\d+)/)||[])[1]||0);
   const am=a.source.startsWith('oi-wireless-ran-latency-analysis/'),bm=b.source.startsWith('oi-wireless-ran-latency-analysis/');return Number(bm)-Number(am)||a.title.localeCompare(b.title,'zh-CN');
  });
  const browseLabel=group==='bookmarks'?'我的书签':group==='research'?'研究结果与分析':groups[group]||'全部文档';
  main.innerHTML=breadcrumbs(browseLabel)+header('RESEARCH LIBRARY',browseLabel,`共 ${list.length} 篇；相同内容合并展示，保留原始来源位置。`)+`<div class="library-tools"><input id="browseFilter" class="library-input" placeholder="按标题或内容筛选…" aria-label="筛选文档"></div><div id="browseList" class="record-list"></div><div id="browseCount" class="result-limit"></div>`;
  function update(){const q=$('#browseFilter').value.trim().toLowerCase();let items=q?list.filter(d=>(d.title+' '+d.search).toLowerCase().includes(q)):list;$('#browseList').innerHTML=items.length?items.slice(0,120).map(row).join(''):'<div class="empty-state">'+(group==='bookmarks'?'还没有书签。阅读时点击“加入书签”即可收藏。':'没有符合筛选条件的文档。')+'</div>';$('#browseCount').textContent=items.length>120?`显示前120篇，共${items.length}篇；输入关键词缩小范围。`:`共${items.length}篇`;}update();$('#browseFilter').addEventListener('input',update);
 }
 let paperTranslationsPromise;
 function loadPaperTranslations(force=false){
  if(force||!paperTranslationsPromise)paperTranslationsPromise=new Promise(resolve=>{
   const script=document.createElement('script');
   script.src='网页/paper-translations.js?v='+Date.now().toString(36);
   script.onload=()=>resolve(window.READER_PAPER_TRANSLATIONS||{papers:{}});
   script.onerror=()=>resolve({papers:{},unavailable:true});
   document.head.appendChild(script);
  });
  return paperTranslationsPromise;
 }
 let protocolTranslationsPromise;
 function loadProtocolTranslations(force=false){
  if(force||!protocolTranslationsPromise)protocolTranslationsPromise=new Promise(resolve=>{
   const script=document.createElement('script');script.src='网页/protocol-translations.js?v='+Date.now().toString(36);
   script.onload=()=>resolve(window.READER_PROTOCOL_TRANSLATIONS||{papers:{}});
   script.onerror=()=>resolve({papers:{},unavailable:true});document.head.appendChild(script);
  });return protocolTranslationsPromise;
 }
 function translatedPaper(p){
  const entry=(p.spec?window.READER_PROTOCOL_TRANSLATIONS:window.READER_PAPER_TRANSLATIONS)?.papers?.[p.id];
  if(p.spec&&entry?.sourceSHA&&entry.sourceSHA!==window.READER_PROTOCOL_PDFS?.documents?.[p.id]?.sha256)return {status:'source-mismatch'};
  return entry;
 }
 function canPreviewTranslation(translated){
  return ['generated','ready'].includes(translated?.status)&&typeof translated.file==='string'&&translated.file.length>0&&Number.isInteger(translated.pages)&&translated.pages>0;
 }
 function translationLabel(translated){
  return translated?.visualQA==='passed'?'中文 PDF（已完成页面核对）':'中文 PDF 预览（尚未校对）';
 }
 function chinesePdfPanel(p,page){
  if(p.id==='book')return '';
  const translated=translatedPaper(p);
  if(translated?.status==='original-chinese')return '';
  if(!canPreviewTranslation(translated)){
   const message=translated?.status==='source-mismatch'?'中文 PDF 对应的原文转换件已更新，需要重新生成译稿；仍可阅读上方原文。':translated?.status==='failed'?'中文 PDF 生成失败，仍可阅读上方原文。':translated?.status==='processing'?'中文 PDF 正在生成，生成后即可预览。':'暂未生成中文 PDF，仍可阅读上方原文。';
   return `<section class="pdf-translation" aria-labelledby="chinesePdfHeading"><h2 id="chinesePdfHeading">中文译文</h2><p class="pdf-hint">${message}</p><button id="refreshZhPdf" class="soft-button">刷新中文状态</button></section>`;
  }
  const zhPage=Math.max(1,Math.min(translated.pages,page));
  const direct=encodeURI(translated.file)+'#page='+zhPage+'&zoom=95';
  const note=translated.visualQA==='passed'?'已完成页面核对的中文辅助译本，可与上方英文对照；专业含义仍以原文为准。':'中文 PDF 已生成，可先预览；尚未完成逐页校对，译文、公式与排版请结合上方原文阅读。';
  return `<section class="pdf-translation" aria-labelledby="chinesePdfHeading"><h2 id="chinesePdfHeading">中文译文</h2><p class="pdf-hint">${note}</p><div class="pdf-controls"><button id="prevZhPdf" class="soft-button" ${zhPage===1?'disabled':''}>上一页</button><label>中文 PDF 第 <input id="zhPdfPage" type="number" min="1" max="${translated.pages}" value="${zhPage}"> / ${translated.pages} 页</label><button id="goZhPdf" class="soft-button">跳转</button><button id="nextZhPdf" class="soft-button" ${zhPage===translated.pages?'disabled':''}>下一页</button><button id="syncZhPdf" class="soft-button">对齐原文第 ${page} 页</button><a id="openZhPdf" class="soft-button primary" href="${direct}" target="_blank" rel="noopener">独立打开中文 PDF ↗</a><button id="refreshZhPdf" class="soft-button">刷新中文状态</button></div><iframe id="chinesePdfFrame" class="pdf-frame" title="${E(p.title)}，中文 PDF 第 ${zhPage} 页" src="${direct}" loading="lazy"></iframe></section>`;
 }
 function bindChinesePdf(p,page){
  if($('#refreshZhPdf'))$('#refreshZhPdf').onclick=()=>{const hash=location.hash;(p.spec?loadProtocolTranslations(true):loadPaperTranslations(true)).then(()=>{if(location.hash===hash&&$('#chinesePdfPanel')){$('#chinesePdfPanel').innerHTML=chinesePdfPanel(p,page);bindChinesePdf(p,page);}});};
  const frame=$('#chinesePdfFrame');if(!frame)return;
  const translated=translatedPaper(p);
  function go(n){
   const current=Math.max(1,Math.min(translated.pages,n));
   const direct=encodeURI(translated.file)+'#page='+current+'&zoom=95';
   $('#zhPdfPage').value=current;frame.src=direct;
   frame.title=p.title+'，中文 PDF 第 '+current+' 页';$('#openZhPdf').href=direct;
   $('#prevZhPdf').disabled=current===1;$('#nextZhPdf').disabled=current===translated.pages;
  }
  $('#goZhPdf').onclick=()=>go(Number($('#zhPdfPage').value)||1);
  $('#zhPdfPage').onkeydown=e=>{if(e.key==='Enter')$('#goZhPdf').click();};
  $('#prevZhPdf').onclick=()=>go((Number($('#zhPdfPage').value)||1)-1);
  $('#nextZhPdf').onclick=()=>go((Number($('#zhPdfPage').value)||1)+1);
  $('#syncZhPdf').onclick=()=>go(page);
 }
 function paperLibrary(){
  main.innerHTML=breadcrumbs('文献与材料')+header('SOURCE LIBRARY','文献与材料','点击引用页码即可直达。页码均为本地PDF从1开始的页序。')+`<div class="library-tools"><input id="paperFilter" class="library-input" placeholder="搜索论文名称、P24、QUEST、AUGUSTE…" aria-label="筛选文献"></div><div id="paperList"></div>`;
  function update(){const q=$('#paperFilter').value.trim().toLowerCase();const ps=C.papers.filter(p=>(p.id+' '+p.title+' '+(p.titleZh||'')+' '+(canPreviewTranslation(translatedPaper(p))?'中文译文 '+translationLabel(translatedPaper(p)):'' )).toLowerCase().includes(q)).sort((a,b)=>a.id==='book'?-1:b.id==='book'?1:a.id.localeCompare(b.id));$('#paperList').innerHTML=ps.map(p=>`<div class="library-card"><span class="file-icon">${p.id==='book'?'BOOK':p.id}</span><div class="card-body"><h3><a href="#/paper/${p.id}">${E(p.title)}</a></h3>${p.titleZh?`<p>${E(p.titleZh)}</p>`:''}<p>${p.pages} 页 · ${(p.bytes/1048576).toFixed(1)} MB · ${p.kind}原文件${canPreviewTranslation(translatedPaper(p))?' · '+translationLabel(translatedPaper(p)):''}</p>${p.citedPages.length?`<div class="page-links">${p.citedPages.slice(0,18).map(n=>`<a class="page-link" href="#/paper/${p.id}?page=${n}">第${n}页</a>`).join('')}</div>`:''}</div><a class="soft-button" href="#/paper/${p.id}">阅读 ↗</a></div>`).join('')||'<div class="empty-state">没有找到匹配的文献。</div>';}update();$('#paperFilter').addEventListener('input',update);loadPaperTranslations().then(()=>{if($('#paperFilter'))update();});
 }
 function paperView(id,params){
  const p=C.papers.find(p=>p.id===id);if(!p)return missing('没有找到这份文献。');
  const page=Math.max(1,Math.min(p.pages,Number(params.get('page'))||1));const direct=encodeURI(p.file)+'#page='+page+'&zoom=95';
  let back=storage.get('returnTo','#/library/papers');if(!back.startsWith('#/doc/'))back='#/library/papers';
  main.innerHTML=`<section class="pdf-view">${breadcrumbs('文献原文')}<div class="eyebrow">${E(p.id==='book'?'TEXTBOOK':p.id)} · LOCAL PDF</div><h1>${E(p.title)}</h1>${p.titleZh?`<p>${E(p.titleZh)}</p><p class="pdf-hint">${E(p.publication||'')} · ${E(p.versionNote||'')}</p>`:''}<div class="pdf-controls"><a class="soft-button" href="${E(back)}">← 返回阅读文档</a><button id="prevPdf" class="soft-button" ${page===1?'disabled':''}>上一页</button><label>本地PDF第 <input id="pdfPage" type="number" min="1" max="${p.pages}" value="${page}"> / ${p.pages} 页</label><button id="goPdf" class="soft-button">跳转</button><button id="nextPdf" class="soft-button" ${page===p.pages?'disabled':''}>下一页</button><a class="soft-button primary" href="${direct}" target="_blank" rel="noopener">独立打开PDF ↗</a></div>${p.id!=='book'?'<h2>英文原文</h2>':''}<iframe class="pdf-frame" title="${E(p.title)}，本地PDF第${page}页" src="${direct}"></iframe><p class="pdf-hint">若浏览器未内嵌显示PDF，请点击“独立打开PDF”。采用PDF页序定位，可能与论文印刷页码不同。文件：${E(p.file)}</p><div id="chinesePdfPanel">${chinesePdfPanel(p,page)}</div></section>`;
  function go(n){location.hash=`#/paper/${id}?page=${Math.max(1,Math.min(p.pages,n))}`;}
  $('#goPdf').onclick=()=>go(Number($('#pdfPage').value)||1);$('#pdfPage').onkeydown=e=>{if(e.key==='Enter')$('#goPdf').click();};$('#prevPdf').onclick=()=>go(page-1);$('#nextPdf').onclick=()=>go(page+1);
  bindChinesePdf(p,page);
  if(p.id!=='book'){
   const currentHash=location.hash;
   loadPaperTranslations().then(()=>{
    if(location.hash!==currentHash||!$('#chinesePdfPanel'))return;
    $('#chinesePdfPanel').innerHTML=chinesePdfPanel(p,page);bindChinesePdf(p,page);
   });
  }
 }
 function protocolLibrary(){
  const specs=Object.groupBy?Object.groupBy(C.protocols,p=>p.spec):C.protocols.reduce((a,p)=>((a[p.spec]??=[]).push(p),a),{});
  main.innerHTML=breadcrumbs('3GPP 协议')+header('STANDARDS LIBRARY','3GPP 协议库','点击即可预览 PDF；由用户提供的 Word 本地转换，原 Word、ZIP 与条款检索入口保留。')+`<div class="library-tools"><input id="protocolFilter" class="library-input" placeholder="查找协议编号，例如38.321、38.331、23.501…" aria-label="查找协议"></div><div id="protocolList"></div>`;
  function update(){const q=$('#protocolFilter').value.trim().toLowerCase();$('#protocolList').innerHTML=Object.entries(specs).filter(([s,ps])=>(s+' '+ps[0].version+' '+(ps[0].titleZh||'')).toLowerCase().includes(q)).sort(([a],[b])=>a.localeCompare(b)).map(([spec,parts])=>`<div class="library-card"><span class="file-icon">3GPP</span><div class="card-body"><h3><a href="#/protocol/${spec}">TS ${spec}</a> <span class="pill">V${E(parts[0].version)}</span></h3>${parts[0].titleZh?`<p>${E(parts[0].titleZh)}</p>`:''}<p>${parts.length} 个原文分册 · PDF 预览 · 保留原 Word 与 ZIP</p><div class="page-links">${parts.length>1?parts.map(p=>`<a class="page-link" href="#/protocol/${spec}?part=${p.id}">${E(p.part)}</a>`).join(''):['4','5','6'].filter(n=>parts[0].toc.some(t=>t.clause===n)).map(n=>`<a class="page-link" href="#/protocol/${spec}?clause=${n}">第${n}章</a>`).join('')}</div></div><a class="soft-button" href="#/protocol/${spec}">阅读 PDF ↗</a></div>`).join('')||'<div class="empty-state">没有找到匹配的协议。</div>';}update();$('#protocolFilter').addEventListener('input',update);
 }
 let protocolPdfLoading;
 function protocolPdfs(){
  if(window.READER_PROTOCOL_PDFS)return Promise.resolve(window.READER_PROTOCOL_PDFS);
  if(!protocolPdfLoading)protocolPdfLoading=new Promise(resolve=>{const script=document.createElement('script');script.src='网页/protocol-pdfs.js?v='+Date.now().toString(36);script.onload=()=>resolve(window.READER_PROTOCOL_PDFS||null);script.onerror=()=>resolve(null);document.head.appendChild(script);});
  return protocolPdfLoading;
 }
 function protocolPdfView(spec,parts,p,c,pdf,params){
  const clause=params.get('clause'),requestedVersion=params.get('version');
  const mismatch=requestedVersion&&requestedVersion!==p.version;
  const page=Math.max(1,Math.min(pdf.pages,Number(params.get('page'))||pdf.clausePages[clause]||1));
  const base='#/protocol/'+spec+'?part='+p.id+(requestedVersion?'&version='+encodeURIComponent(requestedVersion):'');
  const textUrl=base+'&view=text'+(clause?'&clause='+encodeURIComponent(clause):'')+(params.get('q')?'&q='+encodeURIComponent(params.get('q')):'');
  const direct=encodeURI(pdf.file)+'#page='+page+'&zoom=95';
  const clauseNotice=clause?(pdf.clausePages[clause]?`条款 ${E(clause)} 起于转换 PDF 第 ${pdf.clausePages[clause]} 页；当前显示第 ${page} 页。`:`尚未核定条款 ${E(clause)} 的转换 PDF 页序，请使用“条款网页检索”。`):'';
  let back=storage.get('returnTo','#/library/protocols');if(!back.startsWith('#/doc/'))back='#/library/protocols';
  main.innerHTML=`<section class="pdf-view">${breadcrumbs('3GPP 协议 / TS '+spec)}<div class="eyebrow">3GPP TS ${E(spec)} · V${E(p.version)} · LOCAL PDF</div><h1>TS ${E(spec)} · V${E(p.version)}</h1>${p.titleZh?`<p>${E(p.titleZh)}</p><p class="pdf-hint">${E(p.versionNote||'')}</p>`:''}<p class="pdf-hint">由用户提供的 Word 本地转换，非 3GPP 官方下载 PDF；原 Word 与 ZIP 保留。${E(p.part)} · ${pdf.pages} 页。</p>${mismatch?`<div class="source-notice"><strong>版本提示：引用为 V${E(requestedVersion)}，此原文及转换件为 V${E(p.version)}，不能视为相同版本。</strong></div>`:''}<div class="pdf-controls"><a class="soft-button" href="${E(back)}">← 返回阅读文档</a><a class="soft-button primary" href="${direct}" target="_blank" rel="noopener">独立打开 PDF ↗</a><a class="soft-button" href="${encodeURI(p.file)}" target="_blank" rel="noopener">打开 Word 原文 ↗</a>${p.archive?`<a class="soft-button" href="${encodeURI(p.archive)}" download>原始 ZIP</a>`:''}<a class="soft-button" href="${E(textUrl)}">条款网页检索</a>${parts.length>1?`<select id="protocolPart" aria-label="选择原文分册">${parts.map(x=>`<option value="${x.id}" ${x.id===p.id?'selected':''}>${E(x.part)}</option>`).join('')}</select>`:''}</div><div class="pdf-controls"><button id="prevPdf" class="soft-button" ${page===1?'disabled':''}>上一页</button><label>本地 PDF 第 <input id="pdfPage" type="number" min="1" max="${pdf.pages}" value="${page}"> / ${pdf.pages} 页</label><button id="goPdf" class="soft-button">跳转</button><button id="nextPdf" class="soft-button" ${page===pdf.pages?'disabled':''}>下一页</button><span class="pdf-hint">${clauseNotice}</span></div><iframe class="pdf-frame" title="TS ${E(spec)} V${E(p.version)}，本地转换 PDF 第 ${page} 页" src="${direct}"></iframe><p class="pdf-hint">转换页序可能与原 Word 的印刷页码不同。可放大查看图表；复杂版式需精确核对时仍以原 Word 为准。</p><div id="chinesePdfPanel">${chinesePdfPanel(p,page)}</div></section>`;
  const go=n=>{location.hash=base+'&page='+Math.max(1,Math.min(pdf.pages,n));};
  $('#goPdf').onclick=()=>go(Number($('#pdfPage').value)||1);$('#pdfPage').onkeydown=e=>{if(e.key==='Enter')$('#goPdf').click();};$('#prevPdf').onclick=()=>go(page-1);$('#nextPdf').onclick=()=>go(page+1);
  if($('#protocolPart'))$('#protocolPart').onchange=e=>{location.hash='#/protocol/'+spec+'?part='+e.target.value;};
  setToc(c.toc,base,h=>pdf.clausePages[h.clause]?base+'&clause='+encodeURIComponent(h.clause):base+'&view=text&anchor='+encodeURIComponent(h.id));
  bindChinesePdf(p,page);
  const currentHash=location.hash;
  loadProtocolTranslations().then(()=>{
   if(location.hash!==currentHash||!$('#chinesePdfPanel'))return;
   $('#chinesePdfPanel').innerHTML=chinesePdfPanel(p,page);bindChinesePdf(p,page);
  });
 }
 async function protocolView(spec,params,seq){
  const parts=C.protocols.filter(p=>p.spec===spec);if(!parts.length)return missing('没有找到这个协议编号的本地原文。');
  const clause=params.get('clause');let p=parts.find(p=>p.id===params.get('part'));
  if(!p&&clause)p=parts.find(p=>p.toc.some(t=>t.clause===clause));
  p??=parts.find(p=>!p.part.includes('cover'))||parts[0];
  const [c,pdfData]=await Promise.all([content(p.id),protocolPdfs()]);if(seq!==state.sequence)return;
  const pdf=pdfData?.documents?.[p.id];
  const textRequested=params.get('view')==='text'||(params.has('q')&&!params.has('page'));
  if(!textRequested&&pdf?.source_sha256===p.sha256){protocolPdfView(spec,parts,p,c,pdf,params);return;}
  const v=params.get('version');const mismatch=v&&v!==p.version;
  main.innerHTML=`<div class="doc-view">${breadcrumbs('3GPP 协议 / TS '+spec)}<div class="eyebrow">3GPP TS ${spec} · V${E(p.version)}</div><div class="source-notice">这是从用户提供Word生成的<strong>本地转换阅读页</strong>，用于检索和跳转；版式、矢量图或复杂公式需要精确核对时，请打开官方Word原文。此版本未另行声明为官网最高版。${mismatch?`<br><strong>版本提示：引用写的是V${E(v)}，本地可用原文为V${E(p.version)}，不能视为相同版本。</strong>`:''}</div><div class="protocol-tools"><a class="soft-button" href="${encodeURI(p.file)}" target="_blank" rel="noopener">打开官方Word原文 ↗</a>${p.archive?`<a class="soft-button" href="${encodeURI(p.archive)}" download>原始ZIP</a>`:''}${parts.length>1?`<select id="protocolPart" aria-label="选择原文分册">${parts.map(x=>`<option value="${x.id}" ${x.id===p.id?'selected':''}>${E(x.part)}</option>`).join('')}</select>`:''}<input id="clauseInput" value="${E(clause||'')}" placeholder="条款号或IE关键词，如5.4.5、SchedulingRequestConfig" aria-label="定位条款或关键词"><button class="soft-button primary" id="findClause">定位</button></div><article class="article protocol-article">${c.html}</article></div>`;
  if(pdf?.source_sha256===p.sha256){const link=document.createElement('a');link.className='soft-button primary';link.href=`#/protocol/${spec}?part=${p.id}`+(clause?'&clause='+encodeURIComponent(clause):'');link.textContent='PDF 预览 ↗';main.querySelector('.protocol-tools').prepend(link);}
  else{const notice=document.createElement('p');notice.className='source-notice';notice.textContent='本分册的 PDF 预览尚未生成或与原文版本不匹配；当前仅显示条款检索辅助页。';main.querySelector('.protocol-tools').before(notice);}
  const url=`#/protocol/${spec}?part=${p.id}&view=text`;setToc(c.toc,url);
  if($('#protocolPart'))$('#protocolPart').onchange=e=>{location.hash=`#/protocol/${spec}?part=${e.target.value}&view=text`;};
  $('#findClause').onclick=()=>locateProtocol($('#clauseInput').value.trim(),c.toc);
  $('#clauseInput').onkeydown=e=>{if(e.key==='Enter')$('#findClause').click();};
  if(params.get('anchor'))jump(params.get('anchor'));else if(clause)locateProtocol(clause,c.toc);else if(params.get('q'))locateProtocol(params.get('q'),c.toc);
 }
 function locateProtocol(q,toc){
  if(!q)return;
  let h=toc.find(t=>t.clause===q||t.id===q);
  let el=h?document.getElementById(h.id):null;
  if(!el){const n=q.toLowerCase();el=Array.from(main.querySelectorAll('.protocol-article p,.protocol-article h1,.protocol-article h2,.protocol-article h3,.protocol-article td')).find(e=>e.textContent.toLowerCase().includes(n));}
  main.querySelectorAll('.section-found').forEach(e=>e.classList.remove('section-found'));
  if(el){el.classList.add('section-found');setTimeout(()=>el.scrollIntoView({block:'start',behavior:'instant'}),50);}else notify('本分册未找到该条款或关键词，请查看分册与目录。');
 }
 function localReference(params){const path=params.get('path')||'';main.innerHTML=breadcrumbs('来源位置')+header('SOURCE REFERENCE','实验文件与运行环境引用')+`<div class="source-notice">这个链接引用的是实验源代码、原始数据或运行环境文件。阅读站已收录研究文档、论文与协议；实验日志、抓包、凭据和运行目录不作为网页附件打包。</div><p>原始工作区位置：</p><pre class="library-card">${E(path)}</pre><button class="soft-button" id="copyPath">复制来源位置</button> <button class="soft-button" id="returnRef">← 返回刚才的文档</button>`;$('#copyPath').onclick=()=>copy(path);$('#returnRef').onclick=()=>window.history.back();}
 function copy(text){
  if(navigator.clipboard?.writeText){navigator.clipboard.writeText(text).then(()=>notify('已复制')).catch(()=>legacyCopy(text));}else legacyCopy(text);
 }
 function legacyCopy(text){const t=document.createElement('textarea');t.value=text;t.style.position='fixed';t.style.top='-1000px';document.body.appendChild(t);t.select();try{document.execCommand('copy');notify('已复制');}catch{notify('浏览器未允许复制，请手动选择文本。');}t.remove();}
 function highlight(text,q){const i=text.toLowerCase().indexOf(q.toLowerCase());if(i<0)return E(text);return E(text.slice(0,i))+'<mark>'+E(text.slice(i,i+q.length))+'</mark>'+E(text.slice(i+q.length));}
 function search(){
  const q=$('#searchInput').value.trim();if(!q){$('#searchResults').innerHTML='<div class="empty-state">输入关键词，从研究资料中查找。<br>例如：单向时延、HOL、SR周期、预算、38.321</div>';return;}
  const terms=q.toLowerCase().split(/\s+/);const results=[];
  for(const d of C.docs){const title=d.title.toLowerCase(),body=d.search.toLowerCase();if(!terms.every(t=>title.includes(t)||body.includes(t)))continue;let score=terms.reduce((n,t)=>n+(title.includes(t)?12:1),0)+(d.group==='knowledge'?5:0)+(d.source.startsWith('oi-wireless-ran-latency-analysis/')?3:0);const at=body.indexOf(terms[0]);const start=Math.max(0,at-35);results.push({url:docUrl(d),title:d.title,group:groups[d.group],snippet:d.search.slice(start,start+150).replace(/\s+/g,' '),score});}
  for(const p of C.papers){if(terms.every(t=>(p.title+' '+p.id+' '+(p.titleZh||'')).toLowerCase().includes(t)))results.push({url:'#/paper/'+p.id,title:p.id+' · '+p.title,group:'文献原文',snippet:p.pages+'页 · 本地PDF',score:20});}
  for(const f of algorithmFamilies){if(terms.every(t=>[f.name,f.code,f.subtitle,f.description,...f.keywords].join(' ').toLowerCase().includes(t)))results.push({url:algorithmUrl(f,'results'),title:f.name+' · 算法入口',group:'算法分类',snippet:f.description+' 可切换到算法知识点，查看对应知识与结果。',score:40});}
  for(const p of C.protocols){if(terms.every(t=>(p.spec+' '+p.version+' '+p.title+' '+(p.titleZh||'')).toLowerCase().includes(t)))results.push({url:'#/protocol/'+p.spec+'?part='+p.id,title:p.title,group:'协议原文',snippet:p.part,score:25});}
  results.sort((a,b)=>b.score-a.score);$('#searchResults').innerHTML=results.length?results.slice(0,50).map(r=>`<a class="search-result" href="${r.url}"><small>${E(r.group)}</small><strong>${highlight(r.title,q)}</strong><p>${highlight(r.snippet,q)}</p></a>`).join('')+`<div class="search-help">找到 ${results.length} 项，显示前 ${Math.min(results.length,50)} 项。</div>`:'<div class="empty-state">没有找到匹配结果，请换一个关键词。</div>';
 }
 const dialog=$('#searchDialog');function openSearch(){dialog.showModal();setTimeout(()=>$('#searchInput').focus(),20);search();}
 $('#searchButton').onclick=openSearch;$('#closeSearch').onclick=()=>dialog.close();
 dialog.addEventListener('click',e=>{if(e.target===dialog||e.target.closest('a.search-result'))dialog.close();});
 $('#searchInput').addEventListener('input',()=>{clearTimeout(state.searchTimer);state.searchTimer=setTimeout(search,130);});
 document.addEventListener('keydown',e=>{const tag=document.activeElement.tagName;const typing=['INPUT','TEXTAREA','SELECT'].includes(tag);if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'||e.key==='/'&&!typing){e.preventDefault();openSearch();}});
 const initialTheme=storage.get('theme',window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');document.documentElement.dataset.theme=initialTheme;
 $('#themeButton').onclick=()=>{const theme=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=theme;storage.set('theme',theme);};
 $('#menuButton').onclick=()=>document.body.classList.toggle('menu-open');$('#sidebarShade').onclick=()=>document.body.classList.remove('menu-open');
 $('#backTop').onclick=()=>window.scrollTo({top:0,behavior:'smooth'});
 let scrollTimer;window.addEventListener('scroll',()=>{const h=document.documentElement.scrollHeight-innerHeight;const percent=Math.round(h?Math.min(1,scrollY/h)*100:100);if($('#progressBar'))$('#progressBar').style.width=percent+'%';$('#backTop').classList.toggle('visible',scrollY>500);if(state.doc){clearTimeout(scrollTimer);scrollTimer=setTimeout(()=>{const item=history.find(h=>h.id===state.doc);if(item){item.percent=percent;item.scroll=scrollY;storage.set('history',history);}},200);}},{passive:true});
 async function route(){
  const seq=++state.sequence;const raw=location.hash.slice(1)||'/';const [path,query='']=raw.split('?');const parts=path.split('/').filter(Boolean);const params=new URLSearchParams(query);
  state.route=path;state.doc=null;document.body.classList.remove('has-toc','menu-open');$('#pageToc').innerHTML='';window.scrollTo({top:0,behavior:'instant'});
  if(state.observer)state.observer.disconnect();sidebar();
  try{
   if(!parts.length)home();
   else if(parts[0]==='doc'){main.innerHTML='<div class="initial-loading">正在打开文档…</div>';await docView(parts[1],params,seq);}
   else if(parts[0]==='browse')browse(parts[1]||'all');
   else if(parts[0]==='algorithm')algorithmView(parts[1],parts[2]||'results');
   else if(parts[0]==='bookmarks')browse('bookmarks');
   else if(parts[0]==='library'&&parts[1]==='papers')paperLibrary();
   else if(parts[0]==='library'&&parts[1]==='protocols')protocolLibrary();
   else if(parts[0]==='paper')paperView(parts[1],params);
   else if(parts[0]==='protocol'){main.innerHTML='<div class="initial-loading">正在打开协议阅读页…</div>';await protocolView(parts[1],params,seq);}
   else if(parts[0]==='local')localReference(params);
   else missing('这个阅读地址不存在。');
   if(parts[0]!=='algorithm')document.title=(state.doc?docs.get(state.doc).title+' · ':'')+C.title;
  }catch(e){console.error(e);missing(e.message);}
 }
 window.addEventListener('hashchange',route);route();
})();
