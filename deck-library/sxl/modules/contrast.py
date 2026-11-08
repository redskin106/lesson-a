"""contrast — two pictures side by side with a coloured label and a chip sentence under each. Data:
{'m':'contrast','phase':'STUDY','title':'Not the same!','left':{'label':'Not allowed','grad':'red','pic':'mu_1.jpg','chips':[('c1','You'),...]},'right':{...}}"""
from ..core import *
def col(x,c,s):
    return (stp(f'<div class="chip" style="position:absolute;left:{x}px;top:176px;font-size:40px;padding:10px 40px;border-radius:999px;background:{GRAD.get(c["grad"],c["grad"])}">{c["label"]}</div>',s)
      +stp(pic(x,252,840,440,c['pic'],48,fit=c.get('fit','cover')),s)
      +stp(f'<div class="a" style="left:{x}px;top:722px;width:840px;display:flex;flex-wrap:wrap;gap:14px 12px">'+chips(c['chips'],50,'8px 28px')+'</div>',s+1,pills=True)
      +(stp(f'<div class="a" style="left:{x}px;top:930px">{spill(c["cap"],c.get("sc"),42,"8px 34px")}</div>',s+1) if c.get('cap') else ''))
@module('contrast')
def contrast(d):
    return (header(d['phase'],d.get('title'))+col(90,d['left'],1)+col(990,d['right'],3)
      +stp('<div style="position:absolute;left:955px;top:200px;width:6px;height:740px;border-radius:3px;background:linear-gradient(180deg,rgba(154,92,255,0),#9a5cff 30%,#ff4fa3 70%,rgba(255,79,163,0))"></div>',3))
