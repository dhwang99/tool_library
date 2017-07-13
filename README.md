>  平时用到的一些工具、库等等集合。是一个大杂汇。叫 toolbox更合适一些

>  包括shell，python，分词，上传文件，自动登陆，远程同步等等小工具集, 也有python爬虫、抽取、同步数据等小程序

>  也包括一些hadoop,sparksql,查看gpu等相关的程序

#### 1. shell
>   1) remote_ctrl 

>     一个登陆远程机器、在远程机器批执行命令、上传/下载数据、发布程序的脚本. 

>   2) transfer

>     经中转给目标机器同步数据的程序。实际上用代理应该更好(squid支持http/https/ssh/rsync等)

>   3) testadsl

>     用nmap扫描端口，找内部adsl代理的程序。并对发现结果进行了试用

>   4) getopts.sh

>    脚本实现的 switch, 让交互更方便一些


#### 2. python 
     
>    1) extract_by_re

>        通过正则进行抽取的小脚本。用来抽sina, 学习用, 不商用

>    2) extract_by_xpath

>        通过 xpath进行抽取。 抽取几个知识类的网站，学习用

>    3) log_parse

>        用来解析日志的小程序。附加了些统计的功能

>    4) multi_search.py

>       多模匹配 + 多进程, 可以用来发现敏感词（不足：字符串匹配，未分词）

>    5) produce_consumer_for_senddata.py

>        为推送服务写的生产者、消费者model

>    6) push_data_by_httppost

>        通过http接口，提交post前的客户端和服务端程序。其中服务器端程序用php写的

>    7) seg_test.py

>        jieba分词的小示例

>    8) tcp_client.py

>        tcp客户示例

>    9) urlparse

>        解析url的程序

>    10) vr_data

>       一个离线、在线入redis的计算小程序。包括一些匹配计算、入redis、http代理访问等功能

>    11) zhihu_download.py

>       广度遍历爬取zhihu的小程序。其中的cookie用的是自己的。也是学习用

>    12) simhash.py

>      算simhash的小程序


#### 3. Hadoop相关的脚本 
>   用hadoop下的hdfs存储、mapreduce进行计算。会存一些例程序 

#### 4. sparksql相关的脚本 
>   用spark sql做数据统计。  

#### 5. gpu相关的脚本 
>   17年4月开始使用gpu, 工具不多，仅为留档用 
