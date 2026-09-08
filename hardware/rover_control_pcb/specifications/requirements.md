# Rev A requirements — preliminary

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| CTRL-01 | Control/interface only; no traction current through logic board | Power schematic and harness review |
| CTRL-02 | Driver enables default inactive through power-up/reset/brownout | Scoped output and driver-enable tests |
| CTRL-03 | Hardware emergency-stop inhibits dangerous motion independently of MCU | Wired-chain failure tests |
| CTRL-04 | Reviewed nominal-24 V input protection and 5 V/3.3 V rails | Worst-case voltage, current, thermal calculations and test |
| CTRL-05 | Four wheel PWM/direction channels plus conveyor interface | Exact driver voltage/polarity/rate compatibility |
| CTRL-06 | Up to four actuator interfaces with feedback/limit provision | Axis count, driver type, travel limit and interlock review |
| CTRL-07 | USB programming/debug and Jetson serial | USB/ESD/power-backfeed review and transport test |
| CTRL-08 | Optional CAN with correct termination/protection | Network topology, transceiver/MCU support, error tests |
| CTRL-09 | Voltage/current monitoring only where electrically justified | Analog front-end design and calibrated measurements |

Unresolved gates: exact driver models; input voltage range including transients; available control current; actuator independence/grouping; UART ground versus isolation; encoder type; sensor connector standards; MCU module and memory variant; connector ratings; board size/mounting; environmental requirements. No rated fuse value, regulator, TVS, trace width, or pin assignment is selected until those inputs are known.
