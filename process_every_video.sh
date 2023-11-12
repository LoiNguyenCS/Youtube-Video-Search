#!/bin/bash

input_folder="$1"
for video_path in "$input_folder"/*/*.mp4; do
    echo "$video_path"
    if [ -f "$video_path" ]; then
        python3 video-encoding.py "$video_path" 
    fi
done
