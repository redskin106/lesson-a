"""Group clue pages for the L3/L4 ball hunt: one page per group (A-D). Phone portrait, no names, no scoring."""
import sys,os,html
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','..','lessons-3-4','src'))
import content as K
COL=[('A','Red','#ff5a6a'),('B','Blue','#2a8cf0'),('C','Green','#19b38a'),('D','Yellow','#f2a900')]
def page(lesson,letter,name,col,clues,frames):
    cards=''
    for i,c in enumerate(clues):
        aud=c['pic']=='🎧'
        txt=html.escape(c['text']).replace('\n','<br>')
        cards+=f'<button class="cd" data-say="{html.escape(c["text"]) if aud else ""}"><div class="e">{c["pic"]}</div><div class="h">Clue {i+1}</div><div class="t">{txt}</div><div class="tp">{"Tap · listen" if aud else "Tap to read"}</div></button>'
    fr=''.join(f'<div class="fr">{html.escape(f)}</div>' for f in frames)
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lesson {lesson} · Group {name}</title><style>
*{{box-sizing:border-box}}body{{margin:0;font-family:Outfit,system-ui,sans-serif;background:linear-gradient(#f5ecff,#dff1ff);color:#1c1b2e;padding:18px}}
.top{{display:flex;align-items:center;gap:12px;margin-bottom:14px}}.dot{{width:54px;height:54px;border-radius:50%;background:{col};box-shadow:0 6px 16px rgba(0,0,0,.2)}}h1{{font-size:26px;margin:0}}.sub{{font-size:16px;color:#5a5a74;margin:2px 0 0}}
.cd{{position:relative;display:block;width:100%;min-height:150px;margin:0 0 14px;padding:16px 18px;border-radius:30px;border:5px solid {col};background:#fff;text-align:left;font:inherit;cursor:pointer;box-shadow:0 10px 24px rgba(60,30,140,.14)}}
.cd{{display:grid;grid-template-columns:70px 1fr;column-gap:14px}}.cd .e{{font-size:50px;grid-row:1/4}}.cd .h{{font-weight:800;font-size:20px;color:{col}}}.cd .t{{display:none;font-weight:800;font-size:25px;line-height:1.25;margin-top:6px}}.cd .tp{{font-size:16px;color:#6a6a7e;margin-top:8px}}.cd.on .t{{display:block}}.cd.on .tp{{display:none}}
.sec{{font-weight:800;font-size:20px;margin:22px 0 8px}}.fr{{background:#fff;border-radius:22px;padding:12px 16px;margin-bottom:8px;font-weight:700;font-size:20px}}.sec2{{font-size:17px;color:#5a5a74;margin-top:6px}}
</style></head><body><div class="top"><div class="dot"></div><div><h1>Group {name}</h1><div class="sub">Lesson {lesson} · Your clues are a secret</div></div></div>
{cards}<div class="sec">Ask with the ball</div>{fr}<div class="sec2">Answer in a full sentence. 3 of you hold a clue. 1 of you writes.</div>
<script>document.querySelectorAll('.cd').forEach(function(b){{b.onclick=function(){{b.classList.add('on');var s=b.dataset.say;if(s&&window.speechSynthesis){{speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(s);u.lang='en-US';u.rate=.9;speechSynthesis.speak(u)}}}}}});</script></body></html>'''
out=os.path.join(os.path.dirname(__file__),'..','..','lessons-3-4','groups'); os.makedirs(out,exist_ok=True)
import importlib.util,json
_sp=importlib.util.spec_from_file_location('l34',os.path.join(os.path.dirname(__file__),'lessons34.py'));_m=importlib.util.module_from_spec(_sp);_sp.loader.exec_module(_m)
ORDER=[('red','1','#ff5a6a'),('blue','2','#2a8cf0'),('green','3','#19b38a'),('yellow','4','#f2a900')]
import base64,glob
ADIR=os.path.join(os.path.dirname(__file__),'..','..','lessons-3-4','source-audio','l4_fix')
ADIR3=os.path.join(os.path.dirname(__file__),'..','..','lessons-3-4','source-audio','l3_hunt')
def _clip(n,L=4):
    p=os.path.join(ADIR3,'L3_%02d.mp3'%n) if L==3 else os.path.join(ADIR,'FIX_%02d.mp3'%n)
    return 'data:audio/mpeg;base64,'+base64.b64encode(open(p,'rb').read()).decode() if os.path.exists(p) else ''
SPK='<svg viewBox="0 0 24 24" width="44" height="44" aria-hidden="true"><path d="M3 9v6h4l5 4V5L7 9H3z" fill="#fff"/><path d="M15.5 8.5a5 5 0 010 7M18 6a8.5 8.5 0 010 12" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round"/></svg>'
JS="""var cur=null;function stop(){if(cur){cur.pause();cur=null}if(window.speechSynthesis)speechSynthesis.cancel();document.querySelectorAll('.nt.on').forEach(function(x){x.classList.remove('on')})}
document.querySelectorAll('.nt').forEach(function(b){b.onclick=function(){var was=b.classList.contains('on');stop();if(was)return;b.classList.add('on');var c=b.dataset.clip;if(c){cur=new Audio(c);cur.onended=function(){b.classList.remove('on')};cur.play()}else if(window.speechSynthesis){var u=new SpeechSynthesisUtterance(b.dataset.say);u.lang='en-GB';u.rate=.85;u.onend=function(){b.classList.remove('on')};speechSynthesis.speak(u)}}});"""
def notes(items,L=4):
    return ''.join(f'<button class="nt" aria-label="voice note" data-clip="{_clip(f["n"],L)}" data-say="{html.escape(f["voice"])}"><span class="pic">{f["pic"]}</span><span class="pl">{SPK}</span></button>' for f in items)
CSS="""*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}body{margin:0;font-family:Outfit,system-ui,sans-serif;background:linear-gradient(#f5ecff,#dff1ff);color:#1c1b2e;padding:20px;min-height:100vh}
.top{display:flex;align-items:center;gap:14px;margin-bottom:18px}.num{width:84px;height:84px;border-radius:50%;background:var(--c);color:#fff;font-weight:800;font-size:56px;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(0,0,0,.22)}
.nt{display:flex;align-items:center;justify-content:space-between;width:100%;height:150px;margin:0 0 16px;padding:0 26px;border-radius:36px;border:6px solid var(--c);background:#fff;box-shadow:0 10px 24px rgba(60,30,140,.14);font:inherit;cursor:pointer}
.nt .pic{font-size:84px;line-height:1}.nt .pl{width:92px;height:92px;border-radius:50%;background:var(--c);display:flex;align-items:center;justify-content:center;flex:none}
.nt.on{background:#fff7e0}.nt.on .pl{animation:pu 1s infinite}@keyframes pu{50%{transform:scale(1.14)}}.g{margin:6px 0 10px;font-weight:800;font-size:26px}"""
def page4(idx,L=4):
    key,name,col=ORDER[idx]
    mine=[f for f in (_m.FIX3 if L==3 else _m.FIX) if f['owner']==key]
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{"Voice-note hunt" if L==3 else "Fix the ward"} · Group {name}</title><style>:root{{--c:{col}}}{CSS}</style></head><body><div class="top"><div class="num">{name}</div></div>{notes(mine,L)}<script>{JS}</script></body></html>'
def teacher(L=4):
    FX=_m.FIX3 if L==3 else _m.FIX
    sec=''.join(f'<div class="g" style="color:{ORDER[i][2]}">Group {ORDER[i][1]}</div><div style="--c:{ORDER[i][2]}">{notes([f for f in FX if f["owner"]==ORDER[i][0]],L)}</div>' for i in range(4))
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fix the ward · teacher</title><style>{CSS}</style></head><body><div class="top"><h1 style="margin:0;font-size:26px">All 12 voice notes (teacher laptop)</h1></div>{sec}<script>{JS}</script></body></html>'
import glob as _g
for _f in _g.glob(os.path.join(out,'l4-*.html')): os.remove(_f)
open(os.path.join(out,'l4-teacher.html'),'w').write(teacher())
for idx in range(4):
    open(os.path.join(out,f'l4-{ORDER[idx][1]}.html'),'w').write(page4(idx)); print(4,ORDER[idx][1])
for _f in _g.glob(os.path.join(out,'l3-*.html')): os.remove(_f)
open(os.path.join(out,'l3-teacher.html'),'w').write(teacher(3))
for idx in range(4):
    open(os.path.join(out,f'l3-{ORDER[idx][1]}.html'),'w').write(page4(idx,3)); print(3,ORDER[idx][1])
