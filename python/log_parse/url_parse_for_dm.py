# encoding=utf8

import urlparse
import urllib
import sys
import pdb

sch_prefix=['/s/?w=',
            '/ms/search.jsp?key=']

sch_prefix=['http://wenwen.sogou.com/s/?w=',
            'http://wenwen.sogou.com/ms/search.jsp?key=']


def match_pv_ch(url, prefix):
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


def do_test():
    url1='http://dm.wenwen.sogou.com/dt/wenwen/p?ref=http%3A%2F%2Fwenwen.sogou.com%2Fs%2F%3Fw%3D%25E4%25BA%25BA%25E5%2580%259F%25E4%25BA%2586%25E6%2588%2591%25E5%2587%25A0%25E5%258D%2581%25E5%259D%2597%25E9%2592%25B1%26ch%3Dww.xqy.xgss&url=http%3A%2F%2Fwenwen.sogou.com%2Fz%2Fq406109890.htm%3Fsw%3D%25E4%25BA%25BA%25E5%2580%259F%25E4%25BA%2586%25E6%2588%2591%25E5%2587%25A0%25E5%258D%2581%25E5%259D%2597%25E9%2592%25B1%26ch%3Dnew.w.search.0%26&dt_ssuid=1910337324&login=0&rnd=0.9716372163457865'


    url2 = 'http://dm.wenwen.sogou.com/dt/wenwen/p?ref=http%3A%2F%2Fwenwen.sogou.com%2Fquestion%2F%3Fqid%3D6272168284301755240%26ch%3Dww.sy.tj%26pid%3Dww.sy.tj&url=http%3A%2F%2Fwenwen.sogou.com%2Fs%2F%3Fw%3Dexcel%2520%25E7%25AD%259B%25E9%2580%2589%25E5%2588%25B0%25E5%258F%25A6%25E4%25B8%2580%25E5%25BC%25A0%25E8%25A1%25A8%26ch%3Dww.xqy.xgss&dt_ssuid=1910337324&login=0&rnd=0.8542865670836299'

    url3 = 'http://dm.wenwen.sogou.com/dt/wenwen/p?ref=http%3A%2F%2Fwenwen.sogou.com%2Fquestion%2F%3Fqid%3D6272168209521509216%26ch%3Dww.sy.tj%26pid%3Dww.sy.tj&url=http%3A%2F%2Fwenwen.sogou.com%2Fms%2Fsearch.jsp%3Fkey%3D%25E7%25A9%25BA%25E8%25B0%2583%25E5%25AE%25A4%25E5%2586%2585%25E6%258C%2582%25E6%259C%25BA%25E5%25AE%2589%25E8%25A3%2585%25E5%259B%25BE%25E8%25A7%25A3%26ch%3Dww.wap.xqy.related.search&dt_ssuid=1910337324&login=0&rnd=0.42119706058736983'

    rs1 = match_pv_ch(url1, sch_prefix)
    rs2 = match_pv_ch(url2, sch_prefix)
    rs3 = match_pv_ch(url3, sch_prefix)

    print rs1

    print rs2

    print rs3


def do_parse_line(line):
    arr = line.split('\t')
    if len(arr) > 3:
        get_arr = arr[2].split(' ')
        #pdb.set_trace()
        if len(get_arr) > 2:
            ps = match_pv_ch(get_arr[1], sch_prefix)
            if ps != None:
                print "%s\t%s" % (ps[0], ps[1])

def do_parse_file():
    fname = sys.argv[1]
    f = open(fname)

    for logline in f:
        do_parse_line(logline)

    
    
if __name__ == "__main__":
    #do_test()
    if len(sys.argv) > 1:
        do_parse_file()
        sys.exit()

    for logline in sys.stdin:
        do_parse_line(logline)
