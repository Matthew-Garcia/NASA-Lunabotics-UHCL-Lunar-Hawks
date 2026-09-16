# Physical PCB layout — A6 draft

The board now contains all 201 schematic components, including the 15 intentional DNP signal links, plus four provisional M3 mounting holes. It is a 160 x 100 mm, four-copper-layer board. This replaces the earlier empty-outline stage.

## Arrangement

- Top left: fused controller input and the 5 V / 3.3 V converters.
- Top edge: USB programming and the ESP32 antenna, with the library antenna keepout retained across copper layers.
- Top right: two CAN connectors, termination and transceiver.
- Left edge: six status LEDs; lower left: the voltage-free permissive connector and interlock logic.
- Lower center: PWM expansion and three output buffers.
- Bottom edge: nine driver-command connectors.
- Right edge: four wheel Stop connectors and their default-request circuits.

Inner layer 1 is a ground reference plane. Inner layer 2 carries a 3.3 V pour and some signal routes; the pour clears around those routes. Signals use front/back and inner-layer-2 copper with through vias. A bottom-layer 5 V pour distributes power around signal routes, with dedicated supply vias. Inner layer 1 remains the ground reference. Component references are on the front fabrication layer to keep the silkscreen readable; connector functions and status meanings are on silkscreen. The mechanical hole pattern and connector access still require enclosure review.

This is a physical routing draft, not a manufacturing release. Review switcher hot loops, ground-return widths, power neck-downs, USB differential routing, decoupler access, plane return paths and production stackup before fabrication. Preliminary routing rules assume 0.15 mm minimum copper clearance/track width, 0.5 mm vias with 0.25 mm drills, and some library thermal holes of 0.2 mm; confirm fabrication capability. No fabricated or powered PCB has been tested.

Motor-current paths remain off this board. The user's 10 A total battery draw is a planning assumption, not a verified worst-case load or a DC rating for the E-stop. The physical layout does not resolve the existing E-stop interruption rating or the J301 permissive integration. All 15 DNP links remain DNP. Sensor/end-limit circuits and firmware remain outstanding.

See PCB_Both_Logos_DRC.json and PCB_Layout_Status.json for the latest measured routing/check status. Schematic ERC and PCB DRC are separate checks; a clean schematic does not mean the PCB is ready to fabricate.

The draft uses 0.15 mm signal tracks. Sixty power-track segments were widened to 0.5 mm where clearance allowed, and a bottom 5 V pour was added. Short power neck-downs and regulator current paths still require thermal/current-capacity and switching-loop review before fabrication; connectivity alone is not sufficient. The preview may omit unavailable component models, including the CAN connector bodies.

## Final A6 connectivity check

KiCad 9.0.4 PCB DRC, with schematic-parity checking enabled: zero violations, zero unconnected items, zero schematic-parity issues. No violations were excluded to obtain this result. All 201 schematic components are placed; four board-only mounting holes are additional. All 15 intended DNP links remain marked DNP. This is completion of the physical routing draft, not electrical/thermal/EMC validation or fabrication approval.

PCB_Front_Logo.png and PCB_Blue_White_Routing.svg show front silkscreen and front/back routing for review; inner routes and pours are visible in the native board. PCB_Placement.csv lists all positions. Component references are on F.Fab.

## Blue appearance update

The PCB specifies blue solder mask and white silkscreen on both sides. PCB_Front_Logo.png and PCB_Blue_White_Routing.svg illustrate front and back routing in white/light blue on a blue background; these trace colors are for visualization. Physical copper traces are covered by solder mask, except exposed pads. Inner-layer routes and copper pours are omitted from this illustration for readability.

J402 (DUMP2) is connected: pins 2 and 3 have back-copper signal routes, and pin 1 connects to ground through the ground plane. The prior top-only preview hid these connections.

The user confirmed the ESP32 with the metal shield. Retain the directly soldered ESP32-WROOM-32E-N4 module; no bare-QFN redesign or plug-in development board is requested. This appearance update does not change electrical connectivity.

ESP32 visualization fix: bundled the ESP32-WROOM-32E STEP model and replaced the missing WROOM-32D model reference. Applied +2.99 mm model Y offset to account for the library footprint origin difference. Electrical pads and routing are unchanged. The metal shield and integrated module antenna are part of this assembly; no bare-chip RF redesign was performed.

## Team logo
LOGO1 is a 48 mm monochrome version of the supplied UHCL logo on B.Silkscreen, centered at (137, 91) mm and readable from the rear. It is board-only artwork excluded from BOM and placement. Source and monochrome artwork are in artwork/. Latest logo DRC: zero violations and zero unconnected items. Fine lettering/0.12 mm artwork detail still needs silkscreen capability review. The front title and electrical design are preserved.


Front logo trial: LOGO2, 23 mm wide, F.Silkscreen, centered at (140.5, 85.5) mm. Back logo retained. Both logo footprints are excluded from BOM and assembly placement. No copper or component placement changed. DRC reports zero violations and zero unconnected items. The full emblem's fine lettering at 23 mm may not reproduce reliably in silkscreen; simplify or omit the front trial before manufacture if the fabricator cannot resolve it.

