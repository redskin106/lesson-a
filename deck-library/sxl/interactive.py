"""Interactive (offline, single-file) renderer. Same data dicts as the static deck.
build_interactive(spec, out_html): spec items with m in {chat, sort, timeline}. Everything is inlined (fonts, art, emoji, sounds synthesised) -> no network.
General layer = SXLSound (primer engine, copied) + Motion On/Calm/Off. Behaviour per module is in JS below."""
import re, json, base64, io, os, pathlib
from . import core as _c
from PIL import Image
from . import core
from .core import *
from .modules import chat as C
from .modules.chat import gapchip, AV

def _b64(path, kind):
    if kind == 'font': return 'data:font/woff2;base64,' + base64.b64encode(open(path, 'rb').read()).decode()
    im = Image.open(path)
    if kind == 'art':
        im = im.convert('RGB'); im.thumbnail((560, 560)); b = io.BytesIO(); im.save(b, 'JPEG', quality=64)
        return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    b = io.BytesIO(); im.thumbnail((200, 200)); im.save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()

def inline_assets(html):
    cache = {}
    def rep(m):
        u = m.group(0); p = u[len('file://'):]
        if p.endswith('.mp4'): return 'data:video/mp4;base64,' + base64.b64encode(open(p,'rb').read()).decode()
        if u not in cache:
            kind = 'font' if p.endswith('.woff2') else 'art' if '/art/' in p else 'emoji'
            cache[u] = _b64(p, kind)
        return cache[u]
    return re.sub(r'file:///[^")\'\s&]+', rep, html)

# ---------- slide builders (markup identical to static modules; behaviour via data-* hooks) ----------
def chat_markup(d, sid):
    L = d['lines']; av = d.get('avatars', {}); data = []; rows = ''
    for i, l in enumerate(L):
        s, c, bank = C.parts(l); pc = l[3] if len(l) > 3 else None
        left = s in ('N', 'D'); a = EM(av.get(s, AV[s]))
        if isinstance(c, dict):
            inner = f'<img src="{ART}{c["img"]}" style="height:150px;width:266px;border-radius:30px;background:#fff;object-fit:contain">'; gaps = []; pc = 'x' if False else pc
        elif isinstance(c, str):
            inner = f'<div style="font-family:O;font-weight:800;font-size:52px;color:#1c1b2e">{c}</div>'; gaps = []
        else:
            parts_ = []; gaps = []
            for c_, t, g in c:
                if g:
                    gaps.append([c_, t]); parts_.append(f'<span class="gp" data-c="{c_}" data-t="{t}"><span class="op">{gapchip(c_, t)}</span><span class="fl" style="display:none">{ch(c_, t, 46, "8px 26px")}</span></span>')
                else: parts_.append(ch(c_, t, 46, '8px 26px'))
            inner = '<div style="display:flex;gap:12px;align-items:center">' + ''.join(parts_) + '</div>'
        pimg = (f'<img src="{ART}{pc}" style="height:112px;width:112px;border-radius:26px;margin-left:30px;background:#fff;object-fit:contain">' if pc else '')
        bub = f'<div class="gl" style="position:static;height:{170 if isinstance(c, dict) else 130}px;border-radius:{70 if isinstance(c, dict) else 65}px;display:flex;align-items:center;padding:0 {18 if (pc or isinstance(c, dict)) else 46}px 0 {18 if isinstance(c, dict) else 46}px;{"" if left else "background:rgba(214,190,255,.75);"}">{inner}{pimg}</div>'
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

def tintch(html, word):
    i = SIDX.get(word.lower().strip('.'))
    if i is None: return html
    a, b, tc = STRENGTH[i]
    return html.replace('style="', f'style="background:linear-gradient(135deg,{a},{b});color:{tc};', 1)

def sort_markup(d, sid):
    rows = d['rows']; n = len(rows); top, bot = 168, (772 if len(d['bank']) > 8 else 812); step = (bot - top) / n; h = min(int(step - 18), 190); fs = min(64, int(h * .36)); ps = max(8, int(h * .1)); gh = int(fs * 1.3 + 2 * ps)
    out = header(d['phase'], d.get('title')); bank = d['bank']; plain = [b if isinstance(b, tuple) else ('c2', b) for b in bank if b != '|']
    for i, r in enumerate(rows):
        y = int(top + i * step); pre = r.get('pre', ('c1', 'You')) if r.get('pre', 1) else None; end = r.get('end')
        a = r.get('ans', [plain[i][1]]); a = [a] if isinstance(a, str) else a
        ph = pic(180, y, h, h, r['pic'], r=int(h * .23)); j = ph.index(' ', ph.index('<')); ph = ph[:j] + f' data-rp="{i}" class="rp"' + ph[j:] if 'class="' not in ph[:ph.index('>')] else ph.replace('class="', f'data-rp="{i}" class="rp ', 1)
        out += num(90, y + h // 2 - 32, i + 1) + ph + f'<img class="spk" data-i="{i}" src="{EM("sparkles")}" style="left:{180 + h - 80}px;top:{y - 20}px;width:120px">'
        x0 = 180 + h + 40
        def slot(k, cls, col, w):
            return (f'<span class="slot" data-i="{i}" data-t="{a[k]}"><span class="op">{gap(col, w, "…", h=gh)}</span>'
                    f'<span class="fl" style="display:none">{tintch(ch(cls, a[k], fs, f"{ps}px {int(fs * .55)}px"), a[k])}</span></span>')
        vw = max(240, int(max(len(t) for r2 in rows for t in ([r2.get('ans')] if isinstance(r2.get('ans'), str) else (r2.get('ans') or ['xxxxx']))) * fs * .56 + fs * 1.3)); slots = slot(0, 'c2', '#9a5cff', vw) + ('' if end else slot(1, 'c3', '#ff7a3c', 470))
        out += (f'<div class="gl" style="left:{x0}px;top:{y}px;width:{1830 - x0}px;height:{h}px;border-radius:{int(h * .4)}px;display:flex;align-items:center;gap:22px;padding:0 50px">'
                + (ch(pre[0], pre[1], fs, f'{ps}px {int(fs * .55)}px') if pre else '') + slots
                + (ch(end[0], end[1], fs, f'{ps}px {int(fs * .55)}px') if end else '') + '</div>')
    need = {}
    for r in rows:
        a = r.get('ans'); a = [a] if isinstance(a, str) else (a or [])
        for t in a: need[t] = need.get(t, 0) + 1
    two = len(bank) > 8; bfs = 42 if two else (44 if len(bank) > 6 else (58 if len(bank) > 4 else 64)); btn = ''
    for b in bank:
        if b == '|': btn += ('<div style="flex-basis:100%;height:0"></div>' if two else '<div style="width:6px;height:70px;border-radius:3px;background:#b9a6f5;margin:0 10px"></div>'); continue
        c, t = b if isinstance(b, tuple) else ('c2', b)
        btn += f'<button class="bk" data-t="{t}" data-n="{need.get(t, 1)}">{ch(c, t, bfs, "10px 30px" if bfs < 58 else "10px 34px")}</button>'
    out += (f'<div class="gl" style="left:90px;top:790px;width:1740px;height:198px;border-radius:64px;display:flex;flex-wrap:wrap;align-content:center;justify-content:center;gap:14px 22px;padding:0 44px" id="bk-{sid}">{btn}</div>' if two else f'<div class="gl" style="left:90px;top:830px;width:1740px;height:158px;border-radius:79px;display:flex;align-items:center;gap:22px;padding:0 44px" id="bk-{sid}">{btn}</div>')
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

def pick_markup(d, sid):
    from .modules.kit import pick_html
    return pick_html(d, True) + f'<script type="application/json" id="d-{sid}">{json.dumps({"ok": d["ok"]})}</script>'

def connect_markup(d, sid):
    from .modules.kit import connect_html
    return connect_html(d, sid)

BUILD = {'connect': connect_markup, 'pick': pick_markup, 'chat': chat_markup, 'sort': sort_markup, 'timeline': timeline_markup, 'sound_sort': sound_markup, 'match_pairs': match_markup, 'spot_fib': fib_markup}


CSS_EXTRA = """.cn{position:absolute;width:480px;height:180px;border-radius:50px;background:rgba(255,255,255,.66);border:5px solid rgba(255,255,255,.92);box-shadow:0 10px 26px rgba(60,30,140,.16);cursor:pointer;z-index:2;transition:top .7s cubic-bezier(.3,.9,.3,1),background .3s,border-color .3s,transform .2s}
.cn .tx{position:absolute;left:182px;top:0;width:286px;height:100%;display:flex;flex-wrap:wrap;gap:8px;align-items:center;opacity:0;transition:opacity .4s}
.cn.rv .tx{opacity:1}.cn.sel{border-color:#7b3cf0;transform:scale(1.04)}
.cd{fill:none;stroke-width:10;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;animation:cdr var(--du,.45s) var(--dl,.05s) ease-out forwards}@keyframes cdr{to{stroke-dashoffset:0}}
.cn.okp{animation:cok .6s}@keyframes cok{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
.cfull{transition:opacity .4s}
.pk{border:0;background:none;padding:0;cursor:pointer;transition:transform .2s,opacity .3s}.pk:hover{transform:translateY(-4px)}.pk.off{opacity:.32;transform:none}.pk.pickd{transform:scale(1.04);filter:drop-shadow(0 0 28px rgba(79,207,122,.8))}
.vplay{width:132px;height:132px;border-radius:50%;border:0;cursor:pointer;background:linear-gradient(135deg,#9a5cff,#ff4fa3);box-shadow:0 14px 28px rgba(106,53,232,.4),inset 0 2px 0 rgba(255,255,255,.5);display:flex;align-items:center;justify-content:center;padding:0 0 0 8px;margin-top:6px;transition:transform .15s}
.vplay:active{transform:scale(.92)}
#vov{position:fixed;inset:0;z-index:50;display:none;align-items:center;justify-content:center;background:rgba(28,20,70,.62);backdrop-filter:blur(8px)}
#vov.on{display:flex}
#vov video{display:none;width:min(82vw,146vh);max-height:82vh;border-radius:26px;background:#000;box-shadow:0 30px 80px rgba(0,0,0,.5)}
#vov video.on{display:block}
#vx{position:absolute;top:3vh;right:3vw;width:72px;height:72px;border-radius:50%;border:0;cursor:pointer;background:#fff;display:flex;align-items:center;justify-content:center;padding:0;box-shadow:0 8px 20px rgba(0,0,0,.3)}

html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#eeeef3;transition:background .5s}
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
#ctl{position:absolute;left:50%;transform:translateX(-50%);bottom:12px;z-index:50;display:flex;gap:14px}
#ctl button{font:700 24px Outfit,O,sans-serif;padding:4px 20px;border-radius:999px;background:rgba(255,255,255,.8);border:3px solid #fff;color:#6a35e8;box-shadow:0 8px 20px rgba(80,60,160,.15)}
#nx{position:absolute;right:90px;bottom:34px;z-index:40;width:96px;height:96px;border-radius:50%;background:linear-gradient(135deg,#9a5cff,#6a35e8);color:#fff;font:800 56px O;display:none;align-items:center;justify-content:center;box-shadow:0 20px 40px rgba(80,40,200,.4)}
#clk{position:absolute;right:150px;bottom:44px;z-index:40;font:700 26px O;color:#4a3a8a;background:rgba(255,255,255,.75);padding:6px 18px;border-radius:999px;display:none}
#rpt{position:absolute;inset:60px 200px;z-index:80;background:rgba(255,255,255,.96);border-radius:40px;padding:30px 40px;font:500 24px O;overflow:auto;display:none;box-shadow:0 30px 80px rgba(40,20,90,.35)}
#rpt table{border-collapse:collapse;width:100%}#rpt td,#rpt th{padding:4px 10px;border-bottom:1px solid #ddd;text-align:left}#rpt tr.o td{background:#f1e9ff}
.tstart{cursor:pointer}.tclock.run{animation:none}
#pv{position:absolute;left:30px;bottom:34px;z-index:40;width:64px;height:64px;border-radius:50%;background:rgba(255,255,255,.7);color:#6a35e8;font:800 36px O;display:flex;align-items:center;justify-content:center;opacity:.55}
#cnt{position:absolute;left:110px;bottom:46px;z-index:40;font:700 24px O;color:#6a6a7e}
.sl.night{background:#0b0a10;color:#f6f3ff}.night .mu{color:#a9a3cc}.night .gl,.night .tag,.night .pill{background:rgba(255,255,255,.09);border-color:rgba(255,255,255,.18)}.night .grad{background:linear-gradient(90deg,#c9a2ff,#ff8cc6);-webkit-background-clip:text;color:transparent}
.vh{opacity:0;transform:translateY(24px) scale(.97)}.vs{transition:opacity .45s,transform .5s cubic-bezier(.2,.9,.3,1.2)}.vh.vs{opacity:0}
.gl.tp{animation:pu .5s}
.sx{transition:opacity .45s,transform .5s cubic-bezier(.2,.9,.3,1.2),filter .4s}.sx.sh{opacity:0;transform:translateY(22px) scale(.96);pointer-events:none}.sx.dim{opacity:.38;filter:saturate(.5)}
.chip.pin{opacity:0;transform:scale(.4)}.chip.pp{animation:moc .5s cubic-bezier(.2,1.6,.4,1)}
.bk{touch-action:none}.bk.ghost{opacity:.3}.bk.drag{position:absolute;z-index:60;pointer-events:none;transform:scale(1.12) rotate(-3deg);filter:drop-shadow(0 18px 22px rgba(40,20,90,.35));transition:none}.bk.drag.back{transition:left .35s cubic-bezier(.3,1.4,.5,1),top .35s cubic-bezier(.3,1.4,.5,1)}
.cbt{transition:transform .25s}.cbt.sel{transform:translateY(-8px) scale(1.04);filter:drop-shadow(0 0 0 #9a5cff)}.cbt.sel>div:first-child,.cbt.sel>div:first-of-type{box-shadow:0 0 0 8px #9a5cff,0 14px 30px rgba(106,53,232,.4)}.cbp,.dpp{transition:opacity .35s}.dlr{transition:transform .25s}.dlr.sel{transform:scale(1.015)}.dpb{transition:transform .3s}.dpb.sel{transform:scale(1.18) translateY(-6px)}.dpb.sel .dpc{border-color:#9a5cff!important;box-shadow:0 0 0 6px rgba(154,92,255,.35),0 14px 30px rgba(106,53,232,.4)!important}
.gsel{position:absolute;top:70px;z-index:5;width:76px;height:76px;border-radius:50%;background:rgba(255,255,255,.7);font:800 38px O;color:#6a35e8;display:flex;align-items:center;justify-content:center;cursor:pointer}.gsel.sel{background:linear-gradient(135deg,#9a5cff,#6a35e8);color:#fff}.gslab{position:absolute;top:84px;font:700 26px O;color:#4a5a7a;letter-spacing:.12em}
.gp.hov{box-shadow:0 0 0 6px rgba(154,92,255,.6);border-radius:30px}
.gl.hov{box-shadow:0 0 0 6px rgba(154,92,255,.55),0 0 40px rgba(154,92,255,.5)}
.rp.react{animation:react .8s}@keyframes react{25%{transform:scale(1.14) rotate(-3deg)}55%{transform:scale(.97) rotate(2deg)}100%{transform:none}}
.spk{position:absolute;opacity:0;pointer-events:none;z-index:30}.spk.go{animation:spk 1.1s both}@keyframes spk{0%{opacity:0;transform:scale(.3) rotate(-20deg)}30%{opacity:1;transform:scale(1.2) rotate(10deg)}100%{opacity:0;transform:translateY(-50px) scale(1)}}
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
PHBG={ENGAGE:'linear-gradient(135deg,#ffd27a,#ff9fb8 45%,#ffb066)',STUDY:'linear-gradient(135deg,#b98cff,#8fb4ff 50%,#7fd3ff)',ACTIVATE:'linear-gradient(135deg,#9fe8c4,#7fe0d8 50%,#a8e6ff)',night:'#0b0a10'};function bgfit(){var on=document.querySelector('.sl.on');var pb=on&&PHBG[on.dataset.ph];document.body.style.background=(innerWidth/innerHeight>1920/1080+0.01&&pb)?pb:'#eeeef3'}function fit(){var s=Math.min(innerWidth/1920,innerHeight/1080);var st=$('#stage');st.style.transform='scale('+s+')';st.style.left=(innerWidth-1920*s)/2+'px';st.style.top=(innerHeight-1080*s)/2+'px';bgfit()}
addEventListener('resize',fit);fit();
var slides=$$('.sl'),cur=-1;
[$('#stage')].concat(slides).forEach(function(e){e.addEventListener('scroll',function(){if(e.id==='stage'||!e.classList.contains('thread')){e.scrollTop=0;e.scrollLeft=0}})});
function go(i){if(i<0||i>=slides.length)return;tickClk();slides.forEach(function(s){s.classList.remove('on')});cur=i;lastI=i;lastT=Date.now();upd();var s=slides[i];s.classList.add('on');bgfit();$('#nx').classList.remove('on');if(!s.__init){s.__init=1;INIT[s.dataset.m](s)}else if(s.__done)$('#nx').classList.add('on');}
var T0=Date.now(),SL=[],lastT=Date.now(),lastI=-1,showClk=false;
function fmt(s){s=Math.round(s);return Math.floor(s/60)+':'+('0'+s%60).slice(-2)}
function tickClk(){var now=Date.now();if(lastI>=0)SL[lastI]=(SL[lastI]||0)+(now-lastT)/1000;lastT=now;if(!showClk)return;var tot=SL.reduce(function(a,b){return a+(b||0)},0),plan=0,pc=0;slides.forEach(function(s,i){var m=+s.dataset.min||0;if(!s.dataset.opt)plan+=m;if(i<=cur&&!s.dataset.opt)pc+=m});$('#clk').textContent='slide '+fmt((SL[cur]||0))+'  ·  total '+fmt(tot)+' / plan '+fmt(pc*60)+' (core '+fmt(plan*60)+')'}
setInterval(tickClk,500);
$('#ck').onclick=function(){showClk=!showClk;$('#clk').style.display=showClk?'block':'none';tickClk()};
$('#rp').onclick=function(){var r=$('#rpt');if(r.style.display==='block'){r.style.display='none';return}tickClk();var h='<h2>Rehearsal report</h2><table><tr><th>#</th><th>Slide</th><th>Plan</th><th>Actual</th></tr>',tx='',tp=0,ta=0;slides.forEach(function(s,i){var m=(+s.dataset.min||0)*60,a=SL[i]||0;if(!s.dataset.opt)tp+=m;ta+=a;h+='<tr class="'+(s.dataset.opt?'o':'')+'"><td>'+(i+1)+'</td><td>'+s.dataset.label+(s.dataset.opt?' (optional)':'')+'</td><td>'+fmt(m)+'</td><td>'+fmt(a)+'</td></tr>';tx+=(i+1)+'\t'+s.dataset.label+'\t'+fmt(m)+'\t'+fmt(a)+'\n'});h+='<tr><td></td><td><b>Total</b> (plan = core only)</td><td><b>'+fmt(tp)+'</b></td><td><b>'+fmt(ta)+'</b></td></tr></table><p>Timer slides run on their own clock: skip them with the arrow when you like. Click Report again to close.</p>';r.innerHTML=h;r.style.display='block'};
function upd(){$('#cnt').textContent=(cur+1)+' / '+slides.length;$('#pv').style.display=cur>0?'flex':'none'}
$('#pv').onclick=function(){go(cur-1)};
function finish(s){s.__done=1;P('done');wait(500).then(function(){if(cur<slides.length-1)$('#nx').classList.add('on')})}
function adv(){var s=slides[cur];return !!(s&&s.__adv&&s.__adv())}
$('#nx').onclick=function(){if(adv())return;P('open');go(cur+1)};
var VOV=$('#vov');function vclose(){if(!VOV)return;VOV.classList.remove('on');$$('video',VOV).forEach(function(v){v.pause();v.classList.remove('on')})}
if(VOV){document.addEventListener('click',function(e){var b=e.target.closest('.vplay');if(b){e.stopPropagation();var v=$('#vid-'+b.dataset.v);if(!v)return;$$('video',VOV).forEach(function(x){x.classList.remove('on')});v.classList.add('on');v.currentTime=0;VOV.classList.add('on');v.play();P('pop');return}if(e.target===VOV||e.target.id==='vx')vclose()},true)}
addEventListener('keydown',function(e){if(VOV&&VOV.classList.contains('on')){if(e.key==='Escape')vclose();return}if(e.key==='ArrowRight'||e.key===' '){if(adv())return}if(e.key==='ArrowRight'&&$('#nx').classList.contains('on'))go(cur+1);if(e.key==='ArrowLeft')go(cur-1)});
var cfgs=['On','Calm','Off'],ci=0;
$('#mo').onclick=function(){ci=(ci+1)%3;SXL.cfg.calm=ci==1;SXL.cfg.off=ci==2;document.body.className=['','calm','off'][ci];this.textContent='Motion: '+cfgs[ci]};
$('#sf').onclick=function(){var on=SXLSound.toggle();this.textContent='Sound: '+(on?'On':'Off')};
function wrong(el){P('boop');el.classList.remove('shake');void el.offsetWidth;el.classList.add('shake')}
function put(slotEl){$('.op',slotEl).style.display='none';var f=$('.fl',slotEl);f.style.display='inline-block';f.classList.add('mo');P('pop');setTimeout(function(){P('tick')},90)}
var INIT={};
/* ---- chat: tap-to-fill, auto-scroll, free scroll-back ---- */
INIT.chat=function(s){
 var id=s.dataset.id,D=JSON.parse($('#d-'+id).textContent),th=$('#th-'+id),bar=$('#bk-'+id),rows=$$('.row',th),i=-1;
 function next(){i++;if(i>=D.n){finish(s);return}var r=rows[i];r.classList.add('show');if(i>0)P('arrive');var need=r.offsetTop+r.offsetHeight+16-th.clientHeight;if(need>th.scrollTop+2)th.scrollTo({top:need,behavior:SXL.cfg.off?'auto':'smooth'});
  if(D.gapn[i]){bar.innerHTML=D.banks[i];bar.style.visibility='visible';bar.__r=r}else{bar.style.visibility='hidden';wait(1100).then(next)}}
 bar.onclick=function(e){var b=e.target.closest('.bk');if(!b||!bar.__r)return;var g=$$('.gp',bar.__r).filter(function(x){return !x.__f})[0];if(!g)return;
  if(b.dataset.t===g.dataset.t&&b.dataset.c===g.dataset.c){g.__f=1;put(g);b.classList.add('used');if(!$$('.gp',bar.__r).some(function(x){return !x.__f})){bar.__r=null;wait(900).then(next)}}else wrong(b)};
 /* drag and react (tap still works) */
 var dragged=false;
 function gapsOf(r){return r?$$('.gp',r).filter(function(x){return !x.__f}):[]}
 function nearest(cx,list){var best=null,bd=1e9;list.forEach(function(x){var r=x.getBoundingClientRect(),d=Math.abs(cx-(r.left+r.width/2));if(d<bd){bd=d;best=x}});return best}
 var oc=bar.onclick;bar.onclick=function(e){if(dragged){dragged=false;return}oc(e)};
 bar.addEventListener('pointerdown',function(e){var b=e.target.closest('.bk');if(!b||b.classList.contains('used')||!bar.__r||e.button>0)return;var x0=e.clientX,y0=e.clientY,clone=null,hov=null,k=s.getBoundingClientRect().width/1920;
  function tgt(cx,cy){var el=document.elementFromPoint(cx,cy),row=el&&el.closest('.row');if(row!==bar.__r)return null;return nearest(cx,gapsOf(row))}
  function mv(ev){var dx=ev.clientX-x0,dy=ev.clientY-y0;if(!clone){if(dx*dx+dy*dy<64)return;clone=b.cloneNode(true);clone.classList.add('drag');b.classList.add('ghost');s.appendChild(clone);P('pop')}
   var r=s.getBoundingClientRect();clone.style.left=((ev.clientX-r.left)/k-clone.offsetWidth/2)+'px';clone.style.top=((ev.clientY-r.top)/k-clone.offsetHeight/2)+'px';
   var t=tgt(ev.clientX,ev.clientY);if(hov&&hov!==t){hov.classList.remove('hov');hov=null}if(t&&t!==hov){t.classList.add('hov');hov=t}}
  function up(ev){document.removeEventListener('pointermove',mv);document.removeEventListener('pointerup',up);if(!clone)return;dragged=true;setTimeout(function(){dragged=false},60);if(hov){hov.classList.remove('hov');hov=null}b.classList.remove('ghost');
   var t=tgt(ev.clientX,ev.clientY),row=bar.__r;
   if(t&&b.dataset.t===t.dataset.t&&b.dataset.c===t.dataset.c){clone.remove();t.__f=1;put(t);b.classList.add('used');if(!gapsOf(row).length){bar.__r=null;wait(900).then(next)}}
   else{if(t)wrong(t);else P('tick');var r=b.getBoundingClientRect(),sr=s.getBoundingClientRect();clone.classList.add('back');clone.style.left=((r.left-sr.left)/k)+'px';clone.style.top=((r.top-sr.top)/k)+'px';var c=clone;setTimeout(function(){c.remove()},380)}}
  document.addEventListener('pointermove',mv);document.addEventListener('pointerup',up)});
 next();};
/* ---- sort: tap a word, tap its picture row ---- */
INIT.sort=function(s){
 var id=s.dataset.id,bar=$('#bk-'+id),slots=$$('.slot',s),sel=null,left=slots.length,dragged=false;
 function pick(b){$$('.bk',bar).forEach(function(x){x.classList.remove('sel')});sel=b;if(b){b.classList.add('sel');P('tick')}}
 function use(b){b.__n=(b.__n==null?+(b.dataset.n||1):b.__n)-1;if(b.__n<=0)b.classList.add('used')}
 function react(i){var p=$('[data-rp="'+i+'"]',s),k=$('.spk[data-i="'+i+'"]',s);if(p){p.classList.remove('react');void p.offsetWidth;p.classList.add('react')}if(k){k.classList.remove('go');void k.offsetWidth;k.classList.add('go')}}
 function ok(sl,b){sl.__f=1;put(sl);use(b);react(sl.dataset.i);if(--left==0)finish(s)}
 bar.onclick=function(e){if(dragged){dragged=false;return}var b=e.target.closest('.bk');if(b&&!b.classList.contains('used'))pick(sel===b?null:b)};
 slots.forEach(function(sl){sl.onclick=function(){if(sl.__f)return;if(!sel){sl.classList.add('pulse');setTimeout(function(){sl.classList.remove('pulse')},1700);P('tick');return}
  if(sel.dataset.t===sl.dataset.t){var b=sel;b.classList.remove('sel');sel=null;ok(sl,b)}else{var b2=sel;wrong(sl);b2.classList.remove('sel');sel=null}}});
 /* drag and react */
 function sc(){return s.getBoundingClientRect().width/1920}
 function target(cx,cy){var el=document.elementFromPoint(cx,cy),row=el&&el.closest('.gl');if(!row||!row.querySelector('.slot'))return null;var fr=$$('.slot',row).filter(function(x){return !x.__f});if(!fr.length)return {row:row,slot:null};var best=null,bd=1e9;fr.forEach(function(x){var r=x.getBoundingClientRect(),d=Math.abs(cx-(r.left+r.width/2));if(d<bd){bd=d;best=x}});return {row:row,slot:best}}
 bar.addEventListener('pointerdown',function(e){var b=e.target.closest('.bk');if(!b||b.classList.contains('used')||e.button>0)return;var x0=e.clientX,y0=e.clientY,clone=null,hov=null,k=sc();
  function mv(ev){var dx=ev.clientX-x0,dy=ev.clientY-y0;if(!clone){if(dx*dx+dy*dy<64)return;pick(null);clone=b.cloneNode(true);clone.classList.add('drag');b.classList.add('ghost');s.appendChild(clone);P('pop')}
   var r=s.getBoundingClientRect();clone.style.left=((ev.clientX-r.left)/k-clone.offsetWidth/2)+'px';clone.style.top=((ev.clientY-r.top)/k-clone.offsetHeight/2)+'px';
   var t=target(ev.clientX,ev.clientY);if(hov&&(!t||t.row!==hov)){hov.classList.remove('hov');hov=null}if(t&&t.slot&&t.row!==hov){t.row.classList.add('hov');hov=t.row}}
  function up(ev){document.removeEventListener('pointermove',mv);document.removeEventListener('pointerup',up);if(!clone)return;dragged=true;setTimeout(function(){dragged=false},60);if(hov){hov.classList.remove('hov');hov=null}b.classList.remove('ghost');
   var t=target(ev.clientX,ev.clientY);
   if(t&&t.slot&&t.slot.dataset.t===b.dataset.t){clone.remove();ok(t.slot,b)}
   else{if(t&&t.row){wrong(t.row)}else P('tick');var r=b.getBoundingClientRect(),sr=s.getBoundingClientRect();clone.classList.add('back');clone.style.left=((r.left-sr.left)/k)+'px';clone.style.top=((r.top-sr.top)/k)+'px';var c=clone;setTimeout(function(){c.remove()},380)}}
  document.addEventListener('pointermove',mv);document.addEventListener('pointerup',up)});};
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
INIT.connect=function(s){
 var D=JSON.parse($('#d-'+s.dataset.id).textContent),ts=$$('.cn',s),svg=$('#ag-'+s.dataset.id),full=$('#cf-'+s.dataset.id),NS='http://www.w3.org/2000/svg',sid=s.dataset.id;
 var pos=[[],[],[]],els={},rowOf={},nextRow=0,linked={},sel=null,done=0;
 ts.forEach(function(e){var c=+e.dataset.c,id=+e.dataset.id,sl=Math.round((parseInt(e.style.top)-D.top)/D.row);pos[c][sl]=id;els[c+'_'+id]=e;e.onclick=function(){tap(e)}});
 function place(c,id,r){var cur=pos[c].indexOf(id),o=pos[c][r];if(cur===r)return;pos[c][r]=id;pos[c][cur]=o;els[c+'_'+id].style.top=(D.top+r*D.row)+'px';els[c+'_'+o].style.top=(D.top+cur*D.row)+'px'}
 function stroke(d,w,col,g,dl,du){var p=document.createElementNS(NS,'path');p.setAttribute('class','cd');p.setAttribute('pathLength','1');p.setAttribute('stroke',col);p.setAttribute('stroke-width',w);p.style.setProperty('--dl',dl+'s');p.style.setProperty('--du',du+'s');p.dataset.g=g;p.setAttribute('d',d);svg.appendChild(p)}
 function arrow(id,r,a,b){var y=D.top+r*D.row+D.h/2,x1=D.x[a]+D.w+12,x2=D.x[b]-16,col=D.col[id%4],m=(x1+x2)/2,st=0;
  if(st===0){/* marker: wobbly straight line, then two short head strokes */
   stroke('M'+x1+' '+(y+3)+'Q'+m+' '+(y-6)+' '+x2+' '+y,9,col,id,.05,.42);
   stroke('M'+(x2-34)+' '+(y-26)+'L'+x2+' '+y,9,col,id,.47,.14);stroke('M'+(x2-34)+' '+(y+26)+'L'+x2+' '+y,9,col,id,.58,.14)}
  else{/* brush: curved thick stroke, then a loose chevron head */
   var cy=(a===0&&b===2)?60:46;
   stroke('M'+x1+' '+(y+12)+'C'+(x1+40)+' '+(y-cy)+' '+(x2-50)+' '+(y+cy)+' '+x2+' '+(y-4),14,col,id,.05,.5);
   stroke('M'+(x2-38)+' '+(y-34)+'Q'+(x2-16)+' '+(y-16)+' '+x2+' '+(y-4),13,col,id,.53,.14);stroke('M'+(x2-34)+' '+(y+30)+'Q'+(x2-14)+' '+(y+12)+' '+x2+' '+(y-4),13,col,id,.64,.14)}}
 function tap(e){var c=+e.dataset.c,id=+e.dataset.id;e.classList.add('rv');
  if(!sel){sel=e;e.classList.add('sel');P('tick');return}
  if(sel===e){e.classList.remove('sel');sel=null;return}
  if(+sel.dataset.c===c){sel.classList.remove('sel');sel=e;e.classList.add('sel');P('tick');return}
  var a=sel;sel=null;a.classList.remove('sel');
  if(+a.dataset.id===id){link(a,e)}else{wrong(a);wrong(e)}}
 function link(a,b){var id=+a.dataset.id;if(rowOf[id]===undefined)rowOf[id]=nextRow++;var r=rowOf[id];linked[id]=linked[id]||{};var before=Object.keys(linked[id]).length;linked[id][a.dataset.c]=1;linked[id][b.dataset.c]=1;
  if(Object.keys(linked[id]).length===before)return;
  for(var c in linked[id]){place(+c,id,r);var m=els[c+'_'+id];m.classList.add('rv');m.style.background=D.col[id%4]+'30';m.style.borderColor=D.col[id%4];m.classList.remove('okp');void m.offsetWidth;m.classList.add('okp')}
  P('pop');setTimeout(function(){P('tick')},90);
  $$('path',svg).forEach(function(p){if(+p.dataset.g===id)p.remove()});var L=linked[id];
  if(L[0]&&L[1])arrow(id,r,0,1);if(L[1]&&L[2])arrow(id,r,1,2);if(L[0]&&L[2]&&!L[1])arrow(id,r,0,2);
  if(L[0]&&L[1]&&L[2]){done++;var fl=$('.fl[data-id="'+id+'"]',full);fl.style.opacity=1;$$('.chip',fl).forEach(function(c){c.classList.add('mo')});full.style.opacity=1;P('good');if(done===D.n)finish(s)}}
};
INIT.pick=function(s){
 var ok=JSON.parse($('#d-'+s.dataset.id).textContent).ok,bs=$$('.pk',s),done=0;
 bs.forEach(function(b){b.onclick=function(){if(done)return;if(+b.dataset.i===ok){done=1;bs.forEach(function(x){if(x!==b)x.classList.add('off')});b.classList.add('ok','pickd');var sy=$('.psay',s);if(sy)sy.style.opacity=1;P('pop');setTimeout(function(){P('tick')},90);finish(s)}else{b.classList.add('off');wrong(b)}}})};
/* ---- true or a fib: tick or cross under each sentence ---- */
INIT.spot_fib=function(s){
 var n=JSON.parse($('#d-'+s.dataset.id).textContent).n,left=n;
 $$('.tf',s).forEach(function(b){b.onclick=function(){var ok=b.dataset.v===b.dataset.ok;if(ok){$$('.tf[data-k="'+b.dataset.k+'"]',s).forEach(function(x){x.classList.add('off')});b.classList.remove('off');b.classList.add('pick');P('pop');setTimeout(function(){P('tick')},90);if(--left==0)finish(s)}else{b.classList.add('off');P('boop')}}})};

/* ---- view slides: everything arrives one piece at a time; tap a piece to make it bounce; slot machine spins; dial stops are tappable ---- */
INIT.view=function(s){
 $$('.dlr',s).forEach(function(t){t.onclick=function(){$('.dlm',s).style.top=(+t.dataset.y-8)+'px';$$('.dlr',s).forEach(function(x){x.classList.remove('sel')});t.classList.add('sel');$$('.dpp',s).forEach(function(p){p.style.opacity=(p.dataset.i===t.dataset.i)?1:0});P('pop');setTimeout(function(){P('tick')},250)}});
 $$('.dpb',s).forEach(function(t){t.onclick=function(){$$('.dpb',s).forEach(function(x){x.classList.remove('sel')});t.classList.add('sel');$('.dpn',s).style.transform='rotate('+(90-(+t.dataset.a))+'deg)';$$('.dpp',s).forEach(function(p){p.style.opacity=(p.dataset.i===t.dataset.i)?1:0});P('pop');setTimeout(function(){P('tick')},250)}});
 $$('.cbt',s).forEach(function(t){t.onclick=function(){$$('.cbt',s).forEach(function(x){x.classList.remove('sel')});t.classList.add('sel');$$('.cbp',s).forEach(function(p){p.style.opacity=(p.dataset.i===t.dataset.i)?1:0});P('pop');var p=$('.cbp[data-i="'+t.dataset.i+'"] .chip',s);if(p){p.classList.remove('pp');void p.offsetWidth;p.classList.add('pp')}}});
 var stp=$$('[data-s]',s);
 if(stp.length){stp.forEach(function(e){e.classList.add('sx','sh');if(e.dataset.pills)$$('.chip',e).forEach(function(c){c.classList.add('pin')})});
  var mx=Math.max.apply(null,stp.map(function(e){return +e.dataset.s})),ix=1;
  s.__adv=function(){if(ix>mx)return false;var g=0;stp.forEach(function(e){if(+e.dataset.s===ix){e.classList.remove('sh');g=Math.max(g,+(e.dataset.g||0));if(e.dataset.pills){var cs=$$('.chip',e);cs.forEach(function(c,j){setTimeout(function(){c.classList.remove('pin');c.classList.add('pp');P(j%2?'tick':'pop')},260*j+150)})}}});
   if(ix===mx){stp.forEach(function(e){e.classList.remove('dim')})}else if(g){stp.forEach(function(e){if(e.dataset.g&&+e.dataset.g<g)e.classList.add('dim')})}
   if(ix===1)P('open');else if(!stp.some(function(e){return +e.dataset.s===ix&&e.dataset.pills}))P('pop');ix++;if(ix>mx)P('good');return true};
  s.addEventListener('click',function(e){if(e.target.closest('.tstart,.spinbtn,.dstop,.vplay'))return;s.__adv()});}
 var kids=$$(':scope > *',s).filter(function(e){return !e.hasAttribute('data-s')&&!e.classList.contains('orb')&&!e.querySelector('.tag')&&!e.classList.contains('tag')&&e.tagName!=='SCRIPT'});
 var skip=false;kids.forEach(function(k){k.classList.add('vh')});
 var i=0;function step(){if(i>=kids.length){s.__done=1;wait(300).then(function(){if(cur<slides.length-1)$('#nx').classList.add('on')});return}
  var k=kids[i++];k.classList.add('vs');k.classList.remove('vh');if(i%2==1&&i<9)P('tick');var d=kids.length>14?70:150;(skip||SXL.cfg.off?Promise.resolve():wait(d)).then(step)}
 s.addEventListener('click',function(){skip=true},{once:true});
 P('open');wait(250).then(step);
 s.addEventListener('click',function(e){var g=e.target.closest('.gl');if(g&&!g.closest('.bagx')){g.classList.remove('tp');void g.offsetWidth;g.classList.add('tp');P('tick')}});
 var nr=$$('.sr',s).length;if(nr){var lb=document.createElement('div');lb.className='gslab';lb.style.left='640px';lb.textContent='GROUPS';s.appendChild(lb);for(var q=2;q<=nr;q++){var gb=document.createElement('div');gb.className='gsel'+(q===nr?' sel':'');gb.dataset.n=q;gb.textContent=q;gb.style.left=(790+(q-2)*96)+'px';s.appendChild(gb)}}
 var gs=$$('.gsel',s);gs.forEach(function(g){g.onclick=function(e){e.stopPropagation();var n=+g.dataset.n;gs.forEach(function(x){x.classList.toggle('sel',x===g)});$$('.sr',s).forEach(function(r){r.style.display=(+r.dataset.k<n)?'flex':'none'});P('tick')}});
 var sp=$('.spinbtn',s);if(sp){sp.style.cursor='pointer';sp.onclick=function(){if(sp.__d)return;sp.__d=1;var n=0,iv=setInterval(function(){P('tick');if(++n>8){clearInterval(iv);$$('.reelp,.reelc',s).forEach(function(r){if(r.dataset.real)r.innerHTML=r.dataset.real});$$('img',s).forEach(function(im){if(im.style.filter&&im.style.filter.indexOf('blur')>-1){im.style.filter='none';im.style.opacity=1;im.style.transform='none'}});P('good')}},110)}}
 var ts=$('.tstart',s);if(ts){var tc=$('.tclock',s),left=+tc.dataset.sec,iv2=null;ts.onclick=function(){if(iv2){clearInterval(iv2);iv2=null;return}P('tick');iv2=setInterval(function(){left--;tc.innerHTML='<span class="grad">'+Math.floor(left/60)+':'+('0'+left%60).slice(-2)+'</span>';if(left<=0){clearInterval(iv2);iv2=null;P('done');tc.classList.add('tp')}},1000)}}
 $$('.dstop',s).forEach(function(d){d.style.cursor='pointer';d.onclick=function(e){e.stopPropagation();d.classList.remove('tp');void d.offsetWidth;d.classList.add('tp');P('pop')}});
};
go(0);
"""

def vov_markup(spec):
    import json as _j
    keys=sorted({c['video'] for d in spec for c in d.get('cards',[]) if c.get('video')})
    if not keys: return ''
    return '<div id="vov">'+''.join(f'<video id="vid-{k}" playsinline controls preload="none" src="file:///home/claude/work/lesson/media/{k}.mp4"></video>' for k in keys)+'<button id="vx" aria-label="Close"><svg width="30" height="30" viewBox="0 0 30 30"><path d="M6 6L24 24M24 6L6 24" stroke="#6a35e8" stroke-width="5" stroke-linecap="round"/></svg></button></div>'

def build_interactive(spec, out, title='SkillsXLab · interactive slice'):
    secs = ''; allspec = list(spec)
    for n, d in enumerate(allspec):
        sid = f's{n}'; ph_ = d.get('phase'); night = d.get('mode') == 'night'; orbs = phase_orbs(ph_) if ph_ in PAL and not night else ''
        if d['m'] in BUILD: m = d['m']; body = BUILD[m](d, sid)
        else: m = 'view'; body = core.MODULES[d['m']](d)
        secs += f'<section class="sl{" night" if night else ""}" data-ph="{"night" if night else (ph_ or "")}" data-m="{m}" data-id="{sid}" data-mod="{d["m"]}" data-min="{d.get("min",0)}" data-label="{d.get("label",d.get("title") or d["m"])}"{" data-opt=1" if d.get("optional") else ""}>{orbs}{body}</section>'
    html = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>'
            f'<style>{css("day")}{CSS_EXTRA}</style></head><body><div id="stage">{secs}</div>'
            '<div id="ctl"><button id="sf">Sound: On</button><button id="ck">Clock</button><button id="rp">Report</button><button id="mo">Motion: On</button></div><button id="pv"><svg width="30" height="30" viewBox="0 0 44 44"><path d="M36 22H10M20 11L9 22L20 33" fill="none" stroke="#6a35e8" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg></button><button id="nx"><svg width="44" height="44" viewBox="0 0 44 44"><path d="M8 22H34M24 11L35 22L24 33" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg></button><div id="cnt"></div><div id="clk"></div><div id="rpt"></div>'
            +vov_markup(spec)
            +f'<script>{SFX_JS}</script><script>{APP_JS}</script></body></html>')
    html = inline_assets(html)
    pathlib.Path(out).write_text(html, encoding='utf-8')
    return len(html)
