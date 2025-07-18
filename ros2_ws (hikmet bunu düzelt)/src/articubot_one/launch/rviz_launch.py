from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="rviz2",
            executable="rviz2",
            name="rviz2",
            output="screen"
        ),
        Node(
            package="nav2_map_server",
            executable="map_server",
            name="map_server",
            parameters=[{
                "yaml_filename": "/home/rob/ros2_ws/ozanv1.yaml"
            }],
            output="screen"
        )
    ])