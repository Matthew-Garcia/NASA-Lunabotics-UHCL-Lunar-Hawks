# Rev A design-review and release checklist

## Completed / checked in current design state

- [x] Select ESP32-WROOM as the Rev A low-level controller.
- [x] Establish Jetson UART at 115200 baud and required Classical CAN/TWAI architecture.
- [x] Establish the 160 × 100 mm provisional four-layer stack and functional connector zoning.
- [x] Enforce the ESP32 antenna keepout at the board edge.
- [x] Complete provisional placement of all 182 components.
- [x] Clear checked placement, edge, bounds and RF-keepout violations.
- [x] Correct D3 TPD2E2U06 and U4 TLV76733 footprint copper issues.
- [x] Keep high-current motor/actuator load paths outside the control PCB architecture.

## Open before routing completion / fabrication

- [ ] Reconcile and independently verify Layer 2 ground and Layer 3 power-zone work already started.
- [ ] Resolve the CAN_H pin-width/routability warning without a waiver.
- [ ] Confirm exact external BLDC, excavation-motor and actuator-driver electrical interfaces.
- [ ] Confirm encoder, limit-switch, E-stop and dump-latch electrical specifications.
- [ ] Finalize input transient envelope and 5 V / 3.3 V current/thermal budgets.
- [ ] Verify USB power-backfeed prevention and Jetson/USB UART isolation from each other.
- [ ] Independently review hardware E-stop, watchdog, `MOTION_ENABLE` and restart prevention.
- [ ] Route power and safety first, then CAN, UART, ESP32 support, feedback and remaining low-speed I/O.
- [ ] Verify controlled return paths, decoupling placement, CAN routing and ESP32 RF exclusion after routing.
- [ ] Run full post-routing DRC and document every intentional waiver.
- [ ] Finalize mounting holes, enclosure geometry, connector access and harness strain relief.
- [ ] Review U4 exposed-pad paste aperture and final CAM outputs.
- [ ] Bring up rails first on a current-limited supply with all external power drivers disconnected.
- [ ] Validate boot/reset/brownout, E-stop, watchdog, communication loss, sensor faults and disable chain.
- [ ] Release final BOM, Gerbers, drill files and assembly drawings only after review and validation.

A completed placement or clean placement check does **not** mean the PCB is fabrication-ready or hardware-validated.
