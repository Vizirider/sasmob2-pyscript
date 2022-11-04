#! /bin/bash

#export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1

mkdir /home/jetson/IoT/common/deepstream/output_detection
mkdir /home/jetson/IoT/common/deepstream/output_tracking
mkdir /home/jetson/IoT/common/deepstream/output_tracking_temp

/home/jetson/IoT/common/deepstream/deepstream-app -c /home/jetson/IoT/common/deepstream/deepstream_app_sources_trafficcamnet.txt -t

