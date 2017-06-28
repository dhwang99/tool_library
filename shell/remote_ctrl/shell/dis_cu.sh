#!/bin/bash

cd ..

if [ $# -eq 0 ]
then
	echo "please input target{link|test|online|all"}
	exit 1;
else
	target="$1";
fi

if [ $target = "link" -o $target = "all" ]
then
	data_dir="/data/twse_spider_link/cu";
	host="cu_3";
	./lscp cu data/cu.tgz $data_dir/cu.tgz
	./lcmd host "cd $data_dir; mkdir bak; rm bak/src -rf; mv src bak/; tar xzvf cu.tgz; cd proj; make clean; make"
fi

if [ $target = "test" -o $target = "all" ]
then
	data_dir="/data/twse_spider_test/cu";
	host="cu_3";
	./lscp $cu data/cu.tgz $data_dir/cu.tgz
	./lcmd $host "cd $data_dir; mkdir bak; rm bak/src -rf; mv src bak/; tar xzvf cu.tgz; cd proj; make clean; make"
fi

if [ $target = "all" -o $target = "online" ]
then
	data_dir="/data/twse_spider/cu";
	host="cu";
	./lscp $cu data/cu.tgz $data_dir/cu.tgz
	./lcmd $host "cd $data_dir; mkdir bak; rm bak/src -rf; mv src bak/; tar xzvf cu.tgz; cd proj; make clean; make"
fi
