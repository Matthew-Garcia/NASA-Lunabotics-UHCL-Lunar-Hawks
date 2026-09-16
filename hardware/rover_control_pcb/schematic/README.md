# KiCad 9.0 schematic set

The rover controller electrical design is maintained natively in **KiCad 9.0** as a hierarchical schematic project.

The current project architecture separates the controller into these functional sheets:

- `01_Power.kicad_sch` — protected controller power and regulated rails
- `02_MCU_Comms.kicad_sch` — ESP32-WROOM low-level controller and core communications
- `03_Safety.kicad_sch` — watchdog, arm/re-arm, enable, and inhibit logic
- `04_Drivers.kicad_sch` — external wheel and rover-mechanism driver command interfaces
- `05_Sensors.kicad_sch` — sensor/feedback architecture
- `06_USB_Programming.kicad_sch` — USB-C programming and service interface
- `07_CAN_Bus.kicad_sch` — Classical CAN transceiver, protection, connectors, and termination
- `08_Wheel_Stop.kicad_sch` — wheel stop/brake request interfaces

Top-level KiCad project files are maintained at `hardware/rover_control_pcb/` as `Lunar_Hawks_Rover_Control.kicad_pro`, `Lunar_Hawks_Rover_Control.kicad_sch`, and `Lunar_Hawks_Rover_Control.kicad_pcb`.

High-current wheel, excavation, and linear-actuator load current remains external to this PCB. The board provides low-current control, communication, monitoring, and inhibit functions.

The design remains an engineering snapshot pending final fabrication review and powered hardware validation.
