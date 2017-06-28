#!/bin/bash

if [ $# -lt 1 ]
then
	echo "please input check_words.";
	exit 1;
fi

cd ..;
./lcmd cu "cd /data/twse_spider/videoeu/euserver1/bin/video_content/.bak;  grep \"$1\" *.new"
./lcmd cu "cd /data/twse_spider/videoeu/euserver2/bin/video_content/.bak;  grep \"$1\" *.new"
./lcmd cu_2 "cd /data/twse_spider/videoeu/euserver3/bin/video_content/.bak;  grep \"$1\" *.new"
