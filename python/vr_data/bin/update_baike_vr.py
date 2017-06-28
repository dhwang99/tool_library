#!/usr/bin/python
#coding=utf8

import redis
import time
import sys
import os
import pdb
import json
import urllib
import requests
import logging
import time
import HTMLParser

redis_conf_test = { 
    'host':'redis.master.luedongapp.11009.soso-redis.com',
    'port':11009,
    'db':0,
    'password':'wenwen@sogou.com'
}

redis_conf_online = { 
    'host':'redis.master.baikestructuraldata.10000.soso-redis.com',
    'port':10000,
    'db':0,
    'password':'quntribe@sogou.com'
}

proxy_conf = []
#like this: 
proxy_conf = [
   {"http": "10.240.80.91:8080", "https": "10.240.80.91:8081"},
   {"http": "10.240.80.92:8080", "https": "10.240.80.92:8081"}
]


def create_logger(logfilename , logName=None) :
    import logging,logging.handlers
    logger = logging.getLogger(logName)
    infohdlr = logging.StreamHandler(sys.stdout)
    infohdlr.setLevel(logging.INFO)
    #detail
    debughdlr = logging.StreamHandler(sys.stdout)
    debughdlr.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)6s  %(threadName)-12s %(filename)-10s  %(lineno)4d:%(funcName)16s|| %(message)s')

    infohdlr.setFormatter(formatter)
    debughdlr.setFormatter(formatter)

    logger.addHandler(infohdlr)
    logger.addHandler(debughdlr)

    logger.setLevel(logging.DEBUG)
    return logger

class VRMatchReq:
    def __init__(self):
        self.baikeid= 0
        self.query = ''
        self.extend_query = ''
        self.source = ''
        self.match_type = 0  #0: default; 1: full url match; 2: regular match for url
        self.url_req = ''   #url req

        self.line = ''

        self.vr_url_prefix='http://api.open.sogou.com/apiopen/openapi/vrinfo?from=sogoubaike&reqtype=json&type=0&query='
        
    def parse_line(self, line):
        line = line.strip()
        arr = line.split('\t')
        ll = len(arr)
        if ll < 6:
            return None

        self.baikeid= int(arr[0])
        self.query = arr[1]
        self.extend_query = arr[2]
        self.source = arr[3]
        self.match_type = int(arr[4])  #0: default; 1: full url match; 2: regular match for url
        self.url_req = arr[5]   #url req

        if self.baikeid <= 0 or self.query == '' or self.extend_query == '' or self.source == '' or self.match_type < 0:
            return None

        self.line = line

        return self

    def get_vr_url(self):
        query = self.query + " " + self.extend_query
        quote_query = urllib.quote(query)
        return self.vr_url_prefix + quote_query

    def get_redis_key(self):
        return 'baiketupu_' + self.source + '_' + str(self.baikeid);

class BaikeVRDumper:
    def __init__(self, online_redis):
        self.vr_reqs = []
        redis_conf = redis_conf_online
        if online_redis == False:
            redis_conf = redis_conf_test

        self.rd = redis.Redis(host=redis_conf['host'],
                                port=redis_conf['port'],
                                db=redis_conf['db'],
                                password=redis_conf['password'])

        self.good_dump_count = 0
        self.source_counts = {}       #每个类型下的词条数
        self.source_dump_counts = {}  #成功匹配的词条数
        self.down_err_count = 0       #下载错误数。可能是网络问题，也有可能是代理问题，也有可能是服务器问题。需要分析
        self.blank_data_count = 0     #空数据错误数。基本上是服务器错

    def load_reqs(self, req_file):
        logger = logging.getLogger()
        with open(req_file) as fp:
            for line in fp:
                vr_req = VRMatchReq()
                if vr_req.parse_line(line) == None:
                    infostr = "Error: load req error: %s" % line
                    logger.error(infostr)
                    return None

                self.vr_reqs.append(vr_req)
                self.source_counts.setdefault(vr_req.source, 0)
                self.source_counts[vr_req.source] += 1

        self.source_dump_counts = dict.fromkeys(self.source_counts, 0)
        return self


    def get_vr_data(self, vr_req, try_count):
        vr_url = vr_req.get_vr_url()
        proxy_count = len(proxy_conf)
        vr_res = None
        proxy = None
        for try_id in range(try_count): 
            try:
                if proxy_count > 0:
                    proxy = proxy_conf[try_id % proxy_count]
                vr_res = requests.get(vr_url, proxies=proxy, timeout=10)
                if vr_res != None and vr_res.ok:
                    return vr_res.content
                self.blank_data_count += 1
            except Exception,ex:
                self.down_err_count += 1
                pass
        return None
    
    # return new url if ok
    # return None if checking failed 
    def check_and_convert_imgurl(self, url, try_count):
        #lurl = HTMLParser.HTMLParser().unescape(url)
        lurl = url
        proxy = None
        proxy_count = len(proxy_conf)
        for try_id in range(try_count): 
            try:
                if proxy_count > 0:
                    proxy = proxy_conf[try_id % proxy_count]
                vr_res = requests.get(lurl, proxies=proxy, timeout=10)
                if vr_res != None:
                    if vr_res.ok:
                        return url
                    if vr_res.status_code >= 400 and vr_res.status_code <500: #only 4xx, return None
                        return '' 
            except Exception,ex:
                pass

        return url 


    def check_data(self, json_obj, vr_req):
        if json_obj == None or len(json_obj) == 0:
            return 1 

        item = json_obj[0].get('item')
        if item == None:
            return 2 

        display = item.get('display')
        if display == None:
            return 3 

        url = display.get('url')
        if url == None:
            return 4 

        if vr_req.match_type == 1:
            if url != vr_req.url_req:
                return 5 
        elif vr_req.match_type == 2:
            return 6 

        return 0 

    def update_redis(self, json_obj, vr_req):
        key = vr_req.get_redis_key()

        #for checking
        json_obj[0]['baiketupu_update_time'] =  int(time.time())
        json_obj[0]['baiketupu_key'] = key

        json_str = json.dumps(json_obj)

        res = self.rd.set(key, json_str)
        if res:
            return json_obj
        else:
            return None


    def dump_by_reqfile(self, filename):
        logger = logging.getLogger()

        if self.load_reqs(filename) != None:
            infostr = "OK: load reqs."
            logger.info(infostr)
        else:
            infostr = "Err: load reqs."
            logger.error(infostr)
            return None

        for req in self.vr_reqs:
            vr_data = self.get_vr_data(req, 3)
            if vr_data == None:
                infostr = "get_vr_data error.req: %s" % req.line
                logger.error(infostr)
                continue

            js_obj = json.loads(vr_data)
            check_ret = self.check_data(js_obj, req)
            if check_ret == 0:
                ret = True
                if req.source == 'original':
                    iconitem = js_obj[0]['item']['display']['icon']
                    if iconitem != None:
                        imgurl = iconitem['@iconaddress']
                        newurl = self.check_and_convert_imgurl(imgurl, 2)
                        iconitem['@iconaddress'] = newurl
                        if newurl == '':
                            infostr = "image is 404. req: %s" % req.line
                            logger.error(infostr)


                ret = self.update_redis(js_obj, req)
                if ret == None:
                    infostr = "insert redis error for req:'%s'" % req.line
                    logger.error(infostr)
                else:
                    self.good_dump_count += 1
                    self.source_dump_counts[req.source] += 1
            else:
                #pdb.set_trace()
                infostr = "check data format error. check_ret:%s req:'%s'" % (check_ret, req.line)
                logger.error(infostr)

        return self

    def stat_log(self):
        arrs = []
        down_str = "downerr:%s blankdata:%s" % (self.down_err_count, self.blank_data_count)
        arrs.append(down_str)

        total_str = 'total:%s total_ok:%s' % (len(self.vr_reqs), self.good_dump_count)
        arrs.append(total_str)

        for t,c in self.source_counts.iteritems():
            source_str = '%s_total:%s %s_ok:%s' % (t, c, t, self.source_dump_counts[t])
            arrs.append(source_str)

        infostr = " ".join(arrs)
        return infostr


if __name__ == "__main__" :
    if len(sys.argv) < 2:
        print "Usage: input error !"
        sys.exit(1)
    
    online_redis = True
    if len(sys.argv) > 2:
        online_redis = False

    logfilename="../log/dump.log"
    logger = create_logger(logfilename)
    
    beg_time = int(time.time())
    baike_dumper = BaikeVRDumper(online_redis)
    baike_dumper.dump_by_reqfile(sys.argv[1])
    end_time = int(time.time())

    infostr = "dump vr to baike. use_time:%s %s" % ((end_time - beg_time), baike_dumper.stat_log())
    logger.info(infostr)
