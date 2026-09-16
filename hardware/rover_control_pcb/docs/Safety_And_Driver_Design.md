# Driver commands and hardware interlock - A4 circuit draft

This stage adds command circuitry for nine external motor drivers and a PCB command interlock. It does not complete the external E-stop power-disconnect system. Motor currents, relay/contactor details and module harness verification remain open. The PCB is still unplaced and unrouted.

## Board-side connector map

These are newly assigned PCB pin numbers, not a transcription of module header order. Headers are provisional 2.54 mm prototype footprints; select locking rover harness connectors before layout release.

| Connector | Load | Pin 1 | Pin 2 | Pin 3 | Pin 4 |
|---|---|---|---|---|---|
| J401 | Dump actuator 1 | GND | IN1 | IN2 | - |
| J402 | Dump actuator 2 | GND | IN1 | IN2 | - |
| J403 | Excavator deployment actuator 1 | GND | IN1 | IN2 | - |
| J404 | Excavator deployment actuator 2 | GND | IN1 | IN2 | - |
| J405 | Excavator motor | GND | ENA/PWM | IN1 | IN2 |
| J406 | Wheel 1 | GND | SPEED/PWM | DIR | - |
| J407 | Wheel 2 | GND | SPEED/PWM | DIR | - |
| J408 | Wheel 3 | GND | SPEED/PWM | DIR | - |
| J409 | Wheel 4 | GND | SPEED/PWM | DIR | - |

All commands pass through SN74AHCT244PWR buffers powered by 5 V. Wheel direction commands then drive Q401-Q404 open-drain MOSFETs; their connector pins no longer receive push-pull voltage outputs. Their TTL-compatible inputs accept the 3.3 V commands. Each command has a 10 kohm input pulldown, 220 ohm output series resistor, and a 10 kohm pulldown after the series resistor. For wheel DIR, that pulldown is on the MOSFET gate, not on the connector drain. Hardware disable makes the buffer outputs high impedance; the pulldowns then establish low provided the external modules do not overpower them. Harness opens require module-side pulldowns too.

The eleven series resistors for J405-J409 are explicitly DNP (do not populate), keeping unverified wheel/excavator commands disconnected in this draft. These modules cannot be operated through these headers until their input behavior is verified and the links are deliberately fitted. Actuator links are populated provisionally based on the DRV8871 IC specifications; verify the purchased module circuitry and terminal order before wiring.

DRV8871 inputs 00 produce coast/sleep, not mechanical holding or an emergency brake. Its recommended logic input range extends to 5.5 V. The excavator module's optocoupler current and +5 V signal-power pin remain unresolved: J405 intentionally does not export a supply. The unused excavator channel must be disabled at the module. Reversal requires a stopped motor and the seller's stated dead time, not merely swapping bits while moving.

The newly supplied ZS-X11H V2 diagram identifies a dedicated PWM throttle input labeled 2.5-5 V, 50 Hz-20 kHz, plus an external-PWM jumper. The screw-terminal 0-5 V Speed input is shown separately with a potentiometer. Rotation and Stop are illustrated as switches to driver GND; Brake is illustrated as a switch to the driver's own 5 V output. See Driver_Interfaces.md for the full evidence update.

Wheel DIR now uses Q401-Q404 open-drain switches to GND; the gate-drive links remain DNP pending module qualification. STOP/BRAKE/SC interfaces are not implemented. Do not connect the driver's onboard 5 V output to the PCB's 5 V rail. PWM duty polarity, open-circuit behavior, control currents and speed-output voltage remain unverified. Wheel speed zero is not claimed as the complete E-stop mechanism.

## PWM and GPIO assignment

PCA9685PW at 7-bit I2C address 0x40 provides 15 assigned outputs. All address pins are grounded; EXTCLK is grounded because the internal oscillator is used. Its OE pin is low; separate physical buffers enforce command inhibition regardless of PCA output configuration. The expander can retain stale commands across an ESP32 reset, so explicit initialization is essential.

| PCA channel | Function |
|---|---|
| 0, 1 | Dump 1 IN1, IN2 |
| 2, 3 | Dump 2 IN1, IN2 |
| 4, 5 | Deployment 1 IN1, IN2 |
| 6, 7 | Deployment 2 IN1, IN2 |
| 8 | Excavator ENA/PWM |
| 9, 10 | Excavator IN1, IN2; static full-off/full-on |
| 11-14 | Wheel 1-4 DIR; static full-off/full-on |
| 15 | Unused, no connection |

Initial actuator/excavator PWM target is about 1 kHz. With a nominal 25 MHz PCA clock, PRE_SCALE=5 gives about 1017 Hz. Actual clock tolerance applies. All PWM channels share this frequency. At that frequency, the excavator seller's 10 us pulse requirement limits usable non-static duty near the ends; provisionally keep both high and low pulses at least 10 us. Full-off and full-on are separate static modes. DRV8871 pulse limits and actuator noise/heating must also be checked. Paired actuators need measured position or other synchronization safeguards; issuing equal PWM is not position synchronization.

| ESP32 GPIO | Function |
|---|---|
| 16, 17 | I2C SDA, SCL; 4.7 kohm pullups to 3.3 V |
| 13, 14, 18, 19 | Wheel 1-4 speed PWM; dedicated PWM throttle; initial 20 kHz trial, pending module verification |
| 4 | Software watchdog toggle |
| 27 | ARM_REQUEST, default pulldown |
| 34 | SAFETY_OK input |
| 35 | MOTION_ENABLED readback |
| 21, 22 | Existing CAN TX, RX |
| 23, 32 | Existing heartbeat LED, CAN LED |
| 1, 3 | Existing USB/service UART |

GPIO25, GPIO26, GPIO33 and input-only GPIO36/39 remain available in the draft; final sensor allocation and optional Jetson UART are pending. Boot straps and flash-reserved pins are not used for new motor commands.

## Hardware interlock behavior

J301 is a two-wire, voltage-free auxiliary-contact input. Pin 1 receives 3.3 V through 1 kohm; pin 2 returns to a 10 kohm pulldown, 10 nF filter and Schmitt buffer. Closed contact produces about 3.0 V at the Schmitt input. Contact current is about 0.3 mA: use a contact rated for low-level signals. This is a short, protected local connection to a safety device, not a general-purpose long field cable or 24 V input. No external voltage is allowed. Field ESD/transient protection remains to be finalized with the harness.

The expected external auxiliary contact closes only when an independent E-stop system permits motion. An open contact or broken wire inhibits commands. A short across the wires is not detected. This single-channel input, common logic and shared enable net are not a safety-rated E-stop controller and do not provide single-fault tolerance.

U302 (SN74LVC1G123DCUR) monitors rising edges from GPIO4 with A held low. R303=200 kohm and C303=1 uF give a nominal timeout around 0.2 seconds; the exact minimum/maximum must be characterized across tolerance, voltage and temperature. The timing capacitor connects between CEXT and RCEXT, not to ground. The timer's clear pin follows ESP_EN.

U303 clears the arm latch unless all three conditions are high: SAFETY_OK, watchdog Q, and ESP_EN. U304 latches an ARM_REQUEST rising edge, with D and preset tied high. Any loss of a permissive clears it asynchronously. Restoring the permissives alone does not set it again. U305 additionally requires ARM_REQUEST to remain high, plus ESP_EN, before enabling the outputs. Dropping ARM_REQUEST therefore inhibits commands immediately without waiting for the watchdog.

Q301 (AO3400A, characterized at 2.5 V gate drive) translates the enable into the common active-low buffer enable. R306 pulls that enable to 5 V by default; R307 holds the MOSFET gate low when undriven.

| Condition | Intended command behavior |
|---|---|
| Power-up | Inhibited; requires valid permissives and new arm edge |
| Safety contact opens | Latch clears; buffers disable |
| Heartbeat stops high or low | Watchdog expires; latch clears; buffers disable |
| ESP_EN reset asserted | Latch clears and final enable drops |
| ARM_REQUEST drops | Final enable drops immediately |
| Contact/heartbeat restored, ARM held high | Latch remains cleared; no automatic re-arm |
| Valid permissives plus new intentional arm edge | Commands may pass through buffers |

Internal ESP32 reset does not necessarily pull ESP_EN low. Default GPIO27 pulldown inhibits as GPIOs return to reset state, and missing heartbeat provides the timeout path. Power ramps, brownouts, GPIO boot behavior, latch recovery timing and transistor/buffer enable behavior still need hardware validation. No worst-case stopping time or safety integrity level is claimed.

D301 green indicates the PCB command gate is enabled. D302 red indicates the arm latch is cleared; it is an INHIBITED indicator, not a comprehensive fault lamp. Because ARM can drop before the watchdog clears the latch, both LEDs can temporarily be off. Neither LED verifies contactor position or that a motor is stationary.

## Firmware contract (not implemented firmware)

1. On every boot, force ARM_REQUEST low, wheel PWM low, and watchdog low. Wait until the previous latch/watchdog state has cleared; do not immediately revive an old watchdog pulse train.
2. Initialize I2C and PCA9685 in the disabled state; set every output full-off, non-inverted, push-pull. Configure frequency while asleep as required, then wake and wait for the oscillator. Disable unused group-call features or handle them deliberately.
3. Read back critical configuration and confirm communication. Confirm external safety permission and fresh operator commands. Do not re-use pre-reset motion requests.
4. Service the watchdog from the successful main control cycle, not an autonomous PWM peripheral or an unconditional timer interrupt. Toggle at intervals giving a rising edge about every 20 ms only while command freshness, required feedback, I2C success and local safety checks are valid.
5. A fresh explicit arm request may then raise GPIO27. Verify MOTION_ENABLED readback before motion. Restoring E-stop or communication alone must not auto-arm.
6. On any fault, lower ARM_REQUEST, stop the heartbeat and clear commands when communication is available. An I2C bus failure must not prevent GPIO27 from dropping.
7. Apply stopped-motor direction sequencing, actuator limits and pair-synchronization logic. Define and validate CAN command timeout, end limits and feedback before load testing.

## External E-stop integration still required

The independent E-stop system must remove or otherwise safely inhibit energy to all nine motor branches without relying on ESP32, CAN or this PCB. Its auxiliary contact feeds J301. Keep controller diagnostics powered from an appropriately protected branch if the final system architecture permits it.

The physical button, relay/contactor or safety relay, coil voltage, DC switching ratings, reset method, feedback contacts, motor stopping behavior and stored-energy handling are not yet specified. The existing fusebox and converters do not perform this function. Do not invent coil-terminal wiring or choose a contactor from the battery's Ah capacity. The excavator vendor's back-drive warning and mechanical load holding need to be addressed in the external design.

E-stop button link received: BAOMAIN B00NTT91Y0; see the latest evidence below. Pending user information: separate relay/contactor model and confirmation of button latching action. The ZS-X11H V2 diagram now identifies terminals and the PWM range; installed revision and harness/control behavior still require verification. Motor stall currents, feedback/end-limit hardware and final locking connectors are also needed before release.

## Validation

175 schematic components, including 11 DNP links. Zero KiCad ERC errors/warnings. Existing 38 power/communications connectivity checks pass. Additional checks cover all 19 command paths, all nine connector maps, 15 PCA channels, four ESP32 PWM channels, I2C/address pins, 23 interlock net groups, independent signal nets, 106 new footprint pad mappings and the custom logic pin tables. No dynamic circuit simulation, physical E-stop performance test, PCB DRC or compliance validation has been completed.

## Primary references

- DRV8871: https://www.ti.com/lit/ds/symlink/drv8871.pdf
- PCA9685: https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf
- Output buffers: https://www.ti.com/lit/ds/symlink/sn74ahct244.pdf
- Schmitt buffer: https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf
- Watchdog monostable: https://www.ti.com/lit/ds/symlink/sn74lvc1g123.pdf
- Re-arm latch: https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf
- AND gates: https://www.ti.com/lit/ds/symlink/sn74lvc1g11.pdf
- Enable MOSFET: https://www.aosmd.com/sites/default/files/res/datasheets/AO3400A.pdf

The user-supplied module listing and photos remain the source of module-specific claims; IC datasheets alone do not verify a seller's breakout wiring.


## E-stop button identified from user link

User supplied Amazon ASIN B00NTT91Y0: BAOMAIN enclosed red mushroom E-stop station, advertised with 1 NO and 1 NC contact and 660 V / 10 A markings. This identifies the button station, not a separate motor-power relay/contactor.

Amazon currently describes press-to-stop / clockwise twist-to-reset. A similar BAOMAIN manufacturer page instead says momentary and specifies AC 660 V / 10 A. Exact equivalence is not established, so confirm that the installed button stays latched when pressed and requires deliberate reset. Do not infer a DC motor interruption rating from the generic voltage/current markings.

Proposed role: the normally closed contact participates in the external de-energize-to-stop control circuit, subject to verified DC control-load rating and final safety architecture. Do not route all rover motor current through this button based on the listing. A 1NO+1NC assembly does not provide two independent NC channels. Do not reuse the same NC terminals simultaneously for a powered coil circuit and PCB J301; J301 accepts a separate voltage-free permissive contact only.

The actual relay/contactor or safety relay, coil supply, load ratings and feedback/reset arrangement remain unknown. No contactor wiring or PCB changes were made based on this link. Needed clarification: whether a separate relay/contactor is already installed and its model, and confirmation of the physical button's latching action.

Sources:
- https://www.amazon.com/dp/B00NTT91Y0
- https://baomain.com/products/momentary-emergency-stop-switch (similar manufacturer product; exact match unconfirmed)


## Confirmed installed E-stop wiring - supersedes relay uncertainty

The user confirms that battery power passes directly through the E-stop switch. The DC meter has four terminals: two connect to the battery; of the remaining two, the positive feed goes through the switch to fusebox positive, and the negative feed goes directly to fusebox negative. Terminal functions here describe the user's wiring; the meter model, printed terminal numbers and internal shunt arrangement are not verified.

Functional topology:
Battery +/- -> DC meter battery-side connections.
DC meter load-side positive -> latching E-stop switch -> fusebox positive.
DC meter load-side negative -> fusebox negative.
Fusebox -> four wheel controllers directly, plus five buck/driver branches for four actuators and the excavator motor.

There is no separate relay/contactor in the reported installation. Pressing the E-stop opens the motor distribution feed; twisting restores that feed. This confirms maintained/latching behavior on the installed button despite inconsistent web descriptions. It does not establish motor stopping time or suitability of the switch for the DC interruption duty.

The switch carries the aggregate current of every load downstream of that fusebox, not just a control signal. Its exact DC make/break rating, motor startup/stall current, converter inrush and wiring protection must be checked before accepting this as the final power-cutoff design. The advertised generic 660 V / 10 A marking is not verification for this DC motor load. Main protection ahead of the switch/meter is not yet established by the described topology; do not infer its absence or presence.

The existing proposed controller logic feed comes from a dedicated branch of this same fusebox. Under this topology, pressing E-stop also removes controller PCB power; restoring it causes a cold start. The separate Jetson V-mount supply is unaffected by this switch as described. Keeping controller diagnostics alive would require an explicitly redesigned, separately protected upstream logic branch; that change has not been made.

PCB J301 remains an unpowered dry-contact permissive input; it must not connect to either battery-carrying switch terminal. No spare NC permissive contact or external auxiliary relay is established by this wiring. The advertised spare NO contact is not automatically a suitable closed-when-permitted contact for J301. J301 therefore remains an unresolved integration point, and the current draft stays inhibited without a valid permissive; do not bypass it silently.

No schematic connectivity or component-population changes were made in this evidence update. Next engineering work is to validate the direct-switch DC load rating and resolve the independent low-voltage permissive interface, then finish the wheel switch-emulation circuitry. Required motor/current and switch contact-block data remain pending.


## A4 wheel-direction switch revision - current implementation

Q401-Q404 (AO3400A, SOT-23) now emulate ground-switching of each ZS-X11H Rotation input. J406-J409 pin 3 connects to its MOSFET drain; pin 1 is the shared signal ground/source. Gate drive comes from the hardware-inhibited buffer through the existing 220 ohm DNP link and has a 10 kohm pulldown. These are non-isolated open-drain switches, not voltage sources or isolated relay contacts. No PCB 5 V pullup was added to Rotation.

Once the links are qualified and populated, command high closes the switch to ground; command low or hardware inhibit releases it. Open/released is a direction state, not a stop command. Determine actual wheel direction with the motor unloaded; change direction only after stopping. Verify the effects of simultaneous PWM inhibition and direction release before load testing. No behavior under loss of a ground wire is guaranteed.

The eleven wheel/excavator links remain DNP. The diagram supports this interface topology but does not establish Rotation voltage, pullup current, open-circuit state or transient levels. Validate these against the 30 V MOSFET rating with appropriate margin before use. Wheel PWM still uses the separate dedicated throttle input. STOP/BRAKE/SC and J301 low-voltage permissive integration remain unfinished.

175 schematic components now, including 11 DNP links. ERC: zero errors/warnings. Existing checks pass, plus four MOSFET gate/source/drain-to-header checks, confirmation of no direct power-rail tie on Rotation outputs, and corresponding footprint-pad checks. No physical validation or PCB routing has been completed.

The earlier build_driver_stage.py generator predates this revision and must not be rerun over the current files without porting the changes. The native KiCad files are the deliverable.
