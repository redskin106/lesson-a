import sys, pathlib
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent)); sys.path.insert(0,str(HERE.parent.parent/'lessons-3-4'/'src'))
import content as K
from sxl.team_page import build_team_page
cols2=['#e0304a','#2a6ae0','#10a98d','#e89200']
teams=[(a,b,c,c2) for (a,b,c),c2 in zip(K.TEAMS,cols2)]
data={'teams':teams,'dials':K.DIALS,'l3':{'clues':K.L3_CLUES},'l4':{'clues':K.L4_CLUES}}
print(build_team_page(data,str(HERE.parent.parent/'lessons-3-4'/'team.html')))
