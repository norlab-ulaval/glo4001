#!/usr/bin/env bash
cd ~/glo4001
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp ~/glo4001/scripts/jupyter.service /etc/systemd/system/jupyter.service
cp ~/glo4001/scripts/ros_rover.service /etc/systemd/system/ros_rover.service

sudo systemctl daemon-reload

sudo systemclt enable jupyter
sudo systemclt enable ros_rover

sudo systemctl start jupyter
sudo systemctl start ros_rover
