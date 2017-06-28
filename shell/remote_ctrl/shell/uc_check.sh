#!/bin/bash

cd ..

#for cu
cmdstr="$1.sh";

./lcmd uc "ps aux|grep uc|grep -v grep"
