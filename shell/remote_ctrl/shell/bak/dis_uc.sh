#!/bin/bash

if [ $# -eq 0 ]
then
	echo "please input target{link|test|online|all"}
	exit 1;
else
	target="$1";
fi

cd ..

#for uc

if [ $target = "online" -o $target = "all" ]
then
	root_dir=/data7/source/uc;
	./lscp uc data/uc.tgz $root_dir; 
	./lcmd uc "cd $root_dir; rm bak/modules -rf; mv modules bak/; tar xzvf uc.tgz; cd proj; make clean; make"
fi

if [ $target = "test" -o $target = "all" ]
then
	root_dir=/data7/source/uc;
	./lscp test data/uc.tgz $root_dir; 
	./lcmd test "cd $root_dir; rm bak/modules -rf; mv modules bak/; tar xzvf uc.tgz; cd proj; make clean; make"
fi
