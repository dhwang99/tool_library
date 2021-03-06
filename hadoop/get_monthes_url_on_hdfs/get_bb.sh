
module_name=filtertask

daa="yesterday"
if [ $# -gt 0 ]
then
    daa="$1"
fi
dm=`date +%Y%m -d "$daa"`
dd=`date +%Y%m%d -d $daa`
dt=`date +%Y%m%d%H`
dt1=`date +%Y%m%d%H -d '1 hour ago'`

regstr='bk(.m)?.sg.com'
regstr='ww(.m)?.sg.com'
regstr='jy.bb.com/'
regstr='bk.bb.com/'

#/logdata/sgrank/full_hour/201605/20160503/2016050300/part*
input="/logdata/sgrank/full_hour/${dm}/${dd}/*/part*"

echo $input

hadoop fs -rmr wdh/$module_name

hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
-input $input  \
-output wdh/$module_name \
-jobconf mapred.job.name=$module_name \
-jobconf mapred.reduce.tasks=0 \
-mapper "python map_url.py \"$regstr\""  \
-file map_url.py \
-numReduceTasks 0 


tmpdir=tmpdata
dstdir=bk_data
if [ -d $tmpdir ]
then
	rm $tmpdir/part*
else
	mkdir $tmpdir 
fi

hadoop fs -get wdh/$module_name/part* $tmpdir/

cat $tmpdir/part* > $dstdir/bb_bk.dat.$dd

#awk -F"\t" '{show += $1; clk += $2;} END {print show"\t"clk;}'  $tmpdir/part* >$dstdir/bk.uniq.$dd

sh get_top_lemma.sh $dd

