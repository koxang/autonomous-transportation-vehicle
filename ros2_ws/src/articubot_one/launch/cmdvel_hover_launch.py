from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='articubot_one',
            executable='cmdvel_hover',
            name='cmdvel_hover',
            output='screen'
        )
    ])