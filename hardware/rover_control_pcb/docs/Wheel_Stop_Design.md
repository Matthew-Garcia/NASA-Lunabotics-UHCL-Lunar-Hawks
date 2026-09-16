# Wheel Stop interface draft — A5

Four channels use the ZS-X11H diagram supplied by the user, which shows Stop switched to ground. Actual module polarity, input current, startup behavior and stopping performance still require verification. This circuit is a Stop request, not a motor-power disconnect or a safety-rated function.

## Connections

J801/J802/J803/J804 correspond to wheels 1/2/3/4. Pin 1 is signal GND, pin 2 goes to that driver's STOP input, and pin 3 goes to that driver's 5 V OUT. These are provisional 2.54 mm prototype headers. Each driver 5 V net is separate from every other driver and from PCB 5 V. Grounds are shared; the system is not galvanically isolated.

Each AO3400A Stop MOSFET has a 47 kO gate pull-up powered by its own driver. An LTV-817S-B optocoupler pulls the gate down while motion is permitted. A common AO3400A driven by hardware MOTION_ENABLED lights all four optocouplers through individual 680 O resistors. Approximate LED load is 22 mA total on PCB 5 V, within the preliminary 150 mA direct-5-V allocation; the complete load budget still needs reconciliation. Optocoupler ordering suffix, temperature margins and package dimensions require procurement review.

## Intended states after qualification and link population

| Driver 5 V | Hardware motion enable / PCB supply | Stop request |
|---|---|---|
| Present | Disabled or PCB unpowered | MOSFET closes Stop to ground |
| Present | Enabled, PCB rails valid | Optocoupler opens Stop switch |
| Absent | Any | Not guaranteed by this circuit |

R821–R824 are deliberately not populated. As delivered, these four Stop connector signals are disconnected from their MOSFETs. Do not interpret the draft as providing operational stopping protection. The 11 wheel/excavator command links also remain DNP.

A broken signal ground, missing driver 5 V wire, stuck enable, or component fault can defeat the request. No brake or speed-feedback circuit is included. The user diagram shows Brake switched to driver 5 V, so it must not be treated as another ground-switch input. Stop release is common to all wheels; per-wheel speed remains controlled by PWM.

## E-stop and permissive

The confirmed installed circuit routes meter load positive through the latching push/twist E-stop directly to fusebox positive. Meter load negative goes directly to fusebox negative. There is no separate contactor. The proposed controller branch on that fusebox also loses power when pressed; Jetson uses its separate battery. Restart must require a fresh arm command and cleared stale outputs.

Aggregate DC interruption capability of the installed switch is not established. J301 is a 3.3 V voltage-free-contact input, not a battery input. Its valid closed-when-permitted contact arrangement remains unresolved; it has not been bypassed. The existing power-switch terminals must not connect to J301. Without a valid permissive, the draft stays inhibited.

## Qualification before assembly release

Verify each actual driver's Stop polarity, open/closed behavior, voltage and sink current with a current-limited test setup and safely restrained/unloaded mechanics. Check startup, disarm, watchdog expiry, MCU reset, controller power loss, driver power loss and restoration. Confirm no automatic restart after power or permissive restoration. Check stopping time under representative load separately. Populate links only after compatibility is established. Bench measurements, firmware and physical stopping tests have not been performed.

KiCad ERC and netlist checks verify connections and pad-number coverage only; they do not validate the above operating behavior. PCB placement and routing remain pending.

References: user-supplied ZS-X11H diagram; AO3400A datasheet https://www.aosmd.com/sites/default/files/res/datasheets/AO3400A.pdf ; Lite-On LTV-8X7 series https://optoelectronics.liteon.com/upload/download/DS-70-96-0016/LTV-8X7%20series%20%20Rev.S.PDF .
