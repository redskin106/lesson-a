"""Recolour pillows teal (matches the floor-sleeping picture). Originals kept in art_orig/. Run from the lesson folder."""
import numpy as np, shutil, os
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
TEAL=np.array([97,168,164])/255.0
SEEDS={'v3_hook1':[(230,370),(1110,510)],'v3_hook3':[(181,339)],'v3_adv_2':[(342,301),(575,241)],'l2c_5_effect':[(355,429),(528,394)],'v2_sleep':[(320,280),(580,230)]}
POLY={'v3_hook3':[[(262,292),(345,284),(370,300),(368,322),(335,340),(300,352),(285,335),(262,300)]]}
for n,seeds in SEEDS.items():
    src=f'art_orig/{n}.jpg'
    if not os.path.exists(src): shutil.copy(f'art/{n}.jpg',src)
    a=np.array(Image.open(src).convert('RGB')).astype(float); lab,_=ndi.label(a.mean(2)>200); mask=np.zeros(lab.shape,bool)
    for x,y in seeds: mask|=lab==lab[y,x]
    mask=ndi.binary_fill_holes(ndi.binary_closing(mask,structure=np.ones((5,5))))
    for poly in POLY.get(n,[]):
        pm=Image.new('L',(a.shape[1],a.shape[0]),0); ImageDraw.Draw(pm).polygon(poly,fill=255); mask|=np.array(pm)>0
    Image.fromarray(np.where(mask[...,None],a*TEAL,a).clip(0,255).astype('uint8')).save(f'art/{n}.jpg',quality=88)
    print(n,'ok')
