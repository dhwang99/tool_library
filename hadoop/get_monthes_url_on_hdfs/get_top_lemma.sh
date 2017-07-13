
daa="yesterday"
if [ $# -gt 0 ]
then
    daa="$1"
fi
dm=`date +%Y%m -d "$daa"`
dd=`date +%Y%m%d -d $daa`
dt=`date +%Y%m%d%H`
dt1=`date +%Y%m%d%H -d '1 hour ago'`

src="baike_data/baidu_baike.dat.${dd}"
dstfile="middata/lemma.${dd}"

grep "_搜狗"  $src |grep -v "图片_" |awk -F"\t" '{c[$2]++;} END {for (i in c) print i"\t"c[i]}' |sort -nr -k 2 -t $'\t' > $dstfile
