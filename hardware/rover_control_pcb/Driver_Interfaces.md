# Driver interface research

## Confirmed module links

- Excavator: one RANSANX module described by the user as L298: https://www.amazon.com/dp/B0F21MNNY6
- Linear actuators: four DRV8871 modules: https://www.amazon.com/dp/B0G4C4KKTB
- Wheels: four ZS-X11H controllers: https://www.amazon.com/dp/B0D97PN96D

Module assignment is confirmed by the user. Physical connector order, polarity, module revisions and cable wiring are not yet verified.

## DRV8871 actuator control

TI's IC datasheet confirms two inputs, IN1 and IN2, per motor. Reserve eight independent logical control signals:

| Actuator | Logical input 1 | Logical input 2 |
|---|---|---|
| Dump 1 | DUMP_1_IN1 | DUMP_1_IN2 |
| Dump 2 | DUMP_2_IN1 | DUMP_2_IN2 |
| Excavator deployment 1 | DEPLOY_1_IN1 | DEPLOY_1_IN2 |
| Excavator deployment 2 | DEPLOY_2_IN1 | DEPLOY_2_IN2 |

These are signal names, not assigned ESP32 GPIOs or connector pin numbers.

IC truth table: 00 = coast/high impedance, then sleep; 01 and 10 = opposite drive directions; 11 = brake. Extend/retract direction depends on motor lead polarity. Both inputs low is an electrical disable, not a guarantee of mechanical load holding. End limits, feedback, paired-actuator synchronization and E-stop behavior remain to be designed.

TI specifies a 1.5 V minimum logic-high threshold, 6.5-45 V operating supply and 3.6 A peak drive. Nominal 3.3 V control is compatible with the bare IC's threshold; verify the module input circuitry before finalizing the interface. Do not treat peak drive current as continuous module capacity. Confirm each actuator's startup/stall current and the module's current-limit resistor/thermal capability.

Manufacturer source: https://www.ti.com/lit/ds/symlink/drv8871.pdf

## Excavator module

The supplied Amazon page could not be retrieved reliably. No physical pinout or electrical input specification has been verified for this exact RANSANX module. The title L298 alone is insufficient to assume a standard L298N breakout circuit, input thresholds, current rating or jumper arrangement. Retain a dedicated external excavator-driver interface, with signals pending module documentation or clear terminal-label photos.

## Power and next decisions

The four actuators and excavator motor are user-specified 12 V loads. Confirm the external 12 V supply arrangement and motor/actuator current requirements. Do not connect these loads directly to the previously proposed 24/25.6 V bus. Motor power remains off the control PCB.

The KiCad project is still a scaffold. This document defines requirements and logical signals, not validated wiring or a released circuit.

## Excavator module: seller description supplied by user

The following supersedes the earlier lack of module specifications. These are seller claims supplied in the conversation, not independently measured characteristics or evidence that the module contains an ST L298 IC.

- Dual H-bridge; one module is assigned to the single excavator motor. Use one channel provisionally; do not parallel outputs without explicit manufacturer support.
- Motor supply: 6.5-27 V, no reverse-polarity allowance. The excavator motor is specified by the user as 12 V, so plan for an external 12 V motor supply. Do not assume compatibility with the maximum charged voltage of the nominal 24/25.6 V bus.
- Control input range: 3-6.5 V, optocoupler inputs. Nominal 3.3 V is within the stated range, but input current, guaranteed thresholds and signal return wiring are unspecified. Do not finalize direct ESP32 drive or isolated-ground wiring from this description alone.
- ENA accepts PWM: 0-10 kHz; stated minimum pulse width 10 us. At 10 kHz, 10 us equals 10% duty; the text does not clarify whether the minimum applies to both high and low pulses. PWM frequency and usable duty range remain provisional.
- Forward/reverse control exists, but terminal order, number of direction inputs and braking truth table are not established by the pasted description. Reserve logical enable/PWM and direction-control functions; do not assign physical pins yet.
- Reversal: seller requires braking for more than 0.1 s AND stopping the motor before reversing. A 100 ms timer alone does not establish that the motor has stopped.
- Seller warns of back-driven motor voltage with module power off. Include this in E-stop/power-loss review; do not assume removal of driver supply alone resolves all stopping behavior.
- Claimed current: 7 A rated per channel and 50 A peak, with no peak duration or thermal test conditions. Do not use the 50 A claim for sizing.
- Seller also specifies <=40 W for a 12 V motor. This corresponds to about 3.3 A if 40 W means electrical input power; it does not reconcile cleanly with a blanket 7 A continuous claim. Actual motor current and module thermal performance need verification.
- Seller suggests input and motor fusing. Its generic 10 A fuse recommendation is not adopted as a final fuse value; coordinate with motor startup, wiring and driver capability.
- Claimed module dimensions: 55 x 55 x 16 mm; mounting holes 3 mm. This is an external module, not the controller PCB outline.

Outstanding hardware evidence: a terminal-label photo or wiring diagram; motor running/stall current; the external 12 V supply arrangement. Driver-interface circuitry remains unimplemented.

## Excavator module header: supplied product image

Viewed in the orientation of the user's product image (control header at upper left, motor terminals at right), the silkscreen appears to show a 2-column by 5-row header:

| Row, top to bottom | Left column | Right column |
|---|---|---|
| 1 | +5V | +5V |
| 2 | ENA | ENB |
| 3 | IN1 | IN3 |
| 4 | IN2 | IN4 |
| 5 | GND | GND |

This is a visual transcription, not numbered connector pins. Confirm against the physical module before making a cable. The diagram labels +5V as signal power and ENA as PWM. It does not establish whether +5V is exclusively an input, internal rail connections, optocoupler input current, braking truth table, or which output terminal block maps to each channel.

Provisional logical interface for the single excavator motor: +5V signal supply (direction/function to verify), ENA/PWM, IN1, IN2 and signal GND. Leave channel B unused, with its inactive input state to be established from module documentation. Do not parallel channels.

The image shows the separate 6.5-27 V motor supply input at lower left and two motor output terminal blocks at right. Use the user-specified 12 V motor supply, separate from controller logic supply. Do not infer galvanic isolation or join signal and power returns solely from the optocoupler description. The pictured 15 A supply fuse and 10 A motor fuse are vendor illustration values, not approved design selections.

Next evidence needed: external 12 V supply arrangement, excavator running/stall current, and confirmation of the control +5V pin function/input current. The PCB pin assignment and driver circuitry remain provisional.


## A3 driver/interlock stage - latest status
The project now has 171 schematic components across six implemented sheets, including 11 DNP links. Command interfaces for nine drivers and a hardware command interlock are drawn; sensors remain pending. This supersedes earlier scaffold-only statements. See Safety_And_Driver_Design.md for actual connector/GPIO assignments and limitations. Wheel/excavator outputs remain disconnected by DNP links until verified; external E-stop power switching is not designed yet. J301 is a voltage-free auxiliary-contact input, not a contactor coil output or 24 V input. PCB placement/routing remains undone.


## ZS-X11H V2 diagram supplied by user - latest evidence

Source: user-supplied annotated image showing ZS-X11H V2. This identifies the illustrated revision, not proof that all four installed modules have identical circuitry.

- Separate PWM throttle input on the lower control connector is labeled 2.5-5 V PWM, 50 Hz-20 kHz. The screw terminal marked 0-5 V Speed is shown with an external potentiometer. Do not interchange these inputs without verification.
- The diagram identifies an external-PWM enable jumper. Verify the physical jumper location/orientation against the installed board before changing it.
- Rotation is illustrated as a switch to driver GND.
- Stop is illustrated as a switch to driver GND.
- Brake is illustrated as a switch to the driver's own 5 V output, NOT GND.
- The driver 5 V output powers the illustrated external potentiometer. It must not be tied to the controller PCB 5 V output or to another driver's 5 V output.
- The lower control connector also shows a speed-pulse output; its amplitude, output circuit and pulses/revolution remain unknown. Do not connect it directly to ESP32 yet.
- The other lower connector is the motor Hall interface. Motor phase terminals are MA/MB/MC; power input is VCC/GND, labeled 6-60 V in the diagram.

Design consequence: keep the wheel PWM signals on ESP32 GPIO13/14/18/19. A 20 kHz initial trial is within the diagram's labeled range, subject to bench validation and confirmed duty polarity. Use the dedicated PWM throttle input. Treat Rotation and Stop as switch-emulation interfaces; the existing push-pull DIR outputs are provisional and must remain disconnected until replaced/qualified. Brake needs a separate driver-referenced high-side/contact interface if used, not the same ground-switch arrangement as Stop.

The image does not establish input current, internal pull resistors, open-circuit behavior, duty-to-speed direction, braking energy handling or which Rotation switch state gives the intended wheel direction. It therefore does not justify populating the wheel links or declaring a complete fail-safe stop. Existing DNP links are retained; no schematic wiring or component population changed in this evidence update.

Still required for the independent motor-power E-stop: button and relay/contactor model(s), coil supply and DC load ratings. Actual installed board revision and control wiring should be checked during harness definition.


## A4 wheel-direction switch revision - current implementation

Q401-Q404 (AO3400A, SOT-23) now emulate ground-switching of each ZS-X11H Rotation input. J406-J409 pin 3 connects to its MOSFET drain; pin 1 is the shared signal ground/source. Gate drive comes from the hardware-inhibited buffer through the existing 220 ohm DNP link and has a 10 kohm pulldown. These are non-isolated open-drain switches, not voltage sources or isolated relay contacts. No PCB 5 V pullup was added to Rotation.

Once the links are qualified and populated, command high closes the switch to ground; command low or hardware inhibit releases it. Open/released is a direction state, not a stop command. Determine actual wheel direction with the motor unloaded; change direction only after stopping. Verify the effects of simultaneous PWM inhibition and direction release before load testing. No behavior under loss of a ground wire is guaranteed.

The eleven wheel/excavator links remain DNP. The diagram supports this interface topology but does not establish Rotation voltage, pullup current, open-circuit state or transient levels. Validate these against the 30 V MOSFET rating with appropriate margin before use. Wheel PWM still uses the separate dedicated throttle input. STOP/BRAKE/SC and J301 low-voltage permissive integration remain unfinished.

175 schematic components now, including 11 DNP links. ERC: zero errors/warnings. Existing checks pass, plus four MOSFET gate/source/drain-to-header checks, confirmation of no direct power-rail tie on Rotation outputs, and corresponding footprint-pad checks. No physical validation or PCB routing has been completed.

The earlier build_driver_stage.py generator predates this revision and must not be rerun over the current files without porting the changes. The native KiCad files are the deliverable.
