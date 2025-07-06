import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/rob/ros2_ws/src/manual_drive/install/manual_drive'
