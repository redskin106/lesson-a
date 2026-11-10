"""Lesson 1 v2: Study regrouped by teaching point. v1 (lesson1.py) stays untouched."""
import sys, copy; sys.path.insert(0,'/home/claude/work/lesson')
from lessons.lesson1 import spec as _s
from lessons.plan import L1, apply
old = copy.deepcopy(_s); rows = list(L1)
# 1-based old positions, new order
# A advice vs orders: 4,5,6,8,13(opt)  B not needed: 7  C the scale: 11,9,10(opt),12
# practice: 14,15   questions: 16,17,18   conversations: 19,20   then Activate 21..30
order = [1,2,3, 4,5,6,8,13, 7, 11,9,10,12, 14,15, 16,17,18, 19,20] + list(range(21,31))
assert sorted(order)==list(range(1,31))
spec = [old[i-1] for i in order]
r2 = [rows[i-1] for i in order]
apply(spec, r2)
