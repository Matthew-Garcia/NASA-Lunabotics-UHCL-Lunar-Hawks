// Reference reconstruction, millimetres. Not measured manufacturing CAD.
// Baseline fin projection is 44 mm in earlier generated CAD; half = 22 mm.
$fn=48;
part="assembly";
fin_original=44;
fin_height=fin_original/2;
wheel_outer_d=304.8;
wheel_width=100;
module beam(p,s){translate(p) cube(s,center=true);}
module wheel(){
 difference(){
  union(){
   difference(){cylinder(r=wheel_outer_d/2-fin_height,h=wheel_width,center=true); cylinder(r=wheel_outer_d/2-fin_height-10,h=102,center=true);}
   cylinder(r=wheel_outer_d/2-fin_height-3,h=8,center=true);
   cylinder(r=38,h=45,center=true);
   for(i=[0:11]) rotate([0,0,i*30]) translate([wheel_outer_d/2-fin_height/2-1,0,0]) cube([fin_height+2,22,96],center=true);
  }
  cylinder(d=18,h=110,center=true);
  for(i=[0:5]) rotate([0,0,i*60]) translate([27.5,0,0]) cylinder(d=6.5,h=110,center=true);
 }
}
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
module gate(){beam([0,0,120],[8,550,240]);}
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
 for(x=[-280,280]) for(y=[-375,375]) translate([x,y,152.4]) rotate([90,0,0]) color("gray") wheel();
 translate([-380,0,310]) color("silver") bucket();
 translate([-380,0,310]) color("gray") gate();
 translate([900,0,70]) rotate([0,-28,0]) {color("gray") conveyor(); for(z=[100:145:970]) translate([12,0,z]) color("navy") scoop();}
 translate([140,-220,310]) enclosure(180,110,40);
 translate([-100,-220,310]) enclosure(260,180,70);
}
if(part=="assembly") assembly();
if(part=="wheel") wheel();
if(part=="chassis") chassis();
if(part=="bucket") bucket();
if(part=="gate") gate();
if(part=="conveyor") conveyor();
if(part=="scoop") scoop();
if(part=="esp32_base") enclosure(180,110,40);
if(part=="esp32_lid") enclosure(180,110,40,true);
if(part=="jetson_base") enclosure(260,180,70);
if(part=="jetson_lid") enclosure(260,180,70,true);
