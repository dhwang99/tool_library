#!/bin/bash

cd ..

#for cu
if [ $# -eq 0 ]
then
	echo "please input target{all|online|fast|extractor|link|test"}
	exit 1;
else
	target="$1";
fi

if [ $target = "all" -o $target = "online" ]
then
	mod_dir="/data/twse_spider/cu";
	./lcmd cu "cd $mod_dir/proj; make clean; make"

	mod_dir="/data7/source/uc";
	./lcmd uc "cd $mod_dir/proj; make clean; make"

	mod_dir="/data7/source/ucmain";
	./lcmd uc "cd $mod_dir/proj; make clean; make"
fi

if [ $target = "all" -o $target = "fast" ]
then
#for fast_ucmain
	mod_dir="/data1/fast_ucmain";
	./lcmd cu "cd $mod_dir/proj; make clean; make"

#for fake eu
	mod_dir="/data1/fast_ucmain/FakeEU";
	./lcmd cu "cd $mod_dir; make clean; make"
fi

#for extractor

if [ $target = "all" -o $target = "extractor" ]
then
	mod_dir="/data1/twse_spider_extractor/cu";
	./lcmd cu_3 "cd $mod_dir/proj; make clean; make"

	mod_dir="/data1/fast_ucmain_extractor";
	./lcmd cu_3 "cd $mod_dir/proj; make clean; make"
fi

#for link

if [ $target = "all" -o $target = "link" ]
then
	mod_dir="/data1/fast_ucmain_linkzhang/";
	./lcmd cu_3 "cd $mod_dir/proj; make clean; make"

	mod_dir="/data1/twse_spider_linkzhang/cu";
	./lcmd cu_3 "cd $mod_dir/proj; make clean; make"

	mod_dir="/data1/twse_spider_linkzhang/videoeu/src/VEDIOEU/";
	./lcmd test "cd $mod_dir/project; make clean; make"
fi

if [ $target = "all" -o $target = "test" ]
then
	mod_dir="/data1/fast_ucmain_spitz";
	./lcmd cu_3 "cd $mod_dir/proj; make clean; make"

	mod_dir="/data1/twse_spider_spitz/cu";
	./lcmd cu_3 "cd $mod_dir/proj; make clean; make"

	mod_dir="/data1/twse_spider_spitz/videoeu/src/VEDIOEU/";
	./lcmd test "cd $mod_dir/project; make clean; make"

	mod_dir="/data1/source/ucmain/";
	./lcmd test "cd $mod_dir/proj; make clean; make"

	mod_dir="/data1/source/ucmain/";
	./lcmd db "cd $mod_dir/proj; make clean; make"

	mod_dir="/data1/source/uc";
	./lcmd test "cd $mod_dir/proj; make clean; make"
fi

#mod_dir="/data/twse_spider/videoeu/src/VEDIOEU";
#./lcmd cu "cd $mod_dir/project; make clean; make"
#./lcmd cu "cd $mod_dir/../../sh; cp videoeuserver ../euserver1/bin"
#./lcmd cu2 "cd $mod_dir/../../sh; cp videoeuserver ../euserver2/bin"
