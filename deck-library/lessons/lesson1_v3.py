"""Lesson 1 v3: v2 order plus more practice in Study (see notes). v1 and v2 stay untouched."""
import sys, copy; sys.path.insert(0,'/home/claude/work/lesson')
from lessons.lesson1_v2 import spec as _s
C=lambda c,t:(c,t,False)
spec=copy.deepcopy(_s)
def at(label):
    return next(i for i,d in enumerate(spec) if d['label']==label)
def minutes(label,m): spec[at(label)]['min']=float(m)

# 1. Fill the gaps (2): five items, mustn't and don't have to side by side
d=spec[at('Sort 2 (negatives)')]
d['bank']=['have to','should','shouldn’t','mustn’t','don’t have to']
d['rows']=[{'pic':'sc2_1.jpg','end':('c3','eat spicy food.'),'ans':'shouldn’t'},{'pic':'sc2_2.jpg','end':('c3','see a doctor.'),'ans':'have to'},
           {'pic':'sc2_4.jpg','end':('c3','drive.'),'ans':'mustn’t'},{'pic':'mu_2.jpg','end':('c3','take it with food.'),'ans':'don’t have to'},
           {'pic':'mu_1.jpg','end':('c3','drink alcohol.'),'ans':'mustn’t'}]
minutes('Sort 2 (negatives)',5)

# 3. Pair talk becomes core, with the five dial pictures as prompts
d=spec[at('Pair talk')]; d.pop('optional',None); d['min']=2.0
d['pics']=['hw_5.jpg','hw_3.jpg','hw_1.jpg','hw_4.jpg','hw_2.jpg']
d['note']='Pick a picture. Tell your partner: You ___ ...'
d['label']='Pair talk (pictures)'

# strips are quick: one minute each
minutes('Boss strip',1); minutes('Friend strip',1)

# 4. Build the question (optional) before the nurse chat
bq={'m':'build','phase':'STUDY','title':'Build the question','optional':True,'pics':[],'fs':70,'bfs':60,'label':'Build the question','min':1.0,
    'parts':[('c4','Where'),('c2','does'),('c1','it'),('c3','hurt?')],
    'bank':[('c3','hurt?'),('c4','Where'),('c2','does'),('c1','it'),('c2','do'),('c3','hurts?'),('c4','When')]}
spec.insert(at('Question it')+1,bq)

# 2. Find the mistakes (as in Lesson 2) closes the Study phase
sp={'m':'spot','phase':'STUDY','title':'Find the mistakes','label':'Find the mistakes','min':2.0,'lines':[
  ('N',[('c4','Where'),('c2','does'),('c1','it'),('c3','hurts?','hurt?')]),
  ('D',[('c4','How much'),('c2','do','does'),('c1','it'),('c3','hurt?')]),
  ('N',[('c2','Did'),('c1','you'),('c2','take'),('c3','anything?')]),
  ('D',[('c1','You'),('c2','should'),('c3','to rest.','rest.')]),
  ('N',[('c1','You'),('c2','have to'),('c3','take this medicine.')]),
  ('D',[('c1','You'),('c2','don’t have to'),('c3','worry.')])]}
spec.insert(at('Doctor chat')+1,sp)
