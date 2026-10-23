# Foldable Bed Laptop Stand

A 3D-printed, foldable, vented laptop stand for a 13–14" laptop, designed to work on a lap or on a mattress. It prints in PETG on a 220 mm bed, folds flat, and is fully parametric: every dimension comes from one short Python script.

> **Status:** design verified in CAD (valid solids, no interference in the deployed pose or during the fold sweep). **Not yet test-printed and not load-tested.** Check the first import in Onshape and the first print before relying on it.

## Renders

![Deployed stand, rear three-quarter view](images/deployed_iso.png)

*Deployed: 20° tilt, vented tray, hinged legs standing in the wide foot boots.*

![Side view showing the 20 degree tilt](images/deployed_side.png)

*Side view: front lip at the left, leg and foot boot at the rear.*

| Folded, three-quarter view | Folded, top view |
|---|---|
| ![Folded stand, three-quarter view](images/folded_iso.png) | ![Folded stand, top view](images/folded_top.png) |

![Print layout of all parts](images/print_layout.png)

*Print layout: two tray halves, 2 legs, 2 boots and 3 bow-tie keys, all flat on the bed.*

## Files

| File | What it is |
|---|---|
| `bed_stand_deployed.step` | Stand in use, desk/mattress plane at Z = 0. 11 named solids: 2 tray halves, 3 bow-tie keys, 2 legs, 2 foot boots, 2 M4 bolt stand-ins (for mating and fit checks only; not printed). |
| `bed_stand_print_layout.step` | The 9 printable parts laid flat and spaced out: 2 tray halves, 3 keys, 2 legs, 2 boots. |
| `stl/*.stl` | Printable meshes, one per part, already in print orientation (see Printing). |
| `images/*.png` | Renders used in this README. |
| `source/bedstand.py` | Parametric model (CadQuery). Edit the parameters at the top. |
| `source/export.py` | Builds both STEP files from `bedstand.py` (writes to the current folder). |

All units are millimetres. Import the STEP files in Onshape with Create → Import.

## Design summary

| Feature | Value |
|---|---|
| Tray | 300 × 200 × 10 mm, tilted 20° when deployed |
| Print split | Two halves, each about 150 × 212 × 20 mm, joined by 3 bow-tie keys |
| Front lip | 8 mm thick, 10 mm high, front corners R10 |
| Ventilation | 36 slots (18 columns × 2 bands), 6 mm wide, solid bridge between bands for stiffness |
| Underside | Two 128 × 30 mm recesses, 1.5 mm deep, for self-adhesive foam |
| Legs | 12 mm wide × 8 mm thick, hinged on the rear outer corners, outside the tray width |
| Hinge | M4 bolt through the tray lug and the leg, 4.3 mm holes, 0.4 mm gap. Friction holds the angle, so tighten the nut. |
| Foot boots | 56 × 52 × 24 mm slip-on boots (0.15 mm clearance) that spread load on soft surfaces |
| Folded | About 317 mm wide, about 20 mm thick. Legs lie beside the tray; boots come off |
| Deployed size | About 365 × 261 × 82 mm including boots |

### How it works
- **Lap or mattress:** the foam strip along the front underside and the wide boots keep the stand from sinking or digging in.
- **Two-piece tray:** each half fits a 220 mm bed. Bow-tie keys across the seam lock the halves together.
- **Fold:** the legs swing from the rear hinge to lie flat beside the tray. The hinge lugs rise only 2 mm above the tray surface so they clear the laptop's feet.

## Bill of materials (parts only)

Prices found 2026-10-15 in USD. Re-check at checkout.

| Part | Qty | Unit | Total | Vendor |
|---|---|---|---|---|
| PETG filament, 1.75 mm, 1 kg | 1 | $22.49 | $22.49 | eBay (Paramount 3D) |
| M4 × 25 mm 304 stainless hex bolts + nuts + washers, 20-set pack | 1 | $9.49 | $9.49 | Walmart.com (Unique Bargains) |
| Neoprene foam tape, 1" × 1/8" × 75 ft, self-adhesive | 1 | $18.95 | $18.95 | Pres-On (presbond.com) |

Parts subtotal: **$50.93**. Tax and shipping: estimated about $10, to be confirmed at checkout.

## Printing

- **Material:** PETG. PLA works but may creep if left in a hot car or in sunlight.
- **Settings (suggested):** 0.2 mm layers, 4 walls, 20–25% infill.
- **Orientation:** as in `bed_stand_print_layout.step`. Tray halves flat (lip up), legs on their side, boots flat with the slot opening up, keys flat. No supports expected.
- **Quantities:** 1 left half, 1 right half, 3 keys, 2 legs, 2 boots.
- **Ready-to-slice STL files** (in `stl/`, millimetres):

| File | Qty | Size (mm) |
|---|---|---|
| `tray_half_left.stl` | 1 | 150 × 212 × 20 |
| `tray_half_right.stl` | 1 | 150 × 212 × 20 |
| `leg_left.stl` | 1 | 12 × 90 × 8 (printed on its side) |
| `leg_right.stl` | 1 | 12 × 90 × 8 (printed on its side) |
| `foot_boot_left.stl` | 1 | 56 × 52 × 24 |
| `foot_boot_right.stl` | 1 | 56 × 52 × 24 |
| `bowtie_key.stl` | 3 | 24 × 10 × 10 |

## Assembly

1. Press the three bow-tie keys into the seam pockets to join the two tray halves. A dab of glue is optional.
2. Cut two strips of foam tape about 128 mm long and stick them into the underside recesses at the front.
3. Fit a leg beside each rear lug. Pass an M4 × 25 bolt through the leg and the lug, with a flat washer under the head on the leg side. On the lug's inner side add a flat washer, a lock washer and the nut.
4. Tighten the nut until the leg holds its angle but can still be folded by hand.
5. Press a boot onto the foot of each leg when using the stand. Remove the boots to fold.

## Regenerating or changing the design

```bash
pip install cadquery
python source/export.py
```

Edit the parameters at the top of `source/bedstand.py` first. The main ones:

| Parameter | Default | Meaning |
|---|---|---|
| `W`, `D`, `T` | 300, 200, 10 | Tray width, depth, thickness |
| `ALPHA` | 20 | Tray tilt in degrees |
| `BETA` | 63 | Leg angle to the surface |
| `HOLE` | 4.3 | Hinge hole diameter (M4 bolt) |
| `FOAM_D` | 1.5 | Depth of the underside foam recess |
| `BOOT_W`, `BOOT_L`, `BOOT_H`, `CLR` | 56, 52, 24, 0.15 | Boot size and fit clearance |

The leg length, boot position and bolt stand-ins are recomputed automatically.

## Known limitations

- The hinge holds its angle by friction only; there is no hard stop. Keep the nut tight.
- The kit's plain nuts and lock washers replace the nylon-lock nut originally suggested. They work, but expect to retighten occasionally.
- Boots are a friction fit; they can slide off if the stand is lifted. Removable putty or a thin shim fixes a loose fit.
- A laptop deeper than 200 mm overhangs the rear of the tray, over the hinge lugs; this was designed for with a 2 mm lug height.
- Not designed for a bed-table (straddling the lap) setup, which needs much taller legs.
- Not load-tested. Do not use with anything heavier than a typical 13–14" laptop.

## Version history

- **v1** (`laptop_stand_*.step`): first desk version, 250 × 240 mm tray, 15° tilt. Superseded by this design.
- **v2** (this design): bed version with split tray, foam recess, boots and friction hinge.

## License

Not chosen yet. Add one before sharing the files.
"# servicenow-aws-integration-hub" 
