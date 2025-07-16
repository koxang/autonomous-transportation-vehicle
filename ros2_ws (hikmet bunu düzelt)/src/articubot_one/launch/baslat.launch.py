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
        # RSP başlat
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(articubot_dir, 'launch', 'rsp.launch.py'))
        ),

        # Lidar başlat
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(articubot_dir, 'launch', 'rplidar.launch.py'))
        ),

        # Odometri yayını
        Node(
            package='articubot_one',
            executable='odom_publisher.py',
            name='odom_publisher',
            output='screen'
        ),

        # Hoverboard kontrolü
        Node(
            package='manual_drive',
            executable='hoverboard_controller',
            name='hoverboard_controller',
            output='screen'
        ),

        # cmd_vel dinleyicisi (kullanıyorsan)
        Node(
            package='articubot_one',
            executable='cmdvel_hover.py',
            name='cmdvel_hover',
            output='screen'
        ),

        # Manuel sürüş Flask API düğümü
        Node(
            package='manual_drive',
            executable='manual_drive_node',
            name='manual_drive_node',
            output='screen'
        ),

        # Ultrasonik sensör
        Node(
            package='articubot_one',
            executable='ultrasonic_sensor_node.py',
            name='ultrasonic_sensor',
            output='screen'
        ),
    ])

