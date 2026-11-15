"""One standalone page per team per lesson (QR code per team). Offline, no networking: the team does the task, puts a hand up, the board approves, the team taps on.
Build: python3 lessons/team_pages2.py  ->  lessons-3-4/teams/l3-red.html ... l4-yellow.html + teams/index.html"""
import sys, pathlib, json
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent)); sys.path.insert(0,str(HERE.parent.parent/'lessons-3-4'/'src'))
import content as K
from sxl import team_page as TP
from sxl.interactive import inline_assets
OUT=HERE.parent.parent/'lessons-3-4'/'teams'; OUT.mkdir(exist_ok=True)
COL={'red':('Red','#e0304a','#ff5a6a'),'blue':('Blue','#2a6ae0','#2a8cf0'),'green':('Green','#10a98d','#19b38a'),'yellow':('Yellow','#e89200','#f2a900')}
LESSON={3:('Lesson 3 · Find the illness',K.L3_CLUES,K.TASK3),4:('Lesson 4 · Find the reason',K.L4_CLUES,K.TASK4)}
EXTRA="""
.tabs{display:flex;gap:10px;margin:10px 0}.tabs button{width:70px;height:70px;border-radius:50%;border:4px solid #fff;background:rgba(255,255,255,.7);font-family:O;font-weight:800;font-size:30px;cursor:pointer}.tabs button.on{background:var(--c);color:#fff}.tabs button.dn{background:#2bd9b6;color:#fff}.tabs button[disabled]{opacity:.4}
.card{font-size:30px;line-height:1.5;background:#efeaff;border-radius:28px;padding:22px 28px;margin:14px 0}.who{font-size:24px;color:#6a6a7e}
.letters{display:flex;gap:12px;margin:8px 0}.letters button{width:80px;height:80px;border-radius:26px;border:4px solid #fff;font-family:O;font-weight:800;font-size:40px;background:rgba(255,255,255,.7);cursor:pointer}.letters button.on{background:var(--c);color:#fff}
"""
JS=r"""
const T=D.tasks,ids=D.ids;let r=0,done=0,L=null;const $=id=>document.getElementById(id);
function draw(){const a=$('app');document.documentElement.style.setProperty('--c',D.c1);
 let h=`<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap"><span class="chip" style="background:linear-gradient(135deg,${D.c1},${D.c2})">${D.name}</span><span class="mu" style="font-size:22px">${D.lesson}</span></div>
 <div class="gl"><div class="mu" style="font-size:22px">Your letter</div><div class="letters">${'ABCD'.split('').map(x=>`<button class="${L===x?'on':''}" data-a="L" data-v="${x}">${x}</button>`).join('')}</div></div>
 <div class="tabs">${[0,1,2,3].map(i=>`<button class="${i===r?'on':''} ${i<done?'dn':''}" ${i>done?'disabled':''} data-a="R" data-v="${i}">${i<done?'✔':i+1}</button>`).join('')}</div>`;
 if(r>=4||done>=4&&r>=3&&0){}
 const t=T[r];
 h+=`<div class="gl"><span class="chip" style="background:linear-gradient(135deg,${D.c1},${D.c2});font-size:28px">${t.ic} ${t.lab}</span>
 <div class="card">${t.card.replace(/\n/g,'<br>')}</div><div class="who">${t.who}</div>
 ${t.stretch?`<div style="margin-top:14px"><button class="b g" data-a="S">⭐ Stretch (optional)</button><div id="st" style="display:none;font-size:26px;font-family:O;font-weight:800">${t.stretch}</div></div>`:''}
 <div style="margin-top:12px" class="mu">${t.w?'Say it. Then write it down on paper.':'Say it aloud.'}</div></div>`;
 if(r<done){h+=`<div class="gl mu">✔ Done. The clue is on the board.</div>`}
 else{h+=`<button class="b" data-a="H">✋ We are ready</button>
  <div id="hd" style="display:none"><div class="hand" style="background:linear-gradient(135deg,${D.c1},${D.c2})">✋ hands up!</div>
  <div class="mu" style="margin:10px 0;font-size:22px">Wait for the teacher or another team to say OK. Then tap below.</div>
  <button class="b" data-a="N">✔ Approved · ${r<3?'next round':'finish'}</button></div>`}
 if(done>=4)h+=`<div class="gl"><div class="big">All four done! 🎉</div><div style="margin-top:8px">Look at the board. Which illness?</div></div>`;
 a.innerHTML=h}
document.addEventListener('click',function(e){var b=e.target.closest('[data-a]');if(!b||b.disabled)return;var a=b.dataset.a,v=b.dataset.v;
 if(a==='L'){L=v;draw()}else if(a==='R'){r=+v;draw()}else if(a==='S'){b.style.display='none';$('st').style.display='block'}else if(a==='H'){$('hd').style.display='block';b.style.display='none'}else if(a==='N'){done=Math.min(4,done+1);r=Math.min(3,done);draw()}});
draw();
"""
def page(n,team):
    title,clues,tasks=LESSON[n]; name,c1,c2=COL[team]
    ids=[c['id'] for c in sorted([c for c in clues if c['team']==team],key=lambda c:c['r'])]
    data=dict(name=name,c1=c1,c2=c2,lesson=title,ids=ids,tasks=[tasks[i] for i in ids])
    html=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{name} team · L{n}</title><style>{TP.CSS}{EXTRA}</style></head><body><div id="app"></div><div id="dbg" style="font:12px monospace;color:#6a6a7e;padding:6px">page v3</div><script>window.addEventListener('error',function(e){document.getElementById('dbg').style.color='red';document.getElementById('dbg').textContent='ERROR: '+e.message});document.addEventListener('click',function(e){var d=document.getElementById('dbg');if(d&&d.textContent.indexOf('ERROR')<0)d.textContent='page v3 · last tap: '+(e.target.tagName||'')+' '+(e.target.textContent||'').slice(0,12)},true);const D={json.dumps(data,ensure_ascii=False)};{JS}</script></body></html>'
    (OUT/f'l{n}-{team}.html').write_text(inline_assets(html),encoding='utf-8')
for n in (3,4):
    for t in COL: page(n,t)
idx='<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Team pages</title><body style="font-family:system-ui;padding:24px;background:#f4f0ff"><h1>Team pages (one QR per team)</h1><p>Each page is one team in one lesson. Open on a tablet or phone.</p>'
for n in (3,4):
    idx+=f'<h2>{LESSON[n][0]}</h2><p>'+' '.join(f'<a style="display:inline-block;margin:6px;padding:16px 28px;border-radius:20px;color:#fff;font-weight:700;text-decoration:none;background:{COL[t][1]}" href="l{n}-{t}.html">{COL[t][0]}</a>' for t in COL)+'</p>'
(OUT/'index.html').write_text(idx+'</body>',encoding='utf-8')
print(sorted(p.name for p in OUT.glob('*.html')))
