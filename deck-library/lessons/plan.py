"""Planned minutes per slide/block (estimates, not tested in class). Rows map 1:1 to slides in order."""
L1=[('Cover','1','Show the title; no talking needed'),('Homework comic','2','"What can you see?" Students tell the story in pairs'),('What should he do?','3','Ball pass: any advice in any English is welcome'),
('Today we learn','1','Read the two sentences aloud once'),('Boss strip','2','Watch first, then say: Boss -> have to'),('Friend strip','2','Same story, Friend -> should'),('Boss: have to / don’t have to','2','Needed / Not needed'),
('Neighbour vs Pharmacist','3','Good idea? / Needed.'),('Dial','3','Five stops. Point and say each one'),('Pair talk','2','OPTIONAL: tell your partner one thing you should / shouldn’t do tonight'),('mustn’t vs don’t have to','2','Not allowed / Not needed'),
('Homework revisited','2','OPTIONAL: fold into the dial'),('Swap!','3','OPTIONAL: Boss should vs Friend have to'),('Sort 1 (pick words)','4','Tap/point; class decides together'),('Sort 2 (negatives)','5','mustn’t only fits the car'),
('Questions card','1','CHECKPOINT: skip slides 15-16 if the class already asks these'),('Question it','2','CHECKPOINT'),('Nurse chat (running)','4','Fill the gaps; scroll back to reread'),('Doctor chat','2','have to / don’t have to'),
('Neighbour twist chat','2','OPTIONAL: Activate twists cover this'),('The Hotline','1','Title only'),('Roles','2','Patient / Nurse / Doctor groups of 3'),('Watch the twist','2','Model the stubborn patient'),('Twists','1','Gibberish, Drama, Stubborn, Neighbour'),
('Slot machine','1','One spin for all groups'),('Nurse prep','3','Question builder + advice tiles + repair kit; 3:00 timer'),('Doctor prep','1','have to tiles'),('Group practice and 1-2 live performances','8','Everyone speaks at once'),('Recap','2','Read down the left, then questions on the right'),('Thank you','0','Wave goodbye')]
L2=[('Case cover','1','Detective hook: "Something strange happened."'),('Evidence board','2','Pictures first, no words'),('The quacks (cast)','2','Meet the four patients'),('Where does it hurt?','1','Four symptoms'),
('Case 1 storyboard','2','Last panel hidden: what happened?'),('Irregular verbs','2','wore, stood, ate, drank, slept: picture then word'),('-ed verbs','2','washed, rubbed, painted'),('Today / yesterday','1','Contrast'),
('Sound sort (blank)','2','TEACHER MODELS: dot, buzz, two dots. Say each word aloud; no audio in the slides'),('Sound sort (solved)','1','Check together'),('Story order','2','CUT FIRST if short on time'),('Sort: wore, stood, ate, slept','3','Tap word then picture'),
('Nurse asks (chat)','4','What did you do? / When did it start? / Did you…?  CUT second step if short'),('Role cards (pairs)','2','Nurse cannot see the case: information gap'),('Choose a case','1','Pairs pick Case 1-4'),
('Story order (case 2)','3','OPTIONAL'),('Spot the fib','2','True or a fib?'),('Match diagnosis','2','Picture to word'),('Doctor advice (chat)','3','Imperatives only: Don’t eat / Take / Rest'),('Pair practice: solve a case','12','Nurse asks, patient answers, doctor advises'),('Cases Solved board','1','Collective, no scores'),('Closing','1','Night mode, quiet finish')]

def apply(spec,rows):
    assert len(spec)==len(rows),(len(spec),len(rows))
    for d,r in zip(spec,rows): d['min']=float(r[1]); d['label']=r[0]
    return spec

L2V2=[('Cover','1','Show the title; no talking needed'),('What happened?','2','Pictures first: students guess in any language'),('Where does it hurt?','2','Four problems: point and say each one'),
('Today we learn','1','Read the two sentences aloud once: Why? / because'),('Why? (1)','3','Cause, arrow, result, then the sentence: stomach, cold'),('Why? (2)','2','Back, arm: say the because-sentence together'),
('Yesterday (5 verbs)','2','eat/ate, drink/drank, sleep/slept, fall/fell, go/went'),('Yesterday (4 more verbs)','1','OPTIONAL: take/took, feel/felt, have/had, start/started'),
('Every day / yesterday','2','Pink time word: the verb changes'),('Time words','2','OPTIONAL: Yesterday / last night / this morning'),('Sort: because I ...','4','Drag the past verb; wrong springs back'),('Sort 2: drank, took','2','OPTIONAL'),
('Why? check (1)','1','OPTIONAL: tap the cause; watch who hesitates'),('Why? check (2)','1','OPTIONAL'),('Statement / question','2','I ate spicy food. / Did you eat spicy food? The verb goes back to eat'),('Nurse chat','5','What\u2019s wrong? Why? When did it start? Did you eat?'),
('Your turn','2','OPTIONAL: tell your partner one thing you did yesterday'),('Doctor chat','3','OPTIONAL: imperatives only (Don\u2019t eat / Drink)'),
('The Clinic','1','Title only'),('Roles','2','Patient knows the cause; nurse asks why'),('Watch the model','1','Read the exchange together before pairs'),('Patient card','1','Patient sees the cause; nurse sees the problem'),
('Nurse prep','3','Question builder; 3:00 timer'),('Patient prep','2','Sentence frames and past verbs'),('Choose a patient','1','Pairs pick Patient 1-6'),('Slot machine','1','OPTIONAL: one spin, new patients'),
('Find the cause (pairs)','9','Nurse asks, patient answers, swap'),('Patients helped','2','Shared board: no scores'),('Recap','2','Read down the page together'),('Thank you','0','Close')]

L2V3=[('Cover','1','Show the title; no talking needed'),('What’s wrong?','2','One picture. Students say it in any language; teacher says: My back hurts.'),
('Why? (hook strip)','2','Dog, floor, back. Watch first, then say: because I slept on the floor'),
('Where does it hurt?','2','Four pains: point and say My ___ hurts'),('Today we learn','1','Now: hurts. Before: ate. One sentence carries both'),
('Does your head hurt?','2','Statement / question: the verb goes back to hurt'),('Nurse chat 1','2','Does your ___ hurt? Two gaps'),
('Yesterday (5 verbs)','2','eat/ate, drink/drank, sleep/slept, fall/fell, go/went'),('Yesterday (4 more verbs)','1','OPTIONAL: take/took, feel/felt, have/had, start/started'),
('Today / yesterday','2','Pink time word: the verb changes'),('Sort: because I ...','3','Drag the past verb; wrong springs back'),('Sort 2: drank, took','2','OPTIONAL'),
('I ate / Did you eat?','2','The same rule as hurt: after did the verb goes back to plain'),('Three little rules','1','Read down: Does → hurt, Did → eat, because → the reason'),('Model strip: now and yesterday','3','Row 1 asks about now (Does). Row 2 asks about before (Did)'),('Connect: before, now, after','3','Tap a picture, then its partner: they slide into one row and an arrow draws. Say each finished sentence together'),
('Help the robot nurse','2','Fix the robot: hurt / fall / drink. CUT the third gap if short'),('Nurse chat 2','3','Why? Because I ate ... Did you eat anything?'),
('Why? check (1)','1','OPTIONAL: tap the cause; watch who hesitates'),('Why? check (2)','1','OPTIONAL'),('Your turn','2','OPTIONAL: tell your partner one thing you did yesterday'),
('The Clinic','1','Title only'),('Roles','1','Patient mimes and answers; Nurse asks Does...; Doctor asks Did...'),('Watch the circle','2','Teacher demonstrates once: mime, ball, ball'),('Think','1','Choose a pain and a cause. Keep it secret'),
('Ball circle','10','Circles of five. Word bank stays on screen. Teacher listens and notes mistakes'),('Silver: habits','2','OPTIONAL: Do you ... every day? / Did you ... yesterday?'),
('Recap','2','Read down the page together. Mistakes noted in the circle are repaired here'),('Thank you','0','Close')]
