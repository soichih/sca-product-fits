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

    curl -X POST -H "Content-Type: application/json" -d "{\"msg\":\"converting $file to single extension fits\"}" $SCA_PROGRESS_URL
    $SCA_SERVICE_DIR/mef2fits.py $file ../$input_task_id/$file

    curl -X POST -H "Content-Type: application/json" -d "{\"msg\":\"converting $file to png\"}" $SCA_PROGRESS_URL
    $SCA_SERVICE_DIR/fits2img.py -t png -o $file.png $file

    echo "cleaning $file"
    rm $file
done


