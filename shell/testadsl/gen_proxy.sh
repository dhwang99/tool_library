#!/bin/bash
hostfile=".hostfile"
sogou-host -e adslspider | grep -v rsync | awk '{print $1;}' > $hostfile 

nmap -iL .hostfile -p 9090 |grep -B 4 'open'|grep -Po 'adsl[\w\.]+' | awk '{print $1":9090" }' > https.proxy.lst
nmap -iL .hostfile -p 8080 |grep -B 4 'open'|grep -Po 'adsl[\w\.]+' |grep 'shop' | awk '{print $1":8080" }' >> https.proxy.lst

nmap -iL .hostfile -p 9090 |grep -B 4 'open'|grep -Po 'adsl[\w\.]+' | awk '{print $1":9090" }' > http.proxy.lst
nmap -iL .hostfile -p 8080 |grep -B 4 'open'|grep -Po 'adsl[\w\.]+' |grep 'shop' | awk '{print $1":8080" }' >> http.proxy.lst
#https and http in one


