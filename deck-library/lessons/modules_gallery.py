"""Review gallery: every new Lesson 3-4 module on its own slide (placeholders, emoji art)."""
import sys, pathlib
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent)); sys.path.insert(0,str(HERE.parent.parent/'lessons-3-4'/'src'))
import content as K
from sxl.interactive import build_interactive
def ex(i,L,phase='STUDY'):
    e=L[i]; lv=e['levels']; ks=['bronze','silver','gold']
    base=dict(m='choice',phase=phase,title=e['title'],hint=e['hint'],label='MODULE choice · '+e['title'],lvl=2)
    if e['kind']=='choice': return dict(base,levels=[{'items':lv[k]} for k in ks])
    return dict(m='build',phase=phase,title=e['title'],label='MODULE build · '+e['title'],levels=[dict(pics=[],parts=[],bank=[]) for k in ks])
def board(title,suspects,clues,twist,test,ans,reveal):
    return dict(m='case_board',phase='ACTIVATE',title=title,label='MODULE case_board · '+title,teams=[(a,b,c,c2) for (a,b,c),c2 in zip(K.TEAMS,['#e0304a','#2a6ae0','#10a98d','#e89200'])],suspects=suspects,clues=clues,twist=twist,test=test,answer=ans,reveal=reveal)
Q=lambda c,t:(c,t)
build_levels=[
 dict(pics=['🌡️'],parts=[Q('c4','How'),Q('c4','long'),Q('c2','have'),Q('c1','you'),Q('c2','had'),Q('c3','a fever?')],extra=[]),
 dict(pics=['🌡️'],parts=[Q('c4','How'),Q('c4','long'),Q('c2','have'),Q('c1','you'),Q('c2','had'),Q('c3','a fever?')],extra=[('c2','did'),('c2','are')]),
 dict(pics=[],parts=[Q('c4','Have'),Q('c1','you'),Q('c2','been'),Q('c2','bitten'),Q('c3','by mosquitoes?')],extra=[('c2','did'),('c2','are'),('c2','bite'),('c4','ever')])]
spec=[
 dict(m='vol_ladder',phase='ENGAGE',label='MODULE vol_ladder',title='Eyes closed. Louder.',rungs=['fever','39 degrees','she has a rash','it might be dengue!','IT CAN\'T BE FLU!'],side='Everyone, eyes closed, at the same time. Whisper first. Each line is louder.'),
 dict(m='timetable',phase='ENGAGE',label='MODULE timetable',title='A student\'s week',days=['Mon','Tue','Wed','Thu','Fri'],rows=[('📚',['📚','📚','📚','📚','📚']),('☕',['☕☕','☕☕☕','☕☕','☕☕☕','☕☕☕☕']),('😴',['3h','4h','3h','2h','3h'])],note='No words. What do you notice?'),
 dict(m='dials3',phase='STUDY',label='MODULE dials3',title='The dials',dials=K.DIALS,note='Use at least one dial in every sentence.'),
 dict(m='choice',phase='STUDY',label='MODULE choice (levels) · Symptoms',title=K.L3_EX[0]['title'],hint=K.L3_EX[0]['hint'],lvl=2,levels=[{'items':K.L3_EX[0]['levels'][k]} for k in ('bronze','silver','gold')]),
 dict(m='choice',phase='STUDY',label='MODULE choice (levels) · might / can\'t',title=K.L3_EX[2]['title'],hint=K.L3_EX[2]['hint'],lvl=2,levels=[{'items':K.L3_EX[2]['levels'][k]} for k in ('bronze','silver','gold')]),
 dict(m='build',phase='STUDY',label='MODULE build (existing, levels) · Ask the patient',title='Ask the patient',lvl=2,levels=[dict(b) for b in build_levels]),
 dict(m='frames3',phase='ACTIVATE',label='MODULE frames3',title='Your sentences (they stay on the board)',groups=[
   {'t':'Easy','c':'teal','l':['She has a fever.','Her pulse is 104.','It might be dengue.']},
   {'t':'Better','c':'sky','l':['Her temperature is higher than normal.','It can\'t be appendicitis because her belly does not hurt.']},
   {'t':'Stretch','c':'rose','l':['It is unlikely to be flu because she has no cough.','It is probably dengue, because she has a rash and she had mosquito bites.'],'fs':36}],note='Any sentence that carries the meaning is good.'),
 board('Case board · Lesson 3',K.L3_SUSPECTS,K.L3_CLUES,K.L3_TWIST,K.L3_TEST,K.L3_ANSWER,'Dengue. Rash on the arms and chest, low platelets and white cells, no cough, mosquito bites a week ago.'),
 board('Case board · Lesson 4',K.L4_SUSPECTS,K.L4_CLUES,K.L4_TWIST,K.L4_TEST,K.L4_ANSWER,'Too much coffee: 8 cups a day, 3 hours of sleep, pulse 110, normal temperature, better on the Sunday without coffee.'),
 dict(m='boss',phase='ACTIVATE',label='MODULE boss',**K.L3_BOSS,sec=90),
 dict(m='reveal',phase='ACTIVATE',label='MODULE reveal',title='The answer',pic='🦟',answer='Dengue',note='Rash · low platelets and white cells · no cough · mosquito bites a week ago.'),
 dict(m='frames3',phase='ACTIVATE',label='MODULE frames3 + write (handover)',title='Tell the doctor',h=470,groups=[{'t':'Handover','c':'violet','l':['A young woman. Day 3 of fever.','Her temperature is ___ than normal.','She has ___ and ___. She has no ___.','It is probably ___ because ___.'],'fs':38}],write=True,note='Write 3 sentences, then read them to your partner.'),
]
if __name__=='__main__':
    out=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else HERE.parent.parent/'lessons-3-4'/'modules.html')
    print(build_interactive(spec,str(out),title='SkillsXLab · new modules review')),
