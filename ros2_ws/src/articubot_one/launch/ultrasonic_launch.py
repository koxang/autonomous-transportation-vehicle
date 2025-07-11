from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='articubot_one',
            executable='ultrasonic_sensor_node',
            name='ultrasonic_sensor_node',
            output='screen'
        )
    ])