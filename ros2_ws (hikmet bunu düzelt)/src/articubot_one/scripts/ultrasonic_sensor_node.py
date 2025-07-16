#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

class UltrasonicSensor(Node):
    def __init__(self):
        super().__init__('ultrasonic_sensor')
        self.publisher_ = self.create_publisher(Range, 'range', 10)  # NAV2 uyumlu topic
        self.timer = self.create_timer(1.0, self.read_sensor)  # 1 Hz

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
        GPIO.output(TRIG, False)
        self.get_logger().info("Ultrasonic node initialized")

    def read_sensor(self):
#        self.get_logger().info("read_sensor çağrıldı")  # Test logu

        distances = []
        for _ in range(5):  # 5 ölçüm yap, ortalama al
            # Trigger pulse
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            # Timeout süresi
            timeout = time.time() + 0.05  # 50 ms max bekleme

            # ECHO HIGH başlamasını bekle
            while GPIO.input(ECHO) == 0:
                if time.time() > timeout:
 #                   self.get_logger().warn("ECHO start timeout")
                    return
            pulse_start = time.time()

            # ECHO HIGH bitmesini bekle
            while GPIO.input(ECHO) == 1:
                if time.time() > timeout:
  #                  self.get_logger().warn("ECHO end timeout")
                    return
            pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance_cm = pulse_duration * 17150.0
            distances.append(distance_cm)
            time.sleep(0.01)  # Ölçümler arası kısa bekleme

        avg_distance = sum(distances) / len(distances)

        msg = Range()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'ultrasonic_link'
        msg.radiation_type = Range.ULTRASOUND
        msg.field_of_view = 0.3
        msg.min_range = 0.02
        msg.max_range = 4.0
        msg.range = avg_distance / 100.0  # m cinsine dönüştür

        self.publisher_.publish(msg)
      

def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicSensor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        GPIO.cleanup()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
