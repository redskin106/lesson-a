# Content for Lessons 3 and 4 (data only). All art = emoji / labelled placeholders until Gemini art exists.
# Medical facts: see project doc claude/medical-cross-check-lessons-3-4-nov2026.md
TEAMS=[('red','Red','#ff5a6a'),('blue','Blue','#2a8cf0'),('green','Green','#19b38a'),('yellow','Yellow','#f2a900')]

def mc(pic,q,opts,ans): return {'pic':pic,'q':q,'opts':opts,'ans':ans}

# ---------------- LESSON 3 : "Which illness?" (dengue) ----------------
L3_SUSPECTS=[('flu','Flu','🤧'),('dengue','Dengue','🦟'),('measles','Measles','🔴'),('food','Food poisoning','🤢'),('appendix','Appendicitis','🩺')]
# team colour = clue type. A audio (unlocked by asking), B numbers, C what the nurse sees, D papers & context
L3_CLUES=[
 # id, team, round, kind, emoji, question (A only), clue text, say (what the team must say), effects, level
 dict(id='A1',team='red',r=1,kind='audio',pic='🎧',ask='How long have you had a fever?',text='Three days.',say='She has had a fever for three days.',fx={}),
 dict(id='A2',team='red',r=2,kind='audio',pic='🎧',ask='Where does it hurt?',text='My head and behind my eyes. My muscles hurt too.',say='Her head, her eyes and her muscles hurt, so it might be flu or dengue. It can\'t be appendicitis.',fx={'dengue':'for','flu':'for','appendix':'against'}),
 dict(id='A3',team='red',r=3,kind='audio',pic='🎧',ask='Do you have a cough?',text='No. No cough.',say='She has no cough, so it is unlikely to be flu or measles.',fx={'flu':'against','measles':'against'}),
 dict(id='A4',team='red',r=4,kind='audio',pic='🎧',ask='Have you been bitten by mosquitoes?',text='Yes, a lot. In the garden by the pond, about a week ago.',say='She was bitten by mosquitoes a week ago, so it might be dengue.',fx={'dengue':'for'}),
 dict(id='B1',team='blue',r=1,kind='number',pic='🌡️',text='Temperature: 39.2 °C   (normal: about 37 °C)',say='Her temperature is 39.2. It is higher than normal, so she has a fever.',fx={'appendix':'against'}),
 dict(id='B2',team='blue',r=2,kind='number',pic='💓',text='Pulse: 104 per minute   (normal: 60 – 100)',say='Her pulse is 104. It is a little higher than normal.',fx={}),
 dict(id='B3',team='blue',r=3,kind='number',pic='🩸',text='Platelets: 95 (normal 150–450)\nWhite cells: 3.1 (normal 4.5–11)',say='Her platelets and white cells are lower than normal. That fits dengue.',fx={'dengue':'for'},level='silver'),
 dict(id='B4',team='blue',r=4,kind='number',pic='🫁',text='Breathing: 18 per minute   (normal: 12 – 20)',say='Her breathing is normal. It is the same as normal.',fx={}),
 dict(id='C1',team='green',r=1,kind='photo',pic='🖐️',text='Red rash on the arms and chest. No rash on the face.',say='She has a rash on her arms and chest, but not on her face. It might be dengue. It is unlikely to be measles.',fx={'dengue':'for','measles':'against'}),
 dict(id='C2',team='green',r=2,kind='photo',pic='👁️',text='Eyes: not red, not watery.',say='Her eyes are not red or watery, so it is unlikely to be measles.',fx={'measles':'against'}),
 dict(id='C3',team='green',r=3,kind='photo',pic='🫄',text='Belly: soft. No pain when the nurse presses.',say='Her belly does not hurt when I press it, so it can\'t be appendicitis.',fx={'appendix':'against'}),
 dict(id='C4',team='green',r=4,kind='photo',pic='👃',text='Nose and throat: normal. No runny nose.',say='She has no runny nose and her throat is normal, so it is unlikely to be flu.',fx={'flu':'against'},level='silver'),
 dict(id='D1',team='yellow',r=1,kind='paper',pic='💉',text='Vaccination card: measles vaccine, 2 doses.',say='She had two measles vaccines, so measles is unlikely.',fx={'measles':'against'}),
 dict(id='D2',team='yellow',r=2,kind='paper',pic='🍱',text='Friend: "We ate the same food. Nobody else is sick."',say='Her friends ate the same food and they are not sick, so food poisoning is less likely.',fx={'food':'against'}),
 dict(id='D3',team='yellow',r=3,kind='paper',pic='🏘️',text='Neighbour: "Two people on our street had a fever last week."',say='Two people on her street were sick, so it might be an infection from mosquitoes.',fx={'dengue':'for'}),
 dict(id='D4',team='yellow',r=4,kind='paper',pic='💊',text='Paracetamol yesterday. The fever went down, then came back.',say='She took paracetamol. The fever went down, then came back.',fx={},level='silver'),
]
L3_TWIST=dict(pic='📞',text='Phone call: "Her sister had flu last week!"',say='Her sister had flu, so flu is possible. But she has no cough and she has a rash.',fx={'flu':'for'})
L3_TEST=dict(q='It is day 3 of the fever. Which test do we do?',opts=['Dengue blood test (NS1)','Chest X-ray','Stool test'],ans=0,
  why='On days 1 to 7 of a fever, a blood test for the virus itself (NS1 antigen or PCR) can confirm dengue. Antibody tests come later (from about day 4 or 5).')
L3_ANSWER='dengue'

# study exercises: levels bronze/silver/gold (teacher can switch any time)
L3_EX=[
 dict(kind='choice',title='Symptoms',hint='Tap the right word.',levels=dict(
   bronze=[mc('🤒','fever',['fever','cough','rash'],'fever'),mc('🤕','headache',['headache','rash','fever'],'headache'),mc('😷','cough',['cough','headache','fever'],'cough'),mc('🔴','rash',['rash','cough','fever'],'rash')],
   silver=[mc('🤒','She has a ___.',['fever','headache','cough','rash'],'fever'),mc('🔴','He has a red ___ on his arm.',['rash','cough','fever','pain'],'rash'),mc('🤢','I feel ___.',['sick','sore','rash','cold'],'sick'),mc('👁️','Her ___ are red and watery.',['eyes','ears','arms','legs'],'eyes')],
   gold=[mc('🤕','A pain in the head = a ___',['headache','stomach ache','backache','earache'],'headache'),mc('🔴','Red spots on the skin = a ___',['rash','fever','cough','bruise'],'rash'),mc('🦟','Dengue comes from ___ bites.',['mosquito','dog','spider','flea'],'mosquito'),mc('💪','Muscle pain = ___ pain',['muscle','muscular','muscly','mussel'],'muscle')])),
 dict(kind='choice',title='Higher or lower?',hint='Compare the number with normal.',levels=dict(
   bronze=[mc('🌡️','Normal 37. Patient 39.2.  The temperature is ___.',['higher','lower'],'higher'),mc('🩸','Normal 150 – 450. Patient 95.  The number is ___.',['higher','lower'],'lower'),mc('🫁','Normal 12 – 20. Patient 18.  Breathing is ___.',['normal','higher'],'normal')],
   silver=[mc('🌡️','Normal 37. Patient 39.2.',['It is higher than normal.','It is lower than normal.','It is the same as normal.'],'It is higher than normal.'),mc('🩸','Normal 4.5 – 11. Patient 3.1.',['It is lower than normal.','It is higher than normal.','It is normal.'],'It is lower than normal.'),mc('💓','Normal 60 – 100. Patient 104.',['It is a little higher than normal.','It is much lower than normal.','It is normal.'],'It is a little higher than normal.')],
   gold=[mc('🌡️','37 and 39.2. Which is right?',['39.2 is higher than 37.','39.2 is more high than 37.','39.2 is higher 37.','37 is higher than 39.2.'],'39.2 is higher than 37.'),mc('🩸','95 and 150. Which is right?',['95 is lower than 150.','95 is lower 150.','95 is more low than 150.','95 is the same as 150.'],'95 is lower than 150.'),mc('🫁','18 and 12 – 20. Which is right?',['18 is the same as normal.','18 is higher than normal.','18 is lower than normal.','18 is normal than.'],'18 is the same as normal.')])),
 dict(kind='choice',title='Might · can\'t · because',hint='Read the clue. Choose the sentence.',levels=dict(
   bronze=[mc('🦟','Clue: mosquito bites.',['It might be dengue.','It can\'t be dengue.'],'It might be dengue.'),mc('🫄','Clue: the belly does not hurt.',['It can\'t be appendicitis.','It might be appendicitis.'],'It can\'t be appendicitis.'),mc('🔴','Clue: rash on arms and chest.',['It might be dengue.','It can\'t be dengue.'],'It might be dengue.')],
   silver=[mc('🦟','Clue: mosquito bites.',['It might be dengue because she had mosquito bites.','It can\'t be dengue because she had mosquito bites.','It might be dengue because she is happy.'],'It might be dengue because she had mosquito bites.'),mc('😷','Clue: no cough.',['It is unlikely to be flu because she has no cough.','It is likely to be flu because she has no cough.','It is unlikely to be flu because she has a cough.'],'It is unlikely to be flu because she has no cough.'),mc('🫄','Clue: belly is soft.',['It can\'t be appendicitis because her belly does not hurt.','It can\'t be appendicitis because her belly hurts.','It might be appendicitis because her belly does not hurt.'],'It can\'t be appendicitis because her belly does not hurt.')],
   gold=[mc('👁️','Clue: eyes are not red.',['It is unlikely to be measles because her eyes are not red.','It is unlikely to be measles, because her eyes are red.','It is unlikely measles because her eyes are not red.','It might not be measles because eyes are not red.'],'It is unlikely to be measles because her eyes are not red.'),mc('🍱','Clue: friends ate the same food. Nobody is sick.',['Food poisoning is less likely, because her friends are not sick.','Food poisoning can\'t be, because her friends are sick.','Food poisoning is less likely, because her friends are sick.','It is less likely food poisoning because friends.'],'Food poisoning is less likely, because her friends are not sick.'),mc('🔴+🦟','Two clues: rash and mosquito bites.',['It is probably dengue, because she has a rash and she had mosquito bites.','It is probably dengue, because she has a rash or she had mosquito bites.','It is probably dengue because rash and mosquito.','It can\'t be dengue, because she has a rash and mosquito bites.'],'It is probably dengue, because she has a rash and she had mosquito bites.')])),
 dict(kind='order',title='Ask the patient',hint='Put the words in order to make the question.',levels=dict(
   bronze=[dict(pic='🌡️',words=['How','long','have','you','had','a','fever?'],extra=[]),dict(pic='🤕',words=['Where','does','it','hurt?'],extra=[])],
   silver=[dict(pic='🌡️',words=['How','long','have','you','had','a','fever?'],extra=['did','are']),dict(pic='😷',words=['Do','you','have','a','cough?'],extra=['Does','are']),dict(pic='🦟',words=['Have','you','been','bitten','by','mosquitoes?'],extra=['did','are'])],
   gold=[dict(pic='🌡️',words=['How','long','have','you','had','a','fever?'],extra=['did','are','since','for']),dict(pic='🦟',words=['Have','you','been','bitten','by','mosquitoes?'],extra=['did','are','bite','ever']),dict(pic='💊',words=['Have','you','taken','any','medicine?'],extra=['did','are','take','some'])])),
]

# ---------------- LESSON 4 : "The Sleepless Patient" (three dials) ----------------
L4_SUSPECTS=[('flu','Flu','🤧'),('food','Food poisoning','🤢'),('coffee','Too much coffee','☕'),('stress','Exam stress','📚'),('heart','Broken heart','💔')]
DIALS=[('A','How often?','#ff9a3c','every day · twice a week · never'),('B','How long? / When?','#2a8cf0','for two weeks · since Monday · at night'),('C','How bad?','#e0408a','a little · quite · very · 3 out of 10'),('D','Compared with normal?','#19b38a','more than · less than · the same as · normal: ...')]
def c4(id,team,r,topic,pic,a,b,c,d,fx,level=None):
    x=dict(id=id,team=team,r=r,topic=topic,pic=pic,dials=dict(A=a,B=b,C=c,D=d),fx=fx)
    if level: x['level']=level
    return x
L4_CLUES=[
 c4('R1','red',1,'Coffee','☕','She says: "Two cups a day." The café card says: 8 cups a day.','Every day for two weeks, since the exams started.','8 cups is a lot.','Usual limit for adults: about 4 or 5 cups a day.',{'coffee':'for'}),
 c4('R2','red',2,'Sleep','🛏️','She sleeps 3 hours most nights.','For two weeks. She wakes up at 3 am.','Very tired in the morning.','Adults need at least 7 hours. She sleeps less than half.',{'coffee':'for','stress':'for'}),
 c4('R3','red',3,'Pulse','💓','Pulse checked 3 times today: 108, 112, 110.','All day, even when she is sitting still.','Faster than normal. Not dangerous.','Normal pulse at rest: 60 – 100.',{'coffee':'for','stress':'for','flu':'for'}),
 c4('R4','red',4,'Temperature','🌡️','Checked twice a day.','36.8 °C for four days.','No fever.','Normal temperature: about 37 °C. Hers is normal.',{'flu':'against'}),
 c4('B1','blue',1,'Stomach','🍽️','She eats one meal a day, but she has no vomiting and no diarrhoea.','Normal stomach for the whole week.','A little hungry, not sick.','With food poisoning, vomiting or diarrhoea is common. She has none.',{'food':'against'}),
 c4('B2','blue',2,'Studying','📚','She studies every night.','Until 2 am, for two weeks.','Very tired.','Her classes start at 8 am.',{'stress':'for','coffee':'for'}),
 c4('B3','blue',3,'Headache','🤕','A headache most afternoons.','Since last week.','3 out of 10. That is mild (1–3 = mild).','0 = no pain. 10 = the worst pain.',{}),
 c4('B4','blue',4,'Phone','📱','She looks at her phone ten times an hour.','Pulse goes up every time it buzzes.','Pulse: about 15 higher than normal.','No new messages today.',{'heart':'for','stress':'for'},level='silver'),
 c4('G1','green',1,'Hands','✋','Her hands shake after every coffee.','For about 30 minutes after each cup.','A little shaky, not very.','Without coffee her hands are normal.',{'coffee':'for'}),
 c4('G2','green',2,'Cough','😷','She never coughs.','No cough for the whole week.','Throat is normal.','With flu, a cough is common. She has none.',{'flu':'against'}),
 c4('G3','green',3,'Mood','😟','She cries a little when people talk about exams.','Only when she talks about exams.','Quite worried.','Her friends say she is usually calm. Now she is worried.',{'stress':'for'}),
 c4('G4','green',4,'Energy','⚡','She is awake at night, tired in class.','Every night for two weeks.','Very tired but very awake at night.','She wants to sleep but she cannot.',{'coffee':'for','stress':'for'},level='silver'),
 c4('Y1','yellow',1,'Before','🗓️','She never had this before the exams.','It started two weeks ago.','A big change.','Last month she was normal.',{'stress':'for','coffee':'for'}),
 c4('Y2','yellow',2,'Sunday','😴','On Sunday she did not drink coffee.','She slept 9 hours and felt better by the evening.','Much better.','Her pulse on Sunday evening: 78. That is normal.',{'coffee':'for'}),
 c4('Y3','yellow',3,'Lunch','🍱','She ate lunch with three friends.','Same lunch, two days ago.','Her friends are fine.','Nobody else is sick.',{'food':'against'}),
 c4('Y4','yellow',4,'Exams','📅','Three exams in four days.','This week.','A lot of work.','Normal: one exam a week.',{'stress':'for'},level='silver'),
]
L4_TWIST=dict(pic='🗣️',text='A friend says: "It\'s just exam stress!"',say='Her friend thinks it is exam stress. But on Sunday, without coffee, she felt better.',fx={'stress':'for'})
L4_TEST=dict(q='Which test do we do?',opts=['Cut down the coffee slowly for a week. Then check her pulse and sleep.','Chest X-ray','Take a blood test for flu'],ans=0,
  why='If the pulse and sleep go back to normal when she cuts down the coffee, the coffee was the cause. (Stopping suddenly can cause headaches, so we cut down slowly.)')
L4_ANSWER='coffee'

L4_EX=[
 dict(kind='choice',title='How bad?',hint='0 = no pain. 10 = the worst pain.',levels=dict(
   bronze=[mc('2️⃣','Pain 2 out of 10',['mild','moderate','severe'],'mild'),mc('5️⃣','Pain 5 out of 10',['mild','moderate','severe'],'moderate'),mc('9️⃣','Pain 9 out of 10',['mild','moderate','severe'],'severe')],
   silver=[mc('2️⃣','The pain is 2 out of 10.',['It is a little painful.','It is very painful.','It is the worst pain.'],'It is a little painful.'),mc('5️⃣','The pain is 5 out of 10.',['It is quite painful.','It is not painful.','It is a little painful.'],'It is quite painful.'),mc('9️⃣','The pain is 9 out of 10.',['It is very painful.','It is a little painful.','It is quite painful.'],'It is very painful.')],
   gold=[mc('3️⃣','3 out of 10. Which is best?',['It is mild. It hurts a little.','It is severe. It hurts a lot.','It is mild. It hurts very much.','It is moderate. It hurts a little.'],'It is mild. It hurts a little.'),mc('6️⃣','6 out of 10. Which is best?',['It is moderate. It hurts quite a lot.','It is mild. It hurts a little.','It is severe. It hurts a little.','It is moderate. It does not hurt.'],'It is moderate. It hurts quite a lot.'),mc('8️⃣','8 out of 10. Which is best?',['It is severe. It hurts a lot.','It is mild. It hurts a lot.','It is severe. It hurts a little.','It is moderate. It hurts a lot.'],'It is severe. It hurts a lot.')])),
 dict(kind='choice',title='How often?',hint='Look at the week.',levels=dict(
   bronze=[mc('📅✔✔✔✔✔✔✔','7 days out of 7',['every day','twice a week','never'],'every day'),mc('📅✔ ✔','2 days out of 7',['every day','twice a week','never'],'twice a week'),mc('📅','0 days out of 7',['every day','twice a week','never'],'never')],
   silver=[mc('☕','8 cups, 7 days a week.',['She drinks coffee every day.','She drinks coffee twice a week.','She never drinks coffee.'],'She drinks coffee every day.'),mc('🏃','Runs Monday and Friday.',['She runs twice a week.','She runs every day.','She never runs.'],'She runs twice a week.'),mc('🚬','0 times.',['He never smokes.','He smokes every day.','He smokes twice a week.'],'He never smokes.')],
   gold=[mc('☕','7 days of 7. Which is best?',['She drinks coffee every day.','She drinks every day coffee.','She every day drinks coffee.','She drinks coffee all day every.'],'She drinks coffee every day.'),mc('📱','10 times an hour.',['She checks her phone ten times an hour.','She checks her phone ten time an hour.','She checks ten times her phone an hour.','She check her phone ten times an hour.'],'She checks her phone ten times an hour.'),mc('😴','Slept well: 1 night out of 7.',['She hardly ever sleeps well.','She always sleeps well.','She often sleeps well.','She never sleeps well.'],'She hardly ever sleeps well.')])),
 dict(kind='choice',title='How long?',hint='for + a time  ·  since + a start',levels=dict(
   bronze=[mc('🗓️','Started on Monday.',['since Monday','for Monday'],'since Monday'),mc('🕑','Two weeks.',['for two weeks','since two weeks'],'for two weeks'),mc('🕑','Three days.',['for three days','since three days'],'for three days')],
   silver=[mc('🗓️','It started on Monday.',['She has had a headache since Monday.','She has had a headache for Monday.','She had a headache since two days.'],'She has had a headache since Monday.'),mc('🕑','It started two weeks ago.',['She has felt tired for two weeks.','She has felt tired since two weeks.','She feels tired for Monday.'],'She has felt tired for two weeks.'),mc('📅','It started when the exams started.',['She has slept badly since the exams started.','She has slept badly for the exams started.','She slept badly since the exams.'],'She has slept badly since the exams started.')],
   gold=[mc('🗓️','Since Monday / for three days?',['She has been tired since Monday.','She has been tired for Monday.','She is tired since Monday.','She was tired since Monday.'],'She has been tired since Monday.'),mc('🕑','Two weeks.',['She has had a fast pulse for two weeks.','She has a fast pulse for two weeks.','She has had a fast pulse since two weeks.','She had a fast pulse for two weeks.'],'She has had a fast pulse for two weeks.'),mc('📅','Since the exams started.',['She has drunk eight cups of coffee a day since the exams started.','She drinks eight cups of coffee a day since the exams started.','She has drunk eight cups of coffee a day for the exams started.','She drank eight cups since exams.'],'She has drunk eight cups of coffee a day since the exams started.')])),
 dict(kind='choice',title='Compared with normal?',hint='Normal is on the right.',levels=dict(
   bronze=[mc('🛏️','Sleeps 3 hours.  Normal: 7+',['less than normal','more than normal'],'less than normal'),mc('💓','Pulse 110.  Normal: 60–100',['more than normal','less than normal'],'more than normal'),mc('🌡️','36.8 °C.  Normal: 37',['the same as normal','more than normal'],'the same as normal')],
   silver=[mc('🛏️','Sleeps 3 hours. Normal: 7 or more.',['She sleeps less than normal.','She sleeps more than normal.','She sleeps the same as normal.'],'She sleeps less than normal.'),mc('☕','Drinks 8 cups. Normal: 4 or 5.',['She drinks more coffee than normal.','She drinks less coffee than normal.','She drinks the same.'],'She drinks more coffee than normal.'),mc('🌡️','36.8 °C. Normal: 37.',['Her temperature is normal.','Her temperature is very high.','Her temperature is very low.'],'Her temperature is normal.')],
   gold=[mc('🛏️','3 hours. Normal 7 or more.',['She sleeps less than half the normal time.','She sleeps more than half the normal time.','She sleeps less than the normal half.','She sleeps normal than less.'],'She sleeps less than half the normal time.'),mc('☕','8 cups. Normal 4 or 5.',['She drinks about twice as much coffee as normal.','She drinks about two as much coffee as normal.','She drinks about twice more coffee normal.','She drinks about twice as much as coffee.'],'She drinks about twice as much coffee as normal.'),mc('💓','110. Normal 60–100.',['Her pulse is faster than normal.','Her pulse is more fast than normal.','Her pulse is faster normal.','Her pulse is as fast as normal.'],'Her pulse is faster than normal.')])),
 dict(kind='order',title='Say it with a dial',hint='Put the words in order.',levels=dict(
   bronze=[dict(pic='☕',words=['She','drinks','eight','cups','every','day.'],extra=[]),dict(pic='🛏️',words=['She','sleeps','less','than','normal.'],extra=[])],
   silver=[dict(pic='☕',words=['She','drinks','eight','cups','every','day.'],extra=['two','always']),dict(pic='🛏️',words=['She','has','slept','badly','for','two','weeks.'],extra=['since','is']),dict(pic='💓',words=['Her','pulse','is','faster','than','normal.'],extra=['more','as'])],
   gold=[dict(pic='☕',words=['She','has','drunk','eight','cups','a','day','since','the','exams','started.'],extra=['for','drinks']),dict(pic='🛏️',words=['She','sleeps','less','than','half','the','normal','time.'],extra=['more','as']),dict(pic='💓',words=['Her','pulse','has','been','faster','than','normal','all','day.'],extra=['is','since'])])),
]

# ---------------- BOSS CHALLENGES (optional, for fun) ----------------
L3_BOSS=dict(
 text='Had the patient\'s pyrexia been attributable to a bacterial aetiology, one would have anticipated a neutrophilic leucocytosis rather than the leucopenia and thrombocytopenia observed, which, in conjunction with the exanthem, are more consistent with an arboviral infection; antibiotics were therefore withheld.',
 q='Why did the doctor NOT give antibiotics?',
 plain=['pyrexia = fever','bacterial = from bacteria','leucopenia = low white cells','thrombocytopenia = low platelets','exanthem = rash','arboviral = a virus from insects (mosquitoes)'],
 simple='The fever was not from bacteria. Her white cells and platelets were LOW, and she had a rash. That fits a virus carried by mosquitoes (dengue).',
 answer='Because dengue is a virus. Antibiotics work on bacteria, not on viruses.')
L4_BOSS=dict(
 text='Notwithstanding the patient\'s insistence that her consumption is modest, the corroborating evidence indicates a habitual intake of approximately twice the recommended ceiling; abrupt cessation, however, may precipitate withdrawal symptoms such as headache and nervousness, so a gradual reduction is generally advised.',
 q='Why does the nurse say "cut down slowly" and not "stop today"?',
 plain=['notwithstanding = even though','consumption = how much she drinks','corroborating evidence = clues that agree','ceiling = limit','abrupt cessation = stopping suddenly','precipitate = cause'],
 simple='She says she drinks a little, but the clues say about double the limit. If she stops suddenly she can get a headache and feel nervous. So she should cut down slowly.',
 answer='Because stopping suddenly can give her a headache and make her nervous.')
