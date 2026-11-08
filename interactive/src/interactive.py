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
    out = header(d['phase'], d.get('title')); ans = d['bank']
    for i, r in enumerate(rows):
        y = int(top + i * step); pre = r.get('pre', ('c1', 'You')) if r.get('pre', 1) else None; end = r['end']
        out += num(90, y + h // 2 - 32, i + 1) + pic(180, y, h, h, r['pic'], r=int(h * .23))
        x0 = 180 + h + 40
        slot = (f'<span class="slot" data-i="{i}" data-t="{ans[i]}"><span class="op">{gap("#9a5cff", 420, "…", h=int(fs * 1.45))}</span>'
                f'<span class="fl" style="display:none">{ch("c2", ans[i], fs, f"{ps}px {int(fs * .55)}px")}</span></span>')
        out += (f'<div class="gl" style="left:{x0}px;top:{y}px;width:{1830 - x0}px;height:{h}px;border-radius:{int(h * .4)}px;display:flex;align-items:center;gap:22px;padding:0 50px">'
                + (ch(pre[0], pre[1], fs, f'{ps}px {int(fs * .55)}px') if pre else '') + slot + ch(end[0], end[1], fs, f'{ps}px {int(fs * .55)}px') + '</div>')
    bfs = 52 if len(d['bank']) > 4 else 56
    out += ('<div class="gl" style="left:90px;top:840px;width:1740px;height:148px;border-radius:72px;display:flex;align-items:center;gap:20px;padding:0 44px" id="bk-' + sid + '">'
            + ''.join(f'<button class="bk" data-t="{t}">{ch("c2", t, bfs, "8px 30px")}</button>' for t in d['bank']) + '</div>')
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

BUILD = {'chat': chat_markup, 'sort': sort_markup, 'timeline': timeline_markup}

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
  if(sel.dataset.t===sl.dataset.t){sl.__f=1;put(sl);sel.classList.remove('sel');sel.classList.add('used');sel=null;if(--left==0)finish(s)}else{var b=sel;wrong(sl);b.classList.remove('sel');sel=null}}});};
/* ---- timeline: tap the card that happened next ---- */
INIT.timeline=function(s){
 var cards=$$('.card',s),slots=$$('.slotn',s),k=0;
 cards.forEach(function(c){c.onclick=function(){if(+c.dataset.idx===k){var sl=slots[k];c.style.left=sl.style.left;c.style.top=sl.style.top;c.style.transform='rotate(0deg)';c.classList.add('done');sl.style.opacity=.0;P('pop');setTimeout(function(){P('tick')},120);k++;if(k==cards.length)finish(s)}else wrong(c)}});};
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
