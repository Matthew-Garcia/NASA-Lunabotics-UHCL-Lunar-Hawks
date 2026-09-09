"""Gazebo regression: start autonomy after the simulation clock is already running."""
import json,math,os,signal,subprocess,time
from pathlib import Path
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import String
out=Path('validation');out.mkdir(exist_ok=True)
log=open(out/'autonomy-start.log','w');processes=[]
def launch(args):
 p=subprocess.Popen(args,stdout=log,stderr=subprocess.STDOUT,start_new_session=True);processes.append(p);return p
rclpy.init();n=Node('autonomy_start_probe');data={};states=[];rotation=0.;previous=None
n.create_subscription(String,'/mission/diagnostic',lambda m:data.__setitem__('diagnostic',m.data),10)
n.create_subscription(String,'/safety/diagnostic',lambda m:data.__setitem__('safety',m.data),10)
def state(m):
 data['state']=m.data
 if not states or states[-1]!=m.data:states.append(m.data)
def odom(m):
 global previous,rotation
 q=m.pose.pose.orientation;yaw=math.atan2(2*(q.w*q.z+q.x*q.y),1-2*(q.y*q.y+q.z*q.z))
 if previous is not None and data.get('state')=='SCAN':rotation+=abs(math.atan2(math.sin(yaw-previous),math.cos(yaw-previous)))
 previous=yaw;data['odom_stamp']=m.header.stamp.sec+m.header.stamp.nanosec*1e-9
n.create_subscription(String,'/mission/state',state,10);n.create_subscription(Odometry,'/odom',odom,10)
status='failed';error=''
try:
 launch(['ros2','launch','lunabotics_description','simulation.launch.py'])
 deadline=time.monotonic()+90
 while data.get('odom_stamp',0)<3:
  rclpy.spin_once(n,timeout_sec=.1)
  if time.monotonic()>deadline:raise RuntimeError('No running simulator odometry')
 launch(['ros2','launch','lunabotics_autonomy','autonomy.launch.py'])
 deadline=time.monotonic()+150
 while time.monotonic()<deadline:
  rclpy.spin_once(n,timeout_sec=.1)
  if data.get('state')=='FAULT':
   until=time.monotonic()+.5
   while time.monotonic()<until:rclpy.spin_once(n,timeout_sec=.05)
   raise RuntimeError(str(data))
  if data.get('state')=='DEPLOY':
   assert 'SCAN' in states and rotation>1.,f'No actual scan rotation: {rotation}'
   status='passed';break
 else:raise RuntimeError('Did not reach DEPLOY: '+str(data))
except Exception as e:
 error=str(e);raise
finally:
 (out/'autonomy-start.json').write_text(json.dumps({'status':status,'error':error,'states':states,'scan_rotation_rad':rotation,'last_data':data},indent=2))
 for p in reversed(processes):
  if p.poll() is None:
   os.killpg(p.pid,signal.SIGINT)
   try:p.wait(timeout=10)
   except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL)
 n.destroy_node()
 if rclpy.ok():rclpy.shutdown()
 log.close()
