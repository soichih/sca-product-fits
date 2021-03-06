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

#report to progress service before we begin
i=0
for file in $files; do
    ((i = i + 1))  
    curl -s -X POST -H "Content-Type: application/json" -d "{\"name\":\"$file\", \"status\":\"waiting\", \"progress\": 0}" ${SCA_PROGRESS_URL}.$i
done

i=0
for file in $files; do
    ((i = i + 1))  

    curl -s -X POST -H "Content-Type: application/json" \
        -d "{\"msg\":\"converting $file to single extension fits\", \"status\":\"running\"}" ${SCA_PROGRESS_URL}.$i

    echo "$SCA_SERVICE_DIR/mef2fits.py $file ../$input_task_id/$file"
    $SCA_SERVICE_DIR/mef2fits.py $file ../$input_task_id/$file
    if [ ! $? -eq 0 ]; then
        curl -s -X POST -H "Content-Type: application/json" \
            -d "{\"msg\":\"mef2fits.py returned $?\", \"status\":\"failed\"}" ${SCA_PROGRESS_URL}.$i
        continue
    fi

    curl -s -X POST -H "Content-Type: application/json" \
        -d "{\"msg\":\"converting $file to png\", \"progress\":0.5}" ${SCA_PROGRESS_URL}.$i

    echo "$SCA_SERVICE_DIR/fits2img.py -t png -o $file $file"
    $SCA_SERVICE_DIR/fits2img.py --mask -t png -o $file $file
    if [ ! $? -eq 0 ]; then
        curl -s -X POST -H "Content-Type: application/json" \
            -d "{\"msg\":\"fits2img returned $?\", \"status\":\"failed\"}" ${SCA_PROGRESS_URL}.$i
        continue 
    fi

    curl -s -X POST -H "Content-Type: application/json" \
        -d "{\"msg\":\"denerating DZI\", \"progress\":0.8}" ${SCA_PROGRESS_URL}.$i
    echo "$SCA_SERVICE_DIR/png2dzi.py ${file}.png ${file}.dzi"
    $SCA_SERVICE_DIR/png2dzi.py ${file}.png ${file}.dzi
    if [ ! $? -eq 0 ]; then
        curl -s -X POST -H "Content-Type: application/json" \
            -d "{\"msg\":\"png2dzi returned $?\", \"status\":\"failed\"}" ${SCA_PROGRESS_URL}.$i
        continue 
    fi

    curl -s -X POST -H "Content-Type: application/json" \
        -d "{\"msg\":\"cleaning up\", \"status\":\"finished\", \"progress\": 1}" ${SCA_PROGRESS_URL}.$i

    #rm $file
done

$SCA_SERVICE_DIR/generate_products.py

#fake it for now
#echo "[]" > products.json
