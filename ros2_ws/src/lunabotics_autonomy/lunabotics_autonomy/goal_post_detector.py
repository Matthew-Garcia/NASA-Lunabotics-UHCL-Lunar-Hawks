#!/usr/bin/env python3
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray, Int32
from cv_bridge import CvBridge

class GoalPostDetector(Node):
    """Detect four tall goal posts and publish image-space target center.

    Assumption for simulation: goal posts are bright/gray vertical structures. For the
    physical arena, tune HSV thresholds from actual competition lighting or replace
    this stage with AprilTags/colored fiducials if permitted.
    """
    def __init__(self):
        super().__init__('goal_post_detector')
        self.declare_parameter('camera_topic', '/camera/image_raw')
        self.declare_parameter('min_area_px', 350.0)
        self.declare_parameter('min_aspect_ratio', 2.0)
        self.declare_parameter('max_aspect_ratio', 12.0)
        self.declare_parameter('hsv_low', [95, 100, 70])
        self.declare_parameter('hsv_high', [135, 255, 255])
        topic = self.get_parameter('camera_topic').value
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, topic, self.cb, qos_profile_sensor_data)
        self.pub_target = self.create_publisher(Float32MultiArray, '/vision/goal_posts/target', 10)
        self.pub_count = self.create_publisher(Int32, '/vision/goal_posts/count', 10)
        self.pub_debug = self.create_publisher(Image, '/vision/goal_posts/debug', 10)

    def cb(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        low = np.array(self.get_parameter('hsv_low').value, dtype=np.uint8)
        high = np.array(self.get_parameter('hsv_high').value, dtype=np.uint8)
        mask = cv2.inRange(hsv, low, high)
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        candidates = []
        min_area = float(self.get_parameter('min_area_px').value)
        amin = float(self.get_parameter('min_aspect_ratio').value)
        amax = float(self.get_parameter('max_aspect_ratio').value)
        for c in contours:
            area = cv2.contourArea(c)
            if area < min_area: continue
            x,y,w,h = cv2.boundingRect(c)
            if w <= 0: continue
            aspect = h / float(w)
            if amin <= aspect <= amax and h > w:
                candidates.append((x,y,w,h,area))
        candidates = sorted(candidates, key=lambda q: q[4], reverse=True)[:4]
        candidates = sorted(candidates, key=lambda q: q[0])
        for x,y,w,h,_ in candidates:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        count = Int32(); count.data = len(candidates); self.pub_count.publish(count)
        if not candidates:
            self.pub_target.publish(Float32MultiArray(data=[]))
        if candidates:
            centers = np.array([[x+w/2.0, y+h/2.0] for x,y,w,h,_ in candidates])
            cx, cy = centers.mean(axis=0)
            span = (max(x+w for x,y,w,h,_ in candidates) - min(x for x,y,w,h,_ in candidates)) / frame.shape[1]
            out = Float32MultiArray()
            out.data = [float(cx/frame.shape[1]), float(cy/frame.shape[0]), float(span), float(len(candidates))]
            self.pub_target.publish(out)
            cv2.circle(frame, (int(cx), int(cy)), 8, (0,0,255), -1)
        self.pub_debug.publish(self.bridge.cv2_to_imgmsg(frame, encoding='bgr8'))

def main(args=None):
    rclpy.init(args=args); n=GoalPostDetector(); rclpy.spin(n); n.destroy_node(); rclpy.shutdown()
if __name__ == '__main__': main()
