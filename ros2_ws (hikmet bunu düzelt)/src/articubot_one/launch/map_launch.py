import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Kendi paketinizin yolunu bulun
    pkg_articubot_one = get_package_share_directory('articubot_one')

    # Harita dosyanızın tam yolunu oluşturun
    # 'maps' klasörü ve 'my_map.yaml' adını kendi projenize göre güncelleyin
    map_file_path = os.path.join(
        pkg_articubot_one,
        '/home/rob/ros2_ws/articiubot_one/maps',       # Haritalarınızın bulunduğu klasörün adı
        'okul_s.yaml' # Harita YAML dosyanızın adı
    )

    # RViz konfigürasyon dosyanızın tam yolunu oluşturun
    # 'config' klasörü ve 'view_map.rviz' adını kendi projenize göre güncelleyin
    rviz_config_file_path = os.path.join(
        pkg_articubot_one,
        'config',
        'view_map.rviz' # Bu iş için özel bir RViz konfigürasyon dosyası
    )

    # 1. Map Server Düğümü
    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'yaml_filename': map_file_path}]
    )

    # 2. RViz Düğümü
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file_path]
    )

    return LaunchDescription([
        map_server_node,
        rviz2_node
    ])