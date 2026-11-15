"""Tablet team page (companion to case_board): colour + letter once, then rounds 1-4. Same look as the decks (glass, gradient chips, Outfit/Poppins).
Lesson 3: roles rotate Reader / Asker / Writer / Speaker; the audio clue unlocks when the Reader builds the question.
Lesson 4: the letter is a dial (A how often, B how long, C how bad, D compared with normal); the speaker rotates every clue."""
import json
from . import core
from .interactive import inline_assets
FD=core.FD
CSS="""
@font-face{font-family:O;font-weight:700;src:url(%sfd/outfit/files/outfit-latin-700-normal.woff2)}
@font-face{font-family:O;font-weight:800;src:url(%soutfit/files/outfit-latin-800-normal.woff2)}
@font-face{font-family:P;font-weight:500;src:url(%spoppins/files/poppins-latin-500-normal.woff2)}
""".replace('fd/','')%(FD,FD,FD)
CSS+="""
*{box-sizing:border-box;margin:0}body{font-family:P,system-ui,sans-serif;color:#1c1b2e;min-height:100vh;padding:18px;background:linear-gradient(135deg,#9fe8c4,#7fe0d8 50%,#a8e6ff) fixed}
.gl{background:rgba(255,255,255,.72);border:3px solid rgba(255,255,255,.95);border-radius:36px;box-shadow:0 14px 40px rgba(80,60,160,.16);padding:22px;margin:14px 0;font-size:21px}
.h{font-family:O;font-weight:800}.big{font-family:O;font-weight:800;font-size:40px;line-height:1.1}.mu{color:#6a6a7e}
.chip{display:inline-block;font-family:O;font-weight:800;color:#fff;border-radius:999px;padding:6px 26px;font-size:26px;box-shadow:0 10px 20px rgba(80,60,160,.25),inset 0 3px 0 rgba(255,255,255,.45)}
.sw{display:flex;gap:14px;flex-wrap:wrap}.sw button{width:88px;height:88px;border-radius:28px;border:5px solid #fff;font-family:O;font-weight:800;font-size:38px;color:#fff;cursor:pointer;box-shadow:0 10px 22px rgba(80,60,160,.25)}
.num{display:inline-flex;align-items:center;justify-content:center;width:54px;height:54px;border-radius:50%;font-family:O;font-weight:800;font-size:32px;color:#fff;background:linear-gradient(135deg,#9a5cff,#ff4fa3);box-shadow:inset 0 3px 0 rgba(255,255,255,.45)}
.pic{font-size:96px;text-align:center;line-height:1.15}
button.b{font-family:O;font-weight:800;font-size:24px;padding:12px 30px;border-radius:999px;border:0;color:#fff;background:linear-gradient(135deg,#7b3cf0,#ff4fa3);margin:6px 8px 6px 0;cursor:pointer;box-shadow:0 10px 20px rgba(80,60,160,.25),inset 0 3px 0 rgba(255,255,255,.45)}
button.g{background:#fff;color:#6a35e8;box-shadow:none;border:3px solid #d9d3f5}
.w{display:inline-block;font-family:O;font-weight:800;font-size:26px;padding:8px 20px;margin:5px;border-radius:999px;background:linear-gradient(135deg,#ffd21f,#ffb21f);color:#fff;border:0;cursor:pointer;box-shadow:inset 0 3px 0 rgba(255,255,255,.45)}.w.u{opacity:.25;pointer-events:none}
textarea{font-family:P;font-weight:500;font-size:22px;width:100%;height:120px;border-radius:24px;border:3px solid #d9d3f5;padding:14px;margin-top:10px}
.top{display:flex;align-items:center;gap:12px}.rd{margin-left:auto;display:flex;gap:8px}.rd button{width:54px;height:54px;border-radius:50%;border:3px solid #fff;background:rgba(255,255,255,.7);font-family:O;font-weight:800;font-size:24px;cursor:pointer}.rd button.on{background:linear-gradient(135deg,#7b3cf0,#ff4fa3);color:#fff}
.hand{font-family:O;font-weight:800;font-size:44px;padding:28px;border-radius:36px;color:#fff;text-align:center;margin-top:12px}
"""
def build_team_page(data, out):
    html=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Team page</title><style>{CSS}</style></head><body><div id="app"></div>
<script>try{{localStorage.getItem('x')}}catch(e){{var _m={{}};Object.defineProperty(window,'localStorage',{{get:function(){{return {{getItem:function(k){{return _m[k]||null}},setItem:function(k,v){{_m[k]=v}},removeItem:function(k){{delete _m[k]}}}}}}}})}}</script>
<script>const D={json.dumps(data,ensure_ascii=False)};{JS}</script></body></html>"""
    import pathlib; pathlib.Path(out).write_text(inline_assets(html),encoding='utf-8'); return len(html)
JS=r"""
const q=new URLSearchParams(location.search),N=q.get('case')==='4'?4:3,C=D['l'+N],K='sxl-team';let me=JSON.parse(localStorage.getItem(K)||'null')||{},r=1;const $=id=>document.getElementById(id),save=()=>localStorage.setItem(K,JSON.stringify(me));
function say(t){try{speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(t);u.lang='en-GB';u.rate=.85;speechSynthesis.speak(u)}catch(e){}}
function shuffle(a){return a.map(x=>[Math.random(),x]).sort((p,q)=>p[0]-q[0]).map(p=>p[1])}
const ROLES=['Reader','Asker','Writer','Speaker'];
function draw(){const a=$('app');
 if(!me.team||!me.letter){a.innerHTML=`<div class="gl"><div class="big">Your colour?</div><div class="sw" style="margin-top:12px">${D.teams.map(t=>`<button style="background:linear-gradient(135deg,${t[2]},${t[3]})" onclick="me.team='${t[0]}';save();draw()">${t[1][0]}</button>`).join('')}</div></div><div class="gl"><div class="big">Your letter?</div><div class="sw" style="margin-top:12px">${['A','B','C','D'].map(l=>`<button style="background:linear-gradient(135deg,#9a5cff,#6a35e8)" onclick="me.letter='${l}';save();draw()">${l}</button>`).join('')}</div></div><div class="mu" style="text-align:center">Your teacher gave you a card.</div>`;return}
 const t=D.teams.find(x=>x[0]===me.team),li='ABCD'.indexOf(me.letter),clue=C.clues.find(c=>c.team===me.team&&c.r===r);
 let h=`<div class="top"><span class="chip" style="background:linear-gradient(135deg,${t[2]},${t[3]})">${t[1]}</span><span class="num">${me.letter}</span><div class="rd">${[1,2,3,4].map(i=>`<button class="${i===r?'on':''}" onclick="r=${i};draw()">${i}</button>`).join('')}</div></div>`;
 if(N===3){const role=ROLES[(li+r-1)%4];h+=`<div class="gl"><div class="big">${role}</div>`;
  if(role==='Reader')h+=clue.kind==='audio'?`<div class="mu" style="margin:8px 0">Build the question. Then listen.</div><div id="qb"></div>`:`<div class="pic">${clue.pic}</div><div style="font-size:30px;text-align:center;font-family:O;font-weight:800">${clue.text.replace(/\n/g,'<br>')}</div><div class="mu" style="margin-top:8px">Keep it secret. Answer your team's questions.</div>`;
  if(role==='Asker')h+=`<div style="margin-top:8px">Ask the Reader:</div><div class="big" style="font-size:30px;margin-top:6px">${{audio:'Reader builds the question first!',number:'What is the number? What is normal?',photo:'What can you see? Where?',paper:'What does it say?'}[clue.kind]}</div>`;
  if(role==='Writer')h+=`<div style="margin-top:8px">Write one sentence down:</div><div class="mu">It might be ___ because ___.<br>It can't be ___ because ___.<br>It is higher / lower than normal.</div>✏️`;
  if(role==='Speaker')h+=`<div style="margin-top:8px">When the Writer is ready: hands up. Say it loudly.</div>`;h+='</div>'}
 else{const d=D.dials[li];h+=`<div class="gl" style="background:${d[2]};color:#fff"><div class="big">${d[0]} · ${d[1]}</div><div style="margin-top:6px">${d[3]}</div></div><div class="gl"><div class="pic">${clue.pic}</div><div style="font-size:30px;text-align:center;font-family:O;font-weight:800">${clue.dials[me.letter]}</div></div><div class="gl"><div class="big" style="font-size:32px">${li===r-1?'🎤 You speak this round!':'Tell your speaker'}</div><div class="mu" style="margin-top:6px">Say at least one dial: how often · how long · how bad · compared with normal.</div><div style="margin-top:8px;font-size:30px">✏️ Write the team sentence down.</div></div>`}
 h+=`<button class="b" onclick="$('hd').style.display='block'">✋ We are ready</button><div id="hd" class="hand" style="display:none;background:linear-gradient(135deg,${t[2]},${t[3]})">✋ hands up!</div><button class="b g" onclick="me={};save();draw()">change team</button>`;a.innerHTML=h;
 if(N===3&&clue.kind==='audio'&&ROLES[(li+r-1)%4]==='Reader'){const w=clue.ask.split(' '),box=$('qb');let n=0;const ans=document.createElement('div');ans.style.cssText='min-height:52px;font-size:26px;font-family:O;font-weight:800;margin:8px 0';box.appendChild(ans);shuffle(w.concat(['did','are'])).forEach(x=>{const b=document.createElement('button');b.className='w';b.textContent=x;b.onclick=()=>{if(x===w[n]){n++;b.classList.add('u');ans.textContent+=x+' ';if(n===w.length){const p=document.createElement('button');p.className='b';p.textContent='🔊 Listen';p.onclick=()=>say(clue.text);box.appendChild(p);say(clue.text)}}};box.appendChild(b)})}}
draw();
"""
