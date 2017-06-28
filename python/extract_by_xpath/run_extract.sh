
jyfile="jingyan.lst.20170223"
#jyfile="zn2jy320.txt"

files=`find data5/ -name "*.html"`
#files=`find dataerr/ -name "*.html"`
#files=`find datarep/ -name "*.html"`
outdir=html_result/

rm titles
rm titles.new

for file in $files
do
    bn=`basename $file`
    size=`stat -c %s $file`
    echo "process $file start."
    if [ $size -lt 100 ]
    then
        continue
    fi
    python extract_jingyan.py $file $outdir/$bn >> titles.new
    echo "process $file end."
done

awk -F"\t" '{if (ARGIND == 1){v=$2"\t"$3"\t"$4; c[$1]=v;} else {n=split($1, a, "/"); k=a[n]; if (k in c) print $1"\t"$2"\t"c[k]}}' titles.new $jyfile > $jyfile.extracted

awk -F"\t" '{split($4, arr, ";"); for (i in arr) c[arr[i]]++;} END {for (i in c) print i}' titles.new > img.urls.new

exit

if [ $# -ge 1 ]
then
    nohup sh down_topimg.sh > img.log &
fi


cp $jyfile.extracted /search/wwwroot/knowledge/jingyan/

