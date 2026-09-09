// Photo-derived open-spoke wheel, dimensions in mm. Provisional hub interfaces.
// 248 mm OD fits nominal 256 mm bed with 4 mm margin per side.
// Twelve swept, tapered fins. 22 mm radial projection retains the earlier half-fin request.
module reference_wheel(outer_d=248, width=100, fin_height=22) {
 rim_r=outer_d/2-fin_height;
 difference() {
  union() {
   // 8 mm continuous tread band plus reinforced edge rings; no solid side disks.
   difference() { cylinder(r=rim_r,h=width,center=true,$fn=120);
                  cylinder(r=rim_r-8,h=width+2,center=true,$fn=120); }
   for(z=[-width/2+6,width/2-6]) translate([0,0,z])
    difference() { cylinder(r=rim_r,h=12,center=true,$fn=120);
                   cylinder(r=rim_r-14,h=14,center=true,$fn=120); }
   cylinder(r=45,h=64,center=true,$fn=96);
   // Twelve thick swept spokes on each side, leaving the web open.
   for(z=[-1,1]) for(i=[0:11]) rotate([0,0,i*30]) hull() {
    translate([40,0,z*27]) cube([14,16,12],center=true);
    rotate([0,0,10]) translate([rim_r-9,0,z*(width/2-8)]) cube([16,16,12],center=true);
   }
   // Thick angled paddles: diagonal across the width, tapered at the shoulders.
   // Envelope clipping keeps the fin-tip outside diameter exactly outer_d.
   intersection() {
    cylinder(d=outer_d,h=width,center=true,$fn=240);
    union() for(i=[0:11]) rotate([0,0,i*30]) hull() {
     for(z=[-width/2+1,width/2-1])
      translate([rim_r-3,0.30*z,z]) cube([8,14,4],center=true);
     for(z=[-width/2+12,width/2-12])
      translate([outer_d/2+1,8+0.30*z,z]) cube([4,8,4],center=true);
    }
   }
  }
  cylinder(d=18,h=width+4,center=true,$fn=64);
  for(i=[0:5]) rotate([0,0,i*60]) translate([27.5,0,0]) cylinder(d=6.5,h=width+4,center=true,$fn=32);
 }
}
