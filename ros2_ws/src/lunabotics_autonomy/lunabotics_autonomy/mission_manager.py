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
        self.fault_reason=''
        self.state='WAIT'; self.since=self.now();self.safe=False;self.scan_t=-100
        self.goal=[];self.goal_t=-100;self.load=0;self.yaw=None;self.odom_t=-100;self.target_yaw=0
        self.cmd=self.create_publisher(Twist,'/cmd_vel',10)
        self.exc=self.create_publisher(Bool,'/excavator/enable',10)
        self.dump=self.create_publisher(Bool,'/bucket/dump',10)
        self.deploy=self.create_publisher(Bool,'/excavator/deploy',10)
        self.release=self.create_publisher(Bool,'/bucket/latch_release',10)
        self.hold=self.create_publisher(Bool,'/mechanisms/hold',10)
        self.mechanisms=[];self.mechanisms_t=-100
        self.create_subscription(Float32MultiArray,'/simulation/mechanisms',self.mechanism_cb,10)
        self.status=self.create_publisher(String,'/mission/state',10)
        self.diagnostic=self.create_publisher(String,'/mission/diagnostic',10)
        self.create_subscription(Bool,'/safety/obstacle_stop',self.safety,10)
        self.create_subscription(Float32MultiArray,'/vision/goal_posts/target',self.goal_cb,10)
        self.create_subscription(Float32,'/simulation/bucket_load',lambda m:setattr(self,'load',m.data),10)
        self.create_subscription(Odometry,'/odom',self.odometry,10)
        self.create_timer(.1,self.tick)
    def now(self):return self.get_clock().now().nanoseconds*1e-9
    def safety(self,m):self.safe=not m.data;self.scan_t=self.now()
    def goal_cb(self,m):self.goal=list(m.data);self.goal_t=self.now()
    def mechanism_cb(self,m):
        self.mechanisms=list(m.data);self.mechanisms_t=self.now()
    def odometry(self,m):
        q=m.pose.pose.orientation;self.yaw=math.atan2(2*(q.w*q.z+q.x*q.y),1-2*(q.y*q.y+q.z*q.z));self.odom_t=self.now()
    def state_to(self,s):
        if s != self.state:
            self.get_logger().info(f'Mission {self.state} -> {s}')
        self.state=s;self.since=self.now()
    def fault(self,reason):
        if self.state == 'FAULT':
            return  # Preserve the first cause even after inputs recover.
        self.fault_reason=f'{self.state}: {reason}'
        self.get_logger().error('MISSION FAULT: '+self.fault_reason)
        self.state_to('FAULT')
    def tick(self):
        now=self.now();elapsed=now-self.since;v=w=0.;exc=dump=False
        enabled=self.get_parameter('simulation_mission').value and self.get_parameter('use_sim_time').value
        fresh=now-self.scan_t<.5 and now-self.odom_t<.5 and now-self.mechanisms_t<.5 and len(self.mechanisms)==4 and all(math.isfinite(x) for x in self.mechanisms)
        deployed=fresh and self.mechanisms[0]>-.01
        stowed=fresh and self.mechanisms[0]<-.24
        lowered=fresh and self.mechanisms[1]<.03
        latched=fresh and self.mechanisms[3]>.5
        closed=fresh and abs(self.mechanisms[2])<.04
        goal=now-self.goal_t<.5 and len(self.goal)==4 and all(math.isfinite(x) for x in self.goal) and self.goal[3]==4
        issues=[]
        if not enabled:issues.append('simulation_mission and use_sim_time must both be enabled')
        for name,stamp in [('safety',self.scan_t),('odometry',self.odom_t),('mechanisms',self.mechanisms_t)]:
            age=now-stamp
            if age>=.5:issues.append(f'{name} feedback stale: {age:.3f}s (limit 0.500s)')
        if len(self.mechanisms)!=4 or not all(math.isfinite(x) for x in self.mechanisms):
            issues.append('invalid mechanism feedback: '+str(self.mechanisms))
        if not self.safe:issues.append('obstacle_stop is true or has not arrived')
        if not enabled or not fresh or not self.safe:
            # Fault latches; never advance a mission on stale/invalid range data.
            if self.state!='WAIT':self.fault('; '.join(issues) or 'input freshness check failed')
        elif self.state=='WAIT':
            if stowed and lowered and latched:self.state_to('SCAN')
        elif self.state=='SCAN':
            w=.25
            if elapsed>2*math.pi/.25:self.state_to('DEPLOY')
        elif self.state=='DEPLOY':
            if deployed:self.state_to('COLLECT')
            elif elapsed>12:self.fault(f'phase timeout after {elapsed:.2f}s; mechanisms={self.mechanisms}')
        elif self.state=='COLLECT':
            exc=True;v=.04
            if self.load>=4:self.state_to('STOP_CONVEYOR')
            elif elapsed>90:self.fault(f'phase timeout after {elapsed:.2f}s; mechanisms={self.mechanisms}')
        elif self.state=='STOP_CONVEYOR':
            if elapsed>.5:self.state_to('RETRACT')
        elif self.state=='RETRACT':
            if stowed:self.state_to('FIND_GOAL')
            elif elapsed>12:self.fault(f'phase timeout after {elapsed:.2f}s; mechanisms={self.mechanisms}')
        elif self.state=='FIND_GOAL':
            w=.2
            if goal:self.state_to('APPROACH')
            elif elapsed>40:self.fault(f'phase timeout after {elapsed:.2f}s; mechanisms={self.mechanisms}')
        elif self.state=='APPROACH':
            if not goal:self.state_to('FIND_GOAL')
            else:
                err=self.goal[0]-.5;w=max(-.25,min(.25,-err*.9));v=.10 if abs(err)<.12 else 0.
                if self.goal[2]>.66 and abs(err)<.04:
                    self.target_yaw=self.yaw+math.pi;self.state_to('TURN_REAR')
        elif self.state=='TURN_REAR':
            e=math.atan2(math.sin(self.target_yaw-self.yaw),math.cos(self.target_yaw-self.yaw));w=max(-.2,min(.2,e))
            if abs(e)<.04:self.state_to('UNLATCH')
            elif elapsed>25:self.fault(f'phase timeout after {elapsed:.2f}s; mechanisms={self.mechanisms}')
        elif self.state=='UNLATCH':
            if not latched:self.state_to('DUMP')
            elif elapsed>4:self.fault(f'phase timeout after {elapsed:.2f}s; mechanisms={self.mechanisms}')
        elif self.state=='DUMP':
            dump=True
            if elapsed>12:self.state_to('LOWER')
        elif self.state=='LOWER':
            if lowered:self.state_to('CLOSE_DOOR')
            elif elapsed>12:self.fault(f'phase timeout after {elapsed:.2f}s; mechanisms={self.mechanisms}')
        elif self.state=='CLOSE_DOOR':
            if closed:self.state_to('RELATCH')
            elif elapsed>10:self.fault(f'phase timeout after {elapsed:.2f}s; mechanisms={self.mechanisms}')
        elif self.state=='RELATCH':
            if latched:self.state_to('DONE')
            elif elapsed>4:self.fault(f'phase timeout after {elapsed:.2f}s; mechanisms={self.mechanisms}')
        deploy=self.state in ['DEPLOY','COLLECT','STOP_CONVEYOR']
        release=self.state in ['UNLATCH','DUMP','LOWER','CLOSE_DOOR']
        exc=exc and self.state=='COLLECT' and deployed and lowered and latched
        dump=self.state=='DUMP' and stowed and not latched
        if self.state not in ['SCAN','COLLECT','FIND_GOAL','APPROACH','TURN_REAR']:v=w=0.
        if self.state in ['FIND_GOAL','APPROACH','TURN_REAR','SCAN'] and not (stowed and lowered and latched):self.fault(f'travel interlock: stowed={stowed}, lowered={lowered}, latched={latched}; mechanisms={self.mechanisms}')
        if self.state in ['WAIT','FAULT','DONE'] or not fresh or not self.safe:v=w=0.;exc=dump=False
        detail=self.fault_reason if self.state=='FAULT' else ('; '.join(issues) or ('waiting for stowed excavator, lowered bucket and engaged latch' if self.state=='WAIT' else self.state))
        self.diagnostic.publish(String(data=detail))
        t=Twist();t.linear.x=float(v);t.angular.z=float(w);self.cmd.publish(t)
        self.exc.publish(Bool(data=exc));self.dump.publish(Bool(data=dump));self.status.publish(String(data=self.state))
        self.deploy.publish(Bool(data=deploy));self.release.publish(Bool(data=release))
        self.hold.publish(Bool(data=self.state in ['WAIT','FAULT','DONE'] or not fresh or not self.safe or not enabled))

def main(args=None):
    rclpy.init(args=args);n=MissionManager()
    try:rclpy.spin(n)
    finally:n.cmd.publish(Twist());n.exc.publish(Bool(data=False));n.hold.publish(Bool(data=True));n.destroy_node();rclpy.shutdown()
