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

echo "download $files for $user;"

srcfile=$files;
bsrcfile=`basename $srcfile`

if [ $# -lt 1 ]
then
        echo "please input filename";
        exit;
fi

cur_dir=`pwd`
dst_dir=$cur_dir/

serdir="/data/sogou"
middir="$serdir/data/$user"

cd shell
echo "begin down data from sogou to bj:"
sh lcmd bj "[ ! -d $middir ] && (mkdir -p $middir)"
sh lcmd bj "cd $serdir; sh down.sh -u $user -f $bsrcfile"
echo "end down data from sogou to bj."

echo "begin down data from bj to cur host:"
sh ldown bj "$middir/$bsrcfile" "$dst_dir" 
echo "end down data from bj to cur host"

echo "remove $bsrcfile from bj:"
sh lcmd bj "cd $middir; rm -f $srcfile"
echo "OK."
