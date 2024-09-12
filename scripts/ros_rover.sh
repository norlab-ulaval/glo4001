#!/usr/bin/env bash
export HOME=/home/norlab
source /opt/ros/foxy/setup.bash
source /home/norlab/ros2_ws/install/setup.bash
cd /home/norlab/ros2_ws/ && ros2 launch rover_launchers rover_base_launch.xml