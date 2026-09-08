# System and interface notes

The source implements ROS 2 joystick commands and an ESP32-WROOM micro-ROS subscriber. It is not a Nav2 or autonomous excavation implementation.

| Signal | Behavior in preserved app.c |
| --- | --- |
| Twist.linear.x | Forward/reverse drive input |
| Twist.angular.z | Turning input |
| Twist.linear.y | Bucket actuator group; thresholds ±0.5 |
| Twist.linear.z | Excavator actuator group; thresholds ±0.5 |
| Twist.angular.y | Mapped in controller YAML but NOT consumed by this C file |

Linear.y/z actuator use is a legacy custom convention, not standard spatial-velocity semantics. Do not connect navigation directly without an adapter and separate actuator interfaces.

Source constants: track-width parameter 0.465 m, linear/angular clamps ±1.0, velocity-to-duty gain 200, PWM 20 kHz with 8-bit duty. These are software settings, not measured maximum speed or independently confirmed dimensions. No encoder feedback is implemented in this file.

| Channel | PWM GPIO | Direction GPIO |
| --- | --- | --- |
| Front right | 32 | 33 |
| Back right | 12 | 13 |
| Front left | 25 | 26 |
| Back left | 27 | 14 |

Bucket group uses GPIO23/22; excavator group uses GPIO19/18. GPIO12 is a boot-strapping concern. These pins are WROOM-era code, not a pinout for the proposed S3 PCB. The source defines two actuator control groups, not four independent axes.

The owner reports 115200-baud Jetson/ESP32 serial operation; transport initialization and UART pins are not supplied by app.c. Confirm both in the original platform project. Sensor integration is reported for the platform, but no sensor drivers, calibration, SLAM configuration, URDF, or navigation nodes are included.

## Power boundaries

The owner describes a fused nominal-24 V motor domain and a separate V-mount-powered Jetson domain. Separate batteries alone do not establish galvanic isolation. Verify signal references, voltage levels, protection, and any intended isolation barriers before connecting UART. The proposed PCB is a signal/interface board, not a high-current motor-power board.
