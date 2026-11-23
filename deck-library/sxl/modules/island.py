"""Lesson 6 modules (desert island). Art slots take emoji until real art arrives.
  item_pick(items[(emoji,name)], rounds[(label,cap,ban)], sec)   Activate 1: pairs choose items, teacher switches the round
  next_event(first, mids, last, rounds, sec)                    Activate 2: What next? card, then Huddle > Answers > Vote
  rule(tag, formula, why, eg)                                   'The rule' slide: formula in colour, why we use it, full examples with pictures
Chrome comes from heist.install_chrome(); a slide carrying clock=/gear= keys also takes cicon= and gset= (see heist.chrome)."""
import json, html as _h
from ..core import *
from .. import core
from .heist import TEAMC

NOFIT='<i class="nofit" style="display:none"></i>'


@module('item_pick')
def item_pick(d):
    """items = 15 x (emoji,name); rounds = [(label,cap,ban_index_or_-1)]; sec = pair-work timer; star = index of the absurd item.
    Tap a tile = a pair's pick (up to the round's cap). Teacher taps a round pill: 1 choose three, 2 no phone (the phone greys out), 3 keep one."""
    o=header(d['phase'],d.get('role','What would you bring?'),'amber')+NOFIT
    o+=stp(glass(90,185,560,470,'<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px"><div style="font-size:210px;line-height:1">🏝️</div>'
        '<div style="font-size:110px;line-height:1">🎒 ❓</div>'
        f'<div class="ipc" style="font-family:O;font-weight:800;font-size:60px;color:#6a35e8">0 / {d["rounds"][0][1]}</div></div>',r=60),1)
    I=d['items']; w=216; h=206; g=15
    for i,(e,n) in enumerate(I):
        x=690+(i%5)*(w+g); y=185+(i//5)*(h+g)
        star='<span style="position:absolute;right:14px;top:8px;font-size:40px">⭐</span>' if d.get('star')==i else ''
        o+=stp(f'<div class="gl ipk" data-i="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:44px;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px">{star}<span style="font-size:108px;line-height:1.05">{e}</span><span style="font-family:O;font-weight:800;font-size:28px;color:#1c1b2e;white-space:nowrap">{n}</span></div>',2)
    sec=int(d.get('sec',240))
    o+=stp(f'<div class="a tclock" data-sec="{sec}" style="left:90px;top:690px;width:400px;text-align:center;font-family:O;font-weight:800;font-size:120px;line-height:1"><span class="grad">{sec//60}:{sec%60:02d}</span></div>',3)
    o+=stp(f'<div class="a tstart" style="left:510px;top:702px;width:140px;height:100px;border-radius:50px;display:flex;align-items:center;justify-content:center;{GR}"><svg width="46" height="46" viewBox="0 0 56 56"><path d="M16 8 L48 28 L16 48 Z" fill="#fff"/></svg></div>',3)
    rp=''.join(f'<div class="ipr{" on" if k==0 else ""}" data-cap="{cap}" data-ban="{ban}" style="display:flex;align-items:center;gap:14px;padding:8px 34px;border-radius:999px;background:rgba(255,255,255,.8);border:4px solid #fff;font-family:O;font-weight:800;font-size:40px;color:#1c1b2e;cursor:pointer;box-shadow:0 8px 18px rgba(80,60,160,.14)"><span style="color:#6a35e8">{k+1}</span>{t}</div>' for k,(t,cap,ban) in enumerate(d['rounds']))
    o+=stp(f'<div class="a" style="left:690px;top:870px;width:1140px;display:flex;gap:18px;justify-content:center">{rp}</div>',4)
    return o


@module('next_event')
def next_event(d):
    """first/last = (emoji,text,kind); mids = [(emoji,text,kind)] (kind: bad | good); rounds = how many mids are drawn (shuffled on load).
    One button walks the round: What next? (card) > Huddle (45 s timer starts) > Answers (2-3 teams, team dots) > Vote (hands) > What next?"""
    o=header(d['phase'],d.get('role','What next?'),'rose')+NOFIT
    data=dict(first=d['first'],mids=d['mids'],last=d['last'],rounds=d.get('rounds',3))
    o+=f'<script type="application/json" class="nxd">{_h.escape(json.dumps(data),False)}</script>'
    o+=('<div class="gl" style="left:90px;top:180px;width:1740px;height:110px;border-radius:55px"></div>'
        '<div class="a" style="left:150px;top:218px;font-size:58px;line-height:1">🏝️</div>'
        '<div class="a" style="left:1700px;top:218px;font-size:58px;line-height:1">⛵</div>'
        '<div class="a" style="left:260px;top:232px;width:1400px;height:12px;border-radius:6px;background:linear-gradient(90deg,#ffd166,#ff9f1c 55%,#d62f48)"></div>'
        '<div class="a nxsun" style="left:240px;top:196px;font-size:88px;line-height:1;transition:left .9s ease">☀️</div>')
    o+=('<div class="gl nxcard" style="left:90px;top:320px;width:820px;height:490px;border-radius:64px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:0 30px;box-sizing:border-box">'
        '<span class="nxk" style="position:absolute;right:34px;top:22px;font-size:70px"></span>'
        '<span class="nxe" style="display:block;height:250px;font-size:200px;line-height:250px">🌴</span>'
        '<span class="nxt" style="font-family:O;font-weight:800;font-size:56px;text-align:center;line-height:1.1;color:#1c1b2e">Press What next?</span></div>')
    sec=int(d.get('sec',45))
    def stepbox(y,h,n,e,inner,cls):
        return (f'<div class="gl nxs {cls}" style="left:950px;top:{y}px;width:880px;height:{h}px;border-radius:50px">'
                f'<span style="position:absolute;left:26px;top:{h//2-45}px;width:90px;height:90px;border-radius:50%;{GR};display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:52px">{n}</span>'
                f'<span style="position:absolute;left:136px;top:{h//2-42}px;font-size:84px;line-height:1">{e}</span>{inner}</div>')
    tm=(f'<div class="a tclock" data-sec="{sec}" style="left:270px;top:22px;width:330px;text-align:center;font-family:O;font-weight:800;font-size:120px;line-height:1"><span class="grad">0:{sec:02d}</span></div>'
        f'<div class="a tstart" style="left:650px;top:34px;width:140px;height:100px;border-radius:50px;display:flex;align-items:center;justify-content:center;{GR}"><svg width="46" height="46" viewBox="0 0 56 56"><path d="M16 8 L48 28 L16 48 Z" fill="#fff"/></svg></div>')
    o+=stepbox(320,160,1,'🗣️',tm,'sA')
    fr=ch('c4','If we had …,',30,'4px 14px')+ch('c1','we would …',30,'4px 14px')+ch('c2','because …',30,'4px 14px')
    dots=''.join(f'<span class="nxd1" style="width:76px;height:76px;border-radius:50%;background:{TEAMC[k]};opacity:.3;display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:42px;color:#fff;cursor:pointer;user-select:none">{k+1}</span>' for k in range(4))
    o+=stepbox(500,190,2,'🎤',f'<div class="a" style="left:250px;top:20px;width:620px;display:flex;gap:8px;flex-wrap:nowrap">{fr}</div><div class="a" style="left:250px;top:96px;width:620px;display:flex;gap:16px;align-items:center">{dots}<span style="font-family:O;font-weight:800;font-size:30px;color:#4a3a8a;margin-left:10px">2–3 teams</span></div>','sB')
    o+=stepbox(710,100,3,'✋','<div class="a" style="left:250px;top:26px;font-family:O;font-weight:800;font-size:42px;color:#1c1b2e">Which idea helps most?</div>','sC')
    o+=('<div class="a nxbtn" style="left:90px;top:850px;width:820px;height:120px;border-radius:60px;display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:60px;cursor:pointer;user-select:none;'+GR+'">What next? ▶</div>'
        '<div class="a nxbk" style="left:950px;top:865px;width:130px;height:90px;border-radius:45px;display:flex;align-items:center;justify-content:center;font-size:48px;cursor:pointer;background:rgba(255,255,255,.85);border:4px solid #fff;color:#6a35e8;user-select:none">◀</div>'
        '<div class="a nxpos" style="left:1110px;top:880px;font-family:O;font-weight:800;font-size:40px;color:#4a3a8a">0 / 0</div>')
    return o


@module('rule')
def rule(d):
    """'The rule' slide. tag=(emoji,text,'real'|'imag'), formula=[(chip class,text)], why=[(emoji,text)] (2-3), eg=[(emoji,[(chip class,text)] or text)] (1-2 full examples),
    pic = big emoji on the right. Steps: formula, why lines one by one, then the example(s)."""
    o=header(d['phase'],d.get('role','The rule'),'violet')+NOFIT
    te,tt,kind=d['tag']
    tc={'real':'linear-gradient(135deg,#ffe29a,#ffb347)','imag':'linear-gradient(135deg,#d6c7ff,#a9c7ff)'}[kind]
    o+=stp(f'<div class="a" style="left:90px;top:170px;height:70px;padding:0 34px;border-radius:999px;background:{tc};display:flex;align-items:center;gap:14px;font-family:O;font-weight:800;font-size:38px;color:#1c1b2e"><span style="font-size:46px;line-height:1">{te}</span>{tt}</div>',1)
    o+=stp(glass(90,255,1740,150,f'<div style="height:100%;display:flex;align-items:center;justify-content:center;gap:14px">{"".join(ch(c,t,56,"8px 30px") for c,t in d["formula"])}</div>',r=64),1,pills=True)
    W=d['why']; n=len(W); E=d['eg']; ne=len(E); exh=110 if ne>1 else 130
    avail=555-ne*(exh+14)-14; rh=min(150,int((avail-16*(n-1))/n))
    for i,(e,t) in enumerate(W):
        o+=stp(glass(90,430+i*(rh+16),1060,rh,f'<div style="height:100%;display:flex;align-items:center;gap:24px;padding:0 34px;box-sizing:border-box"><span style="font-size:{min(78,rh-40)}px;line-height:1;flex:none">{e}</span><span style="font-family:O;font-weight:800;font-size:36px;line-height:1.18;color:#1c1b2e">{t}</span></div>',r=48),2+i)
    pic=d.get('pic','')
    o+=stp(glass(1190,430,640,n*(rh+16)-16,f'<div style="height:100%;display:flex;align-items:center;justify-content:center;font-size:{190 if len(pic)<=3 else 120}px;line-height:1">{pic}</div>',r=64),2)
    ey=430+n*(rh+16)+14
    for k,(e,s_) in enumerate(E):
        body=(''.join(ch(c,t,38,"4px 14px") for c,t in s_) if isinstance(s_,(list,tuple)) else f'<span style="font-family:O;font-weight:800;font-size:40px;line-height:1.15;color:#1c1b2e">{s_}</span>')
        o+=stp(f'<div class="gl" style="left:90px;top:{ey+k*(exh+14)}px;width:1740px;height:{exh}px;border-radius:52px;display:flex;align-items:center;gap:22px;padding:0 34px;box-sizing:border-box;background:linear-gradient(135deg,#d6fbea,#c4f3e6)"><span style="font-size:64px;line-height:1;flex:none">{e}</span><div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">{body}</div></div>',2+n)
    return o


TIMER=lambda sec,x,y,st:(stp(f'<div class="a tclock" data-sec="{sec}" style="left:{x}px;top:{y}px;width:400px;text-align:center;font-family:O;font-weight:800;font-size:100px;line-height:1"><span class="grad">{sec//60}:{sec%60:02d}</span></div>',st)
    +stp(f'<div class="a tstart" style="left:{x+420}px;top:{y+6}px;width:130px;height:96px;border-radius:48px;display:flex;align-items:center;justify-content:center;{GR}"><svg width="44" height="44" viewBox="0 0 56 56"><path d="M16 8 L48 28 L16 48 Z" fill="#fff"/></svg></div>',st))
CHIP='display:flex;align-items:center;gap:14px;padding:10px 30px;border-radius:999px;background:rgba(255,255,255,.88);border:4px solid #fff;font-family:O;font-weight:800;font-size:38px;white-space:nowrap;color:#1c1b2e;box-shadow:0 8px 18px rgba(80,60,160,.14)'


@module('castaway_taboo')
def castaway_taboo(d):
    """Castaway Taboo, made by the teams. mode='make': each team writes 3 paper cards (word + 3 banned words). mode='play': swap cards, one describer, words only; shared counter to goal.
    words = ideas [(emoji,name)], frames = describer starters, goal = shared cards to guess."""
    mk=d.get('mode','make')
    o=header(d['phase'],d.get('role','Castaway Taboo'),'amber')+NOFIT
    if mk=='make':
        card='<div style="width:330px;height:420px;border-radius:36px;background:#fff;border:6px solid #ff9f1c;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;transform:rotate(-4deg);box-shadow:0 16px 30px rgba(80,60,160,.25)"><div style="font-size:120px;line-height:1">❓</div><div style="font-family:O;font-weight:800;font-size:34px;color:#1c1b2e;border-bottom:5px solid #1c1b2e;width:220px;height:46px"></div>'+''.join('<div style="display:flex;gap:12px;align-items:center"><span style="font-size:44px">🚫</span><span style="width:190px;height:6px;background:#bbb;border-radius:3px"></span></div>' for _ in range(3))+'</div>'
        o+=stp(glass(90,185,560,640,'<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px">'+card+'<div style="font-size:90px;line-height:1">✏️ ×3</div></div>',r=60),1)
        W=d['words']; w=190; h=176; g=14
        for i,(e,n) in enumerate(W):
            x=690+(i%5)*(w+g); y=185+(i//5)*(h+g)
            o+=stp(f'<div class="gl" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:40px;display:flex;flex-direction:column;align-items:center;justify-content:center"><span style="font-size:92px;line-height:1.05">{e}</span><span style="font-family:O;font-weight:800;font-size:26px;color:#1c1b2e">{n}</span></div>',2)
        o+=stp(f'<div class="a" style="left:690px;top:590px;width:1140px;display:flex;gap:14px;justify-content:center"><div style="{CHIP}"><span style="color:#6a35e8">1</span>✏️ one word</div><div style="{CHIP}"><span style="color:#6a35e8">2</span>🚫 three banned</div><div style="{CHIP}"><span style="color:#6a35e8">3</span>🃏 three cards</div></div>',3)
        o+=TIMER(int(d.get('sec',240)),690,700,4)
        return o
    o+=stp(glass(90,185,560,640,'<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px"><div style="font-size:120px;line-height:1;white-space:nowrap">🃏➡️👥</div><div style="font-size:120px;line-height:1">🔄</div><div style="font-size:90px;line-height:1;white-space:nowrap">🗣️👂👂👂</div></div>',r=60),1)
    F=d['frames']
    o+=stp(f'<div class="a" style="left:690px;top:185px;width:1140px;display:flex;flex-direction:column;gap:16px;align-items:stretch">'+''.join(f'<div style="{CHIP};font-size:46px;justify-content:center"><span style="font-size:56px">{e}</span>{t}</div>' for e,t in F)+'</div>',2)
    G=int(d.get('goal',12))
    o+=stp(f'<div class="a" style="left:690px;top:520px;width:1140px;display:flex;align-items:center;justify-content:center;gap:34px"><div class="tbm" style="width:130px;height:130px;border-radius:65px;display:flex;align-items:center;justify-content:center;font-size:70px;color:#fff;cursor:pointer;{GR}">−</div><div class="tbc" data-goal="{G}" style="font-family:O;font-weight:800;font-size:110px;color:#1c1b2e;min-width:520px;text-align:center">✅ 0 / {G}</div><div class="tbp" style="width:130px;height:130px;border-radius:65px;display:flex;align-items:center;justify-content:center;font-size:76px;color:#fff;cursor:pointer;{GR}">+</div></div>',3)
    o+=TIMER(int(d.get('sec',360)),690,700,4)
    return o


@module('if_chain')
def if_chain(d):
    """If-Chain: a ball passes round the team; each person says a result and the next starts from it. Teacher taps +link per correct link.
    starters = [(emoji, sentence)], goal = links to get home."""
    o=header(d['phase'],d.get('role','If-Chain'),'amber')+NOFIT
    S=d['starters']; G=int(d.get('goal',12))
    o+=f'<div class="icd" style="display:none">{_h.escape(json.dumps(S))}</div>'
    o+=stp(f'<div class="gl icard" style="left:90px;top:185px;width:700px;height:430px;border-radius:60px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:20px;box-sizing:border-box"><div class="ice" style="font-size:190px;line-height:1">🎲</div><div class="ict" style="font-family:O;font-weight:800;font-size:50px;text-align:center;color:#1c1b2e;line-height:1.15">Press 🎲 to start</div></div>',1)
    o+=stp(f'<div class="a" style="left:830px;top:185px;width:1000px;display:flex;flex-direction:column;gap:14px"><div style="{CHIP};justify-content:center"><span style="font-size:52px">⚽</span>If I … , I would …</div><div style="{CHIP};justify-content:center"><span style="font-size:52px">🔗</span>If I did that, I would …</div></div>',2)
    sl=''.join(f'<div class="icl" style="width:112px;height:112px;border-radius:30px;background:rgba(255,255,255,.55);border:4px dashed #b9b2e8;display:flex;align-items:center;justify-content:center;font-size:62px;opacity:.55">{"🏠" if i==G-1 else "·"}</div>' for i in range(G))
    o+=stp(f'<div class="a icg" data-goal="{G}" style="left:90px;top:640px;width:1740px;display:flex;gap:14px;justify-content:center">{sl}</div>',3)
    o+=stp(f'<div class="a icr" style="left:90px;top:770px;width:1740px;display:flex;gap:26px;justify-content:center"><div class="icn" style="{CHIP};cursor:pointer;font-size:46px">🎲 New start</div><div class="icb" style="width:380px;height:100px;border-radius:50px;display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:46px;color:#fff;cursor:pointer;{GR}">🔗 Next link ▶</div><div class="icx" style="{CHIP};cursor:pointer;font-size:46px">↩️ Dropped</div></div>',4)
    o+=TIMER(int(d.get('sec',240)),700,880,5)
    return o


@module('spot_art')
def spot_art(d):
    """Spot the difference with two real pictures. before/after = art file names (1024x765), hot = [(label,(x0,y0,x1,y1))] in picture pixels.
    The teacher taps the right-hand picture where the class points; each hotspot lights once, count and caption as in spot_change."""
    o=header(d['phase'],d.get('role','Look. What changed?'),'amber')+NOFIT
    w=860; iw=w-20; sc=iw/1024; h=int(765*sc)+20; y0=185
    o+=stp(art(90,y0,w,h,d['before'],r=40,label=d['before'],fit='contain'),1)
    o+=stp(art(970,y0,w,h,d['after'],r=40,label=d['after'],fit='contain'),2)
    hs=''
    for lab,(a,b,c,e) in d['hot']:
        hs+=f'<div class="a sdf" data-t="{lab}" data-c="0" style="left:{int(970+10+a*sc)}px;top:{int(y0+10+b*sc)}px;width:{int((c-a)*sc)}px;height:{int((e-b)*sc)}px;border-radius:30px"></div>'
    o+=stp('<div class="a hscn" style="left:0;top:0;width:1920px;height:1080px;pointer-events:none">'+hs+'</div>',2)
    n=len(d['hot'])
    o+=f'<div class="a hcount" data-n="{n}" style="left:810px;top:{y0+h+14}px;width:300px;text-align:center;font-family:O;font-weight:800;font-size:58px;color:#6a35e8">0 / {n}</div>'
    o+=f'<div class="a hcap" style="left:90px;top:{y0+h+86}px;width:1740px;text-align:center;font-family:O;font-weight:800;font-size:40px;color:#1c1b2e;height:50px"></div>'
    return o


EXT_CSS.append("""
.ipk.sel{box-shadow:0 0 0 10px #ff9f1c!important;background:rgba(255,236,190,.95)!important}.ipk.sel:after{content:"✔";position:absolute;right:12px;top:4px;font-size:40px;color:#10a98d}
.ipk.off{opacity:.25;filter:grayscale(1);pointer-events:none}
.ipr.on{box-shadow:0 0 0 8px #ff9f1c!important;background:#fff4d6!important}
.nxd1.on{opacity:1!important;box-shadow:0 0 0 6px #fff}
.nxs{opacity:.4;transition:opacity .35s,transform .35s,box-shadow .35s}.nxs.cur{opacity:1;box-shadow:0 0 0 8px #ff9f1c,0 16px 34px rgba(80,60,160,.2)!important;transform:scale(1.015)}
.nxcard.bad{box-shadow:0 0 0 10px #ff6b78!important}.nxcard.good{box-shadow:0 0 0 10px #2bd9b6!important}.nxcard.fin{box-shadow:0 0 0 10px #ffd166!important}
.nxcard.pop .nxe{animation:nxp .5s ease-out 1}@keyframes nxp{0%{transform:scale(.4) rotate(-12deg)}60%{transform:scale(1.2)}100%{transform:scale(1)}}
""")
EXT_JS.append(r"""
document.addEventListener('click',function(e){var s=e.target.closest('.sl');if(!s)return;
 var k=e.target.closest('.ipk');
 if(k){var cap=s.__cap||+($('.ipr.on',s)||{dataset:{cap:3}}).dataset.cap,n=$$('.ipk.sel',s).length;
  if(k.classList.contains('sel')){k.classList.remove('sel');P('tick')}else if(n<cap){k.classList.add('sel');P('pop')}else{P('boop')}
  var c=$('.ipc',s);if(c)c.textContent=$$('.ipk.sel',s).length+' / '+cap;return}
 var rp=e.target.closest('.ipr');
 if(rp){$$('.ipr',s).forEach(function(x){x.classList.toggle('on',x===rp)});var cap2=+rp.dataset.cap,ban=+rp.dataset.ban;s.__cap=cap2;
  $$('.ipk',s).forEach(function(x){x.classList.toggle('off',+x.dataset.i===ban);if(+x.dataset.i===ban)x.classList.remove('sel')});
  var sel=$$('.ipk.sel',s);while(sel.length>cap2){sel.pop().classList.remove('sel')}
  $('.ipc',s).textContent=$$('.ipk.sel',s).length+' / '+cap2;P('pop');return}
 var d1=e.target.closest('.nxd1');if(d1){d1.classList.toggle('on');P('tick');return}
},true);
(function(){var SUN=['☀️','🌤️','⛅','🌥️','🌇','🌅'];
 var LAB=['🗣️ Huddle ▶','🎤 Answers ▶','✋ Vote ▶','What next? ▶'];
 function setup(s){if(s.__nx||!s.querySelector('.nxbtn'))return;s.__nx=1;
  var D=JSON.parse(s.querySelector('.nxd').textContent),mids=D.mids.slice();
  for(var i=mids.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=mids[i];mids[i]=mids[j];mids[j]=t}
  var deck=[D.first].concat(mids.slice(0,D.rounds),[D.last]),ix=-1,ph=0,card=$('.nxcard',s),sun=$('.nxsun',s),btn=$('.nxbtn',s),steps=[$('.sA',s),$('.sB',s),$('.sC',s)];
  function show(){var c=deck[ix];
   if(!c){$('.nxe',s).textContent='🌴';$('.nxt',s).textContent='Press What next?';$('.nxk',s).textContent='';card.className='gl nxcard'}
   else{$('.nxe',s).textContent=c[0];$('.nxt',s).textContent=c[1];$('.nxk',s).textContent=c[2]==='bad'?'⚠️':c[2]==='good'?'🍀':'🌅';card.className='gl nxcard '+(c[2]==='bad'?'bad':c[2]==='good'?'good':'fin');void card.offsetWidth;card.classList.add('pop')}
   var f=ix<0?0:ix/(deck.length-1);sun.style.left=(240+f*1330)+'px';sun.textContent=SUN[Math.min(SUN.length-1,Math.round(f*(SUN.length-1)))];
   $('.nxpos',s).textContent=(ix+1)+' / '+deck.length;ph=0;steps.forEach(function(x){x.classList.remove('cur')});
   $$('.nxd1',s).forEach(function(x){x.classList.remove('on')});
   btn.textContent=ix<0?'What next? ▶':LAB[0];if(s.__treset)s.__treset()}
  function phase(p){ph=p;steps.forEach(function(x,k){x.classList.toggle('cur',k===p-1)});
   var last=ix>=deck.length-1;btn.textContent=p>=3?(last?'⛵ Boat!':'What next? ▶'):LAB[p];if(p===1&&s.__tauto)s.__tauto()}
  btn.onclick=function(ev){ev.stopPropagation();var last=ix>=deck.length-1;
   if(ix<0||ph>=3){if(last&&ph>=3){P('good');return}ix++;show();P(ix===deck.length-1?'good':'pop')}
   else{phase(ph+1);P('tick')}};
  $('.nxbk',s).onclick=function(ev){ev.stopPropagation();if(ph>0){phase(ph-1);if(ph===0){steps.forEach(function(x){x.classList.remove('cur')});btn.textContent=LAB[0]}P('tick')}else if(ix>-1){ix--;show();if(ix>=0)phase(3)}};
  s.__nxdeck=deck;s.__nxix=function(){return ix};show()}
 var iv=setInterval(function(){$$('.sl').forEach(setup)},400);})();

document.addEventListener('click',function(e){var s=e.target.closest('.sl');if(!s)return;
 var c=$('.tbc',s);
 if(c){var pl=e.target.closest('.tbp'),mi=e.target.closest('.tbm');
  if(pl||mi){var g=+c.dataset.goal,n=Math.max(0,Math.min(g,(+c.dataset.n||0)+(pl?1:-1)));c.dataset.n=n;
   c.textContent=n>=g?'⛵ '+n+' / '+g:'✅ '+n+' / '+g;P(n>=g?'good':pl?'pop':'tick');e.stopPropagation();return}}
 var ic=$('.icg',s);
 if(ic){var G=+ic.dataset.goal,ls=$$('.icl',s);s.__n=s.__n||0;
  function paint(){ls.forEach(function(x,i){var on=i<s.__n;x.style.opacity=on||i===G-1?1:.55;x.style.background=on?'#fff':'rgba(255,255,255,.55)';x.style.border=on?'4px solid #2bd9b6':'4px dashed #b9b2e8';x.textContent=i===G-1?'🏠':on?'🔗':'·'});
   if(s.__n>=G-1){$('.ict',s).textContent='🏠 Home! The chain saved us.';$('.ice',s).textContent='⛵'}}
  if(e.target.closest('.icb')){if(s.__n<G-1){s.__n++;P('pop')}else P('good');paint();e.stopPropagation();return}
  if(e.target.closest('.icx')){s.__n=Math.max(0,s.__n-1);paint();P('boop');e.stopPropagation();return}
  if(e.target.closest('.icn')){var D=JSON.parse($('.icd',s).textContent);s.__st=s.__st||D.slice().sort(function(){return Math.random()-.5});var k=s.__st.shift();if(!k){s.__st=D.slice().sort(function(){return Math.random()-.5});k=s.__st.shift()}
   $('.ice',s).textContent=k[0];$('.ict',s).textContent=k[1];if(s.__treset)s.__treset();P('pop');e.stopPropagation();return}}
},true);
""")
