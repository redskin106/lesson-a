"""Lesson 1 (have to / should) rebuilt from library modules. Data only."""
import sys; sys.path.insert(0,'/home/claude/work/lesson')
import sxl
G=lambda c,t:(c,t,True); C=lambda c,t:(c,t,False)
YOU=('c1','You')
E_,S_,A_='ENGAGE','STUDY','ACTIVATE'
SHOULDBANK=[('c2','have to'),('c2','don’t have to'),('c2','shouldn’t'),('c2','should')]
spec=[
 {'m':'cover','phase':E_,'tag':'EFL','title':'Lesson <span class="grad">1</span>','phases':['Engage','Study','Activate'],'active':0,
  'cards':[{'pic':'01_c1.jpg','x':1010,'y':150,'w':330,'h':430,'r':-7},{'pic':'01_c2.jpg','x':1290,'y':300,'w':330,'h':430,'r':4},{'pic':'01_c3.jpg','x':1500,'y':120,'w':330,'h':430,'r':-3}]},
 {'m':'columns','phase':E_,'numbered':True,'cols':[{'label':'Two weeks before','pic':'hw_1.jpg','rows':[]},{'label':'The day before','pic':'hw_2.jpg','rows':[]},{'label':'Today','pic':'hw_3.jpg','rows':[]}]},
 {'m':'pic_question','phase':E_,'pic':'hw_3.jpg','q':('What',['should','he do?'])},
 {'m':'today','phase':S_,'emoji':'pointing_viewer','title':'Orders and advice','fs':76,'rows':[[YOU,('c2','have to'),('c3','rest.')],[YOU,('c2','should'),('c3','drink water.')]]},
 {'m':'strip','phase':S_,'role':'Boss','grad':'red','pics':['05_p1.jpg','05_p2.jpg','05a_p3.jpg','05a_p4.jpg','05a_p5.jpg'],'close':[[YOU,('c2','have to')],[('c3','save the planet.')]],'bubble':{'emoji':'red_exclamation_mark'}},
 {'m':'strip','phase':S_,'role':'Friend','grad':'teal','pics':['05_p1.jpg','05_p2.jpg','05b_p3_beach.jpg','05b_p4_m.jpg','05b_p5.jpg'],'close':[[YOU,('c2','should')],[('c3','save the planet.')]],'bubble':{'emoji':'thumbs_up'}},
 {'m':'contrast','phase':S_,'title':'Boss says','left':{'label':'Boss says','grad':'red','pic':'05a_p3.jpg','chips':[YOU,('c2','have to'),('c3','save the planet.')],'cap':'Needed.'},
   'right':{'label':'Boss says','grad':'red','pic':'06_p2.jpg','chips':[YOU,('c2','don’t have to'),('c3','save the planet.')],'cap':'Not needed.'}},
 {'m':'pic_rows','phase':S_,'rows':[
   {'label':'Neighbour','grad':'amber','chips':[YOU,('c2','should'),('c3','put a banana on your head.')],'pics':[f'09a_p{k}.jpg' for k in range(1,5)],'cap':'Good idea?'},
   {'label':'Pharmacist','grad':'teal','chips':[YOU,('c2','have to'),('c3','take this pill.')],'pics':[f'09b_p{k}.jpg' for k in range(1,5)],'cap':'Needed.'}]},
 {'m':'dial','phase':S_,'stops':[(180,'prohibited',['mustn’t'],'not allowed'),(135,'thumbs_down',['shouldn’t'],'bad idea?'),(90,'relieved_face',['don’t have to'],'not needed'),(45,'thumbs_up',['should'],'good idea?'),(0,'red_exclamation_mark',['have to','must'],'needed')]},
 {'m':'contrast','phase':S_,'title':'Not the same!','left':{'label':'Not allowed','grad':'red','pic':'mu_1.jpg','chips':[YOU,('c2','mustn’t'),('c3','drink alcohol.')]},
   'right':{'label':'Not needed','grad':'teal','pic':'mu_2.jpg','chips':[YOU,('c2','don’t have to'),('c3','take it with food.')]}},
 {'m':'columns','phase':S_,'title':'Homework','cols':[
   {'label':'Two weeks before','pic':'hw_1.jpg','rows':[[YOU,('c2','don’t have to'),('c3','rush.')],[YOU,('c2','should'),('c3','start.')]],'gloss':'Not needed · good idea?'},
   {'label':'The day before','pic':'hw_2.jpg','rows':[[YOU,('c2','have to'),('c3','finish.')]],'gloss':'Needed'},
   {'label':'Today','pic':'hw_3.jpg','rows':[[YOU,('c2','shouldn’t'),('c3','work.')]],'gloss':'Bad idea?'}]},
 {'m':'pic_rows','phase':S_,'title':'Swap!','optional':True,'rows':[
   {'label':'Boss','grad':'red','chips':[YOU,('c2','should'),('c3','rest.')],'pics':['sw_1t.jpg','sw_2a.jpg','sw_3.jpg']},
   {'label':'Friend','grad':'teal','chips':[YOU,('c2','have to'),('c3','rest.')],'pics':['sw_1t.jpg','sw_2b.jpg','sw_3.jpg']}]},
 {'m':'sort','phase':S_,'title':'Fill the gaps','bank':['have to','should','|',('c3','go to hospital'),('c3','sleep'),('c3','drink tea')],'rows':[{'pic':'sc_1.jpg','ans':['have to','go to hospital']},{'pic':'sc_2.jpg','ans':['should','sleep']},{'pic':'sc_3.jpg','ans':['should','drink tea']}]},
 {'m':'sort','phase':S_,'title':'Fill the gaps','bank':['have to','should','shouldn’t','don’t have to','mustn’t'],'rows':[
   {'pic':'sc2_1.jpg','end':('c3','eat spicy food.'),'ans':'shouldn’t'},{'pic':'sc2_2.jpg','end':('c3','see a doctor.'),'ans':'have to'},{'pic':'sc2_3.jpg','end':('c3','stay in bed.'),'ans':'don’t have to'},{'pic':'sc2_4.jpg','end':('c3','drive.'),'ans':'mustn’t'}]},
 {'m':'today','phase':S_,'emoji':'red_question_mark','title':'Questions','fs':60,'tfs':96,'rows':[
   [('c4','Where'),('c2','does'),('c1','it'),('c3','hurt?')],[('c4','How much'),('c2','does'),('c1','it'),('c3','hurt?')],[('c4','When'),('c2','did'),('c1','it'),('c3','start?')],[('c2','Did'),('c1','you'),('c2','take'),('c3','anything?')]]},
 {'m':'qgrid','phase':S_,'title':'Question it','items':[
   {'pic':'q_1.jpg','chips':[('c4','Where'),('c2','does'),('c1','it'),('c3','hurt?')]},{'pic':'q_2.jpg','chips':[('c4','How much'),('c2','does'),('c1','it'),('c3','hurt?')]},
   {'pic':'q_3.jpg','chips':[('c4','When'),('c2','did'),('c1','it'),('c3','start?')]},{'pic':'q_4.jpg','chips':[('c4','What'),('c2','happened?')]}]},
 {'m':'chat','phase':S_,'title':'The nurse asks','window':4,'lines':[
   ('N','Hello. What’s the problem?'),('P','I have a headache.'),
   ('N',[G('c4','Where'),C('c2','does'),C('c1','it'),G('c3','hurt?')],[('c4','Where'),('c3','hurt?'),('c4','When'),('c3','hurts')]),('P','My head hurts.'),
   ('N',[G('c4','How much'),C('c2','does'),C('c1','it'),C('c3','hurt?')],[('c4','How much'),('c4','When'),('c4','Where')]),('P','A lot. 4 out of 5.'),
   ('N',[G('c4','When'),C('c2','did'),C('c1','it'),C('c3','start?')],[('c4','How much'),('c4','When'),('c4','Where')]),('P','Two days ago.'),
   ('N',[C('c2','Did'),C('c1','you'),C('c2','take'),G('c3','anything?')],[('c3','anything?'),('c2','should'),('c2','have to'),('c3','something?')]),('P','No.'),
   ('N',[C('c1','You'),G('c2','should'),C('c3','drink water.')],[('c3','anything?'),('c2','should'),('c2','have to'),('c3','something?')]),('P','Thank you!')]},
 {'m':'chat','phase':S_,'title':'The doctor says','window':4,'lines':[
   ('D',[C('c1','You'),G('c2','have to'),C('c3','take this medicine.')],SHOULDBANK),('P','Every day?'),
   ('D',[C('c1','You'),G('c2','don’t have to'),C('c3','take it every day.')],SHOULDBANK),('P','OK. Thank you, doctor.')]},
 {'m':'chat','phase':S_,'title':'The neighbour twist','optional':True,'window':4,'lines':[
   ('P','My neighbour says: put a banana on your head.'),('N',[C('c1','You'),G('c2','shouldn’t'),C('c3','put a banana on your head.')],SHOULDBANK),
   ('P','I don’t want to take medicine!'),('D',[C('c1','You'),G('c2','have to'),C('c3','take it.')],SHOULDBANK)]},
 {'m':'title_card','phase':A_,'line1':'The','line2':'Hotline','arch':[('telephone_receiver',1260,230,420,-10),('woman_health_worker',1450,480,300,8),('face_with_thermometer',1280,640,260,-6)]},
 {'m':'cards','phase':A_,'cards':[
   {'emoji':'face_with_thermometer','name':'Patient','grad':'rose','text':'has the problem<br>and the twist'},
   {'emoji':'woman_health_worker','name':'Nurse','grad':'teal','text':'asks questions<br>gives advice','foot':'Part 1'},
   {'emoji':'man_health_worker','name':'Doctor','grad':'violet','text':'gives strong<br>advice','foot':'Part 2'}]},
 {'m':'chat','phase':A_,'title':'Watch the twist','window':4,'lines':[
   ('P','I have a headache.'),('N',[C('c1','You'),C('c2','should'),C('c3','drink water.')]),('P','No! I don’t want to!'),('D',[C('c1','You'),C('c2','have to'),C('c3','drink water.')])]},
 {'m':'cards','phase':A_,'title':'Your twist','rg':'orange','cards':[
   {'emoji':'zany_face','name':'Gibberish','grad':'orange','text':'“Blah blah blah…”'},{'emoji':'face_with_open_mouth','name':'Drama','grad':'orange','text':'“I’m dying!”'},
   {'emoji':'face_with_symbols_on_mouth','name':'Stubborn','grad':'orange','text':'“I don’t want to!”'},{'emoji':'old_woman','name':'Neighbour','grad':'orange','text':'“My neighbour says…”'}]},
 {'m':'slot','phase':A_,'rows':[('face_with_head-bandage',4,'zany_face',0),('sneezing_face',2,'stopwatch',0),('face_with_thermometer',3,'shushing_face',0),('nauseated_face',5,'zany_face',1),('hot_face',1,'stopwatch',1)]},
 {'m':'prep','phase':A_,'role':'Nurse','grad':'teal','status':('face_with_head-bandage',4,'zany_face'),'lal':'start',
  'left':[('chips',[[('c4','Where'),('c2','does'),('c1','it'),('c3','hurt?')],[('c4','How much'),('c2','does'),('c1','it'),('c3','hurt?')],[('c4','When'),('c2','did'),('c1','it'),('c3','start?')],[('c2','Did'),('c1','you'),('c2','take'),('c3','anything?')]])],
  'right':[('lead',[YOU,('c2','should')]),('tiles',[('sleeping_face','sleep'),('glass_of_milk','drink water'),('hot_beverage','drink tea')])]},
 {'m':'prep','phase':A_,'role':'Doctor','grad':'violet','status':('face_with_head-bandage',4,'zany_face'),
  'left':[('lead',[YOU,('c2','have to')]),('bigtiles',[('hospital','go to hospital'),('pill','take medicine'),('stethoscope','see a doctor')])],
  'right':[('chips',[[('c2','Have'),('c1','you'),('c2','tried'),('c3','this?')],[('c2','Did'),('c1','you'),('c2','take'),('c3','anything?')]]),('label','OPTIONAL')]},
 {'m':'recap','phase':'RECAP','rows':[([YOU,('c2','have to'),('c3','rest.')],'needed'),([YOU,('c2','should'),('c3','drink water.')],'good idea?'),([YOU,('c2','shouldn’t'),('c3','drive.')],'bad idea?'),
   ([YOU,('c2','don’t have to'),('c3','go.')],'not needed'),([YOU,('c2','mustn’t'),('c3','drink.')],'not allowed')],
  'side':[[('c4','Where'),('c2','does'),('c1','it'),('c3','hurt?')],[('c4','When'),('c2','did'),('c1','it'),('c3','start?')],[('c2','Did'),('c1','you'),('c2','take'),('c3','anything?')]],'emoji':'face_with_thermometer'},
]
if __name__=='__main__':
    sxl.build(spec,'/home/claude/work/lesson/lesson1_deck',pdf='/home/claude/work/lesson/SkillsXLab_Lesson1_lib_v1_light.pdf')
