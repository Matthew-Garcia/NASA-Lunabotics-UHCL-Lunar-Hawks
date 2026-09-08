# Preliminary functional BOM — not for purchasing

| Block | Quantity basis | Selection status |
| --- | --- | --- |
| ESP32-S3 module | 1 proposed | Module/memory variant and GPIO budget TBD |
| Protected control supply input | 1 | Fuse, TVS, reverse-protection and filter calculations pending |
| Regulators | 5 V and 3.3 V rails | Ratings/topology depend on load and input envelope |
| Output buffers and enable logic | Driver-channel dependent | Logic levels, polarity, fail-safe defaults TBD |
| External-driver connectors | 4 wheels, conveyor, actuator interfaces | Pin count, pitch and ratings TBD |
| Input conditioning | Limits/encoders/status dependent | Field voltage and signal rate TBD |
| USB-C/ESD/power arbitration | 1 port proposed | Role and backfeed design TBD |
| CAN transceiver/isolation | Optional | Architecture and power budget TBD |
| LEDs/test points | Rails, comms, inhibit | Values and placement TBD |

No manufacturer part numbers or fabricated stock/price claims. External motor drivers and motor-power distribution are outside the logic-board BOM.
