# Stage 2 of the build: primer-notebook.html -> primer-motion-v2.html (motion cues, stamp, sounds). Run build_nb.py first, or build.sh for both.
import os
S=os.path.dirname(os.path.abspath(__file__))+'/'
src=open(S+'primer-notebook.html').read()
# 1. done only when the key control is used
a="if (k === 'rate' && !target.closest('.rating-btn, .pair-rating-btn')) return null;"
assert a in src
src=src.replace(a,a+" if (k === 'ex' && !target.closest('.sentence-audio, .pair-s-audio')) return null; if ((k === 'syl' || k === 'snd') && !target.closest('.syl-all, .ph-all')) return null; if (k === 'say' && !target.closest('.trio-btn.record')) return null;",1)
CSS2=r'''
/* Say it, playground design: round Hear, a Record circle that opens into a waveform bar, a You pill underneath */
.trio-row{column-gap:12px;row-gap:12px;align-items:center}
.trio-row .trio-btn.model{width:48px;height:48px;min-width:0;min-height:0;padding:0;border-radius:50%;background:var(--sky);border:2px solid var(--sky);color:var(--on-sky);justify-self:end;transition:transform .2s var(--ease)}
.trio-row .trio-btn.model.playing{background:var(--sky);box-shadow:0 0 0 4px color-mix(in srgb,var(--sky) 28%,transparent)}
.trio-row .trio-btn.model .trio-label,.trio-row .trio-btn.record .trio-label{display:none}
.trio-row .trio-btn.record{width:56px;height:56px;min-width:0;min-height:0;padding:2px;border-radius:28px;background:var(--surface);border:2px solid var(--line);color:#fff;display:flex;flex-direction:row;align-items:center;justify-content:flex-start;gap:0;overflow:hidden;position:relative;justify-self:start;transition:width .5s cubic-bezier(.34,1.3,.5,1),border-color .3s}
.trio-row .trio-btn.record .trio-icon{width:48px;height:48px;flex:none;border-radius:50%;background:var(--danger);color:#fff;transition:background .3s}
.trio-row .trio-btn.record.recording{width:184px;background:var(--surface);border-color:var(--danger);animation:none}
.trio-btn.record .mo-wave{flex:1;display:flex;gap:3px;align-items:center;height:100%;padding-inline:10px 12px;opacity:0;transition:opacity .3s .15s}
.trio-btn.record.recording .mo-wave{opacity:1}
.mo-wave b{flex:1;max-width:5px;height:60%;background:var(--danger);border-radius:3px;animation:eqb .5s ease-in-out infinite alternate}
.mo-wave b:nth-child(3n){animation-delay:.12s}.mo-wave b:nth-child(3n+1){animation-delay:.24s}.mo-wave b:nth-child(5n){animation-delay:.06s}
.trio-btn.record .mo-tick{position:absolute;left:2px;top:2px;width:48px;height:48px;padding:13px;fill:none;stroke:var(--on-sky);stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round;opacity:0;pointer-events:none}
.trio-btn.record.rec-ok{border-color:var(--sky)}
.trio-btn.record.rec-ok .trio-icon{background:var(--sky)}
.trio-btn.record.rec-ok .trio-icon::before{opacity:0}
.trio-btn.record.rec-ok .mo-tick{opacity:1}
.trio-btn.record.rec-ok .mo-tick path{stroke-dasharray:22;animation:mo-draw .4s .05s both cubic-bezier(.2,.8,.2,1)}
@keyframes mo-draw{from{stroke-dashoffset:22}to{stroke-dashoffset:0}}
.trio-row .trio-btn.playback{height:44px;min-height:0;flex-direction:row;gap:10px;padding-inline:12px 16px;border-radius:22px;background:var(--surface);border:2px solid var(--line);justify-self:center}
.trio-row .trio-btn.playback .trio-icon{color:var(--sky);--icon:20px}
.trio-row .trio-btn.playback .trio-label{font-size:13px;font-weight:700;letter-spacing:0;text-transform:none;color:var(--fg-dim)}
.trio-row .trio-btn.playback.ready{border-color:var(--sky);opacity:1}
.trio-row .trio-btn.playback.ready .trio-label{color:var(--fg)}

html[data-wicons] .pair-word-audio,html[data-wicons] .pair-s-audio{background:var(--sky)!important;background-image:none!important;border:2px solid var(--sky)!important;color:var(--on-sky)!important;animation:none!important;transition:transform .2s var(--ease)}
html[data-wicons] .pair-word-audio:active,html[data-wicons] .pair-s-audio:active{transform:scale(.86)}
html[data-wicons] .pair-word-audio.playing .eqb,html[data-wicons] .pair-s-audio.playing .eqb{display:flex}
html[data-wicons] .pair-word-audio.playing::before,html[data-wicons] .pair-s-audio.playing::before{display:none}
.mo-calm .pair-word-audio .eqb b,.mo-calm .pair-s-audio .eqb b{animation:none!important}
/* narrow columns (phone split, pair cards, monitor side column): the record button stays a circle and rings instead of stretching */
.trio-wrap{container-type:inline-size}
.trio-btn.record.recording{--ringc:var(--danger)}
@container (max-width: 270px){
 .trio-row .trio-btn.record.recording{width:56px;animation:mo-recring 1.2s ease-out infinite}
 .trio-btn.record .mo-wave{display:none}
 .trio-row .trio-btn.record.recording .trio-icon{background:var(--danger)}
}
@keyframes mo-recring{0%{box-shadow:0 0 0 0 color-mix(in srgb,var(--danger) 90%,transparent)}100%{box-shadow:0 0 0 16px color-mix(in srgb,var(--danger) 0%,transparent)}}
.sketch-paper:has(.nb){container-type:inline-size}
/* more-below: double arrows that keep bobbing while there is more to scroll to (replaces the single chevron) */
.more-btn{width:48px!important;height:48px!important;animation:mo-bob 1.1s ease-in-out infinite!important}
.more-btn::before{width:26px!important;height:26px!important}
.more-btn{background:var(--gold,#F2B33D)!important;background-image:none!important;border:0!important;color:#3A2A00!important;box-shadow:0 4px 12px rgba(0,0,0,.25)}
.more-btn::before{-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 5.5l6 6 6-6M6 12.5l6 6 6-6'/%3E%3C/svg%3E") center/contain no-repeat!important;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23000' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 5.5l6 6 6-6M6 12.5l6 6 6-6'/%3E%3C/svg%3E") center/contain no-repeat!important}
@keyframes mo-bob{0%,100%{transform:translateY(0)}50%{transform:translateY(6px)}}
.mo-calm .more-btn,html.mo-calm .more-btn{animation:none!important}
@media (prefers-reduced-motion:reduce){.more-btn{animation:none!important}}
.more-btn:not(.mo-on){display:none!important}
.section .trio-wrap.trio-wrap{gap:12px}
.trio-wrap .past{padding-top:0}
.trio-wrap .past>summary{min-height:40px}
html[data-wicons] .mo-cue:not(.mo-used){animation:mo-ring 1.9s ease-out infinite!important}
.mo-calm .mo-cue,html.mo-calm [data-next]{animation:none!important}
/* play-all buttons match the other round buttons: solid sky */
.syl-all,.ph-all{width:48px!important;height:48px!important;background:var(--sky)!important;border-color:var(--sky)!important;color:var(--on-sky)!important}
/* the smileys are round buttons like Say it, not boxes */
.rating-row,.pair-rating{justify-content:center;gap:16px}
.rating-btn,.pair-rating-btn{flex:none!important;width:56px;height:56px;min-height:0!important;padding:0!important;border-radius:50%!important;background:var(--surface)}
.rating-btn:not(.got-it):not(.practicing),.pair-rating-btn:not(.got-it):not(.practicing){border-color:var(--line)}

/* sound tiles: one look everywhere, the playground chip but smaller. White, bold, fills sky when pressed */
html .ph-tile,html .pair-ph,html .syl-tile{position:relative;overflow:hidden;min-width:48px;min-height:44px!important;height:44px;padding:0 12px!important;border-radius:14px!important;border:2px solid var(--line)!important;font-weight:800!important;font-size:clamp(17px,var(--ph-fs,20px),22px)!important;color:var(--fg)!important;
 background:linear-gradient(var(--sky),var(--sky)) no-repeat left center/0% 100%,var(--surface)!important;transition:background-size .28s var(--ease,ease),color .2s,border-color .2s,transform .2s cubic-bezier(.34,1.56,.64,1)!important}
html .syl-tile.stress{border-color:var(--sky)!important}
html .ph-tile .ph-sub{display:none}
html .ph-tile.tapped,html .pair-ph.pair-ph-tapped{background:linear-gradient(var(--sky),var(--sky)) no-repeat left center/0% 100%,var(--surface)!important;color:var(--fg)!important;transform:none}
html .ph-tile:active,html .pair-ph:active,html .syl-tile:active,html .ph-tile.mo-lit,html .pair-ph.mo-lit,html .syl-tile.mo-lit,html .syl-tile.syl-on{background-size:100% 100%!important;color:var(--on-sky)!important;border-color:var(--sky)!important}
html .ph-tile:active,html .pair-ph:active,html .syl-tile:active{transform:scale(.92)!important}
html .mo-lit{animation:mo-chip .45s cubic-bezier(.34,1.6,.5,1)}
@keyframes mo-chip{0%{transform:scale(.9)}60%{transform:scale(1.07)}100%{transform:scale(1)}}
html.mo-calm .mo-lit{animation:none}
.phoneme-tiles,.pair-phonemes,.syl-tiles{gap:8px!important}
/* drawing card: tick badge once done */
.sketch-paper.done:has(.nb)::after{content:'';position:absolute;right:10px;top:10px;width:36px;height:36px;border-radius:50%;z-index:5;background:var(--sky);box-shadow:0 2px 8px rgba(0,0,0,.2);
 -webkit-mask:none;mask:none}
.sketch-paper.done:has(.nb)::before{content:'';position:absolute;right:10px;top:10px;width:36px;height:36px;z-index:6;background:var(--on-sky);-webkit-mask:var(--ic-check) center/22px no-repeat;mask:var(--ic-check) center/22px no-repeat;animation:mo-chip .45s cubic-bezier(.34,1.6,.5,1)}
/* phone chooser: before a word is picked, both pictures pulse */
@media (max-width:767px){:root:not([data-pair="split"]) .pair-card-layout:not(.picked) .pair-card-img-wrap{animation:mo-ring 1.9s ease-out infinite;border-radius:var(--r-md,16px)}}
/* round buttons stay round when pressed: no square tap flash */
button,summary,.sketch-paper,[role=button]{-webkit-tap-highlight-color:transparent}
button:focus-visible{outline:3px solid color-mix(in srgb,var(--sky) 70%,transparent);outline-offset:2px}

/* word underline: the gold line draws under the target word when the example sentence is played */
.sentence-hl,.pair-sentence-hl{position:relative;display:inline-block}
.sentence-hl::after,.pair-sentence-hl::after{content:'';position:absolute;left:0;right:0;bottom:-3px;height:4px;border-radius:2px;background:var(--gold,#F2B33D);transform:scaleX(0);transform-origin:left;transition:transform .55s var(--ease,ease)}
.sentence-hl.on::after,.pair-sentence-hl.on::after{transform:scaleX(1)}
html.mo-calm .sentence-hl::after,html.mo-calm .pair-sentence-hl::after{transition:none}
/* status on the picture: New / Learning / Known stamp, and class dots */
.card-img,.pair-card-img{container-type:inline-size}
.mo-stamp{position:absolute;z-index:4;top:10px;left:10px;display:inline-flex;align-items:center;gap:6px;height:28px;padding-inline:9px 11px;border-radius:14px;background:var(--surface);border:2px solid var(--line);color:var(--fg-dim,#5B6B7A);font-size:12px;font-weight:800;letter-spacing:.02em;overflow:hidden;pointer-events:none}
.mo-stamp svg{width:15px;height:15px;fill:transparent;stroke:currentColor;stroke-width:2.4;stroke-linejoin:round;transition:fill .4s}
.mo-stamp.s-learn{border-color:var(--sky);color:var(--sky)}
.mo-stamp.s-learn svg{fill:color-mix(in srgb,var(--sky) 45%,transparent)}
.mo-stamp.s-known{background:var(--gold,#F2B33D);border-color:var(--gold,#F2B33D);color:#3A2A00}
.mo-stamp.s-known svg{fill:currentColor}
.mo-stamp::after{content:'';position:absolute;top:0;bottom:0;left:-60%;width:40%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.75),transparent);transform:skewX(-20deg);opacity:0}
.mo-stamp.shine::after{animation:mo-shine 1.1s var(--ease,ease)}
@keyframes mo-shine{0%{left:-60%;opacity:1}100%{left:130%;opacity:1}}
.mo-class{position:absolute;z-index:4;left:50%;width:max-content;bottom:10px;transform:translateX(-50%);display:inline-flex;align-items:center;gap:6px;height:26px;padding-inline:10px;border-radius:13px;background:var(--surface);border:2px solid var(--line);pointer-events:none;white-space:nowrap}
.mo-class svg{flex:none;width:14px;height:14px;fill:var(--gold,#F2B33D)}
.mo-cnt{flex:none;font-size:12px;font-weight:800;color:var(--fg-dim,#5B6B7A);font-variant-numeric:tabular-nums}
@container (max-width:170px){.mo-stamp .mo-lb{display:none}.mo-stamp{padding-inline:8px}}
/* past recordings: in a narrow column drop the date so the play button never leaves the box */
.past-list{container-type:inline-size}
@container (max-width:300px){.past-row,.tight .past-row{grid-template-columns:var(--icon) minmax(0,1fr) var(--ring-lg);grid-template-areas:"n w p";gap:var(--sp-sm)}.past-d{display:none}.past-n{grid-area:n}.past-w{grid-area:w}.past-p{grid-area:p}}
/* celebration on the smileys */
.mo-spark{position:fixed;width:10px;height:10px;border-radius:50%;pointer-events:none;z-index:9999}
.mo-ringfx{position:fixed;border-radius:50%;border:3px solid var(--amber);pointer-events:none;z-index:9999}
'''
css=r"""
/* ===== Motion sections layer: tick icons, pulse guidance, wobble, Say it layout ===== */
@keyframes mo-ring{0%{box-shadow:0 0 0 0 color-mix(in srgb,var(--amber,#E39B00) 95%,transparent)}60%{box-shadow:0 0 0 9px color-mix(in srgb,var(--amber,#E39B00) 55%,transparent)}100%{box-shadow:0 0 0 17px color-mix(in srgb,var(--amber,#E39B00) 0%,transparent)}}
.section[data-next]:not([open]){animation:next-glow var(--dur-pulse) ease-in-out 4 alternate,mo-ring 1.9s ease-out infinite}
.mo-cue:not(.mo-used){animation:mo-ring 1.9s ease-out infinite}
.section.done .mo-cue{animation:none}
.trio-hint{display:none}
/* done: the section icon becomes a sky rounded square with a drawn tick */
.section.done > summary.slabel::before{display:none}
.section.done > summary.slabel::after{margin-left:auto}
.section.done > summary .sec-ic{position:relative;-webkit-mask:none;mask:none;background:var(--sky);border-radius:9px;width:calc(var(--icon)*1.3);height:calc(var(--icon)*1.3);margin-right:var(--sp-xs);transition:border-radius .4s}
.section.done > summary .sec-ic::after{content:'';position:absolute;inset:20%;background:var(--on-sky);-webkit-mask:var(--ic-check) center/contain no-repeat;mask:var(--ic-check) center/contain no-repeat;animation:mo-tick .45s .1s both cubic-bezier(.2,.8,.2,1)}
@keyframes mo-tick{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
/* Say it: listen and record side by side, You underneath */
.trio-row{display:grid;grid-template-columns:repeat(2,auto);justify-content:center;justify-items:center;gap:var(--sp-sm)}
.trio-btn.model{grid-column:1;grid-row:1}.trio-btn.record{grid-column:2;grid-row:1}.trio-btn.playback{grid-column:1/-1;grid-row:2}
/* Sounds: a play button like Syllables */
.ph-ctl{display:flex;justify-content:center}
/* playground icon style for the audio and translate buttons */
html[data-wicons]{--ic-speaker:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M3%209v6h4l5%205V4L7%209H3zm13.5%203A4.5%204.5%200%200%200%2014%208v8a4.5%204.5%200%200%200%202.5-4z'/%3E%3C/svg%3E")}
html[data-wicons] .act-row{--ring:48px;--icon:24px}
html[data-wicons] .word-audio,html[data-wicons] .sentence-audio{background:var(--sky)!important;background-image:none!important;border:2px solid var(--sky)!important;color:var(--on-sky)!important;animation:none!important;transition:transform .2s var(--ease)}
html[data-wicons] .word-audio:active,html[data-wicons] .sentence-audio:active,html[data-wicons] .act-row .tr-globe:active{transform:scale(.86)}
html[data-wicons] .act-row .tr-globe{background:var(--surface-2)!important;border:2px solid var(--line)!important;color:var(--sky)!important;transition:transform .2s var(--ease)}
html[data-wicons] .act-row .tr-globe[data-ic]{font-size:0}
html[data-wicons] .act-row .tr-globe[data-ic]::before{background:none!important;-webkit-mask:none!important;mask:none!important;content:'A\A\6587';width:auto;height:auto;font-size:13px;font-weight:800;line-height:1.1;white-space:pre;text-align:center;display:block}
.eqb{display:none;gap:3px;align-items:center;height:18px}
.eqb b{width:4px;height:100%;background:currentColor;border-radius:2px;animation:eqb .6s ease-in-out infinite alternate}
.eqb b:nth-child(2){animation-delay:.15s}.eqb b:nth-child(3){animation-delay:.3s}.eqb b:nth-child(4){animation-delay:.1s}
@keyframes eqb{from{transform:scaleY(.25)}to{transform:scaleY(1)}}
html[data-wicons] .word-audio.playing .eqb,html[data-wicons] .sentence-audio.playing .eqb{display:flex}
html[data-wicons] .word-audio.playing::before,html[data-wicons] .sentence-audio.playing::before{display:none}
.mo-calm .mo-cue,.mo-calm .eqb b,html.mo-calm .section[data-next]{animation:none!important}
"""
js=r"""
(function(){
 var root=document.documentElement; root.setAttribute('data-wicons','');
 var $$=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
 // shared bus: one calm check, one 300ms tick (only while a card is open and the page is visible), one batched DOM watcher
 var MO=window.MO={ tasks:[], dom:[],
  calm:function(){return !!((window.PrimerMotion&&PrimerMotion.cfg&&PrimerMotion.cfg.calm)||document.documentElement.classList.contains('mo-calm')||(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches))},
  every:function(f){MO.tasks.push(f)}, onDom:function(f){MO.dom.push(f); f()} };
 setInterval(function(){ if(document.hidden||!document.querySelector('#screen-single.active,#screen-pair.active'))return; MO.tasks.forEach(function(f){try{f()}catch(x){}}) },300);
 var domQ=0; new MutationObserver(function(){ if(domQ)return; domQ=requestAnimationFrame(function(){domQ=0; MO.dom.forEach(function(f){f()})}) }).observe(document.body,{subtree:true,childList:true});
 var reduced=MO.calm;
 var WOB=[{transform:'scale(1)'},{transform:'scale(.88,1.1)'},{transform:'scale(1.1,.92)'},{transform:'scale(.97,1.03)'},{transform:'scale(1)'}];
 var WSEL='.word-audio,.sentence-audio,.tr-globe,.trio-btn,.syl-tile,.ph-tile,.pair-ph,.syl-all,.ph-all,.rating-btn,.pair-rating-btn,.pair-word-audio,.pair-s-audio,.compare-play';
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest(WSEL); if(!b||reduced())return; b.animate(WOB,{duration:450})},true);
 // equaliser bars while a word or sentence plays
 function eq(){ $$('.word-audio,.sentence-audio,.pair-word-audio,.pair-s-audio').forEach(function(b){ if(!b.querySelector('.eqb')) b.insertAdjacentHTML('beforeend','<span class="eqb" aria-hidden="true"><b></b><b></b><b></b><b></b></span>') }) }
 ['playWordAudio','playSentenceAudio'].forEach(function(n,i){var o=window[n]; if(typeof o!=='function')return; window[n]=function(){var r=o.apply(this,arguments); var b=document.getElementById(i?'sc-sentence-audio':'sc-word-audio'); if(b){b.classList.add('playing'); clearTimeout(b._t); b._t=setTimeout(function(){b.classList.remove('playing')},1100)} return r}});
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.pair-word-audio,.pair-s-audio'); if(!b)return; b.classList.add('playing'); clearTimeout(b._t); b._t=setTimeout(function(){b.classList.remove('playing')},1100)},true);
 // Sounds: a play button that lights each sound in turn
 function phCtl(){ $$('.phoneme-tiles,.pair-phonemes').forEach(function(c){ if(c.nextElementSibling&&c.nextElementSibling.classList.contains('ph-ctl'))return; c.insertAdjacentHTML('afterend','<div class="syl-controls ph-ctl"><button class="syl-all ph-all" data-ic="play" type="button" aria-label="Play every sound in order">&#9654;</button></div>') }) }
 var phTok=0;
 document.addEventListener('click',function(e){
  var b=e.target.closest&&e.target.closest('.ph-all'); if(!b)return;
  if(b.classList.contains('playing')){ phTok++; b.classList.remove('playing'); b.dataset.ic='play'; try{_phQueue.length=0; if(_phAudio){_phAudio.pause()} _phPlaying=false; _phAudio=null}catch(x){} document.querySelectorAll('.mo-lit').forEach(function(t){t.classList.remove('mo-lit')}); e.stopImmediatePropagation(); return }
  var tiles=$$('.ph-tile,.pair-ph',b.closest('.sounds-wrap')||b.parentNode.parentNode), t=++phTok;
  tiles.forEach(function(x){x.classList.remove('tapped','pair-ph-tapped')}); b.classList.add('playing'); b.dataset.ic='pause';
  tiles.forEach(function(x,i){setTimeout(function(){ if(t!==phTok)return; x.classList.remove('tapped','pair-ph-tapped'); x.click(); if(i===tiles.length-1)setTimeout(function(){if(t===phTok){b.classList.remove('playing'); b.dataset.ic='play'}},600) },i*750)});
 },true);
 // pulse guidance: open and not done -> pulse the key control until it is pressed
 function seq(d){
  var m=d.querySelector('.trio-btn.model'), r=d.querySelector('.trio-btn.record'), p=d.querySelector('.trio-btn.playback.ready');
  var list=[m,r,p]; for(var i=0;i<3;i++){ if(list[i]&&!list[i].classList.contains('mo-used'))return list[i]; if(!list[i])return null } return null;
 }
 function keys(d){
  if(d.classList.contains('say')){var s=seq(d); return s?[s]:[]}
  if(d.classList.contains('ex'))return $$('.sentence-audio,.pair-s-audio',d).slice(0,1);
  if(d.classList.contains('syl'))return $$('.syl-all',d).slice(0,1);
  if(d.classList.contains('snd'))return $$('.ph-all',d).slice(0,1);
  if(d.classList.contains('sk'))return $$('.sketch-paper',d).slice(0,1);
  if(d.classList.contains('rate'))return $$('.rating-btn,.pair-rating-btn',d);
  return [];
 }
 function sync(){
  $$('details.section').forEach(function(d){
   var on=d.open&&!d.hidden&&!d.classList.contains('done'), want=on?keys(d):[];
   $$('.mo-cue',d).forEach(function(x){ if(want.indexOf(x)<0)x.classList.remove('mo-cue') });
   if(!on){d.__ready=0;return}
   if(!d.__ready){d.__ready=Date.now()}
   if(Date.now()-d.__ready<600)return;
   want.forEach(function(x){ if(!x.classList.contains('mo-used'))x.classList.add('mo-cue') });
  });
 }
 function stepCues(){
  var wait=Date.now()-(window.__moT||0)>1500;
  $$('.screen.active [data-next]').forEach(function(x){ if(x.tagName==='DETAILS'||!x.matches('.word-audio,.pair-word-audio'))return; if(wait&&!x.classList.contains('mo-used'))x.classList.add('mo-cue') });
  if(wait)$$('.screen.active').forEach(function(sc){ var hs=$$('.pair-card-half',sc); if(!hs.length)hs=[sc]; hs.forEach(function(h){ var a=$$('.word-audio,.pair-word-audio',h)[0]; if(!a)return; if(!a.classList.contains('mo-used'))a.classList.add('mo-cue'); else { var f=$$('.flip-show',h)[0]; if(f&&!f.classList.contains('mo-used'))f.classList.add('mo-cue') } }) });
  $$('.mo-cue').forEach(function(x){ if(!x.closest('details.section')&&!x.hasAttribute('data-next')&&!x.matches('.word-audio,.pair-word-audio,.flip-show'))x.classList.remove('mo-cue') });
 }
 MO.every(function(){sync();stepCues()});
 document.addEventListener('click',function(e){
  var x=e.target.closest&&e.target.closest('.mo-cue,.word-audio,.pair-word-audio,.flip-show,.trio-btn,.sentence-audio,.syl-all,.ph-all,.rating-btn,.pair-rating-btn,.sketch-paper'); if(!x)return;
  x.classList.add('mo-used'); x.classList.remove('mo-cue');
  if(x.classList.contains('rating-btn')||x.classList.contains('pair-rating-btn'))$$('.rating-btn,.pair-rating-btn',x.closest('details')).forEach(function(y){y.classList.add('mo-used');y.classList.remove('mo-cue')});
 },true);
 var ft=0; function freshSoon(){ clearTimeout(ft); ft=setTimeout(fresh,30) }
 function fresh(){ window.__moT=Date.now(); if(window.__sxlGuided)window.__sxlGuided.reset(); window.__moScrolled=0; $$('#screen-single,.pair-card-half').forEach(function(h){h.__aud=0;h.__pic=0}); $$('.sentence-hl.on,.pair-sentence-hl.on').forEach(function(h){h.classList.remove('on')}); $$('.mo-used').forEach(function(x){x.classList.remove('mo-used')}); $$('.mo-cue').forEach(function(x){x.classList.remove('mo-cue')}); $$('details.section,summary').forEach(function(d){d.__ready=0; d.__nudged=0; d.__auto=0}); eq(); phCtl(); window.dispatchEvent(new Event('mo-fresh')) }
 ['renderSingle','renderPair'].forEach(function(n){var o=window[n]; if(typeof o!=='function')return; window[n]=function(){var r=o.apply(this,arguments); freshSoon(); return r}});
 MO.onDom(function(){eq();phCtl()});
 $$('.screen').forEach(function(sc){ if(!/single|pair/.test(sc.id))return; new MutationObserver(function(){ var on=sc.classList.contains('active'); if(on&&!sc.__on)freshSoon(); sc.__on=on }).observe(sc,{attributes:true,attributeFilter:['class']}) });
 document.addEventListener('visibilitychange',function(){ if(!document.hidden&&document.querySelector('#screen-single.active,#screen-pair.active'))freshSoon() });
 eq(); phCtl();
})();
"""

css+=CSS2
JS2=r'''
(function(){
 // tiles light up solid sky on press, the same for single words, pairs and syllables
 document.addEventListener('click',function(e){ var t=e.target.closest&&e.target.closest('.ph-tile,.pair-ph,.syl-tile'); if(!t)return;
  t.classList.remove('mo-lit'); void t.offsetWidth; t.classList.add('mo-lit'); clearTimeout(t._lt); t._lt=setTimeout(function(){t.classList.remove('mo-lit')},900) },true);
 // tapping a playing audio button stops it
 var media=[], lastBtn=null, AB='.word-audio,.sentence-audio,.pair-word-audio,.pair-s-audio,.trio-btn.model,.compare-play';
 var op=HTMLMediaElement.prototype.play;
 HTMLMediaElement.prototype.play=function(){ if(media.indexOf(this)<0)media.push(this); var b=lastBtn, el=this; var r=op.apply(this,arguments);
  if(b&&Date.now()-b.__t<1500&&!b.__live){ b.__live=el; b.classList.add('playing'); var off=function(){ if(b.__live===el){b.__live=null;b.classList.remove('playing')} el.removeEventListener('ended',off); el.removeEventListener('pause',off) }; el.addEventListener('ended',off); el.addEventListener('pause',off) }
  return r };
 document.addEventListener('click',function(e){ var b=e.target.closest&&e.target.closest(AB); if(!b)return;
  if(b.__live){ e.stopImmediatePropagation(); e.preventDefault(); media.forEach(function(m){try{m.pause()}catch(x){}}); try{speechSynthesis.cancel()}catch(x){} b.__live=null; b.classList.remove('playing'); return }
  lastBtn=b; b.__t=Date.now() },true);
 // opening a section scrolls so the whole section can be seen (its top stays in view if it is taller than the screen)
 function scroller(el){ for(var p=el.parentElement;p&&p!==document.body;p=p.parentElement){ var o=getComputedStyle(p).overflowY; if((o==='auto'||o==='scroll')&&p.scrollHeight>p.clientHeight+2)return p } return null }
 function settle(sec,cb){ var last=-1,n=0,t0=Date.now(),iv=setInterval(function(){ var h=sec.offsetHeight; n=(h===last)?n+1:0; last=h; if((n>=3&&Date.now()-t0>250)||Date.now()-t0>1500){ clearInterval(iv); if(sec.open)cb() } },100) }
 function show(sec){ window.__moScrolled=Date.now(); var c=scroller(sec); if(!c)return; var cr=c.getBoundingClientRect(), r=sec.getBoundingClientRect();
  var peek=0, scope=sec.closest('.pair-card-half')||sec.closest('.screen')||document, lst=[].slice.call(scope.querySelectorAll('details.section')).filter(function(d){return !d.hidden&&d.offsetParent}), ix=lst.indexOf(sec), n1=lst[ix+1], n2=lst[ix+2]; if(n1){ var lastS=(n2||n1).querySelector('summary'); peek=lastS.getBoundingClientRect().bottom-r.bottom+16 } var over=r.bottom-(cr.bottom-12-peek), room=r.top-(cr.top+8); var sh=(sec.querySelector('summary')||sec).getBoundingClientRect().height; var d=Math.min(over,Math.max(room,0)+sh+6); if(d>4){ var calm=(window.PrimerMotion&&PrimerMotion.cfg&&PrimerMotion.cfg.calm)||(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches); c.scrollBy({top:d,behavior:calm?'auto':'smooth'}) } }

 // celebration: sparks burst from the smiley, and from a section when it ticks
 var calmNow=MO.calm;
 function burst(el,n,dist){ if(calmNow()||!el)return; var r=el.getBoundingClientRect(), cx=r.left+r.width/2, cy=r.top+r.height/2, cols=['#F2B33D','#0B8BC7','#2FB67C','#E85D9A','#FFD76A'];
  for(var i=0;i<n;i++){ var d=document.createElement('i'); d.className='mo-spark'; d.style.left=(cx-5)+'px'; d.style.top=(cy-5)+'px'; d.style.background=cols[i%cols.length]; document.body.appendChild(d);
   var a=(i/n)*Math.PI*2+Math.random()*.4, k=dist*(.7+Math.random()*.6);
   var an=d.animate([{transform:'translate(0,0) scale(1)',opacity:1},{transform:'translate('+Math.cos(a)*k+'px,'+Math.sin(a)*k+'px) scale(.2)',opacity:0}],{duration:650+Math.random()*250,easing:'cubic-bezier(.2,.7,.3,1)'}); an.onfinish=(function(x){return function(){x.remove()}})(d) } }
 function spin(b){ if(calmNow())return; b.animate([{transform:'scale(.8) rotate(0)'},{transform:'scale(1) rotate(360deg)'}],{duration:700,easing:'cubic-bezier(.34,1.3,.5,1)'}) }
 function tilt(b,big){ if(calmNow())return; b.animate(big?[{transform:'scale(1) rotate(0)'},{transform:'scale(1.3) rotate(-14deg)',offset:.3},{transform:'scale(1.15) rotate(10deg)',offset:.6},{transform:'scale(1) rotate(0)'}]:[{transform:'rotate(0)'},{transform:'rotate(-14deg)',offset:.25},{transform:'rotate(12deg)',offset:.55},{transform:'rotate(-6deg)',offset:.8},{transform:'rotate(0)'}],{duration:big?560:520,easing:'cubic-bezier(.34,1.56,.64,1)'}) }
 document.addEventListener('click',function(e){ var b=e.target.closest&&e.target.closest('.rating-btn,.pair-rating-btn'); if(!b)return;
  var got=b.classList.contains('got-it')||b.id==='sc-got-it'||b.dataset.rate==='got-it'; if(got){burst(b,18,70); tilt(b,true)} else spin(b) },true);
 new MutationObserver(function(ms){ ms.forEach(function(m){ var d=m.target; if(!d.matches||!d.matches('details.section')||!d.classList.contains('done')||(m.oldValue||'').split(' ').indexOf('done')>=0)return; var ic=d.querySelector('summary .sec-ic')||d.querySelector('summary'); setTimeout(function(){burst(ic,9,34)},120) }) }).observe(document.body,{subtree:true,attributes:true,attributeFilter:['class'],attributeOldValue:true});

 // never leave a section title half cut off at the bottom: nudge just enough to show the whole title row
 var lastUser=0; ['wheel','touchstart','pointerdown','keydown'].forEach(function(ev){document.addEventListener(ev,function(){lastUser=Date.now()},{capture:true,passive:true})});
 function reveal(){ if(window.__moScrolled||lastUser>(window.__moT||0)||Date.now()-lastUser<1500||Date.now()-(window.__moT||0)<3900)return;
  var scr=document.querySelector('.screen.active'); if(!scr||!started(scr))return;
  var secs=[].slice.call(scr.querySelectorAll('details.section')).filter(function(d){return !d.hidden&&d.offsetParent});
  for(var i=0;i<secs.length;i++){ var d=secs[i]; if(d.__nudged)continue; var sm=d.querySelector('summary'); if(!sm)continue; var c=scroller(d); if(!c)continue;
   var cr=c.getBoundingClientRect(), r=sm.getBoundingClientRect(); if(r.height<8)continue;
   if(r.top<cr.bottom-4&&r.bottom>cr.bottom-10){ d.__nudged=1; var calm=calmNow(); c.scrollBy({top:Math.ceil(r.bottom-(cr.bottom-14)),behavior:calm?'auto':'smooth'}); return }
   if(r.top>=cr.bottom-4)break } }
 MO.every(reveal);

 // Say it: waveform and tick live inside the record button
 var TICK='<svg class="mo-tick" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
 function decor(){ [].forEach.call(document.querySelectorAll('.trio-btn.record'),function(b){ if(b.querySelector('.mo-wave'))return; var w='<span class="mo-wave" aria-hidden="true">'; for(var i=0;i<16;i++)w+='<b></b>'; b.insertAdjacentHTML('beforeend',w+'</span>'+TICK) }) }
 MO.onDom(decor);
 new MutationObserver(function(ms){ ms.forEach(function(m){ var b=m.target; if(!b.matches||!b.matches('.trio-btn.record'))return; var was=(m.oldValue||'').split(' ').indexOf('recording')>=0, now=b.classList.contains('recording');
  if(now&&!was){ b.__rs=Date.now(); b.classList.remove('rec-ok') }
  if(!now&&was&&Date.now()-(b.__rs||0)>600){ b.classList.add('rec-ok'); setTimeout(function(){b.classList.remove('rec-ok')},2600) } }) }).observe(document.body,{subtree:true,attributes:true,attributeFilter:['class'],attributeOldValue:true});
 // layer 2 and 3: the bobbing arrow, and a gentle scroll when the arrow has been ignored
 function below(el){ var c=scroller(el); if(!c)return false; return el.getBoundingClientRect().top>=c.getBoundingClientRect().bottom-4 }
 var since=new WeakMap();
 function vis(scr){ return [].slice.call(scr.querySelectorAll('details.section')).filter(function(d){return !d.hidden&&d.offsetParent}) }
 function arrows(){ [].forEach.call(document.querySelectorAll('.more-btn'),function(b){ var scr=b.closest('.screen'); if(!scr||!scr.classList.contains('active')){ if(b.classList.contains('mo-on'))b.classList.remove('mo-on'); return }
  var t=vis(scr).filter(function(d){return !d.classList.contains('done')}).map(function(d){return d.querySelector('summary')}).concat([].slice.call(scr.querySelectorAll('.mo-cue')).filter(function(x){return x.offsetParent}));
  var out=t.filter(below); var now=Date.now();
  if(!out.length){ since.delete(b); if(b.classList.contains('mo-on'))b.classList.remove('mo-on'); return }
  if(!since.has(b))since.set(b,now); if(now-since.get(b)>900)b.classList.add('mo-on');
  var nx=out.filter(function(x){return x.parentNode&&x.parentNode.matches&&x.parentNode.matches('details.section[data-next]')})[0];
  if(nx&&!nx.__auto&&started(scr)&&now-since.get(b)>2600&&now-lastUser>2000&&now-(window.__moScrolled||0)>3500){ nx.__auto=1; var c=scroller(nx); if(c){ var all=vis(scr), i=all.indexOf(nx.parentNode), last=all[Math.min(i+1,all.length-1)].querySelector('summary'), cr=c.getBoundingClientRect(), r=last.getBoundingClientRect(); c.scrollBy({top:Math.ceil(r.bottom-(cr.bottom-16)),behavior:calmNow()?'auto':'smooth'}) } } }) }
 MO.every(arrows);

 // the word underline draws when the example sentence is played
 document.addEventListener('click',function(e){ var b=e.target.closest&&e.target.closest('.sentence-audio,.pair-s-audio'); if(!b||b.__live)return; var sc=b.closest('.pair-card-half')||document.getElementById('screen-single'); if(!sc)return; [].forEach.call(sc.querySelectorAll('.sentence-hl,.pair-sentence-hl'),function(h){h.classList.add('on')}) },true);
 // what the learner has done at the start: audio and flip pressed this visit
 document.addEventListener('click',function(e){ var t=e.target; if(!t.closest)return; var sc=t.closest('.pair-card-half')||t.closest('#screen-single'); if(!sc)return;
  if(t.closest('.word-audio,.pair-word-audio'))sc.__aud=1; if(t.closest('.flip-show,.flip-face.front'))sc.__pic=1 },true);
 function started(scr){ var hs=[].slice.call(scr.querySelectorAll('.pair-card-half')); if(!hs.length)hs=[scr];
  return hs.some(function(h){ return h.__aud&&(!h.querySelector('.flip-slot:not([hidden]) .flip-show')||h.__pic) }) }
 // stamp and class dots
 var STAR='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 17.3l-5.4 3.2 1.4-6.1-4.7-4.1 6.2-.5L12 4l2.5 5.8 6.2.5-4.7 4.1 1.4 6.1z"/></svg>';
 var LAB={new:'New',learn:'Learning',known:'Known'}, KN={};
 try{ (JSON.parse(localStorage.getItem('sxl.known')||'[]')).forEach(function(w){KN[w]=1}) }catch(e){}
 var LN={}; try{ (JSON.parse(localStorage.getItem('sxl.learn')||'[]')).forEach(function(w){LN[w]=1}) }catch(e){}
 function saveLN(){ try{ localStorage.setItem('sxl.learn',JSON.stringify(Object.keys(LN))) }catch(e){} }
 function saveKN(){ try{ localStorage.setItem('sxl.known',JSON.stringify(Object.keys(KN))) }catch(e){} }
 function wordOfScope(sc){ var w=sc.querySelector('#sc-word,.pair-word-text'); return w?w.textContent.replace('*','').trim():'' }
 function total(){ try{ return singleCards.length||26 }catch(e){ return 26 } }
 function status(){ [].forEach.call(document.querySelectorAll('#screen-single,.pair-card-half'),function(sc){ if(!sc.offsetParent)return;
  var img=sc.querySelector('.card-img,.pair-card-img'); if(!img)return; var w=wordOfScope(sc); if(!w)return;
  var st=img.querySelector('.mo-stamp');
  if(!st){ img.insertAdjacentHTML('beforeend','<div class="mo-stamp s-new" data-s="new" aria-hidden="true">'+STAR+'<span class="mo-lb">New</span></div><div class="mo-class" role="img" aria-label="Words known">'+STAR+'<span class="mo-cnt"></span></div>'); st=img.querySelector('.mo-stamp') }
  if(img.__w!==w){ img.__w=w; st.dataset.s='' }
  var secs=[].slice.call(sc.querySelectorAll('details.section')).filter(function(d){return !d.hidden&&d.offsetParent}), n=secs.filter(function(d){return d.classList.contains('done')}).length;
  var state=!n?'new':(n<secs.length?'learn':'known'); if(state==='learn'&&!LN[w]){LN[w]=1;saveLN()} if(KN[w])state='known'; else if(state==='new'&&LN[w])state='learn'; var was=st.dataset.s;
  if(was!==state){ st.dataset.s=state; st.className='mo-stamp s-'+state; st.querySelector('.mo-lb').textContent=LAB[state];
   if(was&&!calmNow()){ if(state==='known'){ st.animate([{transform:'scale(2.8) rotate(-16deg)',opacity:0,offset:0,easing:'cubic-bezier(.55,0,1,.65)'},{transform:'scale(1.14,.84) rotate(0deg)',opacity:1,offset:.38,easing:'cubic-bezier(.34,1.56,.64,1)'},{transform:'none',opacity:1,offset:1}],{duration:760,easing:'linear'}); setTimeout(function(){st.classList.add('shine');setTimeout(function(){st.classList.remove('shine')},1200)},300) } else st.animate([{transform:'scale(.7)'},{transform:'none'}],{duration:350,easing:'cubic-bezier(.34,1.56,.64,1)'}) }
   if(state==='known'&&!KN[w]){ KN[w]=1; saveKN(); if(was)setTimeout(function(){ paint(img,true) },450) } }
  paint(img,false) }) }
 function paint(img,pop){ var cl=img.querySelector('.mo-class'); if(!cl)return; var n=Math.min(total(),Object.keys(KN).length), cnt=cl.querySelector('.mo-cnt'), t=n+' / '+total();
  if(cnt.textContent!==t){ var had=cnt.textContent; cnt.textContent=t; if(had&&pop&&!calmNow()){ cl.animate([{transform:'translateX(-50%) scale(1)'},{transform:'translateX(-50%) scale(1.25)',offset:.4},{transform:'translateX(-50%) scale(1)'}],{duration:550,easing:'cubic-bezier(.34,1.56,.64,1)'}); burst(cl.querySelector('svg'),10,34) } } }
 MO.every(status);
 // opening past recordings also scrolls so the next section shows
 document.addEventListener('toggle',function(e){ var d=e.target; if(!d||!d.matches||!d.matches('details.past')||!d.open)return; var sec=d.closest('details.section'); if(!sec)return; settle(d,function(){show(sec)}) },true);
 document.addEventListener('toggle',function(e){ var sec=e.target; if(!sec||!sec.matches||!sec.matches('details.section')||!sec.open)return;
  settle(sec,function(){show(sec)});
 },true);
})();
'''
sfxcss=r"""
.sfx-toggle{position:fixed;left:10px;bottom:76px;z-index:60;width:36px;height:36px;border-radius:50%;border:2px solid var(--line);background:var(--surface);color:var(--sky);display:grid;place-items:center;padding:0;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.12)}
.sfx-toggle svg{width:20px;height:20px;fill:currentColor}
.sfx-toggle .off{display:none}.sfx-toggle[aria-pressed="false"] .on{display:none}.sfx-toggle[aria-pressed="false"] .off{display:block}
.sfx-toggle:focus-visible{outline:2px solid var(--sky);outline-offset:2px}
"""
sfxjs=r"""
(function(){
 var ctx=null, on=true, VOL=.55, log=(window.__sfx=[]);
 try{on=localStorage.getItem('sxl.sfx')!=='off'}catch(e){}
 var calm=function(){return (window.PrimerMotion&&PrimerMotion.cfg&&PrimerMotion.cfg.calm)};
 function ac(){ if(!ctx){var C=window.AudioContext||window.webkitAudioContext; if(!C)return null; try{ctx=new C()}catch(e){return null}} if(ctx.state==='suspended'){try{ctx.resume()}catch(e){}} return ctx }
 function tone(f,d,o){ o=o||{}; var c=ac(); if(!c)return; var t=c.currentTime+(o.at||0), osc=c.createOscillator(), g=c.createGain();
  osc.type=o.type||'sine'; osc.frequency.setValueAtTime(f,t); if(o.to)osc.frequency.exponentialRampToValueAtTime(o.to,t+d);
  g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(Math.max(.0002,(o.g||.2)*VOL),t+.008); g.gain.exponentialRampToValueAtTime(0.0001,t+d);
  osc.connect(g); g.connect(c.destination); osc.start(t); osc.stop(t+d+.03) }
 function noise(d,o){ o=o||{}; var c=ac(); if(!c)return; var n=Math.floor(c.sampleRate*d), buf=c.createBuffer(1,n,c.sampleRate), a=buf.getChannelData(0); for(var i=0;i<n;i++)a[i]=Math.random()*2-1;
  var src=c.createBufferSource(); src.buffer=buf; var f=c.createBiquadFilter(); f.type='bandpass'; f.Q.value=o.q||1.2; var t=c.currentTime; f.frequency.setValueAtTime(o.f||1200,t); if(o.to)f.frequency.exponentialRampToValueAtTime(o.to,t+d);
  var g=c.createGain(); g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(Math.max(.0002,(o.g||.1)*VOL),t+d*.25); g.gain.exponentialRampToValueAtTime(0.0001,t+d);
  src.connect(f); f.connect(g); g.connect(c.destination); src.start(t) }
 var S={
  pop:function(){tone(640,.09,{to:380,g:.2})},
  tick:function(){tone(900,.04,{type:'triangle',g:.07})},
  open:function(){tone(392,.12,{g:.12});tone(523,.15,{at:.07,g:.12})},
  close:function(){tone(523,.1,{g:.09});tone(392,.13,{at:.06,g:.09})},
  done:function(){[523,659,784,1047].forEach(function(f,i){tone(f,.3,{at:i*.07,g:.15})})},
  recOn:function(){tone(440,.1,{g:.16});tone(660,.15,{at:.09,g:.16})},
  recOff:function(){tone(660,.1,{g:.14});tone(440,.15,{at:.09,g:.14})},
  good:function(){[659,880,1175].forEach(function(f,i){tone(f,.26,{at:i*.08,g:.16})})},
  boop:function(){tone(330,.18,{to:260,g:.16})},
  scribble:function(){noise(.9,{f:2400,to:3200,q:2,g:.07})},
  whoosh:function(){noise(.5,{f:450,to:2400,q:.7,g:.2}); tone(300,.28,{to:520,g:.05})},
  arrive:function(){[523.25,587.33,659.25,783.99].forEach(function(f,i){var L=i===3?1.1:.5; tone(f,L,{at:i*.16,g:.2}); tone(f*2,L*.55,{at:i*.16,g:.045})})}
 };
 var lastArr=0;
 function play(n){ if(!on||calm())return; if(n==='arrive'){ if(Date.now()-lastArr<900)return; lastArr=Date.now() } log.push(n); try{S[n]()}catch(e){} }
 window.SXLSound={play:play};
 // wiring
 ['pointerdown','touchend','click','keydown'].forEach(function(e){document.addEventListener(e,function(){ if(on)ac() },true)}); // any tap keeps the audio awake (iPhone needs a tap to switch it on)
 document.addEventListener('click',function(e){
  var t=e.target.closest&&e.target.closest('button,.sketch-paper,.syl-tile,.ph-tile,.pair-ph'); if(!t||t.closest('.sfx-toggle'))return;
  if(t.closest('#screen-index,.arrow-btn,.nav-back'))return; // opening a card plays the jingle only
  if(t.matches('summary,.slabel'))return;
  if(t.matches('.syl-tile,.ph-tile,.pair-ph'))return play('tick');
  if(t.id==='sc-got-it'||t.dataset.rate==='got-it')return play('good');
  if(t.id==='sc-practicing'||t.dataset.rate==='practicing')return play('boop');
  if(t.matches('.trio-btn.record')){t.__r=!t.__r; return play(t.__r?'recOn':'recOff')}
  if(t.matches('.sketch-paper'))return;
  play('pop');
 },true);
 document.addEventListener('toggle',function(e){var d=e.target; if(!d||!d.matches||!d.matches('details.section'))return; play(d.open?'open':'close'); if(d.open&&d.matches('.sk'))setTimeout(function(){play('scribble')},450)},true);
 new MutationObserver(function(ms){ms.forEach(function(m){var d=m.target; if(!d.matches||!d.matches('details.section'))return; var was=(m.oldValue||'').split(/\s+/).indexOf('done')>=0, is=d.classList.contains('done'); if(is&&!was)play('done')})}).observe(document.body,{subtree:true,attributes:true,attributeFilter:['class'],attributeOldValue:true});
 ['renderSingle','renderPair'].forEach(function(n){var o=window[n]; if(typeof o!=='function')return; window[n]=function(){var r=o.apply(this,arguments); setTimeout(function(){play('whoosh')},120); return r}});
 // mute switch
 var b=document.createElement('button'); b.type='button'; b.className='sfx-toggle'; b.setAttribute('aria-label','Sounds'); b.setAttribute('aria-pressed',on);
 b.innerHTML='<svg class="on" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3A4.5 4.5 0 0 0 14 8v8a4.5 4.5 0 0 0 2.5-4z"/></svg><svg class="off" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9v6h4l5 5V4L7 9H3zm13.6 3 2.7-2.7-1.4-1.4-2.7 2.7-2.7-2.7-1.4 1.4 2.7 2.7-2.7 2.7 1.4 1.4 2.7-2.7 2.7 2.7 1.4-1.4z"/></svg>';
 b.addEventListener('click',function(){on=!on; b.setAttribute('aria-pressed',on); try{localStorage.setItem('sxl.sfx',on?'on':'off')}catch(e){} if(on){ac();S.pop()}});
 document.body.appendChild(b);
})();
"""

out=src.replace('</style>',css+sfxcss+'\n</style>',1).replace('</body>','<script>'+js+'</script><script>'+sfxjs+'</script><script>'+JS2+'</script></body>',1)
assert '<title>Primer Notebook Card</title>' in out
out=out.replace('<title>Primer Notebook Card</title>','<title>Vocab Primer Motion</title>')
open(S+'primer-motion-v2.html','w').write(out); print(len(out)//1024,'KB')
