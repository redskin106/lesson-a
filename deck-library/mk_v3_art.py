"""Placeholder art for Lesson 2 v3: simple stickmen + emoji props on pale backgrounds. Real art comes from Gemini later."""
from PIL import Image, ImageDraw
import os
E='/home/claude/work/emoji/e3d/'; OUT='/home/claude/work/lesson/art/'
INK=(28,27,46); RED=(235,64,52); W,H=1280,720

def base(bg=(250,246,255)):
    im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im); return im,d
def emo(im,name,cx,cy,s):
    e=Image.open(E+name+'.png').convert('RGBA').resize((s,s)); im.paste(e,(int(cx-s/2),int(cy-s/2)),e)
def line(d,pts,w=12): d.line(pts,fill=INK,width=w,joint='curve')
def burst(d,x,y,r=46):
    d.ellipse([x-r,y-r,x+r,y+r],outline=RED,width=10)
    import math
    for a in range(0,360,45):
        c,s=math.cos(math.radians(a)),math.sin(math.radians(a)); d.line([x+c*(r+12),y+s*(r+12),x+c*(r+40),y+s*(r+40)],fill=RED,width=10)
def man(d,x,y,pose='stand',s=1.0,flip=1):
    """x,y = feet centre. pose: stand, back, stomach, head, arm, eat, lie"""
    hr=int(58*s); body=int(190*s); leg=int(150*s); arm=int(120*s)
    hx,hy=x,y-leg-body-hr; sx,sy=x,y-leg-body+int(20*s); hipy=y-leg
    if pose=='lie':
        # lying on the floor, head to the left
        hx,hy=x-int(210*s),y-hr-6; d.ellipse([hx-hr,hy-hr,hx+hr,hy+hr],outline=INK,width=12,fill=(255,255,255))
        line(d,[(hx+hr,hy+10),(x+int(160*s),hy+10)],12); line(d,[(x+int(160*s),hy+10),(x+int(300*s),y-int(60*s))],12); line(d,[(x+int(160*s),hy+10),(x+int(310*s),y-6)],12)
        line(d,[(hx+hr+int(40*s),hy+10),(hx+hr+int(120*s),y-int(60*s))],12); return
    d.ellipse([hx-hr,hy-hr,hx+hr,hy+hr],outline=INK,width=12,fill=(255,255,255))
    line(d,[(x,hy+hr),(x,hipy)],12)
    line(d,[(x,hipy),(x-int(60*s),y)],12); line(d,[(x,hipy),(x+int(60*s),y)],12)
    ay=sy
    if pose=='stand': line(d,[(x,ay),(x-arm,ay+int(100*s))],12); line(d,[(x,ay),(x+arm,ay+int(100*s))],12)
    if pose=='back':
        line(d,[(x,ay),(x-int(110*s),ay+int(60*s)),(x-int(70*s),hipy-int(30*s))],12); line(d,[(x,ay),(x+arm,ay+int(100*s))],12); burst(d,x-int(70*s)-30,hipy-int(60*s),int(40*s))
    if pose=='stomach':
        line(d,[(x,ay),(x-int(80*s),ay+int(80*s)),(x-int(10*s),ay+int(120*s))],12); line(d,[(x,ay),(x+int(80*s),ay+int(80*s)),(x+int(10*s),ay+int(120*s))],12); burst(d,x,ay+int(150*s),int(44*s))
    if pose=='head':
        line(d,[(x,ay),(x-int(100*s),ay-int(20*s)),(hx-hr+6,hy+10)],12); line(d,[(x,ay),(x+int(100*s),ay-int(20*s)),(hx+hr-6,hy+10)],12); burst(d,hx,hy-hr-30,int(34*s))
    if pose=='arm':
        line(d,[(x,ay),(x-arm,ay+int(100*s))],12); line(d,[(x,ay),(x+int(110*s),ay+int(60*s))],12); line(d,[(x+int(110*s),ay+int(60*s)),(x+int(60*s),ay+int(130*s))],12); burst(d,x+int(120*s)+20,ay+int(70*s),int(36*s))
    if pose=='eat':
        line(d,[(x,ay),(x-arm,ay+int(100*s))],12); line(d,[(x,ay),(x+int(100*s),ay+int(40*s)),(hx+hr+10,hy+hr)],12)
    if pose in ('back','stomach','head','arm'):
        d.arc([hx-24,hy+6,hx+24,hy+40],200,340,fill=INK,width=8)   # unhappy mouth
    return

def save(im,name): im.convert('RGB').save(OUT+name,quality=88)

# ---- pain pictures (cast / word bank)
for n,p,bg in [('head','head',(255,244,244)),('stomach','stomach',(255,246,236)),('back','back',(245,244,255)),('arm','arm',(238,248,255))]:
    im,d=base(bg); d.line([(0,640),(W,640)],fill=(220,215,235),width=6); man(d,W//2,640,p,1.0 if p=='head' else 1.25); save(im,f'v3_{n}.jpg')

# ---- portrait (cast) and square (word bank) pain pictures: big figure
def gen(prefix,w,h,floor,scale):
    global W,H
    W,H=w,h
    for n,p,bg in [('head','head',(255,244,244)),('stomach','stomach',(255,246,236)),('back','back',(245,244,255)),('arm','arm',(238,248,255))]:
        im,d=base(bg); d.line([(0,floor),(W,floor)],fill=(220,215,235),width=6); man(d,W//2,floor,p,scale*(0.85 if p=='head' else 1)); save(im,f'{prefix}_{n}.jpg')
gen('v3p',720,1120,1020,1.75); gen('v3s',600,600,560,1.0)
W,H=1280,720

# ---- hook strip: dog on bed -> sleeps on floor -> back hurts
im,d=base((250,246,255)); d.line([(0,640),(W,640)],fill=(220,215,235),width=6); emo(im,'bed',820,520,380); emo(im,'dog_face',840,390,170); man(d,330,640,'stand',1.2); save(im,'v3_hook1.jpg')
im,d=base((236,238,255)); d.line([(0,640),(W,640)],fill=(220,215,235),width=6); emo(im,'bed',1000,520,330); emo(im,'dog_face',1020,410,150); man(d,420,640,'lie',1.2); emo(im,'zzz',250,430,120); save(im,'v3_hook2.jpg')
im,d=base((255,248,238)); d.line([(0,640),(W,640)],fill=(220,215,235),width=6); man(d,W//2,640,'back',1.3); save(im,'v3_hook3.jpg')

# ---- model strip: row Now / row Yesterday
def nurse_scene(name,bubble,pose='stomach',bg=(240,250,250)):
    im,d=base(bg); d.line([(0,640),(W,640)],fill=(220,215,235),width=6)
    emo(im,'woman_health_worker',300,470,330); emo(im,'speech_balloon',480,200,200); emo(im,bubble,480,200,100)
    man(d,980,640,pose,1.15); save(im,name)
nurse_scene('v3_m2.jpg','red_question_mark')
im,d=base((255,246,236)); d.line([(0,640),(W,640)],fill=(220,215,235),width=6); man(d,W//2-80,640,'stomach',1.25); emo(im,'check_mark_button',W//2+300,300,220); save(im,'v3_m3.jpg')
im,d=base((255,246,236)); d.line([(0,640),(W,640)],fill=(220,215,235),width=6); man(d,W//2-120,640,'eat',1.25); emo(im,'hot_pepper',W//2+120,230,150); save(im,'v3_m4.jpg')
nurse_scene('v3_m5.jpg','hot_pepper','stand',(240,250,250))
im,d=base((255,246,236)); d.line([(0,640),(W,640)],fill=(220,215,235),width=6); man(d,W//2-80,640,'stand',1.25); emo(im,'check_mark_button',W//2+300,300,220); save(im,'v3_m6.jpg')

# ---- robot nurse
im,d=base((240,250,250)); d.line([(0,640),(W,640)],fill=(220,215,235),width=6); emo(im,'robot',640,400,420); save(im,'v3_robot.jpg')
print('ok',[f for f in os.listdir(OUT) if f.startswith('v3_')])
