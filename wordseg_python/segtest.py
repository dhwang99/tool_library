#!/usr/bin/env python
#coding:gbk
'''
Created on 2013-3-15

@author: felicia
'''
import sys
import Global
if __name__ ==  '__main__':
    infile = sys.argv[1]
    outfile = sys.argv[2]
    #fi = open('training_set.txt', 'r')
    #fo = open('keywd.txt', 'w')
    fi = open(infile, 'r')
    fo = open(outfile, 'w')
    kw = {}
    for line in fi:
        segResult = Global.GetTokenPos(line)
        for segword, pos in segResult:
            if not kw.has_key(segword):
                kw[segword] = [pos, 0]
            kw[segword][-1] += 1
    l = kw.items()
    l.sort(key = lambda x: x[-1][-1], reverse = True)
    for segword, (pos, cnt) in l:
        fo.write('%s\t%d\t%d\n' %(segword, pos, cnt))
    fi.close()
    fo.close()
    '''
    segResult = Global.GetTokenPos("你好你好")    
    for i, (segword, pos) in enumerate(segResult):
    print segword,pos
    '''
