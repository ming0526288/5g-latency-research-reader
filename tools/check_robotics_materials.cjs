/* Scoped checks for the four new papers and the local industrial standard. */
const fs=require('fs'),path=require('path'),assert=require('assert'),crypto=require('crypto');
const {JSDOM,ResourceLoader,VirtualConsole}=require('/usr/share/nodejs/jsdom');
const root=path.resolve(__dirname,'..'), wait=ms=>new Promise(r=>setTimeout(r,ms));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(path.join(root,p))).digest('hex');
async function until(fn,label){for(let i=0;i<250;i++){if(fn())return;await wait(40);}throw Error('Timeout: '+label);}
class Local extends ResourceLoader{fetch(url,options){if(options.element?.localName==='iframe')return null;return super.fetch(url,options);}}
(async()=>{
 const errors=[],steps=[],vc=new VirtualConsole();
 vc.on('jsdomError',e=>{if(!/navigation|scroll|PDF/i.test(e.message))errors.push(e.message);});
 const dom=await JSDOM.fromFile(path.join(root,'index.html'),{resources:new Local(),runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
  w.scrollTo=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};w.matchMedia=()=>({matches:false});w.IntersectionObserver=class{observe(){}disconnect(){}};
  const storage=new Map();Object.defineProperty(w,'localStorage',{value:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)}});
  w.HTMLDialogElement.prototype.showModal=function(){this.open=true};w.HTMLDialogElement.prototype.close=function(){this.open=false};
 }});
 const w=dom.window,d=w.document;
 try{
  await until(()=>d.querySelector('.path-card'),'home');
  const cat=w.READER_CATALOG, ids=['P36','P37','P38','P39'];
  w.location.hash='#/library/papers';await until(()=>d.querySelector('#paperFilter'),'library');
  d.querySelector('#paperFilter').value='协作机器人';d.querySelector('#paperFilter').dispatchEvent(new w.Event('input'));
  assert(d.querySelector('#paperList a[href="#/paper/P36"]'));steps.push('Paper library finds P36 by its Chinese title');
  for(const id of ids){
   const source=cat.papers.find(p=>p.id===id);assert(source);assert.equal(hash(source.file),source.sha256);
   w.location.hash='#/paper/'+id+'?page=2';
   await until(()=>d.querySelector('#chinesePdfFrame')?.getAttribute('src').includes(id+'.zh.pdf#page=2'),'paired PDF '+id);
   assert.equal(d.querySelectorAll('.pdf-frame').length,2);
   const entry=w.READER_PAPER_TRANSLATIONS.papers[id];assert.equal(entry.sourceSHA,source.sha256);assert.equal(hash(entry.file),entry.sha256);assert.equal(entry.pages,source.pages);
   assert(d.querySelector('#chinesePdfFrame').getAttribute('src').includes('&zoom=95'));
   assert(d.querySelector('.pdf-translation').textContent.includes('尚未完成逐页校对'));
   d.querySelector('#zhPdfPage').value='9999';d.querySelector('#goZhPdf').click();assert.equal(d.querySelector('#zhPdfPage').value,String(source.pages));
   d.querySelector('#syncZhPdf').click();assert.equal(d.querySelector('#zhPdfPage').value,'2');assert.equal(d.querySelector('#pdfPage').value,'2');
  }
  steps.push('All four originals and Chinese drafts have matching SHA/page counts and independent bounded paging');
  w.location.hash='#/library/protocols';await until(()=>d.querySelector('#protocolFilter'),'protocol library');
  d.querySelector('#protocolFilter').value='信息物理';d.querySelector('#protocolFilter').dispatchEvent(new w.Event('input'));assert(d.querySelector('a[href="#/protocol/22.104"]'));
  w.location.hash='#/protocol/22.104?clause=3.1';
  await until(()=>d.querySelector('#chinesePdfFrame')?.getAttribute('src').includes('sa8970741f141.zh.pdf'),'protocol Chinese PDF');
  const source=cat.protocols.find(p=>p.spec==='22.104'),pdf=w.READER_PROTOCOL_PDFS.documents[source.id],entry=w.READER_PROTOCOL_TRANSLATIONS.papers[source.id];
  assert.equal(source.version,'19.2.0');assert(source.file.endsWith('.doc'));assert.equal(hash(source.file),source.sha256);assert.equal(pdf.source_sha256,source.sha256);
  assert.equal(hash(pdf.file),pdf.sha256);assert.equal(entry.sourceSHA,pdf.sha256);assert.equal(hash(entry.file),entry.sha256);assert.equal(entry.pages,105);
  assert.equal(d.querySelectorAll('.pdf-frame').length,2);assert.equal(d.querySelector('#pdfPage').value,String(pdf.clausePages['3.1']));
  d.querySelector('#zhPdfPage').value='999';d.querySelector('#goZhPdf').click();assert.equal(d.querySelector('#zhPdfPage').value,'105');
  steps.push('TS 22.104 DOC/ZIP retained, readable original/Chinese 105-page PDFs, actual clause mapping and paging');
  w.READER_PROTOCOL_TRANSLATIONS.papers[source.id]={...entry,sourceSHA:'stale'};
  w.location.hash='#/protocol/22.104?page=2';await until(()=>d.querySelector('#main').textContent.includes('需要重新生成译稿'),'stale translation');assert(!d.querySelector('#chinesePdfFrame'));
  w.READER_PROTOCOL_TRANSLATIONS.papers[source.id]=entry;
  steps.push('A protocol draft from an outdated converted source is not displayed as matching');
  d.querySelector('#searchButton').click();d.querySelector('#searchInput').value='信息价值';d.querySelector('#searchInput').dispatchEvent(new w.Event('input'));
  await until(()=>d.querySelector('#searchResults a[href="#/paper/P39"]'),'Chinese global search');
  assert.deepEqual(errors,[]);
  const report={status:'PASS',papers:ids,protocol:'22.104 V19.2.0',steps,errors,scope:'Actual local reader DOM/file hashes/paging/search; not translation semantic certification or native PDF pixel verification.'};
  fs.writeFileSync(path.join(root,'校验/机器人闭环补充资料核验.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
 }finally{w.close();}
})().catch(e=>{console.error(e.stack);process.exitCode=1});
