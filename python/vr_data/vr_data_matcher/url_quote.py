import urllib
import sys
#对字符串进行编码
for url in sys.stdin:
    url=url.strip()
    a=urllib.quote(url)
    print a
