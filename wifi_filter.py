#This script filters the data that has been collected from the access points.
import os

fold = "/opt/sasmob/sync/wifi/"
dirs = os.listdir(fold)
for f in dirs:
    if "under_writing" in f:
        file = os.path.join(fold, f)
        fname = f[0:19]
        t_cmd = 'sudo tshark -r {} -T fields -e frame.time_epoch -e wlan.sa -e wlan.da -e wlan.fc.type_subtype -Y "wlan.fc.type_subtype == 0x04"   -e wlan_radio.channel -e wlan_radio.frequency -e wlan_radio.signal_dbm > /opt/sasmob/sync/wifi/processed/{}_wifi.out'.format(file, fname)
        os.system(t_cmd)
        os.remove(file)
