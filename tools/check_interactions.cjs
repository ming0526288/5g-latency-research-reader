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
 await waitFor(()=>d.querySelector('.article').textContent.includes('两个 Priority = 5 的 UE'),'mixed-language spacing in actual foundation');
 const original=d.createElement('article');original.innerHTML=w.READER_CONTENT[basic.id].html;
 const article=d.querySelector('.article');
 const texts=(root,selector)=>[...root.querySelectorAll(selector)].map(el=>el.textContent);
 assert.deepEqual(texts(article,'code'),texts(original,'code'));
 assert.deepEqual([...article.querySelectorAll('.katex,math')].map(el=>el.outerHTML),[...original.querySelectorAll('.katex,math')].map(el=>el.outerHTML));
 assert.deepEqual([...article.querySelectorAll('[id]')].map(el=>el.id),[...original.querySelectorAll('[id]')].map(el=>el.id));
 assert.deepEqual([...article.querySelectorAll('a')].map(el=>el.getAttribute('href')),[...original.querySelectorAll('a')].map(el=>el.getAttribute('href')));
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
 steps.push('实际Priority段落及动态粗体/内联代码边界已补间距；单位排版正常；代码、URL、文件名、公式、协议原文、链接与标题ID保持；重复处理不累加空格');
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
