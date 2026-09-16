# Lunar Hawks Rover Control - KiCad 9 physical PCB draft

Open Lunar_Hawks_Rover_Control.kicad_pro. Reload from disk if KiCad was already open; avoid saving a stale editor copy over external edits.

## Physical PCB draft

Open Lunar_Hawks_Rover_Control.kicad_pcb for the placed and routed layout. PCB_Front_Logo.png shows the board. PCB_Both_Logos_DRC.json and PCB_Layout_Status.json list remaining issues; do not infer PCB readiness from the schematic ERC result. See PCB_Layout_Notes.md for layer use and release limitations.

## Implemented

201 components across seven circuit sheets (including 15 DNP signal links):

| Sheet | Contents |
|---|---|
| 01_Power | Fused-branch input; reverse-polarity diode; SMBJ33A surge suppressor; LMR36510 5 V buck; TPS62160 3.3 V buck |
| 02_MCU_Comms | Soldered ESP32-WROOM-32E-N4; reset and BOOT buttons; reset timing; bypass capacitors; GPIO2/GPIO12 strap resistors; UART service header; 5 V, 3.3 V and heartbeat LEDs |
| 03_Safety | Dry-contact permissive input; hardware watchdog; re-arm latch; direct arm gating; command-enable and inhibited LEDs |
| 04_Drivers | PCA9685 command expansion; 19 buffered signals for nine external drivers; prototype headers; wheel/excavator links DNP pending verification |
| 06_USB_Programming | USB-C receptacle; separate CC pulldowns; USBLC6 data protection; CP2102N-A02-GQFN24; VBUS divider; bypass capacitors; USB/service UART selection jumper |
| 08_Wheel_Stop | Four driver-powered default Stop requests; hardware-enable release; four DNP qualification links |
| 07_CAN_Bus | TCAN1042HGVDRQ1 transceiver; NUP2105L protection; two parallel CAN connectors; selectable 120-ohm termination; firmware-driven CAN activity LED |

The sensors sheet remains a placeholder. External E-stop power cutoff, wheel STOP qualification, BRAKE/SC, excavator signal-power wiring and final harness interfaces are not completed. The PCB now has 201 placed schematic components, four mounting holes, reference planes and draft routing on a 160 x 100 mm four-layer outline. See PCB_Layout_Notes.md and PCB_Layout_Status.json for the current PCB check results. No fabrication release has been made.

## Programming operation

USB does not supply the controller's power rails. Power the board's logic supplies before programming. CP2102N is supplied from board 3.3 V, with its regulator bypassed and USB VBUS used only for sensing/protection. Set its USB configuration descriptor to self-powered during bring-up.

JP601: one shunt on pins 1-2 selects onboard USB TX; pins 2-3 select the external service UART. Never bridge both positions. Manual download uses BOOT held low while resetting the ESP32, then release BOOT after entering download mode. Automatic RTS/DTR reset circuitry is not implemented. Service-header pin 2 is 3.3 V reference, not a second power input. External service signals must be 3.3 V and must not back-power an unpowered controller.

## CAN operation and integration

Provisional MCU allocation: GPIO21 -> CAN TX; GPIO22 <- CAN RX; GPIO32 -> CAN activity LED; GPIO23 -> heartbeat. Driver GPIOs are now assigned as detailed in Safety_And_Driver_Design.md; sensor allocation is pending. CAN activity requires firmware to stretch successful TX/RX events into visible LED pulses.

Initial bus target is Classical CAN at 500 kbit/s, subject to cable validation. J701 and J702 share the same CAN bus: pin 1 CAN_H, pin 2 CAN_L, pin 3 signal GND. The draft uses Molex Micro-Fit 3.0 43650-0300 headers; harness housing/terminal selection remains pending. JP701 enables this board's 120-ohm termination only when installed at a physical bus end. Use two terminations across the whole bus, not one on every node.

The Jetson J401 requires its own nearby CAN transceiver or suitable adapter; this stage implements only the controller PCB side. Do not connect the Jetson CAN_TX/CAN_RX logic header directly to CAN_H/CAN_L. The draft CAN node is non-isolated. Ground/reference and isolation choices across the separate batteries and optional UART must be validated as one system. Do not route motor-current returns through communication cables.

## Validation

KiCad 9.0.4 exports the full netlist and renders the new sheets. Twenty-six targeted connectivity checks passed, including USB data pairing, VBUS divider, programmer selection, module reset/boot, CAN mapping, bus connectors and LEDs. USB VBUS, board 5 V, board 3.3 V and GND are distinct nets. Each symbol pin number exists in its selected footprint. The project-local TCAN1042HGV symbol's eight pin assignments were checked against TI's SOIC pin table. USB and CAN previews were visually inspected.

ERC now reports zero errors and zero warnings. Four power flags describe the externally supplied return, protected input, and actual regulator outputs; no ERC exclusions were added. Twelve additional power-connectivity checks passed, bringing the total to 38. Both regulator pin assignments were checked against the manufacturer pin tables, and all 20 new physical parts have matching footprint pad numbers. See Schematic_Both_Logos_ERC.rpt and Connectivity_Checks.txt. These checks do not constitute electrical, thermal, EMC or hardware validation.

## Controller power

J101 pin 1 is battery positive from a dedicated fused logic branch; pin 2 is battery return. This is additional to the five external motor buck branches. The circuit assumes an 8S pack reaching 29.2 V; verify the actual pack/charger label. A 1 A, >=60 VDC branch fuse is a candidate only; wire sizing, interrupt rating, inrush and fault coordination remain to be finalized.

D101 blocks reversed input polarity. D102 provides transient suppression, not sustained overvoltage regulation. The 65 V input regulator derives nominal 5 V, then the second buck derives nominal 3.3 V. See Power_Design.md for part choices, component-rating constraints and the preliminary load budget. The two converters are integrated into this PCB; they do not consume any of the user's five external DROK converters.

The existing rail LEDs now connect to real regulator output nets. Motor-current paths and Jetson battery positive remain external. Reload the project from disk to see the power sheet if it was already open.

## Driver commands and interlock

See Safety_And_Driver_Design.md for the connector map, GPIO allocation, hardware behavior and firmware startup contract. J401-J404 are provisional DRV8871 control interfaces. Eleven wheel/excavator series links are DNP, so J405-J409 are not operational until module behavior is verified. All motor power remains external.

J301 accepts only a voltage-free auxiliary contact from an external safety system; never connect 12/24 V. The PCB interlock is not a safety-rated relay and does not remove motor power. The installed direct-switch topology is documented below; DC load suitability and J301 integration remain unresolved. Green means command gate enabled; red means arm latch inhibited, not proof of a fault or a stopped motor.

The updated design passes zero-error/zero-warning ERC and checks for all 19 independent command paths, nine connector maps, PCA/direct PWM mapping, 23 interlock net groups, 106 new footprint pad mappings and 11 intentional DNP links. Power/communications checks continue to pass. No physical safety performance or dynamic circuit simulation is claimed.

## Next design work

- Sensor/end-limit wiring, paired-actuator synchronization and optional Jetson UART allocation.
- Qualify the installed direct-switch E-stop for aggregate DC load and resolve the separate J301 permissive.
- Verify wheel/excavator input behavior, excavator signal supply, wheel STOP/BRAKE/SC and final locking connectors; complete Jetson-side CAN interface.
- Exact component purchasing choices, cable/fuse/current budgets, and physical-layout completion/review.

The earlier MCU-only generator is obsolete now that these sheets have been connected; do not regenerate from it over this project.

## References

- ESP32 hardware guidelines: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32/schematic-checklist.html
- CP2102N power and USB circuits: https://www.silabs.com/documents/public/data-sheets/cp2102n-datasheet.pdf
- TCAN1042HGV-Q1: https://www.ti.com/lit/ds/symlink/tcan1042h-q1.pdf
- CAN protection: https://www.onsemi.com/pdf/datasheet/nup2105l-d.pdf
- USB protection: https://www.st.com/resource/en/datasheet/usblc6-2.pdf

Hardware_Requirements.md and Driver_Interfaces.md preserve user confirmations and unresolved requirements. This project is a new design, not a conversion of the prior Flux layout.

Power references: https://www.ti.com/lit/ds/symlink/lmr36510.pdf and https://www.ti.com/lit/ds/symlink/tps62160.pdf


## Latest installed E-stop topology

User confirms direct power switching: meter load positive -> latching E-stop -> fusebox positive; meter load negative -> fusebox negative. No separate contactor is installed in the reported circuit. The controller's proposed fusebox branch will lose power too. J301 must never connect to the battery-carrying switch terminals; its low-voltage permissive integration remains unresolved. See the latest section of Safety_And_Driver_Design.md. The switch's suitability for aggregate DC motor current has not been established.


## A4 wheel-direction revision
Four open-drain MOSFETs now switch the ZS-X11H Rotation inputs to ground. All 11 provisional wheel/excavator links remain DNP. ERC and updated connectivity checks pass; see Driver_Interfaces_Preview.png and the latest section of Safety_And_Driver_Design.md. Stop/brake interfaces, J301 integration and switch DC load qualification remain unresolved.

## A5 wheel Stop draft
Four driver-powered Stop request circuits have been added. Their four series links remain DNP pending module qualification; total intentional DNP links is 15. See Wheel_Stop_Design.md and Wheel_Stop_Preview.png. All 201 components export correctly; ERC reports zero errors and warnings. Physical PCB placement and routing have now started; the A6 layout status supersedes this earlier schematic-stage note.

## A6 physical routing draft complete

All 201 schematic components and four mounting holes are placed on the 160 x 100 mm four-layer PCB. Routing and copper fills are saved. PCB DRC: 0 violations, 0 unconnected items, 0 schematic-parity issues. No DRC exclusions were added. All 15 DNP links remain DNP. See PCB_Layout_Notes.md and PCB_Layout_Status.json for the reviews still required before fabrication. The native board is no longer an empty outline.

## Bill of materials
See [BOM.md](BOM.md) for the per-board grouped BOM, DNP quantities, outstanding purchasing selections, and external rover equipment. BOM_Components.json provides all 201 individual component records. This remains a draft BOM pending engineering review.

