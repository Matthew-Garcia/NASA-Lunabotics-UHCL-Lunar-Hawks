# ROS 2 Humble teleoperation

The actual package uses joy + joy_teleop, not teleop_twist_joy. The hardcoded old home-directory path is replaced by package-share lookup. Controller mappings are retained but require physical controller verification.

## Build on Ubuntu 22.04 with ROS 2 Humble installed

From the repository root, with colcon and initialized rosdep available:

~~~bash
source /opt/ros/humble/setup.bash
cd ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
ros2 launch lunabotics_teleop rover_joystick_teleop.launch.py
~~~

These commands target the ROS environment, which was unavailable during migration.

The default command topic is /lunabotics/cmd_vel_preview, not the original motor-facing /cmd_vel. Do not start a motor-facing agent for this check. In a second sourced terminal inspect:

~~~bash
ros2 topic echo /joy
ros2 topic echo /lunabotics/cmd_vel_preview
~~~

Button 5 is the configured deadman; axes 1/3 drive and 6/7 actuator groups. These are indices, not a verified mapping for every controller. The YAML maps angular.y but this firmware does not consume it.

Only after safety review and target tests can a reviewed deployment override command_topic:=/cmd_vel. This does not replace a hardware emergency stop or MCU watchdog. No Nav2, sensors, robot model, or autonomous control are included.
