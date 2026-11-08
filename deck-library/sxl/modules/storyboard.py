"""storyboard — N numbered pictures in a row (last may be a '?'), a role chip, and an optional sentence bar. Data:
{'m':'storyboard','phase':'STUDY','title':'Boss says','grad':'red','panels':['a.jpg',...],'hidden_last':False,'sentence':[('c1','You'),...],'prompt':'What happens next?'}"""
from ..core import *
@module('storyboard')
def storyboard(d):
    P=d['panels']; n=len(P)+(1 if d.get('hidden_last') else 0)
    gapx=35; w=int((1740-gapx*(n-1))/n); top=190; h=520 if d.get('sentence') else 640
    if d.get('square'): h=w; top=250
    out=header(d['phase'],d.get('title'),d.get('grad','violet'))
    for i in range(n):
        x=90+i*(w+gapx)
        if i<len(P): out+=art(x,top,w,h,P[i],r=56)
        else: out+=f'<div class="gl" style="left:{x}px;top:{top}px;width:{w}px;height:{h}px;border:5px dashed #b9a6f5;background:rgba(255,255,255,.35);display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:300px;color:#9a5cff">?</div>'
        out+=num(x+20,top-32,i+1,76)
    if d.get('sentence'):
        out+=f'<div class="gl" style="left:90px;top:770px;height:210px;width:1740px;border-radius:70px;display:flex;align-items:center;gap:30px;padding:0 60px">'+chips(d['sentence'],92,'18px 48px')+'</div>'
    if d.get('prompt'):
        out+=f'<div class="gl" style="left:90px;top:890px;height:130px;width:auto;padding:0 34px 0 28px;border-radius:999px;display:flex;align-items:center;gap:20px;font-family:O;font-weight:800;font-size:60px"><span class="chip c4" style="font-size:60px;padding:6px 34px;border-radius:999px">{d["prompt"][0]}</span>{d["prompt"][1]}</div>'
    return out
