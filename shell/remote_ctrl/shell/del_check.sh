#!/bin/bash

if [ $# -lt 1 ]
then
	echo "please input check_words.";
	exit 1;
fi

cd ..;
./lcmd uc "cd /data/tvideo_spider/uc/data/.bak; grep \"$1\" urldel.*"
./lcmd uc_1 "cd /data/tvideo_spider/uc2/data/.bak; grep \"$1\" urldel.*"
