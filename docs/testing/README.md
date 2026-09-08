# Verification and evidence register

## Host checks

~~~bash
python3 firmware/micropython/test.py
python3 -m unittest discover -s tests -v
python3 -m compileall -q firmware/micropython ros2_ws/src tests
~~~

These check dry-run command handling and a limited WebSocket implementation on CPython. They do not validate ESP32 execution, GPIO, ROS runtime, or physical safety. See VALIDATION.md for migration-time results.

| Feature | Available evidence | Required next validation |
| --- | --- | --- |
| Mobility/turning | Owner-reported demo; rover photo | Dated video, procedure, hardware/software revision |
| Conveyor/material transport | Owner-reported demo | Dated clip, load, duration, result |
| Bucket disposal | Owner-reported demo | Limits, current/load checks, video |
| ROS 2 / micro-ROS | Existing source and historical PDF | Clean build, serial setup, topic recording |
| Simulation | Archived Gazebo video | Model/world/configuration and reproducible launch |
| New MicroPython | Host tests | Target interpreter test; no physical actuation implemented |
| Proposed PCB | Requirements only | ERC, DRC, review, staged electrical tests |

Physical-test log fields: date; operator; hardware revision; commit SHA; conditions/load; instruments; procedure; expected result; actual result; evidence filename; issues; pass/fail. Leave unknown measurements unknown.
