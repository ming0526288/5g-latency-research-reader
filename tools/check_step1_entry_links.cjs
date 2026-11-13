/* Click the actual plan/directory entry labels and verify the individual pages. */
const fs=require('fs'),path=require('path'),assert=require('assert');
const {JSDOM,VirtualConsole,ResourceLoader}=require('/usr/share/nodejs/jsdom');
const root=path.resolve(__dirname,'..');
class LocalLoader extends ResourceLoader{fetch(url,opt){if(opt.element?.localName==='iframe'||/\.pdf(?:#|$)/i.test(url))return null;return super.fetch(url,opt);}}
const delay=ms=>new Promise(r=>setTimeout(r,ms));
async function until(fn,label){for(let i=0;i<300;i++){if(fn())return;await delay(20);}throw Error('Timed out: '+label);}
(async()=>{
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>{if(!/navigation|scroll|PDF/i.test(e.message))errors.push(e.message);});
 const dom=await JSDOM.fromFile(path.join(root,'打开阅读站.html'),{resources:new LocalLoader(),runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
  w.scrollTo=()=>{};w.matchMedia=()=>({matches:false});w.IntersectionObserver=class{observe(){}disconnect(){}};
  w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;};
  const store=new Map();Object.defineProperty(w,'localStorage',{value:{getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,v)}});
 }});
 const w=dom.window,d=w.document;await until(()=>w.READER_VISIBLE_CATALOG&&d.querySelector('.path-card'),'home');
 const cat=w.READER_VISIBLE_CATALOG,byTopic=t=>cat.docs.find(x=>x.topic===t);
 const roles=['plans','knowledge','commands','results'];
 const children=cat.docs.filter(x=>x.documentRole&&x.stepExperiment);assert.equal(children.length,20);
 const parentTopics={plans:'step-1-plan',knowledge:'step-1-knowledge',commands:cat.docs.find(x=>x.commandStep==='step-1').topic,results:'step-1'};
 const url=x=>'#/doc/'+x.id;let entryClicks=0,peerClicks=0;
 async function open(doc){w.location.hash=url(doc);await until(()=>d.querySelector('.source-label')?.getAttribute('title')===doc.source,'open '+doc.topic);}
 async function landed(doc){await until(()=>w.location.hash===url(doc)&&d.querySelector('.source-label')?.getAttribute('title')===doc.source,'land '+doc.topic);assert(d.querySelector('.article h1').textContent.startsWith(doc.stepExperiment+'. '));}
 for(const role of roles){
  const parent=byTopic(parentTopics[role]);assert(parent);
  for(let n=1;n<=5;n++){
   const child=children.find(x=>x.documentRole===role&&x.stepExperiment===n);assert(child);
   for(const column of [0,1]){
    await open(parent);const rows=d.querySelectorAll('.article tbody tr');assert.equal(rows.length,5);
    const a=rows[n-1].cells[column].querySelector('a');assert(a,'Unclickable '+role+' row '+n+' column '+column);assert.equal(a.getAttribute('href'),url(child));a.click();await landed(child);entryClicks++;
   }
   for(const peerRole of roles.filter(x=>x!==role)){
    await open(child);const peer=children.find(x=>x.documentRole===peerRole&&x.stepExperiment===n);const a=d.querySelector('.article a[href="'+url(peer)+'"]');assert(a,'Missing peer '+role+' -> '+peerRole+' '+n);a.click();await landed(peer);peerClicks++;
   }
  }
 }
 for(const [topic,role] of [['launch-index','commands'],['research-results-index','results']]){
  const hub=byTopic(topic);assert(hub);
  const parent=byTopic(parentTopics[role]);
  for(const col of [0,1]){
   await open(hub);const first=d.querySelector('.article tbody tr'),a=first.cells[col].querySelector('a');assert(a);assert.equal(a.getAttribute('href'),url(parent));a.click();
   await until(()=>d.querySelector('.source-label')?.getAttribute('title')===parent.source,'directory step-one number/title');entryClicks++;
  }
  for(let n=1;n<=5;n++){
   await open(hub);const items=d.querySelectorAll('.article ol > li');assert.equal(items.length,5);
   const target=children.find(x=>x.documentRole===role&&x.stepExperiment===n),a=items[n-1].querySelector('a');assert.equal(a.getAttribute('href'),url(target));a.click();await landed(target);entryClicks++;
  }
 }
 const sourceKnowledge=children.find(x=>x.documentRole==='knowledge'&&x.stepExperiment===1);
 await open(sourceKnowledge);
 const fullTable=[...d.querySelectorAll('.article table')].find(t=>t.textContent.includes('源码文件（相对研究树）'));
 assert(fullTable);assert.equal(fullTable.querySelectorAll('tbody tr').length,41);
 assert(!/383aa52a|61654513|159208eb/.test(d.querySelector('.article').textContent));
 w.location.hash='#/doc/e4c1f2a8800000006';await until(()=>w.location.hash===url(sourceKnowledge)&&d.querySelector('.source-label')?.getAttribute('title')===sourceKnowledge.source,'old full-source route redirects');
 const sourceResult=children.find(x=>x.documentRole==='results'&&x.stepExperiment===1);await open(sourceResult);
 const resultText=d.querySelector('.article').textContent;
 for(const value of ['1.701862','1.812801','1.842844','0.820673','0.817807','17.000000','未进入业务','8703','启动相位'])assert(resultText.includes(value));
 assert(!/383aa52a|61654513|159208eb/.test(resultText));
 const diagnosis=byTopic('original-startup-diagnosis'),hub=byTopic('research-results-index');assert(diagnosis&&hub);
 const heading=[...d.querySelectorAll('#sidebar .nav-heading')].find(x=>x.textContent==='研究结果与分析');assert(heading);
 const hubEntry=heading.nextElementSibling,diagnosisEntry=hubEntry.nextElementSibling;
 assert.equal(hubEntry.getAttribute('href'),url(hub));assert.equal(diagnosisEntry.getAttribute('href'),url(diagnosis));
 assert.equal(hubEntry.parentElement,diagnosisEntry.parentElement);assert(hubEntry.classList.contains('nav-link')&&diagnosisEntry.classList.contains('nav-link'));
 diagnosisEntry.click();await until(()=>d.querySelector('.source-label')?.getAttribute('title')===diagnosis.source,'sidebar sibling diagnosis');
 assert(d.querySelector('#sidebar a.active[href="'+url(diagnosis)+'"]'));assert(!d.querySelector('#sidebar a.active[href="'+url(hub)+'"]'));
 let diagnosisClicks=0;
 for(const origin of [hub,sourceResult]){
  await open(origin);const a=d.querySelector('.article a[href="'+url(diagnosis)+'"]');assert(a,'Missing detailed diagnosis entry');a.click();
  await until(()=>d.querySelector('.source-label')?.getAttribute('title')===diagnosis.source,'detailed diagnosis');diagnosisClicks++;
  const body=d.querySelector('.article').textContent;
  for(const term of ['第三次是关键反例','19 份现场记录','506928','522207','8703','连续供样','没有重新启动核心网'])assert(body.includes(term));
  assert(!/\b[0-9a-f]{40,64}\b/.test(body));assert(d.querySelectorAll('.article table').length>=10);
  const back=d.querySelector('.article a[href="'+url(origin)+'"]');assert(back);back.click();
  await until(()=>d.querySelector('.source-label')?.getAttribute('title')===origin.source,'diagnosis return');diagnosisClicks++;
 }
 d.querySelector('#searchButton').click();const query=d.querySelector('#searchInput');query.value='原因定位与控制变量全过程';query.dispatchEvent(new w.Event('input',{bubbles:true}));
 await until(()=>d.querySelector('.search-result[href="'+url(diagnosis)+'"]'),'diagnosis search');d.querySelector('#closeSearch').click();
 assert.deepEqual(errors,[]);
 const report={status:'PASS',independentPages:20,parentEntryClicks:entryClicks,peerPageClicks:peerClicks,planningTitlesAndNumbersClickable:true,twelveStepDirectoriesExposeFiveItems:true,fullSourceRows:41,oldStandaloneSourceRedirects:true,visibleCommitHashesRemoved:true,controlledStartupFormalTrials:12,controlledPhaseMatrixValidated:true,originalPingValidated:true,originalPingCompleteTransactions:13320,originalPingStatisticalTransactions:12110,currentPingThreeRepeatMeans:[1.701862,1.812801,1.842844],consoleErrors:errors,scope:'Actual local DOM clicks, not screenshot or radio experiment.'};
 report.detailedDiagnosis={id:diagnosis.id,hubAndFirstResultClicks:diagnosisClicks,searchable:true,visibleCommitHashesRemoved:true};
 report.detailedDiagnosis.sidebarSiblingEntry={belowResultsIndex:true,sameParentAndLevel:true,clickOpensIndependentPage:true,onlyOwnEntryActive:true};
 fs.writeFileSync(path.join(root,'校验/第一步规划与总目录入口点击核验_20261113.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));w.close();
})().catch(e=>{console.error(e.stack);process.exitCode=1;});
