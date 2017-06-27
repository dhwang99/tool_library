# encoding=utf8

import urlparse
import urllib
import sys
import pdb

sch_prefix=['/s/?w=',
        '/ms/search.jsp?key=']

sch_prefix=['http://wenwen.sogou.com/s/?w=',
        'http://wenwen.sogou.com/ms/search.jsp?key=']


def match_pv_ch_from_dm(url, prefix):
    rurl_parsed = urlparse.urlparse(url)

    if rurl_parsed != None:
        rquery = rurl_parsed.query
        if rquery != None:
            querys=urlparse.parse_qs(rquery)
            pv_url = querys.get('url')
            if pv_url != None and len(pv_url) > 0:
                match_prefix = None
                for p in prefix:
                    if pv_url[0].startswith(p):
                        match_prefix = p
                        break

                if match_prefix == None:
                    return None

                ch = None 
                pv_url_parsed = urlparse.urlparse(pv_url[0])
                if pv_url_parsed != None:
                    querys = urlparse.parse_qs(pv_url_parsed.query)
                    if querys != None:
                        chlst = querys.get('ch')
                        if chlst != None and len(chlst) > 0:
                            ch = chlst[0]

                return [match_prefix, ch]

    return None

def match_pv_ch_from_dr(url, prefix):
    match_prefix = None
    for p in prefix:
        if url.startswith(p):
            match_prefix = p
            break

    if match_prefix == None:
        return None

    ch = None 
    pv_url_parsed = urlparse.urlparse(url)
    if pv_url_parsed != None:
        querys = urlparse.parse_qs(pv_url_parsed.query)
        if querys != None:
            chlst = querys.get('ch')
            if chlst != None and len(chlst) > 0:
                ch = chlst[0]

    return [match_prefix, ch]

def do_parse_line_dm(line):
    arr = line.split('\t')
    if len(arr) > 3:
        get_arr = arr[2].split(' ')
        if len(get_arr) > 2:
            ps = match_pv_ch_from_dm(get_arr[1], sch_prefix)
            if ps != None:
                print "%s\t%s" % (ps[0], ps[1])

def do_parse_line_dr(line):
    arr = line.split('\t')
    if len(arr) > 5:
        url = arr[4].strip('"')
        ps = match_pv_ch_from_dr(url, sch_prefix)
        if ps != None:
            print "%s\t%s" % (ps[0], ps[1])

def do_parse_file():
    fname = sys.argv[1]
    f = open(fname)

    for logline in f:
        do_parse_line_dr(logline)
    
    
if __name__ == "__main__":
    #do_test()
    if len(sys.argv) > 1:
        do_parse_file()
        sys.exit()

    for logline in sys.stdin:
        do_parse_line_dr(logline)
