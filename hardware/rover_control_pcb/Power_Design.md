# Controller power design - schematic draft

## Power path and interfaces

Dedicated fusebox logic branch -> J101 (+ pin 1, return pin 2) -> D101 reverse-polarity diode -> protected input -> U101 5 V buck -> U102 3.3 V buck.

This circuitry powers the controller only. It is separate from all five external DROK motor buck converters and from the Jetson's V-mount battery. No motor power goes through this PCB. CAN and programming connections still share signal ground as described in README.md.

## Component choices

| References | Draft selection | Function / constraint |
|---|---|---|
| J101 | Phoenix MKDS 1.5, 2-position, 5 mm pitch footprint | Dedicated fused input; verify exact purchasing part and harness |
| D101 | STPS1H100A, SMA | 100 V, 1 A reverse-polarity series Schottky |
| D102 | Littelfuse SMBJ33A, SMB | Unidirectional TVS: cathode to protected positive, anode to GND |
| C101 | 22 uF / 63 V electrolytic, D8 mm, P3.5 mm | Input bulk and damping; exact ESR, ripple rating and mechanical part pending |
| U101 | LMR36510ADDAR, TI DDA | 65 V operating input, 400 kHz, 1 A buck |
| L101 | Bourns SRN6045TA-220M, 22 uH | 2.3 A typical thermal rating, 3.3 A typical saturation rating |
| C102, C103 | 2.2 uF / 100 V X7R; 220 nF / 100 V X7R | Local input bypass; place immediately at U101 VIN/PGND |
| C104, C105 | 1 uF / 10 V; 100 nF / 16 V | Internal VCC bypass; bootstrap capacitor from BOOT to SW |
| C106, C107 | Two 22 uF / 25 V X7R, 1210 | 5 V output filtering |
| R101, R102 | 100 kohm / 24.9 kohm, 1% | Nominal 5.016 V target |
| U102 | TPS62160DGKR, 8-pin VSSOP/MSOP | 1 A adjustable buck, supplied by 5 V |
| L102 | Bourns SRN6045TA-3R3Y, 3.3 uH | Oversized preliminary inductor; nominal tolerance +/-30%, footprint 6 mm class |
| C108, C109 | 10 uF / 16 V X7R; 22 uF / 16 V X7R | 3.3 V stage input/output bypass |
| R103, R104 | 312 kohm / 100 kohm, 1% | Nominal 3.296 V target |

Regulator power-good pins are intentionally unused. Their enable pins follow their respective inputs. The input supply remains present when motor motion is disabled; the independent E-stop design is still pending. This sheet does not implement battery undervoltage cutoff.

## Preliminary budget

Reserve 600 mA on 3.3 V for ESP32, CP2102N, logic and indicators, plus 150 mA directly on 5 V for CAN and indicators. These are design allowances, not measured currents.

Assuming 80% efficiency for the 3.3 V converter, this requires about 0.643 A at the 5 V regulator. Both stages use 1 A-rated ICs, but load limits depend on PCB cooling and selected passives. Future driver-interface circuitry must fit the remaining budget or trigger resizing. There is no spare-power connector for external loads.

A conservative two-stage planning calculation gives roughly 0.18 A input at 24 V using 80% first-stage efficiency and about 0.7 V diode drop. Battery input current is not equal to the 3.3 V output current. Startup/inrush and transient load peaks require measurement.

## Ratings and release requirements

- Battery maximum is provisionally 29.2 V for 8S LiFePO4; confirm actual battery and charger labels.
- Candidate external fuse: 1 A, at least 60 VDC. This is not a finalized fuse selection; verify interruption capacity, wire protection, inrush and diode/TVS fault coordination.
- SMBJ33A has 33 V standoff and a specified 53.3 V clamp at 11.3 A for its rated pulse. Actual clamping depends on surge waveform, source impedance, wiring and layout; it does not prove immunity to motor transients or sustained overvoltage.
- Use exact capacitors meeting effective capacitance after DC bias, ESR, temperature and ripple requirements. Nominal values and voltage ratings alone do not finalize the BOM. The first-stage output capacitor choice follows TI's 5 V nominal recommendation; account for downstream capacitance in stability testing.
- L102 tolerance and effective output capacitance must be evaluated together against TI's LC stability guidance. Check startup, load steps and light-load operation; the selected inductor is preliminary and can be reduced after validation.
- Keep U101 VIN bypass/hot loop short, SW copper small, and BOOT capacitor close. Connect its exposed pad to the ground plane with thermal vias. Route feedback from the output capacitor separately from switch-current paths. Do the same for U102 VOS/FB and its analog-ground return.
- Test current-limited startup, both rail voltages, ESP32 transmit bursts, USB enumeration/programming, CAN operation, temperature and shutdown before integration with motor power. Transient validation needs representative wiring and load conditions.

KiCad ERC is zero-error/zero-warning. Connectivity and footprint-pad checks pass. The PCB outline is still empty: no placement, routing, thermal verification or fabrication release has been completed.

## Manufacturer references

- TI LMR36510: https://www.ti.com/lit/ds/symlink/lmr36510.pdf
- TI TPS62160: https://www.ti.com/lit/ds/symlink/tps62160.pdf
- ST STPS1H100: https://www.st.com/resource/en/datasheet/stps1h100.pdf
- Littelfuse SMBJ33A: https://www.littelfuse.com/products/overvoltage-protection/tvs-diodes/surface-mount/smbj/smbj33a
- Bourns inductors: https://www.bourns.com/docs/product-datasheets/srn6045ta.pdf
