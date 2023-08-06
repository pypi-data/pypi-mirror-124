#!/bin/bash

## 修改 nginx配置

## 修改 Nginx 目錄
## 改變 nginx
cd  /etc/nginx/conf.d
rm -rf  ./*
rm -rf  default.conf

wget https://raw.githubusercontent.com/moon-start/SH/master/binSHHconf/default.C.conf

## 修改檔案
mv      default.C.conf   default.conf

## 下載 nginx.conf
cd ..
rm -rf  ./nginx.conf
wget https://raw.githubusercontent.com/moon-start/SH/master/binSHHconf/nginx.conf


#### PHP設定檔
rm -rf /etc/php-fpm.d/www.conf
cd /etc/php-fpm.d
wget https://raw.githubusercontent.com/moon-start/SH/master/binSHHconf/www.conf
chmod 644 /etc/php-fpm.d/www.conf
## cd ~/
## 重新
systemctl start php-fpm
systemctl restart php-fpm

nginx -t
##################################
# 避免 nginx: [error] invalid PID number "" in "/run/nginx.pid"
nginx -c /etc/nginx/nginx.conf
nginx -s reload


#安裝需要的套件
yum -y install php-xml rsyslog
systemctl start rsyslog
cls