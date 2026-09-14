# Rev A BOM — preliminary / not for purchasing

The current Flux design contains the selected/provisional parts for the 182-component Rev A schematic and placement. This BOM is still a **development BOM**, not a released procurement list.

Current major devices include:

| Function | Current device / family | Status |
| --- | --- | --- |
| Low-level controller | ESP32-WROOM-32 | Current Rev A controller |
| Reverse-polarity / ideal-diode control | LM74700-Q1 | Provisional; verify final transient envelope |
| 5 V buck | LM5164-Q1 | Provisional values; finalize from load/current budget |
| 3.3 V LDO | TLV76733 | Current design; final thermal/load review pending |
| USB-UART | FT231XS-R | Programming/debug provision |
| CAN transceiver | TCAN1042-Q1 family | Required CAN/TWAI interface |
| Watchdog | TPS3431-Q1 | Hardware safety/watchdog provision |
| Voltage supervisor | TPS3808 | Reset/supervision provision |
| I/O expansion | TCA9539-Q1 family | Driver/input expansion |
| ADC | ADS1115 | Diagnostic/monitoring provision |
| Dump latch | logic buffer + MOSFET + flyback diode | Final latch voltage/current still required |

External BLDC wheel drivers, excavation motor driver, linear-actuator power drivers and high-current fused power distribution are **outside this PCB BOM**.

Manufacturer part numbers and component values remain subject to final electrical validation, routing, availability and fabrication review. Do not purchase the full board from this preliminary list without reviewing the current Flux source and final DRC/release package.
