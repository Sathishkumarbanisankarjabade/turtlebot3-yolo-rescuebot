"""Launch the YOLO detection node from this package.

This launches only the perception node owned by ``my_yolo_system``. Bring up
TurtleBot3 + the SAR world + Nav2 separately (see the README), then start this
launch file to run detection on the ``/camera/image_raw`` topic.

Example:
    ros2 launch my_yolo_system detection.launch.py
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    yolo_node = Node(
        package='my_yolo_system',
        executable='yolo_node',
        name='qr_scanner_node',
        output='screen',
    )

    return LaunchDescription([yolo_node])
