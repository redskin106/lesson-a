"""Lesson 5 modules (night-shift story + boomerang ESA). All content is data, all art slots take emoji until real art arrives.
Chrome (added to ANY slide that carries clock=/gear= keys, call install_chrome() once after all modules are imported):
  clock='8:00 pm'   shared story clock, top right      gear=0..4 (+ gear_new=True)  the crew's toolkit, bottom
New modules:
  story(clock, pics[emoji], lines[text], big)            picture-led story beat, click reveals
  spot_change(base[(e,x,y)], diffs[(idx,new|None,label,clue)], extra[(e,x,y,label)], min)   Engage: two pictures, find what changed
  mingle(card{who,rows[(time,e)]}, steps[emoji], sec, cards_note)   mingle instructions + sample card + countdown
  solid_suspicious(items[{who,say,verdict,why}])        teacher-led call: statement, then verdict
  trap_chain(rows[{trap,if,then}])                      'If ..., we'll ...' chain, picture first
  excuse_pp(chars[(emoji,name)], plans[(plan,pic)], sec)   Excuse Ping-Pong prompts with a 4-second ring
  cards_page(cards,title,out)                           printable cut-out cards (A4, 2x4)"""
import json
from ..core import *
from .. import core

GEARS=[('🗓️','schedule'),('🤝','promise'),('🪤','trap'),('🧯','excuse')]

def chrome(d):
    o=''
    if d.get('clock'):
        o+=f'<div class="a chrome hclk" style="right:330px;top:54px"><span>{d.get("cicon","🕰️")}</span> {d["clock"]}</div>'
    if d.get('gear') is not None:
        n=d['gear']
        cells=''.join(f'<span class="hg{" on" if i<n else ""}{" nw" if d.get("gear_new") and i==n-1 else ""}">{e}</span>' for i,(e,_) in enumerate(d.get('gset') or GEARS))
        o+=f'<div class="a chrome hgear" style="left:430px;top:1006px">{cells}</div>'
    return o

def install_chrome():
    """wrap every registered module so clock/gear keys add the shared chrome"""
    from .. import interactive as I
    def wrap(f,two):
        if getattr(f,'_hw',0): return f
        if two:
            def g(d,sid): return f(d,sid)+chrome(d)
        else:
            def g(d): return f(d)+chrome(d)
        g._hw=1; return g
    for k in list(core.MODULES): core.MODULES[k]=wrap(core.MODULES[k],False)
    for k in list(core.BUILD_EXT): core.BUILD_EXT[k]=wrap(core.BUILD_EXT[k],True)
    for k in list(I.BUILD): I.BUILD[k]=wrap(I.BUILD[k],True)

def _timer(sec,top,adj=True,w=560):
    x=(1920-w)//2
    o=(f'<div class="a tclock" data-sec="{sec}" style="left:{x}px;top:{top}px;width:{w}px;text-align:center;font-family:O;font-weight:800;font-size:150px;line-height:1"><span class="grad">{sec//60}:{sec%60:02d}</span></div>'
       f'<div class="a tstart" style="left:{x+w+40}px;top:{top+10}px;width:150px;height:110px;border-radius:55px;display:flex;align-items:center;justify-content:center;{GR}"><svg width="50" height="50" viewBox="0 0 56 56"><path d="M16 8 L48 28 L16 48 Z" fill="#fff"/></svg></div>')
    if adj:
        for xx,dd,tt in ((x-340,-60,'−1'),(x-190,60,'+1')):
            o+=f'<div class="a tadj" data-d="{dd}" style="left:{xx}px;top:{top+15}px;width:120px;height:90px;border-radius:45px;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.85);border:4px solid #fff;color:#6a35e8;font-family:O;font-weight:800;font-size:42px;box-shadow:0 8px 20px rgba(80,60,160,.16);cursor:pointer;user-select:none">{tt}</div>'
    return o

@module('story')
def story(d):
    """{'phase','role','clock','pics':[emoji x1-4],'lines':[text],'big':'title','tone':'amber'|'night'}"""
    o=header(d['phase'],d.get('role'),d.get('grad','rose'))
    P=d.get('pics',['🏥']); n=len(P)
    o+=stp(glass(90,180,860,760,'',r=64),1)
    cols=2 if n>1 else 1
    sz=int(min(860/cols,760/((n+1)//2 if n>1 else 1))*(.9 if any(str(q).startswith('L6_') for q in P) else .62))
    for i,e in enumerate(P):
        r_,c_=(i//cols,i%cols); rows=(n+cols-1)//cols
        x=90+(860/cols)*c_+((860/cols)-sz)/2; y=180+(760/rows)*r_+((760/rows)-sz)/2
        o+=stp(f'<div class="a" style="left:{int(x)}px;top:{int(y)}px;width:{sz}px;height:{sz}px;font-size:{int(sz*.85)}px;line-height:{sz}px;text-align:center">'+(f'<img src="{ART}{e}" style="width:100%;height:100%;object-fit:contain">' if e.startswith('L6_') else e)+'</div>',1+i)
    big=d.get('big')
    if big: o+=f'<div class="a h" style="left:1000px;top:190px;width:830px;font-size:96px;line-height:1.02">{big}</div>'
    y=(380 if len(big)<16 else 480) if big else 230
    for k,t in enumerate(d.get('lines',[])):
        o+=stp(f'<div class="gl" style="left:1000px;top:{y+k*150}px;width:830px;height:126px;border-radius:50px;display:flex;align-items:center;padding:0 40px;box-sizing:border-box;font-family:O;font-weight:800;font-size:42px;line-height:1.15;color:#1c1b2e">{t}</div>',1+k)
    return o

@module('spot_change')
def spot_change(d):
    """Two scenes. base=[(emoji,x,y)] in a 760x640 box. diffs=[(index,new_emoji|None,label,clue?)]; extra=[(emoji,x,y,label)]."""
    base=d['base']; diffs={i:(n,l,c) for i,n,l,*cc in d['diffs'] for c in [cc[0] if cc else 0]}
    def scene(x0,right):
        s=glass(x0,190,800,690,'',r=56,ex='background:linear-gradient(#fff6e6,#ffe9cc)')
        for i,(e,x,y) in enumerate(base):
            ne,lab,cl=diffs.get(i,(e,'',0)); chg=right and i in diffs
            if right and i in diffs: e=ne or ''
            if e: s+=f'<div class="a{" sdf" if chg else ""}" data-t="{lab}" data-c="{cl}" style="left:{x0+20+x}px;top:{190+20+y}px;font-size:96px;line-height:1">{e}</div>'
            elif chg: s+=f'<div class="a sdf" data-t="{lab}" data-c="{cl}" style="left:{x0+20+x}px;top:{190+20+y}px;width:96px;height:96px;border-radius:50%;border:5px dashed #c0b4e8"></div>'
        if right:
            for e,x,y,lab in d.get('extra',[]): s+=f'<div class="a sdf" data-t="{lab}" data-c="0" style="left:{x0+20+x}px;top:{190+20+y}px;font-size:96px;line-height:1">{e}</div>'
        return s
    tot=len(diffs)+len(d.get('extra',[]))
    o=header(d['phase'],d.get('role','Look. What changed?'),'amber')
    o+=stp('<div class="a hscn" style="left:0;top:0;width:1920px;height:1080px;pointer-events:none">'+scene(90,False)+'</div>',1)+stp('<div class="a hscn" style="left:0;top:0;width:1920px;height:1080px;pointer-events:none">'+scene(1030,True)+'</div>',2)
    o+=f'<div class="a hcount" data-n="{tot}" style="left:810px;top:896px;width:300px;text-align:center;font-family:O;font-weight:800;font-size:58px;color:#6a35e8">0 / {tot}</div>'
    o+=f'<div class="a hcap" style="left:90px;top:960px;width:1740px;text-align:center;font-family:O;font-weight:800;font-size:40px;color:#1c1b2e;height:50px"></div>'
    return o

@module('mingle')
def mingle(d):
    """Mingle instructions. card={'who':emoji,'rows':[(time,emoji)],'hi':row index to match},steps=[emoji..],sec. Printable cards: cards_page()."""
    c=d['card']; o=header(d['phase'],d.get('role','Find your crew'),'teal')
    rows=''.join(f'<div style="display:flex;align-items:center;gap:26px;padding:10px 26px;border-radius:30px;{"background:linear-gradient(135deg,#d6fbea,#9fe8c4);" if i==c.get("hi",1) else "background:rgba(255,255,255,.7);"}"><span style="font-family:O;font-weight:800;font-size:46px;color:#1c1b2e;width:170px">{t}</span><span style="font-size:76px;line-height:1">{emo(e)}</span></div>' for i,(t,e) in enumerate(c['rows']))
    card=f'<div style="display:flex;flex-direction:column;gap:18px;padding:30px 36px;height:100%;box-sizing:border-box"><div style="font-size:120px;line-height:1;text-align:center">{emo(c["who"])}</div>{rows}</div>'
    o+=stp(glass(90,185,540,640,card,r=48,ex='transform:rotate(-3deg)'),1)
    st=d.get('steps',['🚶','🗣️','🤝'])
    for i,e in enumerate(st):
        o+=stp(f'<div class="gl" style="left:{700+i*380}px;top:230px;width:340px;height:340px;border-radius:64px;display:flex;align-items:center;justify-content:center;font-size:{170 if d.get('caps') else 190}px;{'flex-direction:column;gap:8px' if d.get('caps') else ''}">{emo(e)}{('<span style="font-family:O;font-weight:800;font-size:36px;line-height:1.05;color:#1c1b2e;text-align:center">'+d['caps'][i]+'</span>') if d.get('caps') else ''}</div>',2+i)
    if d.get('line'): o+=stp(f'<div class="a h" style="left:700px;top:620px;width:1130px;font-size:72px;text-align:center;line-height:1.05">{d["line"]}</div>',2)
    if d.get('sub'): o+=stp(f'<div class="a" style="left:700px;top:740px;width:1130px;text-align:center;font-family:O;font-weight:800;font-size:44px;line-height:1.2;color:#6a35e8">{d["sub"]}</div>',3)
    o+=_timer(int(d.get('sec',300)),850,w=500)
    return o

@module('solid_suspicious')
def solid_suspicious(d):
    """items=[{'who':emoji,'say':text,'verdict':'solid'|'suspicious','why':text}] — one statement at a time, then the verdict."""
    o=header(d['phase'],d.get('role','Solid or suspicious?'),'rose'); st=1
    for it in d['items']:
        ok=it['verdict']=='solid'
        o+=stp(f'<div class="gl" style="left:90px;top:190px;width:1740px;height:300px;border-radius:64px;display:flex;align-items:center;gap:40px;padding:0 60px;box-sizing:border-box"><span style="font-size:170px;line-height:1">{it["who"]}</span><span style="font-family:O;font-weight:800;font-size:60px;line-height:1.12;color:#1c1b2e">{it["say"]}</span></div>',st)
        o+=stp(f'<div class="a" style="left:90px;top:540px;width:1740px;display:flex;gap:40px;justify-content:center">'
               f'<div class="gl" style="position:relative;width:700px;height:170px;border-radius:85px;display:flex;align-items:center;justify-content:center;gap:24px;font-family:O;font-weight:800;font-size:72px;{"background:linear-gradient(135deg,#2bd9b6,#10a98d);color:#fff" if ok else "opacity:.35"}">✔ Solid</div>'
               f'<div class="gl" style="position:relative;width:700px;height:170px;border-radius:85px;display:flex;align-items:center;justify-content:center;gap:24px;font-family:O;font-weight:800;font-size:72px;{"opacity:.35" if ok else "background:linear-gradient(135deg,#ff6b78,#d62f48);color:#fff"}">✖ Suspicious</div></div>',st+1)
        o+=stp(f'<div class="a" style="left:90px;top:760px;width:1740px;text-align:center;font-family:O;font-weight:800;font-size:46px;color:#4a3a8a">{it["why"]}</div>',st+1)
        st+=2
    return o

@module('trap_chain')
def trap_chain(d):
    """rows=[{'trap':emoji,'if':text,'then':text}] — the trap, then the frame 'If ..., we'll ...'."""
    R=d['rows']; n=len(R); o=header(d['phase'],d.get('role','If… we’ll…'),'amber'); h=int((740-20*(n-1))/n); st=1
    for k,r in enumerate(R):
        y=185+k*(h+20)
        o+=stp(f'<div class="gl" style="left:90px;top:{y}px;width:{h}px;height:{h}px;border-radius:{h//4}px;display:flex;align-items:center;justify-content:center;font-size:{int(h*.6)}px">{r["trap"]}</div>',st)
        o+=stp(f'<div class="a" style="left:{90+h+30}px;top:{y}px;width:{1740-h-30}px;height:{h}px;display:flex;gap:14px;align-items:center;flex-wrap:wrap">'+ch('c4','If',46,'6px 24px')+ch('c1',r['if'],46,'6px 26px')+ch('c2',', we’ll',46,'6px 26px')+ch('c3',r['then'],46,'6px 26px')+'</div>',st+1)
        st+=2
    return o

@module('excuse_pp')
def excuse_pp(d):
    """Excuse Ping-Pong. chars=[(emoji,name)], plans=[(plan text,emoji)], sec=4. Tap start: 4 seconds to shout the excuse."""
    o=header(d['phase'],d.get('role','Excuse ping-pong'),'rose'); st=1
    for i,(e,n) in enumerate(d['chars']):
        o+=stp(f'<div class="gl" style="left:{90+i*330}px;top:190px;width:300px;height:380px;border-radius:56px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px"><span style="font-size:170px;line-height:1">{e}</span><span style="font-family:O;font-weight:800;font-size:34px;text-align:center;color:#1c1b2e;padding:0 12px">{n}</span></div>',1)
    for k,(t,e) in enumerate(d['plans']):
        o+=stp(f'<div class="gl" style="left:790px;top:{190+k*130}px;width:1040px;height:112px;border-radius:50px;display:flex;align-items:center;gap:14px;padding:0 24px;box-sizing:border-box;white-space:nowrap"><span style="font-size:60px;line-height:1">{e}</span>'+ch('c1','We',36,'2px 16px')+ch('c2','were going to',36,'2px 16px')+ch('c3',t,36,'2px 16px')+ch('c4','but…',36,'2px 16px')+'</div>',2+k)
    o+=_timer(int(d.get('sec',4)),720,adj=False,w=420)
    return o


TEAMC=['#e0304a','#2a6ae0','#10a98d','#e89200']
FRAMES={'schedule':[('c1','We'),('c2','are …ing'),('c3','at …')],'promise':[('c1','I'),('c2','will'),('c3','…')],'trap':[('c4','If'),('c1','…,'),('c2',"we'll"),('c3','…')],'excuse':[('c1','We'),('c2','were going to'),('c3','…'),('c4','but…')]}
@module('rpg_scene')
def rpg_scene(d):
    """One RPG scene, ALL four teams act. scene=emoji, problem=text, num=scene number (= which seat number speaks),
    teams=[{'gear':'schedule|promise|trap|excuse','eg':'sample answer (teacher)'}] x4, after=(emoji,line) consequence."""
    o=header(d['phase'],d.get('role',f'Scene {d["num"]}'),'rose')
    o+=stp(glass(90,185,640,675,f'<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;padding:0 30px;box-sizing:border-box"><div style="font-size:290px;line-height:1">{d["scene"]}</div><div style="font-family:O;font-weight:800;font-size:50px;text-align:center;line-height:1.1;color:#1c1b2e">{d["problem"]}</div></div>',r=60),1)
    gi={g:e for e,g in GEARS}
    for k,t in enumerate(d['teams']):
        x=770+(k%2)*540; y=185+(k//2)*345
        frame=''.join(ch(c,tx,34,'4px 16px') for c,tx in FRAMES[t['gear']])
        eg=f'<div data-s="6" class="sh" style="font-family:P;font-weight:600;font-size:30px;color:#0b6b55;line-height:1.2;margin-top:12px">e.g. {t["eg"]}</div>'
        body=(f'<div style="padding:22px 26px;box-sizing:border-box;height:100%"><div style="display:flex;align-items:center;gap:16px"><span style="width:46px;height:46px;border-radius:14px;background:{TEAMC[k]}"></span><span style="font-size:66px;line-height:1">{gi[t["gear"]]}</span>'
              f'<span style="margin-left:auto;font-family:O;font-weight:800;font-size:34px;color:#fff;padding:4px 20px;border-radius:999px;background:{TEAMC[k]}">#{d["num"]} speaks</span></div>'
              f'<div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:22px">{frame}</div>{eg}</div>')
        o+=stp(glass(x,y,520,330,body,r=44),2+k)
    e,l=d['after']
    o+=stp(f'<div class="gl" style="left:90px;top:885px;width:1740px;height:105px;border-radius:52px;display:flex;align-items:center;gap:30px;padding:0 44px;box-sizing:border-box"><span style="font-size:70px;line-height:1">{e}</span><span style="font-family:O;font-weight:800;font-size:44px;color:#1c1b2e">{l}</span></div>',7)
    return o


import html as _h
@module('debate_scene')
def debate_scene(d):
    """Team debate on its feet, whole class votes. scene=emoji, problem, team=0..3, routes=[{e,t,ok:(e,t),ko:(e,t)}] x2, sec=60.
    Teacher taps the route the team chose, the class votes go / no-go (hands), teacher taps the vote: go shows the success, no-go shows what would have happened."""
    o=header(d['phase'],d.get('role',f'Scene {d["num"]}'),'rose')
    o+=stp(glass(90,185,520,520,f'<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;padding:0 24px;box-sizing:border-box"><div style="font-size:230px;line-height:1">{d["scene"]}</div><div style="font-family:O;font-weight:800;font-size:46px;text-align:center;line-height:1.1;color:#1c1b2e">{d["problem"]}</div></div>',r=56),1)
    for i,r in enumerate(d['routes']):
        a=lambda k:_h.escape(r[k][0],True); b=lambda k:_h.escape(r[k][1],True)
        o+=stp(f'<div class="gl drt" data-ok-e="{a("ok")}" data-ok-t="{b("ok")}" data-ko-e="{a("ko")}" data-ko-t="{b("ko")}" style="left:{640+i*600}px;top:185px;width:590px;height:300px;border-radius:52px;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px"><span style="position:absolute;left:24px;top:18px;font-family:O;font-weight:800;font-size:52px;color:#6a35e8">{"AB"[i]}</span><span style="font-size:140px;line-height:1">{r["e"]}</span><span style="font-family:O;font-weight:800;font-size:44px;color:#1c1b2e;text-align:center;padding:0 20px">{r["t"]}</span></div>',1)
    fr=ch('c1','I think we should…',38,'6px 22px')+ch('c4','But if we…,',38,'6px 22px')+ch('c2','…they will…',38,'6px 22px')+ch('c3',"OK, we'll…",38,'6px 22px')
    o+=stp(f'<div class="a" style="left:640px;top:510px;width:1190px;display:flex;gap:14px;flex-wrap:wrap;justify-content:center">{fr}</div>',1)
    tc=TEAMC[d['team']]
    sp=''.join(f'<span class="dsp" style="width:84px;height:84px;border-radius:50%;background:{tc};opacity:.35;display:flex;align-items:center;justify-content:center;font-size:48px;color:#fff;cursor:pointer;user-select:none"></span>' for _ in range(4))
    o+=stp(f'<div class="a" style="left:90px;top:730px;width:520px;display:flex;gap:18px;justify-content:center;align-items:center">{sp}</div>',2)
    sec=int(d.get('sec',60))
    o+=stp(f'<div class="a tclock" data-sec="{sec}" style="left:640px;top:610px;width:420px;text-align:center;font-family:O;font-weight:800;font-size:130px;line-height:1"><span class="grad">{sec//60}:{sec%60:02d}</span></div>',2)
    o+=stp(f'<div class="a tstart" style="left:1080px;top:625px;width:140px;height:100px;border-radius:50px;display:flex;align-items:center;justify-content:center;{GR}"><svg width="46" height="46" viewBox="0 0 56 56"><path d="M16 8 L48 28 L16 48 Z" fill="#fff"/></svg></div>',2)
    o+=stp(f'<div class="a" style="left:1240px;top:640px;width:590px;text-align:center;font-family:O;font-weight:800;font-size:40px;color:{tc}">Team {d["team"]+1} stands. Everyone speaks.</div>',2)
    o+=stp('<div class="a" style="left:90px;top:870px;width:520px;display:flex;gap:30px;justify-content:center"><div class="dvote" data-v="go" style="width:230px;height:120px;border-radius:60px;background:linear-gradient(135deg,#2bd9b6,#10a98d);color:#fff;font-size:70px;display:flex;align-items:center;justify-content:center;cursor:pointer;opacity:.9">👍</div><div class="dvote" data-v="no" style="width:230px;height:120px;border-radius:60px;background:linear-gradient(135deg,#ff6b78,#d62f48);color:#fff;font-size:70px;display:flex;align-items:center;justify-content:center;cursor:pointer;opacity:.9">👎</div></div>',3)
    o+='<div class="gl dout" style="left:640px;top:790px;width:1190px;height:200px;border-radius:56px;display:flex;align-items:center;gap:36px;padding:0 50px;box-sizing:border-box"><span class="oe" style="font-size:120px;line-height:1"></span><span class="ot" style="font-family:O;font-weight:800;font-size:50px;line-height:1.15;color:#1c1b2e"></span></div>'
    return o

@module('guess_class')
def guess_class(d):
    """Class-vs-teacher Guess Who. suspects=[{e,n,a:{key:bool}}], attrs=[{k,e,t}], secret=index, budget=8, frame text.
    The class asks with the frame, teacher taps the matching clue chip: the screen answers YES/NO and greys out suspects. Tap a face to accuse."""
    o=header(d['phase'],d.get('role','Who is bitten?'),'rose')
    S=d['suspects']; n=len(S)
    for i,sp in enumerate(S):
        o+=f'<div class="gl gcs" data-i="{i}" data-a="{_h.escape(json.dumps(sp["a"]),True)}" style="left:{90+i*(int(1740/n))}px;top:185px;width:{int(1740/n)-20}px;height:360px;border-radius:48px;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px"><span style="font-size:170px;line-height:1">{sp["e"]}</span><span style="font-family:O;font-weight:800;font-size:38px;color:#1c1b2e">{sp["n"]}</span></div>'
    o+=f'<div class="a gcsec" data-s="{d.get("secret",0)}" data-b="{d.get("budget",8)}" style="left:90px;top:575px;width:420px;text-align:center;font-family:O;font-weight:800;font-size:44px;color:#6a35e8">Questions left: <span class="gcb" style="font-size:90px;vertical-align:middle">{d.get("budget",8)}</span></div>'
    o+='<div class="gl gcans" style="left:90px;top:700px;width:420px;height:250px;border-radius:56px;display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:110px;color:#6a35e8">?</div>'
    o+=f'<div class="a" style="left:560px;top:575px;width:1270px;text-align:center;font-family:O;font-weight:800;font-size:40px;color:#4a3a8a">{d.get("frame","Is he / she …?")} <span style="font-size:30px;font-weight:600">(teacher: tap the clue the class asks about)</span></div>'
    cs=''.join(f'<div class="gcq" data-k="{a["k"]}" style="display:flex;align-items:center;gap:14px;padding:10px 26px;border-radius:999px;background:rgba(255,255,255,.8);border:4px solid #fff;font-family:O;font-weight:800;font-size:36px;color:#1c1b2e;cursor:pointer;box-shadow:0 8px 18px rgba(80,60,160,.14)"><span style="font-size:56px;line-height:1">{a["e"]}</span>{a["t"]}</div>' for a in d['attrs'])
    o+=f'<div class="a" style="left:560px;top:690px;width:1270px;display:flex;flex-wrap:wrap;gap:16px;justify-content:center">{cs}</div>'
    o+='<div class="a gcwin" style="left:90px;top:960px;width:1740px;text-align:center;font-family:O;font-weight:800;font-size:44px;color:#10a98d;height:50px"></div>'
    return o

# ---------------- printable cards (A4, 2 x 4 per page, cut lines) ----------------
def cards_page(cards,title,out):
    """cards=[{'who':emoji,'rows':[(label,emoji)],'foot':text}] -> standalone printable html"""
    cs=''.join('<div class="c"><div class="w">'+c['who']+'</div>'+''.join(f'<div class="r"><b>{a}</b><i>{b}</i></div>' for a,b in c['rows'])+(f'<div class="f">{c["foot"]}</div>' if c.get('foot') else '')+f'<div class="n">{k+1}</div></div>' for k,c in enumerate(cards))
    html=(f'<!doctype html><meta charset="utf-8"><title>{title}</title><style>@page{{size:A4;margin:8mm}}body{{margin:0;font-family:Arial,sans-serif}}'
          '.g{display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:66mm;gap:0;page-break-after:auto}.c{border:1px dashed #999;padding:5mm;box-sizing:border-box;position:relative;break-inside:avoid}'
          '.w{font-size:20mm;text-align:center;line-height:1}.r{display:flex;align-items:center;gap:6mm;margin-top:2mm;font-size:6mm}.r b{width:20mm}.r i{font-style:normal;font-size:12mm}.f{font-size:5mm;margin-top:3mm;text-align:center}.n{position:absolute;right:3mm;bottom:2mm;font-size:3mm;color:#bbb}'
          f'</style><div class="g">{cs}</div>')
    open(out,'w').write(html); return out

EXT_CSS.append("""
.drt.pick{box-shadow:0 0 0 10px #ff9f1c!important}.dsp.on{opacity:1!important}.dsp.on:after{content:"✔"}.dvote.pick{transform:scale(1.15);box-shadow:0 0 0 8px #fff}.dout{opacity:0;transition:opacity .4s}.dout.on{opacity:1}
.gcs.out{opacity:.22;filter:grayscale(1)}.gcq.used{opacity:.3;pointer-events:none}.gcans.yes{color:#10a98d!important}.gcans.no{color:#d62f48!important}
.hclk{font-family:O;font-weight:800;font-size:34px;color:#4a3a8a;padding:8px 30px;border-radius:999px;background:rgba(255,255,255,.72);border:3px solid #fff;box-shadow:0 8px 18px rgba(80,60,160,.16);white-space:nowrap}
.hgear{display:flex;gap:16px;padding:6px 22px;border-radius:999px;background:rgba(255,255,255,.55);border:3px solid #fff}
.hg{font-size:38px;line-height:1.3;opacity:.22;filter:grayscale(1);transition:all .4s}.hg.on{opacity:1;filter:none}.hg.nw{animation:hgp 1.6s ease-out 1}@keyframes hgp{0%{transform:scale(.6)}50%{transform:scale(1.5)}100%{transform:scale(1)}}
.mdls{display:flex!important;opacity:.16;transition:opacity .25s;top:30px!important}.mdls:hover{opacity:1}.mdl{width:34px!important;height:34px!important;border-width:3px!important;gap:3px!important}.mdl i{width:6px!important;height:6px!important}.mdl.on{transform:scale(1.2)!important}
.sdf{cursor:pointer;border-radius:30px;pointer-events:auto}.sdf.found{background:rgba(255,200,60,.35);box-shadow:0 0 0 8px #ff9f1c;animation:none}
""")
EXT_JS.append(r"""
document.addEventListener('click',function(e){var s=e.target.closest('.sl');if(!s)return;
 var r=e.target.closest('.drt'),v=e.target.closest('.dvote'),sp=e.target.closest('.dsp');
 function upd(){if(!(s.__r&&s.__v))return;var k=s.__v==='go'?'ok':'ko',o=$('.dout',s);$('.oe',o).textContent=s.__r.dataset[k+'E'];$('.ot',o).textContent=s.__r.dataset[k+'T'];o.classList.add('on');P(k==='ok'?'good':'boop')}
 if(r){$$('.drt',s).forEach(function(x){x.classList.toggle('pick',x===r)});s.__r=r;P('pop');upd();return}
 if(v){$$('.dvote',s).forEach(function(x){x.classList.toggle('pick',x===v)});s.__v=v.dataset.v;P('pop');upd();return}
 if(sp){sp.classList.toggle('on');P('tick');return}
 var q=e.target.closest('.gcq');if(q&&s.querySelector('.gcsec')){var sec=$('.gcsec',s),sx=+sec.dataset.s,S=$$('.gcs',s),A=JSON.parse(S[sx].dataset.a),k=q.dataset.k,ans=!!A[k];q.classList.add('used');
  var b=$('.gcb',s);b.textContent=Math.max(0,(+b.textContent)-1);var an=$('.gcans',s);an.textContent=ans?'YES':'NO';an.className='gl gcans '+(ans?'yes':'no');P(ans?'good':'boop');
  S.forEach(function(x){var a=JSON.parse(x.dataset.a);if(!!a[k]!==ans)x.classList.add('out')});return}
 var c=e.target.closest('.gcs');if(c&&s.querySelector('.gcsec')){var sec2=$('.gcsec',s),sx2=+sec2.dataset.s;if(+c.dataset.i===sx2){$('.gcwin',s).textContent='🎉 Yes! The pharmacist is bitten!';$$('.gcs',s).forEach(function(x){if(x!==c)x.classList.add('out')});c.style.boxShadow='0 0 0 12px #2bd9b6';P('good')}else{c.classList.add('out');P('boop');var b2=$('.gcb',s);b2.textContent=Math.max(0,(+b2.textContent)-1)}}
},true);
document.addEventListener('click',function(e){var b=e.target.closest('.sdf');if(!b)return;var s=b.closest('.sl');if(!s||b.classList.contains('found'))return;b.classList.add('found');P('pop');
 var c=$('.hcount',s),n=+c.dataset.n,f=$$('.sdf.found',s).length;c.textContent=f+' / '+n;var cap=$('.hcap',s);if(cap)cap.textContent=(b.dataset.t||'');if(f>=n)P('good')},true);
""")
