<?php
function gzdecode($data) {
  $len = strlen($data);
  if ($len < 18 || strcmp(substr($data,0,2),"\x1f\x8b")) {
   return null;  // Not GZIP format (See RFC 1952)
  }
  $method = ord(substr($data,2,1));  // Compression method
  $flags  = ord(substr($data,3,1));  // Flags
  if ($flags & 31 != $flags) {
   // Reserved bits are set -- NOT ALLOWED by RFC 1952
   return null;
  }
  // NOTE: $mtime may be negative (PHP integer limitations)
  $mtime = unpack("V", substr($data,4,4));
  $mtime = $mtime[1];
  $xfl  = substr($data,8,1);
  $os    = substr($data,8,1);
  $headerlen = 10;
  $extralen  = 0;
  $extra    = "";
  if ($flags & 4) {
   // 2-byte length prefixed EXTRA data in header
   if ($len - $headerlen - 2 < 8) {
     return false;    // Invalid format
   }
   $extralen = unpack("v",substr($data,8,2));
   $extralen = $extralen[1];
   if ($len - $headerlen - 2 - $extralen < 8) {
     return false;    // Invalid format
   }
   $extra = substr($data,10,$extralen);
   $headerlen += 2 + $extralen;
  }

  $filenamelen = 0;
  $filename = "";
  if ($flags & 8) {
   // C-style string file NAME data in header
   if ($len - $headerlen - 1 < 8) {
     return false;    // Invalid format
   }
   $filenamelen = strpos(substr($data,8+$extralen),chr(0));
   if ($filenamelen === false || $len - $headerlen - $filenamelen - 1 < 8) {
     return false;    // Invalid format
   }
   $filename = substr($data,$headerlen,$filenamelen);
   $headerlen += $filenamelen + 1;
  }

  $commentlen = 0;
  $comment = "";
  if ($flags & 16) {
   // C-style string COMMENT data in header
   if ($len - $headerlen - 1 < 8) {
     return false;    // Invalid format
   }
   $commentlen = strpos(substr($data,8+$extralen+$filenamelen),chr(0));
   if ($commentlen === false || $len - $headerlen - $commentlen - 1 < 8) {
     return false;    // Invalid header format
   }
   $comment = substr($data,$headerlen,$commentlen);
   $headerlen += $commentlen + 1;
  }

  $headercrc = "";
  if ($flags & 1) {
   // 2-bytes (lowest order) of CRC32 on header present
   if ($len - $headerlen - 2 < 8) {
     return false;    // Invalid format
   }
   $calccrc = crc32(substr($data,0,$headerlen)) & 0xffff;
   $headercrc = unpack("v", substr($data,$headerlen,2));
   $headercrc = $headercrc[1];
   if ($headercrc != $calccrc) {
     return false;    // Bad header CRC
   }
   $headerlen += 2;
  }

  // GZIP FOOTER - These be negative due to PHP's limitations
  $datacrc = unpack("V",substr($data,-8,4));
  $datacrc = $datacrc[1];
  $isize = unpack("V",substr($data,-4));
  $isize = $isize[1];

  // Perform the decompression:
  $bodylen = $len-$headerlen-8;
  if ($bodylen < 1) {
   // This should never happen - IMPLEMENTATION BUG!
   return null;
  }
  $body = substr($data,$headerlen,$bodylen);
  $data = "";
  if ($bodylen > 0) {
   switch ($method) {
     case 8:
       // Currently the only supported compression method:
       $data = gzinflate($body);
       break;
     default:
       // Unknown compression method
       return false;
   }
  } else {
   // I'm not sure if zero-byte body content is allowed.
   // Allow it for now...  Do nothing...
  }

  // Verifiy decompressed size and CRC32:
  // NOTE: This may fail with large data sizes depending on how
  //      PHP's integer limitations affect strlen() since $isize
  //      may be negative for large sizes.
  if ($isize != strlen($data) || crc32($data) != $datacrc) {
   // Bad format!  Length or CRC doesn't match!
   return false;
  }
  return $data;
}

function check_xml_data($content)
{
    $ret = 0;
    if (strncasecmp($content, "<?xml", 5) == 0)
	return 0;
    
   return 1;
/*
    $xmlParser = xml_parser_create();
    if (xml_parse($xmlParser, $content, true) != true){
	$ret = 1;	
    }

    xml_parser_free($xmlParser); 
    return $ret;
*/
}
?>

<?php

$dstdir='/cangku/instant_data/recv_lf/';
$errordir='/cangku/instant_data/recv_error_lf/';
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
else if ($rawlen <= 50) {
   $error = 2;
}

#$uncompress_data = gzdecode($rawdata, $rawlen);
/*
if (check_xml_data($uncompress_data) != 0) {
    $error = 3;
}
else 
 */
{
    $local_tmp = "$dstdir/.$fileprefix";
    $local_tmp_gz = "$dstdir/.$fileprefix.gz";
    $fp = fopen($local_tmp_gz, 'w');	
    $wlen = fwrite($fp, $rawdata, $rawlen);
    if ($wlen != $rawlen)
	    $error = 101;
    fclose($fp);

    $uncompress_cmd = "cd $dstdir; gzip -d .$fileprefix.gz"; 
    system($uncompress_cmd, $ret);
    if ($ret != 0) {
	unlink(".$fileprefix.gz");
        $error = 115;
    }
		
    $dst = "$dstdir/wenwen_upload_$str_time.$fileprefix.xml";
    if (0 == $error && chmod($local_tmp, 0777) == False)
	    $error = 102;

    if (0 == $error && rename($local_tmp, $dst) == False)
		$error = 103;

   if (0 == $error){
	    $errmsg = "OK. RECV $clen size data; dstfile: $dst.";
	    error_log("wenwen_recv_compress ".$errmsg);
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
    error_log("wenwen_recv_compress ".$errmsg);
    header('HTTP/1.1 500 Internal Server Error');
    echo "ERCV ERROR: $error";
}
?>
