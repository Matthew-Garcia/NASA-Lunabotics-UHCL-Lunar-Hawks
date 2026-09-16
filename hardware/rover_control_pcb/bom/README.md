# KiCad 9.0 BOM

The current bill of materials for the Lunar Hawks low-level embedded control & I/O PCB is maintained from the native KiCad 9.0 design.

Use the current project-level files:

- [`../BOM.md`](../BOM.md) — grouped engineering BOM
- `../BOM_Components.json` — machine-readable component records
- `../PCB_Placement.csv` — draft component position inventory

Current design snapshot: **201 schematic components, 186 populated, 15 DNP**. External BLDC wheel drivers, actuator power drivers, excavation-driver hardware, batteries, fused high-current distribution, and other rover equipment are outside the PCB assembly BOM.

This remains an engineering draft. Exact ordering codes, package selections, ratings, connector mating hardware, assembly consumables, and DNP decisions must be reviewed before procurement or fabrication.
