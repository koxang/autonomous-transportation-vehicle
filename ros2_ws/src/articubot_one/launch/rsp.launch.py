import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    use_ros2_control = LaunchConfiguration('use_ros2_control')

    # Xacro dosyasını işliyoruz
    pkg_path = os.path.join(get_package_share_directory('articubot_one'))
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')

    # Burada xacro parametrelerini dict olarak veriyoruz
    doc = xacro.process_file(xacro_file, mappings={
        'use_ros2_control': 'false',   # dilersen LaunchConfig'e bağlayabilirsin
        'sim_mode': 'false'
    })
    robot_description_config = doc.toxml()

    # robot_state_publisher parametreleri
    params = {
        'robot_description': robot_description_config,
        'use_sim_time': use_sim_time,
    }

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params],
    )
    node_joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument(
            'use_ros2_control',
            default_value='false',
            description='Use ros2_control if true'),

        node_robot_state_publisher,
        node_joint_state_publisher

    ])