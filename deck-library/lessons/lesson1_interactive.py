import sys; sys.path.insert(0,'/home/claude/work/lesson')
from sxl.interactive import build_interactive
from lessons.lesson1 import spec
sorts=[d for d in spec if d['m']=='sort']; chats=[d for d in spec if d['m']=='chat' and d['phase']=='STUDY']
sel=[sorts[0],sorts[1]]+chats
print(build_interactive(sel,'/home/claude/work/lesson/lesson1_interactive.html',title='SkillsXLab · Lesson 1 practice'))
