import chromium from '@sparticuz/chromium';
import puppeteer from 'puppeteer-core';
import fs from 'fs';
import {fileURLToPath} from 'url'; const S=fileURLToPath(new URL('../',import.meta.url));
let html=fs.readFileSync(S+'primer-motion-v2.html','utf8');
const m=html.match(/<script[^>]*id="deck-data"[^>]*>([\s\S]*?)<\/script>/); const deck=JSON.parse(m[1]);
const P="x');window.__pwn=1;//", T='"><img src=x onerror=window.__pwn=1>', U='javascript:window.__pwn=1';
let n=0; for(const c of deck.cards){ 
 for(const k of Object.keys(c)){ if(typeof c[k]!=='string')continue;
  if(/^word\d?$/.test(k)) c[k]=c[k]+P; else if(/^sentence\d?$/.test(k)) c[k]=c[k]+' '+T; else if(/image|audio/i.test(k)&&c[k]) c[k]=U; else if(k==='emoji')c[k]=T } }
html=html.replace(m[1],JSON.stringify(deck)); fs.writeFileSync(S+'evil.html',html);
const b=await puppeteer.launch({args:chromium.args,executablePath:await chromium.executablePath(),headless:'shell'});
const p=await b.newPage();await p.setViewport({width:400,height:720});await p.setRequestInterception(true);p.on('request',r=>/googleapis|gstatic/.test(r.url())?r.abort():r.continue());
p.on('dialog',d=>{console.log('DIALOG',d.message());d.dismiss()});
let errs=0;p.on('pageerror',e=>{errs++;console.log('PAGEERR',e.message)});
await p.goto('file://'+S+'evil.html');await new Promise(r=>setTimeout(r,2000));
await p.evaluate(()=>{try{openSingle(0)}catch(e){window.__e=String(e)}});await new Promise(r=>setTimeout(r,800));
await p.evaluate(()=>{try{openPair(0)}catch(e){window.__e2=String(e)}});await new Promise(r=>setTimeout(r,800));
await p.evaluate(()=>{document.querySelectorAll('button').forEach(b=>{try{b.click()}catch(e){}})});await new Promise(r=>setTimeout(r,800));
console.log('exceptions:',await p.evaluate(()=>[window.__e,window.__e2]));console.log('pwned:',await p.evaluate(()=>window.__pwn||0),'errors:',errs,'injected imgs:',await p.evaluate(()=>document.querySelectorAll('img[src=x]').length));
await b.close();
