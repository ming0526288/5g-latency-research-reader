/* Verify the existing twelve-step route after the 2026-11-14 detail update. */
const fs=require('fs'),path=require('path'),assert=require('assert');
const {JSDOM,VirtualConsole,ResourceLoader}=require('/usr/share/nodejs/jsdom');
const root=path.resolve(__dirname,'..');
class LocalLoader extends ResourceLoader{fetch(url,opt){if(opt.element?.localName==='iframe'||/\.pdf(?:#|$)/i.test(url))return null;return super.fetch(url,opt);}}
const delay=ms=>new Promise(r=>setTimeout(r,ms));
async function until(fn,label){for(let i=0;i<350;i++){if(fn())return;await delay(20);}throw Error('Timed out: '+label);}
(async()=>{
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>{if(!/navigation|scroll|PDF/i.test(e.message))errors.push(e.message);});
 const dom=await JSDOM.fromFile(path.join(root,'打开阅读站.html'),{resources:new LocalLoader(),runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
  w.scrollTo=()=>{};w.matchMedia=()=>({matches:false});w.IntersectionObserver=class{observe(){}disconnect(){}};
  w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;};
  const store=new Map();Object.defineProperty(w,'localStorage',{value:{getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,v)}});
 }});
 const w=dom.window,d=w.document;await until(()=>w.READER_VISIBLE_CATALOG&&d.querySelector('.path-card'),'home');
 const cat=w.READER_VISIBLE_CATALOG,byTopic=t=>cat.docs.find(x=>x.topic===t);
 const checks=[
  ['algorithm-experiment-plan',['0.1024','0.3072','优先核验授权时机','十二步']],
  ['paper-plan',['通信 RTT','16 B','同预算非预测主动授权','2 ms']],
  ['step-2-plan',['R/N','Nr','0.1024','第五、六步']],
  ['step-5-plan',['第二步','分段闭合']],
  ['step-6-plan',['第二步','首包','因果']],
  ['step-7-plan',['两条对照轴','同预算']],
  ['step-8-plan',['优先关注的授权时机','积压服务']],
 ];
 const results=[];
 for(const [topic,terms] of checks){
  const doc=byTopic(topic);assert(doc,topic);w.location.hash='#/doc/'+doc.id;
  await until(()=>d.querySelector('.source-label')?.getAttribute('title')===doc.source,'page '+topic);
  const article=d.querySelector('.article');for(const term of terms)assert(article.textContent.includes(term),topic+': '+term);
  assert(article.querySelectorAll('h2').length>0);for(const h of doc.toc)assert(d.getElementById(h.id),topic+' toc '+h.id);
  results.push({topic,id:doc.id,terms,rendered:true});
 }
 const plans=cat.docs.filter(x=>x.researchStep&&x.topic==='step-'+x.researchStep.split('-')[1]+'-plan');
 assert.deepEqual(plans.map(x=>Number(x.researchStep.slice(5))).sort((a,b)=>a-b),Array.from({length:12},(_,i)=>i+1));
 const firstChildren=cat.docs.filter(x=>x.documentRole&&x.stepExperiment);assert.equal(firstChildren.length,20);
 for(let i=2;i<=12;i++){const doc=cat.docs.find(x=>x.researchStep==='step-'+i&&x.experimentStage==='step-'+i);assert(doc);assert.equal(doc.status,'not-started');}
 for(const topic of ['tdd','scs','multi-ue','layers','tail'])assert(cat.docs.some(x=>x.experimentStage===topic));
 d.querySelector('#searchButton').click();const input=d.querySelector('#searchInput');input.value='0.1024';input.dispatchEvent(new w.Event('input',{bubbles:true}));
 await until(()=>d.querySelector('.search-result[href="#/doc/'+byTopic('algorithm-experiment-plan').id+'"]'),'new plan search');
 assert(d.querySelector('.search-result[href="#/doc/'+byTopic('step-2-plan').id+'"]'));assert.equal(errors.length,0,errors.join('\n'));
 const report={status:'PASS',documents:results,twelveStepsPreserved:true,firstStepIndependentPages:20,steps2to12RemainNotStarted:true,fiveHistoricAnalysisPagesRetained:true,newContentSearchable:true,consoleErrors:errors,newRadioExperiments:0,scope:'Actual local DOM rendering, TOC and search; not a wireless experiment or client-browser screenshot.'};
 fs.writeFileSync(path.join(root,'校验/规划执行细化与PPT对齐核验_20261114.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));w.close();
})().catch(e=>{console.error(e);process.exitCode=1;});
