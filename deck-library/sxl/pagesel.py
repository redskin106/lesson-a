"""Page selector (teacher control, decided 11 Nov 2026, built 23 Nov): click the page counter (bottom left) or press G.
A grid of every slide, grouped by phase colour, current page highlighted, optional slides marked. Click a card to jump.
Or type a page number and press Enter. Escape closes. Wrong numbers do nothing. Works in every interactive deck."""
from . import core

core.EXT_CSS.append("""
#cnt{cursor:pointer;pointer-events:auto}#cnt:hover{color:#6a35e8}
#psel{position:fixed;inset:0;z-index:9999;display:none;background:rgba(28,20,60,.55);backdrop-filter:blur(6px);align-items:center;justify-content:center;font-family:O,sans-serif}
#psel.on{display:flex}
#psp{width:min(1500px,94vw);max-height:90vh;overflow:auto;background:rgba(255,255,255,.94);border-radius:36px;padding:26px 30px 30px;box-shadow:0 30px 80px rgba(20,10,60,.4)}
#psh{display:flex;align-items:center;gap:22px;margin-bottom:18px;font-weight:800;color:#1c1b2e;font-size:26px}
#psh .pgo{margin-left:auto;display:flex;align-items:center;gap:10px;font-size:22px;color:#6a35e8}
#psn{min-width:110px;padding:8px 18px;border-radius:999px;background:#f1ecff;border:3px solid #fff;text-align:center;font-size:26px;color:#6a35e8}
#psg{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px}
.psc{position:relative;padding:12px 14px 12px 18px;border-radius:22px;background:#f6f3ff;border:3px solid transparent;cursor:pointer;min-height:88px;display:flex;flex-direction:column;gap:6px}
.psc:hover{border-color:#9a5cff;background:#fff}.psc.cur{border-color:#ff4fa3;background:#fff;box-shadow:0 0 0 4px rgba(255,79,163,.25)}
.psc b{font-size:24px;color:#6a35e8;line-height:1}.psc span{font-size:17px;font-weight:700;color:#1c1b2e;line-height:1.2}
.psc i{position:absolute;left:0;top:14px;bottom:14px;width:7px;border-radius:4px;background:var(--pc,#9a5cff)}
.psc em{position:absolute;right:12px;top:10px;font-style:normal;font-size:14px;font-weight:800;color:#8a7bb8}
.psc.opt{border-style:dashed;border-color:#d9d0f5}.psc.opt.cur{border-color:#ff4fa3}
#pskey{font-size:15px;font-weight:700;color:#8a7bb8;margin-top:14px;text-align:center}
""")

core.EXT_JS.append(r"""
(function(){
 var PC={ENGAGE:'#ffb347',ACTIVATE:'#2bd9b6',STUDY:'#9a5cff',RECAP:'#ff6b78',EXIT:'#ff6b78',night:'#4a3a8a'};
 var ov=document.createElement('div');ov.id='psel';
 ov.innerHTML='<div id="psp"><div id="psh"><span>Jump to page</span><span class="pgo">type a number, then Enter <span id="psn">—</span></span></div><div id="psg"></div><div id="pskey">G opens · Esc closes · ← → still move one page</div></div>';
 document.body.appendChild(ov);
 var buf='';
 function build(){var g=document.getElementById('psg');g.innerHTML='';
  slides.forEach(function(s,i){var c=document.createElement('div');c.className='psc'+(i===cur?' cur':'')+(s.dataset.opt?' opt':'');c.dataset.i=i;
   c.style.setProperty('--pc',PC[(s.dataset.ph||'').toUpperCase()]||PC[s.dataset.ph]||'#9a5cff');
   var m=+s.dataset.min;c.innerHTML='<i></i><b>'+(i+1)+'</b><span>'+(s.dataset.label||'')+'</span>'+(s.dataset.opt?'<em>optional</em>':(m?'<em>'+(m%1?m.toFixed(1):m)+' min</em>':''));g.appendChild(c)})}
 function open(){buf='';document.getElementById('psn').textContent='—';build();ov.classList.add('on');var c=document.querySelector('.psc.cur');if(c)c.scrollIntoView({block:'center'})}
 function close(){ov.classList.remove('on')}
 function jump(i){if(i>=0&&i<slides.length){close();go(i)}}
 ov.addEventListener('click',function(e){var c=e.target.closest('.psc');if(c){jump(+c.dataset.i);return}if(e.target===ov)close()});
 document.getElementById('cnt').addEventListener('click',function(e){e.stopPropagation();ov.classList.contains('on')?close():open()});
 document.addEventListener('keydown',function(e){
  var on=ov.classList.contains('on');
  if(!on){if((e.key==='g'||e.key==='G')&&!e.ctrlKey&&!e.metaKey&&!e.altKey){e.preventDefault();e.stopImmediatePropagation();open()}return}
  e.stopImmediatePropagation();
  if(e.key==='Escape'||e.key==='g'||e.key==='G'){e.preventDefault();close();return}
  if(/^[0-9]$/.test(e.key)){buf=(buf+e.key).slice(-3);document.getElementById('psn').textContent=buf;e.preventDefault();return}
  if(e.key==='Backspace'){buf=buf.slice(0,-1);document.getElementById('psn').textContent=buf||'—';e.preventDefault();return}
  if(e.key==='Enter'){e.preventDefault();var n=parseInt(buf,10);if(n>=1&&n<=slides.length)jump(n-1);else{buf='';document.getElementById('psn').textContent='—'}}
 },true);
})();
""")
