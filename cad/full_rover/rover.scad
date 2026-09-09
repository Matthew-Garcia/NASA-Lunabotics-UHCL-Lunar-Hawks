// Reference reconstruction, millimetres. Not measured manufacturing CAD.
// Baseline fin projection is 44 mm in earlier generated CAD; half = 22 mm.
$fn=48;
part="assembly";
bucket_tip=0; // degrees; front rises about rear bottom pivot
door_open=0; // degrees relative to bucket; top hinge
excavator_deploy=0; // 0 deployed, -14.3 travel pose
fin_original=44;
fin_height=fin_original/2;
wheel_outer_d=304.8;
wheel_width=100;
module beam(p,s){translate(p) cube(s,center=true);}
use <wheel_open_spoke.scad>
module wheel(){reference_wheel(wheel_outer_d,wheel_width,fin_height);}
module chassis(){
 for(y=[-300,300]) beam([0,y,0],[860,30,30]);
 for(x=[-415,0,415]) beam([x,0,0],[30,630,30]);
 beam([0,0,28],[820,600,6]);
 for(x=[-390,340]) for(y=[-290,290]) beam([x,y,210],[25,25,420]);
 for(y=[-300,300]) beam([0,y,400],[850,16,50]);
}
// Local bucket rear hinge at x=0; extends forward toward x=650.
module bucket(){
 beam([325,0,0],[650,550,8]);
 for(y=[-275,275]) beam([325,y,150],[650,8,300]);
 beam([650,0,150],[8,550,300]);
 for(y=[-260,260]) for(x=[30,620]) beam([x,y,140],[18,18,280]);
}
module gate(){
 beam([0,0,120],[8,550,240]);
 for(y=[-210,210]) translate([0,y,240]) rotate([90,0,0]) cylinder(d=16,h=36,center=true);
}
module latch(){difference(){cube([30,50,25],center=true);translate([10,0,0]) cube([16,18,30],center=true);}}
module actuator_body(){cylinder(d=40,h=300,center=true);}
module actuator_rod(){cylinder(d=16,h=230,center=true);}
module conveyor(){
 for(y=[-265,265]) beam([0,y,520],[35,25,1080]);
 beam([0,0,520],[8,490,980]);
 for(z=[35,1005]) translate([0,0,z]) rotate([90,0,0]) cylinder(d=100,h=570,center=true);
}
module scoop(){
 beam([35,0,0],[80,470,6]);
 beam([0,0,30],[6,470,60]);
 for(y=[-235,235]) beam([35,y,28],[80,6,60]);
}
module enclosure(l,w,h,lid=false){
 if(!lid) difference(){
  translate([-l/2,-w/2,0]) cube([l,w,h]);
  translate([-l/2+3,-w/2+3,3]) cube([l-6,w-6,h]);
  for(x=[-l/2+15:14:l/2-15]) translate([x,-w/2-1,h/2]) cube([7,6,h/3]);
 } else difference(){
  translate([-l/2,-w/2,0]) cube([l,w,3]);
  for(x=[-l/2+12:12:l/2-12]) for(y=[-w/2+12:12:w/2-12]) translate([x,y,-1]) cylinder(d=6,h=5,$fn=6);
 }
}
module assembly(){
 translate([0,0,260]) color("silver") chassis();
 for(x=[-280,280]) for(y=[-375,375]) translate([x,y,152.4]) rotate([90,0,0]) color("firebrick") wheel();
 translate([-380,0,310]) rotate([0,-bucket_tip,0]) {
  color("silver") bucket();
  translate([0,0,240]) rotate([0,door_open,0]) translate([0,0,-240]) color("gray") gate();
  translate([-20,0,15]) color("black") latch();
 }
 translate([424,0,966]) rotate([0,excavator_deploy,0]) translate([476,0,-896]) rotate([0,-28,0]) {color("gray") conveyor(); for(z=[100:145:970]) translate([12,0,z]) color("navy") scoop();}
 for(y=[-260,260]) translate([-200,y,420]) rotate([0,28.6,0]) {actuator_body();translate([0,0,180+bucket_tip*3.49]) actuator_rod();}
 for(y=[-290,290]) translate([330,y,410]) rotate([0,25.8,0]) {actuator_body();translate([0,0,150+(excavator_deploy+14.3)*10.49]) actuator_rod();}
 translate([140,-220,310]) enclosure(180,110,40);
 translate([-100,-220,310]) enclosure(260,180,70);
}
if(part=="assembly") assembly();
if(part=="wheel") wheel();
if(part=="chassis") chassis();
if(part=="bucket") bucket();
if(part=="gate") gate();
if(part=="latch") latch();
if(part=="actuator_body") actuator_body();
if(part=="actuator_rod") actuator_rod();
if(part=="conveyor") conveyor();
if(part=="scoop") scoop();
if(part=="esp32_base") enclosure(180,110,40);
if(part=="esp32_lid") enclosure(180,110,40,true);
if(part=="jetson_base") enclosure(260,180,70);
if(part=="jetson_lid") enclosure(260,180,70,true);
