#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray, Int32
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import serial
import struct
import math
import time

class HoverboardController(Node):
    def __init__(self):
        super().__init__('hoverboard_controller')

        self.subscription = self.create_subscription(
            Int16MultiArray,
            'manual_drive_topic',
            self.listener_callback,
            10
        )

        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
            self.get_logger().info("UART bağlantısı kuruldu.")
        except Exception as e:
            self.get_logger().error(f"UART bağlantısı kurulamadı: {e}")
            raise

        # Odometri için başlangıç değerleri
        self.x = 0.0
        self.y = 0.0
        self.th = 0.0
        self.last_time = self.get_clock().now()

        self.last_steer = 0
        self.last_speed = 0

        self.create_timer(0.1, self.timer_callback)

    def listener_callback(self, msg: Int16MultiArray):
        self.last_steer = msg.data[0]
        self.last_speed = msg.data[1]

        checksum = (0xABCD ^ self.last_steer ^ self.last_speed) & 0xFFFF
        packet = struct.pack('<HhhH', 0xABCD, self.last_steer, self.last_speed, checksum)
        self.ser.write(packet)

        twist = Twist()
        twist.linear.x = float(self.last_speed) / 100.0
        twist.angular.z = -float(self.last_steer) / 57.0
        self.cmd_vel_pub.publish(twist)

#        self.get_logger().info(f"UART gönderildi: steer={self.last_steer}, speed={self.last_speed}")
 #       self.get_logger().info(f"/cmd_vel: linear.x={twist.linear.x:.2f}, angular.z={twist.angular.z:.2f}")

    def timer_callback(self):
        # Hızdan odometri hesaplama
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time

        vx = float(self.last_speed) / 100.0
        vth = -float(self.last_steer) / 57.0

        delta_x = vx * math.cos(self.th) * dt
        delta_y = vx * math.sin(self.th) * dt
        delta_th = vth * dt

        self.x += delta_x
        self.y += delta_y
        self.th += delta_th

        odom_quat = self.create_quaternion_msg(0, 0, self.th)

        # TF yayınla
        t = TransformStamped()
        t.header.stamp = current_time.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation = odom_quat
        self.tf_broadcaster.sendTransform(t)

        # Odometry mesajı
        odom = Odometry()
        odom.header.stamp = current_time.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = odom_quat

        odom.twist.twist.linear.x = vx
        odom.twist.twist.angular.z = vth

        self.odom_pub.publish(odom)

    def create_quaternion_msg(self, roll, pitch, yaw):
        from tf_transformations import quaternion_from_euler
        q = quaternion_from_euler(roll, pitch, yaw)
        from geometry_msgs.msg import Quaternion
        quat = Quaternion()
        quat.x = q[0]
        quat.y = q[1]
        quat.z = q[2]
        quat.w = q[3]
        return quat

def main(args=None):
    rclpy.init(args=args)
    node = HoverboardController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
