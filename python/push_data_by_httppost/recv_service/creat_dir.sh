
tmpdst="recv";
if [ ! -d $tmpdst ]
then
	mkdir $tmpdst 
	chmod 0777 $tmpdst 
fi

tmpdst="recv_e";
if [ ! -d $tmpdst ]
then
	mkdir $tmpdst 
	chmod 0777 $tmpdst 
fi

error_dir='/cangku/instant_data/recv_error'
if [ ! -d $error_dir ]
then
	mkdir $error_dir 
	chmod 0777 $error_dir
	if [ ! -h recv_error ]
	then
		ln -s $error_dir recv_error
	fi
fi
