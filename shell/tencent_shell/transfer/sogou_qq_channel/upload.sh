#/bin/bash

user=""
files=""

while   getopts  :u:f:  opt
do
    case  "$opt"   in
        u)   user=$OPTARG ;;
        f)    files=$OPTARG ;;
        *)   echo  "unknown  option : $opt"
    esac
done

if [ "$user" = "" -o "$files" = "" ]
then
    echo -e "please input user and filename. \nusage: sh $0 -u user -f filename"
    exit 1;
fi

echo "upload $files for $user;"

srcfile=`readlink -f $files`;
bsrcfile=`basename $srcfile`
bsrcdir=`dirname $srcfile`

serdir="/data/sogou"
middir="$serdir/data/$user"

cd shell

echo "begin upload data to bj:"
sh lcmd bj "[ ! -d $middir ] && (mkdir -p $middir)"
sh lscp bj  "$srcfile" "$middir/$bsrcfile"
echo "end to bj."

echo "begin upload to sogou:"
sh lcmd bj "cd $serdir; sh upload.sh -u $user -f $bsrcfile"
echo "end down data from bj to cur host"

echo "remove $srcfile from bj:"
sh lcmd bj "cd $middir; rm -f $bsrcfile"
echo "OK."

