from bedstand import *
import os
out="."
blue=cq.Color(0.2,0.55,0.9); org=cq.Color(0.9,0.5,0.1); grn=cq.Color(0.3,0.7,0.4); gry=cq.Color(0.75,0.75,0.75); red=cq.Color(0.85,0.25,0.25)

# 1) deployed pose, surface = Z=0, includes bolt proxies
a=cq.Assembly(name="bed_laptop_stand_deployed")
a.add(to_world(half_r),name="tray_half_right",color=blue)
a.add(to_world(half_l),name="tray_half_left",color=blue)
for i,k in enumerate(keys): a.add(to_world(k),name=f"bowtie_key_{i+1}",color=red)
a.add(to_world(leg_dep),name="leg_right",color=org)
a.add(to_world(leg_l_dep),name="leg_left",color=org)
a.add(boot_r,name="foot_boot_right",color=grn)
a.add(boot_l,name="foot_boot_left",color=grn)
a.add(to_world(bolt_r),name="M4x25_bolt_right_proxy",color=gry)
a.add(to_world(bolt_l),name="M4x25_bolt_left_proxy",color=gry)
a.export(f"{out}/bed_stand_deployed.step")

# 2) print layout (no bolts), everything flat
def drop(s,x=0,ymax=0):
    bb=s.val().BoundingBox()
    return s.translate((x-bb.xmin, ymax-bb.ymax, -bb.zmin))
def flat(s): return s.rotate((0,0,0),(0,1,0),90)
l=cq.Assembly(name="bed_laptop_stand_print_layout")
l.add(half_l,name="tray_half_left",color=blue)
l.add(half_r.translate((10,0,0)),name="tray_half_right",color=blue)
l.add(drop(flat(leg_fold),-150,-10),name="leg_right",color=org)
l.add(drop(flat(leg_l_fold),-125,-10),name="leg_left",color=org)
l.add(drop(boot_r,-90,-10),name="foot_boot_right",color=grn)
l.add(drop(boot_l,-25,-10),name="foot_boot_left",color=grn)
for i,k in enumerate(keys): l.add(drop(k,40+i*30,-10),name=f"bowtie_key_{i+1}",color=red)
l.export(f"{out}/bed_stand_print_layout.step")
