"""contrast — two pictures side by side with a coloured label and a chip sentence under each. Data:
{'m':'contrast','phase':'STUDY','title':'Not the same!','left':{'label':'Not allowed','grad':'red','pic':'mu_1.jpg','chips':[('c1','You'),...]},'right':{...}}"""
from ..core import *
def col(x,c):
    return (grad_chip(c['grad'],c['label'],40,'10px 40px').replace('<span','<span style="position:absolute;left:%dpx;top:176px"'%x,1).replace('style="font-size','data-x="',1) if False else
      f'<div class="chip" style="position:absolute;left:{x}px;top:176px;font-size:40px;padding:10px 40px;border-radius:999px;background:{GRAD.get(c["grad"],c["grad"])}">{c["label"]}</div>'
      +pic(x,252,840,440,c['pic'],48,fit=c.get('fit','cover'))
      +f'<div class="a" style="left:{x}px;top:722px;width:840px;display:flex;flex-wrap:wrap;gap:14px 12px">'+chips(c['chips'],50,'8px 28px')+'</div>'
      +(f'<div class="a mu" style="left:{x+6}px;top:900px;font-size:42px">{c["cap"]}</div>' if c.get('cap') else ''))
@module('contrast')
def contrast(d):
    return (header(d['phase'],d.get('title'))+col(90,d['left'])+col(990,d['right'])
      +'<div style="position:absolute;left:955px;top:200px;width:6px;height:740px;border-radius:3px;background:linear-gradient(180deg,rgba(154,92,255,0),#9a5cff 30%,#ff4fa3 70%,rgba(255,79,163,0))"></div>')
