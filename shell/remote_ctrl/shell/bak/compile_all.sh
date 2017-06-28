#!/bin/bash

cd ..

#for cu

mod_dir="/data/twse_spider/cu";
./lcmd cu "cd $mod_dir/proj; make clean; make"

mod_dir="/data7/source/uc";
./lcmd uc "cd $mod_dir/proj; make clean; make"

mod_dir="/data7/source/ucmain";
./lcmd uc "cd $mod_dir/proj; make clean; make"

#for fast_ucmain
mod_dir="/data1/fast_ucmain";
./lcmd cu "cd $mod_dir/proj; make clean; make"

#for fake eu
mod_dir="/data1/fast_ucmain/FakeEU";
./lcmd cu "cd $mod_dir; make clean; make"

#for extractor

mod_dir="/data1/twse_spider_extractor/cu";
./lcmd cu_3 "cd $mod_dir/proj; make clean; make"

mod_dir="/data1/fast_ucmain_extractor";
./lcmd cu_3 "cd $mod_dir/proj; make clean; make"

#for link

mod_dir="/data1/fast_ucmain_linkzhang/ucmain";
./lcmd cu_3 "cd $mod_dir/proj; make clean; make"

mod_dir="/data1/twse_spider_linkzhang/cu";
./lcmd cu_3 "cd $mod_dir/proj; make clean; make"

mod_dir="/data1/ucmain_for_link/ucmain";
./lcmd test "cd $mod_dir/proj; make clean; make"

# for spitz
mod_dir="/data1/fast_ucmain_spitz";
./lcmd cu_3 "cd $mod_dir/proj; make clean; make"

mod_dir="/data1/tvideo_spider/ucmain/";
./lcmd test "cd $mod_dir/proj; make clean; make"

mod_dir="/data1/source/uc";
./lcmd test "cd $mod_dir/proj; make clean; make"

#mod_dir="/data/twse_spider/videoeu/src/VEDIOEU";
#./lcmd cu "cd $mod_dir/project; make clean; make"
#./lcmd cu "cd $mod_dir/../../sh; cp videoeuserver ../euserver1/bin"
#./lcmd cu2 "cd $mod_dir/../../sh; cp videoeuserver ../euserver2/bin"
