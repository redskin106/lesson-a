import sys; sys.path.insert(0,'/home/claude/work/lesson')
from sxl.interactive import build_interactive
from lessons.lesson2 import spec
by={}
for d in spec: by.setdefault(d['m'],[]).append(d)
sel=[by['timeline'][0],by['sort'][0],by['sound_sort'][0],by['chat'][0],by['timeline'][1],by['spot_fib'][0],by['match_pairs'][0],by['chat'][1]]
print(build_interactive(sel,'/home/claude/work/lesson/lesson2_interactive.html'))
