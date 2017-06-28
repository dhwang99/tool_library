#!/bin/bash

hostfile=host/all.lst;
servertype=`echo $1|awk -F"_" '{print $1}'`;
serverid=`echo $1|awk -F"_" '{print $2}'`;

dstfile=$2;

if [ $servertype = "all" ]
then
	cp $hostfile $dstfile.tmp
else
	grep "h_$servertype" $hostfile > $dstfile.tmp
fi

if [ -z "$serverid" ]
then
	echo "in global count"
	ipcount=`wc -l $dstfile.tmp|cut -d " " -f 1`;
	if [ $ipcount -eq 0 ]
	then
		grep "$1" $hostfile > $dstfile.tmp
	fi
fi

if [ -n "$serverid" ]
then
	total=`wc -l $dstfile.tmp|cut -d ' ' -f 1`;
	if [ $total -lt $serverid ]
	then
		echo "the id overloaded. total is $total.";
	fi
	head -n $serverid $dstfile.tmp | tail -n 1 > $dstfile;
	rm $dstfile.tmp;
else
	mv $dstfile.tmp $dstfile
fi
