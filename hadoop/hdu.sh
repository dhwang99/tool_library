
path="."
if [ $# -ge 1 ]
then
    path=$1
fi
hadoop fs -du $path | awk 'BEGIN {m="KMGT";} {c=$1/1000;i=1; while(c>1000) {c=c/1000.0; i++;} printf("%.2f%s\t%s\n", c,substr(m, i, 1),$3); t+=$1;} END {t=t/(1000*1000*1000*1000); printf("%.2fT\ttotal\n",  t);}'
