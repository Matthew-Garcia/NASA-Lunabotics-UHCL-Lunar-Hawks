"""Opt-in simulation sequence. No physical hardware mission is authorized by this node."""
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool, Float32, Float32MultiArray, String

class MissionManager(Node):
    def __init__(self):
        super().__init__('mission_manager')
        self.declare_parameter('simulation_mission',False)
        self.state='WAIT'; self.since=self.now();self.safe=False;self.scan_t=-100
        self.goal=[];self.goal_t=-100;self.load=0;self.yaw=None;self.odom_t=-100;self.target_yaw=0
        self.cmd=self.create_publisher(Twist,'/cmd_vel',10)
        self.exc=self.create_publisher(Bool,'/excavator/enable',10)
        self.dump=self.create_publisher(Bool,'/bucket/dump',10)
        self.status=self.create_publisher(String,'/mission/state',10)
        self.create_subscription(Bool,'/safety/obstacle_stop',self.safety,10)
        self.create_subscription(Float32MultiArray,'/vision/goal_posts/target',self.goal_cb,10)
        self.create_subscription(Float32,'/simulation/bucket_load',lambda m:setattr(self,'load',m.data),10)
        self.create_subscription(Odometry,'/odom',self.odometry,10)
        self.create_timer(.1,self.tick)
    def now(self):return self.get_clock().now().nanoseconds*1e-9
    def safety(self,m):self.safe=not m.data;self.scan_t=self.now()
    def goal_cb(self,m):self.goal=list(m.data);self.goal_t=self.now()
    def odometry(self,m):
        q=m.pose.pose.orientation;self.yaw=math.atan2(2*(q.w*q.z+q.x*q.y),1-2*(q.y*q.y+q.z*q.z));self.odom_t=self.now()
    def state_to(self,s):self.state=s;self.since=self.now()
    def tick(self):
        now=self.now();elapsed=now-self.since;v=w=0.;exc=dump=False
        enabled=self.get_parameter('simulation_mission').value and self.get_parameter('use_sim_time').value
        fresh=now-self.scan_t<.5 and now-self.odom_t<.5
        goal=now-self.goal_t<.5 and len(self.goal)==4 and all(math.isfinite(x) for x in self.goal) and self.goal[3]==4
        if not enabled or not fresh or not self.safe:
            # Fault latches; never advance a mission on stale/invalid range data.
            if self.state!='WAIT':self.state_to('FAULT')
        elif self.state=='WAIT':self.state_to('SCAN')
        elif self.state=='SCAN':
            w=.25
            if elapsed>2*math.pi/.25:self.state_to('COLLECT')
        elif self.state=='COLLECT':
            exc=True;v=.04
            if self.load>=4:self.state_to('FIND_GOAL')
            elif elapsed>90:self.state_to('FAULT')
        elif self.state=='FIND_GOAL':
            w=.2
            if goal:self.state_to('APPROACH')
            elif elapsed>40:self.state_to('FAULT')
        elif self.state=='APPROACH':
            if not goal:self.state_to('FIND_GOAL')
            else:
                err=self.goal[0]-.5;w=max(-.25,min(.25,-err*.9));v=.10 if abs(err)<.12 else 0.
                if self.goal[2]>.66 and abs(err)<.04:
                    self.target_yaw=self.yaw+math.pi;self.state_to('TURN_REAR')
        elif self.state=='TURN_REAR':
            e=math.atan2(math.sin(self.target_yaw-self.yaw),math.cos(self.target_yaw-self.yaw));w=max(-.2,min(.2,e))
            if abs(e)<.04:self.state_to('DUMP')
            elif elapsed>25:self.state_to('FAULT')
        elif self.state=='DUMP':
            dump=True
            if elapsed>12:self.state_to('LOWER')
        elif self.state=='LOWER':
            if elapsed>8:self.state_to('DONE')
        if self.state in ['WAIT','FAULT','DONE'] or not fresh or not self.safe:v=w=0.;exc=dump=False
        t=Twist();t.linear.x=float(v);t.angular.z=float(w);self.cmd.publish(t)
        self.exc.publish(Bool(data=exc));self.dump.publish(Bool(data=dump));self.status.publish(String(data=self.state))

def main(args=None):
    rclpy.init(args=args);n=MissionManager()
    try:rclpy.spin(n)
    finally:n.cmd.publish(Twist());n.exc.publish(Bool(data=False));n.dump.publish(Bool(data=False));n.destroy_node();rclpy.shutdown()
