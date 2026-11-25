"""Lesson 5 v2 (Night Shift) modules. Content is data, layout is a module, all art slots take emoji until real art arrives.
  nscene   full-bleed dark cinematic scene: pic|pic2 (silhouette that turns out to be pic2), line, line2, say (Narrator), snd 'name@ms,...', rain, flash, rev ms,
           title (big title card), html (raw extra layers). Sounds are synthesised in the browser (rain, thunder, steps, cough, laugh, whoosh) until real clips exist.
  nsounds  four sound tiles: tap to hear, the word appears, whisper it to your partner
  crew_guess  Guess Who finale: five crews, open-question frames, teacher taps the class vote, then where the Stranger really hid
  nescape  the glider-coat escape (Grey always escapes)
Recorded clips: Narrator and laugh clips are matched by exact text (see sxl/audio.py); the laugh clip file is looked up as the text '(laugh)'."""
import html as _h
from ..core import *
from .. import core

def _pic(p):
    if isinstance(p,str) and p.endswith(('.png','.jpg')): return f'<img src="{ART}{p}" style="width:100%;height:100%;object-fit:contain">'
    return p
def _e(t): return _h.escape(t or '',True)

@module('nscene')
def nscene(d):
    o=(f'<div class="a nofit nsc" data-rain="{1 if d.get("rain") else 0}" data-snd="{_e(",".join(d.get("snd",[])))}" data-say="{_e(d.get("say",""))}" '
       f'data-flash="{1 if d.get("flash") else 0}" data-rev="{d.get("rev",0)}" data-say2="{_e(d.get("say2",""))}" style="left:0;top:0;width:1920px;height:1080px;background:#07060d;overflow:hidden">')
    if d.get('title'):
        o+=(f'<div class="a nst1" style="left:0;top:300px;width:1920px;text-align:center;font-family:O;font-weight:800;font-size:230px;line-height:1;letter-spacing:.04em"><span class="grad">{d["title"]}</span></div>'
            f'<div class="a" style="left:0;top:580px;width:1920px;text-align:center;font-family:O;font-weight:800;font-size:80px;color:#cfc8f5">{d.get("sub","")}</div>')
    if d.get('pic') and d.get('full'):   # full-bleed wide art (16:9), the line sits on a dark fade at the bottom
        o+=(f'<div class="a nsp nsp1" style="left:0;top:0;width:1920px;height:1080px"><img data-nz="1" src="{ART}{d["pic"]}" style="width:100%;height:100%;object-fit:cover;display:block"></div>'
            +(f'<div class="a nsp nsp2" style="left:0;top:0;width:1920px;height:1080px"><img data-nz="1" src="{ART}{d["pic2"]}" style="width:100%;height:100%;object-fit:cover;display:block"></div>' if d.get('pic2') else '')+
            '<div class="a" style="left:0;top:640px;width:1920px;height:440px;background:linear-gradient(to bottom,rgba(7,6,13,0),rgba(7,6,13,.88) 70%)"></div>')
    elif d.get('pic') and d.get('wide'):   # wide panorama art, centred at 1800 px
        o+=f'<div class="a nsp nsp1" style="left:60px;top:70px;width:1800px;height:760px;display:flex;align-items:center;justify-content:center"><img data-nz="1" src="{ART}{d["pic"]}" style="width:100%;height:100%;object-fit:contain;border-radius:28px"></div>'
    elif d.get('pic'):
        sz=d.get('sz',560)
        o+=(f'<div class="a nsp nsp1{" sil" if d.get("pic2") else ""}" style="left:460px;top:70px;width:1000px;height:720px;display:flex;align-items:center;justify-content:center;font-size:{sz}px;line-height:1">{_pic(d["pic"])}</div>')
        if d.get('pic2'): o+=f'<div class="a nsp nsp2" style="left:460px;top:70px;width:1000px;height:720px;display:flex;align-items:center;justify-content:center;font-size:{sz}px;line-height:1">{_pic(d["pic2"])}</div>'
    o+=d.get('html','')
    if d.get('line'):
        o+=(f'<div class="a nsl nsl1" style="left:90px;top:{880 if d.get('full') else 830}px;width:1740px;text-align:center;font-family:O;font-weight:800;font-size:{d.get("fs",92)}px;line-height:1.05;color:#f6f3ff;text-shadow:0 0 40px rgba(150,120,255,.6)">{d["line"]}</div>')
    if d.get('line2'):
        o+=(f'<div class="a nsl nsl2" style="left:90px;top:830px;width:1740px;text-align:center;font-family:O;font-weight:800;font-size:{d.get("fs",92)}px;line-height:1.05;color:#ffd27a;text-shadow:0 0 40px rgba(255,170,60,.6)">{d["line2"]}</div>')
    if d.get('hint'): o+=f'<div class="a" style="left:0;top:520px;width:1920px;text-align:center;font-family:O;font-weight:700;font-size:44px;color:#6a6a9e">{d["hint"]}</div>'
    o+='<div class="a nfl"></div></div>'
    return o

@module('nsounds')
def nsounds(d):
    """tiles=[(emoji,word,sound)]. Dark slide. Tap a tile: sound plays, word appears."""
    T=d['tiles']; n=len(T); w=int((1740-30*(n-1))/n)
    o=f'<div class="a nofit nsc" data-rain="{1 if d.get("rain") else 0}" data-snd="" data-say="" data-flash="0" data-rev="0" data-say2="" style="left:0;top:0;width:1920px;height:1080px;background:#07060d">'
    o+=f'<div class="a" style="left:90px;top:56px;display:flex;align-items:center;gap:24px"><div class="tag" style="position:static;{GR}">{d.get("phase","ENGAGE")}</div></div>'
    for i,(e,t,s) in enumerate(T):
        x=90+i*(w+30)
        o+=(f'<div class="a nst" data-snd="{s}" style="left:{x}px;top:190px;width:{w}px;height:640px;border-radius:56px;background:rgba(255,255,255,.07);border:3px solid rgba(255,255,255,.2);cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:26px">'
            f'<span style="font-size:{int(w*.5)}px;line-height:1">{e}</span><span class="nsw" style="font-family:O;font-weight:800;font-size:64px;color:#f6f3ff;opacity:0;transition:opacity .4s">{t}</span></div>')
    o+='<div class="a" style="left:90px;top:860px;width:1740px;display:flex;gap:40px;justify-content:center;font-size:110px;line-height:1"><span>👆</span><span>👂</span><span>🤫</span><span>🧑‍🤝‍🧑</span></div>'
    o+='<div class="a nfl"></div></div>'
    return o

@module('crew_guess')
def crew_guess(d):
    """crews=[{e (place emoji), who (staff emoji), n (name), p (place word)}] x5, frames=[question text]. Teacher taps the crew with most hands, then Reveal, then the crew where the Stranger really was."""
    C=d['crews']; n=len(C); w=int((1740-24*(n-1))/n)
    o=header(d['phase'],d.get('role','Who is the Stranger?'),'rose')
    for i,c in enumerate(C):
        x=90+i*(w+24)
        o+=(f'<div class="gl cgc" data-i="{i}" data-p="{_e(c["p"])}" style="left:{x}px;top:180px;width:{w}px;height:370px;border-radius:52px;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px">'
            f'<span style="font-size:130px;line-height:1">{emo(c["e"])}</span><span style="font-size:96px;line-height:1">{emo(c["who"])}</span><span style="font-family:O;font-weight:800;font-size:40px;color:#1c1b2e">{c["n"]}</span></div>')
    F=d['frames']
    o+='<div class="a" style="left:90px;top:585px;width:1740px;display:flex;flex-wrap:wrap;gap:14px;justify-content:center">'+''.join(f'<span class="pill" style="font-size:38px;padding:10px 30px;color:#4a3a8a;font-family:O;font-weight:800">{t}</span>' for t in F)+'</div>'
    o+='<div class="a cgmsg" style="left:90px;top:760px;width:1740px;text-align:center;font-family:O;font-weight:800;font-size:56px;color:#4a3a8a;height:80px">Ask the crews. Listen for a story that does not match.</div>'
    o+=f'<div class="a cgbtn" style="left:690px;top:870px;width:540px;height:110px;border-radius:55px;display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:48px;cursor:pointer;{GR};opacity:.35">1 · Class vote</div>'
    return o

@module('nescape')
def nescape(d):
    html=('<div class="a" style="left:1180px;top:210px;font-size:300px;line-height:1">🪟</div>'
          '<div class="a gly" style="left:540px;top:300px;font-size:300px;line-height:1">🥼</div>'
          '<div class="a gly gw1" style="left:380px;top:300px;font-size:260px;line-height:1;transform:scaleX(-1)">🪽</div>'
          '<div class="a gly gw2" style="left:820px;top:300px;font-size:260px;line-height:1">🪽</div>')
    return nscene(dict(d,html=html,pic=None))

core.EXT_CSS.append("""
.nsc .nsp{opacity:0;transition:opacity 1.2s}.nsc.go .nsp{opacity:1}.nsp.sil{filter:brightness(0) drop-shadow(0 0 30px rgba(220,220,255,.7))}.nsc.rev .nsp1{opacity:0!important}.nsp2{opacity:0}.nsc.go .nsp2{opacity:0}.nsc.rev.go .nsp2{opacity:1}
.nsl{opacity:0;transition:opacity 1s}.nsc.go .nsl1{opacity:1}.nsc.rev .nsl1{opacity:0!important}.nsc.rev .nsl2{opacity:1}
.nst1{opacity:0;transition:opacity 1.4s}.nsc.go .nst1{opacity:1}
.nfl{left:0;top:0;width:1920px;height:1080px;background:#fff;opacity:0;pointer-events:none}.nsc.fl .nfl{animation:nflash 1.2s ease-out 1}
@keyframes nflash{0%{opacity:0}5%{opacity:.95}13%{opacity:.08}20%{opacity:.75}100%{opacity:0}}
.nst:hover{background:rgba(255,255,255,.14)!important}.nst.on{border-color:#c9a2ff!important;box-shadow:0 0 40px rgba(170,120,255,.5)}.nst.on .nsw{opacity:1!important}
.cgc.vote{box-shadow:0 0 0 12px #ff9f1c!important}.cgc.dim{opacity:.45}.cgc.rvl{box-shadow:0 0 0 12px #ff4f7a!important}.cgc.hit{box-shadow:0 0 0 12px #2bd9b6!important}
.gly{opacity:0}.nsc.go .gly{animation:glide 4.2s ease-in 1.6s forwards}.nsc.go .gw1,.nsc.go .gw2{animation:glidew 4.2s ease-in 1.6s forwards}
@keyframes glide{0%{opacity:1;transform:translate(0,0) scale(1) rotate(0)}25%{opacity:1;transform:translate(180px,-60px) scale(1.05) rotate(-6deg)}100%{opacity:1;transform:translate(820px,-300px) scale(.12) rotate(14deg)}}
@keyframes glidew{0%{opacity:1;transform:translate(0,0) scale(.3) rotate(0)}20%{opacity:1;transform:translate(160px,-50px) scale(1.1) rotate(-6deg)}100%{opacity:1;transform:translate(820px,-300px) scale(.12) rotate(14deg)}}
.gw1{transform-origin:right center}
""")

core.EXT_JS.append(r"""
(function(){
 var AC=null,RN=null,RA=null,RF=null,sfxOn=function(){try{return localStorage.getItem('sxl.sfx')!=='off'}catch(e){return true}};
 function ac(){if(!AC){var C=window.AudioContext||window.webkitAudioContext;if(!C)return null;try{AC=new C()}catch(e){return null}}if(AC.state==='suspended'){try{AC.resume()}catch(e){}}return AC}
 function nb(sec){var c=ac(),b=c.createBuffer(1,Math.floor(c.sampleRate*sec),c.sampleRate),d=b.getChannelData(0);for(var i=0;i<d.length;i++)d[i]=Math.random()*2-1;return b}
 function src(buf,loop){var s=ac().createBufferSource();s.buffer=buf;s.loop=!!loop;return s}
 function env(g,t,a,peak,dur){g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(peak,t+a);g.gain.exponentialRampToValueAtTime(.0001,t+dur)}
 var NS=window.NS={
  rain:function(on){if(window.SXLS&&window.SXLS.rain){if(on&&sfxOn()){if(!RA){RA=new Audio(window.SXLS.rain[0]);RA.loop=true;RA.volume=0}RA.play()["catch"](function(){});clearInterval(RF);RF=setInterval(function(){RA.volume=Math.min(.22,RA.volume+.02);if(RA.volume>=.22)clearInterval(RF)},100)}else if(RA){clearInterval(RF);var a=RA;RF=setInterval(function(){a.volume=Math.max(0,a.volume-.05);if(a.volume<=0){clearInterval(RF);a.pause()}},60)}return}var c=ac();if(!c)return;if(on&&sfxOn()){if(RN)return;var s=src(nb(2),true),hp=c.createBiquadFilter(),bp=c.createBiquadFilter(),g=c.createGain();hp.type='highpass';hp.frequency.value=900;bp.type='lowpass';bp.frequency.value=7000;g.gain.value=.0001;g.gain.exponentialRampToValueAtTime(.075,c.currentTime+2);s.connect(hp);hp.connect(bp);bp.connect(g);g.connect(c.destination);s.start();RN={s:s,g:g}}
   else if(RN){var r=RN;RN=null;try{r.g.gain.setTargetAtTime(.0001,c.currentTime,.25);setTimeout(function(){try{r.s.stop()}catch(e){}},900)}catch(e){}}},
  thunder:function(){var c=ac();if(!c)return;var t=c.currentTime,s=src(nb(4)),lp=c.createBiquadFilter(),g=c.createGain();lp.type='lowpass';lp.frequency.setValueAtTime(420,t);lp.frequency.exponentialRampToValueAtTime(70,t+3.2);s.connect(lp);lp.connect(g);g.connect(c.destination);env(g,t,.05,.9,3.6);s.start(t)},
  steps:function(){var c=ac();if(!c)return;for(var i=0;i<4;i++){(function(i){var t=c.currentTime+i*.52,s=src(nb(.3)),lp=c.createBiquadFilter(),g=c.createGain();lp.type='lowpass';lp.frequency.value=260;s.connect(lp);lp.connect(g);g.connect(c.destination);env(g,t,.01,.55,.2);s.start(t)})(i)}},
  cough:function(){var c=ac();if(!c)return;[0,.28,.5].forEach(function(o,i){var t=c.currentTime+o,s=src(nb(.3)),bp=c.createBiquadFilter(),g=c.createGain();bp.type='bandpass';bp.frequency.value=i?900:700;bp.Q.value=1.1;s.connect(bp);bp.connect(g);g.connect(c.destination);env(g,t,.01,i?.45:.7,i?.14:.18);s.start(t)})},
  whoosh:function(){var c=ac();if(!c)return;var t=c.currentTime,s=src(nb(2)),bp=c.createBiquadFilter(),g=c.createGain();bp.type='bandpass';bp.Q.value=.8;bp.frequency.setValueAtTime(300,t);bp.frequency.exponentialRampToValueAtTime(3000,t+1.6);s.connect(bp);bp.connect(g);g.connect(c.destination);env(g,t,.5,.5,1.8);s.start(t)},
  laugh:function(){var c=ac();if(!c)return;var t0=c.currentTime,out=c.createGain(),dl=c.createDelay(.6),fb=c.createGain();out.gain.value=.5;dl.delayTime.value=.23;fb.gain.value=.38;out.connect(c.destination);out.connect(dl);dl.connect(fb);fb.connect(dl);dl.connect(c.destination);
   [0,.36,.72,1.1,1.62].forEach(function(o,i){var t=t0+o,L=i===4?.9:.26,f=(150-i*9),osc=c.createOscillator(),lp=c.createBiquadFilter(),g=c.createGain(),vb=c.createOscillator(),vg=c.createGain();osc.type='sawtooth';osc.frequency.setValueAtTime(f*1.35,t);osc.frequency.exponentialRampToValueAtTime(f,t+L);vb.frequency.value=i===4?7:13;vg.gain.value=i===4?9:5;vb.connect(vg);vg.connect(osc.frequency);lp.type='bandpass';lp.frequency.setValueAtTime(520,t);lp.frequency.linearRampToValueAtTime(980,t+L*.6);lp.Q.value=2.2;osc.connect(lp);lp.connect(g);g.connect(out);env(g,t,.03,.5,L);osc.start(t);vb.start(t);osc.stop(t+L+.05);vb.stop(t+L+.05)})},
  clip:function(n,vol){var L=window.SXLS&&window.SXLS[n];if(!L||!L.length)return false;try{var a=new Audio(L[Math.floor(Math.random()*L.length)]);a.volume=vol;a.play()["catch"](function(){});return true}catch(e){return false}},
  play:function(n){if(!sfxOn())return;try{var V={thunder:.75,steps:.7,cough:.7,whoosh:.7,laugh:.8,laugh2:.8,creak:.7,lights:.6};if(V[n]&&NS.clip(n,V[n]))return;NS[n]&&NS[n]()}catch(e){}},
  say:function(t){if(!t||!sfxOn())return;if(window.SXLsay&&SXLsay(t))return;try{if(!window.speechSynthesis)return;speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(t);u.lang='en-GB';u.rate=.78;u.pitch=.85;speechSynthesis.speak(u)}catch(e){}}
 };
 var T=[];function later(f,ms){T.push(setTimeout(f,ms))}function clr(){T.forEach(clearTimeout);T=[];try{window.speechSynthesis&&speechSynthesis.cancel()}catch(e){}}
 function enter(s){clr();var n=s.querySelector('.nsc');NS.rain(!!(n&&n.dataset.rain==='1'));
  $$('.nsc.go,.nsc.fl,.nsc.rev').forEach(function(x){x.classList.remove('go','fl','rev')});
  if(!n)return;void n.offsetWidth;n.classList.add('go');
  if(n.dataset.flash==='1'&&!SXL.cfg.off&&!SXL.cfg.calm)n.classList.add('fl');
  (n.dataset.snd||'').split(',').filter(Boolean).forEach(function(x){var p=x.split('@');later(function(){NS.play(p[0])},+(p[1]||0))});
  if(n.dataset.say)later(function(){NS.say(n.dataset.say)},n.dataset.flash==='1'?1100:500);
  var rv=+n.dataset.rev;if(rv)later(function(){n.classList.add('rev');if(n.dataset.say2)NS.say(n.dataset.say2)},rv)}
 $$('.sl').forEach(function(s){var was=false;new MutationObserver(function(){var o=s.classList.contains('on');if(o&&!was){was=true;enter(s)}else if(!o)was=false}).observe(s,{attributes:true,attributeFilter:['class']})});
 document.addEventListener('click',function(e){var t=e.target.closest('.nst');if(t){t.classList.add('on');NS.play(t.dataset.snd);return}
  var s=e.target.closest('.sl');if(!s||!s.querySelector('.cgc'))return;
  var cs=$$('.cgc',s),msg=$('.cgmsg',s),btn=$('.cgbtn',s),c=e.target.closest('.cgc');
  if(c&&(!s.__st||s.__st==='vr')){cs.forEach(function(x){x.classList.toggle('vote',x===c);x.classList.remove('dim')});s.__vote=c;btn.style.opacity=1;P('pop');return}
  if(c&&s.__st==='rv'){var v=s.__vote;cs.forEach(function(x){x.classList.remove('vote','rvl','hit','dim');if(x!==c&&x!==v)x.classList.add('dim')});
   if(v===c){c.classList.add('hit');msg.textContent='You found the Stranger’s crew!';P('good')}else{c.classList.add('rvl');v&&v.classList.add('vote');msg.textContent='Not this time. The Stranger was in the '+c.dataset.p+' crew.';P('boop')}
   btn.textContent='The Stranger is going to escape…';btn.style.opacity=.9;s.__st='done';return}
  if(e.target.closest('.cgbtn')){if(!s.__st){if(!s.__vote){msg.textContent='Tap the crew with the most hands first.';return}s.__st='vr';btn.textContent='2 · Reveal the Stranger';msg.textContent='The Stranger is hiding in one crew. Reveal?';P('open');return}
   if(s.__st==='vr'){s.__st='rv';cs.forEach(function(x){x.classList.add('rvl')});msg.textContent='Tap the crew where the Stranger really was.';btn.style.opacity=.35;P('tick');return}}
 },true);
})();
""")
