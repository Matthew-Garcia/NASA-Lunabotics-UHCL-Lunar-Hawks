<p align="center"><img src="media/UHCL_Lunabotics_Logo.jfif" width="180" alt="UHCL Lunar Hawks team logo"></p>

# NASA Lunabotics · UHCL Lunar Hawks

### Proof-of-concept excavation rover
Embedded control · ROS 2 · micro-ROS · Hardware integration

A University of Houston–Clear Lake student and research rover project for regolith collection and transportation. This repository brings together the existing ESP32 firmware, Jetson teleoperation package, mechanical meshes, and software documentation, alongside clearly labeled new development work.

**Status: prototype / research.** Autonomous excavation missions are future work. This is a team-member-maintained project repository, not a NASA-owned or NASA-endorsed software release.

[ROS 2](ros2_ws/README.md) · [micro-ROS](firmware/micro_ros/README.md) · [MicroPython](firmware/micropython/README.md) · [Control PCB](hardware/rover_control_pcb/README.md) · [Research](docs/publication/README.md) · [Testing](docs/testing/README.md)

<p align="center"><img src="media/UHCL_Lunabotics_Rover.jfif" width="760" alt="Lunar Hawks physical rover prototype"></p>

## Demonstration and evidence

[Watch the archived Gazebo simulation clip](media/Gazebo_Sim.mp4) · [Original software documentation](docs/legacy/UHCL_NASA_Lunabotics_Rover_Software_Documentation.pdf)

The team reports demonstrations of mobility, turning, wireless teleoperation, conveyor operation, material transport, and disposal-bucket actuation. Those historical demonstrations do **not** certify this reorganized checkout or the newly added examples. Physical videos and dated test logs should be added to the [evidence register](docs/testing/README.md).

| Area | Included here | Verification status |
| --- | --- | --- |
| ESP32 micro-ROS | Original C application and colcon metadata | Preserved source; no firmware build or hardware retest |
| Jetson ROS 2 | Teleop package, controller YAML, portable launch | Setup updated; ROS runtime validation pending |
| MicroPython | boot.py, test.py, main.py | New dry-run protocol examples; no GPIO motor driver |
| Mechanical | Five original STL files | Meshes preserved; dimensions and printing suitability not revalidated |
| Rover control PCB | Requirements, interfaces, preliminary BOM, review checklist | Concept only; no routed board or manufacturing outputs |
| Research | Owner-supplied paper details and manuscript slot | Acceptance reported by owner; manuscript and DOI not supplied |
| Autonomous mission | Roadmap only | Not implemented or demonstrated by this repository |

## Control architecture

~~~mermaid
flowchart TD
    Controller["Xbox controller"] --> Joy["Jetson: joy_node"]
    Joy --> Teleop["joy_teleop: controller mapping"]
    Teleop -->|"/cmd_vel: Twist"| Agent["micro-ROS agent"]
    Agent -->|"Serial transport"| MCU["ESP32-WROOM: original C firmware"]
    MCU --> Wheels["External wheel drivers: PWM + direction"]
    MCU --> Actuators["External actuator drivers: two control groups"]
    Wheels --> Drive["Four drive motors"]
    Actuators --> Mechanisms["Bucket and excavator lift mechanisms"]
~~~

The proposed ESP32-S3 PCB is a future revision, **not pin-compatible or firmware-compatible by assumption** with the original WROOM implementation. MicroPython and micro-ROS are alternative MCU firmware environments.

## Start with software-only checks

~~~bash
git clone https://github.com/Matthew-Garcia/NASA-Lunabotics-Lunar-Hawks.git
cd NASA-Lunabotics-Lunar-Hawks
python3 firmware/micropython/test.py
python3 -m unittest discover -s tests -v
~~~

For workspace build and topic-only launch, see [ROS 2 setup](ros2_ws/README.md). For original firmware integration requirements, see [micro-ROS notes](firmware/micro_ros/README.md). Do not energize motors using these instructions: read the [safety checklist](docs/electrical/SAFETY.md).

## Repository map

| Path | Purpose |
| --- | --- |
| firmware/micro_ros/ | Preserved ESP32 C firmware and integration limitations |
| firmware/micropython/ | Three-file dry-run WebSocket prototype |
| ros2_ws/src/lunabotics_teleop/ | ROS 2 controller package |
| hardware/rover_control_pcb/ | Proposed control/interface board package |
| cad/ | Original STL models and provenance notes |
| docs/architecture/ | Interfaces, command semantics, power boundaries |
| docs/testing/ | Evidence register and hardware acceptance plan |
| docs/publication/ | Research status and authorized-manuscript location |
| docs/legacy/ | Original software PDF |
| simulation/ | Existing demo link and missing simulation-source checklist |
| media/ | Original rover/team images and Gazebo clip |
| tests/ | Host-side command and WebSocket tests |

## Roadmap

- [ ] Pin deployed JetPack, ESP-IDF, micro-ROS, controller, and transport versions.
- [ ] Add an MCU command timeout, fail-safe error handling, and finite-value validation.
- [ ] Separate actuator commands from the conventional drive Twist interface.
- [ ] Validate joystick release/disconnect behavior with motors disconnected.
- [ ] Upload physical demonstrations and measured results with revision IDs.
- [ ] Complete and independently review the proposed PCB schematic and layout.
- [ ] Supply URDF, Gazebo world, sensors, and reproducible simulation launch.
- [ ] Validate localization/navigation before autonomous excavation.

## People and research

**Matthew Garcia** — repository maintainer; systems integration and embedded/robotics contributor. **Dr. Luong Nguyen** — research adviser and co-author. Credit also belongs to the UHCL Lunar Hawks team; [contribution records](CONTRIBUTING.md) should identify component authors and adapted third-party work.

Research title supplied by the owner: *Design and Implementation of a Proof-of-Concept Excavating Rover Platform for Lunar Regolith Collection and Transportation*. See [publication status](docs/publication/README.md) for acceptance versus presentation and publication.

[Portfolio](https://matthew-garcia-portfolio.vercel.app/) · [LinkedIn](https://www.linkedin.com/in/matthew-garcia-165634195/) · [Original repository](https://github.com/Matthew-Garcia/uhcl-lunar-hawks-lunabotics)

## License and provenance

The original MIT license is retained. See [NOTICE](NOTICE.md) for source revision and rights caveats. New example code is AI-assisted and requires review and target validation before any hardware use.
