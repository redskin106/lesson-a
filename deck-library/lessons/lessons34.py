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
    fix=lambda it:dict(it,pic='📅') if len(it['pic'])>4 else it
    d=dict(m='choice',phase=phase,title=e['title'],hint=e['hint'],label='Exercise · '+e['title'],lvl=1,levels=[{'items':[fix(i) for i in e['levels'][k]]} for k in ('bronze','silver','gold')]); d.update(kw); return d
def board(title,sus,clues,twist,test,ans,reveal,debate,rule=''):
    return dict(m='case_board',phase='ACTIVATE',title=title,label='Case board · '+title,min=17,teams=[(a,b,c,c2) for (a,b,c),c2 in zip(K.TEAMS,TEAMC)],suspects=sus,clues=clues,twist=twist,test=test,answer=ans,reveal=reveal,debate=debate,rule=rule)

# ============================ LESSON 3 ============================
SYM=[[dict(pic=p,q='Look. Which word?',opts=o,ans=o[0]) for p,o in (('🤒',['fever','cough','rash']),('🤕',['headache','rash','fever']),('😷',['cough','fever','headache']),('🔴',['rash','cough','fever']))],
 [dict(pic='🤒',q='She has a high temperature.',opts=['fever','cough','rash'],ans='fever'),dict(pic='🤕',q='His head hurts.',opts=['headache','rash','fever'],ans='headache'),dict(pic='🔴',q='Red spots on the skin.',opts=['rash','cough','fever'],ans='rash'),dict(pic='😷',q='She coughs a lot.',opts=['cough','fever','headache'],ans='cough')],
 [dict(pic='🌡️',q='Her temperature is 39.2. Her skin is hot.',opts=['fever','rash','nausea'],ans='fever'),dict(pic='🤕',q='It hurts behind my eyes.',opts=['headache','cough','rash'],ans='headache'),dict(pic='🔴',q='Red spots on the arms and chest.',opts=['rash','fever','nausea'],ans='rash'),dict(pic='🤢',q='She feels sick and wants to vomit.',opts=['nausea','cough','headache'],ans='nausea')]]
L3=[
 dict(m='cover',label='Cover',tag='NURSING ENGLISH',title='Lesson <span class="grad">3</span>',phases=['Engage','Study','Activate'],active=0,cards=[dict(pic='🩺',x=1010,y=150,w=330,h=430,r=-7),dict(pic='🌡️',x=1380,y=330,w=330,h=430,r=6)]),
 dict(m='vol_ladder',phase='ENGAGE',label='Eyes closed. Louder.',min=3,title='Eyes closed. Louder.',rungs=['fever','39 degrees','she has a rash','it might be dengue!',"IT CAN'T BE FLU!"],side='Everyone, eyes closed, at the same time. Whisper first. Each line is louder.'),
 dict(m='predict',phase='ENGAGE',label='Meet the patient',min=3,title='Meet the patient',cap=False,items=[dict(frames=[dict(e='🧍‍♀️',c='She walks in. She looks hot.'),dict(e='🌡️',c='The nurse takes her temperature.'),dict(e='😟',c='The nurse looks worried.')],q='❓ What is wrong with her?')]),
 dict(m='today',phase='STUDY',label='Today',min=1,emoji='stethoscope',title='Detective nurses',role='Today we are',rows=[[('c4','Ask'),('c3','the right question')],[('c1','Read'),('c3','the numbers')],[('c2','might'),('c4',"can't"),('c3','because')]]),
 dict(m='choice',phase='STUDY',title='Symptoms',hint='Tap the right word.',label='Exercise · Symptoms',min=3,lvl=1,levels=lv(SYM)),
 exch(K.L3_EX[1],min=3),
 exch(K.L3_EX[2],min=3),
 dict(m='build',phase='STUDY',label='Exercise · Ask the patient (1)',title='Ask the patient',min=3,lvl=1,levels=[dict(pics=['🌡️'],parts=[Q('c4','How'),Q('c4','long'),Q('c2','have'),Q('c1','you'),Q('c2','had'),Q('c3','a fever?')],extra=e) for e in ([],[('c2','did'),('c2','are')],[('c2','did'),('c2','are'),('c4','since'),('c4','for')])]),
 dict(m='build',phase='STUDY',label='Exercise · Ask the patient (2)',title='Ask the patient',min=2,optional=True,lvl=1,levels=[dict(pics=['🦟'],parts=[Q('c4','Have'),Q('c1','you'),Q('c2','been'),Q('c2','bitten'),Q('c3','by mosquitoes?')],extra=e) for e in ([],[('c2','did'),('c2','are')],[('c2','did'),('c2','are'),('c2','bite'),('c4','ever')])]),
 dict(m='spell',phase='STUDY',label='Extra · Name the illness',optional=True,min=3,title='Name the illness',items=G2.ITEMS,lvl=1,levels=[dict(mode='tiles',showpic=True,decoys=0),dict(mode='tiles',showpic=False,decoys=4),dict(mode='type',showpic=False)]),
 dict(m='odd',phase='STUDY',label='Extra · What is wrong with this chart?',optional=True,min=2,items=G3.CHART,lvl=2,mode='chart'),
 dict(m='guess_who',phase='ACTIVATE',label='Extra · Guess who (warm-up for the Asker)',optional=True,min=4,attrs=G3.AT,patients=G3.PAT,rounds=2,lvl=1,levels=[dict(n=6,ask='full'),dict(n=9,ask='full'),dict(n=12,ask='word')]),
 dict(m='frames3',phase='ACTIVATE',label='Your sentences',min=2,title='Your sentences (they stay on the board)',groups=[
   {'t':'Easy','c':'teal','l':['She has a fever.','Her pulse is 104.','It might be dengue.'],'fs':46},
   {'t':'Better','c':'sky','l':['Her temperature is higher than normal.',"It can't be appendicitis because her belly does not hurt."],'fs':44},
   {'t':'Stretch','c':'rose','l':['It is unlikely to be flu because she has no cough.','It is probably dengue, because she has a rash and she had mosquito bites.'],'fs':38}],note='Any sentence that carries the meaning is good.'),
 dict(m='frames3',phase='ACTIVATE',label='How the hunt works',min=2,title='How the hunt works',grad='violet',groups=[
   {'t':'Teams of 4','c':'violet','l':['Your colour = your clues','Your letter = your job','The job changes every clue: Reader · Asker · Writer · Speaker'],'fs':42},
   {'t':'One clue','c':'teal','l':['1  Reader gets the clue','2  Asker asks · Reader answers','3  Writer: write the sentence down','4  Speaker: hands up · say it loudly'],'fs':42},
   {'t':'Then','c':'rose','l':['Teacher: "OK" → the clue appears for everybody','Another team: say it differently','Waiting? Write down what you hear.'],'fs':42}]),
 board('Find the illness',K.L3_SUSPECTS,K.L3_CLUES,K.L3_TWIST,K.L3_TEST,K.L3_ANSWER,'Dengue. Rash on the arms and chest, low platelets and white cells, no cough, mosquito bites a week ago.',
   dict(title="Wait… which can't it be?",lines=['Stand at the illness you believe.','Say why: <b>"It can\'t be flu because…"</b>','Hear a better reason? Move.']),rule='Say it in a full sentence.'),
 dict(m='boss',phase='ACTIVATE',label='Boss question (just for fun)',optional=True,min=3,**K.L3_BOSS,sec=90),
 dict(m='listen_fix',phase='ACTIVATE',label='Listen and fix (handover)',min=3,title='Listen and fix',items=[
   dict(text='Her temperature is lower than normal',say='Her temperature is higher than normal',opts=['lowest','more']),
   dict(text='She has a cough',say='She has no cough',opts=['not','any']),
   dict(text='The rash is on her face',say='The rash is on her chest',opts=['arm','leg'])],lvl=1,levels=[dict(mode='opts'),dict(mode='opts'),dict(mode='type')]),
 dict(m='frames3',phase='ACTIVATE',label='Tell the doctor (handover)',min=8,title='Tell the doctor',h=540,groups=[
   {'t':'Easy · fill the gaps','c':'teal','l':['A young woman. Day 3 of fever.','Her temperature is ___ than normal.','She has ___ and ___. No ___.','It is probably ___ because ___.'],'fs':36},
   {'t':'Better · S B A','c':'sky','l':['<b>S</b>  Patient: ___. Day ___ of ___.','<b>B</b>  She had ___ last week.','<b>A</b>  It might be ___. It can\'t be ___ because ___.'],'fs':36},
   {'t':'Stretch · your patient','c':'rose','l':['Invent your own patient.','Pick 4 facts. Say <b>S B A</b>.','<b>R</b>  "Please check ___."','Use might · can\'t · because.'],'fs':36}],write=True,note='Write it down. Then tell your partner.'),
 dict(m='taboo',phase='ACTIVATE',label='Extra · Taboo (fun)',optional=True,min=4,items=G3.TB+[dict(w='rash',e='🔴',no=['red','skin','spots','itchy'])],lvl=1,levels=[dict(limit=2),dict(limit=3,secs=60),dict(limit=4,secs=45)]),
 dict(m='exit',phase='EXIT',label='Exit',min=1,line1='One useful',line2='question.',prompt='Ask the person next to you.',emoji='light_bulb'),
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
 exch(K.L4_EX[0],min=3),
 exch(K.L4_EX[2],min=3),
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
 board('Find the reason',K.L4_SUSPECTS,K.L4_CLUES,K.L4_TWIST,K.L4_TEST,K.L4_ANSWER,'Too much coffee: 8 cups a day, 3 hours of sleep, pulse 110, normal temperature, better on the Sunday without coffee.',
   dict(title='Wait… is it just stress?',lines=['Stand at the reason you believe.','Say why with a dial: <b>"She has slept badly for two weeks."</b>','Hear a better reason? Move.']),rule='At least one dial in every sentence.'),
 dict(m='boss',phase='ACTIVATE',label='Boss question (just for fun)',optional=True,min=3,**K.L4_BOSS,sec=90),
 dict(m='frames3',phase='ACTIVATE',label='"Doctor, I\'m too busy."',min=8,title='"Doctor, I\'m too busy."',h=470,groups=[
   {'t':'Patient','c':'rose','l':['"I\'m too busy to sleep."','"I need coffee. I have three exams."'],'fs':38},
   {'t':'You (the nurse)','c':'teal','l':['"You should sleep at least seven hours."','"How many cups do you drink every day?"','"For two weeks? That is more than normal."'],'fs':32},
   {'t':'Say one thing','c':'violet','l':['Choose a dial.','Make it kind.'],'fs':42}],write=True,note='Write down one kind sentence. Then say it to your partner.'),
 dict(m='taboo',phase='ACTIVATE',label='Extra · Taboo (fun)',optional=True,min=4,items=[dict(w='coffee',e='☕',no=['cup','drink','morning','caffeine']),dict(w='insomnia',e='🌙',no=['sleep','night','cannot','bed']),dict(w='pulse',e='💓',no=['heart','beat','wrist','minute']),dict(w='headache',e='🤕',no=['head','pain','hurt','tablet'])],lvl=1,levels=[dict(limit=2),dict(limit=3,secs=60),dict(limit=4,secs=45)]),
 dict(m='exit',phase='EXIT',label='Exit',min=1,line1='Sleep well',line2='tonight.',prompt='Tell the person next to you one dial.',emoji='sleeping_face'),
]
if __name__=='__main__':
    out=HERE.parent.parent/'lessons-3-4'
    print(build_interactive(L3,str(out/'lesson3_v2.html'),title='SkillsXLab · Lesson 3 · Which illness?'))
    print(build_interactive(L4,str(out/'lesson4_v2.html'),title='SkillsXLab · Lesson 4 · The Impossible Week'))
