import sys; sys.path.insert(0,'/home/claude/work/lesson')
G=lambda c,t:(c,t,True); C=lambda c,t:(c,t,False)
E_,S_,A_='ENGAGE','STUDY','ACTIVATE'
BECAUSE=('c4','because')
spec=[
 # ---------- ENGAGE ----------
 {'m':'cover','phase':E_,'title':'Lesson <span class="grad">2</span>','phases':['Engage','Study','Activate'],'active':0,
  'cards':[{'pic':'v3_head.jpg','x':1530,'y':110,'w':330,'h':430,'r':4},{'pic':'v3_back.jpg','x':1010,'y':150,'w':330,'h':430,'r':-7},{'pic':'v3_stomach.jpg','x':1250,'y':330,'w':330,'h':430,'r':3}]},
 {'m':'pic_question','phase':E_,'pic':'v3_back.jpg','q':('What’s',['wrong?'])},
 {'m':'pic_rows','phase':E_,'title':'','rows':[{'label':'Why does it hurt?','grad':'violet','chips':[('c4','Because'),('c1','I'),('c2','slept'),('c3','on the floor.')],'pics':['v3_hook1.jpg','v3_hook2.jpg','v3_hook3.jpg']}]},
 # ---------- STUDY ----------
 {'m':'today','phase':S_,'emoji':'thinking_face','title':'Then and now','fs':62,'rows':[
   {'icon':'face_with_thermometer','chips':[('c1','My stomach'),('c2','hurts.')]},
   {'icon':'red_question_mark','chips':[('c4','Why'),('c2','does'),('c1','it'),('c2','hurt?')]},
   {'icon':'hot_pepper','chips':[('c4','Because'),('c1','I'),('c2','ate'),('c3','spicy food.')]}]},
 {'m':'cast','phase':S_,'title':'Where does it hurt?','items':[
   {'pic':'v3p_head.jpg','label':'My head hurts','grad':'violet','fit':'contain','cap':'headache'},{'pic':'v3p_stomach.jpg','label':'My stomach hurts','grad':'violet','fit':'contain','cap':'stomachache'},
   {'pic':'v3p_back.jpg','label':'My back hurts','grad':'violet','fit':'contain','cap':'backache'},{'pic':'v3p_arm.jpg','label':'My arm hurts','grad':'violet','fit':'contain'}]},
 {'m':'contrast','phase':S_,'title':'Asking questions','left':{'label':'Statement','grad':'violet','pic':'v3_head.jpg','fit':'contain','chips':[('c1','My head'),('c2','hurts.')]},
   'right':{'label':'Question','grad':'teal','qmark':True,'pic':'v3_head.jpg','fit':'contain','chips':[('c2','Does'),('c1','your head'),('c2','hurt?')]}},
 {'m':'chat','phase':S_,'title':'The nurse guesses','window':4,'lines':[
   ('P',{'img':'l2c_1_cause.jpg'}),
   ('N',[C('c2','Does'),G('c1','your stomach'),C('c2','hurt?')],[('c1','your stomach'),('c1','your head'),('c1','your back')]),
   ('P',[C('c1','Yes, it'),G('c2','does'),C('c4','because'),C('c1','I'),G('c2','ate'),C('c3','spicy food.')],[('c2','does'),('c2','ate'),('c2','do'),('c2','eat')]),
   ('P',{'img':'l2c_3_cause.jpg'}),
   ('N',[C('c2','Does'),G('c1','your back'),C('c2','hurt?')],[('c1','your back'),('c1','your arm'),('c1','your head')]),
   ('P',[C('c1','Yes, it'),G('c2','does'),C('c4','because'),C('c1','I'),G('c2','slept'),C('c3','on the floor.')],[('c2','slept'),('c2','does'),('c2','sleep'),('c2','do')]),
   ('P',{'img':'v3_no.jpg'}),
   ('N',[C('c2','Does'),G('c1','your head'),C('c2','hurt?')],[('c1','your head'),('c1','your arm'),('c1','your back')]),
   ('P',[C('c1','No, it'),G('c2','doesn’t.')],[('c2','doesn’t.'),('c2','does.'),('c2','don’t.'),('c2','didn’t.')])]},
 {'m':'verb_pairs','phase':S_,'kind':'irr','title':'Yesterday','rows':[
   {'pic':'v2_eat.jpg','now':'eat','then':'ate'},{'pic':'v2_drink.jpg','now':'drink','then':'drank'},{'pic':'v2_sleep.jpg','now':'sleep','then':'slept'},
   {'pic':'v2_fall.jpg','now':'fall','then':'fell'},{'pic':'v2_go.jpg','now':'go','then':'went'}]},
 {'m':'verb_pairs','phase':S_,'title':'Yesterday · more','kind':'irr','optional':True,'rows':[
   {'pic':'v2_take.jpg','now':'take','then':'took'},{'pic':'v2_feel.jpg','now':'feel','then':'felt'},{'pic':'v2_have.jpg','now':'have','then':'had'},{'pic':'v2_be.jpg','now':'be','then':'was'}]},
 {'m':'verb_pairs','phase':S_,'title':'Regular verbs','kind':'reg','rows':[
   {'pic':'v2_start.jpg','now':'start','then':'started'},{'pic':'v2_call.jpg','now':'call','then':'called'},{'pic':'v2_cook.jpg','now':'cook','then':'cooked'},{'pic':'v2_walk.jpg','now':'walk','then':'walked'}]},
 {'m':'rules','phase':S_,'title':'Past: two rules','emoji':'hourglass_not_done','rows':[
   ([('c1','I','S'),('c2','ate','V'),('c3','spicy food.','O')],'irregular: eat → ate'),
   ([('c1','I','S'),('c2','was','V'),('c3','tired.','O')],'irregular: be → was'),
   ([('c1','I','S'),('c2','walked','V'),('c3','home.','O')],'regular: walk + ed')]},
 {'m':'contrast','phase':S_,'title':'Yesterday and today','left':{'label':'Yesterday','grad':'rose','pic':'l2c_1_cause.jpg','fit':'contain','chips':[('c1','I'),('c2','ate'),('c3','spicy food.')]},
   'right':{'label':'Today','grad':'sky','pic':'v2_rice.jpg','fit':'contain','chips':[('c1','I'),('c2','eat'),('c3','rice.')]}},
 {'m':'sort','phase':S_,'title':'Why does it hurt? (1)','bank':['sleep','ate','fall','fell','eat','slept'],'rows':[
   {'pic':'l2c_1_effect.jpg','pre':('c4','Because I'),'end':('c3','spicy food.'),'ans':['ate']},
   {'pic':'l2c_3_effect.jpg','pre':('c4','Because I'),'end':('c3','on the floor.'),'ans':['slept']},
   {'pic':'l2c_4_effect.jpg','pre':('c4','Because I'),'end':('c3','off a bike.'),'ans':['fell']}]},
 {'m':'sort','phase':S_,'title':'Why? (2)','bank':['took','go','drink','take','went','drank'],'rows':[
   {'pic':'l2c_2_effect.jpg','pre':('c4','Because I'),'end':('c3','out in the rain.'),'ans':['went']},
   {'pic':'l2c_5_effect.jpg','pre':('c4','Because I'),'end':('c3','too much coffee.'),'ans':['drank']},
   {'pic':'l2c_6_effect.jpg','pre':('c4','Because I'),'end':('c3','medicine.'),'ans':['took']}]},
 {'m':'contrast','phase':S_,'title':'I ate. Did you eat?','left':{'label':'Statement','grad':'violet','pic':'l2c_1_cause.jpg','chips':[('c1','I'),('c2','ate'),('c3','spicy food.')]},
   'right':{'label':'Question','grad':'teal','qmark':True,'pic':'l2c_1_cause.jpg','chips':[('c2','Did'),('c1','you'),('c2','eat'),('c3','spicy food?')]}},
 {'m':'rules','phase':S_,'title':'Three little rules','emoji':'light_bulb','rows':[
   ([('c2','Does','V'),('c1','your head','S'),('c2','hurt?','V')],'Does → hurt'),
   ([('c2','Did','V'),('c1','you','S'),('c2','eat?','V')],'Did → eat'),
   ([('c4','Because','B'),('c1','I','S'),('c2','ate','V'),('c3','spicy food.','O')],'because → why')]},
 {'m':'contrast','phase':S_,'title':'Silver · habits','optional':True,'left':{'label':'Every day','grad':'sky','qmark':True,'pic':'l2c_1_cause.jpg','chips':[('c2','Do'),('c1','you'),('c2','eat'),('c3','spicy food?')]},
   'right':{'label':'Yesterday','grad':'rose','qmark':True,'pic':'l2c_1_cause.jpg','chips':[('c2','Did'),('c1','you'),('c2','eat'),('c3','spicy food?')]}},
 {'m':'connect','phase':S_,'title':'Connect','rows':[
   {'cause':'l2c_1_cause.jpg','now':'l2c_1_effect.jpg','adv':'v3_adv_1.jpg','c':[('c1','I'),('c2','ate'),('c3','spicy food.')],'n':[('c1','My stomach'),('c2','hurts')],'a':[('c2','Drink'),('c3','water.')]},
   {'cause':'l2c_3_cause.jpg','now':'l2c_3_effect.jpg','adv':'v3_adv_2.jpg','c':[('c1','I'),('c2','slept'),('c3','on the floor.')],'n':[('c1','My back'),('c2','hurts')],'a':[('c2','Sleep'),('c3','on a bed.')]},
   {'cause':'l2c_4_cause.jpg','now':'l2c_4_effect.jpg','adv':'v3_adv_3.jpg','c':[('c1','I'),('c2','fell'),('c3','off a bike.')],'n':[('c1','My arm'),('c2','hurts')],'a':[('c2','Rest'),('c3','your arm.')]}]},
 {'m':'spot','phase':S_,'title':'Find the mistakes','lines':[
   ('N',[('c1','His stomach'),('c2','hurts.')]),
   ('D',[('c2','Did'),('c1','he'),('c2','ate','eat'),('c3','spicy food?')]),
   ('N',[('c1','Yes, he'),('c2','did.')]),
   ('D',[('c2','Does'),('c1','his head'),('c2','hurts?','hurt?')]),
   ('N',[('c1','No, it'),('c2','doesn’t.')]),
   ('D',[('c4','Why'),('c2','does'),('c1','it'),('c2','hurt?')]),
   ('N',[('c4','Because'),('c1','he'),('c2','eat','ate'),('c3','spicy food.')])]},
 {'m':'chat','phase':S_,'title':'The handover','split':True,'window':5,'lines':[
   ('N','Room 4. His stomach hurts.',None,'v3_stomach.jpg'),
   ('D',[C('c2','Does'),C('c1','his head'),G('c2','hurt?')],[('c2','hurt?'),('c2','hurts?')],'v3_head.jpg'),
   ('N','No, it doesn’t.',None,'v3_no.jpg'),
   ('D','Why does it hurt?',None,'v3_stomach.jpg'),
   ('N',[C('c4','Because'),C('c1','he'),G('c2','ate'),C('c3','spicy food.')],[('c2','ate'),('c2','eat')],'l2c_1_cause.jpg'),
   ('D',[C('c2','Did'),C('c1','he'),G('c2','drink'),C('c3','water?')],[('c2','drink'),('c2','drank')],'v2_drink.jpg'),
   ('N','No, he didn’t.',None,'v3_no.jpg'),
   ('D',[C('c1','He'),C('c2','should'),G('c2','drink'),C('c3','water.')],[('c2','drink'),('c2','drank')],'v3_adv_1.jpg')]},
 {'m':'pick','phase':S_,'title':'Why does it hurt?','optional':True,'steps':True,'effect':'l2c_3_effect.jpg','options':['l2c_5_cause.jpg','l2c_3_cause.jpg','l2c_6_cause.jpg'],'ok':1,'say':[('c4','Because'),('c1','I'),('c2','slept'),('c3','on the floor.')]},
 {'m':'pick','phase':S_,'title':'Why do you have a cold?','q':'Why do you have a cold?','optional':True,'steps':True,'effect':'l2c_2_effect.jpg','options':['l2c_5_cause.jpg','l2c_4_cause.jpg','l2c_2_cause.jpg'],'ok':2,'say':[('c4','Because'),('c1','I'),('c2','went'),('c3','out in the rain.')]},
 {'m':'timer','phase':S_,'title':'Your turn','optional':True,'min':2,'icons':['face_with_thermometer'],'note':'Tell your partner one thing you did yesterday.'},
 # ---------- ACTIVATE ----------
 {'m':'title_card','phase':A_,'line1':'The','line2':'Clinic','arch':[('woman_health_worker',1450,480,300,8),('face_with_thermometer',1280,640,260,-6),('stethoscope',1290,230,380,-8)]},
 {'m':'build','phase':A_,'title':'Build the sentence','pics':['l2c_3_effect.jpg','l2c_3_cause.jpg'],'parts':[('c1','My back'),('c2','hurts'),('c4','because'),('c1','I'),('c2','slept'),('c3','on the floor.')],
  'bank':[('c2','slept'),('c1','I'),('c3','on the floor.'),('c2','hurt'),('c4','because'),('c1','My back'),('c2','sleep'),('c2','hurts')]},
 {'m':'build','phase':A_,'title':'Build the question','optional':True,'pics':[],'fs':70,'bfs':60,'parts':[('c2','Did'),('c1','you'),('c2','eat'),('c3','spicy food?')],
  'bank':[('c3','spicy food?'),('c2','ate'),('c2','Did'),('c1','you'),('c2','eat'),('c2','Does')]},
 {'m':'build','phase':A_,'title':'Build the question','optional':True,'pics':[],'fs':70,'bfs':60,'parts':[('c2','Does'),('c1','your back'),('c2','hurt?')],
  'bank':[('c2','hurt?'),('c1','your back'),('c2','Does'),('c2','hurts?'),('c2','Did'),('c1','my back')]},
 {'m':'build','phase':A_,'title':'Build the question','optional':True,'pics':[],'fs':70,'bfs':60,'parts':[('c2','Did'),('c1','you'),('c2','sleep'),('c3','on the floor?')],
  'bank':[('c3','on the floor?'),('c2','slept'),('c2','Did'),('c1','you'),('c2','sleep'),('c2','Does')]},
 {'m':'make_patient','phase':A_,'title':'Make a patient','min':5,
  'pains':[('v3p_head.jpg','head'),('v3p_stomach.jpg','stomach'),('v3p_back.jpg','back'),('v3p_arm.jpg','arm')],
  'causes':[('l2c_1_cause.jpg','eat','spicy food','ate'),('l2c_3_cause.jpg','sleep','on the floor','slept'),('l2c_4_cause.jpg','fall','off a bike','fell'),('l2c_2_cause.jpg','go','out in the rain','went'),('l2c_5_cause.jpg','drink','too much coffee','drank')]},
 {'m':'role_cards','phase':A_,'title':'Nurse · Doctor · Class','cards':[
   {'emoji':'woman_health_worker','name':'Nurse','grad':'teal','job':'knows the secret','says':[('c1','His stomach'),('c2','hurts.')]},
   {'emoji':'man_health_worker','name':'Doctor','grad':'violet','job':'asks questions','says':[('c2','Did'),('c1','he'),('c2','eat…?')]},
   {'emoji':'soccer_ball','name':'Class','grad':'orange','job':'ball: guess and help','says':[('c4','Because'),('c1','he'),('c2','ate…')]}]},
 {'m':'today','phase':A_,'emoji':'soccer_ball','role':'The class decides','title':'Pass the ball','fs':62,'rows':[
   {'icon':'thinking_face','chips':[('c4','Because'),('c1','he'),('c2','ate'),('c3','spicy food.')]},
   {'icon':'light_bulb','chips':[('c1','He'),('c2','should'),('c2','drink'),('c3','water.')]}]},
 {'m':'timer','phase':A_,'title':'Play','min':10,'icons':['woman_health_worker','man_health_worker','soccer_ball'],'note':'Nurse and doctor talk. The class asks, guesses, helps.'},
 {'m':'recap','phase':'RECAP','rows':[([('c1','My stomach'),('c2','hurts.')],'now'),([('c4','Because'),('c1','I'),('c2','ate'),('c3','spicy food.')],'yesterday'),([('c2','Does'),('c1','your stomach'),('c2','hurt?')],'ask'),([('c2','Did'),('c1','you'),('c2','eat'),('c3','spicy food?')],'ask')],'emoji':'face_with_thermometer'},
 {'m':'closing','phase':E_,'stack':True,'line1':'Thank','line2':'you!','sub':'See you next time.','emoji':'waving_hand'},
]
from lessons.plan import L2V4,apply
apply(spec,[r for r in L2V4])
