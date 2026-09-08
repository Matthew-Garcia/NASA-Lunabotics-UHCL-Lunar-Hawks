# ESP32 micro-ROS — preserved rover source

esp32_twist_subscriber/app.c and app-colcon.meta are unchanged. Entry point: appMain(void *arg), not standalone ESP-IDF app_main. They require the original platform wrapper, transport setup, and build environment.

The original target is ESP32-WROOM-32. An ESP32-S3 port requires GPIO and LEDC-mode review. Do not flash this code onto a different board by assumption.

## Build context — not a verified clean-build recipe

The legacy project used ROS 2 Humble and micro_ros_setup with a FreeRTOS ESP32 target. Full pinned toolchain, ESP-IDF revision, wrapper, transport initialization, UART mapping, and board configuration were not supplied. Recover them before flashing. Historical PDF instructions have not all been verified.

See [micro_ros_setup Humble](https://github.com/micro-ROS/micro_ros_setup/tree/humble) for framework context. Restore the matching environment, integrate the application in its application directory, and configure serial transport. app-colcon.meta alone does not define baud rate or UART pins. The owner reports 115200 baud; verify both endpoints.

The firmware can retain nonzero outputs after communications loss. Read [safety limitations](../../docs/electrical/SAFETY.md). MicroPython is an alternative firmware image, not a script running alongside this micro-ROS application.
