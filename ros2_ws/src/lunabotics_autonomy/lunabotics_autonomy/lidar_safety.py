#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool, Float32

class LidarSafety(Node):
    def __init__(self):
        super().__init__('lidar_safety')
        self.declare_parameter('scan_topic', '/scan')
        self.declare_parameter('stop_distance_m', 0.65)
        self.declare_parameter('slow_distance_m', 1.25)
        self.sub = self.create_subscription(LaserScan, self.get_parameter('scan_topic').value, self.cb, 10)
        self.stop_pub = self.create_publisher(Bool, '/safety/obstacle_stop', 10)
        self.dist_pub = self.create_publisher(Float32, '/safety/front_clearance', 10)
    def cb(self, msg):
        vals=[]
        for i,r in enumerate(msg.ranges):
            a=msg.angle_min+i*msg.angle_increment
            if abs(a) < math.radians(35) and math.isfinite(r) and msg.range_min < r < msg.range_max:
                vals.append(r)
        d=min(vals) if vals else float('inf')
        b=Bool(); b.data=d<float(self.get_parameter('stop_distance_m').value); self.stop_pub.publish(b)
        f=Float32(); f.data=float(d if math.isfinite(d) else msg.range_max); self.dist_pub.publish(f)

def main(args=None):
    rclpy.init(args=args); n=LidarSafety(); rclpy.spin(n); n.destroy_node(); rclpy.shutdown()
if __name__ == '__main__': main()
