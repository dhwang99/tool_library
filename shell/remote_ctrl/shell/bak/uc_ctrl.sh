#!/bin/bash

cd ..

#for cu
cmdstr="$1.sh";

./lcmd uc "cd /data/tvideo_spider/uc/shell; sh $cmdstr $2"
./lcmd uc "cd /data/tvideo_spider/uc2/shell; sh $cmdstr $2"
