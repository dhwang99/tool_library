从腾讯机房传数据给sogou

当前lufang在消息总线上拿到数据后，把数据推到 10.130.68.165 机器的 /data/wenwen/push_sogou/目录下

crontab里每一分钟会调用一次transfer.sh上传数据

分别给问问和sogou
