#!/bin/bash

#make sure jq is installed on $SCA_SERVICE_DIR
if [ ! -f $SCA_SERVICE_DIR/jq ];
then
        echo "installing jq"
        wget https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 -O $SCA_SERVICE_DIR/jq
        chmod +x $SCA_SERVICE_DIR/jq
fi

input_task_id=`$SCA_SERVICE_DIR/jq -r '.input_task_id' config.json`
#echo "using $input_task_id"
mkdir -p output

files=`$SCA_SERVICE_DIR/jq -r '.[0] .files[] .filename' ../$input_task_id/products.json`
echo $files

for file in $files; do
    echo "processing $file"

    echo "converting to single extension" 
    $SCA_SERVICE_DIR/mef2fits.py $fits ../$input_task_id/$file
done


