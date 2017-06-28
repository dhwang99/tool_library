
pid=`ps aux|grep update_baike_vr.py|awk '{print $2}'`
kill $pid
