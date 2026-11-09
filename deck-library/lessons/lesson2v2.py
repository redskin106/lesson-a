import sys; sys.path.insert(0,'/home/claude/work/lesson')
G=lambda c,t:(c,t,True); C=lambda c,t:(c,t,False)
E_,S_,A_='ENGAGE','STUDY','ACTIVATE'
spec=[
 {'m':'cause_chain','phase':S_,'title':'Why?','rows':[
   {'cause':'l2c_1_cause.jpg','effect':'l2c_1_effect.jpg','sent':[('c1','My stomach hurts'),('c4','because'),('c1','I'),('c2','ate'),('c3','spicy food.')]},
   {'cause':'l2c_2_cause.jpg','effect':'l2c_2_effect.jpg','sent':[('c1','I have a cold'),('c4','because'),('c1','I'),('c2','went'),('c3','out in the rain.')]}]},
 {'m':'sort','phase':S_,'title':'Why does it hurt?','bank':['ate','went','slept','fell','eat','go','sleep','fall'],'rows':[
   {'pic':'l2c_1_effect.jpg','pre':('c4','because I'),'end':('c3','spicy food.'),'ans':['ate']},
   {'pic':'l2c_2_effect.jpg','pre':('c4','because I'),'end':('c3','out in the rain.'),'ans':['went']},
   {'pic':'l2c_3_effect.jpg','pre':('c4','because I'),'end':('c3','on the floor.'),'ans':['slept']},
   {'pic':'l2c_4_effect.jpg','pre':('c4','because I'),'end':('c3','off a bike.'),'ans':['fell']}]},
 {'m':'pick','phase':S_,'title':'Why?','effect':'l2c_5_effect.jpg','options':['l2c_6_cause.jpg','l2c_5_cause.jpg','l2c_3_cause.jpg'],'ok':1},
 {'m':'chat','phase':S_,'title':'The nurse asks','window':4,'lines':[
   ('N','What’s wrong?'),('P','My stomach hurts.'),('N','Why?'),
   ('P',[C('c4','Because'),C('c1','I'),G('c2','ate'),C('c3','spicy food.')],[('c2','ate'),('c2','eat'),('c2','went'),('c2','slept')])]},
]
