#!/bin/bash

cd ..

#for cu

./lcmd uc "killall ucdb_search1 ucdb_search2";
sleep 5;
./lcmd uc "cd /data/tvideo_spider/uc_search1; sh start.sh"
./lcmd uc "cd /data/tvideo_spider/uc_search2; sh start.sh"
