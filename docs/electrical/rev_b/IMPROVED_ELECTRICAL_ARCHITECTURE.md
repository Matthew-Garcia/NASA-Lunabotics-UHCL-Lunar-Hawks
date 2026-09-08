# Improved Rover Electrical Architecture — Rev B recommendations

The uploaded KiCad schematic and presentation show a split architecture with a 24 V high-current domain and a separate V-mount/Jetson computing domain. Preserve that separation.

## Recommended Rev B topology

1. **24 V traction / excavation bus**
   - Battery → main fuse → latching E-stop / contactor → fused distribution block.
   - Separate branch fuses for FL, FR, RL, RR drive controllers, conveyor motor driver, and linear-actuator drivers.
   - Add TVS suppression across the 24 V bus near the distribution point.
   - Add bulk electrolytic + ceramic decoupling at every motor-controller branch.

2. **Jetson compute domain**
   - Keep the V-mount battery separate from the traction battery.
   - Add a dedicated input fuse, reverse-polarity protection, and transient clamp ahead of the Jetson regulator/input.
   - Bond grounds only where required by signal interfaces; avoid motor return current through logic ground wiring.

3. **ESP32 / low-voltage logic**
   - Use a regulated 5 V / 3.3 V logic rail with local 100 nF decoupling at each IC/module plus 10–47 µF local bulk capacitance.
   - UART between Jetson and ESP32: add series resistors (33–100 Ω) on TX/RX and a clearly defined common reference. If cable length/noise becomes significant, move to differential RS-485/CAN rather than raw TTL UART.

4. **Emergency stop**
   - E-stop should remove actuator energy at the contactor/enable layer, not rely solely on software PWM = 0.
   - Keep compute alive if desired for logging, while motor/actuator power is hard-disabled.

5. **Motor-driver reality check**
   - The uploaded schematic contains mixed labels such as DRV8871 symbols whose displayed values reference L298N or ZS-X11H modules. Normalize the schematic so the symbol, footprint, driver part/module name, current rating, and motor type all agree.
   - The paper describes four brushless DC wheel motors; verify that the selected driver symbols actually represent the physical BLDC controllers used on the rover. DRV8871/L298N are brushed DC H-bridge devices and should not be shown as BLDC wheel drivers unless they truly are controlling brushed motors.

6. **Sensors**
   - Add explicit fused/regulator branches for RPLIDAR and camera/USB peripherals if externally powered.
   - Route LiDAR/camera cabling away from high-current motor wiring where practical.

7. **Instrumentation**
   - Add labeled test points for 24V_BUS, MOTOR_RETURN, 5V_LOGIC, 3V3, ESP32_TX, ESP32_RX, E_STOP_SENSE and each actuator command.
   - Add current measurement shunt/Hall sensor on the main 24 V bus if you want energy-per-task metrics for the next research phase.
