#!/bin/bash

while true; do
    sleep 600
       	ansible-pull -o -U git@ssh.dev.azure.com:v3/griffsoftdeviot/IoT/IoT >> logging.txt
done
