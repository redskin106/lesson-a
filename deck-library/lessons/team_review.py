"""Review decks: every team task, in lesson style, answers visible. Build: python3 lessons/team_review.py -> lessons-3-4/team_review3.html, team_review4.html"""
import sys, pathlib
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent)); sys.path.insert(0,str(HERE.parent.parent/'lessons-3-4'/'src')); sys.path.insert(0,str(HERE))
import content as K
from sxl.interactive import build_interactive
TG={'red':'rose','blue':'sky','green':'teal','yellow':'amber'}
NAME={'red':'Red','blue':'Blue','green':'Green','yellow':'Yellow'}
def unlock(c): return (c.get('text') or ('<b>'+c['topic']+'</b><br>'+'<br>'.join(f'{k} {v}' for k,v in c['dials'].items()))).replace('\n','<br>')
def deck(n,clues,tasks):
    sp=[dict(m='cover',label='Cover',tag='REVIEW · TEAM TASKS',title=f'Lesson <span class="grad">{n}</span> team tasks',phases=['Red','Blue','Green','Yellow'],active=0,cards=[dict(pic='✋',x=1010,y=150,w=330,h=430,r=-7),dict(pic='📝',x=1380,y=330,w=330,h=430,r=6)])]
    for team in ('red','blue','green','yellow'):
        for c in sorted([c for c in clues if c['team']==team],key=lambda c:c['r']):
            sp.append(dict(m='task_card',phase='ACTIVATE',label=f"{NAME[team]} · round {c['r']} · {tasks[c['id']]['lab']}",min=2,team=NAME[team],tg=TG[team],r=c['r'],t=tasks[c['id']],unlock=unlock(c),pic=c['pic']))
    return sp
out=HERE.parent.parent/'lessons-3-4'
print(build_interactive(deck(3,K.L3_CLUES,K.TASK3),str(out/'team_review3.html'),title='SkillsXLab · Lesson 3 · team tasks (review)'))
print(build_interactive(deck(4,K.L4_CLUES,K.TASK4),str(out/'team_review4.html'),title='SkillsXLab · Lesson 4 · team tasks (review)'))
