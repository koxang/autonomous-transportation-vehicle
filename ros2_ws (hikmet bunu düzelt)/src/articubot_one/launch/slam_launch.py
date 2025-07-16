from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription([
        # Robot model (URDF + TF + /robot_description)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('articubot_one'),
                    'launch',
                    'rsp.launch.py'
                ])
            ]),
            launch_arguments={'use_sim_time': 'false'}.items()
        ),

        # SLAM toolbox
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[{
                'use_sim_time': False
            },
            PathJoinSubstitution([
                FindPackageShare('articubot_one'),
                'config',
                'mapper_params_online_async.yaml'
            ])]
        )
    ])
