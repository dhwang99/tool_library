#/bin/bash

# sh getopts.sh -u aaa -f bbb -d adf

user=""
files=""

while   getopts  :u:f:  opt
do
    case  "$opt"   in
        u)   echo  "found  the -u option,with value: $OPTARG "; user=$OPTARG ;;
        f)   echo  "found  the -f option ,with value : $OPTARG"; files=$OPTARG ;;
        *)   echo  "unknown  option : $opt"
    esac
done

echo "user:$user;"
echo "files: $files;"
