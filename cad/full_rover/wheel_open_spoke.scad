// Photo-derived open-spoke wheel, dimensions in mm. Provisional hub interfaces.
// 248 mm OD fits nominal 256 mm bed with 4 mm margin per side.
// Twelve swept, tapered fins. 22 mm radial projection retains the earlier half-fin request.
module wheel_body(outer_d=248, width=94, fin_height=22) {
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
      translate([rim_r-3,tan(25)*z,z]) cube([8,10,4],center=true);
     for(z=[-width/2+12,width/2-12])
      translate([outer_d/2+1,8+tan(25)*z,z]) cube([4,4,4],center=true);
    }
   }
  }
  // Six blind 2.5 mm pilot holes per face for prototype cover fasteners.
  for(side=[-1,1]) for(i=[0:5]) rotate([0,0,i*60])
   translate([rim_r-4,0,side*(width/2)]) rotate([side==1?180:0,0,0])
    translate([0,0,-1]) cylinder(d=2.5,h=9,$fn=24);
  cylinder(d=18,h=width+4,center=true,$fn=64);
  for(i=[0:5]) rotate([0,0,i*60]) translate([27.5,0,0]) cylinder(d=6.5,h=width+4,center=true,$fn=32);
 }
}

// Same cover is printed twice. All sizes in mm. Central opening is not a dust seal.
module wheel_cover(outer_d=248, fin_height=22) {
 rim_r=outer_d/2-fin_height;
 difference() {
  cylinder(r=rim_r,h=3,$fn=120);
  translate([0,0,-1]) cylinder(d=28,h=5,$fn=64);
  for(i=[0:5]) rotate([0,0,i*60]) translate([rim_r-4,0,-1]) cylinder(d=3.4,h=5,$fn=24);
 }
}
module reference_wheel(outer_d=248,width=100,fin_height=22) {
 wheel_body(outer_d,width-6,fin_height);
}
module assembled_reference_wheel(outer_d=248,width=100,fin_height=22) {
 reference_wheel(outer_d,width,fin_height);
 for(side=[-1,1]) translate([0,0,side*(width/2-3)]) rotate([side==1?0:180,0,0]) wheel_cover(outer_d,fin_height);
}
