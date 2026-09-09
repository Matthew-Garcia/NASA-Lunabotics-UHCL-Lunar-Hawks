# Photo-derived open-spoke wheel

This revision replaces the full-rover wheel with an open web, swept spokes, narrow tread band and twelve angled, shoulder-tapered fins inspired by the supplied red wheel photograph. It is an approximate reconstruction, not the original CAD.

- Overall outside diameter, including fins: 304.8 mm.
- Overall width: 100 mm.
- Fin stations: 12, equally spaced at 30 degrees.
- Radial fin projection: 22 mm, half the earlier generated 44 mm value; the photo provides no measured fin length.
- Provisional interface retained: 18 mm bore; six 6.5 mm holes on a 55 mm bolt circle.
- OpenSCAD dimensions are millimetres; URDF scales the STL by 0.001.

Source: `wheel_open_spoke.scad`, used by `rover.scad`. Export from the repository root:

```bash
openscad -o cad/full_rover/wheel.stl -D 'part="wheel"' cad/full_rover/rover.scad
python3 tools/build_description.py
python3 tools/preview_wheel.py
```

The STL is watertight and connected, with measured bounds of 304.8 × 304.8 × 100 mm. This establishes mesh validity only. Hub fit, spoke and tread strength, fabrication method, and loading remain unverified. Simulation mass and cylindrical collision proxies are unchanged estimates; angled-fin soil interaction is not modeled.

The preserved `cad/autonomy_rover/` wheel is the older concept. The full-rover Gazebo/RViz model uses this replacement. Earlier screenshots in `docs/validation/` predate this wheel revision.

![Actual wheel mesh preview](wheel_preview.png)
