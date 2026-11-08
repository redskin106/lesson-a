import sys; sys.path.insert(0,'/home/claude/work/lesson')
import sxl
G=lambda c,t:(c,t,True); C=lambda c,t:(c,t,False)
E_,S_,A_='ENGAGE','STUDY','ACTIVATE'
CASE=lambda n:[f'case{n}_{k}.jpg' for k in range(1,5)]
spec=[
 # ---------- ENGAGE ----------
 {'m':'case_cover','phase':E_,'title':'The Strange<br>Patient','sub':'Case file · past and present'},
 {'m':'evidence_board','phase':E_,'title':'The patient','patient':'l2_sym_ankle.jpg','clues':['clue_cabbage.jpg','clue_onelegged.jpg','clue_fork.jpg'],'question':('What','happened?')},
 {'m':'cast','phase':E_,'title':'Who gave the advice?','items':[
   {'pic':'l2_quack_2.jpg','label':'Neighbour'},{'pic':'l2_quack_3.jpg','label':'Grandma'},{'pic':'l2_quack_1.jpg','label':'Influencer'},{'pic':'l2_quack_4.jpg','label':'Market Uncle'}]},
 # ---------- STUDY ----------
 {'m':'cast','phase':S_,'title':'Where does it hurt?','items':[
   {'pic':'l2_sym_headache.jpg','label':'headache','grad':'violet','fit':'contain'},{'pic':'l2_sym_stomach.jpg','label':'stomach ache','grad':'violet','fit':'contain'},
   {'pic':'l2_sym_ankle.jpg','label':'sprained ankle','grad':'violet','fit':'contain'},{'pic':'l2_sym_rash.jpg','label':'rash','grad':'violet','fit':'contain'}]},
 {'m':'storyboard','phase':S_,'title':'Case 1 · the Neighbour','grad':'amber','panels':CASE(1),'square':True,'prompt':('What','did he do?')},
 {'m':'verb_pairs','phase':S_,'title':'Yesterday · irregular','rows':[
   {'pic':'v_wear.jpg','now':'wear','then':'wore'},{'pic':'v_stand.jpg','now':'stand','then':'stood'},{'pic':'v_eat.jpg','now':'eat','then':'ate'},
   {'pic':'v_drink.jpg','now':'drink','then':'drank'},{'pic':'v_sleep.jpg','now':'sleep','then':'slept'}]},
 {'m':'verb_pairs','phase':S_,'title':'Yesterday · add -ed','rows':[
   {'pic':'v_wash.jpg','now':'wash','then':'washed'},{'pic':'v_rub.jpg','now':'rub','then':'rubbed'},{'pic':'v_paint.jpg','now':'paint','then':'painted'}]},
 {'m':'contrast','phase':S_,'title':'Today and yesterday','left':{'label':'Today','grad':'sky','pic':'v_wear.jpg','fit':'contain','chips':[('c1','I'),('c2','wear'),('c3','a hat.')]},
   'right':{'label':'Yesterday','grad':'violet','pic':'case1_2.jpg','fit':'contain','chips':[('c1','He'),('c2','wore'),('c3','a cabbage.')]}},
 {'m':'sound_sort','phase':S_,'title':'Listen. Which sound?','bags':[{'icon':'dot1','words':['washed']},{'icon':'buzz','words':['rubbed']},{'icon':'dot2','words':['painted']}]},
 {'m':'sound_sort','phase':S_,'title':'The -ed sounds','solved':True,'bags':[{'icon':'dot1','words':['washed']},{'icon':'buzz','words':['rubbed']},{'icon':'dot2','words':['painted']}]},
 {'m':'timeline','phase':S_,'title':'Put the story in order','pics':CASE(1),'order':[2,0,3,1]},
 {'m':'sort','phase':S_,'title':'What did he do?','bank':['wore','stood','ate','slept'],'rows':[
   {'pic':'case1_2.jpg','pre':('c1','He'),'end':('c3','a cabbage hat.')},{'pic':'case1_3.jpg','pre':('c1','He'),'end':('c3','on one leg.')},
   {'pic':'case2_2.jpg','pre':('c1','She'),'end':('c3','ten bananas.')},{'pic':'case4_3.jpg','pre':('c1','He'),'end':('c3','in the garden.')}]},
 {'m':'chat','phase':S_,'title':'The nurse asks','window':4,'lines':[
   ('N',[G('c4','What'),C('c2','did'),C('c1','you'),G('c2','do?')],[('c4','What'),('c4','Where'),('c2','do?'),('c2','did?')]),
   ('P','I wore a cabbage hat.'),
   ('N',[C('c4','When'),C('c2','did'),C('c1','it'),G('c2','start?')],[('c2','start?'),('c2','starts?'),('c2','started?')]),
   ('P','Last night.'),
   ('N',[G('c2','Did'),C('c1','you'),C('c2','sleep'),C('c3','well?')],[('c2','Did'),('c2','Do'),('c2','Does')]),
   ('P','No, I didn’t.')]},
 # ---------- ACTIVATE ----------
 {'m':'role_cards','phase':A_,'title':'Pairs · the nurse cannot see the case','cards':[
   {'emoji':'face_with_thermometer','name':'Patient','grad':'rose','job':'holds the case picture'},
   {'emoji':'woman_health_worker','name':'Nurse','grad':'teal','job':'asks questions'}],
  'qs':[('c4','What'),('c2','did'),('c1','you'),('c2','do?'),('c4','When'),('c2','did'),('c1','it'),('c2','start?')]},
 {'m':'cast','phase':A_,'title':'Choose a case file','items':[
   {'pic':'l2_quack_2.jpg','label':'Case 1'},{'pic':'l2_quack_3.jpg','label':'Case 2'},{'pic':'l2_quack_1.jpg','label':'Case 3'},{'pic':'l2_quack_4.jpg','label':'Case 4'}]},
 {'m':'timeline','phase':A_,'title':'Case 2 · put it in order','pics':CASE(2),'order':[3,1,0,2]},
 {'m':'spot_fib','phase':A_,'title':'True or a fib?','pic':'case2_2.jpg','statements':[([('c1','She'),('c2','ate'),('c3','ten bananas.')],True),([('c1','She'),('c2','drank'),('c3','ten bananas.')],False)]},
 {'m':'match_pairs','phase':A_,'title':'Which diagnosis?','pics':['l2_sym_headache.jpg','l2_sym_stomach.jpg','l2_sym_ankle.jpg','l2_sym_rash.jpg'],'words':['headache','stomach ache','sprained ankle','rash']},
 {'m':'chat','phase':A_,'title':'The doctor gives advice','window':4,'lines':[
   ('D','You have a stomach ache.'),('P','What should I do?'),
   ('D',[G('c2','Don’t eat'),C('c3','ten bananas.')],[('c2','Don’t eat'),('c2','Take'),('c2','Rest')],'adv_nobanana.jpg'),
   ('P','OK.'),
   ('D',[G('c2','Rest')],[('c2','Don’t eat'),('c2','Take'),('c2','Rest')],'adv_rest.jpg'),
   ('P','Yes, doctor.'),
   ('D',[G('c2','Take'),C('c3','this medicine.')],[('c2','Don’t eat'),('c2','Take'),('c2','Rest')],'adv_pill.jpg'),
   ('P','Thank you, doctor.')]},
 {'m':'solved_board','phase':A_,'title':'Cases solved','items':[
   {'pic':'l2_quack_2.jpg','solved':True},{'pic':'l2_quack_3.jpg','solved':True},{'pic':'l2_quack_1.jpg'},{'pic':'l2_quack_4.jpg'}]},
 {'m':'closing','mode':'night','line1':'One strange','line2':'case.','sub':'Tell the story to the person next to you.'},
]
if __name__=='__main__':
    sxl.build(spec,'/home/claude/work/lesson/lesson2_deck',pdf='/home/claude/work/lesson/SkillsXLab_Lesson2_deck_v1_light.pdf')
    print(len(sxl.expand_spec(spec)))
