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
ORDER=[('red','Red','#ff5a6a','🔴'),('blue','Blue','#2a8cf0','🔵'),('green','Green','#19b38a','🟢'),('yellow','Yellow','#f2a900','🟡')]
def page4(idx):
    key,name,col,dot=ORDER[idx]; nxt=ORDER[(idx+1)%4]; prv=ORDER[(idx-1)%4]
    mine=[f for f in _m.FIX if f['owner']==key]; hold=[f for f in _m.FIX if f['owner']==prv[0]]
    cards=''
    for f in mine:
        opts=json.dumps(f['opts'],ensure_ascii=False)
        cards+=f'<div class="mk" data-ans="{html.escape(f["fix"])}" data-o=\'{html.escape(opts,quote=True)}\'><div class="w"><span class="e">{f["pic"]}</span><s>{html.escape(f["wrong"])}</s></div><div class="ask">{nxt[3]} Ask {nxt[1]}: "Can I hear your voice note about the {f["topic"].lower()}?"</div><button class="hb">✔ We listened</button><div class="op" style="display:none"></div><div class="ok" style="display:none">✅ Fixed! Say it to the class.</div></div>'
    vn=''.join(f'<div class="vn"><button class="pl" data-say="{html.escape(f["voice"])}">🎧</button><div><b>{f["pic"]} Voice note: {f["topic"].lower()}</b><div class="who">{f["who"]}</div></div></div>' for f in hold)
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fix the ward · Group {name}</title><style>
*{{box-sizing:border-box}}body{{margin:0;font-family:Outfit,system-ui,sans-serif;background:linear-gradient(#f5ecff,#dff1ff);color:#1c1b2e;padding:18px}}
.top{{display:flex;align-items:center;gap:12px;margin-bottom:12px}}.dot{{width:50px;height:50px;border-radius:50%;background:{col}}}h1{{font-size:25px;margin:0}}.sub{{font-size:15px;color:#5a5a74}}
.sec{{font-weight:800;font-size:20px;margin:18px 0 8px}}.mk,.vn{{background:#fff;border:5px solid {col};border-radius:26px;padding:14px 16px;margin-bottom:12px;box-shadow:0 8px 20px rgba(60,30,140,.12)}}
.w{{font-size:24px;font-weight:800}}.w .e{{font-size:36px;margin-right:10px}}.w s{{color:#c01850}}.ask{{font-size:16px;color:#5a5a74;margin:8px 0}}
.hb,.opt{{display:block;width:100%;margin:8px 0 0;padding:12px 16px;border-radius:20px;border:3px solid #d8c9ff;background:#f7f2ff;font:700 18px Outfit,system-ui;text-align:left}}.hb{{text-align:center;background:{col};color:#fff;border:0}}
.opt.bad{{background:#ffe0e6;border-color:#ff8aa0;animation:sh .3s}}.opt.good{{background:#d6fbea;border-color:#2bd9b6}}.ok{{font-weight:800;font-size:20px;margin-top:10px;color:#0f9a8c}}
.vn{{display:flex;gap:14px;align-items:center}}.pl{{flex:none;width:76px;height:76px;border-radius:50%;border:0;background:{col};font-size:38px}}.who{{font-size:15px;color:#6a6a7e;margin-top:2px}}.hint{{font-size:15px;color:#5a5a74}}
@keyframes sh{{25%{{transform:translateX(-6px)}}75%{{transform:translateX(6px)}}}}</style></head><body>
<div class="top"><div class="dot"></div><div><h1>Group {name}</h1><div class="sub">Fix the ward · Lesson 4</div></div></div>
<div class="sec">Your mistakes</div>{cards}<div class="hint">Ask the other group. Listen. Then choose the fix.</div>
<div class="sec">Your voice notes ({prv[3]} {prv[1]} will ask you)</div>{vn}
<script>function shuf(a){{for(var i=a.length-1;i>0;i--){{var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t}}return a}}
document.querySelectorAll('.pl').forEach(function(b){{b.onclick=function(){{if(window.speechSynthesis){{speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(b.dataset.say);u.lang='en-GB';u.rate=.85;speechSynthesis.speak(u)}}}}}});
document.querySelectorAll('.mk').forEach(function(m){{var op=m.querySelector('.op');m.querySelector('.hb').onclick=function(){{this.style.display='none';op.style.display='block';shuf(JSON.parse(m.dataset.o)).forEach(function(t){{var b=document.createElement('button');b.className='opt';b.textContent=t;b.onclick=function(){{if(t===m.dataset.ans){{b.classList.add('good');op.querySelectorAll('.opt').forEach(function(x){{x.disabled=true}});m.querySelector('.ok').style.display='block'}}else{{b.classList.add('bad');setTimeout(function(){{b.classList.remove('bad')}},400)}}}};op.appendChild(b)}})}}}});</script></body></html>'''
for idx in range(4):
    open(os.path.join(out,f'l4-{ORDER[idx][0]}.html'),'w').write(page4(idx)); print(4,ORDER[idx][1])
for lesson,clues,hunt in ((3,K.L3_CLUES,K.HUNT3),):
    by={c['id']:c for c in clues}
    for letter,name,col in COL:
        mine=[by[i] for i in hunt if i[0]==letter]
        open(os.path.join(out,f'l{lesson}-{letter}.html'),'w').write(page(lesson,letter,name,col,mine,[f[0] if isinstance(f,(tuple,list)) else f for f in K.FRAMES]))
        print(lesson,letter,len(mine))
