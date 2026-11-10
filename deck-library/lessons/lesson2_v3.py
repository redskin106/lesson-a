"""Lesson 2 v3: v2 plus a regular-verb sort, four-line sorts and a pictured Your turn. v1 and v2 stay untouched."""
import sys, copy; sys.path.insert(0,'/home/claude/work/lesson')
from lessons import lesson2_v2 as _v2
spec=copy.deepcopy(_v2.spec)
def at(label): return next(i for i,d in enumerate(spec) if d['label']==label)

# Sort 1: four lines (ate, slept, fell, went). Sort 3 (optional): drank, took
s1=spec[at('Sort 1: because I ...')]; s2=spec[at('Sort 2: because I ...')]
s1['bank']=['sleep','ate','fall','fell','eat','slept','go','went']
s1['label']='Sort 2: because I ...'
s1['rows']=[
  {'pic':'l2c_1_effect.jpg','pre':('c4','Because I'),'end':('c3','spicy food.'),'ans':['ate']},
  {'pic':'l2c_3_effect.jpg','pre':('c4','Because I'),'end':('c3','on the floor.'),'ans':['slept']},
  {'pic':'l2c_4_effect.jpg','pre':('c4','Because I'),'end':('c3','off a bike.'),'ans':['fell']},
  {'pic':'l2c_2_effect.jpg','pre':('c4','Because I'),'end':('c3','out in the rain.'),'ans':['went']}]
s2['bank']=['took','drink','drank','take']
s2['rows']=[
  {'pic':'l2c_5_effect.jpg','pre':('c4','Because I'),'end':('c3','too much coffee.'),'ans':['drank']},
  {'pic':'l2c_6_effect.jpg','pre':('c4','Because I'),'end':('c3','medicine.'),'ans':['took']}]
s2['optional']=True; s2['label']='Sort 3: drank, took'; s2['min']=2.0
s2['title']='Why? (3)'

# New: regular verbs sort, right after Regular verbs
rs={'m':'sort','phase':'STUDY','title':'Yesterday I ...','label':'Sort 1: regular verbs','min':2.0,
    'bank':['walked','called','cooked','started','walk','call'],
    'rows':[{'pic':'v2_walk.jpg','pre':('c1','I'),'end':('c3','home.'),'ans':['walked']},
            {'pic':'v2_call.jpg','pre':('c1','I'),'end':('c3','my friend.'),'ans':['called']},
            {'pic':'v2_cook.jpg','pre':('c1','I'),'end':('c3','dinner.'),'ans':['cooked']},
            {'pic':'v2_start.jpg','pre':('c1','I'),'end':('c3','work.'),'ans':['started']}]}
spec.insert(at('Regular verbs')+1, rs)

# Your turn: core, with pictures as prompts
yt=spec[at('Your turn')]; yt.pop('optional',None); yt['min']=2.0
yt['pics']=['v2_eat.jpg','v2_walk.jpg','v2_cook.jpg','v2_call.jpg','v2_go.jpg']
yt['note']='Pick a picture. Tell your partner: Yesterday I ...'
yt['label']='Your turn (pictures)'
