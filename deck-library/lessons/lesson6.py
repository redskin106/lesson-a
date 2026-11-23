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
    # gear tracker removed 24 Nov (Nick: not necessary)
    d.update(kw); return d
def Q(pic,q,ans,*wrong): return dict(pic=pic,q=q,opts=[ans,*wrong],ans=ans)
def rec(title,hint,bz,sv,gd,gear,**kw):
    return dict(m='choice',phase='STUDY',title=title,hint=hint,label='Recognise · '+title,min=1.5,lvl=2,levels=[{'items':x} for x in (bz,sv,gd)],**C('S',gear),**kw)
def teach(label,role,pics,lines,gear,**kw):
    """pics = one picture per line (the big picture on the left changes as each line appears)"""
    return dict(m='teach',phase='STUDY',label='Teach · '+label,min=1.5,role=role,pic=pics[0],pics=pics,tts=True,lines=lines,**C('S',gear),**kw)
def rule(label,gear,**kw): return dict(m='rule',phase='STUDY',label='Rule · '+label,min=.5,**C('S',gear),**kw)
def produce(label,title,pairs,gear,**kw):
    return dict(m='pairs',phase='STUDY',label='Produce · '+label,min=1.5,title=title,pairs=pairs,ball=True,bigpic=True,hint='Throw the ball. Answer in a full sentence.',picOnly=True,**C('S',gear),**kw)

ENGAGE=[
 dict(m='cover',phase='ENGAGE',label='Cover',title='Lesson <span class="grad">6</span>',phases=['Engage','Study','Activate','Recap'],active=0,cards=[dict(pic='L6_sc_island_far.png',x=1010,y=150,w=330,h=430,r=-7),dict(pic='L6_sc_sunset_boat.png',x=1380,y=330,w=330,h=430,r=6)]),
 dict(m='story',phase='ENGAGE',label='Cold open · storm and wreck',min=1,role='Last night',pics=['L6_sc_storm.png','L6_sc_sinking.png','L6_sc_wreckage.png','L6_sc_island_far.png'],big='Washed ashore.',lines=['The ship sank in the storm.','Sixteen people reached the island.','The supply boat passes once.','At sunset.'],**C('E')),
 dict(m='story',phase='ENGAGE',label='Cold open · look and predict',min=1,optional=True,role='Look',pics=['L6_sc_wreckage.png','L6_sc_island_far.png','L6_p_hungry.png','❓'],big='What do you see?',lines=['Tell your partner: three things.','What happened?','What do they need?'],**C('E')),
 dict(m='spot_art',phase='ENGAGE',label='Spot what changed · the beach',min=2,role='Look. What changed after the storm?',before='L6_beach_before.png',after='L6_beach_after.png',
      hot=[('The tent is gone!',(258,283,545,450)),('The canoe is upside down.',(675,335,965,500)),('The fire is out.',(495,390,660,535)),('There is a crate.',(738,445,860,570)),('The bucket is on its side.',(133,554,309,687)),('One gull is gone.',(676,64,730,92)),('There is one coconut, not three.',(315,98,403,184))],**C('E')),
]

# 15 items: survival, comfort, one phone (for the "no phone" round), one absurd item (piano, starred)
ITEMS=[('L6_flashlight.png','flashlight'),('L6_rope.png','rope'),('L6_matches.png','matches'),('L6_water.png','water'),('L6_tinned_food.png','tinned food'),('L6_mirror.png','mirror'),('L6_tent.png','tent'),('L6_fishing_rod.png','fishing rod'),('L6_first_aid_kit.png','first-aid kit'),('L6_radio.png','radio'),('L6_knife.png','knife'),('L6_phone.png','phone'),('L6_blanket.png','blanket'),('L6_book.png','book'),('L6_piano.png','piano')]
A1=[
 dict(m='story',phase='ACTIVATE',label='Story · 4:30 pm the question',min=.5,role='Before the storm',pics=['L6_sc_bags.png','L6_backpack.png','❓'],big='What would you bring?',lines=['A trip to an island.'],**C('A1',0)),
 dict(m='item_pick',phase='ACTIVATE',label='What would you bring and why',min=8.5,role='Tell your partner. What would you bring?',items=ITEMS,
      rounds=[('Choose 3',3,-1),('No phone',3,11),('Keep 1',1,-1)],prompts=['What would you bring? Why?','No phone! What now? Why?','Only one. Which? Why?'],star=14,sec=240,**C('A1',0)),
]

STUDY=[
 dict(m='today',phase='STUDY',label='Today',min=1,emoji='L6_sc_island_far',title='If we had…',role='Today we say',
      rows=[dict(icon='L6_backpack.png',chips=[('c1','I'),('c2','would'),('c3','bring'),('c4','a rope')]),dict(icon='L6_x_raft_logs.png',chips=[('c4','If'),('c1','we had a rope,'),('c2','we'),('c3','would build a raft')]),dict(icon='L6_x_point.png',chips=[('c4','If'),('c1','I were you,'),('c2','I'),('c3','would stay')]),dict(icon='❓',chips=[('c4','What'),('c2','would'),('c1','you do'),('c3','if you saw a ship?')])],fs=42,tfs=84,**C('S',0)),
 dict(m='teach',phase='STUDY',label='Words · stranded rescue shipwreck',min=1.5,role='Three words for the story',words=[('L6_w_stranded.png','stranded'),('L6_w_rescue.png','rescue'),('L6_w_shipwreck.png','shipwreck')],**C('S',0)),
 dict(m='teach',phase='STUDY',label='Words · signal shelter raft',min=1.5,role='Three more words',words=[('L6_w_signal.png','signal'),('L6_w_shelter.png','shelter'),('L6_w_raft.png','raft')],**C('S',0)),
 # optional: first conditional, written down as a rule
 rule('first conditional review',0,optional=True,role='Quick review · real situations',tag=('☀️','Real · it can happen','real'),
      formula=[('c4','If'),('c1','+ present simple,'),('c2','will'),('c3','+ verb')],
      why=[('☀️','A real, likely situation in the future.'),('➡️','We say what we expect to happen next.')],pic='L6_ev_rain_fire.png',
      eg=[('L6_water.png',[('c4','If'),('c1','we find clean water,'),('c2','we will'),('c3','drink it.')]),('L6_ev_rain_fire.png',[('c4','If'),('c1','it rains heavily,'),('c2','we will'),('c3','stay in the shelter.')])]),
 # --- block 1: I would bring ... because ...  (exercises use new content, never the Teach lines)
 teach('I would bring','Block 1 · I would bring',['L6_rope.png','L6_water.png','L6_phone.png','L6_backpack.png'],['I would bring a rope.','I would bring water because I would be thirsty.','I would not bring my phone.','What would you bring?'],0),
 rule('I would bring',0,role='The rule',tag=('☁️','Imagine · not real now','imag'),
      formula=[('c1','I'),('c2','would'),('c3','+ verb'),('c4','because …')],
      why=[('☁️','We imagine the island. We are not there now.'),('🎒','Would = my choice in the imagined situation.'),('💬','Because = my reason.')],pic='L6_sc_island_far.png',
      eg=[('L6_mirror.png',[('c1','I'),('c2','would bring'),('c3','a mirror'),('c4','because it would help us signal a plane.')])]),
 rec('I would bring','Finish the sentence.',
   [Q('L6_radio.png','Imagine: a desert island. You want help. I ___ bring a radio.','would','did'),
    Q('L6_tent.png','Imagine: a desert island. It might rain. I ___ bring a tent.','would','am'),
    Q('L6_fishing_rod.png','Imagine: a desert island. You are hungry. I ___ bring a fishing rod.','would','was')],
   [Q('L6_mirror.png','On a desert island, I would bring a mirror because ___','I could signal a plane.','I can signaling a plane.','I signal would a plane.'),
    Q('L6_knife.png','On a desert island, I would bring a knife because ___','I would cut wood.','I would cutting wood.','I cut would wood.'),
    Q('L6_first_aid_kit.png','On a desert island, I would bring a first-aid kit because ___','someone might be hurt.','someone might hurting.','someone hurt might.')],
   [Q('L6_piano.png','On a desert island, I would not bring a piano because ___','it would be too heavy.','it is would too heavy.','would be heavy it.'),
    Q('L6_phone.png','On a desert island, I would not bring my phone because ___','there would be no signal.','there is would no signal.','no signal would be there is.'),
    Q('L6_salt.png','On a desert island, I would bring salt because ___','the food would taste better.','the food tastes would better.','the food would to taste better.')],0),
 produce('I would bring','Say what you would bring',[('L6_sun_cream.png sun cream','I would bring sun cream because the sun would be strong.'),('L6_kite.png a kite','I would bring a kite because it could be a signal.'),('L6_teddy_bear.png a teddy bear','I would bring a teddy bear because it would make me feel safer.')],1),
 # --- block 2: second conditional (core)
 teach('If we had','Block 2 · If we had…',['L6_x_raft_logs.png','L6_tinned_food.png','L6_x_sailboat.png','L6_phone.png'],['If we had a rope, we would build a raft.','If we had some food, we would not be hungry.','If I had a boat, I would sail home.','If you had a phone, what would you do?'],1),
 rule('If we had',1,role='The rule',tag=('☁️','Imaginary · unlikely','imag'),
      formula=[('c4','If'),('c1','+ past simple,'),('c2','would'),('c3','+ verb')],
      why=[('☁️','An imagined situation. We do not have it now.'),('⏰','"had" looks like the past, but we mean now.'),('💭','We say what we would do.')],pic='💭',
      eg=[('L6_net.png',[('c4','If'),('c1','we had a net,'),('c2','we would'),('c3','catch fish.')])]),
 rec('If we had','Finish the wish.',
   [Q('L6_tinned_food.png','If we ___ tins of food, we would eat well.','had','have'),
    Q('L6_paddle.png','If I ___ a paddle, I would row to the next island.','had','have'),
    Q('L6_radio.png','If they had a radio, they ___ call for help.','would','will')],
   [Q('L6_x_raft_logs.png','If we had wood, we ___ a fire.','would make','will make','made'),
    Q('L6_coconut.png','If I had a knife, I ___ a coconut.','would open','will open','opened'),
    Q('L6_water.png','If they had water, they ___ thirsty.','would not be','will not be','are not be')],
   [Q('L6_net.png','Choose the correct sentence.','If we had a net, we would catch fish.','If we would have a net, we would catch fish.','If we had a net, we will catch fish.','If we have a net, we would catch fish.'),
    Q('L6_map.png','Choose the correct sentence.','If I had a map, I would not be lost.','If I had a map, I will not be lost.','If I would have a map, I would not be lost.','If I had a map, I would not to be lost.'),
    Q('L6_ev_rain_fire.png','Choose the correct sentence.','If it did not rain, we would have no water.','If it does not rain, we would have no water.','If it did not rain, we will have no water.','If it did not rain, we would to have no water.')],1),
 produce('If we had','Make a wish',[('L6_life_ring.png life ring','If we had a life ring, we would rescue our friend in the sea.'),('L6_flashlight.png flashlight','If we had a flashlight, we would explore the cave.'),('L6_phone.png a phone','If we had a phone, we would call the coast guard.')],2),
 # --- block 3: advice
 teach('If I were you','Block 3 · If I were you',['L6_sc_island_far.png','L6_x_no_seawater.png','L6_x_big_fire.png','L6_x_point.png'],['If I were you, I would stay on the beach.','If I were you, I would not drink sea water.','If I were you, I would make a big fire.','What would you do if you were me?'],2),
 rule('If I were you',2,role='The rule',optional=True,tag=('💭','Advice · imaginary','imag'),
      formula=[('c4','If'),('c1','I were you,'),('c2','I would'),('c3','+ verb')],
      why=[('💬','We give advice to a friend.'),('🪞','We imagine: I am in your place.'),('✅','Say "were", not "was", after I.')],pic='L6_x_point.png',
      eg=[('L6_mushroom.png',[('c4','If'),('c1','I were you,'),('c2','I would'),('c3','not eat it.')])]),
 rec('If I were you','Give advice.',
   [Q('L6_ev_shark_raft.png','There is a shark. If I ___ you, I would stay out of the water.','were','was'),
    Q('L6_ev_rain_fire.png','It is raining. If I were you, I ___ find shelter.','would','will'),
    Q('L6_coconut.png','If I were you, I ___ not eat that.','would','am')],
   [Q('L6_snake.png','A snake! Choose the advice.','If I were you, I would walk away slowly.','If I was you, I would walk away slowly.','If I were you, I will walk away slowly.'),
    Q('L6_hot_sun.png','The sun is strong. Choose the advice.','If I were you, I would sit in the shade.','If I were you, I would to sit in the shade.','If I am you, I would sit in the shade.'),
    Q('L6_dead_radio.png','The radio is dead. Choose the advice.','If I were you, I would wait for the sun to charge it.','If I were you, I would waited for the sun to charge it.','If I was you, I would wait for the sun.')],
   [Q('L6_mushroom.png','A friend wants to eat a wild mushroom. Choose the advice.','If I were you, I would not eat it.','If I were you, I will not eat it.','If I was you, I would not eat it.','If I were you, I would not to eat it.'),
    Q('L6_tide.png','The tide is coming in. Choose the advice.','If I were you, I would move the supplies up the beach.','If I were you, I would moving the supplies up the beach.','If I am you, I would move the supplies up the beach.','If I were you, I will move supplies up the beach.'),
    Q('L6_p_tired.png','A friend is very tired. Choose the advice.','If I were you, I would take a rest.','If I were you, I would took a rest.','If I was you, I would take a rest.','If I were you, I take a rest.')],2),
 produce('If I were you','Give advice',[('L6_p_hurt_ankle.png hurt ankle','If I were you, I would sit down and rest.'),('L6_p_very_hot.png very hot','If I were you, I would find some shade.'),('L6_p_afraid_night.png afraid at night','If I were you, I would stay close to the fire.')],3),
 # --- block 4: questions
 teach('What would you do if','Block 4 · What would you do if…?',['L6_sc_sunset_boat.png','L6_x_meal.png','L6_x_swimmer_far.png','L6_x_wave_hand.png'],['What would you do if you saw a ship?','What would you do if you were hungry?','Would you swim to the next island? No, I would not.','If I saw a ship, I would wave.'],3),
 rule('What would you do if',3,role='The rule',tag=('❓','Ask about an imagined situation','imag'),
      formula=[('c4','What'),('c2','would'),('c1','you'),('c3','do'),('c4','if you + past simple?')],
      why=[('❓','We ask what a person would do in an imagined situation.'),('🗣️','We answer: I would + verb.')],pic='🐒',
      eg=[('🐒','What would you do if you saw a monkey? I would give it a banana.')],
      prompts=[('L6_p_hungry.png','if you were hungry?'),('L6_ev_shark_raft.png','if you saw a shark?'),('L6_p_cold.png','if you were cold?')]),
 rec('What would you do if','Ask and answer.',
   [Q('L6_snake.png','___ would you do if you saw a snake?','What','Who'),
    Q('L6_ev_rain_fire.png','What would you ___ if it rained all day?','do','did'),
    Q('L6_crab.png','Would you eat a crab?','Yes, I would.','Yes, I do.')],
   [Q('L6_p_cold.png','Choose the question.','What would you do if you were cold?','What you would do if you were cold?','What would you did if you were cold?'),
    Q('L6_palm_tree.png','Choose the answer to: Would you climb the palm tree?','No, I would not. It is too high.','No, I would not climb. It is too high I would.','No, I do not would. It is too high.'),
    Q('L6_fire_out.png','Choose the question.','What would you do if the fire went out?','What would you do if the fire goes out?','What do you would if the fire went out?')],
   [Q('L6_helicopter.png','Choose the best question.','What would you do if a helicopter flew over us?','What would you do if a helicopter will fly over us?','What you would do if a helicopter flew over us?','What would you did if a helicopter flew over us?'),
    Q('L6_biscuits.png','Answer: Would you share your last biscuit?','Yes, I would, because we need to stay strong together.','Yes, I would to, because we need to stay strong together.','Yes, I will would, because we need to stay strong.','Yes, I would share, because we are need to stay strong.'),
    Q('L6_map.png','Choose the best question.','Where would you go if you had a boat?','Where you would go if you had a boat?','Where would you went if you had a boat?','Where would you go if you would have a boat?')],3),
 dict(m='mingle',phase='STUDY',label='Mingle · Island interview',min=2,role='Island interview',card=dict(who='L6_sc_island_far.png',rows=[('a shark','L6_ev_shark_raft.png'),('a storm','L6_sc_storm.png'),('a ship','L6_sc_sunset_boat.png')],hi=0),steps=['🚶','🗣️','🔄'],caps=['Stand up. Find a classmate.','Ask. Listen.','Swap. Find a new one.'],line='Ask 3 classmates.',sub='What would you do if you saw a shark? I would …',sec=180,**C('S',4)),
 # --- block 5 optional
 dict(m='teach',phase='STUDY',label='Stretch · what were you doing?',min=1.5,optional=True,role='Challenge · before the storm',pic='L6_x_sailboat.png',pics=['L6_x_sailboat.png','L6_p_tired.png','L6_sc_sinking.png'],tts=True,lines=['I was sailing when the storm hit.','We were sleeping when the ship hit a rock.','What were you doing when it happened?'],**C('S',4)),
]

DECK_FIRST=('L6_ev_storm_shelter.png','The storm took our shelter.','bad')
DECK_MIDS=[('L6_ev_crate.png','A crate washes ashore.','good'),('L6_ev_ankle.png','Someone hurt their ankle.','bad'),('L6_ev_rain_fire.png','Rain puts out the fire.','bad'),('L6_ev_plane.png','A plane flies very high.','good'),('L6_ev_shark_raft.png','A shark circles the raft.','bad'),('L6_ev_water_gone.png','The water is nearly gone.','bad'),('L6_ev_parrot_rope.png','A parrot steals our rope!','bad'),('L6_ev_coconut_tree.png','We find a coconut tree.','good')]
DECK_LAST=('L6_ev_boat_sunset.png','The boat is coming!','fin')
A2=[
 dict(m='story',phase='ACTIVATE',label='Story · 5:30 pm the island fights back',min=1,role='Back on the island',pics=['L6_sc_island_far.png','L6_sc_sunset_boat.png','L6_x_sailboat.png','❓'],big='One more hour.',lines=['Things will happen.','Teams: huddle, then answer.'],**C('A2',4)),
 dict(m='howto',phase='ACTIVATE',label='How it works · What next?',min=1,role='How it works',steps=[('L6_ev_shark_raft.png','A problem appears.'),('👥','Team talk. 45 seconds.'),('🎤','Say your idea.'),('✋','Class vote.')],line='If we had …, we would … because …',**C('A2',4)),
 dict(m='next_event',phase='ACTIVATE',label='What next? · event deck',min=11,role='What next?',first=DECK_FIRST,mids=DECK_MIDS,last=DECK_LAST,rounds=3,sec=45,**C('A2',4)),
 dict(m='reveal',phase='ACTIVATE',label='Reveal · rescued',min=1,title='Rescued!',pic='L6_x_sailboat.png',answer='All safe.',grad='teal',note='Our ideas got us rescued.',**C('A2',4)),
]

RECAP=[
 dict(m='recap',phase='RECAP',label='Recap · then and now',min=2,emoji='L6_sc_island_far',
      rows=[([('c1','I'),('c2','would'),('c3','bring'),('c4','a rope')],'what would you bring'),([('c4','If'),('c1','we had a rope,'),('c2','we'),('c3','would build a raft')],'wish'),([('c4','If'),('c1','I were you,'),('c2','I'),('c3','would stay')],'advice'),([('c4','What'),('c2','would'),('c1','you do'),('c3','if you saw a ship?')],'question')],**C('R',4)),
 dict(m='story',phase='RECAP',label='Story · sunset coda',min=1,role='Sunset',pics=['L6_sc_island_far.png','L6_sc_sunset_boat.png','L6_x_sailboat.png','L6_x_wave_hand.png'],big='If we had stayed…',lines=['…we would have missed the boat.'],**C('R',4)),
 dict(m='closing',phase='EXIT',label='Thank you',min=1,stack=True,line1='Thank',line2='you!',sub='See you next time.',emoji='L6_x_wave_hand'),
 dict(m='planb',phase='STUDY',label='Teacher · Plan B',optional=True,title='Plan B (teacher only)',tiles=[
   dict(e='📵',t='No phones',min='swap',use='Print the 15 item cards, pairs choose on paper.'),
   dict(e='⏱️',t='Running long',min='-4 min',use='Skip every optional slide. Use 3 event rounds.'),
   dict(e='⏩',t='Running short',min='+4 min',use='Add the optional rule and stretch slides. Draw a 5th round.'),
   dict(e='🃏',t='Games (optional)',min='+4 to +10',use='Castaway Taboo before What next?, or If-Chain as the last 4 minutes.'),
   dict(e='📝',t='Board notes',min='always',use='During Activate 1, write what they could not say. Use these for the Recap.')]),
]

GAMES=[
 dict(m='castaway_taboo',mode='make',phase='ACTIVATE',label='Game · Castaway Taboo 1: make the cards',min=4,optional=True,role='Castaway Taboo · make',
      words=[('L6_flashlight.png','flashlight'),('L6_rope.png','rope'),('L6_matches.png','matches'),('L6_water.png','water'),('L6_tinned_food.png','tinned food'),('L6_mirror.png','mirror'),('L6_tent.png','tent'),('L6_fishing_rod.png','fishing rod'),('L6_first_aid_kit.png','first-aid kit'),('L6_radio.png','radio')],sec=240,**C('A2',4)),
 dict(m='castaway_taboo',mode='play',phase='ACTIVATE',label='Game · Castaway Taboo 2: swap and play',min=6,optional=True,role='Castaway Taboo · play',
      frames=[('🗣️','You use it to …'),('🏝️','On an island, it would help us …'),('🔍','You find it in / on / near …')],goal=12,sec=360,**C('A2',4)),
 dict(m='if_chain',phase='RECAP',label='Game · If-Chain',min=4,optional=True,role='If-Chain',goal=12,sec=240,
      starters=[('🚤','If I had a boat, I would sail home.'),('📻','If I had a radio, I would call for help.'),('🔥','If we had matches, we would make a fire.'),('🦈','If I saw a shark, I would stay on the raft.'),('🌧️','If it rained, I would collect water.'),('🍍','If I were hungry, I would catch a fish.')],**C('R',4)),
]

# Activate 2: What next? > Rescued! > (optional) Castaway Taboo. After the Thank you: optional If-Chain, then Plan B.
_clo=next(i for i,x in enumerate(RECAP) if x['m']=='closing')
L6=ENGAGE+A1+STUDY+A2[1:]+GAMES[:2]+RECAP[:_clo+1]+GAMES[2:]+RECAP[_clo+1:]

if __name__=='__main__':
    install_chrome()
    out=HERE.parent.parent/'lessons-6'; out.mkdir(exist_ok=True)
    print(build_interactive(L6,str(out/'lesson6_v1.html'),title='SkillsXLab · Lesson 6 · Washed Ashore (grey box)'))
    tot=sum(s.get('min',0) for s in L6 if not s.get('optional'))
    print('core minutes',tot, 'slides',len(L6))
