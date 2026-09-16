# PCB Layout — KiCad 9.0

This directory documents the current **KiCad 9.0** PCB layout for the UHCL Lunar Hawks low-level embedded control and I/O board.

## Board

- 160 × 100 mm working outline
- four copper layers
- blue solder mask / white silkscreen configuration
- ESP32-WROOM-32E-N4 controller module
- USB-C programming/service interface
- Classical CAN interface with controller-side transceiver and selectable termination
- external command interfaces for four wheel drivers
- external command interfaces for excavation, deployment, and disposal mechanisms
- low-voltage watchdog / re-arm / inhibit logic
- control signals only — high-current motor power remains external

## Layout intent

The board is partitioned around the low-level embedded-control role beneath the Jetson Orin NX high-level ROS 2/autonomy computer. Connector placement is organized around rover harnessing, with wheel/mechanism interfaces along the board edges, CAN/service access near the top, and protected control-power circuitry separated from signal/control sections.

The ESP32 antenna region must retain its RF keepout. Ground return continuity, CAN routing, decoupling, connector pinout verification, mounting clearances, and final manufacturing constraints must be checked before fabrication.

## Validation status

This is an engineering design snapshot, not a manufacturing release. Final DRC, fabrication outputs, stackup confirmation, electrical review, hardware bring-up, and rover integration are still required.
