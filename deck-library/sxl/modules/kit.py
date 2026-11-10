"""kit — general modules ported/generalised from Lesson 1. All content is data. See sxl/README.md for the catalog.
cover, title_card, today, columns, pic_question, strip, pic_rows, qgrid, dial, cards, slot, prep, recap, exit
Grad names: violet red teal amber rose orange sky, or any CSS gradient string."""
import math
from ..core import *
G=lambda g:GRAD.get(g,g)
def stp(html,s,g=None,pills=False):
    """Mark an element as reveal step s (click-per-step in interactive decks; ignored in static output)."""
    i=html.index('<'); j=html.index(' ',i)
    return html[:j]+f' data-s="{s}"'+(f' data-g="{g}"' if g else '')+(' data-pills="1"' if pills else '')+html[j:]
def pill(t,fs=36,mu=True): return f'<span class="pill{" mu" if mu else ""}" style="font-size:{fs}px;padding:12px 38px;{"" if mu else "color:#6a35e8"}">{t}</span>'
def chiprow(cs,fs=46,p='8px 26px',gap='12px',wrap=False): return f'<div style="display:flex;gap:{gap};{"flex-wrap:wrap;" if wrap else ""}align-items:center">'+''.join(ch(c,t,fs,p) for c,t in cs)+'</div>'
def sh(): return 'filter:drop-shadow(0 16px 18px rgba(40,20,90,.3))'
def dots(n,total=5): return '<div style="display:flex;gap:16px">'+''.join(f'<div style="width:44px;height:44px;border-radius:50%;{GR if k<n else "background:rgba(154,92,255,.18)"}"></div>' for k in range(total))+'</div>'

@module('cover')
def cover(d):
    """{'tag':'EFL','title':'Lesson <span class="grad">1</span>','phases':['Engage','Study','Activate'],'active':0,'cards':[{'pic':f,'x':1010,'y':150,'w':330,'h':430,'r':-7}]}"""
    o=f'<div class="tag" style="left:110px;top:90px;{GR}font-size:30px">{d["tag"]}</div>' if d.get('tag') else ''
    o+=f'<div class="a h" style="left:104px;top:640px;font-size:210px;line-height:.9;white-space:nowrap">{d["title"]}</div>'
    o+='<div class="a" style="left:110px;top:900px;display:flex;gap:20px">'+''.join(pill(t,36,i!=d.get('active',0)) for i,t in enumerate(d.get('phases',[])))+'</div>'
    for c in d.get('cards',[]):
        o+=(f'<div class="gl" style="left:{c["x"]}px;top:{c["y"]}px;width:{c["w"]}px;height:{c["h"]}px;border-radius:56px;padding:14px;transform:rotate({c.get("r",0)}deg);background:rgba(255,255,255,.9)">'
            f'<img src="{ART}{c["pic"]}" style="width:100%;height:100%;object-fit:cover;border-radius:42px;display:block"></div>')
    return o

@module('title_card')
def title_card(d):
    """Section title with an arch of emoji. {'phase':'ACTIVATE','line1':'The','line2':'Hotline','arch':[('telephone_receiver',1260,230,420,-10),...]}"""
    o=header(d['phase'])+f'<div class="a h" style="left:110px;top:300px;font-size:260px;line-height:.92">{d["line1"]}<br><span class="grad">{d["line2"]}</span></div>'
    o+='<div class="gl" style="left:1210px;top:150px;width:580px;height:780px;border-radius:290px 290px 64px 64px"></div>'
    return o+''.join(em(n,x,y,w,r) for n,x,y,w,r in d.get('arch',[]))

@module('today')
def today(d):
    """{'phase':'STUDY','emoji':'pointing_viewer','title':'Orders and advice','rows':[[(c,t),...] or {'icon':emoji,'chips':[...]}],'fs':76,'tfs':104}"""
    fs=d.get('fs',70); tfs=d.get('tfs',104); rows=''
    for i,r in enumerate(d['rows']):
        cs,ic=(r['chips'],r.get('icon')) if isinstance(r,dict) else (r,None)
        row=chiprow(cs,fs,'8px 30px','16px')
        if ic: row=f'<div style="display:flex;gap:28px;align-items:center"><img src="{EM(ic)}" style="width:110px;{sh()}">{row}</div>'
        rows+=stp(f'<div class="rw">{row}</div>',i+2,pills=True)
    return (header(d['phase'],d.get('role','Today we learn'),'violet')
      +'<div class="gl" style="left:90px;top:168px;width:1740px;height:820px;border-radius:72px"></div>'
      +f'<div class="a" style="left:200px;top:168px;width:1520px;height:820px;display:flex;align-items:center;gap:90px">'
      +stp(f'<img src="{EM(d["emoji"])}" style="width:300px;{sh()}">',1)
      +f'<div style="display:flex;flex-direction:column;gap:44px;align-items:flex-start">'+stp(f'<div style="font-family:O;font-weight:800;font-size:{tfs}px;color:#1c1b2e;white-space:nowrap;line-height:1">{d["title"]}</div>',1)
      +rows+'</div></div>')

@module('columns')
def columns(d):
    """2-3 columns, each a labelled picture with chip rows and a gloss. {'cols':[{'label','grad'?,'pic','rows':[[chips]],'gloss'}]}"""
    C=d['cols']; n=len(C); gx=40; w=int((1740-gx*(n-1))/n); w=min(w,560); ph=int(w*9/16); gx=int((1740-w*n)/(n-1)) if n>1 else 0
    o=header(d['phase'],d.get('title'),d.get('rg','violet')); nb=d.get('numbered')
    if d.get('card'):
        cw=int((1740-30*(n-1))/n); st=1
        for i,c in enumerate(C):
            x=90+i*(cw+30); g=i+1; pw=cw-40; ph2=int(pw*9/16)
            tn=c.get('tint'); o+=stp(f'<div class="gl" style="left:{x}px;top:168px;width:{cw}px;height:820px;border-radius:64px;{stint(tn) if tn is not None else ""}"></div>',st,g)
            o+=stp(f'<div class="a" style="left:{x}px;top:196px;width:{cw}px;display:flex;justify-content:center">{grad_chip(c.get("grad","violet"),c["label"],44,"8px 34px")}</div>',st,g)
            o+=stp(pic(x+20,270,pw,ph2,c['pic'],40),st,g); st+=1
            for k_,r in enumerate(c['rows']):
                yy=270+ph2+40+k_*104
                if k_: o+=stp(f'<div class="a" style="left:{x+60}px;top:{yy-14}px;width:{cw-120}px;height:3px;border-radius:2px;background:rgba(124,70,230,.25)"></div>',st,g)
                o+=stp(f'<div class="a" style="left:{x}px;top:{yy}px;width:{cw}px;display:flex;gap:8px;justify-content:center">'+''.join(ch(a,b,40,'6px 16px') for a,b in r)+'</div>',st,g,pills=True); st+=1
            if c.get('gloss'):
                gl=c['gloss']; gl=[(gl,None)] if isinstance(gl,str) else gl
                o+=stp(f'<div class="a" style="left:{x}px;top:872px;width:{cw}px;display:flex;gap:10px;justify-content:center">'+''.join(spill(t,ix,38,'8px 22px' if len(gl)>1 else '8px 32px') for t,ix in gl)+'</div>',st,g)
        return o
    for i,c in enumerate(C):
        x=90+i*(w+gx)
        if nb: o+=num(x+w//2-32,200,i+1)+pic(x,290,w,ph,c['pic'],40)+f'<div class="a" style="left:{x}px;top:{290+ph+36}px;width:{w}px;display:flex;justify-content:center">{grad_chip(c.get("grad","violet"),c["label"],44,"8px 34px")}</div>'; continue
        o+=f'<div class="a" style="left:{x}px;top:200px;width:{w}px;display:flex;justify-content:center">{grad_chip(c.get("grad","violet"),c["label"],44,"8px 34px")}</div>'+pic(x,290,w,ph,c['pic'],40)
        for k,r in enumerate(c['rows']):
            o+=f'<div class="a" style="left:{x-20}px;top:{290+ph+50+k*104}px;width:{w+40}px;display:flex;gap:10px;justify-content:center">'+''.join(ch(a,b,46,'8px 22px') for a,b in r)+'</div>'
        if c.get('gloss'): o+=f'<div class="a" style="left:{x}px;top:{290+ph+60+len(c["rows"])*104}px;width:{w}px;text-align:center"><span class="pill" style="font-size:44px;padding:8px 36px;color:#6a35e8;white-space:nowrap">{c["gloss"]}</span></div>'
    return o

@module('pic_question')
def pic_question(d):
    """One big picture + a question panel. {'phase':'ENGAGE','pic':f,'q':('What',['should','he do?'])}"""
    w,rest=d['q']
    return (header(d['phase'])+stp(pic(90,235,1240,686,d['pic'],56),1)
      +stp('<div class="gl" style="left:1370px;top:235px;width:460px;height:686px;border-radius:56px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px;font-family:O;font-weight:800;font-size:76px;line-height:1.05">'
      +f'<span class="chip c4" style="font-size:80px;padding:8px 36px;border-radius:999px">{w}</span>'+''.join(f'<span>{t}</span>' for t in rest)
      +f'<div style="width:120px;height:120px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:80px;{GR}">?</div></div>',2))

EARTH='<svg width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="#4fa7ff" stroke="#1c1b2e" stroke-width="4"/><path d="M14 22c6-8 14-6 16 0s-6 8-4 14-10 6-12-2z" fill="#4fcf7a"/><path d="M38 14c8-2 14 4 12 10s-8 4-10 10 8 8 0 12-8-18-2-32z" fill="#4fcf7a"/></svg>'
def bubble(x,y,mark):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:176px;height:104px;border-radius:52px;background:#fff;border:5px solid #1c1b2e;display:flex;align-items:center;justify-content:center;gap:6px;box-shadow:0 10px 24px rgba(40,20,90,.25)">{EARTH}<img src="{EM(mark)}" style="width:54px"></div>'
        f'<div style="position:absolute;left:{x+28}px;top:{y+98}px;width:0;height:0;border-left:14px solid transparent;border-right:14px solid transparent;border-top:26px solid #1c1b2e"></div>'
        f'<div style="position:absolute;left:{x+32}px;top:{y+94}px;width:0;height:0;border-left:10px solid transparent;border-right:10px solid transparent;border-top:20px solid #fff"></div>')
@module('strip')
def strip(d):
    """5-panel story strip + a closing chip panel. {'role':'Boss','grad':'red','pics':[5 files],'close':[[chips],[chips]],'bubble':{'panel':3,'emoji':'thumbs_up'}}"""
    o=header(d['phase'],d['role']+' says' if 'title' not in d else d['title'],d.get('grad','violet'))
    xs=[90,680,1270]; ny=[168,593]; py=[248,673]
    for i,f in enumerate(d['pics']):
        r,c=divmod(i,3); o+=stp(num(xs[c]+248,ny[r],i+1),i+1)+stp(pic(xs[c],py[r],560,315,f),i+1)
    n=len(d['pics'])+1
    o+=stp('<div class="gl" style="left:1270px;top:673px;width:560px;height:315px;border-radius:56px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px">'+''.join(chiprow(r,52,'10px 30px','14px') for r in d['close'])+'</div>',n,pills=True)
    b=d.get('bubble')
    if b: o+=f'<div data-s="{b.get("panel",3)}" style="position:absolute;left:0;top:0">'+bubble(1440,252,b['emoji'])+'</div>'
    return o

@module('pic_rows')
def pic_rows(d):
    """Rows of pictures with a label chip + sentence. {'rows':[{'label','grad','chips':[..],'pics':[files],'cap':'...'}]}"""
    R=d['rows']; n=len(R); o=header(d['phase'],d.get('title')); st=1
    for j,r in enumerate(R):
        y=168+j*425+(150 if n==1 else 0); k=len(r['pics']); w=int((1740-30*(k-1))/k); w=min(w,(560 if n==1 else 440) if k==3 else 405); h=int(w*9/16); gx=(60 if n>1 else int((1740-w*k)/(k-1))) if k>1 else 0
        for i,f in enumerate(r['pics']): o+=stp(pic(90+i*(w+gx),y+90,w,h,f,36),st+i)
        o+=stp(f'<div class="a" style="left:90px;top:{y}px;display:flex;align-items:center;gap:0"><div class="chip" style="font-size:44px;padding:10px 40px;border-radius:999px;background:{G(r["grad"])}">{r["label"]}</div><div style="width:6px;height:54px;border-radius:3px;background:rgba(124,70,230,.4);margin:0 44px"></div>{chiprow(r["chips"])}</div>',st+k,pills=True)
        used=k+1
        if r.get('cap'): o+=stp(f'<div class="a" style="left:{90+(k-1)*(w+gx)}px;top:{y+90+h+10}px;width:{w}px;display:flex;justify-content:center">{spill(r["cap"],r.get("sc"),34,"6px 28px")}</div>',st+k+1); used+=1
        st+=used
    return o

@module('qgrid')
def qgrid(d):
    """2x2 pictures with a question chip row under each. {'items':[{'pic','chips'}]}"""
    o=header(d['phase'],d.get('title','Question it'))
    for i,it in enumerate(d['items'][:4]):
        r,c=divmod(i,2); x=90+c*920; y=168+r*420
        o+=stp(pic(x+140,y,540,304,it['pic'],40),2*i+1)+stp(f'<div class="a" style="left:{x}px;top:{y+322}px;width:820px;display:flex;gap:12px;justify-content:center">'+''.join(ch(a,b,46,'8px 26px') for a,b in it['chips'])+'</div>',2*i+2,pills=True)
    return o

@module('dial')
def dial(d):
    """Strength dial. stops left->right: [(angle,emoji,[labels],gloss)]. angle 180..0."""
    cx,cy,R=960,800,430; S=d['stops']
    pts=[(cx+R*math.cos(math.radians(a)),cy-R*math.sin(math.radians(a))) for a,*_ in S]
    svg=(f'<svg style="position:absolute;left:0;top:0" width="1920" height="1080"><defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#ff6b78"/><stop offset=".3" stop-color="#ffb347"/><stop offset=".5" stop-color="#7fd3ff"/><stop offset=".75" stop-color="#9a5cff"/><stop offset="1" stop-color="#ff4fa3"/></linearGradient></defs>'
         f'<path d="M {cx-R} {cy} A {R} {R} 0 0 1 {cx+R} {cy}" fill="none" stroke="url(#g)" stroke-width="30" stroke-linecap="round"/>'
         f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-R+60}" stroke="#1c1b2e" stroke-width="10" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="24" fill="#1c1b2e"/></svg>')
    o=header(d['phase'],d.get('title','How strong?'),'violet')+svg
    for (x,y),(a,e,ts,gl) in zip(pts,S):
        o+=f'<div class="gl dstop" style="left:{x-65}px;top:{y-65}px;width:130px;height:130px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#fff;border-color:#fff"><img src="{EM(e)}" style="width:84px"></div>'
        labs=''.join(ch('c2',t,52 if i==0 else 40,'8px 30px' if i==0 else '6px 22px') for i,t in enumerate(ts))
        g=f'<div class="mu" style="font-size:30px;margin-top:6px">{gl}</div>' if gl else ''
        if a>=135: o+=f'<div style="position:absolute;left:{x-65-24-560}px;top:{y-60}px;width:560px;display:flex;flex-direction:column;align-items:flex-end;justify-content:center;height:120px"><div style="display:flex;gap:10px">{labs}</div>{g}</div>'
        elif a==90: o+=f'<div style="position:absolute;left:{x-300}px;top:{y-65-130}px;width:600px;display:flex;flex-direction:column;align-items:center;height:120px;justify-content:center"><div style="display:flex;gap:10px">{labs}</div>{g}</div>'
        else: o+=f'<div style="position:absolute;left:{x+65+24}px;top:{y-(80 if len(ts)>1 else 60)}px;width:440px;display:flex;flex-direction:column;gap:10px;align-items:flex-start;height:{160 if len(ts)>1 else 120}px;justify-content:center"><div style="display:flex;flex-direction:column;gap:10px;align-items:flex-start">{labs}</div>{g}</div>'
    return o

@module('choice_board')
def choice_board(d):
    """Picture dial: 5 tiles (weak->strong). Tap a tile -> big picture + sentence + gloss. {'stops':[{'word','pic','chips','gloss','grad'}],'start':4}"""
    S=d['stops']; n=len(S); st=d.get('start',n-1)
    o=header(d['phase'],d.get('title','How strong?'),'violet')
    o+='<div class="gl" style="left:90px;top:168px;width:1740px;height:470px;border-radius:72px"></div>'
    for i,s in enumerate(S):
        op=1 if i==st else 0
        o+=f'<div class="cbp" data-i="{i}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;opacity:{op};pointer-events:none">'
        o+=pic(124,194,774,418,s['pic'],48)
        o+=f'<div class="a" style="left:960px;top:230px;width:830px;display:flex;flex-direction:column;align-items:center;gap:40px">{chiprow(s["chips"],64,"10px 32px","14px",wrap=True)}<span class="pill" style="font-size:54px;padding:10px 44px;color:#6a35e8;white-space:nowrap">{s["gloss"]}</span></div></div>'
    w=268; h=151; gx=int((1560-w*n)/(n-1))
    o+='<div class="gl" style="left:90px;top:668px;width:1740px;height:320px;border-radius:64px"></div>'
    for i,s in enumerate(S):
        x=130+i*(w+gx)
        o+=(f'<div class="cbt{" sel" if i==st else ""}" data-i="{i}" style="position:absolute;left:{x}px;top:700px;width:{w}px;height:{h+110}px;cursor:pointer">'
            +pic(0,0,w,h,s['pic'],30)
            +f'<div class="a" style="left:0;top:{h+34}px;width:{w}px;text-align:center"><span class="chip" style="font-size:38px;padding:6px 26px;border-radius:999px;background:{G(s["grad"])}">{s["word"]}</span></div></div>')
    return o

@module('dial_pics')
def dial_pics(d):
    """Dial + pictures: arc with five picture bubbles and a needle; tap a bubble -> needle swings, big picture + sentence + gloss at right.
    {'stops':[{'word','pic','grad','chips','gloss'}] weak->strong left->right, 'start':4}"""
    S=d['stops']; n=len(S); st=d.get('start',n-1); cx,cy,R,br=640,780,400,82
    ang=[180-i*(180/(n-1)) for i in range(n)]
    o=header(d['phase'],d.get('title','How strong?'),'violet')
    o+=(f'<svg style="position:absolute;left:0;top:0" width="1920" height="1080"><defs><linearGradient id="dg" x1="0" x2="1"><stop offset="0" stop-color="#ff6b78"/><stop offset=".3" stop-color="#ffb347"/><stop offset=".5" stop-color="#7fd3ff"/><stop offset=".75" stop-color="#9a5cff"/><stop offset="1" stop-color="#ff4fa3"/></linearGradient></defs>'
        f'<path d="M {cx-R} {cy} A {R} {R} 0 0 1 {cx+R} {cy}" fill="none" stroke="url(#dg)" stroke-width="30" stroke-linecap="round"/></svg>')
    L=R-br-50
    o+=(f'<div class="dpn" data-cx="{cx}" style="position:absolute;left:{cx-9}px;top:{cy-L}px;width:18px;height:{L}px;border-radius:9px;background:#1c1b2e;transform-origin:50% 100%;transform:rotate({90-ang[st]}deg);transition:transform .7s cubic-bezier(.3,1.5,.5,1)"></div>'
        f'<div style="position:absolute;left:{cx-30}px;top:{cy-30}px;width:60px;height:60px;border-radius:50%;background:#1c1b2e"></div>')
    for i,s in enumerate(S):
        a=math.radians(ang[i]); x=cx+R*math.cos(a); y=cy-R*math.sin(a)
        o+=(f'<div class="dpb{" sel" if i==st else ""}" data-i="{i}" data-a="{ang[i]:.0f}" style="position:absolute;left:{x-br-60}px;top:{y-br}px;width:{2*br+120}px;height:{2*br+90}px;cursor:pointer;text-align:center">'
            f'<div class="dpc" style="position:absolute;left:60px;top:0;width:{2*br}px;height:{2*br}px;border-radius:50%;border:8px solid #fff;box-shadow:0 12px 26px rgba(40,20,90,.3);background:#fff;box-sizing:border-box;overflow:hidden"><img src="{ART}{s["pic"]}" style="position:absolute;height:{(2*br-16)*s.get("focus",(.5,.5,1))[2]:.0f}px;width:auto;left:{(2*br-16)/2-s.get("focus",(.5,.5,1))[0]*(2*br-16)*s.get("focus",(.5,.5,1))[2]*1.7917:.0f}px;top:{(2*br-16)/2-s.get("focus",(.5,.5,1))[1]*(2*br-16)*s.get("focus",(.5,.5,1))[2]:.0f}px"></div>'
            +(f'<div style="position:absolute;left:-300px;width:350px;text-align:right;top:{br-26}px">' if 90<ang[i]<180 else (f'<div style="position:absolute;left:{60+2*br+10}px;width:350px;text-align:left;top:{br-26}px">' if 0<ang[i]<90 else f'<div style="position:absolute;left:0;right:0;top:{2*br+10}px">'))
            +f'<span class="chip" style="font-size:36px;padding:5px 24px;border-radius:999px;background:{G(s["grad"])};white-space:nowrap">{s["word"]}</span></div></div>')
    o+='<div class="gl" style="left:1230px;top:168px;width:600px;height:820px;border-radius:72px"></div>'
    for i,s in enumerate(S):
        o+=(f'<div class="dpp" data-i="{i}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;opacity:{1 if i==st else 0};pointer-events:none">'
            +pic(1260,214,540,304,s['pic'],44)
            +f'<div class="a" style="left:1250px;top:560px;width:560px;height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center">{chiprow(s["chips"],50,"8px 28px","12px",wrap=True)}</div>'
            +f'<div class="a" style="left:1250px;top:800px;width:560px;text-align:center"><span class="pill" style="font-size:50px;padding:10px 44px;color:#6a35e8;white-space:nowrap">{s["gloss"]}</span></div></div>')
    return o

@module('dial_ladder')
def dial_ladder(d):
    """Vertical ladder: strongest at the top. Same stop data as dial_pics; tap a rung -> marker slides, picture + sentence + gloss at right."""
    S=d['stops']; n=len(S); st=d.get('start',n-1); top0=168; rh=148; gp=16; x0=150; w=1040
    tinted=d.get('tinted'); T=[('#ff6b78','#d62f48','#fff'),('#ffa07a','#ee6a36','#fff'),('#ffe27a','#e3b21c','#3a2f00'),('#6fd79a','#2fa85e','#fff'),('#3fc27c','#168648','#fff')]
    def tc(i): return T[min(i,len(T)-1)]
    o=header(d['phase'],d.get('title','How strong?'),'violet')
    o+=f'<div style="position:absolute;left:96px;top:{top0}px;width:16px;height:{n*rh+(n-1)*gp}px;border-radius:8px;background:{"linear-gradient(180deg,#168648,#6fd79a 30%,#ffe27a 50%,#ee6a36 75%,#d62f48)" if tinted else "linear-gradient(180deg,#ff4fa3,#9a5cff 30%,#7fd3ff 50%,#ffb347 75%,#ff6b78)"}"></div>'
    ys=[top0+(n-1-i)*(rh+gp) for i in range(n)]
    for i,s in enumerate(S):
        y=ys[i]; f=s.get('focus',(.5,.5,1)); sz=rh-28; ins=sz-12
        o+=(f'<div class="dlr{" sel" if i==st else ""}" data-i="{i}" data-y="{y}" style="position:absolute;left:{x0}px;top:{y}px;width:{w}px;height:{rh}px;cursor:pointer">'
            f'<div class="gl" style="left:0;top:0;width:{w}px;height:{rh}px;border-radius:{rh//2}px;{("background:linear-gradient(90deg,"+tc(i)[0]+"55,"+tc(i)[0]+"22);border-color:"+tc(i)[0]+"aa") if tinted else ""}"></div>'
            f'<div style="position:absolute;left:14px;top:14px;width:{sz}px;height:{sz}px;border-radius:50%;border:6px solid #fff;box-sizing:border-box;background:#fff;overflow:hidden;box-shadow:0 8px 18px rgba(40,20,90,.25)"><img src="{ART}{s["pic"]}" style="position:absolute;height:{ins*f[2]:.0f}px;width:auto;left:{ins/2-f[0]*ins*f[2]*1.7917:.0f}px;top:{ins/2-f[1]*ins*f[2]:.0f}px"></div>'
            f'<div style="position:absolute;left:{sz+50}px;top:0;height:{rh}px;display:flex;align-items:center"><span class="chip" style="font-size:50px;padding:8px 34px;border-radius:999px;background:{("linear-gradient(135deg,"+tc(i)[0]+","+tc(i)[1]+");color:"+tc(i)[2]) if tinted else G(s["grad"])};white-space:nowrap">{s["word"]}</span>'
            +(f'<span style="margin-left:22px;font-family:O;font-weight:800;font-size:32px;color:#8a86a3;background:rgba(255,255,255,.6);padding:4px 22px;border-radius:999px">{s["alt"]}</span>' if s.get("alt") else '')+'</div>'
            f'<div style="position:absolute;right:40px;top:0;height:{rh}px;display:flex;align-items:center"><span class="pill" style="font-size:40px;padding:8px 32px;color:#6a35e8;white-space:nowrap">{s["gloss"]}</span></div></div>')
    o+=f'<div class="dlm" style="position:absolute;left:{x0-8}px;top:{ys[st]-8}px;width:{w+16}px;height:{rh+16}px;border-radius:{rh//2+8}px;border:7px solid #9a5cff;box-shadow:0 0 0 6px rgba(154,92,255,.25),0 14px 34px rgba(106,53,232,.35);pointer-events:none;transition:top .55s cubic-bezier(.3,1.4,.5,1)"></div>'
    o+='<div class="gl" style="left:1230px;top:168px;width:600px;height:820px;border-radius:72px"></div>'
    for i,s in enumerate(S):
        o+=(f'<div class="dpp" data-i="{i}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;opacity:{1 if i==st else 0};pointer-events:none">'
            +(f'<div class="gl" style="left:1230px;top:168px;width:600px;height:820px;border-radius:72px;background:linear-gradient(180deg,{tc(i)[0]}66,{tc(i)[0]}22);border-color:{tc(i)[0]}aa"></div>' if tinted else '')
            +pic(1260,214,540,304,s['pic'],44)
            +f'<div class="a" style="left:1250px;top:560px;width:560px;height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center">{chiprow(s["chips"],50,"8px 28px","12px",wrap=True)}</div>'
            +f'<div class="a" style="left:1250px;top:800px;width:560px;text-align:center"><span class="pill" style="font-size:50px;padding:10px 44px;color:#6a35e8;white-space:nowrap">{s["gloss"]}</span></div></div>')
    return o

@module('cards')
def cards(d):
    """2-4 tall cards. {'cards':[{'emoji','name','grad','text','foot'}]}"""
    C=d['cards']; n=len(C); w=min(540,int((1740-60*(n-1))/n)); gx=int((1740-w*n)/(n-1)) if n>1 else 0
    o=header(d['phase'],d.get('title'),d.get('rg','violet'))
    for i,c in enumerate(C):
        x=90+i*(w+gx)
        o+=stp(f'<div class="gl" style="left:{x}px;top:168px;width:{w}px;height:820px;border-radius:72px;display:flex;flex-direction:column;align-items:center;gap:36px;padding:{70 if n<4 else 90}px 24px 0">'
            f'<img src="{EM(c["emoji"])}" style="width:{260 if n<4 else 210}px;{sh()}"><div class="chip" style="font-size:{64 if n<4 else 52}px;padding:12px {56 if n<4 else 40}px;border-radius:999px;background:{G(c["grad"])}">{c["name"]}</div>'
            f'<div style="font-family:O;font-weight:800;font-size:{46 if n<4 else 44}px;color:#1c1b2e;text-align:center;line-height:1.15;padding:0 20px">{c.get("text","")}</div>'
            +(f'<div class="pill" style="font-size:38px;padding:10px 36px;color:#6a35e8">{c["foot"]}</div>' if c.get('foot') else '')
            +(f'<button class="vplay" data-v="{c["video"]}" aria-label="Play video"><svg width="64" height="64" viewBox="0 0 64 64"><path d="M22 14L52 32L22 50Z" fill="#fff" stroke="#fff" stroke-width="6" stroke-linejoin="round"/></svg></button>' if c.get('video') else '')+'</div>',i+1)
    if d.get('note'): o+=f'<div class="pill" style="position:absolute;left:150px;top:900px;font-size:36px;padding:10px 36px">{d["note"]}</div>'
    return o

def reel(emo,spin=False):
    import html as _h
    real=f'<img src="{EM(emo)}" style="width:84px">'
    inner=(f'<img src="{EM(emo)}" style="width:84px;filter:blur(7px);opacity:.55;transform:translateY(-14px)"><img src="{EM(emo)}" style="width:84px;filter:blur(7px);opacity:.55;transform:translateY(14px);margin-left:-60px">' if spin else real)
    return f'<div class="reelc" data-real="{_h.escape(real)}" style="width:500px;height:100px;border-radius:50px;background:rgba(255,255,255,.75);box-shadow:inset 0 4px 10px rgba(80,60,160,.15);display:flex;align-items:center;justify-content:center;overflow:hidden">{inner}</div>'
def reelp(n,spin=False):
    import html as _h
    x=('<div style="font-family:O;font-weight:800;font-size:60px;color:#9a5cff;letter-spacing:.2em;filter:blur(3px)">· · ·</div>' if spin else dots(n))
    return f'<div class="reelp" data-real="{_h.escape(dots(n))}" style="width:500px;height:100px;border-radius:50px;background:rgba(255,255,255,.75);box-shadow:inset 0 4px 10px rgba(80,60,160,.15);display:flex;align-items:center;justify-content:center">{x}</div>'
@module('slot')
def slot(d):
    """Slot machine: every row = (problem emoji, pain 1-5, twist emoji, spinning?). Heads are data."""
    heads=d.get('heads',['PROBLEM','PAIN','TWIST'])
    o=header(d['phase'])+'<div class="a" style="left:300px;top:176px;display:flex;gap:20px;font-family:O;font-weight:700;font-size:28px;letter-spacing:.14em;color:#4a5a7a">'+''.join(f'<div style="width:500px;text-align:center">{t}</div>' for t in heads)+'</div>'
    o+=f'<div class="spinbtn" style="position:absolute;left:1650px;top:60px;width:180px;height:100px;border-radius:50px;display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:44px;color:#fff;{GR}">SPIN</div>'
    o+='<div class="srows" style="position:absolute;left:90px;top:226px;width:1740px;height:770px;display:flex;flex-direction:column;justify-content:center;gap:20px">'
    for k_,(a,p,t,sp) in enumerate(d['rows']):
        o+=(f'<div class="gl sr" data-k="{k_}" style="position:relative;flex:1 1 0;max-height:176px;min-height:110px;border-radius:66px;display:flex;align-items:center;gap:20px;padding:0 36px">'
            f'<div style="width:84px;height:84px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:50px;margin-right:24px;{GR}">{k_+1}</div>'+reel(a,sp)+reelp(p,sp)+reel(t,sp)+'</div>')
    o+='</div>'
    return o

tile=lambda e,t:f'<div style="width:330px;height:170px;border-radius:44px;background:rgba(255,255,255,.75);display:flex;align-items:center;gap:16px;padding:0 20px"><img src="{EM(e)}" style="width:80px"><div style="font-family:O;font-weight:800;font-size:30px;line-height:1.1;color:#1c1b2e">{t}</div></div>'
bigtile=lambda e,t,w=190,h=230,iw=100,fs=34:f'<div style="width:{w}px;height:{h}px;border-radius:44px;background:rgba(255,255,255,.75);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px"><img src="{EM(e)}" style="width:{iw}px"><div style="font-family:O;font-weight:800;font-size:{fs}px;color:#1c1b2e;text-align:center;line-height:1.1">{t}</div></div>'
def block(b):
    k=b[0]
    if k=='chips': return ''.join(chiprow(r) for r in b[1])
    if k=='lead': return chiprow(b[1],56,'8px 30px')
    if k=='tiles': return '<div style="display:flex;gap:20px">'+''.join(bigtile(e,t) for e,t in b[1])+'</div>'
    if k=='bigtiles': return '<div style="display:flex;gap:26px">'+''.join(bigtile(e,t,270,300,140,40) for e,t in b[1])+'</div>'
    if k=='qrows': return '<div style="display:flex;flex-direction:column;gap:34px;width:100%">'+''.join(f'<div style="display:flex;align-items:center;gap:28px;background:rgba(255,255,255,.7);border-radius:64px;padding:30px 36px"><img src="{EM(e)}" style="width:100px;{sh()}">{chiprow(cs,46,"8px 26px","10px")}</div>' for e,cs in b[1])+'</div>'
    if k=='label': return f'<div style="font-family:O;font-weight:700;font-size:30px;color:#4a5a7a;letter-spacing:.08em">{b[1]}</div>'
    return ''
@module('prep')
def prep(d):
    """Group prep screen: left panel / right panel (lists of blocks) + 'Repair kit' tiles + status (emoji, pain dots) + timer.
    block kinds: ('chips',[[chips]]) ('lead',[chips]) ('tiles',[(emoji,text)]) ('bigtiles',..) ('label',text)"""
    o=header(d['phase'],d['role'],d.get('grad','violet'))
    s=d.get('status')
    if s: o+=f'<div class="gl" style="left:820px;top:40px;height:100px;width:auto;padding:0 40px;border-radius:50px;display:flex;align-items:center;gap:26px"><img src="{EM(s[0])}" style="width:64px">{dots(s[1])}<img src="{EM(s[2])}" style="width:64px"></div>'
    o+=f'<div class="pill" style="position:absolute;right:90px;top:50px;font-size:50px;padding:10px 46px;color:#fff;{GR}">{d.get("timer","3:00")}</div>'
    kit=d.get('repair','default'); ph=552 if kit else 820
    wl,wr=d.get('widths',(1010,700))
    for x,w,blocks,al in [(90,wl,d['left'],d.get('lal','center')),(90+wl+30,wr,d['right'],'center')]:
        o+=stp(f'<div class="gl" style="left:{x}px;top:168px;width:{w}px;height:{ph}px;border-radius:72px;padding:44px 40px;display:flex;flex-direction:column;align-items:{"flex-start" if al=="start" else "center"};justify-content:center;gap:{26 if al=="start" else 32}px">'+''.join(block(b) for b in blocks)+'</div>',1 if x==90 else 2)
    if kit:
        o+=stp('<div class="gl" style="left:90px;top:760px;width:1740px;height:228px;border-radius:72px;display:flex;align-items:center;gap:20px;padding:0 40px"><div class="chip" style="font-size:40px;padding:10px 34px;border-radius:999px;background:linear-gradient(135deg,#ff8a3c,#ff4f7a)">Repair kit</div>'+''.join(tile(e,t) for e,t in (d['repair'] if isinstance(d.get('repair'),list) and d['repair'] else [('red_question_mark','Sorry?'),('speech_balloon','Say that again?'),('stopwatch','Slower, please.'),('face_with_open_mouth','I don’t understand.')]))+'</div>',3)
    return o

@module('recap')
def recap(d):
    """{'phase':'RECAP','rows':[([chips],'gloss')],'side':[[chips]],'emoji':'face_with_thermometer'}"""
    o=header(d['phase'])+f'<div class="a h" style="left:90px;top:130px;font-size:68px">{d.get("title","Today we can say…")}</div>'
    nr=len(d['rows'])
    for k,(cs,g) in enumerate(d['rows']):
        o+=stp(f'<div class="gl" style="left:90px;top:{240+k*150}px;width:{960 if d.get('side') else 1270}px;height:128px;border-radius:64px;display:flex;align-items:center;gap:14px;padding:0 36px">{chiprow(cs,48,"8px 24px","14px")}<span style="margin-left:auto">{spill(g,None,34,"6px 26px")}</span></div>',k+1,pills=True)
    if d.get('side'):
        o+=stp('<div class="gl" style="left:1080px;top:240px;width:750px;height:728px;border-radius:72px"></div>',nr+1)
        for k,q in enumerate(d['side']): o+=stp(f'<div class="a" style="left:1100px;top:{300+k*150}px;width:710px;display:flex;gap:10px;justify-content:center">'+''.join(ch(a,b,44,'8px 22px') for a,b in q)+'</div>',nr+1+k,pills=True)
    if d.get('emoji'): o+=stp(f'<img src="{EM(d["emoji"])}" style="position:absolute;left:1520px;top:{300 if not d.get("side") else 770}px;width:{260 if not d.get("side") else 190}px;{sh()}">',nr+len(d.get('side') or [])+(0 if d.get('side') else 1))
    return o+'<div class="a mu" style="right:36px;bottom:12px;font-size:15px;opacity:.55">Emoji: Microsoft Fluent Emoji (MIT)</div>'

@module('rules')
def rules(d):
    """Rows of colour-coded pills with a small letter under each (S subject, V verb, O object, B because) + a key at the bottom.
    {'rows':[([(cls,text,letter)],'gloss')]}"""
    o=header(d['phase'])+f'<div class="a h" style="left:90px;top:130px;font-size:68px">{d.get("title","Three little rules")}</div>'
    nr=len(d['rows'])
    for k,(cs,g) in enumerate(d['rows']):
        y=230+k*200
        body=''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px">{ch(c,t,48,"8px 24px")}<span style="font-family:O;font-weight:800;font-size:34px;color:#7b3cf0">{l}</span></div>' for c,t,l in cs)
        o+=stp(f'<div class="gl" style="left:90px;top:{y}px;width:1500px;height:170px;border-radius:70px;display:flex;align-items:center;gap:18px;padding:0 44px">{body}<span style="margin-left:auto">{spill(g,None,40,"8px 30px")}</span></div>',k+1,pills=True)
    key=[('c1','S','Subject'),('c2','V','Verb'),('c3','O','Object'),('c4','B','because')]
    o+='<div class="gl" style="left:90px;top:850px;width:1500px;height:110px;border-radius:55px;display:flex;align-items:center;justify-content:center;gap:34px">'+''.join(f'<div style="display:flex;align-items:center;gap:10px">{ch(c,l,36,"4px 20px")}<span style="font-family:O;font-weight:700;font-size:34px;color:#4a3a8a">{t}</span></div>' for c,l,t in key)+'</div>'
    if d.get('emoji'): o+=stp(f'<img src="{EM(d["emoji"])}" style="position:absolute;left:1640px;top:300px;width:230px;{sh()}">',nr)
    return o

@module('exit')
def exit_(d):
    """{'phase':'EXIT','line1':'One useful','line2':'question.','prompt':'Ask the person next to you','emoji':'light_bulb'}"""
    return (header(d.get('phase','EXIT'))+f'<div class="a h" style="left:90px;top:250px;font-size:170px;line-height:1.02">{d["line1"]}<br><span class="grad">{d["line2"]}</span></div>'
      +f'<div class="gl" style="left:90px;top:700px;height:130px;width:auto;padding:0 50px;border-radius:999px;display:flex;align-items:center;font-family:O;font-weight:800;font-size:52px">{d["prompt"]}</div>'
      +em(d.get('emoji','light_bulb'),1330,200,420,8))

PAL['RECAP']=PAL['EXIT']=PAL['ENGAGE']

@module('timer')
def timer(d):
    """Activity slide with a visible countdown. {'phase':'ACTIVATE','title':'Group practice','min':8,'icons':['face_with_thermometer',..],'note':'Everyone speaks at once'}"""
    sec=int(d.get('min',3)*60); icons=''.join(f'<img src="{EM(e)}" style="width:190px;{sh()}">' for e in d.get('icons',['stopwatch']))
    return (header(d['phase'],d['title'],d.get('rg','violet'))
      +'<div class="gl" style="left:90px;top:168px;width:1740px;height:820px;border-radius:72px"></div>'
      +f'<div class="a" style="left:90px;top:230px;width:1740px;display:flex;gap:60px;justify-content:center">{icons}</div>'
      +f'<div class="a tclock" data-sec="{sec}" style="left:90px;top:440px;width:1740px;text-align:center;font-family:O;font-weight:800;font-size:330px;line-height:1"><span class="grad">{sec//60}:{sec%60:02d}</span></div>'
      +f'<div class="a tstart" style="left:860px;top:830px;width:200px;height:120px;border-radius:60px;display:flex;align-items:center;justify-content:center;{GR}"><svg width="56" height="56" viewBox="0 0 56 56"><path d="M16 8 L48 28 L16 48 Z" fill="#fff"/></svg></div>'
      +(f'<div class="a mu" style="left:90px;top:730px;width:1740px;text-align:center;font-size:44px">{d["note"]}</div>' if d.get('note') else ''))

ARROW='<svg width="200" height="120" viewBox="0 0 200 120"><defs><linearGradient id="ar" x1="0" x2="1"><stop offset="0" stop-color="#7b3cf0"/><stop offset="1" stop-color="#ff4fa3"/></linearGradient></defs><path d="M20 60H165M122 22L168 60L122 98" fill="none" stroke="url(#ar)" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/></svg>'

@module('cause_chain')
def cause_chain(d):
    """Cause -> consequence stories. Pictures first, then the sentence. {'rows':[{'cause':f,'effect':f,'sent':[(cls,text)..]}]}"""
    R=d['rows']; n=len(R); o=header(d['phase'],d.get('title')); st=1; w,h=480,270; pitch=420 if n>1 else 0; y0=170 if n>1 else 250
    x0=int((1920-(2*w+200))/2)
    for j,r in enumerate(R):
        y=y0+j*pitch
        o+=stp(pic(x0,y,w,h,r['cause'],40),st)
        o+=stp(f'<div class="a" style="left:{x0+w}px;top:{y+h//2-60}px;width:200px">{ARROW}</div>',st+1)
        o+=stp(pic(x0+w+200,y,w,h,r['effect'],40),st+1)
        o+=stp(f'<div class="a" style="left:90px;top:{y+h+22}px;width:1740px;display:flex;gap:12px;justify-content:center">'+''.join(ch(c,t,46,'8px 26px') for c,t in r['sent'])+'</div>',st+2,pills=True)
        st+=3
    return o

def pick_html(d,btn=False):
    """Concept check: a picture and 'Why?', tap the right cause. {'effect':f,'options':[f,f,f],'ok':index}"""
    o=header(d['phase'],d.get('title','Why?'),'violet')
    o+=pic(90,170,640,360,d['effect'],44)
    o+=f'<div class="a" style="left:780px;top:200px;display:flex;align-items:center;gap:26px">{ch("c4",d.get("q","Why does it hurt?"),76 if len(d.get("q","Why does it hurt?"))<=18 else 66,"10px 46px")}</div>'
    o+=f'<div class="a psay" style="left:780px;top:400px;width:1050px;display:flex;flex-wrap:wrap;gap:12px;opacity:0;transition:opacity .5s">'+''.join(ch(c,t,44,"6px 22px") for c,t in d.get('say',[]))+'</div>'
    n=len(d['options']); w=int((1740-50*(n-1))/n); h=int(w*9/16); y=600
    for i,f in enumerate(d['options']):
        x=90+i*(w+50); card=pic(0 if btn else x,0 if btn else y,w,h,f,40)
        o+=(f'<button class="pk" data-i="{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:40px">{card}</button>' if btn else card)
    return o

@module('pick')
def pick(d): return pick_html(d)

@module('ball_circle')
def ball_circle(d):
    """The ball circle: three stations joined by ball arrows, a word bank (pain pictures + past verbs) that stays on screen, and a timer.
    {'phase','title','min','stations':[{'emoji','name','grad','chips':[(cls,text)]}],'pain':[(pic,label)],'verbs':[(pic,past)]}"""
    sec=int(d.get('min',10)*60); o=header(d['phase'],d.get('title'))
    o+=(f'<div class="a tclock" data-sec="{sec}" style="left:1380px;top:34px;width:300px;text-align:center;font-family:O;font-weight:800;font-size:92px;line-height:1"><span class="grad">{sec//60}:{sec%60:02d}</span></div>'
        f'<div class="a tstart" style="left:1700px;top:44px;width:130px;height:84px;border-radius:42px;display:flex;align-items:center;justify-content:center;{GR}"><svg width="40" height="40" viewBox="0 0 56 56"><path d="M16 8 L48 28 L16 48 Z" fill="#fff"/></svg></div>')
    S=d['stations']; w=520; gap=90; y=168; h=470
    BALL=('<svg viewBox="0 0 100 100" width="80" height="80" style="position:absolute;left:%dpx;top:300px;%s"><defs><radialGradient id="bg" cx="35%%" cy="30%%"><stop offset="0" stop-color="#ffd27a"/><stop offset="1" stop-color="#ff8a3c"/></radialGradient></defs><circle cx="50" cy="50" r="46" fill="url(#bg)" stroke="#fff" stroke-width="4"/><path d="M8 40Q50 62 92 40M10 66Q50 44 90 66" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/></svg>')
    for i,s in enumerate(S):
        x=90+i*(w+gap); st=i+1
        if i>0:
            o+=stp(f'<div class="a" style="left:{x-gap}px;top:400px;width:{gap}px;transform:scale(.45);transform-origin:left top">{ARROW}</div>',st)
        o+=stp(glass(x,y,w,h,'',r=64),st)
        o+=stp(f'<img src="{EM(s["emoji"])}" style="position:absolute;left:{x+w//2-90}px;top:{y+26}px;width:180px;{sh()}">',st)
        o+=stp(f'<div class="a" style="left:{x}px;top:{y+226}px;width:{w}px;display:flex;justify-content:center">{grad_chip(s["grad"],s["name"],52,"8px 44px")}</div>',st)
        o+=stp(f'<div class="a" style="left:{x+20}px;top:{y+318}px;width:{w-40}px;display:flex;flex-wrap:wrap;gap:10px;justify-content:center">'+''.join(ch(c,t,36,'6px 18px') for c,t in s['chips'])+'</div>',st,pills=True)
    by=670; bh=318; k=len(S)
    pain=d['pain']; pw=190
    o+=stp(glass(90,by,880,bh,'',r=56),k+1)
    for i,(f,lab) in enumerate(pain):
        x=120+i*(pw+20); o+=stp(pic(x+20,by+28,150,150,f,26,fit='contain'),k+1)+stp(f'<div class="a" style="left:{x}px;top:{by+192}px;width:{pw}px;display:flex;justify-content:center">{ch("c3",lab,36,"4px 18px")}</div>',k+1)
    o+=stp(f'<div class="a mu" style="left:120px;top:{by+250}px;width:820px;font-size:34px">Where does it hurt?</div>',k+1)
    V=d['verbs']; vw=130
    o+=stp(glass(1000,by,830,bh,'',r=56),k+2)
    for i,(f,t) in enumerate(V):
        x=1034+i*(vw+28); o+=stp(pic(x,by+40,vw,vw,f,26,fit='contain'),k+2)+stp(f'<div class="a" style="left:{x-10}px;top:{by+190}px;width:{vw+20}px;display:flex;justify-content:center">{ch("c2",t,38,"4px 16px")}</div>',k+2)
    o+=stp(f'<div class="a mu" style="left:1034px;top:{by+250}px;width:780px;font-size:34px">What did you do?</div>',k+2)
    return o


CNX=['#7b3cf0','#17b890','#ff9f1c','#ff4f7a']
def connect_html(d,sid):
    """Three columns (yesterday / now / after). Tap a tile in one column, then its partner in another: they slide onto one row and an arrow draws.
    {'rows':[{'cause':f,'now':f,'adv':f,'c':[(cls,t)],'n':[(cls,t)],'a':[(cls,t)]}]}"""
    R=d['rows']; n=len(R); W,ROW,TOP,TH=480,186,236,168; X=[90,720,1350]
    ordr=[[(i+c)%n for i in range(n)] for c in range(3)]
    o=header(d['phase'],d.get('title'))
    for c,(g,t) in enumerate([('rose','yesterday'),('sky','now'),('teal','after')]):
        o+=f'<div class="a" style="left:{X[c]}px;top:172px;width:{W}px;display:flex;justify-content:center">{grad_chip(g,t,40,"6px 40px")}</div>'
    o+=f'<svg id="cv-{sid}" style="position:absolute;left:0;top:0;width:1920px;height:1080px;pointer-events:none;z-index:1;overflow:visible"><defs>'+''.join(f'<marker id="ah{sid}{i}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4.2" markerHeight="4.2" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="{CNX[i%4]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></marker>' for i in range(n))+f'<filter id="rf{sid}" x="-5%" y="-30%" width="110%" height="160%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="3"/></filter></defs><g id="ag-'+sid+f'" filter="url(#rf{sid})"></g></svg>'
    keys=['cause','now','adv']; sk=['c','n','a']
    for c in range(3):
        for slot,i in enumerate(ordr[c]):
            r=R[i]
            o+=(f'<div class="cn" data-c="{c}" data-id="{i}" style="left:{X[c]}px;top:{TOP+slot*ROW}px">'
                +pic(12,12,TH-24,TH-24,r[keys[c]],34)
                +'<div class="tx">'+''.join(ch(a,b,38,'6px 18px') for a,b in r[sk[c]])+'</div></div>')
    o+=f'<div class="gl cfull" id="cf-{sid}" style="left:90px;top:800px;width:1620px;height:216px;border-radius:60px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;opacity:0"></div>'
    L=lambda cs:'<div style="display:flex;gap:12px">'+''.join(ch(a,b,38,'2px 18px') for a,b in cs)+'</div>'
    o=o.replace('opacity:0"></div>','opacity:0">'+''.join(f'<div class="fl" data-id="{i}" style="opacity:0;transition:opacity .4s;display:flex;gap:12px;justify-content:center">'+L(R[i]['n']+[('c4','because')]+R[i]['c'])[len('<div style="display:flex;gap:12px">'):-6]+'</div>' for i in range(n))+'</div>',1)
    full=[]
    import json as _j
    o+=f'<script type="application/json" id="d-{sid}">{_j.dumps({"n":n,"full":full,"col":CNX,"row":ROW,"top":TOP,"x":X,"w":W,"h":TH})}</script>'
    return o

@module('connect')
def connect(d): return connect_html(d,'x')


@module('make_patient')
def make_patient(d):
    """Groups invent a patient: pick a pain and a secret cause from picture banks, then fill the handover frame.
    {'phase':'ACTIVATE','title':'Make a patient','pains':[files],'causes':[files],'frame':[[chips],[chips]]}"""
    out=header(d['phase'],d.get('title','Make a patient'),'violet')
    P=d['pains']; C=d['causes']; COL={'c1':'#34d0f2','c2':'#9a5cff','c3':'#ff7a3c','c4':'#ffb21f'}
    out+=stp(f'<div class="a" style="left:90px;top:158px">{ch("c4","Where does it hurt?",54,"6px 34px")}</div>',1,'p')
    w=int((1740-3*40)/4)
    for k,f in enumerate(P): out+=stp(art(90+k*(w+40),240,w,230,f,r=44,label=f,fit='contain'),1,'p')
    out+=stp(f'<div class="a" style="left:90px;top:488px">{ch("c4","Why?",54,"6px 34px")}</div>',2,'c')
    w2=int((1740-4*30)/5)
    for k,f in enumerate(C): out+=stp(art(90+k*(w2+30),570,w2,230,f,r=44,label=f,fit='contain'),2,'c')
    out+=stp('<div class="gl" style="left:90px;top:826px;width:1740px;height:170px;border-radius:72px"></div>',3,'f')
    for r,row in enumerate(d.get('frame',[])):
        out+=stp(f'<div class="a" style="left:150px;top:{840+r*72}px;display:flex;gap:14px;align-items:center">'+''.join(ch(c,t,40,'2px 22px') if t else gap(COL[c],150,'…',h=56,fs=34) for c,t in row)+'</div>',3,'f')
    return out
