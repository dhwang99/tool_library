
path="."
if [ $# -ge 1 ]
then
    path=$1
fi
hadoop fs -rmr .Trash/*
