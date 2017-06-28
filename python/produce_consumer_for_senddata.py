#!/usr/bin/env python
#encoding=utf8

import os
import sys
import pdb
import logging
import time
import getopt
import re
import redis

import fcntl
import signal
import multiprocessing 

def create_logger(logfilename , logName=None) :
    import logging,logging.handlers
    logger = logging.getLogger(logName)
    LOG_FILE = logfilename
    #infohdlr = logging.StreamHandler(sys.stdout)
    #infohdlr = logging.handlers.TimedRotatingFileHandler(logfilename,when='D',interval=1,backupCount=40)
    infohdlr = logging.handlers.RotatingFileHandler(LOG_FILE,maxBytes=1024*1024,backupCount=40)
    infohdlr.setLevel(logging.INFO)
    #detail
    #debughdlr = logging.StreamHandler(sys.stdout)
    #debughdlr = logging.handlers.TimedRotatingFileHandler(logfilename,when='D',interval=1,backupCount=40)
    debughdlr = logging.handlers.RotatingFileHandler(LOG_FILE,maxBytes=1024*1024,backupCount=40)
    debughdlr.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)6s  %(threadName)-12s %(filename)-10s  %(lineno)4d:%(funcName)16s|| %(message)s')

    infohdlr.setFormatter(formatter)
    debughdlr.setFormatter(formatter)

    logger.addHandler(infohdlr)
    logger.addHandler(debughdlr)

    logger.setLevel(logging.DEBUG)
    return logger

#待发送url列表，在进程起的时候初始化
class UrlItems:
    def __init__(self):
        server = multiprocessing.Manager()
        self.url_list = server.list()

    def load_urls(self, fname):
        logger = logging.getLogger()
        infostr = "init url items."
        logger.debug(infostr)

        with open(fname, 'r') as fp:
            for line in fp:
                line = line.strip()
                self.url_list.insert(0, line)

        url_size = len(self.url_list)
        infostr = "wait send urlsize: %s" % (url_size)
        logger.debug(infostr)

    def pop_url(self):
        url = None
        try:
            url = self.url_list.pop()
        except Exception, e:
            url = None
            print e
        
        return url 


def send_worker(outf, push_max, lock):
    logger = logging.getLogger()
    outfile = open(outf, 'a+')
    send_status = 0
    while True:
        send_status =  (send_status + 1) % 2 
        url = g_items.pop_url()
        if url == None:
            dinfo = 'Can not get url. total send: %s' % g_push_count.value
            logger.debug(dinfo)
            break

        '''
        do send action and set send status 
        '''
        target_id = "12345"
        g_check_url_count.value += 1
        time.sleep(0.1)  #为测试用
        dinfo = 'sendurl: %s. target:%s; status: %s; check count: %s; push count: %s' % \
                (url, target_id, send_status, g_check_url_count.value, g_push_count.value)
        logger.debug(dinfo)
        
        #写文件状态. 原url,输出的url或id, 发送状态;
        fcntl.flock(outfile,fcntl.LOCK_EX)
        outfile.flush()
        dinfo = "%s\t%s\t%s" % (url, target_id, send_status)
        outfile.write("%s\n" % dinfo)
        outfile.flush()
        fcntl.flock(outfile,fcntl.LOCK_UN)

        if send_status == 0:
            #成功。计数器加1
            g_push_count.value += 1
            #判断任务是否完成
            if g_push_count.value >= push_max:
                dinfo = 'all sent. total send: %s' % g_push_count.value
                logger.debug(dinfo)
                break

#全局url队列
g_items = UrlItems()
#当前成功推送量
g_push_count = multiprocessing.Value('i', 0)
#当前尝试推送的url量
g_check_url_count = multiprocessing.Value('i', 0)

if __name__ == '__main__':
    process_num = 5
    [infname, outfname, push_max] = sys.argv[1:]
    push_max = int(push_max)
    logfilename = "../log/sendlog"
    logger = create_logger(logfilename)

    g_items.load_urls(infname)
    #初始化已发送URL数.所以输出文件名每天不一样。最好为 url.sent.lst.%Y%m%d
    pre_sent_ok = 0
    try:
        with open(outfname) as fp:
            for line in fp:
                line = line.strip()
                arr = line.split('\t')
                if len(arr) < 3:
                    continue
                if int(arr[2]) == 0:  #状态0表明当天已成功推送
                    pre_sent_ok += 1
    except Exception, e:
        pass

    g_push_count.value = pre_sent_ok  

    dinfo = "Begin Send work. infile: %s; outfile: %s; push_max: %s; pre_sent_ok: %s" % \
            (infname, outfname, push_max, pre_sent_ok)
    logger.debug(dinfo)

    #多进程模型.本次用多进程模型
    record = []
    lock = multiprocessing.Lock()
    for i in range(process_num):
        process = multiprocessing.Process(target=send_worker,args=(outfname, push_max, lock))
        process.start()
        record.append(process)

    for process in record:
        process.join()

    #多线程模型
    ''' 
    lock  = threading.Lock()
    for i in range(process_num):
        thread = threading.Thread(target=send_worker,args=(outfname, push_max, lock))
        thread.start()
        record.append(thread)

    for thread in record:
        thread.join()
    '''

    dinfo = "All Process finished. check urls: %s; Sent urls: %s. Recommend urls count: %s" %\
             (g_check_url_count.value, g_push_count.value, push_max)
             
    logger.debug(dinfo)
