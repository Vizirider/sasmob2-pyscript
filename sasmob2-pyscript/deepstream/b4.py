from genericpath import exists
from operator import index
import os
from pickle import FALSE
from wsgiref import headers
import pandas as pd
from os import path
import glob 
import datetime
import shutil
import csv
import time
import calendar
import gzip

def szeged_count(**kwargs):

    def getTrackingData(path_to_tracker_output,x, y):
        tracking_data=pd.read_csv(path_to_tracker_output,header=None,sep=' ', on_bad_lines='skip',compression= 'infer',dtype={3: str})
        tracking_data = tracking_data.dropna()
        tracking_data=tracking_data[[0,1,2,3,7,8,9,10]]
        tracking_data.columns=['frameID','timestamp','label','trackID','x0','y0','x1','y1']
        
        tracking_data['x0']=tracking_data['x0']*x
        tracking_data['x1']=tracking_data['x1']*x
        tracking_data['y0']=tracking_data['y0']*y
        tracking_data['y1']=tracking_data['y1']*y
        
        tracking_data["trackID"]=tracking_data["trackID"].astype(int)
        
        tracking_data['timestamp']=pd.to_datetime(tracking_data['timestamp'], format="%Y:%m:%dT%H:%M:%S.%fZ")
        tracking_data['y_center']=(tracking_data['y0']+tracking_data['y1'])/2
        tracking_data['x_center']=(tracking_data['x0']+tracking_data['x1'])/2
        return tracking_data
    
    
    
    def getObjNum(data):
        data_car_usz=data[(data['label']=='car') & (data['y1']>130) ]
        data_count=data['trackID'].value_counts().reset_index()
        data_count.columns=['trackID','count']
        data_first=data_car_usz.drop_duplicates(keep='first',subset=['trackID'])
        data_last=data_car_usz.drop_duplicates(keep='last',subset=['trackID'])
        data_merged_usz=data_first.merge(data_last, on='trackID')
        data_merged_usz=data_merged_usz.merge(data_count, on='trackID')
        data_merged_usz=data_merged_usz[data_merged_usz['y1_y']>data_merged_usz['y1_x']]

        data_car_bv=data[(data['label']=='car') & (data['y1']>130)]
        data_first=data_car_bv.drop_duplicates(keep='first',subset=['trackID'])
        data_last=data_car_bv.drop_duplicates(keep='last',subset=['trackID'])
        data_merged_bv=data_first.merge(data_last, on='trackID')
        data_merged_bv=data_merged_bv.merge(data_count, on='trackID')
        data_merged_bv=data_merged_bv[data_merged_bv['y1_y']<data_merged_bv['y1_x']]
        
        to_ujszeged_car=len(data_merged_usz[(data_merged_usz['y1_y']>350)&
                                    #(data_merged_usz['y1_x']<200)&
                                    (data_merged_usz['y1_y']-data_merged_usz['y1_x']>50) & 
                                    (data_merged_usz['count']>4)])

        to_belvaros_car=len(data_merged_bv[(data_merged_bv['x1_x']>800) &
                                   (data_merged_bv['x1_y']<850) &
                                   (data_merged_bv['x1_y']-data_merged_bv['x1_x']<-100) & 
                                   (data_merged_bv['count']>4)])
        
        
        data_first=data.drop_duplicates(keep='first',subset=['trackID'])
        data_last=data.drop_duplicates(keep='last',subset=['trackID'])
        data_merged=data_first.merge(data_last, on='trackID')
        data_merged=data_merged.merge(data_count, on='trackID')
        data_merged.head()

        b_b=data_merged[(data_merged['label_x']=='bicycle')&
                (data_merged['x1_x']-data_merged['x1_y']>10)&
                (data_merged['x1_x']>700)
               &(data_merged['x1_y']<800)]
        
        b_usz=data_merged[(data_merged['label_x']=='bicycle')&
                (data_merged['y1_x']-data_merged['y1_y']<-50)&
                (data_merged['y1_x']<500)&
                 (data_merged['y1_y']>400)]
        
        sc_b=data_merged[(data_merged['label_x']=='scooter')&
                (data_merged['x1_x']-data_merged['x1_y']>10)&
                 (data_merged['count']>2)&
                (data_merged['x1_x']>800)&
                (data_merged['x1_y']<850)]
        
        sc_usz=data_merged[(data_merged['label_x']=='scooter')&
                (data_merged['y1_x']-data_merged['y1_y']<-10)&
                   (data_merged['count']>4)&
                (data_merged['y1_x']<500)&
                  (data_merged['y1_y']>450)]
        
        gy_b=data_merged[(data_merged['label_x']=='pedestrian')&
                (data_merged['y1_x']-data_merged['y1_y']>50)&
                 (data_merged['count']>20)&
                   (data_merged['x1_x']<600)&
                   (data_merged['x1_x']>150)&
                (data_merged['y1_x']>400)&
                (data_merged['y1_y']<450)]
        
        gy_usz=data_merged[(data_merged['label_x']=='pedestrian')&
                (data_merged['y1_x']-data_merged['y1_y']<-50)&
                 (data_merged['count']>20)&
                   (data_merged['x1_x']<600)&
                   (data_merged['x1_x']>150)&
                (data_merged['y1_x']<450)&
                (data_merged['y1_y']>400)]
                   #(data_merged['y1_x']<500)&
                #(data_merged['y1_y']>500)]
                
        gy_usz=max([0,len(gy_usz)-len(b_usz)-len(sc_usz)])
        
        
        return to_belvaros_car, to_ujszeged_car, gy_b, gy_usz, b_b, b_usz, sc_b, sc_usz

    
    ###############################
    # main

    def main():
        today = datetime.date.today() 
        date = today.strftime("%Y-%m-%d")
        #date = "2022-06-14"
        #print(date)
        #filename = "/mnt/sasmob/AP2/counted_objects_direction_belvaros/{}.csv".format(date)
        filename = "/home/jetson/sasmob2-pyscript/deepstream/output_tracking/{}.csv".format(date) #output filename 
        #filename = "/home/inclouded/ssmb/{}.csv".format(date)
        #os.remove(filename) #only if rerunning the script
        fields_list = ['timestamp',
                        'Vehicle to downtown',
                        'Vehicle to Újszeged',
                        'Bicyclist to downtown',
                        'Bicyclist to Újszeged',
                        'Pedestrian to downtown',
                        'Pedestrian to Újszeged',
                        'Scooter to downtown',
                        'Scooter to Újszeged']
        if not exists(filename):
            print("File Does not exist, creating new file.")
            i_data = pd.DataFrame([], columns = fields_list )
            i_data.to_csv(filename, index=False, sep=";")

        data = pd.read_csv(filename, names=fields_list, sep=";")
        print(len(data))
        stampverify = []
        if not len(data) == 1:
            data = data.drop(data.index[-1])
            proc_timestamps = data.iloc[:, 0]
            for p in proc_timestamps:
                stampverify.append(p)
        

 
        ##### begin processing

        frame_w=960 #a lentebbi algoritmus ilyen felbontású képekre van megadva
        frame_h=544 #a lentebbi algoritmus ilyen felbontású képekre van megadva

        real_frame_w=960 # a tanított neuronháló végül ilyen felbontásban ad eredményt
        real_frame_h=544 # a tanított neuronháló végül ilyen felbontásban ad eredményt

        x_ratio=frame_w/real_frame_w
        y_ratio=frame_h/real_frame_h
        
        #root = "/home/inclouded/ssmb/ssmb/1220904006/raw/track_zip/"
        root="/home/jetson/sasmob2-pyscript/deepstream/output_tracking/" #input directory
        

        files= os.listdir(root)
        #files = os.listdir(root)

        prev_tracking_data=[]
        prev_car1_IDs=set()
        prev_car2_IDs=set()
        prev_bike_u_IDs=set()
        prev_bike_b_IDs=set()
        prev_ped_u_IDs=set()
        prev_ped_b_IDs=set()
        
        # This cycle has to be run to log files of the 5 min data: the new ones, and 
        #the last one allready processed.
        
        
        tracking_datas=[]
        for file_name in glob.iglob(root +'**/*.txt', recursive=True):
                print(file_name)
                #pth = root+"{}".format(pth)
                #print(os.path.getsize(pth))
                sz = os.path.getsize(file_name)
                if sz < 50:
                    print('File is empty')
                    #os.remove(pth)
                    continue
                tracking_data=getTrackingData(file_name, x_ratio, y_ratio)  
                tracking_datas.append(tracking_data) 
        
        #########
        all_tracking_data=pd.concat(tracking_datas)
        
        #filter not important parts of image
        all_tracking_data=all_tracking_data[(all_tracking_data['x1']>160) & (all_tracking_data['y1']>160)]

        
        all_tracking_data=all_tracking_data.sort_values(by='timestamp').reset_index(drop=True)
        
        all_tracking_data['5m']=all_tracking_data['timestamp'].dt.floor('5min')

        timestamps=all_tracking_data['5m'].drop_duplicates().tolist()
        new_timestamps = []
        for tst in timestamps:
            if not str(tst)[0:16] in stampverify:
                new_timestamps.append(str(tst))
        tracking_data=pd.DataFrame()

        
        for ts in new_timestamps:
            
            #prev_tracking_data=tracking_data.copy()
            
            tracking_data=all_tracking_data[all_tracking_data['5m']==ts].reset_index(drop=True)
            
            car_b, car_usz, gy_b, gy_usz, b_b, b_usz, sc_b, sc_usz=getObjNum(tracking_data)
            ts_str=str(ts)

            
            dict_data = {
                        'timestamp':ts_str[0:16],
                        'Vehicle to downtown':str(car_b),
                        'Vehicle to Újszeged':str(car_usz),
                        'Bicyclist to downtown':str(len(b_b)),
                        'Bicyclist to Újszeged':str(len(b_usz)),
                        'Pedestrian to downtown':str(len(gy_b)),
                        'Pedestrian to Újszeged':str(gy_usz),
                        'Scooter to downtown':str(len(sc_b)),
                        'Scooter to Újszeged':str(len(sc_usz)) 
                        }
            data = data.append(dict_data, ignore_index=True)
            data.to_csv(filename, header=False,index=False, sep=";")
            

    #dates = ["2022-07-05", "2022-07-23", "2022-07-30"]
    #for date in dates:

        #main(date)
    main()
szeged_count()

