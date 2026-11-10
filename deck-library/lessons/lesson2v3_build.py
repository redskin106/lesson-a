import sys; sys.path.insert(0,'/home/claude/work/lesson')
from sxl.interactive import build_interactive
from lessons.lesson2v3 import spec
print(len(spec),'slides',sum(s['min'] for s in spec if not s.get('optional')),'core min',sum(s['min'] for s in spec),'total')
print(build_interactive(spec,'/home/claude/work/lesson/lesson2v3_slice.html',title='SkillsXLab · Lesson 2 · Why does it hurt?'))
