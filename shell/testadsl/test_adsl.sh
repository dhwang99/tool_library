
total=32
id=1
https_proxies="proxy_https.lst"

while [ $id -le $total ]
do
    idstr=`printf "%02d" $id`
    if [ $id -le 16 ]
    then
        webproxy="http://adslspider${idstr}.web.zw.vm.ted:8080"
    else
        webproxy="http://adslspider${idstr}.web.zw.vm.ted:9090"
    fi

    wget -T 3 -e "http_proxy=$webproxy" "http://www.zhihu.com/" -O data.$idstr -o log.$idstr
    ret=$?
    echo "webret: $webproxy $ret"

    let id=id+1
done

id=1
while [ $id -le $total ]
do
    idstr=`printf "%02d" $id`
    if [ $id -le 16 ]
    then
        shopproxy="http://adslspider${idstr}.shop.zw.vm.ted:8080"
    else
        shopproxy="http://adslspider${idstr}.shop.zw.ted:8080"
    fi

    wget -e "http_proxy=$shopproxy" "http://www.zhihu.com/" -O shopdata.$idstr -o shoplog.$idstr

    ret=$?
    echo "shopret: $shopproxy $ret"

    let id=id+1
done
