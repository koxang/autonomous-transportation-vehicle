#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16MultiArray

class CmdVelToHover(Node):
    def __init__(self):
        super().__init__('cmdvel_hover')
        self.subscription = self.create_subscription(Twist, '/cmd_vel', self.cmdvel_callback, 10)
        self.publisher = self.create_publisher(Int16MultiArray, 'manual_drive_topic', 10)
        self.get_logger().info('cmdvel_hover düğümü başlatıldı.')

    def cmdvel_callback(self, msg: Twist):
        speed = int(msg.linear.x * 100)         # 0.25 m/s → 25
        steer = int(-msg.angular.z * 57)        # 1.0 rad/s → -30
        out = Int16MultiArray()
        out.data = [steer, speed]
        self.publisher.publish(out)
        self.get_logger().info(f"Alındı: lin.x={msg.linear.x:.2f}, ang.z={msg.angular.z:.2f} → steer={steer}, speed={speed}")

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelToHover()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()