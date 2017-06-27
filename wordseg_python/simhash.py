#!/usr/bin/python
# coding=utf-8
import hashlib
def get_simhash(tokens):
    v = [0] * 128
    for t in [int(hashlib.md5(x).hexdigest(),16) for x in tokens]: #t为token的普通hash值 
        for i in range(128):
            bitmask = 1 << i
            if t & bitmask :
                v[i] += 1 #查看当前bit位是否为1,是的话将该位+1
            else:
                v[i] -= 1 #否则的话,该位-1
        fingerprint = 0
    for i in range(128):
        if v[i] >= 0:
            fingerprint += 1 << i
    return fingerprint #整个文档的fingerprint为最终各个位>=0的和
    
def get_haiming_distance(hash1,hash2):
    x = (hash1 ^ hash2) & ((1 << 128) - 1)
    tot = 0;
    while x :
        tot += 1
        x &= x - 1
    return tot

if __name__ == "__main__":
    import sys
    if len(sys.argv)<3:
        print "Usage: %s [simhash or haiming_distance] filename",sys.argv[0]
        sys.exit()
    if sys.argv[1]=="simhash":
        fin = open(sys.argv[2])
        index = 0
        hash1 = 0
        hash2 = 0
        for line in fin.readlines():
            print line,"\t",str(get_simhash(line.strip().split("\t")))
            if index==0:
                hash1 = get_simhash(line.strip().split("\t"))
            elif index==1:
                hash2 = get_simhash(line.strip().split("\t"))
            index +=1
        fin.close()
        print "HAIMING_DISTANCE\t",str(get_haiming_distance(hash1,hash2))
    elif sys.argv[1]=="haming_distance":
        fin = open(sys.argv[2])
        for line in fin.readlines():
            print line,"\t",str(get_haiming_distance(line))
        fin.close()
