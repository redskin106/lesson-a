"""chat — a running conversation with gaps. ONE data dict drives both outputs.
Data: {'m':'chat','phase':'STUDY','title':'Fill the gaps','window':4,
       'lines':[(side, content[, bank]), ...], 'bank':[('c4','Where'),...]   # default bank
       'avatars':{'N':'woman_health_worker'}}
  side: P patient (right), N nurse (left), D doctor (left). content: 'text' or [(chip_class,text,is_gap),...]
STATIC EXPORT (PDF/PPT): the thread is split into steps. A step ends at each line that has a gap; lines after the last gap form a final step.
  Each step shows the last `window` lines; earlier lines fade; gaps of earlier lines are shown filled, the current line's gaps are open.
INTERACTIVE (later): same data, one scrolling thread; auto-scrolls as each gap is filled; swipe/slider scrolls back. (behaviour sheet below)
BEHAVIOUR: drop right chip in gap -> sfx 'pop' then 'tick', mo-chip; wrong -> 'boop', chip returns, no penalty; line completes -> next bubble 'arrive' + slide-up; calm mode mutes sfx.
"""
from ..core import *
AV={'P':'face_with_thermometer','N':'woman_health_worker','D':'man_health_worker'}
def gapchip(c,t):
    col={'c1':'#34d0f2','c2':'#9a5cff','c3':'#ff7a3c','c4':'#ffb21f'}[c]
    return f'<span style="display:inline-flex;align-items:center;justify-content:center;height:84px;min-width:{40+len(t)*30}px;border-radius:44px;border:5px dashed {col};color:transparent;font-family:O;font-weight:800;font-size:46px;padding:0 20px">{t}</span>'
def line(y,side,content,av,filled=False,op=1,pic_=None):
    left=side in ('N','D'); a=EM(av.get(side,AV[side]))
    inner=(f'<div style="font-family:O;font-weight:800;font-size:52px;color:#1c1b2e">{content}</div>' if isinstance(content,str)
           else '<div style="display:flex;gap:12px;align-items:center">'+''.join(gapchip(c,t) if (g and not filled) else ch(c,t,46,'8px 26px') for c,t,g in content)+'</div>')
    pimg=(f'<img src="{ART}{pic_}" style="height:112px;width:112px;border-radius:26px;margin-left:30px;background:#fff;object-fit:contain">' if pic_ else '')
    bub=f'<div class="gl" style="position:static;height:130px;border-radius:65px;display:flex;align-items:center;padding:0 {18 if pic_ else 46}px 0 46px;{"" if left else "background:rgba(214,190,255,.75);"}">{inner}{pimg}</div>'
    avh=f'<div class="gl" style="position:static;width:110px;height:110px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;background:#fff"><img src="{a}" style="width:78px"></div>'
    side_css='left:90px;' if left else 'right:90px;'
    return f'<div class="a" style="{side_css}top:{y}px;opacity:{op};display:flex;align-items:center;gap:22px;{"" if left else "flex-direction:row-reverse"}">{avh}{bub}</div>'
def has_gap(c): return not isinstance(c,str) and any(g for _,_,g in c)
def parts(l): return l[0],l[1],(l[2] if len(l)>2 else None)
def expand(d):
    L=d['lines']; gaps=[i for i,l in enumerate(L) if has_gap(l[1])]
    ends=gaps+([len(L)-1] if (not gaps or gaps[-1]<len(L)-1) else [])
    return [dict(d,upto=e,final=(e==len(L)-1 and not (e in gaps)) ,step=k) for k,e in enumerate(ends)]
@module('chat',expand=expand)
def chat(d):
    L=d['lines']; e=d.get('upto',len(L)-1); w=d.get('window',4)
    vis=list(range(max(0,e-w+1),e+1))
    out=header(d['phase'],d.get('title','Fill the gaps'))
    off=w-len(vis)   # anchor to the bottom so the newest line sits in the same place on every step
    for k,i in enumerate(vis):
        s,c,_=parts(L[i]); age=e-i; pc=L[i][3] if len(L[i])>3 else None
        out+=line(180+(off+k)*178,s,c,d.get('avatars',{}),filled=(i<e or d.get('final',False) or not has_gap(c)),op=(1,.8,.6,.45)[min(age,3)],pic_=pc)
    bank=parts(L[e])[2] or d.get('bank') if has_gap(L[e][1]) else None
    if bank: out+='<div class="gl" style="left:90px;top:896px;width:1740px;height:100px;border-radius:50px;display:flex;align-items:center;gap:20px;padding:0 40px">'+''.join(ch(c,t,46,'8px 26px') for c,t in bank)+'</div>'
    return out
