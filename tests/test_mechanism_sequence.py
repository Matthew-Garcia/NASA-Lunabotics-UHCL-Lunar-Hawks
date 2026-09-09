"""Exercise mission interlocks with message stubs; not Gazebo runtime coverage."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch
class Message:
    def __init__(self,**kw):self.__dict__.update(kw)
class Twist:
    def __init__(self):self.linear=NS(x=0.);self.angular=NS(z=0.)
class Publisher:
    def publish(self,m):self.last=m
def manager(state,positions,elapsed=1):
    stubs={'rclpy':NS(),'rclpy.node':NS(Node=object),'geometry_msgs.msg':NS(Twist=Twist),'nav_msgs.msg':NS(Odometry=Message),'std_msgs.msg':NS(Bool=Message,Float32=Message,Float32MultiArray=Message,String=Message)}
    path=Path(__file__).resolve().parents[1]/'ros2_ws/src/lunabotics_autonomy/lunabotics_autonomy/mission_manager.py'
    with patch.dict('sys.modules',stubs):
        spec=importlib.util.spec_from_file_location('mission_test_subject',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    n=mod.MissionManager.__new__(mod.MissionManager)
    n.now=lambda:100.;n.get_parameter=lambda name:NS(value=True)
    n.state=state;n.since=100.-elapsed;n.scan_t=n.odom_t=n.mechanisms_t=100.;n.safe=True;n.mechanisms=positions;n.goal_t=-100.;n.goal=[];n.load=0;n.yaw=0.;n.target_yaw=0.
    for name in ['cmd','exc','dump','status','deploy','release','hold']:setattr(n,name,Publisher())
    return n
class MechanismSequence(unittest.TestCase):
    def test_wait_for_deployment(self):
        n=manager('DEPLOY',[-.15,0,0,1]);n.tick()
        self.assertEqual(n.state,'DEPLOY');self.assertFalse(n.exc.last.data);self.assertTrue(n.deploy.last.data)
    def test_stop_before_retraction(self):
        n=manager('COLLECT',[0,0,0,1]);n.load=4;n.tick()
        self.assertEqual(n.state,'STOP_CONVEYOR');self.assertFalse(n.exc.last.data);self.assertEqual(n.cmd.last.linear.x,0.)
    def test_wait_for_latch_release(self):
        n=manager('UNLATCH',[-.25,0,0,1]);n.tick()
        self.assertTrue(n.release.last.data);self.assertFalse(n.dump.last.data)
    def test_never_latch_open_door(self):
        n=manager('CLOSE_DOOR',[-.25,0,.6,0]);n.tick()
        self.assertEqual(n.state,'CLOSE_DOOR');self.assertTrue(n.release.last.data)
    def test_timeout_holds_mechanisms(self):
        n=manager('DEPLOY',[-.15,0,0,1],elapsed=15);n.tick()
        self.assertEqual(n.state,'FAULT');self.assertTrue(n.hold.last.data)
    def test_stale_feedback_holds_mechanisms(self):
        n=manager('DUMP',[-.25,.5,.5,0]);n.mechanisms_t=98;n.tick()
        self.assertEqual(n.state,'FAULT');self.assertTrue(n.hold.last.data);self.assertFalse(n.dump.last.data)
    def test_travel_requires_stowed_excavator(self):
        n=manager('FIND_GOAL',[0,0,0,1]);n.tick()
        self.assertEqual(n.state,'FAULT');self.assertEqual(n.cmd.last.angular.z,0.)
