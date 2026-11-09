"""Investigation modules (Lesson 2 'case file'): case_cover, evidence_board, cast, verb_pairs, timeline, sound_sort,
role_cards, match_pairs, spot_fib, solved_board, closing.
BEHAVIOUR (interactive, later): reveals are tap-to-open ('open' sfx, mo-chip); drag to place ('pop'/'tick'); wrong -> 'boop' + return;
solved board stamps with 'done'; calm mode mutes. Static fallback = these slides."""
from ..core import *
def tilt(html,deg,cx,cy): return f'<div style="position:absolute;left:0;top:0;width:1920px;height:1080px;transform:rotate({deg}deg);transform-origin:{cx}px {cy}px">{html}</div>'
def pill(txt,x,y,fs=40,g='violet'): return f'<div class="chip" style="position:absolute;left:{x}px;top:{y}px;font-size:{fs}px;padding:10px 40px;border-radius:999px;background:{GRAD.get(g,g)}">{txt}</div>'
def question(x,y,q,rest,fs=60):
    return f'<div class="gl" style="left:{x}px;top:{y}px;height:130px;width:auto;padding:0 34px 0 28px;border-radius:999px;display:flex;align-items:center;gap:20px;font-family:O;font-weight:800;font-size:{fs}px"><span class="chip c4" style="font-size:{fs}px;padding:6px 34px;border-radius:999px">{q}</span>{rest}</div>'

@module('case_cover')
def case_cover(d):
    return (f'<div class="tag" style="font-size:30px">{d.get("kicker","A2 · NURSING ENGLISH")}</div>'
      +f'<div class="a h grad" style="left:104px;top:210px;font-size:168px;line-height:.98">{d["title"]}</div>'
      +f'<div class="a mu" style="left:118px;top:800px;font-size:50px">{d.get("sub","")}</div>'
      +'<div class="a" style="left:110px;top:900px;display:flex;gap:20px">'+''.join(f'<span class="pill {"" if i==0 else "mu"}" style="font-size:36px;padding:12px 38px;{"color:#6a35e8" if i==0 else ""}">{t}</span>' for i,t in enumerate(['Engage','Study','Activate']))+'</div>'
      +tilt(glass(1250,130,520,780,'',r=48)+f'<div class="a" style="left:1250px;top:130px;width:520px;height:90px;border-radius:48px 48px 0 0;background:{GRAD["amber"]}"></div>',4,1510,520)
      +em('detective',1330,250,360,-6)+em('stethoscope',1500,560,240,14)+em('thermometer',1300,640,200,-14))

@module('evidence_board')
def evidence_board(d):
    out=header(d['phase'],d.get('title','The patient'),'amber')+art(90,190,700,700,d['patient'],r=56,label='patient picture')
    out+=pill('Clues',860,190,40,'amber')
    for i,c in enumerate(d['clues']):
        x=860+i*330; out+=tilt(art(x,270,300,300,c,r=40,label=c),(-4,3,-2)[i%3],x+150,420)+tilt(num(x+10,236,i+1,64),0,0,0)
    out+=question(860,700,*d.get('question',('What','happened?')))
    return out

@module('cast')
def cast(d):
    """Click 1: picture appears. Click 2: its label pill pops in. Repeat for each item."""
    n=len(d['items']); w=int((1740-30*(n-1))/n); out=header(d['phase'],d.get('title'),d.get('grad','amber'))
    for i,it in enumerate(d['items']):
        x=90+i*(w+30); out+=stp(art(x,170,w,640,it['pic'],r=48,label=it['pic'],fit=it.get('fit','cover')),2*i+1)
        out+=stp(f'<div class="a" style="left:{x}px;top:830px;width:{w}px;display:flex;justify-content:center">{grad_chip(it.get("grad","amber"),it["label"],44,"10px 40px")}</div>',2*i+2,pills=True)
        if it.get('cap'): out+=stp(f'<div class="a mu" style="left:{x}px;top:925px;width:{w}px;text-align:center;font-size:34px">{it["cap"]}</div>',2*i+2)
    return out

@module('verb_pairs')
def verb_pairs(d):
    """One picture, then its 'now' pill, then arrow + past pill, one item at a time. The arrow sits midway between the two pills."""
    R=d['rows']; n=len(R); w=min(400,int((1740-30*(n-1))/n)); gx=int((1740-w*n)/(n-1)) if n>1 else 0
    x0=90+(1740-(w*n+gx*(n-1)))//2
    fs=max(44,int(w*.17)); nh=int(fs*1.35)+16; ah=64; gp=22
    out=header(d['phase'],d.get('title','Yesterday'),d.get('grad','violet'))
    for i,r in enumerate(R):
        x=x0+i*(w+gx); y=190+w+36; b=3*i
        out+=stp(art(x,190,w,w,r['pic'],r=48,label=r['pic'],fit='contain'),b+1)
        out+=stp(f'<div class="a" style="left:{x}px;top:{y}px;width:{w}px;display:flex;justify-content:center">{ch("c2",r["now"],fs,"8px 30px")}</div>',b+2,pills=True)
        out+=stp(f'<div class="a" style="left:{x}px;top:{y+nh+gp}px;width:{w}px;display:flex;justify-content:center"><svg width="46" height="{ah}" viewBox="0 0 46 64"><path d="M23 4 L23 52 M7 36 L23 54 L39 36" fill="none" stroke="#9a5cff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg></div>',b+3)
        out+=stp(f'<div class="a" style="left:{x}px;top:{y+nh+gp+ah+gp}px;width:{w}px;display:flex;justify-content:center">{grad_chip("violet",r["then"],int(fs*1.15),"10px 36px")}</div>',b+3,pills=True)
    return out

@module('timeline')
def timeline(d):
    P=d['pics']; n=len(P); order=d.get('order',list(range(n))); w=min(330,int((1740-40*(n-1))/n)); gx=int((1740-w*n)/(n-1)) if n>1 else 0
    out=header(d['phase'],d.get('title','What happened first?'),'amber')
    for k,idx in enumerate(order):
        x=90+k*(w+gx); out+=tilt(art(x,170,w,w,P[idx],r=44,label=P[idx]),(-3,2,-2,3)[k%4],x+w//2,180+w//2)
    sy=170+w+80
    for k in range(n):
        x=90+k*(w+gx)
        out+=f'<div class="a" style="left:{x}px;top:{sy}px;width:{w}px;height:{w}px;border-radius:44px;border:5px dashed #b9a6f5;background:rgba(255,255,255,.4);display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:120px;color:#b9a6f5">{k+1}</div>'
    return out

DOTS={'dot1':'●','dot2':'● ●','buzz':'〰'}
@module('sound_sort')
def sound_sort(d):
    B=d['bags']; n=len(B); w=int((1740-40*(n-1))/n); out=header(d['phase'],d.get('title','Listen. Which sound?'),'orange')
    for i,b in enumerate(B):
        x=90+i*(w+40); out+=glass(x,170,w,560,'',r=64)
        out+=f'<div class="a" style="left:{x}px;top:200px;width:{w}px;text-align:center;font-family:O;font-weight:800;font-size:150px;color:#6a35e8">{DOTS[b["icon"]]}</div>'
        words=b['words'] if d.get('solved') else []
        out+=f'<div class="a" style="left:{x+30}px;top:470px;width:{w-60}px;display:flex;flex-direction:column;gap:16px;align-items:center">'+''.join(ch('c2',t,60,'8px 36px') for t in words)+'</div>'
        if not words: out+=f'<div class="a" style="left:{x+80}px;top:520px;width:{w-160}px;height:140px;border-radius:44px;border:5px dashed #b9a6f5"></div>'
    if not d.get('solved'):
        out+='<div class="gl" style="left:90px;top:790px;width:1740px;height:190px;border-radius:80px;display:flex;align-items:center;gap:26px;padding:0 60px">'+''.join(ch('c2',t,64,'10px 40px') for b in B for t in b['words'])+'</div>'
    else:
        out+='<div class="a mu" style="left:110px;top:800px;font-size:44px">tap · hand on throat · clap clap</div>'
    return out

@module('role_cards')
def role_cards(d):
    """Three role cards: picture, name, job, then the sentence that role says (chips inside the card)."""
    C=d['cards']; n=len(C); w=int((1740-40*(n-1))/n); out=header(d['phase'],d.get('title'),d.get('grad','amber'))
    for i,c in enumerate(C):
        x=90+i*(w+40); out+=stp(glass(x,170,w,820,'',r=64),i+1)
        out+=stp(em(c['emoji'],x+w//2-130,215,260),i+1)
        out+=stp(f'<div class="a" style="left:{x}px;top:500px;width:{w}px;display:flex;justify-content:center">{grad_chip(c["grad"],c["name"],64,"12px 56px")}</div>',i+1)
        out+=stp(f'<div class="a mu" style="left:{x}px;top:620px;width:{w}px;text-align:center;font-size:38px">{c["job"]}</div>',i+1)
        if c.get('says'):
            out+=stp(f'<div class="a" style="left:{x+20}px;top:720px;width:{w-40}px;height:230px;display:flex;flex-wrap:wrap;align-content:center;justify-content:center;gap:12px 14px">'+''.join(ch(k,t,46,'8px 24px') for k,t in c['says'])+'</div>',n+1+i,pills=True)
    return out

@module('match_pairs')
def match_pairs(d):
    P=d['pics']; W=d['words']; n=len(P); w=int((1740-40*(n-1))/n); out=header(d['phase'],d.get('title','Match'),'violet')
    for i,p in enumerate(P):
        x=90+i*(w+40); out+=art(x,170,w,w,p,r=44,label=p)+num(x+16,136,i+1,64)
    out+='<div class="gl" style="left:90px;top:%dpx;width:1740px;height:300px;border-radius:72px;display:flex;align-items:center;justify-content:center;gap:36px;padding:0 40px">'%(170+w+60)+''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:14px">{gap("#9a5cff",64,"",h=64)}{ch("c3",t,52,"8px 30px")}</div>' for t in W)+'</div>'
    return out

@module('spot_fib')
def spot_fib(d):
    out=header(d['phase'],d.get('title','True or a fib?'),'red')+art(90,170,820,820,d['pic'],r=56,label=d['pic'])
    for k,(chips_,ok) in enumerate(d['statements']):
        y=200+k*400
        out+=f'<div class="gl" style="left:980px;top:{y}px;width:850px;height:230px;border-radius:70px;display:flex;align-items:center;gap:14px;padding:0 40px;flex-wrap:wrap">'+chips(chips_,50,'8px 26px')+'</div>'
        out+=em('check_mark_button',1100,y+250,110)+em('cross_mark',1260,y+250,110)
    return out

@module('solved_board')
def solved_board(d):
    I=d['items']; n=len(I); w=int((1740-30*(n-1))/n); out=header(d['phase'],d.get('title','Cases solved'),'teal')
    for i,it in enumerate(I):
        x=90+i*(w+30); out+=art(x,170,w,640,it['pic'],r=48,label=it['pic'])
        if it.get('solved'): out+=tilt(em('check_mark_button',x+w-160,640,170),0,0,0)
        else: out+=f'<div class="a" style="left:{x+w-170}px;top:650px;width:150px;height:150px;border-radius:50%;border:6px dashed #b9a6f5;background:rgba(255,255,255,.5)"></div>'
    out+=f'<div class="gl" style="left:90px;top:850px;width:1740px;height:130px;border-radius:65px;display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:56px">{d.get("footer","Every case solved by the class.")}</div>'
    return out

@module('closing')
def closing(d):
    if d.get('stack'):
        return (em(d.get('emoji','waving_hand'),810,120,300,0)
          +f'<div class="a h" style="left:0;right:0;top:440px;text-align:center;font-size:200px;line-height:1;white-space:nowrap">{d["line1"]} <span class="grad">{d["line2"]}</span></div>'
          +f'<div class="a mu" style="left:0;right:0;top:720px;text-align:center;font-size:58px">{d.get("sub","")}</div>')
    return (f'<div class="a h" style="left:0;right:0;top:250px;text-align:center;font-size:150px;line-height:1.08">{d["line1"]}<br><span class="grad">{d["line2"]}</span></div>'
      +f'<div class="a mu" style="left:0;right:0;top:700px;text-align:center;font-size:54px">{d.get("sub","")}</div>'+em(d.get('emoji','detective'),1480,150,250,10))
