#! /bin/sh
baseDir=$(cd "$(dirname "$0")"; pwd)
if [ $# -lt 1 ]
then
	echo "please input filename."
        exit 1;
fi

cd $baseDir;

filename=$1
midname=$2
#midname="aaaa.$filename"

#gzip -c -d $filename > $midname

agents=("http://10.204.8.228:65470/" "http://10.204.19.229:65470/" "http://10.204.19.230:65470/")

#grep -v '<unick>.*</unick>' $midname | grep -v '<askerNick>.*</askerNick>' > $filename.1
#mv $filename.1 $midname

curdate=`date +%Y%m%d`
curtime=`date +"%Y%m%d %H:%M:%S"`
logfile="log/log.dh.$curdate"
filesize=`stat -c%s $filename`

if [ -z "$filesize" -o "$filesize" = "0" ]
then
	echo "[$curtime] ERROR.NO SEND $filename to dh. size: $filesize." >> $logfile;
	exit $transfer_status
fi

transfer_status=1
for agent in ${agents[*]} 
do
	url="http://push./wenwen/datarecv/recv_compress.php"
	wget -e "http_proxy=${agent}"  --timeout=30 -t 3 $url --post-file="$filename" -O wget.data -o wget.log
	if [ $? -eq 0 ]
	then
		echo "[$curtime] OK.send $filename to dh. size: $filesize." >> $logfile;
		transfer_status=0
		break;
	fi
done

if [ $transfer_status -ne 0 ]
then
	echo "[$curtime] ERROR.send $filename to dh. size: $filesize." >> $logfile;
fi
#rm $midname

exit $transfer_status
