# turtlebot3-yolo-rescuebot

ROS 2 and Gazebo-based TurtleBot3 project for search-and-rescue style simulation with YOLO object detection, patrol behavior, follower logic, and custom environment assets.

## Overview

`turtlebot3-yolo-rescuebot` is a robotics project built for simulation-based development using TurtleBot3, ROS 2, and Gazebo. The repository includes YOLO-based perception, autonomous behavior scripts, utility tools, and a custom search-and-rescue world for testing and experimentation.

The project is designed to support object detection and robot behavior development in a simulated indoor rescue environment.

## Features

- YOLO-based object detection
- ROS 2 integration
- TurtleBot3 simulation workflow
- Custom Gazebo world for search-and-rescue scenarios
- Patrol behavior script
- Smart follower behavior script
- CSV plotting utility for result visualization
- Pretrained and custom model weights

## Repository Structure

```text
turtlebot3-yolo-rescuebot/
├── README.md
├── __init__.py
├── patrol.py
├── plot_csv.py
├── qr_best.pt
├── sar_room_world.sdf
├── setup.py
├── smart_follower.py
├── yolo_node.py
└── yolov8n.pt
File Descriptions
yolo_node.py

ROS 2 node for running YOLO-based object detection.

yolov8n.pt

YOLOv8 nano pretrained weights.

qr_best.pt

Custom trained weights for specific object detection tasks.

smart_follower.py

Behavior script for follower-style robot movement based on target or detection logic.

patrol.py

Behavior script for autonomous patrol movement.

plot_csv.py

Utility script for plotting CSV-based logged results.

sar_room_world.sdf

Custom Gazebo world for indoor search-and-rescue simulation.

setup.py

Python package setup configuration.

__init__.py

Python package initializer.





Requirements

Recommended setup:

Ubuntu 22.04
ROS 2 Humble
Python 3.10 or newer
Gazebo
TurtleBot3 packages
OpenCV
NumPy
Ultralytics YOLO
Installation




Clone the repository into your ROS 2 workspace:

cd ~/tb3_ws/src
git clone https://github.com/Banisankar/turtlebot3-yolo-rescuebot.git
cd ~/tb3_ws
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
Environment Setup




Before running the package, source ROS 2 and your workspace:

source /opt/ros/humble/setup.bash
cd ~/tb3_ws
source install/setup.bash



To check whether the package is visible:

ros2 pkg list | grep my_yolo_system
Running the YOLO Node



Run the detection node after sourcing the workspace:

source /opt/ros/humble/setup.bash
cd ~/tb3_ws
source install/setup.bash
ros2 run my_yolo_system yolo_node
Running Patrol Behavior
source /opt/ros/humble/setup.bash
cd ~/tb3_ws
source install/setup.bash
python3 patrol.py
Running Smart Follower
source /opt/ros/humble/setup.bash
cd ~/tb3_ws
source install/setup.bash
python3 smart_follower.py
Gazebo World



This repository includes a custom Gazebo world file:

sar_room_world.sdf

You can open it with Gazebo using:

gazebo sar_room_world.sdf

Depending on your project setup, this world may also be launched through a ROS 2 launch file.



Plotting Results

To plot CSV results:

python3 plot_csv.py

Make sure the script points to the correct CSV file path before running it.

Build Notes
Ensure all Python dependencies are installed before building.
Make sure model file paths are correct inside the scripts.
If ROS 2 cannot detect the package, rebuild the workspace and source it again.
The ROS 2 package name used in this project is my_yolo_system.
The executable registered in setup.py is yolo_node.
Applications



This project can be used for:

robot perception experiments
object detection in simulation
TurtleBot3-based robotics development
search-and-rescue scenario prototyping
ROS 2 and Gazebo practice
YOLO integration in mobile robotics
