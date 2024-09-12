#!/usr/bin/env bash
cd ~/glo4001
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

sudo cp ~/glo4001/scripts/jupyter.service /etc/systemd/system/jupyter.service
sudo cp ~/glo4001/scripts/ros_rover.service /etc/systemd/system/ros_rover.service

sudo systemclt daemon-reload

sudo systemclt enable jupyter
sudo systemclt enable ros_rover

sudo systemclt start jupyter
sudo systemclt start ros_rover
