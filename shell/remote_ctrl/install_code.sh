#/bin/sh

if [ $# -lt 1 ]
then
	echo "Usage: $0 modulename(such as su, sbu, gbu, rbu,...) target(such as test, abnormal, abmini)"
	exit 1
fi

modulename=$1

dsthost="10.151.135.154"

srchost="devhost_1"
srcroot="/data1/williamwang/soso_video/source/trunk/"
dstroot="/data2/source/"

middir="/tmp/"


case "$modulename" in
"content_filter")
	moduledir="relevance/content_filter/content_filter/content_filter/"
	;;

"index_selector")
	moduledir="relevance/content_filter/content_filter/index_selecter/vqq"
	;;

"index_rela")
	moduledir="relevance/video_relevance/index_rela/"
	;;

"search_rela")
	moduledir="relevance/video_relevance/search_rela"
	;;

*)
	echo "unavailable module. please check it."
	exit 2
	;;
esac

binname="${modulename}.tgz"
midfile="$middir/$binname"
if [ -f $midfile ]
then
	rm $midfile
	echo "rm $middir"
fi

#echo "$modulename:$target"
#echo $srchost $srcdir/$binname $middir
#echo $midfile $dsthost $dstdir
#exit

srcdir="$srcroot/$moduledir"
dstdir="$dstroot/$moduledir"

sh lcmd $srchost "cd $srcdir; rm $binname; tar czvf $binname *"

sh ldown $srchost $srcdir/$binname $middir
sh lscp $midfile $dsthost $dstdir  

sh lcmd $dsthost "cd $dstdir; tar xzvf $binname; make clean; make; make install"

#rm $midfile
