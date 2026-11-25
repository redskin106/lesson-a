from PIL import Image
import numpy as np
from scipy import ndimage as ndi
SH={
 's1_jobs':(5,3,'j_meds j_beds j_lift j_call j_clean j_cook j_lock j_notes j_tea j_pulse j_tv j_phone j_sleep j_games j_dance',24,170),
 's2_words':(3,2,'w_antidote w_outbreak w_sabotage w_quarantine w_contagious w_side_effects',24,170),
 's3_scenes':(3,3,'sc_hospital_rain sc_corridor sc_coat_stand_shape sc_coat_stand_plain sc_lab_door sc_lightning_window sc_lift_stuck sc_glider_escape sc_morning_bed',24,225),
 's4_clues':(3,2,'c_slot c_note c_coat c_bag c_vent c_coat_folded',24,170),
 's5_events':(3,2,'ev_lab_locked ev_lights_out ev_bed4 ev_lift_stuck ev_phone ev_corridor_shape',24,170),
 's6_crews':(5,2,'cr_lab cr_kitchen cr_lift cr_pharmacy cr_corridor st_mia st_joy st_ben st_pat st_dan',24,170),
 's7_teach':(4,4,'t1_timetable t1_lift t1_cooker t1_late t2_bag t2_torch t2_phone t2_tea t3_alarm t3_cable t3_button t3_torch_off t4_lift_stop t4_phone_dead t4_locked t4_hand',24,170),
 's8_rec1':(5,4,'r_parcel r_mop r_ambulance r_pizza r_guard_bed r_phone r_lab_tech r_wrench r_battery r_cup r_alarm r_umbrella r_hand r_stove r_rain r_bus r_clock r_pills r_plug r_tube',24,170),
 's9_rec2':(4,3,'r2_book r2_run r2_plate r2_walk r2_sleep r2_window r2_water r2_van_hand p_calendar_phone p_tea_sugar p_van_hand p_door_alarm',24,170),
}
def cut(name,cols,rows,names,dil,thr):
    if name in ('s3_scenes','s7_teach'): return cutgrid(name,cols,rows,names,thr)
    im=Image.open(f'sheets/L5_{name}.jpg').convert('L');a=np.array(im);H,W=a.shape
    m=ndi.binary_dilation(a<thr,iterations=dil)
    lab,n=ndi.label(m)
    cx=[(c+.5)*W/cols for c in range(cols)];cy=[(r+.5)*H/rows for r in range(rows)]
    boxes={}
    for i,sl in enumerate(ndi.find_objects(lab)):
        ys,xs=sl
        if (lab[sl]==i+1).sum()<400: continue
        x=(xs.start+xs.stop)/2;y=(ys.start+ys.stop)/2
        c=int(np.argmin([abs(x-v) for v in cx]));r=int(np.argmin([abs(y-v) for v in cy]))
        b=boxes.get((r,c),[W,H,0,0]);boxes[(r,c)]=[min(b[0],xs.start),min(b[1],ys.start),max(b[2],xs.stop),max(b[3],ys.stop)]
    res=[]
    for k,nm in enumerate(names.split()):
        r,c=divmod(k,cols);b=boxes.get((r,c))
        if not b: print('MISSING',name,nm);continue
        p=dil+6;x0,y0,x1,y1=b;x0=max(0,x0-p//2);y0=max(0,y0-p//2);x1=min(W,x1+p//2);y1=min(H,y1+p//2)
        g=a[y0:y1,x0:x1].astype(float)
        white=g>225
        lab2,_=ndi.label(white)
        edge=set(np.unique(np.concatenate([lab2[0],lab2[-1],lab2[:,0],lab2[:,-1]])))-{0}
        outside=np.isin(lab2,list(edge))
        alpha=np.where(outside,255-g,255).clip(0,255)
        rgb=np.where(outside,0,g)
        Image.fromarray(np.dstack([rgb,rgb,rgb,alpha]).astype('uint8'),'RGBA').save(f'cuts/L5_{nm}.png')
        res.append((nm,(x1-x0,y1-y0)))
    return res

def cutgrid(name,cols,rows,names,thr):
    im=Image.open(f'sheets/L5_{name}.jpg').convert('L');a=np.array(im);H,W=a.shape;res=[]
    for k,nm in enumerate(names.split()):
        r,c=divmod(k,cols);x0,x1=int(c*W/cols),int((c+1)*W/cols);y0,y1=int(r*H/rows),int((r+1)*H/rows)
        g=a[y0:y1,x0:x1];ys,xs=np.where(g<thr)
        if len(ys)<400: print('MISSING',nm);continue
        p=14;bx0=max(0,xs.min()-p);bx1=min(g.shape[1],xs.max()+p);by0=max(0,ys.min()-p);by1=min(g.shape[0],ys.max()+p)
        Image.fromarray(g[by0:by1,bx0:bx1]).convert('RGB').save(f'cuts/L5_{nm}.png');res.append(nm)
    return res

if __name__=='__main__':
    for nm,(c,r,names,d,t) in SH.items(): print(nm,len(cut(nm,c,r,names,d,t)),'cuts')
