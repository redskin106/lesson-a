# Stage 1 of the build: primer-motion-real.html -> primer-notebook.html (Draw card notebook). Run build_v2.py next, or build.sh for both.
import os
S=os.path.dirname(os.path.abspath(__file__))+'/'
src=open(S+'primer-motion-real.html').read()
css=r"""
/* ---- Notebook picture: the written word beside a stand-in illustration, in the picture slot ---- */
.nb{--nb-pen:var(--sky);--nb-gold:var(--gold,#E39B00);--nb-rule:color-mix(in srgb,var(--sky) 20%,var(--surface,#fff));--nb-margin:color-mix(in srgb,#E5484D 35%,var(--surface,#fff));
 position:absolute;inset:0;z-index:2;container-type:inline-size;background-color:var(--surface,#fff);background-image:linear-gradient(to bottom,transparent calc(100% - 1.5px),var(--nb-rule) 0);background-size:100% 12.5%;border-radius:inherit}
.nb::before{content:'';position:absolute;left:9cqw;top:0;bottom:0;width:2px;background:var(--nb-margin)}
.nb .nb-sk{position:absolute;left:50%;top:-2cqw;width:48cqw;height:48cqw;margin-left:-24cqw}
.nb svg{display:block;width:100%;height:100%;overflow:visible}
.nb .nb-fill path{fill:color-mix(in srgb,var(--sky) 28%,transparent);stroke:none}
.nb .nb-sun{fill:var(--nb-gold)}
.nb .nb-line path{fill:none;stroke:var(--nb-pen);stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:0;filter:url(#nb-rough)}
.nb .nb-word{position:absolute;left:50%;transform:translateX(-50%);font-family:'Caveat','Segoe Print','Bradley Hand','Comic Sans MS',cursive;font-weight:700;line-height:1;color:var(--nb-pen);white-space:nowrap}
.nb .nb-ink{display:inline-block;clip-path:inset(-10% -14% -30% -4%)}
.nb .nb-pen{position:absolute;left:100%;top:55%;width:.14em;height:.14em;border-radius:50%;background:var(--nb-gold);opacity:0;transform:translate(-50%,-50%)}
.nb .nb-swash{position:absolute;left:0;bottom:-.12em;width:100%;height:.22em;overflow:visible}
.nb .nb-swash path{fill:none;stroke:var(--nb-gold);stroke-width:5;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:0}
.sketch-paper:has(.nb){position:relative;display:block;width:100%;max-width:320px;aspect-ratio:100/72;margin-inline:auto;overflow:hidden;padding:0}
.sketch-paper:has(.nb) .sk-emoji{display:none}
.sketch-paper.done .nb{background-color:var(--sky-tint)}
.sketch-wrap:has(.nb) .sketch-word,.sketch-wrap:has(.nb) .trio-hint{display:none}
"""
js=r"""
(function(){
 var P=function(d){return '<path pathLength="1" d="'+d+'"/>'};
 var STAND='<svg viewBox="0 0 200 200" aria-hidden="true"><g class="nb-fill">'+P('M30 44H170Q178 44 178 52V148Q178 156 170 156H30Q22 156 22 148V52Q22 44 30 44Z')+'</g><circle class="nb-sun" cx="72" cy="78" r="11"/><g class="nb-line">'+['M30 44H170Q178 44 178 52V148Q178 156 170 156H30Q22 156 22 148V52Q22 44 30 44Z','M22 140L72 100L104 126L130 106L178 140','M150 176L174 150L186 160L162 186Z','M150 176L146 190L162 186'].map(P).join('')+'</g></svg>';
 document.body.insertAdjacentHTML('beforeend','<svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="nb-rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="3.2"/></filter></svg>');
 var EASE='cubic-bezier(.45,.05,.25,1)';
 var reduced=function(){return (window.PrimerMotion&&PrimerMotion.cfg&&PrimerMotion.cfg.calm)||(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)};
 function fit(nb){
  var W=nb.clientWidth; if(!W)return; var w=nb.querySelector('.nb-word'), ink=nb.querySelector('.nb-ink');
  var fs=W*.16, avail=W*.8; w.style.fontSize=fs+'px'; var iw=ink.offsetWidth; if(iw>avail){fs=fs*avail/iw; w.style.fontSize=fs+'px'}
  w.style.top=((nb.clientHeight||W*.72)*.84-fs*.8)+'px';
 }
 function play(nb,delay){
  if(reduced())return; var lines=[].slice.call(nb.querySelectorAll('.nb-line path')), t=delay;
  lines.forEach(function(p,i){p.animate([{strokeDashoffset:1},{strokeDashoffset:0}],{duration:i===0?700:380,delay:t,easing:EASE,fill:'backwards'}); t+=i===0?560:200});
  [].forEach.call(nb.querySelectorAll('.nb-fill path,.nb-sun'),function(f){f.animate([{opacity:0},{opacity:1}],{duration:420,delay:delay+500,fill:'backwards'})});
  var ink=nb.querySelector('.nb-ink'), pen=nb.querySelector('.nb-pen'), sw=nb.querySelector('.nb-swash path'), d=520+ink.textContent.length*110, w0=t-250;
  ink.animate([{clipPath:'inset(-10% 100% -30% -4%)'},{clipPath:'inset(-10% -14% -30% -4%)'}],{duration:d,delay:w0,easing:'cubic-bezier(.6,.1,.4,1)',fill:'backwards'});
  pen.animate([{left:'0%',opacity:0},{left:'0%',opacity:1,offset:.06},{left:'100%',opacity:1,offset:.94},{left:'100%',opacity:0}],{duration:d,delay:w0,easing:'cubic-bezier(.6,.1,.4,1)',fill:'backwards'});
  sw.animate([{strokeDashoffset:1},{strokeDashoffset:0}],{duration:360,delay:w0+d,easing:EASE,fill:'backwards'});
 }
 function all(){
  [].forEach.call(document.querySelectorAll('.sketch-paper'),function(p){
   var half=p.closest('.pair-card-half'), w=half?half.querySelector('.pair-word-text'):document.getElementById('sc-word');
   var word=w&&w.textContent.trim(); if(!word)return;
   var old=p.querySelector('.nb'); if(old)old.remove();
   var nb=document.createElement('div'); nb.className='nb'; nb.setAttribute('role','img'); nb.setAttribute('aria-label',word);
   nb.innerHTML='<div class="nb-sk">'+STAND+'</div><div class="nb-word" aria-hidden="true"><span class="nb-ink"></span><i class="nb-pen"></i><svg class="nb-swash" viewBox="0 0 100 10" preserveAspectRatio="none">'+P('M1 6C25 1 55 9 99 3')+'</svg></div>';
   nb.querySelector('.nb-ink').textContent=word; p.appendChild(nb); fit(nb);
  });
 }
 document.addEventListener('toggle',function(e){var d=e.target; if(!d||!d.matches||!d.matches('details.section.sk')||!d.open)return;
  [].forEach.call(d.querySelectorAll('.nb'),function(nb){fit(nb); nb.getAnimations({subtree:true}).forEach(function(a){a.cancel()}); play(nb,350)})},true);
 ['renderSingle','renderPair'].forEach(function(n){var o=window[n]; if(typeof o!=='function')return; window[n]=function(){var r=o.apply(this,arguments); Promise.resolve().then(function(){setTimeout(all,0)}); return r}});
 window.addEventListener('resize',function(){[].forEach.call(document.querySelectorAll('.nb'),fit)});
 var refit=function(){[].forEach.call(document.querySelectorAll('.nb'),fit)};
 if(document.fonts){ if(document.fonts.ready)document.fonts.ready.then(refit); if(document.fonts.load)document.fonts.load('700 1em Caveat').then(refit,function(){}); if(document.fonts.addEventListener)document.fonts.addEventListener('loadingdone',refit) }
})();
"""
head='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&display=swap">'
out=src.replace('</style>',css+'\n</style>',1)
out=out.replace('</head>',head+'</head>',1) if '</head>' in out else head+out
out=out.replace('</body>','<script>'+js+'</script></body>',1)
out=out.replace('<title>Primer Motion Test</title>','<title>Primer Notebook Card</title>')
open(S+'primer-notebook.html','w').write(out); print(len(out)//1024,'KB')
