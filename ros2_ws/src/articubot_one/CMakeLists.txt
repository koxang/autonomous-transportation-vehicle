cmake_minimum_required(VERSION 3.5)
project(articubot_one)

# C standartları
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Bağımlılıklar
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)

# Python dosyalarını kur
install(
  PROGRAMS
    scripts/cmdvel_hover.py
    scripts/odom_publisher.py
    scripts/ultrasonic_sensor_node.py
  DESTINATION lib/${PROJECT_NAME}
)

# Konfigürasyon, URDF, launch dosyaları vs.
install(
  DIRECTORY config description launch worlds
  DESTINATION share/${PROJECT_NAME}
)

# Testler
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()