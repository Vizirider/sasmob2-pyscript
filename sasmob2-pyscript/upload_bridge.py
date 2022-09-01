import os
import shutil
from google.cloud import storage
import datetime
import re
from shutil import copyfile, rmtree
from socket import gethostname
from zipfile import ZipFile
import gzip

bucket = "sasmob-data"
config = "/home/jetson/data/g_creds.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config
host = gethostname()
date = datetime.datetime.now().strftime("%Y-%m-%d")
timest = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def upload_to_bucket(blob_name, file_path, bucket_name):
        try:
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(file_path)
            return True

        except Exception as e:
            print(e)
            return False

def track_move():
    folder = "/home/jetson/deepstream/output_tracking/"
    files = files = os.listdir(folder)
    if not os.path.exists('/home/jetson/deepstream/track_tmp'):
        os.makedirs('/home/jetson/deepstream/track_tmp')
    if not os.path.exists('/home/jetson/deepstream/track_tmp_zip'):
        os.makedirs('/home/jetson/deepstream/track_tmp_zip')
    for file in files:
        fi_path = os.path.join(folder, file)
        target = "/home/jetson/deepstream/track_tmp/{}".format(file)
        shutil.move(fi_path, target)
    z_folder = '/home/jetson/deepstream/track_tmp'
    z_files = os.listdir(z_folder)
    for z_file in z_files:
        file = os.path.join(z_folder, z_file)
        with open(file, 'rb') as f_in:
            with open('/home/jetson/deepstream/track_tmp_zip/{}_{}.gz'.format(timest,z_file), 'wb') as f_out:
                with gzip.GzipFile(file, 'wb', fileobj=f_out) as f_out:
                    shutil.copyfileobj(f_in, f_out)
        os.remove(file)

def track_upload():
    up_folder = "/home/jetson/deepstream/track_tmp_zip/"
    up_files = os.listdir(up_folder)
    for u_file in up_files:
        u_fi_path = os.path.join(up_folder, u_file)
        date = u_file[0:10]
        print(date)
        blob = '{}/raw/track_zip/{}/{}'.format(host, date, u_file )
        up = upload_to_bucket(blob,u_fi_path, bucket )
        print(up)
        if up is True:
            os.remove(u_fi_path)
            print("Upload Complete")
        else:
            print("Upload Incomplete")
            break
track_move()
track_upload()
