#!/bin/bash

cd ..
cur_time=`date +"%Y%m%d-%H:%M:%S"`;
echo $cur_time" protodesc.h protodesc.dat to online" >> "dis.log"

function dis_fun()
{
	sh lcmd $dst_host "cd $proto_header_dir; mkdir bak;cp protodesc.h bak/protodesc.h.$cur_time";
	sh lscp $dst_host data/protodesc.h $proto_header_dir;

	sh lcmd $dst_host "cd $proto_data_dir; mkdir bak;cp protodesc.dat bak/protodesc.dat.$cur_time";
	sh lscp $dst_host data/protodesc.dat $proto_data_dir; 
}

#backup the old protocol data and copy new protocol to cu and other host

if [ $# -gt 0 ]
then
	dsthost=$1;
else
	echo 'please input dsthost.'
	exit;
fi

if [ $target = "all" -o $target = "online" ]
then
	#for cu & eu
	proto_header_dir="/data/twse_spider/common/protocol/include/";
	proto_data_dir="/data/twse_spider/data/";
	dst_host="cu";
	dis_fun;

	#for ucdb and ucselect 
	proto_header_dir="/data7/source/uc/modules/ProtoDesc/";
	proto_data_dir="/data/tvideo_spider/uc/etc/";
	#dst_host="uc";
	dst_host="uc";
	dis_fun;

	#for ucmain
	proto_header_dir="/data7/source/ucmain/modules/protodesc/";
	proto_data_dir="/data/tvideo_spider/uc/etc/";
	dst_host="uc";
	dis_fun;

	#for fastucmain
	proto_header_dir="/data1/fast_ucmain/modules/protodesc/";
	proto_data_dir="/data1/fast_ucmain/bin/";
	dst_host="cu";
	dis_fun;

	#for fakeec
	proto_header_dir="/data1/fast_ucmain/FakeEU/";
	proto_data_dir="/data1/fast_ucmain/FakeEU/";
	dst_host="cu";
	dis_fun;
fi


#for link test cu and fastucmain
if [ $dsthost = "link" ]
then
	#for link fastucmain
	proto_header_dir="/data1/fast_ucmain_linkzhang/modules/protodesc/";
	proto_data_dir="/data1/fast_ucmain_linkzhang/bin/";
	dst_host="cu_3";
	dis_fun;

	#for link cu & eu
	proto_header_dir="/data1/twse_spider_linkzhang/common/protocol/include/";
	proto_data_dir="/data1/twse_spider_linkzhang/data/";
	dst_host="cu_3";
	dis_fun;

	#for link ucmain
	proto_header_dir="/data1/ucmain_for_link/modules/protodesc/";
	proto_data_dir="/data1/ucmain_for_link/bin/";
	dst_host="test";
	dis_fun;
fi

if [ $dsthost = "test" ]
then
	#fast ucmain
	proto_header_dir="/data1/fast_ucmain_spitz/modules/protodesc/";
	proto_data_dir="/data1/fast_ucmain_spitz/bin/";
	dst_host="cu_3";
	dis_fun;

	#cu & eu
	proto_header_dir="/data/twse_spider_spitz/common/protocol/include/";
	proto_data_dir="/data/twse_spider_spitz/data/";
	dst_host="cu_3";
	dis_fun;

	#uc
	proto_header_dir="/data1/source/uc/modules/ProtoDesc/";
	proto_data_dir="/data1/tvideo_spider/uc/etc/";
	dst_host="test";
	dis_fun;

	#ucmain 1
	proto_header_dir="/data1/source/ucmain/modules/protodesc";
	proto_data_dir="/data1/ucmain/ucmain/bin";
	dst_host="test";
	dis_fun;

	#ucmain 2
	proto_header_dir="/data1/source/ucmain/modules/protodesc";
	proto_data_dir="/data1/ucmain/ucmain/bin";
	dst_host="db";
	dis_fun;
fi

if [ $dsthost = "extractor" ]
then
	proto_header_dir="/data1/fast_ucmain_extractor/modules/protodesc/";
	proto_data_dir="/data1/fast_ucmain_extractor/bin/";
	dst_host="cu_3";
	dis_fun;

	proto_header_dir="/data1/twse_spider_extractor/common/protocol/include/";
	proto_data_dir="/data1/twse_spider_extractor/bin/";
	dst_host="cu_3";
	dis_fun;
fi

