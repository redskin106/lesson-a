import json, pathlib, content as K
OUT=pathlib.Path(__file__).resolve().parent.parent
ex=lambda i,L: {'t':'exercise','phase':'STUDY','ex':L[i]}
def data_board():
    return {'teams':K.TEAMS,'dials':K.DIALS,
     'l3':dict(title='Lesson 3 · Which illness?',kind='3',suspects=K.L3_SUSPECTS,clues=K.L3_CLUES,twist=K.L3_TWIST,test=K.L3_TEST,answer=K.L3_ANSWER,
       reveal='Dengue. Rash on the arms and chest, low platelets and white cells, no cough, mosquito bites a week ago. Tell the class: in real life the nurse reports the clues and the doctor decides.'),
     'l4':dict(title='Lesson 4 · The Sleepless Patient',kind='4',suspects=K.L4_SUSPECTS,clues=K.L4_CLUES,twist=K.L4_TWIST,test=K.L4_TEST,answer=K.L4_ANSWER,
       reveal='Too much coffee (8 cups a day, 3 hours of sleep, pulse 110, normal temperature, better on the Sunday without coffee). Exam stress is part of the story, but the coffee is what we can change.')}
L3=[
 {'t':'cover','kicker':'NURSING ENGLISH · LESSON 3','title':'Which illness?','sub':'Ask. Listen. Decide.','pic':'🩺'},
 {'t':'ladder','phase':'ENGAGE','title':'Eyes closed. Louder.','rungs':['fever','39 degrees','she has a rash','it might be dengue!','IT CAN\'T BE FLU!'],'side':'Everyone, eyes closed, all at the same time. Start with a whisper. Each line is louder. Nobody is listening to you, only to themselves.'},
 {'t':'scene','phase':'ENGAGE','title':'Meet the patient (no sound)','frames':[{'pic':'🧍‍♀️🥵','cap':'She walks in. She looks hot.'},{'pic':'🌡️','cap':'The nurse takes her temperature.'},{'pic':'😟','cap':'The nurse looks worried.'},{'pic':'❓','cap':'What is wrong with her?'}],'note':'Placeholder frames. Final version: stick-figure clip over a real hospital background, no sound, no real faces.'},
 {'t':'text','phase':'STUDY','title':'Today: detective nurses','lines':['🗣️ Ask the right question','🔢 Read the numbers: higher / lower than normal','🧩 might · can\'t · because'],'note':'Study exercises: your teacher can change the level (bronze, silver, gold).'},
 ex(0,K.L3_EX),ex(1,K.L3_EX),ex(2,K.L3_EX),ex(3,K.L3_EX),
 {'t':'frames','phase':'ACTIVATE','title':'Your sentences (they stay on the board)','groups':[
   {'t':'Easy','c':'#19b38a','l':['She has a fever.','Her pulse is 104.','It might be dengue.']},
   {'t':'Better','c':'#2a8cf0','l':['Her temperature is higher than normal.','It can\'t be appendicitis because her belly does not hurt.']},
   {'t':'Stretch','c':'#e0408a','l':['It is unlikely to be flu because she has no cough.','It is probably dengue, because she has a rash and she had mosquito bites.']}],
  'note':'Any sentence that carries the meaning is good. Hacks are welcome.'},
 {'t':'frames','phase':'ACTIVATE','title':'How the hunt works','groups':[
   {'t':'Teams of 4','l':['Your colour = your clues','Your letter = your job','The job changes every clue (Reader · Asker · Writer · Speaker)'],'fs':34},
   {'t':'One clue','l':['1 Reader gets the clue','2 Asker asks · Reader answers','3 Writer writes the sentence on the tablet','4 Speaker: hands up · say it loudly'],'fs':34},
   {'t':'Then','l':['Teacher: "OK" → the clue appears for everybody','Another team: say it differently','Waiting? Write what you hear.'],'fs':34}],
  'note':'Tablets: open the team page. Teacher: board on the screen.'},
 {'t':'hunt','phase':'ACTIVATE','title':'Find the illness','lines':['5 suspects. 16 clues. Which can\'t it be?','Use might · can\'t · because','Late twist coming. Don\'t panic.'],'href':'board.html?case=3'},
 {'t':'text','phase':'ACTIVATE','title':'Wait… which can\'t it be?','lines':['Stand up: Dengue / Flu / Measles','Say why: "It can\'t be flu because..."','Change your side if you hear a better reason.'],'note':'Teacher: confirming test on the board → "Which test?"'},
 {'t':'test','phase':'ACTIVATE'},
 {'t':'reveal','phase':'ACTIVATE','title':'The answer','pic':'🦟','answer':'Dengue','note':'Rash · low platelets and white cells · no cough · mosquito bites a week ago.'},
 {'t':'boss','phase':'BOSS','title':'Boss question','boss':K.L3_BOSS},
 {'t':'handover','phase':'ACTIVATE','title':'Tell the doctor (handover)','frame':'<b>Patient: a young woman. Day 3 of fever.</b><br>Her temperature is ___ (higher / lower than normal).<br>She has ___ and ___.<br>She has no ___.<br>It is probably ___ because ___.<br>It can\'t be ___ because ___.','note':'Write 3 sentences. Read them to your partner. Quiet voices are fine.'},
 {'t':'cover','kicker':'THANK YOU','title':'Well done, detectives','sub':'See you next time.','pic':'🩺','bg':'NIGHT'},
]
L4=[
 {'t':'cover','kicker':'NURSING ENGLISH · LESSON 4','title':'The Impossible Week','sub':'Describe it precisely.','pic':'📅','bg':'ENGAGE'},
 {'t':'ladder','phase':'ENGAGE','title':'Eyes closed. How bad?','rungs':['a little','quite','very','really','the worst!'],'side':'Eyes closed, all together. The louder you are, the worse it is. Whisper = a little. Shout = the worst.'},
 {'t':'timetable','phase':'ENGAGE','title':'A student\'s week (no words)','days':['Mon','Tue','Wed','Thu','Fri'],'rows':[['🌙',['📚','📚','📚','📚','📚']],['🏥',['🏃','🏃','🏃','🏃','🏃']],['☕',['☕☕','☕☕☕','☕☕','☕☕☕','☕☕☕☕']],['😴',['3h','4h','3h','2h','3h']]],'note':'Placeholder timetable. Look. What do you notice? Tell your neighbour.'},
 {'t':'dials','phase':'STUDY','title':'Three dials (and one checker)'},
 ex(0,K.L4_EX),ex(1,K.L4_EX),ex(2,K.L4_EX),ex(3,K.L4_EX),ex(4,K.L4_EX),
 {'t':'frames','phase':'ACTIVATE','title':'Your sentences (they stay on the board)','groups':[
   {'t':'Easy','c':'#19b38a','l':['She drinks coffee every day.','She is very tired.','Her pulse is high.']},
   {'t':'Better','c':'#2a8cf0','l':['She has slept badly for two weeks.','Her pulse is faster than normal.']},
   {'t':'Stretch','c':'#e0408a','l':['She has drunk eight cups a day since the exams started, which is about twice as much as normal.']}],
  'note':'Use at least one dial. Hacks are welcome.'},
 {'t':'frames','phase':'ACTIVATE','title':'Everybody lies','groups':[
   {'t':'The patient says…','l':['"I only drink two cups."','"I sleep fine."'],'fs':38},
   {'t':'The numbers say…','l':['The café card: 8 cups.','The watch: 3 hours of sleep.'],'fs':38},
   {'t':'You decide','l':['"She says ___, but ___."','Which clue do you believe?'],'fs':38}],
  'note':'Teams of 4. Your letter is your dial: A how often · B how long · C how bad · D compared with normal. The speaker changes every clue.'},
 {'t':'hunt','phase':'ACTIVATE','title':'Find the reason','lines':['5 reasons. 16 clues. Everybody lies.','Say it with a dial.','Late twist coming.'],'href':'board.html?case=4'},
 {'t':'text','phase':'ACTIVATE','title':'Wait… is it just stress?','lines':['Stand up: coffee / exam stress / broken heart','Say why with a dial: "She has slept badly for two weeks."'],'note':'Teacher: confirming test → "Which test?"'},
 {'t':'test','phase':'ACTIVATE'},
 {'t':'reveal','phase':'ACTIVATE','title':'The reason','pic':'☕','answer':'Too much coffee','note':'8 cups · 3 hours of sleep · pulse 110 · better on the Sunday without coffee.'},
 {'t':'boss','phase':'BOSS','title':'Boss question','boss':K.L4_BOSS},
 {'t':'frames','phase':'ACTIVATE','title':'"Doctor, I\'m too busy."','groups':[
   {'t':'Patient','c':'#e0408a','l':['"I\'m too busy to sleep."','"I need coffee. I have three exams."'],'fs':40},
   {'t':'You (the nurse)','c':'#19b38a','l':['"You should sleep at least seven hours."','"How many cups do you drink every day?"','"For two weeks? That is more than normal."'],'fs':36},
   {'t':'Say one thing','l':['Choose a dial.','Make it kind.'],'fs':40}],
  'note':'Pairs, 2 minutes. Swap. Placeholder script; the real one comes after testing.'},
 {'t':'cover','kicker':'THANK YOU','title':'Good job, nurses','sub':'Sleep well tonight.','pic':'😴','bg':'NIGHT'},
]
for name,slides,title in [('lesson3',L3,'Lesson 3 · Which illness?'),('lesson4',L4,'Lesson 4 · The Impossible Week')]:
    kind='3' if name=='lesson3' else '4'
    D={'n':kind,'slides':slides,'dials':K.DIALS,'test':(K.L3_TEST if kind=='3' else K.L4_TEST)}
    html=(pathlib.Path(__file__).parent/'deck.html').read_text().replace('__TITLE__',title).replace('__DATA__',json.dumps(D,ensure_ascii=False))
    (OUT/f'{name}.html').write_text(html)
B=json.dumps(data_board(),ensure_ascii=False)
for f in ('board','team'):
    (OUT/f'{f}.html').write_text((pathlib.Path(__file__).parent/f'{f}.html').read_text().replace('__DATA__',B))
print('built',[p.name for p in OUT.glob('*.html')])
