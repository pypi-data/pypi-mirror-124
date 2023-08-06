#!/bin/bash
filename="/var/log/query.log"

echo -n "印出完整路徑 "; echo $filename
echo -n "取出路徑 "; echo ${filename%\/*}
echo -n "取出檔名 "; echo ${filename##*/}
echo -n "取出副檔名 "; echo ${filename##*.}
echo -n "去掉最後的副檔名 "; echo ${filename%.*}

# ############################
# for dir in $(ls `pwd`/Django)
# do
     
#  rm -rf /usr/bin/$dir 
# done
# #############################