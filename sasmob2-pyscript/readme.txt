Gps_collect.py: Used to collect gps data through the gps reciever attached to the mikrotik router uses ssh to get the data.
                Can be executed using python3 most probably all the packages are preinstalled if not please intall it using pip. 
                Before executing open the py file and change the ip address, user, pass and the file location.

Wifi_collect.py: The script can be executed if an access point is connected to the router. Used to collect data from mobile data network. 
                 Executes using python same like gps the user, pass and ip needs to be replaced with proper value.
                 ANother wifi_filter is used to filter out the data for only the required data and save it in a file. 
                 The wificollect runs constantly and the wifi filter runs every 5 or 10 mins.
           
upload.py: Used to gather all the raw data and upload it to the google cloud. Executes with python and requires service key json file to communicate with the google cloud.

Deepstream AI: 
   - Extract the deepstream.zip file.
   - Open deepstream_app_source1_trafficcamnet.txt change the ip address in source0 and source1.
   - please only change the ip it should look something like  uri=rtsp://admin:@10.0.6.1:554
   - Once you have changed the config goto /home/jetson/deepstream and run ./run_deploy.sh
   - The ai should start running and create output in ./output_tracking which will be uploaded to cloud and from there it will be processed.
   
*****If you have any issue please message me in slack or by mail.*****
