"""Fail-closed range monitor. It is not a certified hardware emergency stop."""
import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool,Float32
class LidarSafety(Node):
    def __init__(self):
        super().__init__('lidar_safety');self.last=-100.;self.distance=0.;self.valid=False
        self.declare_parameter('stop_distance_m',.6)
        self.create_subscription(LaserScan,'/scan',self.cb,qos_profile_sensor_data)
        self.stop=self.create_publisher(Bool,'/safety/obstacle_stop',10)
        self.clear=self.create_publisher(Float32,'/safety/front_clearance',10)
        self.create_timer(.1,self.tick)
    def now(self):return self.get_clock().now().nanoseconds*1e-9
    def cb(self,m):
        vals=[r for r in m.ranges if math.isfinite(r) and m.range_min<=r<=m.range_max]
        # All-around monitoring protects turns and rear-facing bucket operations.
        usable=sum(math.isfinite(r) and m.range_min<=r<=m.range_max or r==float('inf') for r in m.ranges)
        self.valid=len(m.ranges)>0 and usable>=.8*len(m.ranges)
        self.distance=min(vals) if vals else m.range_max;self.last=self.now()
    def tick(self):
        bad=not self.valid or self.now()-self.last>.5 or self.distance<self.get_parameter('stop_distance_m').value
        self.stop.publish(Bool(data=bad));self.clear.publish(Float32(data=float(self.distance)))
def main(args=None):
    rclpy.init(args=args);n=LidarSafety();rclpy.spin(n);n.destroy_node();rclpy.shutdown()
