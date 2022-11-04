#!/bin/sh

filename="/home/jetson/IoT/common/deepstream/deepstream_app_sources_trafficcamnet.txt"
camera1=10.84.2.1
camera2=10.84.2.2
camera3=10.84.2.3
ip=$(/sbin/ifconfig eth0 | grep 'inet ' | cut -d: -f2 | awk '{ print substr($2,1, length($2)-2) }')

sed -i "s/$camera1/$ip.1/" $filename
sed -i "s/$camera2/$ip.2/" $filename
sed -i "s/$camera3/$ip.3/" $filename