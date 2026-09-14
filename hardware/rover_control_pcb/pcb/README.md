# PCB layout — Rev A

Flux component placement is provisionally complete on a **160 × 100 mm** working outline.

## Stackup

- Layer 1 — signals and components
- Layer 2 — continuous ground plane
- Layer 3 — power distribution
- Layer 4 — signals and components
- standard through-hole vias

## Placement zoning

- left edge — power input, USB/programming, Jetson UART, CAN and E-stop
- right edge — wheel, excavation/conveyor, dump and actuator interfaces
- bottom edge — encoder, sensor and limit interfaces
- top edge — ESP32-WROOM with enforced RF antenna keepout
- lower-right — dump-latch output stage

All 182 placed components passed the checked placement, edge, bounds and RF-keepout criteria. D3 and U4 footprint copper errors were corrected before routing.

## Current routing state

Bulk routing has **not** been completed. Layer 2 ground and Layer 3 power-zone work was started and needs to be reconciled/verified before routing resumes. One CAN_H pin-width/routability warning remains to be resolved without a waiver. Final power widths also depend on the actual load/current budget.

`flux/rover_control_safety_revA.d356.xz` is a compressed D356 layout/netlist export from the current Flux project.

```bash
xz -d rover_control_safety_revA.d356.xz
```

Do not treat this directory as manufacturing release data. Final airwire/DRC checks, mechanical geometry, routing and hardware validation are still required.
