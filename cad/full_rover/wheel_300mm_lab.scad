// UHCL Lunar Hawks 300 mm laboratory-printer wheel test article.
// Outside diameter: 300 mm; axial width: 100 mm.
// Twelve swept fins at 30 degree spacing with 22 mm radial projection.
// Open-face configuration: optional side covers are intentionally omitted.
// Hub bore and bolt pattern remain provisional and must be checked on the rover.

use <wheel_open_spoke.scad>

part = "open";

// The open test article is 100 mm wide as a single printable body.
if (part == "open")
    wheel_body(outer_d=300, width=100, fin_height=22);

// The covered assembly uses a 94 mm body plus two 3 mm covers.
if (part == "body_for_covers")
    wheel_body(outer_d=300, width=94, fin_height=22);

if (part == "cover")
    wheel_cover(outer_d=300, fin_height=22);

if (part == "covered")
    assembled_reference_wheel(outer_d=300, width=100, fin_height=22);
