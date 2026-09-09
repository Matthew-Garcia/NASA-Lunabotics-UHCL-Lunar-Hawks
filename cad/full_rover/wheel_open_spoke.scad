// Photo-derived open-spoke wheel, dimensions in mm. Provisional hub interfaces.
// Twelve swept, tapered fins. 22 mm radial projection retains the earlier half-fin request.
module reference_wheel(outer_d=304.8, width=100, fin_height=22) {
 rim_r=outer_d/2-fin_height;
 difference() {
  union() {
   // Thin continuous tread band plus reinforced edge rings; no solid side disks.
   difference() { cylinder(r=rim_r,h=width,center=true,$fn=120);
                  cylinder(r=rim_r-3.5,h=width+2,center=true,$fn=120); }
   for(z=[-width/2+3,width/2-3]) translate([0,0,z])
    difference() { cylinder(r=rim_r,h=6,center=true,$fn=120);
                   cylinder(r=rim_r-8,h=8,center=true,$fn=120); }
   cylinder(r=38,h=45,center=true,$fn=96);
   // Twelve narrow swept spokes on each side, leaving the web open.
   for(z=[-1,1]) for(i=[0:11]) rotate([0,0,i*30]) hull() {
    translate([34,0,z*18]) cube([8,7,5],center=true);
    rotate([0,0,10]) translate([rim_r-5,0,z*(width/2-5)]) cube([9,7,5],center=true);
   }
   // Thin angled paddles: diagonal across the width, tapered at the shoulders.
   // Envelope clipping keeps the fin-tip outside diameter exactly outer_d.
   intersection() {
    cylinder(d=outer_d,h=width,center=true,$fn=240);
    union() for(i=[0:11]) rotate([0,0,i*30]) hull() {
     for(z=[-width/2+1,width/2-1])
      translate([rim_r-1,0.30*z,z]) cube([3,4,2],center=true);
     for(z=[-width/2+12,width/2-12])
      translate([outer_d/2+1,8+0.30*z,z]) cube([2,4,2],center=true);
    }
   }
  }
  cylinder(d=18,h=width+4,center=true,$fn=64);
  for(i=[0:5]) rotate([0,0,i*60]) translate([27.5,0,0]) cylinder(d=6.5,h=width+4,center=true,$fn=32);
 }
}
