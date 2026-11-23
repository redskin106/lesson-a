from PIL import Image
import numpy as np
from scipy import ndimage as ndi
SH={
 's1_items':(5,3,'flashlight rope matches water tinned_food mirror tent fishing_rod first_aid_kit radio knife phone blanket book piano'),
 's2_props':(5,4,'sun_cream kite teddy_bear life_ring salt coconut net paddle map snake mushroom crab helicopter tide palm_tree hot_sun fire_out dead_radio backpack biscuits'),
 's3_people':(4,2,'p_hurt_ankle p_very_hot p_afraid_night p_tired p_cold p_hungry p_swimming p_waving_ship'),
 's4_events':(5,2,'ev_storm_shelter ev_crate ev_ankle ev_rain_fire ev_plane ev_shark_raft ev_water_gone ev_parrot_rope ev_coconut_tree ev_boat_sunset'),
 's5_vocab':(3,2,'w_stranded w_rescue w_shipwreck w_signal w_shelter w_raft'),
 's6_scenes':(3,2,'sc_storm sc_sinking sc_wreckage sc_island_far sc_sunset_boat sc_bags'),
 's7_extras':(3,3,'x_raft_logs x_sailboat x_big_fire x_no_seawater x_ship_far x_meal x_swimmer_far x_wave_hand x_point'),
}
def cut(name,cols,rows,names,dil):
    im=Image.open(f'sheets/L6_{name}.jpg').convert('L');a=np.array(im);H,W=a.shape
    dark=a<170
    m=ndi.binary_dilation(dark,iterations=dil)
    lab,n=ndi.label(m)
    cx=[(c+.5)*W/cols for c in range(cols)];cy=[(r+.5)*H/rows for r in range(rows)]
    boxes={}
    objs=ndi.find_objects(lab)
    for i,sl in enumerate(objs):
        ys,xs=sl
        area=(lab[sl]==i+1).sum()
        if area<400: continue
        x=(xs.start+xs.stop)/2;y=(ys.start+ys.stop)/2
        c=int(np.argmin([abs(x-v) for v in cx]));r=int(np.argmin([abs(y-v) for v in cy]))
        b=boxes.get((r,c),[W,H,0,0]);boxes[(r,c)]=[min(b[0],xs.start),min(b[1],ys.start),max(b[2],xs.stop),max(b[3],ys.stop)]
    res=[]
    for k,nm in enumerate(names.split()):
        r,c=divmod(k,cols);b=boxes.get((r,c))
        if not b: print('MISSING',name,nm);continue
        p=dil+6;x0,y0,x1,y1=max(0,b[0]-0),max(0,b[1]-0),min(W,b[2]),min(H,b[3])
        x0=max(0,x0-p//2);y0=max(0,y0-p//2);x1=min(W,x1+p//2);y1=min(H,y1+p//2)
        g=a[y0:y1,x0:x1].astype(float)
        # outside background -> transparent, interior white stays opaque
        white=g>225
        lab2,_=ndi.label(white)
        edge=set(np.unique(np.concatenate([lab2[0],lab2[-1],lab2[:,0],lab2[:,-1]])))-{0}
        outside=np.isin(lab2,list(edge))
        alpha=np.where(outside,255-g,255).clip(0,255)
        rgb=np.where(outside,0,g)
        out=np.dstack([rgb,rgb,rgb,alpha]).astype('uint8')
        Image.fromarray(out,'RGBA').save(f'cuts/L6_{nm}.png')
        res.append((nm,(x1-x0,y1-y0)))
    return res
if __name__=='__main__':
    for nm,(c,r,names) in SH.items():
        print(nm,cut(nm,c,r,names,24))
