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

cd data;

rsync -arl  --progress  guest@106.1.1.1::data/$user/$srcfile $user/$srcfile
