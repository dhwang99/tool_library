Exec=update_baike_vr.py
exec_prefix=${Exec%%.*}
confile="../conf/vr_match.conf"
logbin="./cronolog"

if ! pgrep $Exec > /dev/null;then
    main_name=`echo $Exec | cut -d '.' -f 1`
	nohup ./$Exec $confile | $logbin -p 30days -l "../log/${exec_prefix}.log" "../log/${exec_prefix}.%Y-%m-%d" 2>../log/err.log  &
	echo "$(date +'%F %T') $Exec started!"
else
	echo "$(date +'%F %T') $Exec already started!"
fi
