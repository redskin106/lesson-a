import asyncio
from playwright.async_api import async_playwright
L1=[('Cover','1','Show the title; no talking needed'),('Homework comic','2','"What can you see?" Students tell the story in pairs'),('What should he do?','3','Ball pass: any advice in any English is welcome'),
('Today we learn','1','Read the two sentences aloud once'),('Boss strip','2','Watch first, then say: Boss -> have to'),('Friend strip','2','Same story, Friend -> should'),('Boss: have to / don’t have to','2','Needed / Not needed'),
('Neighbour vs Pharmacist','3','Good idea? / Needed.'),('Dial','3','Five stops. Point and say each one. Then 2-minute pair talk: one thing you should / shouldn’t do tonight'),('mustn’t vs don’t have to','2','Not allowed / Not needed'),
('Homework revisited','2','OPTIONAL: fold into the dial'),('Swap!','3','OPTIONAL: Boss should vs Friend have to'),('Sort 1 (pick words)','4','Tap/point; class decides together'),('Sort 2 (negatives)','5','mustn’t only fits the car'),
('Questions card','1','CHECKPOINT: skip slides 15-16 if the class already asks these'),('Question it','2','CHECKPOINT'),('Nurse chat (running)','4','Fill the gaps; scroll back to reread'),('Doctor chat','2','have to / don’t have to'),
('Neighbour twist chat','2','OPTIONAL: Activate twists cover this'),('The Hotline','1','Title only'),('Roles','2','Patient / Nurse / Doctor groups of 3'),('Watch the twist','2','Model the stubborn patient'),('Twists','1','Gibberish, Drama, Stubborn, Neighbour'),
('Slot machine','1','One spin for all groups'),('Nurse prep','3','Question builder + advice tiles + repair kit; 3:00 timer'),('Doctor prep','1','have to tiles'),('Group practice and 1-2 live performances','8','Everyone speaks at once'),('Recap','2','Read down the left, then questions on the right')]
L2=[('Case cover','1','Detective hook: "Something strange happened."'),('Evidence board','2','Pictures first, no words'),('The quacks (cast)','2','Meet the four patients'),('Where does it hurt?','1','Four symptoms'),
('Case 1 storyboard','2','Last panel hidden: what happened?'),('Irregular verbs','2','wore, stood, ate, drank, slept: picture then word'),('-ed verbs','2','washed, rubbed, painted'),('Today / yesterday','1','Contrast'),
('Sound sort (blank)','2','TEACHER MODELS: dot, buzz, two dots. Say each word aloud; no audio in the slides'),('Sound sort (solved)','1','Check together'),('Story order','2','CUT FIRST if short on time'),('Sort: wore, stood, ate, slept','3','Tap word then picture'),
('Nurse asks (chat)','4','What did you do? / When did it start? / Did you…?  CUT second step if short'),('Role cards (pairs)','2','Nurse cannot see the case: information gap'),('Choose a case','1','Pairs pick Case 1-4'),
('Story order (case 2)','3','OPTIONAL'),('Spot the fib','2','True or a fib?'),('Match diagnosis','2','Picture to word'),('Doctor advice (chat)','3','Imperatives only: Don’t eat / Take / Rest'),('Pair practice: solve a case','12','Nurse asks, patient answers, doctor advises'),('Cases Solved board','1','Collective, no scores'),('Closing','1','Night mode, quiet finish')]
def page(title,rows,note):
    tot=sum(float(r[1]) for r in rows); opt=sum(float(r[1]) for r in rows if 'OPTIONAL' in r[2] or 'CUT' in r[2] or 'CHECKPOINT' in r[2])
    tr=''.join(f'<tr class="{"o" if any(k in r[2] for k in ("OPTIONAL","CUT","CHECKPOINT")) else ""}"><td>{i+1}</td><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>' for i,r in enumerate(rows))
    return f'<h1>{title}</h1><p>Total {tot:g} min. Optional/cut rows (shaded) {opt:g} min, so core {tot-opt:g} min. Estimates, not yet tested in class. {note}</p><table><tr><th>#</th><th>Slide / block</th><th>min</th><th>Cue</th></tr>{tr}</table>'
H=('<style>body{font-family:Outfit,Arial,sans-serif;font-size:11px}h1{font-size:20px;margin:0 0 4px}table{border-collapse:collapse;width:100%;margin-top:8px}td,th{border-bottom:1px solid #ddd;padding:3px 6px;text-align:left}th{background:#eee}tr.o td{background:#f1e9ff}.pb{page-break-after:always}</style>')
html=H+'<div class="pb">'+page('Lesson 1: have to / should (run sheet)',L1,'Pair talk after the dial is a suggested addition.')+'</div>'+page('Lesson 2: The Case of the Strange Patient (run sheet)',L2,'Teacher models the sound sort.')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(); await pg.set_content(html); await pg.pdf(path='/home/claude/work/lesson/SkillsXLab_run_sheets.pdf',format='A4',margin={'top':'14mm','bottom':'14mm','left':'12mm','right':'12mm'})
asyncio.run(main())
