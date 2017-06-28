<?php
function check_xml_data($content)
{
    $ret = 0;
    $xmlParser = xml_parser_create();
    if (xml_parse($xmlParser, $content, true) != true){
	$ret = 1;	
    }

    xml_parser_free($xmlParser); 
    return $ret;
}
?>

<?php

$dstdir='/cangku/instant_data/recv_new/';
$errordir='/cangku/instant_data/recv_error/';
#$dstdir='recv';
list($s1, $s2) = explode(' ', microtime());
#setlocale(LC_ALL, 'zh_CN.UTF8');
date_default_timezone_set('Asia/Chongqing');
$str_time = strftime("%Y%m%d-%H%M%S");
$fileprefix = $s2.".".$s1;

$rawdata = file_get_contents("php://input");
$rawlen = strlen($rawdata);

$headers = getallheaders();
$clen = $headers['Content-Length'];

if (array_key_exists('Referer', $headers)) {
	if (strpos($headers['Referer'], "upload.htm") > 0) {
		if (strncasecmp("xmldata=", $rawdata, 8) == 0) {
			$rawdata = urldecode(substr($rawdata, 8));
			echo "rawdata:".htmlspecialchars($rawdata)."; len:$rawlen";
			$rawlen = strlen($rawdata);
			$clen = $rawlen;
		}
	}
}


$error = 0;
//simple check recved data
if ($clen != $rawlen) {
   $error = 1;
}
else if ($rawlen <= 100) {
   $error = 2;
}
else if (check_xml_data($rawdata) != 0) {
    $error = 3;
}
else {
    $local_tmp = "$dstdir/.$fileprefix";
    $fp = fopen($local_tmp, 'w');	
    $wlen = fwrite($fp, $rawdata, $rawlen);
    if ($wlen != $rawlen)
	    $error = 101;
    fclose($fp);
		
    $dst = "$dstdir/wenwen_upload_$str_time.$fileprefix.xml";
    if (0 == $error && chmod($local_tmp, 0777) == False)
	$error = 102;

    if (0 == $error && rename($local_tmp, $dst) == False)
		$error = 103;

   if (0 == $error){
	    $errmsg = "OK. RECV $clen size data; dstfile: $dst.";
	    error_log("wenwen_recv ".$errmsg);
	    echo "RECV OK.";
    }
}

if (0 != $error) {
    //save error result.
    $local_tmp = "$errordir/error".strval($error)."_$str_time.$fileprefix.xml";
    $fp = fopen($local_tmp, 'w');
    $wlen = fwrite($fp, $rawdata, $rawlen);
    if ($wlen != $rawlen)
	    $error = 111;
    fclose($fp);

    $errmsg = "Error: $error.";
    error_log("wenwen_recv ".$errmsg);
    header('HTTP/1.1 500 Internal Server Error');
    echo "ERCV ERROR: $error";
}
?>
