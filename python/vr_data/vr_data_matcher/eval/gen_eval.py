import random
import sys

fin=open(sys.argv[1])
fout=open(sys.argv[2], 'w')
lines=fin.readlines()
random.shuffle(lines)
fout.writelines(lines[0:200])


