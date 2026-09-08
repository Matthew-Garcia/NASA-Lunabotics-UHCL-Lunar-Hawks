# Proposed interfaces — no released connector pinout

| Interface | Planned provision | Must resolve before schematic |
| --- | --- | --- |
| Jetson UART | TX/RX/reference or isolation | Voltage levels, port, pins, isolation and baud |
| Wheels | 4 PWM + 4 direction, enable architecture | Driver input levels, active states, PWM range |
| Conveyor | External driver control | PWM/direction/enable requirements and safe stop |
| Actuators | Up to 4 external-driver interfaces | Two grouped axes versus four independent axes |
| Limit inputs | Protected digital inputs | Normally-closed strategy, wiring faults, count |
| Encoders | Feedback provision | A/B/count, voltage, frequency, conditioning |
| IMU | Optional local I2C/SPI | Device, voltage, bus length, pullups, interrupts |
| LiDAR/camera | Usually Jetson-side, not blindly routed through MCU | Actual USB/UART/Ethernet interface and bandwidth |
| Emergency stop | Independent hardware disable plus status sense | Driver disable/contactors, failure behavior |
| CAN (optional) | Transceiver, protection, selectable termination | Isolation, network topology and pin budget |
| USB-C | Programming/debug | USB role, CC resistors, ESD, power arbitration |

All connector IDs, pin numbers, and component values remain TBD. ESP32-S3 GPIO/peripheral budget must account for flash/PSRAM, USB, boot straps, PWM resources, serial, feedback, and enable channels. If the budget does not fit, reduce/group channels or choose a reviewed distributed architecture rather than invent pins.
