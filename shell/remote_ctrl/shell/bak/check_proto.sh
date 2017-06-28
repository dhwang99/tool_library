#!/bin/bash

cd ..

cur_time=`date +"%Y%m%d-%H:%M:%S"`;
proto_h_md5=`md5sum data/protodesc.h|awk '{print $1;}'`;
proto_dat_md5=`md5sum data/protodesc.dat|awk '{print $1;}'`;

echo $proto_h_md5;
echo $proto_dat_md5;

function check_fun()
{
	#sh lcmd $dst_host "cd $proto_header_dir; md5=\`md5sum protodesc.h\`; if [ \"$md5\" = $proto_h_md5 ] then echo header_check_OK; fi;";
	sh lcmd $dst_host "md5=\`md5sum $proto_header_dir/protodesc.h|awk '{print \$1;}'\`; if [ $proto_h_md5 = \$md5 ]; then echo OK_check_head.\$md5;else echo ERROR_check_head.\$md5;fi;";
	sh lcmd $dst_host "md5=\`md5sum $proto_data_dir/protodesc.dat|awk '{print \$1;}'\`; if [ $proto_dat_md5 = \$md5 ]; then echo OK_check_data.\$md5;else echo ERROR_check_data.\$md5;fi;";
	#sh lcmd $dst_host "md5=\`md5sum $proto_data_dir/protodesc.dat|awk '{print \$1;}'\`; echo \$md5;";
}

#backup the old protocol data and copy new protocol to cu and other host

#for cu
proto_header_dir="/data/twse_spider/common/protocol/include/";
proto_data_dir="/data/twse_spider/data/";
dst_host="cu";
check_fun;

#for ucdb and ucselect 
proto_header_dir="/data1/source/uc/modules/ProtoDesc/";
proto_data_dir="/data/tvideo_spider/uc/etc/";
#dst_host="uc";
dst_host="uc";
check_fun;

#for ucmain
proto_header_dir="/data1/source/ucmain/modules/protodesc/";
proto_data_dir="/data/tvideo_spider/uc/etc/";
dst_host="uc";
check_fun;

#for fastucmain
proto_header_dir="/data1/fast_ucmain/modules/protodesc/";
proto_data_dir="/data1/fast_ucmain/modules/protodesc";
dst_host="cu_1";
check_fun;

#for fakeuc
proto_header_dir="/data1/fast_ucmain/FakeEU/";
proto_data_dir="/data1/fast_ucmain/FakeEU/";
dst_host="cu_1";
check_fun;
