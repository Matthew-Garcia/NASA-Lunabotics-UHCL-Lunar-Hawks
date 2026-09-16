# NASA Lunabotics — UHCL Lunar Hawks Low-Level Embedded Control & I/O PCB

**Native KiCad 9.0 rover-control hardware design** for the University of Houston–Clear Lake Lunar Hawks Lunabotics rover.

This board is the rover's **low-level embedded control and I/O PCB**. The NVIDIA Jetson Orin NX remains the high-level ROS 2/autonomy computer, while this PCB handles the hardware-facing embedded layer: ESP32 control, CAN communication, programming/service I/O, safety/inhibit logic, and command interfaces to external wheel and mechanism drivers.

> **Engineering draft — not released for fabrication or powered operation.** ERC/DRC results establish design-file consistency, not electrical, thermal, RF, EMC, harness, or safety qualification.

## Designed in KiCad 9.0

The controller is designed and maintained **natively in KiCad 9.0**. The current design snapshot was validated with the KiCad 9 toolchain.

The KiCad project includes the project file, hierarchical schematic sheets, routed PCB layout, local symbol resources, 3D-model support, board artwork, BOM/component records, placement data, layout notes, and electrical validation reports.

## Rover control hierarchy

```text
NVIDIA Jetson Orin NX
High-level ROS 2 / autonomy / perception / planning
                 |
                 | CAN / system interface
                 v
LOW-LEVEL EMBEDDED CONTROL & I/O PCB
ESP32 / safety logic / command generation / hardware I/O
                 |
                 v
External motor drivers / actuators / excavation / disposal
```

The board silkscreen identifies the design as:

- **NASA LUNABOTICS — UHCL LUNAR HAWKS**
- **LOW-LEVEL EMBEDDED CONTROL & I/O PCB**
- **CONTROL SIGNALS ONLY — NO MOTOR POWER**

## Current board

- 160 × 100 mm working outline
- four copper layers
- blue solder mask / white silkscreen configuration
- ESP32-WROOM-32E-N4 embedded controller module
- USB-C programming/service interface
- Classical CAN interface with two parallel connectors and selectable 120 Ω termination
- four external BLDC wheel-driver command interfaces
- external linear-actuator / excavation / deployment / disposal command interfaces
- protected controller power conversion to 5 V and 3.3 V rails
- watchdog, re-arm, command-enable, and inhibit logic
- provisional wheel-stop request interfaces
- system/status indicators and service headers
- four mounting holes and Lunar Hawks board artwork
- **motor-current paths remain external to the PCB**

## Architecture notes

**Embedded controller:** the ESP32 provides the low-level hardware-control layer. Manual BOOT/reset support and the USB programming path are integrated on the board.

**CAN:** the controller-side CAN node includes the transceiver, protection, parallel bus connectors, and selectable termination. The Jetson requires its own appropriate CAN transceiver/adapter; logic-level CAN signals are not connected directly to CAN_H/CAN_L.

**Driver interfaces:** motor power is intentionally external. This PCB supplies command/control interfaces to the external wheel and rover-mechanism driver hardware.

**Safety/inhibit layer:** low-voltage interlock, watchdog, arm/re-arm, and command-inhibit functions are included. This PCB is not a safety-rated high-current disconnect; the rover's high-current emergency power interruption remains external.

## KiCad project organization

- [`schematic/`](schematic/) — KiCad schematic architecture and interface sheets
- [`pcb/`](pcb/) — PCB-layout notes and KiCad layout status
- [`bom/`](bom/) — preliminary BOM/component information
- [`images/`](images/) — board-render documentation
- [`cad/`](cad/) — mechanical/STEP integration notes
- [`source/`](source/) — source-of-record notes for the native KiCad design
- [`specifications/`](specifications/) — requirements, interfaces, and design-review gates

## Remaining engineering review

Before fabrication or rover integration, verify regulator current paths and thermal margin, manufacturing stackup, USB behavior, ESP32 RF/antenna clearance, CAN topology/termination/grounding, exact component ordering codes, connector pinouts and voltage compatibility, wheel/excavator STOP/BRAKE/direction behavior, external E-stop integration, mechanical clearances, sensor/end-limit implementation, paired-actuator synchronization, firmware bring-up, and powered hardware testing.

No manufacturing Gerber/drill release is included in this design snapshot.

## Repository location

Branch: `development/full-rover-simulation`  
Directory: `hardware/rover_control_pcb/`
