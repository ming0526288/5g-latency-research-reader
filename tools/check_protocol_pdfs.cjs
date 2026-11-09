/* Functional checks of real reader routes. PDF pixels are checked separately. */
const fs=require('fs'),path=require('path'),assert=require('assert');
const {JSDOM,ResourceLoader,VirtualConsole}=require('/usr/share/nodejs/jsdom');
const root=path.resolve(__dirname,'..');
const wait=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function until(test,label){for(let i=0;i<300;i++){if(test())return;await wait(40);}throw Error('Timed out: '+label);}
class Loader extends ResourceLoader{fetch(url,options){if(options.element?.localName==='iframe'||/\.pdf(?:#|$)/i.test(url))return null;return super.fetch(url,options);}}
(async()=>{
 const errors=[],steps=[];const vc=new VirtualConsole();
 vc.on('jsdomError',e=>{if(!/navigation|scroll|PDF/i.test(e.message))errors.push(e.message);});
 const dom=await JSDOM.fromFile(path.join(root,'index.html'),{resources:new Loader(),runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
  w.scrollTo=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};w.matchMedia=()=>({matches:false});w.IntersectionObserver=class{observe(){}disconnect(){}};
  w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;};
  const data=new Map();Object.defineProperty(w,'localStorage',{value:{getItem:k=>data.get(k)??null,setItem:(k,v)=>data.set(k,v)}});
 }});
 const w=dom.window,d=w.document;
 try{
  await until(()=>d.querySelectorAll('.path-card').length===6,'entry');
  const ids=w.READER_CATALOG.protocols.map(p=>p.id);
  w.location.hash='#/library/protocols';await until(()=>d.querySelector('#protocolList'),'library');
  assert(d.querySelector('#protocolList').textContent.includes('PDF 预览'));steps.push('Protocol library reads PDF by default');
  w.location.hash='#/doc/kc3e4e8560cabef23';await until(()=>d.querySelector('.article'),'basic explanation');
  const figureLink=[...d.querySelectorAll('.article a')].find(a=>a.textContent.includes('点击直达本地转换 PDF 第 49 页'));
  assert(figureLink,'Figure reference is a real direct link');figureLink.click();
  await until(()=>d.querySelector('.pdf-frame')?.title.includes('23.501'),'figure PDF view');
  assert(d.querySelector('.pdf-frame').getAttribute('src').includes('#page=49&zoom=95'));
  assert.equal(d.querySelector('#pdfPage').value,'49');assert(!d.querySelector('.protocol-article'));
  assert(d.querySelector('#main').textContent.includes('非 3GPP 官方下载 PDF'));
  assert([...d.querySelectorAll('.pdf-controls a')].some(a=>a.getAttribute('href').endsWith('.docx')));
  steps.push('Exact architecture figure opens converted PDF page 49, with original Word/ZIP preserved');
  d.querySelector('#nextPdf').click();await until(()=>d.querySelector('#pdfPage')?.value==='50','next page');
  d.querySelector('#prevPdf').click();await until(()=>d.querySelector('#pdfPage')?.value==='49','previous page');
  const total=Number(d.querySelector('#pdfPage').max);d.querySelector('#pdfPage').value=String(total+100);d.querySelector('#goPdf').click();
  await until(()=>d.querySelector('#pdfPage')?.value===String(total),'page bounds');steps.push('Previous/next/page input and bounds work');
  w.location.hash='#/protocol/23.501?clause=4.2.7&view=text';
  await until(()=>d.querySelector('.protocol-article .section-found')?.id==='clause-4-2-7','text clause search');
  const pdfLink=[...d.querySelectorAll('.protocol-tools a')].find(a=>a.textContent.includes('PDF 预览'));assert(pdfLink);pdfLink.click();
  const first=w.READER_CATALOG.protocols.find(p=>p.spec==='23.501');
  await until(()=>d.querySelector('#pdfPage')?.value===String(w.READER_PROTOCOL_PDFS.documents[first.id].clausePages['4.2.7']),'clause PDF page');
  steps.push('Clause text search and return to PDF preserve the requested clause');
  w.location.hash='#/protocol/23.501?version=19.0.0';await until(()=>d.querySelector('.source-notice strong')?.textContent.includes('不能视为相同版本'),'version mismatch');
  steps.push('Version mismatch remains explicit in PDF mode');
  const manifest=w.READER_PROTOCOL_PDFS.documents;
  assert(ids.every(id=>manifest[id]),'All local original parts have a PDF entry');
  for(const p of w.READER_CATALOG.protocols){
   const pdf=manifest[p.id];assert.equal(pdf.source_sha256,p.sha256);assert(fs.existsSync(path.join(root,pdf.file)));assert(pdf.pages>0);
  }
  const multi=w.READER_CATALOG.protocols.filter(p=>p.spec==='24.501');
  w.location.hash='#/protocol/24.501';await until(()=>d.querySelector('#protocolPart')&&d.querySelector('.pdf-frame')?.title.includes('24.501'),'multi-part PDF');
  const selected=multi.find(p=>p.id===d.querySelector('#protocolPart').value);assert(!selected.part.includes('cover'));
  const last=multi[multi.length-1];d.querySelector('#protocolPart').value=last.id;d.querySelector('#protocolPart').dispatchEvent(new w.Event('change'));
  await until(()=>d.querySelector('.pdf-frame')?.getAttribute('src').includes(last.part+'.pdf'),'multi-part change');
  steps.push('All 34 source-matched PDF previews exist; multipart selection defaults to main body and switches correctly');
  assert.deepEqual(errors,[]);
  const report={status:'PASS',steps,parts:ids.length,scope:'Real local reader scripts and DOM routes; PDF native viewer pixels and remote client access checked separately.'};
  fs.writeFileSync(path.join(root,'校验/协议PDF阅读交互核验.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
 }finally{dom.window.close();}
})().catch(error=>{console.error(error.stack||String(error));process.exitCode=1;});
