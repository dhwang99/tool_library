#!/bin/bash
baseDir=$(cd "$(dirname "$0")"; pwd)
runningFile=${baseDir}'/scriptrunning.txt'
if [[ ! -f $runningFile ]]
then
    echo 'hello' > $runningFile
    bakDir=${baseDir}'/bak'
#    for filename in `ls ${baseDir}/*.sign`; do
    for filename in `find ${baseDir} -name "*.sign"`; do
        newname=${filename%.*}".new"
        delname=${filename%.*}".del"
        if [[ -f $newname ]]
        then
            cp $newname $newname".next"
            #grep -v '<unick>.*</unick>' $newname > $newname".next"
            #python $baseDir'/yitao.py' $newname".next"
            python $baseDir'/sogou.py' $newname".next"
	    ${baseDir}/dh_transfer.sh $newname".next.drct.gz" $newname".next.drct"
	    mv $newname $bakDir
	    rm $newname".next"
            rm $newname".next.drct.gz"
            #rm $newname".next.filt"
            if [[ -f $newname".next.drct" ]]
            then
                #echo rm $newname".next.drct"
	        rm $newname".next.drct"
            fi
        fi
        if [[ -f $delname ]]
        then
            echo '<?xml version="1.0" encoding="utf-8"?>' > $delname".next"
            echo '<dump>' >> $delname".next"
            awk ' {print "<question><qid>"$1"</qid></question>"} ' $delname >> $delname".next"
            echo '</dump>' >> $delname".next"
            #python $baseDir'/yitao.py' $delname".next"
            python $baseDir'/sogou.py' $delname".next"
            ${baseDir}/dh_transfer.sh $delname".next.drct.gz" $delname".next.drct"
	    #echo  python $baseDir'/sogou.py' $delname".next"
            mv $delname $bakDir
            rm $delname".next" 
            #rm $delname".next.filt" 
            rm $delname".next.drct.gz"
            if [[ -f $delname".next.drct" ]]
            then
                #echo rm $delname".next.drct"
	        rm $delname".next.drct"
            fi
        fi
        mv $filename $bakDir
    done
    rm $runningFile
fi
