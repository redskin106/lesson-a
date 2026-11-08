import sys; sys.path.insert(0,'/home/claude/work/lesson')
from sxl.interactive import build_interactive
from lessons.lesson1 import spec
# preview slice: today (orders/advice), Boss strip, Homework cards, sort 1
pick=[spec[i] for i,d in enumerate(spec) if (d['m']=='today' and d.get('title')=='Orders and advice') or (d['m']=='strip' and d.get('role')=='Boss') or (d['m']=='columns' and d.get('card')) or d['m']=='sort'][:4]
for d in pick: d.pop('min',None); d['label']=d.get('label','preview')
print([d['m'] for d in pick])
print(build_interactive(pick,'/home/claude/work/lesson/lesson1_preview.html',title='SkillsXLab · reveal preview'))
