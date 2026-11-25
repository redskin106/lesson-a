"""Lesson 5 v2 grey-box · "Night Shift" · boomerang ESA with a cinematic intro and the Grey story.
Spec: project docs claude/lesson5-story-bible-nov2026.md and claude/lesson5-draft-lesson-nov2026.md. Placeholders: emoji for art, synthesised sounds + browser voice.
Build: python3 lessons/lesson5_v2.py -> lessons-5/lesson5_v3.html (+ lessons-5/lesson5_v3_cards.html). v1 files stay untouched."""
import sys, pathlib
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from sxl.interactive import build_interactive
from sxl.modules import clue, kit, heist, island, nightshift   # registers every module
from sxl.modules.heist import install_chrome, cards_page, cards_sheet

CK={'I':'6:58 pm','E':'7:00 pm','A1':'8:00 pm','S':'10:00 pm','A2':'11:00 pm','R':'12:00'}
GS=[('🗓️','plan'),('💭','idea'),('🪤','consequence'),('💔','excuse')]
def C(k,**kw): d=dict(clock=CK[k],cicon='🌙'); d.update(kw); return d
def Q(pic,q,ans,*wrong): return dict(pic=pic,q=q,opts=[ans,*wrong],ans=ans)
def rec(title,hint,bz,sv,gd,**kw):
    return dict(m='choice',phase='STUDY',title=title,hint=hint,label='Recognise · '+title,min=1.25,lvl=2,levels=[{'items':x} for x in (bz,sv,gd)],**C('S'),**kw)
def teach(label,role,pics,lines,**kw):
    return dict(m='teach',phase='STUDY',label='Teach · '+label,min=1.5,role=role,pic=pics[0],pics=pics,tts=True,lines=lines,**C('S'),**kw)
def produce(label,title,pairs,**kw):
    d=dict(m='pairs',phase='STUDY',label='Produce · '+label,min=1.5,title=title,pairs=pairs,ball=True,hint='Throw the ball. Answer in a full sentence.',**C('S')); d.update(kw); return d
def rule(label,**kw): return dict(m='rule',phase='STUDY',label='Rule · '+label,min=.4,role='The rule',**C('S'),**kw)
def clue_slide(n,label,pic,line,**kw):
    return dict(m='story',phase='STUDY',label=f'Clue {n} · {label}',min=.25,role=f'Clue {n}',pics=[pic],big=f'Clue {n}',lines=[line],**C('S'),**kw)

# ------------------------------------------------------------------ 0. cinematic intro (about 2 min)
INTRO=[
 dict(m='cover',mode='night',phase='ENGAGE',label='Cover',title='Lesson <span class="grad">5</span>',phases=['Engage','Study','Activate','Recap'],active=0,cards=[dict(pic='L5_sc_hospital_rain.png',x=1010,y=150,w=330,h=430,r=-7),dict(pic='L5_sc_lightning_window.png',x=1380,y=330,w=330,h=430,r=6)]),
 dict(m='nscene',mode='night',phase='ENGAGE',label='Intro 1 · black screen, rain',min=.2,rain=True,pic='L5_sc_rain_black.png',full=True),
 dict(m='nscene',mode='night',phase='ENGAGE',label='Intro 2 · shift change',min=.3,rain=True,pic='L5_sc_hospital_rain.png',full=True,line='Haven Hospital. 6:58 pm. Shift change.',fs=76,say='Haven Hospital. Six fifty-eight p.m. Shift change.',**C('I')),
 dict(m='nscene',mode='night',phase='ENGAGE',label='Intro 3 · lightning, the corridor',min=.3,rain=True,flash=True,snd=['thunder@0'],pic='L5_sc_corridor.png',full=True,line='Ward 3. Five patients are asleep.',fs=76,say='Ward three. Five patients are asleep.',**C('I')),
 dict(m='nscene',mode='night',phase='ENGAGE',label='Intro 4 · the footprints',min=.4,rain=True,flash=True,snd=['thunder@0','steps@900','cough@2600'],pic='L5_sc_footsteps.png',full=True,line='Something is there.',fs=80,say='Something is there.',**C('I')),
 dict(m='nscene',mode='night',phase='ENGAGE',label='Intro 6 · the lab door and the laugh',min=.3,rain=True,flash=True,snd=['thunder@0','creak@200','laugh@1700'],pic='L5_sc_door_ajar.png',full=True,line='Someone is hiding in the building.',fs=76,say='Someone is hiding in the building.',**C('I')),
 dict(m='nscene',mode='night',phase='ENGAGE',label='Intro 7 · title',min=.2,rain=True,title='NIGHT SHIFT',sub='7:00 pm. Midnight is coming.',**C('E')),
]

# ------------------------------------------------------------------ 1. Engage (7 pm)
ENGAGE=[
 dict(m='story',phase='ENGAGE',label='Briefing · something is about to happen',min=1,role='The briefing',clock=CK['E'],cicon='🌙',pics=['L5_sc_door_ajar.png','L5_sc_footsteps.png','L5_sc_vent.png'],big='Something is about to happen.',lines=['Someone is in the building.','We do not know who.','At midnight, he is going to open the vent.']),
 dict(m='spot_art',phase='ENGAGE',label='Spot what changed · the lab',min=1.5,role='Look. What changed?',before='L5_lab_before.png',after='L5_lab_after.png',
      hot=[('The big bottle is gone!',(170,273,230,405)),('The window is open.',(591,74,872,381)),('The chair is on the floor.',(632,501,958,724)),('The door is locked.',(875,307,981,421)),('There is a torch.',(433,410,586,479)),('There is a bandage on the floor.',(465,661,645,714)),('A drawer is open.',(425,540,607,654))],**C('E')),
]

# ------------------------------------------------------------------ 2. Activate 1 (8 pm): five crews + Grey
A1=[
 dict(m='item_pick',phase='ACTIVATE',label='Plan your night shift',min=9,role='Tell your partner. What are you doing tonight?',centre='L5_i_night_plan.png',
      items=[('L5_j_meds.png','give meds'),('L5_j_beds.png','check beds'),('L5_j_lift.png','fix the lift'),('L5_j_call.png','call courier'),('L5_j_clean.png','clean ward'),('L5_j_cook.png','cook'),('L5_j_lock.png','lock the lab'),('L5_j_notes.png','write notes'),('L5_j_tea.png','make tea'),('L5_j_pulse.png','take pulse'),('L5_j_tv.png','watch TV'),('L5_j_phone.png','my phone'),('L5_j_sleep.png','sleep'),('L5_j_games.png','play games'),('L5_j_dance.png','dance')],
      free=True,prompts=['What are you doing tonight? Why?'],sec=240,**C('A1')),
]

# ------------------------------------------------------------------ 3. Study (10 pm): four blocks, a clue after each
STUDY=[
 dict(m='today',phase='STUDY',label='Today',min=1,emoji='stethoscope',title='Night-shift plans',role='Today we say',
      rows=[[('c1','Mia'),('c2',"is meeting"),('c4','the courier at ten')],[('c1','The Stranger'),('c2',"is going to"),('c3','open the vent')],[('c4','If'),('c1','you open it,'),('c2','it'),('c3','will ring')],[('c1','He'),('c2','was going to'),('c4','but…')]],fs=52,tfs=84,**C('S')),
 dict(m='teach',phase='STUDY',label='Words · antidote outbreak sabotage',min=1.5,role='Three words',words=[('L5_w_antidote.png','antidote'),('L5_w_outbreak.png','outbreak'),('L5_w_sabotage.png','sabotage')],**C('S')),
 dict(m='teach',phase='STUDY',label='Words · quarantine contagious side effects',min=1.5,role='Three more words',words=[('L5_w_quarantine.png','quarantine'),('L5_w_contagious.png','contagious'),('L5_w_side_effects.png','side effects')],**C('S')),
 # --- block 1: fixed plans (present continuous). Teach = timetable lines; exercises use NEW people and plans.

 teach('Fixed plans','Block 1 · Fixed plans',['L5_t1_courier.png', 'L5_t1_lift.png', 'L5_t1_cooker.png', 'L5_t1_late.png'],['Mia is meeting the courier at ten.','Dan and Ben are fixing the lift at ten thirty.','Joy is not cooking tonight.','Is Pat working late? Yes, he is.']),
 rule('Fixed plans',tag=('🗓️','Fixed · arranged','real'),
      formula=[('c1','Mia'),('c2','is'),('c3','+ verb-ing'),('c4','at ten')],
      why=[('🗓️','The plan is on the timetable.'),('⏰','We know the time. It is arranged.'),('➡️','We say it with is / are + verb-ing.')],pic='L5_rl_fixed.png',
      eg=[('L5_j_beds.png',[('c1','The nurse'),('c2','is checking'),('c3','the beds'),('c4','at eight.')])]),
 rec('Fixed plans','Read the timetable. Choose the sentence.',
   [Q('L5_r_parcel.png','It is 8:00. The timetable says: nurse, delivery, 9:00.','The nurse is taking a delivery at nine.','The nurse took a delivery at nine.'),
    Q('L5_r_mop.png','It is 10:00. The timetable says: cleaner, ward 2, 10:15.','The cleaner is working on Ward 2 at ten fifteen.','The cleaner worked on Ward 2 at ten fifteen.'),
    Q('L5_r_ambulance.png','It is 10:30. The timetable says: driver, ambulance, 11:00.','The driver is leaving at eleven.','The driver left at eleven.')],
   [Q('L5_r_pizza.png','Your friend has a pizza for her break. Ask about her plan.','What are you eating during your break?','What do you ate during your break?','What you are eating during your break?'),
    Q('L5_r_guard_bed.png','The guard has the night off. Choose the sentence.','The guard is not working tonight.','The guard not is working tonight.','The guard does not working tonight.'),
    Q('L5_r_phone.png','Two nurses have the same plan: a call at ten. Choose the sentence.','They are making a call at ten.','They makes a call at ten.','They are make a call at ten.')],
   [Q('L5_r_lab_tech.png','The lab tech has a meeting at ten, so she cannot come. Choose the best sentence.','She is meeting the boss at ten, so she cannot come.','She will meeting the boss at ten, so she cannot come.','She meet the boss at ten, so she cannot come.','She is meet the boss at ten, so she cannot come.'),
    Q('L5_r_wrench.png','The door repair moves from ten to eleven. Choose the best sentence.','They are not fixing the door at ten any more. They are fixing it at eleven.','They not are fixing the door at ten any more.','They are not fix the door at ten any more.','They do not fixing the door at ten any more.'),
    Q('L5_r_colleague.png','You talk to a colleague. Ask about her plan after the shift.','Are you doing anything after the shift?','Do you doing anything after the shift?','Are you do anything after the shift?','You are doing anything after the shift?')]),
 produce('Fixed plans (listen)','Listen. Which picture?',[('🔊 audio 1','The nurse is giving the medicine at nine.'),('🔊 audio 2','The cleaner is cleaning the ward at ten.'),('🔊 audio 3','The nurse is taking a pulse at eleven.')],listen=True,ball=False,rpics=['L5_j_meds.png','L5_j_clean.png','L5_j_pulse.png'],hint='Tap a sound. Listen. Tap its picture.'),
 dict(m='story',phase='STUDY',label='Clue 1 · the antidote is gone',min=.4,role='Clue 1',pics=['L5_c_antidote_gone.png','L5_c_slot.png'],big='Clue 1',lines=['The antidote is gone.','One slot is empty: 10:45.'],**C('S')),
 # --- block 2: plan or decision
 teach('Plan or decision','Block 2 · Plan or decision',['L5_t2_bag.png', 'L5_t2_torch.png', 'L5_t2_phone.png', 'L5_t2_tea.png'],['The Stranger has a packed bag. He is going to leave.','The lights went out. I will get a torch.','Mia has the schedule. She is going to call the courier.','There is no tea. I will make some.']),
 rule('Plan or decision',tag=('💡','Plan, or sudden idea','real'),
      formula=[('c1','Plan:'),('c2','is going to'),('c3','+ verb')],
      why=[('🗓️','A plan on paper = going to.'),('💡','A sudden idea = will.'),('⚡','I decide NOW = I will.')],pic='L5_rl_plan.png',
      eg=[('L5_j_cook.png',[('c1','Joy'),('c2','is going to'),('c3','cook an egg.')]),('L5_r2_window.png',[('c4','It is cold!'),('c1','I'),('c2','will'),('c3','close the window.')])]),
 rec('Plan or decision','Plan, or sudden idea?',
   [Q('L5_t1_timetable.png','On the board: Ben fixes the lift on Friday. Ben ___ fix the lift on Friday.','is going to','will'),
    Q('L5_r_battery.png','Oh no! The phone is dead! I ___ find a charger.','will','am going to'),
    Q('L5_t1_timetable.png','On the board: Mia has a meeting at ten. She ___ be late.','is not going to','will not going to')],
   [Q('L5_r_cup.png','There is no water! I ___ go to the machine.','will','am going to','went'),
    Q('L5_t1_timetable.png','On the board: the night shift starts at seven. We ___ start at seven.','are going to','will','start going to'),
    Q('L5_r_alarm.png','The alarm is ringing! I ___ call security.','will','am going to','call going to')],
   [Q('L5_r_umbrella.png','A: It is raining. B: Oh no. I ___ get an umbrella.','will','am going to','am getting','get'),
    Q('L5_t1_timetable.png','The plan is on the board. They ___ open the vent at midnight.','are going to','will','are go to','going to'),
    Q('L5_r_hand.png','Nobody wants to check the lift. OK, I ___ do it.','will','am going to','do going to','am doing going')]),
 produce('Plan or decision (picture to text)','Plan or idea?',[('L5_p_calendar_phone.png','Pat is going to call the courier at nine.'),('L5_p_tea_sugar.png','There is no sugar. I will go to the shop.'),('L5_p_van_hand.png','The van is here. OK, I will drive it.')],ball=False,picOnly=True,bigpic=True,hint='Tap a picture. Find its sentence.'),
 clue_slide(2,'the note','L5_c_note.png','A crumpled note: a clock at midnight and the lift. Sabotage!'),
 dict(m='howto',phase='STUDY',label='Stand-up break',min=1,optional=True,role='Stand up',steps=[('L6_i_mingle.png','Stand up. Walk to someone new.'),('L6_i_pair_talk.png','Say your plan. Say why.'),('L6_i_swap_cards.png','Your partner answers. Swap. Sit down.')],dialog=[(0,'Tonight at eight, I am going to cook, because I am hungry.'),(1,'Great! I will bring the tea, because it is cold outside.')],**C('S')),
 # --- block 3: traps (first conditional). Recognise = spot the mistake.
 teach('If … will','Block 3 · Consequences',['L5_t3_alarm.png', 'L5_t3_cable.png', 'L5_t3_wake.png', 'L5_t3_button.png'],['If you open the door, the alarm will ring.','If we cut the cable, the lift will not move.','If you press the red button, everyone will wake up.','What will happen if I press it?']),
 rule('Consequences',tag=('➡️','Consequence · if this, then that','real'),
      formula=[('c4','If'),('c1','+ present simple,'),('c2','will'),('c3','+ verb')],
      why=[('➡️','If one thing happens, a result follows.'),('🔧','After if: present simple. The result: will.'),('🚫','Not after if: will.')],pic='L5_rl_if.png',
      eg=[('L5_r_rain.png',[('c4','If'),('c1','it rains,'),('c2','the floor will'),('c3','be wet.')])]),
 rec('Consequences (spot the mistake)','One sentence is wrong. Tap it.',
   [Q('L5_r_stove.png','Which sentence is wrong?','If you touch the stove, you will to burn your hand.','If you touch the stove, you will burn your hand.','If you touch the stove, you will cry.'),
    Q('L5_r_rain.png','Which sentence is wrong?','If it will rain, the floor will be wet.','If it rains, the floor will be wet.','If it rains, we will stay inside.'),
    Q('L5_t2_torch.png','Which sentence is wrong?','If the torch dies, we use will the phone.','If the torch dies, we will use the phone.','If the torch dies, we will wait.')],
   [Q('L5_sc_lab_door.png','Which sentence is wrong?','If you knock, he would open.','If you knock, he will open.','If you knock, he will not answer.'),
    Q('L5_r_bus.png','Which sentence is wrong?','If we hurry, we would catch the bus.','If we hurry, we will catch the bus.','If we hurry, we will not be late.'),
    Q('L5_w_sabotage.png','Which sentence is wrong?','If someone sabotages the phone, we would use the radio.','If someone sabotages the phone, we will use the radio.','If someone sabotages the lift, we will take the stairs.')],
   [Q('L5_r_pills.png','Which sentence is wrong?','If the nurse comes, she will gives you water.','If the nurse comes, she will give you water.','If the nurse comes, I will tell her.','If the nurse does not come, we will call her.'),
    Q('L5_w_contagious.png','Which sentence is wrong?','If the patient is contagious, we will to quarantine him.','If the patient is contagious, we will quarantine him.','If the patient is contagious, he will stay in his room.','If the patient is not contagious, he will go home.'),
    Q('L5_r_tube.png','Which sentence is wrong?','If the test is positive, we will called the doctor.','If the test is positive, we will call the doctor.','If the test is negative, we will relax.','If the test is not ready, we will wait.')]),
 clue_slide(3,'the white coat','L5_c_coat.png','A white coat. A name tag: Dr. Volkov. A stethoscope on the wrong hook.'),
 # --- block 4: broken plans
 teach('Broken plans','Block 4 · Broken plans',['L5_t4_lift_stop.png', 'L5_t4_phone_dead.png', 'L5_t4_locked.png', 'L5_t4_hand.png'],['Dr. Volkov was going to take the lift, but it stopped.','I was going to call, but the line was dead.','They were going to help, but the door was locked.','Were you going to come? Yes, but…']),
 rule('Broken plans',tag=('💔','Broken plan · it did not happen','imag'),
      formula=[('c1','I'),('c2','was going to'),('c3','+ verb,'),('c4','but …')],
      why=[('💔','The plan was real. Then it changed.'),('⏪','We say was / were going to.'),('🙋','but = the reason it did not happen.')],pic='L5_rl_broken.png',
      eg=[('L5_r2_sleep.png',[('c1','I'),('c2','was going to'),('c3','get up,'),('c4','but I fell asleep.')])]),
 rec('Broken plans','What was the plan? What went wrong?',
   [Q('L5_r_pizza.png','The plan: pizza. The shop was closed. We ___ eat pizza, but the shop was closed.','were going to','are going to'),
    Q('L5_r2_book.png','The plan: read. The light went out. I ___ read, but the light went out.','was going to','am going to'),
    Q('L5_r2_run.png','The plan: run. It rained. They ___ run, but it rained.','were going to','are going to')],
   [Q('L5_r2_plate.png','Choose the sentence.','We were going to cook, but the oven was broken.','We was going to cook, but the oven was broken.','We were going cook, but the oven was broken.'),
    Q('L5_r2_walk.png','Choose the sentence.','She was going to leave, but the guard came.','She were going to leave, but the guard came.','She was going leave, but the guard came.'),
    Q('L5_r2_sleep.png','Choose the sentence.','I was going to sleep, but the alarm rang.','I were going to sleep, but the alarm rang.','I was going sleep, but the alarm rang.')],
   [Q('L5_w_side_effects.png','Plan A failed. Which sentence says it?','We were going to give him the antidote, but it had side effects.','We are going to give him the antidote, but it had side effects.','We were going to gave him the antidote, but it had side effects.','We was going to give him the antidote, but it had side effects.'),
    Q('❓','Ask about someone’s old plan.','Were you going to join the team?','Was you going to join the team?','Did you going to join the team?','Were you go to join the team?'),
    Q('L5_t4_hand.png','Say it was NOT the plan.','I was not going to say anything.','I did not going to say anything.','I was not go to say anything.','I not was going to say anything.')]),
 dict(m='excuse_pp',phase='STUDY',label='Produce · Excuse Ping-Pong (your own sentences)',min=2.5,role='Excuse ping-pong',
      chars=[('😡','Angry Chief Nurse'),('🤕','Clumsy Intern')],example=[(0,'Where is the medicine? You were going to bring it!'),(1,'We were going to bring it, but the cart broke.')],plans=[('…','🛏️'),('…','🔒'),('…','📞'),('…','🚨')],**C('S')),
 clue_slide(4,'the half-packed bag','L5_c_bag.png','A half-packed bag. A strange gadget on the floor.'),
]

# ------------------------------------------------------------------ 4. Activate 2 (11 pm): debate, curveball, crews, escape
A2=[
 dict(m='nscene',mode='night',phase='ACTIVATE',label='Story · 11 pm the lights go out',min=.5,rain=True,flash=True,snd=['thunder@0','lights@500'],pic='L5_ev_lights_out.png',line='11 pm. One hour left.',fs=84,say='Eleven p.m. One hour left.',**C('A2')),
 dict(m='mingle',phase='ACTIVATE',label='Mingle · who is with me at 10:45?',min=2.5,role='Find your crew',
      card=dict(who='🧑‍⚕️',rows=[('10:00','L5_j_eat.png'),('10:45','L5_j_tests.png'),('11:30','L5_j_clean.png')],hi=1),steps=['L6_i_mingle.png','L6_i_pair_talk.png','L6_i_huddle.png'],line='Who is with me at 10:45?',sub='Cards face down. Same pictures = same crew.',sec=150,**C('A2')),
 dict(m='mingle_ex',phase='ACTIVATE',label='Example · find your crew',min=1,role='Example',
      cards=[dict(who='🧑‍🔬',rows=[('10:00','L5_j_call.png'),('10:45','L5_j_tests.png'),('11:30','L5_j_eat.png')]),dict(who='🧑‍🏫',rows=[('10:00','L5_j_eat.png'),('10:45','L5_j_tests.png'),('11:30','L5_j_clean.png')])],hi=1,
      dialog=[(0,'Where were you at 10:45?'),(1,'In the lab. And you?'),(0,'In the lab! Same crew.')],done='Same crew!',**C('A2')),
 dict(m='howto',phase='ACTIVATE',label='How it works · ward emergency',min=.25,role='How it works',steps=[('L5_ev_lights_out.png','An emergency appears.'),('L6_i_huddle.png','Every crew makes ONE plan. Use your own words.'),('L6_i_pair_talk.png','One member says it.'),('L6_i_vote.png','Vote: which plan saves the ward?')],line='Follow the dice.',**C('A2')),
 dict(m='next_event',phase='ACTIVATE',label='Ward emergency · dice and deck',min=4.5,role='Ward emergency',crews=5,
      first=('L5_ev_lab_locked.png','The lab door is locked.','bad'),
      mids=[('L5_w_outbreak.png','Outbreak! Bed 4 is coughing.','bad'),('L5_w_sabotage.png','Sabotage! The phone line is cut.','bad'),('L5_w_quarantine.png','Quarantine! The ward door is locked.','bad'),('L5_w_antidote.png','The antidote is gone!','bad'),('L5_ev_lights_out.png','The lights go out.','bad')],
      last=('L5_ev_midnight.png','Midnight is close. Who is the Stranger?','fin'),rounds=2,sec=20,
      ends=('🦠','🏥'),idle='L6_i_huddle.png',idlet='Press Next emergency',notimer=True,mover='🛡️',track=['🛡️'],free='Your own plan. Your own sentence.',
      vote='Best plan? Hands up.',dotsnote='1 each',endlabel='🕵️ Find him!',btn0='Next emergency ▶',**C('A2')),
 dict(m='nscene',mode='night',phase='ACTIVATE',label='Curveball · the lab door was open',min=.5,flash=True,snd=['thunder@0'],pic='L5_sc_lab_door.png',sz=480,line='The lab door was open at 10:45.',fs=76,say='The lab door was open at ten forty-five. But one crew says they were inside…',**C('A2')),
 dict(m='howto',phase='ACTIVATE',label='How it works · find the Stranger',min=.5,role='How it works',steps=[('L6_i_mingle.png','The lab crew spreads out. One crew member each.'),('L6_i_pair_talk.png','Detective pairs ask two questions.'),('L6_i_huddle.png','Compare. Same answers?'),('L6_i_vote.png','Vote. Who is the Stranger?')],line='Three say the same. One is different.',**C('A2')),
 dict(m='suspect_board',phase='ACTIVATE',label='Find the Stranger · detective board',min=4,role='Who is the Stranger?',n=4,places=['L5_j_call.png','L5_j_eat.png','L5_j_tv.png','L5_j_clean.png','L5_j_sleep.png','L5_j_microscope.png'],novote=True,
      frames=[('🕙','Where were you at 10:00?'),('🕦','At 11:30, you were going to … but …?')],reveal='The Stranger had a different card!',**C('A2')),
 dict(m='nscene',mode='night',phase='ACTIVATE',label='Chase 1 · stop',min=.3,rain=True,flash=True,snd=['thunder@0','run@500'],pic='L5_sc_corridor.png',full=True,line='Dr. Volkov! Stop!',fs=84,say='Doctor Volkov! Stop!',**C('A2')),
 dict(m='nscene',mode='night',phase='ACTIVATE',label='Chase 2 · the lift',min=.3,rain=True,snd=['run@0','creak@2300'],pic='L5_sc_lift_stuck.png',full=True,line='The lift is stuck!',fs=84,say='He is running to the lift. But the lift is stuck!',**C('A2')),
 dict(m='nscene',mode='night',phase='ACTIVATE',label='Escape · the glider coat',min=1,rain=True,flash=True,snd=['laugh2@300','whoosh@1700'],pic='L5_sc_glider_escape.png',wide=True,line='Dr. Volkov escapes!',fs=84,say='He was going to escape by the lift, but… the coat had wings.',**C('A2')),

 # optional game after Activate 2 (Nick, 24 Nov): the teams design their own cards on paper, then swap and play
 dict(m='howto',phase='ACTIVATE',label='How it works · Night-shift Taboo (design the cards)',min=5,optional=True,role='How it works',steps=[('L6_t_three_cards.png','Design 3 cards. Use the story words.'),('L6_t_swap_teams.png','Swap cards with another team.'),('L6_t_describe.png','One describes. Others guess.'),('L6_t_banned.png','Never say the banned words.')],line='Guess the cards together.',sec=240,**C('A2')),
 dict(m='castaway_taboo',mode='play',phase='ACTIVATE',label='Game · Night-shift Taboo 2: swap and play',min=6,optional=True,role='Night-shift Taboo · play',
      frames=[('🗣️','You use it to …'),('🏥','In a hospital, you …'),('🔍','You find it in / on / near …')],nocount=True,**C('A2')),
]

# ------------------------------------------------------------------ 5. Recap
RECAP=[
 dict(m='recap',phase='RECAP',label='Recap · then and now',min=2,emoji='stethoscope',
      rows=[([('c1','Mia'),('c2','is meeting'),('c3','the courier at ten')],'fixed plan'),([('c1','The Stranger'),('c2','is going to'),('c3','open the vent')],'plan'),([('c4','If'),('c1','you open it,'),('c2','it'),('c3','will ring')],'consequence'),([('c1','He'),('c2','was going to'),('c4','but…')],'broken plan')],**C('R')),
 dict(m='nscene',mode='night',phase='RECAP',label='Story · 12 coda',min=1,rain=True,pic='L5_sc_glider_escape.png',full=True,line='We were going to catch him, but…',line2='To be continued…',rev=5000,say='We were going to catch him, but he glided away.',say2='To be continued.',**C('R')),
 dict(m='closing',phase='EXIT',label='Thank you',min=1,stack=True,line1='Thank',line2='you!',sub='See you next time.',emoji='handshake'),
]
# optional stretch AFTER the thank-you page (Nick, 24 Nov)
STRETCH=[
 dict(m='teach',phase='STUDY',label='Stretch 1 · unless / before / as soon as',min=2,optional=True,role='Stretch · say it harder',pic='⏰',pics=['⏰','🔒','💡'],tts=True,lines=['Volkov will escape unless we lock the window.','Before midnight, we will find him.','As soon as the lights come on, we will go.'],**C('R')),
 dict(m='teach',phase='STUDY',label='Stretch 2 · future continuous',min=1.5,optional=True,role='Stretch · say it harder',pic='🕛',tts=True,lines=['At midnight, he will be standing in the lift.','This time tomorrow, we will be sleeping.','Where will you be waiting?'],**C('R')),
 dict(m='planb',phase='STUDY',label='Teacher · Plan B',optional=True,title='Plan B (teacher only)',tiles=[
   dict(e='📵',t='No phones',min='swap',use='Use the printed crew cards (lesson5_v3_cards.html).'),
   dict(e='⏱️',t='Running long',min='-4 min',use='Skip Taboo, the stand-up break and one emergency round.'),
   dict(e='⏩',t='Running short',min='+4 min',use='Show the two stretch slides after the Thank you page.'),
   dict(e='🕵️',t='Stranger slip',min='before class',use='Print the crew cards: 18 + the secret Stranger card 19. Hand card 19 to ONE student with card 18, quietly. Cards face down. Note who.'),
   dict(e='📝',t='Board notes',min='always',use='During Activate 1 (Plan your night shift), write what they could not say. Use these for the Recap.'),
   dict(e='🤔',t='Head Up (extra)',min='+5 min',use='Taboo word on a sticky note on each forehead. Ask yes/no questions: Is it a person?')]),
]
L5V2=INTRO+ENGAGE+A1+STUDY+A2+RECAP+STRETCH

# ------------------------------------------------------------------ printable cards: 5 crews (4,3,3,3,2) + Grey, same look; plus Grey slip
def _cards():
    # 18 students: 17 real crew members + the Stranger. Crews 3(lab)+4+4+3+3 = 17. The Stranger matches the LAB crew at 10:45 only.
    IC={'📞': 'L5_j_call.png', '🍜': 'L5_j_eat.png', '🧪': 'L5_j_tests.png', '🧹': 'L5_j_clean.png', '🍳': 'L5_j_cook.png', '📺': 'L5_j_tv.png', '🛗': 'L5_j_lift.png', '💊': 'L5_j_meds.png', '🛌': 'L5_j_sleep.png', '🔬': 'L5_j_microscope.png'}
    story=[tuple(IC[e] for e in t) for t in [('📞','🧪','🍜'),('🍜','🍳','📺'),('📺','🛗','🧹'),('🧹','💊','📞'),('🍜','🧹','🛌')]]
    sizes=[3,4,4,3,3]; faces=['🧑‍🔬','🧑‍🍳','🧑‍🔧','🧑‍⚕️','🧑‍🏭','🧑‍🏫','🧑‍🚀','🧑‍🎤','🧑‍🌾','🧑‍🎨','🧑‍✈️','🧑‍💼','🧑‍🎓','🧑‍🦱','🧑‍🦳','🧑‍🚒','🧑‍💻','🧑‍🔬']
    cards=[]; k=0
    for c,sz in enumerate(sizes):
        a,b,d=story[c]
        for _ in range(sz):
            cards.append(dict(who=faces[k],rows=[('10:00',a),('10:45',b),('11:30',d)],foot='Same pictures = same crew.')); k+=1
    cards.append(dict(who=faces[k],rows=[('10:00','L5_j_sleep.png'),('10:45','L5_j_tests.png'),('11:30','L5_j_microscope.png')],foot='Same pictures = same crew.'))  # the Stranger: only 10:45 matches the lab crew
    return cards
GREY_SLIP=[dict(who='L5_i_stranger.png',rows=[('10:00','L5_j_call.png'),('10:45','L5_j_tests.png'),('11:30','❓')],foot='You are the Stranger. Say what the lab crew says at 10:00 and 10:45. At 11:30 make something up. Tell nobody.')]  # the cover story = the lab crew's day

def _texts():
    t=[]
    for x in L5V2:
        if x['m'] in ('teach','story'): t+=[l for l in x.get('lines',[])]+list((x.get('says') or {}).values())
        if x['m']=='pairs': t+=[b for a,b in x['pairs']]
        if x['m'] in ('howto','mingle_ex'): t+=[tx for _,tx in x.get('dialog',[])]
        if x['m']=='rule': t+=[' '.join(w for _,w in e[1]) for e in x.get('eg',[])]
        if x['m']=='choice':
            for lv in x.get('levels',[]):
                for q in lv['items']:
                    t+=[o for o in q['opts'] if o!=q['ans']] if 'wrong' in q['q'] else [q['ans']]
        if x['m'] in ('nscene','nescape'): t+=[x.get('say',''),x.get('say2','')]
    return [s for s in t if s]
if __name__=='__main__':
    from sxl import audio
    audio.register(HERE.parent.parent/'lessons-5'/'audio',_texts())
    audio.register_sfx(HERE.parent.parent/'lessons-5'/'sfx')
    install_chrome()
    out=HERE.parent.parent/'lessons-5'; out.mkdir(exist_ok=True)
    print(build_interactive(L5V2,str(out/'lesson5_v3.html'),title='SkillsXLab · Lesson 5 · Night Shift (grey box v3)'))
    print(cards_sheet(_cards(),GREY_SLIP[0],'L5 crew cards (18, one is the Stranger) + Stranger slip',str(out/'lesson5_v3_cards.html')))
    tot=sum(s.get('min',0) for s in L5V2 if not s.get('optional'))
    print('core minutes',round(tot,1),'slides',len(L5V2))
