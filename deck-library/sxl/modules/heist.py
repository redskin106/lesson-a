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
        o+=f'<div class="a chrome hclk" style="right:330px;top:54px"><span>🕰️</span> {d["clock"]}</div>'
    if d.get('gear') is not None:
        n=d['gear']
        cells=''.join(f'<span class="hg{" on" if i<n else ""}{" nw" if d.get("gear_new") and i==n-1 else ""}">{e}</span>' for i,(e,_) in enumerate(GEARS))
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
    sz=int(min(860/cols,760/((n+1)//2 if n>1 else 1))*.62)
    for i,e in enumerate(P):
        r_,c_=(i//cols,i%cols); rows=(n+cols-1)//cols
        x=90+(860/cols)*c_+((860/cols)-sz)/2; y=180+(760/rows)*r_+((760/rows)-sz)/2
        o+=stp(f'<div class="a" style="left:{int(x)}px;top:{int(y)}px;width:{sz}px;height:{sz}px;font-size:{int(sz*.85)}px;line-height:{sz}px;text-align:center">{e}</div>',1+i)
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
    rows=''.join(f'<div style="display:flex;align-items:center;gap:26px;padding:10px 26px;border-radius:30px;{"background:linear-gradient(135deg,#d6fbea,#9fe8c4);" if i==c.get("hi",1) else "background:rgba(255,255,255,.7);"}"><span style="font-family:O;font-weight:800;font-size:46px;color:#1c1b2e;width:170px">{t}</span><span style="font-size:76px;line-height:1">{e}</span></div>' for i,(t,e) in enumerate(c['rows']))
    card=f'<div style="display:flex;flex-direction:column;gap:18px;padding:30px 36px;height:100%;box-sizing:border-box"><div style="font-size:120px;line-height:1;text-align:center">{c["who"]}</div>{rows}</div>'
    o+=stp(glass(90,185,540,640,card,r=48,ex='transform:rotate(-3deg)'),1)
    st=d.get('steps',['🚶','🗣️','🤝'])
    for i,e in enumerate(st):
        o+=stp(f'<div class="gl" style="left:{700+i*380}px;top:230px;width:340px;height:340px;border-radius:64px;display:flex;align-items:center;justify-content:center;font-size:190px">{e}</div>',2+i)
    if d.get('line'): o+=stp(f'<div class="a h" style="left:700px;top:620px;width:1130px;font-size:72px;text-align:center;line-height:1.05">{d["line"]}</div>',2)
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
.hclk{font-family:O;font-weight:800;font-size:34px;color:#4a3a8a;padding:8px 30px;border-radius:999px;background:rgba(255,255,255,.72);border:3px solid #fff;box-shadow:0 8px 18px rgba(80,60,160,.16);white-space:nowrap}
.hgear{display:flex;gap:16px;padding:6px 22px;border-radius:999px;background:rgba(255,255,255,.55);border:3px solid #fff}
.hg{font-size:38px;line-height:1.3;opacity:.22;filter:grayscale(1);transition:all .4s}.hg.on{opacity:1;filter:none}.hg.nw{animation:hgp 1.6s ease-out 1}@keyframes hgp{0%{transform:scale(.6)}50%{transform:scale(1.5)}100%{transform:scale(1)}}
.mdls{display:flex!important;opacity:.16;transition:opacity .25s;top:30px!important}.mdls:hover{opacity:1}.mdl{width:34px!important;height:34px!important;border-width:3px!important;gap:3px!important}.mdl i{width:6px!important;height:6px!important}.mdl.on{transform:scale(1.2)!important}
.sdf{cursor:pointer;border-radius:30px;pointer-events:auto}.sdf.found{background:rgba(255,200,60,.35);box-shadow:0 0 0 8px #ff9f1c;animation:none}
""")
EXT_JS.append(r"""
document.addEventListener('click',function(e){var b=e.target.closest('.sdf');if(!b)return;var s=b.closest('.sl');if(!s||b.classList.contains('found'))return;b.classList.add('found');P('pop');
 var c=$('.hcount',s),n=+c.dataset.n,f=$$('.sdf.found',s).length;c.textContent=f+' / '+n;var cap=$('.hcap',s);if(cap)cap.textContent=(b.dataset.t||'');if(f>=n)P('good')},true);
""")
