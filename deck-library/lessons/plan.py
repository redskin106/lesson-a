"""Planned minutes per slide/block (estimates, not tested in class). Rows map 1:1 to slides in order."""
L1=[('Cover','1','Show the title; no talking needed'),('Homework comic','2','"What can you see?" Students tell the story in pairs'),('What should he do?','3','Ball pass: any advice in any English is welcome'),
('Today we learn','1','Read the two sentences aloud once'),('Boss strip','2','Watch first, then say: Boss -> have to'),('Friend strip','2','Same story, Friend -> should'),('Boss: have to / don’t have to','2','Needed / Not needed'),
('Neighbour vs Pharmacist','3','Good idea? / Needed.'),('Dial','3','Five stops. Point and say each one'),('Pair talk','2','OPTIONAL: tell your partner one thing you should / shouldn’t do tonight'),('mustn’t vs don’t have to','2','Not allowed / Not needed'),
('Homework revisited','2','OPTIONAL: fold into the dial'),('Swap!','3','OPTIONAL: Boss should vs Friend have to'),('Sort 1 (pick words)','4','Tap/point; class decides together'),('Sort 2 (negatives)','5','mustn’t only fits the car'),
('Questions card','1','CHECKPOINT: skip slides 15-16 if the class already asks these'),('Question it','2','CHECKPOINT'),('Nurse chat (running)','4','Fill the gaps; scroll back to reread'),('Doctor chat','2','have to / don’t have to'),
('Neighbour twist chat','2','OPTIONAL: Activate twists cover this'),('The Hotline','1','Title only'),('Roles','2','Patient / Nurse / Doctor groups of 3'),('Watch the twist','2','Model the stubborn patient'),('Twists','1','Gibberish, Drama, Stubborn, Neighbour'),
('Slot machine','1','One spin for all groups'),('Nurse prep','3','Question builder + advice tiles + repair kit; 3:00 timer'),('Doctor prep','1','have to tiles'),('Group practice and 1-2 live performances','8','Everyone speaks at once'),('Recap','2','Read down the left, then questions on the right')]
L2=[('Case cover','1','Detective hook: "Something strange happened."'),('Evidence board','2','Pictures first, no words'),('The quacks (cast)','2','Meet the four patients'),('Where does it hurt?','1','Four symptoms'),
('Case 1 storyboard','2','Last panel hidden: what happened?'),('Irregular verbs','2','wore, stood, ate, drank, slept: picture then word'),('-ed verbs','2','washed, rubbed, painted'),('Today / yesterday','1','Contrast'),
('Sound sort (blank)','2','TEACHER MODELS: dot, buzz, two dots. Say each word aloud; no audio in the slides'),('Sound sort (solved)','1','Check together'),('Story order','2','CUT FIRST if short on time'),('Sort: wore, stood, ate, slept','3','Tap word then picture'),
('Nurse asks (chat)','4','What did you do? / When did it start? / Did you…?  CUT second step if short'),('Role cards (pairs)','2','Nurse cannot see the case: information gap'),('Choose a case','1','Pairs pick Case 1-4'),
('Story order (case 2)','3','OPTIONAL'),('Spot the fib','2','True or a fib?'),('Match diagnosis','2','Picture to word'),('Doctor advice (chat)','3','Imperatives only: Don’t eat / Take / Rest'),('Pair practice: solve a case','12','Nurse asks, patient answers, doctor advises'),('Cases Solved board','1','Collective, no scores'),('Closing','1','Night mode, quiet finish')]

def apply(spec,rows):
    assert len(spec)==len(rows),(len(spec),len(rows))
    for d,r in zip(spec,rows): d['min']=float(r[1]); d['label']=r[0]
    return spec
