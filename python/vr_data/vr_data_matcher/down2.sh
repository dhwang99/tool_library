#!/bin/bash

#export http_proxy=10.240.80.91:8080


purl="http://api.open.sogou.com/apiopen/openapi/vrinfo?from=sogoubaike&reqtype=json&type=0&query="

local_host_state=`nmap 10.134.96.110 -p 80|grep -B 4 'open'`
if [ ! -z "$local_host_state" ]
then
	purl="http://10.134.96.110/apiopen/openapi/vrinfo?from=sogoubaike&reqtype=json&type=0&query="
fi

dstfile="extract_urls.lst"
rm $dstfile

function down_fun()
{
    ff=$1
    type=$2
    ename=$3

    while read line
    do
        baikeid=`echo -e "$line" | awk -F"\t" '{print $1;}'`
        query=`echo -e "$line" | awk -F"\t" '{print $2;}' | awk -F"（" '{print $1;}'`
        fulltitle=`echo -e "$line" | awk -F"\t" '{print $2;}'`
        quote_query=`echo "$query $type" | python url_quote.py`
        url="${purl}${quote_query}"
     
        dfile="data/${ename}_${baikeid}"
        wget -O $dfile "$url" >> logs 2>&1
    
        srcurl=`grep -Po '(?<=\"url\":\").*?(?=\")' $dfile|head -n 1`
        if [ -z $srcurl ]
        then
            srcurl="null";
        else
            srcurl=`echo $srcurl|python url_unescape.py`
        fi
        echo -e "$baikeid\t$query\t$fulltitle\t$type\t$srcurl\t$url" >> $dstfile
    done < $ff
}


if [ 0 -eq 1 ]
then
	ff=film_20170326.txt  
	type="小说"
	ename="film"
	down_fun $ff $type $ename
	
	ff=tv_play_20170326.txt
	type="小说"
	ename="tv"
	down_fun $ff $type $ename
	
	ff=star_20170326.txt  
	type="行程"
	ename="plan"
	down_fun $ff $type $ename
	
	ff=famous_weibo_20170326.txt
	type="微博"
	ename="weibo"
	down_fun $ff $type $ename
fi

ff=company_leader.lst
	type="微博"
	ename="weibo"
	down_fun $ff $type $ename

sh convert.sh
