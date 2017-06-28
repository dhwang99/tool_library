cd ..
./lcmd cu_3 'killall -9 cu_test videoeuserver_test ucmain_test'
./lcmd test 'killall -9 ucdb_video_1 ucdb_video_2 ucselect_video_1 ucselect_video_2'
./lcmd test 'killall -9 ucmain'
./lcmd db 'killall -9 ucmain'

./lcmd cu_3 'cd /data1/twse_spider_test/cu/bin; ./cu_test -d'
./lcmd cu_3 'cd /data1/twse_spider_test/videoeu/euserver1/bin; sh start.sh'
./lcmd cu_3 'cd /data1/fast_ucmain_test/bin; sh start.sh'

./lcmd test 'cd /data1/ucmain/bin; sh start.sh'
./lcmd db 'cd /data1/ucmain/bin; sh start.sh'

./lcmd test 'cd /data/tvideo_spider/uc/shell; sh clean.sh' 
./lcmd test 'cd /data/tvideo_spider/uc2/shell; sh clean.sh' 

./lcmd test 'cd /data/tvideo_spider/uc/shell; sh init.sh' 
./lcmd test 'cd /data/tvideo_spider/uc2/shell; sh init.sh' 

./lcmd test 'cd /data/tvideo_spider/uc/shell; sh start.sh' 
./lcmd test 'cd /data/tvideo_spider/uc2/shell; sh start.sh' 

