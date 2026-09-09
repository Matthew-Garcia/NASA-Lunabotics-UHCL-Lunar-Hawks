// UHCL Lunar Hawks 300 mm laboratory-printer wheel test article.
// Outside diameter: 300 mm; axial width: 100 mm.
// Twelve swept fins at 30 degree spacing with 22 mm radial projection.
// Open-face configuration: optional side covers are intentionally omitted.
// Hub bore and bolt pattern remain provisional and must be checked on the rover.

use <wheel_open_spoke.scad>

wheel_body(outer_d=300, width=100, fin_height=22);
