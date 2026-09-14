# Rev A requirements — active development

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| CTRL-01 | Control/interface board only; no traction, excavation-motor, or linear-actuator load current through the logic PCB | Power schematic, PCB review and harness review |
| CTRL-02 | External driver enables default inactive through boot, reset, brownout and floating MCU GPIO states | Scoped output and driver-enable tests |
| CTRL-03 | Hardware E-stop / global `MOTION_ENABLE` inhibits dangerous motion independently of ESP32 firmware | Wired-chain failure tests |
| CTRL-04 | Protected nominal 24 V / 25.6 V LiFePO4 control input with reviewed 5 V and 3.3 V rails | Worst-case voltage, current, transient and thermal calculations plus bench test |
| CTRL-05 | Four external BLDC wheel-driver command channels for FL, FR, RL and RR | Exact driver voltage/polarity/PWM compatibility and HIL test |
| CTRL-06 | Separate external excavation/conveyor motor-driver interface | Driver control compatibility and safe-stop test |
| CTRL-07 | Four external linear-actuator driver interfaces: `ACT_EXC_1/2` and `ACT_DUMP_1/2` | Driver type, travel-limit and synchronization/interlock review |
| CTRL-08 | Dedicated energize-to-release dump-latch driver with safe default latched state | Latch voltage/current, flyback, thermal and failure-state tests |
| CTRL-09 | USB programming/debug for ESP32-WROOM plus dedicated Jetson serial at 115200 baud | Flash/recovery, backfeed, ESD and UART transport tests |
| CTRL-10 | Required Classical CAN / ESP32 TWAI interface with external transceiver, protection and selectable termination | Network topology, termination and CAN error tests |
| CTRL-11 | Encoder, limit-switch, E-stop-status and driver-fault input provisions | Signal-level, conditioning and fault-injection tests |
| CTRL-12 | Voltage/current/diagnostic monitoring only where electrically justified | Analog front-end review and calibrated measurements |
| CTRL-13 | ESP32-WROOM RF antenna region must maintain an all-layer copper/trace/via/component keepout | PCB DRC and RF-keepout inspection |

## Open release gates

Exact external motor/actuator driver models and I/O levels; final battery/transient envelope; total 5 V / 3.3 V load budget; encoder electrical type; limit-switch field wiring; E-stop/contact implementation; final connector mechanics/ratings; dump-latch electrical specifications; enclosure/mounting geometry; final routing/trace widths; CAN_H/CAN_L routing verification; complete post-routing DRC; fabrication review; and bench/HIL validation.

The current 160 × 100 mm board outline and component placement are provisional until rover mechanical integration is finalized.
