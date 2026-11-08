"""sort — pictured rows 'You [gap] ...' + a bank of chips. Data:
{'m':'sort','phase':'STUDY','title':'Fill the gaps','rows':[{'pic':'sc2_1.jpg','pre':('c1','You'),'end':('c3','eat spicy food.')}],'bank':['have to','should']}
Rows size themselves to fit 1-5 rows."""
from ..core import *
@module('sort')
def sort(d):
    rows=d['rows']; n=len(rows); top,bot=168,830; step=(bot-top)/n; h=int(step-18); h=min(h,190); fs=min(72,int(h*.42)); ps=max(10,int(h*.22))
    out=header(d['phase'],d.get('title'))
    for i,r in enumerate(rows):
        y=int(top+i*step); pre=r.get('pre',('c1','You')) if r.get('pre',1) else None; end=r.get('end')
        out+=num(90,y+h//2-32,i+1)+pic(180,y,h,h,r['pic'],r=int(h*.23))
        x0=180+h+40
        out+=(f'<div class="gl" style="left:{x0}px;top:{y}px;width:{1830-x0}px;height:{h}px;border-radius:{int(h*.4)}px;display:flex;align-items:center;gap:22px;padding:0 50px">'
              +(ch(pre[0],pre[1],fs,f'{ps}px {int(fs*.55)}px') if pre else '')+gap('#9a5cff',420,'…',h=int(fs*1.45))+(ch(end[0],end[1],fs,f'{ps}px {int(fs*.55)}px') if end else gap('#ff7a3c',470,'…',h=int(fs*1.45)))+'</div>')
    bfs=52 if len(d['bank'])>4 else 56  # bank items: 'word' | (cls,'word') | '|' divider
    out+=('<div class="gl" style="left:90px;top:840px;width:1740px;height:148px;border-radius:72px;display:flex;align-items:center;gap:20px;padding:0 44px">'
          +''.join(('<div style="width:6px;height:70px;border-radius:3px;background:#b9a6f5;margin:0 10px"></div>' if t=='|' else ch(*(t if isinstance(t,tuple) else ('c2',t)),bfs,'8px 30px')) for t in d['bank'])+'</div>')
    return out
