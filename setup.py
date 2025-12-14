import os
from glob import glob

from setuptools import setup

package_name = 'my_yolo_system'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        # Gazebo world(s)
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
        # YOLO model weights
        (os.path.join('share', package_name, 'models'), glob('models/*.pt')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Sathishkumar Banisankar Jabade',
    maintainer_email='jabadesbanisankar@gmail.com',
    description='ROS 2 / Gazebo TurtleBot3 search-and-rescue package with YOLOv8 '
                'detection, Nav2 patrol, and an AprilTag smart-follower.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'yolo_node = my_yolo_system.yolo_node:main',
            'patrol = my_yolo_system.patrol:main',
            'smart_follower = my_yolo_system.smart_follower:main',
            'plot_csv = my_yolo_system.plot_csv:main',
        ],
    },
)
