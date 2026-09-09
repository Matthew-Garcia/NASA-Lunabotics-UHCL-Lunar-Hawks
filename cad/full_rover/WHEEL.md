# Reinforced 248 mm wheel for a nominal 256 mm build plate

Photo-derived open-spoke wheel, resized for a one-piece print on the user's 256 × 256 × 256 mm printer. This replaces the earlier 304.8 mm full-rover wheel. It retains twelve swept fins at 30-degree intervals and their 22 mm radial projection.

| Feature | Previous wheel | Revised wheel |
| --- | --- | --- |
| Outside diameter including fins | 304.8 mm | 248 mm |
| Axial width | 100 mm | 100 mm |
| Tread band radial thickness | 3.5 mm | 8 mm |
| Edge ring radial / axial thickness | 8 / 6 mm | 14 / 12 mm |
| Spoke tangential / axial section at endpoints | 7 / 5 mm | 16 / 12 mm |
| Hub diameter / axial length | 76 / 45 mm | 90 / 64 mm |
| Fin root tangential section | 4 mm | 14 mm |
| Fin tip tangential section before envelope clipping | 4 mm | 8 mm |

Spokes flare into the rim and hub. The fin envelope is clipped to 248 mm outside diameter; tapered shoulders and curved clipping mean local dimensions vary. Provisional hub interfaces remain an 18 mm bore and six 6.5 mm through-holes on a 55 mm bolt circle. The thicker hub needs longer mounting hardware; confirm real shaft engagement, fasteners and clearance before use.

## Print placement

1. Import `wheel.stl` into Bambu Studio as millimetres at **100% scale**. Do not rescale it to 256 mm.
2. Keep the axle vertical (STL Z axis), center the wheel at X=128, Y=128 and drop its lowest face onto the plate. Model height is 100 mm.
3. The model footprint is 248 × 248 mm, leaving 4 mm per side on the nominal plate. A 3 mm exterior brim produces a maximum 254 × 254 mm bounding envelope, leaving 1 mm per side.
4. Slice with the actual X1C printer/plate profile. Check machine exclusion areas, calibration/prime paths, skirt, supports and brim. Supports beneath the recessed hub/spokes need inspection, and their bases must stay within the plate. Do not disable machine exclusions merely to force the slice to fit.
5. Preview every layer and check estimated filament/time. This is a substantial print: the CAD solid volume is about 1.63 litres before infill choices and supports. A near-full-bed footprint alone does not establish a successful print.

The printable wheel is one piece; no segmented joint is needed to fit the nominal volume. The model has been geometrically checked but has **not been sliced or physically printed in this revision**. Larger brims/support bases may need revised placement or a smaller parametric diameter.

## Simulation integration

All four Gazebo/RViz wheel meshes are replaced. Collision radius is 0.124 m and both differential-drive diameter entries are 0.248 m. Axle mounts stay in their existing chassis positions, so the chassis sits 28.4 mm lower than with the previous wheel. CAD assembly placement and Gazebo spawn height account for that change. Recheck excavation travel and terrain clearance; a full mission was not rerun for this revision. Wheel mass/inertia remain estimates, and collision cylinders do not model fin/soil contact.

## Reproduce and inspect

```bash
openscad -o cad/full_rover/wheel.stl -D 'part="wheel"' cad/full_rover/rover.scad
python3 tools/build_description.py
python3 tools/preview_wheel.py
```

`wheel_open_spoke.scad` contains the parametric wheel module. `wheel_fit_report.json` records measured STL dimensions and mesh checks. The mesh is watertight, consistently wound and connected. These checks and thicker geometry do not establish a load rating or field-test durability. Material, layer bonding, hub fit, torsion, side loads and impact testing still matter.

The preserved `cad/autonomy_rover/` wheel is the older concept. Previous screenshots and runtime reports in `docs/validation/` predate this change.

![Actual reinforced wheel mesh](wheel_preview.png)
