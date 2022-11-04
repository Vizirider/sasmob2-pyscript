#script to ssh into the access point and get the wlan data.
import paramiko
import time
from time import sleep
import datetime
import csv
import os
from socket import gethostname
import ftplib

while True:
    host = gethostname()

    router_ip = "10.0.{}.7".format(host)
    router_username = "admin"
    router_password = "SASMobAlfa12345!"
    tstp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(router_ip,username=router_username,password=router_password,look_for_keys=False )
    ssh_stdin, ssh_stdout, ssh_stderr=ssh.exec_command("/interface wireless sniffer sniff wlan1 duration=300")
    sleep(300)
    print(ssh_stderr.readlines())
    ssh.close()


    ftp_server = ftplib.FTP(router_ip, router_username, router_password)
    filename = "under_writing"
    fname = "/opt/sasmob/sync/wifi/{}_under_writing".format(tstp)

    with open(fname, "wb") as file:
        # Command for Downloading the file "RETR filename"
        ftp_server.retrbinary(f"RETR {filename}", file.write)
    ftp_server.quit()

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(router_ip,username=router_username,password=router_password,look_for_keys=False )
    ssh_stdin, ssh_stdout, ssh_stderr= ssh.exec_command("/file remove under_writing")
    print(ssh_stderr.readlines())
    ssh.close()
