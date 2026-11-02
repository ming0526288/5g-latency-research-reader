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
 const cat=w.READER_CATALOG;const basic=cat.docs.find(x=>x.aliases.some(a=>a.endsWith('算法知识点说明/00_通信与时延基础知识.md')));
 w.location.hash='#/doc/'+basic.id;await waitFor(()=>d.querySelector('.article .katex'),'foundation');
 assert(d.querySelectorAll('.article mfrac').length>=2);assert(d.querySelector('.diagram-panel img').getAttribute('src').includes('闭环测量'));
 steps.push('基础知识真实正文加载；分式为KaTeX/MathML；已有四时间戳示意图插入');
 d.querySelector('#bookmarkDoc').click();assert(d.querySelector('#bookmarkDoc').textContent.includes('已收藏'));
 w.location.hash='#/bookmarks';await waitFor(()=>d.querySelector('.record-row'),'bookmarks');assert(d.querySelector('.record-row').textContent.includes('通信与时延'));
 steps.push('加入书签并在书签页找到原文档');
 d.querySelector('#searchButton').click();const input=d.querySelector('#searchInput');input.value='QUEST';input.dispatchEvent(new w.Event('input',{bubbles:true}));
 await waitFor(()=>d.querySelectorAll('.search-result').length>0,'search');assert(d.querySelector('.search-result').textContent.toLowerCase().includes('quest'));d.querySelector('#closeSearch').click();
 steps.push('全文搜索QUEST返回实际文档与文献结果');
 w.location.hash='#/paper/P24?page=7';await waitFor(()=>d.querySelector('.pdf-frame'),'PDF route');assert(d.querySelector('.pdf-frame').getAttribute('src').includes('#page=7'));assert.equal(d.querySelector('#pdfPage').value,'7');
 d.querySelector('#pdfPage').value='9';d.querySelector('#goPdf').click();await waitFor(()=>w.location.hash.includes('page=9')&&d.querySelector('#pdfPage')?.value==='9','PDF page control');
 steps.push('P24引用页序7及页码控件9写入真实本地PDF地址');
 await tick(80);
 w.location.hash='#/protocol/38.321?clause=5.4.5';await waitFor(()=>d.querySelector('.protocol-article')||d.querySelector('.empty-state'),'protocol');assert(d.querySelector('.protocol-article'),d.querySelector('#main').textContent+' '+failures.join('\n'));await waitFor(()=>d.querySelector('.section-found'),'clause location');
 assert.equal(d.querySelector('.section-found').id,'clause-5-4-5');assert(d.querySelector('.protocol-tools a').getAttribute('href').includes('.docx'));
 steps.push('从PDF页切换至TS38.321阅读页，定位5.4.5条，并提供原始DOCX入口');
 const theme=w.document.documentElement.dataset.theme;d.querySelector('#themeButton').click();assert.notEqual(w.document.documentElement.dataset.theme,theme);
 steps.push('主题切换控制正常');
 assert.deepEqual(failures,[]);
 const result={status:'PASS',kind:'jsdom DOM integration, not live browser rendering',steps,jsdomErrors:failures};fs.writeFileSync(path.join(root,'校验/交互逻辑校验.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));w.close();
})().catch(e=>{console.error(e.stack);const diagnostic=debugWindow?{hash:debugWindow.location.hash,mainText:debugWindow.document.querySelector('#main')?.textContent.slice(0,400),scripts:[...debugWindow.document.scripts].map(s=>s.src).slice(-5),loadedPayloads:Object.keys(debugWindow.READER_CONTENT||{})}:{};console.log(JSON.stringify(diagnostic));fs.writeFileSync(path.join(root,'校验/交互逻辑校验.json'),JSON.stringify({status:'FAIL',steps,error:e.message,jsdomErrors:failures,diagnostic},null,2));process.exitCode=1;});
