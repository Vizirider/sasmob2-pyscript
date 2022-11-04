import sys
import os
from azure.storage.blob import BlobClient
from zipfile import ZipFile

import azureconst

HOSTNAME = sys.argv[1]

blob = BlobClient.from_connection_string(conn_str=azureconst.CONN_STR,container_name="iofiles", blob_name="{}/experiment-dir-final.zip".format(HOSTNAME))

try:

    with open('experiment-dir-final.zip',"wb") as f:

        f.write(blob.download_blob().readall())

        print('experiment-dir-final.zip downloaded from container: iotfiles  successfully')
        
        with ZipFile('experiment-dir-final.zip', 'r') as zipObj:
            zipObj.extractall(azureconst.DEEPSTREAM_DIRECTORY + 'model')
            
    os.remove("experiment-dir-final.zip")

except Exception as e:

    print(e)