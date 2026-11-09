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
 {'m':'today','phase':S_,'emoji':'thinking_face','title':'Reasons','fs':70,'rows':[
   {'icon':'red_question_mark','chips':[('c4','Why'),('c2','does'),('c1','it'),('c2','hurt?')]},
   {'icon':'hot_pepper','chips':[('c4','Because'),('c1','I'),('c2','ate'),('c3','spicy food.')]}]},
 {'m':'cast','phase':S_,'title':'Where does it hurt?','items':[
   {'pic':'v3p_head.jpg','label':'My head hurts','grad':'violet','fit':'contain','cap':'headache'},{'pic':'v3p_stomach.jpg','label':'My stomach hurts','grad':'violet','fit':'contain','cap':'stomachache'},
   {'pic':'v3p_back.jpg','label':'My back hurts','grad':'violet','fit':'contain','cap':'backache'},{'pic':'v3p_arm.jpg','label':'My arm hurts','grad':'violet','fit':'contain'}]},
 {'m':'contrast','phase':S_,'title':'Does your head hurt?','left':{'label':'Statement','grad':'violet','pic':'v3_head.jpg','fit':'contain','chips':[('c1','My head'),('c2','hurts.')]},
   'right':{'label':'Question','grad':'teal','pic':'v3_head.jpg','fit':'contain','chips':[('c2','Does'),('c1','your head'),('c2','hurt?')]}},
 {'m':'chat','phase':S_,'title':'The nurse asks','window':4,'lines':[
   ('N','What’s wrong?'),('P',{'img':'v3_head.jpg'}),
   ('N',[C('c2','Does'),C('c1','your head'),G('c2','hurt?')],[('c2','hurt?'),('c2','hurts?')]),('P',{'img':'v3_yes.jpg'}),
   ('N',[C('c2','Does'),C('c1','your stomach'),G('c2','hurt?')],[('c2','hurt?'),('c2','hurts?')]),('P',{'img':'v3_no.jpg'})]},
 {'m':'verb_pairs','phase':S_,'title':'Yesterday','rows':[
   {'pic':'v2_eat.jpg','now':'eat','then':'ate'},{'pic':'v2_drink.jpg','now':'drink','then':'drank'},{'pic':'v2_sleep.jpg','now':'sleep','then':'slept'},
   {'pic':'v2_fall.jpg','now':'fall','then':'fell'},{'pic':'v2_go.jpg','now':'go','then':'went'}]},
 {'m':'verb_pairs','phase':S_,'title':'Yesterday · more','optional':True,'rows':[
   {'pic':'v2_take.jpg','now':'take','then':'took'},{'pic':'v2_feel.jpg','now':'feel','then':'felt'},{'pic':'v2_have.jpg','now':'have','then':'had'},{'pic':'v2_start.jpg','now':'start','then':'started'}]},
 {'m':'contrast','phase':S_,'title':'Yesterday and today','left':{'label':'Yesterday','grad':'rose','pic':'l2c_1_cause.jpg','fit':'contain','chips':[('c1','I'),('c2','ate'),('c3','spicy food.')]},
   'right':{'label':'Today','grad':'sky','pic':'v2_rice.jpg','fit':'contain','chips':[('c1','I'),('c2','eat'),('c3','rice.')]}},
 {'m':'sort','phase':S_,'title':'Why does it hurt? (1)','bank':['sleep','ate','fall','fell','eat','slept'],'rows':[
   {'pic':'l2c_1_effect.jpg','pre':('c4','Because I'),'end':('c3','spicy food.'),'ans':['ate']},
   {'pic':'l2c_3_effect.jpg','pre':('c4','Because I'),'end':('c3','on the floor.'),'ans':['slept']},
   {'pic':'l2c_4_effect.jpg','pre':('c4','Because I'),'end':('c3','off a bike.'),'ans':['fell']}]},
 {'m':'sort','phase':S_,'title':'Why does it hurt? (2)','bank':['took','go','drink','take','went','drank'],'rows':[
   {'pic':'l2c_2_effect.jpg','pre':('c4','Because I'),'end':('c3','out in the rain.'),'ans':['went']},
   {'pic':'l2c_5_effect.jpg','pre':('c4','Because I'),'end':('c3','too much coffee.'),'ans':['drank']},
   {'pic':'l2c_6_effect.jpg','pre':('c4','Because I'),'end':('c3','medicine.'),'ans':['took']}]},
 {'m':'contrast','phase':S_,'title':'I ate. Did you eat?','left':{'label':'Statement','grad':'violet','pic':'l2c_1_cause.jpg','chips':[('c1','I'),('c2','ate'),('c3','spicy food.')]},
   'right':{'label':'Question','grad':'teal','pic':'l2c_1_cause.jpg','chips':[('c2','Did'),('c1','you'),('c2','eat'),('c3','spicy food?')]}},
 {'m':'rules','phase':S_,'title':'Three little rules','emoji':'light_bulb','rows':[
   ([('c2','Does','V'),('c1','your head','S'),('c2','hurt?','V')],'Does → hurt'),
   ([('c2','Did','V'),('c1','you','S'),('c2','eat?','V')],'Did → eat'),
   ([('c4','Because','B'),('c1','I','S'),('c2','ate','V'),('c3','spicy food.','O')],'because → why')]},
 {'m':'contrast','phase':S_,'title':'Silver · habits','optional':True,'left':{'label':'Every day','grad':'sky','pic':'l2c_1_cause.jpg','chips':[('c2','Do'),('c1','you'),('c2','eat'),('c3','spicy food?')]},
   'right':{'label':'Yesterday','grad':'rose','pic':'l2c_1_cause.jpg','chips':[('c2','Did'),('c1','you'),('c2','eat'),('c3','spicy food?')]}},
 {'m':'pic_rows','phase':S_,'title':'Now and yesterday','rows':[
   {'label':'Now','grad':'sky','chips':[('c2','Does'),('c1','your stomach'),('c2','hurt?')],'pics':['v3_stomach.jpg','v3_m2.jpg','v3_m3.jpg'],'cap':'Yes, it does.'},
   {'label':'Yesterday','grad':'rose','chips':[('c2','Did'),('c1','you'),('c2','eat'),('c3','spicy food?')],'pics':['v3_m4.jpg','v3_m5.jpg','v3_m6.jpg'],'cap':'Yes, I did.'}]},
 {'m':'connect','phase':S_,'title':'Connect','rows':[
   {'cause':'l2c_1_cause.jpg','now':'l2c_1_effect.jpg','adv':'v3_adv_1.jpg','c':[('c1','I'),('c2','ate'),('c3','spicy food.')],'n':[('c1','My stomach'),('c2','hurts')],'a':[('c2','Drink'),('c3','water.')]},
   {'cause':'l2c_3_cause.jpg','now':'l2c_3_effect.jpg','adv':'v3_adv_2.jpg','c':[('c1','I'),('c2','slept'),('c3','on the floor.')],'n':[('c1','My back'),('c2','hurts')],'a':[('c2','Sleep'),('c3','on a bed.')]},
   {'cause':'l2c_4_cause.jpg','now':'l2c_4_effect.jpg','adv':'v3_adv_3.jpg','c':[('c1','I'),('c2','fell'),('c3','off a bike.')],'n':[('c1','My arm'),('c2','hurts')],'a':[('c2','Rest'),('c3','your arm.')]}]},
 {'m':'chat','phase':S_,'title':'Help the robot nurse','window':4,'avatars':{'N':'robot'},'lines':[
   ('P',{'img':'v3_arm.jpg'}),
   ('N',[C('c2','Does'),C('c1','your arm'),G('c2','hurt?')],[('c2','hurt?'),('c2','hurts?')]),('P',{'img':'v3_yes.jpg'}),
   ('N',[C('c2','Did'),C('c1','you'),G('c2','fall?')],[('c2','fall?'),('c2','fell?')]),('P',{'img':'l2c_4_cause.jpg'}),
   ('N',[C('c2','Did'),C('c1','you'),G('c2','go'),C('c3','to hospital?')],[('c2','go'),('c2','went')]),('P',{'img':'v3_hospital.jpg'})]},
 {'m':'chat','phase':S_,'title':'The nurse asks','window':4,'lines':[
   ('N','What’s wrong?'),('P',{'img':'v3_stomach.jpg'}),
   ('N',[C('c2','Did'),C('c1','you'),G('c2','eat'),C('c3','anything?')],[('c2','eat'),('c2','ate')]),('P',{'img':'l2c_1_cause.jpg'}),
   ('N','Why does it hurt?'),
   ('P',[C('c4','Because'),C('c1','I'),G('c2','ate'),C('c3','spicy food.')],[('c2','ate'),('c2','eat'),('c2','went'),('c2','slept')])]},
 {'m':'pick','phase':S_,'title':'Why does it hurt?','optional':True,'effect':'l2c_5_effect.jpg','options':['l2c_6_cause.jpg','l2c_5_cause.jpg','l2c_3_cause.jpg'],'ok':1,'say':[('c4','Because'),('c1','I'),('c2','drank'),('c3','too much coffee.')]},
 {'m':'pick','phase':S_,'title':'Why does it hurt?','optional':True,'effect':'l2c_2_effect.jpg','options':['l2c_5_cause.jpg','l2c_4_cause.jpg','l2c_2_cause.jpg'],'ok':2,'say':[('c4','Because'),('c1','I'),('c2','went'),('c3','out in the rain.')]},
 {'m':'timer','phase':S_,'title':'Your turn','optional':True,'min':2,'icons':['face_with_thermometer'],'note':'Tell your partner one thing you did yesterday.'},
 # ---------- ACTIVATE ----------
 {'m':'title_card','phase':A_,'line1':'The','line2':'Clinic','arch':[('woman_health_worker',1450,480,300,8),('face_with_thermometer',1280,640,260,-6),('stethoscope',1290,230,380,-8)]},
 {'m':'role_cards','phase':A_,'title':'Three jobs · pass the ball','cards':[
   {'emoji':'face_with_thermometer','name':'Patient','grad':'rose','job':'mimes the pain','says':[('c1','My head'),('c2','hurts.')]},
   {'emoji':'woman_health_worker','name':'Nurse','grad':'teal','job':'asks about now','says':[('c2','Does'),('c1','your head'),('c2','hurt?')]},
   {'emoji':'man_health_worker','name':'Doctor','grad':'violet','job':'asks about before','says':[('c2','Did'),('c1','you'),('c2','sleep'),('c3','badly?')]}]},
 {'m':'chat','phase':A_,'title':'Watch the circle','window':5,'lines':[
   ('P',{'img':'v3_stomach.jpg'}),('N','Does your stomach hurt?'),('P','Yes, it does.'),('D','Did you eat spicy food?',None,'l2c_1_cause.jpg'),('P','Yes, I did.'),('D','His stomach hurts because he ate spicy food.')]},
 {'m':'timer','phase':A_,'title':'Think','min':1,'icons':['thinking_face','face_with_thermometer'],'note':'Choose one pain. Choose one cause. Keep it secret.'},
 {'m':'ball_circle','phase':A_,'title':'The ball circle','min':10,
  'stations':[{'emoji':'face_with_thermometer','name':'Patient','grad':'rose','chips':[('c1','My head'),('c2','hurts.')]},
              {'emoji':'woman_health_worker','name':'Nurse','grad':'teal','chips':[('c2','Does'),('c1','your head'),('c2','hurt?')]},
              {'emoji':'man_health_worker','name':'Doctor','grad':'violet','chips':[('c2','Did'),('c1','you'),('c2','sleep…?')]}],
  'pain':[('v3s_head.jpg','head'),('v3s_stomach.jpg','stomach'),('v3s_back.jpg','back'),('v3s_arm.jpg','arm')],
  'verbs':[('v2_eat.jpg','ate'),('v2_drink.jpg','drank'),('v2_sleep.jpg','slept'),('v2_fall.jpg','fell'),('v2_go.jpg','went')]},
 {'m':'recap','phase':'RECAP','rows':[([('c1','My stomach'),('c2','hurts.')],'now'),([('c4','Because'),('c1','I'),('c2','ate'),('c3','spicy food.')],'yesterday'),([('c2','Does'),('c1','your stomach'),('c2','hurt?')],'ask'),([('c2','Did'),('c1','you'),('c2','eat'),('c3','spicy food?')],'ask')],'emoji':'face_with_thermometer'},
 {'m':'closing','phase':E_,'stack':True,'line1':'Thank','line2':'you!','sub':'See you next time.','emoji':'waving_hand'},
]
from lessons.plan import L2V3,apply
apply(spec,[r for r in L2V3])
