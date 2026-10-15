import math
import cadquery as cq

# ---------------- parameters (mm) ----------------
W, D, T = 300.0, 200.0, 10.0         # tray size / thickness (13-14" laptop)
LIP_H, LIP_T = 10.0, 8.0             # front lip
ALPHA = 20.0                         # tray tilt (deg)
BETA = 63.0                          # leg angle to the surface (deg)
ARM_T, ARM_W = 8.0, 12.0             # leg thickness (x) / width (in plane)
GAP = 0.4                            # lug-to-leg clearance
HOLE = 4.3                           # hinge hole for M4 bolt
FOOT_Z = 4.0                         # leg is cut flat here; boot floor below it
SLOT_W, PITCH, NCOL = 6.0, 14.0, 18
SEG_A, SEG_B = (45.0, 108.0), (122.0, 185.0)
FOAM_D, FOAM_Y = 1.5, (10.0, 40.0)   # recess for adhesive foam strip (underside)
KEY_YS = [24.0, 115.0, 192.5]        # bow-tie key positions along the seam
BOOT_W, BOOT_L, BOOT_H, CLR = 56.0, 52.0, 24.0, 0.15

HY, HZ = D + 6.0, ARM_W / 2          # hinge axis (y, z) in tray frame
xl0 = W / 2 - ARM_T                  # lug x range [xl0, W/2]
xa0 = W / 2 + GAP                    # leg x range [xa0, xa0+ARM_T]

def ky(poly, dy=0.0):
    return [(x, y + dy) for x, y in poly]

KEY = [(-12, -5), (-12, 5), (0, 2.5), (12, 5), (12, -5), (0, -2.5)]
KEY_POCKET = [(-12.3, -5.3), (-12.3, 5.3), (0, 2.8), (12.3, 5.3), (12.3, -5.3), (0, -2.8)]

# ---------------- tray (right half, x >= 0) ----------------
base = cq.Workplane("XY").box(W, D, T, centered=(True, False, False))
lip = cq.Workplane("XY").box(W, LIP_T, LIP_H, centered=(True, False, False)).translate((0, 0, T))
outline = (cq.Workplane("XY").box(W, D, T + LIP_H, centered=(True, False, False))
           .edges("|Z").edges("<Y").fillet(10))
tray = outline.intersect(base.union(lip))

pts = []
for i in range(NCOL):
    x = (i - (NCOL - 1) / 2) * PITCH
    for (y0, y1) in (SEG_A, SEG_B):
        pts.append((x, (y0 + y1) / 2))
slots = (cq.Workplane("XY").workplane(offset=-1).pushPoints(pts)
         .slot2D(SEG_A[1] - SEG_A[0], SLOT_W, 90).extrude(T + 2))
tray = tray.cut(slots)

# foam-strip recesses on the underside (kept clear of the seam keys)
for sx in (1, -1):
    r = (cq.Workplane("XY").workplane(offset=-1)
         .center(sx * 76, (FOAM_Y[0] + FOAM_Y[1]) / 2)
         .rect(128, FOAM_Y[1] - FOAM_Y[0]).extrude(FOAM_D + 1))
    tray = tray.cut(r)

# bow-tie key pockets across the seam
for y in KEY_YS:
    p = cq.Workplane("XY").workplane(offset=-1).polyline(ky(KEY_POCKET, y)).close().extrude(T + 2)
    tray = tray.cut(p)

def lug(x0):
    w = (cq.Workplane("YZ").workplane(offset=x0)
         .polyline([(D - 2, 0), (HY, 0), (HY, ARM_W), (D - 2, ARM_W)]).close().extrude(ARM_T))
    w = w.union(cq.Workplane("YZ").workplane(offset=x0).center(HY, HZ).circle(ARM_W / 2).extrude(ARM_T))
    hole = (cq.Workplane("YZ").workplane(offset=x0 - 1).center(HY, HZ)
            .circle(HOLE / 2).extrude(ARM_T + 2))
    return w.cut(hole)

full = tray.union(lug(xl0)).union(lug(xl0).mirror("YZ"))
half_r = full.intersect(cq.Workplane("XY").box(W, D + 40, 100, centered=(False, False, False))
                        .translate((0, -10, -10)))
half_l = half_r.mirror("YZ")

# seam keys (print 3)
keys = [cq.Workplane("XY").polyline(ky(KEY, y)).close().extrude(T) for y in KEY_YS]

# ---------------- legs ----------------
phi = math.radians(BETA + ALPHA)
dy, dz = math.cos(phi), -math.sin(phi)
ang = math.degrees(math.atan2(dz, dy))
ZH = HY * math.sin(math.radians(ALPHA)) + HZ * math.cos(math.radians(ALPHA))
L = (ZH - FOOT_Z) / math.sin(math.radians(BETA)) + 12.0

def arm2d(x0, thick, width, hole=True, length=L):
    my, mz = HY + dy * length / 2, HZ + dz * length / 2
    w = (cq.Workplane("YZ").workplane(offset=x0).center(my, mz)
         .slot2D(length + width, width, ang).extrude(thick))
    if hole:
        w = w.cut(cq.Workplane("YZ").workplane(offset=x0 - 1).center(HY, HZ)
                  .circle(HOLE / 2).extrude(thick + 2))
    return w

def to_world(s): return s.rotate((0, 0, 0), (1, 0, 0), ALPHA)
def to_local(s): return s.rotate((0, 0, 0), (1, 0, 0), -ALPHA)

def below(z):
    return cq.Workplane("XY").box(2000, 2000, 500, centered=(True, True, False)).translate((0, 0, z - 500))

leg_dep = to_local(to_world(arm2d(xa0, ARM_T, ARM_W)).cut(below(FOOT_Z)))     # +x leg, deployed
leg_l_dep = leg_dep.mirror("YZ")

fold = 180.0 - ang
def fold_arm(s, a=None):
    return s.rotate((0, HY, HZ), (1, HY, HZ), fold if a is None else a)
leg_fold = fold_arm(leg_dep)
leg_l_fold = leg_fold.mirror("YZ")

# ---------------- boots (slip over the leg foot, world frame) ----------------
xc = xa0 + ARM_T / 2
leg_world = to_world(leg_dep)
slab = leg_world.intersect(cq.Workplane("XY").box(2000, 2000, 0.6, centered=(True, True, False))
                           .translate((0, 0, FOOT_Z)))
bb = slab.val().BoundingBox()
yf = (bb.ymin + bb.ymax) / 2
boot_box = (cq.Workplane("XY").box(BOOT_W, BOOT_L, BOOT_H, centered=(True, True, False))
            .translate((xc, yf, 0)))
cutter = to_world(arm2d(xa0 - CLR, ARM_T + 2 * CLR, ARM_W + 2 * CLR, hole=False, length=L + 40)
                  ).intersect(cq.Workplane("XY").box(2000, 2000, 400, centered=(True, True, False))
                              .translate((0, 0, FOOT_Z)))
boot_r = boot_box.cut(cutter)
boot_l = boot_r.mirror("YZ")

# ---------------- M4 bolt proxies (deployed assembly only) ----------------
def bolt():
    x_end = xa0 + ARM_T + 0.8           # outside face of leg + washer
    x_start = xl0 - 5.8                 # nut side (washer + nylock nut)
    shank = (cq.Workplane("YZ").workplane(offset=x_start).center(HY, HZ)
             .circle(2.0).extrude(x_end - x_start))
    head = cq.Workplane("YZ").workplane(offset=x_end).center(HY, HZ).circle(3.5).extrude(2.8)
    return shank.union(head)
bolt_r = bolt()
bolt_l = bolt_r.mirror("YZ")
