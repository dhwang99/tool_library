id=1

while [ $id -le 2 ]
do
    down_date=`date +"%Y%m%d" -d "$id days ago"`
    echo $down_date
    sh get_bb.sh $down_date
    #sh get_top_lemma.sh $down_date
    let id=id+1
done

exit

dates='20160808 20160807 20160806 20160805 20160804 20160803 20160802 20160801'

for down_date in $dates
do
    #down_date=`date +"%Y%m%d" -d "$id days ago"`
    echo $down_date
    #sh get_baidu_baike.sh $down_date
    #sh get_top_lemma.sh $down_date
    let id=id+1
done
