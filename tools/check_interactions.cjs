/* DOM integration checks of the actual offline entry and application scripts.
 * This does not substitute for a real browser/layout/PDF viewer check. */
const fs=require('fs');const path=require('path');const assert=require('assert');
const {JSDOM,VirtualConsole,ResourceLoader}=require('/usr/share/nodejs/jsdom');
const root=path.resolve(__dirname,'..');const steps=[];const failures=[];
let debugWindow;
class LocalLoader extends ResourceLoader{fetch(url,options){if(options.element?.localName==='iframe'||/\.pdf(?:#|$)/i.test(url))return null;return super.fetch(url,options);}}
const tick=ms=>new Promise(r=>setTimeout(r,ms));
async function waitFor(fn,label){for(let i=0;i<240;i++){if(fn())return;await tick(50);}throw new Error('Timed out: '+label);}
(async()=>{
 const vc=new VirtualConsole();vc.on('jsdomError',e=>{if(!/navigation|scroll|PDF/i.test(e.message))failures.push(e.message);});vc.on('error',e=>failures.push(String(e?.stack||e)));
 const dom=await JSDOM.fromFile(path.join(root,'打开阅读站.html'),{resources:new LocalLoader(),runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,
  beforeParse(w){w.scrollTo=()=>{};w.matchMedia=()=>({matches:false});w.IntersectionObserver=class{observe(){}disconnect(){}};w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;};const data=new Map();Object.defineProperty(w,'localStorage',{value:{getItem:k=>data.get(k)??null,setItem:(k,v)=>data.set(k,v)}});}
 });
 const w=dom.window,d=w.document;
 debugWindow=w;
 await waitFor(()=>d.querySelectorAll('.path-card').length===6,'home reading path');
 steps.push('file://入口加载本地catalog.js、CSS及app.js；首页六步路线完整');
 const cat=w.READER_VISIBLE_CATALOG||w.READER_CATALOG;
 const legacyModulesVisible=w.READER_ALGORITHMS.publication?.legacyModulesVisible!==false;
 const algorithmFamilies=legacyModulesVisible?w.READER_ALGORITHMS.families:[];
 const knowledgeHeading=[...d.querySelectorAll('#sidebar .nav-heading')].find(el=>el.textContent==='知识点');
 assert(knowledgeHeading);const studyLinks=[];
 for(let el=knowledgeHeading.nextElementSibling;el&&!el.classList.contains('nav-heading');el=el.nextElementSibling)studyLinks.push(el);
 assert.equal(studyLinks.length,(legacyModulesVisible?7:6)+Number(Boolean(cat.knowledgeTopics['scheduling-basics']))+Number(Boolean(cat.knowledgeTopics['measurement-methods']))+Number(Boolean(cat.knowledgeTopics['source-version-basics'])));
 assert(!d.querySelector('#sidebar details'));
 assert(studyLinks.every(el=>el.matches('a.nav-link')&&!/^\d+$/.test(el.querySelector('.nav-icon').textContent)));
 const studyUrls=studyLinks.map(el=>el.getAttribute('href'));
 for(const url of studyUrls){
  d.querySelector(`#sidebar a[href="${url}"]`).click();
  if(url.startsWith('#/doc/')){
   const target=cat.docs.find(doc=>doc.id===url.slice('#/doc/'.length));assert(target);
   await waitFor(()=>w.location.hash===url&&d.querySelector('.article')&&d.querySelector('.source-label')?.getAttribute('title')===target.source,'knowledge entry '+target.title);
  }else{
   await waitFor(()=>w.location.hash===url&&d.querySelectorAll('.algorithm-card').length===algorithmFamilies.length,'algorithm knowledge selection');
   assert.deepEqual([...d.querySelectorAll('.algorithm-card')].map(a=>a.getAttribute('href')),algorithmFamilies.map(f=>'#/algorithm/'+f.id+'/knowledge'));
   assert.equal(Number(d.querySelector('#sidebar a[href="'+url+'"] .nav-count').textContent),algorithmFamilies.length);
  }
 }
 steps.push('基础知识入口保留；旧算法分类按归档状态控制');
 if(cat.knowledgeTopics['scheduling-basics']){
  const intro=cat.docs.find(x=>x.id===cat.knowledgeTopics['scheduling-basics']);
  w.location.hash='#/doc/'+intro.id;
  await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===intro.source,'new scheduling overview');
  assert.equal(d.querySelector('.article table').querySelectorAll('tbody tr').length,7);
  assert(d.querySelector('.article .katex'));
  const names=['RR','MT','PF','PB','EDF','M-LWDF','QUEST'];
  for(const name of names){
   const target=cat.docs.find(x=>x.source==='说明/算法知识点说明/调度算法入门/'+name+'_知识点说明.md');assert(target);
   const overviewLink=d.querySelector('.article a[href="#/doc/'+target.id+'"]');assert(overviewLink);overviewLink.click();
   await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===target.source,'new algorithm intro '+name);
   const article=d.querySelector('.article');assert(article.querySelector('table'));assert(article.querySelector('.katex'));
   assert(article.textContent.includes('两个 UE 的例子'));assert(article.textContent.includes('对时延有什么用'));
   for(const heading of target.toc)assert(d.getElementById(heading.id));
   if(name==='PF')assert(article.textContent.includes('20 / 10 = 2')&&article.textContent.includes('12 / 3 = 4'));
   if(name==='M-LWDF')assert(article.textContent.includes('超时概率目标不等于标准 PER'));
   const back=article.querySelector('a[href="#/doc/'+intro.id+'"]');assert(back);back.click();
   await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===intro.source,'back to overview '+name);
  }
  d.querySelector('#searchButton').click();const input=d.querySelector('#searchInput');
  for(const name of names){
   input.value=name;input.dispatchEvent(new w.Event('input',{bubbles:true}));await tick(220);
   const target=cat.docs.find(x=>x.source==='说明/算法知识点说明/调度算法入门/'+name+'_知识点说明.md');
   assert(d.querySelector('.search-result[href="#/doc/'+target.id+'"]'),'New note searchable: '+name);
  }
  d.querySelector('#closeSearch').click();steps.push('新版七算法速览、逐篇公式/例子/目录/回链与搜索通过；旧算法归档保持');
 }
 if(legacyModulesVisible){
 for(const family of algorithmFamilies){
  d.querySelector('#sidebar a[href="#/browse/algorithms"]').click();
  await waitFor(()=>w.location.hash==='#/browse/algorithms'&&d.querySelector('.library-heading h1')?.textContent==='算法实现与结果'&&d.querySelectorAll('.algorithm-card').length===algorithmFamilies.length,'implementation algorithm selection');
  const resultUrl='#/algorithm/'+family.id+'/results';d.querySelector('.algorithm-card[href="'+resultUrl+'"]').click();
  await waitFor(()=>d.querySelector('.library-heading h1')?.textContent===family.name+' · 实现与结果','algorithm result '+family.id);
  assert.deepEqual([...d.querySelectorAll('.record-row')].map(a=>a.getAttribute('href')),family.results.flatMap(s=>s.documents).map(id=>'#/doc/'+id));
  assert(d.querySelector('#sidebar a[href="#/browse/algorithms"].active'));
  const knowledgeUrl='#/algorithm/'+family.id+'/knowledge';d.querySelector('.algorithm-learning > a').click();
  await waitFor(()=>w.location.hash===knowledgeUrl&&d.querySelector('.library-heading h1')?.textContent===family.name+' · 算法知识点','same algorithm knowledge '+family.id);
  assert(d.querySelector('#sidebar a[href="#/browse/algorithm-knowledge"].active'));
  const ids=[...d.querySelectorAll('.record-row')].map(a=>a.getAttribute('href').slice('#/doc/'.length));
  assert.deepEqual(ids,family.knowledge.flatMap(s=>s.documents));
  if(family.id==='quest')assert(['PF_知识点说明.md','WAIT_知识点说明.md','QUEST_知识点说明.md'].every(name=>ids.some(id=>cat.docs.find(doc=>doc.id===id).source.endsWith('/'+name))));
  d.querySelector('.record-row').click();
  await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===cat.docs.find(doc=>doc.id===ids[0]).source,'algorithm knowledge document '+family.id);
  assert([...d.querySelectorAll('.doc-pagination a[href^="#/doc/"]')].every(a=>ids.includes(a.getAttribute('href').slice('#/doc/'.length))));
  const resultLink=d.querySelector('.algorithm-context a[href="'+resultUrl+'"]');assert(resultLink);resultLink.click();
  await waitFor(()=>d.querySelector('.library-heading h1')?.textContent===family.name+' · 实现与结果','document return to its algorithm '+family.id);
  const resultIds=family.results.flatMap(s=>s.documents);d.querySelector('.record-row').click();
  await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===cat.docs.find(doc=>doc.id===resultIds[0]).source,'algorithm implementation document '+family.id);
  assert([...d.querySelectorAll('.doc-pagination a[href^="#/doc/"]')].every(a=>resultIds.includes(a.getAttribute('href').slice('#/doc/'.length))));
  const learnLink=d.querySelector('.algorithm-context a[href="'+knowledgeUrl+'"]');assert(learnLink);learnLink.click();
  await waitFor(()=>d.querySelector('.library-heading h1')?.textContent===family.name+' · 算法知识点','implementation to knowledge '+family.id);
 }
 d.querySelector('#sidebar a[href="#/browse/algorithm-knowledge"]').click();
 await waitFor(()=>d.querySelector('#algorithmFilter'),'algorithm filter');
 const filter=d.querySelector('#algorithmFilter');filter.value='QUEST';filter.dispatchEvent(new w.Event('input',{bubbles:true}));
 assert.equal(d.querySelectorAll('.algorithm-card').length,1);assert(d.querySelector('.algorithm-card h2').textContent==='QUEST');
 steps.push('两个算法入口均先选方向；逐方向结果行归属准确；结果跳同算法知识页；知识正文可返回该算法结果；QUEST含自身、消融与对照知识；筛选可用');
 }else{
  assert(!d.querySelector('#sidebar a[href="#/browse/algorithms"]'));
  assert(!d.querySelector('#sidebar a[href="#/browse/algorithm-knowledge"]'));
  steps.push('旧算法知识与实现结果导航撤下，源索引保留归档身份');
 }
 if(cat.experimentStages){
  const heading=[...d.querySelectorAll('#sidebar .nav-heading')].find(el=>el.textContent==='研究结果与分析');
  const links=[];for(let el=heading.nextElementSibling;el&&!el.classList.contains('nav-heading');el=el.nextElementSibling)links.push(el);
  const resultHub=cat.docs.find(doc=>doc.topic==='research-results-index');assert(resultHub);
  assert.equal(links[0].getAttribute('href'),'#/doc/'+resultHub.id);
  assert.equal(links.length,1+Number(legacyModulesVisible));
  const headings=[...d.querySelectorAll('#sidebar .nav-heading')];assert.equal(headings[headings.indexOf(heading)-1].textContent,'启动命令');
  const materialsHeading=[...d.querySelectorAll('#sidebar .nav-heading')].find(el=>el.textContent==='研究资料');
  const materials=[];for(let el=materialsHeading.nextElementSibling;el&&!el.classList.contains('nav-heading');el=el.nextElementSibling)materials.push(el);
  assert.deepEqual(materials.map(el=>el.getAttribute('href')),['#/library/papers','#/library/protocols']);
  assert(materials[0].textContent.includes('文献与材料'));
  for(const [topic,id] of Object.entries(cat.experimentStages)){
   const url='#/doc/'+id;d.querySelector('#sidebar a[href="#/doc/'+resultHub.id+'"]').click();
   await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===resultHub.source,'results hub');
   const entryLink=d.querySelector('.article a[href="'+url+'"]');assert(entryLink);entryLink.click();
   await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===cat.docs.find(x=>x.id===id).source,'experiment page '+topic);
   if(topic==='source-changes'){
    assert(d.querySelector('.article h1').textContent.includes('原始源码与当前研究版本'));
    assert(d.querySelectorAll('.article table').length>=4);
    assert(d.querySelector('.article').textContent.includes('61654513d5'));
    assert(d.querySelector('.article').textContent.includes('不是全部时延结果都已重测'));
    continue;
   }
   const resultDoc=cat.docs.find(x=>x.id===id);
   if(resultDoc.status==='not-started'){
    assert(d.querySelector('.article').textContent.includes('尚未执行，暂无结果与分析'));
    assert.equal(d.querySelectorAll('.article table,.article figure,.article pre,.article .katex').length,0);
    const plan=cat.docs.find(x=>x.topic===resultDoc.planTopic);assert(plan&&plan.researchStep===resultDoc.researchStep);
    assert(d.querySelector('.article a[href="#/doc/'+plan.id+'"]'));
    continue;
   }
   if(resultDoc.independentExperiment==='E-SRC-01'){
    assert.equal(resultDoc.status,'partial');assert(!resultDoc.researchStep&&!resultDoc.planTopic);
    const text=d.querySelector('.article').textContent;
    assert(text.includes('未进入业务')&&text.includes('中断')&&text.includes('根因未确定'));
    assert(text.includes('original-ping-v1')&&!text.includes('80 B / 16 B 字段与功能'));
    assert(d.querySelector('.article a[href="#/doc/'+cat.knowledgeTopics['source-version-basics']+'"]'));
    continue;
   }
   if(resultDoc.independentExperiment){
    assert.equal(resultDoc.independentExperiment,'E-MEAS-01');assert.equal(resultDoc.status,'partial');
    assert(!resultDoc.researchStep&&!resultDoc.planTopic);
    const text=d.querySelector('.article').textContent;
    assert(text.includes('39600')&&text.includes('36000')&&text.includes('尚未完成'));
    assert(!text.includes('original-ping-v1'));assert(d.querySelectorAll('.article figure').length>=4);
    assert(d.querySelector('.article a[href="#/doc/'+cat.knowledgeTopics['measurement-methods']+'"]'));
    continue;
   }
   if(resultDoc.status==='complete'){
    assert.equal(resultDoc.researchStep,'step-1');
    const text=d.querySelector('.article').textContent;
    assert(text.includes('6600')&&text.includes('6000')&&text.includes('不是额外重测'));
    assert(!text.includes('39600'));assert(d.querySelectorAll('.article table').length>=1);
    assert(d.querySelector('.article a[href="#/doc/'+cat.experimentStages['measurement-tools']+'"]'));
    continue;
   }
   assert(d.querySelectorAll('.article figure').length>=2);
   assert(d.querySelector('.article a[href^="网页/images/"][target="_blank"]'));
   const backlink=[...d.querySelectorAll('.article a')].find(a=>a.getAttribute('href').startsWith('#/doc/'+cat.knowledgeTopics[topic]+'?anchor='));
   assert(backlink);const target=backlink.getAttribute('href');backlink.click();
   await waitFor(()=>w.location.hash===target&&d.querySelector('.source-label')?.getAttribute('title')===cat.docs.find(x=>x.id===cat.knowledgeTopics[topic]).source,'knowledge backlink '+topic);
   assert(d.getElementById(new URLSearchParams(target.split('?')[1]).get('anchor')));
  }
  d.querySelector('#searchButton').click();const query=d.querySelector('#searchInput');
  const resultSearchId=cat.experimentStages.tdd||cat.experimentStages['step-1'];
  query.value=cat.experimentStages.tdd?'抓包失败':'第一步结果与分析';query.dispatchEvent(new w.Event('input',{bubbles:true}));
  await waitFor(()=>d.querySelector('.search-result[href="#/doc/'+resultSearchId+'"]'),'published result indexed');d.querySelector('#closeSearch').click();
  d.querySelector('#searchButton').click();query.value='原始源码与当前研究版本';query.dispatchEvent(new w.Event('input',{bubbles:true}));
  await waitFor(()=>d.querySelector('.search-result[href="#/doc/'+cat.experimentStages['source-changes']+'"]'),'source version review indexed');d.querySelector('#closeSearch').click();
  for(const [term,id] of [['80 B 与 16 B 测量格式对比',cat.knowledgeTopics['measurement-methods']],['独立实验：80 B 与 16 B',cat.experimentStages['measurement-tools']],['原始源码与当前版本：知识点分析',cat.knowledgeTopics['source-version-basics']],['独立实验：原始源码与当前版本对比',cat.experimentStages['source-version-retest']]]){
   d.querySelector('#searchButton').click();query.value=term;query.dispatchEvent(new w.Event('input',{bubbles:true}));
   await waitFor(()=>d.querySelector('.search-result[href="#/doc/'+id+'"]'),'separate measurement page searchable '+term);
   d.querySelector('#closeSearch').click();
  }
  steps.push('当前结果入口、源码版本、空结果状态、规划互链与搜索正常；历史页不作为新结果');
 }
 if(cat.knowledgeTopics){
  assert.equal(Object.keys(cat.knowledgeTopics).length,(legacyModulesVisible?7:6)+(cat.knowledgeTopics['scheduling-basics']?8:0)+Number(Boolean(cat.knowledgeTopics['measurement-methods']))+Number(Boolean(cat.knowledgeTopics['source-version-basics'])));
  const tdd=cat.knowledgeTopics.tdd;w.location.hash='#/doc/'+tdd;
  await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===cat.docs.find(x=>x.id===tdd).source,'reader-owned TDD lesson');
  assert(d.querySelector('.article .source-figure a[target="_blank"]'));
  const citation=[...d.querySelectorAll('.article a')].find(a=>a.getAttribute('href').startsWith('#/protocol/38.213?')&&a.getAttribute('href').includes('q='));
  assert(citation);citation.click();
  await waitFor(()=>d.querySelector('.protocol-article .section-found')?.textContent.includes('Table 11.1.1-1'),'TDD original table location');
  d.querySelector('#searchButton').click();const query=d.querySelector('#searchInput');query.value='从字段算出整周期';query.dispatchEvent(new w.Event('input',{bubbles:true}));
  await waitFor(()=>d.querySelector('.search-result[href="#/doc/'+tdd+'"]'),'new knowledge indexed for search');d.querySelector('#closeSearch').click();
  steps.push('已发布知识入口、TDD插图和38.213原表定位正常；新正文可搜索');
 }
 const basic=cat.docs.find(x=>x.aliases.some(a=>a.endsWith('算法知识点说明/00_通信与时延基础知识.md')));
 w.location.hash='#/doc/'+basic.id;await waitFor(()=>d.querySelector('.article .katex'),'foundation');
 assert(d.querySelectorAll('.article mfrac').length>=2);
 const timingDiagram=d.querySelector('.article img[alt="同一事务的上行、回复处理和下行应用边界"]')||d.querySelector('.diagram-panel img');
 assert(timingDiagram);assert(timingDiagram.getAttribute('src').endsWith('.svg'));
 assert(!d.querySelector('.article').textContent.includes('TDDLAT01'));assert(!d.querySelector('.article').textContent.includes('TDDLAT01、LOOP0001'));
 assert(d.querySelector('.article a[href="#/doc/'+cat.knowledgeTopics['measurement-methods']+'"]'));
 steps.push('当前基础知识正文、KaTeX/MathML分式和同事务应用边界示意图正常');
 await waitFor(()=>d.querySelector('.article').textContent.includes('目标应用负载 8 Mbps'),'units in current foundation');
 const original=d.createElement('article');original.innerHTML=w.READER_CONTENT[basic.id].html;
 const article=d.querySelector('.article');
 const texts=(root,selector)=>[...root.querySelectorAll(selector)].map(el=>el.textContent);
 assert.deepEqual(texts(article,'code'),texts(original,'code'));
 assert.deepEqual([...article.querySelectorAll('.katex,math')].map(el=>el.outerHTML),[...original.querySelectorAll('.katex,math')].map(el=>el.outerHTML));
 assert.deepEqual([...article.querySelectorAll('[id]')].map(el=>el.id),[...original.querySelectorAll('[id]')].map(el=>el.id));
 const archivedIds=new Set(w.READER_ALGORITHMS.publication?.archivedDocumentIds||[]);
 const expectedLinks=[...original.querySelectorAll('a')].map(el=>el.getAttribute('href')).filter(href=>{
  if(href.startsWith('#/doc/')&&archivedIds.has(href.slice(6).split('?')[0]))return false;
  return legacyModulesVisible||!/^#\/(?:algorithm\/|browse\/algorithm)/.test(href);
 });
 assert.deepEqual([...article.querySelectorAll('a')].map(el=>el.getAttribute('href')),expectedLinks);
 const fixture=d.createElement('section');fixture.id='spacing-fixture';
 fixture.innerHTML='<p id="mixed-prose">两个<strong>Priority=5</strong>的<code>UE</code>，每个UE的速率为8Mbps，延迟为0.5ms，另一速率为2Mbit/s。</p><p id="literal-url">网址https://example.test/page?q=5&amp;v=8</p><p id="literal-file">文件：report1.md</p><pre><code>Priority=5\npython3 foo.py --port=8765</code></pre><p id="inline-command">运行<code>python3 foo.py --port=8765</code>命令。</p><p id="inline-math">公式<math><mi>λ</mi><mo>=</mo><mn>5</mn></math>保持。</p><div class="protocol-article">原协议Priority=5和8Mbps</div>';
 const codeBefore=texts(fixture,'code');const mathBefore=fixture.querySelector('math').outerHTML;
 d.body.appendChild(fixture);
 await waitFor(()=>fixture.querySelector('#mixed-prose').textContent==='两个 Priority = 5 的 UE，每个 UE 的速率为 8 Mbps，延迟为 0.5 ms，另一速率为 2 Mbit/s。','dynamic mixed-language spacing');
 assert.equal(fixture.querySelector('#literal-url').textContent,'网址 https://example.test/page?q=5&v=8');
 assert.equal(fixture.querySelector('#literal-file').textContent,'文件：report1.md');
 assert.deepEqual(texts(fixture,'code'),codeBefore);assert.equal(fixture.querySelector('math').outerHTML,mathBefore);
 assert.equal(fixture.querySelector('.protocol-article').textContent,'原协议Priority=5和8Mbps');
 const once=fixture.innerHTML;w.READER_TYPOGRAPHY.apply(fixture);assert.equal(fixture.innerHTML,once);fixture.remove();
 steps.push('当前单位段落与动态Priority排版正常；代码、公式、原文与已发布链接保持；归档引用不再可点击；重复排版不累加空格');
 d.querySelector('#bookmarkDoc').click();assert(d.querySelector('#bookmarkDoc').textContent.includes('已收藏'));
 w.location.hash='#/bookmarks';await waitFor(()=>d.querySelector('.record-row'),'bookmarks');assert(d.querySelector('.record-row').textContent.includes('通信与时延'));
 steps.push('加入书签并在书签页找到原文档');
 d.querySelector('#searchButton').click();const input=d.querySelector('#searchInput');input.value='QUEST';input.dispatchEvent(new w.Event('input',{bubbles:true}));
 await waitFor(()=>d.querySelector('.search-result')?.textContent.toLowerCase().includes('quest'),'QUEST search results refreshed');d.querySelector('#closeSearch').click();
 if(legacyModulesVisible)assert(d.querySelector('.search-result[href="#/algorithm/quest/results"]'));
 else{assert(!d.querySelector('.search-result[href^="#/algorithm/"]'));assert(d.querySelector('.search-result[href="#/paper/P24"]'));}
 steps.push('全文搜索QUEST返回实际文档与文献结果');
 w.location.hash='#/paper/P24?page=7';await waitFor(()=>d.querySelector('.pdf-frame'),'PDF route');assert(d.querySelector('.pdf-frame').getAttribute('src').includes('#page=7'));assert.equal(d.querySelector('#pdfPage').value,'7');
 d.querySelector('#pdfPage').value='9';d.querySelector('#goPdf').click();await waitFor(()=>w.location.hash.includes('page=9')&&d.querySelector('#pdfPage')?.value==='9','PDF page control');
 steps.push('P24引用页序7及页码控件9写入真实本地PDF地址');
 await tick(80);
 w.location.hash='#/protocol/38.321?clause=5.4.5&view=text';await waitFor(()=>d.querySelector('.protocol-article')||d.querySelector('.empty-state'),'protocol');assert(d.querySelector('.protocol-article'),d.querySelector('#main').textContent+' '+failures.join('\n'));await waitFor(()=>d.querySelector('.section-found'),'clause location');
 assert.equal(d.querySelector('.section-found').id,'clause-5-4-5');assert([...d.querySelectorAll('.protocol-tools a')].some(a=>a.getAttribute('href').includes('.docx')));
 steps.push('从PDF页切换至TS38.321阅读页，定位5.4.5条，并提供原始DOCX入口');
 const theme=w.document.documentElement.dataset.theme;d.querySelector('#themeButton').click();assert.notEqual(w.document.documentElement.dataset.theme,theme);
 steps.push('主题切换控制正常');
 assert.deepEqual(failures,[]);
 const result={status:'PASS',kind:'jsdom DOM integration, not live browser rendering',steps,jsdomErrors:failures};fs.writeFileSync(path.join(root,'校验/交互逻辑校验.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));w.close();
})().catch(e=>{console.error(e.stack);const diagnostic=debugWindow?{hash:debugWindow.location.hash,mainText:debugWindow.document.querySelector('#main')?.textContent.slice(0,400),scripts:[...debugWindow.document.scripts].map(s=>s.src).slice(-5),loadedPayloads:Object.keys(debugWindow.READER_CONTENT||{})}:{};console.log(JSON.stringify(diagnostic));fs.writeFileSync(path.join(root,'校验/交互逻辑校验.json'),JSON.stringify({status:'FAIL',steps,error:e.message,jsdomErrors:failures,diagnostic},null,2));process.exitCode=1;});
