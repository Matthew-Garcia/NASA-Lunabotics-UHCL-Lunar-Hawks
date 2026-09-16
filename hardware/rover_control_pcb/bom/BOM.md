# Lunar Hawks controller PCB — draft bill of materials

**Status: engineering draft; not released for procurement or assembly.**

Per board: **201 schematic components; 186 populated, 15 DNP.** Quantities do not include purchasing spares. Four board-only mounting holes are mechanical features, not electronic parts.

Generated from a fresh KiCad schematic netlist. References, values, and DNP status were checked against the current PCB. A specified part number is copied from the design, not a claim of stock availability or completed package validation.

## Assembly BOM

| Qty per board | Populate qty | References | Value / function | Specified part number | Footprint | Status |
| ---: | ---: | --- | --- | --- | --- | --- |
| 1 | 1 | C101 | 22uF / 63V | TBD | Capacitor_THT:CP_Radial_D8.0mm_P3.50mm | Populate; Exact ordering code not selected |
| 1 | 1 | C102 | 2.2uF / 100V X7R | TBD | Capacitor_SMD:C_1210_3225Metric | Populate; Exact ordering code not selected |
| 1 | 1 | C103 | 220nF / 100V X7R | TBD | Capacitor_SMD:C_0805_2012Metric | Populate; Exact ordering code not selected |
| 1 | 1 | C104 | 1uF / 10V | TBD | Capacitor_SMD:C_0805_2012Metric | Populate; Exact ordering code not selected |
| 1 | 1 | C105 | 100nF / 16V | TBD | Capacitor_SMD:C_0805_2012Metric | Populate; Exact ordering code not selected |
| 2 | 2 | C106, C107 | 22uF / 25V X7R | TBD | Capacitor_SMD:C_1210_3225Metric | Populate; Exact ordering code not selected |
| 1 | 1 | C108 | 10uF / 16V X7R | TBD | Capacitor_SMD:C_0805_2012Metric | Populate; Exact ordering code not selected |
| 1 | 1 | C109 | 22uF / 16V X7R | TBD | Capacitor_SMD:C_1206_3216Metric | Populate; Exact ordering code not selected |
| 1 | 1 | C201 | 10uF / 10V X7R | TBD | Capacitor_SMD:C_0805_2012Metric | Populate; Exact ordering code not selected |
| 1 | 1 | C202 | 100nF / 10V X7R | TBD | Capacitor_SMD:C_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | C203 | 1uF / 10V X7R | TBD | Capacitor_SMD:C_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | C301 | 10nF / 16V | TBD | Capacitor_SMD:C_0603_1608Metric | Populate; Exact ordering code not selected |
| 11 | 11 | C302, C304, C305, C306, C307, C401, C403, C404, C405, C607, C701 | 100nF / 16V | TBD | Capacitor_SMD:C_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | C303 | 1uF / 16V X7R | TBD | Capacitor_SMD:C_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | C402 | 4.7uF / 10V | TBD | Capacitor_SMD:C_0603_1608Metric | Populate; Exact ordering code not selected |
| 3 | 3 | C601, C603, C605 | 4.7uF / 10V | TBD | Capacitor_SMD:C_0805_2012Metric | Populate; Exact ordering code not selected |
| 4 | 4 | C602, C604, C606, C703 | 100nF / 10V | TBD | Capacitor_SMD:C_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | C702 | 4.7uF / 16V | TBD | Capacitor_SMD:C_0805_2012Metric | Populate; Exact ordering code not selected |
| 1 | 1 | D101 | STPS1H100A | STPS1H100A | Diode_SMD:D_SMA | Populate; Verify ordering code and package |
| 1 | 1 | D102 | SMBJ33A | SMBJ33A | Diode_SMD:D_SMB | Populate; Verify ordering code and package |
| 3 | 3 | D201, D202, D203 | GREEN | TBD | LED_SMD:LED_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | D301 | GREEN_COMMAND_ENABLE | TBD | LED_SMD:LED_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | D302 | RED_INHIBITED | TBD | LED_SMD:LED_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | D701 | NUP2105LT1G | NUP2105LT1G | Package_TO_SOT_SMD:SOT-23 | Populate; Verify ordering code and package |
| 1 | 1 | D702 | GREEN / CAN ACT | TBD | LED_SMD:LED_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | J101 | FUSED_LOGIC_INPUT | TBD | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2_1x02_P5.00mm_Horizontal | Populate; Exact ordering code not selected |
| 1 | 1 | J201 | SERVICE_UART_3V3 | TBD | Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | J301 | SAFETY_AUX_DRY_CONTACT | TBD | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2_1x02_P5.00mm_Horizontal | Populate; Exact ordering code not selected |
| 1 | 1 | J401 | DUMP_1 | TBD | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | J402 | DUMP_2 | TBD | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | J403 | DEPLOY_1 | TBD | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | J404 | DEPLOY_2 | TBD | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | J405 | EXCAVATOR | TBD | Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | J406 | WHEEL_1 | TBD | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | J407 | WHEEL_2 | TBD | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | J408 | WHEEL_3 | TBD | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | J409 | WHEEL_4 | TBD | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | J601 | USB4105-GF-A | USB4105-GF-A | Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal | Populate; Verify ordering code and package |
| 1 | 1 | J701 | CAN_TO_JETSON | TBD | Connector_Molex:Molex_Micro-Fit_3.0_43650-0300_1x03_P3.00mm_Horizontal | Populate; Exact ordering code not selected |
| 1 | 1 | J702 | CAN_EXPANSION | TBD | Connector_Molex:Molex_Micro-Fit_3.0_43650-0300_1x03_P3.00mm_Horizontal | Populate; Exact ordering code not selected |
| 1 | 1 | J801 | WHEEL_1_STOP | TBD | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | J802 | WHEEL_2_STOP | TBD | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | J803 | WHEEL_3_STOP | TBD | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | J804 | WHEEL_4_STOP | TBD | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | JP601 | UART_SOURCE | TBD | Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | JP701 | END_TERMINATION | TBD | Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical | Populate; Exact ordering code not selected |
| 1 | 1 | L101 | 22uH / SRN6045TA-220M | SRN6045TA-220M | Inductor_SMD:L_Bourns_SRN6045TA | Populate; Verify ordering code and package |
| 1 | 1 | L102 | 3.3uH / SRN6045TA-3R3Y | SRN6045TA-3R3Y | Inductor_SMD:L_Bourns_SRN6045TA | Populate; Verify ordering code and package |
| 10 | 10 | Q301, Q401, Q402, Q403, Q404, Q801, Q802, Q803, Q804, Q805 | AO3400A | AO3400A | Package_TO_SOT_SMD:SOT-23 | Populate; Verify ordering code and package |
| 2 | 2 | R101, R104 | 100k 1% | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | R102 | 24.9k 1% | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | R103 | 312k 1% | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 48 | 48 | R201, R202, R203, R204, R302, R304, R305, R306, R410, R412, R413, R415, R416, R418, R419, R421, R422, R424, R425, R427, R428, R430, R431, R433, R434, R436, R437, R439, R440, R442, R443, R445, R446, R448, R449, R451, R452, R454, R455, R457, R458, R460, R461, R463, R464, R466, R701, R702 | 10k | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 2 | 2 | R205, R206 | 470 | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | R207 | 2.2k | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 7 | 7 | R208, R209, R301, R308, R309, R604, R704 | 1k | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | R303 | 200k 1% | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 2 | 2 | R307, R805 | 100k | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 2 | 2 | R401, R402 | 4.7k | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 8 | 8 | R411, R414, R417, R420, R423, R426, R429, R432 | 220R | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 2 | 2 | R601, R602 | 5.1k 1% | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | R603 | 0R | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | R605 | 22.1k 1% | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | R606 | 47.5k 1% | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | R703 | 120R 1% / 0.25W | TBD | Resistor_SMD:R_1206_3216Metric | Populate; Exact ordering code not selected |
| 4 | 4 | R801, R802, R803, R804 | 680R 1% | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 4 | 4 | R811, R812, R813, R814 | 47k 1% | TBD | Resistor_SMD:R_0603_1608Metric | Populate; Exact ordering code not selected |
| 1 | 1 | SW201 | RESET | TBD | Button_Switch_SMD:SW_SPST_TL3342 | Populate; Exact ordering code not selected |
| 1 | 1 | SW202 | BOOT | TBD | Button_Switch_SMD:SW_SPST_TL3342 | Populate; Exact ordering code not selected |
| 1 | 1 | U101 | LMR36510ADDAR | LMR36510ADDAR | Package_SO:Texas_HTSOP-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.4x3.1mm_ThermalVias | Populate; Verify ordering code and package |
| 1 | 1 | U102 | TPS62160DGKR | TPS62160DGKR | Package_SO:MSOP-8_3x3mm_P0.65mm | Populate; Verify ordering code and package |
| 1 | 1 | U201 | ESP32-WROOM-32E-N4 | ESP32-WROOM-32E-N4 | RF_Module:ESP32-WROOM-32D | Populate; Verify ordering code and package |
| 1 | 1 | U301 | SN74LVC1G17DBVR | SN74LVC1G17DBVR | Package_TO_SOT_SMD:SOT-23-5 | Populate; Verify ordering code and package |
| 1 | 1 | U302 | SN74LVC1G123DCUR | SN74LVC1G123DCUR | Package_SO:VSSOP-8_2.3x2mm_P0.5mm | Populate; Verify ordering code and package |
| 2 | 2 | U303, U305 | SN74LVC1G11DBVR | SN74LVC1G11DBVR | Package_TO_SOT_SMD:SOT-23-6 | Populate; Verify ordering code and package |
| 1 | 1 | U304 | SN74LVC1G74DCUR | SN74LVC1G74DCUR | Package_SO:VSSOP-8_2.3x2mm_P0.5mm | Populate; Verify ordering code and package |
| 1 | 1 | U401 | PCA9685PW | PCA9685PW | Package_SO:TSSOP-28_4.4x9.7mm_P0.65mm | Populate; Verify ordering code and package |
| 3 | 3 | U402, U403, U404 | SN74AHCT244PWR | SN74AHCT244PWR | Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm | Populate; Verify ordering code and package |
| 1 | 1 | U601 | CP2102N-A02-GQFN24 | CP2102N-A02-GQFN24 | Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.6x2.6mm | Populate; Verify ordering code and package |
| 1 | 1 | U602 | USBLC6-2SC6 | USBLC6-2SC6 | Package_TO_SOT_SMD:SOT-23-6 | Populate; Verify ordering code and package |
| 1 | 1 | U701 | TCAN1042HGVDRQ1 | TCAN1042HGVDRQ1 | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | Populate; Verify ordering code and package |
| 4 | 4 | U801, U802, U803, U804 | LTV-817S-B | LTV-817S-B | Package_DIP:SMDIP-4_W9.53mm | Populate; Verify ordering code and package |
| 11 | 0 | R435, R438, R441, R444, R447, R450, R453, R456, R459, R462, R465 | 220R DNP | TBD | Resistor_SMD:R_0603_1608Metric | DNP; Exact ordering code not selected |
| 4 | 0 | R821, R822, R823, R824 | 0R DNP | TBD | Resistor_SMD:R_0603_1608Metric | DNP; Exact ordering code not selected |

## Items to resolve before ordering

- Generic resistors, capacitors, LEDs, headers, and switches need exact manufacturer ordering codes. Confirm voltage, power, tolerance, dielectric, temperature, and mechanical ratings against circuit requirements; unspecified ratings are not implied by a footprint.
- U201 specifies ESP32-WROOM-32E-N4 but uses the library footprint named ESP32-WROOM-32D. Its pad geometry must be checked against the selected module land pattern. The corrected 3D model alone does not validate the footprint.
- Keep all 15 DNP links unpopulated until their associated external driver interfaces have been qualified. Their BOM population quantity is zero.
- Mating cable housings, crimp terminals, jumper shunts, mounting screws/standoffs, the bare PCB, and assembly consumables are not counted above. Select these after connector and enclosure review.

## External rover equipment — excluded from PCB assembly quantities

| Quantity | Equipment | Basis / unresolved detail |
| ---: | --- | --- |
| 4 | ZS-X11H BLDC driver modules | User-supplied equipment; external to controller PCB |
| 4 | DRV8871 actuator driver modules | One per linear actuator; exact module variant to verify |
| 1 | RANSANX excavator driver module | User-described dual H-bridge; exact module identity and ratings to verify |
| 5 | DROK buck converter modules | External motor/actuator supplies; separate from PCB regulators |
| 4 | BLDC wheel motors | Verify whether all match the linked STEPperONLINE motor |
| 4 | 12 V linear actuators | Two dump, two excavator deployment; exact models pending |
| 1 | 12 V excavator motor | Exact model pending |
| 1 | Jetson Orin NX 16 GB with Seeed J401 carrier | User-supplied computer; Jetson-side CAN transceiver still needs selection |
| 1 | Talentcell 25.6 V, 6 Ah LiFePO4 battery | Exact model/BMS ratings pending |
| 1 | Separate V-mount battery for Jetson | Verify exact D-Tap output specification |
| 1 each | DC meter, fusebox, E-stop | Exact meter/fuse selections and E-stop DC interruption rating unresolved |

## Source files

- `Lunar_Hawks_Rover_Control.kicad_sch` and its child sheets.
- `Lunar_Hawks_Rover_Control.kicad_pcb` for population cross-check.
- `BOM_Components.json` contains one record per schematic component for machine-readable use.
