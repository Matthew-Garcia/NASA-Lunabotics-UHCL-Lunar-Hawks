# Rev A interfaces — active development

| Interface | Current provision | Finalize / verify |
| --- | --- | --- |
| Jetson UART | Dedicated TX/RX/reference interface at 115200 baud | Exact Jetson connector/pins, logic levels, grounding and cable details |
| USB programming/debug | USB-to-UART path to ESP32-WROOM UART0 with boot/reset support | USB power-backfeed behavior, ESD and recovery flashing |
| CAN | Required Classical CAN / ESP32 TWAI through external transceiver; CAN_H/CAN_L, reference, protection and selectable 120 Ω termination | Network topology, connector pinout, termination policy and final routing |
| Wheels | 4 external BLDC driver interfaces: FL / FR / RL / RR | Exact driver control protocol/levels; intended low-current PWM/DIR/ENABLE/FAULT style interface |
| Excavation motor | External motor-driver control interface | Exact external driver input requirements and safe-stop behavior |
| Excavator lift | `ACT_EXC_1`, `ACT_EXC_2` external actuator-driver interfaces | Driver type, direction/enable signals, current/position feedback and synchronization policy |
| Dump lift | `ACT_DUMP_1`, `ACT_DUMP_2` external actuator-driver interfaces | Driver type, direction/enable signals, current/position feedback and synchronization policy |
| Dump latch | Dedicated onboard logic/MOSFET output stage; energize-to-release | Actual latch voltage/current, connector rating, flyback and thermal margin |
| Limit inputs | Protected/conditioned digital input provision | Normally-closed/open field strategy, voltage and connector pinout |
| Wheel encoders | Quadrature/feedback input provision | Encoder voltage, A/B/index count, frequency and conditioning |
| Driver faults/status | Input provisions from external power-driver boards | Signal polarity and voltage levels |
| E-stop | Independent hardware motion-disable chain plus ESP32 status sense | Contact/contactor implementation and failure behavior |
| Diagnostics | Test points, voltage/current monitoring and LEDs where justified | Measurement scaling/calibration and accessible placement |
| LiDAR / cameras | Jetson-side perception devices, not routed through this low-level PCB | Final rover harness and Jetson interfaces |

## Motor-power boundary

The wheel BLDC phase wires and high-current motor/actuator supply paths **do not connect to the ESP32 control PCB**. Each external power driver receives fused battery power and connects to the PCB only through its low-current command/status connector.

## ESP32-WROOM allocation

ESP32-WROOM is the selected Rev A controller. Programming/debug, Jetson UART, CAN/TWAI, safety enables, external-driver commands and feedback must remain compatible with ESP32 boot-strap behavior and available GPIO/peripherals. Final pin assignments must be checked against the actual WROOM module variant before fabrication.
