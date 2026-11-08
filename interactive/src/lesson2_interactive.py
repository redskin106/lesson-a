import sys; sys.path.insert(0,'/home/claude/work/lesson')
from sxl.interactive import build_interactive
from lessons.lesson2 import spec
pick=[d for d in spec if d['m'] in('timeline','sort','chat')]
pick=[pick[0],pick[1],pick[2]]   # case-1 timeline, sort, nurse chat
print(build_interactive(pick,'/home/claude/work/lesson/lesson2_interactive.html'))
