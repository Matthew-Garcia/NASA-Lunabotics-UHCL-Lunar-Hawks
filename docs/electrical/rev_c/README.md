# Rev C system wiring schematic

Open `Lunar_Hawks_RevC.kicad_sch` in KiCad 9. This is a new system-wiring draft, not a routed PCB or a completed component-level replacement for the uploaded schematic.

The four wheel controllers are explicit external **BLDC modules** with U/V/W phases. They no longer use an inappropriate DRV8871 IC symbol as a BLDC controller. Separate fused branches supply conveyor and actuator-driver modules. A hardware NC E-stop breaks the DC contactor coil circuit. A separate compute supply and isolated UART module avoid intentionally joining motor and computer grounds.

All module ports are logical interface names, **not physical connector pin numbers**. Every signal is wired to a named net; the exact module connections are also listed in `module_connections.json`.

Unresolved design inputs: exact BLDC controller model and input voltage thresholds, Jetson carrier and input rating, converter specifications, motor stall currents, fuse/wire/contactor ratings, actual ESP32 pin map, actuator limit switches and synchronization. Coil flyback suppression, transient/reverse-polarity protection and a hardware watchdog require component-level selection and wiring. Check that USB or chassis connections cannot bypass intended isolation.

Validation performed: S-expression parse and explicit module/net generation. KiCad 9.0.9 loaded/rendered this schematic and reported zero ERC errors and warnings in GitHub Actions run 34298704677. Electrical performance remains unverified. Do not manufacture from this draft.

## C.1 mechanism update

Bucket and lift channels represent two actuator pairs (four actuators total); the lift pair deploys the excavator. Conveyor motor control is separate. F23/U23/Y1 add a logical fused latch-solenoid branch and clamped low-side driver. J23/U24/J24 document door, latch and actuator endpoint feedback. U24 represents pending ESP32 GPIO assignments, not a second microcontroller. A solenoid release is an assumption until the actual electronic latch is identified; coil voltage, duty cycle, suppression and driver selection are not finalized. The top-hinged door has no powered door motor.

ERC checks logical module connectivity here. The generic passive module pins do not validate voltage compatibility, protection sizing, isolation hardware or physical connector assignments.
