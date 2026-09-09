"""Regenerate the reference-derived URDF. Meshes are mm; ROS geometry is m."""
from pathlib import Path
import xml.etree.ElementTree as E
import shutil
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'ros2_ws/src/lunabotics_description'
r=E.Element('robot',name='lunar_hawks')
def sub(p,t,**a): return E.SubElement(p,t,{k:str(v) for k,v in a.items()})
def txt(p,t,v): sub(p,t).text=str(v)
def link(n,mesh=None,m=1,box=None,color='0.65 0.68 0.70 1'):
 l=sub(r,'link',name=n); i=sub(l,'inertial'); sub(i,'mass',value=m)
 sub(i,'inertia',ixx=max(.002,m*.04),iyy=max(.002,m*.05),izz=max(.002,m*.05),ixy=0,ixz=0,iyz=0)
 v=sub(l,'visual'); g=sub(v,'geometry')
 if mesh: sub(g,'mesh',filename=f'package://lunabotics_description/meshes/{mesh}.stl',scale='.001 .001 .001')
 else: sub(g,'box',size=box or '.04 .04 .04')
 sub(sub(v,'material',name=n+'_color'),'color',rgba=color)
 if box: sub(sub(sub(l,'collision'),'geometry'),'box',size=box)
 return l
def joint(n,parent,child,xyz='0 0 0',rpy='0 0 0',typ='fixed',axis='0 1 0',limits=None):
 j=sub(r,'joint',name=n,type=typ);sub(j,'parent',link=parent);sub(j,'child',link=child);sub(j,'origin',xyz=xyz,rpy=rpy)
 if typ=='fixed':txt(sub(r,'gazebo',reference=n),'preserveFixedJoint','true')
 if typ!='fixed':
  sub(j,'axis',xyz=axis);sub(j,'dynamics',damping=.4,friction=.05)
  if limits: sub(j,'limit',lower=limits[0],upper=limits[1],effort=800,velocity=.2)
 return j
link('base_link','chassis',20,box='.86 .63 .08')
for side,y in [('l',.375),('r',-.375)]:
 for end,x in [('f',.28),('r',-.28)]:
  n='wheel_'+end+side; l=link(n,'wheel',2,color='.65 .10 .08 1')
  c=sub(l,'collision');sub(sub(c,'geometry'),'cylinder',radius=.1524,length=.1)
  joint(n+'_joint','base_link',n,f'{x} {y} -.1076','1.57079632679 0 0','continuous',axis='0 0 -1')
  gz=sub(r,'gazebo',reference=n);txt(gz,'mu1',1);txt(gz,'mu2',1)
link('bucket','bucket',5)
joint('bucket_joint','base_link','bucket','-.38 0 .05',typ='revolute',axis='0 -1 0',limits=(0,1.0))
door=link('rear_door','gate',1)
sub(door.find('visual'),'origin',xyz='0 0 -.24')
sub(door.find('inertial'),'origin',xyz='0 0 -.12')
c=sub(door,'collision');sub(c,'origin',xyz='0 0 -.12');sub(sub(c,'geometry'),'box',size='.008 .55 .24')
door_joint=joint('rear_door_joint','bucket','rear_door','0 0 .24',typ='revolute',limits=(0,1.6))
# Low-friction free hinge; generic actuator friction prevented gravity closure.
door_joint.find('dynamics').set('friction','0.002')
door_joint.find('dynamics').set('damping','0.08')
link('electronic_latch','latch',box='.03 .05 .025',m=.1)
joint('latch_mount','bucket','electronic_latch','-.02 0 .015')
# Compound collision permits material to sit inside the open bucket.
b=r.find("link[@name='bucket']")
for xyz,size in [('.325 0 0','.65 .55 .008'),('.325 -.275 .15','.65 .008 .3'),('.325 .275 .15','.65 .008 .3'),('.65 0 .15','.008 .55 .3')]:
 c=sub(b,'collision');sub(c,'origin',xyz=xyz);sub(sub(c,'geometry'),'box',size=size)
link('excavator_pivot',box='.04 .55 .04',m=.3)
joint('excavator_deploy_joint','base_link','excavator_pivot','.424 0 .706',typ='revolute',limits=(-.25,0))
link('conveyor','conveyor',4)
joint('conveyor_mount','excavator_pivot','conveyor','.476 0 -.896','0 -.488692 0')
link('conveyor_drive',box='.04 .04 .04',m=.1)
joint('conveyor_drive_joint','conveyor','conveyor_drive','0 0 1.005',typ='continuous')
for i in range(7):
 link(f'scoop_{i}','scoop',.1,color='.04 .1 .3 1')
 joint(f'scoop_{i}_joint','conveyor',f'scoop_{i}','.012 0 .1',typ='prismatic',axis='0 0 1',limits=(0,.95))
for name,x,y,mesh in [('esp32',.14,-.22,'esp32_base'),('jetson',-.10,-.22,'jetson_base')]:
 link(name,mesh,.3);joint(name+'_mount','base_link',name,f'{x} {y} .05')
 lid=mesh.replace('base','lid');link(name+'_lid',lid,.1);joint(name+'_lid_mount',name,name+'_lid','0 0 '+('.04' if name=='esp32' else '.07'))
for side,y in [('left',.26),('right',-.26)]:
 link('actuator_'+side,'actuator_body',box='.04 .04 .36',m=.7)
 joint('actuator_'+side+'_mount','base_link','actuator_'+side,f'-.2 {y} .16','0 .5 0')
for side in ['left','right']:
 link('actuator_rod_'+side,'actuator_rod',box='.016 .016 .25',m=.2)
 joint('actuator_rod_'+side+'_joint','actuator_'+side,'actuator_rod_'+side,'0 0 .18',typ='prismatic',axis='0 0 1',limits=(0,.2))
for side,y in [('left',.29),('right',-.29)]:
 link('excavator_actuator_'+side,'actuator_body',box='.04 .04 .3',m=.7)
 joint('excavator_actuator_'+side+'_mount','base_link','excavator_actuator_'+side,f'.33 {y} .15','0 .45 0')
 link('excavator_rod_'+side,'actuator_rod',box='.016 .016 .23',m=.2)
 joint('excavator_rod_'+side+'_joint','excavator_actuator_'+side,'excavator_rod_'+side,'0 0 .15',typ='prismatic',axis='0 0 1',limits=(0,.15))
link('lidar_link',box='.06 .06 .05',m=.15);joint('lidar_mount','base_link','lidar_link','.15 0 .5')
link('camera_link',box='.04 .08 .04',m=.1);joint('camera_mount','base_link','camera_link','.36 0 .48')
sub(r,'link',name='camera_optical_frame');joint('camera_optical','camera_link','camera_optical_frame',rpy='-1.57079632679 0 -1.57079632679')
gz=sub(r,'gazebo'); sub(gz,'plugin',name='mechanisms',filename='liblunar_mechanisms.so'); d=sub(gz,'plugin',name='drive',filename='libgazebo_ros_diff_drive.so')
for t,v in [('num_wheel_pairs',2),('left_joint','wheel_fl_joint'),('right_joint','wheel_fr_joint'),('left_joint','wheel_rl_joint'),('right_joint','wheel_rr_joint'),('wheel_separation',.75),('wheel_separation',.75),('wheel_diameter',.3048),('wheel_diameter',.3048),('max_wheel_torque',40),('max_wheel_acceleration',.5),('command_topic','cmd_vel'),('odometry_topic','odom'),('odometry_frame','odom'),('robot_base_frame','base_link'),('publish_odom','true'),('publish_odom_tf','true'),('publish_wheel_tf','false')]:txt(d,t,v)
js=sub(gz,'plugin',name='joint_states',filename='libgazebo_ros_joint_state_publisher.so');txt(js,'update_rate',30)
for n in ['wheel_fl_joint','wheel_fr_joint','wheel_rl_joint','wheel_rr_joint','bucket_joint','rear_door_joint','excavator_deploy_joint','conveyor_drive_joint']+['actuator_rod_left_joint','actuator_rod_right_joint','excavator_rod_left_joint','excavator_rod_right_joint']+[f'scoop_{i}_joint' for i in range(7)]:txt(js,'joint_name',n)
g=sub(r,'gazebo',reference='lidar_link');s=sub(g,'sensor',name='lidar',type='ray');txt(s,'update_rate',10)
ray=sub(s,'ray');h=sub(sub(ray,'scan'),'horizontal')
for t,v in [('samples',720),('resolution',1),('min_angle',-3.14159),('max_angle',3.14159)]:txt(h,t,v)
rr=sub(ray,'range')
for t,v in [('min',.1),('max',18),('resolution',.01)]:txt(rr,t,v)
pl=sub(s,'plugin',name='laser',filename='libgazebo_ros_ray_sensor.so');ros=sub(pl,'ros');txt(ros,'remapping','~/out:=scan');txt(pl,'output_type','sensor_msgs/LaserScan');txt(pl,'frame_name','lidar_link')
g=sub(r,'gazebo',reference='camera_link');s=sub(g,'sensor',name='camera',type='camera');txt(s,'update_rate',15);cam=sub(s,'camera');txt(cam,'horizontal_fov',1.4);im=sub(cam,'image')
for t,v in [('width',640),('height',480),('format','R8G8B8')]:txt(im,t,v)
clip=sub(cam,'clip');txt(clip,'near',.05);txt(clip,'far',30)
pl=sub(s,'plugin',name='camera',filename='libgazebo_ros_camera.so');ros=sub(pl,'ros');txt(ros,'namespace','/');txt(pl,'camera_name','camera');txt(pl,'frame_name','camera_optical_frame')
E.indent(r)
(P/'urdf/lunar_hawks.urdf').write_text(E.tostring(r,encoding='unicode'))
for f in (ROOT/'cad/full_rover').glob('*.stl'):shutil.copy(f,P/'meshes'/f.name)
