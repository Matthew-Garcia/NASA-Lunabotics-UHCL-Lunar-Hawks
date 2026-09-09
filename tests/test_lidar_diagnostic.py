"""Reason reporting must retain fail-closed stop behavior."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch
import unittest
class Message:
    def __init__(self,**kw):self.__dict__.update(kw)
class Pub:
    def publish(self,m):self.last=m
class LidarDiagnostic(unittest.TestCase):
    def node(self):
        stubs={'rclpy':NS(),'rclpy.node':NS(Node=object),'rclpy.qos':NS(qos_profile_sensor_data=None),'sensor_msgs.msg':NS(LaserScan=Message),'std_msgs.msg':NS(Bool=Message,Float32=Message,String=Message)}
        p=Path(__file__).resolve().parents[1]/'ros2_ws/src/lunabotics_autonomy/lunabotics_autonomy/lidar_safety.py'
        with patch.dict('sys.modules',stubs):
            spec=importlib.util.spec_from_file_location('lidar_subject',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        n=m.LidarSafety.__new__(m.LidarSafety);n.now=lambda:100.;n.get_parameter=lambda x:NS(value=2 if x=='near_confirm_scans' else .6)
        n.get_logger=lambda:NS(info=lambda x:None,warning=lambda x:None)
        n.stop=Pub();n.clear=Pub();n.diagnostic=Pub();n.previous_codes=None;n.last_stop='none';n.near_count=0
        return n
    def test_invalid_scan_stops_despite_distant_return(self):
        n=self.node();n.cb(Message(ranges=[5.86]+[float('nan')]*9,range_min=.1,range_max=18));n.tick()
        self.assertTrue(n.stop.last.data);self.assertIn('INVALID_SCAN',n.diagnostic.last.data)
    def test_stale_scan_stops_despite_distant_return(self):
        n=self.node();n.cb(Message(ranges=[5.86]*10,range_min=.1,range_max=18));n.last=99;n.tick()
        self.assertTrue(n.stop.last.data);self.assertIn('STALE_SCAN',n.diagnostic.last.data)
    def test_near_stop_reason_retained_after_clear(self):
        n=self.node();n.cb(Message(ranges=[.2]*10,range_min=.1,range_max=18));n.cb(Message(ranges=[.2]*10,range_min=.1,range_max=18));n.tick()
        self.assertTrue(n.stop.last.data)
        n.cb(Message(ranges=[5.86]*10,range_min=.1,range_max=18));n.tick()
        self.assertFalse(n.stop.last.data);self.assertTrue(n.diagnostic.last.data.startswith('CLEAR'))
        self.assertIn('last_stop=NEAR_RETURN',n.diagnostic.last.data)

    def test_single_near_scan_is_not_a_confirmed_stop(self):
        n=self.node();n.cb(Message(ranges=[.2]*10,range_min=.1,range_max=18));n.tick()
        self.assertFalse(n.stop.last.data)
        self.assertIn('PENDING_NEAR_RETURN',n.diagnostic.last.data)
