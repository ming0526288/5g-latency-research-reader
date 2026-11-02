/* Reading-only spacing; source files, machine literals and equations stay intact. */
(() => {
 'use strict';
 const han=/\p{Script=Han}/u;
 const western=/[A-Za-z0-9\u0370-\u03ff]/u;
 const blocks=new Set(['address','article','aside','blockquote','br','button','caption','dd','details','div','dl','dt','figcaption','figure','footer','form','h1','h2','h3','h4','h5','h6','header','hr','li','main','nav','ol','p','section','summary','table','tbody','td','th','thead','tr','ul']);
 const ignored='pre,script,style,textarea,input,select,math,svg,.katex,.protocol-article,.source-label,[data-no-spacing]';
 // These remain single tokens, including query strings and embedded filenames.
 const literals=/(?:[a-z][a-z0-9+.-]*:\/\/|mailto:|www\.)[^\s<>"']+|(?<![A-Za-z0-9_])(?:[A-Za-z]:[\\/]|\.{0,2}\/)[^\s<>"']+|[\w\p{Script=Han}.\/-]+\.(?:py|js|cjs|json|md|pdf|docx|zip|conf|yaml|yml|csv|pcap|html|css)\b/giu;
 const needsSpace=(left,right)=>(han.test(left)&&western.test(right))||(western.test(left)&&han.test(right));
 function prose(text){
  return text
   .replace(/(\d+(?:\.\d+)?)(Gbps|Mbps|Kbps|kbps|Gbit\/s|Mbit\/s|kbit\/s|GHz|MHz|kHz|Hz|GB|MB|KB|KiB|MiB|GiB|ms|us|ns|μs|µs|s)(?![A-Za-z0-9_])/g,'$1 $2')
   .replace(/([A-Za-z_\u0370-\u03ff][A-Za-z0-9_\u0370-\u03ff]*|5QI)[ \t]*(==|!=|<=|>=|=|<|>|≤|≥)[ \t]*([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)(?![\w.])/g,'$1 $2 $3')
   .replace(/(\p{Script=Han})([A-Za-z0-9\u0370-\u03ff])/gu,'$1 $2')
   .replace(/([A-Za-z0-9\u0370-\u03ff])(\p{Script=Han})/gu,'$1 $2');
 }
 function readableText(text){
  const pieces=[];let start=0;
  for(const match of text.matchAll(literals)){
   pieces.push(prose(text.slice(start,match.index)),match[0]);start=match.index+match[0].length;
  }
  pieces.push(prose(text.slice(start)));
  return pieces.reduce((result,piece)=>result+(result&&piece&&needsSpace(result.slice(-1),piece[0])?' ':'')+piece,'');
 }
 function apply(root){
  if(!root||root.nodeType!==1||root.matches(ignored))return;
  const entries=[];
  function visit(node,protectedText=false){
   if(node.nodeType===3){if(node.data)entries.push({node,protectedText});return;}
   if(node.nodeType!==1)return;
   if(node.matches(ignored)){entries.push(null);return;}
   const boundary=blocks.has(node.localName);
   if(boundary)entries.push(null);
   const keep=protectedText||['code','kbd','samp'].includes(node.localName);
   for(const child of node.childNodes)visit(child,keep);
   if(boundary)entries.push(null);
  }
  visit(root);
  let previous=null;
  for(const entry of entries){
   if(!entry){previous=null;continue;}
   const {node,protectedText}=entry;
   if(!protectedText){const spaced=readableText(node.data);if(spaced!==node.data)node.data=spaced;}
   if(previous&&needsSpace(previous.node.data.slice(-1),node.data[0])){
    // Put boundary spaces in prose so copying an inline command stays exact.
    if(!protectedText)node.data=' '+node.data;
    else if(!previous.protectedText)previous.node.data+=' ';
   }
   previous=entry;
  }
 }
 window.READER_TYPOGRAPHY={apply,readableText};
 // Routes, filters and search replace content dynamically. Observe text only;
 // disconnect during formatting so our own changes cannot create a loop.
 const observer=new MutationObserver(refresh);
 function refresh(){
  observer.disconnect();apply(document.body);
  observer.observe(document.body,{subtree:true,childList:true,characterData:true});
 }
 refresh();
})();
