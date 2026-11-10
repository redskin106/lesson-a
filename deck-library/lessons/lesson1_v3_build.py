import sys; sys.path.insert(0,'/home/claude/work/lesson')
from sxl.interactive import build_interactive
from lessons.lesson1_v3 import spec
print(build_interactive(spec,'/home/claude/work/lesson/lesson1_v3.html',title='SkillsXLab · Lesson 1 · What should he do?'))
