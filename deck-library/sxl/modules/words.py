"""Word-tile family (Batch 1): spell ("Name the illness"), scramble, unveil (hangman remastered).
One engine in JS (INIT.wordgame) drives three modes. Medals: put levels:[{bronze},{silver},{gold}] on the slide.
Rules: wrong answers never cost anything; a hint glow appears after repeated misses; collective (no scores); content is data.
Data: {'phase','title','items':[{'w':'dengue','clue':'A fever from mosquito bites.','pic':'🦟','cat':'an illness'}], ...mode options}
 spell:    mode 'tiles' (tap letters in order) or 'type' (keyboard, near-spelling accepted); showpic; decoys (extra letters)
 scramble: letters shuffled, tap to place; first=True locks the first letter
 unveil:   covered picture, alphabet keys; limit=N decoys on the keyboard (0 = only the word's letters, None = full); hint=True shows the category"""
import json
from ..core import *

def word_html(d,sid,kind):
    I=d['items']; o=header(d['phase'],d.get('title',{'spell':'Name the illness','scramble':'Unscramble','unveil':'What is it?'}[kind]),d.get('grad','violet'))
    o+=f'<div class="a" style="right:{(130 if d.get("_lvg") else 90)}px;top:60px;display:flex;gap:12px">'+''.join('<span class="chd" style="width:26px;height:26px;border-radius:50%"></span>' for _ in I)+'</div>'
    for k,it in enumerate(I):
        ph=520 if kind=='unveil' else 640
        o+='<div class="wi" style="display:none">'+f'<div class="wpic">{picx(it.get("pic","❓"),90,180,640,ph,56)}</div>'
        o+=f'<div class="wcov a" style="left:90px;top:180px;width:640px;height:{ph}px;border-radius:56px;overflow:hidden;display:none"></div>'
        o+=f'<div class="a wlisten" style="left:90px;top:180px;width:640px;height:{ph}px;display:none"><div class="gl" style="position:absolute;inset:0;border-radius:56px;display:flex;align-items:center;justify-content:center;font-size:190px">🎧</div></div>'
        if it.get('clue'): o+=f'<div class="gl wclue" style="left:780px;top:190px;width:1050px;border-radius:48px;padding:24px 38px;font-family:O;font-weight:800;font-size:{46 if len(it["clue"])<60 else 38}px;line-height:1.2;position:absolute">{it["clue"]} <button class="wsay" style="border:0;background:none;font-size:46px;cursor:pointer"><i class="sico"></i></button></div>'
        un=kind=='unveil'
        o+='<div class="a wslots" style="left:780px;top:%dpx;width:1050px;display:flex;flex-wrap:wrap;gap:12px"></div><div class="a whint" style="left:780px;top:%dpx;width:1050px;font-family:O;font-weight:800;font-size:36px;color:#6a35e8;opacity:0"></div>'%(400 if un else 420,670 if un else 610)
        o+=('<div class="a wbank" style="left:90px;top:730px;width:1740px;display:flex;flex-wrap:wrap;gap:12px;justify-content:center"></div></div>' if un else '<div class="a wbank" style="left:780px;top:690px;width:1050px;display:flex;flex-wrap:wrap;gap:12px;justify-content:flex-start"></div></div>')
    data={'kind':kind,'items':[{'w':i['w'],'cat':i.get('cat',''),'say':i.get('say',i['w'])} for i in I],**{k:d[k] for k in ('mode','showpic','decoys','first','limit','hint') if k in d}}
    return o+f'<script type="application/json" id="d-{sid}">{json.dumps(data,ensure_ascii=False)}</script>'
BUILD_EXT['spell']=lambda d,sid:word_html(d,sid,'spell')
BUILD_EXT['scramble']=lambda d,sid:word_html(d,sid,'scramble')
BUILD_EXT['unveil']=lambda d,sid:word_html(d,sid,'unveil')

EXT_CSS.append("""
.wt{box-sizing:border-box;display:flex;align-items:center;justify-content:center;padding:0;line-height:1;width:118px;height:132px;border-radius:34px;border:0;color:#fff;font-family:O;font-weight:800;font-size:74px;text-transform:uppercase;cursor:pointer;background:linear-gradient(135deg,#9a5cff,#6a35e8);box-shadow:0 12px 24px rgba(80,60,160,.3),inset 0 4px 0 rgba(255,255,255,.45);transition:transform .2s,opacity .3s}
.wt:active{transform:scale(.94)}.wt.used{opacity:.18;pointer-events:none}.wt.glow{animation:wgl 1s infinite}.wt.k{width:70px;height:80px;font-size:44px;border-radius:24px;background:linear-gradient(135deg,#ffd21f,#ffb21f)}.wt.k.hit{background:linear-gradient(135deg,#2bd9b6,#10a98d)}.wt.k.miss{opacity:.22;pointer-events:none}
@keyframes wgl{50%{box-shadow:0 0 0 14px rgba(255,210,31,.55)}}
.ws1{box-sizing:border-box;width:100px;height:116px;border-radius:30px;border:5px dashed #b9a6f5;display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:68px;text-transform:uppercase;color:#fff;cursor:default;transition:transform .25s}
.ws1.f{border:0;background:linear-gradient(135deg,#ff9a3c,#ff4fa3);box-shadow:0 12px 24px rgba(200,80,100,.3),inset 0 4px 0 rgba(255,255,255,.45);animation:wpop .35s}.ws1.sp{border:0;width:40px}.ws1.lk{background:linear-gradient(135deg,#2bd9b6,#10a98d)}
@keyframes wpop{0%{transform:scale(.6)}60%{transform:scale(1.12)}100%{transform:scale(1)}}
.wcv{background:linear-gradient(135deg,rgba(154,92,255,.92),rgba(111,60,232,.92));border:3px solid rgba(255,255,255,.7);transition:opacity .6s,transform .6s;display:flex;align-items:center;justify-content:center;color:#fff;font-family:O;font-weight:800;font-size:50px}.wcv.gone{opacity:0;transform:scale(.7);pointer-events:none}
.wty{font-family:O;font-weight:800;font-size:60px;padding:10px 30px;border-radius:30px;border:5px solid #d9d3f5;width:760px;outline:none;text-transform:lowercase}
.wok{border:0;cursor:pointer;font-family:O;font-weight:800;font-size:44px;padding:12px 44px;border-radius:999px;color:#fff;background:linear-gradient(135deg,#7b3cf0,#ff4fa3);margin-left:20px;box-shadow:inset 0 4px 0 rgba(255,255,255,.45)}
""")
EXT_JS.append(r"""
/* ---- word-tile engine: spell / scramble / unveil ---- */
function lev(a,b){var m=[],i,j;for(i=0;i<=a.length;i++){m[i]=[i]}for(j=0;j<=b.length;j++)m[0][j]=j;for(i=1;i<=a.length;i++)for(j=1;j<=b.length;j++)m[i][j]=Math.min(m[i-1][j]+1,m[i][j-1]+1,m[i-1][j-1]+(a[i-1]===b[j-1]?0:1));return m[a.length][b.length]}
function shufl(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a}
function wordgame(s){
 var D=JSON.parse($('#d-'+s.dataset.id).textContent),items=$$('.wi',s),dots=$$('.chd',s),k=0,kind=D.kind,mode=D.mode||'tiles',AB='abcdefghijklmnopqrstuvwxyz'.split('');
 function say(t){try{if(!SXL.say)return;speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(t);u.lang='en-GB';u.rate=.8;speechSynthesis.speak(u)}catch(e){}}
 function start(n){
  items.forEach(function(e,i){e.style.display=i===n?'block':'none'});dots.forEach(function(d,i){d.classList.toggle('on',i===n);d.classList.toggle('dn',i<n)});
  var it=items[n],W=D.items[n].w.toLowerCase(),L=W.split(''),slots=$('.wslots',it),bank=$('.wbank',it),hint=$('.whint',it),pic=$('.wpic',it),cov=$('.wcov',it),lis=$('.wlisten',it),wrongs=0,next=0,fails=0,done=0;
  slots.innerHTML='';bank.innerHTML='';
  var sp=L.map(function(c){var e=document.createElement('div');e.className='ws1'+(c===' '?' sp':'');if(c!==' ')e.dataset.c=c;slots.appendChild(e);return e});
  var nn=L.length,sw=Math.max(46,Math.min(130,Math.floor((1050-12*(nn-1))/nn)));sp.forEach(function(e){if(e.dataset.c){e.style.width=sw+'px';e.style.height=Math.round(sw*1.16)+'px';e.style.fontSize=Math.round(sw*.68)+'px'}});
  var need=sp.filter(function(e){return e.dataset.c});
  if(kind==='spell'&&D.showpic===false){pic.style.display='none';lis.style.display='block'}
  if(kind==='scramble'&&D.showpic===false){pic.style.display='none';lis.style.display='block'}
  var sy=$('.wsay',it);if(sy)sy.onclick=function(){say(D.items[n].say)};say(D.items[n].say);
  function win(){done=1;P('good');need.forEach(function(e){e.classList.add('f')});hint.style.opacity=1;hint.textContent='✔ '+W;say(D.items[n].say);
   if(kind==='unveil')$$('.wcv',cov).forEach(function(c){c.classList.add('gone')});
   setTimeout(function(){if(n===items.length-1)finish(s);else{k++;start(k)}},1700)}
  function glowTile(c){var b=$$('.wt',bank).filter(function(x){return x.dataset.c===c&&!x.classList.contains('used')&&!x.classList.contains('miss')})[0];if(b)b.classList.add('glow')}
  /* ---------- spell ---------- */
  if(kind==='spell'&&mode==='type'){
   var row=document.createElement('div');row.style.cssText='display:flex;align-items:center';row.innerHTML='<input class="wty" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="type the word"><button class="wok">Check</button>';bank.appendChild(row);
   slots.style.opacity=.55;need.forEach(function(e){e.textContent=''});
   var inp=$('input',row);setTimeout(function(){try{inp.focus()}catch(e){}},300);
   function chk(){var v=inp.value.trim().toLowerCase();if(!v)return;
    if(v===W){win();return}
    var tol=W.length>8?2:1;if(lev(v,W)<=tol){need.forEach(function(e,i){e.textContent=e.dataset.c});hint.style.opacity=1;hint.textContent='Nearly! ✔ '+W;done=1;P('good');setTimeout(function(){if(n===items.length-1)finish(s);else{k++;start(k)}},2200);return}
    fails++;P('boop');inp.classList.remove('shake');void inp.offsetWidth;inp.classList.add('shake');
    if(fails>=2){hint.style.opacity=1;hint.textContent='Starts with: '+W[0].toUpperCase()+'  ·  '+W.length+' letters'}if(fails>=4){var h=W.slice(0,Math.min(W.length,fails-1));hint.textContent='Starts with: '+h.toUpperCase()}}
   $('.wok',row).onclick=chk;inp.onkeydown=function(e){if(e.key==='Enter')chk()};return}
  /* ---------- spell tiles / scramble ---------- */
  if(kind==='spell'||kind==='scramble'){
   var dec=[];if(kind==='spell'&&D.decoys){var pool=AB.filter(function(c){return L.indexOf(c)<0});dec=shufl(pool).slice(0,D.decoys)}
   var tiles=shufl(need.map(function(e){return e.dataset.c}).concat(dec));
   if(kind==='scramble'&&D.first){var f=need[0];f.textContent=f.dataset.c;f.classList.add('f','lk');tiles.splice(tiles.indexOf(f.dataset.c),1)}
   var filled=[];
   tiles.forEach(function(c){var b=document.createElement('button');b.className='wt';b.textContent=c;b.dataset.c=c;b.style.width=sw+'px';b.style.height=Math.round(sw*1.16)+'px';b.style.fontSize=Math.round(sw*.68)+'px';bank.appendChild(b);
    b.onclick=function(){if(done)return;
     if(kind==='spell'){var e=need[next];if(e&&e.dataset.c===c){e.textContent=c;e.classList.add('f');b.classList.add('used');P('pop');setTimeout(function(){P('tick')},80);$$('.wt',bank).forEach(function(x){x.classList.remove('glow')});next++;wrongs=0;if(next===need.length)win()}
      else{wrongs++;wrong(b);if(wrongs>=2){var need2=need[next]&&need[next].dataset.c;if(need2)glowTile(need2)}}}
     else{var free=need.filter(function(e){return !e.classList.contains('f')})[0];if(!free)return;free.textContent=c;free.classList.add('f');free.__t=b;b.classList.add('used');P('pop');
      if(!need.some(function(e){return !e.classList.contains('f')})){var got=need.map(function(e){return e.textContent}).join(''),want=need.map(function(e){return e.dataset.c}).join('');
       if(got===want)win();else{fails++;P('boop');need.forEach(function(e){if(!e.classList.contains('lk')){e.classList.add('shake')}});setTimeout(function(){need.forEach(function(e){if(!e.classList.contains('lk')){e.classList.remove('shake','f');e.textContent='';if(e.__t)e.__t.classList.remove('used')}})},550);if(fails>=2){hint.style.opacity=1;hint.textContent='Hint: '+W.slice(0,Math.min(fails,W.length-1)).toUpperCase()+'…'}}}}}});
   if(kind==='scramble')need.forEach(function(e){e.style.cursor='pointer';e.onclick=function(){if(done||!e.classList.contains('f')||e.classList.contains('lk'))return;e.textContent='';e.classList.remove('f');if(e.__t)e.__t.classList.remove('used');P('tick')}});
   return}
  /* ---------- unveil ---------- */
  if(kind==='unveil'){
   cov.style.display='block';cov.innerHTML='';var cells=need.length,cols=Math.ceil(Math.sqrt(cells*1.25)),rows=Math.ceil(cells/cols);cov.style.display='grid';cov.style.gridTemplateColumns='repeat('+cols+',1fr)';cov.style.gridTemplateRows='repeat('+rows+',1fr)';
   var cv=[];for(var q=0;q<cols*rows;q++){var c=document.createElement('div');c.className='wcv';c.textContent='?';if(q>=cells)c.classList.add('gone');cov.appendChild(c);cv.push(c)}
   var order=shufl(cv.filter(function(e){return !e.classList.contains('gone')})),oi=0,use=AB;
   if(D.limit!==null&&D.limit!==undefined){var ex=shufl(AB.filter(function(c){return L.indexOf(c)<0})).slice(0,D.limit);use=AB.filter(function(c){return L.indexOf(c)>=0||ex.indexOf(c)>=0})}
   if(D.hint!==false){hint.textContent='It is '+(D.items[n].cat||'a word')+'. '+L.filter(function(c){return c!==' '}).length+' letters.';hint.style.opacity=1}
   var got=0;
   use.forEach(function(c){var b=document.createElement('button');b.className='wt k';b.textContent=c;b.dataset.c=c;bank.appendChild(b);
    b.onclick=function(){if(done||b.classList.contains('miss')||b.classList.contains('hit'))return;
     var hit=need.filter(function(e){return e.dataset.c===c});
     if(hit.length){b.classList.add('hit');P('pop');hit.forEach(function(e){e.textContent=c;e.classList.add('f');got++;var cc=order[oi++];if(cc)cc.classList.add('gone')});wrongs=0;if(got===need.length)win()}
     else{b.classList.add('miss');P('boop');wrongs++;if(wrongs>=3&&D.hint===false){hint.style.opacity=1;hint.textContent='It is '+(D.items[n].cat||'a word')+'.'}}}})}
 }
 s.__jump=function(i){k=i;start(i)};start(0)}
INIT.spell=wordgame;INIT.scramble=wordgame;INIT.unveil=wordgame;
""")
