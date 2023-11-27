#!/bin/bash

input_folder="$1"
xml_file_list=()
for text_path in "$input_folder"/*/*.xml; do
    xml_file_list+=("$text_path")
done
python3 text_embedding.py "${xml_file_list[@]}"
