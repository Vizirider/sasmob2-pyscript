#! /bin/bash

#export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1

mkdir ./output_detection
mkdir ./output_tracking

./deepstream-app -c deepstream_app_sources_trafficcamnet.txt -t
