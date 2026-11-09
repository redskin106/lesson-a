import sys; sys.path.insert(0,'/home/claude/work/lesson')
G=lambda c,t:(c,t,True); C=lambda c,t:(c,t,False)
E_,S_,A_='ENGAGE','STUDY','ACTIVATE'
BECAUSE=('c4','because')
spec=[
 # ---------- ENGAGE ----------
 {'m':'cover','phase':E_,'title':'Lesson <span class="grad">2</span>','phases':['Engage','Study','Activate'],'active':0,
  'cards':[{'pic':'l2c_1_effect.jpg','x':1010,'y':150,'w':330,'h':430,'r':-7},{'pic':'l2c_2_effect.jpg','x':1290,'y':300,'w':330,'h':430,'r':4},{'pic':'l2c_4_effect.jpg','x':1500,'y':120,'w':330,'h':430,'r':-3}]},
 {'m':'pic_question','phase':E_,'pic':'l2c_1_effect.jpg','q':('What',['happened?'])},
 # ---------- STUDY ----------
 {'m':'cast','phase':S_,'title':'Where does it hurt?','items':[
   {'pic':'l2c_1_effect.jpg','label':'stomach ache','grad':'violet','fit':'contain'},{'pic':'l2c_2_effect.jpg','label':'a cold','grad':'violet','fit':'contain'},
   {'pic':'l2c_3_effect.jpg','label':'back pain','grad':'violet','fit':'contain'},{'pic':'l2c_4_effect.jpg','label':'a sore arm','grad':'violet','fit':'contain'}]},
 {'m':'cause_chain','phase':S_,'title':'Why?','rows':[
   {'cause':'l2c_1_cause.jpg','effect':'l2c_1_effect.jpg','sent':[('c1','My stomach hurts'),BECAUSE,('c1','I'),('c2','ate'),('c3','spicy food.')]},
   {'cause':'l2c_2_cause.jpg','effect':'l2c_2_effect.jpg','sent':[('c1','I have a cold'),BECAUSE,('c1','I'),('c2','went'),('c3','out in the rain.')]}]},
 {'m':'cause_chain','phase':S_,'title':'Why?','rows':[
   {'cause':'l2c_3_cause.jpg','effect':'l2c_3_effect.jpg','sent':[('c1','My back hurts'),BECAUSE,('c1','I'),('c2','slept'),('c3','on the floor.')]},
   {'cause':'l2c_4_cause.jpg','effect':'l2c_4_effect.jpg','sent':[('c1','My arm hurts'),BECAUSE,('c1','I'),('c2','fell'),('c3','off a bike.')]}]},
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
 {'m':'pick','phase':S_,'title':'Why?','effect':'l2c_5_effect.jpg','options':['l2c_6_cause.jpg','l2c_5_cause.jpg','l2c_3_cause.jpg'],'ok':1},
 {'m':'pick','phase':S_,'title':'Why?','optional':True,'effect':'l2c_2_effect.jpg','options':['l2c_5_cause.jpg','l2c_4_cause.jpg','l2c_2_cause.jpg'],'ok':2},
 {'m':'chat','phase':S_,'title':'The nurse asks','window':4,'lines':[
   ('N','What’s wrong?'),('P','My stomach hurts.'),('N','Why?'),
   ('P',[C('c4','Because'),C('c1','I'),G('c2','ate'),C('c3','spicy food.')],[('c2','ate'),('c2','eat'),('c2','went'),('c2','slept')]),
   ('N',[C('c4','When'),C('c2','did'),C('c1','it'),G('c2','start?')],[('c2','start?'),('c2','started?')]),
   ('P','Last night.'),
   ('N',[C('c2','Did'),C('c1','you'),G('c2','eat'),C('c3','anything?')],[('c2','eat'),('c2','ate')]),
   ('P','Yes, I did.')]},
 # ---------- ACTIVATE ----------
 {'m':'role_cards','phase':A_,'title':'Pairs · the nurse does not know why','cards':[
   {'emoji':'face_with_thermometer','name':'Patient','grad':'rose','job':'knows the cause'},
   {'emoji':'woman_health_worker','name':'Nurse','grad':'teal','job':'asks why'}],
  'qs':[('c4','What’s'),('c2','wrong?'),('c4','Why?'),('c4','When'),('c2','did'),('c1','it'),('c2','start?')]},
 {'m':'cast','phase':A_,'title':'Choose a patient','items':[
   {'pic':'l2c_1_effect.jpg','label':'Patient 1','fit':'contain'},{'pic':'l2c_2_effect.jpg','label':'Patient 2','fit':'contain'},
   {'pic':'l2c_3_effect.jpg','label':'Patient 3','fit':'contain'},{'pic':'l2c_4_effect.jpg','label':'Patient 4','fit':'contain'}]},
 {'m':'slot','phase':A_,'optional':True,'heads':['PROBLEM','PAIN','CAUSE'],'rows':[('nauseated_face',3,'hot_pepper',1),('sneezing_face',2,'cloud_with_rain',1),('grimacing_face',4,'bed',1),('face_with_head-bandage',3,'bicycle',1),('shaking_face',2,'hot_beverage',1)]},
 {'m':'timer','phase':A_,'title':'Find the cause','min':12,'icons':['woman_health_worker','face_with_thermometer'],'note':'Nurse asks. Patient answers. Swap.'},
 {'m':'solved_board','phase':A_,'title':'Patients helped','footer':'Every patient helped by the class.','items':[
   {'pic':'l2c_1_effect.jpg','solved':True},{'pic':'l2c_2_effect.jpg','solved':True},{'pic':'l2c_3_effect.jpg'},{'pic':'l2c_4_effect.jpg'}]},
 {'m':'closing','phase':E_,'stack':True,'line1':'Thank','line2':'you!','sub':'See you next time.','emoji':'waving_hand'},
]
from lessons.plan import L2V2,apply
apply(spec,[r for r in L2V2])
