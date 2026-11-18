"""Lessons 3 and 4, rebuilt from the reviewed library modules (L1-2 look). Build: python3 lessons/lessons34.py"""
import sys, pathlib
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent)); sys.path.insert(0,str(HERE.parent.parent/'lessons-3-4'/'src')); sys.path.insert(0,str(HERE))
import content as K
from sxl.interactive import build_interactive
import modules_gallery2 as G2, modules_gallery3 as G3
from sxl.modules.clue import stick, bubble_svg, ART
def _cards(cx,base,sc): return f'<rect x="{cx-16*sc}" y="{base-118*sc}" width="{30*sc}" height="{38*sc}" rx="4" fill="#ffc13b" stroke="#1c1b2e" stroke-width="4" transform="rotate(-10 {cx} {base-100*sc})"/>'
_P1=''.join(stick(x,395,1.15,'hold')+_cards(x,395,1.15) for x in (90,200,310))+'<text x="200" y="95" font-size="72" text-anchor="middle">🤫</text>'
_P2=stick(85,395,1.25,'throw')+'<circle cx="200" cy="175" r="21" fill="#ff9f1c" stroke="#1c1b2e" stroke-width="4"/><path d="M130 235 Q210 120 300 235" fill="none" stroke="#9a5cff" stroke-width="5" stroke-dasharray="3 12" stroke-linecap="round"/>'+stick(300,395,1.15,'up')+stick(365,395,1.0,'down')+bubble_svg(20,16,330,92,'Have you got\na clue about …?',fs=26,tx=105)
_P3=stick(100,395,1.15,'hold')+'<text x="150" y="330" font-size="52">📝</text>'+stick(300,395,1.2,'up')+bubble_svg(70,16,320,110,'Yes, we have.\nHer pulse is 104.',fs=26,tx=300)
_P4=('<rect x="40" y="40" width="320" height="230" rx="24" fill="#fff" stroke="#c9b6ff" stroke-width="5"/>'+''.join(f'<rect x="{62+c*100}" y="{64+r*100}" width="86" height="80" rx="14" fill="{"#2bd9b6" if (r,c)==(0,1) else "#efeaff"}"/>' for r in (0,1) for c in (0,1,2))+'<text x="205" y="125" font-size="46" text-anchor="middle" fill="#fff">✔</text>'+'<text x="250" y="258" font-size="64">👆</text>'+stick(70,395,1.15,'point')+'<text x="270" y="380" font-size="60">📝</text><text x="330" y="380" font-size="60">📝</text>')
HUNT_COMIC=[dict(svg=_P1,cap='3 of you hold a clue. 1 is the recorder.'),dict(svg=_P2,cap='One question per throw.'),dict(svg=_P3,cap='Answer in a full sentence.'),dict(svg=_P4,cap='Teacher taps. Everyone writes.')]
Q=lambda c,t:(c,t)
TEAMC=['#e0304a','#2a6ae0','#10a98d','#e89200']
def lv(items3): return [{'items':i} for i in items3]
def exch(e,phase='STUDY',**kw):
    fix=lambda it:dict(it,pic='🔁' if e['title'].startswith('How often') else '📅') if len(it['pic'])>4 else it
    d=dict(m='choice',phase=phase,title=e['title'],hint=e['hint'],label='Exercise · '+e['title'],lvl=1,levels=[{'items':[fix(i) for i in e['levels'][k]]} for k in ('bronze','silver','gold')]); d.update(kw); return d
L4SAY={'R1':'She says: two cups a day. The café card says: eight cups a day.','R2':'She sleeps three hours most nights. Normal is seven or more.','R3':'Her pulse is 108 to 112. Normal is 60 to 100.','B1':'She has no vomiting and no diarrhoea.','B2':'She studies until 2 am every night, for two weeks.','B3':'She has a headache most afternoons. It is 3 out of 10: mild.','G1':'Her hands shake for 30 minutes after every coffee.','G2':'She never coughs. No cough all week.','G3':'She cries a little when people talk about exams. She is quite worried.','Y1':'She never had this before the exams. It started two weeks ago.','Y2':'On Sunday she drank no coffee. She slept nine hours. She was not shaky or dizzy. She felt much better.','Y3':'She ate lunch with three friends. Her friends are fine.'}
def board(title,sus,clues,twist,test,ans,reveal,debate,rule=''):
    return dict(m='case_board',phase='ACTIVATE',title=title,label='Case board · '+title,min=14,teams=[(a,b,c,c2) for (a,b,c),c2 in zip(K.TEAMS,TEAMC)],suspects=sus,clues=[dict(c,text=L4SAY.get(c['id'],c.get('text')),dials=None,topic=c.get('topic') or K.TOPIC3.get(c['id']),short=(K.SHORT3 if clues is K.L3_CLUES else K.SHORT4).get(c['id'])) for i in (K.HUNT3 if clues is K.L3_CLUES else K.HUNT4) for c in clues if c['id']==i],hunt=True,frames=K.FRAMES,twist=twist,test=test,answer=ans,reveal=reveal,debate=debate,rule=rule)

# ============================ LESSON 3 ============================
def _q(pic,q,ans,*wrong,**kw): return dict(pic=pic,q=q,opts=[ans,*wrong],ans=ans,**kw)
SYM=[[_q('🌡️','What does the nurse write?','She has a fever.','She has a rash.','She has a cough.',say='I am so hot! Can I sleep in the fridge?'),
  _q('😷','What does the nurse write?','He has a cough.','He has a rash.','He has a fever.',say='Cough, cough! The whole ward is moving away from me.'),
  _q('🔴','What does the nurse write?','He has a rash on his arm.','He has a cough on his arm.','He has a fever on his arm.',say='Look at my arm! I look like a strawberry!'),
  _q('🤕','What does the nurse write?','He has a headache.','He has a rash.','He has a fever.',say='I studied all night. Now my head hurts so much!')],
 [_q('🤒','What does the nurse write?','She has a fever and a headache.','She has a fever and a rash.','She has a cough and a rash.',say='Hot skin. Pounding head. I only want my bed.'),
  _q('🦟','What does the nurse write?','She has a rash on her legs.','She has a cough on her legs.','She has a headache on her legs.',say='A mosquito bit me at the pond. Now my legs have red spots!'),
  _q('😷','What does the nurse write?','He has a cough, but he does not have a fever.','He has a fever, but he does not have a cough.','He has a cough and a fever.',say='I cough, but no fever. Do not worry, nurse!'),
  _q('💪','What does the nurse write?','Her head, her eyes and her muscles hurt.','Her head, her eyes and her muscles hurts.','Her head and her eyes hurt, but her muscles are fine.',say='My head, my eyes, my muscles… even my hair hurts!')],
 [_q('🤒','What does the nurse write?','She has a fever and a headache.','She have a fever and a headache.','She has fever and headache a.','She has a fever and a cough.',say='Fever and a headache. It is only a cold, nurse!'),
  _q('🦟','What does the nurse write?','She was bitten by a mosquito a week ago.','A mosquito was bitten her a week ago.','She bit a mosquito a week ago.','She was bite by a mosquito.',say='A mosquito bit me a week ago. Now I am sick.'),
  _q('🔴','What does the nurse write?','She has a rash on her arms but not on her face.','She has a rash on her arms but no on her face.','She have rash on arms, not face.','She has a rash on her face but not on her arms.',say='Red spots on my arms, but not on my face. Phew!'),
  _q('🥵','What does the nurse write?','She has a very high fever.','She has a low fever.','She have a very high fever.','She has fever very high.',say='I only feel a little warm. (Thermometer: 41 °C)')]]
U_PL='×10⁹/L'
HL=dict(bronze=[
  _q('🌡️','The normal temperature is 37 °C. Her temperature is 39.2 °C. Her temperature is ___ than normal.','higher','lower'),
  _q('🩸',f'Normal platelets: 150,000 to 450,000 per µL. Her platelets: 95,000 per µL. Her platelets are ___ than normal.','lower','higher'),
  _q('🫁','Normal breathing: 12 to 20 breaths per minute. Her breathing: 18 breaths per minute. Her breathing is ___.','normal','higher','lower'),
  _q('💓','Normal pulse: 60 to 100 beats per minute. Her pulse: 48 beats per minute. Her pulse is ___ than normal.','lower','higher')],
 silver=[
  _q('🌡️','Normal temperature: 37 °C. Her temperature: 39.2 °C.','Her temperature is much higher than normal.','Her temperature is slightly higher than normal.','Her temperature is lower than normal.'),
  _q('💓','Normal pulse: 60 to 100 beats per minute. Her pulse: 104 beats per minute.','Her pulse is slightly higher than normal.','Her pulse is much lower than normal.','Her pulse is normal.'),
  _q('🩸',f'Normal white cells: 4,500 to 11,000 per µL. Her white cells: 3,100 per µL.','Her white cells are lower than normal.','Her white cells are much higher than normal.','Her white cells are normal.'),
  _q('🌡️','Normal temperature: 37 °C. Her temperature: 38.1 °C.','Her temperature is slightly higher than normal. It is a mild fever.','Her temperature is much higher than normal.','Her temperature is lower than normal.')],
 gold=[
  _q('🥵','A patient says "I feel a little warm." The thermometer says 41 °C. Normal is 37 °C.','Her temperature is dangerously higher than normal. It is not a little warm!','Her temperature is slightly higher than normal.','Her temperature is much lower than normal.','Her temperature is normal.'),
  _q('🩸',f'Platelets: 95,000 per µL. Normal: 150,000 to 450,000 per µL.','Her platelets are much lower than the normal range.','Her platelets are much more low than normal.','Her platelets are within the normal range.','Her platelets is lower than normal.'),
  _q('🫁','Breathing: 18 breaths per minute. Normal: 12 to 20 breaths per minute.','Her breathing is within the normal range.','Her breathing is higher than the normal range.','Her breathing is lower than the normal range.','Her breathing is normal than.'),
  _q('💓','A sleeping marathon runner: 48 beats per minute. Normal for most adults: 60 to 100.','Her pulse is lower than the normal range, but she is very fit.','Her pulse is much higher than normal.','Her pulse is normal.','Her pulse are lower than normal.')])
def _d(e,now,normal,s_,z): return dict(e=e,now=now,normal=normal,s=s_,z=z)
DIAL_DEMO=[_d('💓','Pulse: 104 beats per minute','60 to 100 beats per minute','Her pulse is',4),
 _d('🌡️','Temperature: 39.2 °C','about 37 °C','Her temperature is',5),
 _d('🌡️','Temperature: 41 °C','about 37 °C','Her temperature is',6),
 _d('🫁','Breathing: 16 breaths per minute','12 to 20 breaths per minute','Her breathing is',3)]
DIAL_LV=[
 [_d('💓','Pulse: 104 beats per minute','60 to 100 beats per minute','Her pulse is',4),_d('🌡️','Temperature: 41 °C','about 37 °C','Her temperature is',6),_d('🫁','Breathing: 16 breaths per minute','12 to 20 breaths per minute','Her breathing is',3),_d('💓','Pulse: 56 beats per minute','60 to 100 beats per minute','Her pulse is',2)],
 [_d('🌡️','Temperature: 39.2 °C','about 37 °C','Her temperature is',5),_d('🫁','Breathing: 21 breaths per minute','12 to 20 breaths per minute','Her breathing is',4),_d('🩸',f'Platelets: 95,000 per µL',f'150,000 to 450,000 per µL','Her platelets are',1),_d('💓','Pulse: 130 beats per minute','60 to 100 beats per minute','Her pulse is',5)],
 [_d('🌡️','Temperature: 32 °C','about 37 °C','Her temperature is',0),_d('💓','Pulse: 42 beats per minute','60 to 100 beats per minute','Her pulse is',1),_d('🩸',f'Platelets: 20,000 per µL',f'150,000 to 450,000 per µL','Her platelets are',0),_d('🫁','Breathing: 40 breaths per minute','12 to 20 breaths per minute','Her breathing is',6)]]
L3=[
 dict(m='cover',phase='ENGAGE',label='Cover',title='Lesson <span class="grad">3</span>',phases=['Engage','Study','Activate'],active=0,cards=[dict(pic='🩺',x=1010,y=150,w=330,h=430,r=-7),dict(pic='🌡️',x=1380,y=330,w=330,h=430,r=6)]),
 dict(m='vol_ladder',phase='ENGAGE',label='Eyes closed. Louder.',min=3,title=None,clips=['bello.mp3','banana.mp3','papaya.mp3','kampai.mp3'],rungs=['Bello!','Banana!','Tu e bella<br>como la papaya!','KAMPAI!'],side='Everyone, eyes closed, at the same time. Whisper first. Each word is louder.'),
 dict(m='predict',phase='ENGAGE',label='Meet the patient',min=3,title='Meet the patient',cap=False,items=[dict(frames=[dict(e='🧍‍♀️',c='She walks in. She looks hot.'),dict(e='🌡️',c='The nurse takes her temperature.'),dict(e='😟',c='The nurse looks worried.')],q='❓ What is wrong with her?')]),
 dict(m='today',phase='STUDY',label='Today',min=1,emoji='stethoscope',title='Detective nurses',role='Today we are',rows=[[('c4','Ask'),('c3','the right question')],[('c1','Read'),('c3','the numbers')],[('c2','might'),('c4',"can't"),('c3','because')]]),
 dict(m='teach',phase='STUDY',label='Teach · Symptoms',min=2,role='Four symptoms',words=[('🤒','fever'),('🤕','headache'),('😷','cough'),('🔴','rash')]),
 dict(m='teach',phase='STUDY',label='Teach · Symptom sentences',min=2,role='Listen to the patient',pic='🤒',tts=True,hint='Tap a line. Listen to the patient. Then say what the nurse writes.',lines=[('She has a fever.','Ohhh… why is it so hot in here? Is the air-con broken?'),('He has a headache.','My head… boom, boom, boom. Like a drum!'),('He has a cough.','Cough, cough… sorry… I sound like a goat!'),('She has a rash on her arm.','Look at my arm! Red spots! What is wrong with me?')]),
 dict(m='choice',phase='STUDY',title='Symptoms',hint='Choose the right word or sentence.',label='Exercise · Symptoms',min=3,lvl=3,levels=lv(SYM)),
 dict(m='teach',phase='STUDY',label='Teach · Higher or lower',min=2,role='Compare with normal',pic='🌡️',lines=['The normal temperature is 37 °C.','Her temperature is 39.2 °C.','Her temperature is higher than normal.','She has a fever.']),
 dict(m='dial',phase='STUDY',label='Teach · The dial (slightly, much, dangerously)',min=3,title='How much higher? How much lower?',items=DIAL_DEMO,hint='Tap the zone. Say the sentence.'),
 dict(m='teach',phase='STUDY',label='Teach · How much?',min=2,role='How much higher?',pic='💓',lines=['Her pulse is 104. Normal is 60 to 100. It is slightly higher.','Her temperature is 41 °C. Normal is 37 °C. It is dangerously high.',f'Her platelets are 95,000 per µL. Normal is 150 to 450. They are much lower.','Her breathing is 18. Normal is 12 to 20. It is about normal.']),
 exch(dict(K.L3_EX[1],levels=HL),min=4,lvl=3),
 dict(m='dial',phase='STUDY',label='Exercise · The dial',min=3,optional=True,title='The dial',lvl=3,levels=[dict(items=x) for x in DIAL_LV],hint='Tap the zone. Say the sentence.'),
 dict(m='teach',phase='STUDY',label='Teach · Might, can\'t, because',min=2,role='Clue → sentence',pic='🦟',lines=['Clue: mosquito bites.','It might be dengue.','Clue: her belly does not hurt.','It can\'t be appendicitis.']),
 exch(K.L3_EX[2],min=3),
 dict(m='teach',phase='STUDY',label='Teach · Ask the patient',min=2,role='Good questions',pic='🩺',lines=['How long have you had a fever?','Where does it hurt?','Do you have a cough?','Did a mosquito bite you?']),
 dict(m='build',phase='STUDY',label='Exercise · Ask the patient (1)',title='Ask the patient',min=3,lvl=1,levels=[dict(pics=['🌡️'],parts=[Q('c4','How'),Q('c4','long'),Q('c2','have'),Q('c1','you'),Q('c2','had'),Q('c3','a fever?')],extra=e) for e in ([],[('c2','did'),('c2','are')],[('c2','did'),('c2','are'),('c4','since'),('c4','for')])]),
 dict(m='build',phase='STUDY',label='Exercise · Ask the patient (2)',title='Ask the patient',min=2,optional=True,lvl=1,levels=[dict(pics=['🦟'],parts=[Q('c2','Did'),Q('c1','a mosquito'),Q('c4','bite'),Q('c3','you?')],extra=e) for e in ([],[('c2','Have'),('c2','were')],[('c2','Have'),('c2','were'),('c2','bitten'),('c4','bit')])]),
 dict(m='spell',phase='STUDY',label='Extra · Name the illness',optional=True,min=3,title='Name the illness',items=G2.ITEMS,lvl=1,levels=[dict(mode='tiles',showpic=True,decoys=0),dict(mode='tiles',showpic=False,decoys=4),dict(mode='type',showpic=False)]),
 dict(m='odd',phase='STUDY',label='Extra · What is wrong with this chart?',optional=True,min=2,items=G3.CHART,lvl=2,mode='chart'),
 dict(m='frames3',phase='ACTIVATE',label='Your sentences',min=2,title='Your sentences (they stay on the board)',groups=[
   {'t':'Easy','c':'teal','l':['She has a fever.','Her pulse is slightly higher than normal.','It might be dengue.'],'fs':44},
   {'t':'Better','c':'sky','l':['Her temperature is much higher than normal.',"It can't be appendicitis because her belly does not hurt."],'fs':42},
   {'t':'Stretch','c':'rose','l':['It is unlikely to be flu because she has no cough.','It is probably dengue, because she has a rash and she had mosquito bites.','Her platelets are much lower than normal.'],'fs':36}],note='Any sentence that carries the meaning is good.'),
 dict(m='comic',phase='ACTIVATE',label='How the hunt works',min=2,title='How the hunt works',panels=HUNT_COMIC),
 board('Find the illness',K.L3_SUSPECTS,K.L3_CLUES,K.L3_TWIST,K.L3_TEST,K.L3_ANSWER,'<b>It is dengue.</b><br>She has had a fever for three days and a rash on her arms and chest.<br>Her platelets and white cells are lower than normal.<br>She was bitten by mosquitoes a week ago.<br>It can\'t be flu, because she has no cough.<br>It can\'t be appendicitis, because her belly does not hurt.',
   dict(title="Wait… which can't it be?",lines=['Stand at the illness you believe.','Say why in one sentence.','Better reason? Move.']),rule='Say it in a full sentence.'),
 dict(m='boss',phase='ACTIVATE',label='Boss question (just for fun)',optional=True,min=3,**K.L3_BOSS,sec=90),
 dict(m='listen_fix',phase='ACTIVATE',label='Listen and fix (handover)',min=3,optional=True,title='Listen and fix',items=[
   dict(text='Her temperature is lower than normal',say='Her temperature is higher than normal',opts=['lowest','more']),
   dict(text='She has a cough',say='She has no cough',opts=['not','any']),
   dict(text='The rash is on her face',say='The rash is on her chest',opts=['arm','leg'])],lvl=1,levels=[dict(mode='opts'),dict(mode='opts'),dict(mode='type')]),
 dict(m='frames3',phase='ACTIVATE',label='Tell the doctor (handover)',min=8,optional=True,title='Tell the doctor',h=780,groups=[
   {'t':'Easy · fill the gaps','c':'teal','l':['A young woman. Day 3 of fever.','Her temperature is ___ than normal.','She has ___ and ___. No ___.','It is probably ___ because ___.'],'fs':34},
   {'t':'Better · S B A','c':'sky','l':['<b>S</b>  Patient: ___. Day ___ of ___.','<b>B</b>  She had ___ last week.','<b>A</b>  It might be ___. It can\'t be ___ because ___.'],'fs':34},
   {'t':'Stretch · your patient','c':'rose','l':['Invent your own patient.','Pick 4 facts. Say <b>S B A</b>.','<b>R</b>  "Please check ___."','Use might · can\'t · because.'],'fs':34}],note='Write it on paper. Then tell your partner.'),
 dict(m='qr_card',phase='ACTIVATE',label='Taboo rules',min=2,title='Taboo for nurses',rules=['Groups of 4. One person describes.','Only the describer looks at the phone.','Say the word <u>without</u> the ✖ words.','Words only. 🚫 No miming. 🚫 No drawing. 🚫 No pointing.'],qr='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAV4AAAFeCAIAAABCSeBNAAAHv0lEQVR4Xu3d3a3bRhSF0dzAZSQ1pP8yUkPSB/Max4PRhjcOZqSs9WxJwx8TH4kD3q/neX4B+N6vdgjwI5cGwKUByKgGQDUAGdUAqAYgoxoA1QBkvu3/2e+//ZF9z9v46+8/f3qtp/bGfs37Vc1tb/PNc2fdnau6035fuaEA3FAAGdUAqAYgoxoA1QBkVAOgGoCMagAWXkxD7s1NnjWamcXPmyzcO7Wvmt+986y7c1XNflYNgGcNQEY1AKoByKgGQDUAGdUAqAYgoxqAhWoacq+ZxNo7NXnWbNHc+x3n9kaz5uYI7vdzcxSaVTXecc2qAVhwaQBcGoCMagBUA5BRDYBqADKqAVANQGZwGvLzNNOBp9462WjWPDf/15ibHP08bigANxRARjUAqgHIqAZANQAZ1QCoBiCjGoAF05DfOTUt18wONmu+c95xbovIqQbAswYgoxoA1QBkVAOgGoCMagBUA5BRDcDC4DRkM9N2p2Z2cK/55uazjeb4NtOfe837O5stalZ1J9UALLg0AC4NQEY1AKoByKgGQDUAGdUAqAYgU01Dzs20ndJMFjaffUentvfU7+593v8FNxSAGwogoxoA1QBkVAOgGoCMagBUA5BRDcDCi2nIubflfZ7mrYSNdzxGc2uem5WcW/OdVAPgWQOQUQ2AagAyqgFQDUBGNQCqAcioBmDh63mezY6Zmy2b06x57g1/zSxds6q5322+udHsjTnN3pjbomZVqgHwrAHIqAZANQAZ1QCoBiCjGgDVAGRUA7DwYhpyr5niat6k2Mx4nVoz/9Yc/UZz5jSas25vbotUA7Dg0gC4NAAZ1QCoBiCjGgDVAGRUA6AagMyLv5TdTHE1E2/NjFfzbsg5zd6409wxapxaVfO7zbkxd7a7oQDcUAAZ1QCoBiCjGgDVAGRUA6AagIxqABYG/1J2M6c1N4XZaLao0fzuqT0597vNN+81E41zq5qz317VAHjWAGRUA6AagIxqAFQDkFENgGoAMqoBWHjxbsi9uSm9ubm05j18p/ZGY257/2+aecfmfG7OuoZqABZcGgCXBiCjGgDVAGRUA6AagIxqAFQDkHkxDdnM0jWzkntz39xMrTXTcnunVjW3Rc3xbTR7cs7c+dxwQwG4oQAyqgFQDUBGNQCqAcioBkA1ABnVACy8mIY8NafV/G4zw9dMf85ptmivmQ5sjlFj7neb/XznmdMcX9UAeNYAZFQDoBqAjGoAVAOQUQ2AagAyqgFYqP5SdqOZPDs1D9fMljXb20zaNWt+R3PnxtxR2K+52aLms6oB8KwByKgGQDUAGdUAqAYgoxoA1QBkVAOwMPiXsk/N4c3NHc6Z21fNPFzz2TnNVOIpd+7JPdUAeNYAZFQDoBqAjGoAVAOQUQ2AagAyqgFYGPxL2XdOgDXv4Ws0M3ynZiUbczOpzTc35s7nU1u0pxoAzxqAjGoAVAOQUQ2AagAyqgFQDUBGNQAL1bshG81s2dz0WDOzuHfnmufmLO80d9Y139yYO2NVA+BZA5BRDYBqADKqAVANQEY1AKoByKgGYKF6N+Te3KRd881zU4nN3phbVbOv3lGzvXMTjXPHd+6bVQPgWQOQUQ2AagAyqgFQDUBGNQCqAcioBmDhxTTk3udNnjXzcKf+BndjbpZuztxZ15jbk832NlQDsODSALg0ABnVAKgGIKMaANUAZFQDoBqATDUNudfMhzWfnZsea1Y1p1nVqX3V/O7c9t75zae4oQDcUAAZ1QCoBiCjGgDVAGRUA6AagIxqABYGpyH35ubhmvc7Nk5t0Z32e2Nu7rDRHMG5s31v7mxXDcCCSwPg0gBkVAOgGoCMagBUA5BRDYBqADKD05Bz83B7czNtjTvn/+bMbW/zzc2ZMzd3uDe3vXtuKAA3FEBGNQCqAcioBkA1ABnVAKgGIKMagIWv53k2O+bUJNacUzOae80EZzOl13y20fzu552Tc+dGQzUACy4NgEsDkFENgGoAMqoBUA1ARjUAqgHIvHg3ZDOl93nmJimbCb+5Ve3dueZmb8yd7XdOf+631w0F4IYCyKgGQDUAGdUAqAYgoxoA1QBkVAOw8GIaspl4u9N+AuwdZ+kazfbuzU0W7s2dsc1E4ynNUVANwIJLA+DSAGRUA6AagIxqAFQDkFENgGoAMi+mIfeaWas5c/Nwc5o1N5+dO77N7GBzXt25N/bm1twcBTcUgBsKIKMaANUAZFQDoBqAjGoAVAOQUQ3AQjUNuTc349VMyzXm3qQ4p9lXzRFsfrfRHKNme+c0W9QcBdUALLg0AC4NQEY1AKoByKgGQDUAGdUAqAYgMzgN+XmaN+2dmrRrfreZw2v21V6zRY1mb5zSHAU3FIAbCiCjGgDVAGRUA6AagIxqAFQDkFENwIJpyDfwjnN4e3MTje+4r+5cs2oAPGsAMqoBUA1ARjUAqgHIqAZANQAZ1QAsDE5DNn+l905zU2vNNzefndOsqjlzmrchntLMhjb7ak81AJ41ABnVAKgGIKMaANUAZFQDoBqAjGoAFqppyGaK606ntmjud5tpublVnXJqi5qjsDc3/akaAM8agIxqAFQDkFENgGoAMqoBUA1ARjUAC1/P89gxwH+oBmDBpQFwaQAyqgFQDUBGNQCqAcioBkA1AJl/AMjkld1QO5K7AAAAAElFTkSuQmCC',url='redskin106.github.io/lesson-a/lessons-3-4/taboo3.html',caption='Scan: describer only'),
 dict(m='taboo',phase='ACTIVATE',label='Taboo for nurses (demo / class version)',min=3,optional=True,items=G3.TB+[dict(w='rash',e='🔴',no=['red','skin','spots','itchy'])],lvl=1,levels=[dict(limit=2),dict(limit=3,secs=60),dict(limit=4,secs=45)]),
 dict(m='recap',phase='RECAP',label='Recap',min=2,rows=[([('c1','Her temperature'),('c2','is'),('c3','slightly higher')],'than normal'),([('c1','It'),('c2','might be'),('c3','dengue.')],'maybe'),([('c1','It'),('c2',"can't be"),('c3','flu')],'because…'),([('c2','Have'),('c1','you'),('c3','had a fever?')],'ask')],emoji='stethoscope'),
 dict(m='closing',phase='EXIT',label='Thank you',min=1,stack=True,line1='Thank',line2='you!',sub='See you next time.',emoji='handshake'),
]

# ============================ LESSON 4 ============================
def cmp3(b,s,g): return dict(m='choice',phase='STUDY',title='Compare',hint='Look at the numbers. Choose the sentence.',label='Exercise · Compare (than · the most)',optional=True,min=3,lvl=1,levels=lv([b,s,g]))
C4=lambda pic,q,opts,ans:dict(pic=pic,q=q,opts=opts,ans=ans)
CMP=cmp3(
 [C4('☕','Monday: 2 cups. Friday: 4 cups.',['Friday has more coffee than Monday.','Monday has more coffee than Friday.','Friday has the same coffee as Monday.'],'Friday has more coffee than Monday.'),
  C4('😴','Monday: 3 hours of sleep. Thursday: 2 hours.',['Thursday has less sleep than Monday.','Thursday has more sleep than Monday.','Monday has less sleep than Thursday.'],'Thursday has less sleep than Monday.'),
  C4('💓','Her pulse: 110. Normal: 80.',['Her pulse is faster than normal.','Her pulse is slower than normal.','Her pulse is the same as normal.'],'Her pulse is faster than normal.')],
 [C4('😴','Mon 3h · Tue 4h · Wed 3h · Thu 2h · Fri 3h. Which night is the worst?',['Thursday is the worst night.','Thursday is the worse night.','Thursday is the most bad night.','Tuesday is the worst night.'],'Thursday is the worst night.'),
  C4('☕','Mon 2 · Tue 3 · Wed 2 · Thu 3 · Fri 4 cups.',['She drinks the most coffee on Friday.','She drinks the more coffee on Friday.','She drinks the most coffee on Monday.','She drinks most coffee than Friday.'],'She drinks the most coffee on Friday.'),
  C4('😴','Tuesday: 4 hours. Thursday: 2 hours.',['She sleeps more on Tuesday than on Thursday.','She sleeps more on Tuesday that on Thursday.','She sleeps the more on Tuesday.','She sleeps most than on Thursday.'],'She sleeps more on Tuesday than on Thursday.')],
 [C4('🥱','Monday: tired. Friday: very tired.',['She is more tired on Friday than on Monday.','She is tireder on Friday than on Monday.','She is the most tired on Monday than Friday.','She is more tired Friday than Monday.'],'She is more tired on Friday than on Monday.'),
  C4('💓','Pulse: Mon 90 · Wed 100 · Fri 110.',['Friday has the fastest pulse of the week.','Friday has the most fast pulse of the week.','Friday has a faster pulse of the week.','Monday has the fastest pulse of the week.'],'Friday has the fastest pulse of the week.'),
  C4('☕','She drinks 8 cups. Normal: about 4.',['She drinks twice as much coffee as normal.','She drinks twice more coffee than normal.','She drinks twice much as normal.','She drinks twice as many coffee than normal.'],'She drinks twice as much coffee as normal.')])
# ================= L3 post-processing: 16 Nov review round =================
TABOO3=[d for d in L3 if d['m']=='taboo'][0]
ROOM_SPOTS=[dict(e='🌡️',x=1130,y=300,t='A thermometer: 39.2 °C.'),dict(e='🦟',x=640,y=40,t='There is a hole in the mosquito net.'),dict(e='🍱',x=1350,y=470,t='Half-eaten rice. She is not hungry.'),
 dict(e='🧻',x=130,y=470,t='A box of tissues. It is empty.'),dict(e='💊',x=1430,y=240,t='Paracetamol. Two tablets yesterday.'),dict(e='📅',x=330,y=70,t='A calendar. Day 3 is circled.'),
 dict(e='🏞️',x=110,y=250,t='A pond outside the window.'),dict(e='🐱',x=1120,y=520,t='A sleepy cat.')]
DIAL_MIX=[_d('💓','Pulse: 104 beats per minute','60 to 100 beats per minute','Her pulse is',4),_d('🌡️','Temperature: 39.2 °C','about 37 °C','Her temperature is',5),
 _d('🌡️','Temperature: 41 °C','about 37 °C','Her temperature is',6),_d('🫁','Breathing: 16 breaths per minute','12 to 20 breaths per minute','Her breathing is',3),
 _d('💓','Pulse: 56 beats per minute','60 to 100 beats per minute','Her pulse is',2),_d('🩸',f'Platelets: 95,000 per µL',f'150,000 to 450,000 per µL','Her platelets are',1)]
CUT3={'Teach · How much?','Exercise · The dial','Extra · Name the illness','Extra · What is wrong with this chart?','Listen and fix (handover)','Taboo for nurses (demo / class version)'}
_new=[]
for d in L3:
    lb=d.get('label')
    if lb in CUT3: continue
    if lb=='Meet the patient': d=dict(m='room',phase='ENGAGE',label='The room of clues',min=3,title='The room of clues',spots=ROOM_SPOTS)
    elif lb=='Eyes closed. Louder.': d=dict(d,min=2)
    elif lb=='Teach · Symptom sentences':
        d=dict(d,pics=['🤒','🤕','😷','🔴'],role='Listen to the patient',lines=[('She has a fever.','Ohhh… why is it so hot in here? Is the air-con broken?'),('He has a headache.','My head… boom, boom, boom. Like a drum!'),('He has a cough.','Cough, cough… sorry… I sound like a goat!'),('She has a rash on her arm.','Look at my arm! Red spots! Am I turning into a tomato?')])
        d.pop('hint',None)
    elif lb=='Teach · Higher or lower':
        d=dict(d,min=1,lines=['The normal temperature is 37 °C.','Her temperature is 39.2 °C.','Her temperature is [[higher]] than normal.','She has a fever.'])
    elif lb=='Teach · The dial (slightly, much, dangerously)':
        d=dict(d,min=4,items=DIAL_MIX,label='Teach · The dial',title='How much higher? How much lower?'); d.pop('hint',None)
    elif lb=='Teach · Might, can\'t, because':
        d=dict(d,min=1,lines=[dict(t='Clue: mosquito bites.',c='amber'),dict(t='<span style="color:#0f9a8c">It</span> <span style="color:#2f9e4a">[[might]] be</span> <span style="color:#e8821a">dengue.</span>',c='teal'),dict(t='Clue: her belly does not hurt.',c='amber'),dict(t='<span style="color:#0f9a8c">It</span> <span style="color:#2f9e4a">[[can\'t]] be</span> <span style="color:#e8821a">appendicitis.</span>',c='teal')])
    elif lb=='Teach · Symptoms': d=dict(d,min=1)
    elif lb=='Teach · Ask the patient': d=dict(d,min=1)
    elif lb=='Exercise · Might · can\'t · because': d=dict(d,lvl=2)
    elif lb=='Exercise · Ask the patient (1)': d=dict(d,lvl=2,min=3)
    elif lb=='Case board · Find the illness': d=dict(d,min=11)
    elif lb=='Tell the doctor (handover)':
        d=dict(m='frames3',phase='ACTIVATE',label='Tell the doctor (spoken)',min=3,title='Tell the doctor',groups=[
          {'t':'S · Situation','c':'teal','l':['A young woman. Day 3 of fever.'],'fs':40},
          {'t':'B · Background','c':'sky','l':['She was bitten by mosquitoes a week ago.','She has a rash.'],'fs':40},
          {'t':'A · Assessment','c':'rose','l':['It is probably dengue.','It can\'t be flu because she has no cough.'],'fs':40}],note='Tell your partner. Then swap.')
    elif lb=='Your sentences': d=dict(d,label='Your toolkit',title='Your hunt toolkit',groups=[
        {'t':'❓ Ask','c':'teal','l':['Have you got a clue about …?','What does your clue say about …?','Does the patient have …?'],'fs':44},
        {'t':'📢 Report','c':'sky','l':['Her temperature is much higher than normal.','She has a rash on her arms.','Her platelets are much lower than normal.'],'fs':40},
        {'t':'⚖️ Argue','c':'rose','l':['It might be dengue because …',"It can't be flu because …",'It is unlikely to be measles because …'],'fs':40}],note='Ask with a question. Answer in a full sentence.')
    elif lb=='Boss question (just for fun)':
        _new.append(dict(m='planb',phase='ACTIVATE',label='Plan B (teacher)',optional=True,min=1,title='Plan B · if you have time left',tiles=[dict(e='🩺',t='Tell the doctor',min='3–6 min',use='Written or spoken Situation, Background, Assessment.'),dict(e='🧩',t='Boss question',min='3 min',use='Fast finishers.'),dict(e='🗣️',t='Ask the patient (2)',min='3 min',use='More question practice.'),dict(e='🎧',t='Listen and fix',min='4 min',use='Hear it once, tap the wrong word.'),dict(e='🔤',t='Name the illness',min='4 min',use='Spelling warm-up for mixed levels.'),dict(e='🗂️',t='Paper clues',min='10 min',use='Tech fails or the ball stalls: each group reads its 3 clue cards aloud in turn.')]))
    elif lb=='Taboo rules': d=dict(d,min=7,label='Taboo for nurses')
    _new.append(d)
L3=_new

L4=[
 dict(m='cover',phase='ENGAGE',label='Cover',title='Lesson <span class="grad">4</span>',phases=['Engage','Study','Activate'],active=0,cards=[dict(pic='📅',x=1010,y=150,w=330,h=430,r=-7),dict(pic='☕',x=1380,y=330,w=330,h=430,r=6)]),
 dict(m='vol_ladder',phase='ENGAGE',label='Eyes closed. How bad?',min=3,title='Eyes closed. How bad?',rungs=['a little','quite','very','really','the worst!'],side='Eyes closed, all together. The louder you are, the worse it is. Whisper = a little. Shout = the worst.'),
 dict(m='predict',phase='ENGAGE',label='The impossible day',min=3,title='The impossible day',cap=False,items=[dict(frames=[dict(e='📚',c='Books. Exams.'),dict(e='☕',c='Cup after cup of coffee.'),dict(e='🌙',c='Night. Still awake.'),dict(e='😴',c='Asleep at the desk.')],q='❓ Why is she so tired?')]),
 dict(m='dials3',phase='STUDY',label='The dials',min=3,title='Three dials (and one checker)',dials=K.DIALS,note='Use at least one dial in every sentence.'),
 dict(m='timetable',phase='STUDY',label='Her week',min=2,title='Her week',days=['Mon','Tue','Wed','Thu','Fri'],rows=[('☕',['☕☕','☕☕☕','☕☕','☕☕☕','☕☕☕☕']),('😴',['3h','4h','3h','2h','3h'])],note='Look. What do you notice? Tell your neighbour.'),
 dict(m='teach',phase='STUDY',label='Teach · How bad?',min=2,role='How bad?',pic='🤕',lines=['0 = no pain.','3 out of 10: mild. It hurts a little.','5 out of 10: moderate.','9 out of 10: severe. It hurts a lot.']),
 exch(K.L4_EX[0],min=3),
 dict(m='teach',phase='STUDY',label='Teach · How long?',min=2,role='How long?',pic='🗓️',lines=['It started on Monday.','She has had a headache since Monday.','Two weeks.','She has felt tired for two weeks.']),
 exch(K.L4_EX[2],min=3),
 dict(m='teach',phase='STUDY',label='Teach · Compared with normal',min=2,role='Compared with normal',pic='🛏️',lines=['She sleeps 3 hours. Normal: 7.','She sleeps less than normal.','Her pulse is 110. Normal: 60–100.','Her pulse is faster than normal.']),
 exch(K.L4_EX[3],min=3),
 exch(K.L4_EX[1],optional=True,min=3),
 CMP,
 dict(m='build',phase='STUDY',label='Exercise · Say it with a dial (1)',title='Say it with a dial',min=3,lvl=1,levels=[
   dict(pics=['☕'],parts=[Q('c1','She'),Q('c2','drinks'),Q('c3','eight cups'),Q('c4','every day.')],extra=[]),
   dict(pics=['☕'],parts=[Q('c1','She'),Q('c2','drinks'),Q('c3','eight cups'),Q('c4','every day.')],extra=[('c2','drank'),('c4','always')]),
   dict(pics=['☕'],parts=[Q('c1','She'),Q('c2','has drunk'),Q('c3','eight cups a day'),Q('c4','since the exams started.')],extra=[('c2','drinks'),('c4','for the exams.')],fs=44)]),
 dict(m='build',phase='STUDY',label='Exercise · Say it with a dial (2)',title='Say it with a dial',min=2,optional=True,lvl=1,levels=[
   dict(pics=['💓'],parts=[Q('c1','Her pulse'),Q('c2','is'),Q('c3','faster than normal.')],extra=[]),
   dict(pics=['💓'],parts=[Q('c1','Her pulse'),Q('c2','is'),Q('c3','faster than normal.')],extra=[('c2','are'),('c3','more fast than normal.')]),
   dict(pics=['💓'],parts=[Q('c1','Her pulse'),Q('c2','has been'),Q('c3','faster than normal'),Q('c4','all day.')],extra=[('c2','is'),('c4','since all day.')],fs=44)]),
 dict(m='spell',phase='STUDY',label='Extra · Name the symptom',optional=True,min=3,title='Name the symptom',lvl=1,items=[
   dict(w='insomnia',pic='🌙',clue='You cannot sleep at night.',cat='a sleep problem'),dict(w='headache',pic='🤕',clue='Pain in the head.',cat='a symptom'),
   dict(w='caffeine',pic='☕',clue='The drug in coffee that keeps you awake.',cat='a drug'),dict(w='pulse',pic='💓',clue='The number of heartbeats in one minute.',cat='a measurement')],
   levels=[dict(mode='tiles',showpic=True,decoys=0),dict(mode='tiles',showpic=False,decoys=4),dict(mode='type',showpic=False)]),
 dict(m='label_reader',phase='STUDY',label='Extra · Read the label (how often, how much)',optional=True,min=3,lab=G3.LAB,qs=G3.QS,lvl=1,levels=[dict(qtext=True),dict(qtext=True),dict(qtext=False)]),
 dict(m='frames3',phase='ACTIVATE',label='Your sentences',min=2,title='Your sentences (they stay on the board)',groups=[
   {'t':'Easy','c':'teal','l':['She drinks coffee every day.','She is very tired.','Her pulse is high.'],'fs':46},
   {'t':'Better','c':'sky','l':['She has slept badly for two weeks.','Her pulse is faster than normal.'],'fs':44},
   {'t':'Stretch','c':'rose','l':['She has drunk eight cups a day since the exams started, which is twice as much as normal.','Friday was the worst night of the week.'],'fs':36}],note='Any sentence that carries the meaning is good.'),
 dict(m='frames3',phase='ACTIVATE',label='Everybody lies',min=2,title='Everybody lies',grad='violet',groups=[
   {'t':'The patient says…','c':'rose','l':['"I only drink two cups."','"I sleep fine."'],'fs':48},
   {'t':'The numbers say…','c':'sky','l':['The café card: 8 cups.','The watch: 3 hours of sleep.'],'fs':48},
   {'t':'You decide','c':'teal','l':['"She says ___, but ___."','Which clue do you believe?'],'fs':48}]),
 dict(m='comic',phase='ACTIVATE',label='How the hunt works',min=2,title='How the hunt works',panels=HUNT_COMIC),
 board('Find the reason',K.L4_SUSPECTS,K.L4_CLUES,K.L4_TWIST,K.L4_TEST,K.L4_ANSWER,'<b>It is too much coffee.</b><br>She says she drinks two cups, but the café card says eight.<br>She sleeps only 3 hours, and her pulse is faster than normal.<br>She has no fever and no cough, so it can\'t be flu.<br>She has no stomach problems, so it can\'t be food poisoning.<br>On Sunday she drank no coffee, and she felt much better.',
   dict(title='Wait… is it just stress?',lines=['Stand at the reason you believe.','Say why with a dial.','Better reason? Move.']),rule='At least one dial in every sentence.'),
 dict(m='boss',phase='ACTIVATE',label='Boss question (just for fun)',optional=True,min=3,**K.L4_BOSS,sec=90),
 dict(m='frames3',phase='ACTIVATE',label='"Doctor, I\'m too busy."',min=8,title='"Doctor, I\'m too busy."',h=470,groups=[
   {'t':'Patient','c':'rose','l':['"I\'m too busy to sleep."','"I need coffee. I have three exams."'],'fs':38},
   {'t':'You (the nurse)','c':'teal','l':['"You should sleep at least seven hours."','"How many cups do you drink every day?"','"For two weeks? That is more than normal."'],'fs':32},
   {'t':'Say one thing','c':'violet','l':['Choose a dial.','Make it kind.'],'fs':42}],write=True,note='Write down one kind sentence. Then say it to your partner.'),
 dict(m='taboo',phase='ACTIVATE',label='Extra · Taboo (fun)',optional=True,min=4,items=[dict(w='shaky',e='🤲',no=['shake','hands','cold','fall']),dict(w='coffee',e='☕',no=['cup','drink','morning','caffeine']),dict(w='dizzy',e='😵\u200d💫',no=['spin','head','fall','room']),dict(w='pulse',e='💓',no=['heart','beat','wrist','minute']),dict(w='nauseous',e='🤢',no=['sick','vomit','stomach','feel']),dict(w='headache',e='🤕',no=['head','pain','hurt','tablet']),dict(w='breathless',e='😮\u200d💨',no=['breath','air','run','stairs']),dict(w='exam',e='📝',no=['test','study','paper','university'])],lvl=1,levels=[dict(limit=2),dict(limit=3,secs=60),dict(limit=4,secs=45)]),
 dict(m='recap',phase='RECAP',label='Recap',min=2,rows=[([('c1','She'),('c2','has felt'),('c3','tired'),('c4','for two weeks.')],'for'),([('c1','Her pulse'),('c2','is'),('c3','faster than normal.')],'than'),([('c1','She'),('c2','drinks'),('c3','the most coffee')],'the most'),([('c1','You'),('c2','should'),('c3','sleep more.')],'advice'),([('c1','He'),('c2','is'),('c3','breathless, sweaty and pale.')],'symptoms')],emoji='sleeping_face'),
 dict(m='closing',phase='EXIT',label='Thank you',min=1,stack=True,line1='Thank',line2='you!',sub='See you next time.',emoji='handshake'),
]

# ---- L4 Activate: Fix the ward (night nurse handover with 12 mistakes, audio voice notes) ----
_FIXD=[
 ('red','🌡️','Temperature','Temperature: 73 °C','Temp 73 °C','Nurse','Her temperature is thirty-six point eight. Normal. Seventy-three? That was the coffee!',['Her temperature is normal.','Her temperature is very high.','Her temperature is very low.'],{'flu':'against'}),
 ('blue','☕','Coffee','Drinks two cups a day','2 cups a day','Barista','Eight cups a day. Every day. I know her order!',['She drinks eight cups every day.','She drinks two cups every day.','She never drinks coffee.'],{'coffee':'for'}),
 ('green','🛏️','Sleep','Sleeps nine hours','Sleeps 9 hours','Smartwatch','Sleep last night: three hours. She woke up exhausted.',['She sleeps three hours. That is less than recommended.','She sleeps nine hours. That is more than she needs.','She sleeps seven hours. That is enough.'],{'coffee':'for','stress':'for'}),
 ('yellow','💓','Pulse','Pulse 56: lower than normal','Pulse 56','Nurse','Her pulse is one hundred and ten. Her heart is racing.',['Her pulse is 110. It is higher than normal.','Her pulse is 56. It is lower than normal.','Her pulse is 80. It is normal.'],{'coffee':'for','stress':'for'}),
 ('red','🤕','Headache','Headache: 9 out of 10','Headache 9/10','Patient','My headache is only a little. Three out of ten.',['Her headache is 3 out of 10. It is mild.','Her headache is 9 out of 10. It is severe.','Her headache is 5 out of 10. It is moderate.'],{}),
 ('blue','🗓️','Start','It started yesterday','Started yesterday','Friend','She has felt like this since the exams started. About two weeks.',['It started two weeks ago.','It started yesterday.','It started two years ago.'],{'stress':'for','coffee':'for'}),
 ('green','😷','Cough','Coughs every night','Coughs every night','Patient','I never cough. Not once.',['She never coughs.','She coughs every night.','She coughs twice a week.'],{'flu':'against'}),
 ('yellow','🤢','Stomach','Vomiting and diarrhoea','Vomiting','Friend','We ate the same lunch. Nobody else is sick.',['Nobody else is sick.','Everybody is sick.','She has vomiting and diarrhoea.'],{'food':'against'}),
 ('red','💊','Plan','Plan: two strong coffees','Plan: 2 strong coffees','Doctor','No more coffee suddenly. She should cut down slowly.',['She should cut down coffee slowly.','She should drink two strong coffees.','She should stop coffee today.'],{'coffee':'for'}),
 ('blue','💔','Cause','Cause: broken heart','Broken heart','Patient','Nobody broke my heart! My phone just buzzes with exam messages.',["It can't be a broken heart. It is her phone.",'It is a broken heart.','It is flu.'],{'heart':'against'}),
 ('green','🌞','Sunday','Worse on Sunday','Worse on Sunday','Nurse','On Sunday she drank no coffee. She slept nine hours and felt much better.',['She felt much better on Sunday.','She felt worse on Sunday.','She felt the same on Sunday.'],{'coffee':'for'}),
 ('yellow','📚','Exams','One exam a week','1 exam a week','Teacher','Three exams in four days! She is exhausted.',['She has three exams in four days.','She has one exam a week.','She has no exams.'],{'stress':'for'})]
FIX=[dict(n=i+1,owner=o,pic=pc,topic=tp,wrong=w,short=sh,who=who,voice=v,fix=op[0],opts=op,fx=fx) for i,(o,pc,tp,w,sh,who,v,op,fx) in enumerate(_FIXD)]
FIX_CLUES=[dict(id=f'M{f["n"]}',team=f['owner'],r=1,topic=f['topic'],pic=f['pic'],short=f['short'],text=f['fix'],fx=f['fx']) for f in FIX]
_FP=stick(110,395,1.2,'down')+'<text x="190" y="340" font-size="64">☕</text><text x="215" y="260" font-size="50">🌡️</text><text x="190" y="170" font-size="40" font-family="Outfit,sans-serif" font-weight="800" fill="#e0304a">73 °C!</text><text x="40" y="110" font-size="60">💤</text>'
_FP2=stick(120,395,1.2,'hold')+'<text x="190" y="360" font-size="80">📝</text><text x="195" y="300" font-size="60" fill="#e0304a">❌</text>'
_FP3=stick(90,395,1.15,'up')+stick(310,395,1.15,'point')+bubble_svg(20,16,330,100,'Can I hear your\nvoice note?',fs=26,tx=120)
_FP4=stick(130,395,1.2,'hold')+'<text x="195" y="330" font-size="86">🎧</text><text x="255" y="190" font-size="110" fill="#2bd9b6" font-family="Outfit,sans-serif" font-weight="800">✔</text>'
FIX_COMIC=[dict(svg=_FP,cap='The night nurse made mistakes.'),dict(svg=_FP2,cap='Find the mistakes on the board.'),dict(svg=_FP3,cap='Ask the class.'),dict(svg=_FP4,cap='Listen. Write the fix. Say it.')]

# ================= L4 post-processing: 16 Nov review round =================
def _o(pic,q,*opts,**kw): return dict(pic=pic,q=q,opts=list(opts),ans=opts[0],**kw)
def _lvs(a,b,c): return [{'items':a},{'items':b},{'items':c}]
_C=lambda sv:'<svg>'
_Pn1=stick(110,395,1.2,'hold')+'<text x="190" y="370" font-size="84">📚</text><text x="215" y="130" font-size="76">📅</text><text x="200" y="200" font-size="38" font-family="Outfit,sans-serif" font-weight="800" fill="#e0304a">3 exams!</text>'
_Pn2=stick(110,395,1.2,'hold')+'<text x="185" y="340" font-size="60">☕☕</text><text x="175" y="270" font-size="56">☕☕☕</text><text x="210" y="130" font-size="90">📱</text>'
_Pn3='<text x="235" y="130" font-size="120">🌙</text><text x="40" y="110" font-size="64">⏰</text><text x="30" y="160" font-size="34" font-family="Outfit,sans-serif" font-weight="800">2:00 am</text><text x="260" y="380" font-size="66">🐱</text>'+stick(120,395,1.2,'down')+'<text x="68" y="236" font-size="38">👀</text>'
_Pn4=stick(130,395,1.2,'down')+'<text x="195" y="330" font-size="80">😴</text><text x="250" y="170" font-size="190" font-family="Outfit,sans-serif" font-weight="800" fill="#9a5cff">?</text>'
COMIC4=[dict(svg=_Pn1,cap='Books. Exams.'),dict(svg=_Pn2,cap='Coffee. Phone.'),dict(svg=_Pn3,cap='Night. Awake.'),dict(svg=_Pn4,cap='Asleep at the desk.')]
BAD=[dict(word='no pain',e='🙂',gloss='0',sen='He has [[no]] pain.'),dict(word='a little',e='😕',gloss='1–3 · mild',sen='It hurts [[a little]].'),dict(word='quite',e='😣',gloss='4–6 · moderate',sen='It is [[quite]] painful.'),dict(word='very',e='😖',gloss='7–8',sen='It hurts [[very]] much.'),dict(word='the worst',e='😭',gloss='9–10 · severe',sen='It is [[the worst]] pain.')]
HOWLONG=dict(m='choice',phase='STUDY',title='How long?',label='Exercise · How long?',lvl=2,min=2,levels=_lvs(
 [_o('🗓️','Today is Friday. The pain began on Wednesday.','It started two days ago.','It started two days.'),_o('🗓️','The headache began on Monday.','It started on Monday.','It started in Monday.'),_o('🕑','The problem began 14 days ago.','It started two weeks ago.','It started two weeks.')],
 [_o('🗓️','Today is Friday. She began to feel tired on Monday.','She is tired. It started on Monday.','She is tired. It started on Friday.','She is tired. It started Monday ago.'),_o('🤕','The headache began three days ago.','She has a headache. It started three days ago.','She has a headache. It started on three days.','She has a headache. It started since three days.'),_o('🌙','She cannot sleep. It began two weeks ago.','She cannot sleep. It started two weeks ago.','She cannot sleep. It started for two weeks.','She cannot sleep. It started two weeks.')],
 K.L4_EX[2]['levels']['gold']))
NORMAL=dict(m='choice',phase='STUDY',title='Compared with normal?',label='Exercise · Compared with normal?',lvl=2,min=3,levels=_lvs(
 [_o('🛏️','She sleeps 3 hours. Normal is 7 hours.','She sleeps less than normal.','She sleeps more than normal.'),_o('💓','Her pulse is 110. Normal is 60 to 100.','Her pulse is higher than normal.','Her pulse is lower than normal.'),_o('🌡️','Her temperature is 36.8 °C. Normal is about 37 °C.','Her temperature is normal.','Her temperature is higher than normal.')],
 [_o('☕','She drinks 8 cups. Normal is 4 or 5.','She drinks more coffee than normal.','She drinks less coffee than normal.','Her coffee is normal.'),_o('💓','Her pulse is 78. Normal is 60 to 100.','Her pulse is normal.','Her pulse is higher than normal.','Her pulse is lower than normal.'),_o('🛏️','She sleeps 5 hours. Normal is 7 to 9 hours.','She sleeps less than normal.','She sleeps more than normal.','Her sleep is normal.')],
 [_o('💓','Pulse: 110. Normal: 60 to 100. The nurse is not worried.','Her pulse is a little higher than normal, but it is not dangerous.','Her pulse is much higher than normal. It is dangerous.','Her pulse is lower than normal.'),_o('🛏️','She sleeps 3 hours. Normal is 7 to 9 hours.','She sleeps much less than normal.','She sleeps a little less than normal.','She sleeps more than normal.'),_o('☕','She drinks 8 cups. Adults usually drink 4 or 5.','She drinks almost twice as much coffee as normal.','She drinks half as much coffee as normal.','She drinks the same coffee as normal.')]))
COMPARE=dict(m='choice',phase='STUDY',title='Compare',label='Exercise · Compare (than · the most)',optional=True,lvl=2,min=3,levels=_lvs(
 [_o('☕','Monday: 2 cups. Friday: 4 cups.','Friday has more coffee than Monday.','Monday has more coffee than Friday.'),_o('😴','Monday: 3 hours of sleep. Thursday: 2 hours.','Thursday has less sleep than Monday.','Thursday has more sleep than Monday.'),_o('💓','Her pulse is 110. Normal is 60 to 100.','Her pulse is higher than normal.','Her pulse is lower than normal.')],
 [_o('☕','Mon 2 · Tue 3 · Wed 2 · Thu 3 · Fri 4 cups.','Friday has the most coffee.','Monday has the most coffee.','Wednesday has the most coffee.'),_o('😴','Mon 3 · Tue 4 · Wed 3 · Thu 2 · Fri 3 hours of sleep.','Thursday has the least sleep.','Tuesday has the least sleep.','Thursday has the most sleep.'),_o('💓','Pulse: Monday 90 · Tuesday 100 · Wednesday 110.','Wednesday has the highest pulse.','Monday has the highest pulse.','Wednesday has the lowest pulse.')],
 [_o('☕','Monday: 2 cups. Friday: 4 cups.','She drinks twice as much coffee on Friday as on Monday.','She drinks half as much coffee on Friday as on Monday.','She drinks the same coffee on Friday as on Monday.'),_o('😴','Mon 3 · Tue 4 · Wed 3 · Thu 2 · Fri 3 hours.','Thursday is the worst night, and Tuesday is the best.','Thursday is the best night, and Tuesday is the worst.','Every night is the same.'),_o('💓','Pulse: 108, 112, 110. Normal: 60 to 100.','Her pulse is higher than normal all day.','Her pulse is lower than normal all day.','Her pulse is normal all day.')]))
PLANB4=dict(m='planb',phase='ACTIVATE',label='Plan B (teacher)',optional=True,min=1,title='Plan B · if you have time left',tiles=[
 dict(e='🎯',t='Taboo for nurses',min='7 min',use='Groups finish early. QR phone page: describer only, words only.'),dict(e='🩺',t='"Doctor, I\'m too busy."',min='6–8 min',use='Strong groups. Say one kind sentence to the patient.'),dict(e='🤥',t='Everybody lies',min='3 min',use='The argue phase is quiet. Patient says vs numbers say.'),
 dict(e='🧩',t='Boss question',min='3 min',use='Fast finishers: why "cut down slowly"?'),dict(e='🔤',t='Name the symptom',min='4 min',use='Spelling warm-up for mixed levels.'),dict(e='🗂️',t='Paper fallback',min='10 min',use='Tech fails: read the 12 voice-note sentences aloud from paper; groups still choose the fix.')])
# ================= L4 Study rebuilt on the L3 skeleton (16 Nov, Nick) =================
_q4=_q
SYM4=[[_q4('🥱','What does the nurse write?','She is exhausted.','She is dizzy.','She is shaky.',say="I can't keep my eyes open!"),
  _q4('😵‍💫','What does the nurse write?','He feels dizzy.','He feels shaky.','He feels exhausted.',say='The room is spinning!'),
  _q4('🤲','What does the nurse write?','Her hands are shaky.','Her hands are dizzy.','Her hands are exhausted.',say="My hands won't stop shaking!"),
  _q4('💓','What does the nurse write?','Her heart is racing.','Her heart is sleeping.','Her heart is shaky.',say='Boom-boom-boom! My heart is racing!')],
 [_q4('🥱','What does the nurse write?','She is exhausted because she sleeps three hours a night.','She is exhausted because she sleeps nine hours a night.','She is exhausted because she drinks no coffee.',say='Three hours of sleep. Every night. I am so tired!'),
  _q4('☕','What does the nurse write?','His hands are shaky after every coffee.','His hands are shaky before every coffee.','His hands are dizzy after every coffee.',say='After each coffee, my hands shake!'),
  _q4('😵‍💫','What does the nurse write?','She feels dizzy when she stands up.','She feels dizzy when she sits down.','She is dizzy when she stands down.',say='When I stand up, the room spins.'),
  _q4('💓','What does the nurse write?','His heart is racing, but he is not in danger.','His heart is racing, and he is in danger.','His heart race, but he is not in danger.',say='Racing heart… but I feel okay, nurse.')],
 [_q4('🥱','What does the nurse write?','She is exhausted, but she cannot fall asleep.','She is exhausted, but she can fall asleep.','She exhausted, but she cannot fall asleep.',say='I am so tired… but in bed, I just stare at the ceiling.'),
  _q4('😵‍💫','What does the nurse write?','He is dizzy and his hands are shaky.','He is dizzy and his hands shaky.','He dizzy and his hands are shaky.',say='I feel dizzy and my hands will not stop shaking.'),
  _q4('☕','What does the nurse write?','She says she drinks two cups, but the café card says eight.','She says she drinks eight cups, but the café card says two.','She say she drinks two cups, but the café card says eight.',say='Two cups. Maybe three. Okay… eight.'),
  _q4('💓','What does the nurse write?','Her heart is racing much faster than normal.','Her heart is racing much slowly than normal.','Her heart is racing much fast than normal.',say='My heart will not slow down!')]]
BAD=[dict(word='no pain',e='🙂',gloss='0',sen='He has [[no]] pain.',say='I feel nothing, nurse.'),dict(word='mild',e='😕',gloss='1–3',sen='The pain is [[mild]].',say='Just a little pain. I can ignore it.'),dict(word='moderate',e='😣',gloss='4–6',sen='The pain is [[moderate]].',say='It hurts quite a lot. I need a pill.'),dict(word='severe',e='😖',gloss='7–8',sen='The pain is [[severe]].',say="It hurts very much. I can't work!"),dict(word='unbearable',e='😭',gloss='9–10',sen='The pain is [[unbearable]].',say='It is the worst pain of my life!')]
LONG=[dict(word='today',e='☀️',gloss='0 days',sen='It started [[today]].',say='I woke up like this this morning.'),dict(word='2 days ago',e='📅',gloss='2 days',sen='It started [[two days ago]].',say='It started two days ago, on Wednesday.'),dict(word='last week',e='🗓️',gloss='7 days',sen='It started [[last week]].',say='It started last week, after the party.'),dict(word='2 weeks ago',e='🕑',gloss='14 days',sen='It started [[two weeks ago]].',say='I have been like this for two weeks.'),dict(word='the exams',e='📚',gloss='since…',sen='It started [[when the exams started]].',say='It started when the exams started.')]
HB=_lvs=None
def _lv3(a,b,c): return [{'items':a},{'items':b},{'items':c}]
HB4=[[_q4('😕','What does the nurse write?','The pain is mild.','The pain is severe.','The pain is moderate.',say='Just a little pain. I can ignore it.'),_q4('😣','What does the nurse write?','The pain is moderate.','The pain is mild.','The pain is unbearable.',say='It hurts quite a lot. I need a pill.'),_q4('😭','What does the nurse write?','The pain is unbearable.','The pain is mild.','The pain is moderate.',say='It is the worst pain of my life!')],
 [_q4('😖','What does the nurse write?','His pain is severe. It is 8 out of 10.','His pain is mild. It is 8 out of 10.','His pain is severe. It is 2 out of 10.',say="Eight out of ten. I can't sleep!"),_q4('😕','What does the nurse write?','Her headache is mild. It is 2 out of 10.','Her headache is severe. It is 2 out of 10.','Her headache is mild. It is 9 out of 10.',say='Two out of ten. It is nothing.'),_q4('😣','What does the nurse write?','His pain is moderate. It is 5 out of 10.','His pain is unbearable. It is 5 out of 10.','His pain is mild. It is 5 out of 10.',say='Five out of ten. It hurts, but I can walk.')],
 [_q4('😭','What does the nurse write?','Her headache was moderate yesterday, but today it is unbearable.','Her headache was unbearable yesterday, but today it is moderate.','Her headache was moderate yesterday, but today it moderate.',say='Yesterday it was okay. Today it is the worst pain of my life!'),_q4('😖','What does the nurse write?','His pain is severe, so he cannot work.','His pain is mild, so he cannot work.','His pain is severe, so he can work.',say="It hurts very much. I can't work!"),_q4('🙂','What does the nurse write?','She has no pain now. It was mild last week.','She has no pain now. It was unbearable last week.','She have no pain now. It was mild last week.',say='Nothing now. Last week, only a little.')]]
LONGEX=dict(m='choice',phase='STUDY',title='How long?',label='Exercise · How long?',lvl=2,min=2,levels=_lv3(
 [_q4('☀️','What does the nurse write?','It started today.','It started two weeks ago.','It started last week.',say='I woke up like this this morning.'),_q4('🕑','What does the nurse write?','It started two weeks ago.','It started two days ago.','It started today.',say='I have been like this for two weeks.'),_q4('📚','What does the nurse write?','It started when the exams started.','It started when the exams finished.','It started yesterday.',say='It started when the exams started.')],
 [_q4('📅','What does the nurse write?','She has a headache. It started two days ago.','She has a headache. It started on two days.','She has a headache. It started since two days.',say='My head hurts. It started two days ago.'),_q4('🗓️','What does the nurse write?','He is tired. It started on Monday.','He is tired. It started Monday ago.','He is tired. It started in Monday.',say='I am so tired. It started on Monday.'),_q4('🕑','What does the nurse write?','She cannot sleep. It started two weeks ago.','She cannot sleep. It started for two weeks.','She cannot sleep. It started two weeks.',say='I cannot sleep. Two weeks ago it began.')],
 K.L4_EX[2]['levels']['gold']))
DIAL4=[_d('💓','Pulse: 110 beats per minute','60 to 100 beats per minute','Her pulse is',4),_d('☕','Coffee: 8 cups a day','up to 4 cups a day','Her coffee is',5),_d('🛏️','Sleep: 3 hours a night','7 to 9 hours a night','Her sleep is',1),_d('🌡️','Temperature: 36.8 °C','about 37 °C','Her temperature is',3),_d('💓','Pulse: 45 beats per minute','60 to 100 beats per minute','Her pulse is',1),_d('☕','Coffee: 12 cups a day','up to 4 cups a day','Her coffee is',6)]
HL4=dict(m='choice',phase='STUDY',title='Higher or lower?',label='Exercise · Higher or lower?',lvl=3,min=3,levels=_lv3(
 [_o('🛏️','Normal sleep: 7 to 9 hours. Her sleep: 3 hours. Her sleep is ___ than normal.','lower','higher'),_o('☕','Normal coffee: up to 4 cups. Her coffee: 8 cups. Her coffee is ___ than normal.','higher','lower'),_o('💓','Normal pulse: 60 to 100. Her pulse: 45. Her pulse is ___ than normal.','lower','higher')],
 [_o('💓','Normal pulse: 60 to 100 beats per minute. Her pulse: 110.','Her pulse is slightly higher than normal.','Her pulse is much higher than normal.','Her pulse is lower than normal.'),_o('🛏️','Normal sleep: 7 to 9 hours. Her sleep: 3 hours.','Her sleep is much lower than normal.','Her sleep is slightly lower than normal.','Her sleep is higher than normal.'),_o('🌡️','Normal temperature: about 37 °C. Her temperature: 36.8 °C.','Her temperature is normal.','Her temperature is higher than normal.','Her temperature is lower than normal.')],
 [_o('☕','Coffee: 12 cups a day. Normal: up to 4 cups.','Her coffee is dangerously higher than normal.','Her coffee is slightly higher than normal.','Her coffee is much lower than normal.'),_o('🛏️','A patient says "I sleep fine." The watch says 3 hours. Normal: 7 to 9.','Her sleep is much lower than normal. She does not sleep fine!','Her sleep is normal.','Her sleep is slightly higher than normal.'),_o('💓','A sleeping marathon runner: 48 beats per minute. Normal: 60 to 100.','Her pulse is lower than the normal range, but she is very fit.','Her pulse is much higher than normal.','Her pulse is normal.')]))
_MI=lambda t:'<span style="color:#0f9a8c">It</span> <span style="color:#2f9e4a">'+t+'</span>'
MIGHT_T=dict(m='teach',phase='STUDY',label="Teach · Might, can't, because",min=1,role='Clue → sentence',pic='☕',lines=[dict(t='Clue: her hands shake after every coffee.',c='amber'),dict(t=_MI('[[might]] be')+' <span style="color:#e8821a">the coffee.</span>',c='teal'),dict(t='Clue: she has no cough.',c='amber'),dict(t=_MI("[[can't]] be")+' <span style="color:#e8821a">flu.</span>',c='teal')])
MIGHT_E=dict(m='choice',phase='STUDY',title='Might or can\'t?',label="Exercise · Might · can't · because",lvl=2,min=2,levels=_lv3(
 [_o('☕','Clue: her hands shake after every coffee.','It might be the coffee.',"It can't be the coffee."),_o('😷','Clue: she has no cough.',"It can't be flu.",'It might be flu.'),_o('🍱','Clue: her friends ate the same lunch. They are fine.',"It can't be food poisoning.",'It might be food poisoning.')],
 [_o('📚','Clue: she is very worried about her exams.','It might be exam stress because she is worried about her exams.',"It can't be exam stress because she is worried about her exams.",'It might be flu because she is worried.'),_o('🍽️','Clue: no vomiting and no diarrhoea.',"It can't be food poisoning because she has no vomiting.",'It might be food poisoning because she has no vomiting.',"It can't be food poisoning because she is worried."),_o('💓','Clue: her pulse goes up every time her phone buzzes.','It might be her phone, not a broken heart.','It might be a broken heart, not her phone.',"It can't be her phone.")],
 [_o('☕','Clue: on Sunday she drank no coffee and felt much better.','It is probably the coffee, because she felt better without it.','It is probably flu, because she felt better without coffee.',"It can't be the coffee, because she felt better."),_o('🌡️','Clue: her temperature is normal and she does not cough.',"It is unlikely to be flu, because she has no fever and no cough.",'It is likely to be flu, because she has no fever.',"It can't be tired, because she has no fever."),_o('📅','Clue: it started two weeks ago, when the exams started.','It might be exam stress, because it started with the exams.','It might be flu, because it started two weeks ago.',"It can't be exam stress, because it started two weeks ago.")]))
ASK_T=dict(m='teach',phase='STUDY',label='Teach · Ask the patient',min=1,role='Good questions',pic='🩺',lines=['How often do you drink coffee?','How long have you felt tired?','Do you sleep well at night?','How bad is the headache?'])
def _askb(pic,parts,lab,opt=False,mn=2): return dict(m='build',phase='STUDY',label=lab,title='Ask the patient',min=mn,optional=opt,lvl=2,levels=[dict(pics=[pic],parts=parts,extra=e) for e in ([],[('c2','did'),('c2','are')],[('c2','did'),('c2','are'),('c4','since'),('c4','for')])])
ASK_B1=_askb('☕',[Q('c4','How'),Q('c4','often'),Q('c2','do'),Q('c1','you'),Q('c2','drink'),Q('c3','coffee?')],'Exercise · Ask the patient (1)')
ASK_B2=_askb('😴',[Q('c4','How'),Q('c4','long'),Q('c2','have'),Q('c1','you'),Q('c2','felt'),Q('c3','tired?')],'Exercise · Ask the patient (2)',True)
TODAY4=dict(m='today',phase='STUDY',label='Today',min=1,emoji='stethoscope',title='Night-shift nurses',role='Today we are',rows=[[('c4','Say'),('c3','how bad')],[('c1','Say'),('c3','how long')],[('c2','might'),('c4',"can't"),('c3','because')]])

# ---- 17 Nov round: comprehension-first audio exercises (Nick's notes p7, p9, p11) ----
def _a(pic,say,ans,*w): return _q4(pic,'What does the nurse write?',ans,*w,say=say)
SYM4=[[_a('🥱',"I can't keep my eyes open!",'She is exhausted.','She is dizzy.','She is shaky.'),
  _a('😵‍💫','The room is spinning!','He feels dizzy.','He feels exhausted.','He feels shaky.'),
  _a('🤲',"My hands won't stop shaking!",'Her hands are shaky.','Her hands are cold.','Her hands are sore.'),
  _a('💓','Boom-boom-boom! My heart is racing!','Her heart is racing.','Her heart is slow.','Her heart is sore.')],
 [_a('🥱','Three hours of sleep. Every night. I am so tired!','She sleeps very little.','She sleeps a lot.','She sleeps well.'),
  _a('☕','After each coffee, my hands shake!','Her hands shake after she drinks coffee.','Her hands shake before she drinks coffee.','Her hands never shake.'),
  _a('😵‍💫','When I stand up, the room spins.','She feels dizzy when she stands up.','She feels dizzy when she sits down.','She feels dizzy when she sleeps.'),
  _a('💓','Racing heart… but I feel okay, nurse.','His heart is fast, but he feels okay.','His heart is slow, and he feels ill.','His heart is fast, and he feels very ill.')],
 [_a('🥱','I am so tired… but in bed, I just stare at the ceiling.','She is exhausted, but she cannot sleep.','She is exhausted, and she sleeps well.','She is not tired.'),
  _a('😵‍💫','I feel dizzy and my hands will not stop shaking.','He has two problems: dizzy and shaky hands.','He has one problem: dizzy.','He has no problems.'),
  _a('☕','Two cups. Maybe three. Okay… eight.','She drinks much more coffee than she first says.','She drinks only two cups.','She does not drink coffee.'),
  _a('💓','My heart will not slow down!','Her heart is racing and she cannot calm down.','Her heart is slow and calm.','Her heart has stopped.')]]
HB4=[[_a('😕','Just a little pain. I can ignore it.','The pain is mild.','The pain is severe.','The pain is moderate.'),_a('😣','It hurts quite a lot. I need a pill.','The pain is moderate.','The pain is mild.','The pain is unbearable.'),_a('😭','It is the worst pain of my life!','The pain is unbearable.','The pain is mild.','The pain is moderate.')],
 [_a('😖',"Eight out of ten. I can't sleep!",'His pain is severe.','His pain is mild.','He has no pain.'),_a('😕','Two out of ten. It is nothing.','Her pain is mild.','Her pain is severe.','Her pain is unbearable.'),_a('😣','Five out of ten. It hurts, but I can walk.','His pain is moderate.','His pain is mild.','His pain is unbearable.')],
 [_a('😭','Yesterday it was okay. Today it is the worst pain of my life!','Her pain got much worse.','Her pain got better.','Her pain is the same.'),_a('😖',"It hurts very much. I can't work!",'He is in severe pain and cannot work.','He has mild pain and can work.','He has no pain and cannot work.'),_a('🙂','Nothing now. Last week, only a little.','Her pain is gone.','Her pain is getting worse.','Her pain is unbearable.')]]
LONGEX=dict(m='choice',phase='STUDY',title='How long?',label='Exercise · How long?',aud=True,lvl=2,min=2,levels=_lv3(
 [_a('☀️','I woke up like this this morning.','It started today.','It started two weeks ago.','It started last week.'),_a('🕑','I have been like this for two weeks.','It started two weeks ago.','It started two days ago.','It started today.'),_a('📚','It started when the exams started.','It started when the exams started.','It started when the exams finished.','It started yesterday.')],
 [_a('📅','It began on Wednesday. Today is Friday.','It started two days ago.','It started two weeks ago.','It started two months ago.'),_a('🗓️','I have felt tired since Monday. Today is Thursday.','She has felt tired for three days.','She has felt tired for three weeks.','She has felt tired for one day.'),_a('🕑','Fourteen days. Every night, no sleep.','She has not slept well for two weeks.','She has not slept well for two days.','She has not slept well for four days.')],
 [_a('📚','Before the exams, I slept well. Now I do not sleep.','The problem started with the exams.','The problem started before the exams.','The problem finished with the exams.'),_a('🤕','Yesterday I felt fine. Today my head is exploding!','The headache is new.','The headache is old.','She has no headache.'),_a('🌅','Every morning for a month, I wake up with a headache.','The headache is a daily problem for a month.','The headache started yesterday.','The headache happens once a year.')]))
DIAL4=[_d('💓','Pulse: 110 beats per minute','60 to 100 beats per minute','Her pulse is',4),_d('☕','Coffee: 8 cups a day','up to 4 cups a day','Her coffee intake is',5),_d('🛏️','Sleep: 3 hours a night','7 to 9 hours a night','Her sleep time is',1),_d('🌡️','Temperature: 36.8 °C','about 37 °C','Her temperature is',3),_d('💓','Pulse: 45 beats per minute','60 to 100 beats per minute','His pulse is',1),_d('☕','Coffee: 12 cups a day','up to 4 cups a day','Her coffee intake is',6)]
MIGHT_T=dict(MIGHT_T,lines=[dict(t='Clue: her hands shake after every coffee. They also shake after every meal.',c='amber'),dict(t=_MI('[[might]] be')+' <span style="color:#e8821a">the coffee. It might be low blood sugar.</span>',c='teal'),dict(t='Clue: she has no cough. She has no fever.',c='amber'),dict(t=_MI("[[can't]] be")+' <span style="color:#e8821a">flu.</span>',c='teal')])
ASK_T=dict(ASK_T,pics=['☕','😴','🌙','🤕'])

# ---- 17 Nov round 2 (Nick): audio on click, natural sentences, caffeine facts, vocab+, picture exercises ----
_a2=_a
SYM4=[l[:] for l in SYM4]
SYM4[0].append(_a('🤢',"I feel sick. I think I'm going to vomit.",'She feels nauseous.','She feels dizzy.','She feels exhausted.'))
SYM4[1].append(_a('😮‍💨',"I climbed one floor… and I can't catch my breath.",'He is breathless.','He is dizzy.','He is hungry.'))
SYM4[2].append(_a('😓','I am sweating, and my face is white. Is the air-con on?','She is sweaty and pale.','She is sweaty and red.','She is cold and pale.'))
HB4[1]=[_a('😖','It hurts a lot. I cannot sleep.','His pain is severe.','His pain is mild.','He has no pain.'),_a('😕','It hurts a little. I can ignore it.','Her pain is mild.','Her pain is severe.','Her pain is unbearable.'),_a('😣','It hurts, but I can still walk.','His pain is moderate.','His pain is mild.','His pain is unbearable.')]
DIAL4=[_d('💓','Pulse: 110 beats per minute','60 to 100 beats per minute','Her pulse is',4),_d('🛏️','Sleep: 6 hours a night','7 to 9 hours a night','Her sleep time is',2),_d('☕','Coffee: 5 cups a day','up to 4 cups a day','Her coffee intake is',4),_d('🛏️','Sleep: 3 hours a night','7 to 9 hours a night','Her sleep time is',1),_d('☕','Coffee: 8 cups a day','up to 4 cups a day','Her coffee intake is',5),_d('☕','Coffee: 12 cups a day','up to 4 cups a day','Her coffee intake is',6)]
def _da(e,now,normal,st,z,say): return dict(_d(e,now,normal,st,z),say=say)
DIALA=[_da('💓','Pulse: 150 beats per minute','60 to 100 beats per minute','Her pulse is',5,'Her pulse is one hundred and fifty. Normal is sixty to one hundred.'),
 _da('🛏️','Sleep: 6 hours a night','7 to 9 hours a night','Her sleep time is',2,'She sleeps six hours a night. Normal is seven to nine hours.'),
 _da('☕','Coffee: 5 cups a day','up to 4 cups a day','Her coffee intake is',4,'She drinks five cups of coffee a day. A healthy limit is up to four cups.'),
 _da('🌡️','Temperature: 37 °C','about 37 °C','Her temperature is',3,'Her temperature is thirty-seven degrees. Normal is about thirty-seven.'),
 _da('💓','Pulse: 38 beats per minute','60 to 100 beats per minute','Her pulse is',0,'Her pulse is thirty-eight beats a minute. Normal is sixty to one hundred.'),
 _da('☕','Coffee: 12 cups a day','up to 4 cups a day','Her coffee intake is',6,'She drinks twelve cups of coffee a day. A healthy limit is up to four cups.')]
DIALX=dict(m='dial',phase='STUDY',label='Exercise · Higher or lower?',min=3,title='Listen: higher or lower?',aud=True,items=DIALA)
MIGHT_T=dict(MIGHT_T,lines=[dict(t='Clue: her hands shake after every coffee. They also shake when she skips lunch.',c='amber'),dict(t=_MI('[[might]] be')+' <span style="color:#e8821a">the coffee. It might be low blood sugar.</span>',c='teal'),dict(t='Clue: she has no cough. She has no fever.',c='amber'),dict(t=_MI("[[can't]] be")+' <span style="color:#e8821a">flu.</span>',c='teal')])
PAIRS=dict(m='pairs',phase='STUDY',label="Exercise · Might · can't",min=2,title="Clue → sentence",hint='Tap a clue. Then tap the sentence that fits.',pairs=[('She has no cough and no fever.',"It can't be flu."),('Her friends ate the same lunch. They are fine.',"It can't be food poisoning."),('Her hands shake after every coffee.','It might be the coffee.'),('She has been worried about her exams for two weeks.','It might be stress.'),('Her temperature is 36.8 °C.',"It can't be a fever.")])
def _days(v,em='☕'): return [(d_,(em+('' if k==1 else '×%d'%k)) if k else '–') for d_,k in zip(['Mon','Tue','Wed','Thu','Fri'],v)]
def _wk(v,u='☕'): return [(d_,('%s%s'%(u,'×%d'%k)) if k else '–') for d_,k in zip(['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],v)]
def _freq(v): return [(d_,'☕' if k else '✖️') for d_,k in zip(['M','T','W','T','F','S','S'],v)]
def _g(pic,grid,q,ans,*w,gfs=48): return dict(pic=pic,grid=grid,q=q,ans=ans,opts=[ans,*w],gfs=gfs)
HOWOFTEN=dict(m='choice',phase='STUDY',title='How often?',label='Exercise · How often?',lvl=2,min=3,levels=_lv3(
 [_g('☕',_freq([1,1,1,1,1,1,1]),'How often does she drink coffee?','every day','never','twice a week',gfs=44),_g('☕',_freq([0,0,0,0,0,0,0]),'How often does she drink coffee?','never','every day','twice a week',gfs=44),_g('☕',_freq([0,1,0,0,1,0,0]),'How often does she drink coffee?','twice a week','every day','never',gfs=44)],
 [_g('☕',_freq([1,1,1,1,1,1,1]),'What does the nurse write?','She drinks coffee every day.','She never drinks coffee.','She drinks coffee twice a week.',gfs=44),_g('☕',_freq([1,1,1,1,1,0,0]),'What does the nurse write?','She drinks coffee on weekdays only.','She drinks coffee at the weekend only.','She drinks coffee every day.',gfs=44),_g('☕',_freq([0,1,0,0,1,0,0]),'What does the nurse write?','She drinks coffee twice a week.','She drinks coffee every day.','She never drinks coffee.',gfs=44)],
 [_g('☕',_freq([1,1,1,1,1,0,0]),'What does the nurse write?','She drinks coffee five days a week, but not at the weekend.','She drinks coffee every day.','She drinks coffee at the weekend only.',gfs=44),_g('☕',_freq([0,0,0,0,0,1,1]),'What does the nurse write?','She only drinks coffee at the weekend.','She drinks coffee every day except the weekend.','She never drinks coffee.',gfs=44),_g('☕',_freq([1,1,1,1,1,1,0]),'What does the nurse write?','She drinks coffee every day except Sunday.','She drinks coffee only on Sunday.','She drinks coffee every day.',gfs=44)]))
WEEKQ=dict(m='choice',phase='STUDY',title='Is she telling the truth?',label='Her week · Is she telling the truth?',aud=True,lvl=2,min=3,levels=_lv3(
 [dict(pic='☕',say=sy,q='The café card says: '+cc+'. Is she telling the truth?',ans=a_,opts=[a_,b_]) for sy,cc,a_,b_ in [('I drink two coffees a day. Only two!','2 cups','Yes. She tells the truth.','No. She drinks more.'),('Two cups. Maybe three.','5 cups','No. She drinks more.','Yes. She tells the truth.'),('Just one coffee today, I promise.','1 cup','Yes. She tells the truth.','No. She drinks more.')]],
 [dict(pic='☕',say=sy,q='The café card says: '+cc+'. Is she telling the truth?',ans=a_,opts=[a_,b_,c_]) for sy,cc,a_,b_,c_ in [('Four cups, I know it is a lot.','4 cups','Yes. She tells the truth.','No. She drinks less.','No. She drinks more.'),('Only two cups on Friday!','8 cups','No. She drinks much more.','Yes. She tells the truth.','No. She drinks less.'),('I drink the same every day.','Mon 2 · Fri 8','No. Friday is much higher.','Yes. It is the same every day.','No. Friday is lower.')]],
 [dict(pic='🛏️',say=sy,q='The watch says: '+cc+'. Is she telling the truth?',ans=a_,opts=[a_,b_,c_]) for sy,cc,a_,b_,c_ in [('I sleep fine. Seven hours, easy.','3 hours','No. She sleeps much less.','Yes. She sleeps seven hours.','No. She sleeps more.'),('I sleep about six hours.','6 hours','Yes. She tells the truth.','No. She sleeps less.','No. She sleeps more.'),('My heart is fine. Totally normal.','110 beats per minute','Not really. Her pulse is higher than normal.','Yes. Her pulse is normal.','No. Her pulse is lower than normal.')]]))
_cg=lambda lab,v,u: [(d_,(u+'×%d'%k)) for d_,k in zip(lab,v)]
COMPARE2=dict(m='choice',phase='STUDY',title='Compare',label='Exercise · Compare (than · the most)',lvl=2,min=3,levels=_lv3(
 [dict(pic='☕',grid=_cg(['Mon','Fri'],[2,4],'☕'),gfs=40,q='Look at the cups. Which sentence is true?',ans='She drinks more coffee on Friday than on Monday.',opts=['She drinks more coffee on Friday than on Monday.','She drinks more coffee on Monday than on Friday.','She drinks the same on Monday and Friday.']),dict(pic='🛏️',grid=_cg(['Mon','Thu'],[3,2],'🌙'),gfs=40,q='Look at the nights. Which sentence is true?',ans='She sleeps less on Thursday than on Monday.',opts=['She sleeps less on Thursday than on Monday.','She sleeps more on Thursday than on Monday.','She sleeps the same on Thursday and Monday.']),dict(pic='💓',grid=[('Normal','60–100'),('Her pulse','110')],gfs=34,q='Which sentence is true?',ans='Her pulse is higher than normal.',opts=['Her pulse is higher than normal.','Her pulse is lower than normal.','Her pulse is the same as normal.'])],
 [dict(pic='☕',grid=_cg(['Mon','Tue','Wed','Thu','Fri'],[2,3,2,3,4],'☕'),gfs=30,q='Look at her week. Which sentence is true?',ans='She drinks the most coffee on Friday.',opts=['She drinks the most coffee on Friday.','She drinks the most coffee on Monday.','She drinks the least coffee on Friday.']),dict(pic='🛏️',grid=_cg(['Mon','Tue','Wed','Thu','Fri'],[3,4,3,2,3],'🌙'),gfs=30,q='Look at her week. Which sentence is true?',ans='She sleeps the least on Thursday.',opts=['She sleeps the least on Thursday.','She sleeps the most on Thursday.','She sleeps the least on Tuesday.']),dict(pic='💓',grid=[('Mon','90'),('Tue','100'),('Wed','110')],gfs=34,q='Her pulse during the week. Which sentence is true?',ans='Her pulse gets faster every day.',opts=['Her pulse gets faster every day.','Her pulse gets slower every day.','Her pulse stays the same.'])],
 [dict(pic='☕',grid=_cg(['Mon','Fri'],[2,4],'☕'),gfs=40,q='Which sentence is true?',ans='She drinks twice as much coffee on Friday as on Monday.',opts=['She drinks twice as much coffee on Friday as on Monday.','She drinks half as much coffee on Friday as on Monday.','She drinks the same on Friday and Monday.']),dict(pic='🛏️',grid=_cg(['Mon','Tue','Wed','Thu','Fri'],[3,4,3,2,3],'🌙'),gfs=30,q='Which sentence is true?',ans='Tuesday is her best night, and Thursday is her worst.',opts=['Tuesday is her best night, and Thursday is her worst.','Thursday is her best night, and Tuesday is her worst.','Every night is the same.']),dict(pic='💓',grid=[('Mon','108'),('Tue','112'),('Wed','110')],gfs=34,q='Normal: 60 to 100. Which sentence is true?',ans='Her pulse is higher than normal every day.',opts=['Her pulse is higher than normal every day.','Her pulse is lower than normal every day.','Her pulse is normal every day.'])]))
MORE_W=dict(m='teach',phase='STUDY',label='Teach · More symptoms',min=1,role='Four more feelings',words=[('🤢','nauseous'),('😮‍💨','breathless'),('😓','sweaty'),('🫥','pale')])
MORE_S=dict(m='teach',phase='STUDY',label='Teach · More patient sentences',min=2,role='Listen to the patient',pic='🤢',pics=['🤢','😮‍💨','😓','🫥'],tts=True,lines=[('She feels nauseous.',"I feel sick. I think I'm going to vomit."),('He is breathless.',"I climbed one floor… and I can't catch my breath."),('She is sweaty.','I am sweating, even with the air-con on!'),('She looks pale.','My friends say I look like a ghost.')])

# ---- 17 Nov round 3 ----
_R=lambda d: dict(d,ref='recommended',nl='Recommended')
DIAL4=[_d('💓','Pulse: 110 beats per minute','60 to 100 beats per minute','Her pulse is',4),_R(_d('🛏️','Sleep: 3 hours a night','7 to 9 hours a night','Her sleep time is',1)),_R(_d('☕','Coffee: 5 cups a day','up to 4 cups a day','Her coffee intake is',4)),_R(_d('🛏️','Sleep: 6 hours a night','7 to 9 hours a night','Her sleep time is',2)),_R(_d('☕','Coffee: 8 cups a day','up to 4 cups a day','Her coffee intake is',5)),_R(_d('☕','Coffee: 12 cups a day','up to 4 cups a day','Her coffee intake is',6))]
DIALA=[_da('💓','Pulse: 150 beats per minute','60 to 100 beats per minute','Her pulse is',5,'Her pulse is one hundred and fifty. Normal is sixty to one hundred.'),
 _R(_da('🛏️','Sleep: 6 hours a night','7 to 9 hours a night','Her sleep time is',2,'She sleeps six hours a night. The recommended amount is seven to nine hours.')),
 _R(_da('☕','Coffee: 5 cups a day','up to 4 cups a day','Her coffee intake is',4,'She drinks five cups of coffee a day. The recommended limit is four cups.')),
 _da('🌡️','Temperature: 37 °C','about 37 °C','Her temperature is',3,'Her temperature is thirty-seven degrees. Normal is about thirty-seven.'),
 _da('💓','Pulse: 38 beats per minute','60 to 100 beats per minute','Her pulse is',0,'Her pulse is thirty-eight beats a minute. Normal is sixty to one hundred.'),
 _R(_da('☕','Coffee: 12 cups a day','up to 4 cups a day','Her coffee intake is',6,'She drinks twelve cups of coffee a day. The recommended limit is four cups.'))]
DIALX=dict(DIALX,items=DIALA)
_MS=lambda t,x: _MI(t)+' <span style="color:#e8821a">'+x+'</span>'
MIGHT_T=dict(MIGHT_T,lines=[dict(k='🤔 Guessing',t='Her hands shake after every coffee. They also shake when she skips lunch.',c='amber'),dict(k='→ might',t=_MS('[[might]] be','the coffee.')+'<br>'+_MS('[[might]] be','low blood sugar.'),c='teal'),dict(k='🚫 Almost sure it is NOT',t='She has no cough. She has no fever.',c='amber'),dict(k="→ can't",t=_MS("[[can't]] be",'flu.'),c='teal')])
PAIRS=dict(PAIRS,pairs=[('She has no cough and no fever.',"It can't be flu."),('Her friends ate the same lunch. They are fine.',"It can't be food poisoning."),('Her hands shake when she skips breakfast.','It might be low blood sugar.'),('She has been worried about her exams for two weeks.','It might be stress.'),('She drinks eight cups of coffee a day.','It might be the coffee.')])
_cal=lambda *c: dict(grid=c,gfs=40)
LONGEX['levels'][1]['items']=[
 dict(pic='📅',grid=[('Mon','·'),('Tue','·'),('Wed','🤒'),('Thu','·'),('Fri','📍<div style="font-size:22px">today</div>')],gfs=44,say='It began on Wednesday.',q='What does the nurse write?',ans='It started two days ago.',opts=['It started two days ago.','It started two weeks ago.','It started two months ago.']),
 dict(pic='🗓️',grid=[('Mon','😴'),('Tue','·'),('Wed','·'),('Thu','📍<div style="font-size:22px">today</div>')],gfs=44,say='I have felt tired since Monday.',q='What does the nurse write?',ans='She has felt tired for three days.',opts=['She has felt tired for three days.','She has felt tired for three weeks.','She has felt tired for one day.']),
 dict(pic='🕑',grid=[('Week 1','🌙✖️'),('Week 2','🌙✖️'),('Today','📍')],gfs=44,say='Every night for two weeks, I cannot sleep.',q='What does the nurse write?',ans='She has not slept well for two weeks.',opts=['She has not slept well for two weeks.','She has not slept well for two days.','She has not slept well for four days.'])]

# one dial exercise: 2 shown, then listening (Nick 17 Nov)
_nos=lambda d_:{k:v for k,v in d_.items() if k!='say'}
_s3=dict(DIAL4[1],say='She sleeps three hours a night. The recommended amount is seven to nine hours.')
# Nick 17 Nov: mix written and spoken clues (spoken: sleep, sleep, coffee; numbers are written)
_T41=_d('🌡️','Temperature: 41 °C','about 37 °C','Her temperature is',6)
DIAL1=[DIAL4[0],_s3,_nos(DIALA[3]),DIALA[0],_nos(DIALA[1]),DIALA[4],_nos(DIALA[2]),_T41]

# ---- 17 Nov round 4: 3 items per level, woven vocab, truth bridge, Fix the ward as class questions ----
SYM4=[[_a('🥱',"I can't keep my eyes open!",'She is exhausted.','She is dizzy.','She is shaky.'),_a('💓','Boom-boom-boom! My heart is racing!','Her heart is racing.','Her heart is slow.','Her heart is sore.'),_a('🤢',"I feel sick. I think I'm going to vomit.",'She feels nauseous.','She feels dizzy.','She feels exhausted.')],
 [_a('😵‍💫','When I stand up, the room spins.','She feels dizzy when she stands up.','She feels dizzy when she sits down.','She feels dizzy when she sleeps.'),_a('☕','After each coffee, my hands shake!','Her hands shake after she drinks coffee.','Her hands shake before she drinks coffee.','Her hands never shake.'),_a('😮‍💨',"I climbed one floor… and I can't catch my breath.",'He is breathless.','He is dizzy.','He is hungry.')],
 [_a('🥱','I am so tired… but in bed, I just stare at the ceiling.','She is exhausted, but she cannot sleep.','She is exhausted, and she sleeps well.','She is not tired.'),_a('😓','I am sweating, and my face is white. Is the air-con on?','She is sweaty and pale.','She is sweaty and red.','She is cold and pale.'),_a('☕','Two cups. Maybe three. Okay… eight.','She drinks much more coffee than she first says.','She drinks only two cups.','She does not drink coffee.')]]
PAIRS=dict(PAIRS,pairs=[('She has no cough and no fever.',"It can't be flu."),('Her friends ate the same lunch. They are fine.',"It can't be food poisoning."),('Her hands shake when she skips breakfast.','It might be low blood sugar.'),('She is breathless and sweaty before every exam.','It might be stress.'),('She drinks eight cups of coffee a day.','It might be the coffee.')])
_FP3=stick(90,395,1.15,'up')+stick(310,395,1.15,'point')+bubble_svg(10,8,380,128,'Does anyone have\na voice note about\nthe temperature?',fs=25,tx=110)
FIX_COMIC=[dict(svg=_FP,cap='The night nurse made mistakes.'),dict(svg=_FP2,cap='Find the mistakes on the board.'),dict(svg=_FP3,cap='One group asks the class. Everyone listens.'),dict(svg=_FP4,cap='"Yes, we do." Listen. Choose the fix. Say it.')]

# ---- 17 Nov round 5: cups wording in Compare, truth exercise not all coffee, Plan B cleanup ----
def _tq(pic,say,src,ans,*w): return dict(pic=pic,say=say,q=src+' Is she telling the truth?',ans=ans,opts=[ans,*w])
WEEKQ=dict(m='choice',phase='STUDY',title='Is she telling the truth?',label='Her week · Is she telling the truth?',aud=True,lvl=2,min=3,levels=_lv3(
 [_tq('☕','I drink two coffees a day. Only two!','The café card says: 2 cups.','Yes. She tells the truth.','No. She drinks more.'),
  _tq('🛏️','I sleep fine. Seven hours, easy.','The watch says: 3 hours.','No. She sleeps less.','Yes. She tells the truth.'),
  _tq('🌡️','I have no fever.','The thermometer says: 36.8 °C.','Yes. She tells the truth.','No. She has a fever.')],
 [_tq('💓','My heart is fine. Totally normal.','The monitor says: 110 beats per minute.','Not really. Her pulse is higher than normal.','Yes. Her pulse is normal.','No. Her pulse is lower than normal.'),
  _tq('🛏️','I sleep about six hours.','The watch says: 6 hours.','Yes. She tells the truth.','No. She sleeps less.','No. She sleeps more.'),
  _tq('☕','Only two cups on Friday!','The café card says: 8 cups.','No. She drinks much more.','Yes. She tells the truth.','No. She drinks less.')],
 [_tq('📚','I am not worried about the exams at all.','Her friend says: she cannot sleep before every exam.','No. She is worried.','Yes. She is calm.','Yes. She is happy.'),
  _tq('🤕','My headache is mild. Two out of ten.','The nurse says: she cannot work.','No. It is not mild. It is severe.','Yes. It is mild.','Yes. It is moderate.'),
  _tq('💓','My pulse is always the same.','The monitor says: Monday 90, Tuesday 100, Wednesday 110.','No. It gets faster every day.','Yes. It is the same every day.','No. It gets slower every day.')]))
_cups=lambda lab,v: [(d_,'☕×%d'%k) for d_,k in zip(lab,v)]
COMPARE2=dict(COMPARE2,levels=_lv3(
 [dict(pic='☕',grid=_cups(['Mon','Fri'],[2,4]),gfs=40,q='Look at the cups. Which sentence is true?',ans='She has more cups on Friday than on Monday.',opts=['She has more cups on Friday than on Monday.','She has more cups on Monday than on Friday.','She has the same number of cups on both days.']),
  dict(pic='🛏️',grid=_cg(['Mon','Thu'],[3,2],'🌙'),gfs=40,q='Look at the nights. Which sentence is true?',ans='She sleeps less on Thursday than on Monday.',opts=['She sleeps less on Thursday than on Monday.','She sleeps more on Thursday than on Monday.','She sleeps the same on Thursday and Monday.']),
  dict(pic='💓',grid=[('Normal','60–100'),('Her pulse','110')],gfs=34,q='Which sentence is true?',ans='Her pulse is higher than normal.',opts=['Her pulse is higher than normal.','Her pulse is lower than normal.','Her pulse is the same as normal.'])],
 [dict(pic='☕',grid=_cups(['Mon','Tue','Wed','Thu','Fri'],[2,3,2,3,4]),gfs=30,q='Look at her week. Which sentence is true?',ans='She has the most cups on Friday.',opts=['She has the most cups on Friday.','She has the most cups on Monday.','She has the fewest cups on Friday.']),
  dict(pic='🛏️',grid=_cg(['Mon','Tue','Wed','Thu','Fri'],[3,4,3,2,3],'🌙'),gfs=30,q='Look at her week. Which sentence is true?',ans='She sleeps the least on Thursday.',opts=['She sleeps the least on Thursday.','She sleeps the most on Thursday.','She sleeps the least on Tuesday.']),
  dict(pic='💓',grid=[('Mon','90'),('Tue','100'),('Wed','110')],gfs=34,q='Her pulse during the week. Which sentence is true?',ans='Her pulse gets faster every day.',opts=['Her pulse gets faster every day.','Her pulse gets slower every day.','Her pulse stays the same.'])],
 [dict(pic='☕',grid=_cups(['Mon','Fri'],[2,4]),gfs=40,q='Which sentence is true?',ans='She has twice as many cups on Friday as on Monday.',opts=['She has twice as many cups on Friday as on Monday.','She has half as many cups on Friday as on Monday.','She has the same number of cups on both days.']),
  dict(pic='🛏️',grid=_cg(['Mon','Tue','Wed','Thu','Fri'],[3,4,3,2,3],'🌙'),gfs=30,q='Which sentence is true?',ans='Tuesday is her best night, and Thursday is her worst.',opts=['Tuesday is her best night, and Thursday is her worst.','Thursday is her best night, and Tuesday is her worst.','Every night is the same.']),
  dict(pic='💓',grid=[('Mon','108'),('Tue','112'),('Wed','110')],gfs=34,q='Normal: 60 to 100. Which sentence is true?',ans='Her pulse is higher than normal every day.',opts=['Her pulse is higher than normal every day.','Her pulse is lower than normal every day.','Her pulse is normal every day.'])]))
PLANB4=dict(PLANB4,tiles=[t for t in PLANB4['tiles'] if t['t'] not in ('Everybody lies','Name the symptom','Boss question')])
NEW_STUDY=[TODAY4,
 dict(m='teach',phase='STUDY',label='Teach · Symptoms',min=1,role='Four feelings',words=[('🥱','exhausted'),('😵‍💫','dizzy'),('🤲','shaky'),('💓','racing heart')]),
 dict(m='teach',phase='STUDY',label='Teach · Symptom sentences',min=2,role='Listen to the patient',pic='🥱',pics=['🥱','😵‍💫','🤲','💓'],tts=True,lines=[('She is exhausted.',"Ohhh… I can't keep my eyes open. I could sleep standing up!"),('He feels dizzy.','The room is spinning like a washing machine!'),('Her hands are shaky.',"Look at my hands! They won't stop shaking!"),('Her heart is racing.','My heart is racing, nurse. Boom-boom-boom!')]),
 MORE_W,
 dict(m='choice',phase='STUDY',title='Symptoms',label='Exercise · Symptoms',aud=True,min=3,lvl=3,levels=lv(SYM4)),
 dict(m='rungs',phase='STUDY',label='Teach · How bad?',min=1,title='How bad?',stops=BAD,start=2),
 dict(m='choice',phase='STUDY',title='How bad?',label='Exercise · How bad?',aud=True,min=2,lvl=2,levels=lv(HB4)),
 dict(m='rungs',phase='STUDY',label='Teach · How long?',min=1,title='How long?',stops=LONG,start=3),
 LONGEX,
 dict(m='dial',phase='STUDY',label='Exercise · Higher or lower?',min=4,title='How much higher? How much lower?',aud=True,items=DIAL1),
 MIGHT_T,PAIRS]

_n4=[]
for d in L4:
    lb=d.get('label')
    if lb=='Eyes closed. How bad?': d=dict(d,min=2,title=None,clips=['kampai.mp3','bello.mp3','papaya.mp3','banana.mp3'],rungs=['KAMPAI!','Bello!','Tu e bella<br>como la papaya!','Banana!'],side='Everyone, eyes closed, at the same time. Whisper first. Each word is louder.')
    elif lb=='The impossible day': d=dict(m='comic',phase='ENGAGE',label='The impossible night',min=3,title='The impossible night',panels=COMIC4)
    elif lb=='The dials': d=dict(m='teach',phase='STUDY',label='Teach · The dials',min=3,role='Say it with dials',pic='☕',lines=[dict(k='Start',t='She drinks coffee.'),dict(k='How often?',t='She drinks coffee [[every day]].',c='orange'),dict(k='How long?',t='It started [[two weeks ago]].',c='sky'),dict(k='How bad?',t='She is [[very]] tired.',c='rose')])
    elif lb=='Her week': d=dict(m='week',phase='STUDY',label='Her week',min=3,title='Her week',days=[dict(d='Mon',cups=2,h=3,says='Two coffees. I am fine!'),dict(d='Tue',cups=3,h=4,says='Three cups. One more…'),dict(d='Wed',cups=2,h=3,says='Only two. So tired.'),dict(d='Thu',cups=3,h=2,says='My hands shake…'),dict(d='Fri',cups=4,h=3,says='Four cups! I cannot stop.')])
    elif lb=='Teach · How bad?': d=dict(m='rungs',phase='STUDY',label='Teach · How bad?',min=2,title='How bad?',stops=BAD,start=2)
    elif lb=='Exercise · How bad?': d=dict(d,lvl=2)
    elif lb=='Teach · How long?': d=dict(d,min=1,lines=['She has a headache.','It started [[on]] Monday.','It started [[two days ago]].','It started [[two weeks ago]].'])
    elif lb=='Exercise · How long?': d=HOWLONG
    elif lb=='Teach · Compared with normal': d=dict(d,min=1,lines=['She sleeps 3 hours. Normal is 7 hours.','She sleeps [[less than]] normal.','Her pulse is 110. Normal is 60 to 100.','Her pulse is [[higher than]] normal.'])
    elif lb=='Exercise · Compared with normal?': d=NORMAL
    elif lb=='Exercise · How often?': d=dict(d,lvl=2)
    elif lb=='Exercise · Compare (than · the most)': d=COMPARE
    elif lb in('Exercise · Say it with a dial (1)','Exercise · Say it with a dial (2)','Extra · Name the symptom','Extra · Read the label (how often, how much)'): d=dict(d,lvl=2)
    elif lb=='Your sentences': d=dict(d,label='Your toolkit',title='Your hunt toolkit',groups=[
        {'t':'❓ Ask','c':'teal','l':['Can I hear your voice note about …?','What does it say about …?','Is that a mistake?'],'fs':44},
        {'t':'📢 Report','c':'sky','l':['The handover says … but the voice note says …','She drinks eight cups every day.','Her pulse is higher than normal.'],'fs':38},
        {'t':'⚖️ Argue','c':'rose','l':['It might be too much coffee because …',"It can't be a broken heart because …","It can't be flu because she has no cough."],'fs':38}],note='Ask with a question. Answer in a full sentence.')
    elif lb=='How the hunt works': d=dict(d,label='How Fix the ward works',title='How Fix the ward works',panels=FIX_COMIC)
    elif lb=='Case board · Find the reason': d=dict(d,reveal=d['reveal']+'<br>🌙 The night nurse wrote a chart just like her own: eight coffees, three hours of sleep!',title='Fix the ward',label='Case board · Fix the ward',clues=FIX_CLUES,unit='mistakes fixed',fix=True,min=11,teams=[(a,'Group %d'%(i+1),c,c2) for i,(a,b,c,c2) in enumerate(d['teams'])],frames=['Does anyone have a voice note about …?','Yes, we do. Come and listen.','Is that a mistake?'])
    elif lb=='Boss question (just for fun)': continue
    elif lb=='"Doctor, I\'m too busy."': continue
    elif lb=='"Doctor, I\'m too busy."': d=dict(d,min=6)
    _n4.append(d)
_by={d.get('label'):d for d in _n4}
_EXTRA=['Teach · The dials','Exercise · How often?','Exercise · Compare (than · the most)','Exercise · Say it with a dial (1)','Exercise · Say it with a dial (2)']
_by['Her week']=WEEKQ; _by['Exercise · How often?']=HOWOFTEN; _by['Exercise · Compare (than · the most)']=COMPARE2
_i=[d.get('label') for d in _n4].index('Your toolkit')
L4=_n4[:3]+NEW_STUDY+_n4[_i:]
L4=[(dict(WEEKQ,phase='ACTIVATE',label='Everybody lies',title='Everybody lies?',min=3) if d.get('label')=='Everybody lies' else d) for d in L4]
# Nick 17 Nov pm: Everybody lies before the toolkit; recap matches the core Study; Taboo stays in the main run
_ix={d.get('label'):i for i,d in enumerate(L4)}
_a,_b=_ix['Your toolkit'],_ix['Everybody lies']
if _a<_b: L4[_a],L4[_b]=L4[_b],L4[_a]
_RC=[([('c1','She'),('c2','has felt'),('c3','tired'),('c4','for two weeks.')],'for'),([('c1','Her pulse'),('c2','is'),('c3','much higher than normal.')],'than'),([('c1','It'),('c2','might be'),('c3','too much coffee.')],'might'),([('c1','It'),('c2',"can't be"),('c3','flu.')],'because…'),([('c1','He'),('c2','is'),('c3','breathless, sweaty and pale.')],'symptoms')]
_T=[]
for d in L4:
    if d.get('label')=='Recap': d=dict(d,rows=_RC)
    elif d.get('m')=='taboo': d=dict(d,label='Taboo for nurses',optional=False,min=5)
    _T.append(d)
L4=_T
# dial: picture-arc version is the main exercise; the zone-word arc stays as an optional backup right after it (Nick 17 Nov)
_L=[]
for d in L4:
    if d.get('m')=='dial' and d.get('label')=='Exercise · Higher or lower?':
        _L.append(dict(d,min=4))
    else: _L.append(d)
L4=_L
# ---- 17 Nov midday 2 (Nick): because on the teach slide, new words reused, audio chat bridge, Today/Recap match, partner prompts ----
_PT='💬 Tell your partner. Then tap.'
_MIGHT_T2=dict(MIGHT_T,lines=[dict(k='🤔 Guessing',t='Her hands are shaky after coffee. Also when she skips lunch.',c='amber'),dict(k='→ might',t=_MS('[[might]] be','too much coffee.')+'<br>'+_MS('[[might]] be','low blood sugar.'),c='teal'),dict(k='🚫 Almost sure it is NOT',t='She has no cough. She has no fever.',c='amber'),dict(k="→ can't + because",t=_MS("[[can't]] be",'flu [[because]] she has no fever.'),c='teal')])
_PAIRS2=dict(PAIRS,hint='⚽ Tap a clue. Pass the ball to a student.',ball=True,lvl=1,pairs=[('She has no cough and no fever.',"It can't be flu."),('Her friends ate the same lunch. They are fine.',"It can't be food poisoning."),('Her hands are shaky when she skips breakfast.','It might be low blood sugar.'),('She is breathless and sweaty before every exam.','It might be stress.'),('She drinks eight cups of coffee a day.','It might be too much coffee.')],levels=[{},{'hide':True},{'hide':True,'pairs':[('She has no cough and no fever.',"It can't be flu because she has no fever."),('Her friends ate the same lunch. They are fine.',"It can't be food poisoning because they are fine."),('Her hands are shaky when she skips breakfast.','It might be low blood sugar because she skips breakfast.'),('She is breathless and sweaty before every exam.','It might be stress because it happens before exams.'),('She drinks eight cups of coffee a day.','It might be too much coffee because she drinks eight cups.')]}])
_Q=lambda c,t,g=False:(c,t,g)
CHAT4=dict(m='chat',phase='STUDY',label='Exercise · Patient chat (voice messages)',min=4,title='Voice messages',window=4,pt='🎧 Listen. Then answer as the nurse.',lines=[
 ('P',dict(say='My hands are shaky and my heart is racing. What is wrong with me?')),
 ('N',[_Q('c2','Do you drink'),_Q('c3','a lot of coffee?',True)],[('c3','a lot of coffee?'),('c3','a lot of water?'),('c3','a lot of tea?')]),
 ('P',dict(say='Eight cups a day! Coffee is my best friend.')),
 ('N',[_Q('c1','It'),_Q('c2','might',True),_Q('c2','be'),_Q('c3','too much coffee.')],[('c2','might'),('c2',"can't")]),
 ('P',dict(say='I feel nauseous and sweaty. What is wrong with me?')),
 ('N',[_Q('c2','Do you have'),_Q('c3','a fever?',True)],[('c3','a fever?'),('c3','a rash?'),('c3','a cat?')]),
 ('P',dict(say='No fever. No cough. Only my cat looks worried.')),
 ('N',[_Q('c1','It'),_Q('c2',"can't",True),_Q('c2','be'),_Q('c3','flu'),_Q('c4','because',True),_Q('c1','you have no fever.')],[('c2','might'),('c2',"can't"),('c4','because'),('c4','but')]),
 ('P',dict(say='I am exhausted and dizzy. What is wrong with me?')),
 ('N',[_Q('c2','Do you have'),_Q('c3','exams?',True)],[('c3','exams?'),('c3','a cat?'),('c3','a fever?')]),
 ('P',dict(say='Yes! They started two weeks ago. And my cat watches me all night.')),
 ('N',[_Q('c1','It'),_Q('c2','might',True),_Q('c2','be'),_Q('c3','stress'),_Q('c4','because',True),_Q('c1','you have exams.')],[('c2','might'),('c2',"can't"),('c4','because'),('c4','but')]),
 ('P',dict(say='Okay, okay. You are right. But I need one more coffee.')),
])
_ZG={'pulse_hi':'slightly 101–120 · much 121–150 · dangerously over 150','pulse_lo':'slightly 50–59 · much 40–49 · dangerously under 40','sleep':'slightly 5–6 h · much 3–4 h · dangerously under 3 h','temp_n':'normal: 36 to 37.5 °C','temp_hi':'slightly 38–39 · much 39–40 · dangerously over 40','coffee':'slightly 5–6 · much 7–9 · dangerously 10 or more'}
_DG=[('pulse_hi',True),('sleep',0),('temp_n',0),('pulse_hi',0),('sleep',0),('pulse_lo',0),('coffee',0),('temp_hi',0)]
for _it,(_g,_dm) in zip(DIAL1,_DG): _it['guide']=_ZG[_g]; _it['demo']=bool(_dm)
_T3=[]
for d in L4:
    lb=d.get('label'); m=d['m']
    if m=='today': d=dict(d,rows=[[('c4','Say'),('c3','how bad')],[('c1','Say'),('c3','how long')],[('c4','Say'),('c3','higher / lower than normal')],[('c2','might'),('c4',"can't"),('c3','because')]])
    elif lb=="Teach · Might, can't, because": d=_MIGHT_T2
    elif lb=="Exercise · Might · can't": d=_PAIRS2; _T3.append(d); _T3.append(CHAT4); continue
    elif lb=='Recap': d=dict(d,rows=[([('c1','He'),('c2','is'),('c3','breathless, sweaty and pale.')],'symptoms'),([('c1','His pain'),('c2','is'),('c3','severe.')],'how bad'),([('c1','It'),('c2','started'),('c4','two weeks ago.')],'ago'),([('c1','Her pulse'),('c2','is'),('c3','much higher than normal.')],'than'),([('c1','It'),('c2','might be'),('c3','too much coffee.')],'might'),([('c1','It'),('c2',"can't be"),('c3','flu because she has no fever.')],'because')])
    if m in ('choice','dial','chat') and lb and (lb.startswith('Exercise') or lb.startswith('Everybody')) and not d.get('pt') and lb!='Exercise · Symptoms': d=dict(d,pt=_PT)
    _T3.append(d)
L4=_T3
def _rr(o,m):
    if isinstance(o,str):
        for a,b in m.items(): o=o.replace(a,b)
        return o
    if isinstance(o,list): return [_rr(x,m) for x in o]
    if isinstance(o,dict): return {k:_rr(v,m) for k,v in o.items()}
    if isinstance(o,tuple): return tuple(_rr(x,m) for x in o)
    return o
L4=[d if d['m'] in ('dial','chat','pairs','recap','today') else _rr(d,{'say':None}) if False else d for d in L4]
_SAYM={"I woke up like this this morning.":"I feel dizzy. I woke up like this this morning.","I have been like this for two weeks.":"I am exhausted. I have been like this for two weeks."}
def _say_only(o):
    if isinstance(o,dict): return {k:(_rr(v,_SAYM) if k=='say' else _say_only(v)) for k,v in o.items()}
    if isinstance(o,list): return [_say_only(x) for x in o]
    return o
L4=[_say_only(d) if d.get('label') in ('Teach · How long?','Exercise · How long?') else d for d in L4]
TABOO4=[d for d in L4 if d['m']=='taboo'][0]
TABOO4['items']=[dict(w='shaky',e='🤲',no=['shake','hands','cold','fall']),dict(w='coffee',e='☕',no=['cup','drink','morning','caffeine']),dict(w='dizzy',e='😵‍💫',no=['spin','head','fall','room']),dict(w='pulse',e='💓',no=['heart','beat','wrist','minute']),dict(w='nauseous',e='🤢',no=['sick','vomit','stomach','feel']),dict(w='headache',e='🤕',no=['head','pain','hurt','tablet']),dict(w='breathless',e='😮‍💨',no=['breath','air','run','stairs']),dict(w='exam',e='📝',no=['test','study','paper','university'])]

# ---- 17 Nov pm: Gemini art placed (slots without art yet keep their emoji / drawing) ----
ARTMAP={'🥱':'l4_c1_exhausted.jpg','🤲':'l4_c3_shaky.jpg','💓':'l4_c4_racing_heart.jpg','🤢':'l4_c5_nauseous.jpg','🫥':'l4_c8_pale.jpg','😵‍💫':'l4_c2_dizzy.jpg','😮‍💨':'l4_c6_breathless.jpg','😓':'l4_c7_sweaty.jpg'}
_ARTLB=('Teach · Symptoms','Teach · Symptom sentences','Teach · More symptoms','Teach · More patient sentences','Exercise · Symptoms')
def _artswap(o):
    if isinstance(o,str): return ARTMAP.get(o,o)
    if isinstance(o,list): return [_artswap(x) for x in o]
    if isinstance(o,tuple): return tuple(_artswap(x) for x in o)
    if isinstance(o,dict): return {k:_artswap(v) for k,v in o.items()}
    return o
L4=[_artswap(d) if d.get('label') in _ARTLB else d for d in L4]
for d in L4:
    if d['m']=='cover': d['cards']=[dict(d['cards'][0],pic='l4_a1_cover_exams.jpg'),dict(d['cards'][1],pic='l4_a2_cover_coffee.jpg')]
COMIC4[0]['img']='l4_b1_books.jpg'; COMIC4[1]['img']='l4_b2_coffee.jpg'; COMIC4[2]['img']='l4_b3_night.jpg'
FIX_COMIC[0]['img']='l4_d1_night_nurse.jpg'; FIX_COMIC[1]['img']='l4_d2_find.jpg'; FIX_COMIC[2]['img']='l4_d3_ask.jpg'; FIX_COMIC[3]['img']='l4_d4_fix.jpg'
# 17 Nov 15:00: Everybody lies listen cards get art where it exists (thermometer/headache still emoji)
_LIEMAP={'☕':'l4_b2_coffee.jpg','🛏️':'l4_b3_night.jpg','💓':'l4_c4_racing_heart.jpg','📚':'l4_b1_books.jpg'}
def _liefix(o):
    if isinstance(o,dict): return {k:(_LIEMAP.get(v,v) if k=='pic' else _liefix(v)) for k,v in o.items()}
    if isinstance(o,list): return [_liefix(x) for x in o]
    return o
L4=[_liefix(d) if d.get('label')=='Everybody lies' else d for d in L4]
# 17 Nov 15:15 (Nick): B4 art, toolkit bubbles, teach pics
COMIC4[3]['img']='l4_b4_asleep.jpg'
for _p in COMIC4: _p['cap']=''
for d in L4:
    if d.get('label')=='Your toolkit': d['bubbles']=True
    if d.get('label')=="Teach · Might, can't, because": d['pics']=['l4_c3_shaky.jpg','l4_g2_might_causes.jpg','l4_h1_thermometer.jpg','l4_h1_thermometer.jpg']; d['pic']='l4_c3_shaky.jpg'
    if d.get('label')=='Exercise · Symptoms':
        d=d
# 17 Nov 15:30: pain faces -> art, cups, thermometer
_FMAP={'🙂':'l4_f5_pain_gone.jpg','😕':'l4_f1_pain_mild.jpg','😣':'l4_f2_pain_moderate.jpg','😖':'l4_f3_pain_severe.jpg','😭':'l4_f4_pain_unbearable.jpg'}
def _fm(o,M):
    if isinstance(o,str): return M.get(o,o)
    if isinstance(o,list): return [_fm(x,M) for x in o]
    if isinstance(o,tuple): return tuple(_fm(x,M) for x in o)
    if isinstance(o,dict): return {k:_fm(v,M) for k,v in o.items()}
    return o
def _cupfix(o):
    if isinstance(o,dict):
        if o.get('pic')=='☕' and o.get('say'): 
            return dict({k:_cupfix(v) for k,v in o.items()},pic='l4_g1_cups_eight.jpg' if o['say'].startswith('Two cups') else 'l4_c3_shaky.jpg')
        return {k:_cupfix(v) for k,v in o.items()}
    if isinstance(o,list): return [_cupfix(x) for x in o]
    return o
_nl=[]
for d in L4:
    lb=d.get('label')
    if lb in ('Teach · How bad?','Exercise · How bad?'): d=_fm(d,_FMAP)
    if lb=='Exercise · Symptoms': d=_cupfix(d)
    if lb in ('Everybody lies',"Teach · Might, can't, because"): d=_fm(d,{'🌡️':'l4_h1_thermometer.jpg','🤕':'l4_h2_headache_mild.jpg'})
    _nl.append(d)
L4=_nl
# 17 Nov 15:45: toolkit as colour-coded chips (like the grammar rows), p13 dial art
_S,_V,_O,_B,_T='s','v','o','b','t'
for d in L4:
    if d.get('label')=='Your toolkit':
        d['bubbles']=False
        d['chips']=[
          [[('Can',_V),('I',_S),('hear',_V),('your voice note',_O),('about …?',_O)],[('What',_B),('does',_V),('it',_S),('say',_V),('about …?',_O)],[('Is',_V),('that',_S),('a mistake?',_O)]],
          [[('The handover',_S),('says',_V),('…',_O),('but',_B),('the voice note',_S),('says',_V),('…',_O)],[('She',_S),('drinks',_V),('eight cups',_O),('every day.',_T)],[('Her pulse',_S),('is',_V),('higher than normal.',_O)]],
          [[('It',_S),('might be',_V),('too much coffee',_O),('because …',_B)],[('It',_S),("can't be",_V),('a broken heart',_O),('because …',_B)],[('It',_S),("can't be",_V),('flu',_O),('because',_B),('she',_S),('has',_V),('no cough.',_O)]]]
    if d.get('label')=='Exercise · Higher or lower?':
        _DA={('💓','Pulse: 110 beats per minute'):'l4_c4_racing_heart.jpg',('💓','Pulse: 150 beats per minute'):'l4_c4_racing_heart.jpg',('💓','Pulse: 38 beats per minute'):'l4_h4_pulse_slow.jpg',('🛏️','Sleep: 3 hours a night'):'l4_b3_night.jpg',('🛏️','Sleep: 6 hours a night'):'l4_b3_night.jpg',('🌡️','Temperature: 37 °C'):'l4_h1_thermometer.jpg',('🌡️','Temperature: 41 °C'):'l4_h3_fever_high.jpg',('☕','Coffee: 5 cups a day'):'l4_b2_coffee.jpg'}
        import os as _os
        for _k,_f in {('💓','Pulse: 110 beats per minute'):'l4_i1_pulse_slightly_high.jpg',('💓','Pulse: 38 beats per minute'):'l4_i2_pulse_dangerously_low.jpg',('🛏️','Sleep: 6 hours a night'):'l4_i3_sleep_6h_rested.jpg'}.items():
            if _os.path.exists('/home/claude/work/lesson/art/'+_f): _DA[_k]=_f
        for it in d['items']:
            if it['s'].startswith('Her temperature'): it['nt']=1
        for it in d['items']:
            a=_DA.get((it['e'],it['now']))
            if a: it['art']=ART+a
# ---- Nick 17 Nov 21:29 batch (L4) ----
import re as _re
def _she(o):
    if isinstance(o,str):
        for a,b in (('He','She'),('he','she'),('His','Her'),('his','her'),('him','her')): o=_re.sub(r'\b'+a+r'\b',b,o)
        return o
    if isinstance(o,list): return [_she(x) for x in o]
    if isinstance(o,tuple): return tuple(_she(x) for x in o)
    if isinstance(o,dict): return {k:(v if k in ('art','pic','pics','m','phase') else _she(v)) for k,v in o.items()}
    return o
_NEWREV=("<b>[[It is too much coffee.]]</b><br>She says she drinks two cups, but the café card says [[eight]].<br>She sleeps only [[3 hours]], and her pulse is [[faster than normal]].<br>"
 "She has [[no fever and no cough]], so it can't be flu.<br>She has [[no stomach problems]], so it can't be food poisoning.<br>On Sunday she drank [[no coffee]], and she felt [[much better]].<br>"
 "🌙 The night nurse wrote a chart just like her own: eight coffees, three hours of sleep!")
_LF4=dict(m='listen_fix',phase='ACTIVATE',label='Listen and fix (night chart)',min=4,title='Listen and fix the chart',items=[
   dict(text='She drinks two cups of coffee every day',say='She drinks eight cups of coffee every day',opts=['five','ten']),
   dict(text='Her pulse is lower than normal',say='Her pulse is higher than normal',opts=['slower','much']),
   dict(text='She sleeps nine hours a night',say='She sleeps three hours a night',opts=['six','seven']),
   dict(text='Her headache is mild',say='Her headache is severe',opts=['moderate','unbearable'])],lvl=1,levels=[dict(mode='opts'),dict(mode='opts'),dict(mode='type')])
_L=[]
for d in L4:
    lb=d.get('label')
    if lb=='Exercise · How bad?': d=dict(d,pt='')
    if lb=='Your toolkit': d=dict(d,note=None)
    if lb=='Case board · Fix the ward':
        import re as _r2
        d=dict(d,reveal=_re.sub(r'\[\[(.+?)\]\]',r'<span class="ulw">\1</span>',_NEWREV))
    import os as _o3
    _ex=lambda f:_o3.path.exists('/home/claude/work/lesson/art/'+f)
    if d.get('m')=='vol_ladder' and _ex('l4_j1_eyes_closed.jpg'): d=dict(d,emoji='l4_j1_eyes_closed.jpg')
    if lb=='Taboo for nurses' and _ex('l4_k1_taboo_words_only.jpg'): d=dict(d,introArt=ART+'l4_k1_taboo_words_only.jpg')
    _L.append(d)
    if lb=='How Fix the ward works':
        import base64 as _b64
        _qd=lambda n:'data:image/png;base64,'+_b64.b64encode(open(f'/home/claude/lesson-a/lessons-3-4/source-art/print/qr_{n}.png','rb').read()).decode()
        _L.append(dict(m='qr_groups',phase='ACTIVATE',label='Group QR codes',title='Scan your group',min=1,qrs=[_qd(n) for n in '1234'],cols=['#ff5a6a','#2a8cf0','#19b38a','#f2a900']))
L4=[_she(d) for d in _L]
import base64 as _b64a
def _fixclip(n):
    f='/home/claude/lesson-a/lessons-3-4/source-audio/l4_fix/FIX_%02d.mp3'%n
    return 'data:audio/mpeg;base64,'+_b64a.b64encode(open(f,'rb').read()).decode() if _o3.path.exists(f) else ''
_gi=lambda o:[dict(pic=f['pic'],clip=_fixclip(f['n']),say=f['voice'].replace('"','&quot;')) for f in FIX if f['owner']==o]
_ci=next(i for i,d in enumerate(L4) if d.get('label')=='Thank you')
L4.insert(_ci+1,dict(m='audio_all',phase='ACTIVATE',label='Teacher backup · all group voice notes',optional=True,min=1,title='All voice notes',groups=[_gi(o) for o in ('red','blue','green','yellow')],cols=['#ff5a6a','#2a8cf0','#19b38a','#f2a900']))
L4.append(dict(m='boss',phase='ACTIVATE',label='Boss question (just for fun)',optional=True,min=3,**K.L4_BOSS,sec=90))
# ================= L3 REBUILD (18 Nov): L4 patterns ported, more audio, more teaching points =================
_PT3='💬 Tell your partner. Then tap.'
SYM3=[[_a2('🌡️','I am so hot! Can I sleep in the fridge?','She has a fever.','She has a rash.','She has a cough.'),
  _a2('😷','Cough, cough! The whole ward is moving away from me.','He has a cough.','He has a rash.','He has a fever.'),
  _a2('🔴','Look at my arm! I look like a strawberry!','He has a rash on his arm.','He has a cough on his arm.','He has a fever on his arm.')],
 [_a2('🥶','Brrr… I am shaking under three blankets! But my head is hot.','She has chills and a fever.','She has a rash and a fever.','She has a cough and chills.'),
  _a2('🧴',"Ugh, my arm is so itchy! I could scratch it all night.",'His arm is itchy.','His arm is stiff.','His arm is cold.'),
  _a2('🤕','My head, my eyes, my muscles… even my hair hurts!','Her head, her eyes and her muscles hurt.','Her head hurts, but her muscles are fine.','Her eyes hurt, but her head is fine.')],
 [_a2('🍚','No breakfast, no lunch, no dinner. I am just not hungry!','She has no appetite.','She has a big appetite.','She is itchy.'),
  _a2('🔴','Red spots on my arms. They itch, but my face is fine.','She has an itchy rash on her arms, but not on her face.','She has an itchy rash on her face, but not on her arms.','She has a rash on her arms and her face.'),
  _a2('🦟','A mosquito bit me a week ago. Now I am sick.','She was bitten by a mosquito a week ago.','She bit a mosquito a week ago.','A mosquito was sick a week ago.')]]
MORE3_W=dict(m='teach',phase='STUDY',label='Teach · More symptoms',min=1,role='Four more',words=[('🥶','chills'),('🧴','itchy'),('🫨','stiff'),('🍚','no appetite')])
MORE3_S=dict(m='teach',phase='STUDY',label='Teach · More patient sentences',min=2,optional=True,role='Listen to the patient',pic='🥶',pics=['🥶','🧴','🫨','🍚'],tts=True,lines=[('She has chills.','I am freezing! But my forehead is burning.'),('His arm is itchy.',"I can't stop scratching!"),('His neck is stiff.','I cannot turn my head. It is so stiff!'),('She has no appetite.','I do not want food. Not even my favourite noodles.')])
# --- the dial: one slide (demo, teaching ranges, art, spoken items), L3 content, "than normal" kept ---
_ZG3={'pulse_hi':'slightly 101–120 · much 121–150 · dangerously over 150','pulse_lo':'slightly 50–59 · much 40–49 · dangerously under 40','temp_hi':'slightly 38–39 · much 39–40 · dangerously over 40','temp_lo':'slightly 35–36 · much 33–35 · dangerously under 33','breath':'normal: 12 to 20 breaths a minute','plat':'normal 150–450 thousand · low under 150 · very low under 50'}
DIAL3=[_d('💓','Pulse: 104 beats per minute','60 to 100 beats per minute','Her pulse is',4),
 _da('🌡️','Temperature: 41 °C','about 37 °C','Her temperature is',6,'Her temperature is forty-one degrees. Normal is about thirty-seven.'),
 _d('🌡️','Temperature: 39.2 °C','about 37 °C','Her temperature is',5),
 _da('🩸','Platelets: 95,000 per µL','150,000 to 450,000 per µL','Her platelets are',1,'Her platelets are ninety-five thousand. Normal is one hundred and fifty to four hundred and fifty thousand.'),
 _d('🫁','Breathing: 16 breaths per minute','12 to 20 breaths per minute','Her breathing is',3),
 _da('💓','Pulse: 130 beats per minute','60 to 100 beats per minute','Her pulse is',5,'Her pulse is one hundred and thirty. Normal is sixty to one hundred.'),
 _da('🫁','Breathing: 40 breaths per minute','12 to 20 breaths per minute','Her breathing is',6,'She breathes forty times a minute. Normal is twelve to twenty.'),
 _da('🌡️','Temperature: 32 °C','about 37 °C','Her temperature is',0,'Her temperature is thirty-two degrees. Normal is about thirty-seven.')]
_DG3=[('pulse_hi',True),('temp_hi',0),('temp_hi',0),('plat',0),('breath',0),('pulse_hi',0),('breath',0),('temp_lo',0)]
for _it,(_g,_dm) in zip(DIAL3,_DG3): _it['guide']=_ZG3[_g]; _it['demo']=bool(_dm)
# --- listen and tick the numbers (units) ---
NUM3=dict(m='choice',phase='STUDY',title='Listen: the number',label='Exercise · Listen and tick the numbers',aud=True,lvl=2,min=3,pt=_PT3,levels=_lv3(
 [_a2('🌡️','Her temperature is thirty-nine point two degrees.','39.2 °C','29.2 °C','39.2 beats per minute'),_a2('💓','Her pulse is one hundred and four beats a minute.','104 beats per minute','140 beats per minute','104 °C'),_a2('🫁','She breathes eighteen times a minute.','18 breaths per minute','80 breaths per minute','18 °C')],
 [_a2('🩸','Platelets: ninety-five thousand per microlitre.','95,000 per µL','9,500 per µL','950,000 per µL'),_a2('🌡️','Normal is about thirty-seven. Hers is thirty-eight point one.','Her temperature is 38.1 °C. Normal is 37 °C.','Her temperature is 38.1 °C. Normal is 36 °C.','Her temperature is 31.8 °C. Normal is 37 °C.'),_a2('💓','Her pulse is forty-eight. Normal is sixty to one hundred.','Her pulse is 48. Normal is 60 to 100.','Her pulse is 84. Normal is 60 to 100.','Her pulse is 48. Normal is 16 to 100.')],
 [_a2('🩸','White cells: three thousand one hundred per microlitre. Normal is four and a half to eleven thousand.','White cells: 3,100 per µL. Normal: 4,500 to 11,000.','White cells: 31,000 per µL. Normal: 4,500 to 11,000.','White cells: 3,100 per µL. Normal: 45,000 to 110,000.'),_a2('🌡️','She says she feels a little warm. The thermometer says forty-one degrees!','The thermometer says 41 °C. That is dangerously high.','The thermometer says 14 °C. That is dangerously low.','The thermometer says 41 °C. That is normal.'),_a2('🫁','Breathing: twenty-one breaths a minute. Normal is twelve to twenty.','Her breathing is 21. It is slightly higher than normal.','Her breathing is 12. It is lower than normal.','Her breathing is 21. It is normal.')]))
# --- asking history questions (teach + hear the answer, pick the question) ---
HIST_T=dict(m='teach',phase='STUDY',label='Teach · Ask the patient',min=2,role='Good questions',pic='🩺',pics=['🌡️','🤕','😷','🦟'],lines=['How long have you had a fever?','Where does it hurt?','Do you have a cough?','Did a mosquito bite you?'])
HIST_E=dict(m='choice',phase='STUDY',title='Which question?',label='Exercise · Hear the answer, pick the question',aud=True,lvl=2,min=3,pt=_PT3,levels=_lv3(
 [dict(pic='🌡️',say='Three days.',q='Which question did the nurse ask?',ans='How long have you had a fever?',opts=['How long have you had a fever?','Where does it hurt?','Do you have a cough?']),
  dict(pic='🤕',say='Behind my eyes. And my muscles.',q='Which question did the nurse ask?',ans='Where does it hurt?',opts=['Where does it hurt?','How long have you had a fever?','Did a mosquito bite you?']),
  dict(pic='🦟',say='Yes, a lot. By the pond, a week ago.',q='Which question did the nurse ask?',ans='Did a mosquito bite you?',opts=['Did a mosquito bite you?','Do you have a cough?','Where does it hurt?'])],
 [dict(pic='😷',say='No cough. Not once this week.',q='Which question did the nurse ask?',ans='Do you have a cough?',opts=['Do you have a cough?','Do you have a rash?','Did you have a cough?']),
  dict(pic='🌡️',say='It started on Monday. So three days.',q='Which question did the nurse ask?',ans='When did the fever start?',opts=['When did the fever start?','Where does the fever start?','Who has a fever?']),
  dict(pic='🍱',say='We all ate the same lunch. Nobody else is sick.',q='Which question did the nurse ask?',ans='Did your friends eat the same food?',opts=['Did your friends eat the same food?','Did you eat the same food?','Do your friends eat food?'])],
 [dict(pic='💊',say='Paracetamol, yesterday. The fever went down, and then it came back.',q='Which question did the nurse ask?',ans='Did you take any medicine?',opts=['Did you take any medicine?','Do you take any medicine?','Did you make any medicine?']),
  dict(pic='🏘️',say='Yes. Two people on my street had a fever last week.',q='Which question did the nurse ask?',ans='Is anyone else sick near you?',opts=['Is anyone else sick near you?','Are you sick near anyone else?','Is anyone sick else you?']),
  dict(pic='💉',say='Two doses, in school. I have the card.',q='Which question did the nurse ask?',ans='Have you had the measles vaccine?',opts=['Have you had the measles vaccine?','Do you have the measles vaccine?','Have you got measles?'])]))
# --- certainty ladder (can't → unlikely → might → probably → it is) ---
CERT=[dict(word="can't",e='🚫',gloss='0%',sen="It [[can't]] be appendicitis.",say="It can't be appendicitis. I am sure."),
 dict(word='unlikely',e='🤏',gloss='10–20%',sen='It is [[unlikely]] to be flu.',say='It is unlikely to be flu. Maybe one chance in ten.'),
 dict(word='might',e='🤔',gloss='30–60%',sen='It [[might]] be dengue.',say='It might be dengue. Maybe.'),
 dict(word='probably',e='👍',gloss='70–90%',sen='It is [[probably]] dengue.',say='It is probably dengue. I am nearly sure.'),
 dict(word='it is',e='✅',gloss='100%',sen='It [[is]] dengue.',say='It is dengue. The test says so.')]
CERT_T=dict(m='rungs',phase='STUDY',label='Teach · How sure?',min=2,title='How sure is the nurse?',stops=CERT,start=2)
CERT_E=dict(m='choice',phase='STUDY',title='How sure?',label='Exercise · How sure?',aud=True,lvl=2,min=3,pt=_PT3,levels=_lv3(
 [_a2('🚫',"It can't be appendicitis.",'The nurse is sure. It is not appendicitis.','The nurse is not sure.','It is appendicitis.'),_a2('🤔','It might be dengue.','The nurse is not sure. Maybe.','The nurse is sure.',"It can't be dengue."),_a2('✅','It is dengue.','The nurse is sure. It is dengue.','Maybe it is dengue.',"It can't be dengue.")],
 [_a2('🤏','It is unlikely to be measles.','Measles: a small chance.','Measles: a very big chance.','Measles: 100%.'),_a2('👍','It is probably dengue.','Dengue: a big chance.','Dengue: a small chance.','Dengue: 0%.'),_a2('🤔','It might be flu, or it might be dengue.','The nurse has two ideas.','The nurse has one idea.','The nurse has no idea.')],
 [_a2('🤏','It is unlikely to be flu, because she has no cough.','Flu: unlikely. The reason is no cough.','Flu: probably. The reason is no cough.','Flu: unlikely. The reason is a cough.'),_a2('👍','It is probably dengue, because she has a rash and a mosquito bite.','Dengue: probably. Two clues.','Dengue: unlikely. Two clues.','Dengue: probably. No clues.'),_a2('🚫',"It can't be appendicitis, because her belly does not hurt.",'Appendicitis: no. Her belly is fine.','Appendicitis: yes. Her belly hurts.','Appendicitis: maybe.')]))
# --- might / can't: line-by-line picture teach, then the ball drill ---
MIGHT3_T=dict(m='teach',phase='STUDY',label="Teach · Might, can't, because",min=1,role='Clue → sentence',pic='🦟',lines=[dict(k='🤔 Guessing',t='She was bitten by mosquitoes. She has a fever and a rash.',c='amber'),dict(k='→ might',t=_MS('[[might]] be','dengue.')+'<br>'+_MS('[[might]] be','measles.'),c='teal'),dict(k='🚫 Almost sure it is NOT',t='She has no cough. She has no runny nose.',c='amber'),dict(k="→ can't + because",t=_MS("[[can't]] be",'flu [[because]] she has no cough.'),c='teal')])
_P3A=[('She has no cough.',"It can't be flu."),('Her belly does not hurt.',"It can't be appendicitis."),('She was bitten by mosquitoes.','It might be dengue.'),('She has a rash and a fever.','It might be measles.'),('She had two measles vaccines.',"It is unlikely to be measles.")]
_P3B=[('She has no cough.',"It can't be flu because she has no cough."),('Her belly does not hurt.',"It can't be appendicitis because her belly does not hurt."),('She was bitten by mosquitoes.','It might be dengue because mosquitoes bit her.'),('She has a rash and a fever.','It might be measles because she has a rash and a fever.'),('She had two measles vaccines.','It is unlikely to be measles because she had two vaccines.')]
PAIRS3=dict(m='pairs',phase='STUDY',label="Exercise · Might · can't",min=3,title='Clue → sentence',hint='⚽ Tap a clue. Pass the ball to a student.',ball=True,lvl=1,pairs=_P3A,levels=[{},{'hide':True},{'hide':True,'pairs':_P3B}])
# --- ruling out (audio): "no cough" so "it can't be flu" ---
RULE3=dict(m='choice',phase='STUDY',title='Ruling out',label='Exercise · Ruling out',aud=True,lvl=2,min=3,pt=_PT3,levels=_lv3(
 [_a2('😷','No cough. No runny nose.',"It can't be flu.",'It might be flu.',"It can't be dengue."),_a2('🫄','Her belly is soft. It does not hurt.',"It can't be appendicitis.",'It might be appendicitis.',"It can't be a fever."),_a2('🍱','We ate the same food. Nobody else is sick.',"It can't be food poisoning.",'It might be food poisoning.',"It can't be a friend.")],
 [_a2('😷','She has a fever, but she has no cough.',"It is unlikely to be flu.",'It is probably flu.','It is flu.'),_a2('👁️','Her eyes are not red. They are not watery.','It is unlikely to be measles.','It is probably measles.','It is measles.'),_a2('💉','She had two measles vaccines.','It is unlikely to be measles.','It is probably measles.','It is measles.')],
 [_a2('😷','No cough, so it can not be flu.',"It can't be flu because she has no cough.","It might be flu because she has no cough.","It can't be flu because she has a cough."),_a2('🫄','Her belly does not hurt when I press it.',"It can't be appendicitis because her belly does not hurt.","It might be appendicitis because her belly hurts.","It can't be appendicitis because her belly hurts."),_a2('🌡️','Fever, rash and mosquito bites. No cough.','It is probably dengue because she has a rash and mosquito bites.','It is unlikely to be dengue because she has a rash.',"It can't be dengue because she has a fever.")]))
# --- but / although / so (audio, optional) ---
BAS3=dict(m='choice',phase='STUDY',title='But · although · so',label='Exercise · But · although · so',aud=True,optional=True,lvl=2,min=3,pt=_PT3,levels=_lv3(
 [_a2('🌡️','She has a fever, but she has no cough.','She has a fever. She has no cough.','She has a fever and a cough.','She has no fever and no cough.'),_a2('🔴','She has a rash, but no fever.','She has a rash. She has no fever.','She has a rash and a fever.','She has no rash and no fever.'),_a2('😷','He has a cough, but he has no fever.','He has a cough. He has no fever.','He has a cough and a fever.','He has no cough.')],
 [_a2('🌡️','Although she has a fever, she has no cough.','She has a fever. She has no cough.','She has no fever. She has a cough.','She has a fever and a cough.'),_a2('🦟','She was bitten by mosquitoes, so it might be dengue.','Mosquito bites are a reason for dengue.','Mosquito bites are a reason for flu.','Mosquito bites are not important.'),_a2('🍱','Her friends ate the same food, so it is unlikely to be food poisoning.','Her friends are not sick. So: food poisoning is unlikely.','Her friends are sick. So: food poisoning is likely.','Her friends ate nothing.')],
 [_a2('🌡️','Although she has a high fever, her pulse is only slightly higher than normal.','Fever: high. Pulse: only a little higher.','Fever: low. Pulse: very high.','Fever: high. Pulse: very high.'),_a2('🔴','She has a rash, but not on her face, so measles is unlikely.','The rash is not on her face. So measles is unlikely.','The rash is on her face. So measles is likely.','She has no rash. So measles is likely.'),_a2('🩸','Her platelets are low, so it might be dengue, but we need a blood test.','Low platelets: maybe dengue. A blood test will tell.','Low platelets: sure it is dengue.','Low platelets: nothing to do.')]))
# --- tests: teach + match ---
TEST_T=dict(m='teach',phase='STUDY',label='Teach · Which test?',min=2,optional=True,role='Test → because',pic='🩸',pics=['🩸','🫁','💩','🧬'],lines=['We need a blood test because it would show the virus.','We need a chest X-ray because it would show the lungs.','We need a stool test because it would show food poisoning.','We need a urine test because it would show an infection.'])
TEST_E=dict(m='pairs',phase='STUDY',label='Exercise · Which test?',min=2,optional=True,title='Question → test',hint='Tap the question. Then tap the test.',pairs=[('Is it dengue?','We need a blood test.'),('Is it pneumonia? She has a bad cough.','We need a chest X-ray.'),('Is it food poisoning?','We need a stool test.'),('Is it a kidney infection?','We need a urine test.')])
# --- voice-message chat, L3 content ---
CHAT3=dict(m='chat',phase='STUDY',label='Exercise · Patient chat (voice messages)',min=4,title='Voice messages',window=4,pt='🎧 Listen. Then answer as the nurse.',lines=[
 ('P',dict(say='I have a fever and red spots on my arms. What is wrong with me?')),
 ('N',[_Q('c2','Do you have'),_Q('c3','a cough?',True)],[('c3','a cough?'),('c3','a mosquito?'),('c3','a banana?')]),
 ('P',dict(say='No cough. No runny nose. But my head and my eyes hurt.')),
 ('N',[_Q('c1','It'),_Q('c2',"can't",True),_Q('c2','be'),_Q('c3','flu'),_Q('c4','because',True),_Q('c1','you have no cough.')],[('c2','might'),('c2',"can't"),('c4','because'),('c4','but')]),
 ('P',dict(say='A mosquito bit me a week ago, by the pond.')),
 ('N',[_Q('c1','It'),_Q('c2','might',True),_Q('c2','be'),_Q('c3','dengue'),_Q('c4','because',True),_Q('c1','a mosquito bit you.')],[('c2','might'),('c2',"can't"),('c4','because'),('c4','but')]),
 ('P',dict(say='Is it really dengue? How do you know?')),
 ('N',[_Q('c1','It is'),_Q('c2','probably',True),_Q('c3','dengue,'),_Q('c4','but',True),_Q('c1','we need a blood test.')],[('c2','probably'),('c2','never'),('c4','but'),('c4','so')]),
 ('P',dict(say='Okay. Please do the test. Quickly, please.')),
])
# --- Everybody lies (L3) ---
LIE3=dict(m='choice',phase='ACTIVATE',title='Everybody lies?',label='Everybody lies',aud=True,lvl=2,min=3,pt=_PT3,levels=_lv3(
 [_tq('🌡️','I only feel a little warm.','The thermometer says: 41 °C.','No. She has a very high fever.','Yes. She tells the truth.'),
  _tq('🦟','A mosquito? No, never.','Her friend says: she was bitten many times at the pond.','No. She was bitten.','Yes. She tells the truth.'),
  _tq('😷','I have a terrible cough.','The nurse says: no cough.','No. She has no cough.','Yes. She tells the truth.')],
 [_tq('💓','My heart is fine. Totally normal.','The monitor says: 104 beats per minute. Normal: 60 to 100.','Not really. Her pulse is higher than normal.','Yes. Her pulse is normal.','No. Her pulse is lower than normal.'),
  _tq('🌡️','I have had a fever for two days.','The chart says: fever for three days.','No. It is three days.','Yes. She tells the truth.','No. It is one day.'),
  _tq('🍱','Same lunch as my friends. Nobody else is sick.','Her friends say: we are all fine.','Yes. She tells the truth.','No. Her friends are sick.','No. She ate different food.')],
 [_tq('🩸','My blood is perfect.','The lab says: platelets 95,000. Normal: 150,000 to 450,000.','No. Her platelets are much lower than normal.','Yes. Her blood is normal.','No. Her platelets are higher than normal.'),
  _tq('🔴','The rash is on my face.','The nurse says: the rash is on her arms and chest, not her face.','No. The rash is not on her face.','Yes. The rash is on her face.','No. She has no rash.'),
  _tq('💊','I took paracetamol and the fever never came back.','The nurse says: the fever went down, then came back.','No. The fever came back.','Yes. The fever stayed away.','No. She did not take paracetamol.')]))
# --- toolkit chips ---
_S,_V,_O,_B,_T='s','v','o','b','t'
TOOL3_CHIPS=[
 [[('Does',_V),('anyone',_S),('have',_V),('a voice note',_O),('about …?',_O)],[('Can',_V),('I',_S),('hear',_V),('your voice note?',_O)],[('What',_B),('does',_V),('it',_S),('say',_V),('about …?',_O)]],
 [[('Her temperature',_S),('is',_V),('much higher than normal.',_O)],[('She',_S),('has',_V),('a rash',_O),('on her arms.',_T)],[('Her platelets',_S),('are',_V),('much lower than normal.',_O)]],
 [[('It',_S),('might be',_V),('dengue',_O),('because …',_B)],[('It',_S),("can't be",_V),('flu',_O),('because',_B),('she',_S),('has',_V),('no cough.',_O)],[('It',_S),('is unlikely to be',_V),('measles',_O),('because …',_B)]]]
# --- how the voice-note hunt works ---
_H1=stick(100,395,1.2,'hold')+'<text x="165" y="330" font-size="86">🎧</text><text x="250" y="150" font-size="60" font-family="Outfit,sans-serif" font-weight="800" fill="#9a5cff">×3</text>'
_H3=stick(130,395,1.2,'hold')+'<text x="195" y="330" font-size="86">🎧</text><text x="215" y="190" font-size="40" font-family="Outfit,sans-serif" font-weight="800" fill="#10a98d">Her pulse is 104.</text>'
HUNT3_COMIC=[dict(svg=_H1,cap='Each group has 3 voice notes.'),dict(svg=_FP3,cap='One group asks the class.'),dict(svg=_H3,cap='Listen. Say it in a sentence.'),dict(svg=_P4,cap='Teacher taps. The board fills.')]
HUNT3_COMIC[0]['img']='l4_d4_fix.jpg'; HUNT3_COMIC[1]['img']='l4_d3_ask.jpg'; HUNT3_COMIC[2]['img']='l4_d2_find.jpg'; HUNT3_COMIC[3]['img']='l3_e4_board_fills.jpg'
# --- the 12 voice notes (numbered groups 1-4) ---
_FIX3D=[('A2','🤕','Head, eyes, muscles','Patient','My head hurts… and behind my eyes. My muscles hurt too. Everything aches.','Her head, her eyes and her muscles hurt.'),
 ('A3','😷','Cough','Patient','No. No cough. Not once this week.','She has no cough.'),
 ('A4','🦟','Mosquitoes','Patient','Yes, a lot! In the garden, by the pond… about a week ago.','She was bitten by mosquitoes a week ago.'),
 ('B1','🌡️','Temperature','Nurse','Her temperature is thirty-nine point two. Normal is about thirty-seven.','Her temperature is 39.2 °C. Normal is about 37 °C.'),
 ('B2','💓','Pulse','Nurse','Her pulse is one hundred and four beats a minute. Normal is sixty to one hundred.','Her pulse is 104. Normal is 60 to 100.'),
 ('B3','🩸','Blood test','Lab','Her platelets are ninety-five thousand. Normal is one hundred and fifty to four hundred and fifty thousand. White cells: three thousand one hundred. Normal is four and a half to eleven thousand.','Her platelets and white cells are lower than normal.'),
 ('C1','🔴','Rash','Nurse','She has a red rash on her arms and on her chest. No rash on her face.','She has a rash on her arms and chest, but not on her face.'),
 ('C2','👁️','Eyes','Doctor','Her eyes are not red. They are not watery.','Her eyes are not red or watery.'),
 ('C3','🫄','Belly','Doctor','Her belly is soft. I press here… she says: no pain.','Her belly is soft. It does not hurt.'),
 ('D1','💉','Vaccination','Nurse','Vaccination card… measles vaccine. Two doses.','She had two measles vaccines.'),
 ('D2','🍱','Friend','Friend','We ate the same food at lunch. Nobody else is sick.','Her friends ate the same food. Nobody else is sick.'),
 ('D3','🏘️','Neighbour','Neighbour','Two people on our street had a fever last week.','Two people on her street had a fever last week.')]
_OWN3={'A':'red','B':'blue','C':'green','D':'yellow'}
FIX3=[dict(n=i+1,id=cid,owner=_OWN3[cid[0]],pic=pc,topic=tp,who=wh,voice=v,fact=ft) for i,(cid,pc,tp,wh,v,ft) in enumerate(_FIX3D)]
_BY3={f['id']:f for f in FIX3}
# ---- 18 Nov (Nick): sentences more human and fun, like L4 ----
_V3={'A2':'My head hurts… and behind my eyes. And my muscles! Even my hair hurts.','A3':'No cough. Not even a little one. My cat coughs more than me!','A4':'Mosquitoes? Yes, loads! In the garden, by the pond… about a week ago.',
 'B1':'Her temperature is thirty-nine point two. Normal is about thirty-seven. That is a proper fever.','B2':'Her pulse is one hundred and four beats a minute. Normal is sixty to one hundred. A little fast.',
 'B3':'Lab result. Platelets: ninety-five thousand. Normal is one hundred and fifty to four hundred and fifty thousand. White cells: three thousand one hundred. Normal is four and a half to eleven thousand.',
 'C1':'She has a red rash on her arms and on her chest. But her face? Nothing. Clear.','C2':'Her eyes? Not red. Not watery. They look fine.','C3':'I press her belly here… and here… She says: no pain. She even smiled.',
 'D1':'Vaccination card… measles vaccine. Two doses. Very good!','D2':'We ate the same food at lunch. Nobody else is sick. Not even me!','D3':'Two people on our street had a fever last week. Poor things.'}
for _f in FIX3: _f['voice']=_V3[_f['id']]
NUM3=dict(NUM3,levels=_lv3(
 [_a2('🌡️','Thirty-nine point two! Is that bad, nurse?','39.2 °C','29.2 °C','39.2 beats per minute'),_a2('💓',"My pulse? One hundred and four. My heart is going crazy!",'104 beats per minute','140 beats per minute','104 °C'),_a2('🫁','I breathe eighteen times a minute. I counted. I was bored.','18 breaths per minute','80 breaths per minute','18 °C')],
 [_a2('🩸','The lab says my platelets are ninety-five thousand. The normal range is one hundred and fifty to four hundred and fifty thousand. Is that okay?','Platelets: 95,000 per µL. Normal: 150,000 to 450,000.','Platelets: 9,500 per µL. Normal: 150,000 to 450,000.','Platelets: 95,000 per µL. Normal: 15,000 to 45,000.'),_a2('🌡️','Thirty-eight point one. Normal is thirty-seven… so a bit high?','Her temperature is 38.1 °C. Normal is 37 °C.','Her temperature is 38.1 °C. Normal is 36 °C.','Her temperature is 31.8 °C. Normal is 37 °C.'),_a2('💓','My pulse is forty-eight. Normal is sixty to one hundred. Am I a robot?','Her pulse is 48. Normal is 60 to 100.','Her pulse is 84. Normal is 60 to 100.','Her pulse is 48. Normal is 16 to 100.')],
 [_a2('🩸','My white cells are three thousand one hundred. Normal is four and a half to eleven thousand. They are tiny!','White cells: 3,100 per µL. Normal: 4,500 to 11,000.','White cells: 31,000 per µL. Normal: 4,500 to 11,000.','White cells: 3,100 per µL. Normal: 45,000 to 110,000.'),_a2('🌡️','I feel a little warm. What? Forty-one degrees?!','The thermometer says 41 °C. That is dangerously high.','The thermometer says 14 °C. That is dangerously low.','The thermometer says 41 °C. That is normal.'),_a2('🫁','Twenty-one breaths a minute. Normal is twelve to twenty. Almost normal, no?','Her breathing is 21. It is only slightly higher than normal.','Her breathing is 12. It is lower than normal.','Her breathing is 21. It is normal.')]))
HIST_E=dict(HIST_E,levels=_lv3(
 [dict(pic='🌡️',say='Three days. Three very long days.',q='Which question did the nurse ask?',ans='How long have you had a fever?',opts=['How long have you had a fever?','Where does it hurt?','Do you have a cough?']),
  dict(pic='🤕',say='Behind my eyes. And my muscles. Everything hurts!',q='Which question did the nurse ask?',ans='Where does it hurt?',opts=['Where does it hurt?','How long have you had a fever?','Did a mosquito bite you?']),
  dict(pic='🦟',say='Yes! Loads of bites, by the pond, a week ago.',q='Which question did the nurse ask?',ans='Did a mosquito bite you?',opts=['Did a mosquito bite you?','Do you have a cough?','Where does it hurt?'])],
 [dict(pic='😷',say='No cough. Not even a little one.',q='Which question did the nurse ask?',ans='Do you have a cough?',opts=['Do you have a cough?','Do you have a rash?','Did you have a cough?']),
  dict(pic='🌡️',say='It started on Monday. So… three days.',q='Which question did the nurse ask?',ans='When did the fever start?',opts=['When did the fever start?','Where does the fever start?','Who has a fever?']),
  dict(pic='🍱',say='We all ate the same lunch. Nobody else is sick, thank goodness.',q='Which question did the nurse ask?',ans='Did your friends eat the same food?',opts=['Did your friends eat the same food?','Did you eat the same food?','Do your friends eat food?'])],
 [dict(pic='💊',say='Paracetamol, yesterday. The fever went down… and then it came back.',q='Which question did the nurse ask?',ans='Did you take any medicine?',opts=['Did you take any medicine?','Do you take any medicine?','Did you make any medicine?']),
  dict(pic='🏘️',say='Yes! Two people on my street had a fever last week.',q='Which question did the nurse ask?',ans='Is anyone else sick near you?',opts=['Is anyone else sick near you?','Are you sick near anyone else?','Is anyone sick else you?']),
  dict(pic='💉',say='Two doses, at school. I even kept the card!',q='Which question did the nurse ask?',ans='Have you had the measles vaccine?',opts=['Have you had the measles vaccine?','Do you have the measles vaccine?','Have you got measles?'])]))
CERT_E=dict(CERT_E,levels=_lv3(
 [_a2('🚫',"Appendicitis? No way. Her belly is fine.",'No chance. It is not appendicitis.','Maybe. We do not know.','Yes. It is appendicitis.'),_a2('🤔',"Dengue? Hmm… it might be dengue. I'm not sure yet.",'Maybe. We are not sure yet.','Definitely dengue.','No chance.'),_a2('✅','It is dengue. The test says so.','Yes. We are sure.','Maybe.','No chance.')],
 [_a2('🤏',"Measles? I doubt it. It is unlikely.",'A small chance.','A big chance.','Definitely measles.'),_a2('👍',"Dengue? I'm nearly sure. It is probably dengue.",'A big chance.','A small chance.','No chance.'),_a2('🤔',"It might be flu, it might be dengue. I can't decide!",'Two ideas. Not sure yet.','Only one idea.','No ideas at all.')],
 [_a2('🤏','Flu? Unlikely. She has no cough, you see.','Probably not flu. She has no cough.','Probably flu. She has no cough.','Probably not flu. She has a bad cough.'),_a2('👍',"Dengue, probably! Rash, mosquito bites… it all fits.",'Probably dengue. The clues fit.','Probably not dengue. The clues do not fit.','Definitely not dengue.'),_a2('🚫',"Appendicitis? It can't be. I pressed her belly and she just laughed.",'No. Her belly is fine.','Yes. Her belly hurts.','Maybe. We need an X-ray.')]))
RULE3=dict(RULE3,levels=_lv3(
 [_a2('😷','No cough, no runny nose. Nothing!',"It can't be flu.",'It might be flu.',"It can't be dengue."),_a2('🫄','Her belly is soft. She even asked for lunch!',"It can't be appendicitis.",'It might be appendicitis.',"It can't be a fever."),_a2('🍱','We ate the same food. Nobody else is sick. Not even the cat!',"It can't be food poisoning.",'It might be food poisoning.',"It can't be a friend.")],
 [_a2('😷','She has a fever, but no cough. Strange.',"It is unlikely to be flu.",'It is probably flu.','It is flu.'),_a2('👁️',"Her eyes are fine. Not red, not watery.",'It is unlikely to be measles.','It is probably measles.','It is measles.'),_a2('💉','Two measles vaccines. She even has the card!','It is unlikely to be measles.','It is probably measles.','It is measles.')],
 [_a2('😷','No cough… so it can not be flu, right?',"It can't be flu because she has no cough.","It might be flu because she has no cough.","It can't be flu because she has a cough."),_a2('🫄','I pressed her belly. She just smiled.',"It can't be appendicitis because her belly does not hurt.","It might be appendicitis because her belly hurts.","It can't be appendicitis because her belly hurts."),_a2('🌡️','Fever, rash, mosquito bites. No cough. Hmm, hmm, hmm…','It is probably dengue because she has a rash and mosquito bites.','It is unlikely to be dengue because she has a rash.',"It can't be dengue because she has a fever.")]))
BAS3=dict(BAS3,levels=_lv3(
 [_a2('🌡️','I have a fever, but no cough. Weird, right?','She has a fever. She has no cough.','She has a fever and a cough.','She has no fever and no cough.'),_a2('🔴','A rash, but no fever. Strange!','She has a rash. She has no fever.','She has a rash and a fever.','She has no rash and no fever.'),_a2('😷','He coughs all day, but he has no fever.','He has a cough. He has no fever.','He has a cough and a fever.','He has no cough.')],
 [_a2('🤒','Although I feel awful, I still want to go to class!','She feels awful. She wants to go to class.','She feels great. She wants to go to class.','She feels awful. She stays in bed.'),_a2('🦟',"Mosquito bites, so it might be dengue.",'The mosquito bites are a clue for dengue.','The mosquito bites are a clue for flu.','The mosquito bites are not important.'),_a2('🍱',"My friends ate the same food, so it is probably not food poisoning.",'Her friends are fine. So it is probably not food poisoning.','Her friends are sick. So it is probably food poisoning.','Her friends ate nothing.')],
 [_a2('🌡️','Although my fever is high, my pulse is only a little fast.','Fever: high. Pulse: only a little fast.','Fever: low. Pulse: very fast.','Fever: high. Pulse: very fast.'),_a2('🔴',"I have a rash, but not on my face, so measles is unlikely.",'The rash is not on her face. So measles is unlikely.','The rash is on her face. So measles is likely.','She has no rash. So measles is likely.'),_a2('🩸','My platelets are low, so maybe dengue. But we need a blood test first.','Low platelets: maybe dengue. A blood test will tell.','Low platelets: definitely dengue.','Low platelets: nothing to do.')]))
TEST_T=dict(TEST_T,lines=['Is it dengue? We need a blood test, because it would show the virus.','Is it pneumonia? We need a chest X-ray, because it would show the lungs.','Is it food poisoning? We need a stool test, because it would show the germs.','Is it a kidney infection? We need a urine test, because it would show the infection.'])
CHAT3=dict(CHAT3,lines=[
 ('P',dict(say='I have a fever and red spots on my arms. What is wrong with me?')),
 ('N',[_Q('c2','Do you have'),_Q('c3','a cough?',True)],[('c3','a cough?'),('c3','a mosquito?'),('c3','a banana?')]),
 ('P',dict(say='No cough. Not even a little one. My cat coughs more than me!')),
 ('N',[_Q('c1','It'),_Q('c2',"can't",True),_Q('c2','be'),_Q('c3','flu'),_Q('c4','because',True),_Q('c1','you have no cough.')],[('c2','might'),('c2',"can't"),('c4','because'),('c4','but')]),
 ('P',dict(say='A mosquito bit me a week ago, by the pond. A big one!')),
 ('N',[_Q('c1','It'),_Q('c2','might',True),_Q('c2','be'),_Q('c3','dengue'),_Q('c4','because',True),_Q('c1','a mosquito bit you.')],[('c2','might'),('c2',"can't"),('c4','because'),('c4','but')]),
 ('P',dict(say='Dengue?! How do you know? Are you a doctor?')),
 ('N',[_Q('c1','It is'),_Q('c2','probably',True),_Q('c3','dengue,'),_Q('c4','but',True),_Q('c1','we need a blood test.')],[('c2','probably'),('c2','never'),('c4','but'),('c4','so')]),
 ('P',dict(say='Okay, do the test. But please be quick. My cat is waiting!')),
])
LIE3=dict(LIE3,levels=_lv3(
 [_tq('🌡️',"I only feel a little warm. Really!",'The thermometer says: 41 °C.','No. She has a very high fever.','Yes. She tells the truth.'),
  _tq('🦟','A mosquito? Me? Never! I love nature.','Her friend says: she was bitten many times at the pond.','No. She was bitten.','Yes. She tells the truth.'),
  _tq('😷','I have a terrible cough. Cough, cough!','The nurse says: no cough.','No. She has no cough.','Yes. She tells the truth.')],
 [_tq('💓','My heart is fine. Totally normal. Stop looking at the monitor!','The monitor says: 104 beats per minute. Normal: 60 to 100.','Not really. Her pulse is higher than normal.','Yes. Her pulse is normal.','No. Her pulse is lower than normal.'),
  _tq('🌡️','I have had a fever for two days. Okay, maybe two and a half.','The chart says: fever for three days.','No. It is three days.','Yes. She tells the truth.','No. It is one day.'),
  _tq('🍱','Same lunch as my friends. Nobody else is sick.','Her friends say: we are all fine.','Yes. She tells the truth.','No. Her friends are sick.','No. She ate different food.')],
 [_tq('🩸','My blood is perfect. I eat vegetables!','The lab says: platelets 95,000. Normal: 150,000 to 450,000.','No. Her platelets are much lower than normal.','Yes. Her blood is normal.','No. Her platelets are higher than normal.'),
  _tq('🔴','The rash is on my face. Everywhere!','The nurse says: the rash is on her arms and chest, not her face.','No. The rash is not on her face.','Yes. The rash is on her face.','No. She has no rash.'),
  _tq('💊','I took paracetamol and the fever never came back. Never!','The nurse says: the fever went down, then came back.','No. The fever came back.','Yes. The fever stayed away.','No. She did not take paracetamol.')]))

_L3=[]
for d in L3:
    lb=d.get('label'); m=d['m']
    if lb=='Eyes closed. Louder.': d=dict(next(x for x in L4 if x['m']=='vol_ladder'))
    if m=='today': d=dict(d,rows=[[('c4','Ask'),('c3','the right question')],[('c1','Read'),('c3','the numbers')],[('c2','might'),('c4',"can't"),('c3','because')],[('c2','probably'),('c4','unlikely')]])
    if lb=='Teach · Symptoms': _L3+= [d]; continue
    if lb=='Teach · Symptom sentences': _L3+= [d,MORE3_W,MORE3_S,dict(m='choice',phase='STUDY',title='Symptoms',label='Exercise · Symptoms',aud=True,min=3,lvl=3,pt=_PT3,levels=lv(SYM3))]; continue
    if lb in ('Exercise · Symptoms','Teach · Higher or lower','Teach · The dial','Exercise · Higher or lower?','Teach · Might, can\'t, because',"Exercise · Might · can't · because",'Teach · Ask the patient','Exercise · Ask the patient (1)','Exercise · Ask the patient (2)'):
        if lb=='Teach · The dial': _L3+=[dict(m='dial',phase='STUDY',label='Exercise · Higher or lower?',min=4,title='How much higher? How much lower?',aud=True,items=DIAL3,pt=_PT3),NUM3]
        elif lb=="Teach · Might, can't, because": _L3+=[HIST_T,HIST_E,CERT_T,CERT_E,MIGHT3_T,PAIRS3,RULE3,BAS3,TEST_T,TEST_E,CHAT3]
        continue
    if lb=='Your toolkit': d=dict(d,note=None,bubbles=False,chips=TOOL3_CHIPS,title='Your hunt toolkit')
    if lb=='How the hunt works': d=dict(d,label='How the voice-note hunt works',title='How the voice-note hunt works',panels=HUNT3_COMIC)
    if lb in ('Taboo for nurses','Plan B (teacher)','Tell the doctor (spoken)'): continue
    if lb=='Recap': d=dict(d,rows=[([('c1','She'),('c2','has'),('c3','chills and a rash.')],'symptoms'),([('c1','Her pulse'),('c2','is'),('c3','higher than normal.')],'than'),([('c1','It'),('c2','is probably'),('c3','dengue.')],'probably'),([('c1','It'),('c2',"can't be"),('c3','flu because she has no cough.')],'why'),([('c2','Have'),('c1','you'),('c3','had a fever?')],'ask')])
    if lb=='Case board · Find the illness':
        d=dict(d,frames=['Does anyone have a voice note about …?','Yes, we do. Come and listen.','Is that a clue for flu?'],unit='clues found',clues=[dict(c,pic=_BY3[c['id']]['pic'],kind=None,topic=_BY3[c['id']]['topic'],text=_BY3[c['id']]['fact']) for c in d['clues']])
    _L3.append(d)
    if lb=='Your toolkit' : pass
_ix3={d.get('label'):i for i,d in enumerate(_L3)}
# Everybody lies goes before the toolkit (warm-up for the hunt)
_L3.insert(_ix3['Your toolkit'],LIE3)
_i3=[d.get('label') for d in _L3].index('How the voice-note hunt works')
import base64 as _b3
_qd3=lambda n:'data:image/png;base64,'+_b3.b64encode(open(f'/home/claude/lesson-a/lessons-3-4/source-art/print/qr3_{n}.png','rb').read()).decode()
_L3.insert(_i3+1,dict(m='qr_groups',phase='ACTIVATE',label='Group QR codes',title='Scan your group',min=1,qrs=[_qd3(n) for n in '1234'],cols=['#ff5a6a','#2a8cf0','#19b38a','#f2a900']))
# Taboo: in the deck, fixed order, L3 words (same module and art as L4)
TABOO3=dict(TABOO4,items=[dict(w='fever',e='🌡️',no=['hot','temperature','thermometer','high']),dict(w='rash',e='🔴',no=['red','skin','spots','itchy']),dict(w='cough',e='😷',no=['throat','cold','sneeze','loud']),dict(w='headache',e='🤕',no=['head','pain','hurt','tablet']),dict(w='mosquito',e='🦟',no=['bite','insect','fly','blood']),dict(w='pulse',e='💓',no=['heart','beat','wrist','minute']),dict(w='vaccine',e='💉',no=['needle','injection','protect','arm']),dict(w='chills',e='🥶',no=['cold','shiver','freeze','shake'])])
_j3=[d.get('label') for d in _L3].index('Case board · Find the illness')
_L3.insert(_j3+1,TABOO3)
# end matter: teacher backup page of all 12 voice notes after Thank you
def _fixclip3(n):
    f='/home/claude/lesson-a/lessons-3-4/source-audio/l3_hunt/L3_%02d.mp3'%n
    return 'data:audio/mpeg;base64,'+_b3.b64encode(open(f,'rb').read()).decode() if _o3.path.exists(f) else ''
_gi3=lambda o:[dict(pic=f['pic'],clip=_fixclip3(f['n']),say=f['voice'].replace('"','&quot;')) for f in FIX3 if f['owner']==o]
_ct=next(i for i,d in enumerate(_L3) if d.get('label')=='Thank you')
_L3.insert(_ct+1,dict(m='audio_all',phase='ACTIVATE',label='Teacher backup · all group voice notes',optional=True,min=1,title='All voice notes',groups=[_gi3(o) for o in ('red','blue','green','yellow')],cols=['#ff5a6a','#2a8cf0','#19b38a','#f2a900']))
L3=_L3
L3=[d for d in L3 if d['m']!='boss']
_bi=[d.get('label') for d in L3].index('Thank you')+1
L3.insert(_bi,dict(m='boss',phase='ACTIVATE',label='Boss question (just for fun)',optional=True,min=3,**K.L3_BOSS,sec=90))
# timing: extras are optional so the core stays near the target (Nick decides what to run)
_OPT3={'Exercise · Listen and tick the numbers':3,'Exercise · How sure?':2}
_MIN3={'Teach · How sure?':1,'Teach · Ask the patient':1,'The room of clues':2}
L3=[dict(d,optional=True,min=_OPT3[d['label']]) if d.get('label') in _OPT3 else dict(d,min=_MIN3[d['label']]) if d.get('label') in _MIN3 else d for d in L3]
# ---- 18 Nov: L3 art placed (Gemini batch 1), slots without art keep their emoji ----
ARTMAP3={'🍱':'l3_f1_shared_lunch.jpg','👁️':'l3_f2_eyes_fine.jpg','💉':'l3_f3_vaccine_two.jpg','🤒':'l3_b1_fever.jpg','🌡️':'l3_b1_fever.jpg','🤕':'l3_b2_headache.jpg','😷':'l3_b3_cough.jpg','🔴':'l3_b4_rash.jpg','🥶':'l3_b5_chills.jpg','🧴':'l3_b6_itchy.jpg','🫨':'l3_b7_stiff.jpg','🍚':'l3_b8_no_appetite.jpg','🦟':'l3_c1_mosquito_bite.jpg','🩸':'l3_c2_blood_test.jpg','🫁':'l3_c3_chest_xray.jpg','💩':'l3_c4_stool_test.jpg','🧬':'l3_c5_urine_test.jpg'}
_ART3=('Teach · Symptoms','Teach · Symptom sentences','Teach · More symptoms','Teach · More patient sentences','Exercise · Symptoms','Teach · Ask the patient','Teach · Which test?','Exercise · Hear the answer, pick the question','Exercise · Ruling out','Exercise · But · although · so')
_s=700/1116.0
def _rs(dx,dy,t): return dict(e='',x=int(243+dx*_s-56),y=int(dy*_s-56),t=t)
ROOM3=[_rs(255,590,'A thermometer: 39.2 °C.'),_rs(395,690,'Paracetamol. Two tablets yesterday.'),_rs(1255,230,'A calendar. Days are crossed out.'),_rs(1740,430,'Her lunch. She did not eat much.'),_rs(1310,545,'A sleepy cat.'),_rs(700,1015,'A box of tissues. Used.'),_rs(640,490,'She looks hot and tired.')]
_n3=[]
for d in L3:
    lb=d.get('label')
    if lb in _ART3: d=_fm(d,ARTMAP3)
    if lb=='Everybody lies': d=_fm(d,{k_:v_ for k_,v_ in ARTMAP3.items() if k_ in ('🦟','😷','🔴')})
    if d['m']=='cover' and _ex('l3_a1_cover_stethoscope.jpg'): d=dict(d,cards=[dict(d['cards'][0],pic='l3_a1_cover_stethoscope.jpg'),dict(d['cards'][1],pic='l3_a2_cover_thermometer.jpg')])
    if d['m']=='room' and _ex('l3_a0_room.jpg'): d=dict(d,img='l3_a0_room.jpg',spots=ROOM3)
    _n3.append(d)
L3=_n3
# 18 Nov (Nick): cut p11 (numbers), p15 (How sure? exercise) and Everybody lies from L3
L3=[d for d in L3 if d.get('label') not in ('Exercise · Listen and tick the numbers','Exercise · How sure?','Everybody lies')]
# dial art + no-numbers flag for temperature (as L4)
for d in L3:
    if d['m']=='dial' and d.get('label')=='Exercise · Higher or lower?':
        _DA3={('💓','Pulse: 104 beats per minute'):'l4_i1_pulse_slightly_high.jpg',('💓','Pulse: 130 beats per minute'):'l4_c4_racing_heart.jpg',('🌡️','Temperature: 41 °C'):'l4_h3_fever_high.jpg',('🌡️','Temperature: 39.2 °C'):'l3_d1_temp_39.jpg',('🌡️','Temperature: 32 °C'):'l3_d5_temp_low.jpg'}
        for it in d['items']:
            if it['s'].startswith('Her temperature') or it['s'].startswith('Her breathing'): it['nt']=1
            a=_DA3.get((it['e'],it['now']))
            if not a: a={('🩸','Platelets: 95,000 per µL'):'l3_d4_platelets_low.jpg',('🫁','Breathing: 16 breaths per minute'):'l3_d2_breathing_normal.jpg',('🫁','Breathing: 40 breaths per minute'):'l3_d3_breathing_fast.jpg'}.get((it['e'],it['now']))
            if a: it['art']=ART+a

# 18 Nov (Nick): no instruction lines at the top of the pages (L3 and L4)
for _d in L3+L4: _d.pop('pt',None)

def _inject_audio(html_path,adir):
    """Recorded clips (ElevenLabs) keyed by exact spoken text. speechSynthesis.speak is wrapped: a matching line plays the clip,
    anything else falls back to the browser voice. Nothing in the slide data changes."""
    import json as _j,base64 as _b
    man=_j.load(open(adir/'manifest.json',encoding='utf-8'))
    M={' '.join(m['text'].split()):'data:audio/mpeg;base64,'+_b.b64encode(open(adir/m['file'],'rb').read()).decode() for m in man}
    js=("<script>(function(){var M="+_j.dumps(M,ensure_ascii=False)+";var ss=window.speechSynthesis;if(!ss)return;var os=ss.speak.bind(ss),oc=ss.cancel.bind(ss),cur=null;"
        "function nz(t){return (t||'').replace(/\\s+/g,' ').trim()}"
        "ss.speak=function(u){var src=M[nz(u.text)];if(!src)return os(u);try{if(cur){cur.pause();cur=null}var a=new Audio(src);cur=a;a.onended=function(){if(cur===a)cur=null;if(u.onend)u.onend({})};a.onerror=function(){os(u)};var p=a.play();if(p&&p.catch)p.catch(function(){os(u)})}catch(e){os(u)}};"
        "ss.cancel=function(){if(cur){cur.pause();cur=null}oc()};})();</script>")
    h=open(html_path,encoding='utf-8').read(); i=h.rindex('</body>')
    open(html_path,'w',encoding='utf-8').write(h[:i]+js+h[i:])
    print('audio clips embedded:',len(M))

if __name__=='__main__':
    out=HERE.parent.parent/'lessons-3-4'
    print(build_interactive(L3,str(out/'lesson3_v2.html'),title='SkillsXLab · Lesson 3 · Which illness?'))
    print(build_interactive(L4,str(out/'lesson4_v2.html'),title='SkillsXLab · Lesson 4 · The Impossible Week'))
    _inject_audio(out/'lesson4_v2.html',out/'source-audio'/'l4_pages')
    if (out/'source-audio'/'l3_pages'/'manifest.json').exists(): _inject_audio(out/'lesson3_v2.html',out/'source-audio'/'l3_pages')
    for n,t in ((4,TABOO4),):
        print(build_interactive([dict(t,label='Taboo for nurses',optional=False)],str(out/f'taboo{n}.html'),title=f'SkillsXLab · Taboo for nurses · Lesson {n}'))
