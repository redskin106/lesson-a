"""Review gallery 2 (Batch 1): word-tile modules."""
import sys, pathlib
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from sxl.interactive import build_interactive
ITEMS=[{'w':'dengue','pic':'🦟','clue':'A fever you get from mosquito bites.','cat':'an illness'},
 {'w':'rash','pic':'🔴','clue':'Red spots on the skin.','cat':'a symptom'},
 {'w':'platelets','pic':'🩸','clue':'Blood cells that help the blood to clot.','cat':'part of the blood'},
 {'w':'appendicitis','pic':'🩺','clue':'Pain in the lower right of the belly. The doctor may take out a small part.','cat':'an illness'}]
spec=[
 dict(m='spell',phase='STUDY',label='MODULE spell · Name the illness',title='Name the illness',items=ITEMS,lvl=2,
  levels=[dict(mode='tiles',showpic=True,decoys=0),dict(mode='tiles',showpic=False,decoys=4),dict(mode='type',showpic=False)]),
 dict(m='scramble',phase='STUDY',label='MODULE scramble',title='Unscramble',items=ITEMS,lvl=2,
  levels=[dict(showpic=True,first=True),dict(showpic=True,first=False),dict(showpic=False,first=False)]),
 dict(m='unveil',phase='ACTIVATE',label='MODULE unveil (reveal)',title='What is it?',items=ITEMS,lvl=2,
  levels=[dict(limit=0,hint=True),dict(limit=None,hint=True),dict(limit=None,hint=False)]),
]
if __name__=='__main__':
    out=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else HERE.parent.parent/'lessons-3-4'/'modules2.html')
    print(build_interactive(spec,str(out),title='SkillsXLab · modules review 2'))
