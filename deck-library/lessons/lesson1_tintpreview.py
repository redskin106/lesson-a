import sys; sys.path.insert(0,'/home/claude/work/lesson')
from sxl.interactive import build_interactive
from lessons.lesson1 import spec
cb=[d for d in spec if d['m']=='dial_ladder'][0]
a=dict(cb); a['tinted']=True; a['label']='tinted'
b=dict(cb); b['label']='current'
print(build_interactive([a,b],'/home/claude/work/lesson/lesson1_tintpreview.html',title='How strong? tinted vs current'))
