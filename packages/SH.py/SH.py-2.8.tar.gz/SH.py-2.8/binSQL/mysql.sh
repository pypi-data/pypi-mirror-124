#!/usr/bin/expect -f
#coding:utf-8



### chmod +x 這個檔案
### 使用方式..    打上檔名即可
### 1秒後 自動執行
set timeout 1                   
# 設定超時時間



### set timeout 下面
### 後面不可以加東西
# 接收第1個引數,作為 name
set name [lindex $argv 0 ]   
# set PassAA [ lindex $argv 1 ]     # 接收第1個引數,作為 AA
# set PassBB [ lindex $argv 2 ]     # 接收第2個引數,作為 BB

 



##### A
#spawn echo "$name">txt.sql
# spawn notepad.sh   "SHOW DATABASES;"
#     expect eof


# ##### B
# spawn notepadB.sh
#     expect "輸入密碼\r"
#     send "hello123\r"
    
#     expect eof


# ##### C
# spawn rm -rf ./txt.sql
#     expect eof

##### 
spawn showD
    expect "輸入密碼\r"
    send "hello123\r"
    
    expect eof

#####
spawn cat cat.txt
    expect eof