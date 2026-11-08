"""Interactive (offline, single-file) renderer. Same data dicts as the static deck.
build_interactive(spec, out_html): spec items with m in {chat, sort, timeline}. Everything is inlined (fonts, art, emoji, sounds synthesised) -> no network.
General layer = SXLSound (primer engine, copied) + Motion On/Calm/Off. Behaviour per module is in JS below."""
import re, json, base64, io, os, pathlib
from PIL import Image
from . import core
from .core import *
from .modules import chat as C
from .modules.chat import gapchip, AV

def _b64(path, kind):
    if kind == 'font': return 'data:font/woff2;base64,' + base64.b64encode(open(path, 'rb').read()).decode()
    im = Image.open(path)
    if kind == 'art':
        im = im.convert('RGB'); im.thumbnail((640, 640)); b = io.BytesIO(); im.save(b, 'JPEG', quality=72)
        return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    b = io.BytesIO(); im.thumbnail((200, 200)); im.save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

def inline_assets(html):
    cache = {}
    def rep(m):
        u = m.group(0); p = u[len('file://'):]
        if u not in cache:
            kind = 'font' if p.endswith('.woff2') else 'art' if '/art/' in p else 'emoji'
            cache[u] = _b64(p, kind)
        return cache[u]
    return re.sub(r'file:///[^")\'\s]+', rep, html)

# ---------- slide builders (markup identical to static modules; behaviour via data-* hooks) ----------
def chat_markup(d, sid):
    L = d['lines']; av = d.get('avatars', {}); data = []; rows = ''
    for i, l in enumerate(L):
        s, c, bank = C.parts(l); pc = l[3] if len(l) > 3 else None
        left = s in ('N', 'D'); a = EM(av.get(s, AV[s]))
        if isinstance(c, str):
            inner = f'<div style="font-family:O;font-weight:800;font-size:52px;color:#1c1b2e">{c}</div>'; gaps = []
        else:
            parts_ = []; gaps = []
            for c_, t, g in c:
                if g:
                    gaps.append([c_, t]); parts_.append(f'<span class="gp" data-c="{c_}" data-t="{t}"><span class="op">{gapchip(c_, t)}</span><span class="fl" style="display:none">{ch(c_, t, 46, "8px 26px")}</span></span>')
                else: parts_.append(ch(c_, t, 46, '8px 26px'))
            inner = '<div style="display:flex;gap:12px;align-items:center">' + ''.join(parts_) + '</div>'
        pimg = (f'<img src="{ART}{pc}" style="height:112px;width:112px;border-radius:26px;margin-left:30px;background:#fff;object-fit:contain">' if pc else '')
        bub = f'<div class="gl" style="position:static;height:130px;border-radius:65px;display:flex;align-items:center;padding:0 {18 if pc else 46}px 0 46px;{"" if left else "background:rgba(214,190,255,.75);"}">{inner}{pimg}</div>'
        avh = f'<div class="gl" style="position:static;width:110px;height:110px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;background:#fff"><img src="{a}" style="width:78px"></div>'
        rows += f'<div class="row" data-i="{i}" style="align-self:{"flex-start" if left else "flex-end"};display:none;align-items:center;gap:22px;{"" if left else "flex-direction:row-reverse"}">{avh}{bub}</div>'
        bk = bank or d.get('bank') if gaps else None
        data.append({'gaps': gaps, 'bank': [[a_, b_] for a_, b_ in (bk or [])]})
    bankhtml = {}
    for i, x in enumerate(data):
        bankhtml[i] = ''.join(f'<button class="bk" data-c="{c_}" data-t="{t}">{ch(c_, t, 46, "8px 26px")}</button>' for c_, t in x['bank'])
    return (header(d['phase'], d.get('title')) +
            f'<div class="thread" id="th-{sid}">{rows}<div style="height:30px;flex-shrink:0"></div></div>'
            f'<div class="gl bankbar" id="bk-{sid}" style="left:90px;top:896px;width:1740px;height:100px;border-radius:50px;display:flex;align-items:center;gap:20px;padding:0 40px"></div>'
            f'<script type="application/json" id="d-{sid}">{json.dumps({"banks": bankhtml, "n": len(L), "gapn": [len(x["gaps"]) for x in data]})}</script>')

def sort_markup(d, sid):
    rows = d['rows']; n = len(rows); top, bot = 168, 830; step = (bot - top) / n; h = min(int(step - 18), 190); fs = min(72, int(h * .42)); ps = max(10, int(h * .22))
    out = header(d['phase'], d.get('title')); bank = d['bank']; plain = [b if isinstance(b, tuple) else ('c2', b) for b in bank if b != '|']
    for i, r in enumerate(rows):
        y = int(top + i * step); pre = r.get('pre', ('c1', 'You')) if r.get('pre', 1) else None; end = r.get('end')
        a = r.get('ans', [plain[i][1]]); a = [a] if isinstance(a, str) else a
        out += num(90, y + h // 2 - 32, i + 1) + pic(180, y, h, h, r['pic'], r=int(h * .23))
        x0 = 180 + h + 40
        def slot(k, cls, col, w):
            return (f'<span class="slot" data-i="{i}" data-t="{a[k]}"><span class="op">{gap(col, w, "…", h=int(fs * 1.45))}</span>'
                    f'<span class="fl" style="display:none">{ch(cls, a[k], fs, f"{ps}px {int(fs * .55)}px")}</span></span>')
        slots = slot(0, 'c2', '#9a5cff', 420) + ('' if end else slot(1, 'c3', '#ff7a3c', 470))
        out += (f'<div class="gl" style="left:{x0}px;top:{y}px;width:{1830 - x0}px;height:{h}px;border-radius:{int(h * .4)}px;display:flex;align-items:center;gap:22px;padding:0 50px">'
                + (ch(pre[0], pre[1], fs, f'{ps}px {int(fs * .55)}px') if pre else '') + slots
                + (ch(end[0], end[1], fs, f'{ps}px {int(fs * .55)}px') if end else '') + '</div>')
    need = {}
    for r in rows:
        a = r.get('ans'); a = [a] if isinstance(a, str) else (a or [])
        for t in a: need[t] = need.get(t, 0) + 1
    bfs = 52 if len(bank) > 4 else 56; btn = ''
    for b in bank:
        if b == '|': btn += '<div style="width:6px;height:70px;border-radius:3px;background:#b9a6f5;margin:0 10px"></div>'; continue
        c, t = b if isinstance(b, tuple) else ('c2', b)
        btn += f'<button class="bk" data-t="{t}" data-n="{need.get(t, 1)}">{ch(c, t, bfs, "8px 30px")}</button>'
    out += f'<div class="gl" style="left:90px;top:840px;width:1740px;height:148px;border-radius:72px;display:flex;align-items:center;gap:20px;padding:0 44px" id="bk-{sid}">{btn}</div>'
    return out

def timeline_markup(d, sid):
    P = d['pics']; n = len(P); order = d.get('order', list(range(n))); w = min(330, int((1740 - 40 * (n - 1)) / n)); gx = int((1740 - w * n) / (n - 1)) if n > 1 else 0
    out = header(d['phase'], d.get('title', 'What happened first?'), 'amber'); sy = 170 + w + 80
    for k in range(n):
        x = 90 + k * (w + gx)
        out += (f'<div class="a slotn" data-k="{k}" style="left:{x}px;top:{sy}px;width:{w}px;height:{w}px;border-radius:44px;border:5px dashed #b9a6f5;background:rgba(255,255,255,.4);display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:{int(w * .35)}px;color:#b9a6f5">{k + 1}</div>')
    for k, idx in enumerate(order):
        x = 90 + k * (w + gx); rot = (-3, 2, -2, 3)[k % 4]
        out += (f'<button class="card" data-idx="{idx}" data-x="{x}" data-sx="{90 + idx * (w + gx)}" data-sy="{sy}" style="left:{x}px;top:170px;width:{w}px;height:{w}px;transform:rotate({rot}deg)">'
                + art(0, 0, w, w, P[idx], r=44, label=P[idx]) + '</button>')
    return out + f'<script type="application/json" id="d-{sid}">{json.dumps({"n": n})}</script>'


DOTS={'dot1':'●','dot2':'● ●','buzz':'〰'}
HINT={'dot1':'tap','buzz':'hand on throat','dot2':'clap clap'}
def sound_markup(d, sid):
    B=d['bags']; n=len(B); w=int((1740-40*(n-1))/n); out=header(d['phase'],d.get('title','Listen. Which sound?'),'orange'); aud=d.get('audio',{})
    for i,b in enumerate(B):
        x=90+i*(w+40); out+=glass(x,170,w,560,'',r=64)
        out+=f'<div class="a bagic" data-i="{i}" style="left:{x}px;top:200px;width:{w}px;text-align:center;font-family:O;font-weight:800;font-size:150px;color:#6a35e8">{DOTS[b["icon"]]}</div>'
        out+=f'<div class="a mu bagh" style="left:{x}px;top:640px;width:{w}px;text-align:center;font-size:40px;opacity:0">{HINT[b["icon"]]}</div>'
        out+=f'<div class="a bag" data-i="{i}" style="left:{x}px;top:170px;width:{w}px;height:560px;border-radius:64px"><div class="drop" style="position:absolute;left:30px;top:300px;width:{w-60}px;display:flex;flex-direction:column;gap:16px;align-items:center;min-height:140px;border-radius:44px;border:5px dashed #b9a6f5;padding:6px"></div></div>'
    words=[(t,i) for i,b in enumerate(B) for t in b['words']]
    out+=('<div class="gl" style="left:90px;top:790px;width:1740px;height:190px;border-radius:80px;display:flex;align-items:center;gap:26px;padding:0 60px" id="bk-'+sid+'">'
          +''.join(f'<button class="bk" data-t="{t}" data-bag="{i}" data-a="{aud.get(t,"")}">{ch("c2",t,64,"10px 40px")}</button>' for t,i in words)+'</div>')
    return out+f'<script type="application/json" id="d-{sid}">{json.dumps({"demo":d.get("demo",0)})}</script>'

def match_markup(d, sid):
    P=d['pics']; W=d['words']; n=len(P); w=int((1740-40*(n-1))/n); out=header(d['phase'],d.get('title','Match'),'violet')
    for i,p in enumerate(P):
        x=90+i*(w+40); out+=f'<button class="mp" data-i="{i}" style="position:absolute;left:{x}px;top:170px;width:{w}px;height:{w}px;border-radius:44px">'+art(0,0,w,w,p,r=44,label=p)+num(16,-34,i+1,64)+'</button>'
    order=[(i*3+1)%n for i in range(n)] if n>2 else list(range(n))
    out+='<div class="gl" style="left:90px;top:%dpx;width:1740px;height:300px;border-radius:72px;display:flex;align-items:center;justify-content:center;gap:36px;padding:0 40px">'%(170+w+60)
    for i in order:
        out+=f'<button class="mw" data-i="{i}" style="display:flex;flex-direction:column;align-items:center;gap:14px"><span class="mg">{gap("#9a5cff",64,"",h=64)}</span>{ch("c3",W[i],52,"8px 30px")}</button>'
    return out+'</div>'+f'<script type="application/json" id="d-{sid}">{json.dumps({"n":n})}</script>'

def fib_markup(d, sid):
    out=header(d['phase'],d.get('title','True or a fib?'),'red')+art(90,170,820,820,d['pic'],r=56,label=d['pic'])
    for k,(chips_,ok) in enumerate(d['statements']):
        y=200+k*400
        out+=f'<div class="gl" style="left:980px;top:{y}px;width:850px;height:230px;border-radius:70px;display:flex;align-items:center;gap:14px;padding:0 40px;flex-wrap:wrap">'+core.chips(chips_,50,'8px 26px')+'</div>'
        out+=(f'<button class="tf" data-k="{k}" data-v="1" data-ok="{int(ok)}" style="position:absolute;left:1100px;top:{y+250}px;width:110px;height:110px">'+f'<img src="{E}check_mark_button.png" style="width:110px">'+'</button>'
              +f'<button class="tf" data-k="{k}" data-v="0" data-ok="{int(ok)}" style="position:absolute;left:1260px;top:{y+250}px;width:110px;height:110px">'+f'<img src="{E}cross_mark.png" style="width:110px">'+'</button>')
    return out+f'<script type="application/json" id="d-{sid}">{json.dumps({"n":len(d["statements"])})}</script>'

BUILD = {'chat': chat_markup, 'sort': sort_markup, 'timeline': timeline_markup, 'sound_sort': sound_markup, 'match_pairs': match_markup, 'spot_fib': fib_markup}


CSS_EXTRA = """
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#eeeef3}
body{width:100%!important;height:100%!important}
#stage{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;overflow:hidden}
.sl{position:absolute;inset:0;display:none;overflow:hidden}.sl.on{display:block}
.thread{position:absolute;left:90px;top:168px;width:1740px;height:712px;overflow-y:auto;display:flex;flex-direction:column;gap:48px;scrollbar-width:thin;scrollbar-color:#b9a6f5 transparent;padding:6px 8px}
.row:first-child{margin-top:auto}
.row.show{display:flex!important;animation:up .5s cubic-bezier(.2,.9,.3,1.2) both}
@keyframes up{from{opacity:0;transform:translateY(60px)}to{opacity:1;transform:none}}
button{all:unset;cursor:pointer;-webkit-tap-highlight-color:transparent}
.bk{display:inline-block;transition:transform .2s}.bk:active{transform:scale(.94)}.bk.sel{transform:translateY(-14px) scale(1.06);filter:drop-shadow(0 20px 18px rgba(80,40,160,.35))}
.bk.used{opacity:.25;pointer-events:none}
.shake{animation:sh .35s}@keyframes sh{20%{transform:translateX(-14px)}40%{transform:translateX(12px)}60%{transform:translateX(-8px)}80%{transform:translateX(5px)}}
.mo{animation:moc .5s cubic-bezier(.2,1.6,.4,1)}@keyframes moc{from{transform:scale(.4)}to{transform:scale(1)}}
.card{position:absolute;transition:left .6s cubic-bezier(.3,1.2,.4,1),top .6s cubic-bezier(.3,1.2,.4,1),transform .5s}
.bag{pointer-events:auto;cursor:pointer}.drop.hot{background:rgba(255,255,255,.5)}.mp,.mw{cursor:pointer}.mp.sel,.mw.sel{transform:translateY(-12px) scale(1.04)}.mp.ok{opacity:.55;pointer-events:none}.mw.ok{pointer-events:none}.tf{transition:opacity .3s,transform .2s}.tf.off{opacity:.18;pointer-events:none}.tf.pick{transform:scale(1.25)}
.card.done{pointer-events:none}
.pulse{animation:pu .8s 2}@keyframes pu{50%{transform:scale(1.05)}}
.calm *,.off *{animation-duration:.01s!important;transition-duration:.01s!important}
#ctl{position:absolute;right:30px;top:20px;z-index:50;display:flex;gap:14px}
#ctl button{font:700 28px Outfit,O,sans-serif;padding:8px 22px;border-radius:999px;background:rgba(255,255,255,.8);border:3px solid #fff;color:#6a35e8;box-shadow:0 8px 20px rgba(80,60,160,.15)}
#nx{position:absolute;right:90px;bottom:34px;z-index:40;width:96px;height:96px;border-radius:50%;background:linear-gradient(135deg,#9a5cff,#6a35e8);color:#fff;font:800 56px O;display:none;align-items:center;justify-content:center;box-shadow:0 20px 40px rgba(80,40,200,.4)}
#nx.on{display:flex;animation:up .5s both}
"""

# general layer: primer SXLSound engine (copied from vocab-primer/live-test/motion/vp-motion.js) + shared helpers
SFX_JS = r"""
(function(){
 var ctx=null,on=true,VOL=.55; try{on=localStorage.getItem('sxl.sfx')!=='off'}catch(e){}
 window.SXL={cfg:{calm:false,off:false}};
 var calm=function(){return SXL.cfg.calm||SXL.cfg.off};
 function ac(){if(!ctx){var C=window.AudioContext||window.webkitAudioContext;if(!C)return null;try{ctx=new C()}catch(e){return null}}if(ctx.state==='suspended'){try{ctx.resume()}catch(e){}}return ctx}
 function tone(f,d,o){o=o||{};var c=ac();if(!c)return;var t=c.currentTime+(o.at||0),osc=c.createOscillator(),g=c.createGain();osc.type=o.type||'sine';osc.frequency.setValueAtTime(f,t);if(o.to)osc.frequency.exponentialRampToValueAtTime(o.to,t+d);g.gain.setValueAtTime(0.0001,t);g.gain.exponentialRampToValueAtTime(Math.max(.0002,(o.g||.2)*VOL),t+.008);g.gain.exponentialRampToValueAtTime(0.0001,t+d);osc.connect(g);g.connect(c.destination);osc.start(t);osc.stop(t+d+.03)}
 var S={pop:function(){tone(640,.09,{to:380,g:.2})},tick:function(){tone(900,.04,{type:'triangle',g:.07})},
  done:function(){[523,659,784,1047].forEach(function(f,i){tone(f,.3,{at:i*.07,g:.15})})},
  good:function(){[659,880,1175].forEach(function(f,i){tone(f,.26,{at:i*.08,g:.16})})},boop:function(){tone(330,.18,{to:260,g:.16})},
  arrive:function(){[523.25,587.33,659.25,783.99].forEach(function(f,i){var L=i===3?1.1:.5;tone(f,L,{at:i*.16,g:.2});tone(f*2,L*.55,{at:i*.16,g:.045})})},
  open:function(){tone(392,.12,{g:.12});tone(523,.15,{at:.07,g:.12})}};
 var lastArr=0;
 window.SXLSound={play:function(n){if(!on||calm())return;if(n==='arrive'){if(Date.now()-lastArr<900)return;lastArr=Date.now()}try{S[n]()}catch(e){}},toggle:function(){on=!on;try{localStorage.setItem('sxl.sfx',on?'on':'off')}catch(e){}return on}};
 ['pointerdown','touchend','click','keydown'].forEach(function(e){document.addEventListener(e,function(){if(on)ac()},true)});
})();
"""

APP_JS = r"""
var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var P=function(n){SXLSound.play(n)}, wait=function(ms){return new Promise(function(r){setTimeout(r,SXL.cfg.off?0:ms)})};
function fit(){var s=Math.min(innerWidth/1920,innerHeight/1080);var st=$('#stage');st.style.transform='scale('+s+')';st.style.left=(innerWidth-1920*s)/2+'px';st.style.top=(innerHeight-1080*s)/2+'px'}
addEventListener('resize',fit);fit();
var slides=$$('.sl'),cur=-1;
function go(i){if(i<0||i>=slides.length)return;slides.forEach(function(s){s.classList.remove('on')});cur=i;var s=slides[i];s.classList.add('on');$('#nx').classList.remove('on');if(!s.__init){s.__init=1;INIT[s.dataset.m](s)}else if(s.__done)$('#nx').classList.add('on');}
function finish(s){s.__done=1;P('done');wait(500).then(function(){if(cur<slides.length-1)$('#nx').classList.add('on')})}
$('#nx').onclick=function(){P('open');go(cur+1)};
addEventListener('keydown',function(e){if(e.key==='ArrowRight'&&$('#nx').classList.contains('on'))go(cur+1);if(e.key==='ArrowLeft')go(cur-1)});
var cfgs=['On','Calm','Off'],ci=0;
$('#mo').onclick=function(){ci=(ci+1)%3;SXL.cfg.calm=ci==1;SXL.cfg.off=ci==2;document.body.className=['','calm','off'][ci];this.textContent='Motion: '+cfgs[ci]};
$('#sf').onclick=function(){var on=SXLSound.toggle();this.textContent='Sound: '+(on?'On':'Off')};
function wrong(el){P('boop');el.classList.remove('shake');void el.offsetWidth;el.classList.add('shake')}
function put(slotEl){$('.op',slotEl).style.display='none';var f=$('.fl',slotEl);f.style.display='inline-block';f.classList.add('mo');P('pop');setTimeout(function(){P('tick')},90)}
var INIT={};
/* ---- chat: tap-to-fill, auto-scroll, free scroll-back ---- */
INIT.chat=function(s){
 var id=s.dataset.id,D=JSON.parse($('#d-'+id).textContent),th=$('#th-'+id),bar=$('#bk-'+id),rows=$$('.row',th),i=-1;
 function next(){i++;if(i>=D.n){finish(s);return}var r=rows[i];r.classList.add('show');if(i>0)P('arrive');th.scrollTo({top:th.scrollHeight,behavior:SXL.cfg.off?'auto':'smooth'});
  if(D.gapn[i]){bar.innerHTML=D.banks[i];bar.style.visibility='visible';bar.__r=r}else{bar.style.visibility='hidden';wait(1100).then(next)}}
 bar.onclick=function(e){var b=e.target.closest('.bk');if(!b||!bar.__r)return;var g=$$('.gp',bar.__r).filter(function(x){return !x.__f})[0];if(!g)return;
  if(b.dataset.t===g.dataset.t&&b.dataset.c===g.dataset.c){g.__f=1;put(g);b.classList.add('used');if(!$$('.gp',bar.__r).some(function(x){return !x.__f})){bar.__r=null;wait(900).then(next)}}else wrong(b)};
 next();};
/* ---- sort: tap a word, tap its picture row ---- */
INIT.sort=function(s){
 var id=s.dataset.id,bar=$('#bk-'+id),slots=$$('.slot',s),sel=null,left=slots.length;
 function pick(b){$$('.bk',bar).forEach(function(x){x.classList.remove('sel')});sel=b;if(b){b.classList.add('sel');P('tick')}}
 bar.onclick=function(e){var b=e.target.closest('.bk');if(b&&!b.classList.contains('used'))pick(sel===b?null:b)};
 slots.forEach(function(sl){sl.onclick=function(){if(sl.__f)return;if(!sel){sl.classList.add('pulse');setTimeout(function(){sl.classList.remove('pulse')},1700);P('tick');return}
  if(sel.dataset.t===sl.dataset.t){sl.__f=1;put(sl);sel.classList.remove('sel');sel.__n=(sel.__n==null?+(sel.dataset.n||1):sel.__n)-1;if(sel.__n<=0)sel.classList.add('used');sel=null;if(--left==0)finish(s)}else{var b=sel;wrong(sl);b.classList.remove('sel');sel=null}}});};
/* ---- timeline: tap the card that happened next ---- */
INIT.timeline=function(s){
 var cards=$$('.card',s),slots=$$('.slotn',s),k=0;
 cards.forEach(function(c){c.onclick=function(){if(+c.dataset.idx===k){var sl=slots[k];c.style.left=sl.style.left;c.style.top=sl.style.top;c.style.transform='rotate(0deg)';c.classList.add('done');sl.style.opacity=.0;P('pop');setTimeout(function(){P('tick')},120);k++;if(k==cards.length)finish(s)}else wrong(c)}});};
/* ---- sound sort: watch the first word go in, then place the rest. Optional per-word audio (data-a) only if supplied. ---- */
INIT.sound_sort=function(s){
 var id=s.dataset.id,D=JSON.parse($('#d-'+id).textContent),bar=$('#bk-'+id),bags=$$('.bag',s),sel=null,left=$$('.bk',bar).length;
 function drop(b,bag){var d=$('.drop',bag);d.appendChild(b.cloneNode(true));$$('button',d).forEach(function(x){x.className='';x.style.pointerEvents='none'});b.classList.remove('sel');b.classList.add('used');d.lastChild.classList.add('mo');P('pop');setTimeout(function(){P('tick')},90);if(--left==0)finish(s)}
 function hint(i){var h=$$('.bagh',s)[i],ic=$$('.bagic',s)[i];h.style.opacity=1;ic.classList.add('pulse');setTimeout(function(){ic.classList.remove('pulse')},1700)}
 function play(b){var a=b.dataset.a;if(a&&!SXL.cfg.calm&&!SXL.cfg.off){try{new Audio(a).play()}catch(e){}}}
 bar.onclick=function(e){var b=e.target.closest('.bk');if(!b||b.classList.contains('used'))return;$$('.bk',bar).forEach(function(x){x.classList.remove('sel')});sel=(sel===b)?null:b;if(sel){sel.classList.add('sel');P('tick');play(sel)}};
 bags.forEach(function(g){g.onclick=function(){if(!sel){hint(+g.dataset.i);P('tick');return}if(sel.dataset.bag===g.dataset.i){var b=sel;sel=null;drop(b,g);hint(+g.dataset.i)}else{var b2=sel;sel=null;b2.classList.remove('sel');wrong(g)}}});
 /* demo (teacherless modelling): first word flies into its bag, its icon pulses with the gesture hint */
 var first=$$('.bk',bar)[D.demo];if(first){wait(900).then(function(){first.classList.add('sel');P('tick');play(first);return wait(900)}).then(function(){var g=bags[+first.dataset.bag];sel=null;drop(first,g);hint(+g.dataset.i)})}};
/* ---- match pairs: tap a picture, tap its word ---- */
INIT.match_pairs=function(s){
 var ps=$$('.mp',s),ws=$$('.mw',s),sp=null,left=ps.length;
 ps.forEach(function(p){p.onclick=function(){ps.forEach(function(x){x.classList.remove('sel')});sp=(sp===p)?null:p;if(sp){sp.classList.add('sel');P('tick')}}});
 ws.forEach(function(w){w.onclick=function(){if(!sp){w.classList.add('pulse');setTimeout(function(){w.classList.remove('pulse')},1700);P('tick');return}
  if(sp.dataset.i===w.dataset.i){var g=$('.mg',w);g.innerHTML='<span class="chip c1 mo" style="font-size:42px;padding:2px 20px;border-radius:44px">'+(+sp.dataset.i+1)+'</span>';sp.classList.remove('sel');sp.classList.add('ok');w.classList.add('ok');sp=null;P('pop');setTimeout(function(){P('tick')},90);if(--left==0)finish(s)}else{wrong(sp);sp.classList.remove('sel');sp=null}}})};
/* ---- true or a fib: tick or cross under each sentence ---- */
INIT.spot_fib=function(s){
 var n=JSON.parse($('#d-'+s.dataset.id).textContent).n,left=n;
 $$('.tf',s).forEach(function(b){b.onclick=function(){var ok=b.dataset.v===b.dataset.ok;if(ok){$$('.tf[data-k="'+b.dataset.k+'"]',s).forEach(function(x){x.classList.add('off')});b.classList.remove('off');b.classList.add('pick');P('pop');setTimeout(function(){P('tick')},90);if(--left==0)finish(s)}else{b.classList.add('off');P('boop')}}})};
go(0);
"""

def build_interactive(spec, out, title='SkillsXLab · interactive slice'):
    secs = ''; allspec = [d for d in spec if d['m'] in BUILD]
    for n, d in enumerate(allspec):
        sid = f's{n}'; ph_ = d.get('phase'); orbs = phase_orbs(ph_) if ph_ in PAL else ''
        secs += f'<section class="sl" data-m="{d["m"]}" data-id="{sid}">{orbs}{BUILD[d["m"]](d, sid)}</section>'
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>'
            f'<style>{css("day")}{CSS_EXTRA}</style></head><body><div id="stage">{secs}</div>'
            '<div id="ctl"><button id="sf">Sound: On</button><button id="mo">Motion: On</button></div><button id="nx">→</button>'
            f'<script>{SFX_JS}</script><script>{APP_JS}</script></body></html>')
    html = inline_assets(html)
    pathlib.Path(out).write_text(html, encoding='utf-8')
    return len(html)
