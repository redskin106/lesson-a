"""Batches 2+3 play modules (one shared look). All: no scores, wrong = nudge only, content as data, levels:[b,s,g] override keys.
odd(items[{cards[{t,e}|{t,v}],odd,why}], mode pic|text|chart) · listen_fix(items[{text,say,opts}], mode opts|type)
triage(buckets,items[{t,e,b,why}], show both|text) · label_reader(lab{title,lines[{id,t,e}]},qs[{q,a}], qtext) 
taboo(items[{w,e,no[]}], limit, secs) · guess_who(attrs,patients,rounds,ask full|word) · ward_memory(pairs[{a,b}])
predict(items[{frames[{e,c}],q,opts[{t,e}],a,outcome}], cap, nopt)"""
import json
from ..core import *

def pg_html(d,sid,title,n):
    o=header(d['phase'],d.get('title',title),d.get('grad','violet'))
    o+='<div class="a" style="right:130px;top:60px;display:flex;gap:12px">'+''.join('<span class="chd" style="width:26px;height:26px;border-radius:50%"></span>' for _ in range(n))+'</div>'
    o+='<div class="pg" style="position:absolute;left:90px;top:170px;width:1740px;height:750px"></div>'
    data={k:v for k,v in d.items() if k not in ('phase','m','label','levels','lvl','_lvg')}
    return o+f'<script type="application/json" id="d-{sid}">{json.dumps(data,ensure_ascii=False)}</script>'
def reg(name,title,cnt):
    BUILD_EXT[name]=lambda d,sid:pg_html(d,sid,title,cnt(d))
reg('odd','Odd one out',lambda d:len(d['items']))
reg('listen_fix','Listen and fix',lambda d:len(d['items']))
reg('triage','Triage sort',lambda d:len(d['items']))
reg('label_reader','Read the label',lambda d:len(d['qs']))
reg('taboo','Taboo for nurses',lambda d:len(d['items']))
reg('guess_who','Guess who',lambda d:d.get('rounds',2))
reg('ward_memory','Ward memory',lambda d:len(d['pairs']))
reg('predict','Watch and predict',lambda d:len(d['items']))

EXT_CSS.append("""
.pg{font-family:O;font-weight:800;color:#2a1c5a}
.plq{position:absolute;left:0;top:0;width:1700px;border-radius:44px;padding:20px 40px;font-size:46px;line-height:1.15}
.pbox{position:absolute;left:0;top:140px;width:1700px;display:flex;flex-wrap:wrap;gap:26px;justify-content:center}
.pcd{border:0;cursor:pointer;font-family:O;font-weight:800;color:#2a1c5a;background:rgba(255,255,255,.72);backdrop-filter:blur(14px);border-radius:44px;box-shadow:0 14px 30px rgba(80,60,160,.22),inset 0 4px 0 rgba(255,255,255,.8);padding:22px 30px;font-size:46px;min-width:340px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;transition:transform .2s,opacity .4s;position:relative}
.pcd i{font-style:normal;font-size:140px;line-height:1.1}.pcd:active{transform:scale(.96)}
.pcd.ok{background:linear-gradient(135deg,#2bd9b6,#10a98d);color:#fff}.pcd.glow{animation:wgl 1s infinite}.pcd.sel{outline:8px solid #ffd21f;transform:scale(1.05)}.pcd.fade{opacity:.18;pointer-events:none}
.prow{flex-direction:row;justify-content:space-between;width:1000px;min-width:0;padding:18px 44px;font-size:48px}.prow b{color:#6a35e8}.prow.ok b{color:#fff}
.pwhy{position:absolute;left:0;top:660px;width:1700px;text-align:center;font-size:44px;color:#6a35e8;opacity:0;transition:opacity .4s}
.ptq{position:absolute;left:0;top:0;width:1700px;display:flex;gap:20px;justify-content:center;flex-wrap:wrap}.ptq .pcd{min-width:0;font-size:36px;padding:14px 24px}.ptq .pcd i{font-size:70px}
.pbk{position:absolute;top:260px;width:540px;height:400px;border-radius:44px;border:6px solid;background:rgba(255,255,255,.45);cursor:pointer;display:flex;flex-direction:column;align-items:center;padding-top:14px;font-size:44px}
.pbk small{font-size:30px;opacity:.8}.pbl{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:10px;padding:0 10px}.pbl .pcd{min-width:0;font-size:26px;padding:8px 14px;border-radius:24px}.pbl .pcd i{font-size:36px}
.plab{position:absolute;left:0;top:0;width:900px;border-radius:44px;padding:20px 30px}.plab .pcd{width:100%;min-width:0;flex-direction:row;justify-content:flex-start;gap:20px;font-size:36px;margin:8px 0;padding:12px 26px;border-radius:30px;text-align:left}.plab .pcd i{font-size:48px}
.plab h3{margin:0 0 6px;font-size:52px;text-align:center}
.pqq{position:absolute;left:950px;top:0;width:750px;border-radius:44px;padding:30px 40px;font-size:50px;line-height:1.2;min-height:300px}
.ptb{position:absolute;left:0;top:0;width:1000px;height:560px;border-radius:56px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;font-size:96px;text-align:center}
.ptb ul{list-style:none;padding:0;margin:0;font-size:46px;color:#d3265c}.ptb ul li:before{content:"✖ "}
.pbt{border:0;cursor:pointer;font-family:O;font-weight:800;font-size:44px;padding:16px 40px;border-radius:999px;color:#fff;background:linear-gradient(135deg,#7b3cf0,#ff4fa3);box-shadow:inset 0 4px 0 rgba(255,255,255,.45);margin:10px}
.pbt.g{background:linear-gradient(135deg,#2bd9b6,#10a98d)}.pbt.o{background:linear-gradient(135deg,#ffd21f,#ffb21f);color:#2a1c5a}
.pfs{position:absolute;display:flex;flex-direction:column;align-items:flex-start}
.pwd{display:inline-block;padding:6px 18px;margin:4px 6px;border-radius:20px;cursor:pointer;font-size:62px;transition:background .3s}.pwd.bad{background:linear-gradient(135deg,#ff9a3c,#ff4fa3);color:#fff}.pwd.fx{background:linear-gradient(135deg,#2bd9b6,#10a98d);color:#fff}
.pmem{position:absolute;left:0;top:0;width:1700px;display:grid;gap:22px;justify-content:center}.pmem .pcd{height:200px;min-width:0;font-size:38px;text-align:center;line-height:1.1;padding:10px}.pmem .pcd i{font-size:96px}
.pmem .pcd.bk{background:linear-gradient(135deg,#9a5cff,#6a35e8);color:#fff;font-size:90px}.pmem .pcd.m{background:linear-gradient(135deg,#2bd9b6,#10a98d);color:#fff;pointer-events:none}
.pfr{position:absolute;top:0;display:flex;gap:30px}.pfr .pcd{width:440px;min-width:0;height:380px;opacity:0;transform:scale(.8);font-size:34px;text-align:center}.pfr .pcd.on{opacity:1;transform:scale(1)}
.gwg{position:absolute;left:0;top:130px;width:1100px;display:grid;grid-template-columns:repeat(6,1fr);gap:16px}.gwg .pcd{min-width:0;padding:10px;font-size:30px;height:200px}.gwg .pcd i{font-size:70px}.gwg .pcd small{font-size:36px;letter-spacing:4px}
.gwq{position:absolute;left:1140px;top:130px;width:560px;display:flex;flex-direction:column;gap:10px}.gwq .pcd{min-width:0;flex-direction:row;font-size:30px;padding:10px 22px;border-radius:30px}.gwq .pcd i{font-size:40px}.gwq .pcd.fade{opacity:.35}
""")
EXT_JS.append(r"""
/* ---- play modules ---- */
function jd(s){return JSON.parse($('#d-'+s.dataset.id).textContent)}
function pmk(t,c,h,p){var e=document.createElement(t);e.className=c||'';if(h!=null)e.innerHTML=h;if(p)p.appendChild(e);return e}
function pdots(s,k){$$('.chd',s).forEach(function(d,i){d.classList.toggle('on',i===k);d.classList.toggle('dn',i<k)})}
function psay(t){try{if(!SXL.say)return;speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(t);u.lang='en-GB';u.rate=.8;speechSynthesis.speak(u)}catch(e){}}
function pshuf(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a}
function plev(a,b){var m=[],i,j;for(i=0;i<=a.length;i++)m[i]=[i];for(j=0;j<=b.length;j++)m[0][j]=j;for(i=1;i<=a.length;i++)for(j=1;j<=b.length;j++)m[i][j]=Math.min(m[i-1][j]+1,m[i][j-1]+1,m[i-1][j-1]+(a[i-1]===b[j-1]?0:1));return m[a.length][b.length]}
function pstep(s,st,ms){setTimeout(function(){st.k++;if(st.k>=st.n)finish(s);else st.draw()},ms||1900)}
/* odd one out / wrong chart */
INIT.odd=function(s){var D=jd(s),I=D.items,st={k:0,n:I.length},mode=D.mode||'pic';
 st.draw=function(){pdots(s,st.k);var it=I[st.k],g=$('.pg',s),w=0,dn=0;g.innerHTML='';pmk('div','gl plq',D.q||(mode==='chart'?'What is wrong with this chart?':'Which one is different?'),g);
  var box=pmk('div','pbox',null,g),why=pmk('div','pwhy',it.why||'',g);
  var cs=it.cards.map(function(c,i){var b=pmk('button','pcd'+(mode==='chart'?' prow':''),mode==='chart'?'<span>'+c.t+'</span><b>'+c.v+'</b>':(mode==='pic'?'<i>'+(c.e||'')+'</i>':'')+'<span>'+c.t+'</span>',box);
   b.onclick=function(){if(dn)return;if(i===it.odd){dn=1;b.classList.add('ok');P('good');why.style.opacity=1;psay(it.why||'');pstep(s,st,2400)}else{wrong(b);w++;if(w>=3)cs[it.odd].classList.add('glow')}};return b})};
 st.draw()};
/* listen and fix */
INIT.listen_fix=function(s){var D=jd(s),I=D.items,st={k:0,n:I.length},mode=D.mode||'opts';
 st.draw=function(){pdots(s,st.k);var it=I[st.k],g=$('.pg',s),W=it.text.split(' '),H=it.say.split(' '),bad=-1,dn=0,w=0;for(var i=0;i<W.length;i++)if(W[i]!==H[i]){bad=i;break}
  g.innerHTML='';pmk('div','gl plq','<button class="pbt" style="margin:0 20px 0 0;font-size:44px">🔊 Listen</button>Tap the word that is different.',g).querySelector('button').onclick=function(){psay(it.say)};psay(it.say);
  var box=pmk('div','gl',null,g);box.style.cssText='position:absolute;left:0;top:170px;width:1700px;border-radius:44px;padding:40px;text-align:center;line-height:1.5';
  var ws=W.map(function(x,i){var e=pmk('span','pwd',x,box);e.onclick=function(){if(dn)return;if(i!==bad){wrong(e);return}dn=1;e.classList.add('bad');P('pop');ask()};return e});
  var area=pmk('div','',null,g);area.style.cssText='position:absolute;left:0;top:470px;width:1700px;text-align:center';
  function fixed(){ws[bad].textContent=H[bad];ws[bad].classList.remove('bad');ws[bad].classList.add('fx');P('good');psay(it.say);pstep(s,st,2200)}
  function ask(){area.innerHTML='<div style="font-size:42px;margin-bottom:14px">Fix it:</div>';
   if(mode==='type'){var inp=pmk('input','wty',null,area);inp.placeholder='type the right word';var b=pmk('button','pbt','Check',area);function chk(){var v=inp.value.trim().toLowerCase(),t=H[bad].toLowerCase().replace(/[^a-z0-9]/g,'');if(v===t||plev(v,t)<=1&&t.length>3){fixed()}else{w++;wrong(inp);if(w>=2)b.textContent='Starts with '+t[0].toUpperCase()}}b.onclick=chk;inp.onkeydown=function(e){if(e.key==='Enter')chk()};try{inp.focus()}catch(e){}}
   else pshuf(it.opts.concat([H[bad]])).forEach(function(o){var b=pmk('button','pcd',o,area);b.style.margin='0 14px';b.style.display='inline-flex';b.onclick=function(){if(o===H[bad]){b.classList.add('ok');fixed()}else wrong(b)}})}};
 st.draw()};
/* triage sort */
INIT.triage=function(s){var D=jd(s),B=D.buckets,I=pshuf(D.items),g=$('.pg',s),sel=null,left=I.length,placed=0;pdots(s,0);
 var q=pmk('div','ptq',null,g),note=pmk('div','pwhy','',g);note.style.top='680px';var cards=[];
 var bk=B.map(function(b,bi){var e=pmk('div','pbk','<span>'+(b.e||'')+' '+b.n+'</span><small>'+b.s+'</small><div class="pbl"></div>',g);e.style.left=(bi*580+10)+'px';e.style.borderColor=b.c;e.style.color=b.c;e.style.background='rgba(255,255,255,.55)';
  e.onclick=function(){if(!sel)return;var it=sel.__it;if(it.b===bi){P('pop');sel.classList.remove('sel');$('.pbl',e).appendChild(sel);sel.onclick=null;sel.style.cursor='default';placed++;pdots(s,placed);note.textContent=it.why||'';note.style.opacity=it.why?1:0;sel=null;if(--left===0){P('good');setTimeout(function(){finish(s)},1500)}}else{wrong(e);sel.classList.remove('sel');sel=null}};return e});
 I.forEach(function(it){var b=pmk('button','pcd',(D.show==='text'?'':'<i>'+(it.e||'')+'</i>')+'<span>'+it.t+'</span>',q);b.__it=it;b.onclick=function(){cards.forEach(function(c){c.classList.remove('sel')});b.classList.add('sel');sel=b;psay(it.t)};cards.push(b)})};
/* label reader */
INIT.label_reader=function(s){var D=jd(s),Q=D.qs,L=D.lab,st={k:0,n:Q.length};
 st.draw=function(){pdots(s,st.k);var g=$('.pg',s),dn=0,w=0,qq=Q[st.k];g.innerHTML='';var lab=pmk('div','gl plab','<h3>'+L.title+'</h3>',g),rows={};
  L.lines.forEach(function(l){var b=pmk('button','pcd',(l.e?'<i>'+l.e+'</i>':'')+'<span>'+l.t+'</span>',lab);rows[l.id]=b;b.onclick=function(){if(dn)return;if(l.id===qq.a){dn=1;b.classList.add('ok');P('good');pstep(s,st,1700)}else{wrong(b);w++;if(w>=3)rows[qq.a].classList.add('glow')}}});
  var q=pmk('div','gl pqq',(D.qtext===false?'<div style="font-size:120px;text-align:center">🎧</div>':qq.q)+'<br><button class="pbt" style="font-size:38px">🔊 Listen</button>',g);q.querySelector('button').onclick=function(){psay(qq.q)};psay(qq.q)};
 st.draw()};
/* taboo for nurses */
INIT.taboo=function(s){var D=jd(s),Q=pshuf(D.items),lim=D.limit||3,done=0,N=D.items.length,shown=0,t=null,tm=D.secs||0,left=tm;pdots(s,0);
 var g=$('.pg',s),card=pmk('div','gl ptb',null,g),btn=pmk('div','',null,g);btn.style.cssText='position:absolute;left:1040px;top:20px;width:660px;text-align:center';
 var info=pmk('div','',null,g);info.style.cssText='position:absolute;left:1040px;top:470px;width:660px;font-size:36px;text-align:center;color:#6a35e8';
 function draw(){var it=Q[0];card.innerHTML=shown?'<div style="font-size:120px">'+(it.e||'')+'</div><div>'+it.w+'</div><ul>'+it.no.slice(0,lim).map(function(x){return'<li>'+x+'</li>'}).join('')+'</ul>':'<div style="font-size:90px">🙈</div><div style="font-size:44px;font-weight:700">Describer only: tap Show.<br>Others: guess! Say it in English.</div>';
  btn.innerHTML='';var a=pmk('button','pbt o',shown?'🙈 Hide':'👀 Show',btn);a.onclick=function(){shown=!shown;P('tick');draw()};
  var b=pmk('button','pbt g','✔ Got it',btn);b.onclick=function(){P('good');Q.shift();done++;pdots(s,done);shown=0;if(!Q.length){finish(s);return}draw();clk()};
  var c=pmk('button','pbt','↷ Pass',btn);c.onclick=function(){Q.push(Q.shift());shown=0;P('tick');draw();clk()};
  info.innerHTML='Words left: '+Q.length+'<br>Do not say the ✖ words, or the word itself!'}
 function clk(){clearInterval(t);if(!tm)return;left=tm;t=setInterval(function(){left--;if(left<=0){clearInterval(t);info.innerHTML='⏰ Time! Pass the tablet.'}else info.innerHTML='⏳ '+left+' s<br>Words left: '+Q.length},1000)}
 draw();clk()};
/* guess who, patient edition */
INIT.guess_who=function(s){var D=jd(s),R=D.rounds||2,r=0,A=D.attrs,all=D.patients;
 function round(){pdots(s,r);var g=$('.pg',s),P1=pshuf(all).slice(0,D.n||all.length),sec=P1[Math.floor(Math.random()*P1.length)],done=0,asked=0;g.innerHTML='';
  var top=pmk('div','gl plq','Find the secret patient. Ask questions. Then tap your guess.',g);top.style.fontSize='40px';
  var grid=pmk('div','gwg',null,g),ans=pmk('div','pwhy','',g);ans.style.cssText='left:0;top:600px;font-size:56px;opacity:1;width:1100px';var qs=pmk('div','gwq',null,g);
  var cs=P1.map(function(p){var b=pmk('button','pcd','<i>'+p.e+'</i><small>'+p.a.map(function(k){return A.filter(function(x){return x.k===k})[0].e}).join('')+'</small>',grid);b.onclick=function(){if(done)return;if(p===sec){done=1;b.classList.add('ok');P('good');ans.textContent='🎉 Yes! That is the patient!';r++;setTimeout(function(){if(r>=R)finish(s);else round()},2000)}else{b.classList.add('fade');wrong(b)}};return b});
  A.forEach(function(a){var b=pmk('button','pcd','<i>'+a.e+'</i><span>'+(D.ask==='word'?a.w:a.q)+'</span>',qs);b.onclick=function(){if(done||b.classList.contains('fade'))return;b.classList.add('fade');var yes=sec.a.indexOf(a.k)>=0;psay(a.q);ans.textContent=(yes?'Yes ✔ ':'No ✖ ')+(yes?'The patient has ':'The patient does not have ')+a.w+'.';P(yes?'pop':'tick');
   P1.forEach(function(p,i){var has=p.a.indexOf(a.k)>=0;if(has!==yes)cs[i].classList.add('fade')})}})}
 round()};
/* ward memory */
INIT.ward_memory=function(s){var D=jd(s),P2=D.pairs,g=$('.pg',s),grid=pmk('div','pmem',null,g),open=[],lock=0,got=0,cols=P2.length>6?4:P2.length>4?4:4;pdots(s,0);grid.style.gridTemplateColumns='repeat('+cols+',360px)';
 function face(x){return /^[←-⯿\u{1F000}-\u{1FFFF}]/u.test(x)?'<i>'+x+'</i>':'<span>'+x+'</span>'}
 var cards=[];P2.forEach(function(p,i){cards.push({k:i,t:p.a},{k:i,t:p.b})});pshuf(cards).forEach(function(c){var b=pmk('button','pcd bk','?',grid);b.onclick=function(){if(lock||b.classList.contains('m')||open.indexOf(b)>=0)return;b.classList.remove('bk');b.innerHTML=face(c.t);b.__c=c;P('tick');psay(/^[←-⯿\u{1F000}-\u{1FFFF}]/u.test(c.t)?'':c.t);open.push(b);
  if(open.length===2){lock=1;var x=open[0],y=open[1];if(x.__c.k===y.__c.k){setTimeout(function(){x.classList.add('m');y.classList.add('m');P('good');got++;pdots(s,got);open=[];lock=0;if(got===P2.length)setTimeout(function(){finish(s)},900)},500)}else setTimeout(function(){[x,y].forEach(function(z){z.classList.add('bk');z.textContent='?'});open=[];lock=0},1100)}}})};
/* watch and predict */
INIT.predict=function(s){var D=jd(s),I=D.items,st={k:0,n:I.length};
 st.draw=function(){pdots(s,st.k);var it=I[st.k],g=$('.pg',s),dn=0,w=0;g.innerHTML='';var fr=pmk('div','pfr',null,g),F=it.frames.map(function(f,i){var c=pmk('div','pcd','<i>'+f.e+'</i>'+(D.cap===false?'':'<span>'+f.c+'</span>'),fr);return c});var fw=Math.min(440,Math.floor((1700-30*(it.frames.length-1))/it.frames.length));F.forEach(function(c){c.style.width=fw+'px'});fr.style.left=Math.max(0,(1700-(fw*it.frames.length+30*(it.frames.length-1)))/2)+'px';if(D.cap===false){fr.style.top='20px';F.forEach(function(c){c.style.height='500px';c.querySelector('i').style.fontSize='210px'})}
  var q=pmk('div','gl plq',it.q,g);q.style.top=(D.cap===false?'560px':'420px');q.style.opacity=0;var box=pmk('div','pbox',null,g);box.style.top=(D.cap===false?'700px':'560px');box.style.opacity=0;var out=pmk('div','pwhy',it.outcome||'',g);out.style.top='700px';
  F.forEach(function(c,i){setTimeout(function(){c.classList.add('on');P('pop');if(D.cap!==false)psay(it.frames[i].c)},700+i*1900)});
  setTimeout(function(){q.style.opacity=1;box.style.opacity=1;psay(it.q);if(!(it.opts||[]).length&&st.k===st.n-1)finish(s)},700+F.length*1900);
  var opts=(it.opts||[]).map(function(o,i){return{o:o,i:i}}),n=D.nopt||opts.length;if(n<opts.length){var rest=pshuf(opts.filter(function(x){return x.i!==it.a})).slice(0,n-1);opts=pshuf(rest.concat(opts.filter(function(x){return x.i===it.a})))}
  opts.forEach(function(x){var b=pmk('button','pcd','<i style="font-size:70px">'+(x.o.e||'')+'</i><span>'+x.o.t+'</span>',box);b.style.minWidth='300px';b.onclick=function(){if(dn)return;if(x.i===it.a){dn=1;b.classList.add('ok');P('good');out.style.opacity=1;psay(it.outcome||'');pstep(s,st,2800)}else{wrong(b);w++;if(w>=2){F.forEach(function(c){c.classList.remove('on');setTimeout(function(){c.classList.add('on')},300)})}}}})};
 st.draw()};
""")
