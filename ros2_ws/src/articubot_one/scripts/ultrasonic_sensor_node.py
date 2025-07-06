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
        self.publisher_ = self.create_publisher(Range, 'ultrasonic_range', 10)
        self.timer = self.create_timer(0.1, self.read_sensor)  # 10Hz
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)

    def read_sensor(self):
        GPIO.output(TRIG, False)
        time.sleep(0.05)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150.0

        msg = Range()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'ultrasonic_link'
        msg.radiation_type = Range.ULTRASOUND
        msg.field_of_view = 0.3
        msg.min_range = 0.02
        msg.max_range = 4.0
        msg.range = distance / 100.0
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicSensor()
    rclpy.spin(node)
    GPIO.cleanup()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()