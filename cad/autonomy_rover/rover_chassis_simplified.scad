// Simplified simulation/reference CAD, dimensions in mm based on published overall envelope.
$fn=64;
L=870; W=750; deck=18;
module chassis(){
 color("gray") translate([0,0,220]) cube([L,W,deck],center=true);
 for(y=[-W/2+35,W/2-35]) for(x=[-L/2+45,L/2-45]) translate([x,y,360]) cube([40,40,280],center=true);
 // front conveyor reference body
 translate([L/2+90,0,350]) rotate([0,-45,0]) cube([650,500,70],center=true);
 // rear collection bucket reference
 translate([-L/2+130,0,430]) cube([300,600,420],center=true);
}
chassis();
