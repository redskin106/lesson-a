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
import importlib.util
_sp=importlib.util.spec_from_file_location('l34',os.path.join(os.path.dirname(__file__),'lessons34.py'));_m=importlib.util.module_from_spec(_sp);_sp.loader.exec_module(_m)
L4C=[dict(c,text=_m.L4SAY[c['id']]) for c in K.L4_CLUES if c['id'] in _m.L4SAY]
L4G=[('R','Red','#ff5a6a'),('B','Blue','#2a8cf0'),('G','Green','#19b38a'),('Y','Yellow','#f2a900')]
for letter,name,col in L4G:
    by={c['id']:c for c in L4C}; mine=[by[i] for i in K.HUNT4 if i[0]==letter and i in by]
    open(os.path.join(out,f'l4-{name.lower()}.html'),'w').write(page(4,letter,name,col,mine,[f[0] if isinstance(f,(tuple,list)) else f for f in K.FRAMES])); print(4,name,len(mine))
for lesson,clues,hunt in ((3,K.L3_CLUES,K.HUNT3),):
    by={c['id']:c for c in clues}
    for letter,name,col in COL:
        mine=[by[i] for i in hunt if i[0]==letter]
        open(os.path.join(out,f'l{lesson}-{letter}.html'),'w').write(page(lesson,letter,name,col,mine,[f[0] if isinstance(f,(tuple,list)) else f for f in K.FRAMES]))
        print(lesson,letter,len(mine))
