"""Lessons 3 and 4, rebuilt from the reviewed library modules (L1-2 look). Build: python3 lessons/lessons34.py"""
import sys, pathlib
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent)); sys.path.insert(0,str(HERE.parent.parent/'lessons-3-4'/'src')); sys.path.insert(0,str(HERE))
import content as K
from sxl.interactive import build_interactive
import modules_gallery2 as G2, modules_gallery3 as G3
from sxl.modules.clue import stick, bubble_svg
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
L4SAY={'R1':'She says: two cups a day. The café card says: eight cups a day.','R2':'She sleeps three hours most nights. Normal is seven or more.','R3':'Her pulse is 108 to 112. Normal is 60 to 100.','B1':'She has no vomiting and no diarrhoea.','B2':'She studies until 2 am every night, for two weeks.','B3':'She has a headache most afternoons. It is 3 out of 10: mild.','G1':'Her hands shake for 30 minutes after every coffee.','G2':'She never coughs. No cough all week.','G3':'She cries a little when people talk about exams. She is quite worried.','Y1':'She never had this before the exams. It started two weeks ago.','Y2':'On Sunday she drank no coffee. She slept nine hours and felt much better.','Y3':'She ate lunch with three friends. Her friends are fine.'}
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
  _q('🥵','What does the nurse write?','He has a very high fever.','He has a low fever.','He have a very high fever.','He has fever very high.',say='I only feel a little warm. (Thermometer: 41 °C)')]]
U_PL='×10⁹/L'
HL=dict(bronze=[
  _q('🌡️','The normal temperature is 37 °C. Her temperature is 39.2 °C. Her temperature is ___ than normal.','higher','lower'),
  _q('🩸',f'Normal platelets: 150,000 to 450,000 per µL. Her platelets: 95,000 per µL. Her platelets are ___ than normal.','lower','higher'),
  _q('🫁','Normal breathing: 12 to 20 breaths per minute. Her breathing: 18 breaths per minute. Her breathing is ___.','normal','higher','lower'),
  _q('💓','Normal pulse: 60 to 100 beats per minute. His pulse: 48 beats per minute. His pulse is ___ than normal.','lower','higher')],
 silver=[
  _q('🌡️','Normal temperature: 37 °C. Her temperature: 39.2 °C.','Her temperature is much higher than normal.','Her temperature is slightly higher than normal.','Her temperature is lower than normal.'),
  _q('💓','Normal pulse: 60 to 100 beats per minute. Her pulse: 104 beats per minute.','Her pulse is slightly higher than normal.','Her pulse is much lower than normal.','Her pulse is normal.'),
  _q('🩸',f'Normal white cells: 4,500 to 11,000 per µL. Her white cells: 3,100 per µL.','Her white cells are lower than normal.','Her white cells are much higher than normal.','Her white cells are normal.'),
  _q('🌡️','Normal temperature: 37 °C. His temperature: 38.1 °C.','His temperature is slightly higher than normal. It is a mild fever.','His temperature is much higher than normal.','His temperature is lower than normal.')],
 gold=[
  _q('🥵','A patient says "I feel a little warm." The thermometer says 41 °C. Normal is 37 °C.','His temperature is dangerously higher than normal. It is not a little warm!','His temperature is slightly higher than normal.','His temperature is much lower than normal.','His temperature is normal.'),
  _q('🩸',f'Platelets: 95,000 per µL. Normal: 150,000 to 450,000 per µL.','Her platelets are much lower than the normal range.','Her platelets are much more low than normal.','Her platelets are within the normal range.','Her platelets is lower than normal.'),
  _q('🫁','Breathing: 18 breaths per minute. Normal: 12 to 20 breaths per minute.','Her breathing is within the normal range.','Her breathing is higher than the normal range.','Her breathing is lower than the normal range.','Her breathing is normal than.'),
  _q('💓','A sleeping marathon runner: 48 beats per minute. Normal for most adults: 60 to 100.','His pulse is lower than the normal range, but he is very fit.','His pulse is much higher than normal.','His pulse is normal.','His pulse are lower than normal.')])
def _d(e,now,normal,s_,z): return dict(e=e,now=now,normal=normal,s=s_,z=z)
DIAL_DEMO=[_d('💓','Pulse: 104 beats per minute','60 to 100 beats per minute','Her pulse is',4),
 _d('🌡️','Temperature: 39.2 °C','about 37 °C','Her temperature is',5),
 _d('🌡️','Temperature: 41 °C','about 37 °C','His temperature is',6),
 _d('🫁','Breathing: 16 breaths per minute','12 to 20 breaths per minute','Her breathing is',3)]
DIAL_LV=[
 [_d('💓','Pulse: 104 beats per minute','60 to 100 beats per minute','Her pulse is',4),_d('🌡️','Temperature: 41 °C','about 37 °C','His temperature is',6),_d('🫁','Breathing: 16 breaths per minute','12 to 20 breaths per minute','Her breathing is',3),_d('💓','Pulse: 56 beats per minute','60 to 100 beats per minute','His pulse is',2)],
 [_d('🌡️','Temperature: 39.2 °C','about 37 °C','Her temperature is',5),_d('🫁','Breathing: 21 breaths per minute','12 to 20 breaths per minute','His breathing is',4),_d('🩸',f'Platelets: 95,000 per µL',f'150,000 to 450,000 per µL','Her platelets are',1),_d('💓','Pulse: 130 beats per minute','60 to 100 beats per minute','Her pulse is',5)],
 [_d('🌡️','Temperature: 32 °C','about 37 °C','His temperature is',0),_d('💓','Pulse: 42 beats per minute','60 to 100 beats per minute','His pulse is',1),_d('🩸',f'Platelets: 20,000 per µL',f'150,000 to 450,000 per µL','Her platelets are',0),_d('🫁','Breathing: 40 breaths per minute','12 to 20 breaths per minute','Her breathing is',6)]]
L3=[
 dict(m='cover',label='Cover',tag='NURSING ENGLISH',title='Lesson <span class="grad">3</span>',phases=['Engage','Study','Activate'],active=0,cards=[dict(pic='🩺',x=1010,y=150,w=330,h=430,r=-7),dict(pic='🌡️',x=1380,y=330,w=330,h=430,r=6)]),
 dict(m='vol_ladder',phase='ENGAGE',label='Eyes closed. Louder.',min=3,title='Eyes closed. Louder.',rungs=['Bello!','Banana!','Poopaye!','Tulaliloo ti amo!','KAMPAI!'],side='Everyone, eyes closed, at the same time. Whisper first. Each word is louder.'),
 dict(m='predict',phase='ENGAGE',label='Meet the patient',min=3,title='Meet the patient',cap=False,items=[dict(frames=[dict(e='🧍‍♀️',c='She walks in. She looks hot.'),dict(e='🌡️',c='The nurse takes her temperature.'),dict(e='😟',c='The nurse looks worried.')],q='❓ What is wrong with her?')]),
 dict(m='today',phase='STUDY',label='Today',min=1,emoji='stethoscope',title='Detective nurses',role='Today we are',rows=[[('c4','Ask'),('c3','the right question')],[('c1','Read'),('c3','the numbers')],[('c2','might'),('c4',"can't"),('c3','because')]]),
 dict(m='teach',phase='STUDY',label='Teach · Symptoms',min=2,role='Four symptoms',words=[('🤒','fever'),('🤕','headache'),('😷','cough'),('🔴','rash')]),
 dict(m='teach',phase='STUDY',label='Teach · Symptom sentences',min=2,role='Listen to the patient',pic='🤒',tts=True,hint='Tap a line. Listen to the patient. Then say what the nurse writes.',lines=[('She has a fever.','Ohhh… why is it so hot in here? Is the air-con broken?'),('He has a headache.','My head… boom, boom, boom. Like a drum!'),('He has a cough.','Cough, cough… sorry… I sound like a goat!'),('She has a rash on her arm.','Look at my arm! Red spots! Am I turning into a tomato?')]),
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
 dict(m='qr_card',phase='ACTIVATE',label='Taboo rules',min=2,title='Taboo for nurses',rules=['Groups of 4. One person describes.','Only the describer looks at the phone.','Say the word <u>without</u> the ✖ words.','Words only. 🚫 No miming. 🚫 No drawing. 🚫 No pointing.'],qr='data:image/png;base64,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',url='redskin106.github.io/lesson-a/lessons-3-4/taboo3.html',caption='Scan: describer only'),
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
 _d('🌡️','Temperature: 41 °C','about 37 °C','His temperature is',6),_d('🫁','Breathing: 16 breaths per minute','12 to 20 breaths per minute','Her breathing is',3),
 _d('💓','Pulse: 56 beats per minute','60 to 100 beats per minute','His pulse is',2),_d('🩸',f'Platelets: 95,000 per µL',f'150,000 to 450,000 per µL','Her platelets are',1)]
CUT3={'Teach · How much?','Exercise · The dial','Extra · Name the illness','Extra · What is wrong with this chart?','Listen and fix (handover)','Taboo for nurses (demo / class version)'}
_new=[]
for d in L3:
    lb=d.get('label')
    if lb in CUT3: continue
    if lb=='Meet the patient': d=dict(m='room',phase='ENGAGE',label='The room of clues',min=3,title='The room of clues',spots=ROOM_SPOTS)
    elif lb=='Eyes closed. Louder.': d=dict(d,min=2)
    elif lb=='Teach · Symptom sentences':
        d=dict(d,role='Listen to the patient',lines=[('She has a fever.','Ohhh… why is it so hot in here? Is the air-con broken?'),('He has a headache.','My head… boom, boom, boom. Like a drum!'),('He has a cough.','Cough, cough… sorry… I sound like a goat!'),('She has a rash on her arm.','Look at my arm! Red spots! Am I turning into a tomato?')])
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
 dict(m='cover',label='Cover',tag='NURSING ENGLISH',title='Lesson <span class="grad">4</span>',phases=['Engage','Study','Activate'],active=0,cards=[dict(pic='📅',x=1010,y=150,w=330,h=430,r=-7),dict(pic='☕',x=1380,y=330,w=330,h=430,r=6)]),
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
 dict(m='taboo',phase='ACTIVATE',label='Extra · Taboo (fun)',optional=True,min=4,items=[dict(w='coffee',e='☕',no=['cup','drink','morning','caffeine']),dict(w='insomnia',e='🌙',no=['sleep','night','cannot','bed']),dict(w='pulse',e='💓',no=['heart','beat','wrist','minute']),dict(w='headache',e='🤕',no=['head','pain','hurt','tablet'])],lvl=1,levels=[dict(limit=2),dict(limit=3,secs=60),dict(limit=4,secs=45)]),
 dict(m='recap',phase='RECAP',label='Recap',min=2,rows=[([('c1','She'),('c2','has felt'),('c3','tired'),('c4','for two weeks.')],'for'),([('c1','Her pulse'),('c2','is'),('c3','faster than normal.')],'than'),([('c1','She'),('c2','drinks'),('c3','the most coffee')],'the most'),([('c1','You'),('c2','should'),('c3','sleep more.')],'advice')],emoji='sleeping_face'),
 dict(m='closing',phase='EXIT',label='Thank you',min=1,stack=True,line1='Thank',line2='you!',sub='See you next time.',emoji='handshake'),
]

# ---- L4 Activate: Fix the ward (night nurse handover with 12 mistakes, audio voice notes) ----
_FIXD=[
 ('red','🌡️','Temperature','Temperature: 73 °C','Temp 73 °C','Nurse','Her temperature is thirty-six point eight. Normal. Seventy-three? That was the coffee!',['Her temperature is normal.','Her temperature is very high.','Her temperature is very low.'],{'flu':'against'}),
 ('blue','☕','Coffee','Drinks two cups a day','2 cups a day','Barista','Eight cups a day. Every day. I know her order!',['She drinks eight cups every day.','She drinks two cups every day.','She never drinks coffee.'],{'coffee':'for'}),
 ('green','🛏️','Sleep','Sleeps nine hours','Sleeps 9 hours','Smartwatch','Sleep last night: three hours.',['She sleeps three hours. That is less than normal.','She sleeps nine hours. That is more than normal.','She sleeps seven hours. That is normal.'],{'coffee':'for','stress':'for'}),
 ('yellow','💓','Pulse','Pulse 56: lower than normal','Pulse 56','Nurse','Her pulse is one hundred and ten.',['Her pulse is 110. It is higher than normal.','Her pulse is 56. It is lower than normal.','Her pulse is 80. It is normal.'],{'coffee':'for','stress':'for'}),
 ('red','🤕','Headache','Headache: 9 out of 10','Headache 9/10','Patient','My headache is only a little. Three out of ten.',['Her headache is 3 out of 10. It is mild.','Her headache is 9 out of 10. It is severe.','Her headache is 5 out of 10. It is moderate.'],{}),
 ('blue','🗓️','Start','It started yesterday','Started yesterday','Friend','She has felt like this since the exams started. About two weeks.',['It started two weeks ago.','It started yesterday.','It started two years ago.'],{'stress':'for','coffee':'for'}),
 ('green','😷','Cough','Coughs every night','Coughs every night','Patient','I never cough. Not once.',['She never coughs.','She coughs every night.','She coughs twice a week.'],{'flu':'against'}),
 ('yellow','🤢','Stomach','Vomiting and diarrhoea','Vomiting','Friend','We ate the same lunch. Nobody else is sick.',['Nobody else is sick.','Everybody is sick.','She has vomiting and diarrhoea.'],{'food':'against'}),
 ('red','💊','Plan','Plan: two strong coffees','Plan: 2 strong coffees','Doctor','No more coffee suddenly. She should cut down slowly.',['She should cut down coffee slowly.','She should drink two strong coffees.','She should stop coffee today.'],{'coffee':'for'}),
 ('blue','💔','Cause','Cause: broken heart','Broken heart','Patient','Nobody broke my heart! My phone just buzzes with exam messages.',["It can't be a broken heart. It is her phone.",'It is a broken heart.','It is flu.'],{'heart':'against'}),
 ('green','🌞','Sunday','Worse on Sunday','Worse on Sunday','Nurse','On Sunday she drank no coffee. She slept nine hours and felt much better.',['She felt much better on Sunday.','She felt worse on Sunday.','She felt the same on Sunday.'],{'coffee':'for'}),
 ('yellow','📚','Exams','One exam a week','1 exam a week','Teacher','Three exams in four days!',['She has three exams in four days.','She has one exam a week.','She has no exams.'],{'stress':'for'})]
FIX=[dict(n=i+1,owner=o,pic=pc,topic=tp,wrong=w,short=sh,who=who,voice=v,fix=op[0],opts=op,fx=fx) for i,(o,pc,tp,w,sh,who,v,op,fx) in enumerate(_FIXD)]
FIX_CLUES=[dict(id=f'M{f["n"]}',team=f['owner'],r=1,topic=f['topic'],pic=f['pic'],short=f['short'],text=f['fix'],fx=f['fx']) for f in FIX]
_FP=stick(110,395,1.2,'down')+'<text x="190" y="340" font-size="64">☕</text><text x="215" y="260" font-size="50">🌡️</text><text x="190" y="170" font-size="40" font-family="Outfit,sans-serif" font-weight="800" fill="#e0304a">73 °C!</text><text x="40" y="110" font-size="60">💤</text>'
_FP2=stick(120,395,1.2,'hold')+'<text x="190" y="360" font-size="80">📝</text><text x="195" y="300" font-size="60" fill="#e0304a">❌</text>'
_FP3=stick(90,395,1.15,'up')+stick(310,395,1.15,'point')+bubble_svg(20,16,330,100,'Can I hear your\nvoice note?',fs=26,tx=120)
_FP4=stick(130,395,1.2,'hold')+'<text x="195" y="330" font-size="86">🎧</text><text x="255" y="190" font-size="110" fill="#2bd9b6" font-family="Outfit,sans-serif" font-weight="800">✔</text>'
FIX_COMIC=[dict(svg=_FP,cap='The night nurse made mistakes.'),dict(svg=_FP2,cap='Find the mistakes on your page.'),dict(svg=_FP3,cap='Ask another group.'),dict(svg=_FP4,cap='Listen. Choose the fix. Say it.')]

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
_n4=[]
for d in L4:
    lb=d.get('label')
    if lb=='Eyes closed. How bad?': d=dict(d,min=2,rungs=['Bello!','Banana!','Poopaye!','Tulaliloo ti amo!','KAMPAI!'],side='Everyone, eyes closed, at the same time. Whisper first. Each word is louder.')
    elif lb=='The impossible day': d=dict(m='comic',phase='ENGAGE',label='The impossible night',min=3,title='The impossible night',panels=COMIC4,y=230,h=470)
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
        {'t':'⚖️ Argue','c':'rose','l':['It might be the coffee because …',"It can't be a broken heart because …","It can't be flu because she has no cough."],'fs':38}],note='Ask with a question. Answer in a full sentence.')
    elif lb=='How the hunt works': d=dict(d,label='How Fix the ward works',title='How Fix the ward works',panels=FIX_COMIC)
    elif lb=='Case board · Find the reason': d=dict(d,reveal=d['reveal']+'<br>🌙 The night nurse wrote a chart just like her own: eight coffees, three hours of sleep!',title='Fix the ward',label='Case board · Fix the ward',clues=FIX_CLUES,unit='mistakes fixed',fix=True,min=11,frames=['Can I hear your voice note about …?','What does it say about …?','Is that a mistake?'])
    elif lb=='Boss question (just for fun)': _n4.append(PLANB4); d=dict(d)
    elif lb=='"Doctor, I\'m too busy."': d=dict(d,min=6)
    _n4.append(d)
L4=_n4
TABOO4=[d for d in L4 if d['m']=='taboo'][0]
if __name__=='__main__':
    out=HERE.parent.parent/'lessons-3-4'
    print(build_interactive(L3,str(out/'lesson3_v2.html'),title='SkillsXLab · Lesson 3 · Which illness?'))
    print(build_interactive(L4,str(out/'lesson4_v2.html'),title='SkillsXLab · Lesson 4 · The Impossible Week'))
    for n,t in ((3,TABOO3),(4,TABOO4)):
        print(build_interactive([dict(t,label='Taboo for nurses',optional=False)],str(out/f'taboo{n}.html'),title=f'SkillsXLab · Taboo for nurses · Lesson {n}'))
