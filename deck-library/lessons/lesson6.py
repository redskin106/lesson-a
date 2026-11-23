"""Lesson 6 grey-box · "Washed Ashore" · boomerang ESA (Engage > Activate 1 > Study > Activate 2 > Recap)
Spec: project doc claude/lesson6-spec-nov2026.md. Placeholders: emoji for art, browser voice, wording is draft.
Build: python3 lessons/lesson6.py -> lessons-6/lesson6_v1.html (review round 1 applied 23 Nov, late)"""
import sys, pathlib
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from sxl.interactive import build_interactive
from sxl.modules import clue, kit, heist, island   # registers every module
from sxl.modules.heist import install_chrome

CK={'E':'4:00 pm','A1':'4:30 pm','S':'5:00 pm','A2':'5:30 pm','R':'sunset'}
CI={'E':'☀️','A1':'☀️','S':'🌤️','A2':'🌇','R':'🌅'}
GS=[('🎒','item'),('☁️','wish'),('🫵','advice'),('❓','question')]
def C(k,g=None,**kw):
    d=dict(clock=CK[k],cicon=CI[k],gset=GS)
    if g is not None: d['gear']=g
    d.update(kw); return d
def Q(pic,q,ans,*wrong): return dict(pic=pic,q=q,opts=[ans,*wrong],ans=ans)
def rec(title,hint,bz,sv,gd,gear,**kw):
    return dict(m='choice',phase='STUDY',title=title,hint=hint,label='Recognise · '+title,min=1.5,lvl=2,levels=[{'items':x} for x in (bz,sv,gd)],**C('S',gear),**kw)
def teach(label,role,pics,lines,gear,**kw):
    """pics = one picture per line (the big picture on the left changes as each line appears)"""
    return dict(m='teach',phase='STUDY',label='Teach · '+label,min=1.5,role=role,pic=pics[0],pics=pics,tts=True,lines=lines,**C('S',gear),**kw)
def rule(label,gear,**kw): return dict(m='rule',phase='STUDY',label='Rule · '+label,min=.5,**C('S',gear),**kw)
def produce(label,title,pairs,gear,**kw):
    return dict(m='pairs',phase='STUDY',label='Produce · '+label,min=1.5,title=title,pairs=pairs,ball=True,bigpic=True,hint='Throw the ball. Answer in a full sentence.',**C('S',gear,gear_new=True),**kw)

ENGAGE=[
 dict(m='cover',phase='ENGAGE',label='Cover',title='Lesson <span class="grad">6</span>',phases=['Engage','Study','Activate','Recap'],active=0,cards=[dict(pic='🏝️',x=1010,y=150,w=330,h=430,r=-7),dict(pic='🌅',x=1380,y=330,w=330,h=430,r=6)]),
 dict(m='story',phase='ENGAGE',label='Cold open · storm and wreck',min=1,role='Last night',pics=['⛈️','🚢','🌊','🏝️'],big='Washed ashore.',lines=['The ship sank in the storm.','Sixteen people reached the island.','The supply boat passes once.','At sunset.'],**C('E')),
 dict(m='teach',phase='ENGAGE',label='Words · stranded rescue shipwreck',min=1.5,role='Three words',words=[('🏝️','stranded'),('🚁','rescue'),('🚢','shipwreck')],**C('E')),
 dict(m='spot_change',phase='ENGAGE',label='Spot what changed · the beach',min=2,role='Look. What changed after the storm?',
      base=[('🌴',40,40),('⛺',260,50),('🛶',480,40),('🪣',50,230),('🔥',290,250),('🐚',500,240),('🪵',50,430),('🦀',300,440)],
      diffs=[(1,None,'The tent is gone!',0),(2,'🪵','the boat is a log',0),(4,'💨','the fire is out',0),(6,'🧰','a crate washed up',0)],
      extra=[('📻',540,440,'a radio on the sand… working?')],**C('E')),
]

# 15 items: survival, comfort, one phone (for the "no phone" round), one absurd item (piano, starred)
ITEMS=[('🔦','flashlight'),('🪢','rope'),('🔥','matches'),('💧','water'),('🥫','tinned food'),('🪞','mirror'),('⛺','tent'),('🎣','fishing rod'),('🩹','first-aid kit'),('📻','radio'),('🔪','knife'),('📱','phone'),('🧣','blanket'),('📖','book'),('🎹','piano')]
A1=[
 dict(m='story',phase='ACTIVATE',label='Story · 4:30 pm the question',min=.5,role='Before the storm',pics=['🧳','🎒','❓'],big='What would you bring?',lines=['A trip to an island.'],**C('A1',0)),
 dict(m='item_pick',phase='ACTIVATE',label='What would you bring and why',min=8.5,role='Tell your partner. What would you bring?',items=ITEMS,
      rounds=[('Choose 3',3,-1),('No phone',3,11),('Keep 1',1,-1)],star=14,sec=240,**C('A1',0)),
]

STUDY=[
 dict(m='today',phase='STUDY',label='Today',min=1,emoji='stethoscope',title='If we had…',role='Today we say',
      rows=[dict(icon='🎒',chips=[('c1','I'),('c2','would'),('c3','bring'),('c4','a rope')]),dict(icon='🪵🪢',chips=[('c4','If'),('c1','we had a rope,'),('c2','we'),('c3','would build a raft')]),dict(icon='🫵',chips=[('c4','If'),('c1','I were you,'),('c2','I'),('c3','would stay')]),dict(icon='❓',chips=[('c4','What'),('c2','would'),('c1','you do'),('c3','if you saw a ship?')])],fs=46,tfs=84,**C('S',0)),
 dict(m='teach',phase='STUDY',label='Words · signal shelter raft',min=1.5,role='Three more words',words=[('📡','signal'),('⛺','shelter'),('🪵','raft')],**C('S',0)),
 # optional: first conditional, written down as a rule
 rule('first conditional review',0,optional=True,role='Quick review · real situations',tag=('☀️','Real · it can happen','real'),
      formula=[('c4','If'),('c1','+ present simple,'),('c2','will'),('c3','+ verb')],
      why=[('☀️','A real, likely situation in the future.'),('➡️','We say what we expect to happen next.')],pic='🌧️⛺',
      eg=[('💧',[('c4','If'),('c1','we find clean water,'),('c2','we will'),('c3','drink it.')]),('🌧️',[('c4','If'),('c1','it rains heavily,'),('c2','we will'),('c3','stay in the shelter.')])]),
 # --- block 1: I would bring ... because ...  (exercises use new content, never the Teach lines)
 teach('I would bring','Block 1 · I would bring',['🪢','💧','📵','🎒'],['I would bring a rope.','I would bring water because I would be thirsty.','I would not bring my phone.','What would you bring?'],0),
 rule('I would bring',0,role='The rule',tag=('☁️','Imagine · not real now','imag'),
      formula=[('c1','I'),('c2','would'),('c3','+ verb'),('c4','because …')],
      why=[('☁️','We imagine the island. We are not there now.'),('🎒','Would = my choice in the imagined situation.'),('💬','Because = my reason.')],pic='🏝️',
      eg=[('🪞',[('c1','I'),('c2','would bring'),('c3','a mirror'),('c4','because it would help us signal a plane.')])]),
 rec('I would bring','Finish the sentence.',
   [Q('📻','Imagine: a desert island. You want help. I ___ bring a radio.','would','did'),
    Q('⛺','Imagine: a desert island. It might rain. I ___ bring a tent.','would','am'),
    Q('🎣','Imagine: a desert island. You are hungry. I ___ bring a fishing rod.','would','was')],
   [Q('🪞','On a desert island, I would bring a mirror because ___','I could signal a plane.','I can signaling a plane.','I signal would a plane.'),
    Q('🔪','On a desert island, I would bring a knife because ___','I would cut wood.','I would cutting wood.','I cut would wood.'),
    Q('🩹','On a desert island, I would bring a first-aid kit because ___','someone might be hurt.','someone might hurting.','someone hurt might.')],
   [Q('🎹','On a desert island, I would not bring a piano because ___','it would be too heavy.','it is would too heavy.','would be heavy it.'),
    Q('📱','On a desert island, I would not bring my phone because ___','there would be no signal.','there is would no signal.','no signal would be there is.'),
    Q('🧂','On a desert island, I would bring salt because ___','the food would taste better.','the food tastes would better.','the food would to taste better.')],0),
 produce('I would bring','Say what you would bring',[('🧴 sun cream','I would bring sun cream because the sun would be strong.'),('🪁 a kite','I would bring a kite because it could be a signal.'),('🧸 a teddy bear','I would bring a teddy bear because it would make me feel safer.')],1),
 # --- block 2: second conditional (core)
 teach('If we had','Block 2 · If we had…',['🪵🪢','🥫','⛵','📱'],['If we had a rope, we would build a raft.','If we had some food, we would not be hungry.','If I had a boat, I would sail home.','If you had a phone, what would you do?'],1),
 rule('If we had',1,role='The rule',tag=('☁️','Imaginary · unlikely','imag'),
      formula=[('c4','If'),('c1','+ past simple,'),('c2','would'),('c3','+ verb')],
      why=[('☁️','An imagined situation. We do not have it now.'),('⏰','"had" looks like the past, but we mean now.'),('💭','We say what we would do.')],pic='💭',
      eg=[('🎣',[('c4','If'),('c1','we had a net,'),('c2','we would'),('c3','catch fish.')])]),
 rec('If we had','Finish the wish.',
   [Q('🥫','If we ___ tins of food, we would eat well.','had','have'),
    Q('🛶','If I ___ a paddle, I would row to the next island.','had','have'),
    Q('📡','If they had a radio, they ___ call for help.','would','will')],
   [Q('🪵','If we had wood, we ___ a fire.','would make','will make','made'),
    Q('🥥','If I had a knife, I ___ a coconut.','would open','will open','opened'),
    Q('🧴','If they had water, they ___ thirsty.','would not be','will not be','are not be')],
   [Q('🪢','Choose the correct sentence.','If we had a net, we would catch fish.','If we would have a net, we would catch fish.','If we had a net, we will catch fish.','If we have a net, we would catch fish.'),
    Q('🎒','Choose the correct sentence.','If I had a map, I would not be lost.','If I had a map, I will not be lost.','If I would have a map, I would not be lost.','If I had a map, I would not to be lost.'),
    Q('🌧️','Choose the correct sentence.','If it did not rain, we would have no water.','If it does not rain, we would have no water.','If it did not rain, we will have no water.','If it did not rain, we would to have no water.')],1),
 produce('If we had','Make a wish',[('🛟 life ring','If we had a life ring, we would rescue our friend in the sea.'),('🔦 flashlight','If we had a flashlight, we would explore the cave.'),('📞 a phone','If we had a phone, we would call the coast guard.')],2),
 # --- block 3: advice
 teach('If I were you','Block 3 · If I were you',['🏖️','🚱','🔥','🫵'],['If I were you, I would stay on the beach.','If I were you, I would not drink sea water.','If I were you, I would make a big fire.','What would you do if you were me?'],2),
 rec('If I were you','Give advice.',
   [Q('🦈','There is a shark. If I ___ you, I would stay out of the water.','were','was'),
    Q('🌧️','It is raining. If I were you, I ___ find shelter.','would','will'),
    Q('🥥','If I were you, I ___ not eat that.','would','am')],
   [Q('🐍','A snake! Choose the advice.','If I were you, I would walk away slowly.','If I was you, I would walk away slowly.','If I were you, I will walk away slowly.'),
    Q('☀️','The sun is strong. Choose the advice.','If I were you, I would sit in the shade.','If I were you, I would to sit in the shade.','If I am you, I would sit in the shade.'),
    Q('🪫','The radio is dead. Choose the advice.','If I were you, I would wait for the sun to charge it.','If I were you, I would waited for the sun to charge it.','If I was you, I would wait for the sun.')],
   [Q('🍄','A friend wants to eat a wild mushroom. Choose the advice.','If I were you, I would not eat it.','If I were you, I will not eat it.','If I was you, I would not eat it.','If I were you, I would not to eat it.'),
    Q('🌊','The tide is coming in. Choose the advice.','If I were you, I would move the supplies up the beach.','If I were you, I would moving the supplies up the beach.','If I am you, I would move the supplies up the beach.','If I were you, I will move supplies up the beach.'),
    Q('😴','A friend is very tired. Choose the advice.','If I were you, I would take a rest.','If I were you, I would took a rest.','If I was you, I would take a rest.','If I were you, I take a rest.')],2),
 produce('If I were you','Give advice',[('🤕 hurt ankle','If I were you, I would sit down and rest.'),('🥵 very hot','If I were you, I would find some shade.'),('😰 afraid at night','If I were you, I would stay close to the fire.')],3),
 # --- block 4: questions
 teach('What would you do if','Block 4 · What would you do if…?',['🚢','🍽️','🏊','👋'],['What would you do if you saw a ship?','What would you do if you were hungry?','Would you swim to the next island? No, I would not.','If I saw a ship, I would wave.'],3),
 rule('What would you do if',3,role='The rule',tag=('❓','Ask about an imagined situation','imag'),
      formula=[('c4','What'),('c2','would'),('c1','you'),('c3','do'),('c4','if you + past simple?')],
      why=[('❓','We ask what a person would do in an imagined situation.'),('🗣️','We answer: I would + verb.')],pic='🐒',
      eg=[('🐒','What would you do if you saw a monkey?'),('🍌','I would give it a banana.')]),
 rec('What would you do if','Ask and answer.',
   [Q('🐍','___ would you do if you saw a snake?','What','Who'),
    Q('🌧️','What would you ___ if it rained all day?','do','did'),
    Q('🦀','Would you eat a crab?','Yes, I would.','Yes, I do.')],
   [Q('🥶','Choose the question.','What would you do if you were cold?','What you would do if you were cold?','What would you did if you were cold?'),
    Q('🌴','Choose the answer to: Would you climb the palm tree?','No, I would not. It is too high.','No, I would not climb. It is too high I would.','No, I do not would. It is too high.'),
    Q('🌑','Choose the question.','What would you do if the fire went out?','What would you do if the fire goes out?','What do you would if the fire went out?')],
   [Q('🚁','Choose the best question.','What would you do if a helicopter flew over us?','What would you do if a helicopter will fly over us?','What you would do if a helicopter flew over us?','What would you did if a helicopter flew over us?'),
    Q('🍽️','Answer: Would you share your last biscuit?','Yes, I would, because we need to stay strong together.','Yes, I would to, because we need to stay strong together.','Yes, I will would, because we need to stay strong.','Yes, I would share, because we are need to stay strong.'),
    Q('🗺️','Choose the best question.','Where would you go if you had a boat?','Where you would go if you had a boat?','Where would you went if you had a boat?','Where would you go if you would have a boat?')],3),
 produce('What would you do if','Island interview',[('🦈 a shark','What would you do if you saw a shark? I would get out of the water.'),('🌪️ a big storm','What would you do if there was a big storm? I would go into the cave.'),('🚢 a ship far away','What would you do if you saw a ship far away? I would light a fire.')],4),
 # --- block 5 optional
 dict(m='teach',phase='STUDY',label='Stretch · past continuous backstory',min=1.5,optional=True,role='Say it harder',pic='⛵',pics=['⛵','😴','❓'],tts=True,lines=['I was sailing when the storm hit.','We were sleeping when the ship hit a rock.','What were you doing when it happened?'],**C('S',4)),
]

DECK_FIRST=('🌪️','The storm took our shelter.','bad')
DECK_MIDS=[('📦','A crate washes ashore.','good'),('🤕','Someone hurt their ankle.','bad'),('🌧️','Rain puts out the fire.','bad'),('✈️','A plane flies very high.','good'),('🦈','A shark circles the raft.','bad'),('💧','The water is nearly gone.','bad'),('🦜','A parrot steals our rope!','bad'),('🥥','We find a coconut tree.','good')]
DECK_LAST=('🌅','The boat is coming!','fin')
A2=[
 dict(m='story',phase='ACTIVATE',label='Story · 5:30 pm the island fights back',min=1,role='Back on the island',pics=['🏝️','🌇','🛶','❓'],big='One more hour.',lines=['Things will happen.','Teams: huddle, then answer.'],**C('A2',4)),
 dict(m='next_event',phase='ACTIVATE',label='What next? · event deck',min=12,role='What next?',first=DECK_FIRST,mids=DECK_MIDS,last=DECK_LAST,rounds=3,sec=45,**C('A2',4)),
 dict(m='reveal',phase='ACTIVATE',label='Reveal · rescued',min=1,title='Rescued!',pic='⛵',answer='All safe.',grad='teal',note='Every team saved the island.',**C('A2',4)),
]

RECAP=[
 dict(m='recap',phase='RECAP',label='Recap · then and now',min=2,emoji='stethoscope',
      rows=[([('c1','I'),('c2','would'),('c3','bring'),('c4','a rope')],'what would you bring'),([('c4','If'),('c1','we had a rope,'),('c2','we'),('c3','would build a raft')],'wish'),([('c4','If'),('c1','I were you,'),('c2','I'),('c3','would stay')],'advice'),([('c4','What'),('c2','would'),('c1','you do'),('c3','if you saw a ship?')],'question')],**C('R',4)),
 dict(m='story',phase='RECAP',label='Story · sunset coda',min=1,role='Sunset',pics=['🌅','⛵','👋'],big='If we had stayed…',lines=['…we would have missed the boat.'],**C('R',4)),
 dict(m='closing',phase='EXIT',label='Thank you',min=1,stack=True,line1='Thank',line2='you!',sub='See you next time.',emoji='handshake'),
 dict(m='planb',phase='STUDY',label='Teacher · Plan B',optional=True,title='Plan B (teacher only)',tiles=[
   dict(e='📵',t='No phones',min='swap',use='Print the 15 item cards, pairs choose on paper.'),
   dict(e='⏱️',t='Running long',min='-4 min',use='Skip Block 5 and the first-conditional review. Use 3 event rounds.'),
   dict(e='⏩',t='Running short',min='+4 min',use='Do the optional stretch block. Draw a 5th event round.'),
   dict(e='🃏',t='Games (optional)',min='+4 to +10',use='Castaway Taboo (teams make cards, then play) before What next? · If-Chain as the last 4 minutes. Swap in for the optional block.'),
   dict(e='📝',t='Board notes',min='always',use='During Activate 1, write what they could not say. Use these for the Recap.')]),
]

GAMES=[
 dict(m='castaway_taboo',mode='make',phase='ACTIVATE',label='Game · Castaway Taboo 1: make the cards',min=4,optional=True,role='Castaway Taboo · make',
      words=[('🔦','flashlight'),('🪢','rope'),('🔥','matches'),('💧','water'),('🥫','tinned food'),('🪞','mirror'),('⛺','tent'),('🎣','fishing rod'),('🩹','first-aid kit'),('📻','radio')],sec=240,**C('A2',4)),
 dict(m='castaway_taboo',mode='play',phase='ACTIVATE',label='Game · Castaway Taboo 2: swap and play',min=6,optional=True,role='Castaway Taboo · play',
      frames=[('🗣️','You use it to …'),('🏝️','On an island, it would help us …'),('🔍','You find it in / on / near …')],goal=12,sec=360,**C('A2',4)),
 dict(m='if_chain',phase='RECAP',label='Game · If-Chain',min=4,optional=True,role='If-Chain',goal=12,sec=240,
      starters=[('🚤','If I had a boat, I would sail home.'),('📻','If I had a radio, I would call for help.'),('🔥','If we had matches, we would make a fire.'),('🦈','If I saw a shark, I would stay on the raft.'),('🌧️','If it rained, I would collect water.'),('🍍','If I were hungry, I would catch a fish.')],**C('R',4)),
]

L6=ENGAGE+A1+STUDY+A2[:1]+GAMES[:2]+A2[1:]+GAMES[2:]+RECAP

if __name__=='__main__':
    install_chrome()
    out=HERE.parent.parent/'lessons-6'; out.mkdir(exist_ok=True)
    print(build_interactive(L6,str(out/'lesson6_v1.html'),title='SkillsXLab · Lesson 6 · Washed Ashore (grey box)'))
    tot=sum(s.get('min',0) for s in L6 if not s.get('optional'))
    print('core minutes',tot, 'slides',len(L6))
