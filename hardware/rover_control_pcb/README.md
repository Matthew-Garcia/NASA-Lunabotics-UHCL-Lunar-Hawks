# Lunar Hawks Rover Control & Interface PCB — Rev A concept

**Design requirements only. Not a completed, routed, fabricated, or tested board.** No Gerbers or production BOM are supplied.

Scope: a low-current control/interface PCB between the Jetson and external motor/actuator drivers. High-current load wiring remains on separate fused distribution. ESP32-S3 is a proposed controller, not a confirmed pin-compatible replacement for the original ESP32-WROOM.

[Requirements](specifications/requirements.md) · [Interfaces](specifications/interfaces.md) · [Preliminary BOM](bom/README.md) · [Design review](specifications/review.md)

~~~mermaid
flowchart TD
    Supply["Nominal 24 V control supply"] --> Protect["Fuse, reverse protection, transient/filter stage"]
    Protect --> Rails["5 V / 3.3 V regulators"]
    Rails --> MCU["Proposed ESP32-S3"]
    Jetson["Jetson UART interface"] <--> MCU
    MCU --> Buffer["Reviewed buffers and default-off enables"]
    Buffer --> Drivers["External wheel, conveyor and actuator drivers"]
    Estop["Independent wired emergency stop"] --> Disable["Hardware driver-disable chain"]
    Disable --> Drivers
    Sensors["Feedback and limit inputs"] --> MCU
~~~

Galvanic isolation is undecided: any UART/CAN isolation requires an explicit isolation barrier and appropriate power design. Do not assume two batteries isolate logic signals.

Directory slots under schematic/, pcb/, and gerbers/ explicitly record missing deliverables, not empty KiCad projects pretending to be designs.
