vr_data_matcher: 
 down2.sh, 用来进行离线标注数据制作。生成文件为未标注的 vr_match.conf
 离线数据未标注数据制作，最好放到sogou环境，效率更高

vr_match.conf 为网页VR数据和百科词条的匹配规则列表。
1. 格式
当前格式为：
百科id\t百科词\tVR检索扩展词\t类型名\t匹配规则\turl...

2,3:
   百科词+检索扩展词，构成vr请求的query

4. 类型列表
 类型名为：
   a. original: 词条的原著作品。主要针对影视
   b. starPlan: 明星行程
   c. weibo: 明星微博列表

5. 匹配规则：
   0: 默认规则。主要对结果进行完整性检查。所有数据都要求进行完整性检查，然后才能上线. 完整性只检查json数据里的通用字段
   1: url完全匹配。 即和第4列进行完全的url匹配
   2: url正则匹配。 返回文档是的url和规则正则匹配

6. 规则
   当下只有url匹配规则. 正则匹配

运行：
  运行依赖python requests库。如果没有安装，需要安装一下

  定期执行 start_vr_dumper.sh, 根据 vr_match.conf, 把VR数据同步到百科；需要对日志里的Error日志进行监控和报警
  有各种错误：如网络错误、返回数据格式错误等等；日志里记录的错误原因，可以细分
  
  start_vr_dumper_test.sh, 给测试的redis倒库
 
 redis shell:
  bin/目录下，可以直接删记录或更新记录. 示例如下：
  sh redis_online.sh "GET baiketupu_original_428478"
  key: baiketupu_original_, baiketupu_starPlan_, baiketupu_weibo_,
  命令参考 http://redisdoc.com/
  删除：


  sh redis_online.sh KEYS "baiketupu_original_*" | xargs redis_online.sh DEL
  sh redis_online.sh KEYS "baiketupu_starPlan_*" | xargs redis_online.sh DEL
  sh redis_online.sh KEYS "baiketupu_weibo_*" | xargs redis_online.sh DEL

  sh redis_test.sh KEYS "baiketupu_weibo_*" | xargs redis_test.sh DEL
  sh redis_test.sh KEYS "baiketupu_starPlan_*" | xargs redis_test.sh DEL
  sh redis_test.sh KEYS "baiketupu_original_*" | xargs redis_test.sh DEL
