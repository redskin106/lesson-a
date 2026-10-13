// Regression test for the motion layer: node regress.mjs [file]
import chromium from '@sparticuz/chromium';
import puppeteer from 'puppeteer-core';
import {fileURLToPath} from 'url'; const S=fileURLToPath(new URL('../',import.meta.url));
const FILE=process.argv[2]||'primer-motion-v2.html';
const b=await puppeteer.launch({args:chromium.args,executablePath:await chromium.executablePath(),headless:'shell'});
const w=ms=>new Promise(r=>setTimeout(r,ms));
let fails=0; const ok=(n,c,x)=>{console.log((c?'PASS ':'FAIL ')+n+(c?'':'  '+JSON.stringify(x)));if(!c)fails++};
const newPage=async(vw=400,vh=720)=>{const p=await b.newPage();await p.setViewport({width:vw,height:vh});await p.setRequestInterception(true);p.on('request',r=>/googleapis|gstatic/.test(r.url())?r.abort():r.continue());p.on('pageerror',e=>{console.log('PAGEERR',e.message);fails++});await p.goto('file://'+S+FILE);await w(1800);return p};
const cls=(p,sel)=>p.evaluate(s=>{var e=document.querySelector(s);return e?e.className.replace(/\s+/g,' '):null},sel);
const ev=(p,f,...a)=>p.evaluate(f,...a);

// ---- single card
let p=await newPage();
await ev(p,()=>{localStorage.clear();openSingle(singleCards.findIndex(c=>c.word==='rectangle'))}); await w(1800);
const top=()=>ev(p,()=>document.getElementById('sc-scroll').scrollTop);
await p.evaluate(()=>{window.__l=0;var c=document.getElementById('sc-scroll');var o=c.scrollBy;c.scrollBy=function(){window.__l++;return o.apply(this,arguments)}});
await w(7000);
ok('single: no auto-scroll while idle',(await ev(p,()=>window.__l))===0);
ok('single: audio pulses first',/mo-cue/.test(await cls(p,'#screen-single .word-audio')));
ok('single: flip does not pulse before audio',!/mo-cue/.test(await cls(p,'#screen-single .flip-show')||''));
ok('single: stamp New',(await ev(p,()=>document.querySelector('#screen-single .mo-stamp').textContent))==='New');
await ev(p,()=>document.querySelector('#screen-single .word-audio').click()); await w(400);
ok('single: audio marked used',/mo-used/.test(await cls(p,'#screen-single .word-audio')));
await w(900);
ok('single: flip pulses after audio',/mo-cue/.test(await cls(p,'#screen-single .flip-show')));
await ev(p,()=>document.querySelector('#screen-single .flip-show').click()); await w(5500);
ok('single: scrolls after audio+flip',(await ev(p,()=>window.__l))>0);
await ev(p,()=>document.querySelector('#screen-single details.section.ex summary').click()); await w(1200);
await ev(p,()=>document.querySelector('#screen-single .sentence-audio').click()); await w(1200);
ok('single: underline draws',/\bon\b/.test(await cls(p,'#screen-single .sentence-hl')));
ok('single: stamp Learning',(await ev(p,()=>document.querySelector('#screen-single .mo-stamp').textContent))==='Learning');
// finish everything
await ev(p,()=>{['syl','snd','say','sk','rate'].forEach(k=>{var d=document.querySelector('#screen-single details.section.'+k);if(d&&!d.hidden)d.classList.add('done')});document.querySelector('#screen-single details.section.ex').classList.add('done')}); await w(1000);
ok('single: stamp Known',(await ev(p,()=>document.querySelector('#screen-single .mo-stamp').textContent))==='Known');
ok('single: counter 1 / 26',(await ev(p,()=>document.querySelector('#screen-single .mo-cnt').textContent))==='1 / 26');
// revisit via Next/Prev
await ev(p,()=>stepCard(1)); await w(500); await ev(p,()=>stepCard(-1)); await w(2600);
ok('revisit: ticks cleared',(await ev(p,()=>document.querySelectorAll('#screen-single details.section.done').length))===0);
ok('revisit: audio pulses again',/mo-cue/.test(await cls(p,'#screen-single .word-audio')));
ok('revisit: flip not pulsing yet',!/mo-cue/.test(await cls(p,'#screen-single .flip-show')||''));
ok('revisit: still Known',(await ev(p,()=>document.querySelector('#screen-single .mo-stamp').textContent))==='Known');
// Home -> open, after pressing audio+flip
await ev(p,()=>document.querySelector('#screen-single .word-audio').click()); await w(1200);
await ev(p,()=>{goIndex()}); await w(500); await ev(p,()=>openSingle(singleCards.findIndex(c=>c.word==='rectangle'))); await w(2600);
ok('home->open: only audio pulses',(await ev(p,()=>document.querySelectorAll('#screen-single .mo-cue').length))===1,await ev(p,()=>[...document.querySelectorAll('#screen-single .mo-cue')].map(x=>x.className)));
await p.close();

// ---- pair card
p=await newPage();
await ev(p,()=>{localStorage.clear();openPair(0)}); await w(2200);
ok('pair: both audios pulse',(await ev(p,()=>document.querySelectorAll('.pair-card-half .pair-word-audio.mo-cue').length))===2);
await ev(p,()=>document.querySelectorAll('.pair-card-half').forEach(h=>{h.querySelector('.pair-word-audio').click();h.querySelector('.flip-show')?.click();h.querySelector('details.section.ex summary').click();h.querySelector('.pair-s-audio')?.click()})); await w(1800);
ok('pair: section done',(await ev(p,()=>document.querySelectorAll('.pair-card-half details.section.done').length))>=1);
ok('pair: underline draws',(await ev(p,()=>document.querySelectorAll('.pair-card-half .sentence-hl.on').length))>=1);
await ev(p,()=>{goIndex()}); await w(500); await ev(p,()=>openPair(0)); await w(2600);
ok('pair revisit: ticks cleared',(await ev(p,()=>document.querySelectorAll('.pair-card-half details.section.done').length))===0);
ok('pair revisit: both audios pulse',(await ev(p,()=>document.querySelectorAll('.pair-card-half .pair-word-audio.mo-cue').length))===2);
await p.close();

// ---- monitor width, no page errors and stamp present
p=await newPage(1280,800);
await ev(p,()=>openPair(0)); await w(2000);
ok('monitor: stamps present',(await ev(p,()=>document.querySelectorAll('.pair-card-half .mo-stamp').length))===2);
ok('monitor: no horizontal overflow',await ev(p,()=>document.documentElement.scrollWidth<=innerWidth+1));
await p.close();

// ---- idle cost: timers while on the index screen
p=await newPage();
const cost=await ev(p,()=>new Promise(res=>{var n=0,o=window.requestAnimationFrame;var t0=performance.now();var mo=0;var ob=new MutationObserver(m=>mo+=m.length);ob.observe(document.documentElement,{subtree:true,attributes:true,childList:true});setTimeout(()=>{ob.disconnect();res(mo)},3000)}));
ok('index screen idle: no DOM churn',cost<5,cost);
await p.close();
await b.close(); console.log(fails?('FAILED '+fails):'ALL PASS'); process.exit(fails?1:0);
