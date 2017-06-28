#/bin/bash

user=""
files=""

host="106.120.1.1"

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

srcfile=$files;

cd data;

rsync -arlR  --progress --chmod=og+w $user/$srcfile guest@$host::data/
