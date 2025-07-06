import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16MultiArray

class CmdVelToManualDrive(Node):
    def __init__(self):
        super().__init__('cmdvel_to_manualdrive')

        # Subscriber to /cmd_vel
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10)

        # Publisher to manual_drive_topic (Int16MultiArray)
        self.publisher_ = self.create_publisher(Int16MultiArray, 'manual_drive_topic', 10)

    def cmd_vel_callback(self, msg: Twist):
        # Gelen linear.x ve angular.z değerlerini speed ve steer'a çevir

        # Örneğin:
        # speed = linear.x * 100 (orantı, ihtiyacına göre ayarla)
        # steer = -angular.z * 30 (senin mevcut koduna göre)

        speed = int(msg.linear.x * 100)
        steer = int(-msg.angular.z * 30)

        # Sınır kontrolü (isteğe bağlı)
        if speed > 127:
            speed = 127
        elif speed < -127:
            speed = -127

        if steer > 127:
            steer = 127
        elif steer < -127:
            steer = -127

        # Mesaj oluştur
        out_msg = Int16MultiArray()
        out_msg.data = [steer, speed]

        # Yayınla
        self.publisher_.publish(out_msg)

        self.get_logger().info(f"Converted /cmd_vel to steer={steer}, speed={speed}")

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelToManualDrive()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()