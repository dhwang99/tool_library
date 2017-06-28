<?php
	$file_pattern=dirname(__FILE__)."/recv_error/error*.xml";
	$delcmd = "rm -f $file_pattern";
	exec($delcmd, $res1, $ret1);
	echo "delcmd: $delcmd<br>";
	echo "ret: $ret1.<br.";
	print_r($res1);
?>
