#this launch file used for launching the essentials for mapping or navigating in Rviz 
#and if you want to launch files seperately than you have to launch or run (for the nodes) the files one by one
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir
import os

def generate_launch_description():
    # Paket dizinlerini bul
    from ament_index_python.packages import get_package_share_directory
    articubot_dir = get_package_share_directory('articubot_one')
    manual_drive_dir = get_package_share_directory('manual_drive')
    nav2_dir = get_package_share_directory('nav2_bringup')

    return LaunchDescription([
        # RSP (publishes the robot state)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(articubot_dir, 'launch', 'rsp.launch.py'))
        ),

        # Lidar 
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(articubot_dir, 'launch', 'rplidar.launch.py'))
        ),

        # Odometry
        Node(
            package='articubot_one',
            executable='odom_publisher.py',
            name='odom_publisher',
            output='screen'
        ),

        # Hoverboard_controller (this file is to control the hoverboard through the messages that come from mobile application)
        Node(
            package='manual_drive',
            executable='hoverboard_controller',
            name='hoverboard_controller',
            output='screen'
        ),

        # cmdvel_hover (this file is used for control the hoverboard through the messages from cmdvel while doing navigation)
        Node(
            package='articubot_one',
            executable='cmdvel_hover.py',
            name='cmdvel_hover',
            output='screen'
        ),

        # Manuel sürüş Flask API node
        Node(
            package='manual_drive',
            executable='manual_drive_node',
            name='manual_drive_node',
            output='screen'
        ),

        # Ultrasonic sensor
        Node(
            package='articubot_one',
            executable='ultrasonic_sensor_node.py',
            name='ultrasonic_sensor',
            output='screen'
        ),
    ])

