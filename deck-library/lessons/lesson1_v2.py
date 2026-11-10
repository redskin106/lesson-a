"""Lesson 1 v2: Study regrouped by teaching point; Activate gets the four twist scripts. v1 (lesson1.py) stays untouched."""
import sys, copy; sys.path.insert(0,'/home/claude/work/lesson')
from lessons.lesson1 import spec as _s
from lessons.plan import L1, apply
G=lambda c,t:(c,t,True); C=lambda c,t:(c,t,False)
YOU=C('c1','You'); A_='ACTIVATE'
old = copy.deepcopy(_s); rows = list(L1)

# labels and glosses never carry a full stop (sentences do)
def strip_caps(x):
    if isinstance(x, dict):
        for k,v in list(x.items()):
            if k=='cap' and isinstance(v,str): x[k]=v.rstrip('.')
            else: strip_caps(v)
    elif isinstance(x,(list,tuple)):
        for v in x: strip_caps(v)
for d in old: strip_caps(d)

# slot machine: third column is the pain level the nurse asks about
for d in old:
    if d['m']=='slot': d['heads']=['PROBLEM','HOW MUCH?','TWIST']

def chat(title, lines, optional=False):
    d={'m':'chat','phase':A_,'title':title,'window':4,'lines':lines}
    if optional: d['optional']=True
    return d
SB=[('c2','should'),('c2','shouldn’t'),('c2','have to'),('c2','mustn’t')]
HB=[('c2','have to'),('c2','don’t have to'),('c2','shouldn’t')]
stubborn=chat('Watch the twist · Stubborn',[
  ('P','My stomach hurts.'),('N',[C('c2','Did'),C('c1','you'),C('c2','take'),C('c3','anything?')]),('P','No.'),
  ('N',[YOU,G('c2','should'),C('c3','take this pill.')],SB),('P','I don’t want to!'),
  ('D',[YOU,G('c2','have to'),C('c3','take it.')],HB),('P','OK. Thank you.')])
drama=chat('Twist · Drama',[
  ('P','I’m dying!'),('N',[G('c4','How much'),C('c2','does'),C('c1','it'),C('c3','hurt?')],[('c4','How much'),('c4','When'),('c4','Where')]),
  ('P','A lot. 5 out of 5!'),('N',[YOU,G('c2','should'),C('c3','drink water.')],SB),('P','I’m dying!'),
  ('D',[YOU,G('c2','don’t have to'),C('c3','worry.')],HB),('D',[YOU,G('c2','have to'),C('c3','rest.')],HB),('P','OK. Thank you, doctor.')],True)
neighbour=chat('Twist · Neighbour',[
  ('P','My neighbour says: drink beer.'),('N',[YOU,G('c2','shouldn’t'),C('c3','drink beer.')],SB),
  ('P','But my neighbour says…'),('D',[YOU,G('c2','mustn’t'),C('c3','drink alcohol.')],SB),('P','OK. Thank you.')],True)
gibberish=chat('Twist · Gibberish',[
  ('P','Blah blah blah…'),('N','Sorry? Where does it hurt?'),('P','Blah… my head!'),
  ('N',[G('c4','How much'),C('c2','does'),C('c1','it'),C('c3','hurt?')],[('c4','How much'),('c4','When'),('c4','Where')]),('P','Blah… 4!'),
  ('N',[YOU,G('c2','should'),C('c3','rest.')],SB),('D',[YOU,G('c2','have to'),C('c3','take this medicine.')],HB),('P','OK. Thank you.')],True)

# old 1-based positions; 20 (neighbour twist) and 23 (watch the twist) are replaced by the four twist scripts
order = [1,2,3, 4,5,6,8,13, 7, 11,9,10,12, 14,15, 16,17,18, 19, 21,22]
new_after_cards = [drama,neighbour,gibberish]
spec=[old[i-1] for i in order]; r2=[rows[i-1] for i in order]
spec += [stubborn]; r2 += [('Watch the twist: Stubborn','2','Nurse advises (should), the patient refuses, the doctor steps in (have to). Fill the gaps together')]
spec += [old[23]]; r2 += [rows[23]]                      # Your twist cards
spec += new_after_cards
r2 += [('Twist: Drama','1','OPTIONAL: I’m dying! The nurse asks How much; the doctor calms (don’t have to worry)'),
       ('Twist: Neighbour','1','OPTIONAL: neighbour says drink beer. shouldn’t, then the doctor: mustn’t'),
       ('Twist: Gibberish','1','OPTIONAL: repair first (Sorry? Where does it hurt?), then the normal questions')]
spec += [old[i-1] for i in range(25,31)]; r2 += [rows[i-1] for i in range(25,31)]
apply(spec, r2)
