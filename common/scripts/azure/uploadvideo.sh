#!/bin/bash

#eg: bash uploadvideo.sh 1 0 0 20

IP=$(/sbin/ifconfig eth0 | grep 'inet ' | cut -d: -f2 | awk '{ print substr($2,1, length($2)-2) }')
path="/home/jetson/testLuca/video"
mkdir -p $path
LENGTH=${4:-3}

if [[ $1 == 1 && $2 == 0 && $3 == 0 ]]; then
 echo "Recording from camera1, video length: $LENGTH s, path: $path"
 sudo /usr/bin/ffmpeg -rtsp_transport tcp -i rtsp://admin:@$IP.1 -c:v copy -t $LENGTH $path/camera1.mp4

elif [[ $1 == 0 && $2 == 1 && $3 == 0 ]]; then 
 echo "Recording from camera2, video length: $LENGTH s, path: $path"
 sudo /usr/bin/ffmpeg -rtsp_transport tcp -i rtsp://admin:@$IP.2 -c:v copy -t $LENGTH $path/camera2.mp4

elif [[ $1 == 0 && $2 == 0 && $3 == 1 ]]; then 
 echo "Recording from camera3, video length: $LENGTH s, path: $path"
 sudo /usr/bin/ffmpeg -rtsp_transport tcp -i rtsp://admin:@$IP.3 -c:v copy -t $LENGTH $path/camera3.mp4

elif [[ $1 == 1 && $2 == 1 && $3 == 0 ]]; then 
 echo "Recording from camera1 and camera2, video length: $LENGTH s, path: $path"
 sudo /usr/bin/ffmpeg -rtsp_transport tcp -i rtsp://admin:@$IP.1 -c:v copy -t $LENGTH $path/camera1.mp4
 sudo /usr/bin/ffmpeg -rtsp_transport tcp -i rtsp://admin:@$IP.2 -c:v copy -t $LENGTH $path/camera2.mp4

elif [[ $1 == 1 && $2 == 0 && $3 == 1 ]]; then 
 echo "Recording from camera1 and camera3, video length: $LENGTH s, path: $path"
 sudo /usr/bin/ffmpeg -rtsp_transport tcp -i rtsp://admin:@$IP.1 -c:v copy -t $LENGTH $path/camera1.mp4
 sudo /usr/bin/ffmpeg -rtsp_transport tcp -i rtsp://admin:@$IP.3 -c:v copy -t $LENGTH $path/camera3.mp4

elif [[ $1 == 0 && $2 == 1 && $3 == 1 ]]; then 
 echo "Recording from camera2 and camera3, video length: $LENGTH s, path: $path"
 sudo /usr/bin/ffmpeg -rtsp_transport tcp -i rtsp://admin:@$IP.2 -c:v copy -t $LENGTH $path/camera2.mp4
 sudo /usr/bin/ffmpeg -rtsp_transport tcp -i rtsp://admin:@$IP.3 -c:v copy -t $LENGTH $path/camera3.mp4

else
 echo "Recording from all cameras, video length: $LENGTH s, path: $path"
 sudo /usr/bin/ffmpeg -rtsp_transport tcp -i rtsp://admin:@$IP.1 -c:v copy -t $LENGTH $path/camera1.mp4
 sudo /usr/bin/ffmpeg -rtsp_transport tcp -i rtsp://admin:@$IP.2 -c:v copy -t $LENGTH $path/camera2.mp4
 sudo /usr/bin/ffmpeg -rtsp_transport tcp -i rtsp://admin:@$IP.3 -c:v copy -t $LENGTH $path/camera3.mp4

fi

CONNECTION_STRING=$(curl -sS 'https://griotstorageaccount.blob.core.windows.net/device-config/connection.json?sp=r&st=2022-07-14T11:21:26Z&se=2023-07-14T19:21:26Z&spr=https&sv=2021-06-08&sr=b&sig=AX8Aymgd5wVOOaW4bYLCFIztZo%2F1wa7LKhVPd5GEAkc%3D' | jq '.[] | select(.host == "'"$(hostname)"'")' | jq '.connectionString' | tr -d '"') 

python3 uploadvideo.py $CONNECTION_STRING