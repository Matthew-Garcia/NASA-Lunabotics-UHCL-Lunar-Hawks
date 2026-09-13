# Rover Control & Safety PCB — Rev A schematic

Native KiCad schematic work has started in this folder.

## Current state

- `rover_control_revA.kicad_sch` — top-level hierarchical architecture sheet.
- `01_power_protection.kicad_sch` — nominal-24 V control-input, protection and logic-rail interface sheet.
- `02_mcu_comms.kicad_sch` — proposed ESP32-S3, Jetson serial, USB/debug and CAN interface sheet.
- `03_safety_estop.kicad_sch` — hardware motion-inhibit / emergency-stop interface sheet.
- `04_driver_outputs.kicad_sch` — external wheel, conveyor and actuator-driver control interface sheet.
- `05_sensors_feedback.kicad_sch` — encoder, limit, status, analog-monitoring and optional IMU interface sheet.

These files intentionally begin as **native KiCad architecture/interface sheets**. They establish the hierarchy and electrical interface contract without fabricating component-level detail that depends on unresolved rover hardware.

## Not fabrication-ready

The schematic is **not ERC-complete, routed, fabricated, or tested**. Exact motor/actuator driver models, control input levels/polarities, battery/transient envelope, connector families/ratings, encoder type, E-stop/contactor implementation, and ESP32-S3 module/pin budget must be confirmed before component selection is frozen.

High-current traction, conveyor and actuator load current remains off this PCB on separate fused power distribution. The board is intended for low-current control, sensing, communications and hardware-safe driver enables.

See `../specifications/requirements.md`, `../specifications/interfaces.md`, and `../specifications/review.md` for the release gates.
