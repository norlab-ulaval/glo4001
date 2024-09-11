# Installation Jetson Orin

## Design III

Flashing:

1. **Warning before flashing:** You need to use a USB 2.0 port on your host computer. You will receive a Failed message by the SDK Manager if you use a 3.0 port. Also, you need to put the Jetson Orin Nano in recovery mode. To do so, you unplug the power and add a jumper on the pin 9 and 10 of the J14 connector. These pins are under the fan. They are identified as *GND* and *FCREC.* If you are not in recovery mode, the SDK Manager won’t detect your device. The SDK version you install cannot be 6.0.0. We suggest 5.12  
2. Follow the *Software Configuration* steps in: [https://www.waveshare.com/wiki/Jetson\_Orin\_Nano](https://www.waveshare.com/wiki/Jetson_Orin_Nano)

Installation:

1. Accept license terms  
2. Choose language: English  
3. Choose keyboard layout: English (US)  
4. Do not connect to a wifi network  
5. Choose timezone: Toronto  
6. Fill personal information: robmob, robmob  
   1. Name: robmob  
   2. Computer’s name: robmob-orin  
   3. Password: robmob  
   4. Require password to login  
7. Do not install Chromium  
8. Login  
9. Select “No, don’t send system info”  
10. Disable location services  
11. Connect Orin to ethernet  
12. Open a terminal  
13. sudo apt update  
14. sudo apt upgrade  
15. sudo snap refresh  
16. sudo apt install software-properties-common  
17. sudo add-apt-repository universe  
18. sudo apt update && sudo apt install curl \-y  
19. sudo apt install python3-pip  
20. In the network settings, add a wired connection:  
    1. Name: Internet  
    2. Mac address: eth0  
    3. IPV4:  
       1. IPV4 Method: Automatic  
       2. DNS: Automatic  
       3. Routes: Automatic  
21. Create hotspot  
    1. In terminal, write:c  
    2. In GUI:  
       1. Add connection (Add icon in bottom left)  
       2. Select wifi  
       3. Connection name: hotspot  
       4. SSID: robmob-wifi  
       5. Mode: Hotspot  
       6. Device: wlan0  
       7. In IPV4 Settings:  
          1. Add new address  
             1. Address: 192.168.0.10\<team\_id\> (example: 192.168.0.105 for team 5\)  
             2. Netmask: 255.255.255.0  
             3. Gateway: 192.168.0.1  
22. sudo chmod 777 /dev/ttyUSB0  
23. sudo chmod 777 /dev/ttyUSB1  
24. echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules  
25. sudo udevadm control \--reload-rules && sudo udevadm trigger

\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#\#

26. Sensor’s driver installations  
    1. Camera ([https://docs.luxonis.com/projects/api/en/latest/samples/host\_side/opencv\_support/](https://docs.luxonis.com/projects/api/en/latest/samples/host_side/opencv_support/))  
       1. In /home/robmob/ create folder: repos  
       2. In the repos folder:  
          1. git clone [https://github.com/luxonis/depthai-python.git](https://github.com/luxonis/depthai-python.git)  
          2. cd depthai-python/examples  
          3. echo "export OPENBLAS\_CORETYPE=ARMV8" \>\> \~/.bashrc && source \~/.bashrc  
          4. python3 install\_requirements.py  
          5. echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7",   
             MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules  
             sudo udevadm control \--reload-rules && sudo udevadm trigger  
    2. Lidar ()  
27. You need to give right permission for the USB ports related to the lidar and the low-level computer  
    1. sudo chmod 777 /dev/\<port name\> (example: sudo chmod 777 /dev/ttyUSB0)  
28. ROS Related:  
    1. sudo curl \-sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \-o /usr/share/keyrings/ros-archive-keyring.gpg  
    2. echo "deb \[arch=$(dpkg \--print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg\] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU\_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list \> /dev/null  
    3. sudo apt update  
    4. sudo apt upgrade  
    5. sudo apt install ros-foxy-ros-base python3-argcomplete  
    6. sudo apt install ros-dev-tools  
    7. source /opt/ros/foxy/setup.bash  
    8. git clone –recursive git@github.com:norlab-ulaval/design-3-robot-project.git ros2\_ws  
    9. cd \~/ros2\_ws  
    10. ./symlink\_build.sh  
    11. Add the following lines to your \~/.bashrc:  
        1. \# custom commands  
        2. source \~/ros2\_ws/install/setup.bash  
        3. export ROS\_DOMAIN\_ID=\<team\_id\>  
    12. source \~/.bashrc  
    13. sudo apt install ros-foxy-joy\*  
    14. sudo apt install ros-foxy-teleop-twist-joy  
    15. sudo apt install ros-foxy-twist-mux  
    16. sudo apt install ros-foxy-depthai-ros-driver  
    17. sudo chmod 777 /dev/ttyUSB0  
        1. (for lidar permission)  
    18. pip3 install pyserial  
    19. sudo usermod \-a \-G input team\<team-id\>

        

