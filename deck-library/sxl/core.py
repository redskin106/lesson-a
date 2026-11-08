"""SkillsXLab lesson-deck core: theme, primitives, registry, renderer.
A module is a function(d)->html body, registered with @module('name'). Content is data (dicts); layout lives in modules.
"""
import asyncio, pathlib, os, shutil
FD='file:///home/claude/work/dir/node_modules/@fontsource/'
E='file:///home/claude/work/emoji/e3d/'
ART='file:///home/claude/work/lesson/art/'
def css(m):
    n=m=='night'; w=m=='white'
    bg='#0b0a10' if n else '#ffffff' if w else '#eeeef3'; tx='#f6f3ff' if n else '#1c1b2e'; mu='#a9a3cc' if n else '#6a6a7e'
    gl='rgba(255,255,255,.09)' if n else '#ffffff' if w else 'rgba(255,255,255,.66)'; gb='rgba(255,255,255,.18)' if n else '#e4e0f3' if w else 'rgba(255,255,255,.95)'
    sh='0 30px 70px rgba(0,0,0,.35)' if n else '0 30px 80px rgba(110,70,200,.22), 0 6px 16px rgba(110,70,200,.10)' if w else '0 30px 70px rgba(80,60,160,.18)'
    return f"""
@font-face{{font-family:O;font-weight:700;src:url({FD}outfit/files/outfit-latin-700-normal.woff2)}}
@font-face{{font-family:O;font-weight:800;src:url({FD}outfit/files/outfit-latin-800-normal.woff2)}}
@font-face{{font-family:P;font-weight:500;src:url({FD}poppins/files/poppins-latin-500-normal.woff2)}}
*{{box-sizing:border-box;margin:0}}
body{{width:1920px;height:1080px;overflow:hidden;position:relative;font-family:P,sans-serif;background:{bg};color:{tx}}}
.a{{position:absolute}} .h{{font-family:O;font-weight:800;line-height:1.02}} .mu{{color:{mu}}}
.orb{{position:absolute;border-radius:50%;filter:blur(260px);opacity:{.2 if n else .06 if w else .9}}}
.gl{{position:absolute;background:{gl};border:3px solid {gb};border-radius:56px;box-shadow:{sh}}}
.tag{{position:absolute;left:110px;top:64px;font-family:O;font-weight:700;font-size:34px;letter-spacing:.06em;padding:12px 38px;border-radius:999px;background:{gl};border:3px solid {gb};color:{'#c9a2ff' if n else '#6a35e8'}}}
.pg{{position:absolute;right:90px;bottom:22px;font-size:26px;color:{mu}}}
.ph{{position:absolute;background:linear-gradient(135deg,{'#2c2a52,#3d3a70' if n else '#d4d8e4,#b5bccd'});border:4px dashed {mu};border-radius:44px;display:flex;align-items:center;justify-content:center;text-align:center;color:{mu};font-size:38px;line-height:1.3}}
.chip{{display:inline-flex;flex-shrink:0;white-space:nowrap;align-items:center;font-family:O;font-weight:800;color:#fff;border-radius:44px;box-shadow:0 18px 34px rgba(80,60,160,.3),inset 0 3px 0 rgba(255,255,255,.45)}}
.c1{{background:linear-gradient(135deg,#34d0f2,#2a8cf0)}} .c2{{background:linear-gradient(135deg,#9a5cff,#6a35e8)}} .c3{{background:linear-gradient(135deg,#ff9a3c,#ff4fa3)}} .c4{{background:linear-gradient(135deg,#ffd21f,#ff9a3c);color:#3a2300}}
.pill{{display:inline-flex;align-items:center;font-family:O;font-weight:700;border-radius:999px;background:{gl};border:3px solid {gb}}}
img.e{{position:absolute;filter:drop-shadow(0 22px 26px rgba(40,20,90,.3))}}
.grad{{background:linear-gradient(90deg,{'#c9a2ff,#ff8cc6' if n else '#7b3cf0,#ff4fa3'});-webkit-background-clip:text;color:transparent}}
"""

# ---------- tokens ----------
GR="background:linear-gradient(135deg,#9a5cff,#ff4fa3);color:#fff;box-shadow:0 14px 28px rgba(120,60,200,.35),inset 0 3px 0 rgba(255,255,255,.45);border:none"
GRAD={'violet':'linear-gradient(135deg,#7b3cf0,#ff4fa3)','red':'linear-gradient(135deg,#ff6b78,#ff3d4f)','teal':'linear-gradient(135deg,#2bd9b6,#10a98d)',
      'amber':'linear-gradient(135deg,#ffc13b,#ff9f1c)','rose':'linear-gradient(135deg,#ff8aa8,#ff4f7a)','orange':'linear-gradient(135deg,#ff9a3c,#ff5a1f)','sky':'linear-gradient(135deg,#34d0f2,#2a8cf0)'}
PAL={'ENGAGE':[('#ffd27a',-300,-300,1300,1100),('#ff9fb8',700,-420,1200,950),('#ffb066',1050,380,1250,1000),('#ffc6a0',-300,520,1000,900),('#d9b8ff',450,300,900,800)],
     'STUDY':[('#b98cff',-300,-300,1300,1100),('#8fb4ff',700,-420,1200,950),('#7fd3ff',1050,380,1250,1000),('#c9a2ff',-300,520,1000,900),('#ffb7d5',450,300,900,800)],
     'ACTIVATE':[('#9fe8c4',-300,-300,1300,1100),('#7fe0d8',700,-420,1200,950),('#c8f2a8',1050,380,1250,1000),('#b5f0e0',-300,520,1000,900),('#a8e6ff',450,300,900,800)]}
def phase_orbs(p,k=1.5):
    cs=[(c,x-(k-1)/2*w,y-(k-1)/2*h,k*w,k*h) for c,x,y,w,h in PAL[p]]
    return ''.join(f'<div class="orb" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c}"></div>' for c,x,y,w,h in cs)

# ---------- primitives ----------
EM=lambda n:f'{E}{n}.png'
def em(n,x,y,w,r=0): return f'<img class="e" src="{E}{n}.png" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({r}deg)">'
ch=lambda c,t,fs=64,p='10px 34px':f'<span class="chip {c}" style="font-size:{fs}px;padding:{p};border-radius:44px">{t}</span>'
def grad_chip(g,t,fs=44,p='8px 34px'): return f'<span class="chip" style="font-size:{fs}px;padding:{p};border-radius:999px;background:{GRAD.get(g,g)}">{t}</span>'
def gap(col,w,t='…',h=104,fs=40): return f'<div style="width:{w}px;height:{h}px;border-radius:44px;border:5px dashed {col};display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:{fs}px;color:{col}">{t}</div>'
def num(x,y,n,s=64): return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:O;font-weight:800;font-size:{int(s*.6)}px;{GR}">{n}</div>'
def header(phase,role=None,rg='violet'):
    h=f'<div class="a" style="left:90px;top:56px;display:flex;align-items:center;gap:24px"><div class="tag" style="position:static;{GR}">{phase}</div>'
    if role: h+=grad_chip(rg,role,34,'12px 38px')
    return h+'</div>'
def pic(x,y,w,h,f,r=40,fit='cover'):
    if not os.path.exists('/home/claude/work/lesson/art/'+f): return ph(x,y,w,h,f,r=r)
    return f'<div class="gl" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{r}px;padding:10px"><img src="{ART}{f}" style="width:100%;height:100%;object-fit:{fit};background:#fff;border-radius:{r-10}px;display:block"></div>'
def ph(x,y,w,h,label,fs=32,r=56,dim=False):
    return f'<div class="gl" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{r}px;padding:14px;{"opacity:.55;" if dim else ""}"><div style="width:100%;height:100%;border-radius:{r-16}px;background:linear-gradient(135deg,#c8ceda,#9aa5b8);border:4px dashed #6a6a7e;display:flex;align-items:center;justify-content:center;font-size:{fs}px;color:#4a5a6e;text-align:center;line-height:1.3;padding:16px">{label}</div></div>'
def art(x,y,w,h,f,r=40,label='',fit='cover'):
    """picture if the art file exists, otherwise a labelled placeholder (lets decks build before art arrives)"""
    return pic(x,y,w,h,f,r,fit) if os.path.exists('/home/claude/work/lesson/art/'+f) else ph(x,y,w,h,label or f,r=r)
def glass(x,y,w,h,inner='',r=56,ex=''): return f'<div class="gl" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{r}px;{ex}">{inner}</div>'
def chips(row,fs=64,p='10px 34px'):
    """row = [('c1','You'),('c2','should'),...]"""
    return ''.join(ch(c,t,fs,p) for c,t in row)

# ---------- registry + render ----------
MODULES={}; EXPAND={}
def module(name,expand=None):
    """expand(d)->[d,...] lets a module turn one data dict into several static slides (e.g. a scrolling chat)."""
    def deco(fn):
        MODULES[name]=fn
        if expand: EXPAND[name]=expand
        return fn
    return deco
def expand_spec(spec):
    out=[]
    for d in spec: out+=EXPAND[d['m']](d) if d['m'] in EXPAND else [d]
    return out
def slide_html(d):
    fn=MODULES[d['m']]; body=fn(d)
    mode=d.get('mode','day'); ph_=d.get('phase')
    orbs=phase_orbs(ph_) if ph_ in PAL and mode=='day' else ''
    return mode, orbs+body
def build(spec,outdir,pdf=None,light=True):
    """spec = list of slide dicts {'m': module, 'phase': 'STUDY', ...data}. Writes PNGs (and optional PDF)."""
    import importlib, pkgutil
    from playwright.async_api import async_playwright
    spec=expand_spec(spec)
    shutil.rmtree(outdir,ignore_errors=True); os.makedirs(outdir)
    async def main():
        async with async_playwright() as p:
            b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1920,'height':1080})
            for n,d in enumerate(spec,1):
                m,body=slide_html(d)
                pathlib.Path('/tmp/sxl_t.html').write_text(f'<html><head><style>{css(m)}</style></head><body>{body}<div class="pg">{n}</div></body></html>')
                await pg.goto('file:///tmp/sxl_t.html'); await pg.wait_for_timeout(300)
                await pg.screenshot(path=f'{outdir}/{n:02d}.png')
            await b.close()
    asyncio.run(main())
    if pdf:
        from PIL import Image
        fs=sorted(pathlib.Path(outdir).glob('*.png'))
        ims=[Image.open(f).convert('RGB') for f in fs]
        if light: ims=[i.resize((1280,720),Image.LANCZOS) for i in ims]
        ims[0].save(pdf,save_all=True,append_images=ims[1:],resolution=96,quality=55)
    return outdir

def stp(html,s,g=None,pills=False):
    """Mark element as reveal step s (click-per-step in interactive decks; ignored in static output)."""
    i=html.index('<'); j=html.index(' ',i)
    return html[:j]+f' data-s="{s}"'+(f' data-g="{g}"' if g else '')+(' data-pills="1"' if pills else '')+html[j:]
