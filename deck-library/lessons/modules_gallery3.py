"""Review gallery 3 (Batches 2+3): play modules."""
import sys, pathlib, itertools
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from sxl.interactive import build_interactive
C=lambda t,e:dict(t=t,e=e)
ODD=[dict(cards=[C('fever','🌡️'),C('headache','🤕'),C('rash','🔴'),C('shoe','👟')],odd=3,why='A shoe is not a symptom.'),
     dict(cards=[C('nurse','🧑‍⚕️'),C('doctor','🩺'),C('pharmacist','💊'),C('bus','🚌')],odd=3,why='A bus is not a person who works in a hospital.'),
     dict(cards=[C('syringe','💉'),C('bandage','🩹'),C('thermometer','🌡️'),C('pizza','🍕')],odd=3,why='Pizza is not a medical tool.')]
CHART=[dict(cards=[dict(t='Temperature',v='37.1 °C'),dict(t='Pulse',v='78 beats per minute'),dict(t='Breathing',v='78 breaths per minute'),dict(t='Pain',v='3 out of 10')],odd=2,why='78 breaths per minute is dangerously high. Normal is 12 to 20.'),
       dict(cards=[dict(t='Pulse',v='72 beats per minute'),dict(t='Temperature',v='98.6 °C'),dict(t='Breathing',v='16 breaths per minute'),dict(t='Pain',v='2 out of 10')],odd=1,why='98.6 is a Fahrenheit number. In °C, normal is about 37 °C.')]
LF=[dict(text='The patient has a low fever',say='The patient has a high fever',opts=['short','new']),
    dict(text='Take two tablets before meals',say='Take two tablets after meals',opts=['during','with']),
    dict(text='The rash is on his right arm',say='The rash is on his left arm',opts=['back','head'])]
TR=[dict(t="can't breathe",e='🫁',b=0,why="Can't breathe = RED. Help now."),dict(t='bleeding a lot',e='🩸',b=0,why='Heavy bleeding = RED.'),
    dict(t='broken arm',e='🦴',b=1,why='Broken arm = YELLOW. Soon.'),dict(t='high fever',e='🌡️',b=1,why='High fever = YELLOW.'),
    dict(t='small cut',e='🩹',b=2,why='Small cut = GREEN. Can wait.'),dict(t='mild cough',e='😷',b=2,why='Mild cough = GREEN.')]
BK=[dict(n='RED',s='now',c='#e0263e',e='🚑'),dict(n='YELLOW',s='soon',c='#d89a00',e='⏳'),dict(n='GREEN',s='can wait',c='#10a98d',e='🪑')]
LAB=dict(title='PARACETAMOL 500 mg',lines=[dict(id='name',t='Paracetamol tablets',e='💊'),dict(id='dose',t='Adults: 1–2 tablets',e='🔢'),dict(id='freq',t='Every 4–6 hours',e='⏰'),
    dict(id='max',t='Maximum 8 tablets in 24 hours',e='⛔'),dict(id='exp',t='Expiry: 06/2028',e='📅'),dict(id='store',t='Keep below 30 °C',e='🌡️')])
QS=[dict(q='How many tablets can an adult take at one time?',a='dose'),dict(q='How often can the patient take it?',a='freq'),dict(q='What is the maximum in one day?',a='max'),dict(q='When does the medicine expire?',a='exp')]
TB=[dict(w='dengue',e='🦟',no=['mosquito','fever','virus','blood']),dict(w='thermometer',e='🌡️',no=['temperature','hot','measure','mouth']),
    dict(w='injection',e='💉',no=['needle','vaccine','arm','pain']),dict(w='stethoscope',e='🩺',no=['listen','heart','doctor','chest'])]
AT=[dict(k='fever',e='🌡️',w='a fever',q='Does the patient have a fever?'),dict(k='rash',e='🔴',w='a rash',q='Does the patient have a rash?'),dict(k='cough',e='😷',w='a cough',q='Does the patient have a cough?'),
    dict(k='head',e='🤕',w='a headache',q='Does the patient have a headache?'),dict(k='vomit',e='🤢',w='vomiting',q='Is the patient vomiting?')]
keys=[a['k'] for a in AT]; combos=list(itertools.combinations(keys,2))+[(k,) for k in keys]
FACE=['🧑','👩','👨','🧓','👴','👵','🧒','👧','👦','🧔','👱','🧑‍🦰']
PAT=[dict(e=FACE[i],a=list(combos[i % len(combos)])) for i in range(12)]
PR=[dict(a='🌡️',b='fever'),dict(a='🔴',b='rash'),dict(a='😷',b='cough'),dict(a='🤢',b='vomit')]
PR2=[dict(a='fever',b='a high temperature'),dict(a='rash',b='red spots on the skin'),dict(a='cough',b='air comes out of the mouth with noise'),dict(a='vomit',b='food comes up from the stomach'),dict(a='headache',b='pain in the head'),dict(a='dizzy',b='the room is moving')]
PRD=[dict(frames=[dict(e='🧍',c='The patient has a fever.'),dict(e='🦟',c='A mosquito bit him last week.'),dict(e='🩸',c='The blood test: low platelets.')],q='What does the nurse do next?',
      opts=[dict(t='Give aspirin',e='💊'),dict(t='Give fluids and rest',e='💧'),dict(t='Send him to work',e='🏃')],a=1,outcome='Fluids and rest. No aspirin with dengue.'),
     dict(frames=[dict(e='🚶‍♀️',c='The patient says she is dizzy.'),dict(e='💓',c='Her pulse is 120.')],q='What does the nurse do?',
      opts=[dict(t='Ask her to sit down',e='🪑'),dict(t='Ask her to run',e='🏃'),dict(t='Do nothing',e='😴')],a=0,outcome='Sit her down and check again.')]
spec=[
 dict(m='odd',phase='STUDY',label='MODULE odd · Odd one out / wrong chart',items=ODD,lvl=1,levels=[dict(mode='pic'),dict(mode='text'),dict(mode='chart',items=CHART)]),
 dict(m='listen_fix',phase='STUDY',label='MODULE listen_fix',items=LF,lvl=1,levels=[dict(mode='opts'),dict(mode='opts'),dict(mode='type')]),
 dict(m='triage',phase='ACTIVATE',label='MODULE triage',buckets=BK,items=TR,lvl=1,levels=[dict(show='both'),dict(show='text'),dict(show='text')]),
 dict(m='label_reader',phase='STUDY',label='MODULE label_reader',qs=QS,lvl=1,levels=[dict(qtext=True),dict(qtext=True),dict(qtext=False)],lab=LAB),
 dict(m='taboo',phase='ACTIVATE',label='MODULE taboo',items=TB,lvl=1,levels=[dict(limit=2),dict(limit=3,secs=60),dict(limit=4,secs=45)]),
 dict(m='guess_who',phase='ACTIVATE',label='MODULE guess_who',attrs=AT,patients=PAT,rounds=2,lvl=1,levels=[dict(n=6,ask='full'),dict(n=9,ask='full'),dict(n=12,ask='word')]),
 dict(m='ward_memory',phase='STUDY',label='MODULE ward_memory',pairs=PR,lvl=1,levels=[dict(pairs=PR),dict(pairs=PR2[:5]),dict(pairs=PR2)]),
 dict(m='predict',phase='ENGAGE',label='MODULE predict',items=PRD,lvl=1,levels=[dict(cap=True,nopt=2),dict(cap=True,nopt=3),dict(cap=False,nopt=3)]),
]
if __name__=='__main__':
    out=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else HERE.parent.parent/'lessons-3-4'/'modules3.html')
    print(build_interactive(spec,str(out),title='SkillsXLab · modules review 3'))
