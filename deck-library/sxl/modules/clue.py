"""Lesson 3-4 modules (investigation + describing): vol_ladder, dials3, frames3, timetable, reveal  (view modules, stepped reveal);
choice (levelled practice), boss (optional timed challenge), case_board (hands-up approval board).  Plug and play: a lesson is a list of slide dicts.
Any slide dict can carry  levels:[{bronze},{silver},{gold}]  (+ lvl:1-3) to get the medal switch (keys 1/2/3).
Art slots accept an art file name or an emoji (shown on a glass card until Gemini art exists)."""
import json
from ..core import *
from .case import tilt

TEAMS_DEFAULT=[('red','Red','#ff5a6a','#e0304a'),('blue','Blue','#34a0f8','#2a6ae0'),('green','Green','#2bd9b6','#10a98d'),('yellow','Yellow','#ffc13b','#e89200')]

# ---------------- view modules (pieces arrive one at a time; tap to bounce) ----------------
def _clip(f):
    """audio clip -> data URI if the file exists (Nick's own recordings live in work/lesson/audio), else None = silent button"""
    import os,base64
    if not f: return None
    for dd in ('/home/claude/work/lesson/audio/','/home/claude/work/audio/'):
        p=dd+f
        if os.path.exists(p):
            mt='audio/mpeg' if p.endswith('.mp3') else 'audio/wav' if p.endswith('.wav') else 'audio/ogg' if p.endswith('.ogg') else 'audio/mp4'
            return f'data:{mt};base64,'+base64.b64encode(open(p,'rb').read()).decode()
    return None

@module('vol_ladder')
def vol_ladder(d):
    """Eyes-closed volume ladder. {'phase','title','rungs':[text...],'side':text,'emoji':'🙈'}"""
    o=header(d['phase'],d.get('title','Eyes closed. Louder.'),d.get('grad','rose')); R=d['rungs']; n=len(R); Y0=190
    for i,t in enumerate(R):
        fs=50+int(i*46/max(1,n-1)); x=100+i*(62 if n>4 else 80); y=int(Y0)
        nl=t.count('<br>')+1; Y0+=nl*fs*(1.3 if nl>1 else 1.15)+22+(34 if n>4 else 44)
        clip=_clip((d.get('clips') or [None]*n)[i]) if d.get('clips') else None
        btn=(f'<button class="vsp{"" if clip else " mute"}" data-a="{clip or ""}" style="width:{fs+40}px;height:{fs+40}px"><i class="sico"></i></button>' if d.get('clips') else '')
        o+=stp(f'<div class="a" style="left:{x}px;top:{y}px;display:flex;align-items:center;gap:26px">{grad_chip("violet" if i<n-1 else "rose",t,fs,"8px 40px")}{btn}</div>',i+1,pills=True)
    o+=stp(glass(1180,190,650,640,f'<div style="font-size:150px;text-align:center;margin-top:20px">{('<img src="'+ART+d['emoji']+'" style="width:300px;height:300px;object-fit:contain;border-radius:36px;background:#fff">') if _isart(d.get('emoji')) else d.get("emoji","🙈")}</div><div style="font-family:P;font-weight:500;font-size:42px;line-height:1.45;padding:10px 46px;text-align:center">{d["side"]}</div>',r=56),n+1)
    return o

@module('dials3')
def dials3(d):
    """The dials. {'phase','title','dials':[(letter,name,colour,'ex · ex · ex'),...],'note'}"""
    D=d['dials']; n=len(D); w=int((1740-30*(n-1))/n); o=header(d['phase'],d.get('title','The dials'),'violet')
    for i,(L,name,col,ex) in enumerate(D):
        x=90+i*(w+30); lines=''.join(f'<div style="margin:22px 0;font-family:P;font-weight:500;font-size:46px;line-height:1.25">{e}</div>' for e in ex.split(' · '))
        card=glass(x,190,w,640,'',r=56)+f'<div class="a" style="left:{x}px;top:190px;width:{w}px;height:210px;border-radius:56px 56px 0 0;background:{col}"></div>'
        card+=f'<div class="a" style="left:{x+34}px;top:226px;width:{w-68}px;font-family:O;font-weight:800;font-size:{46 if len(name)<18 else 40}px;color:#fff;line-height:1.05">{name}</div>'
        card+=num(x+34,330,L,76)+f'<div class="a" style="left:{x+34}px;top:430px;width:{w-68}px">{lines}</div>'
        o+=stp(card,i+1)
    if d.get('note'): o+=stp(f'<div class="a mu" style="left:90px;top:858px;width:1740px;text-align:center;font-size:38px">{d["note"]}</div>',n+1)
    return o

@module('frames3')
def frames3(d):
    """Sentence frames. {'phase','title','groups':[{'t','c','l':[lines],'fs'}],'note','write':bool}"""
    G=d['groups']; n=len(G); w=int((1740-30*(n-1))/n); o=header(d['phase'],d.get('title','Say it'),d.get('grad','teal')); h=d.get('h',560 if d.get('write') else (670 if d.get('note') else 745))
    if d.get('chips'):
        CH={'s':('linear-gradient(135deg,#33d1f7,#2b8fef)','#fff'),'v':('linear-gradient(135deg,#9a5cff,#6a35e8)','#fff'),'o':('linear-gradient(135deg,#ff9a4d,#ff4f8b)','#fff'),'b':('linear-gradient(135deg,#ffd21f,#ffa63a)','#3a2400'),'t':('linear-gradient(135deg,#ff8fb5,#e0306a)','#fff')}
        BH=232; GP=20
        for i,g in enumerate(G):
            y=172+i*(BH+GP); ic,_,lab=g['t'].partition(' ')
            rows=''.join(('<div' if j==0 else '<div data-s="%d"'%(3*i+j+1))+' style="flex:1;min-height:0;border-radius:999px;background:rgba(255,255,255,.62);border:3px solid #fff;display:flex;align-items:center;gap:12px;padding:0 30px;box-shadow:0 6px 16px rgba(60,30,140,.10)">'+''.join(f'<span style="padding:4px 24px 6px;border-radius:999px;background:{CH[k][0]};color:{CH[k][1]};font-family:O;font-weight:800;font-size:35px;white-space:nowrap;box-shadow:0 5px 10px rgba(60,30,140,.18)">{w_}</span>' for w_,k in row)+'</div>' for j,row in enumerate(d['chips'][i]))
            body=(f'<div style="height:100%;box-sizing:border-box;display:flex;align-items:center;gap:30px;padding:18px 28px">'
                  f'<div style="flex:none;width:230px;text-align:center"><div style="display:inline-block;width:104px;height:104px;border-radius:50%;background:#fff;font-size:66px;line-height:104px;box-shadow:0 8px 20px rgba(60,30,140,.18)">{ic}</div><div style="margin-top:8px">{grad_chip(g.get("c","violet"),lab,38,"4px 26px")}</div></div>'
                  f'<div style="flex:1;align-self:stretch;display:flex;flex-direction:column;gap:10px">{rows}</div></div>')
            o+=stp(glass(90,y,1740,BH,body,r=56),3*i+1)
        if d.get('note'): o+=stp(f'<div class="a mu" style="left:90px;top:{172+3*(BH+GP)-6}px;width:1740px;text-align:center;font-size:30px">{d["note"]}</div>',10)
        return o
    if d.get('bubbles'):
        AC={'teal':'#10a98d','sky':'#4f86f0','rose':'#e0306a','amber':'#e8a21a','violet':'#7a45f0'}; nr=max(len(g['l']) for g in G); bh=int((h-330-(nr-1)*18)/nr)
        for i,g in enumerate(G):
            x=90+i*(w+30); ic,_,lab=g['t'].partition(' ')
            o+=glass(x,180,w,h,f'<div style="text-align:center;padding-top:26px"><div style="display:inline-block;width:130px;height:130px;border-radius:50%;background:#fff;font-size:84px;line-height:130px;box-shadow:0 10px 24px rgba(60,30,140,.18)">{ic}</div><div style="margin-top:14px">{grad_chip(g.get("c","violet"),lab,46,"6px 34px")}</div></div>',r=52)
        for r_ in range(nr):
            row=''
            for i,g in enumerate(G):
                if r_>=len(g['l']): continue
                x=90+i*(w+30); c=AC.get(g.get('c'),'#7a45f0'); fs=g.get('fs',40)-8; y=180+330+r_*(bh+18)
                row+=f'<div class="a" style="left:{x+22}px;top:{y}px;width:{w-44}px;height:{bh}px;box-sizing:border-box;border-radius:30px;background:#fff;border:5px solid {c};box-shadow:0 8px 20px rgba(60,30,140,.16);display:flex;align-items:center;padding:0 22px;font-family:P;font-weight:500;font-size:{fs}px;line-height:1.25">{g["l"][r_]}</div><div class="a" style="left:{x+70}px;top:{y-16}px;width:0;height:0;border-left:16px solid transparent;border-right:16px solid transparent;border-bottom:18px solid {c}"></div>'
            o+=stp(f'<div class="a" style="left:0;top:0">{row}</div>',r_+1)
        k=nr+1
        if d.get('note'): o+=stp(f'<div class="a mu" style="left:90px;top:{180+h+30}px;width:1740px;text-align:center;font-size:34px">{d["note"]}</div>',k)
        return o
    for i,g in enumerate(G):
        x=90+i*(w+30); fs=g.get('fs',40)
        body=f'<div style="padding:30px 34px;height:{h}px;box-sizing:border-box;display:flex;flex-direction:column;align-items:flex-start">{grad_chip(g.get("c","violet"),g["t"],44,"6px 30px")}<div style="flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:20px;align-self:stretch">'+''.join(f'<div style="margin:18px 0 0;font-family:P;font-weight:500;font-size:{fs}px;line-height:1.3">{l}</div>' for l in g['l'])+'</div></div>'
        o+=stp(glass(x,180,w,h,body,r=52),i+1)
    k=n+1
    if d.get('write'):
        wy=180+h+30+(56 if d.get('note') else 0)
        o+=stp(f'<div class="gl" style="left:90px;top:{wy}px;width:1740px;height:{915-wy}px;border-radius:48px;padding:14px"><textarea placeholder="Write it down…" style="width:100%;height:100%;border:0;background:transparent;font-family:P;font-weight:500;font-size:40px;resize:none;outline:none"></textarea></div>',k);k+=1
    if d.get('note'): o+=stp(f'<div class="a mu" style="left:90px;top:{180+h+30}px;width:1740px;text-align:center;font-size:34px">{d["note"]}</div>',k)
    return o

@module('timetable')
def timetable(d):
    """Silent timetable. {'phase','title','days':[..],'rows':[(emoji,[cell...])],'note'}"""
    days=d['days']; R=d['rows']; n=len(days); cw=int((1740-170)/n); o=header(d['phase'],d.get('title','A week'),'amber')
    o+=''.join(f'<div class="a" style="left:{260+i*cw}px;top:170px;width:{cw-14}px;text-align:center">{grad_chip("sky",t,38,"4px 24px")}</div>' for i,t in enumerate(days))
    rh=int(min(300 if len(R)<=2 else 190,(860-230)/len(R))); big=rh>=250
    for r,(lab,cells) in enumerate(R):
        y=230+r*rh; row=glass(90,y,150,rh-16,f'<div style="font-size:{110 if big else 74}px;text-align:center;line-height:{rh-16}px">{lab}</div>',r=40)
        row+=''.join(glass(260+i*cw,y,cw-14,rh-16,f'<div style="font-family:O;font-weight:800;font-size:{(84 if big else 46) if len(str(c))<8 else (62 if big else 36)}px;text-align:center;line-height:{rh-16}px">{c}</div>',r=36) for i,c in enumerate(cells))
        o+=stp(row,r+1)
    if d.get('note'): o+=stp(f'<div class="a mu" style="left:90px;top:{230+rh*len(R)+4}px;width:1740px;text-align:center;font-size:36px">{d["note"]}</div>',len(R)+1)
    return o

@module('reveal')
def reveal(d):
    """The answer. {'phase','title','pic':emoji|art,'answer','note','grad'}"""
    o=header(d['phase'],d.get('title','The answer'),'teal')
    o+=stp(picx(d['pic'],110,190,640,640,56),1)
    o+=stp(f'<div class="a" style="left:830px;top:300px">{grad_chip(d.get("grad","teal"),d["answer"],140,"14px 60px")}</div>',2,pills=True)
    if d.get('note'): o+=stp(glass(830,520,1000,{210 if len(d["note"])<60 else 310},f'<div style="height:100%;display:flex;align-items:center;padding:0 44px;box-sizing:border-box;font-family:O;font-weight:800;font-size:{54 if len(d["note"])<60 else 42}px;line-height:1.3">{d["note"]}</div>',r=52),3)
    return o

# ---------------- choice: levelled one-at-a-time practice ----------------
def choice_html(d,sid):
    """{'phase','title','hint','items':[{'pic','q','say'?,'opts':[...],'ans':text}]}   put levels:[...] on the slide for medals.  say = patient quote shown in a stickman speech bubble"""
    I=d['items']; n=len(I); o=header(d['phase'],d.get('title','Choose'),d.get('grad','violet'))
    o+=f'<div class="a" style="right:{(130 if d.get("_lvg") else 90)}px;top:60px;display:flex;gap:12px">'+''.join(f'<span class="chd" style="width:26px;height:26px;border-radius:50%"></span>' for _ in I)+'</div>'
    import random
    for k,it in enumerate(I):
        rest=[t for t in it['opts'] if t!=it['ans']]; random.Random(k*7+len(it['q'])).shuffle(rest); rest.insert((k*2+len(d.get('title','')))%len(it['opts']),it['ans']); it=dict(it,opts=rest)
        o+='<div class="chi" style="display:none">'
        if it.get('say') and it.get('grid') and (it.get('aud') or d.get('aud')):
            cells=''.join(f'<div style="text-align:center"><div style="font-family:O;font-weight:800;font-size:28px;color:#6a35e8">{a_}</div><div style="font-size:{it.get("gfs",48)}px;line-height:1.2;margin-top:8px">{b_}</div></div>' for a_,b_ in it['grid'])
            o+=glass(90,180,630,750,f'<div style="height:100%;display:flex;flex-direction:column;justify-content:center;gap:70px;padding:0 14px"><div class="caud" data-say="{it["say"]}" style="margin:0 24px;padding:48px 20px;border-radius:48px;background:#fff;border:5px solid #d9c8ff;text-align:center;font-family:O;font-weight:800;font-size:54px;cursor:pointer"><i class="sico"></i> Tap to listen</div><div style="display:flex;justify-content:space-around;align-items:flex-start">{cells}</div></div>',r=56)
        elif it.get('say') and (it.get('aud') or d.get('aud')):
            sv=(f'<svg viewBox="0 0 630 750" width="630" style="display:block"><rect x="24" y="26" width="582" height="704" rx="44" fill="#fff"/><image href="{ART}{it["pic"]}" x="40" y="170" width="550" height="560" preserveAspectRatio="xMidYMid meet"/>{bubble_svg(52,44,170,120,"",fs=72,tx=120)}{spkg(52+170/2,44+120/2,84)}</svg>' if _isart(it.get("pic")) else f'<svg viewBox="0 0 630 750" width="630" style="display:block">{bubble_svg(110,250,170,120,"",fs=72,tx=200)}{spkg(110+170/2,250+120/2,84)}{stick(230,715,1.85,"hold")}<text x="395" y="600" font-size="150">{it.get("pic","")}</text></svg>')
            o+=glass(90,180,630,750,sv,r=56)+f'<div class="caud" data-say="{it["say"]}" style="position:absolute;left:{(130 if _isart(it.get('pic')) else 190)}px;top:{(214 if _isart(it.get('pic')) else 420)}px;width:230px;height:170px;z-index:4;cursor:pointer;border-radius:40px"></div>'
        elif it.get('say'):
            sv=(f'<svg viewBox="0 0 630 750" width="630" style="display:block"><rect x="24" y="26" width="582" height="704" rx="44" fill="#fff"/><image href="{ART}{it["pic"]}" x="40" y="170" width="550" height="560" preserveAspectRatio="xMidYMid meet"/>{bubble_svg(40,40,550,200,it["say"],fs=42,tx=215)}</svg>' if _isart(it.get("pic")) else f'<svg viewBox="0 0 630 750" width="630" style="display:block">{bubble_svg(24,26,582,290,it["say"],fs=42,tx=230)}{stick(230,715,1.85,"hold")}<text x="395" y="600" font-size="150">{it.get("pic","")}</text></svg>')
            o+=glass(90,180,630,750,sv,r=56)
        elif it.get('grid'):
            cells=''.join(f'<div style="text-align:center"><div style="font-family:O;font-weight:800;font-size:26px;color:#6a35e8">{a_}</div><div style="font-size:{it.get("gfs",48)}px;line-height:1.25;margin-top:6px">{b_}</div></div>' for a_,b_ in it['grid'])
            o+=glass(90,180,630,750,f'<div style="height:100%;display:flex;flex-direction:column;justify-content:center;gap:48px;padding:0 14px"><div style="text-align:center;font-size:90px">{it.get("pic","")}</div><div style="display:flex;justify-content:space-around;align-items:flex-start">{cells}</div></div>',r=56)
        else: o+=picx(it.get('pic','❓'),90,180,630,750,56)
        NO=len(it['opts']);QH=250 if NO<5 else 170
        o+=f'<div class="gl" style="left:770px;top:180px;width:1060px;height:{QH}px;box-sizing:border-box;border-radius:48px;padding:0 40px;display:flex;align-items:center;font-family:O;font-weight:800;font-size:40px;line-height:1.2;position:absolute">{it["q"]}</div>'
        o+=f'<div class="a cho-wrap" style="left:770px;top:{180+QH+22}px;width:1060px;height:{750-QH-22}px;display:flex;flex-direction:column;gap:22px">'+''.join(f'<button class="cho" data-ok="{1 if t==it["ans"] else 0}" style="font-size:{40 if NO<5 else 34}px;line-height:1.15;padding:0 44px;flex:1;min-height:0;display:flex;align-items:center">{t}</button>' for t in it['opts'])+'</div></div>'
    return o
BUILD_EXT['choice']=choice_html
# ---------------- task_card: one team task shown in lesson style, answers visible (review) ----------------
@module('task_card')
def task_card(d):
    """{'phase','team':'Red','tg':gradient,'r':1,'t':{lab,ic,who,card,key,stretch,w},'unlock':'text','pic':emoji}"""
    t=d['t']; o=header(d.get('phase','ACTIVATE'),f"{d['team']} team · round {d['r']}",d.get('tg','violet'))
    o+=picx(d.get('pic','❓'),90,190,420,300,56)
    o+=f'<div class="a" style="left:90px;top:510px;width:420px;text-align:center">{grad_chip(d.get("tg","violet"),t["ic"]+" "+t["lab"],40,"8px 26px")}</div>'
    n=len(t['card']); fs=46 if n<150 else 40 if n<230 else 34
    o+=glass(560,190,1270,350,f'<div style="height:100%;box-sizing:border-box;display:flex;align-items:center;padding:20px 44px;font-family:P;font-weight:500;font-size:{fs}px;line-height:1.4"><div>{t["card"].replace(chr(10),"<br>")}</div></div>',r=52)
    o+=f'<div class="a mu" style="left:560px;top:556px;width:1270px;font-size:30px">{t["who"]} · {"say it, then write it down" if t["w"] else "aloud only"}</div>'
    o+=stp(glass(560,620,1270,150,f'<div style="padding:24px 44px;font-family:O;font-weight:800;font-size:40px;line-height:1.25;color:#0b6b55">✔ Answer: {t["key"]}</div>',r=44,ex='background:linear-gradient(135deg,#d6fbea,#c4f3e6)'),1)
    if t.get('stretch'): o+=stp(glass(560,790,1270,110,f'<div style="padding:20px 44px;font-family:P;font-weight:500;font-size:34px">⭐ Stretch: {t["stretch"]}</div>',r=44,ex='background:linear-gradient(135deg,#fff3c4,#ffe7a8)'),2)
    o+=stp(glass(90,570,420,330,f'<div style="padding:20px 24px;font-family:P;font-weight:500;font-size:{28 if len(d["unlock"])<90 else 21}px;line-height:1.3"><b style="font-family:O">Unlocks</b><br>{d["unlock"]}</div>',r=44),3)
    return o

# ---------------- teach: watch, listen, repeat (no tapping to answer, nothing to get wrong) ----------------
def _isart(p): return isinstance(p,str) and '.' in p and len(p)<48 and p.rsplit('.',1)[-1] in ('jpg','png','jpeg')
def _artimg(p,r=40,fit='cover'):
    if p.startswith('L6_'): fit='contain'
    return f'<img src="{ART}{p}" style="width:100%;height:100%;object-fit:{fit};border-radius:{r}px;display:block;background:#fff">'

def _ul(t):
    import re
    return re.sub(r'\[\[(.+?)\]\]',r'<span class="ulw">\1</span>',t)

@module('teach')
def teach(d):
    """{'phase','role','pic':emoji|art,'lines':[...]} or {'words':[(emoji,word),...]}.
    line = 'text' | (answer, patient_line)  -> three taps: audio, patient text, answer | {'t':text,'c':'amber'|'teal'}.
    [[word]] gets an animated underline when its line appears. tts=True: tap a line to hear it."""
    tts=d.get('tts',False)
    o=header(d.get('phase','STUDY'),d.get('role','Watch · listen · repeat'),'violet')
    if d.get('words'):
        C=d['words']; n=len(C); w=int((1740-30*(n-1))/n)
        for i,(e,t) in enumerate(C):
            x=90+i*(w+30); sa=f' data-say="{t}"' if tts else ''
            ea=(f'<div style="position:absolute;left:18px;right:18px;top:18px;bottom:150px;border-radius:42px;overflow:hidden">{_artimg(e,42)}</div>' if _isart(e) else f'<div style="position:absolute;left:0;right:0;top:90px;text-align:center;font-size:{int(w*.5)}px;line-height:1">{e}</div>')
            o+=stp(f'<div class="gl tch"{sa} style="left:{x}px;top:190px;width:{w}px;height:740px;border-radius:56px">{ea}</div>',2*i+1)
            o+=stp(f'<div class="a" style="left:{x}px;top:{190+740-140}px;width:{w}px;text-align:center;font-family:O;font-weight:800;font-size:68px;line-height:1.1">{_ul(t)}</div>',2*i+2)
    else:
        L=d['lines']; _p0=d.get('pic','❓')
        o+=(f'<div class="gl tpic" style="left:90px;top:190px;width:640px;height:740px;border-radius:56px;display:block;padding:34px;box-sizing:border-box;background:#fff"><img src="{ART}{_p0}" style="width:100%;height:100%;object-fit:contain;display:block"></div>' if _isart(_p0) and _p0.startswith('L6_') else picx(_p0,90,190,640,740,56).replace('class="gl"','class="gl tpic"',1))
        sh=lambda x:(x['t'] if isinstance(x,dict) else x[0] if isinstance(x,(tuple,list)) else x).replace('<span','').replace('</span>','')
        fs=42 if max(len(sh(x)) for x in L)<60 else 38
        BG={'orange':'background:linear-gradient(135deg,#ffe6cc,#ffd2a6)','sky':'background:linear-gradient(135deg,#d9ecff,#c3e0ff)','rose':'background:linear-gradient(135deg,#ffe0ec,#ffcadd)','amber':'background:linear-gradient(135deg,#fff3c4,#ffe7a8)','teal':'background:linear-gradient(135deg,#d6fbea,#c4f3e6)'}
        for i,t in enumerate(L):
            y=190+i*int(740/len(L)); h=int(740/len(L))-26; ex=''
            if isinstance(t,(tuple,list)):
                body=f'<div style="flex:1;display:flex;align-items:center;gap:26px"><span class="sp" style="font-size:64px"><i class="sico"></i></span><div><div class="pt" style="display:none;font-family:P;font-weight:500;font-size:30px;color:#6a35e8;margin-bottom:6px">{t[1]}</div><div class="an" style="display:none">{_ul(t[0])}</div></div></div>'; sa=f' data-say="{t[1]}" data-seq="1"'
            elif isinstance(t,dict): body=('<span style="flex:none;margin-right:26px;padding:6px 22px;border-radius:999px;background:#fff;font-size:30px;color:#6a35e8">'+t['k']+'</span>' if t.get('k') else '')+'<div>'+_ul(t['t'])+'</div>'; sa=''; ex=BG.get(t.get('c'),'')
            else: body='<div>'+_ul(t)+'</div>'; sa=f' data-say="{t}"' if tts else ''
            if d.get('pics'): sa+=f' data-pic="{ART+d["pics"][i] if _isart(d["pics"][i]) else d["pics"][i]}"'
            o+=(lambda h,seq:h if seq else stp(h,i+1))(f'<div class="gl tch"{sa} style="left:780px;top:{y}px;width:1050px;height:{h}px;border-radius:48px;display:flex;align-items:center;padding:0 44px;box-sizing:border-box;font-family:O;font-weight:800;font-size:{fs}px;line-height:1.15;{ex}">{body}</div>',isinstance(t,(tuple,list)))
    if d.get('hint'): o+=f'<div class="a mu" style="left:90px;top:858px;width:1740px;text-align:center;font-size:36px">{d["hint"]}</div>'
    return o

@module('week')
def week(d):
    """Her week, revealed day by day. {'phase','title','days':[{'d','cups','h','says'}]}"""
    o=header(d['phase'],d.get('title','Her week'),d.get('grad','amber')); D=d['days']; n=len(D); w=int((1740-24*(n-1))/n)
    for i,x in enumerate(D):
        cups=''.join('☕' for _ in range(x['cups'])); bar=int(x['h']/9*(w-80))
        body=(f'<div style="text-align:center;padding-top:22px"><span class="chip" style="font-size:34px;padding:6px 30px;border-radius:999px;background:linear-gradient(135deg,#9a5cff,#ff5aa5)">{x["d"]}</span></div>'
          f'<div style="text-align:center;font-size:64px;line-height:1.2;height:170px;margin-top:14px;padding:0 10px">{cups}</div>'
          f'<div style="text-align:center;font-size:44px;margin-top:6px">🌙 <b style="font-family:O">{x["h"]} h</b></div>'
          f'<div style="margin:12px 40px 0;height:22px;border-radius:11px;background:rgba(255,255,255,.7)"><div style="width:{bar}px;height:100%;border-radius:11px;background:linear-gradient(90deg,#ff6b78,#ffb347)"></div></div>'
          f'<div style="margin:22px 22px 0;padding:14px 18px;border-radius:26px;background:#fff;font-family:P;font-weight:500;font-size:30px;line-height:1.25;text-align:center">{x["says"]}</div>')
        o+=stp(glass(90+i*(w+24),200,w,640,body,r=44),i+1)
    return o

@module('rungs')
def rungs(d):
    """Vertical ladder, strongest on top. {'phase','title','stops':[{'word','e','gloss','sen','grad'}] weak->strong,'start'}"""
    S=d['stops']; n=len(S); st=d.get('start',n-1); top0=180; gp=14; rh=int((756-(n-1)*gp)/n); x0=150; w=1040
    T=['#6fd79a','#c7e36a','#ffd25a','#ff9a5a','#ff5a6a']
    o=header(d['phase'],d.get('title','How bad?'),'violet')
    ys=[top0+(n-1-i)*(rh+gp) for i in range(n)]
    for i,s_ in enumerate(S):
        y=ys[i]; c=T[min(i,len(T)-1)]
        o+=(f'<div class="rgr" data-i="{i}" data-y="{y}" style="position:absolute;left:{x0}px;top:{y}px;width:{w}px;height:{rh}px;cursor:pointer;border-radius:{rh//2}px;background:linear-gradient(90deg,{c}88,{c}33);border:5px solid #fff;box-sizing:border-box;display:flex;align-items:center;padding:0 26px;gap:28px;box-shadow:0 10px 24px rgba(60,30,140,.16)">'
            +(f'<span style="flex:none;width:96px;height:96px;border-radius:50%;overflow:hidden;background:#fff;display:block">{_artimg(s_["e"],48)}</span>' if _isart(s_["e"]) else f'<span style="font-size:76px;line-height:1">{s_["e"]}</span>')+f'<span class="chip" style="font-size:46px;padding:6px 32px;border-radius:999px;background:linear-gradient(135deg,{c},{c}cc);color:#1c1b2e;white-space:nowrap">{s_["word"]}</span>'
            f'<span style="margin-left:auto;font-family:O;font-weight:800;font-size:36px;color:#6a35e8;background:rgba(255,255,255,.7);padding:6px 26px;border-radius:999px;white-space:nowrap">{s_["gloss"]}</span></div>')
    o+=f'<div class="rgm" style="position:absolute;left:{x0-10}px;top:{ys[st]-10}px;width:{w+20}px;height:{rh+20}px;border-radius:{rh//2+10}px;border:7px solid #9a5cff;box-shadow:0 0 0 6px rgba(154,92,255,.25),0 14px 34px rgba(106,53,232,.35);pointer-events:none;transition:top .55s cubic-bezier(.3,1.4,.5,1)"></div>'
    o+='<div class="gl" style="left:1230px;top:180px;width:600px;height:756px;border-radius:72px"></div>'
    for i,s_ in enumerate(S):
        o+=(f'<div class="rgp" data-i="{i}" style="position:absolute;left:1230px;top:180px;width:600px;height:756px;opacity:{1 if i==st else 0};transition:opacity .3s;pointer-events:none">'
            +(f'<div style="margin:40px 50px 0;height:430px">{_artimg(s_["e"],44,"contain")}</div>' if _isart(s_["e"]) else f'<div style="text-align:center;font-size:230px;line-height:1;margin-top:70px">{s_["e"]}</div>')
            +(f'<div class="rsy" data-say="{s_["say"]}" style="margin:26px 36px 0;text-align:center;font-family:P;font-weight:500;font-size:30px;color:#6a35e8">{s_["say"]}</div>' if s_.get('say') else '')+f'<div style="margin:22px 40px 0;text-align:center;font-family:O;font-weight:800;font-size:46px;line-height:1.2">{_ul(s_["sen"])}</div></div>')
    return o

def _bp(c,d,fs,gap):
    """bigpic: a clue like '🧴 sun cream' shows the emoji large and the words beside it"""
    if not d.get('bigpic') or ' ' not in c: return c
    e,t=c.split(' ',1)
    return f'<span style="font-size:{fs}px;line-height:1;margin-right:{gap}px">{emo(e)}</span><span>{t}</span>'
def _bp_s(c,d):
    if not d.get('bigpic') or ' ' not in c: return ''
    return f'<span style="font-size:70px;line-height:1;margin-right:22px;flex:none">{emo(c.split(" ",1)[0])}</span>'

@module('pairs')
def pairs(d):
    """Tap a clue, then its sentence. {'phase','title','pairs':[(clue,sentence)],'hint'}"""
    import random
    Pr=d['pairs']; n=len(Pr); o=header(d['phase'],d.get('title','Match'),'violet'); h=int((680-18*(n-1))/n)
    order=list(range(n)); _r=random.Random(len(d.get('title',''))+n); _r.shuffle(order)
    while n>1 and any(order[k]==k for k in range(n)): _r.shuffle(order)
    if d.get('hide'): order=list(range(n))
    PO=bool(d.get('picOnly')); PW=520
    for i,(c_,s_) in enumerate(Pr):
        o+=f'<div class="ptl gl" data-i="{i}"{(' data-say="'+__import__("html").escape(s_,True)+'"') if d.get('listen') else ''}{' data-nz="1"' if (d.get('listen') or d.get('hide')) else ''} style="left:90px;top:{190+i*(h+18)}px;width:{PW if PO else 860}px;height:{h}px;border-radius:44px;cursor:pointer;display:flex;align-items:center;{"justify-content:center;" if PO else ""}padding:0 {10 if PO else 36}px;box-sizing:border-box;font-family:O;font-weight:800;font-size:40px;line-height:1.2;background:{"#fff;border:6px solid #ffd978" if PO else "linear-gradient(135deg,#fff3c4,#ffe7a8)"}">{(f'<span style="font-size:{h-44}px;line-height:1">{emo(c_.split(" ",1)[0])}</span>' if PO else _bp(c_,d,110,34))}</div>'
    for j,i in enumerate(order):
        o+=f'<div class="ptr gl{' hid' if d.get('hide') else ''}" data-i="{i}" style="left:{90+PW+40 if PO else 990}px;top:{190+j*(h+18)}px;width:{1740-PW-40 if PO else 840}px;height:{h}px;border-radius:44px;cursor:pointer;display:flex;align-items:center;padding:0 36px;box-sizing:border-box;font-family:O;font-weight:800;font-size:44px;color:#0b6b55;background:linear-gradient(135deg,#d6fbea,#c4f3e6)">{'' if PO else _bp_s(Pr[i][0],d)}<span class="ptx">{Pr[i][1]}</span></div>'
    if d.get('listen'): o+='<span class="plis" style="display:none"></span>'
    if d.get('ball'): o+=f'<div class="a" style="left:420px;top:884px;font-size:72px;line-height:1;display:flex;align-items:center">{emo("L6_i_throw_ball.png")}</div>'
    if d.get('ball'): o+=f'<div class="a pbn" data-d="{d["hint"]}" style="left:90px;top:890px;width:1740px;text-align:center;font-family:O;font-weight:800;font-size:40px;color:#6a35e8">{d["hint"]}</div>'
    elif d.get('hint'): o+=f'<div class="a mu" style="left:90px;top:895px;width:1740px;text-align:center;font-size:32px">{d["hint"]}</div>'
    return o

@module('planb')
def planb(d):
    """Teacher reference: backup activities. {'phase','title','tiles':[{'e','t','min','use'}]}"""
    o=header(d['phase'],d.get('title','Plan B'),'amber'); T=d['tiles']; n=len(T); cols=3; w=int((1740-30*(cols-1))/cols); h=330
    for i,t in enumerate(T):
        x=90+(i%cols)*(w+30); y=185+(i//cols)*(h+26)
        o+=glass(x,y,w,h,f'<div style="padding:22px 30px"><div style="font-size:64px;line-height:1">{t["e"]} <span style="font-family:O;font-weight:800;font-size:40px;vertical-align:middle">{t["t"]}</span></div><div style="margin-top:12px"><span class="chip" style="font-size:28px;padding:4px 20px;border-radius:999px;background:linear-gradient(135deg,#9a5cff,#ff5aa5)">{t["min"]}</span></div><div style="font-family:P;font-weight:500;font-size:30px;line-height:1.3;margin-top:14px;color:#4a4a62">{t["use"]}</div></div>',r=44)
    return o

@module('room')
def room(d):
    """The room of clues: stickman patient in bed, tap objects to read what they say. {'phase','title','spots':[{'e','x','y','t'}]}"""
    o=header(d['phase'],d.get('title','The room of clues'),d.get('grad','amber'))
    sv=('<svg viewBox="0 0 1740 700" width="1740" style="position:absolute;left:0;top:0">'
     '<rect x="0" y="470" width="1740" height="230" fill="#e8dcc8"/><rect x="330" y="400" width="760" height="150" rx="26" fill="#fff" stroke="#1c1b2e" stroke-width="7"/>'
     '<rect x="330" y="470" width="760" height="85" rx="22" fill="#9ad4ff" stroke="#1c1b2e" stroke-width="7"/><rect x="330" y="400" width="130" height="75" rx="30" fill="#fff" stroke="#1c1b2e" stroke-width="7"/>'
     '<circle cx="395" cy="392" r="42" fill="#fff" stroke="#1c1b2e" stroke-width="7"/><circle cx="380" cy="386" r="5" fill="#1c1b2e"/><circle cx="410" cy="386" r="5" fill="#1c1b2e"/><path d="M382 408 Q395 400 408 408" stroke="#1c1b2e" stroke-width="5" fill="none" stroke-linecap="round"/>'
     '<text x="455" y="370" font-size="48">💦</text><rect x="330" y="555" width="20" height="90" fill="#1c1b2e"/><rect x="1070" y="555" width="20" height="90" fill="#1c1b2e"/>'
     '<path d="M300 130 Q710 -30 1120 130" stroke="#9a5cff" stroke-width="5" fill="none" stroke-dasharray="4 12" stroke-linecap="round"/></svg>')
    if d.get('img'):
        sv=f'<img src="{ART}{d["img"]}" style="position:absolute;left:243px;top:0;width:1254px;height:700px;object-fit:contain">'
    o+=f'<div class="gl room" style="left:90px;top:170px;width:1740px;height:700px;border-radius:56px;overflow:hidden;background:{"#fff" if d.get("img") else "linear-gradient(#f6efe2,#f3e9d6)"}">{sv}'
    for k,sp in enumerate(d['spots']):
        o+=f'<button class="rsp{" rg" if d.get("img") else ""}" data-t="{sp["t"]}" style="left:{sp["x"]}px;top:{sp["y"]}px">{"" if d.get("img") else sp["e"]}</button>'
    o+='</div><div class="a rcap" style="left:90px;top:885px;width:1740px;text-align:center;font-family:O;font-weight:800;font-size:46px;height:56px;color:#1c1b2e"></div>'
    return o

BUILD_EXT['room']=lambda d,sid=None: room(d)

@module('qr_groups')
def qr_groups(d):
    """{'phase','title','qrs':[data-uri x4],'cols':[colour x4]} four big group codes in a row"""
    o=header(d['phase'],d['title'],d.get('grad','rose'))
    W=420; gap=(1740-4*W)//3
    for i,(q,c) in enumerate(zip(d['qrs'],d['cols'])):
        x=90+i*(W+gap)
        inner=(f'<div style="display:flex;flex-direction:column;align-items:center;gap:26px;padding-top:34px">'
               f'<div style="width:150px;height:150px;border-radius:50%;background:{c};color:#fff;font-family:O;font-weight:800;font-size:112px;line-height:150px;text-align:center">{i+1}</div>'
               f'<img data-z="1" src="{q}" style="cursor:zoom-in;width:300px;height:300px;border-radius:22px;image-rendering:pixelated;background:#fff;padding:8px"></div>')
        o+=stp(glass(x,200,W,600,inner,r=56),i+1)
    return o

def audio_all(d,sid=None):
    """{'phase','title','groups':[[{'pic','clip','say'} x3] x4],'cols':[...]} all group voice notes on one page (teacher backup)"""
    o=header(d['phase'],d['title'],d.get('grad','rose'))
    W=420; gap=(1740-4*W)//3
    for i,(g,c) in enumerate(zip(d['groups'],d['cols'])):
        x=90+i*(W+gap)
        btns=''.join(f'<button class="aab" data-clip="{n["clip"]}" data-say="{n["say"]}" style="border-color:{c}"><span class="aap">{n["pic"]}</span><span class="aas" style="background:{c}"><i class="sico" style="filter:invert(1) brightness(2)"></i></span></button>' for n in g)
        inner=(f'<div style="display:flex;flex-direction:column;align-items:center;gap:16px;padding-top:24px">'
               f'<div style="width:110px;height:110px;border-radius:50%;background:{c};color:#fff;font-family:O;font-weight:800;font-size:82px;line-height:110px;text-align:center">{i+1}</div>{btns}</div>')
        o+=glass(x,190,W,800,inner,r=56)
    return o

BUILD_EXT['audio_all']=audio_all

@module('qr_card')
def qr_card(d):
    """{'phase','title','rules':[lines],'qr':data-uri,'url','caption'} rules on the left, QR on the right"""
    o=header(d['phase'],d['title'],d.get('grad','rose'))
    body='<div style="padding:34px 44px">'+''.join(f'<div style="margin:0 0 22px;font-family:O;font-weight:800;font-size:{d.get("fs",44)}px;line-height:1.2">{l}</div>' for l in d['rules'])+'</div>'
    o+=stp(glass(90,180,1030,720,body,r=56),1)
    q=f'<div style="text-align:center;padding-top:34px"><img src="{d["qr"]}" style="width:480px;height:480px;border-radius:24px;image-rendering:pixelated"><div style="font-family:O;font-weight:800;font-size:40px;margin-top:20px">{d.get("caption","Scan to play")}</div><div style="font-family:P;font-size:24px;color:#6a6a7e;margin-top:8px">{d["url"]}</div></div>'
    o+=stp(glass(1160,180,670,720,q,r=56),2)
    return o

def stick(cx,base,sc=1.0,pose='down',col='#1c1b2e'):
    """simple stickman svg group. pose: down|up|throw|hold|point"""
    hy=base-150*sc; r=24*sc; neck=hy+r; hip=base-62*sc; w=7
    arms={'down':[(-34,40),(34,40)],'up':[(-36,-10),(36,-44)],'throw':[(-30,40),(50,-40)],'hold':[(-30,26),(30,26)],'point':[(-30,40),(58,-8)]}[pose]
    sh=neck+22*sc
    g=f'<g stroke="{col}" stroke-width="{w}" stroke-linecap="round" fill="none">'
    g+=f'<circle cx="{cx}" cy="{hy}" r="{r}" fill="#fff"/><line x1="{cx}" y1="{neck}" x2="{cx}" y2="{hip}"/>'
    for dx,dy in arms: g+=f'<line x1="{cx}" y1="{sh}" x2="{cx+dx*sc}" y2="{sh+dy*sc}"/>'
    g+=f'<line x1="{cx}" y1="{hip}" x2="{cx-26*sc}" y2="{base}"/><line x1="{cx}" y1="{hip}" x2="{cx+26*sc}" y2="{base}"/></g>'
    g+=f'<circle cx="{cx-8*sc}" cy="{hy-3*sc}" r="{2.6*sc}" fill="{col}"/><circle cx="{cx+8*sc}" cy="{hy-3*sc}" r="{2.6*sc}" fill="{col}"/><path d="M{cx-8*sc} {hy+9*sc} Q{cx} {hy+15*sc} {cx+8*sc} {hy+9*sc}" stroke="{col}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
    return g

def spkg(cx,cy,sz):
    k=sz/24
    return f'<g transform="translate({cx-12*k+0.7*k},{cy-12*k}) scale({k})"><path d="M3 9v6h4l5 4V5L7 9z" fill="#6a35e8"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.2 5.6a9 9 0 0 1 0 12.8" fill="none" stroke="#6a35e8" stroke-width="2.2" stroke-linecap="round"/></g>'

def bubble_svg(x,y,w,h,text,fs=21,tail='down',tx=None):
    import textwrap
    lines=[]
    for part in text.split('\n'): lines+=textwrap.wrap(part,max(8,int((w-44)/(fs*.54)))) or ['']
    n=len(lines)
    t=''.join(f'<text x="{x+w/2}" y="{y+h/2+(i-(n-1)/2)*fs*1.25+fs*.34}" font-family="Outfit,sans-serif" font-weight="800" font-size="{fs}" text-anchor="middle" fill="#1c1b2e">{l}</text>' for i,l in enumerate(lines))
    tx=tx if tx is not None else x+w/2
    tp=f'<polygon points="{tx-16},{y+h-2} {tx+16},{y+h-2} {tx+4},{y+h+26}" fill="#fff" stroke="#c9b6ff" stroke-width="4"/><rect x="{tx-18}" y="{y+h-8}" width="36" height="9" fill="#fff"/>'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="#fff" stroke="#c9b6ff" stroke-width="4"/>{tp}{t}'

@module('comic')
def comic(d):
    """4-panel stickman comic. {'phase','title','panels':[{'svg':svg-body,'cap':text}]}"""
    o=header(d['phase'],d['title'],d.get('grad','violet')); P=d['panels']; n=len(P); w=int((1740-24*(n-1))/n)
    for i,pn in enumerate(P):
        x=90+i*(w+24)
        panel=(f'<div style="width:{w-30}px;height:{w-30}px;margin:0 auto;border-radius:30px;overflow:hidden;border:4px solid #1c1b2e">{_artimg(pn["img"],26)}</div>' if pn.get('img') else f'<svg viewBox="0 0 400 420" width="{w-30}" style="display:block;margin:0 auto">{pn["svg"]}</svg>')
        body=f'<div style="height:100%;display:flex;flex-direction:column;justify-content:center;gap:24px">{panel}'+(f'<div style="padding:0 22px;text-align:center;font-family:O;font-weight:800;font-size:38px;line-height:1.15">{pn["cap"]}</div>' if pn.get("cap") else '')+'</div>'
        o+=stp(glass(x,d.get('y',190),w,d.get('h',745),body,r=48),i+1)
    return o

def _dial_scene(z):
    """stickman against the green normal line: up on a box / ladder / tower, or down in a dip / hole / well"""
    L=205; off={4:25,5:60,6:100,3:0,2:-25,1:-55,0:-85}[z]; cx=395; g=''
    pit=-off if off<0 else 0
    if pit:
        g+=f'<rect x="0" y="{L}" width="{cx-70}" height="140" fill="#d9c7a6"/><rect x="{cx+70}" y="{L}" width="{790-cx-70}" height="140" fill="#d9c7a6"/><rect x="{cx-70}" y="{L+pit}" width="140" height="140" fill="#d9c7a6"/><line x1="{cx-70}" y1="{L}" x2="{cx-70}" y2="{L+pit}" stroke="#1c1b2e" stroke-width="6"/><line x1="{cx+70}" y1="{L}" x2="{cx+70}" y2="{L+pit}" stroke="#1c1b2e" stroke-width="6"/>'
    else: g+=f'<rect x="0" y="{L}" width="790" height="140" fill="#d9c7a6"/>'
    if off>0:
        g+=f'<rect x="{cx-55}" y="{L-off}" width="110" height="{off}" fill="#ffc13b" stroke="#1c1b2e" stroke-width="6"/>'
        if off>=60:
            g+=f'<line x1="{cx+75}" y1="{L}" x2="{cx+75}" y2="{L-off}" stroke="#1c1b2e" stroke-width="6"/><line x1="{cx+115}" y1="{L}" x2="{cx+115}" y2="{L-off}" stroke="#1c1b2e" stroke-width="6"/>'+''.join(f'<line x1="{cx+75}" y1="{L-t}" x2="{cx+115}" y2="{L-t}" stroke="#1c1b2e" stroke-width="5"/>' for t in range(20,off,28))
    base=L-off if off>0 else L+(-pit if False else pit)
    g+=stick(cx,base,.6,'up' if off>0 or pit else 'down')
    if z==6: g+=f'<text x="{cx+30}" y="{base-95}" font-size="46">💦</text>'
    if z==0: g+=f'<text x="{cx+40}" y="{base-70}" font-size="46">🆘</text>'
    g+=f'<line x1="0" y1="{L}" x2="790" y2="{L}" stroke="#10a98d" stroke-width="7" stroke-dasharray="22 14"/>'
    return g

def _dial_html(d,sid):
    import math,json as _j
    cx,cy,R,r=450,470,430,230; a=180/7
    cols=['#2a3fc4','#4f86f0','#8fc8ff','#2bd9b6','#ffc13b','#ff8a3d','#e0263e']; txt=['#fff','#fff','#1c1b2e','#fff','#1c1b2e','#fff','#fff']
    words=['dangerously','much','slightly','normal','slightly','much','dangerously']
    def pt(rad,th): return cx+rad*math.cos(math.radians(th)),cy-rad*math.sin(math.radians(th))
    sv=''
    if d.get('pics'):
        # arc of picture medallions (the L1 'dial preview' design): one stickman scene per stop, needle points at the stop
        RR=380; sv+='<defs><linearGradient id="dg'+sid+'" x1="0" y1="0" x2="1" y2="0">'+''.join(f'<stop offset="{k_/6:.2f}" stop-color="{c_}"/>' for k_,c_ in enumerate(cols))+'</linearGradient>'
        for i in range(7):
            mx,my=pt(RR,180-(i+.5)*a); sv+=f'<clipPath id="mc{sid}{i}"><circle cx="{mx:.1f}" cy="{my:.1f}" r="64"/></clipPath>'
        sv+='</defs>'
        sx0,sy0=pt(RR,180); sx1,sy1=pt(RR,0)
        sv+=f'<path d="M{sx0:.1f} {sy0:.1f} A{RR} {RR} 0 0 1 {sx1:.1f} {sy1:.1f}" fill="none" stroke="url(#dg{sid})" stroke-width="22" stroke-linecap="round" opacity=".9"/>'
        for i in range(7):
            mx,my=pt(RR,180-(i+.5)*a)
            _pw=150 if i in (0,6) else 108
            _lx_=mx+(34 if i in (1,2) else -34 if i in (4,5) else 0)
            sv+=(f'<g class="dz" data-z="{i}"><circle cx="{mx:.1f}" cy="{my:.1f}" r="72" fill="{cols[i]}"/><circle cx="{mx:.1f}" cy="{my:.1f}" r="64" fill="#fff"/>'
                 f'<g clip-path="url(#mc{sid}{i})"><svg x="{mx-64:.1f}" y="{my-64:.1f}" width="128" height="128" viewBox="235 -25 320 320" preserveAspectRatio="xMidYMid slice"><rect x="0" y="-60" width="790" height="400" fill="#f1ecff"/>{_dial_scene(i)}</svg></g>'
                 f'<rect x="{_lx_-_pw/2:.1f}" y="{my+80:.1f}" width="{_pw}" height="42" rx="21" fill="{cols[i]}"/><text x="{_lx_:.1f}" y="{my+110:.1f}" text-anchor="middle" font-family="Outfit,sans-serif" font-weight="800" font-size="25" fill="{txt[i]}">{words[i]}</text></g>')
    for i in range(0 if d.get('pics') else 7):
        t0,t1=180-i*a,180-(i+1)*a; x0,y0=pt(R,t0); x1,y1=pt(R,t1); x2,y2=pt(r,t1); x3,y3=pt(r,t0); mx,my=pt((R+r)/2,(t0+t1)/2)
        sv+=f'<path class="dz" data-z="{i}" d="M{x0:.1f} {y0:.1f} A{R} {R} 0 0 1 {x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f} A{r} {r} 0 0 0 {x3:.1f} {y3:.1f} Z" fill="{cols[i]}"/>'
        sv+=f'<text x="{mx:.1f}" y="{my+9:.1f}" text-anchor="middle" font-family="Outfit,sans-serif" font-weight="800" font-size="30" fill="{txt[i]}" pointer-events="none">{words[i]}</text>'
    _lx,_hx,_ly=(262,638,522) if d.get('pics') else (70,830,528)
    sv+=f'<text x="{_lx}" y="{_ly}" font-family="Outfit,sans-serif" font-weight="800" font-size="{30 if d.get("pics") else 34}" fill="#2a3fc4">◀ lower</text><text x="{_hx}" y="{_ly}" text-anchor="end" font-family="Outfit,sans-serif" font-weight="800" font-size="{30 if d.get("pics") else 34}" fill="#e0263e">higher ▶</text>'
    sv+=f'<g class="nd" style="transform-origin:{cx}px {cy}px;transform:rotate(-90deg);transition:transform .9s cubic-bezier(.3,1.35,.5,1)"><polygon points="{cx-11},{cy} {cx+11},{cy} {cx},{cy-(215 if d.get('pics') else 395)}" fill="#1c1b2e"/></g><circle cx="{cx}" cy="{cy}" r="30" fill="#1c1b2e"/><circle cx="{cx}" cy="{cy}" r="11" fill="#fff"/>'
    o=header(d['phase'],d.get('title','How much?'),d.get('grad','violet'))
    o+=f'<div class="a" style="right:{130 if d.get("_lvg") else 90}px;top:60px;display:flex;gap:12px">'+''.join('<span class="chd" style="width:26px;height:26px;border-radius:50%"></span>' for _ in d['items'])+'</div>'
    o+=f'<div class="a" style="left:90px;top:185px;width:840px"><svg viewBox="0 0 900 540" width="840">{sv}</svg></div>'
    o+='<div class="gl dcard" style="left:90px;top:725px;width:840px;height:210px;border-radius:48px"></div>'
    o+='<div class="gl dsen" style="left:970px;top:190px;width:860px;height:190px;border-radius:48px"></div>'
    sc=''.join(f'<g class="sc" data-z="{z}" style="display:none">{_dial_scene(z)}</g>' for z in range(7))
    o+=f'<div class="gl dscn" style="left:970px;top:405px;width:860px;height:530px;border-radius:48px;overflow:hidden"><svg viewBox="0 0 790 330" width="860" height="530" style="display:block"><line class="qq" x1="0" y1="205" x2="790" y2="205" stroke="#10a98d" stroke-width="7" stroke-dasharray="22 14"/><text class="qq" x="395" y="140" font-size="90" text-anchor="middle">❔</text>{sc}</svg><div class="dart" style="position:absolute;left:0;top:0;right:0;bottom:0;background:#fff;display:none;border-radius:48px"></div></div>'
    return o+f'<script type="application/json" id="d-{sid}">{_j.dumps({"items":d["items"],"aud":bool(d.get("aud"))},ensure_ascii=False)}</script>'
BUILD_EXT['dial']=_dial_html


@module('choice')
def _choice_static(d): return choice_html(d,'x')

# ---------------- boss: optional timed challenge with a free pass ----------------
def boss_html(d,sid):
    """{'phase','title','text','q','plain':[glosses],'simple','answer','sec'}"""
    b=d; o=header(d.get('phase','ACTIVATE'),'Optional boss','rose')
    o+=glass(90,170,1060,470,f'<div style="height:100%;box-sizing:border-box;display:flex;align-items:center;padding:30px 50px;font-family:P;font-weight:500;font-size:{37 if len(b["text"])<330 else 31 if len(b["text"])<345 else 28}px;line-height:1.45"><div>{b["text"]}</div></div>',r=56)
    o+=f'<div class="a" style="left:90px;top:665px;width:1060px;font-family:O;font-weight:800;font-size:54px;line-height:1.1">{b["q"]}</div>'
    o+=f'<div class="a" style="left:90px;top:790px;display:flex;gap:28px;align-items:center"><div class="bstime" style="font-family:O;font-weight:800;font-size:110px;min-width:190px" data-sec="{b.get("sec",90)}"><span class="grad">{b.get("sec",90)}</span></div><button class="bsb bstart">{grad_chip("violet","▶ start",48,"10px 44px")}</button><button class="bsb bgive">{grad_chip("rose","😵‍💫",64,"2px 40px")}</button></div>'
    fp=(f'<div style="height:100%;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-evenly;padding:28px 38px">'
        f'<div>{grad_chip("amber","Free pass",44,"2px 28px")}</div>'
        f'<div style="font-family:P;font-weight:500;font-size:26px;line-height:1.4">'+'<br>'.join(f'<b>{g.split(" = ")[0]}</b> = {g.split(" = ")[1]}' for g in b['plain'])+'</div>'
        f'<div style="font-family:P;font-weight:500;font-size:26px;line-height:1.35">{b["simple"]}</div>'
        f'<div style="background:linear-gradient(135deg,#2bd9b6,#10a98d);color:#fff;border-radius:30px;padding:14px 24px;font-family:O;font-weight:800;font-size:27px;line-height:1.25">{b["answer"]}</div></div>')
    o+=f'<div class="bfl">'+glass(1190,170,640,740,'<div style="height:100%;box-sizing:border-box;display:flex;flex-direction:column;justify-content:center;padding:0 40px;text-align:center"><div style="font-size:170px;line-height:1.1">🔒</div><div style="font-family:O;font-weight:800;font-size:54px;margin-top:20px">Free pass</div><div style="font-family:P;font-weight:500;font-size:36px;margin-top:20px;line-height:1.4">Stuck? Tap 😵‍💫 when your team is ready.</div></div>',r=56)+'</div>'
    o+=f'<div class="bfp" style="opacity:0;transition:opacity .6s,transform .6s;transform:translateY(40px)">{glass(1190,170,640,760,fp,r=56)}</div>'
    return o
BUILD_EXT['boss']=boss_html

# ---------------- case_board: hands-up approval board ----------------
def case_board_html(d,sid):
    """{'phase','title','teams':[(id,name,c1,c2)],'suspects':[(id,name,emoji)],'clues':[{id,team,r,pic,text|dials,say,ask,kind,fx}],'twist','test','answer','reveal'}"""
    o=header(d['phase'],d.get('title','Case board'),'amber')
    o+='<div class="a cbcount"></div><div class="a cbsus"></div><div class="a cbgrid"></div><div class="a cbbar"></div><div class="a cbtw"></div><div class="a cbq"></div>'
    o+='<div class="cbm"><div class="cbmb"></div></div>'
    data={k:d[k] for k in ('teams','suspects','clues','twist','test','answer','reveal','debate','rule','hunt','frames','unit','fix') if k in d}
    return o+f'<script type="application/json" id="d-{sid}">{json.dumps(data,ensure_ascii=False)}</script>'
BUILD_EXT['case_board']=case_board_html

# ---------------- CSS ----------------
EXT_CSS.append("""
.ptr.hid{justify-content:center}.ptr.hid .ptx{display:none}.ptr.hid:after{content:'?';font-size:54px}.ptr.hid{pointer-events:none}
.sico{display:inline-block;width:1em;height:1em;background:url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M3 9v6h4l5 4V5L7 9z' fill='%236a35e8'/><path d='M15.5 8.5a5 5 0 0 1 0 7M18.2 5.6a9 9 0 0 1 0 12.8' fill='none' stroke='%236a35e8' stroke-width='2.2' stroke-linecap='round'/></svg>") center/contain no-repeat;vertical-align:-.14em;flex:none}.vsp{display:flex;align-items:center;justify-content:center}.vsp .sico{width:58%;height:58%}.vsp{border:5px solid #fff;border-radius:50%;background:linear-gradient(135deg,#ffd27a,#ff9fb8);box-shadow:0 10px 24px rgba(60,30,140,.25);cursor:pointer;line-height:1;padding:0;flex-shrink:0}.vsp.mute{opacity:.55}.vsp:active{transform:scale(.94)}
.mdls{position:absolute;left:50%;top:44px;transform:translateX(-50%);display:flex;gap:18px;z-index:6}
.mdl{width:74px;height:74px;border-radius:50%;border:5px solid rgba(255,255,255,.9);box-shadow:0 10px 24px rgba(60,30,140,.28),inset 0 4px 0 rgba(255,255,255,.5);cursor:pointer;display:flex;align-items:center;justify-content:center;gap:5px;opacity:.5;transition:transform .25s,opacity .25s}
.mdl i{width:11px;height:11px;border-radius:50%;background:rgba(255,255,255,.95);display:block}
.mdl.on{opacity:1;transform:scale(1.28);box-shadow:0 0 0 8px rgba(255,255,255,.45),0 12px 28px rgba(60,30,140,.35)}
.chd{cursor:pointer;position:relative;background:rgba(255,255,255,.7);border:4px solid #fff;box-shadow:0 4px 12px rgba(60,30,140,.18)}.chd.on{background:#9a5cff;border-color:#fff;transform:scale(1.25)}.chd.dn{background:#2bd9b6}.chd:after{content:'';position:absolute;inset:-12px;border-radius:50%}
.cho{font-family:O;font-weight:800;text-align:left;padding:28px 48px;border-radius:999px;background:rgba(255,255,255,.78);border:5px solid #fff;box-shadow:0 10px 26px rgba(60,30,140,.16);color:#1c1b2e;cursor:pointer;line-height:1.15;transition:transform .2s,opacity .3s,background .3s}
.cho:active{transform:scale(.97)}.cho.ok{background:linear-gradient(135deg,#2bd9b6,#10a98d);color:#fff;border-color:#fff}.cho.off{opacity:.3;pointer-events:none}.cho.nope{opacity:.4}
.bsb{border:0;background:none;padding:0;cursor:pointer}
.cbcount{right:90px;top:58px;font-family:O;font-weight:800;font-size:40px;padding:10px 38px;border-radius:999px;background:linear-gradient(135deg,#ffc13b,#ff9f1c);color:#fff;box-shadow:0 14px 28px rgba(200,120,0,.3)}
.cbsus{left:90px;top:145px;width:1740px;display:flex;gap:18px}
.cbs{flex:1;height:100px;box-sizing:border-box;border-radius:36px;background:rgba(255,255,255,.7);border:4px solid #fff;box-shadow:0 10px 26px rgba(60,30,140,.14);display:flex;align-items:center;justify-content:center;gap:12px;font-family:O;font-weight:800;font-size:30px;transition:opacity .5s,background .5s}.cbs>div{text-align:left;line-height:1.05}
.cbs b{display:block;font-size:54px;line-height:1}.cbs .mk{font-size:26px;height:30px;letter-spacing:1px;margin-top:2px}.cbs.win{background:linear-gradient(135deg,#bff5df,#7fe0d8);transform:scale(1.04)}.cbs.dim{opacity:.35}
.cbgrid{left:90px;top:305px;width:1740px;height:535px;display:grid;grid-template-columns:repeat(4,1fr);gap:26px}
.cbgrid.hunt{top:335px;height:515px;grid-template-rows:repeat(3,1fr);gap:14px 18px}.cbgrid.hunt .cbt.rd{animation:none;background:rgba(255,255,255,.85)}.cbgrid.hunt .cbt.rd .tx{font-family:O;font-weight:800;font-size:34px}
.cbq.tw{background:linear-gradient(135deg,#ffe3ea,#ffd0dc);color:#c01850}.cbq{left:90px;top:262px;width:1740px;height:58px;border-radius:32px;background:rgba(255,255,255,.75);border:4px solid #fff;display:flex;align-items:center;gap:30px;padding:0 34px;box-sizing:border-box;font-family:O;font-weight:800;font-size:28px;color:#6a35e8;white-space:nowrap}.cbq i{font-style:normal;color:#1c1b2e;font-family:P;font-weight:500}.cbcount .pgb{display:inline-block;width:260px;height:22px;border-radius:11px;background:rgba(255,255,255,.55);vertical-align:middle;margin-right:16px;overflow:hidden}.cbcount .pgb b{display:block;height:100%;background:#fff;border-radius:11px;transition:width .6s}
.gd{font-family:P;font-weight:600;font-size:26px;color:#6a35e8;margin-top:8px;line-height:1.2}.wt{font-family:O;font-weight:800;font-size:34px;color:#6a35e8;margin-bottom:6px}
g.dz{stroke:none}g.dz.dim{opacity:1;filter:grayscale(.85) brightness(1.1)}.dz{cursor:pointer;stroke:#fff;stroke-width:6;transition:filter .2s,opacity .3s}.dz:hover{filter:brightness(1.08)}.dz.glow{filter:drop-shadow(0 0 16px #fff) brightness(1.1)}.dz.dim{opacity:.55}
.dcard,.dsen{box-sizing:border-box;padding:26px 40px;font-family:O;font-weight:800;line-height:1.25;display:flex;flex-direction:column;justify-content:center}.dcard{font-size:42px}.dcard small{font-family:P;font-weight:500;font-size:34px;color:#4a4a62;margin-top:10px}.dsen{font-size:42px;color:#1c1b2e}.dsen u{text-decoration:none;display:inline-block;width:260px;border-bottom:6px solid #c9b6ff;vertical-align:baseline}.dsen.ok{background:linear-gradient(135deg,#d6fbea,#c4f3e6)}.dsen .say{font-family:P;font-weight:500;font-size:30px;color:#6a6a7e;margin-top:12px}
.mdls{display:none!important}
.ulw{background:linear-gradient(90deg,#9a5cff,#ff5aa5) no-repeat 0 100%;background-size:0 9px;padding-bottom:6px}[data-s]:not(.sh) .ulw{animation:ulwd .8s .9s ease-out forwards}.sh .ulw{animation:none;background-size:0 9px}@keyframes ulwd{to{background-size:100% 9px}}
.rsp.rg{width:112px;height:112px;background:rgba(255,138,31,.10);border:6px solid #ff8a1f;box-shadow:0 0 0 0 rgba(255,138,31,.5);animation:rgp 2.2s infinite}.rsp.rg.on{background:rgba(43,217,182,.18);border-color:#2bd9b6;animation:none}@keyframes rgp{70%{box-shadow:0 0 0 22px rgba(255,138,31,0)}100%{box-shadow:0 0 0 0 rgba(255,138,31,0)}}.rsp{position:absolute;width:150px;height:150px;border-radius:50%;border:6px solid #fff;background:rgba(255,255,255,.85);box-shadow:0 12px 26px rgba(60,30,140,.2);font-size:84px;line-height:1;cursor:pointer;transition:transform .2s,background .3s}.rsp:hover{transform:scale(1.07)}.rsp.on{background:#d6fbea;border-color:#2bd9b6}
.cbcol{display:flex;flex-direction:column;gap:12px;min-height:0}
.cbh{height:62px;border-radius:24px;color:#fff;font-family:O;font-weight:800;font-size:38px;text-align:center;line-height:62px;box-shadow:inset 0 3px 0 rgba(255,255,255,.4)}
.cbt{flex:1;min-height:0;border-radius:30px;background:rgba(255,255,255,.55);border:4px solid #fff;display:flex;align-items:center;gap:14px;padding:0 20px;font-family:P;font-weight:500;font-size:27px;line-height:1.18;overflow:hidden;text-align:left;color:#1c1b2e;position:relative}.cbt .tx{flex:1;min-width:0}.cbt.ov:after{content:'\2922';position:absolute;right:14px;bottom:4px;font-size:30px;color:#7b3cf0}
.cbt .pc{font-size:48px;flex-shrink:0}.cbt.lk{opacity:.45}.cbt.rd{cursor:pointer;background:#fff;animation:cbp 1.6s infinite}.cbt.ok{background:#fff;cursor:pointer;box-shadow:0 8px 22px rgba(60,30,140,.18)}
@keyframes cbp{50%{box-shadow:0 0 0 10px rgba(154,92,255,.2)}}
.cbbar{left:90px;top:866px;display:flex;gap:16px}
.cbb{border:0;cursor:pointer;font-family:O;font-weight:800;font-size:32px;padding:8px 30px;border-radius:999px;background:rgba(255,255,255,.85);color:#4a2bb8;box-shadow:0 8px 20px rgba(60,30,140,.18)}
.cbtw{left:1190px;top:858px;width:640px;font-family:O;font-weight:800;font-size:27px;line-height:1.1;color:#c0306a;display:none;background:#fff;border-radius:40px;padding:8px 26px}
.cbm{position:absolute;inset:0;background:rgba(40,20,100,.42);display:none;align-items:center;justify-content:center;z-index:8}.cbm.on{display:flex}
.cbmb{width:1200px;max-height:850px;overflow:auto;background:#fff;border-radius:56px;padding:44px 56px;box-shadow:0 40px 100px rgba(40,20,100,.45);font-family:P;font-weight:500;font-size:36px;line-height:1.4;color:#1c1b2e}
.cbmb .ulw{animation:ulwd .7s .7s ease-out forwards}.cbmb h3{font-family:O;font-weight:800;font-size:56px;margin:0 0 14px}.cbmb .ex{background:#efeaff;border-radius:30px;padding:20px 30px;margin:18px 0;font-size:38px}
.cbmb .tg{display:inline-block;margin:8px 12px 8px 0;padding:10px 30px;border-radius:999px;border:5px solid #d9d3f5;font-family:O;font-weight:800;font-size:38px;cursor:pointer;background:#fff}.cbmb .tg.on{background:#2bd9b6;color:#fff;border-color:#fff}
.cbmb .stx{margin-left:6px}.cbmb .bt{border:0;font-family:O;font-weight:800;font-size:38px;padding:14px 44px;border-radius:999px;margin:10px 14px 0 0;cursor:pointer;color:#fff;background:linear-gradient(135deg,#7b3cf0,#ff4fa3)}.cbmb .bt.g{background:#d9d3f5;color:#333}.cbmb .bt[disabled]{opacity:.35}
""")

# ---------------- behaviour ----------------
EXT_JS.append(r"""
SXL.say=false;
document.addEventListener('keydown',function(e){if(/INPUT|TEXTAREA/.test((e.target||{}).tagName||''))return;if('123'.indexOf(e.key)<0||e.key==='')return;var m=document.querySelector('.sl.on .mdl[data-l="'+e.key+'"]');if(m)m.click()});
window.__sxlPic=function(pb){var pc=document.querySelector('.sl.on .tpic');if(pc){var pv=pb.dataset.pic;if(/^(file:|data:image)|\.(jpg|png)$/.test(pv)){pc.style.display='block';var ct=/\.png$|^data:image\/png/.test(pv);pc.style.padding=ct?'34px':'10px';pc.style.fontSize='';pc.innerHTML='<img src="'+pv+'" style="width:100%;height:100%;object-fit:'+(ct?'contain':'cover')+';border-radius:46px;display:block;background:#fff">'}else{pc.style.display='flex';pc.style.padding='0';var nn=Array.from(pv).filter(function(c){return c.charCodeAt(0)>255}).length;pc.style.fontSize=(nn<=1?352:nn===2?230:150)+'px';pc.textContent=pv}pc.classList.remove('pp');void pc.offsetWidth;pc.classList.add('pp')}}
document.addEventListener('click',function(e){var pb=e.target.closest('[data-pic]');if(pb)window.__sxlPic(pb);var b=e.target.closest('[data-seq]');if(b&&b.classList.contains('tch')){var st=+(b.dataset.st||0);if(st===0){var pt=b.querySelector('.pt');if(pt)pt.style.display='block';b.dataset.st=1}else if(st===1){var an=b.querySelector('.an');if(an)an.style.display='block';b.dataset.st=2;P('pop');return}}
 var b=e.target.closest('[data-say]');if(b&&b.classList.contains('tch')){var dl=b.classList.contains('dtl'),shw=function(){if(dl&&!b.__t){b.__t=1;b.style.fontSize='40px';b.style.lineHeight='1.3';b.innerHTML='\uD83D\uDD0A '+b.dataset.say}};try{speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(b.dataset.say);u.lang='en-GB';u.rate=.8;if(dl){u.onend=shw;setTimeout(shw,Math.max(3500,b.dataset.say.length*110))}speechSynthesis.speak(u)}catch(x){shw()}P('tick')}});
document.addEventListener('click',function(e){var b=e.target.closest('.vsp');if(!b)return;e.stopPropagation();P('tick');var a=b.dataset.a;if(a){try{if(window.__va)window.__va.pause();window.__va=new Audio(a);window.__va.play()}catch(x){}}});
document.addEventListener('click',function(e){var d=e.target.closest('.chd');if(!d)return;var sl=d.closest('.sl');if(!sl||!sl.__jump)return;e.stopPropagation();var i=Array.prototype.indexOf.call(d.parentNode.children,d);P('tick');sl.__jump(i)},true);
/* teacher aid: Aa shows the words of the audio line on screen (no-audio fallback) */
setInterval(function(){var s=slides[cur],b=$('#aa');if(!b)return;var h=!!(s&&s.__tx&&s.__tx());b.style.display=h?'block':'none';if(!h)$('#trp').style.display='none'},300);
$('#aa').onclick=function(e){e.stopPropagation();var s=slides[cur],t=s&&s.__tx&&s.__tx(),p=$('#trp');if(!t)return;if(s.__rv)s.__rv();p.textContent=t;p.style.display='block';P('tick')};
document.addEventListener('click',function(e){if(!e.target.closest('#aa')){var p=$('#trp');if(p)p.style.display='none'}},true);
/* temporary review skip: hide with ?noskip */
if(!/noskip/.test(location.search)){var sk=$('#sk');sk.style.display='block';setInterval(function(){sk.style.visibility=(cur<slides.length-1)?'visible':'hidden'},300);sk.onclick=function(){var s=slides[cur];if(s)s.__done=1;P('tick');if(cur<slides.length-1)go(cur+1)}}

/* ---- medals: levels:[...] on a slide give three sections; the medal picks which one is in the deck ---- */
function setLvl(g,l){var all=$$('.sl[data-lvg="'+g+'"]');all.forEach(function(e){e.classList.toggle('lvx',+e.dataset.lv!==l);e.classList.remove('on')});slides=$$('.sl:not(.lvx)');var n=all.filter(function(e){return +e.dataset.lv===l})[0];P('pop');go(slides.indexOf(n))}
document.addEventListener('click',function(e){var b=e.target.closest('.mdl');if(b){e.stopPropagation();setLvl(+b.dataset.g,+b.dataset.l)}},true);
addEventListener('keydown',function(e){if(e.target&&/^(TEXTAREA|INPUT)$/.test(e.target.tagName))return;var s=slides[cur];if(s&&s.dataset.lvg&&'123'.indexOf(e.key)>-1&&e.key.length===1)setLvl(+s.dataset.lvg,+e.key)});
/* ---- choice ---- */
INIT.choice=function(s){
 var items=$$('.chi',s),dots=$$('.chd',s),k=0;
 function show(n){items.forEach(function(e,i){e.style.display=i===n?'block':'none'});dots.forEach(function(d,i){d.classList.toggle('on',i===n);d.classList.toggle('dn',!!items[i].__ok)});
  var box=$('.cho-wrap',items[n]),arr=$$('.cho',items[n]);for(var i=arr.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=arr[i];arr[i]=arr[j];arr[j]=t}arr.forEach(function(b){box.appendChild(b)});var au=$('.caud',items[n]);if(au){box.style.transition='opacity .5s';box.style.opacity=0;box.style.pointerEvents='none';au.style.cursor='pointer';au.onclick=function(){var rv=function(){box.style.opacity=1;box.style.pointerEvents='auto';};P('tick');try{speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(au.dataset.say),dn=0,go=function(){if(!dn){dn=1;rv()}};u.lang='en-GB';u.rate=.85;u.onend=go;speechSynthesis.speak(u);setTimeout(go,Math.max(3500,au.dataset.say.length*110))}catch(e){rv()}}}}
 items.forEach(function(it,n){$$('.cho',it).forEach(function(b){b.onclick=function(){if(it.__ok)return;
  if(b.dataset.ok==='1'){it.__ok=1;dots[n]&&dots[n].classList.add('dn');b.classList.add('ok');$$('.cho',it).forEach(function(x){if(x!==b)x.classList.add('off')});P('pop');setTimeout(function(){P('tick')},90);
   try{var u=new SpeechSynthesisUtterance(b.textContent);u.lang='en-GB';u.rate=.85;speechSynthesis.cancel();if(SXL.say)speechSynthesis.speak(u)}catch(e){}
   if(items.every(function(x){return x.__ok}))finish(s);else setTimeout(function(){if(k!==n)return;k=Math.min(n+1,items.length-1);if(items[k].__ok){var q=items.findIndex(function(x){return !x.__ok});if(q>-1)k=q}show(k)},900)}
  else{b.classList.add('nope');wrong(b)}}})});
 s.__jump=function(i){var it=items[i];it.__ok=0;$$('.cho',it).forEach(function(b){b.classList.remove('ok','off','nope')});k=i;show(i)};
 s.__tx=function(){return ''};s.__rv=function(){var b=$('.cho-wrap',items[k]);if(b){b.style.opacity=1;b.style.pointerEvents='auto'}};
 show(0)};

INIT.pairs=function(s){var L=$$('.ptl',s),R=$$('.ptr',s),sel=null,left=L.length,bn=$('.pbn',s),hid=R.length&&R[0].classList.contains('hid');$('#nx').classList.remove('on');
 function bsay(t){if(bn)bn.textContent=t}
 function reveal(l){var r=R.filter(function(x){return x.dataset.i===l.dataset.i})[0];r.classList.remove('hid');r.style.pointerEvents='';return r}
 L.forEach(function(l){l.onclick=function(){if(l.__ok)return;
  if(hid&&sel===l){var r=reveal(l);l.__ok=r.__ok=1;l.style.outline='';var PC=['linear-gradient(135deg,#ffd6e8,#ffb8d6)','linear-gradient(135deg,#cfe6ff,#a9d1ff)','linear-gradient(135deg,#d8f5c4,#b9e89c)','linear-gradient(135deg,#ffdcb8,#ffc58a)','linear-gradient(135deg,#e3d4ff,#c9b0ff)'],cc=PC[(5-left)%5];l.style.background=r.style.background=cc;l.style.color=r.style.color='#1c1b2e';l.innerHTML='\u2714 '+l.innerHTML;sel=null;P('pop');bsay('\uD83D\uDD01 Everybody repeats.');if(--left==0){P('good');s.__done=1;$('#nx').classList.add('on')}else setTimeout(function(){bsay(bn.dataset.d)},3500);return}
  L.forEach(function(x){x.style.outline=''});sel=(sel===l)?null:l;if(sel){l.style.outline='7px solid #9a5cff';P('tick');if(l.dataset.say&&s.querySelector('.plis')){try{speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(l.dataset.say);u.lang='en-GB';u.rate=.85;speechSynthesis.speak(u)}catch(e){}}bsay(hid?'\u26BD Ball to a student. Say the sentence. Tap the clue again to check.':'\u26BD Ball to a student. Say the sentence. Then tap it.')}else bsay(bn?bn.dataset.d:'')}});
 R.forEach(function(r){r.onclick=function(){if(r.__ok)return;if(!sel){P('tick');return}
  if(sel.dataset.i===r.dataset.i){sel.__ok=r.__ok=1;sel.style.outline='';var PC=['linear-gradient(135deg,#ffd6e8,#ffb8d6)','linear-gradient(135deg,#cfe6ff,#a9d1ff)','linear-gradient(135deg,#d8f5c4,#b9e89c)','linear-gradient(135deg,#ffdcb8,#ffc58a)','linear-gradient(135deg,#e3d4ff,#c9b0ff)'],cc=PC[(5-left)%5];sel.style.background=r.style.background=cc;sel.style.color=r.style.color='#1c1b2e';sel.innerHTML='✔ '+sel.innerHTML;r.innerHTML='✔ '+r.innerHTML;sel=null;P('pop');bsay('\uD83D\uDD01 Everybody repeats.');if(--left==0){P('good');s.__done=1;$('#nx').classList.add('on')}else setTimeout(function(){bsay(bn?bn.dataset.d:'')},3500)}
  else{try{wrong(sel)}catch(e){}sel.style.outline='';sel=null}}})};
INIT.rungs=function(s){var rg=$$('.rgr',s),pn=$$('.rgp',s),m=$('.rgm',s);rg.forEach(function(r){r.onclick=function(){m.style.top=(+r.dataset.y-10)+'px';pn.forEach(function(p){p.style.opacity=(p.dataset.i===r.dataset.i)?1:0});P('pop')}})};
/* ---- room of clues ---- */
INIT.room=function(s){var cap=$('.rcap',s);$('#nx').classList.add('on');$$('.rsp',s).forEach(function(b){b.onclick=function(){b.classList.add('on');cap.textContent=b.dataset.t;P('pop')}})};
/* ---- dial ---- */
INIT.dial=function(s){
 var D=JSON.parse($('#d-'+s.dataset.id).textContent),I=D.items,k=0,done=0,wt=-1,fin={},card=$('.dcard',s),sen=$('.dsen',s),nd=$('.nd',s),dots=$$('.chd',s),zs=$$('.dz',s),scs=$$('.sc',s),qq=$$('.qq',s),dart=$('.dart',s);
 function scn(z){scs.forEach(function(g){g.style.display=(+g.dataset.z===z)?'block':'none'});qq.forEach(function(q){q.style.display=z<0?'block':'none'});if(dart)dart.style.display=dart.firstChild?'block':'none'}
 var W=[['dangerously','lower'],['much','lower'],['slightly','lower'],['','normal'],['slightly','higher'],['much','higher'],['dangerously','higher']];
 function ang(z){return (z+.5)*180/7-90}
 function ic(e){return /\.jpg$|^file:|^data:image/.test(e)?'<img src="'+e+'" style="height:84px;width:84px;border-radius:50%;object-fit:cover;vertical-align:middle;background:#fff;margin-right:8px">':e}
 function sent(it,z){var w=W[z];return z===3?it.s+' normal.':it.s+' <b>'+w[0]+' '+w[1]+'</b>'+(it.nt?'':' than '+(it.ref||'normal'))+'.'}
 function go1(){if(wt<0)return false;wt=-1;P('tick');if(k>=I.length-1){finish(s);return true}k++;show();if(!s.__done)$('#nx').classList.remove('on');return true}
 s.__adv=go1;s.addEventListener('click',function(e){if(e.target.closest('.dz,.chd'))return;go1()});
 function show(){var it=I[k];done=0;wt=-1;nd.style.transform='rotate(-90deg)';if(dart)dart.innerHTML=it.art?'<img src="'+it.art+'" style="width:100%;height:100%;object-fit:contain;border-radius:48px;display:block">':'';scn(-1);zs.forEach(function(z){z.classList.remove('glow','dim')});
  dots.forEach(function(d,i){d.classList.toggle('on',i===k);d.classList.toggle('dn',!!fin[i])});
  if(D.aud&&it.say)card.innerHTML='<div class="tch dtl" data-say="'+it.say+'" style="cursor:pointer;text-align:center;font-size:52px"><i class="sico"></i> Tap to listen</div>';else card.innerHTML='<div>'+(it.art?'':it.e+' ')+it.now+'</div><small>'+(it.nl||'Normal')+': '+it.normal+'</small>';sen.classList.remove('ok');
  if(it.guide&&it.demo)card.insertAdjacentHTML('beforeend','<div class="gd">'+it.guide+'</div>');
  sen.innerHTML='<div>'+it.s+' <u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u>'+(it.nt?'':' than '+(it.ref||'normal'))+'.</div>';var pp=$('.ptp',s);if(pp)pp.style.visibility=it.demo?'hidden':'visible';
  if(it.demo){done=1;var kk=k;setTimeout(function(){if(k!==kk)return;fin[kk]=1;dots[kk].classList.add('dn');nd.style.transform='rotate('+ang(it.z)+'deg)';scn(it.z);var z=zs[it.z];z.classList.add('glow');zs.forEach(function(o){if(o!==z)o.classList.add('dim')});sen.classList.add('ok');sen.innerHTML='<div>'+sent(it,it.z)+'</div>';P('good')},1500);setTimeout(function(){if(k!==kk)return;wt=kk;$('#nx').classList.add('on')},2600)}}
 zs.forEach(function(z){z.onclick=function(){if(done)return;var it=I[k],n=+z.dataset.z;nd.style.transform='rotate('+ang(n)+'deg)';scn(n);
  if(n===it.z){done=1;fin[k]=1;dots[k].classList.add('dn');z.classList.add('glow');zs.forEach(function(o){if(o!==z)o.classList.add('dim')});P('good');sen.classList.add('ok');sen.innerHTML='<div>'+sent(it,n)+'</div>';if(D.aud&&it.say)card.innerHTML='<div>'+(it.art?'':it.e+' ')+it.now+'</div><small>'+(it.nl||'Normal')+': '+it.normal+'</small>';
   var kn=k;setTimeout(function(){if(k!==kn)return;if(I.every(function(_,j){return fin[j]||I[j].demo})){finish(s);return}k=Math.min(k+1,I.length-1);var q=I.findIndex(function(x,j){return !fin[j]&&!x.demo});if(fin[k]&&q>-1)k=q;show()},3200)}
  else{P('tick');setTimeout(function(){if(!done){nd.style.transform='rotate(-90deg)';scn(-1)}},900);try{wrong(z)}catch(e){}}}});
 s.__jump=function(i){k=i;show()};
 s.__tx=function(){var it=I[k];return (D.aud&&it&&it.say)?it.say:''};
 show()};
/* ---- boss ---- */
INIT.boss=function(s){
 var t=$('.bstime',s),left=+t.dataset.sec,iv=null,fp=$('.bfp',s);$('#nx').classList.add('on');
 function draw(){t.innerHTML='<span class="grad">'+left+'</span>'}
 function give(){clearInterval(iv);var tz=$('.bfl',s);if(tz)tz.style.display='none';fp.style.opacity=1;fp.style.transform='none';P('good');finish(s)}
 $('.bstart',s).onclick=function(){clearInterval(iv);left=+t.dataset.sec;draw();P('pop');iv=setInterval(function(){left--;draw();if(left<=10&&left>0)P('tick');if(left<=0)give()},1000)};
 $('.bgive',s).onclick=give};
/* ---- case_board ---- */
INIT.case_board=function(s){
 var D=JSON.parse($('#d-'+s.dataset.id).textContent),ok={},won=false,tw=false;
 var sus=$('.cbsus',s),grid=$('.cbgrid',s),cnt=$('.cbcount',s),bar=$('.cbbar',s),m=$('.cbm',s),mb=$('.cbmb',s),twb=$('.cbtw',s),qb=$('.cbq',s);
 function say(t){try{if(!SXL.say)return;speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(t);u.lang='en-GB';u.rate=.85;speechSynthesis.speak(u)}catch(e){}}
 function clue(id){return id==='TW'?D.twist:D.clues.filter(function(c){return c.id===id})[0]}
 function fx(){var f={};D.suspects.forEach(function(x){f[x[0]]={f:0,a:0}});Object.keys(ok).forEach(function(id){var c=clue(id),e=c.fx||{};for(var k in e){if(f[k])f[k][e[k]==='for'?'f':'a']++}});return f}
 function txt(c){return (D.hunt&&c.short)?c.short:(c.dials?('<b>'+(c.topic||'')+'</b>'):(c.text||'').replace(/\n/g,'<br>'))}
 function draw(){
  var tot=D.clues.length,done=Object.keys(ok).filter(function(k){return k!=='TW'}).length;if(D.hunt)cnt.innerHTML='<span class="pgb"><b style="width:'+Math.round(100*done/tot)+'%"></b></span>'+done+' / '+tot+' '+(D.unit||'clues found');else cnt.textContent=(tot-done)+' answers to go';
  var f=fx();sus.innerHTML=D.suspects.map(function(x){return '<div class="cbs'+(won?(x[0]===D.answer?' win':' dim'):'')+'"><b>'+x[2]+'</b><div>'+x[1]+'<div class="mk"><span style="color:#10a98d">'+new Array(f[x[0]].f+1).join('✔')+'</span> <span style="color:#e0306a">'+new Array(f[x[0]].a+1).join('✖')+'</span></div></div></div>'}).join('');
  if(D.hunt){grid.className='a cbgrid hunt';grid.innerHTML=D.clues.map(function(c){return ok[c.id]?'<div class="cbt ok" data-id="'+c.id+'" data-k="read"><span class="pc">'+c.pic+'</span><span class="tx">'+(D.fix?c.text:txt(c))+'</span></div>':'<div class="cbt rd" data-id="'+c.id+'" data-k="found"><span class="pc">'+c.pic+'</span><span class="tx">'+(D.fix?(c.short||''):(c.topic||''))+'</span></div>'}).join('')}
  else grid.innerHTML=D.teams.map(function(t){var open=true,mine=D.clues.filter(function(c){return c.team===t[0]}).sort(function(a,b){return a.r-b.r});
   return '<div class="cbcol"><div class="cbh" style="background:linear-gradient(135deg,'+t[2]+','+t[3]+')">'+t[1]+'</div>'+mine.map(function(c){var o=ok[c.id],rd=!o&&open;if(!o)open=false;
    if(o)return '<div class="cbt ok" data-id="'+c.id+'" data-k="read"><span class="pc">'+c.pic+'</span><span class="tx">'+txt(c)+'</span></div>';
    return '<div class="cbt '+(rd?'rd':'lk')+'" data-id="'+c.id+'" data-k="'+(rd?'ask':'')+'"><span class="pc">'+(rd?'✋':'🔒')+'</span><span>'+(rd?'tap when the team is ready':'')+'</span></div>'}).join('')+'</div>'}).join('');
  fit();if(tw){if(D.hunt&&qb){qb.classList.add('tw');qb.innerHTML='⚡ '+D.twist.pic+' '+D.twist.text}else{twb.style.display='block';twb.innerHTML='⚡ '+D.twist.pic+' '+D.twist.text}}}
 function fit(){$$('.cbt.ok',grid).forEach(function(t){var x=$('.tx',t),f=(x.textContent.length<24?40:x.textContent.length<46?33:27);x.style.fontSize=f+'px';while(f>22&&(x.scrollHeight>t.clientHeight-8)){f--;x.style.fontSize=f+'px'}if(x.scrollHeight>t.clientHeight-8)t.classList.add('ov')})}
 function sheet(h){mb.innerHTML=h;m.classList.add('on')}
 function close(){m.classList.remove('on')}
 function dialsHtml(c){return c.dials?'<div class="ex">'+Object.keys(c.dials).map(function(k){return '<b>'+k+'</b> '+c.dials[k]}).join('<br>')+'</div>':''}
 grid.onclick=function(e){var t=e.target.closest('.cbt');if(!t||!t.dataset.k)return;var c=clue(t.dataset.id);P('tick');
  if(t.dataset.k==='found'){ok[c.id]=1;draw();P('good');if(c.kind==='audio')say(c.text);return}
  if(t.dataset.k==='read'){sheet('<h3>'+c.pic+' '+(c.topic||c.id)+'</h3><div class="ex">'+(c.text||'').replace(/\n/g,'<br>')+'</div>'+dialsHtml(c)+(D.hunt?'<button class="bt g" data-a="un" data-id="'+c.id+'">↩ Not found yet</button>':'')+'<button class="bt g" data-a="x">Close</button>');return}
  var k=c.task,h;
   if(k){var need=k.w!==false;h='<h3>'+c.pic+' <span style="font-size:40px;background:#efeaff;border-radius:999px;padding:6px 26px;vertical-align:middle">'+k.ic+' '+k.lab+'</span></h3><div class="ex" style="font-size:33px;line-height:1.4">'+k.card.replace(/\n/g,'<br>')+'</div><div style="font-size:28px;color:#6a6a7e">'+k.who+'</div><div style="font-size:28px;color:#6a6a7e;margin-top:8px">Check: <b>'+k.key+'</b> · listen for the meaning, not grammar. '+(D.rule||'')+'</div>'+(k.stretch?'<div style="margin:6px 0"><span class="tg" data-a="st" style="font-size:30px">⭐ Stretch (optional)</span><span class="stx" style="display:none;font-size:30px"><b>'+k.stretch+'</b></span></div>':'')+'<div style="margin:12px 0"><span class="tg" data-a="t1">Said aloud</span>'+(need?'<span class="tg" data-a="t2">Written down</span>':'')+'</div><button class="bt" data-a="ap" data-id="'+c.id+'" data-need="'+(need?2:1)+'" disabled>Approve · show clue</button><button class="bt g" data-a="x">Not yet</button>'}
   else h='<h3>'+c.pic+' '+c.id+'</h3>'+(c.ask?'<div>The team should ask: <b>"'+c.ask+'"</b></div>':'')+'<div class="ex">Listen for the meaning:<br><b>'+c.say+'</b></div><div style="font-size:30px;color:#6a6a7e">Approve on meaning, not grammar. '+(D.rule||'')+' Another team: "say it differently".</div><div style="margin:16px 0"><span class="tg" data-a="t1">Said aloud</span><span class="tg" data-a="t2">Written down</span></div><button class="bt" data-a="ap" data-id="'+c.id+'" data-need="2" disabled>Approve · show clue</button><button class="bt g" data-a="x">Not yet</button>';sheet(h)};
 mb.onclick=function(e){var b=e.target.closest('[data-a]');if(!b)return;var a=b.dataset.a;
  if(a==='x'){close();return}
  if(a==='un'){delete ok[b.dataset.id];close();draw();return}
  if(a==='t1'||a==='t2'){b.classList.toggle('on');P('tick');var ap=$('[data-a="ap"]',mb),n=$$('.tg.on[data-a=t1],.tg.on[data-a=t2]',mb).length;ap.disabled=n<+ap.dataset.need;return}
   if(a==='st'){b.style.display='none';$('.stx',mb).style.display='inline';P('open');return}
  if(a==='ap'){var c=clue(b.dataset.id);ok[c.id]=1;close();draw();P('good');if(c.kind==='audio')say(c.text);return}
  if(a==='opt'){var T=D.test;if(+b.dataset.i===T.ans){b.style.background='#2bd9b6';b.style.color='#fff';$('.why',mb).textContent=T.why;P('good')}else{b.style.opacity=.4;wrong(b)}}};
 if(D.frames){var q=$('.cbq',s);q.innerHTML='❓ Ask:&nbsp;'+D.frames.map(function(f){return '<i>'+f+'</i>'}).join('<span style="color:#c9b6ff">·</span>')}
 bar.innerHTML='<button class="cbb" data-b="tw">⚡ Late twist</button><button class="cbb" data-b="test">🧪 Confirming test</button><button class="cbb" data-b="rv">🎬 Reveal</button>'+(D.debate?'<button class="cbb" data-b="db">🗣️ Debate</button>':'');
 bar.onclick=function(e){var b=e.target.closest('[data-b]');if(!b)return;P('tick');var k=b.dataset.b;
  if(k==='tw'){tw=true;ok.TW=1;draw();P('open');say(D.twist.text.replace(/["⚡]/g,''))}
  if(k==='test'){var T=D.test;sheet('<h3>🧪 '+T.q+'</h3>'+T.opts.map(function(o,i){return '<button class="bt g" style="display:block;width:100%;text-align:left" data-a="opt" data-i="'+i+'">'+o+'</button>'}).join('')+'<div class="ex why">Let the teams argue first.</div><button class="bt g" data-a="x">Close</button>')}
  if(k==='db'){var f=fx(),top=D.suspects.slice().sort(function(a,b){return (f[b[0]].f-f[b[0]].a)-(f[a[0]].f-f[a[0]].a)}).slice(0,3);sheet('<h3>🗣️ '+D.debate.title+'</h3><div class="ex">'+top.map(function(x){return '<span class="tg">'+x[2]+' '+x[1]+'</span>'}).join('')+'</div>'+D.debate.lines.map(function(l){return '<div style="margin:8px 0">'+l+'</div>'}).join('')+'<button class="bt g" data-a="x">Close</button>')}
  if(k==='rv'){won=true;draw();var a=D.suspects.filter(function(x){return x[0]===D.answer})[0];P('arrive');sheet('<h3 style="font-size:84px">'+a[2]+' '+a[1]+'</h3><div class="ex">'+D.reveal+'</div><button class="bt g" data-a="x">Close</button>');$$('.ulw',mb).forEach(function(u,i){u.style.animationDelay=(0.7+i*0.75)+'s'});finish(s)}};
 $('#nx').classList.add('on');draw()};


INIT.audio_all=function(s){
 var cur=null;function stop(){if(cur){cur.pause();cur=null}if(window.speechSynthesis)speechSynthesis.cancel();$$('.aab.on',s).forEach(function(x){x.classList.remove('on')})}
 $$('.aab',s).forEach(function(b){b.onclick=function(){var was=b.classList.contains('on');stop();if(was)return;b.classList.add('on');
  var c=b.dataset.clip;if(c){cur=new Audio(c);cur.onended=function(){b.classList.remove('on')};cur.play()}else if(window.speechSynthesis){var u=new SpeechSynthesisUtterance(b.dataset.say);u.lang='en-GB';u.rate=.85;u.onend=function(){b.classList.remove('on')};speechSynthesis.speak(u)}}});
 $('#nx').classList.add('on')};
""")

EXT_CSS.append(".aab{display:flex;align-items:center;justify-content:space-between;box-sizing:border-box;width:370px;height:196px;padding:0 30px;border-radius:44px;border:7px solid;background:#fff;cursor:pointer;box-shadow:0 10px 24px rgba(60,30,140,.14)}.aap{font-size:104px;line-height:1}.aas{width:110px;height:110px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:56px}.aab.on{background:#fff7e0}.aab.on .aas{animation:pu .8s infinite}.zoomv img[src^='data:image/png']{width:900px;height:900px;image-rendering:pixelated;padding:30px;box-sizing:border-box}")
