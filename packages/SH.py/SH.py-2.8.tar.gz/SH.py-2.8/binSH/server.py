#!/usr/bin/python
#coding=utf-8　

## 安裝 ##
import os
os.system('apt-get -qq update')
##
os.system('apt-get install php7.2-fpm php7.2-mbstring php7.2-gd php7.2-json php7.2 -y')
os.system('chmod +x /etc/init.d/php7.2-fpm')
##
os.system('apt-get -qq install nginx')
#########################################
#########################################
#########################################
SS='''load_module /usr/lib/nginx/modules/ngx_stream_module.so;
# Nginx的啟用 Linux 帳戶
# user  nginx;
user www-data;
# Nginx的執行緒數量(建議為你的 CPU 核心數 x 2)
# worker_processes  2;
worker_processes auto;
# Error Log 檔的位置
# error_log  /var/log/nginx/error.log warn;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;


include /usr/share/nginx/modules/*.conf;

events {
    # 允許同一時間連線總數量
    worker_connections 1024;
}

### 自己配置stream模塊
### 需要加載 load_module /usr/lib/nginx/modules/ngx_stream_module.so;
stream {
    #upstream mysql_3306 {
    #    server 192.168.1.5:3306;
    #}
    #server {
    #    listen 3306;
    #    proxy_connect_timeout 20s;
    #    proxy_pass mysql_3306;
    #}
 
  # server {
  # listen     22; ##打開http本機的port
  # proxy_pass    ssh;

  # }
  # upstream ssh {          ## 因為ngrok(實體)coable(虛擬)Nginx只能依照實體
  #   # server 8.8.8.8:22; ## 連到ngrok網站:22               ## 對外的連結點 ##類似 ssh -NfR 2222:localhost:22 remote_ip???
  #   server 0.tcp.ngrok.io:18858;  ## 把http網止串聯起來
  #   ##59f2d8f9.ngrok.io:22
  # }


  ## https://snippetinfo.net/mobile/media/2463
  ################### 
  # server {
  #   listen 53 udp ;   #### listen 53 udp;  ### 53; 代表TCP
  #   proxy_pass DNS;
  # }

  # upstream DNS{
  #   ##server 8.8.8.8:53;
  # }

  ####################
  # server {
  #     listen 443;       #### HTTPS/443
  #     proxy_pass admin;
  # }

  # upstream admin {
  #     server admin.uim.cloud:443;
  # }
    
}


 




http {
    # 預設的 log 記錄格式
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    # Access log 檔的位置
    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

 
    include /etc/nginx/conf.d/*.conf;   ## 自己建立的 default.conf
    # include /etc/nginx/default.d/*.conf
    ####### conf.d 等同 default.d
}
'''
with open("/etc/nginx/nginx.conf","w") as f:
    f.writelines(SS)
###
SSA='''
server {
        # 連接到外部的app:2368是隨意指定的PORT
        # https://blog.hellojcc.tw/2015/12/07/nginx-beginner-tutorial/
        # 
        # server_name www.example.com;
        # location / {
        # 打開瀏覽器連到 www.example.com，就能夠連到 port 2368 的 app 了
        # proxy_pass 127.0.0.1:2368;
        # }
        # http {
        # upstream my_upstream {     ## 用途:(網名):proxy_pass http://my_upstream;
        # server 192.168.1.1:2368;
        # server 192.168.1.2:2368;
        # }

        ###### 指定它監聽 port 80
        listen       80 default_server;  ### 設成 預設端口
        listen       [::]:80 default_server;
        server_name  _;
        # 預設監聽的port為80
        # listen       80;
        # server_name  localhost;
        
         
        ## 配置Basic Auth登入認證
        auth_basic "登入認證"; 
        auth_basic_user_file /etc/nginx/conf.d/nginx-htpasswd;
        


        root         /usr/share/nginx/html;

        ##刪除這行## include /etc/nginx/default.d/*.conf;

        
        location / {
            # # ## Ngrok 會擋掉 80代理 #### 偽裝???
            # proxy_set_header X-Real-IP 35.233.193.224;  ###$remote_addr;  ### 指定本 本機端目前IP
            # proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            # proxy_set_header Host $http_host;
            # proxy_set_header X-NginX-Proxy true;
            # # ## curl http://t1.imququ.com/ 測試語法??
       


            ###設定###
            index index.php index.html;
            #########
        }

        ### 編寫新增 ###
        location ~ \.php$ {
            ########### 網頁目錄
            root        /usr/share/nginx/html;
            try_files  $uri = 404;
            ##指定路徑##
            # fastcgi_pass  unix:/run/php-fpm/www.sock;
            ############# /etc/php/7.2/fpm/pool.d/www.conf ##### www.conf
            ############# listen = /run/php/php7.2-fpm.sock
            fastcgi_pass  unix:/run/php/php7.2-fpm.sock;
            # fastcgi_pass 127.0.0.1:9000;

            fastcgi_index  index.php;
            #######################????? 不確定
            #fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_n$

            # fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param SCRIPT_FILENAME /usr/share/nginx/html$fastcgi_script_name;
            ############
            include        /etc/nginx/fastcgi_params;
        }
        ### 新增結束 ###

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }

      
}
'''
with open("/etc/nginx/conf.d/default.conf","w") as f:
    f.writelines(SSA)
##
SSB='''
<?php

phpinfo();

?>
'''
with open("/usr/share/nginx/html/index.php","w") as f:
    f.writelines(SSB)
  
  
## 啟動 ##
os.system('service php7.2-fpm start')
# os.system('service php7.2-fpm restart')
##
os.system('service nginx start')
# os.system('service nginx restart')
##
# os.system('service --status-all')
os.system('nginx -t && nginx -s reload')

## 改變~~檔案屬性~~成網頁

## 配置Basic Auth登入認證
## !htpasswd -c -d /etc/nginx/conf.d/nginx-htpasswd moon 
os.system('apt-get -qq install apache2-utils') ##  apache2-utils
os.system('touch /etc/nginx/conf.d/nginx-htpasswd # 生成檔案')
os.system('echo "moon:6unzLtlfQV2O2" > /etc/nginx/conf.d/nginx-htpasswd')
os.system('echo "root:pBU8A.J4BeuJo" >> /etc/nginx/conf.d/nginx-htpasswd')
