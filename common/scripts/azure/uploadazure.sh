#!/bin/bash

HOST=$(hostname)
CONNECTION_STRING=$(curl -sS 'https://griotstorageaccount.blob.core.windows.net/device-config/connection.json?sp=r&st=2022-07-14T11:21:26Z&se=2023-07-14T19:21:26Z&spr=https&sv=2021-06-08&sr=b&sig=AX8Aymgd5wVOOaW4bYLCFIztZo%2F1wa7LKhVPd5GEAkc%3D' | jq '.[] | select(.host == "'"$HOST"'")' | jq '.connectionString' | tr -d '"') 

python3 uploadazure.py $CONNECTION_STRING
