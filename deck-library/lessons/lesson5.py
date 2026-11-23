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
 # --- block 1: fixed arrangements (present continuous)
 teach('Fixed plans','Block 1 · Fixed plans','🗓️',['We are meeting at 10:45.','Mia is checking the lab at 11.','I am not working tonight.','Are you coming at ten?'],0),
 rec('Fixed plans','Read the calendar. Choose the sentence.',
   [Q('🗓️','The calendar says: Friday, party. What is the plan?','We are having a party on Friday.','We had a party on Friday.'),
    Q('🕙','The note says: meet at 10:45. What is the plan?','We are meeting at 10:45.','We met at 10:45.'),
    Q('🧑‍⚕️','The roster says: Mia, night shift, tonight.','Mia is working tonight.','Mia worked tonight.')],
   [Q('🗓️','Ask about the plan for 10:45.','What are you doing at 10:45?','What do you did at 10:45?','What you are doing at 10:45?'),
    Q('🕦','Dan is NOT in the plan tonight.','Dan is not coming tonight.','Dan not is coming tonight.','Dan does not coming tonight.'),
    Q('🤝','Two people. Same plan. 10:45.','We are meeting at 10:45.','We meets at 10:45.','We are meet at 10:45.')],
   [Q('🗓️','It is on the calendar. Choose the best sentence.','I am meeting the pharmacist at 11, so I cannot help.','I will meeting the pharmacist at 11, so I cannot help.','I meet pharmacist at 11, so I cannot help.','I am meet the pharmacist at 11, so I cannot help.'),
    Q('📅','The plan changed. Choose the best sentence.','We are not meeting at ten any more. We are meeting at eleven.','We not are meeting at ten any more. We are meeting at eleven.','We are not meet at ten any more.','We do not meeting at ten any more.'),
    Q('🕙','Ask a friend about THEIR plan tonight.','Are you doing anything special tonight?','Do you doing anything special tonight?','Are you do anything special tonight?','You are doing anything special tonight?')],0),
 produce('Fixed plans','Say the plan',[('🕙 10:45 · 🃏 · Mia','We are playing cards with Mia at 10:45.'),('🕚 11:00 · 🧪 · lab','I am checking the lab at 11.'),('🌙 tonight · ❌ · work','I am not working tonight.')],1),
 # --- block 2: plan or decision
 teach('Plan or decision','Block 2 · Plan or decision','💭',['Calendar: I am going to call the doctor.','Surprise! The lights go out. I will find a torch.','On the calendar = going to.','Sudden idea = will.'],1),
 rec('Plan or decision','Calendar, or sudden idea?',
   [Q('🗓️','On the calendar: Mia calls the doctor at 9. Mia ___ call the doctor.','is going to','will'),
    Q('💡','Surprise! The lights go out. I ___ find a torch.','will','am going to'),
    Q('🗓️','On the calendar: we go home at 6. We ___ go home at 6.','are going to','will')],
   [Q('✋','Nobody can carry the boxes. I ___ carry them!','will','am going to','went to'),
    Q('🗓️','On the calendar: Dan has a test on Monday. He ___ study tonight.','is going to','will','goes to'),
    Q('📞','The phone is ringing! I ___ get it!','will','am going to','get')],
   [Q('💡','A: The door is locked! B: Oh no. I ___ get the key.','will','am going to','am getting','get'),
    Q('🗓️','The plan is ready. We ___ escape at midnight.','are going to','will','are go to','going to'),
    Q('✋','Nobody wants the night shift. OK, I ___ do it.','will','am going to','do going to','am doing going')],1),
 produce('Plan or decision','Plan or decision?',[('🗓️ Friday · 🦷 dentist','I am going to see the dentist on Friday.'),('💡 lights out','I will find a torch.'),('✋ nobody can carry the boxes','I will carry them.')],2),
 # --- block 3: traps (first conditional)
 teach('Traps','Block 3 · Traps','🪤',['If the lift stops, we will use the stairs.','If the guard comes, we will hide.','If we hide, he will not see us.','If you press the alarm, everyone will run.'],2),
 rec('Traps','Finish the trap.',
   [Q('🛗','If the lift stops, we ___ the stairs.','will use','used'),
    Q('🚪','If the door is locked, we ___ the window.','will use','used'),
    Q('🔦','If the lights go out, I ___ a torch.','will find','found')],
   [Q('🧑‍✈️','If the guard comes, we ___ hide.','will','are'),
    Q('🚨','If you press the alarm, everyone ___ run.','will','would'),
    Q('🧟','If he is bitten, we ___ him.','will quarantine','quarantined','are quarantine')],
   [Q('🛗','Choose the correct sentence.','If the lift stops, we will use the stairs.','If the lift will stop, we use the stairs.','If the lift stops, we use the stairs will.','If lift stops, we will to use the stairs.'),
    Q('🔒','Choose the correct sentence.','If the door is locked, I will break the window.','If the door will be locked, I break the window.','If the door is locked, I break the window will.','If door is locked, I will to break the window.'),
    Q('🤧','Choose the correct sentence.','If it is contagious, we will wear masks.','If it will be contagious, we wear masks.','If it is contagious, we wear masks will.','If it contagious, we will wear masks.')],2),
 produce('Traps','Trap and answer',[('🛗 the lift stops','If the lift stops, we will take the stairs.'),('🧑‍✈️ the guard comes','If the guard comes, we will hide.'),('🔦 the lights go out','If the lights go out, I will find a torch.')],3),
 # --- block 4: broken plans
 teach('Broken plans','Block 4 · Broken plans','💔',['We were going to escape, but the lift stopped.','I was going to call, but my phone was dead.','They were going to help, but the guard came.','Were you going to come? Yes, but…'],3),
 rec('Broken plans','What was the plan? What went wrong?',
   [Q('🛗','The plan: escape. The lift stopped. We ___ escape, but the lift stopped.','were going to','are going to'),
    Q('📱','The plan: call. The phone was dead. I ___ call, but my phone was dead.','was going to','am going to'),
    Q('🧑‍✈️','The plan: help. The guard came. They ___ help, but the guard came.','were going to','are going to')],
   [Q('🛗','Choose the sentence.','We were going to escape, but the lift stopped.','We was going to escape, but the lift stopped.','We were going escape, but the lift stopped.'),
    Q('💊','Choose the sentence.','She was going to take the medicine, but she was bitten.','She were going to take the medicine, but she was bitten.','She was going take the medicine, but she was bitten.'),
    Q('🔑','Choose the sentence.','I was going to open the door, but I lost the key.','I were going to open the door, but I lost the key.','I was going open the door, but I lost the key.')],
   [Q('🛗','Plan A failed. Which sentence says it?','We were going to take the lift, but it stopped, so we took the stairs.','We are going to take the lift, but it stopped, so we took the stairs.','We were going to took the lift, but it stopped.','We was going to take the lift, but it stopped.'),
    Q('❓','Ask about someone’s old plan.','Were you going to leave tonight?','Was you going to leave tonight?','Did you going to leave tonight?','Were you go to leave tonight?'),
    Q('🙋','Say it was NOT the plan.','I was not going to tell anyone.','I did not going to tell anyone.','I was not go to tell anyone.','I not was going to tell anyone.')],3),
 dict(m='excuse_pp',phase='STUDY',label='Produce · Excuse Ping-Pong',min=2.5,clock=CK['S'],gear=4,gear_new=True,role='Excuse ping-pong',
      chars=[('😡','Angry Chief Doctor'),('🤕','Clumsy Intern')],plans=[('clean the lab','🧪'),('check the patient','🩺'),('call my mum','📞'),('lock the door','🔒')],sec=4),
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
   dict(trap='🛗',**{'if':'the lift stops'},then='take the stairs'),
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
    a1,a2=_cards()
    print(cards_page(a1,'L5 mingle cards · round 1',str(out/'lesson5_cards_round1.html')))
    print(cards_page(a2,'L5 mingle cards · round 2',str(out/'lesson5_cards_round2.html')))
