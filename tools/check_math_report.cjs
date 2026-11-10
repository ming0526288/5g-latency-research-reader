/* Actual reader navigation/search for the canonical formula-check report. */
const fs=require('fs'),path=require('path'),assert=require('assert');
const {JSDOM,ResourceLoader,VirtualConsole}=require('/usr/share/nodejs/jsdom');
const root=path.resolve(__dirname,'..'),wait=ms=>new Promise(r=>setTimeout(r,ms));
class Local extends ResourceLoader{fetch(url,options){if(options.element?.localName==='iframe')return null;return super.fetch(url,options);}}
async function until(fn,label){for(let i=0;i<200;i++){if(fn())return;await wait(40);}throw Error('Timeout: '+label);}
(async()=>{
 const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>{if(!/navigation|scroll|PDF/i.test(e.message))errors.push(e.message);});
 const dom=await JSDOM.fromFile(path.join(root,'index.html'),{resources:new Local(),runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
  w.scrollTo=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};w.matchMedia=()=>({matches:false});w.IntersectionObserver=class{observe(){}disconnect(){}};
  const storage=new Map();Object.defineProperty(w,'localStorage',{value:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)}});
  w.HTMLDialogElement.prototype.showModal=function(){this.open=true};w.HTMLDialogElement.prototype.close=function(){this.open=false};
 }});
 const w=dom.window,d=w.document;
 try{
  await until(()=>d.querySelector('.path-card'),'home');
  const item=w.READER_CATALOG.docs.find(x=>x.title==='39 篇论文译稿公式核查与修复说明');assert(item);
  w.location.hash='#/doc/'+item.id;await until(()=>d.querySelector('#main').textContent.includes('50,869'),'report body');
  const table=[...d.querySelectorAll('#main table')].find(t=>t.textContent.includes('位置记录数'));assert(table);assert.equal(table.querySelectorAll('tbody tr').length,39);
  assert(d.querySelector('#main a[href="#/paper/P39?page=2"]'));
  assert(d.querySelector('#main').textContent.includes('扫描公式不自动认证') || d.querySelector('#main').textContent.includes('OCR 数学不自动认证'));
  const priority=w.READER_CATALOG.docs.find(x=>x.source==='说明/文献导读/39篇文献重要性排序与方法效果简述.md');assert(priority);
  w.location.hash='#/doc/'+priority.id;await until(()=>d.querySelector('#main a[href="#/doc/'+item.id+'"]'),'navigation from literature guide');
  d.querySelector('#searchButton').click();d.querySelector('#searchInput').value='公式核查';d.querySelector('#searchInput').dispatchEvent(new w.Event('input'));
  await until(()=>d.querySelector('#searchResults a[href="#/doc/'+item.id+'"]'),'global search result');
  assert.deepEqual(errors,[]);
  const report={status:'PASS',document:item.id,paperRows:39,steps:['Canonical report loaded with current scope/counts and source links','Literature guide reaches report','Global search finds the generated report'],errors,scope:'Reader DOM/navigation/search only; no new mathematical theorem or wireless experiment'};
  fs.writeFileSync(path.join(root,'校验/公式核查说明网页与搜索核验.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
 }finally{w.close();}
})().catch(e=>{console.error(e.stack);process.exitCode=1;});
