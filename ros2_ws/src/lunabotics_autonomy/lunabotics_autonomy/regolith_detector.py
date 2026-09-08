#!/usr/bin/env python3
"""Simple OpenCV terrain classifier for simulated excavation-zone selection.

It scores the lower half of the image for tan/gray granular-looking regions and publishes
an image-space steering error. This is a baseline; a learned segmentation model is the
recommended later upgrade after real BP-1 data are collected.
"""
import cv2, numpy as np, rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
from cv_bridge import CvBridge
class RegolithDetector(Node):
    def __init__(self):
        super().__init__('regolith_detector'); self.bridge=CvBridge()
        self.sub=self.create_subscription(Image,'/camera/image_raw',self.cb,10)
        self.pub=self.create_publisher(Float32,'/vision/regolith/steering_error',10)
    def cb(self,msg):
        im=self.bridge.imgmsg_to_cv2(msg,'bgr8'); h,w=im.shape[:2]; roi=im[h//2:,:]
        hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        m1=cv2.inRange(hsv,np.array([5,15,45]),np.array([45,180,220]))
        m2=cv2.inRange(hsv,np.array([0,0,40]),np.array([180,55,190]))
        mask=cv2.bitwise_or(m1,m2); M=cv2.moments(mask)
        err=0.0 if M['m00']==0 else ((M['m10']/M['m00'])-w/2)/(w/2)
        out=Float32(); out.data=float(err); self.pub.publish(out)
def main(args=None):
    rclpy.init(args=args); n=RegolithDetector(); rclpy.spin(n); n.destroy_node(); rclpy.shutdown()
if __name__=='__main__': main()
