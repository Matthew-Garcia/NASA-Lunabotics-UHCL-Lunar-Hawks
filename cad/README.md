# Mechanical CAD and meshes

The CAD tree separates preserved project files from generated development geometry:

- The five STL files directly in `cad/` are the original supplied actuator, sprocket, bucket, door-frame and hatch meshes. Their filenames remain unchanged for traceability.
- [`full_rover/`](full_rover/) contains the reference-derived complete rover reconstruction: chassis, excavator, bucket, actuators, electronics enclosures and wheel variants.
- [`autonomy_rover/`](autonomy_rover/) contains the earlier simplified autonomy-development chassis, goal-post and 12-grouser wheel models.

See [`full_rover/WHEEL.md`](full_rover/WHEEL.md) for the 248 mm Bambu-compatible wheel and 300 mm laboratory wheel variants.

Native STEP/SolidWorks sources for the complete rover were not supplied. Before printing or manufacturing, confirm units, scale, hub and fastener interfaces, tolerances, materials, load suitability, authorship and third-party licensing. Generated geometry is reference/development CAD, not a fabrication-authoritative release.
