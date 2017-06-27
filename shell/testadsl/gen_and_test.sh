#!/bin/bash

https_proxies="https.proxy.lst"
http_proxies="http.proxy.lst"

hostfile=".hostfile"

sogou-host -e adslspider | grep -v rsync | awk '{print $1;}' > $hostfile 

nmap -iL .hostfile -p 9090 |grep -B 4 'open'|grep -Po 'adsl[\w\.]+' | awk '{print $1":9090" }' > $https_proxies 
nmap -iL .hostfile -p 8080 |grep -B 4 'open'|grep -Po 'adsl[\w\.]+' |grep 'shop' | awk '{print $1":8080" }' >> $https_proxies

nmap -iL .hostfile -p 9090 |grep -B 4 'open'|grep -Po 'adsl[\w\.]+' | awk '{print $1":9090" }' > $http_proxies 
nmap -iL .hostfile -p 8080 |grep -B 4 'open'|grep -Po 'adsl[\w\.]+' |grep 'shop' | awk '{print $1":8080" }' >> $http_proxies 

echo -e '\n test http proxy:'

while read line
do
    wget -T 3 -e "http_proxy=$line" "https://www.baidu.com/" -O data -o log
    ret=$?
    echo "https proxy ret: $line $ret"

    let id=id+1
done < $https_proxies


echo -e '\n test http proxy:'

while read line
do
    wget -T 3 -t 3 -e "http_proxy=$line" "http://www.baidu.com/" -O data -o log
    ret=$?
    echo "http proxy ret: $line $ret"

    let id=id+1
done < $http_proxies
