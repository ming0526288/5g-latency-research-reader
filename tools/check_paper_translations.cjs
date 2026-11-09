/* Actual reader DOM and local PDF manifests; native PDF rendering is checked separately. */
const fs=require('fs'),path=require('path'),assert=require('assert'),crypto=require('crypto');
const {JSDOM,ResourceLoader,VirtualConsole}=require('/usr/share/nodejs/jsdom');
const root=path.resolve(__dirname,'..');
class Local extends ResourceLoader{fetch(url,options){if(options.element?.localName==='iframe')return null;return super.fetch(url,options);}}
const wait=ms=>new Promise(r=>setTimeout(r,ms));
async function until(fn,label){for(let i=0;i<200;i++){if(fn())return;await wait(40);}throw Error('Timeout: '+label);}
(async()=>{
 const errors=[],steps=[];const vc=new VirtualConsole();vc.on('jsdomError',e=>{if(!/navigation|scroll|PDF/i.test(e.message))errors.push(e.message)});
 const dom=await JSDOM.fromFile(path.join(root,'index.html'),{resources:new Local(),runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){w.scrollTo=()=>{};w.matchMedia=()=>({matches:false});w.IntersectionObserver=class{observe(){}disconnect(){}};const store=new Map();Object.defineProperty(w,'localStorage',{value:{getItem:k=>store.get(k)??null,setItem:(k,v)=>store.set(k,v)}});w.HTMLDialogElement.prototype.showModal=function(){this.open=true};w.HTMLDialogElement.prototype.close=function(){this.open=false};}});
 const w=dom.window,d=w.document;await until(()=>d.querySelector('.path-card'),'home');
 w.location.hash='#/paper/P05?page=3';await until(()=>d.querySelector('#chinesePdfFrame'),'Chinese reader');
 const frames=[...d.querySelectorAll('.pdf-frame')];assert.equal(frames.length,2);assert(frames[0].getAttribute('src').includes('5_AUGUSTE'));assert(frames[1].getAttribute('src').includes('P05.zh.pdf#page=3'));assert.deepEqual([...d.querySelectorAll('.pdf-view h2')].map(e=>e.textContent),['英文原文','中文译文']);steps.push('P05 English first and Chinese second; both open page 3');
 d.querySelector('#zhPdfPage').value='99';d.querySelector('#goZhPdf').click();assert(d.querySelector('#chinesePdfFrame').getAttribute('src').includes('#page=6'));assert(d.querySelector('#nextZhPdf').disabled);assert.equal(d.querySelector('#pdfPage').value,'3');
 d.querySelector('#syncZhPdf').click();assert(d.querySelector('#chinesePdfFrame').getAttribute('src').includes('#page=3'));steps.push('Chinese independent pagination clamps to 6 and aligns with original on request');
 w.location.hash='#/paper/book?page=2';await until(()=>d.querySelector('#pdfPage')?.value==='2','textbook');assert.equal(d.querySelectorAll('.pdf-frame').length,1);assert(!d.querySelector('#chinesePdfHeading'));steps.push('Chinese textbook retains only its original reader');
 const pending=w.READER_CATALOG.papers.find(p=>p.id!=='book'&&!['generated','ready'].includes(w.READER_PAPER_TRANSLATIONS?.papers?.[p.id]?.status));if(pending){w.location.hash='#/paper/'+pending.id+'?page=1';await until(()=>d.querySelector('#refreshZhPdf'),'pending paper');assert.equal(d.querySelectorAll('.pdf-frame').length,1);assert(!d.querySelector('#chinesePdfFrame'));steps.push('Unfinished papers have no fake PDF link or iframe');}
 w.location.hash='#/library/papers';await until(()=>d.querySelector('#paperFilter'),'library');await wait(100);d.querySelector('#paperFilter').value='中文';d.querySelector('#paperFilter').dispatchEvent(new w.Event('input'));assert(d.querySelector('#paperList').textContent.includes('AUGUSTE'));steps.push('Library Chinese filter identifies the actual completed translation');
 const manifest=JSON.parse(fs.readFileSync(path.join(root,'说明/paper-translations.json')));const ready=Object.entries(manifest.papers).filter(([,p])=>p.status==='ready');assert(ready.length>=1);
 for(const [id,p] of ready){assert(p.visualQA==='passed');const data=fs.readFileSync(path.join(root,p.file));assert.equal(crypto.createHash('sha256').update(data).digest('hex'),p.sha256);assert.equal(p.pages,w.READER_CATALOG.papers.find(source=>source.id===id).pages);}
 const previewable=Object.entries(manifest.papers).filter(([,p])=>['generated','ready'].includes(p.status));
 for(const [id,p] of previewable){
  const source=w.READER_CATALOG.papers.find(source=>source.id===id);assert(source);assert.equal(p.pages,source.pages);const bytes=fs.readFileSync(path.join(root,p.file));assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),p.sha256);
  w.location.hash='#/paper/'+id+'?page=1';await until(()=>d.querySelector('#chinesePdfFrame')?.getAttribute('src').includes(id+'.zh.pdf#page=1'),'draft '+id);assert.equal(d.querySelectorAll('.pdf-frame').length,2);assert(d.querySelectorAll('.pdf-frame')[0].getAttribute('src').startsWith(encodeURI(source.file)));assert.equal(d.querySelector('#zhPdfPage').max,String(p.pages));
 }
 const expected=w.READER_CATALOG.papers.filter(p=>p.id!=='book').length;
 if(process.argv.includes('--require-all'))assert.equal(previewable.length,expected,'All English papers must have a real translated file and reader');
 steps.push('Every generated draft has matching bytes/page count and an actual second reader: '+previewable.length+'/'+expected);
 assert.deepEqual(errors,[]);const report={status:'PASS',scope:'DOM/navigation/local file identity; not a native-browser PDF renderer test',ready:ready.map(([id])=>id),previewable:previewable.map(([id])=>id),expected,allDisplayed:previewable.length===expected,steps,errors};fs.writeFileSync(path.join(root,'校验/中英文PDF上下阅读器核验.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));w.close();
})().catch(e=>{console.error(e.stack);process.exitCode=1});
