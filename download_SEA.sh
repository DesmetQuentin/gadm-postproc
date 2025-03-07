#!/bin/bash

while IFS= read -r url; do
    # Download the URL using wget
    wget "$url"
done < "url_SEA.txt"

for file in *.zip; do
    folder=${file%.zip}
    mkdir $folder
    mv $file $folder/
    cd $folder
    unzip $file
    rm $file
    cd ..
done
