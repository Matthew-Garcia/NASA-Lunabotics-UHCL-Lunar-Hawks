"""Fail-closed range monitor. It is not a certified hardware emergency stop."""
import math
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool,Float32,String
class LidarSafety(Node):
    def __init__(self):
        super().__init__('lidar_safety');self.last=-100.;self.distance=0.;self.valid=False
        self.usable=0;self.total=0;self.previous_codes=None;self.last_stop='none'
        self.diagnostic=self.create_publisher(String,'/safety/diagnostic',10)
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
        self.usable=usable;self.total=len(m.ranges)
        self.valid=len(m.ranges)>0 and usable>=.8*len(m.ranges)
        self.distance=min(vals) if vals else m.range_max;self.last=self.now()
    def tick(self):
        age=self.now()-self.last;limit=self.get_parameter('stop_distance_m').value
        codes=[]
        if not self.valid:codes.append('INVALID_SCAN')
        if age>.5:codes.append('STALE_SCAN')
        if self.distance<limit:codes.append('NEAR_RETURN')
        bad=bool(codes)
        detail=f'{",".join(codes) or "CLEAR"}: minimum={self.distance:.3f}m; limit={limit:.3f}m; scan_age={age:.3f}s; usable={self.usable}/{self.total}'
        if tuple(codes)!=self.previous_codes:
            if bad:
                self.last_stop=detail
                self.get_logger().warning('LIDAR STOP: '+detail)
            else:self.get_logger().info('LIDAR CLEAR: '+detail)
            self.previous_codes=tuple(codes)
        self.diagnostic.publish(String(data=detail+' | last_stop='+self.last_stop))
        self.stop.publish(Bool(data=bad));self.clear.publish(Float32(data=float(self.distance)))
def main(args=None):
    rclpy.init(args=args);n=LidarSafety();rclpy.spin(n);n.destroy_node();rclpy.shutdown()
