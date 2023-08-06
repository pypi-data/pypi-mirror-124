#!/usr/bin/expect -f
#coding:utf-8



### chmod +x 這個檔案
### 使用方式..    打上檔名即可
### 1秒後 自動執行
set timeout 10                   
# 設定超時時間



### set timeout 下面
### 後面不可以加東西
# 接收第1個引數,作為 name
set name [lindex $argv 0 ]   
# set PassAA [ lindex $argv 1 ]     # 接收第1個引數,作為 AA
# set PassBB [ lindex $argv 2 ]     # 接收第2個引數,作為 BB

 
# 向遠端伺服器請求開啟一個FTP會話，並等待伺服器詢問使用者名稱
spawn sql /usr/bin/$name

    expect "輸入密碼\r"
    send "hello123\r"
    
    expect eof