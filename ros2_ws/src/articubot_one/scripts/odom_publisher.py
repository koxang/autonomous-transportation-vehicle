#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, TransformStamped
from std_msgs.msg import Int32
from tf2_ros import TransformBroadcaster
import math
import time

WHEEL_RADIUS = 0.083  # 6 cm
ENCODER_RESOLUTION = 4096  # 6 bit = 64 adım
WHEEL_BASE = 0.41    # Tekerlekler arası mesafe (metre)

class OdomPublisher(Node):
    def __init__(self):
        super().__init__('odom_publisher')
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.left_encoder_sub = self.create_subscription(Int32, 'left_encoder', self.left_callback, 10)
        self.right_encoder_sub = self.create_subscription(Int32, 'right_encoder', self.right_callback, 10)

        self.last_left = None
        self.last_right = None

        self.x = 0.0
        self.y = 0.0
        self.th = 0.0

        self.last_time = self.get_clock().now()

        self.left_ticks = 0
        self.right_ticks = 0

        self.timer = self.create_timer(0.05, self.update_odometry)  # 20 Hz

    def left_callback(self, msg):
        self.left_ticks = msg.data

    def right_callback(self, msg):
        self.right_ticks = msg.data

    def update_odometry(self):
        current_time = self.get_clock().now()

        if self.last_left is None or self.last_right is None:
            self.last_left = self.left_ticks
            self.last_right = self.right_ticks
            return

        delta_left = self.left_ticks - self.last_left
        delta_right = self.right_ticks - self.last_right

        # Güncel encoder değerlerini sakla
        self.last_left = self.left_ticks
        self.last_right = self.right_ticks

        # Tekerleklerin kat ettiği mesafe (her adım 2πR/64 metre)
        left_dist = (2 * math.pi * WHEEL_RADIUS * delta_left) / ENCODER_RESOLUTION
        right_dist = (2 * math.pi * WHEEL_RADIUS * delta_right) / ENCODER_RESOLUTION

        # Ortalama ilerleme ve yön değişimi
        delta_s = (left_dist + right_dist) / 2.0
        delta_th = (right_dist - left_dist) / WHEEL_BASE

        dt = (current_time - self.last_time).nanoseconds / 1e9

        # Yeni pozisyon hesapla
        self.x += delta_s * math.cos(self.th + delta_th / 2.0)
        self.y += delta_s * math.sin(self.th + delta_th / 2.0)
        self.th += delta_th

        q = self.quaternion_from_euler(0, 0, self.th)

        # TF yayınla
        t = TransformStamped()
        t.header.stamp = current_time.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        self.tf_broadcaster.sendTransform(t)

        # Odometry mesajı
        odom = Odometry()
        odom.header.stamp = current_time.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_footprint'
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]
        odom.twist.twist.linear.x = delta_s / dt
        odom.twist.twist.angular.z = delta_th / dt

        self.odom_pub.publish(odom)

        self.last_time = current_time

    def quaternion_from_euler(self, roll, pitch, yaw):
        """Euler açılarını quaterniona çevir."""
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - \
             math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + \
             math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - \
             math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + \
             math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        return [qx, qy, qz, qw]

def main(args=None):
    rclpy.init(args=args)
    node = OdomPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()