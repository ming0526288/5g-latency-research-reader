const fs=require('fs');
const [pkg,input,output]=process.argv.slice(2);
const katex=require(pkg);
const requests=JSON.parse(fs.readFileSync(input,'utf8'));
const errors=[];
const html=requests.map((r,i)=>{
 try {
  const value=katex.renderToString(r.tex,{displayMode:r.display,throwOnError:true,strict:'ignore',trust:false,output:'htmlAndMathml'});
  return `<span class="${r.display?'math-display':'math-inline'}">${value}</span>`;
 } catch(e){errors.push({index:i,tex:r.tex,error:e.message});return '';}
});
fs.writeFileSync(output,JSON.stringify({html,errors}));
