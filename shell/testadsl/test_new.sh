
https_proxies="https.proxy.lst"
http_proxies="http.proxy.lst"

while read line
do
    wget -T 3 -e "http_proxy=$line" "https://www.baidu.com/" -O data.$idstr -S
    ret=$?
    echo "https proxy ret: $line $ret"

    let id=id+1
done < $https_proxies

while read line
do
    wget -T 3 -t 3 -e "http_proxy=$line" "http://www.baidu.com/" -O data.$idstr -S
    ret=$?
    echo "http proxy ret: $line $ret"

    let id=id+1
done < $http_proxies
