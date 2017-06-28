#!/bin/bash

if [ $# -eq 0 ]
then
	echo "please input target{link|test|online|all"}
	exit 1;
else
	target="$1";
fi

cd ..

if [ $target = "online" -o $target="all" ]
then
	root_dir=/data7/source/ucmain;
	./lscp uc data/ucmain.tgz $root_dir; 
	./lcmd uc "cd $root_dir; rm bak/modules -rf; mv modules bak/; tar xzvf ucmain.tgz; cd proj; make clean; make"
fi

if [ $target = "link" -o $target="all" ]
then
	root_dir=/data1/ucmain_for_link;
	./lscp test data/ucmain.tgz $root_dir; 
	./lcmd test "cd $root_dir; rm bak/modules -rf; mv modules bak/; tar xzvf ucmain.tgz; cd proj; make clean; make"
fi

if [ $target = "test" -o $target="all" ]
then
	root_dir=/data1/source/ucmain;
	#test ucmain1
	./lscp test data/ucmain.tgz $root_dir; 
	./lcmd test "cd $root_dir; rm bak/modules -rf; mv modules bak/; tar xzvf ucmain.tgz; cd proj; make clean; make"

	#test ucmain2
	root_dir=/data1/source/ucmain;
	./lscp db data/ucmain.tgz $root_dir; 
	./lcmd db "cd $root_dir; rm bak/modules -rf; mv modules bak/; tar xzvf ucmain.tgz; cd proj; make clean; make"
fi
