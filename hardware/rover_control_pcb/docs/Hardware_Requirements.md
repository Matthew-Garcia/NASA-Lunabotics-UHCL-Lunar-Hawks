# Confirmed rover hardware

This mapping reflects the user's latest correction and supersedes earlier driver assignments.

| Function | Quantity | Motor/load | External driver |
|---|---:|---|---|
| Wheel propulsion | 4 | BLDC wheel motors | 4 x ZS-X11H, one per motor |
| Dump bucket | 2 | 12 VDC linear actuators | 2 x DRV8871, one per actuator |
| Excavator deployment | 2 | 12 VDC linear actuators | 2 x DRV8871, one per actuator |
| Excavator motor | 1 | 12 VDC motor | 1 x RANSANX L298 module |

Total: nine motor/actuator loads and nine external driver modules.

- Low-level controller: ESP32-WROOM; exact module variant pending.
- High-level computer: NVIDIA Jetson Orin NX; carrier-board model pending.
- Wheel controller link supplied by user: https://www.amazon.com/BLDC-Three-Phase-Brushless-Controller-Function/dp/B0D97PN96D
- ZS-X11H and RANSANX L298 model names are user-confirmed. Exact module revisions, terminal pinouts and electrical specifications have not yet been independently verified.

## Retained architecture

Nominal 24/25.6 V control-power input, 5 V and 3.3 V logic rails, Jetson UART, CAN and independent hardware E-stop. High-current motor power remains off the control PCB. The source of the 12 V motor/actuator supply is still to be confirmed.

## Interface decisions pending

- Exact module pinouts and control-input electrical requirements for ZS-X11H, RANSANX L298 and DRV8871 boards.
- Excavator and linear-actuator running/startup/stall currents; module current limits and thermal capability.
- Wheel motor voltage/current and Hall-sensor connections.
- Stop/brake/inhibit behavior of each driver type for the hardware E-stop design.
- Jetson carrier-board model and UART interface voltage.
- Actuator feedback, end limits and paired-actuator synchronization requirements.

The KiCad design remains an architecture scaffold; no driver circuits or connector pinouts have been implemented.

Exact user-supplied module links and DRV8871 control research are recorded in Driver_Interfaces.md.

## Battery, distribution and CAN - latest user confirmation

Battery: Talentcell 25.6 V nominal, 6 Ah LiFePO4. Exact label/model and maximum charge/discharge specifications are still to be verified; LF8011 appears to match the description but is not user-confirmed. 6 Ah is capacity, not a 6 A discharge-current limit.

Existing distribution as described by user: battery -> DC current meter/sensing -> fuse box -> drivers and loads. Meter model, high-side/low-side shunt arrangement, upstream cable protection and any voltage conversion are unspecified. A meter and fuse box do not reduce the battery voltage to 12 V.

The 12 V actuator and excavator branches require a suitable external 12 V supply stage. No converter has yet been confirmed. Do not finalize driver power wiring from the stated chain. Treat approximately 29.2 V as a provisional full-charge design assumption for an 8-series-cell LiFePO4 pack, subject to exact battery label verification; this exceeds the excavator module's seller-stated 27 V maximum. Input component selection must also account for transients. Converter capacity and battery discharge capability must be checked against actual simultaneous motor currents before selection.

CAN is explicitly requested for BOTH Jetson-to-ESP32 communication and future expansion boards. Proposed topology: one shared Classical CAN bus connecting Jetson, controller PCB and expansion nodes. Provide a CAN transceiver at the ESP32 and two parallel bus connectors for cable continuation, with selectable 120-ohm termination on the controller board. These connectors are the same bus, not independent CAN controllers. Termination belongs at the two physical bus ends. Bitrate and cable topology remain to be finalized.

Jetson carrier-board identity is required to determine whether it already has a CAN transceiver or needs an external transceiver/adapter. Keep UART in the agreed architecture as an additional interface. Existing motor drivers retain their discrete control interfaces; adding CAN to the controller does not make the driver modules CAN devices. Hardware E-stop remains independent of successful CAN communication.

Primary references:
- https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/twai.html
- https://docs.nvidia.com/jetson/archives/r36.4.4/DeveloperGuide/HR/ControllerAreaNetworkCan.html

No CAN circuit or power-converter circuit has yet been implemented in the schematic.

## Confirmed external buck converter

User confirms use of DROK adjustable CC/CV buck converter, Amazon ASIN B078Q1624B:
https://www.amazon.com/dp/B078Q1624B

Manufacturer product specifications for the matching 5.3-32 V / 12 A module:
- Recommended input range: 5.3-32 V.
- Adjustable output: 1.2-32 V, with input at least 0.8 V above output.
- Long-term output current: 8 A; up to 12 A with enhanced cooling.
- Natural-cooling output power: 120 W, also subject to 8 A current limit; enhanced-cooling power up to 160 W.
- At a proposed 12 V setting, 8 A corresponds to 96 W shared by all attached loads. This is a specification-based budget, not verified installed performance.

The converter's existence is now confirmed, superseding earlier statements that no converter was identified. Its quantity, installed position relative to the fuse box, actual output setting, current-limit setting and supplied load branches remain unknown. Do not assume it powers every 12 V load or the Jetson. The nominal battery voltage lies within its input range; verify battery maximum and transient voltage against the 32 V recommended maximum. Motor startup/stall and simultaneous-load currents must fit the converter, battery and protection limits.

Manufacturer source:
https://www.droking.com/Adjustable-CC-CV-Buck-Converter-Power-Supply-Module-CC-CV-Buck-Converter-DC-5.3V-32V-24v-Step-Down-Voltage-Regulator-12A-160W-Adapter-Driver

## Confirmed 12 V branch topology

User clarified the order as fuse box -> buck converter -> driver, then confirmed FIVE buck converters. Interpreted allocation: one DROK per each of the four 12 V actuator/DRV8871 branches and one DROK for the 12 V excavator/RANSANX driver branch. This supersedes the earlier possibility of one shared converter.

Battery -> DC current meter/sensing -> fuse box -> individual DROK buck -> external driver -> load.

| Branch | Converter | Driver | Load |
|---|---|---|---|
| Dump 1 | DROK 1 | DRV8871 1 | 12 V linear actuator |
| Dump 2 | DROK 2 | DRV8871 2 | 12 V linear actuator |
| Excavator deployment 1 | DROK 3 | DRV8871 3 | 12 V linear actuator |
| Excavator deployment 2 | DROK 4 | DRV8871 4 | 12 V linear actuator |
| Excavator motor | DROK 5 | RANSANX module, one channel | 12 V excavator motor |

12 V is the required load supply target; actual converter settings have not been measured or confirmed. Converter limits apply per branch. The battery, current meter, shared wiring and fuse-box feed must support the combined input load. Five converters do not increase battery discharge capability. Individual load currents, fuse ratings and battery discharge rating remain open. Wheel-driver supply details and Jetson carrier/power details remain to be confirmed. No power circuitry has been implemented in KiCad yet.

## Confirmed wheel-driver supply

User confirms all four ZS-X11H wheel drivers receive power directly from the battery-fed fuse box, without buck converters. Each connects to its corresponding BLDC wheel motor. The four wheel-motor voltage/current ratings remain unconfirmed; the driver's voltage range alone does not establish motor compatibility.

Confirmed distribution:
- Talentcell 25.6 V nominal, 6 Ah LiFePO4 -> DC meter/sensing -> fuse box.
- Four wheel branches: fuse box -> ZS-X11H -> BLDC wheel motor.
- Four actuator branches: fuse box -> individual DROK buck (12 V target) -> DRV8871 -> actuator.
- One excavator branch: fuse box -> individual DROK buck (12 V target) -> RANSANX driver -> excavator motor.

This documents nine motor/actuator branches and five converters. Main fuse, branch fuse values, conductor sizes, current budget and E-stop power switching are not yet designed. Jetson and controller power branches remain to be established.

## Jetson carrier identified from underside photo

Photo clearly shows Seeed Studio reComputer J401 V1.0, with user-confirmed Jetson Orin NX 16 GB. This resolves earlier carrier identification questions. Do not substitute specifications for J401B, J401 Mini or J401 Robotics variants.

The board photo marks 9-19 V, 5 A MAX at the input. Seeed's J401 documentation confirms 9-19 V DC input; its datasheet lists an optional 12 V / 5 A supply with 5.5/2.5 mm barrel jack. Do not connect the nominal 25.6 V battery directly to this jack. Existing Jetson power source is still unknown; the five already-confirmed DROK converters are allocated to motor/actuator loads, not the Jetson.

The photo shows a header labeled 3V3, GND, CAN_RX, CAN_TX. These are logic-side CAN signals, not CAN_H/CAN_L. Seeed's J401 interface documentation states an external CAN transceiver is required. Plan a Jetson-side transceiver close to the carrier header and an ESP32-side transceiver on the control PCB, connected via the shared differential CAN bus with expansion nodes. Exact connector orientation, pin numbers and transceiver implementation remain to be verified before cable construction. Use Classical CAN frames for compatibility with ESP32-WROOM.

Sources:
- User's underside photograph (board model and power/header markings).
- https://wiki.seeedstudio.com/J401_carrierboard_Hardware_Interfaces_Usage/
- https://files.seeedstudio.com/wiki/reComputer-J4012/reComputer-J401-datasheet.pdf

## Jetson separate V-mount battery supply

User reports Jetson powered from a separate V-mount battery through D-Tap. Supplied ASIN B0CJ8Z28CS currently identifies NEEWER PS099E, 6800 mAh / 99 Wh / 14.54 V nominal. This resolves the previously unknown Jetson power source; it does not consume one of the five motor-branch DROK converters.

NEEWER distinguishes BP/D-Tap output (14.54 V nominal, 14 A max listed) from the regulated DC12V port (12 V, 3 A max). Therefore do not label the D-Tap connection as confirmed regulated 12 V. NEEWER lists 16.8 V D-Tap charging; approximately 16.8 V full-charge pack voltage is an inference consistent with that specification, not a measured cable output. Nominal and expected full-charge voltages lie within the J401 9-19 V input range. Actual D-Tap-to-barrel cable regulation, polarity, connector fit, current capability and voltage under load remain unverified.

Retain two separate positive power systems: Talentcell for motor/control distribution and V-mount for Jetson. Do not join positive outputs. Separate batteries alone do not provide galvanic isolation once UART/CAN reference wires or other cables join the systems. CAN isolation/reference and optional UART isolation must be designed consistently; do not claim electrical isolation solely from separate batteries.

Sources:
- https://www.amazon.com/dp/B0CJ8Z28CS
- https://eu.neewer.com/products/neewer-ps099e-6800mah-14-5v-99wh-v-mount-battery-66603180
- https://wiki.seeedstudio.com/J401_carrierboard_Hardware_Interfaces_Usage/

## Implementation update: onboard USB and controller CAN

The project now has 49 components across MCU, USB and CAN circuit sheets. This supersedes earlier statements that CAN/USB are entirely unimplemented. See README.md for the current implementation and validation status. The Jetson-side external CAN transceiver remains pending. The current controller CAN node is non-isolated and uses a signal-reference conductor; it is not claimed to isolate the two battery systems. CAN activity LED is on GPIO32, heartbeat on GPIO23. Hardware-enable and fault/E-stop LEDs remain pending with the safety/interface design. The regulator power sheet and motor interfaces remain unfinished.


## Power circuit stage - current status
Protected controller power is now implemented in 01_Power. The project has 69 physical components across four implemented sheets. A dedicated fusebox branch feeds reverse-polarity/surge protection, a 5 V LMR36510 and a 3.3 V TPS62160. The five external motor bucks remain unchanged. 29.2 V maximum pack voltage is an 8S design assumption pending label confirmation. See Power_Design.md and README.md for current validation and pending work. PCB placement/routing, safety, drivers and sensors remain incomplete.


## A3 driver/interlock stage - latest status
The project now has 171 schematic components across six implemented sheets, including 11 DNP links. Command interfaces for nine drivers and a hardware command interlock are drawn; sensors remain pending. This supersedes earlier scaffold-only statements. See Safety_And_Driver_Design.md for actual connector/GPIO assignments and limitations. Wheel/excavator outputs remain disconnected by DNP links until verified; external E-stop power switching is not designed yet. J301 is a voltage-free auxiliary-contact input, not a contactor coil output or 24 V input. PCB placement/routing remains undone.


## ZS-X11H diagram received
The user supplied a ZS-X11H V2 wiring diagram identifying a dedicated 2.5-5 V PWM input (50 Hz-20 kHz), external PWM jumper, Rotation/Stop switches to GND and Brake switch to driver 5 V. See Driver_Interfaces.md for interpretation and remaining uncertainties. Wheel DIR circuitry still requires switch-emulation revision/qualification; DNP links remain. No schematic changes in this evidence update. External E-stop hardware details remain pending.


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

## Wheel motor identification supplied by user

User supplied STEPperONLINE 57BLR50-24-01-HG100 product link in the wheel-load discussion. Treat as the proposed common model for the four wheels, pending confirmation that all installed units match.
Manufacturer listing: 24 V, rated current 5.0 A +/-10%, rated power 84 W, geared speed 35 RPM +/-10%, 100:1 gearbox, rated output torque 14.95 Nm. Source: https://www.omc-stepperonline.com/24v-84w-35rpm-geared-brushless-dc-motor-100-1-high-precision-gearbox-57blr50-24-01-hg100

Four identical units sum to 20 A nominal listed motor rated current (18-22 A with the stated tolerance). This is a preliminary motor-rating total, not a verified battery-side demand or startup/stall limit: the listing does not define its current measurement sufficiently for that conclusion, and PWM/controller operation affects DC-bus current. Actuator, excavation, converter and logic loads remain additional. Do not size the contactor, fuse or battery/BMS from this sum alone. Do not infer electrical input current from 84 W / 24 V in place of the listed current.

The user's earlier '6A' remains ambiguous; it has not been accepted as total rover current or a verified DC switch rating. The AI-generated 6 A resistive / 2 A inductive switch claims are not manufacturer evidence. Installed BAOMAIN direct switching remains unqualified. No schematic changes made by this motor-identification update.
