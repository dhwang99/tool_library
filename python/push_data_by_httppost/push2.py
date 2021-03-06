# -*- coding: utf-8 -*-
import md5
import re
import MultipartPostHandler
import urllib2
import sys
import urllib
import base64
import os
encodeStr = 'utf-8'
questionHead = '<question>'.encode(encodeStr)
xmlHead = '<?xml version="1.0" encoding="utf-8"?>\n'.encode(encodeStr)
dumpHead = '<dump>\n'.encode(encodeStr)
dumpTail = '</dump>\n'.encode(encodeStr)
typeDelete = '<type>delete</type>'
typeUpdate = '<type>update</type>'

agentIPList=("", "")

def xmlFilter(sourceName, targetName):
    source = open(sourceName)
    target = file(targetName, 'w');
    target.write(xmlHead)
    target.write(dumpHead)   
    source.readline()
    source.readline()
    questions = source.read().decode('gbk', 'ignore')[:-8].split('<question>')
    qNum = len(questions)
    qidPat = re.compile('.*<qid>(.*)</qid>.*', re.MULTILINE|re.DOTALL)
    catPat = re.compile('.*<categoryID>(.*)</categoryID>.*', re.MULTILINE|re.DOTALL)
    titlePat = re.compile('.*<title>(.*)</title>.*', re.MULTILINE|re.DOTALL)
    typeStr = ''
    isDelType = False
    if '.new' in sourceName:
        typeStr = typeUpdate
        isDelType = False
    elif '.del' in sourceName:
        typeStr = typeDelete
        isDelType = True
    else:
        return ''
    md5sum = ''
    for i in range(1, qNum):
        target.write(questionHead)
        target.write(typeStr)
        target.write(questions[i].encode(encodeStr))
        idMatch = qidPat.match(questions[i])
        if idMatch != None:
            qidStr = idMatch.group(1)
            md5Str = md5.new(qidStr).hexdigest()
            # print 'qid: ',
            # print qidStr
            # print 'md5: ',
            # print md5Str
            if md5sum == '':
                md5sum = md5Str
    source.close()
    target.write(dumpTail)
    target.close()
    return md5sum

def upload(targetName, md5sum):
    params = {'source':'wenwen', 'sign':md5sum, 'type':'compressed','data':open(targetName).read()}
    #params = {'source':'wenwen', 'data':'<qid> 1234567890 </qid>', 'sign':md5.new('1234567890').hexdigest()}
#    validatorURL = "http:/cgi-bin/upload"   
    result  = 0
    for ip in agentIPList:
        validatorURL    = "http://" + ip + "/wenwen/datarecv_normal/recv2.php"
	print validatorURL
#    validatorURL  = "http:/cgi-bin/upload"
        request = urllib2.Request(validatorURL)
#    username = 'wenwen'
#    password = 'wenwen.soso'
#    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
#    request.add_header("Authorization", "Basic %s" % base64string)   
    #result = urllib2.urlopen(request).read()
        opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler())
        result = opener.open(request, params).read()
        if result != 0:
            continue;
        else:
            break;
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
            md5sum = xmlFilter(sourceName, targetName)
            if md5sum != '':
                print md5sum
                os.system(zipCmd)
                #result = upload(zipName, md5sum)
            else:
                result = 'skipped';
        except Exception, e:
            print e
        else:
            print "uploaded %s \n result is %s" % (zipName, result)

