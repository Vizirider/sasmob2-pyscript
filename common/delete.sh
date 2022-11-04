#!/bin/sh

yes | sudo apt-get remove --auto-remove curl
yes | sudo apt-get remove --auto-remove jq  
yes | sudo apt-get remove --purge aziot-edge
yes | sudo docker rm -f edgeHub
yes | sudo docker rm -f DeviceProxy
yes | sudo docker rm -f edgeAgent
yes | sudo docker rm -f IoTEdgeMetricsCollector
yes | sudo apt-get remove --purge moby-cli
yes | sudo apt-get remove --purge moby-engine
yes | sudo systemctl stop deepstream.service upload.service ansible.service
yes | sudo systemctl disable deepstream.service 
yes | sudo systemctl disable upload.service
yes | sudo systemctl disable ansible.service
yes | sudo rm /lib/systemd/system/deepstream.service # and symlinks that might be related
yes | sudo rm /lib/systemd/system/upload.service
yes | sudo rm /lib/systemd/system/ansible.service
yes | sudo rm /etc/init.d/deepstream.service
yes | sudo rm /etc/init.d/upload.service
yes | sudo rm /etc/init.d/ansible.service
yes | sudo systemctl daemon-reload
yes | sudo systemctl reset-failed
sudo rm -R /home/jetson/IoT
