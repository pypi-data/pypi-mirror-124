#!/bin/bash

## 改變 nginx
cd  /etc/nginx/conf.d
rm -rf  ./*
rm -rf  default.conf
wget https://raw.githubusercontent.com/moon-start/SH/master/binSHHconf/default.B.conf

## 修改檔案
mv      default.B.conf   default.conf
sed -i "s/專案名稱/$1/g"  default.conf



## 下載 nginx.conf (如果缺少)
cd ..
rm -rf  ./nginx.conf
wget https://raw.githubusercontent.com/moon-start/SH/master/binSHHconf/nginx.conf

nginx -t
nginx -s reload



## 改變admin