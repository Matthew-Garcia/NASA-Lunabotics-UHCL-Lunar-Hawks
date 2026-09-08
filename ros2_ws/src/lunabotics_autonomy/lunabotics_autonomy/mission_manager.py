#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool, Float32, Float32MultiArray, Int32

class MissionManager(Node):
    """Compact mission state machine for supervised autonomy experiments.

    ENTER -> SEARCH_REGOLITH -> EXCAVATE -> SEARCH_GOAL -> ALIGN_GOAL -> DUMP -> DONE

    Actuator outputs are std_msgs/Bool so they can be bridged later to the existing
    ESP32/micro-ROS interfaces without changing the perception code.
    """
    def __init__(self):
        super().__init__('mission_manager')
        self.state='ENTER'; self.state_t=time.monotonic(); self.stop=False; self.reg_err=0.0; self.goal=None; self.goal_count=0
        self.cmd=self.create_publisher(Twist,'/cmd_vel',10)
        self.exc=self.create_publisher(Bool,'/excavator/enable',10)
        self.dump=self.create_publisher(Bool,'/bucket/dump',10)
        self.status=self.create_publisher(Int32,'/mission/state_code',10)
        self.create_subscription(Bool,'/safety/obstacle_stop',lambda m:setattr(self,'stop',m.data),10)
        self.create_subscription(Float32,'/vision/regolith/steering_error',lambda m:setattr(self,'reg_err',m.data),10)
        self.create_subscription(Float32MultiArray,'/vision/goal_posts/target',self.goal_cb,10)
        self.create_subscription(Int32,'/vision/goal_posts/count',lambda m:setattr(self,'goal_count',m.data),10)
        self.timer=self.create_timer(0.1,self.tick)
    def goal_cb(self,m): self.goal=list(m.data)
    def set_state(self,s): self.state=s; self.state_t=time.monotonic(); self.get_logger().info('STATE -> '+s)
    def drive(self,v,w):
        t=Twist(); t.linear.x=0.0 if self.stop and v>0 else float(v); t.angular.z=float(w); self.cmd.publish(t)
    def boolpub(self,p,val): m=Bool(); m.data=bool(val); p.publish(m)
    def tick(self):
        elapsed=time.monotonic()-self.state_t
        codes={'ENTER':0,'SEARCH_REGOLITH':1,'EXCAVATE':2,'SEARCH_GOAL':3,'ALIGN_GOAL':4,'DUMP':5,'DONE':6}
        sm=Int32(); sm.data=codes[self.state]; self.status.publish(sm)
        if self.state=='ENTER':
            self.drive(0.18,0.0)
            if elapsed>6.0: self.set_state('SEARCH_REGOLITH')
        elif self.state=='SEARCH_REGOLITH':
            self.drive(0.10,-0.35*self.reg_err)
            if elapsed>8.0: self.set_state('EXCAVATE')
        elif self.state=='EXCAVATE':
            self.boolpub(self.exc,True); self.drive(0.055,0.0)
            if elapsed>12.0: self.boolpub(self.exc,False); self.set_state('SEARCH_GOAL')
        elif self.state=='SEARCH_GOAL':
            self.drive(0.0,0.28)
            if self.goal_count>=4 and self.goal: self.set_state('ALIGN_GOAL')
        elif self.state=='ALIGN_GOAL':
            if not self.goal: self.set_state('SEARCH_GOAL'); return
            x=self.goal[0]; span=self.goal[2]
            err=x-0.5
            self.drive(0.08 if span<0.55 else 0.0,-0.8*err)
            if abs(err)<0.06 and span>=0.50: self.set_state('DUMP')
        elif self.state=='DUMP':
            self.drive(0.0,0.0); self.boolpub(self.dump,True)
            if elapsed>5.0: self.boolpub(self.dump,False); self.set_state('DONE')
        else: self.drive(0.0,0.0)

def main(args=None):
    rclpy.init(args=args); n=MissionManager(); rclpy.spin(n); n.destroy_node(); rclpy.shutdown()
if __name__=='__main__': main()
