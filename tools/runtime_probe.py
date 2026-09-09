"""Run only in an isolated simulation ROS domain. Fail on missing data/interlocks."""
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import time
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image, LaserScan, JointState
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool, Float32MultiArray
from geometry_msgs.msg import Twist

out=Path('validation');out.mkdir(exist_ok=True)
log=open(out/'simulation.log','w')
proc=subprocess.Popen(['ros2','launch','lunabotics_description','simulation.launch.py'],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
rclpy.init();n=Node('runtime_probe')
data={};checks=[];snapshots=[]
def receive(key):return lambda m:data.__setitem__(key,m)
for typ,topic,key,qos in [(Image,'/camera/image_raw','camera',qos_profile_sensor_data),(LaserScan,'/scan','scan',qos_profile_sensor_data),(Odometry,'/odom','odom',10),(JointState,'/joint_states','joints',10),(Float32MultiArray,'/simulation/mechanisms','mechanisms',10)]:
    n.create_subscription(typ,topic,receive(key),qos)
flags={'/excavator/enable':False,'/excavator/deploy':False,'/bucket/dump':False,'/bucket/latch_release':False,'/mechanisms/hold':False}
pubs={key:n.create_publisher(Bool,key,10) for key in flags}
drive=n.create_publisher(Twist,'/cmd_vel',10)
velocity=Twist()
def step():
    drive.publish(velocity)
    for key,v in flags.items():pubs[key].publish(Bool(data=v))
    rclpy.spin_once(n,timeout_sec=.08)
    if proc.poll() is not None:raise RuntimeError('Simulation launch exited')
def wait_for(name,predicate,seconds=25):
    until=time.monotonic()+seconds
    while time.monotonic()<until:
        step()
        if predicate():
            checks.append(name)
            snapshots.append({'check':name,'state':list(state()) if 'mechanisms' in data else [],'pose':str(data['odom'].pose.pose) if 'odom' in data else ''})
            return
    raise RuntimeError('Timeout: '+name)
def pause(seconds):
    until=time.monotonic()+seconds
    while time.monotonic()<until:step()
def state():return data['mechanisms'].data
def scoop():
    m=data['joints'];return m.position[list(m.name).index('scoop_0_joint')]
try:
    wait_for('sensor topics and mechanism feedback',lambda:all(k in data for k in ['camera','scan','odom','joints','mechanisms']),90)
    assert data['camera'].width>0 and len(data['scan'].ranges)>100
    assert all(math.isfinite(x) for x in state())
    wait_for('stowed and latched',lambda:state()[0]<-.24 and state()[3]>.5)
    flags['/excavator/enable']=True
    a=scoop();pause(1);assert abs(scoop()-a)<.005,'conveyor ran while stowed'
    checks.append('conveyor inhibited while stowed')
    flags['/excavator/enable']=False;flags['/excavator/deploy']=True
    wait_for('excavator deployed',lambda:state()[0]>-.01)
    flags['/excavator/enable']=True;a=scoop()
    wait_for('scoops move',lambda:abs(scoop()-a)>.05)
    flags['/excavator/enable']=False;pause(.7);a=scoop();pause(.5)
    assert abs(scoop()-a)<.005;checks.append('conveyor stops')
    flags['/excavator/deploy']=False
    wait_for('excavator retracted',lambda:state()[0]<-.24)
    flags['/bucket/dump']=True;pause(1)
    assert state()[1]<.03;checks.append('latch blocks tipping')
    flags['/bucket/latch_release']=True
    wait_for('latch released',lambda:state()[3]<.5)
    wait_for('bucket tipped',lambda:state()[1]>.9)
    wait_for('passive door opened',lambda:state()[2]>.1)
    flags['/bucket/dump']=False
    wait_for('bucket lowered',lambda:state()[1]<.03)
    wait_for('passive door closed',lambda:abs(state()[2])<.04)
    flags['/bucket/latch_release']=False
    wait_for('latch engaged',lambda:state()[3]>.5)
    x=data['odom'].pose.pose.position.x;velocity.linear.x=.05
    until=time.monotonic()+3
    while time.monotonic()<until:step()
    velocity.linear.x=0.;drive.publish(velocity);assert abs(data['odom'].pose.pose.position.x-x)>.02
    checks.append('drive displacement')
    subprocess.run(['import','-window','root',str(out/'gazebo-rviz.png')],check=True)
    # Raise each application separately; Xvfb has no desktop window manager.
    for title, filename in [('Gazebo','gazebo.png'), ('RViz','rviz.png')]:
        search=subprocess.run(['xdotool','search','--onlyvisible','--name',title],
                              text=True,capture_output=True)
        windows=search.stdout.split()
        # Window titles are not deterministic under headless Xvfb. The combined
        # root capture and process/topic checks remain authoritative.
        if not windows:
            continue
        window=windows[-1]
        subprocess.run(['xdotool','windowsize',window,'1400','960'],check=True)
        subprocess.run(['xdotool','windowmove',window,'0','0'],check=True)
        subprocess.run(['xdotool','windowraise',window],check=True)
        pause(1)
        subprocess.run(['import','-window','root',str(out/filename)],check=True)
    text=(out/'simulation.log').read_text()
    assert 'rviz2' in text, 'RViz was not launched'
    assert 'process has died' not in text, 'A simulation process died; inspect log'
    (out/'runtime.json').write_text(json.dumps({'passed':checks,'status':'passed','snapshots':snapshots},indent=2))
except Exception as e:
    subprocess.run(['import','-window','root',str(out/'gazebo-rviz-failure.png')],check=False)
    (out/'runtime.json').write_text(json.dumps({'passed':checks,'status':'failed','error':str(e),'snapshots':snapshots,'received_topics':list(data),'mechanisms':list(state()) if 'mechanisms' in data else []},indent=2))
    raise
finally:
    drive.publish(Twist());pubs['/mechanisms/hold'].publish(Bool(data=True))
    os.killpg(proc.pid,signal.SIGINT)
    try:proc.wait(timeout=10)
    except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL)
    n.destroy_node();rclpy.shutdown();log.close()
