"""Lesson 5 grey-box · "The Night Shift" · boomerang ESA (Engage > Activate 1 > Study > Activate 2 > Recap)
Placeholders: emoji for art, browser voice, sentence wording is draft. Build: python3 lessons/lesson5.py
Slide ids are positional now; when the deck freezes, art/audio are keyed to the 'label' of each slide."""
import sys, pathlib
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from sxl.interactive import build_interactive
from sxl.modules import clue, kit, heist   # registers every module
from sxl.modules.heist import install_chrome, cards_page

CK={'E':'7:00 pm','A1':'8:00 pm','S':'10:00 pm','A2':'11:00 pm','R':'12:00'}
def Q(pic,q,ans,*wrong): return dict(pic=pic,q=q,opts=[ans,*wrong],ans=ans)
def rec(title,hint,bz,sv,gd,gear,**kw):
    return dict(m='choice',phase='STUDY',title=title,hint=hint,label='Recognise · '+title,min=1.5,lvl=2,clock=CK['S'],gear=gear,levels=[{'items':x} for x in (bz,sv,gd)],**kw)
def teach(label,role,pic,lines,gear,**kw): return dict(m='teach',phase='STUDY',label='Teach · '+label,min=1.5,role=role,pic=pic,tts=True,lines=lines,clock=CK['S'],gear=gear,**kw)
def produce(label,title,pairs,gear,**kw): return dict(m='pairs',phase='STUDY',label='Produce · '+label,min=1.5,title=title,pairs=pairs,ball=True,hint='Throw the ball. Answer in a full sentence.',clock=CK['S'],gear=gear,gear_new=True,**kw)

# ------------------------------------------------------------------ the five phases
ENGAGE=[
 dict(m='cover',phase='ENGAGE',label='Cover',title='Lesson <span class="grad">5</span>',phases=['Engage','Activate','Study','Activate','Recap'],active=0,cards=[dict(pic='🏥',x=1010,y=150,w=330,h=430,r=-7),dict(pic='🌙',x=1380,y=330,w=330,h=430,r=6)]),
 dict(m='story',phase='ENGAGE',label='Story · 7 pm',min=1,clock=CK['E'],role='Tonight',pics=['🏥','🌙','🧑‍🔬','💉'],big='Night shift.',lines=['Five people. One plan.','The antidote is in the lab.']),
 dict(m='teach',phase='ENGAGE',label='Words · antidote outbreak sabotage',min=1.5,clock=CK['E'],role='Three words',words=[('💉','antidote'),('🦠','outbreak'),('🔧','sabotage')]),
 dict(m='spot_change',phase='ENGAGE',label='Spot what changed',min=2,clock=CK['E'],role='Look. What changed?',
      base=[('🧪',40,40),('💉',260,50),('🌡️',480,40),('🔬',50,230),('📋',290,250),('🩺',500,240),('🧯',50,430),('🚪',300,440)],
      diffs=[(1,None,'The antidote is gone! Sabotage!',0),(3,'🔦','a torch, not a microscope',0),(5,'🚨','an alarm, not a stethoscope',0),(7,'🔒','the door is locked',0)],
      extra=[('🩹',540,440,'a bandage on the table… whose?')]),
]

A1=[
 dict(m='story',phase='ACTIVATE',label='Story · 8 pm',min=.5,clock=CK['A1'],gear=0,role='The shift begins',pics=['🕗','👥','🃏'],big='Find your crew.',lines=['Everyone has a plan for tonight.']),
 dict(m='mingle',phase='ACTIVATE',label='Mingle · who is with me at 10:45?',min=8.5,clock=CK['A1'],gear=0,role='Find your crew',
      card=dict(who='🧑‍⚕️',rows=[('10:00','🍜'),('10:45','🃏'),('11:30','🧹')],hi=1),steps=['🚶','🗣️','🤝'],line='Who is with me at 10:45?',sec=300),
]

STUDY=[
 dict(m='today',phase='STUDY',label='Today',min=1,clock=CK['S'],gear=0,emoji='stethoscope',title='Night-shift plans',role='Today we say',
      rows=[[('c1','We'),('c2',"'re meeting"),('c4','at 10:45')],[('c1','I'),('c2',"'ll"),('c3','help')],[('c4','If'),('c1','it stops,'),('c2',"we'll"),('c3','run')],[('c1','We'),('c2','were going to'),('c4','but…')]],fs=56,tfs=90),
 dict(m='teach',phase='STUDY',label='Words · quarantine contagious side effects',min=1.5,clock=CK['S'],gear=0,role='Three more words',words=[('🚧','quarantine'),('🤧','contagious'),('😵','side effects')]),
 # --- block 1: fixed arrangements (present continuous). Exercises use NEW situations, not the Teach lines.
 teach('Fixed plans','Block 1 · Fixed plans','🗓️',['We are meeting at 10:45.','Mia is checking the lab at 11.','I am not working tonight.','Are you coming at ten?'],0),
 rec('Fixed plans','Read the plan. Choose the sentence.',
   [Q('🚌','The ticket says: bus, 7:30 am. What is the plan?','We are taking the bus at 7:30.','We took the bus at 7:30.'),
    Q('🎂','The calendar says: Sam, birthday party, Saturday.','Sam is having a party on Saturday.','Sam had a party on Saturday.'),
    Q('📚','The timetable says: exam, Monday, 9:00.','We are taking an exam on Monday.','We took an exam on Monday.')],
   [Q('🍕','Ask a friend about THEIR plan for lunch.','What are you eating for lunch?','What do you ate for lunch?','What you are eating for lunch?'),
    Q('⚽','Tom is NOT in the match on Sunday.','Tom is not playing on Sunday.','Tom not is playing on Sunday.','Tom does not playing on Sunday.'),
    Q('🎬','Two friends. Same plan. Film, 8 pm.','We are watching a film at 8.','We watches a film at 8.','We are watch a film at 8.')],
   [Q('🦷','The dentist is on Friday, so you cannot come. Choose the best sentence.','I am seeing the dentist on Friday, so I cannot come.','I will seeing the dentist on Friday, so I cannot come.','I see dentist on Friday, so I cannot come.','I am see the dentist on Friday, so I cannot come.'),
    Q('✈️','The plan changed. Choose the best sentence.','We are not flying on Monday any more. We are flying on Tuesday.','We not are flying on Monday any more.','We are not fly on Monday any more.','We do not flying on Monday any more.'),
    Q('🎓','Ask a friend about THEIR plan after class.','Are you doing anything after class?','Do you doing anything after class?','Are you do anything after class?','You are doing anything after class?')],0),
 produce('Fixed plans','Say the plan',[('🚌 7:30 · school','We are taking the bus to school at 7:30.'),('🍜 1 pm · Mia · lunch','I am having lunch with Mia at 1.'),('🌙 tonight · ❌ · study','I am not studying tonight.')],1),
 # --- block 2: plan or decision
 teach('Plan or decision','Block 2 · Plan or decision','💭',['Calendar: I am going to call the doctor.','Surprise! The lights go out. I will find a torch.','On the calendar = going to.','Sudden idea = will.'],1),
 rec('Plan or decision','Calendar, or sudden idea?',
   [Q('🗓️','On the calendar: we visit Gran on Sunday. We ___ visit Gran on Sunday.','are going to','will'),
    Q('🌧️','Surprise! It starts to rain. I ___ get an umbrella.','will','am going to'),
    Q('🗓️','On the calendar: Lia takes an exam in May. Lia ___ study hard.','is going to','will')],
   [Q('🍽️','Oh no, there is no food! I ___ cook rice!','will','am going to','cooked'),
    Q('🗓️','On the calendar: Ben moves house in June. He ___ pack boxes.','is going to','will','moves to'),
    Q('🔋','My phone is dead! I ___ charge it.','will','am going to','charge going')],
   [Q('🥤','A: There is no water! B: Oh no. I ___ buy some.','will','am going to','am buying','buy'),
    Q('🗓️','The trip is planned. We ___ leave at six.','are going to','will','are go to','going to'),
    Q('✋','Nobody wants to clean. OK, I ___ do it.','will','am going to','do going to','am doing going')],1),
 produce('Plan or decision','Plan or decision?',[('🗓️ Saturday · 🎂 party','I am going to go to the party on Saturday.'),('💡 no sugar in the tea','I will get some sugar.'),('✋ nobody can drive','I will drive.')],2),
 # --- block 3: traps (first conditional)
 teach('Traps','Block 3 · Traps','🪤',['If the lift stops, we will use the stairs.','If the guard comes, we will hide.','If we hide, he will not see us.','If you press the alarm, everyone will run.'],2),
 rec('Traps','Finish the trap.',
   [Q('🌧️','If it rains, we ___ the bus.','will take','took'),
    Q('📱','If my phone dies, I ___ you.','will call','called'),
    Q('😴','If I am late, I ___ sorry.','will say','said')],
   [Q('📚','If you study, you ___ the test.','will pass','would','are'),
    Q('🥤','If we are thirsty, we ___ water.','will drink','would','are'),
    Q('🚌','If the bus is late, we ___ a taxi.','will take','would','are taking')],
   [Q('🌧️','Choose the correct sentence.','If it rains, we will stay at home.','If it will rain, we stay at home.','If it rains, we stay at home will.','If rains, we will to stay at home.'),
    Q('🏪','Choose the correct sentence.','If the shop is closed, I will buy food online.','If the shop will be closed, I buy food online.','If the shop is closed, I buy food online will.','If shop is closed, I will to buy food online.'),
    Q('😴','Choose the correct sentence.','If you are tired, you will sleep well.','If you will be tired, you sleep well.','If you are tired, you sleep well will.','If you tired, you will sleep well.')],2),
 produce('Traps','Trap and answer',[('🌧️ it rains','If it rains, we will stay at home.'),('🔋 the battery dies','If the battery dies, I will use a charger.'),('🚌 the bus is late','If the bus is late, we will take a taxi.')],3),
 # --- block 4: broken plans
 teach('Broken plans','Block 4 · Broken plans','💔',['We were going to escape, but the lift stopped.','I was going to call, but my phone was dead.','They were going to help, but the guard came.','Were you going to come? Yes, but…'],3),
 rec('Broken plans','What was the plan? What went wrong?',
   [Q('🎬','The plan: cinema. It was full. We ___ go to the cinema, but it was full.','were going to','are going to'),
    Q('📖','The plan: study. I was tired. I ___ study, but I was tired.','was going to','am going to'),
    Q('⚽','The plan: play. It rained. They ___ play, but it rained.','were going to','are going to')],
   [Q('🍽️','Choose the sentence.','We were going to eat out, but the restaurant was closed.','We was going to eat out, but the restaurant was closed.','We were going eat out, but the restaurant was closed.'),
    Q('🏃','Choose the sentence.','She was going to run, but her shoe broke.','She were going to run, but her shoe broke.','She was going run, but her shoe broke.'),
    Q('😴','Choose the sentence.','I was going to sleep, but the music was loud.','I were going to sleep, but the music was loud.','I was going sleep, but the music was loud.')],
   [Q('🚌','Plan A failed. Which sentence says it?','We were going to take the bus, but it was late, so we walked.','We are going to take the bus, but it was late, so we walked.','We were going to took the bus, but it was late.','We was going to take the bus, but it was late.'),
    Q('❓','Ask about someone’s old plan.','Were you going to join the trip?','Was you going to join the trip?','Did you going to join the trip?','Were you go to join the trip?'),
    Q('🙋','Say it was NOT the plan.','I was not going to say anything.','I did not going to say anything.','I was not go to say anything.','I not was going to say anything.')],3),
 dict(m='excuse_pp',phase='STUDY',label='Produce · Excuse Ping-Pong',min=2.5,clock=CK['S'],gear=4,gear_new=True,role='Excuse ping-pong',
      chars=[('😡','Angry Chief Doctor'),('🤕','Clumsy Intern')],plans=[('wash the dishes','🍽️'),('do my homework','📖'),('feed the cat','🐈'),('take out the rubbish','🗑️')],sec=4),
 # --- block 5 (optional stretch)
 dict(m='teach',phase='STUDY',label='Stretch · future continuous',min=1.5,optional=True,clock=CK['S'],gear=4,role='Say it harder',pic='🕛',tts=True,lines=['At midnight, I will be hiding in the lab.','This time tomorrow, we will be flying home.','Where will you be waiting?']),
]

SS_ITEMS=[
   dict(who='🧑‍🔬',say='I am working in the lab at 10:45. Mia is working with me.',verdict='solid',why='Mia agrees: solid.'),
   dict(who='🧑‍🍳',say='I am eating noodles at 10:45. Nobody saw me.',verdict='suspicious',why='Nobody can say: suspicious.'),
   dict(who='🧑‍⚕️',say='I am in the pharmacy at 10:45. I am alone. I have no symptoms.',verdict='suspicious',why='Alone, and no friends say yes: suspicious.'),
   dict(who='🧑‍🚒',say='I am fixing the lift at 10:45. Dan is helping me.',verdict='solid',why='Dan agrees: solid.')]
SOLID=[dict(m='solid_suspicious',phase='ACTIVATE',label=f'Solid or suspicious? {i+1}',min=3.5/len(SS_ITEMS),clock=CK['A2'],gear=4,role='Solid or suspicious?',items=[it]) for i,it in enumerate(SS_ITEMS)]
A2=[
 dict(m='story',phase='ACTIVATE',label='Story · 11 pm outbreak',min=1,clock=CK['A2'],gear=4,role='Outbreak!',pics=['⛈️','🌑','🦠','🚨'],big='Outbreak!',lines=['The lights go out.','Someone has symptoms.']),
 dict(m='mingle',phase='ACTIVATE',label='Mingle · make the escape plan',min=6,clock=CK['A2'],gear=4,role='Make the escape plan',
      card=dict(who='🧑‍🔧',rows=[('plan','🗓️'),('promise','🤝'),('trap','🪤')],hi=0),steps=['🗣️','👂','✍️'],line='Make the plan. Use your gears.',sec=360),
 *SOLID,
 dict(m='reveal',phase='ACTIVATE',label='Reveal · the bitten one',min=1,clock=CK['A2'],gear=4,title='Who is bitten?',pic='🧑‍⚕️',answer='Pharmacist',grad='rose',note='Alone at 10:45. A bandage on one hand. Remember the picture at 7 pm? 🩹'),
 dict(m='trap_chain',phase='ACTIVATE',label='Trap chain · If… we’ll…',min=6,clock=CK['A2'],gear=4,role='If… we’ll…',rows=[
   dict(trap='🔦',**{'if':'the lights go out'},then='use a torch'),
   dict(trap='🚪',**{'if':'the door is locked'},then='climb through the window'),
   dict(trap='🚨',**{'if':'the alarm rings'},then='run to the exit'),
   dict(trap='🧟',**{'if':'the pharmacist is bitten'},then='quarantine them')]),
]

RECAP=[
 dict(m='recap',phase='RECAP',label='Recap · then and now',min=2,clock=CK['R'],gear=4,emoji='stethoscope',
      rows=[([('c1','We'),('c2',"are meeting"),('c3','at 10:45')],'fixed plan'),([('c1','I'),('c2','will'),('c3','help')],'sudden idea'),([('c4','If'),('c1','it stops,'),('c2',"we'll"),('c3','run')],'trap'),([('c1','We'),('c2','were going to'),('c4','but…')],'broken plan')]),
 dict(m='story',phase='RECAP',label='Story · 12 coda',min=1,clock=CK['R'],gear=4,role='Midnight',pics=['🛗','😬','🚪'],big='We were going to escape, but…',lines=['…the lift stopped.']),
 dict(m='closing',phase='EXIT',label='Thank you',min=1,stack=True,line1='Thank',line2='you!',sub='See you next time.',emoji='handshake'),
 dict(m='planb',phase='STUDY',label='Teacher · Plan B',optional=True,title='Plan B (teacher only)',tiles=[
   dict(e='📵',t='No phones',min='swap',use='Use the printed cards from the cards page.'),
   dict(e='⏱️',t='Running long',min='-4 min',use='Skip Block 5. Cut the trap chain to 3 rows.'),
   dict(e='⏩',t='Running short',min='+4 min',use='Do the optional stretch block. Add one more Solid or Suspicious.'),
   dict(e='📝',t='Board notes',min='always',use='During Activate 1, write what they could not say. Use these for the Recap.')]),
]


# ------------------------------------------------------------------ VARIANT: RPG Activate 2 (all four teams act in every scene)
def sc(n,scene,problem,teams,after,**kw):
    return dict(m='rpg_scene',phase='ACTIVATE',label=f'RPG scene {n} · {problem}',min=3.5,clock=CK['A2'],gear=4,num=n,scene=scene,problem=problem,teams=[dict(gear=g,eg=e) for g,e in teams],after=after,**kw)
A2_RPG=[
 dict(m='story',phase='ACTIVATE',label='Story · 11 pm outbreak',min=1,clock=CK['A2'],gear=4,role='Outbreak!',pics=['⛈️','🌑','🦠','🚨'],big='Outbreak!',lines=['Four teams. Four gears.','Number 1s speak first.']),
 sc(1,'🌑','The lights go out.',[('schedule','We are meeting at the exit at midnight.'),('promise','I will find a torch.'),('trap','If the guard comes, we will hide.'),('excuse','We were going to use the lift, but the power is off.')],('🔦','Torch found. The crew moves.')),
 sc(2,'🔒','The door is locked.',[('schedule','We are climbing through the window at 11:30.'),('promise','I will carry the ladder.'),('trap','If the window is stuck, we will break it.'),('excuse','We were going to use the key, but it is lost.')],('🪟','Through the window. One floor to go.')),
 sc(3,'🚨','The alarm rings.',[('schedule','We are running to the stairs now.'),('promise','I will turn off the alarm.'),('trap','If the doctors come, we will say we are cleaning.'),('excuse','We were going to be quiet, but the alarm is so loud.')],('🤫','Alarm off. Nobody saw a thing.')),
 sc(4,'🩹','Someone has symptoms.',[('schedule','We are checking everyone at 10:45.'),('promise','I will ask the pharmacist.'),('trap','If it is contagious, we will quarantine them.'),('excuse','We were going to leave, but one is sick.')],('🧟','The pharmacist! Alone at 10:45. Bitten.')),
 dict(m='reveal',phase='ACTIVATE',label='Reveal · the bitten one',min=1,clock=CK['A2'],gear=4,title='Who is bitten?',pic='🧑‍⚕️',answer='Pharmacist',grad='rose',note='Alone at 10:45. A bandage on one hand. Remember the picture at 7 pm? 🩹'),
]
L5_RPG=ENGAGE+A1+STUDY+A2_RPG+RECAP

# ------------------------------------------------------------------ VARIANT: debate Activate 2 (team debates on its feet, whole class votes, Guess Who finale)
def dsc(n,team,scene,problem,routes,**kw):
    return dict(m='debate_scene',phase='ACTIVATE',label=f'Debate scene {n} · {problem}',min=3,clock=CK['A2'],gear=4,num=n,team=team,scene=scene,problem=problem,routes=routes,**kw)
def R(e,t,ok,ko): return dict(e=e,t=t,ok=ok,ko=ko)
A2_DEBATE=[
 dict(m='story',phase='ACTIVATE',label='Story · 11 pm outbreak',min=1,clock=CK['A2'],gear=4,role='Outbreak!',pics=['⛈️','🌑','🦠','🚨'],big='Outbreak!',lines=['One team debates. The class votes.','Everyone speaks.']),
 dsc(1,0,'🌑','The lights go out.',[R('🔦','Find the torches',('🔦','Torches on. The crew moves.'),('🔋','We were going to use the torches, but the batteries are dead.')),R('🕯️','Wait for the lights',('💡','The lights come back. Easy.'),('🧟','We were going to wait, but something is moving in the dark.'))]),
 dsc(2,1,'🔒','The door is locked.',[R('🪟','Climb through the window',('🪟','Through the window. One floor to go.'),('🪜','We were going to climb, but the ladder is too short.')),R('🔨','Break the door',('🚪','The door opens. Nobody heard.'),('🔔','We were going to break the door, but the alarm rings.'))]),
 dsc(3,2,'🚨','The alarm rings.',[R('🏃','Run to the stairs',('🏃','Down the stairs. Nobody follows.'),('🧑‍✈️','We were going to run, but the guard is on the stairs.')),R('🤫','Hide in the lab',('🧪','Safe in the lab. The alarm stops.'),('🧟','We were going to hide, but the lab is not empty.'))]),
 dsc(4,3,'🔦','The guard is coming.',[R('🧹','Pretend to clean',('🧹','"Good work!" says the guard.'),('🧽','We were going to clean, but we have no mop.')),R('🚪','Hide in the cupboard',('🤫','The guard walks past.'),('🙈','We were going to hide, but the cupboard is full.'))]),
 dict(m='guess_class',phase='ACTIVATE',label='Guess Who · who is bitten?',min=4,clock=CK['A2'],gear=4,role='Who is bitten?',secret=0,budget=8,frame='Is he / she …?',
   suspects=[dict(e='🧑‍⚕️',n='Pharmacist',a=dict(alone=True,bandage=True,working=True,symptoms=True,ground=True)),
             dict(e='🧑‍🔬',n='Lab tech',a=dict(alone=False,bandage=False,working=True,symptoms=False,ground=False)),
             dict(e='🧑‍🍳',n='Cook',a=dict(alone=True,bandage=False,working=False,symptoms=True,ground=True)),
             dict(e='🧑‍🔧',n='Porter',a=dict(alone=False,bandage=False,working=True,symptoms=False,ground=True)),
             dict(e='🧑‍🚒',n='Lift engineer',a=dict(alone=False,bandage=False,working=True,symptoms=False,ground=False))],
   attrs=[dict(k='alone',e='🧍',t='alone at 10:45'),dict(k='bandage',e='🩹',t='a bandage'),dict(k='working',e='🛠️',t='working at 10:45'),dict(k='symptoms',e='🤒',t='symptoms'),dict(k='ground',e='🛗',t='on the ground floor')]),
]
L5_DEBATE=ENGAGE+A1+STUDY+A2_DEBATE+RECAP

L5=ENGAGE+A1+STUDY+A2+RECAP

# ------------------------------------------------------------------ printable cards
def _cards():
    whos=['🧑‍⚕️','🧑‍🔬','🧑‍🍳','🧑‍🔧','🧑‍🚒','🧑‍🏫','🧑‍🚀','🧑‍🎤','🧑‍🌾','🧑‍🎨','🧑‍✈️','🧑‍💼','🧑‍🏭','🧑‍🎓','🧑‍🦱','🧑‍🦳']
    acts=['🃏','🍜','📺','🧹']; pool=['🍜','📺','🧹','🃏','🧪','📞','🛌','🥤']
    a1=[]
    for i,w in enumerate(whos):
        crew=i%4
        a1.append(dict(who=w,rows=[('10:00',pool[(i+crew+1)%8]),('10:45',acts[crew]),('11:30',pool[(i*3+2)%8])],foot='Find the people with the same picture at 10:45.'))
    a2=[dict(who=w,rows=[('plan','🗓️ We are ___ing at ___.'),('promise','🤝 I will ___.'),('trap','🪤 If ___, we will ___.')],foot='Ask. Listen. Write the plan.') for w in whos]
    return a1,a2

if __name__=='__main__':
    install_chrome()
    out=HERE.parent.parent/'lessons-5'; out.mkdir(exist_ok=True)
    print(build_interactive(L5,str(out/'lesson5_v1.html'),title='SkillsXLab · Lesson 5 · The Night Shift (grey box)'))
    print(build_interactive(L5_RPG,str(out/'lesson5_rpg_v1.html'),title='SkillsXLab · Lesson 5 · The Night Shift (RPG Activate 2)'))
    print(build_interactive(L5_DEBATE,str(out/'lesson5_debate_v1.html'),title='SkillsXLab · Lesson 5 · The Night Shift (debate Activate 2)'))
    a1,a2=_cards()
    print(cards_page(a1,'L5 mingle cards · round 1',str(out/'lesson5_cards_round1.html')))
    print(cards_page(a2,'L5 mingle cards · round 2',str(out/'lesson5_cards_round2.html')))
