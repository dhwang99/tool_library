#!/usr/bin/env python
# coding:gbk
'''
Created on 2013-5-16

@author: felicialin
'''

import sys
import re
"""
# Modified by Angel
if sys.maxint == 9223372036854775807:
    sys.path.append("./TCWordSeg/64")
    sys.path.append("./liblinear/64")
else:
    sys.path.append("./TCWordSeg/32")
    sys.path.append("./liblinear/32")
# End
"""
from TCWordSeg import *

#GLOBAL_SEG_MODE = TC_U2L|TC_POS|TC_S2D|TC_U2L|TC_T2S|TC_ENGU|TC_CN
GLOBAL_SEG_MODE = TC_GU | TC_POS | TC_U2L | TC_S2D | TC_T2S | TC_CN | TC_PGU | TC_LGU | TC_SGU | TC_CONV | TC_WGU
#TCInitSeg("wordseg_python/dict")
TCInitSeg("wordseg_python/dict")
seghandle = TCCreateSegHandle(GLOBAL_SEG_MODE)

#stop_words = ["��"]  #ͣ�ô�����
GLOBAL_SEGWORD = " "  #NԪ����ָ���
        
#�ִ�
def GetTokenPos(wd):
    TCSegment(seghandle, wd)
    rescount = TCGetResultCnt(seghandle)
    SegArray = []
    #SegArray = [("<S>",0),]
    for i in range(rescount):
        wordpos = TCGetAt(seghandle, i)     
        pos = wordpos.pos
        word = wordpos.word
        uword = word.decode("gbk", "ignore")
        if pos == 34 : #������ֱ���ӵ�
            continue    
        SegArray += [(wordpos.word, wordpos.pos), ]
        #SegArray += [("<E>",0)]
    return SegArray 
