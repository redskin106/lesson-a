"""Lesson 6 modules (desert island). Art slots take emoji until real art arrives.
  item_pick(items[(emoji,name)], twists[(emoji,text)], sec)   Activate 1: pairs choose three items; teacher flags a twist
  next_event(first, mids, last, rounds, sec)                 Activate 2: What next? button reveals the next event card, sun sinks one step per round
Chrome comes from heist.install_chrome(); a slide carrying clock=/gear= keys also takes cicon= and gset= (see heist.chrome)."""
import json, html as _h
from ..core import *
from .. import core
from .heist import TEAMC


@module('item_pick')
def item_pick(d):
    """items = 12 x (emoji,name); twists = [(emoji,text)]; sec = pair-work timer.
    Tap a tile to mark it as a pair's pick (max 3). Teacher taps a twist chip to flag it."""
    o=header(d['phase'],d.get('role','What would you bring?'),'amber')+'<i class="nofit" style="display:none"></i>'
    o+=stp(glass(90,185,560,470,'<div style="height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px"><div style="font-size:210px;line-height:1">🏝️</div>'
        '<div style="font-size:110px;line-height:1">🎒 ❓</div>'
        '<div class="ipc" style="font-family:O;font-weight:800;font-size:60px;color:#6a35e8">0 / 3</div></div>',r=60),1)
    I=d['items']; w=270; h=206; g=18
    for i,(e,n) in enumerate(I):
        x=690+(i%4)*(w+g); y=185+(i//4)*(h+g)
        o+=stp(f'<div class="gl ipk" data-i="{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:44px;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px"><span style="font-size:118px;line-height:1.05">{e}</span><span style="font-family:O;font-weight:800;font-size:32px;color:#1c1b2e">{n}</span></div>',2)
    sec=int(d.get('sec',240))
    o+=stp(f'<div class="a tclock" data-sec="{sec}" style="left:90px;top:690px;width:400px;text-align:center;font-family:O;font-weight:800;font-size:120px;line-height:1"><span class="grad">{sec//60}:{sec%60:02d}</span></div>',3)
    o+=stp(f'<div class="a tstart" style="left:510px;top:702px;width:140px;height:100px;border-radius:50px;display:flex;align-items:center;justify-content:center;{GR}"><svg width="46" height="46" viewBox="0 0 56 56"><path d="M16 8 L48 28 L16 48 Z" fill="#fff"/></svg></div>',3)
    o+='<div class="a" style="left:90px;top:820px;width:560px;text-align:center;font-family:O;font-weight:800;font-size:34px;color:#4a3a8a">Pairs: choose three. Say why.</div>'
    tw=''.join(f'<div class="ipt" style="display:flex;align-items:center;gap:14px;padding:8px 30px;border-radius:999px;background:rgba(255,255,255,.8);border:4px solid #fff;font-family:O;font-weight:800;font-size:40px;color:#1c1b2e;cursor:pointer;box-shadow:0 8px 18px rgba(80,60,160,.14)"><span style="font-size:60px;line-height:1">{e}</span>{t}</div>' for e,t in d.get('twists',[]))
    o+=stp(f'<div class="a" style="left:690px;top:870px;width:1140px;display:flex;gap:18px;justify-content:center">{tw}</div>',4)
    return o


@module('next_event')
def next_event(d):
    """first/last = (emoji,text,kind); mids = [(emoji,text,kind)] (kind: bad | good); rounds = how many mids are drawn (shuffled on load).
    Teacher presses What next? : next card + timer restarts + sun sinks one step; team dots mark who answered this round."""
    deck=[d['first']]+list(d['mids'])+[d['last']]
    o=header(d['phase'],d.get('role','What next?'),'rose')+'<i class="nofit" style="display:none"></i>'
    data=dict(first=d['first'],mids=d['mids'],last=d['last'],rounds=d.get('rounds',4))
    o+=f'<script type="application/json" class="nxd">{_h.escape(json.dumps(data),False)}</script>'
    # sun track
    o+=('<div class="gl" style="left:90px;top:180px;width:1740px;height:120px;border-radius:60px"></div>'
        '<div class="a" style="left:150px;top:222px;font-size:62px;line-height:1">🏝️</div>'
        '<div class="a" style="left:1700px;top:222px;font-size:62px;line-height:1">⛵</div>'
        '<div class="a" style="left:260px;top:238px;width:1400px;height:12px;border-radius:6px;background:linear-gradient(90deg,#ffd166,#ff9f1c 55%,#d62f48)"></div>'
        '<div class="a nxsun" style="left:240px;top:200px;font-size:92px;line-height:1;transition:left .9s ease">☀️</div>')
    # card
    o+=('<div class="gl nxcard" style="left:90px;top:330px;width:820px;height:490px;border-radius:64px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:0 30px;box-sizing:border-box">'
        '<span class="nxk" style="position:absolute;right:34px;top:22px;font-size:70px"></span>'
        '<span class="nxe" style="display:block;height:260px;font-size:210px;line-height:260px">🌴</span>'
        '<span class="nxt" style="font-family:O;font-weight:800;font-size:56px;text-align:center;line-height:1.1;color:#1c1b2e">Press What next?</span></div>')
    # right: frame, timer, team dots
    fr=ch('c4','If we had …,',38,'6px 20px')+ch('c1','we would …',38,'6px 20px')+ch('c2','because …',38,'6px 20px')
    o+=f'<div class="a" style="left:950px;top:350px;width:880px;display:flex;gap:12px;flex-wrap:wrap;justify-content:center">{fr}</div>'
    sec=int(d.get('sec',45))
    o+=f'<div class="a tclock" data-sec="{sec}" style="left:950px;top:480px;width:440px;text-align:center;font-family:O;font-weight:800;font-size:150px;line-height:1"><span class="grad">0:{sec:02d}</span></div>'
    o+=f'<div class="a tstart" style="left:1430px;top:500px;width:150px;height:110px;border-radius:55px;display:flex;align-items:center;justify-content:center;{GR}"><svg width="50" height="50" viewBox="0 0 56 56"><path d="M16 8 L48 28 L16 48 Z" fill="#fff"/></svg></div>'
    dots=''.join(f'<span class="nxd1" style="width:104px;height:104px;border-radius:50%;background:{TEAMC[k]};opacity:.3;display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:54px;color:#fff;cursor:pointer;user-select:none">{k+1}</span>' for k in range(4))
    o+=f'<div class="a" style="left:950px;top:660px;width:880px;display:flex;gap:30px;justify-content:center;align-items:center"><span style="font-size:80px;line-height:1">🗣️</span>{dots}<span style="font-size:80px;line-height:1">✋</span></div>'
    o+='<div class="a" style="left:950px;top:790px;width:880px;text-align:center;font-family:O;font-weight:800;font-size:36px;color:#4a3a8a">Huddle. 2–3 teams answer. The class votes.</div>'
    o+=('<div class="a nxbtn" style="left:90px;top:855px;width:820px;height:120px;border-radius:60px;display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:64px;cursor:pointer;user-select:none;'+GR+'">What next? ▶</div>'
        '<div class="a nxbk" style="left:940px;top:870px;width:130px;height:90px;border-radius:45px;display:flex;align-items:center;justify-content:center;font-size:48px;cursor:pointer;background:rgba(255,255,255,.85);border:4px solid #fff;color:#6a35e8;user-select:none">◀</div>'
        '<div class="a nxpos" style="left:1100px;top:883px;font-family:O;font-weight:800;font-size:40px;color:#4a3a8a">0 / 0</div>')
    return o


EXT_CSS.append("""
.ipk.sel{box-shadow:0 0 0 10px #ff9f1c!important;background:rgba(255,236,190,.95)!important}.ipk.sel:after{content:"✔";position:absolute;right:16px;top:6px;font-size:46px;color:#10a98d}
.ipt.sel{box-shadow:0 0 0 8px #ff9f1c}.nxd1.on{opacity:1!important;box-shadow:0 0 0 6px #fff}
.nxcard.bad{box-shadow:0 0 0 10px #ff6b78!important}.nxcard.good{box-shadow:0 0 0 10px #2bd9b6!important}.nxcard.fin{box-shadow:0 0 0 10px #ffd166!important}
.nxcard .nxe{transition:transform .3s}.nxcard.pop .nxe{animation:nxp .5s ease-out 1}@keyframes nxp{0%{transform:scale(.4) rotate(-12deg)}60%{transform:scale(1.2)}100%{transform:scale(1)}}
""")
EXT_JS.append(r"""
document.addEventListener('click',function(e){var s=e.target.closest('.sl');if(!s)return;
 var k=e.target.closest('.ipk');
 if(k){var n=$$('.ipk.sel',s).length;if(k.classList.contains('sel')){k.classList.remove('sel');P('tick')}else if(n<3){k.classList.add('sel');P('pop')}else{P('boop')}var c=$('.ipc',s);if(c)c.textContent=$$('.ipk.sel',s).length+' / 3';return}
 var tw=e.target.closest('.ipt');if(tw){$$('.ipt',s).forEach(function(x){x.classList.toggle('sel',x===tw&&!tw.classList.contains('sel'))});P('pop');return}
 var d1=e.target.closest('.nxd1');if(d1){d1.classList.toggle('on');P('tick');return}
},true);
(function(){var SUN=['☀️','🌤️','⛅','🌥️','🌇','🌅'];
 function setup(s){if(s.__nx||!s.querySelector('.nxbtn'))return;s.__nx=1;
  var D=JSON.parse(s.querySelector('.nxd').textContent),mids=D.mids.slice();
  for(var i=mids.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=mids[i];mids[i]=mids[j];mids[j]=t}
  var deck=[D.first].concat(mids.slice(0,D.rounds),[D.last]),ix=-1,card=$('.nxcard',s),sun=$('.nxsun',s),btn=$('.nxbtn',s);
  function show(){var c=deck[ix];
   if(!c){$('.nxe',s).textContent='🌴';$('.nxt',s).textContent='Press What next?';$('.nxk',s).textContent='';card.className='gl nxcard'}
   else{$('.nxe',s).textContent=c[0];$('.nxt',s).textContent=c[1];$('.nxk',s).textContent=c[2]==='bad'?'⚠️':c[2]==='good'?'🍀':'🌅';card.className='gl nxcard '+(c[2]==='bad'?'bad':c[2]==='good'?'good':'fin');void card.offsetWidth;card.classList.add('pop')}
   var f=ix<0?0:ix/(deck.length-1);sun.style.left=(240+f*1330)+'px';sun.textContent=SUN[Math.min(SUN.length-1,Math.round(f*(SUN.length-1)))];
   $('.nxpos',s).textContent=(ix+1)+' / '+deck.length;btn.textContent=ix>=deck.length-1?'⛵ Boat!':'What next? ▶';
   $$('.nxd1',s).forEach(function(x){x.classList.remove('on')});
   if(s.__treset)s.__treset();}
  btn.onclick=function(ev){ev.stopPropagation();if(ix<deck.length-1){ix++;show();P(ix===deck.length-1?'good':'pop');if(ix<deck.length-1&&ix>=0&&s.__tauto)s.__tauto()}};
  $('.nxbk',s).onclick=function(ev){ev.stopPropagation();if(ix>-1){ix--;show();P('tick')}};
  s.__nxdeck=deck;s.__nxix=function(){return ix};show()}
 var iv=setInterval(function(){$$('.sl').forEach(setup)},400);})();
""")
