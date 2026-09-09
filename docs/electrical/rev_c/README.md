# Rev C system wiring schematic

Open `Lunar_Hawks_RevC.kicad_sch` in KiCad 9. This is a new system-wiring draft, not a routed PCB or a completed component-level replacement for the uploaded schematic.

The four wheel controllers are explicit external **BLDC modules** with U/V/W phases. They no longer use an inappropriate DRV8871 IC symbol as a BLDC controller. Separate fused branches supply conveyor and actuator-driver modules. A hardware NC E-stop breaks the DC contactor coil circuit. A separate compute supply and isolated UART module avoid intentionally joining motor and computer grounds.

All module ports are logical interface names, **not physical connector pin numbers**. Every signal is wired to a named net; the exact module connections are also listed in `module_connections.json`.

Unresolved design inputs: exact BLDC controller model and input voltage thresholds, Jetson carrier and input rating, converter specifications, motor stall currents, fuse/wire/contactor ratings, actual ESP32 pin map, actuator limit switches and synchronization. Coil flyback suppression, transient/reverse-polarity protection and a hardware watchdog require component-level selection and wiring. Check that USB or chassis connections cannot bypass intended isolation.

Validation performed: S-expression parse and explicit module/net generation. KiCad load/render/ERC and electrical performance are unverified. Do not manufacture from this draft.
