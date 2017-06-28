import urllib
import sys
#对字符串进行解码
for url in sys.stdin:
    a=urllib.unquote(url)
    print a
