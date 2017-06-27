# -*- coding: utf-8 -*-

import md5
import re
import MultipartPostHandler
import urllib2
import sys
import urllib
import base64
import os

def upload(targetName, md5sum):
    m = md5.new()  
    f = open(targetName,'rb')  
    m.update(f.read())  
    f.close()  
    md5sum = m.hexdigest()  

    http_agents=["http://10.204.8.228:65470/" "http://10.204.19.229:65470/" "http://10.204.19.230:65470/"]
    params = {'source':'wenwen', 'sign':md5sum, 'type':'compressed','data':open(targetName).read()}
	url="http://test/datarecv/recv_compress.php"

    request = urllib2.Request(validatorURL)

    proxy=urllib2.ProxyHandler({'http': http_agents[0]})

    opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler(), proxy)
    result = opener.open(request, params).read()
    return result

if __name__ == "__main__":
    if len(sys.argv[1:]) < 1:
        print "usage: %s file1 file2 file3 ......" % (sys.argv[0],)
        sys.exit()

    for arg in sys.argv[1:]:
        sourceName = arg
        targetName = arg + ".drct"
        zipCmd = "gzip "+ targetName
        zipName = targetName+".gz"
        try:
            os.system(zipCmd)
            result = upload(zipName, md5sum)
        except Exception, e:
            print e
        else:
            print "uploaded %s \n result is %s" % (zipName, result)

