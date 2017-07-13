#!/usr/bin/env python
#!coding: utf8

import urllib
import urlparse
import sys

def get_dict(line):
    d = {}
    for item in line.strip().split('&'):
        tmp = item.split('=')
        if len(tmp) != 2:
            continue
        k, v = tmp
        d[k] = urllib.unquote(v)
    return d

def parse_url():
    for line in sys.stdin:
        d = get_dict(line)
        if d.has_key('ur'):
            url, title = urlparse.urlparse(d['ur']).netloc, d.get('ti', '')
            if url.strip():
                print '%s\t%s\t%s' %(url, title, '1')

def match_url(root_url = 'www.google.com'):
    for line in sys.stdin:
        d = get_dict(line)
        if d.has_key('ur') and d['ur'].find(root_url) != -1:
            d['ti'] = d.get('ti', '')
            print '%s\t%s\t%s' %(d['ur'], d['ti'], '1')

if __name__ == '__main__':
    #parse_url()
    sitereg = sys.argv[1]
    match_url(sitereg)
