"""Lesson 3-4 modules (investigation + describing): vol_ladder, dials3, frames3, timetable, reveal  (view modules, stepped reveal);
choice (levelled practice), boss (optional timed challenge), case_board (hands-up approval board).  Plug and play: a lesson is a list of slide dicts.
Any slide dict can carry  levels:[{bronze},{silver},{gold}]  (+ lvl:1-3) to get the medal switch (keys 1/2/3).
Art slots accept an art file name or an emoji (shown on a glass card until Gemini art exists)."""
import json
from ..core import *
from .case import tilt

TEAMS_DEFAULT=[('red','Red','#ff5a6a','#e0304a'),('blue','Blue','#34a0f8','#2a6ae0'),('green','Green','#2bd9b6','#10a98d'),('yellow','Yellow','#ffc13b','#e89200')]

# ---------------- view modules (pieces arrive one at a time; tap to bounce) ----------------
@module('vol_ladder')
def vol_ladder(d):
    """Eyes-closed volume ladder. {'phase','title','rungs':[text...],'side':text,'emoji':'🙈'}"""
    o=header(d['phase'],d.get('title','Eyes closed. Louder.'),d.get('grad','rose')); R=d['rungs']; n=len(R)
    for i,t in enumerate(R):
        fs=50+int(i*46/max(1,n-1)); x=100+i*62; y=200+i*150
        o+=stp(f'<div class="a" style="left:{x}px;top:{y}px">{grad_chip("violet" if i<n-1 else "rose",t,fs,"8px 40px")}</div>',i+1,pills=True)
    o+=stp(glass(1180,190,650,640,f'<div style="font-size:150px;text-align:center;margin-top:50px">{d.get("emoji","🙈")}</div><div style="font-family:P;font-weight:500;font-size:42px;line-height:1.45;padding:10px 46px;text-align:center">{d["side"]}</div>',r=56),n+1)
    return o

@module('dials3')
def dials3(d):
    """The dials. {'phase','title','dials':[(letter,name,colour,'ex · ex · ex'),...],'note'}"""
    D=d['dials']; n=len(D); w=int((1740-30*(n-1))/n); o=header(d['phase'],d.get('title','The dials'),'violet')
    for i,(L,name,col,ex) in enumerate(D):
        x=90+i*(w+30); lines=''.join(f'<div style="margin:14px 0;font-family:P;font-weight:500;font-size:38px;line-height:1.25">{e}</div>' for e in ex.split(' · '))
        card=glass(x,190,w,640,'',r=56)+f'<div class="a" style="left:{x}px;top:190px;width:{w}px;height:210px;border-radius:56px 56px 0 0;background:{col}"></div>'
        card+=f'<div class="a" style="left:{x+34}px;top:226px;width:{w-68}px;font-family:O;font-weight:800;font-size:{46 if len(name)<18 else 40}px;color:#fff;line-height:1.05">{name}</div>'
        card+=num(x+34,330,L,76)+f'<div class="a" style="left:{x+34}px;top:430px;width:{w-68}px">{lines}</div>'
        o+=stp(card,i+1)
    if d.get('note'): o+=stp(f'<div class="a mu" style="left:90px;top:858px;width:1740px;text-align:center;font-size:38px">{d["note"]}</div>',n+1)
    return o

@module('frames3')
def frames3(d):
    """Sentence frames. {'phase','title','groups':[{'t','c','l':[lines],'fs'}],'note','write':bool}"""
    G=d['groups']; n=len(G); w=int((1740-30*(n-1))/n); o=header(d['phase'],d.get('title','Say it'),d.get('grad','teal')); h=d.get('h',560 if d.get('write') else 640)
    for i,g in enumerate(G):
        x=90+i*(w+30); fs=g.get('fs',40)
        body=f'<div style="padding:30px 34px">{grad_chip(g.get("c","violet"),g["t"],44,"6px 30px")}'+''.join(f'<div style="margin:18px 0 0;font-family:P;font-weight:500;font-size:{fs}px;line-height:1.3">{l}</div>' for l in g['l'])+'</div>'
        o+=stp(glass(x,180,w,h,body,r=52),i+1)
    k=n+1
    if d.get('write'):
        wy=180+h+30+(56 if d.get('note') else 0)
        o+=stp(f'<div class="gl" style="left:90px;top:{wy}px;width:1740px;height:{915-wy}px;border-radius:48px;padding:14px"><textarea placeholder="Write on your tablet…" style="width:100%;height:100%;border:0;background:transparent;font-family:P;font-weight:500;font-size:40px;resize:none;outline:none"></textarea></div>',k);k+=1
    if d.get('note'): o+=stp(f'<div class="a mu" style="left:90px;top:{180+h+30}px;width:1740px;text-align:center;font-size:34px">{d["note"]}</div>',k)
    return o

@module('timetable')
def timetable(d):
    """Silent timetable. {'phase','title','days':[..],'rows':[(emoji,[cell...])],'note'}"""
    days=d['days']; R=d['rows']; n=len(days); cw=int((1740-170)/n); o=header(d['phase'],d.get('title','A week'),'amber')
    o+=''.join(f'<div class="a" style="left:{260+i*cw}px;top:170px;width:{cw-14}px;text-align:center">{grad_chip("sky",t,38,"4px 24px")}</div>' for i,t in enumerate(days))
    rh=int(min(190,(860-230)/len(R)))
    for r,(lab,cells) in enumerate(R):
        y=230+r*rh; row=glass(90,y,150,rh-16,f'<div style="font-size:74px;text-align:center;line-height:{rh-16}px">{lab}</div>',r=40)
        row+=''.join(glass(260+i*cw,y,cw-14,rh-16,f'<div style="font-family:O;font-weight:800;font-size:{46 if len(str(c))<8 else 36}px;text-align:center;line-height:{rh-16}px">{c}</div>',r=36) for i,c in enumerate(cells))
        o+=stp(row,r+1)
    if d.get('note'): o+=stp(f'<div class="a mu" style="left:90px;top:{230+rh*len(R)+4}px;width:1740px;text-align:center;font-size:36px">{d["note"]}</div>',len(R)+1)
    return o

@module('reveal')
def reveal(d):
    """The answer. {'phase','title','pic':emoji|art,'answer','note','grad'}"""
    o=header(d['phase'],d.get('title','The answer'),'teal')
    o+=stp(picx(d['pic'],110,190,640,640,56),1)
    o+=stp(f'<div class="a" style="left:830px;top:300px">{grad_chip(d.get("grad","teal"),d["answer"],140,"14px 60px")}</div>',2,pills=True)
    if d.get('note'): o+=stp(glass(830,520,1000,310,f'<div style="padding:34px 44px;font-family:P;font-weight:500;font-size:42px;line-height:1.45">{d["note"]}</div>',r=52),3)
    return o

# ---------------- choice: levelled one-at-a-time practice ----------------
def choice_html(d,sid):
    """{'phase','title','hint','items':[{'pic','q','opts':[...],'ans':text}]}   put levels:[...] on the slide for medals"""
    I=d['items']; n=len(I); o=header(d['phase'],d.get('title','Choose'),d.get('grad','violet'))
    o+=f'<div class="a" style="right:{(130 if d.get("_lvg") else 90)}px;top:60px;display:flex;gap:12px">'+''.join(f'<span class="chd" style="width:26px;height:26px;border-radius:50%"></span>' for _ in I)+'</div>'
    for k,it in enumerate(I):
        o+=f'<div class="chi" style="display:none">'+picx(it.get('pic','❓'),90,180,700,600,56)
        o+=f'<div class="gl" style="left:850px;top:190px;width:980px;border-radius:48px;padding:26px 40px;font-family:O;font-weight:800;font-size:{50 if len(it["q"])<46 else 42}px;line-height:1.2;position:absolute">{it["q"]}</div>'
        o+='<div class="a cho-wrap" style="left:850px;top:400px;width:980px;display:flex;flex-direction:column;gap:18px">'+''.join(f'<button class="cho" data-ok="{1 if t==it["ans"] else 0}" style="font-size:{44 if len(t)<34 else 38}px">{t}</button>' for t in it['opts'])+'</div></div>'
    if d.get('hint'): o+=f'<div class="a mu" style="left:90px;top:930px;font-size:34px">{d["hint"]}</div>'
    return o
BUILD_EXT['choice']=choice_html
@module('choice')
def _choice_static(d): return choice_html(d,'x')

# ---------------- boss: optional timed challenge with a free pass ----------------
def boss_html(d,sid):
    """{'phase','title','text','q','plain':[glosses],'simple','answer','sec'}"""
    b=d; o=header(d.get('phase','ACTIVATE'),'Optional boss','rose')
    o+=glass(90,170,1060,470,f'<div style="padding:40px 50px;font-family:P;font-weight:500;font-size:37px;line-height:1.5">{b["text"]}</div>',r=56)
    o+=f'<div class="a" style="left:90px;top:665px;width:1060px;font-family:O;font-weight:800;font-size:54px;line-height:1.1">{b["q"]}</div>'
    o+=f'<div class="a" style="left:90px;top:790px;display:flex;gap:28px;align-items:center"><div class="bstime" style="font-family:O;font-weight:800;font-size:110px;min-width:190px" data-sec="{b.get("sec",90)}"><span class="grad">{b.get("sec",90)}</span></div><button class="bsb bstart">{grad_chip("violet","▶ start",48,"10px 44px")}</button><button class="bsb bgive">{grad_chip("rose","We give up",48,"10px 44px")}</button></div>'
    fp=f'<div style="padding:34px 40px">{grad_chip("amber","Free pass",48,"6px 34px")}<div style="margin-top:20px;font-family:P;font-weight:500;font-size:34px;line-height:1.55">'+'<br>'.join(f'<b>{g.split(" = ")[0]}</b> = {g.split(" = ")[1]}' for g in b['plain'])+f'</div><div style="margin-top:26px;font-family:P;font-weight:500;font-size:36px;line-height:1.4">{b["simple"]}</div><div style="margin-top:26px">{grad_chip("teal",b["answer"],40,"8px 30px")}</div><div style="margin-top:22px;font-size:44px">Too easy? 😄</div></div>'
    o+=f'<div class="bfp" style="opacity:0;transition:opacity .6s,transform .6s;transform:translateY(40px)">{glass(1190,170,640,740,fp,r=56)}</div>'
    return o
BUILD_EXT['boss']=boss_html

# ---------------- case_board: hands-up approval board ----------------
def case_board_html(d,sid):
    """{'phase','title','teams':[(id,name,c1,c2)],'suspects':[(id,name,emoji)],'clues':[{id,team,r,pic,text|dials,say,ask,kind,fx}],'twist','test','answer','reveal'}"""
    o=header(d['phase'],d.get('title','Case board'),'amber')
    o+='<div class="a cbcount"></div><div class="a cbsus"></div><div class="a cbgrid"></div><div class="a cbbar"></div><div class="a cbtw"></div>'
    o+='<div class="cbm"><div class="cbmb"></div></div>'
    data={k:d[k] for k in ('teams','suspects','clues','twist','test','answer','reveal') if k in d}
    return o+f'<script type="application/json" id="d-{sid}">{json.dumps(data,ensure_ascii=False)}</script>'
BUILD_EXT['case_board']=case_board_html

# ---------------- CSS ----------------
EXT_CSS.append("""
.mdls{position:absolute;left:50%;top:44px;transform:translateX(-50%);display:flex;gap:18px;z-index:6}
.mdl{width:74px;height:74px;border-radius:50%;border:5px solid rgba(255,255,255,.9);box-shadow:0 10px 24px rgba(60,30,140,.28),inset 0 4px 0 rgba(255,255,255,.5);cursor:pointer;display:flex;align-items:center;justify-content:center;gap:5px;opacity:.5;transition:transform .25s,opacity .25s}
.mdl i{width:11px;height:11px;border-radius:50%;background:rgba(255,255,255,.95);display:block}
.mdl.on{opacity:1;transform:scale(1.28);box-shadow:0 0 0 8px rgba(255,255,255,.45),0 12px 28px rgba(60,30,140,.35)}
.chd{background:rgba(255,255,255,.7);border:4px solid #fff;box-shadow:0 4px 12px rgba(60,30,140,.18)}.chd.on{background:#9a5cff;border-color:#fff;transform:scale(1.25)}.chd.dn{background:#2bd9b6}
.cho{font-family:O;font-weight:800;text-align:left;padding:18px 40px;border-radius:999px;background:rgba(255,255,255,.78);border:5px solid #fff;box-shadow:0 10px 26px rgba(60,30,140,.16);color:#1c1b2e;cursor:pointer;line-height:1.15;transition:transform .2s,opacity .3s,background .3s}
.cho:active{transform:scale(.97)}.cho.ok{background:linear-gradient(135deg,#2bd9b6,#10a98d);color:#fff;border-color:#fff}.cho.off{opacity:.3;pointer-events:none}.cho.nope{opacity:.4}
.bsb{border:0;background:none;padding:0;cursor:pointer}
.cbcount{right:90px;top:58px;font-family:O;font-weight:800;font-size:40px;padding:10px 38px;border-radius:999px;background:linear-gradient(135deg,#ffc13b,#ff9f1c);color:#fff;box-shadow:0 14px 28px rgba(200,120,0,.3)}
.cbsus{left:90px;top:145px;width:1740px;display:flex;gap:18px}
.cbs{flex:1;height:140px;border-radius:40px;background:rgba(255,255,255,.7);border:4px solid #fff;box-shadow:0 10px 26px rgba(60,30,140,.14);text-align:center;font-family:O;font-weight:800;font-size:30px;padding-top:6px;transition:opacity .5s,background .5s}
.cbs b{display:block;font-size:56px;line-height:1.15}.cbs .mk{font-size:28px;height:34px;letter-spacing:2px}.cbs.win{background:linear-gradient(135deg,#bff5df,#7fe0d8);transform:scale(1.04)}.cbs.dim{opacity:.35}
.cbgrid{left:90px;top:305px;width:1740px;height:520px;display:grid;grid-template-columns:repeat(4,1fr);gap:26px}
.cbcol{display:flex;flex-direction:column;gap:12px;min-height:0}
.cbh{height:62px;border-radius:24px;color:#fff;font-family:O;font-weight:800;font-size:38px;text-align:center;line-height:62px;box-shadow:inset 0 3px 0 rgba(255,255,255,.4)}
.cbt{flex:1;min-height:0;border-radius:30px;background:rgba(255,255,255,.55);border:4px solid #fff;display:flex;align-items:center;gap:14px;padding:0 20px;font-family:P;font-weight:500;font-size:25px;line-height:1.2;overflow:hidden;text-align:left;color:#1c1b2e}
.cbt .pc{font-size:48px;flex-shrink:0}.cbt.lk{opacity:.45}.cbt.rd{cursor:pointer;background:#fff;animation:cbp 1.6s infinite}.cbt.ok{background:#fff;cursor:pointer;box-shadow:0 8px 22px rgba(60,30,140,.18)}
@keyframes cbp{50%{box-shadow:0 0 0 10px rgba(154,92,255,.2)}}
.cbbar{left:260px;top:898px;display:flex;gap:16px}
.cbb{border:0;cursor:pointer;font-family:O;font-weight:800;font-size:32px;padding:8px 30px;border-radius:999px;background:rgba(255,255,255,.85);color:#4a2bb8;box-shadow:0 8px 20px rgba(60,30,140,.18)}
.cbtw{left:90px;top:833px;width:1600px;font-family:O;font-weight:800;font-size:32px;color:#c0306a;display:none;background:#fff;border-radius:999px;padding:10px 30px}
.cbm{position:absolute;inset:0;background:rgba(40,20,100,.42);display:none;align-items:center;justify-content:center;z-index:8}.cbm.on{display:flex}
.cbmb{width:1200px;max-height:900px;overflow:auto;background:#fff;border-radius:56px;padding:44px 56px;box-shadow:0 40px 100px rgba(40,20,100,.45);font-family:P;font-weight:500;font-size:36px;line-height:1.4;color:#1c1b2e}
.cbmb h3{font-family:O;font-weight:800;font-size:56px;margin:0 0 14px}.cbmb .ex{background:#efeaff;border-radius:30px;padding:20px 30px;margin:18px 0;font-size:38px}
.cbmb .tg{display:inline-block;margin:8px 12px 8px 0;padding:10px 30px;border-radius:999px;border:5px solid #d9d3f5;font-family:O;font-weight:800;font-size:38px;cursor:pointer;background:#fff}.cbmb .tg.on{background:#2bd9b6;color:#fff;border-color:#fff}
.cbmb .bt{border:0;font-family:O;font-weight:800;font-size:38px;padding:14px 44px;border-radius:999px;margin:10px 14px 0 0;cursor:pointer;color:#fff;background:linear-gradient(135deg,#7b3cf0,#ff4fa3)}.cbmb .bt.g{background:#d9d3f5;color:#333}.cbmb .bt[disabled]{opacity:.35}
""")

# ---------------- behaviour ----------------
EXT_JS.append(r"""
SXL.say=true;
/* ---- medals: levels:[...] on a slide give three sections; the medal picks which one is in the deck ---- */
function setLvl(g,l){var all=$$('.sl[data-lvg="'+g+'"]');all.forEach(function(e){e.classList.toggle('lvx',+e.dataset.lv!==l);e.classList.remove('on')});slides=$$('.sl:not(.lvx)');var n=all.filter(function(e){return +e.dataset.lv===l})[0];P('pop');go(slides.indexOf(n))}
document.addEventListener('click',function(e){var b=e.target.closest('.mdl');if(b){e.stopPropagation();setLvl(+b.dataset.g,+b.dataset.l)}},true);
addEventListener('keydown',function(e){if(e.target&&e.target.tagName==='TEXTAREA')return;var s=slides[cur];if(s&&s.dataset.lvg&&'123'.indexOf(e.key)>-1&&e.key.length===1)setLvl(+s.dataset.lvg,+e.key)});
/* ---- choice ---- */
INIT.choice=function(s){
 var items=$$('.chi',s),dots=$$('.chd',s),k=0;
 function show(n){items.forEach(function(e,i){e.style.display=i===n?'block':'none'});dots.forEach(function(d,i){d.classList.toggle('on',i===n);d.classList.toggle('dn',i<n)});
  var box=$('.cho-wrap',items[n]),arr=$$('.cho',items[n]);for(var i=arr.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=arr[i];arr[i]=arr[j];arr[j]=t}arr.forEach(function(b){box.appendChild(b)})}
 items.forEach(function(it,n){$$('.cho',it).forEach(function(b){b.onclick=function(){if(it.__ok)return;
  if(b.dataset.ok==='1'){it.__ok=1;b.classList.add('ok');$$('.cho',it).forEach(function(x){if(x!==b)x.classList.add('off')});P('pop');setTimeout(function(){P('tick')},90);
   try{var u=new SpeechSynthesisUtterance(b.textContent);u.lang='en-GB';u.rate=.85;speechSynthesis.cancel();if(SXL.say)speechSynthesis.speak(u)}catch(e){}
   if(n===items.length-1)finish(s);else setTimeout(function(){k++;show(k)},900)}
  else{b.classList.add('nope');wrong(b)}}})});
 show(0)};
/* ---- boss ---- */
INIT.boss=function(s){
 var t=$('.bstime',s),left=+t.dataset.sec,iv=null,fp=$('.bfp',s);$('#nx').classList.add('on');
 function draw(){t.innerHTML='<span class="grad">'+left+'</span>'}
 function give(){clearInterval(iv);fp.style.opacity=1;fp.style.transform='none';P('good');finish(s)}
 $('.bstart',s).onclick=function(){clearInterval(iv);left=+t.dataset.sec;draw();P('pop');iv=setInterval(function(){left--;draw();if(left<=10&&left>0)P('tick');if(left<=0)give()},1000)};
 $('.bgive',s).onclick=give};
/* ---- case_board ---- */
INIT.case_board=function(s){
 var D=JSON.parse($('#d-'+s.dataset.id).textContent),ok={},won=false,tw=false;
 var sus=$('.cbsus',s),grid=$('.cbgrid',s),cnt=$('.cbcount',s),bar=$('.cbbar',s),m=$('.cbm',s),mb=$('.cbmb',s),twb=$('.cbtw',s);
 function say(t){try{if(!SXL.say)return;speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(t);u.lang='en-GB';u.rate=.85;speechSynthesis.speak(u)}catch(e){}}
 function clue(id){return id==='TW'?D.twist:D.clues.filter(function(c){return c.id===id})[0]}
 function fx(){var f={};D.suspects.forEach(function(x){f[x[0]]={f:0,a:0}});Object.keys(ok).forEach(function(id){var c=clue(id),e=c.fx||{};for(var k in e){if(f[k])f[k][e[k]==='for'?'f':'a']++}});return f}
 function txt(c){return c.dials?('<b>'+(c.topic||'')+'</b>'):(c.text||'').replace(/\n/g,'<br>')}
 function draw(){
  var tot=D.clues.length,done=Object.keys(ok).filter(function(k){return k!=='TW'}).length;cnt.textContent=(tot-done)+' answers to go';
  var f=fx();sus.innerHTML=D.suspects.map(function(x){return '<div class="cbs'+(won?(x[0]===D.answer?' win':' dim'):'')+'"><b>'+x[2]+'</b>'+x[1]+'<div class="mk"><span style="color:#10a98d">'+new Array(f[x[0]].f+1).join('✔')+'</span> <span style="color:#e0306a">'+new Array(f[x[0]].a+1).join('✖')+'</span></div></div>'}).join('');
  grid.innerHTML=D.teams.map(function(t){var open=true,mine=D.clues.filter(function(c){return c.team===t[0]}).sort(function(a,b){return a.r-b.r});
   return '<div class="cbcol"><div class="cbh" style="background:linear-gradient(135deg,'+t[2]+','+t[3]+')">'+t[1]+'</div>'+mine.map(function(c){var o=ok[c.id],rd=!o&&open;if(!o)open=false;
    if(o)return '<div class="cbt ok" data-id="'+c.id+'" data-k="read"><span class="pc">'+c.pic+'</span><span>'+txt(c)+'</span></div>';
    return '<div class="cbt '+(rd?'rd':'lk')+'" data-id="'+c.id+'" data-k="'+(rd?'ask':'')+'"><span class="pc">'+(rd?'✋':'🔒')+'</span><span>'+(rd?'tap when the team is ready':'')+'</span></div>'}).join('')+'</div>'}).join('');
  if(tw){twb.style.display='block';twb.innerHTML='⚡ '+D.twist.pic+' '+D.twist.text}}
 function sheet(h){mb.innerHTML=h;m.classList.add('on')}
 function close(){m.classList.remove('on')}
 function dialsHtml(c){return c.dials?'<div class="ex">'+Object.keys(c.dials).map(function(k){return '<b>'+k+'</b> '+c.dials[k]}).join('<br>')+'</div>':''}
 grid.onclick=function(e){var t=e.target.closest('.cbt');if(!t||!t.dataset.k)return;var c=clue(t.dataset.id);P('tick');
  if(t.dataset.k==='read'){sheet('<h3>'+c.pic+' '+(c.topic||c.id)+'</h3><div class="ex">'+(c.text||'').replace(/\n/g,'<br>')+'</div>'+dialsHtml(c)+'<button class="bt g" data-a="x">Close</button>');return}
  var h='<h3>'+c.pic+' '+c.id+'</h3>'+(c.ask?'<div>The team should ask: <b>"'+c.ask+'"</b></div>':'')+'<div class="ex">Listen for the meaning:<br><b>'+c.say+'</b></div><div style="font-size:30px;color:#6a6a7e">Approve on meaning, not grammar. Lesson 4: at least one dial. Another team: "say it differently".</div><div style="margin:16px 0"><span class="tg" data-a="t1">Said aloud</span><span class="tg" data-a="t2">Written on the tablet</span></div><button class="bt" data-a="ap" data-id="'+c.id+'" disabled>Approve · show clue</button><button class="bt g" data-a="x">Not yet</button>';sheet(h)};
 mb.onclick=function(e){var b=e.target.closest('[data-a]');if(!b)return;var a=b.dataset.a;
  if(a==='x'){close();return}
  if(a==='t1'||a==='t2'){b.classList.toggle('on');P('tick');$('[data-a="ap"]',mb).disabled=!($('[data-a="t1"]',mb).classList.contains('on')&&$('[data-a="t2"]',mb).classList.contains('on'));return}
  if(a==='ap'){var c=clue(b.dataset.id);ok[c.id]=1;close();draw();P('good');if(c.kind==='audio')say(c.text);return}
  if(a==='opt'){var T=D.test;if(+b.dataset.i===T.ans){b.style.background='#2bd9b6';b.style.color='#fff';$('.why',mb).textContent=T.why;P('good')}else{b.style.opacity=.4;wrong(b)}}};
 bar.innerHTML='<button class="cbb" data-b="tw">⚡ Late twist</button><button class="cbb" data-b="test">🧪 Confirming test</button><button class="cbb" data-b="rv">🎬 Reveal</button>';
 bar.onclick=function(e){var b=e.target.closest('[data-b]');if(!b)return;P('tick');var k=b.dataset.b;
  if(k==='tw'){tw=true;ok.TW=1;draw();P('open');say(D.twist.text.replace(/["⚡]/g,''))}
  if(k==='test'){var T=D.test;sheet('<h3>🧪 '+T.q+'</h3>'+T.opts.map(function(o,i){return '<button class="bt g" style="display:block;width:100%;text-align:left" data-a="opt" data-i="'+i+'">'+o+'</button>'}).join('')+'<div class="ex why">Let the teams argue first.</div><button class="bt g" data-a="x">Close</button>')}
  if(k==='rv'){won=true;draw();var a=D.suspects.filter(function(x){return x[0]===D.answer})[0];P('arrive');sheet('<h3 style="font-size:84px">'+a[2]+' '+a[1]+'</h3><div class="ex">'+D.reveal+'</div><button class="bt g" data-a="x">Close</button>');finish(s)}};
 $('#nx').classList.add('on');draw()};
""")
