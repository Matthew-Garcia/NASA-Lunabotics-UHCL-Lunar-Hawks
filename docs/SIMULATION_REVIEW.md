# Full rover simulation revision

This branch contains a **reference-derived reconstruction**, not the original complete mechanical assembly. It is an integration draft. Verification runs on GitHub Actions using ROS 2 Humble / Gazebo 11 and KiCad 9. See `docs/validation/README.md` for measured results and remaining limits.

## Source and dimensions

The supplied ISMCR manuscript specifies four BLDC drive motors, 40 kg reported total mass, 0.87 × 0.75 × 0.75 m reported envelope, and 304.8 mm diameter × 100 mm wide wheels with 12 grousers. The supplied images establish the frame, bucket and conveyor arrangement. They do not define manufacturing geometry. The reconstruction's extended conveyor and wheel track exceed the reported envelope; those positions need reconciliation with the original assembly before claiming dimensional fidelity.

The current reinforced wheel has 12 fins at 30-degree intervals, 22 mm radial projection, 100 mm width and 248 mm outer diameter to fit a nominal 256 mm print bed. It deliberately differs from the manuscript wheel diameter. See `cad/full_rover/WHEEL.md` for thicknesses and print placement. The 44 mm pre-cut value comes from earlier generated CAD, not a measured original wheel. Bore and bolt pattern are provisional. The generated enclosures have vented lids but lack verified board mounting bosses, connector openings and fastening features. Do not print them as fitted replacement enclosures yet.

## Build on Ubuntu 22.04 / ROS 2 Humble

```bash
sudo apt update
sudo apt install ros-humble-gazebo-ros-pkgs ros-humble-gazebo-dev \
  ros-humble-rviz2 ros-humble-joint-state-publisher-gui \
  ros-humble-cv-bridge python3-opencv python3-colcon-common-extensions
source /opt/ros/humble/setup.bash
cd ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-up-to lunabotics_description
source install/setup.bash
ros2 launch lunabotics_description simulation.launch.py
```

Display only, with joint sliders:

```bash
ros2 launch lunabotics_description display.launch.py
```

Opt-in experimental mission, in a simulation-only ROS domain without physical drivers:

```bash
ros2 launch lunabotics_description simulation.launch.py autonomy:=true
```

The mission waits for LiDAR and odometry, rotates to scan, advances with excavation enabled, checks a simulated transferred-rock count, searches for four blue posts, approaches them, turns the rear toward the target, then releases the electronic latch, tips and lowers the bucket, waits for passive door closure and re-latches. Excavator deployment and retraction use a second actuator pair. Faults latch until node restart. This is a local reactive demonstration, **not Nav2 navigation, SLAM, or general terrain planning**. The gray/tan regolith detector remains a development baseline; excavation-zone selection in this demonstration uses the initial scene arrangement, not validated terrain recognition.

## Simulation scope

- Ground and rocks use terrestrial gravity; the arena is a 10 × 6 m custom test space, not an official competition field.
- Four blue posts make the HSV baseline testable. Real post appearance and geometry require calibrated detection.
- Wheel rotation, bucket tipping, passive top-hinged door opening and illustrative actuator extension have URDF joints.
- Scoops advance and reset along a prismatic path. This does not model a full closed-loop chain or chain tension.
- The C++ plugin scripts rock pickup and transfer. Collision geometry permits gravity discharge from the bucket, but discharge success has not been demonstrated.
- Actuator extension is visually proportional to bucket angle; linkage closure, force and synchronization are not solved.
- Gazebo odometry is simulation data. The manuscript deliberately omits physical wheel-encoder odometry because of slip. LiDAR/inertial localization and Nav2 remain future integration work.
- The simulation mission shares conventional topic names with legacy firmware. Use a separate ROS domain; there is no physical actuator bridge in this revision.

## Files and reproducibility

| Location | Contents |
| --- | --- |
| `cad/full_rover/` | Parametric OpenSCAD, ten generated STL parts |
| `ros2_ws/src/lunabotics_description/` | URDF, meshes, Gazebo plugin, arena, RViz and launch files |
| `ros2_ws/src/lunabotics_autonomy/` | Existing perception with sensor QoS, fail-closed LiDAR and opt-in simulation state machine |
| `docs/electrical/rev_c/` | KiCad system wiring and machine-readable module connections |
| `tools/build_description.py` | Regenerate URDF and copy meshes |
| `tools/build_arena.py` | Regenerate arena |
| `tools/build_wiring_schematic.py` | Regenerate KiCad wiring draft |

The original STL files and uploaded Rev-B schematic remain available for comparison.

## Review gates

1. Compile the Gazebo plugin and launch the scene on Humble. Verify clock, robot TF, joint states, scan and image topics.
2. Verify wheel direction, stable contacts, conveyor path, retained material and actual discharge into the designated pad.
3. Test camera loss, scan loss, invalid scans, obstacles and actuator command loss.
4. Replace dimensional estimates with the original STEP/SolidWorks assembly. Reconcile the extended conveyor envelope.
5. Open the KiCad schematic, run ERC, choose actual modules and finish component-level protective circuits.

References for integration: [Gazebo ROS differential-drive plugin](https://docs.ros.org/en/rolling/p/gazebo_plugins/generated/classgazebo__plugins_1_1GazeboRosDiffDrive.html) and [Gazebo ROS control documentation](https://control.ros.org/humble/doc/gazebo_ros2_control/doc/index.html). Gazebo Classic is retained here for the repository's Humble target.

## Confirmed mechanism correction (Rev C.1)

The rectangular bucket floor becomes the discharge ramp. The rear door is top-hinged, passive and held by an electronic latch. Two actuators tilt the bucket; two additional actuators deploy/retract the excavator. A separate motor drives the scoops.

Sequence: scan, deploy, collect, stop conveyor, retract, locate goal, orient rear, unlatch, tip, lower, wait for door closure, re-latch. State changes wait for simulated position/latch feedback, with timeouts and hold on stale feedback. These are simulation estimates, not real limit-switch readings.

New topics: `/excavator/deploy`, `/bucket/latch_release`, `/mechanisms/hold` (Bool). `/simulation/mechanisms` publishes `[excavator_angle_rad, bucket_angle_rad, door_angle_rad, latch_engaged_0_or_1]`. Fault hold freezes the kinematic bucket/lift, stops scoops and retains latch state; an unlatched door remains passive. Actual latch type, fail state, linkage geometry and actuator synchronization remain unspecified.

The OpenSCAD assembly supports `bucket_tip`, `door_open`, and `excavator_deploy` in degrees. Zero deployment is lowered; -14.3 degrees illustrates travel. Actuator rods are illustrative, not closed-loop linkage solutions. The older preview predates this correction; inspect the regenerated URDF and OpenSCAD for current mechanisms.

24 host tests pass, including seven mission interlock tests using message stubs. KiCad 9.0.9 loads and exports the schematic and reports zero ERC errors and warnings. The Gazebo plugin compiles; runtime results are recorded in `docs/validation/README.md`.
