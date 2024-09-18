#!/usr/bin/env bash
sudo apt install -y python3.8-venv screen udev
cd ~/glo4001
git reset --hard
git pull
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#sudo cp ~/glo4001/scripts/jupyter.service /etc/systemd/system/jupyter.service
#sudo cp ~/glo4001/scripts/ros_rover.service /etc/systemd/system/ros_rover.service

sudo chmod 777 -R /tmp

# udev
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
sudo udevadm control --reload-rules && sudo udevadm trigger

#sudo systemctl daemon-reload

#sudo systemctl enable jupyter
#sudo systemctl enable ros_rover

#sudo systemctl start jupyter
#sudo systemctl start ros_rover

cd ~/ros2_ws
git reset --hard
git pull
./symlink_build.sh
