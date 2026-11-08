import sys; sys.path.insert(0,"/home/claude/work/lesson")
import asyncio
from playwright.async_api import async_playwright
from lessons.plan import L1,L2
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
