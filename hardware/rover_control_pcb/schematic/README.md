# Rover Control & Safety PCB — Rev A schematic

The Rev A electrical design is being developed in Flux with supplemental KiCad architecture/interface sheets retained in this folder.

## Current design

The controller is **ESP32-WROOM**, not ESP32-S3. The current architecture includes:

- protected nominal 24 V / 25.6 V control input and 5 V / 3.3 V rails
- ESP32-WROOM low-level control
- dedicated USB-to-UART programming/debug path
- Jetson Orin NX UART at 115200 baud
- required Classical CAN / TWAI interface using an external CAN transceiver
- independent hardware E-stop / `MOTION_ENABLE` gating
- four external BLDC wheel-driver interfaces
- excavation/conveyor motor-driver interface
- four external linear-actuator driver interfaces
- wheel encoder, limit, fault and diagnostic inputs
- dedicated energize-to-release dump-latch driver stage

## Files

- `rover_control_revA.kicad_sch` — earlier top-level architecture sheet
- `01_power_protection.kicad_sch` — power/protection architecture
- `02_mcu_comms.kicad_sch` — MCU/comms architecture
- `03_safety_estop.kicad_sch` — hardware motion-inhibit architecture
- `04_driver_outputs.kicad_sch` — external driver control interfaces
- `05_sensors_feedback.kicad_sch` — encoder/limit/status architecture
- `flux/rover_control_safety_revA.edif.xz` — compressed EDIF export from the current Flux project

To restore the EDIF export locally:

```bash
xz -d rover_control_safety_revA.edif.xz
```

## Safety / scope

High-current traction, excavation and linear-actuator load current remains off this PCB on separate fused power distribution. The board provides low-current control, sensing, communications and hardware-safe driver enables.

The design is **not yet fabrication-tested**. Placement is complete, but bulk routing, final electrical calculations, DRC, fabrication and hardware bring-up remain pending.
