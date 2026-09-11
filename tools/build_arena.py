from pathlib import Path
import xml.etree.ElementTree as E
root=E.Element('sdf',version='1.6');w=E.SubElement(root,'world',name='lunar_hawks_arena')
def add(p,t,text): E.SubElement(p,t).text=str(text)
add(w,'gravity','0 0 -9.81')
for uri in ['model://sun','model://ground_plane']:add(E.SubElement(w,'include'),'uri',uri)
def obj(name,xyz,size,color,static=True):
 m=E.SubElement(w,'model',name=name);add(m,'static',str(static).lower());add(m,'pose',xyz+' 0 0 0');l=E.SubElement(m,'link',name='body')
 if not static:
  i=E.SubElement(l,'inertial');add(i,'mass',.03);inertia=E.SubElement(i,'inertia')
  for k in ['ixx','iyy','izz']:add(inertia,k,.00002)
 for kind in ['visual','collision']:
  v=E.SubElement(l,kind,name=kind);add(E.SubElement(E.SubElement(v,'geometry'),'box'),'size',size)
  if kind=='visual':
   mat=E.SubElement(v,'material');add(mat,'ambient',color);add(mat,'diffuse',color)
for n,p,s in [('north','3 3 .3','10 .1 .6'),('south','3 -3 .3','10 .1 .6'),('west','-2 0 .3','.1 6 .6'),('east','8 0 .3','.1 6 .6')]:obj(n,p,s,'.3 .3 .3 1')
# Four posts are blue simulation targets, deliberately separated in camera projection.
for i,y in enumerate([-1.0,-.45,.45,1.0]):obj('goal_post_'+str(i),f'6 {y} .65','.09 .09 1.3','.05 .2 .9 1')
obj('disposal_pad','5.2 0 .025','2.6 2.4 .05','.2 .35 .2 1')
for i in range(24):obj('regolith_'+str(i),f'{1.4+(i//6)*.12} {-.20+(i%6)*.08} .035','.045 .045 .045','.45 .4 .32 1',False)
E.indent(root)
p=Path(__file__).resolve().parents[1]/'ros2_ws/src/lunabotics_description/worlds/arena.world';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(E.tostring(root,encoding='unicode'))
