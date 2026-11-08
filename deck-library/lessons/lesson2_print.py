"""Lesson 2 printable set (A4 landscape): teacher key, case cards, patient sheets, nurse + doctor cards."""
import sys; sys.path.insert(0,'/home/claude/work/lesson')
import asyncio, pathlib
from playwright.async_api import async_playwright
from sxl.core import css, ART
Q={1:'l2_quack_2.jpg',2:'l2_quack_3.jpg',3:'l2_quack_1.jpg',4:'l2_quack_4.jpg'}
NAME={1:'Neighbour',2:'Grandma',3:'Influencer',4:'Market Uncle'}
DIAG={1:('sprained ankle','wore · stood'),2:('stomach ache','ate · drank'),3:('rash','rubbed · painted'),4:('headache','washed · slept')}
def img(f,w,h=None,r=14): return f'<img src="{ART}{f}" style="width:{w}px;height:{h or w}px;object-fit:contain;background:#fff;border-radius:{r}px;border:2px solid #d9d4ee">'
def chip(t,c='c2',fs=22): return f'<span class="chip {c}" style="font-size:{fs}px;padding:6px 18px;border-radius:40px">{t}</span>'
def page(title,body,sub=''): return f'<section style="width:1123px;height:794px;position:relative;page-break-after:always;overflow:hidden;background:#fff;padding:34px 44px"><div style="display:flex;align-items:center;gap:18px;margin-bottom:18px"><div class="h grad" style="font-size:38px">{title}</div><div class="mu" style="font-size:20px">{sub}</div></div>{body}</section>'
pages=[]
# 1 teacher key
rows=''
for n in (1,2,3,4):
    rows+=f'<div style="display:flex;align-items:center;gap:16px;margin-bottom:14px">{img(Q[n],110,150)}<div style="width:120px;font-family:O;font-weight:800;font-size:24px">Case {n}<br><span class="mu" style="font-size:18px">{NAME[n]}</span></div>'+''.join(f'<div style="text-align:center">{img(f"case{n}_{k}.jpg",130)}<div class="h" style="font-size:20px">{k}</div></div>' for k in range(1,5))+f'<div style="margin-left:14px">{chip(DIAG[n][0],"c3")}<div style="margin-top:8px">{chip(DIAG[n][1],"c2",20)}</div></div></div>'
pages.append(page('Teacher key','<div>'+rows+'</div>','correct order, diagnosis, verbs'))
# 2-5 case cards
for n in (1,2,3,4):
    order=[2,0,3,1] if n%2 else [3,1,0,2]
    cells=''.join(f'<div style="position:relative;border:2px dashed #b9a6f5;border-radius:18px;padding:10px">{img(f"case{n}_{k+1}.jpg",300)}<div style="position:absolute;left:14px;top:14px">{img(Q[n],56,76,10)}</div></div>' for k in order)
    pages.append(page(f'Case {n} · cut out and put in order',f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px;width:700px;margin:0 auto">{cells}</div>','cut along the dotted lines'))
# 6 patient sheets
strips=''
for n in (1,2,3,4):
    strips+=f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:10px">{img(Q[n],70,92,10)}<div class="h" style="font-size:22px;width:70px">Case {n}</div>'+''.join(img(f"case{n}_{k}.jpg",140) for k in range(1,5))+'</div>'
pages.append(page('Patient sheet','<div>'+strips+'</div>','the patient looks at the pictures · the nurse cannot see them'))
# 7 nurse cards
def qcard(chips_,icon=''): return f'<div style="border:2px dashed #b9a6f5;border-radius:18px;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:10px">{icon}<div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center">{chips_}</div></div>'
c=lambda a,b:f'{chip(a,"c4",26)}{chip(b[0],"c2",26)}{chip(b[1],"c1",26)}{chip(b[2],"c3",26)}'
qs=[qcard(chip('What','c4',28)+chip('did','c2',28)+chip('you','c1',28)+chip('do?','c2',28)),
    qcard(chip('When','c4',28)+chip('did','c2',28)+chip('it','c1',28)+chip('start?','c2',28)),
    qcard(chip('Did','c2',28)+chip('you','c1',28)+chip('eat','c2',28)+chip('anything?','c3',28)),
    qcard(chip('Did','c2',28)+chip('you','c1',28)+chip('sleep','c2',28)+chip('well?','c3',28)),
    qcard(chip('Don’t eat','c2',28)+chip('…','c3',28),img('adv_nobanana.jpg',120)),
    qcard(chip('Take','c2',28)+chip('this medicine.','c3',28),img('adv_pill.jpg',120)),
    qcard(chip('Rest','c2',28),img('adv_rest.jpg',120)),
    qcard(chip('Thank you, doctor.','c1',26))]
pages.append(page('Nurse and doctor cards',f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px">{"".join(qs)}</div>','cut out · nurse asks, doctor advises'))
html=f'<html><head><style>{css("white")} body{{width:auto;height:auto;overflow:visible}}</style></head><body>{"".join(pages)}</body></html>'
pathlib.Path('/tmp/print.html').write_text(html)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(); await pg.goto('file:///tmp/print.html'); await pg.wait_for_timeout(600)
        await pg.pdf(path='/home/claude/work/lesson/SkillsXLab_Lesson2_printables.pdf',width='1123px',height='794px',print_background=True,margin={'top':'0','bottom':'0','left':'0','right':'0'}); await b.close()
asyncio.run(main())
