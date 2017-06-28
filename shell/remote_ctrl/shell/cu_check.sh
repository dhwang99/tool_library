#!/bin/bash

if [ $# -lt 1 ]
then
	echo "please input check_words.";
	exit 1;
fi

if [ $# -eq 2 ]
then
	dd=$2;
else
	dd=`date +%Y%m%d`;
fi

cd ..;
./lcmd cu "cd /data/twse_spider/cu/log/; grep \"$1\" result.log_stat_$dd*"
