"""Lessons 3 and 4, rebuilt from the reviewed library modules (L1-2 look). Build: python3 lessons/lessons34.py"""
import sys, pathlib
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent)); sys.path.insert(0,str(HERE.parent.parent/'lessons-3-4'/'src')); sys.path.insert(0,str(HERE))
import content as K
from sxl.interactive import build_interactive
import modules_gallery2 as G2, modules_gallery3 as G3
Q=lambda c,t:(c,t)
TEAMC=['#e0304a','#2a6ae0','#10a98d','#e89200']
def lv(items3): return [{'items':i} for i in items3]
def exch(e,phase='STUDY',**kw):
    fix=lambda it:dict(it,pic='🔁' if e['title'].startswith('How often') else '📅') if len(it['pic'])>4 else it
    d=dict(m='choice',phase=phase,title=e['title'],hint=e['hint'],label='Exercise · '+e['title'],lvl=1,levels=[{'items':[fix(i) for i in e['levels'][k]]} for k in ('bronze','silver','gold')]); d.update(kw); return d
def board(title,sus,clues,twist,test,ans,reveal,debate,rule=''):
    return dict(m='case_board',phase='ACTIVATE',title=title,label='Case board · '+title,min=14,teams=[(a,b,c,c2) for (a,b,c),c2 in zip(K.TEAMS,TEAMC)],suspects=sus,clues=[dict(c,topic=c.get('topic') or K.TOPIC3.get(c['id'])) for i in (K.HUNT3 if clues is K.L3_CLUES else K.HUNT4) for c in clues if c['id']==i],hunt=True,frames=K.FRAMES,twist=twist,test=test,answer=ans,reveal=reveal,debate=debate,rule=rule)

# ============================ LESSON 3 ============================
def _q(pic,q,ans,*wrong): return dict(pic=pic,q=q,opts=[ans,*wrong],ans=ans)
SYM=[[_q('🤒','Her forehead is as hot as a hot-pot. The thermometer says 39.2.','She has a fever.','She has a rash.','She has a cough.'),
  _q('😷','He coughs all night. Even the ward cat moves away.','He has a cough.','He has a rash.','He has a fever.'),
  _q('🔴','Red spots on his arm, just like a strawberry!','He has a rash on his arm.','He has a cough on his arm.','He has a fever on his arm.'),
  _q('🤕','"Doctor, I studied all night. Now my head is a drum."','He has a headache.','He has a rash.','He has a fever.')],
 [_q('🤒','Hot skin. A pounding head. She wants to lie down.','She has a fever and a headache.','She has a fever and a rash.','She has a cough and a rash.'),
  _q('🦟','A mosquito bit her at the pond. Now her legs have red spots.','She has a rash on her legs.','She has a cough on her legs.','She has a headache on her legs.'),
  _q('😷','He coughs. His skin is cool. His head is fine. He says "Do not worry!"','He has a cough, but he does not have a fever.','He has a fever, but he does not have a cough.','He has a cough and a fever.'),
  _q('💪','Her head hurts. Her eyes hurt. Her muscles hurt. She says "Even my hair hurts."','Her head, her eyes and her muscles hurt.','Her head, her eyes and her muscles hurts.','Her head and her eyes hurt, but her muscles are fine.')],
 [_q('🤒','Fever and headache. She says: "It is only Monday."','She has a fever and a headache.','She have a fever and a headache.','She has fever and headache a.','She has a fever and a cough.'),
  _q('🦟','A mosquito bit her a week ago. Now she is sick.','She was bitten by a mosquito a week ago.','A mosquito was bitten her a week ago.','She bit a mosquito a week ago.','She was bite by a mosquito.'),
  _q('🔴','Rash on the arms. No rash on the face. The patient is worried about his selfie.','She has a rash on her arms but not on her face.','She has a rash on her arms but no on her face.','She have rash on arms, not face.','She has a rash on her face but not on her arms.'),
  _q('🥵','He says: "I only feel a little warm." The thermometer says 41 °C.','He has a very high fever.','He has a low fever.','He have a very high fever.','He has fever very high.')]]
U_PL='×10⁹/L'
HL=dict(bronze=[
  _q('🌡️','The normal temperature is 37 °C. Her temperature is 39.2 °C. Her temperature is ___ than normal.','higher','lower'),
  _q('🩸',f'Normal platelets: 150 to 450 {U_PL}. Her platelets: 95 {U_PL}. Her platelets are ___ than normal.','lower','higher'),
  _q('🫁','Normal breathing: 12 to 20 breaths per minute. Her breathing: 18 breaths per minute. Her breathing is ___.','normal','higher','lower'),
  _q('💓','Normal pulse: 60 to 100 beats per minute. His pulse: 48 beats per minute. His pulse is ___ than normal.','lower','higher')],
 silver=[
  _q('🌡️','Normal temperature: 37 °C. Her temperature: 39.2 °C.','Her temperature is much higher than normal.','Her temperature is slightly higher than normal.','Her temperature is lower than normal.'),
  _q('💓','Normal pulse: 60 to 100 beats per minute. Her pulse: 104 beats per minute.','Her pulse is slightly higher than normal.','Her pulse is much lower than normal.','Her pulse is normal.'),
  _q('🩸',f'Normal white cells: 4.5 to 11 {U_PL}. Her white cells: 3.1 {U_PL}.','Her white cells are lower than normal.','Her white cells are much higher than normal.','Her white cells are normal.'),
  _q('🌡️','Normal temperature: 37 °C. His temperature: 37.4 °C. He says he feels terrible.','His temperature is only slightly higher than normal. It is not a fever.','His temperature is much higher than normal.','His temperature is lower than normal.')],
 gold=[
  _q('🥵','A patient says "I feel a little warm." The thermometer says 41 °C. Normal is 37 °C.','His temperature is far higher than normal. It is not a little warm!','His temperature is slightly higher than normal.','His temperature is much lower than normal.','His temperature is normal.'),
  _q('🩸',f'Platelets: 95 {U_PL}. Normal: 150 to 450 {U_PL}.','Her platelets are much lower than the normal range.','Her platelets are much more low than normal.','Her platelets are within the normal range.','Her platelets is lower than normal.'),
  _q('🫁','Breathing: 18 breaths per minute. Normal: 12 to 20 breaths per minute.','Her breathing is within the normal range.','Her breathing is higher than the normal range.','Her breathing is lower than the normal range.','Her breathing is normal than.'),
  _q('💓','A sleeping marathon runner: 48 beats per minute. Normal for most adults: 60 to 100.','His pulse is lower than the normal range, but he is very fit.','His pulse is much higher than normal.','His pulse is normal.','His pulse are lower than normal.')])
HM=dict(bronze=[
  _q('💓','Normal: 60 to 100. Her pulse: 104.','It is slightly higher.','It is far higher.'),
  _q('🌡️','Normal: 37 °C. His temperature: 41 °C.','It is far higher.','It is slightly higher.'),
  _q('🫁','Normal: 12 to 20. Her breathing: 21.','It is slightly higher.','It is far higher.'),
  _q('🌡️','Normal: 37 °C. Her temperature: 38 °C.','It is slightly higher.','It is far higher.')],
 silver=[
  _q('💓','Normal pulse: 60 to 100. Her pulse: 150.','Her pulse is far higher than normal.','Her pulse is slightly higher than normal.','Her pulse is the same as normal.'),
  _q('🫁','Normal breathing: 12 to 20. His breathing: 21.','His breathing is slightly higher than normal.','His breathing is far higher than normal.','His breathing is lower than normal.'),
  _q('🩸',f'Normal platelets: 150 to 450 {U_PL}. Hers: 140.','Her platelets are slightly lower than normal.','Her platelets are far lower than normal.','Her platelets are higher than normal.'),
  _q('🌡️','Normal: 37 °C. Her temperature: 35.0 °C.','Her temperature is lower than normal.','Her temperature is higher than normal.','Her temperature is normal.')],
 gold=[
  _q('💓','Her pulse is 104. Normal is 60 to 100. Which sentence is best?','Her pulse is only slightly higher than normal, so we watch her.','Her pulse is far higher than normal, so we call the doctor now.','Her pulse is slightly higher normal.','Her pulse are slightly higher than normal.'),
  _q('🩸',f'Platelets 95 {U_PL}. Normal 150 to 450 {U_PL}. Which sentence is best?','Her platelets are much lower than normal, so we tell the doctor.','Her platelets are slightly higher than normal.','Her platelets much lower than normal.','Her platelets is much lower normal.'),
  _q('🌡️','Temperature: 37.2 °C. Normal: about 37 °C. Which sentence is best?','Her temperature is about the same as normal.','Her temperature is far higher than normal.','Her temperature is much lower than normal.','Her temperature is about same normal.'),
  _q('🫁','Breathing: 30 breaths per minute. Normal: 12 to 20. Which sentence is best?','His breathing is far faster than normal. Tell the doctor.','His breathing is slightly faster than normal.','His breathing is normal.','His breathing are far fast than normal.')])
L3=[
 dict(m='cover',label='Cover',tag='NURSING ENGLISH',title='Lesson <span class="grad">3</span>',phases=['Engage','Study','Activate'],active=0,cards=[dict(pic='🩺',x=1010,y=150,w=330,h=430,r=-7),dict(pic='🌡️',x=1380,y=330,w=330,h=430,r=6)]),
 dict(m='vol_ladder',phase='ENGAGE',label='Eyes closed. Louder.',min=3,title='Eyes closed. Louder.',rungs=['fever','39 degrees','she has a rash','it might be dengue!',"IT CAN'T BE FLU!"],side='Everyone, eyes closed, at the same time. Whisper first. Each line is louder.'),
 dict(m='predict',phase='ENGAGE',label='Meet the patient',min=3,title='Meet the patient',cap=False,items=[dict(frames=[dict(e='🧍‍♀️',c='She walks in. She looks hot.'),dict(e='🌡️',c='The nurse takes her temperature.'),dict(e='😟',c='The nurse looks worried.')],q='❓ What is wrong with her?')]),
 dict(m='today',phase='STUDY',label='Today',min=1,emoji='stethoscope',title='Detective nurses',role='Today we are',rows=[[('c4','Ask'),('c3','the right question')],[('c1','Read'),('c3','the numbers')],[('c2','might'),('c4',"can't"),('c3','because')]]),
 dict(m='teach',phase='STUDY',label='Teach · Symptoms',min=2,role='Four symptoms',words=[('🤒','fever'),('🤕','headache'),('😷','cough'),('🔴','rash')]),
 dict(m='teach',phase='STUDY',label='Teach · Symptom sentences',min=2,role='Say it in a sentence',pic='🤒',lines=['She has a fever.','He has a headache.','I have a cough.','She has a rash on her arm.']),
 dict(m='choice',phase='STUDY',title='Symptoms',hint='Choose the right word or sentence.',label='Exercise · Symptoms',min=3,lvl=3,levels=lv(SYM)),
 dict(m='teach',phase='STUDY',label='Teach · Higher or lower',min=2,role='Compare with normal',pic='🌡️',lines=['The normal temperature is 37 °C (degrees Celsius).','Her temperature is 39.2 °C.','Her temperature is higher than normal.','She has a fever.']),
 dict(m='teach',phase='STUDY',label='Teach · Slightly, much, far',min=2,role='How much higher?',words=[('🤏','slightly'),('📈','much'),('🚀','far'),('🟰','about the same')]),
 dict(m='teach',phase='STUDY',label='Teach · How much?',min=2,role='How much higher?',pic='💓',lines=['Her pulse is 104. Normal is 60 to 100. It is slightly higher.','Her temperature is 41 °C. Normal is 37 °C. It is far higher.',f'Her platelets are 95 {U_PL}. Normal is 150 to 450. They are much lower.','Her breathing is 18. Normal is 12 to 20. It is about normal.']),
 exch(dict(K.L3_EX[1],levels=HL),min=4,lvl=3),
 exch(dict(title='How much?',hint='Slightly, much or far?',levels=HM),min=3,optional=True,lvl=3),
 dict(m='teach',phase='STUDY',label='Teach · Might, can\'t, because',min=2,role='Clue → sentence',pic='🦟',lines=['Clue: mosquito bites.','It might be dengue.','Clue: her belly does not hurt.','It can\'t be appendicitis.']),
 exch(K.L3_EX[2],min=3),
 dict(m='teach',phase='STUDY',label='Teach · Ask the patient',min=2,role='Good questions',pic='🩺',lines=['How long have you had a fever?','Where does it hurt?','Do you have a cough?','Have you been bitten by mosquitoes?']),
 dict(m='build',phase='STUDY',label='Exercise · Ask the patient (1)',title='Ask the patient',min=3,lvl=1,levels=[dict(pics=['🌡️'],parts=[Q('c4','How'),Q('c4','long'),Q('c2','have'),Q('c1','you'),Q('c2','had'),Q('c3','a fever?')],extra=e) for e in ([],[('c2','did'),('c2','are')],[('c2','did'),('c2','are'),('c4','since'),('c4','for')])]),
 dict(m='build',phase='STUDY',label='Exercise · Ask the patient (2)',title='Ask the patient',min=2,optional=True,lvl=1,levels=[dict(pics=['🦟'],parts=[Q('c4','Have'),Q('c1','you'),Q('c2','been'),Q('c2','bitten'),Q('c3','by mosquitoes?')],extra=e) for e in ([],[('c2','did'),('c2','are')],[('c2','did'),('c2','are'),('c2','bite'),('c4','ever')])]),
 dict(m='spell',phase='STUDY',label='Extra · Name the illness',optional=True,min=3,title='Name the illness',items=G2.ITEMS,lvl=1,levels=[dict(mode='tiles',showpic=True,decoys=0),dict(mode='tiles',showpic=False,decoys=4),dict(mode='type',showpic=False)]),
 dict(m='odd',phase='STUDY',label='Extra · What is wrong with this chart?',optional=True,min=2,items=G3.CHART,lvl=2,mode='chart'),
 dict(m='frames3',phase='ACTIVATE',label='Your sentences',min=2,title='Your sentences (they stay on the board)',groups=[
   {'t':'Easy','c':'teal','l':['She has a fever.','Her pulse is 104.','It might be dengue.'],'fs':46},
   {'t':'Better','c':'sky','l':['Her temperature is higher than normal.',"It can't be appendicitis because her belly does not hurt."],'fs':44},
   {'t':'Stretch','c':'rose','l':['It is unlikely to be flu because she has no cough.','It is probably dengue, because she has a rash and she had mosquito bites.'],'fs':38}],note='Any sentence that carries the meaning is good.'),
 dict(m='frames3',phase='ACTIVATE',label='How the hunt works',min=2,title='How the hunt works',grad='violet',groups=[
   {'t':'Your group','c':'violet','l':['You have 3 secret clues on your page.','Keep them secret!','Write every clue you hear on paper.'],'fs':42},
   {'t':'Each throw','c':'teal','l':['Hold the ball? Ask ONE group.','<b>Have you got …?</b><br><b>What does your clue say about …?</b>','They answer in a full sentence. Then they throw.'],'fs':38},
   {'t':'Then','c':'rose','l':['Teacher taps the board: the clue appears for everybody.','Everyone argues: which one can\'t it be?'],'fs':42}]),
 board('Find the illness',K.L3_SUSPECTS,K.L3_CLUES,K.L3_TWIST,K.L3_TEST,K.L3_ANSWER,'<b>It is dengue.</b><br>She has had a fever for three days and a rash on her arms and chest.<br>Her platelets and white cells are lower than normal.<br>She was bitten by mosquitoes a week ago.<br>It can\'t be flu, because she has no cough.<br>It can\'t be appendicitis, because her belly does not hurt.',
   dict(title="Wait… which can't it be?",lines=['Stand at the illness you believe.','Say why in one sentence.','Better reason? Move.']),rule='Say it in a full sentence.'),
 dict(m='boss',phase='ACTIVATE',label='Boss question (just for fun)',optional=True,min=3,**K.L3_BOSS,sec=90),
 dict(m='listen_fix',phase='ACTIVATE',label='Listen and fix (handover)',min=3,title='Listen and fix',items=[
   dict(text='Her temperature is lower than normal',say='Her temperature is higher than normal',opts=['lowest','more']),
   dict(text='She has a cough',say='She has no cough',opts=['not','any']),
   dict(text='The rash is on her face',say='The rash is on her chest',opts=['arm','leg'])],lvl=1,levels=[dict(mode='opts'),dict(mode='opts'),dict(mode='type')]),
 dict(m='frames3',phase='ACTIVATE',label='Tell the doctor (handover)',min=8,title='Tell the doctor',h=780,groups=[
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
 dict(m='frames3',phase='ACTIVATE',label='How the hunt works',min=2,title='How the hunt works',grad='violet',groups=[
   {'t':'Your group','c':'violet','l':['You have 3 secret clues on your page.','Keep them secret!','Write every clue you hear on paper.'],'fs':42},
   {'t':'Each throw','c':'teal','l':['Hold the ball? Ask ONE group.','<b>Have you got …?</b><br><b>What does your clue say about …?</b>','They answer in a full sentence. Then they throw.'],'fs':38},
   {'t':'Then','c':'rose','l':['Teacher taps the board: the clue appears for everybody.','Everyone argues: which one can\'t it be?'],'fs':42}]),
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
TABOO3=[d for d in L3 if d['m']=='taboo'][0]
TABOO4=[d for d in L4 if d['m']=='taboo'][0]
if __name__=='__main__':
    out=HERE.parent.parent/'lessons-3-4'
    print(build_interactive(L3,str(out/'lesson3_v2.html'),title='SkillsXLab · Lesson 3 · Which illness?'))
    print(build_interactive(L4,str(out/'lesson4_v2.html'),title='SkillsXLab · Lesson 4 · The Impossible Week'))
    for n,t in ((3,TABOO3),(4,TABOO4)):
        print(build_interactive([dict(t,label='Taboo for nurses',optional=False)],str(out/f'taboo{n}.html'),title=f'SkillsXLab · Taboo for nurses · Lesson {n}'))
