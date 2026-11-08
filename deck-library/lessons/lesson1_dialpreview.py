import sys; sys.path.insert(0,'/home/claude/work/lesson')
from sxl.interactive import build_interactive
from lessons.lesson1 import spec
cb=[d for d in spec if d['m']=='choice_board'][0]
d=dict(cb); d['m']='dial_pics'; d['label']='dial preview'
print(build_interactive([d],'/home/claude/work/lesson/lesson1_dialpreview.html',title='How strong? preview'))
