# Rev A power-stage connectivity — engineering review draft

This document is the pin/net contract for `01_power_protection.kicad_sch`. It is intentionally more explicit than the graphical sheet so every connection can be reviewed before ERC and PCB layout.

**Status:** component-level Rev A candidate design; not released for fabrication. Values marked *candidate* or *provisional* must be rechecked against the actual rover battery, harness, transient environment, load current, temperature rise, and selected packages.

## Design targets

- Nominal rover control input: 24 V class; expected use with the rover's 25.6 V-class LiFePO4 system must be confirmed against the actual pack's maximum charge voltage.
- Logic rails: +5 V and +3.3 V.
- High-current wheel, conveyor, and actuator power does **not** pass through this PCB.
- +5 V design ceiling: 1 A regulator capability, with board/system continuous load to be derated after thermal test.
- +3.3 V regulator capability: 1 A device capability; initial board-level continuous target <= 0.5 A pending thermal validation.

## Input protection

| Ref | Candidate | Connection / intent |
| --- | --- | --- |
| J1 | 2-pin locking power connector, final family TBD | Pin 1 `VIN_24V`; pin 2 `GND` |
| F1 | 1 A, >= 60 V DC-rated SMD fuse candidate; exact MPN TBD after I²t/inrush review | `VIN_24V` -> `VIN_FUSED` |
| D1 | SMBJ33CA candidate, bidirectional TVS | Across `VIN_FUSED` and `GND`; verify actual battery maximum is below TVS standoff and verify surge energy |
| U1 | LM74700-Q1, DBV/SOT-23-6 | Reverse-polarity / ideal-diode controller |
| Q1 | External 100 V N-channel MOSFET, low-RDS(on), exact MPN/package TBD | Series reverse-polarity pass FET; thermal and SOA review required |
| C1 | 100 nF, 100 V X7R | U1 `VCAP` to `ANODE` per controller charge-pump requirement |

### LM74700-Q1 pin contract

| U1 pin | Name | Rev A net |
| ---: | --- | --- |
| 1 | VCAP | `U1_VCAP`; C1 returns to `VIN_FUSED` / ANODE |
| 2 | GND | `GND` |
| 3 | EN | tied to `VIN_FUSED` for always-enabled reverse protection while input is present |
| 4 | CATHODE | `VIN_PROT` / Q1 drain side |
| 5 | GATE | `Q1_GATE` |
| 6 | ANODE | `VIN_FUSED` / Q1 source side |

Q1 source connects to `VIN_FUSED`, drain to `VIN_PROT`, and gate to `Q1_GATE`. Before layout, confirm the selected MOSFET's source/drain orientation, VDS/VGS ratings, RDS(on) at the available gate drive, power dissipation, and body-diode direction against the LM74700-Q1 data sheet.

## Protected input filtering

| Ref | Candidate | Connection |
| --- | --- | --- |
| C2 | 47 uF, 63 V low-ESR bulk | `VIN_PROT` to `GND` |
| C3 | 2.2 uF, 100 V X7R | `VIN_PROT` to `GND`, close to U2 VIN/GND |
| C4 | 2.2 uF, 100 V X7R | `VIN_PROT` to `GND`, close to U2 VIN/GND |

A ferrite/LC input stage is intentionally **not frozen** in Rev A. Add it only after cable-length/EMI measurements so the input network is damped rather than creating a high-Q resonance.

## +5 V buck — LM5164

**U2:** LM5164, 8-pin SO PowerPAD, candidate footprint `Package_SO:SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.29x3mm`.

| U2 pin | Name | Rev A connection |
| ---: | --- | --- |
| 1 | GND | `GND`; exposed pad also to ground plane with thermal vias |
| 2 | VIN | `VIN_PROT` |
| 3 | EN/UVLO | `UVLO_NODE` from R1/R2 divider |
| 4 | RON | R3 to `VIN_PROT`; do **not** combine with UVLO divider |
| 5 | FB | `FB_5V` |
| 6 | PGOOD | `PWR_GOOD`; open-drain, R8 pulls to +3.3 V |
| 7 | BST | C5 to `SW_5V` |
| 8 | SW | `SW_5V`; to L1 and Type-3 ripple network |

### Switching-frequency / on-time network

Target nominal switching frequency: **300 kHz**.

For the LM5164 relation `R_RON(kOhm) ~= VOUT * 2500 / FSW(kHz)`:

- VOUT = 5 V
- FSW = 300 kHz
- calculated RON = 41.67 kOhm
- **R3 candidate: 41.2 kOhm, 1%**, `VIN_PROT` -> U2 RON

### UVLO divider

**Provisional only** until the rover battery envelope is frozen:

- R1 = 1.00 MOhm, `VIN_PROT` -> `UVLO_NODE`
- R2 = 82.5 kOhm, `UVLO_NODE` -> `GND`

Using the LM5164 typical 1.5 V rising and 1.4 V falling enable thresholds, this divider gives approximately **19.7 V turn-on** and **18.4 V turn-off**. Recalculate with min/max thresholds and the actual pack discharge limits before release.

### Bootstrap / power stage

| Ref | Candidate | Connection |
| --- | --- | --- |
| C5 | 2.2 nF, 50 V C0G/X7R | U2 BST -> `SW_5V`; place directly at pins |
| L1 | 68 uH, Isat >= 1.8 A candidate | `SW_5V` -> `+5V` |
| C6 | 22 uF, 25 V X7R | `+5V` -> `GND` |
| C7 | 22 uF, 25 V X7R | `+5V` -> `GND` |

At 24 V nominal input, 5 V output, 68 uH, and 300 kHz, the ideal inductor ripple estimate is about **0.19 A peak-to-peak**. Inductor DCR, temperature rise, saturation margin, and transient response remain release gates.

### Feedback divider

- R4 = 316 kOhm, 1%, `+5V` -> `FB_5V`
- R5 = 100 kOhm, 1%, `FB_5V` -> `GND`
- With a 1.2 V nominal FB reference, target VOUT is approximately **4.99 V**.

### Type-3 ripple injection — candidate

The LM5164 COT regulator requires controlled feedback ripple. Rev A uses a candidate Type-3 network:

- R6 = 196 kOhm, 1%, `SW_5V` -> `RIPPLE_NODE`
- C8 = 3.3 nF, C0G, `RIPPLE_NODE` -> `+5V`
- C9 = 82 pF, C0G, `RIPPLE_NODE` -> `FB_5V`

For R4 || R5 ~= 76 kOhm, the 3.3 nF CA value is comfortably above the data-sheet minimum at 300 kHz. The 196 kOhm candidate produces approximately 20 mV-class injected ripple around the nominal 24 V condition. Recheck the full minimum/maximum VIN range and load-transient target in simulation and on the bench.

### Power-good

- R8 = 10 kOhm, `+3V3` -> `PWR_GOOD`
- U2 PGOOD -> `PWR_GOOD`

`PWR_GOOD` therefore indicates that the LM5164 5 V regulation window is valid. It is **not** an independent 3.3 V supervisor.

## +3.3 V post-regulator

**U3:** TLV76733, fixed 3.3 V / 1 A LDO candidate in SOT-23-5 (`TLV76733DBVR` candidate).

| U3 pin | Name | Rev A connection |
| ---: | --- | --- |
| 1 | IN | `+5V` |
| 2 | GND | `GND` |
| 3 | EN | tied to `+5V` for always-on logic rail when 5 V is present |
| 4 | DNC | no connect |
| 5 | OUT | `+3V3` |

| Ref | Candidate | Connection |
| --- | --- | --- |
| C10 | 4.7 uF, 10 V X7R | U3 IN / `+5V` -> `GND` |
| C11 | 10 uF, 10 V X7R | U3 OUT / `+3V3` -> `GND` |

At 0.5 A on 3.3 V, the LDO dissipates roughly `(5 - 3.3) * 0.5 = 0.85 W`; therefore 0.5 A is already a meaningful thermal case. Validate copper area and junction temperature before allowing larger sustained 3.3 V loads.

## Test points

Provide accessible labeled pads for:

- `TP_VIN` — VIN_24V
- `TP_FUSED` — VIN_FUSED
- `TP_PROT` — VIN_PROT
- `TP_SW` — SW_5V (small probe pad; keep loop area minimal)
- `TP_5V` — +5V
- `TP_3V3` — +3V3
- `TP_PGOOD` — PWR_GOOD
- at least two `TP_GND` points suitable for oscilloscope ground spring access

## Bring-up / release gates

1. Confirm actual pack nominal, maximum charge, minimum permitted discharge, and hot-plug behavior.
2. Select Q1 and verify LM74700-Q1 compatibility, body-diode orientation, VDS/VGS, SOA, RDS(on), and thermal margin.
3. Verify F1 current/time curve against regulator inrush and downstream short-circuit cases.
4. Check SMBJ33CA standoff against battery maximum and clamping/current capability against measured or specified transients.
5. Run LM5164 calculations/WEBENCH or equivalent independent power-stage review across VIN/load corners.
6. Run ERC and resolve every warning intentionally.
7. Review creepage/clearance, switch-node area, feedback routing, thermal vias, and return-current paths before DRC release.
8. Bring up with a current-limited bench supply and external motor/actuator drivers disconnected.
9. Scope VIN_PROT, +5V, +3V3, SW, and PGOOD through start-up, brownout, hot-plug, and representative load steps.
10. Do not release Gerbers or a purchasing BOM until these gates are closed.
