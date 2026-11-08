import sys; sys.path.insert(0,'/home/claude/work/lesson')
from sxl.interactive import build_interactive
from lessons.lesson2 import spec
print(build_interactive(spec,'/home/claude/work/lesson/lesson2_interactive.html',title='SkillsXLab · Lesson 2'))
