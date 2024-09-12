#!/bin/bash

if [ $# -eq 0 ]
then
    echo "Need a bash script as argument."
    exit 1
fi

BASH_SCRIPT_TO_SEND=$1
echo "Sending $BASH_SCRIPT_TO_SEND" and executing on all robots.
read -s -p "Robots password: " REMOTE_PASSWORD

# for ROBOT_IP in 192.168.0.{100..114}
for ROBOT_IP in 192.168.0.{100..114}
do
    if ping -c 1 $ROBOT_IP &> /dev/null
    then
        echo "Sending script to $ROBOT_IP"
        scp $BASH_SCRIPT_TO_SEND robmob@$ROBOT_IP:/tmp
        echo "Executing script on remote machine"
        ssh robmob@$ROBOT_IP "chmod u+x /tmp/$BASH_SCRIPT_TO_SEND; echo $REMOTE_PASSWORD | sudo -S sh -c 'nohup /tmp/$BASH_SCRIPT_TO_SEND > /dev/null 2>&1 &'"
    else
        echo "Robot $ROBOT_IP is ded"
    fi
done
