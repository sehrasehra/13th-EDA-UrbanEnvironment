#!/bin/bash
search_dir="./data"
for path in "$search_dir"/*
do
    filename=$(basename -- ${path} .csv)
    mkdir $filename
    mv $path $filename
done
