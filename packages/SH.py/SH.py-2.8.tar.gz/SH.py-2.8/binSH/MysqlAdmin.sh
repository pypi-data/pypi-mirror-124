#!/bin/sh
#coding:utf-8

### MySQL 區塊
###
###
###
### 更新
apt-get -qq update                         >> log.txt                        
apt-get -qq dist-upgrade                   >> log.txt    
## 首先安裝MySQL client 和 server ：
apt-get  -qq install mysql-client mysql-server        >> log.txt  
############################################
## [mysqld] 內文關鍵字 ############## 修改 ##
echo default-authentication-plugin=mysql_native_password  >>  /etc/mysql/mysql.conf.d/mysqld.cnf
### 第一步

## 啟動服務 ##　 Starting MySQL database server mysqld
service mysql start  　　             >> log.txt  　      
# !apt-get -qq -y install tcl
apt-get -qq -y install expect         >> log.txt  
chmod +x MySQL.sh
### root
./MySQL.sh                            >> log.txt  
### moon
mysql  -e "use mysql;CREATE USER 'moon'@'localhost' IDENTIFIED BY 'hello123';GRANT ALL PRIVILEGES ON *.* TO 'moon'@'localhost' WITH GRANT OPTION;FLUSH PRIVILEGES;"    >> log.txt  

### MysqlAdmin 區塊
###
###
###
### 網站目錄 ###/usr/share/nginx/html ### 底下目錄 改名admin  
wget -qq https://drv.tw/~login0516@gmail.com/gd/www/EXE/SH/phpMyAdmin/phpMyAdmin-4.9.1-all-languages.tar.gz      >> log.txt  
tar  zxvf phpMyAdmin-4.9.1-all-languages.tar.gz                                                                   >> log.txt  
mv -n phpMyAdmin-4.9.1-all-languages /usr/share/nginx/html/admin                                                   >> log.txt  

#### 複製檔案 ## 然後修改
cp /usr/share/nginx/html/admin/config.sample.inc.php /usr/share/nginx/html/admin/config.inc.php
echo "\$cfg['blowfish_secret'] = md5(\$srcret_string.date(\"Ymd\",time())); >>   /usr/share/nginx/html/admin/config.inc.php"
###########
###########  權限群組 ######### www-data 群組  ## nginx 群組 
###########  XP少一個S [session] ## 這是目錄
# !find /var/lib/php/ -type d -name session*  
chown root:www-data /var/lib/php/sessions
###### 安裝套件
apt-get -qq -y install php-mysqlnd 
######## systemctl restart php-fpm
service php7.2-fpm restart                            >> log.txt  
# !service --status-all
### 第三步