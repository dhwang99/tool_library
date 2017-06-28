import sys
import HTMLParser

for url in sys.stdin:
    print HTMLParser.HTMLParser().unescape(url)
