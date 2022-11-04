#!/bin/sh

yes | sudo wget https://packages.microsoft.com/config/ubuntu/18.04/multiarch/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
yes | sudo dpkg -i packages-microsoft-prod.deb
yes | sudo rm packages-microsoft-prod.deb
yes | sudo apt-get update; \
yes | sudo apt-get install moby-engine
sudo cat > /etc/docker/daemon.json << EOF
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    },
    "log-driver": "local",
    "log-opts": {
        "max-size": "10m"
    }
}
EOF
yes | sudo apt-get update; \
yes | sudo apt-get install aziot-edge defender-iot-micro-agent-edge
yes | sudo apt install -y jq
yes | sudo apt-get install curl
HOST=$(hostname)
CONNECTION_STRING=$(curl -sS 'https://griotstorageaccount.blob.core.windows.net/device-config/connection.json?si=deviceConf&spr=https&sv=2021-06-08&sr=b&sig=uM3HcGCJnYfaXleH2ryWK1SbApmxmH6vXh7hjV8iHRQ%3D' | jq '.[] | select(.host == "'"$HOST"'")' | jq '.connectionString' | tr -d '"') 
sudo iotedge config mp --connection-string "$CONNECTION_STRING"
sudo iotedge config apply -c '/etc/aziot/config.toml' 
sudo iotedge system status 
sudo iotedge check00

yes | sudo apt update
yes | sudo apt install ansible
--check ansible-pull with which ansible-pull

mkdir /home/jetson/IoT
sudo chmod -R 777 /home/jetson/IoT

sudo touch /lib/systemd/system/deepstream.service
sudo chmod +x /lib/systemd/system/deepstream.service 
sudo cat > /lib/systemd/system/deepstream.service << EOF
[Unit]
Description=Starting deepstream at every reboot
After=syslog.target network.target

[Service]
SuccessExitStatus=143
Restart=on-failure
RestartSec=1s

User=jetson
Group=jetson

Type=simple


WorkingDirectory=/home/jetson/IoT/common/deepstream
ExecStart=/home/jetson/IoT/common/scripts/deepstream/run_deploy.sh

[Install]
WantedBy=multi-user.target
EOF
sudo touch /lib/systemd/system/upload.service
sudo chmod +x /lib/systemd/system/upload.service 
sudo cat > /lib/systemd/system/upload.service << EOF
[Unit]
Description=Starting uploadazure.sh script at every reboot and every 10 minutes
After=syslog.target network.target

[Service]
SuccessExitStatus=143
Restart=on-failure
RestartSec=1s

User=jetson
Group=jetson

Type=simple


WorkingDirectory=/home/jetson/IoT/common/scripts/azure
ExecStart=/home/jetson/IoT/common/scripts/azure/uploadazure.sh

[Install]
WantedBy=multi-user.target
EOF
EOF
sudo touch /lib/systemd/system/upload.timer
sudo chmod +x /lib/systemd/system/upload.timer 
sudo cat > /lib/systemd/system/upload.timer << EOF
[Timer]
OnCalendar=*-*-* *:*/10:00

[Install]
WantedBy=multi-user.target
EOF
sudo touch /lib/systemd/system/ansible.service
sudo chmod +x /lib/systemd/system/ansible.service 
sudo cat > /lib/systemd/system/ansible.service << EOF
[Unit]
Description=Starting ansible at every reboot
After=syslog.target network.target

[Service]
SuccessExitStatus=143
Restart=on-failure
RestartSec=1s

User=jetson
Group=jetson

Type=simple


WorkingDirectory=/home/jetson/IoT/common/scripts/ansible
ExecStart=/home/jetson/IoT/common/scripts/ansible/cronansible.sh

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable deepstream.service
sudo systemctl enable upload.service
sudo systemctl enable upload.timer
sudo systemctl enable ansible.service
sudo ln /lib/systemd/system/deepstream.service /etc/init.d
sudo ln /lib/systemd/system/upload.service /etc/init.d
sudo ln /lib/systemd/system/upload.timer /etc/init.d
sudo ln /lib/systemd/system/ansible.service /etc/init.d
sudo update-rc.d deepstream.service defaults
sudo update-rc.d upload.service defaults
sudo update-rc.d upload.timer defaults
sudo update-rc.d ansible.service defaults

#sudo -u jetson ansible-pull -U git@ssh.dev.azure.com:v3/griffsoftdeviot/IoT/IoT
