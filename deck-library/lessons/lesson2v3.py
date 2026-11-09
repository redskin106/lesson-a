import sys; sys.path.insert(0,'/home/claude/work/lesson')
G=lambda c,t:(c,t,True); C=lambda c,t:(c,t,False)
E_,S_,A_='ENGAGE','STUDY','ACTIVATE'
BECAUSE=('c4','because')
spec=[
 # ---------- ENGAGE ----------
 {'m':'cover','phase':E_,'title':'Lesson <span class="grad">2</span>','phases':['Engage','Study','Activate'],'active':0,
  'cards':[{'pic':'v3_back.jpg','x':1010,'y':150,'w':330,'h':430,'r':-7},{'pic':'v3_stomach.jpg','x':1290,'y':300,'w':330,'h':430,'r':4},{'pic':'v3_head.jpg','x':1500,'y':120,'w':330,'h':430,'r':-3}]},
 {'m':'pic_question','phase':E_,'pic':'v3_back.jpg','q':('What’s',['wrong?'])},
 {'m':'pic_rows','phase':E_,'title':'Why?','rows':[{'label':'Why?','grad':'violet','chips':[('c1','My back hurts'),BECAUSE,('c1','I'),('c2','slept'),('c3','on the floor.')],'pics':['v3_hook1.jpg','v3_hook2.jpg','v3_hook3.jpg']}]},
 # ---------- STUDY ----------
 {'m':'cast','phase':S_,'title':'Where does it hurt?','items':[
   {'pic':'v3p_head.jpg','label':'My head hurts','grad':'violet','fit':'contain'},{'pic':'v3p_stomach.jpg','label':'My stomach hurts','grad':'violet','fit':'contain'},
   {'pic':'v3p_back.jpg','label':'My back hurts','grad':'violet','fit':'contain'},{'pic':'v3p_arm.jpg','label':'My arm hurts','grad':'violet','fit':'contain'}]},
 {'m':'today','phase':S_,'emoji':'thinking_face','title':'Now and before','fs':34,'rows':[
   {'icon':'red_question_mark','chips':[('c4','Why?')]},
   {'icon':'hot_pepper','chips':[('c1','My stomach'),('c2','hurts'),('c4','because'),('c1','I'),('c2','ate'),('c3','spicy food.')]}]},
 {'m':'contrast','phase':S_,'title':'Does your head hurt?','left':{'label':'Statement','grad':'violet','pic':'v3_head.jpg','fit':'contain','chips':[('c1','My head'),('c2','hurts.')]},
   'right':{'label':'Question','grad':'teal','pic':'v3_head.jpg','fit':'contain','chips':[('c2','Does'),('c1','your head'),('c2','hurt?')]}},
 {'m':'chat','phase':S_,'title':'The nurse asks','window':4,'lines':[
   ('N','What’s wrong?'),('P','My head hurts.'),
   ('N',[C('c2','Does'),C('c1','your head'),G('c2','hurt?')],[('c2','hurt?'),('c2','hurts?')]),('P','Yes, it does.'),
   ('N',[C('c2','Does'),C('c1','your back'),G('c2','hurt?')],[('c2','hurt?'),('c2','hurts?')]),('P','No, my back is fine.')]},
 {'m':'verb_pairs','phase':S_,'title':'Yesterday','rows':[
   {'pic':'v2_eat.jpg','now':'eat','then':'ate'},{'pic':'v2_drink.jpg','now':'drink','then':'drank'},{'pic':'v2_sleep.jpg','now':'sleep','then':'slept'},
   {'pic':'v2_fall.jpg','now':'fall','then':'fell'},{'pic':'v2_go.jpg','now':'go','then':'went'}]},
 {'m':'verb_pairs','phase':S_,'title':'Yesterday · more','optional':True,'rows':[
   {'pic':'v2_take.jpg','now':'take','then':'took'},{'pic':'v2_feel.jpg','now':'feel','then':'felt'},{'pic':'v2_have.jpg','now':'have','then':'had'},{'pic':'v2_start.jpg','now':'start','then':'started'}]},
 {'m':'contrast','phase':S_,'title':'Every day and yesterday','left':{'label':'Every day','grad':'sky','pic':'v2_rice.jpg','fit':'contain','chips':[('c1','I'),('c2','eat'),('c3','rice.')]},
   'right':{'label':'Yesterday','grad':'rose','pic':'l2c_1_cause.jpg','fit':'contain','chips':[('c1','I'),('c2','ate'),('c3','spicy food.')]}},
 {'m':'sort','phase':S_,'title':'Why does it hurt?','bank':['ate','went','slept','fell','eat','go','sleep','fall'],'rows':[
   {'pic':'l2c_1_effect.jpg','pre':('c4','because I'),'end':('c3','spicy food.'),'ans':['ate']},
   {'pic':'l2c_2_effect.jpg','pre':('c4','because I'),'end':('c3','out in the rain.'),'ans':['went']},
   {'pic':'l2c_3_effect.jpg','pre':('c4','because I'),'end':('c3','on the floor.'),'ans':['slept']},
   {'pic':'l2c_4_effect.jpg','pre':('c4','because I'),'end':('c3','off a bike.'),'ans':['fell']}]},
 {'m':'sort','phase':S_,'title':'Why? (2)','optional':True,'bank':['drank','took','drink','take'],'rows':[
   {'pic':'l2c_5_effect.jpg','pre':('c4','because I'),'end':('c3','too much coffee.'),'ans':['drank']},
   {'pic':'l2c_6_effect.jpg','pre':('c4','because I'),'end':('c3','medicine.'),'ans':['took']}]},
 {'m':'contrast','phase':S_,'title':'I ate. Did you eat?','left':{'label':'Statement','grad':'violet','pic':'l2c_1_cause.jpg','chips':[('c1','I'),('c2','ate'),('c3','spicy food.')]},
   'right':{'label':'Question','grad':'teal','pic':'l2c_1_cause.jpg','chips':[('c2','Did'),('c1','you'),('c2','eat'),('c3','spicy food?')]}},
 {'m':'pic_rows','phase':S_,'title':'Now and yesterday','rows':[
   {'label':'Now','grad':'sky','chips':[('c2','Does'),('c1','your stomach'),('c2','hurt?')],'pics':['v3_stomach.jpg','v3_m2.jpg','v3_m3.jpg'],'cap':'Yes, it does.'},
   {'label':'Yesterday','grad':'rose','chips':[('c2','Did'),('c1','you'),('c2','eat'),('c3','spicy food?')],'pics':['v3_m4.jpg','v3_m5.jpg','v3_m6.jpg'],'cap':'Yes, I did.'}]},
 {'m':'connect','phase':S_,'title':'Connect','rows':[
   {'cause':'l2c_1_cause.jpg','now':'l2c_1_effect.jpg','adv':'v3_adv_1.jpg','c':[('c1','I'),('c2','ate'),('c3','spicy food.')],'n':[('c1','My stomach'),('c2','hurts')],'a':[('c2','Drink'),('c3','water.')]},
   {'cause':'l2c_3_cause.jpg','now':'l2c_3_effect.jpg','adv':'v3_adv_2.jpg','c':[('c1','I'),('c2','slept'),('c3','on the floor.')],'n':[('c1','My back'),('c2','hurts')],'a':[('c2','Sleep'),('c3','on a bed.')]},
   {'cause':'l2c_4_cause.jpg','now':'l2c_4_effect.jpg','adv':'v3_adv_3.jpg','c':[('c1','I'),('c2','fell'),('c3','off a bike.')],'n':[('c1','My arm'),('c2','hurts')],'a':[('c2','Rest'),('c3','your arm.')]},
   {'cause':'l2c_2_cause.jpg','now':'l2c_2_effect.jpg','adv':'v3_adv_4.jpg','c':[('c1','I'),('c2','went'),('c3','out in the rain.')],'n':[('c1','I'),('c2','have'),('c3','a cold')],'a':[('c2','Stay'),('c3','warm.')]}]},
 {'m':'chat','phase':S_,'title':'Help the robot nurse','window':4,'avatars':{'N':'robot'},'lines':[
   ('N',[C('c2','Does'),C('c1','your arm'),G('c2','hurt?')],[('c2','hurt?'),('c2','hurts?')]),('P','Yes, it does.'),
   ('N',[C('c2','Did'),C('c1','you'),G('c2','fall?')],[('c2','fall?'),('c2','fell?')]),('P','Yes, I did.'),
   ('N',[C('c2','Did'),C('c1','you'),G('c2','drink'),C('c3','coffee?')],[('c2','drink'),('c2','drank')]),('P','Yes, I did.')]},
 {'m':'chat','phase':S_,'title':'The nurse asks','window':4,'lines':[
   ('N','What’s wrong?'),('P','My stomach hurts.'),('N','Why?'),
   ('P',[C('c4','Because'),C('c1','I'),G('c2','ate'),C('c3','spicy food.')],[('c2','ate'),('c2','eat'),('c2','went'),('c2','slept')]),
   ('N','When did it start?'),('P','Last night.'),
   ('N',[C('c2','Did'),C('c1','you'),G('c2','eat'),C('c3','anything?')],[('c2','eat'),('c2','ate')]),
   ('P','Yes, I did.')]},
 {'m':'pick','phase':S_,'title':'Why?','optional':True,'effect':'l2c_5_effect.jpg','options':['l2c_6_cause.jpg','l2c_5_cause.jpg','l2c_3_cause.jpg'],'ok':1},
 {'m':'pick','phase':S_,'title':'Why?','optional':True,'effect':'l2c_2_effect.jpg','options':['l2c_5_cause.jpg','l2c_4_cause.jpg','l2c_2_cause.jpg'],'ok':2},
 {'m':'timer','phase':S_,'title':'Your turn','optional':True,'min':2,'icons':['face_with_thermometer'],'note':'Tell your partner one thing you did yesterday.'},
 # ---------- ACTIVATE ----------
 {'m':'title_card','phase':A_,'line1':'The','line2':'Clinic','arch':[('woman_health_worker',1450,480,300,8),('face_with_thermometer',1280,640,260,-6),('stethoscope',1290,230,380,-8)]},
 {'m':'role_cards','phase':A_,'title':'Groups of five · pass the ball','cards':[
   {'emoji':'face_with_thermometer','name':'Patient','grad':'rose','job':'mimes the pain, answers'},
   {'emoji':'woman_health_worker','name':'Nurse','grad':'teal','job':'asks where it hurts'},
   {'emoji':'man_health_worker','name':'Doctor','grad':'violet','job':'asks why'}],
  'qs':[('c2','Does'),('c1','your head'),('c2','hurt?'),('c2','Did'),('c1','you'),('c2','sleep?')]},
 {'m':'chat','phase':A_,'title':'Watch the circle','window':5,'lines':[
   ('P','My stomach hurts.'),('N','Does your stomach hurt?'),('P','Yes, it does.'),('D','Did you eat spicy food?'),('P','Yes, I did.'),('D','His stomach hurts because he ate spicy food.')]},
 {'m':'timer','phase':A_,'title':'Think','min':1,'icons':['thinking_face','face_with_thermometer'],'note':'Choose one pain. Choose one cause. Keep it secret.'},
 {'m':'ball_circle','phase':A_,'title':'The ball circle','min':10,
  'stations':[{'emoji':'face_with_thermometer','name':'Patient','grad':'rose','chips':[('c1','My head'),('c2','hurts.')]},
              {'emoji':'woman_health_worker','name':'Nurse','grad':'teal','chips':[('c2','Does'),('c1','your head'),('c2','hurt?')]},
              {'emoji':'man_health_worker','name':'Doctor','grad':'violet','chips':[('c2','Did'),('c1','you'),('c2','sleep…?')]}],
  'pain':[('v3s_head.jpg','head'),('v3s_stomach.jpg','stomach'),('v3s_back.jpg','back'),('v3s_arm.jpg','arm')],
  'verbs':[('v2_eat.jpg','ate'),('v2_drink.jpg','drank'),('v2_sleep.jpg','slept'),('v2_fall.jpg','fell'),('v2_go.jpg','went')]},
 {'m':'contrast','phase':A_,'title':'Silver · habits','optional':True,'left':{'label':'Every day','grad':'sky','pic':'l2c_1_cause.jpg','chips':[('c2','Do'),('c1','you'),('c2','eat'),('c3','spicy food?')]},
   'right':{'label':'Yesterday','grad':'rose','pic':'l2c_1_cause.jpg','chips':[('c2','Did'),('c1','you'),('c2','eat'),('c3','spicy food?')]}},
 {'m':'recap','phase':'RECAP','rows':[([('c1','My stomach'),('c2','hurts.')],'now'),([('c4','because'),('c1','I'),('c2','ate'),('c3','spicy food.')],'yesterday'),([('c2','Does'),('c1','your stomach'),('c2','hurt?')],'ask'),([('c2','Did'),('c1','you'),('c2','eat'),('c3','spicy food?')],'ask')],'emoji':'face_with_thermometer'},
 {'m':'closing','phase':E_,'stack':True,'line1':'Thank','line2':'you!','sub':'See you next time.','emoji':'waving_hand'},
]
from lessons.plan import L2V3,apply
apply(spec,[r for r in L2V3])
