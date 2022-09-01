#Script to get gps data from mikrotik router and create csv files every 10mins.
#Installed in the panels.
import paramiko
import time
from time import sleep
import datetime
import csv
import os
from socket import gethostname

host = gethostname()

router_ip = "10.0.{}.6".format(host) #Change with the ip of the mikrotik router.
router_username = "admin" #user of mikrotik
router_password = "SASMobAlfa12345!" #password of mikrotik
t_end = time.time() + 60 * 10

vals = []
plval = None
ploval = None
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(router_ip,username=router_username,password=router_password,look_for_keys=False )
while time.time() < t_end:

    starttime=time.time()
    time.sleep(0.98) #wait time of 1 sec before each entry of gps data

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    vals.append(timestamp + ";")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/system gps monitor once") #command to get the gps data

    output = ssh_stdout.readlines()
    #Extract only the data we need and fill in with None if no data.
    for line in output:
        if "latitude" in line:
            lat, lval = line.split()
            if lval is not "none":
                vals.append(lval + ";")
            elif lval is "none":
                print("None value")
                continue
        if "longitude" in line:
            log, loval = line.split()
            if loval is not "none":
                vals.append(loval + "\n")
            elif loval is "none":
                print("None value")

    print(lval,loval)
ssh.close
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = '/opt/sasmob/sync/gps/{}.csv'.format(timestamp)
file = open(filename, "w")
fields = ['Timestamp;', 'Latitude;', 'Longitude\n']
file.writelines(fields)
file.writelines(vals)
file.close()

nvals = []

#data filter for bad data
with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        if len(row) >= 4:
            if len(row) == 5:
                #print( row[2], row[3], row[4])
                nrows =  row[2]+ ';' + row[3]+ ';' +row[4] + "\n"
                if "none" in nrows:
                    print("Not good row")
                else:
                    nrow =  row[2]+ ';' + row[3]+ ';' +row[4] + "\n"
                    nvals.append(nrow)
                    #print(nrow)
                #vals.append(nrow)
            elif len(row) == 4:
                #print( row[1], row[2], row[3])
                nrows =  row[1]+ ';' + row[2]+ ';' +row[3]+ "\n"
                if "none" in nrows:
                    print("Not good row")
                else:
                    nrow =  row[1]+ ';' + row[2]+ ';' +row[3] + "\n"
                    nvals.append(nrow)
                    #print(nrow)
                #vals.append(row[1], row[2], row[3])
            elif len(row) < 3:
                print("sorry")
        elif len(row) == 3:
                nrows =  row[0]+ ';' + row[1]+ ';' +row[2]+ "\n"
                if "none" in nrows:
                    print("Not good row")
                else:
                    nrow =  row[0]+ ';' + row[1]+ ';' +row[2] + "\n"
                    nvals.append(nrow)
                    #print(nrow)
                #print(row[0] , row[1], row[2])
               # vals.append(row[1], row[2], row[3])
        

os.remove(filename)
file = open(filename, "w")
file.writelines(nvals)
file.close()
