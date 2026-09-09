// UHCL NASA Lunabotics grouser wheel — parametric test article
// Paper dimensions: 304.8 mm diameter, 100 mm width, 12 evenly spaced grousers.
// Requested change: radial grouser projection shortened to ~half of the prior nominal fin length.
$fn=128;
wheel_d=304.8;
wheel_w=100;
rim_t=14;
hub_d=115;
hub_t=16;
num_grousers=12;
grouser_radial=22; // shortened; baseline parametric fin was 44 mm
grouser_tangential=28;
grouser_axial=96;
shaft_hole=18;
bolt_circle=55;
bolt_d=6.5;
module wheel(){
 difference(){
  union(){
   difference(){ cylinder(d=wheel_d-2*grouser_radial,h=wheel_w,center=true); cylinder(d=wheel_d-2*grouser_radial-2*rim_t,h=wheel_w+2,center=true); }
   cylinder(d=hub_d,h=hub_t,center=true);
   for(a=[0:360/num_grousers:359]) rotate([0,0,a]) translate([(wheel_d/2-grouser_radial/2-rim_t/3),0,0]) cube([grouser_radial+rim_t,grouser_tangential,grouser_axial],center=true);
   for(a=[0:30:330]) rotate([0,0,a]) hull(){ translate([hub_d/2-5,0,0]) cylinder(d=12,h=hub_t,center=true); translate([wheel_d/2-grouser_radial-rim_t/2,0,0]) cylinder(d=12,h=hub_t,center=true); }
  }
  cylinder(d=shaft_hole,h=wheel_w+5,center=true);
  for(a=[0:60:359]) rotate([0,0,a]) translate([bolt_circle/2,0,0]) cylinder(d=bolt_d,h=wheel_w+5,center=true);
 }
}
wheel();
