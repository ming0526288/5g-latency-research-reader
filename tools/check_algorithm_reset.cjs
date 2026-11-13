/* Publication integration: old algorithms stay archived; five analyses are visible. */
const fs=require('fs'),path=require('path'),assert=require('assert'),crypto=require('crypto');
const {JSDOM,VirtualConsole,ResourceLoader}=require('/usr/share/nodejs/jsdom');
const root=path.resolve(__dirname,'..');
class LocalLoader extends ResourceLoader{fetch(url,options){if(options.element?.localName==='iframe'||/\.pdf(?:#|$)/i.test(url))return null;return super.fetch(url,options);}}
const tick=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function waitFor(fn,label){for(let i=0;i<500;i++){if(fn())return;await tick(20);}throw Error('Timed out: '+label);}
(async()=>{
 const manifest=JSON.parse(fs.readFileSync(path.join(root,'说明/algorithms.json'),'utf8'));
 assert.strictEqual(manifest.publication.legacyModulesVisible,false);
 const archived=new Set(manifest.publication.archivedDocumentIds),errors=[];
 const restoration=JSON.parse(fs.readFileSync(path.join(root,'校验/旧五类结果归档清单_20261110.json'),'utf8'));
 const restored=restoration.documents;
 assert.equal(restored.length,5);assert.equal(archived.size,124);
 for(const doc of restored){assert(!archived.has(doc.id));for(const file of doc.files)assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file.path))).digest('hex'),file.sha256,'Original bytes changed: '+file.path);}
 const retainedBookmarks=[...archived].slice(0,2).concat('kc3e4e8560cabef23',restored[0].id);
 const values=new Map([['latency-reader:bookmarks',JSON.stringify(retainedBookmarks)],['latency-reader:history',JSON.stringify(retainedBookmarks.map(id=>({id,percent:50})))]]);
 const vc=new VirtualConsole();vc.on('jsdomError',e=>{if(!/navigation|scroll|PDF/i.test(e.message))errors.push(e.message);});
 const dom=await JSDOM.fromFile(path.join(root,'打开阅读站.html'),{resources:new LocalLoader(),runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
  w.scrollTo=()=>{};w.matchMedia=()=>({matches:false});w.IntersectionObserver=class{observe(){}disconnect(){}};
  w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;};
  Object.defineProperty(w,'localStorage',{value:{getItem:k=>values.get(k)??null,setItem:(k,v)=>values.set(k,v)}});
 }});
 const w=dom.window,d=w.document;await waitFor(()=>d.querySelectorAll('.path-card').length===6,'home');
 const raw=w.READER_CATALOG,published=w.READER_VISIBLE_CATALOG;
 assert.equal(published.docs.length,raw.docs.length-archived.size);
 assert(published.docs.every(doc=>!archived.has(doc.id)));
 assert.equal(published.papers.length,raw.papers.length);assert.equal(published.protocols.length,raw.protocols.length);
 assert(!d.querySelector('#sidebar a[href="#/browse/algorithm-knowledge"]'));assert(!d.querySelector('#sidebar a[href="#/browse/algorithms"]'));
 for(const link of d.querySelectorAll('#main a[href^="#/doc/"]'))assert(!archived.has(link.getAttribute('href').slice(6).split('?')[0]));
 const plan=published.docs.find(doc=>doc.topic==='algorithm-experiment-plan');assert(plan);
 assert.equal(plan.sha256,crypto.createHash('sha256').update(fs.readFileSync(path.join(root,plan.source))).digest('hex'));
 const nav=[...d.querySelectorAll('#sidebar .nav-heading')];assert.equal(nav[0].textContent,'论文规划与研究路线');assert.equal(nav[1].textContent,'知识点');
 const planUrl='#/doc/'+plan.id,paperPlan=published.docs.find(doc=>doc.topic==='paper-plan');assert(paperPlan);
 const planningLinks=[];for(let el=nav[0].nextElementSibling;el&&!el.classList.contains('nav-heading');el=el.nextElementSibling)planningLinks.push(el);
 assert.deepEqual(planningLinks.map(el=>el.getAttribute('href')),['#/doc/'+paperPlan.id,planUrl]);
 assert.equal(planningLinks[0].textContent.replace('↗','').trim(),'时延优化与算法对照');assert.equal(planningLinks[1].textContent.replace('↗','').trim(),'算法实验规划');
 d.querySelector('#sidebar a[href="'+planUrl+'"]').click();await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===plan.source,'new plan');
 assert(d.querySelector('.article').textContent.includes('我主要研究多个 UE 竞争资源时'));
 assert(d.querySelector('.article').textContent.includes('第一步按五项实验组织'));
 for(const item of plan.toc)assert(d.getElementById(item.id),'Missing plan heading '+item.title);
 const stepPlan=published.docs.find(doc=>doc.topic==='step-1-plan');
 const stepResult=published.docs.find(doc=>doc.experimentStage==='step-1');
 assert(stepPlan&&stepResult);assert.equal(stepPlan.researchStep,stepResult.researchStep);assert.equal(stepResult.planTopic,stepPlan.topic);
 const allStepPlans=published.docs.filter(doc=>doc.group==='guides'&&doc.researchStep).sort((a,b)=>a.researchStep.localeCompare(b.researchStep,'en',{numeric:true}));
 const allStepResults=allStepPlans.map(p=>{const result=published.docs.filter(doc=>doc.experimentStage===p.researchStep);assert.equal(result.length,1);assert.equal(result[0].planTopic,p.topic);return result[0];});
 const allStepCommands=allStepPlans.map(p=>{const matches=published.docs.filter(doc=>doc.commandStep===p.researchStep);assert.equal(matches.length,1);assert.equal(matches[0].planTopic,p.topic);assert.equal(matches[0].resultTopic,p.researchStep);return matches[0];});
 const launchIndex=published.docs.find(doc=>doc.topic==='launch-index'),resultsIndex=published.docs.find(doc=>doc.topic==='research-results-index');assert(launchIndex&&resultsIndex);
 const hubHeadings=[...d.querySelectorAll('#sidebar .nav-heading')];assert.equal(hubHeadings[2].textContent,'启动命令');assert.equal(hubHeadings[3].textContent,'研究结果与分析');
 assert.equal(hubHeadings[2].nextElementSibling.getAttribute('href'),'#/doc/'+launchIndex.id);assert(hubHeadings[2].nextElementSibling.nextElementSibling.classList.contains('nav-heading'));
 async function fromHub(hub,target){d.querySelector('#sidebar a[href="#/doc/'+hub.id+'"]').click();await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===hub.source,'hub '+hub.topic);const link=d.querySelector('.article a[href="#/doc/'+target.id+'"]');assert(link,'Missing hub link '+target.id);link.click();await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===target.source,'hub target '+target.id);}
 assert.deepEqual(allStepPlans.map(p=>p.researchStep),Array.from({length:allStepPlans.length},(_,i)=>'step-'+(i+1)));
 assert.deepEqual(Object.keys(published.experimentStages).filter(topic=>!published.docs.find(x=>x.id===published.experimentStages[topic]).parentTopic),['tdd','scs','multi-ue','layers','tail','source-changes',...allStepPlans.map(p=>p.researchStep)]);
 const resultHeading=[...d.querySelectorAll('#sidebar .nav-heading')].find(el=>el.textContent==='研究结果与分析'),resultLinks=[];
 for(let el=resultHeading.nextElementSibling;el&&!el.classList.contains('nav-heading');el=el.nextElementSibling)resultLinks.push(el);
 assert.deepEqual(resultLinks.map(el=>{const copy=el.cloneNode(true);copy.querySelector('.nav-icon')?.remove();return copy.textContent.trim();}),['结果与分析总目录']);assert.equal(resultLinks[0].getAttribute('href'),'#/doc/'+resultsIndex.id);
 const stepPlanUrl='#/doc/'+stepPlan.id,stepResultUrl='#/doc/'+stepResult.id;
 await fromHub(plan,stepPlan);
 assert(d.querySelector('.article').textContent.includes('我的第一步目标'));d.querySelector('.article a[href="'+stepResultUrl+'"]').click();await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===stepResult.source,'empty step result');
 assert.equal(d.querySelector('.article h1').textContent,'第一步结果与分析');assert.equal(stepResult.status,'partial');assert(d.querySelector('.article').textContent.includes('6600')&&d.querySelector('.article').textContent.includes('6000'));assert(d.querySelector('.article').textContent.includes('39600'));assert(d.querySelectorAll('.article table').length>=1);
 d.querySelector('.article a[href="'+stepPlanUrl+'"]').click();await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===stepPlan.source,'paired return');
 for(const [i,p] of allStepPlans.entries()){
  const result=allStepResults[i],purl='#/doc/'+p.id,rurl='#/doc/'+result.id;assert.equal(result.status,i===0?'partial':'not-started');assert.equal(result.title,p.title.replace('规划','结果与分析'));
  await fromHub(plan,p);
  assert(d.querySelector('.article').textContent.includes('我'));assert(d.querySelector('.article a[href="'+rurl+'"]'));
  d.querySelector('.article a[href="'+rurl+'"]').click();await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===result.source,'result '+p.researchStep);
  if(i===0){assert(d.querySelector('.article').textContent.includes('6600'));assert(d.querySelectorAll('.article table').length>=1);}else{assert(d.querySelector('.article').textContent.includes('尚未执行，暂无结果与分析'));assert.equal(d.querySelectorAll('.article table,.article figure,.article pre,.article .katex').length,0);}
  d.querySelector('.article a[href="'+purl+'"]').click();await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===p.source,'back to '+p.researchStep);
  const command=allStepCommands[i],curl='#/doc/'+command.id;assert(d.querySelector('.article a[href="'+curl+'"]'));
  await fromHub(launchIndex,command);assert.equal(command.commandStatus,i===0?'partial':'pending-validation');assert(d.querySelector('.article').textContent.includes(i===0?'已实际运行并核验':'实际启动命令待核验'));assert(d.querySelector('.article a[href="'+purl+'"]'));assert(d.querySelector('.article a[href="'+rurl+'"]'));assert(d.querySelector('.breadcrumbs').textContent.includes('启动命令'));
  await fromHub(resultsIndex,result);assert(d.querySelector('.article a[href="'+curl+'"]'));assert(d.querySelector('#sidebar a.active[href="#/doc/'+resultsIndex.id+'"]'));
 }
 // Restored analyses must be real articles, reachable in navigation and search.
 for(const item of restored){const doc=published.docs.find(x=>x.id===item.id);assert(doc);assert.equal(doc.source,item.source);assert.equal(doc.sha256,item.files.find(f=>f.path===item.source).sha256);await fromHub(resultsIndex,doc);assert.equal(d.querySelector('.article h1').textContent,doc.title);assert(d.querySelectorAll('.article figure').length>=2);}
 w.location.hash='#/browse/research';await waitFor(()=>d.querySelector('.library-heading h1')?.textContent==='研究结果与分析','results catalogue');assert.equal(d.querySelectorAll('.record-row').length,6+allStepPlans.length);
 // Every old document and all former family routes must stop before loading an article.
 for(const id of archived){w.location.hash='#/doc/'+id;await waitFor(()=>d.querySelector('.library-heading h1')?.textContent==='历史内容已归档'&&w.location.hash==='#/doc/'+id,'archived '+id);assert(!d.querySelector('.article'));}
 const oldRoutes=['#/browse/algorithms','#/browse/algorithm-knowledge',...w.READER_ALGORITHMS.families.flatMap(f=>['#/algorithm/'+f.id+'/knowledge','#/algorithm/'+f.id+'/results'])];
 for(const url of oldRoutes){w.location.hash=url;await waitFor(()=>w.location.hash===url&&d.querySelector('.library-heading h1')?.textContent==='历史内容已归档','old family '+url);assert(!d.querySelector('.algorithm-card'));}
 d.querySelector('.empty-state a').click();await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===plan.source,'return to plan');
 d.querySelector('#searchButton').click();const input=d.querySelector('#searchInput');
 for(const query of ['QUEST','剩余资源','算法实验规划',...restored.map(doc=>doc.title),...allStepPlans.map(doc=>doc.title),...allStepResults.map(doc=>doc.title),...allStepCommands.map(doc=>doc.title)]){
  input.value=query;input.dispatchEvent(new w.Event('input',{bubbles:true}));await tick(200);
  for(const link of d.querySelectorAll('.search-result')){const href=link.getAttribute('href');assert(!href.startsWith('#/algorithm/'));if(href.startsWith('#/doc/'))assert(!archived.has(href.slice(6).split('?')[0]));}
  if(query==='算法实验规划')assert(d.querySelector('.search-result[href="'+planUrl+'"]'));
  const match=restored.find(doc=>doc.title===query);if(match)assert(d.querySelector('.search-result[href="#/doc/'+match.id+'"]'),'Restored analysis not searchable: '+query);
  const stepMatch=[...allStepPlans,...allStepResults,...allStepCommands].find(doc=>doc.title===query);if(stepMatch)assert(d.querySelector('.search-result[href="#/doc/'+stepMatch.id+'"]'),'Step not searchable: '+query);
 }
 d.querySelector('#closeSearch').click();w.location.hash='#/bookmarks';await waitFor(()=>d.querySelector('.record-row'),'visible bookmark');
 assert.equal(d.querySelectorAll('.record-row').length,2);assert(d.querySelector('.record-row[href="#/doc/'+restored[0].id+'"]'));assert.deepEqual(JSON.parse(values.get('latency-reader:bookmarks')),retainedBookmarks);
 for(const id of Object.values(published.knowledgeTopics)){w.location.hash='#/doc/'+id;await waitFor(()=>d.querySelector('.source-label')?.getAttribute('title')===published.docs.find(x=>x.id===id).source,'retained knowledge '+id);for(const a of d.querySelectorAll('.article a[href^="#/doc/"]'))assert(!archived.has(a.getAttribute('href').slice(6).split('?')[0]));}
 assert.deepEqual(errors,[]);
 const report={status:'PASS',archivedDocuments:archived.size,restoredAnalyses:restored.map(doc=>doc.id),restoredSourceAndPayloadHashes:true,oldRoutesChecked:oldRoutes.length,publishedDocuments:published.docs.length,newPlan:{id:plan.id,source:plan.source,sha256:plan.sha256,toc:plan.toc.length,firstPerson:true},stepPair:{step:stepPlan.researchStep,planId:stepPlan.id,resultId:stepResult.id,resultStatus:stepResult.status,mutualLinks:true,baselineReusesThreeExistingCompactRuns:true,additionalRuns:0,fiveNumberedExperiments:[1,2,3,4,5],remainingEmptyResults:allStepResults.length-1},publishedResultTopics:Object.keys(published.experimentStages),sidebarAndHome:true,searchAndBookmarkFiltering:true,bookmarkStoragePreserved:true,coreKnowledgeRetained:Object.keys(published.knowledgeTopics).length,papersAndProtocolsRetained:true,consoleErrors:errors,scope:'Offline DOM publication checks; five original analyses restored without editing data; no wireless experiment or screenshot/layout certification.'};
 fs.writeFileSync(path.join(root,'校验/算法旧页下架与新规划核验_20261110.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));dom.window.close();
})().catch(error=>{console.error(error.stack);process.exitCode=1;});
